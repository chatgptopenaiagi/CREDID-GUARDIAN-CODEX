"""Explicit manual local checkpoints for quiescent, owner-controlled POSIX targets.

No quota authority, shell, test execution, push, rollback or preservation CLI.
The caller attests current project-policy approval; saved notes never grant it.
"""
from contextlib import contextmanager
import copy
import fcntl
import hashlib
import os
import re
import stat
import time

from . import inspection as ins
from .cache import CacheError, _safe_file
from .handoff import HandoffStore, _screen
from .preservation import advance, validate_record

MAX_PATHS = 64
MAX_FILE_BYTES = 1024 * 1024
MAX_TOTAL_BYTES = 4 * 1024 * 1024
TOTAL_SECONDS = 60
LOCK = 'cgc-checkpoint.lock'


class CheckpointError(ValueError):
    """Fixed errors only; never include content or subprocess diagnostics."""


def _fail(code):
    raise CheckpointError(code)


def _selection(selected):
    if type(selected) is not dict or not 1 <= len(selected) <= MAX_PATHS:
        _fail('INVALID_SELECTION')
    result = copy.deepcopy(selected)
    for path, digest in result.items():
        if (type(path) is not str or len(path) > 2048 or path.startswith('/')
                or any(ord(c) < 32 or ord(c) == 127 for c in path)
                or any(p in ('', '.', '..') for p in path.split('/'))):
            _fail('INVALID_SELECTION')
        parts = path.lower().split('/')
        forbidden = {'.git', '.codex', '.ssh', '.aws', '.azure', '.gnupg',
                     'node_modules', '__pycache__', '.venv', 'venv', 'build', 'dist',
                     'credentials', 'auth.json', 'id_rsa', 'id_ed25519'}
        if (any(p in forbidden or p.startswith('.env') for p in parts)
                or re.search(r'(?:secret|password|token|credential)', parts[-1])
                or re.search(r'\.(?:pem|key|p12|pfx|zip|tar|gz|7z|db|sqlite3?|bin|pt|pth|safetensors|gguf)$', path.lower())):
            _fail('SENSITIVE_OR_GENERATED_PATH')
        if digest is not None and (type(digest) is not str or not re.fullmatch('[0-9a-f]{64}', digest)):
            _fail('INVALID_SELECTION')
        _screen(path.encode())
    return result


def _snapshot(project, now, expected_head, branch):
    observation = ins.inspect_project(project, now=now)
    if observation['status'] != 'OBSERVED':
        if observation['error_code'] == 'CANCELLED':
            raise KeyboardInterrupt
        _fail('INSPECTION_REFUSED')
    snap = observation['snapshot']
    if snap['head'] != expected_head or snap['branch'] != branch:
        _fail('TARGET_CHANGED')
    if (snap['detached'] or snap['operations'] or snap['submodules']
            or snap['nested_repositories'] or snap['linked_worktrees_present']
            or snap['hidden_index_paths'] or any(c['conflict'] for c in snap['changes'])):
        _fail('UNSAFE_GIT_STATE')
    return observation


def _policy(rootfd, deadline):
    entries = ins._scan(rootfd, deadline)
    if any(n.endswith('/.gitattributes') or n == '.gitattributes'
           or n == '.git/info/attributes' for n in entries):
        _fail('ATTRIBUTES_UNSUPPORTED')
    for name, metadata in entries.items():
        if name.startswith('.git/hooks/') and not name.endswith('.sample'):
            if metadata[2] & 0o111:
                _fail('HOOKS_REQUIRE_SEPARATE_POLICY')
    if any(n.startswith('.git/') and n.endswith('.lock') and n != '.git/' + LOCK for n in entries):
        _fail('GIT_LOCK_PRESENT')


@contextmanager
def _writer(rootfd):
    gitfd = os.open('.git', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=rootfd)
    lockfd = None
    try:
        lockfd = os.open(LOCK, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK,
                         0o600, dir_fd=gitfd)
        _safe_file(lockfd)
        try:
            fcntl.flock(lockfd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            _fail('WRITER_BUSY')
        yield
    finally:
        if lockfd is not None:
            os.close(lockfd)
        os.close(gitfd)


def _contents(rootfd, selected, algorithm, deadline, *, byte_budget=None):
    """Read only approved candidate files, no-follow; return exact Git blob identities."""
    blobs = {}
    total = 0
    for path, approved in sorted(selected.items()):
        ins._check_time(deadline)
        fd = os.dup(rootfd)
        try:
            parts = path.split('/')
            for part in parts[:-1]:
                new = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                os.close(fd); fd = new
            try:
                filefd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
            except FileNotFoundError:
                if approved is not None:
                    _fail('CONTENT_CHANGED')
                blobs[path] = None
                continue
            with os.fdopen(filefd, 'rb') as stream:
                before = os.fstat(stream.fileno())
                if approved is None:
                    _fail('CONTENT_CHANGED')
                if (not stat.S_ISREG(before.st_mode) or before.st_uid != os.getuid()
                        or before.st_nlink != 1 or before.st_mode & 0o022):
                    _fail('UNSAFE_CANDIDATE')
                if before.st_size > MAX_FILE_BYTES:
                    _fail('CONTENT_LIMIT')
                limit = MAX_FILE_BYTES
                if byte_budget is not None:
                    limit = min(limit, byte_budget['remaining'])
                data = stream.read(limit + 1)
                if byte_budget is not None:
                    if len(data) > byte_budget['remaining']:
                        _fail('CONTENT_LIMIT')
                    byte_budget['remaining'] -= len(data)
                if ins._fingerprint(before) != ins._fingerprint(os.fstat(stream.fileno())):
                    _fail('CONTENT_CHANGED')
            total += len(data)
            if len(data) > MAX_FILE_BYTES or total > MAX_TOTAL_BYTES:
                _fail('CONTENT_LIMIT')
            if approved is None or hashlib.sha256(data).hexdigest() != approved:
                _fail('CONTENT_CHANGED')
            try:
                text = data.decode('utf-8')
            except UnicodeError:
                _fail('BINARY_UNSUPPORTED')
            if any(ord(c) < 32 and c not in '\n\r\t' for c in text):
                _fail('BINARY_UNSUPPORTED')
            _screen(data)
            # Also refuse obvious assignments; never output matching data.
            if re.search(rb'(?i)(?:api[_-]?key|password|secret|access[_-]?token)\s*[\"\']?\s*[:=]', data):
                _fail('SENSITIVE_CONTENT')
            blob = hashlib.new(algorithm, b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            blobs[path] = ('100755' if before.st_mode & 0o111 else '100644', blob)
        finally:
            os.close(fd)
    return blobs


def _index(git):
    rows = {}
    for row in git('ls-files', '--stage', '-z').split(b'\0'):
        if not row:
            continue
        meta, path = row.split(b'\t', 1)
        mode, oid, stage = meta.decode('ascii').split(' ')
        if stage != '0':
            _fail('UNSAFE_GIT_STATE')
        rows[os.fsdecode(path)] = (mode, oid)
    return rows


def checkpoint(project, *, expected_head, branch, selected, policy_reviewed,
               record, store_dir, now):
    """Create one normal local commit from reviewed bytes and save continuity.

selected maps exact relative paths to reviewed SHA256 bytes (None = deletion).
policy_reviewed must be True from the current authorized caller, never stored state.
Result UNKNOWN resume status is deliberate; no project test execution is implied.
"""
    result = {'outcome': 'REFUSED', 'error_code': None, 'local_commit': None,
              'head_before': None, 'tree': None, 'handoff_saved': False,
              'staging_attempted': False, 'commit_attempted': False,
              'publication_status': 'NOT_REQUESTED', 'safe_to_resume': 'UNKNOWN'}
    fd = None
    deadline = time.monotonic() + TOTAL_SECONDS
    try:
        if policy_reviewed is not True:
            _fail('CURRENT_AUTHORITY_REQUIRED')
        selected = _selection(selected)
        record = validate_record(record)
        if (record['project_request'] != project or record['trigger'] != 'MANUAL'
                or record['phase'] != 'DOCUMENTING' or record['requested_level'] != 'LOCAL_CHECKPOINT'
                or any(record['evidence'].values())):
            _fail('INVALID_CURRENT_RECORD')
        if (type(branch) is not str or not branch or type(expected_head) is not str
                or not re.fullmatch(r'(?:[0-9a-f]{40}|[0-9a-f]{64})', expected_head)):
            _fail('INVALID_EXPECTATION')
        first = _snapshot(project, now, expected_head, branch)
        fd = ins._open_root(project)
        identity = first['snapshot']['repository_identity']
        if (os.fstat(fd).st_dev, os.fstat(fd).st_ino) != (identity['device'], identity['inode']):
            _fail('TARGET_CHANGED')
        with _writer(fd):
            observation = _snapshot(project, now, expected_head, branch)
            if observation['snapshot']['repository_identity'] != identity:
                _fail('TARGET_CHANGED')
            _policy(fd, deadline)
            snap = observation['snapshot']
            if any(c['index'] not in ('.', '?') or (c['index'] == '.' and c['worktree'] == 'A')
                   for c in snap['changes']):
                _fail('EXISTING_STAGING')
            changes = {c['path']: c for c in snap['changes']}
            if not set(selected) <= changes.keys():
                _fail('SELECTION_NOT_CHANGED_OR_IGNORED')
            flags = ['--literal-pathspecs', '-c', 'core.excludesFile=/dev/null',
                     '-c', 'core.attributesFile=/dev/null', '-c', 'maintenance.auto=false',
                     '-c', 'gc.auto=0']
            def git(*args):
                return ins._run(flags + list(args), cwd=f'/proc/self/fd/{fd}',
                                deadline=deadline, pass_fds=(fd,))
            algorithm = git('rev-parse', '--show-object-format').decode().strip()
            if algorithm not in ('sha1', 'sha256'):
                _fail('UNSUPPORTED_OBJECT_FORMAT')
            blobs = _contents(fd, selected, algorithm, deadline)
            original_index = _index(git)
            intended = dict(original_index)
            for path, blob in blobs.items():
                if blob is None:
                    if path not in intended:
                        _fail('INVALID_DELETION')
                    del intended[path]
                else:
                    intended[path] = blob
            result['head_before'] = expected_head
            # Persist an in-progress handoff before staging, preserving earlier good slots.
            pending = advance(record, 'CHECKPOINTING', now=now,
                              evidence={'inspection_digest': observation['inspection_digest']},
                              notes={'files_changed': sorted(selected)})
            with HandoffStore(store_dir, project=project, create=True) as store, store.writer():
                store.publish(pending, now=now, inspection=observation)
                result['handoff_saved'] = True
                try:
                    # Fresh checks after potentially slow handoff I/O, before first Git mutation.
                    fresh = _snapshot(project, now, expected_head, branch)
                    if fresh['snapshot']['repository_identity'] != identity:
                        _fail('TARGET_CHANGED')
                    _policy(fd, deadline)
                    if _index(git) != original_index or _contents(fd, selected, algorithm, deadline) != blobs:
                        _fail('TARGET_CHANGED')
                    result['staging_attempted'] = True
                    git('add', '--', *sorted(selected))
                    if _index(git) != intended:
                        _fail('STAGING_MISMATCH')
                    tree = ins._oid(git('write-tree').strip())
                    result['tree'] = tree
                    fresh = _snapshot(project, now, expected_head, branch)
                    if fresh['snapshot']['repository_identity'] != identity:
                        _fail('TARGET_CHANGED')
                    _policy(fd, deadline)
                    if _contents(fd, selected, algorithm, deadline) != blobs or _index(git) != intended:
                        _fail('TARGET_CHANGED')
                    result['commit_attempted'] = True
                    git('commit', '-m', 'CGC: preserve reviewed local work')
                    head = ins._oid(git('rev-parse', 'HEAD').strip())
                    if (head == expected_head
                            or git('rev-list', '--parents', '-n', '1', 'HEAD').decode().strip().split() != [head, expected_head]
                            or ins._oid(git('rev-parse', 'HEAD^{tree}').strip()) != tree
                            or git('symbolic-ref', '--short', 'HEAD').decode().strip() != branch
                            or _index(git) != intended):
                        _fail('CHECKPOINT_VERIFICATION_FAILED')
                    result['local_commit'] = head
                    completed = advance(pending, 'VERIFYING', now=now, evidence={'local_commit': head})
                    completed = advance(completed, 'PARTIAL', now=now)
                    result['handoff_saved'] = False
                    store.publish(completed, now=now, inspection=observation)
                    result.update(outcome='LOCAL_CHECKPOINT', handoff_saved=True)
                except (ValueError, OSError, CacheError, KeyboardInterrupt) as error:
                    try:
                        store.record_failure('CANCELLED' if isinstance(error, KeyboardInterrupt)
                                             else 'VERIFICATION_FAILED', now=now)
                    except (ValueError, OSError, CacheError):
                        pass
                    raise
    except CheckpointError as error:
        result['error_code'] = str(error)
    except ins.InspectionError as error:
        result['error_code'] = error.code
    except KeyboardInterrupt:
        result['error_code'] = 'CANCELLED'
    except (ValueError, OSError, CacheError):
        result['error_code'] = 'CHECKPOINT_IO_OR_INPUT_FAILED'
    finally:
        if fd is not None:
            os.close(fd)
    if result['error_code'] and (result['staging_attempted'] or result['commit_attempted']):
        result['outcome'] = 'PARTIAL'
    return result
