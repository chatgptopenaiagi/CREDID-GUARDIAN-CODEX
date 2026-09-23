"""Pure scoped proof evaluation. No recovery, observation, authority or execution."""
import copy
import json
from . import reconciliation as rc
from .verification_capture import matches

VERSION = 'cgc-safe-resume-v3.0-provisional'
POLICY = 'cgc-verifier-v3.0'
MAX_BYTES = 512 * 1024
ACTIONS = ('READ_ONLY_ANALYSIS', 'CONTINUE_EDITING', 'RUN_TESTS',
           'CREATE_CHECKPOINT', 'PUBLISH_CHECKPOINT', 'REPAIR_KNOWN_FAILURE')
LEVELS = ('HANDOFF_ONLY', 'LOCAL_CHECKPOINT', 'REMOTE_VERIFIED')
STATES = ('SATISFIED', 'UNSATISFIED', 'UNKNOWN', 'NOT_APPLICABLE')
RESOLUTIONS = ('RESOLVABLE_NOW', 'RESOLVABLE_WITH_COST', 'REQUIRES_EXTERNAL_EVIDENCE',
               'REQUIRES_HUMAN_REVIEW', 'IRREDUCIBLE_UNDER_CURRENT_SCOPE')
NON_INFLUENCE = ('OUTSIDE_REQUESTED_SCOPE', 'SUPERSEDED_BY_CURRENT_OBSERVATION',
                 'DUPLICATE_EQUIVALENT_EVIDENCE', 'SAME_PROOF_CLASS',
                 'SUBSUMED_BY_HIGHER_PRIORITY_CLAIM', 'NON_SEMANTIC_METADATA')
IDS = tuple('P'+str(i) for i in range(1, 13))


class VerificationError(ValueError):
    def __init__(self, code='INVALID_VERIFICATION'):
        super().__init__(code)


def _bounds(value, depth=0):
    if depth > 32: raise VerificationError('RESOURCE_LIMIT')
    if type(value) is dict:
        for k, v in value.items():
            if type(k) is not str: raise VerificationError()
            _bounds(k, depth+1); _bounds(v, depth+1)
    elif type(value) is list:
        # Inherited index lists retain their existing 10,000-entry bound.
        if len(value) > 10000: raise VerificationError('RESOURCE_LIMIT')
        for v in value: _bounds(v, depth+1)
    elif type(value) is str:
        if len(value) > 2048: raise VerificationError('RESOURCE_LIMIT')
    elif value is not None and type(value) not in (bool, int): raise VerificationError()


def _size(value):
    _bounds(value)
    if len(rc.canonical(value).encode()) > MAX_BYTES: raise VerificationError('RESOURCE_LIMIT')


def _boolean(v):
    if type(v) is not bool: raise VerificationError()


REQUEST = {'project': rc._absolute, 'identity': rc.nullable(rc.IDENTITY),
           'action': rc.enum(*ACTIONS), 'level': rc.enum(*LEVELS),
           'evidence_digest': rc.sha, 'policy_profile': rc.enum(POLICY),
           'test_policy': rc.enum('ACCOUNT_ONLY', 'REQUIRE_CURRENT_PASS', 'UNSPECIFIED')}
INPUT = {'request': REQUEST, 'reconciliation': rc.BASIS,
         'provenance': rc.enum('CURRENT_CAPTURE', 'IMPORTED'),
         'annotation': rc.nullable(rc.text)}
OBLIGATION = {'id': rc.enum(*IDS), 'plane': rc.enum('EVIDENCE', 'AUTHORITY'),
              'required': _boolean, 'status': rc.enum(*STATES), 'reason': rc.text,
              'evidence_refs': rc.array(rc.text), 'resolution_class': rc.nullable(rc.enum(*RESOLUTIONS))}
STEP = {'obligation': rc.enum(*IDS), 'kind': rc.enum('OBSERVATION_ACTION','HUMAN_REVIEW_ACTION','AUTHORITY_REQUEST'),
        'source': rc.text, 'scope_limit': rc.text, 'resolution_class': rc.enum(*RESOLUTIONS)}
NEXT = {'kind': rc.enum('OBSERVATION_ACTION','HUMAN_REVIEW_ACTION','AUTHORITY_REQUEST','NO_ACTION'), 'description': rc.text}
OUTPUT = {'verifier_version': rc.enum(VERSION), 'input': INPUT,
          'proof_obligations': rc.array(OBLIGATION, 12),
          'facts': {'kind': rc.enum('FACT'), 'collection_outcome': rc.enum('OBSERVED','REFUSED'),
                    'head_relationship': rc.enum('UNKNOWN','EQUAL','DIFFERENT'),
                    'historical_head': rc.nullable(rc.oid), 'current_head': rc.nullable(rc.oid),
                    'cause': rc.enum('UNKNOWN'), 'historical_test_result': rc.enum('UNKNOWN','PASSED','FAILED','SKIPPED'),
                    'test_applicability': rc.enum('UNKNOWN','STALE'),
                    'review_applicability': rc.enum('UNKNOWN','CURRENT','CONTRADICTED'),
                    'remote_observation': rc.enum('NOT_QUERIED','UNKNOWN','CURRENT'),
                    'claim_freshness': dict.fromkeys(('durable_intent','local_git_observation','checkpoint_receipt','remote_ref_observation','test_applicability','reviewed_content'), rc.enum('CURRENT','HISTORICAL','STALE','CONTRADICTED','UNKNOWN')),
                    'relationships': rc.array({'domain':rc.text,'subject':rc.text,'reason':rc.text,'freshness':rc.enum('CURRENT','HISTORICAL','STALE','CONTRADICTED','UNKNOWN'),'historical':rc.nullable(rc.text),'current':rc.nullable(rc.text)}),
                    'evidence_refs': rc.array(rc.text)},
          'blockers': rc.array(rc.enum(*IDS),12), 'unknowns': rc.array(rc.enum(*IDS),12),
          'resolution_plan': rc.array(STEP), 'safe_to_resume': rc.enum('YES','NO','UNKNOWN'),
          'decision_state': rc.enum('NO_ACTION_REQUESTED','AUTHORITY_REQUIRED','REFUSED'),
          'authority_required': _boolean, 'mutation_allowed': _boolean,
          'automatic_mutation_authorized': _boolean,
          'preconditions_for_future_action': rc.array(rc.text),
          'non_influence_reasons': rc.array({'claim':rc.enum(*IDS), 'reason':rc.enum(*NON_INFLUENCE)}),
          'next_exact_action': NEXT}


def request_for(projection, *, action='READ_ONLY_ANALYSIS', level='HANDOFF_ONLY', test_policy='ACCOUNT_ONLY'):
    """Pure convenience; expected identity/state still requires caller review."""
    p = rc.validate_result(projection)
    local = p['evidence']['local_first']
    return dict(project=p['evidence']['project'], identity=copy.deepcopy(local['identity']) if local else None,
                action=action, level=level, evidence_digest=rc.digest(p), policy_profile=POLICY, test_policy=test_policy)


def _compose(obligations):
    """Pure evidence composition. No production API accepts caller-supplied proof rows."""
    rc.check(rc.array(OBLIGATION, 12), obligations)
    if [r['id'] for r in obligations] != list(IDS): raise VerificationError()
    if any(r['plane'] != ('AUTHORITY' if r['id']=='P12' else 'EVIDENCE') for r in obligations): raise VerificationError()
    rows = [r for r in obligations if r['required'] and r['plane'] == 'EVIDENCE']
    if not rows or any(r['status'] == 'NOT_APPLICABLE' for r in rows): raise VerificationError()
    if any(r['status'] == 'UNSATISFIED' for r in rows): return 'NO'
    if any(r['status'] == 'UNKNOWN' for r in rows): return 'UNKNOWN'
    return 'YES'


SOURCES = {
 'P1': ('REQUIRES_HUMAN_REVIEW','Confirm exact project and supported observation scope.'),
 'P2': ('RESOLVABLE_NOW','Obtain coherent bounded captured observations; establish any lock ownership without deleting artifacts.'),
 'P3': ('IRREDUCIBLE_UNDER_CURRENT_SCOPE','Establish an accepted bounded writer/quiescence evidence source.'),
 'P4': ('REQUIRES_HUMAN_REVIEW','Explain pending intent using independent evidence without rewriting history.'),
 'P5': ('REQUIRES_EXTERNAL_EVIDENCE','Establish the designated checkpoint scope and base relationship.'),
 'P6': ('RESOLVABLE_NOW','Obtain explicitly scoped publication observations.'),
 'P7': ('REQUIRES_EXTERNAL_EVIDENCE','Obtain approved local-bare ref evidence.'),
 'P8': ('REQUIRES_HUMAN_REVIEW','Obtain fresh contextual review; digests alone are insufficient.'),
 'P9': ('IRREDUCIBLE_UNDER_CURRENT_SCOPE','Establish a supported complete tested-state receipt.'),
 'P10': ('RESOLVABLE_NOW','Reconcile material conflicting observations without choosing a story.'),
 'P11': ('RESOLVABLE_NOW','Establish the exact required preservation-level evidence.'),
 'P12': ('REQUIRES_HUMAN_REVIEW','Establish current scoped authority at the execution boundary.')}
REFS = {'P1': ('/request','/reconciliation/local_first/identity'),
 'P2':('/reconciliation/local_first','/reconciliation/local_last'),
 'P3':('/reconciliation/local_first/locks','/reconciliation/local_first/operations'),
 'P4':('/reconciliation/handoff',), 'P5':('/reconciliation/expected_commit','/reconciliation/local_first/commits'),
 'P6':('/reconciliation/handoff','/reconciliation/remote_first'),
 'P7':('/reconciliation/remote_request','/reconciliation/remote_first','/reconciliation/remote_last'),
 'P8':('/reconciliation/review',), 'P9':('/reconciliation/tests','/reconciliation/handoff'),
 'P10':('/reconciliation',), 'P11':('/reconciliation/handoff','/reconciliation/handoff_last'),
 'P12':('/request/action',)}


def _derive(inp):
    rc.check(INPUT, inp); _size(inp)
    b, req = inp['reconciliation'], inp['request']
    p = rc.classify(b)
    trusted = inp['provenance'] == 'CURRENT_CAPTURE'
    local, last, d = b['local_first'], b['local_last'], b['handoff']
    slot = d['last_known_good']
    analysis = req['action'] == 'READ_ONLY_ANALYSIS'
    remote_needed = req['level'] == 'REMOTE_VERIFIED' or req['action'] == 'PUBLISH_CHECKPOINT'
    checkpoint_needed = req['level'] != 'HANDOFF_ONLY' or req['action'] in ('CREATE_CHECKPOINT','PUBLISH_CHECKPOINT')
    needed = {'P1','P2','P4','P9','P10','P11'}
    if not analysis: needed |= {'P3','P8','P12'}
    if checkpoint_needed: needed.add('P5')
    if remote_needed: needed |= {'P6','P7'}
    rows = {i:dict(id=i,plane='AUTHORITY' if i=='P12' else 'EVIDENCE',required=i in needed,
                  status='UNKNOWN' if i in needed else 'NOT_APPLICABLE',
                  reason='PROOF_UNAVAILABLE' if i in needed else 'OUTSIDE_REQUESTED_SCOPE',
                  evidence_refs=list(REFS[i]),resolution_class=SOURCES[i][0] if i in needed else None) for i in IDS}
    def setp(i,status,reason):
        if i in needed:
            rows[i].update(status=status,reason=reason,resolution_class=None if status=='SATISFIED' else SOURCES[i][0])
    handoff_ok = (d['error_code'] is None and d['generation'] is not None and slot is not None
                  and b['handoff_last'] == {k:d[k] for k in ('generation','digest','error_code')})
    state_ok = p['collection_outcome'] == 'OBSERVED' and local is not None and local == last
    mismatch = (req['project'] != b['project'] or
                (local is not None and req['identity'] is not None and req['identity'] != local['identity']) or
                any(i['reason']=='PROJECT_MISMATCH' for i in p['issues']))
    if trusted:
        if mismatch: setp('P1','UNSATISFIED','PROJECT_IDENTITY_MISMATCH')
        elif local and req['identity'] is not None: setp('P1','SATISFIED','EXACT_CAPTURED_PROJECT')
        if req['evidence_digest'] != rc.digest(p): setp('P2','UNSATISFIED','EXPECTED_EVIDENCE_CHANGED')
        elif state_ok: setp('P2','SATISFIED','COHERENT_CAPTURED_OBSERVATIONS')
        if handoff_ok:
            if analysis: setp('P4','SATISFIED','ATTRIBUTED_INTENT_REPRESENTED')
            elif slot['phase'] not in ('CHECKPOINTING','PUBLISHING'): setp('P4','SATISFIED','NO_PENDING_MUTATION_INTENT')
            setp('P11','SATISFIED','CONTINUITY_READBACK_BOUND')
        if not analysis:
            if local and (local['locks'] or local['operations']):
                setp('P2','UNSATISFIED','UNRESOLVED_MUTATION_ARTIFACT')
                rows['P2']['resolution_class']='REQUIRES_HUMAN_REVIEW'
            # Projection does not carry complete adapter policy or writer coverage.
            if rows['P2']['status']=='SATISFIED': setp('P2','UNKNOWN','ADAPTER_POLICY_COVERAGE_INCOMPLETE')
        if analysis and req['test_policy']=='ACCOUNT_ONLY': setp('P9','SATISFIED','HISTORICAL_TESTS_ACCOUNTED_WITH_LIMITS')
        elif req['test_policy']=='REQUIRE_CURRENT_PASS' and p['test_applicability']=='STALE':
            setp('P9','UNSATISFIED','REQUIRED_TEST_BINDING_STALE')
            rows['P9']['resolution_class']='RESOLVABLE_WITH_COST'
        # Historical HEAD mismatch is preserved and material, not attributed to a cause.
        relevant = [i for i in p['issues'] if i['freshness']=='CONTRADICTED'
                    and (i['domain'] not in ('remote','review') or (i['domain']=='remote' and remote_needed) or not analysis)]
        if state_ok and not relevant: setp('P10','SATISFIED','NO_MATERIAL_CAPTURED_CONTRADICTION')
        if remote_needed:
            if p['remote_observation']=='CURRENT':
                setp('P6','SATISFIED','HISTORICAL_AND_CURRENT_REMOTE_SEPARATE')
                r, rr = b['remote_first'], b['remote_request']
                compared = (r['tip'], r['direct'], r['tracking'], local['head'] if local else None)
                if any(value is not None and value != rr['expected_commit'] for value in compared):
                    setp('P7','UNSATISFIED','REMOTE_REQUIRED_REFS_DIFFER')
                    rows['P7']['resolution_class']='REQUIRES_HUMAN_REVIEW'
                elif all(value is not None for value in compared):
                    setp('P7','SATISFIED','REMOTE_REFS_EQUAL')
                else:
                    setp('P7','UNKNOWN','REMOTE_COMPARISON_INCOMPLETE')
        # Higher-level saved-scope proof is not fabricated from a commit or an expected tree.
        if checkpoint_needed: setp('P5','UNKNOWN','CHECKPOINT_SAVED_SCOPE_UNPROVEN')
        if req['level']!='HANDOFF_ONLY':
            setp('P11','UNSATISFIED' if rows['P7']['status']=='UNSATISFIED' else 'UNKNOWN','HIGHER_PRESERVATION_PROOF_INCOMPLETE')
    else:
        for i in needed - {'P12'}:
            rows[i].update(reason='CURRENT_PROVENANCE_UNAVAILABLE',resolution_class='REQUIRES_EXTERNAL_EVIDENCE')
    if req['action']=='REPAIR_KNOWN_FAILURE': setp('P2','UNKNOWN','UNSUPPORTED_ACTION_PROFILE')
    ordered = [rows[i] for i in IDS]
    verdict = _compose(ordered)
    def priority(i):
        reason = rows[i]['reason']
        if i=='P1' or reason in ('CURRENT_PROVENANCE_UNAVAILABLE','EXPECTED_EVIDENCE_CHANGED','UNSUPPORTED_ACTION_PROFILE'): return (1, IDS.index(i))
        if i=='P11' and not handoff_ok: return (2, 0)
        if reason=='UNRESOLVED_MUTATION_ARTIFACT': return (3, 0)
        if i in ('P3','P4'): return (3, IDS.index(i))
        if i in ('P2','P5','P10'): return (4, IDS.index(i))
        if i in ('P7','P11') and rows[i]['status']=='UNSATISFIED': return (4, IDS.index(i))
        if i in ('P8','P9'): return (5, IDS.index(i))
        if i=='P12': return (7, 0)
        return (6, IDS.index(i))
    blockers = sorted((i for i in IDS if rows[i]['required'] and rows[i]['status'] in ('UNKNOWN','UNSATISFIED')), key=priority)
    plan = [dict(obligation=i,kind='AUTHORITY_REQUEST' if i=='P12' else
                 'HUMAN_REVIEW_ACTION' if rows[i]['resolution_class']=='REQUIRES_HUMAN_REVIEW' else 'OBSERVATION_ACTION',
                 source='Obtain current trusted collector provenance.' if rows[i]['reason']=='CURRENT_PROVENANCE_UNAVAILABLE' else SOURCES[i][1],
                 scope_limit='Evidence work only; no automatic execution or mutation.',resolution_class=rows[i]['resolution_class']) for i in blockers]
    historical = (slot['receipts']['local_commit'] or slot['base_head']) if slot else None
    current = local['head'] if local else None
    facts = dict(kind='FACT',collection_outcome=p['collection_outcome'],historical_head=historical,current_head=current,
                 head_relationship='UNKNOWN' if historical is None or current is None else 'EQUAL' if historical==current else 'DIFFERENT',
                 cause='UNKNOWN',historical_test_result=p['historical_test_result'],test_applicability=p['test_applicability'],
                 review_applicability=p['review_applicability'],remote_observation=p['remote_observation'],
                 claim_freshness=p['claim_freshness'],
                 relationships=[{k:i[k] for k in ('domain','subject','reason','freshness')} |
                   {k:rc.canonical(i[k]) if i[k] is not None else None for k in ('historical','current')} for i in p['issues']],
                 evidence_refs=['/reconciliation/handoff','/reconciliation/local_first','/reconciliation/tests','/reconciliation/review','/reconciliation/remote_first'])
    out = dict(verifier_version=VERSION,input=copy.deepcopy(inp),proof_obligations=ordered,facts=facts,
               blockers=blockers,unknowns=[i for i in IDS if rows[i]['required'] and rows[i]['status']=='UNKNOWN'],
               resolution_plan=plan,safe_to_resume=verdict,
               decision_state='REFUSED' if verdict=='NO' else 'NO_ACTION_REQUESTED' if analysis else 'AUTHORITY_REQUIRED',
               authority_required=not analysis,mutation_allowed=False,automatic_mutation_authorized=False,
               preconditions_for_future_action=['No repository action is authorized by this result. Recollect and revalidate scope/state/authority at use.'],
               non_influence_reasons=[dict(claim=i,reason='OUTSIDE_REQUESTED_SCOPE') for i in IDS if i not in needed],
               next_exact_action=dict(kind=plan[0]['kind'],description=plan[0]['source']) if plan else
                   dict(kind='NO_ACTION',description='No further action for analysis of this captured evidence.'))
    rc.check(OUTPUT,out); _size(out)
    return out


def verify(projection, request, *, capture=None, annotation=None):
    """Pure. A serialized provenance claim is never an argument or authority token."""
    try:
        _size({'projection':projection,'request':request,'annotation':annotation})
        p = rc.validate_result(projection)
        return _derive(dict(request=copy.deepcopy(request),reconciliation=p['evidence'],
                            provenance='CURRENT_CAPTURE' if matches(capture,p) else 'IMPORTED',annotation=annotation))
    except VerificationError: raise
    except (ValueError, TypeError, KeyError, RecursionError, OverflowError): raise VerificationError() from None


def validate_result(result, *, capture=None):
    try:
        _size(result); rc.check(OUTPUT,result)
        inp=result['input']
        expected=verify(rc.classify(inp['reconciliation']),inp['request'],capture=capture,annotation=inp['annotation'])
        if rc.canonical(expected)!=rc.canonical(result): raise VerificationError()
        return expected
    except VerificationError: raise
    except (ValueError,TypeError,KeyError,RecursionError,OverflowError): raise VerificationError() from None


def render_json(result, *, capture=None): return rc.canonical(validate_result(result,capture=capture))


def render_human(result, *, capture=None):
    value=validate_result(result,capture=capture)
    return ('CREDID GUARDIAN CODEX — SCOPED EVIDENCE VERIFICATION\n'
            'YES, if reported, is only for the exact captured-analysis scope. No repository mutation is authorized.\n'
            'Process quiescence is not proven. Editing, tests, checkpointing and publication are not authorized.\n'
            + rc.canonical(value))


def parse_json(data, *, capture=None):
    if type(data) is not str or len(data.encode())>MAX_BYTES: raise VerificationError('RESOURCE_LIMIT')
    def pairs(items):
        d={}
        for k,v in items:
            if k in d: raise VerificationError()
            d[k]=v
        return d
    try: return validate_result(json.loads(data,object_pairs_hook=pairs),capture=capture)
    except (ValueError,TypeError,RecursionError): raise VerificationError() from None


def schema_leaves(spec, prefix=''):
    if isinstance(spec,dict):
        return {p for k,v in spec.items() for p in schema_leaves(v,prefix+'/'+k)}
    if isinstance(spec,tuple) and spec[0]=='nullable': return schema_leaves(spec[1],prefix)
    if isinstance(spec,tuple) and spec[0]=='array': return schema_leaves(spec[1],prefix+'/*')
    return {prefix}
