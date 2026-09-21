"""Bounded Linux/POSIX inspection of an explicit ordinary Git working-tree root.

No target writes, project commands, network, content export or preservation authority.
See docs/V3_CONTRACT.md for the deliberately restricted configuration/layout boundary.
"""
import hashlib
import json
import os
import re
import selectors
import signal
import stat
import subprocess
import time

from .preservation import _stamp, PreservationError

SCHEMA_VERSION = 'cgc-inspection-v3.0-provisional'
MAX_ENTRIES = 10000
MAX_DEPTH = 32
MAX_FILE_BYTES = 16 * 1024 * 1024
MAX_TOTAL_BYTES = 64 * 1024 * 1024
MAX_OUTPUT_BYTES = 256 * 1024
MAX_CONFIG_BYTES = 64 * 1024
TOTAL_SECONDS = 20
COMMAND_SECONDS = 5
GIT = '/usr/bin/git'
OPERATIONS = ('MERGE_HEAD', 'CHERRY_PICK_HEAD', 'REVERT_HEAD', 'rebase-merge',
              'rebase-apply', 'sequencer', 'BISECT_LOG')
DOCUMENTS = ('AGENTS.md', 'README.md', 'PROGRESS.md', 'HANDOFF.md',
             'docs/PROGRESS.md', 'docs/HANDOFF.md', 'docs/V3_PROGRESS.md')
ENV = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'GIT_CONFIG_NOSYSTEM': '1',
       'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_CONFIG_SYSTEM': '/dev/null',
       'GIT_OPTIONAL_LOCKS': '0', 'GIT_TERMINAL_PROMPT': '0',
       'GIT_NO_LAZY_FETCH': '1', 'GIT_NO_REPLACE_OBJECTS': '1',
       'GIT_ATTR_NOSYSTEM': '1'}
CODES = {'INVALID_TARGET', 'UNSAFE_PATH', 'UNSAFE_FILE', 'NOT_REPOSITORY_ROOT',
         'UNSUPPORTED_GITFILE', 'UNSUPPORTED_LAYOUT', 'UNSUPPORTED_CONFIG',
         'RESOURCE_LIMIT', 'TIMEOUT', 'GIT_FAILED', 'MALFORMED_GIT', 'TARGET_CHANGED',
         'FILESYSTEM_ERROR', 'SENSITIVE_METADATA', 'CANCELLED', 'INVALID_TIME'}


class InspectionError(ValueError):
    def __init__(self, code):
        self.code = code if code in CODES else 'MALFORMED_GIT'
        super().__init__(self.code)


def _check_time(deadline):
    if time.monotonic() >= deadline:
        raise InspectionError('TIMEOUT')


def _run(args, *, cwd, deadline, pass_fds=()):
    """Fixed Git executable, isolated environment, bounded combined pipes; no shell."""
    _check_time(deadline)
    end = min(deadline, time.monotonic() + COMMAND_SECONDS)
    proc = subprocess.Popen([GIT, '--no-optional-locks', *args], cwd=cwd, env=ENV,
                            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, start_new_session=True,
                            pass_fds=pass_fds)
    output = bytearray()
    total = 0
    try:
        with selectors.DefaultSelector() as selector:
            for pipe in (proc.stdout, proc.stderr):
                os.set_blocking(pipe.fileno(), False)
                selector.register(pipe, selectors.EVENT_READ)
            while selector.get_map():
                _check_time(end)
                for key, _ in selector.select(min(0.05, max(0, end - time.monotonic()))):
                    chunk = os.read(key.fd, 8192)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    total += len(chunk)
                    if total > MAX_OUTPUT_BYTES:
                        raise InspectionError('RESOURCE_LIMIT')
                    if key.fileobj is proc.stdout:
                        output.extend(chunk)
            try:
                code = proc.wait(timeout=max(0.001, end - time.monotonic()))
            except subprocess.TimeoutExpired:
                raise InspectionError('TIMEOUT') from None
            if code:
                raise InspectionError('GIT_FAILED')
            return bytes(output)
    finally:
        # Also handles Ctrl+C. No project-configured subprocesses are permitted.
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        proc.wait()
        proc.stdout.close()
        proc.stderr.close()


def _open_root(path):
    if (type(path) is not str or not path.startswith('/') or path == '/'
            or len(path) > 2048 or any(ord(c) < 32 or ord(c) == 127 for c in path)
            or any(p in ('', '.', '..') for p in path.split('/')[1:])):
        raise InspectionError('INVALID_TARGET')
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.split('/')[1:]:
            new = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd); fd = new
            st = os.fstat(fd)
            # Root-owned sticky /tmp is allowed as an ancestor, never as the target.
            if st.st_uid not in (0, os.getuid()) or (st.st_mode & 0o022 and not
                    (st.st_uid == 0 and st.st_mode & stat.S_ISVTX)):
                raise InspectionError('UNSAFE_PATH')
        st = os.fstat(fd)
        if st.st_uid != os.getuid() or st.st_mode & 0o022:
            raise InspectionError('UNSAFE_PATH')
        return fd
    except BaseException:
        os.close(fd)
        raise


def _fingerprint(st):
    # atime may change during any read; do not confuse that with content mutation.
    return (st.st_dev, st.st_ino, st.st_mode, st.st_uid, st.st_nlink,
            st.st_size, st.st_mtime_ns, st.st_ctime_ns)


def _scan(rootfd, deadline):
    """Bounded no-follow metadata walk. No worktree file contents are opened."""
    entries = {}
    total = 0
    device = os.fstat(rootfd).st_dev

    def walk(fd, prefix='', depth=0):
        nonlocal total
        _check_time(deadline)
        if depth > MAX_DEPTH:
            raise InspectionError('RESOURCE_LIMIT')
        with os.scandir(fd) as children:
            for child in children:
                _check_time(deadline)
                name = prefix + child.name
                if child.name in {'.codex', '.ssh', '.aws', '.azure', '.gnupg'}:
                    raise InspectionError('UNSAFE_FILE')
                if len(entries) >= MAX_ENTRIES or len(os.fsencode(name)) > 4096:
                    raise InspectionError('RESOURCE_LIMIT')
                st = child.stat(follow_symlinks=False)
                entries[name] = _fingerprint(st)
                metadata = name == '.git' or name.startswith('.git/')
                if st.st_dev != device or st.st_uid != os.getuid():
                    raise InspectionError('UNSAFE_FILE')
                if stat.S_ISLNK(st.st_mode):
                    if metadata:
                        raise InspectionError('UNSAFE_FILE')
                    continue
                if not (stat.S_ISDIR(st.st_mode) or stat.S_ISREG(st.st_mode)):
                    raise InspectionError('UNSAFE_FILE')
                if st.st_mode & 0o022 or (stat.S_ISREG(st.st_mode) and st.st_nlink != 1):
                    raise InspectionError('UNSAFE_FILE')
                if stat.S_ISREG(st.st_mode):
                    total += st.st_size
                    if st.st_size > MAX_FILE_BYTES or total > MAX_TOTAL_BYTES:
                        raise InspectionError('RESOURCE_LIMIT')
                else:
                    # Never descend into linked worktrees/submodule administrative stores.
                    if name in ('.git/worktrees', '.git/modules'):
                        continue
                    sub = os.open(child.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                    try:
                        if _fingerprint(os.fstat(sub)) != _fingerprint(st):
                            raise InspectionError('TARGET_CHANGED')
                        # Nested repositories are boundaries, not additional targets.
                        nested = False
                        if not metadata:
                            try:
                                os.stat('.git', dir_fd=sub, follow_symlinks=False)
                                nested = True
                            except FileNotFoundError:
                                pass
                        if nested:
                            entries[name + '/.git'] = 'NESTED_BOUNDARY'
                        else:
                            walk(sub, name + '/', depth + 1)
                    finally:
                        os.close(sub)
    walk(rootfd)
    for forbidden in ('.git/commondir', '.git/objects/info/alternates',
                      '.git/objects/info/http-alternates', '.git/info/grafts'):
        if forbidden in entries:
            raise InspectionError('UNSUPPORTED_LAYOUT')
    if any(n.endswith('.promisor') or n.startswith('.git/sharedindex.') for n in entries):
        raise InspectionError('UNSUPPORTED_LAYOUT')
    return entries


def _text(raw):
    text = raw.decode('utf-8', 'surrogateescape') if isinstance(raw, bytes) else raw
    if not text or len(text) > 4096 or '\x00' in text:
        raise InspectionError('MALFORMED_GIT')
    # Reject recognizable credentials in metadata, without echoing the offending field.
    if re.search(r'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|://[^/\s]+@)', text):
        raise InspectionError('SENSITIVE_METADATA')
    return text


def _config(rootfd, deadline):
    gitfd = os.open('.git', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=rootfd)
    try:
        fd = os.open('config', os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=gitfd)
    finally:
        os.close(gitfd)
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_size > MAX_CONFIG_BYTES:
            raise InspectionError('RESOURCE_LIMIT')
        raw = _run(['config', '--no-includes', '--file', f'/proc/self/fd/{fd}', '--null', '--list'],
                   cwd='/', deadline=deadline, pass_fds=(fd,))
    finally:
        os.close(fd)
    remotes = set()
    allowed_core = {'repositoryformatversion', 'filemode', 'bare', 'logallrefupdates',
                    'ignorecase', 'precomposeunicode', 'symlinks'}
    for entry in raw.split(b'\0'):
        if not entry:
            continue
        key, _, value = entry.partition(b'\n')
        key = key.decode('utf-8', 'surrogateescape')
        if key.startswith('core.') and key[5:] in allowed_core:
            if key == 'core.bare' and value.lower() not in (b'false', b'no', b'off', b'0'):
                raise InspectionError('UNSUPPORTED_LAYOUT')
        elif key in ('user.name', 'user.email'):
            pass  # Never retained or emitted.
        elif key == 'extensions.objectformat' and value in (b'sha1', b'sha256'):
            pass
        elif re.fullmatch(r'remote\..+\.(url|pushurl|fetch)', key):
            remotes.add(_text(key[7:].rsplit('.', 1)[0]))  # URLs deliberately discarded.
        elif re.fullmatch(r'branch\..+\.(remote|merge)', key):
            pass
        elif re.fullmatch(r'submodule\..+\.(url|active)', key):
            pass  # No submodule recursion; no URL emission.
        else:
            # Includes, filters, fsmonitor, hooksPath, worktree redirection, external
            # attributes/excludes, sparse/promisor/extensions are refused, not executed.
            raise InspectionError('UNSUPPORTED_CONFIG')
    return sorted(remotes)


def _oid(raw):
    if not re.fullmatch(rb'(?:[0-9a-f]{40}|[0-9a-f]{64})', raw):
        raise InspectionError('MALFORMED_GIT')
    return raw.decode('ascii')


def _path(raw):
    value = _text(raw)
    parts = value.rstrip('/').split('/')
    if value.startswith('/') or any(p in ('', '.', '..', '.git') for p in parts):
        raise InspectionError('MALFORMED_GIT')
    return value


def _status(raw):
    fields = {}; changes = []
    items = iter(raw.split(b'\0'))
    for item in items:
        if not item:
            continue
        if item.startswith(b'# '):
            key, sep, value = item[2:].partition(b' ')
            if not sep or key in fields:
                raise InspectionError('MALFORMED_GIT')
            fields[key] = value
            continue
        kind = item[:1]
        if kind in (b'1', b'2', b'u'):
            count = {b'1': 8, b'2': 9, b'u': 10}[kind]
            bits = item.split(b' ', count)
            if len(bits) != count + 1 or not re.fullmatch(rb'[.MADRCUT]{2}', bits[1]):
                raise InspectionError('MALFORMED_GIT')
            change = {'path': _path(bits[-1]), 'index': chr(bits[1][0]),
                      'worktree': chr(bits[1][1]), 'conflict': kind == b'u',
                      'original_path': None}
            if kind == b'2':
                change['original_path'] = _path(next(items))
            changes.append(change)
        elif item.startswith(b'? '):
            changes.append({'path': _path(item[2:]), 'index': '?', 'worktree': '?',
                            'conflict': False, 'original_path': None})
        else:
            raise InspectionError('MALFORMED_GIT')
    if not {b'branch.oid', b'branch.head'} <= fields.keys() or not fields.keys() <= {
            b'branch.oid', b'branch.head', b'branch.upstream', b'branch.ab'}:
        raise InspectionError('MALFORMED_GIT')
    head = None if fields[b'branch.oid'] == b'(initial)' else _oid(fields[b'branch.oid'])
    detached = fields[b'branch.head'] == b'(detached)'
    branch = None if detached else _text(fields[b'branch.head'])
    ahead = behind = None
    if b'branch.ab' in fields:
        match = re.fullmatch(rb'\+([0-9]{1,12}) -([0-9]{1,12})', fields[b'branch.ab'])
        if not match:
            raise InspectionError('MALFORMED_GIT')
        ahead, behind = map(int, match.groups())
    return {'head': head, 'branch': branch, 'detached': detached,
            'upstream': _text(fields[b'branch.upstream']) if b'branch.upstream' in fields else None,
            'ahead': ahead, 'behind': behind,
            'changes': sorted(changes, key=lambda c: c['path'])}


def inspect_project(project, *, now):
    """Return a minimized snapshot or a fixed failure with no partial snapshot/receipt."""
    result = {'schema_version': SCHEMA_VERSION, 'status': 'REFUSED', 'error_code': None,
              'snapshot': None, 'inspection_digest': None, 'safe_to_resume': 'UNKNOWN',
              'automatic_mutation_authorized': False}
    fd = None
    deadline = time.monotonic() + TOTAL_SECONDS
    try:
        try:
            stamp = _stamp(now)
        except PreservationError:
            raise InspectionError('INVALID_TIME') from None
        if isinstance(project, str) and project:
            _text(project)
        try:
            fd = _open_root(project)
        except OSError:
            raise InspectionError('UNSAFE_PATH') from None
        rootstat = _fingerprint(os.fstat(fd))
        try:
            gitstat = os.stat('.git', dir_fd=fd, follow_symlinks=False)
        except FileNotFoundError:
            raise InspectionError('NOT_REPOSITORY_ROOT') from None
        if stat.S_ISREG(gitstat.st_mode):
            raise InspectionError('UNSUPPORTED_GITFILE')
        if not stat.S_ISDIR(gitstat.st_mode):
            raise InspectionError('UNSAFE_FILE')
        before = _scan(fd, deadline)
        remotes = _config(fd, deadline)
        args = ['-c', 'core.fsmonitor=false', '-c', 'core.untrackedCache=false',
                '-c', 'core.excludesFile=/dev/null', '-c', 'core.attributesFile=/dev/null',
                '-c', 'maintenance.auto=false', '-c', 'gc.auto=0']
        def git(*command):
            return _run(args + list(command), cwd=f'/proc/self/fd/{fd}',
                        deadline=deadline, pass_fds=(fd,))
        root = git('rev-parse', '--show-toplevel').rstrip(b'\n')
        if os.fsdecode(root) != project:
            raise InspectionError('NOT_REPOSITORY_ROOT')
        index = git('ls-files', '--stage', '-v', '-z')
        submodules = []
        hidden_index_paths = []
        for row in index.split(b'\0'):
            if not row:
                continue
            meta, sep, path = row.partition(b'\t')
            bits = meta.split(b' ')
            if not sep or len(bits) != 4 or bits[3] not in (b'0', b'1', b'2', b'3') or len(bits[0]) != 1:
                raise InspectionError('MALFORMED_GIT')
            _path(path); _oid(bits[2])
            if bits[0].islower() or bits[0].upper() == b'S':
                hidden_index_paths.append(_path(path))
            if bits[1] == b'160000':
                submodules.append(_path(path))
        command = ('status', '--porcelain=v2', '-z', '--branch', '--untracked-files=all',
                   '--ignore-submodules=all', '--renames')
        raw = git(*command)
        snap = _status(raw)
        # Detect observed races; never advertise a transactional/locked snapshot.
        if raw != git(*command) or index != git('ls-files', '--stage', '-v', '-z'):
            raise InspectionError('TARGET_CHANGED')
        if before != _scan(fd, deadline) or rootstat != _fingerprint(os.fstat(fd)):
            raise InspectionError('TARGET_CHANGED')
        checkfd = _open_root(project)
        try:
            if rootstat != _fingerprint(os.fstat(checkfd)):
                raise InspectionError('TARGET_CHANGED')
        finally:
            os.close(checkfd)
        snap.update(project_request=project, root=project,
                    repository_identity={'device': rootstat[0], 'inode': rootstat[1],
                                         'git_device': gitstat.st_dev, 'git_inode': gitstat.st_ino},
                    observed_at=stamp, evidence_basis='LOCAL_OBSERVATION',
                    consistency='REPEATED_OBSERVATION_NOT_ATOMIC', remotes=remotes,
                    remote_state='NOT_QUERIED', operations=[n for n in OPERATIONS if '.git/' + n in before],
                    linked_worktrees_present='.git/worktrees' in before,
                    submodules=sorted(set(submodules)), submodule_worktrees='NOT_INSPECTED',
                    hidden_index_paths=sorted(set(hidden_index_paths)),
                    document_candidates=[n for n in DOCUMENTS if n in before],
                    instructions='NOT_READ', test_command='UNKNOWN',
                    nested_repositories=sorted(_path(n[:-5]) for n, v in before.items() if v == 'NESTED_BOUNDARY'))
        encoded = json.dumps(snap, sort_keys=True, ensure_ascii=True, allow_nan=False).encode()
        if len(encoded) > MAX_OUTPUT_BYTES:
            raise InspectionError('RESOURCE_LIMIT')
        result.update(status='OBSERVED', snapshot=snap,
                      inspection_digest=hashlib.sha256(encoded).hexdigest())
    except InspectionError as exc:
        result['error_code'] = exc.code
    except KeyboardInterrupt:
        result['error_code'] = 'CANCELLED'
    except OSError:
        result['error_code'] = 'FILESYSTEM_ERROR'
    except (ValueError, StopIteration, KeyError, IndexError):
        result['error_code'] = 'MALFORMED_GIT'
    finally:
        if fd is not None:
            os.close(fd)
    return validate_inspection(result)


def validate_inspection(result):
    """Validate the public envelope and receipt; digest is integrity, not authenticity."""
    try:
        if type(result) is not dict or set(result) != {
                'schema_version', 'status', 'error_code', 'snapshot', 'inspection_digest',
                'safe_to_resume', 'automatic_mutation_authorized'}:
            raise InspectionError('MALFORMED_GIT')
        if (result['schema_version'] != SCHEMA_VERSION or result['safe_to_resume'] != 'UNKNOWN'
                or result['automatic_mutation_authorized'] is not False):
            raise InspectionError('MALFORMED_GIT')
        snap = result['snapshot']
        if result['status'] == 'REFUSED':
            if result['error_code'] not in CODES or snap is not None or result['inspection_digest'] is not None:
                raise InspectionError('MALFORMED_GIT')
        elif result['status'] == 'OBSERVED' and result['error_code'] is None:
            if type(snap) is not dict or set(snap) != {
                    'head', 'branch', 'detached', 'upstream', 'ahead', 'behind', 'changes',
                    'project_request', 'root', 'repository_identity', 'observed_at',
                    'evidence_basis', 'consistency', 'remotes', 'remote_state', 'operations',
                    'linked_worktrees_present', 'submodules', 'submodule_worktrees',
                    'document_candidates', 'instructions', 'test_command', 'nested_repositories', 'hidden_index_paths'}:
                raise InspectionError('MALFORMED_GIT')
            for key, value in {'evidence_basis': 'LOCAL_OBSERVATION',
                               'consistency': 'REPEATED_OBSERVATION_NOT_ATOMIC',
                               'remote_state': 'NOT_QUERIED', 'submodule_worktrees': 'NOT_INSPECTED',
                               'instructions': 'NOT_READ', 'test_command': 'UNKNOWN'}.items():
                if snap[key] != value:
                    raise InspectionError('MALFORMED_GIT')
            if _stamp(snap['observed_at']) != snap['observed_at']:
                raise InspectionError('MALFORMED_GIT')
            root = _text(snap['root'])
            if root != snap['project_request'] or not root.startswith('/') or root == '/' or '..' in root.split('/'):
                raise InspectionError('MALFORMED_GIT')
            identity = snap['repository_identity']
            if type(identity) is not dict or set(identity) != {'device', 'inode', 'git_device', 'git_inode'}:
                raise InspectionError('MALFORMED_GIT')
            if any(type(v) is not int or v < 0 for v in identity.values()):
                raise InspectionError('MALFORMED_GIT')
            for key in ('detached', 'linked_worktrees_present'):
                if type(snap[key]) is not bool:
                    raise InspectionError('MALFORMED_GIT')
            if snap['detached'] != (snap['branch'] is None):
                raise InspectionError('MALFORMED_GIT')
            if snap['head'] is not None:
                _oid(snap['head'].encode('ascii'))
            for key in ('branch', 'upstream'):
                if snap[key] is not None:
                    _text(snap[key])
            for key in ('ahead', 'behind'):
                if snap[key] is not None and (type(snap[key]) is not int or not 0 <= snap[key] < 10**12):
                    raise InspectionError('MALFORMED_GIT')
            for key in ('remotes', 'operations', 'submodules', 'document_candidates', 'nested_repositories', 'hidden_index_paths'):
                values = snap[key]
                if type(values) is not list or len(values) > MAX_ENTRIES or len(set(values)) != len(values):
                    raise InspectionError('MALFORMED_GIT')
                for value in values:
                    _text(value)
                    if key in ('submodules', 'nested_repositories', 'hidden_index_paths'):
                        _path(value)
                if key == 'operations' and not set(values) <= set(OPERATIONS):
                    raise InspectionError('MALFORMED_GIT')
                if key == 'document_candidates' and not set(values) <= set(DOCUMENTS):
                    raise InspectionError('MALFORMED_GIT')
            if type(snap['changes']) is not list or len(snap['changes']) > MAX_ENTRIES:
                raise InspectionError('MALFORMED_GIT')
            for change in snap['changes']:
                if type(change) is not dict or set(change) != {'path', 'index', 'worktree', 'conflict', 'original_path'}:
                    raise InspectionError('MALFORMED_GIT')
                _path(change['path'])
                if change['original_path'] is not None:
                    _path(change['original_path'])
                if (change['index'] not in tuple('.MADRCUT?') or change['worktree'] not in tuple('.MADRCUT?')
                        or type(change['conflict']) is not bool):
                    raise InspectionError('MALFORMED_GIT')
            encoded = json.dumps(snap, sort_keys=True, ensure_ascii=True, allow_nan=False).encode()
            if len(encoded) > MAX_OUTPUT_BYTES or hashlib.sha256(encoded).hexdigest() != result['inspection_digest']:
                raise InspectionError('MALFORMED_GIT')
        else:
            raise InspectionError('MALFORMED_GIT')
        return result
    except (TypeError, ValueError, KeyError, AttributeError, RecursionError):
        raise InspectionError('MALFORMED_GIT') from None


def render_json(result):
    return json.dumps(validate_inspection(result), sort_keys=True, ensure_ascii=True, allow_nan=False)


def render_human(result):
    return 'CREDID GUARDIAN CODEX (CGC) — INSPECTION ONLY\n' + render_json(result)
