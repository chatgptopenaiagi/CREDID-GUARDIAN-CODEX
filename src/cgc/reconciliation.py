"""Bounded read-only evidence collection and pure reconciliation. No recovery authority."""
import copy
import hashlib
import json
import os
import re
import time

from . import inspection as ins, checkpoint as cp, publication as pub
from .cache import CacheError
from .handoff import HandoffStore, _absolute, _screen, validate_state as validate_handoff, ERRORS, FAILURES
from .preservation import _stamp, _text, NEXT, TERMINAL

SCHEMA_VERSION = 'cgc-reconciliation-v3.0-provisional'
MAX_BYTES = 256 * 1024
ERROR_CODES = ins.CODES | ERRORS | FAILURES | {'UNSAFE_CACHE', 'HANDOFF_UNAVAILABLE',
    'LOCAL_UNAVAILABLE', 'INPUT_OR_OBSERVATION_FAILED', 'CONTENT_CHANGED', 'INVALID_SELECTION',
    'SENSITIVE_OR_GENERATED_PATH', 'UNSAFE_CANDIDATE', 'CONTENT_LIMIT', 'BINARY_UNSUPPORTED',
    'SENSITIVE_CONTENT', 'REMOTE_IDENTITY_MISMATCH', 'UNSAFE_REMOTE_LAYOUT', 'REMOTE_HOOKS_UNSUPPORTED',
    'REMOTE_CONFIG_UNSUPPORTED', 'NOT_BARE_REMOTE', 'UNSAFE_CONFIG', 'REMOTE_REF_MISSING_OR_AMBIGUOUS',
    'REMOTE_REF_MISMATCH', 'SYMBOLIC_REMOTE_REF', 'SYMBOLIC_TRACKING_REF'}


class ReconciliationError(ValueError):
    def __init__(self, code='INVALID_RECONCILIATION'):
        super().__init__(code if code == 'RESOURCE_LIMIT' else 'INVALID_RECONCILIATION')


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                      separators=(',', ':'))


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def nullable(spec): return ('nullable', spec)
def array(spec, limit=64): return ('array', spec, limit)
def enum(*values): return ('enum', values)


def oid(value):
    if type(value) is not str or re.fullmatch(r'(?:[0-9a-f]{40}|[0-9a-f]{64})', value) is None:
        raise ReconciliationError()


def sha(value):
    if type(value) is not str or re.fullmatch('[0-9a-f]{64}', value) is None:
        raise ReconciliationError()


def path(value):
    if type(value) is not str:
        raise ReconciliationError()
    ins._path(value.encode())
    if any(p in ('', '.', '..') for p in value.split('/')) or value.startswith('/'):
        raise ReconciliationError()


def artifact(value):
    if type(value) is not str or not value.startswith('.git/') or not value.endswith('.lock'):
        raise ReconciliationError()
    path(value[5:])


def text(value): _text(value)

def number(value):
    if type(value) is not int or not 0 <= value <= 2**63 - 1: raise ReconciliationError()


def code(value):
    if type(value) is not str or value not in ERROR_CODES:
        raise ReconciliationError()


def check(spec, value):
    if isinstance(spec, dict):
        if type(value) is not dict or set(value) != set(spec): raise ReconciliationError()
        for key, child in spec.items(): check(child, value[key])
    elif isinstance(spec, tuple):
        if spec[0] == 'nullable':
            if value is not None: check(spec[1], value)
        elif spec[0] == 'enum':
            if type(value) is not str or value not in spec[1]: raise ReconciliationError()
        else:
            if type(value) is not list or len(value) > spec[2]: raise ReconciliationError()
            for item in value: check(spec[1], item)
    else:
        spec(value)


IDENTITY = dict.fromkeys(('device', 'inode', 'git_device', 'git_inode'), number)
ENTRY = {'path': path, 'mode': enum('100644', '100755', '120000', '160000'),
         'oid': oid, 'stage': enum('0', '1', '2', '3'), 'flag': text}
# Failed commit lookup has no invented tree/parent: represented separately below.
COMMIT = {'oid': oid, 'tree': nullable(oid), 'parents': nullable(array(oid)), 'error_code': nullable(code)}
LOCAL = {'inspection_digest': sha, 'identity': IDENTITY, 'head': nullable(oid),
         'branch': nullable(text), 'upstream': nullable(text),
         'changes': array({'path': path, 'index': enum('.', '?', '!', 'M', 'A', 'D', 'R', 'C', 'U', 'T'), 'worktree': enum('.', '?', '!', 'M', 'A', 'D', 'R', 'C', 'U', 'T')}, ins.MAX_ENTRIES),
         'operations': array(enum(*ins.OPERATIONS)), 'locks': array(artifact), 'index': array(ENTRY, ins.MAX_ENTRIES),
         'index_digest': sha, 'metadata_digest': sha, 'config_digest': sha,
         'commits': array(COMMIT, 2)}
RECEIPTS = dict.fromkeys(('local_commit', 'tracking_commit', 'remote_commit'), nullable(oid))
SLOT = {'generation': number, 'digest': sha, 'phase': enum(*sorted(set(NEXT) | TERMINAL)), 'evidence_basis': enum('SYNTHETIC', 'ADAPTER_REPORTED'),
        'requested_level': enum('HANDOFF_ONLY', 'LOCAL_CHECKPOINT', 'REMOTE_VERIFIED'),
        'receipts': RECEIPTS, 'publication_status': enum('NOT_REQUESTED', 'NOT_ATTEMPTED', 'PUSH_ATTEMPTED', 'FAILED', 'LOCAL_CHECKPOINT_ONLY', 'VERIFIED'), 'reported_safe_to_resume': enum('YES', 'NO', 'PARTIAL', 'UNKNOWN'),
        'paths': array(text), 'known_failures': array(text), 'next_exact_action': text,
        'test_result': enum('UNKNOWN', 'PASSED', 'FAILED', 'SKIPPED'),
        'test_commands': array(text), 'test_results': array(text),
        'base_identity': nullable(IDENTITY), 'base_head': nullable(oid), 'base_branch': nullable(text)}
DURABLE = {'generation': nullable(number), 'digest': nullable(sha),
           'latest_attempt': nullable({'status': enum('PUBLISHED', 'FAILED'), 'at': _stamp,
                                      'error_code': nullable(code), 'handoff_digest': nullable(sha)}),
           'last_known_good': nullable(SLOT), 'previous_known_good': nullable(SLOT), 'error_code': nullable(code)}
REMOTE_REQUEST = {'path': _absolute, 'identity': {'device': number, 'inode': number},
                  'ref': text, 'tracking_ref': text, 'expected_commit': oid}
REMOTE = {'tip': oid, 'direct': oid, 'tracking': nullable(oid), 'config_digest': sha,
          'identity': {'device': number, 'inode': number}, 'tracking_error': nullable(code)}
REVIEW_ENTRY = {'path': path, 'sha256': nullable(sha)}
REVIEW_VALUE = {'path': path, 'mode': nullable(enum('100644', '100755')), 'oid': nullable(oid)}
TEST_INPUT = {'result': enum('UNKNOWN', 'PASSED', 'FAILED', 'SKIPPED'),
              'commands': array(text), 'results': array(text), 'bound_head': nullable(oid)}
BASIS = {'project': _absolute, 'observed_at': _stamp, 'handoff': DURABLE,
         'handoff_last': nullable({'generation': nullable(number), 'digest': nullable(sha), 'error_code': nullable(code)}),
         'local_first': nullable(LOCAL), 'local_last': nullable(LOCAL), 'local_error': nullable(code),
         'remote_request': nullable(REMOTE_REQUEST), 'remote_first': nullable(REMOTE),
         'remote_last': nullable(REMOTE), 'remote_error': nullable(code),
         'review': nullable(array(REVIEW_ENTRY)), 'review_first': nullable(array(REVIEW_VALUE)),
         'review_last': nullable(array(REVIEW_VALUE)), 'review_error': nullable(code),
         'tests': nullable(TEST_INPUT), 'requested_operation': enum('OBSERVE', 'CHECKPOINT', 'PUBLISH'),
         'authority_description': nullable(text),
         'expected_commit': nullable({'parent': oid, 'tree': oid}), 'collection_error': nullable(code)}


def _validate_basis(basis):
    check(BASIS, basis)
    if _stamp(basis['observed_at']) != basis['observed_at']: raise ReconciliationError()
    if basis['project'] == '/': raise ReconciliationError()
    d = basis['handoff']
    if d['generation'] is None:
        if any(d[k] is not None for k in ('digest', 'latest_attempt', 'last_known_good', 'previous_known_good')):
            raise ReconciliationError()
    else:
        if d['digest'] is None or d['latest_attempt'] is None or not 1 <= d['generation'] <= 2**53 - 1: raise ReconciliationError()
        latest, good, previous = d['latest_attempt'], d['last_known_good'], d['previous_known_good']
        if latest['status'] == 'PUBLISHED' and (good is None or latest['error_code'] is not None or latest['handoff_digest'] != good['digest'] or good['generation'] != d['generation']): raise ReconciliationError()
        if latest['status'] == 'FAILED' and (latest['error_code'] not in FAILURES or latest['handoff_digest'] is not None): raise ReconciliationError()
        if latest['at'] != _stamp(latest['at']): raise ReconciliationError()
        if previous and (not good or previous['generation'] >= good['generation']): raise ReconciliationError()
        for slot in (d['last_known_good'], d['previous_known_good']):
            if slot and not 1 <= slot['generation'] <= d['generation']: raise ReconciliationError()
    for local in (basis['local_first'], basis['local_last']):
        if local:
            if local['index_digest'] != digest(local['index']): raise ReconciliationError()
            if local['index'] != sorted(local['index'], key=lambda v: (v['path'], v['stage'])): raise ReconciliationError()
            if len({(v['path'], v['stage']) for v in local['index']}) != len(local['index']): raise ReconciliationError()
            if any(len(v['flag']) != 1 or not v['flag'].isalpha() for v in local['index']): raise ReconciliationError()
            for commit in local['commits']:
                if (commit['error_code'] is None) != (commit['tree'] is not None and commit['parents'] is not None):
                    raise ReconciliationError()
    if basis['tests'] and basis['tests']['result'] in ('PASSED', 'FAILED') and not (basis['tests']['commands'] and basis['tests']['results']):
        raise ReconciliationError()
    if basis['review'] is not None:
        selection = {v['path']: v['sha256'] for v in basis['review']}
        if len(selection) != len(basis['review']): raise ReconciliationError()
        cp._selection(selection)
        for values in (basis['review_first'], basis['review_last']):
            if values is not None:
                if [v['path'] for v in values] != sorted(selection): raise ReconciliationError()
                for value in values:
                    absent = selection[value['path']] is None
                    if absent != (value['mode'] is None) or absent != (value['oid'] is None):
                        raise ReconciliationError()
    elif any(basis[k] is not None for k in ('review_first', 'review_last', 'review_error')):
        raise ReconciliationError()
    if basis['remote_request'] is not None:
        _remote_request(basis['remote_request'], basis['project'])
        for remote in (basis['remote_first'], basis['remote_last']):
            if remote is not None and (remote['tip'] != remote['direct'] or remote['identity'] != basis['remote_request']['identity']
                    or (remote['tracking'] is None) != (remote['tracking_error'] is not None)):
                raise ReconciliationError()
    elif any(basis[k] is not None for k in ('remote_first', 'remote_last', 'remote_error')):
        raise ReconciliationError()
    _screen(canonical(basis).encode())
    if len(canonical(basis).encode()) > MAX_BYTES: raise ReconciliationError('RESOURCE_LIMIT')


ACTIONS = {
    'TARGET': 'Confirm the target identity and failed observation before continuing.',
    'DURABLE': 'Inspect the unavailable durable handoff without altering it.',
    'MUTATION': 'Establish lock and pending-mutation facts without cleanup.',
    'CONFLICT': 'Explain the historical and current Git difference.',
    'REVIEW': 'Obtain fresh reviewed content digests for the intended work.',
    'TESTS': 'Establish the tested-state binding without automatically rerunning tests.',
    'REMOTE': 'Obtain the missing explicitly scoped remote observation.',
    'NONE': 'No action required now; external safe resume remains unverified.'}


def classify(basis):
    """Pure function of complete attributed evidence; never reads a clock or filesystem."""
    try:
        _validate_basis(basis)
        b = copy.deepcopy(basis)
        issues = []
        def issue(priority, domain, subject, freshness, reason, historical=None, current=None, action='CONFLICT'):
            issues.append(dict(priority=priority, domain=domain, subject=subject, freshness=freshness,
                               reason=reason, historical=historical, current=current, action=action))
        d, local, last = b['handoff'], b['local_first'], b['local_last']
        slot = d['last_known_good']
        fatal = b['collection_error'] or b['local_error']
        if local is None or last is None:
            fatal = fatal or 'LOCAL_UNAVAILABLE'
        elif local != last:
            fatal = 'TARGET_CHANGED'
        if fatal: issue(1, 'local', 'project', 'UNKNOWN', fatal, action='TARGET')
        if b['handoff_last'] is not None and b['handoff_last'] != {k: d[k] for k in b['handoff_last']}:
            fatal = 'TARGET_CHANGED'
            issue(1, 'handoff', 'generation', 'CONTRADICTED', fatal, {k: d[k] for k in b['handoff_last']}, b['handoff_last'], 'TARGET')
        if d['error_code']: issue(2, 'handoff', 'continuity', 'UNKNOWN', d['error_code'], action='DURABLE')
        if local:
            if slot and slot['base_identity'] is not None and slot['base_identity'] != local['identity']:
                fatal = 'PROJECT_MISMATCH'
                issue(1, 'local', 'identity', 'CONTRADICTED', fatal, slot['base_identity'], local['identity'], 'TARGET')
            for name in local['locks'] + local['operations']:
                issue(3, 'local', name, 'CURRENT', 'MUTATION_ARTIFACT', current=name, action='MUTATION')
            if slot and slot['phase'] in ('CHECKPOINTING', 'PUBLISHING'):
                issue(3, 'handoff', 'pending_intent', 'HISTORICAL', 'COMPLETION_UNPROVEN',
                      historical=slot['phase'], action='MUTATION')
            if slot:
                expected = slot['receipts']['local_commit'] or slot['base_head']
                if expected and expected != local['head']:
                    issue(4, 'checkpoint', 'HEAD', 'CONTRADICTED', 'HEAD_DIFFERS_FROM_HISTORY', expected, local['head'])
                if slot['base_branch'] is not None and slot['base_branch'] != local['branch']:
                    issue(4, 'local', 'branch', 'CONTRADICTED', 'BRANCH_DIFFERS_FROM_HISTORY', slot['base_branch'], local['branch'])
        review_status = 'UNKNOWN'
        if b['review'] is not None:
            if b['review_error']:
                review_status = 'CONTRADICTED' if b['review_error'] == 'CONTENT_CHANGED' else 'UNKNOWN'
                issue(5, 'review', 'selected_content', review_status, b['review_error'], action='REVIEW')
            elif b['review_first'] is not None and b['review_first'] == b['review_last']:
                review_status = 'CURRENT'
            else:
                fatal = 'TARGET_CHANGED'
                issue(1, 'review', 'selected_content', 'CONTRADICTED', fatal, b['review_first'], b['review_last'], 'TARGET')
        elif slot and slot['paths']:
            issue(5, 'review', 'selected_content', 'UNKNOWN', 'HISTORICAL_DIGESTS_MISSING', action='REVIEW')
        test = b['tests']
        historical_test = test['result'] if test else slot['test_result'] if slot else 'UNKNOWN'
        applicability = 'UNKNOWN'
        if test and test['bound_head'] and local and test['bound_head'] != local['head']:
            applicability = 'STALE'
            issue(5, 'tests', 'HEAD_binding', 'STALE', 'TEST_INPUT_CHANGED', test['bound_head'], local['head'], 'TESTS')
        if historical_test != 'UNKNOWN':
            issue(5, 'tests', 'applicability', applicability, 'COMPLETE_TEST_BINDING_UNAVAILABLE', action='TESTS')
        remote_status = 'NOT_QUERIED'
        r = b['remote_first']
        if b['remote_request']:
            remote_status = 'UNKNOWN'
            if b['remote_error']:
                issue(6, 'remote', 'observation', 'UNKNOWN', b['remote_error'], action='REMOTE')
            elif r is not None and r == b['remote_last']:
                remote_status = 'CURRENT'
                expected = b['remote_request']['expected_commit']
                if r['tip'] != expected:
                    issue(4, 'remote', 'expected_ref', 'CONTRADICTED', 'REMOTE_DIFFERS_FROM_EXPECTED', expected, r['tip'])
                if r['tracking'] != r['tip']:
                    issue(4, 'remote', 'tracking', 'CONTRADICTED', 'TRACKING_DIFFERS_FROM_REMOTE', r['tracking'], r['tip'])
                if slot and slot['receipts']['remote_commit'] and slot['receipts']['remote_commit'] != r['tip']:
                    issue(4, 'remote', 'historical_receipt', 'CONTRADICTED', 'REMOTE_MOVED_SINCE_RECEIPT', slot['receipts']['remote_commit'], r['tip'])
            else:
                fatal = 'TARGET_CHANGED'
                issue(1, 'remote', 'ref', 'CONTRADICTED', fatal, b['remote_first'], b['remote_last'], 'TARGET')
        relation = 'UNKNOWN'
        if local and b['expected_commit']:
            commit = next((c for c in local['commits'] if c['oid'] == local['head']), None)
            if commit and commit['error_code'] is None:
                relation = 'MATCHES_SUPPLIED_EXPECTATION' if (commit['parents'] == [b['expected_commit']['parent']]
                          and commit['tree'] == b['expected_commit']['tree']) else 'DIFFERS_FROM_SUPPLIED_EXPECTATION'
                if relation.startswith('DIFFERS'):
                    issue(4, 'checkpoint', 'structure', 'CONTRADICTED', 'COMMIT_STRUCTURE_MISMATCH', b['expected_commit'], commit)
        issues.sort(key=lambda i: (i['priority'], i['domain'], i['subject'], i['reason']))
        if len(issues) > 64: raise ReconciliationError('RESOURCE_LIMIT')
        if fatal:
            if review_status == 'CURRENT': review_status = 'UNKNOWN'
            if remote_status == 'CURRENT': remote_status = 'UNKNOWN'
            relation = 'UNKNOWN'
        result = dict(schema_version=SCHEMA_VERSION, collection_outcome='REFUSED' if fatal else 'OBSERVED',
                      evidence=b, issues=issues, checkpoint_relation=relation,
                      review_applicability=review_status, historical_test_result=historical_test,
                      test_applicability=applicability, remote_observation=remote_status,
                      process_quiescence='UNKNOWN', authority_state='NO_MUTATION_AUTHORITY',
                      claim_freshness={'durable_intent': 'HISTORICAL' if slot else 'UNKNOWN',
                        'local_git_observation': 'CURRENT' if not fatal else 'UNKNOWN',
                        'checkpoint_receipt': 'HISTORICAL' if slot and slot['receipts']['local_commit'] else 'UNKNOWN',
                        'remote_ref_observation': 'CURRENT' if remote_status == 'CURRENT' else 'UNKNOWN',
                        'test_applicability': applicability, 'reviewed_content': review_status},
                      required_observations=sorted(set(ACTIONS[i['action']] for i in issues)),
                      required_human_actions=[] if b['requested_operation'] == 'OBSERVE' else
                        ['Fresh scoped authority is required before any new ' + b['requested_operation'] + ' action.'],
                      next_exact_action=ACTIONS[issues[0]['action'] if issues else 'NONE'],
                      safe_to_resume='UNKNOWN', mutation_allowed=False, automatic_mutation_authorized=False)
        if len(canonical(result).encode()) > MAX_BYTES: raise ReconciliationError('RESOURCE_LIMIT')
        return result
    except ReconciliationError:
        raise
    except (ValueError, CacheError, TypeError, KeyError, OverflowError, RecursionError, UnicodeError):
        raise ReconciliationError() from None


def validate_result(result):
    try:
        if type(result) is not dict or type(result.get('evidence')) is not dict: raise ReconciliationError()
        expected = classify(result['evidence'])
        if canonical(result) != canonical(expected): raise ReconciliationError()
        return copy.deepcopy(expected)
    except (TypeError, ValueError, RecursionError):
        raise ReconciliationError() from None


def render_json(result): return canonical(validate_result(result))


def render_human(result):
    result = validate_result(result)
    return '\n'.join(['CREDID GUARDIAN CODEX — READ-ONLY RECONCILIATION'] +
                     [key.upper() + ': ' + canonical(value) for key, value in result.items()])


def _handoff(project, store_dir):
    empty = dict(generation=None, digest=None, latest_attempt=None, last_known_good=None,
                 previous_known_good=None, error_code=None)
    try:
        with HandoffStore(store_dir, project=project, create=False) as store:
            state = store.read()
        if state is None: return dict(empty, error_code='HANDOFF_UNAVAILABLE')
        validate_handoff(state)
        result = dict(empty, generation=state['generation'], digest=digest(state), latest_attempt=state['latest_attempt'])
        for key in ('last_known_good', 'previous_known_good'):
            slot = state[key]
            if slot is None: continue
            rec, snapshot = slot['record'], slot['inspection']['snapshot'] if slot['inspection'] else None
            result[key] = dict(generation=slot['generation'], digest=slot['digest'], phase=rec['phase'],
                evidence_basis=rec['evidence_basis'], requested_level=rec['requested_level'],
                receipts={k: rec['evidence'][k] for k in RECEIPTS}, publication_status=rec['publication_status'],
                reported_safe_to_resume=rec['safe_to_resume'], paths=rec['notes']['files_changed'],
                known_failures=rec['notes']['known_failures'], next_exact_action=rec['notes']['next_exact_action'],
                test_result=rec['project_test_status'], test_commands=rec['notes']['tests_run'], test_results=rec['notes']['test_results'],
                base_identity=snapshot['repository_identity'] if snapshot else None,
                base_head=snapshot['head'] if snapshot else None, base_branch=snapshot['branch'] if snapshot else None)
        return result
    except (OSError, CacheError, ValueError) as e:
        return dict(empty, error_code=str(e) if isinstance(e, CacheError) and re.fullmatch('[A-Z_]+', str(e)) else 'HANDOFF_UNAVAILABLE')


def _local(project, historical, now, deadline):
    observation = ins.inspect_project(project, now=now)
    if observation['status'] != 'OBSERVED': raise ins.InspectionError(observation['error_code'])
    snap = observation['snapshot']
    fd = ins._open_root(project)
    try:
        if (os.fstat(fd).st_dev, os.fstat(fd).st_ino) != (snap['repository_identity']['device'], snap['repository_identity']['inode']):
            raise ins.InspectionError('TARGET_CHANGED')
        def git(*args): return pub._git(fd, deadline, *args)
        entries = []
        for row in git('ls-files', '--stage', '-v', '-z').split(b'\0'):
            if not row: continue
            meta, name = row.split(b'\t')
            flag, mode, object_id, stage = meta.decode('ascii').split()
            entries.append(dict(path=ins._path(name), mode=mode, oid=ins._oid(object_id.encode()), stage=stage, flag=flag))
        entries.sort(key=lambda v: (v['path'], v['stage']))
        metadata = ins._scan(fd, deadline)
        config = pub._config_values(fd, deadline)
        commits = []
        for object_id in dict.fromkeys(v for v in (snap['head'], historical) if v):
            commit = dict(oid=object_id, tree=None, parents=None, error_code=None)
            try:
                if git('cat-file', '-t', object_id).strip() != b'commit': raise ins.InspectionError('MALFORMED_GIT')
                tree = ins._oid(git('rev-parse', '--verify', object_id + '^{tree}').strip())
                row = git('rev-list', '--parents', '-n', '1', object_id).decode().split()
                if not row or row[0] != object_id: raise ins.InspectionError('MALFORMED_GIT')
                for parent in row[1:]: oid(parent)
                commit.update(tree=tree, parents=row[1:])
            except ins.InspectionError as e:
                if e.code in ('TIMEOUT', 'RESOURCE_LIMIT', 'CANCELLED'): raise
                commit['error_code'] = e.code
            commits.append(commit)
        return dict(inspection_digest=observation['inspection_digest'], identity=snap['repository_identity'], head=snap['head'],
                    branch=snap['branch'], upstream=snap['upstream'],
                    changes=[{k: change[k] for k in ('path', 'index', 'worktree')} for change in snap['changes']],
                    operations=snap['operations'], locks=sorted(n for n in metadata if n.startswith('.git/') and n.endswith('.lock') and n != '.git/' + cp.LOCK),
                    index=entries, index_digest=digest(entries), metadata_digest=digest(metadata),
                    config_digest=digest({k: [v.hex() for v in values] for k, values in config.items()}), commits=commits)
    finally: os.close(fd)


def _remote_request(request, project):
    check(REMOTE_REQUEST, request)
    if len(request['path']) > 512 or request['path'] == project or request['path'].startswith(project + '/') or project.startswith(request['path'] + '/'):
        raise ReconciliationError()
    for ref, prefix in ((request['ref'], 'refs/heads/'), (request['tracking_ref'], 'refs/remotes/')):
        if not ref.startswith(prefix) or len(ref) > 192 or not re.fullmatch(r'[A-Za-z0-9_/-]+', ref) or '..' in ref or '//' in ref or ref.endswith('/'):
            raise ReconciliationError()
    if any(p in ('.git', '.codex', '.ssh', '.aws', '.azure', '.gnupg') for p in request['path'].split('/')):
        raise ReconciliationError()


def _remote(project, request, deadline):
    fd = ins._open_root(project)
    remote_fd = None
    try:
        remote_fd = pub._bare(request['path'], request['identity'], deadline)
        if pub._git(remote_fd, deadline, 'for-each-ref', '--format=%(symref)', request['ref']).strip():
            raise pub.PublicationError('SYMBOLIC_REMOTE_REF')
        if pub._git(fd, deadline, 'for-each-ref', '--format=%(symref)', request['tracking_ref']).strip():
            raise pub.PublicationError('SYMBOLIC_TRACKING_REF')
        tip = pub._live(fd, request['path'], request['ref'], deadline)
        direct = ins._oid(pub._git(remote_fd, deadline, 'rev-parse', '--verify', request['ref']).strip())
        if direct != tip: raise ins.InspectionError('TARGET_CHANGED')
        if pub._git(remote_fd, deadline, 'cat-file', '-t', tip).strip() != b'commit': raise ins.InspectionError('MALFORMED_GIT')
        tracking = None
        tracking_error = None
        try: tracking = ins._oid(pub._git(fd, deadline, 'rev-parse', '--verify', request['tracking_ref']).strip())
        except ins.InspectionError as e:
            if e.code != 'GIT_FAILED': raise
            tracking_error = e.code
        config = pub._config_values(remote_fd, deadline, bare=True)
        return dict(tip=tip, direct=direct, tracking=tracking, tracking_error=tracking_error,
                    identity=request['identity'], config_digest=digest({k: [v.hex() for v in values] for k, values in config.items()}))
    finally:
        if remote_fd is not None: os.close(remote_fd)
        os.close(fd)


def _review(project, selection, deadline, byte_budget):
    fd = ins._open_root(project)
    try:
        algorithm = pub._git(fd, deadline, 'rev-parse', '--show-object-format').decode().strip()
        if algorithm not in ('sha1', 'sha256'): raise ReconciliationError()
        values = cp._contents(fd, cp._selection(selection), algorithm, deadline, byte_budget=byte_budget)
        return [dict(path=p, mode=v[0] if v else None, oid=v[1] if v else None) for p, v in sorted(values.items())]
    finally: os.close(fd)


def _collect(project, *, store_dir, now, remote=None, review=None, tests=None,
            requested_operation='OBSERVE', authority_description=None, expected_commit=None):
    """Collect once, repeat for comparison; optional explicit local-bare read scope only.

    tests is a current caller's attributed report, optionally bound to HEAD only;
    it cannot establish complete environment/content applicability in this first engine.
    """
    _absolute(project); _absolute(os.fspath(store_dir)); _stamp(now)
    if project == '/': raise ReconciliationError()
    if remote is not None:
        _remote_request(remote, project)
        store_path = os.fspath(store_dir)
        if remote['path'] == store_path or remote['path'].startswith(store_path + '/') or store_path.startswith(remote['path'] + '/'):
            raise ReconciliationError()
    if review is not None: cp._selection(review)
    if tests is not None: check(TEST_INPUT, tests)
    check(enum('OBSERVE', 'CHECKPOINT', 'PUBLISH'), requested_operation)
    if authority_description is not None: text(authority_description)
    if expected_commit is not None: check({'parent': oid, 'tree': oid}, expected_commit)
    b = dict(project=project, observed_at=_stamp(now), handoff=_handoff(project, store_dir),
             handoff_last=None, local_first=None, local_last=None, local_error=None, remote_request=copy.deepcopy(remote),
             remote_first=None, remote_last=None, remote_error=None,
             review=[dict(path=p, sha256=v) for p, v in sorted(review.items())] if review is not None else None,
             review_first=None, review_last=None, review_error=None, tests=copy.deepcopy(tests),
             requested_operation=requested_operation, authority_description=authority_description,
             expected_commit=copy.deepcopy(expected_commit), collection_error=None)
    slot = b['handoff']['last_known_good']
    historical = (slot['receipts']['local_commit'] or slot['base_head']) if slot else None
    budget = ins._OBSERVATION_BUDGET.get()
    deadline = budget['deadline']
    byte_budget = {'remaining': cp.MAX_TOTAL_BYTES}
    try:
        for stage in ('first', 'last'):
            b['local_' + stage] = _local(project, historical, now, deadline)
            if review is not None and b['review_error'] is None:
                try: b['review_' + stage] = _review(project, review, deadline, byte_budget)
                except (ValueError, OSError) as e:
                    b['review_error'] = _error(e)
                    if stage == 'last' and b['review_error'] == 'CONTENT_CHANGED': b['collection_error'] = 'TARGET_CHANGED'
            if remote is not None and b['remote_error'] is None:
                try: b['remote_' + stage] = _remote(project, remote, deadline)
                except (ValueError, OSError) as e:
                    b['remote_error'] = _error(e)
                    if b['remote_error'] == 'TARGET_CHANGED': b['collection_error'] = 'TARGET_CHANGED'
        final_handoff = _handoff(project, store_dir)
        b['handoff_last'] = {k: final_handoff[k] for k in ('generation', 'digest', 'error_code')}
        if final_handoff != b['handoff']:
            b['collection_error'] = 'TARGET_CHANGED'
        ins._check_time(deadline)
    except KeyboardInterrupt: b['local_error'] = 'CANCELLED'
    except (OSError, ValueError) as e: b['local_error'] = _error(e)
    return b


def _error(error):
    if isinstance(error, ins.InspectionError): return error.code
    if isinstance(error, (cp.CheckpointError, pub.PublicationError)) and re.fullmatch('[A-Z_]+', str(error)): return str(error)
    return 'FILESYSTEM_ERROR' if isinstance(error, OSError) else 'INPUT_OR_OBSERVATION_FAILED'


def collect(project, **kwargs):
    with ins.observation_budget():
        return _collect(project, **kwargs)


def reconcile(project, **kwargs):
    return classify(collect(project, **kwargs))
