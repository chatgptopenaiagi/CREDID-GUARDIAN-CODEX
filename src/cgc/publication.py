"""Explicit publication to an approved local bare repository; no network transport.

Current caller approval is separate from all stored evidence. No force, branch
creation, repair, rollback, test execution, automatic trigger or safe-resume claim.
"""
import copy
import json
import os
from pathlib import Path
import re
import stat
import time

from . import checkpoint as cp
from . import inspection as ins
from .cache import CacheError
from .handoff import HandoffStore, _absolute, _screen
from .preservation import advance, validate_record

TOTAL_SECONDS = 60
FLAGS = ['-c', 'protocol.allow=never', '-c', 'protocol.file.allow=always',
         '-c', 'maintenance.auto=false', '-c', 'gc.auto=0',
         '-c', 'core.excludesFile=/dev/null', '-c', 'core.attributesFile=/dev/null']


class PublicationError(ValueError):
    pass


def _fail(code):
    raise PublicationError(code)


def _identity(value, keys):
    if (type(value) is not dict or set(value) != set(keys)
            or any(type(n) is not int or n < 0 for n in value.values())):
        _fail('INVALID_IDENTITY')
    return copy.deepcopy(value)


def _git(fd, deadline, *args):
    return ins._run(FLAGS + list(args), cwd=f'/proc/self/fd/{fd}',
                    pass_fds=(fd,), deadline=deadline)


def _config_values(fd, deadline, *, bare=False):
    """Read a bounded explicit config, without includes or repository discovery."""
    parent = fd if bare else os.open('.git', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
    configfd = None
    try:
        configfd = os.open('config', os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
        st = os.fstat(configfd)
        if not stat.S_ISREG(st.st_mode) or st.st_size > ins.MAX_CONFIG_BYTES:
            _fail('UNSAFE_CONFIG')
        data = ins._run(['config', '--no-includes', '--file', f'/proc/self/fd/{configfd}', '--null', '--list'],
                        cwd='/', pass_fds=(configfd,), deadline=deadline)
        values = {}
        for row in data.split(b'\0'):
            if row:
                key, sep, value = row.partition(b'\n')
                if not sep:
                    _fail('UNSAFE_CONFIG')
                values.setdefault(key.decode('utf-8'), []).append(value)
        return values
    finally:
        if configfd is not None: os.close(configfd)
        if not bare: os.close(parent)


def _bare(path, identity, deadline):
    fd = ins._open_root(path)
    try:
        st = os.fstat(fd)
        if identity != {'device': st.st_dev, 'inode': st.st_ino}:
            _fail('REMOTE_IDENTITY_MISMATCH')
        entries = ins._scan(fd, deadline)
        forbidden = {'objects/info/alternates', 'objects/info/http-alternates',
                     'info/grafts', 'commondir', 'shallow'}
        for name, metadata in entries.items():
            if (metadata == 'NESTED_BOUNDARY' or name == '.git' or name in forbidden
                    or name.endswith(('.lock', '.promisor')) or stat.S_ISLNK(metadata[2])):
                _fail('UNSAFE_REMOTE_LAYOUT')
            if name.startswith('hooks/') and not name.endswith('.sample') and metadata[2] & 0o111:
                _fail('REMOTE_HOOKS_UNSUPPORTED')
        config = _config_values(fd, deadline, bare=True)
        allowed = {'core.repositoryformatversion', 'core.filemode', 'core.bare',
                   'core.logallrefupdates', 'extensions.objectformat'}
        if (not set(config) <= allowed or config.get('core.bare') != [b'true']
                or any(len(v) != 1 for v in config.values())):
            _fail('REMOTE_CONFIG_UNSUPPORTED')
        if _git(fd, deadline, 'rev-parse', '--is-bare-repository').strip() != b'true':
            _fail('NOT_BARE_REMOTE')
        return fd
    except BaseException:
        os.close(fd)
        raise


def _source(project, identity, head, branch, remote_name, remote_path, now, fd, deadline):
    observation = cp._snapshot(project, now, head, branch)
    snap = observation['snapshot']
    if snap['repository_identity'] != identity:
        _fail('SOURCE_IDENTITY_MISMATCH')
    if snap['changes']:
        _fail('DIRTY_SOURCE')
    cp._policy(fd, deadline)
    config = _config_values(fd, deadline)
    prefix = 'remote.' + remote_name + '.'
    if config.get(prefix + 'url') != [remote_path.encode()]:
        _fail('REMOTE_CONFIG_MISMATCH')
    if config.get(prefix + 'pushurl', [remote_path.encode()]) != [remote_path.encode()]:
        _fail('REMOTE_CONFIG_MISMATCH')
    if _git(fd, deadline, 'cat-file', '-t', head).strip() != b'commit':
        _fail('NOT_COMMIT')
    return observation


def _live(fd, remote_path, ref, deadline):
    data = _git(fd, deadline, 'ls-remote', '--refs', '--', remote_path, ref)
    rows = data.splitlines()
    if len(rows) != 1:
        _fail('REMOTE_REF_MISSING_OR_AMBIGUOUS')
    oid, sep, name = rows[0].partition(b'\t')
    if not sep or name != ref.encode():
        _fail('REMOTE_REF_MISMATCH')
    return ins._oid(oid)


def publish(project, *, source_identity, expected_head, branch, remote_name,
            remote_path, remote_identity, expected_remote, publication_reviewed,
            history_reviewed, record, store_dir, now):
    """One approved existing-branch publication; only explicit local paths accepted.

Approval attests review of the entire reachable history at expected_head for this
specific destination. No serialized record, config or credential confers authority.
"""
    result = {'publication_status': 'NOT_ATTEMPTED', 'error_code': None,
              'local_commit': None, 'remote_before': None, 'remote_commit': None,
              'tracking_commit': None, 'publication_attempted': False, 'ref_update_succeeded': False,
              'handoff_saved': False, 'preservation_outcome': 'REFUSED',
              'safe_to_resume': 'UNKNOWN', 'verification_method': 'NOT_PERFORMED',
              'publication_method': 'LOCAL_BARE_OBJECT_TRANSFER_REF_CAS'}
    fd = remote_fd = None
    pending = observation = store = None
    deadline = time.monotonic() + TOTAL_SECONDS
    try:
        if publication_reviewed is not True or history_reviewed is not True:
            _fail('CURRENT_PUBLICATION_AUTHORITY_REQUIRED')
        source_identity = _identity(source_identity, ('device', 'inode', 'git_device', 'git_inode'))
        remote_identity = _identity(remote_identity, ('device', 'inode'))
        for oid in (expected_head, expected_remote):
            if type(oid) is not str or not re.fullmatch(r'(?:[0-9a-f]{40}|[0-9a-f]{64})', oid):
                _fail('INVALID_EXPECTED_COMMIT')
        if (type(remote_name) is not str or not re.fullmatch('[A-Za-z0-9_-]{1,64}', remote_name)
                or type(branch) is not str or not re.fullmatch('[A-Za-z0-9_-][A-Za-z0-9_/-]{0,127}', branch)
                or '..' in branch or '//' in branch or branch.endswith('/')):
            _fail('INVALID_REF')
        remote_path = _absolute(remote_path)
        store_dir = _absolute(store_dir)
        project = _absolute(project)
        if len(remote_path) > 512:
            _fail('REMOTE_PATH_LIMIT')
        paths = [Path(project), Path(remote_path), Path(store_dir)]
        if any(a == b or a in b.parents or b in a.parents
               for i, a in enumerate(paths) for b in paths[i+1:]):
            _fail('OVERLAPPING_PATHS')
        if any(p in {'.git', '.codex', '.ssh', '.aws', '.azure', '.gnupg'} for p in paths[1].parts):
            _fail('PROTECTED_REMOTE_PATH')
        _screen(json.dumps([project, remote_path, store_dir, branch, remote_name]).encode())
        record = validate_record(record)
        if (record['project_request'] != project or record['trigger'] != 'MANUAL'
                or record['phase'] != 'DOCUMENTING' or record['requested_level'] != 'REMOTE_VERIFIED'
                or any(record['evidence'].values())):
            _fail('INVALID_CURRENT_RECORD')
        fd = ins._open_root(project)
        ref = 'refs/heads/' + branch
        tracking = 'refs/remotes/' + remote_name + '/' + branch
        _source(project, source_identity, expected_head, branch, remote_name,
                remote_path, now, fd, deadline)
        with cp._writer(fd):
            observation = _source(project, source_identity, expected_head, branch, remote_name,
                                  remote_path, now, fd, deadline)
            result['local_commit'] = expected_head
            result['preservation_outcome'] = 'LOCAL_CHECKPOINT_ONLY'
            remote_fd = _bare(remote_path, remote_identity, deadline)
            before = _live(fd, remote_path, ref, deadline)
            result['remote_before'] = before
            if before != expected_remote:
                _fail('REMOTE_MOVED')
            # No missing-ref creation, fetching unknown ancestry, or force permission.
            if _git(remote_fd, deadline, 'for-each-ref', '--format=%(symref)', ref).strip():
                _fail('SYMBOLIC_REMOTE_REF')
            if _git(remote_fd, deadline, 'cat-file', '-t', before).strip() != b'commit':
                _fail('NOT_COMMIT')
            current_tracking = ins._oid(_git(fd, deadline, 'rev-parse', '--verify', tracking).strip())
            if _git(fd, deadline, 'for-each-ref', '--format=%(symref)', tracking).strip():
                _fail('SYMBOLIC_TRACKING_REF')
            try:
                _git(fd, deadline, 'merge-base', '--is-ancestor', current_tracking, before)
                _git(fd, deadline, 'merge-base', '--is-ancestor', before, expected_head)
            except ins.InspectionError:
                _fail('NON_FORWARD_OR_UNKNOWN_ANCESTRY')
            context = json.dumps({'publication_intent': 'LOCAL_BARE_FORWARD_CAS',
                                  'source_identity': source_identity, 'remote_identity': remote_identity,
                                  'remote_path': remote_path, 'remote_ref': ref, 'tracking_ref': tracking,
                                  'expected_remote': before, 'expected_head': expected_head}, sort_keys=True)
            pending = advance(record, 'CHECKPOINTING', now=now,
                              evidence={'inspection_digest': observation['inspection_digest'],
                                        'local_commit': expected_head})
            pending = advance(pending, 'PUBLISHING', now=now,
                              notes={'decisions': record['notes']['decisions'] + [context]})
            with HandoffStore(store_dir, project=project, create=True) as store, store.writer():
                store.publish(pending, now=now, inspection=observation)
                try:
                    _source(project, source_identity, expected_head, branch, remote_name,
                            remote_path, now, fd, deadline)
                    check = _bare(remote_path, remote_identity, deadline); os.close(check)
                    if (_live(fd, remote_path, ref, deadline) != before
                            or ins._oid(_git(fd, deadline, 'rev-parse', '--verify', tracking).strip()) != current_tracking):
                        _fail('REMOTE_OR_TRACKING_MOVED')
                    if before != expected_head:
                        result.update(publication_attempted=True, publication_status='ATTEMPTED')
                        # Transfer approved history without creating/updating any ref.
                        _git(remote_fd, deadline, 'fetch', '--no-tags', '--no-write-fetch-head',
                             '--no-auto-maintenance', '--no-recurse-submodules', '--refmap=',
                             '--', project, expected_head)
                        _source(project, source_identity, expected_head, branch, remote_name,
                                remote_path, now, fd, deadline)
                        check = _bare(remote_path, remote_identity, deadline); os.close(check)
                        # Exact nonzero old tip makes branch disappearance/movement fail.
                        # The ancestor check above forbids a history rewind even when the
                        # current caller is otherwise authorized. No force option exists.
                        _git(remote_fd, deadline, 'update-ref', '--no-deref', ref, expected_head, before)
                        result.update(ref_update_succeeded=True, publication_status='PUBLISHED_UNVERIFIED')
                    # Fetch objects without mapping refs. Verify the remote before a
                    # forward-only, compare-and-swap update of the approved tracking ref.
                    _source(project, source_identity, expected_head, branch, remote_name,
                            remote_path, now, fd, deadline)
                    if _git(fd, deadline, 'for-each-ref', '--format=%(symref)', tracking).strip():
                        _fail('SYMBOLIC_TRACKING_REF')
                    check = _bare(remote_path, remote_identity, deadline); os.close(check)
                    _git(fd, deadline, 'fetch', '--no-tags', '--no-write-fetch-head',
                         '--no-auto-maintenance', '--no-recurse-submodules', '--refmap=',
                         '--', remote_path, ref)
                    result['remote_commit'] = _live(fd, remote_path, ref, deadline)
                    direct = ins._oid(_git(remote_fd, deadline, 'rev-parse', '--verify', ref).strip())
                    if result['remote_commit'] != expected_head or direct != expected_head:
                        _fail('VERIFICATION_MISMATCH')
                    _git(fd, deadline, 'update-ref', '--no-deref', tracking,
                         result['remote_commit'], current_tracking)
                    result['tracking_commit'] = ins._oid(_git(fd, deadline, 'rev-parse', '--verify', tracking).strip())
                    result['remote_commit'] = _live(fd, remote_path, ref, deadline)
                    _source(project, source_identity, expected_head, branch, remote_name,
                            remote_path, now, fd, deadline)
                    check = _bare(remote_path, remote_identity, deadline); os.close(check)
                    if not expected_head == result['tracking_commit'] == result['remote_commit'] == direct:
                        _fail('VERIFICATION_MISMATCH')
                    result.update(publication_status='VERIFIED',
                                  verification_method='FETCH_TRACKING_LS_REMOTE_DIRECT_BARE_REF')
                    final = advance(pending, 'VERIFYING', now=now,
                                    evidence={'push_attempted': False,
                                              'tracking_commit': result['tracking_commit'],
                                              'remote_commit': result['remote_commit']})
                    final = advance(final, 'PARTIAL', now=now,
                                    notes={'important_discoveries': record['notes']['important_discoveries'] +
                                           ['Publication VERIFIED by fresh fetch, tracking read, ls-remote and direct bare-ref read; safe resume remains unverified.']})
                    store.publish(final, now=now, inspection=observation)
                    result.update(handoff_saved=True, preservation_outcome='REMOTE_VERIFIED')
                except (ValueError, OSError, CacheError, KeyboardInterrupt) as error:
                    # Keep both the pending local receipt and prior good continuity.
                    # Do not publish another good slot that would evict prior evidence.
                    try:
                        store.record_failure('CANCELLED' if isinstance(error, KeyboardInterrupt)
                                             else 'VERIFICATION_FAILED', now=now)
                    except (ValueError, OSError, CacheError):
                        pass
                    raise
    except PublicationError as error:
        result['error_code'] = str(error)
    except (cp.CheckpointError, ins.InspectionError) as error:
        result['error_code'] = str(error)
    except KeyboardInterrupt:
        result['error_code'] = 'CANCELLED'
    except (ValueError, OSError, CacheError):
        result['error_code'] = 'PUBLICATION_IO_OR_INPUT_FAILED'
    finally:
        if remote_fd is not None: os.close(remote_fd)
        if fd is not None: os.close(fd)
    if result['error_code']:
        if result['publication_status'] == 'ATTEMPTED':
            result['publication_status'] = 'PUBLICATION_UNCERTAIN'
        elif result['publication_status'] == 'NOT_ATTEMPTED':
            result['publication_status'] = 'REFUSED'
        if result['publication_status'] == 'VERIFIED':
            result['preservation_outcome'] = 'PARTIAL'
    return result
