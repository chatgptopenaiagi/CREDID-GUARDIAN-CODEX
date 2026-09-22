"""Bounded continuity storage outside the project; no target operations.

Reuse CGC Cache's private no-follow directory and process-lifetime flock. The
separate envelope retains curated attempt/inspection evidence without upgrading it.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import uuid

from .cache import Cache, CacheError, _safe_file
from .engine import timestamp
from .inspection import validate_inspection
from .preservation import validate_record, _stamp, render_human as render_attempt
from .quota import _decode, QuotaError

SCHEMA_VERSION = 'cgc-handoff-v3.0-provisional'
MAX_HANDOFF_BYTES = 2 * 1024 * 1024
MAX_GENERATION = 2**53 - 1
FAILURES = {'INPUT_REJECTED', 'INSPECTION_FAILED', 'WRITE_FAILED', 'VERIFICATION_FAILED', 'CANCELLED'}
ERRORS = {'INVALID_HANDOFF', 'HANDOFF_SIZE_LIMIT', 'SENSITIVE_HANDOFF', 'UNSAFE_HANDOFF_PATH',
          'CORRUPT_HANDOFF', 'WRITER_REQUIRED', 'HANDOFF_WRITE_FAILED',
          'HANDOFF_PUBLICATION_UNCERTAIN', 'PROJECT_MISMATCH', 'UNSUPPORTED_HANDOFF_SCHEMA'}


class HandoffError(CacheError):
    def __init__(self, code='INVALID_HANDOFF'):
        super().__init__(code if code in ERRORS else 'INVALID_HANDOFF')


def _canonical(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False,
                       separators=(',', ':')) + '\n').encode('ascii')


def _screen(data):
    if re.search(rb'(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|https?://[^\s/":]+:[^\s/"@]+@)', data):
        raise HandoffError('SENSITIVE_HANDOFF')


def _absolute(value):
    value = os.fspath(value)
    if (type(value) is not str or not value.startswith('/') or len(value) > 2048
            or any(c in ('', '.', '..') for c in value.split('/')[1:])
            or any(ord(c) < 32 or ord(c) == 127 for c in value)):
        raise HandoffError('UNSAFE_HANDOFF_PATH')
    return value


def _digest(slot):
    return hashlib.sha256(_canonical({k: v for k, v in slot.items() if k != 'digest'})).hexdigest()


def _validate_slot(slot, project, generation, at):
    if type(slot) is not dict or set(slot) != {
            'generation', 'published_at', 'content_basis', 'record', 'inspection', 'digest'}:
        raise HandoffError()
    if (type(slot['generation']) is not int or not 1 <= slot['generation'] <= generation
            or slot['content_basis'] != 'OPERATOR_CURATED'
            or _stamp(slot['published_at']) != slot['published_at']
            or timestamp(slot['published_at']) > timestamp(at)):
        raise HandoffError()
    record = validate_record(slot['record'])
    if record['project_request'] != project:
        raise HandoffError('PROJECT_MISMATCH')
    if timestamp(record['events'][-1]['at']) > timestamp(slot['published_at']):
        raise HandoffError()
    inspection = slot['inspection']
    if inspection is None:
        if record['evidence']['inspection_digest'] is not None:
            raise HandoffError()
    else:
        validate_inspection(inspection)
        if (inspection['status'] != 'OBSERVED' or inspection['snapshot']['root'] != project
                or inspection['inspection_digest'] != record['evidence']['inspection_digest']
                or timestamp(inspection['snapshot']['observed_at']) > timestamp(slot['published_at'])):
            raise HandoffError()
    if slot['digest'] != _digest(slot):
        raise HandoffError()


def validate_state(state):
    """Strict schema/bounds/bindings; does not authenticate caller-supplied receipts."""
    try:
        if type(state) is not dict or set(state) != {
                'schema_version', 'scope', 'project_request', 'generation', 'latest_attempt',
                'last_known_good', 'previous_known_good', 'safe_to_resume', 'automatic_mutation_authorized'}:
            raise HandoffError()
        if type(state['schema_version']) is not str:
            raise HandoffError()
        if state['schema_version'] != SCHEMA_VERSION:
            raise HandoffError('UNSUPPORTED_HANDOFF_SCHEMA')
        if (state['scope'] != 'CONTINUITY_ONLY'
                or state['safe_to_resume'] != 'UNKNOWN' or state['automatic_mutation_authorized'] is not False):
            raise HandoffError()
        project = _absolute(state['project_request'])
        generation = state['generation']
        if type(generation) is not int or not 1 <= generation <= MAX_GENERATION:
            raise HandoffError()
        latest = state['latest_attempt']
        if type(latest) is not dict or set(latest) != {'status', 'at', 'error_code', 'handoff_digest'}:
            raise HandoffError()
        if _stamp(latest['at']) != latest['at']:
            raise HandoffError()
        good, previous = state['last_known_good'], state['previous_known_good']
        for slot in (good, previous):
            if slot is not None:
                _validate_slot(slot, project, generation, latest['at'])
        if previous is not None and (good is None or previous['generation'] >= good['generation']
                                     or timestamp(previous['published_at']) > timestamp(good['published_at'])):
            raise HandoffError()
        if latest['status'] == 'PUBLISHED':
            if (good is None or good['generation'] != generation or good['published_at'] != latest['at']
                    or latest['error_code'] is not None or latest['handoff_digest'] != good['digest']):
                raise HandoffError()
        elif latest['status'] == 'FAILED':
            if (latest['error_code'] not in FAILURES or latest['handoff_digest'] is not None
                    or (good is not None and good['generation'] >= generation)):
                raise HandoffError()
        else:
            raise HandoffError()
        data = _canonical(state)
        if len(data) > MAX_HANDOFF_BYTES:
            raise HandoffError('HANDOFF_SIZE_LIMIT')
        _screen(data)
        return copy.deepcopy(state)
    except HandoffError:
        raise
    except (ValueError, TypeError, KeyError, AttributeError, RecursionError, OverflowError):
        raise HandoffError() from None


def render_json(state):
    return _canonical(validate_state(state)).decode('ascii').rstrip('\n')


def render_human(state):
    state = json.loads(_canonical(validate_state(state)))
    lines = ['CREDID GUARDIAN CODEX (CGC) — CONTINUITY HANDOFF ONLY',
             'SCHEMA_VERSION: ' + state['schema_version'],
             'PROJECT: ' + json.dumps(state['project_request'], ensure_ascii=True),
             'GENERATION: ' + str(state['generation']),
             'LATEST_ATTEMPT: ' + json.dumps(state['latest_attempt'], sort_keys=True),
             'PROJECT_PRESERVATION_VERIFICATION: NOT_PERFORMED; SAFE_TO_RESUME: UNKNOWN']
    for name in ('last_known_good', 'previous_known_good'):
        slot = state[name]
        lines.append(name.upper() + ': ' + ('NONE' if slot is None else slot['digest']))
        if slot is not None:
            lines += ['PUBLISHED_AT: ' + slot['published_at'],
                      'REPORTED ATTEMPT (receipts not independently verified):',
                      render_attempt(slot['record']),
                      'INSPECTION: ' + json.dumps(slot['inspection'], sort_keys=True, ensure_ascii=True)]
            lines += [key.upper() + ': ' + json.dumps(value, ensure_ascii=True, sort_keys=True)
                      for key, value in sorted(slot['record']['notes'].items())]
    result = '\n'.join(lines)
    if len(result.encode('utf-8')) > MAX_HANDOFF_BYTES:
        raise HandoffError('HANDOFF_SIZE_LIMIT')
    return result


class HandoffStore(Cache):
    """One explicitly selected external private directory, bound to one project.

writer() is inherited unchanged: nonblocking POSIX flock on a persistent lock inode.
Call publish/record_failure under that lock; read/render need no writer lock.
"""
    def __init__(self, directory, *, project, create=False):
        try:
            self.project = _absolute(project)
            directory = _absolute(directory)
            p, d = Path(self.project), Path(directory)
            if p == d or p in d.parents or d in p.parents or any(
                    c in {'.git', '.codex', '.ssh', '.aws', '.azure', '.gnupg'} for c in d.parts):
                raise HandoffError('UNSAFE_HANDOFF_PATH')
            _screen(_canonical([self.project, directory]))
        except (TypeError, ValueError):
            raise HandoffError('UNSAFE_HANDOFF_PATH') from None
        super().__init__(directory, create=create)

    def __enter__(self):
        # Refuse project aliases before creating/opening storage. A missing project
        # is allowed for historical readback; no project content is opened.
        fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
        try:
            for part in self.project.split('/')[1:]:
                try:
                    child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                                    dir_fd=fd)
                except FileNotFoundError:
                    break
                os.close(fd)
                fd = child
        except OSError:
            raise HandoffError('UNSAFE_HANDOFF_PATH') from None
        finally:
            os.close(fd)
        return super().__enter__()

    def read(self):
        fd = None
        try:
            fd = os.open('handoff.json', os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=self.fd)
            _safe_file(fd)
            with os.fdopen(fd, 'rb') as stream:
                fd = None
                raw = stream.read(MAX_HANDOFF_BYTES + 1)
            if len(raw) > MAX_HANDOFF_BYTES:
                raise HandoffError('HANDOFF_SIZE_LIMIT')
            state = validate_state(_decode(raw))
            if state['project_request'] != self.project:
                raise HandoffError('PROJECT_MISMATCH')
            if raw != _canonical(state):
                raise HandoffError('CORRUPT_HANDOFF')
            return state
        except FileNotFoundError:
            return None
        except HandoffError as error:
            if str(error) in {'UNSUPPORTED_HANDOFF_SCHEMA', 'HANDOFF_SIZE_LIMIT', 'PROJECT_MISMATCH'}:
                raise
            raise HandoffError('CORRUPT_HANDOFF') from None
        except (OSError, CacheError, QuotaError, ValueError, RecursionError):
            raise HandoffError('CORRUPT_HANDOFF') from None
        finally:
            if fd is not None:
                os.close(fd)

    def write(self, state):
        # Do not expose Cache.write's unrelated V2 state.json behavior on this store.
        raise HandoffError('INVALID_HANDOFF')

    def _next(self, now):
        if self.lock_fd is None:
            raise HandoffError('WRITER_REQUIRED')
        try:
            now = _stamp(now)
        except ValueError:
            raise HandoffError() from None
        prior = self.read()
        if prior and timestamp(now) < timestamp(prior['latest_attempt']['at']):
            raise HandoffError()
        return {'schema_version': SCHEMA_VERSION, 'scope': 'CONTINUITY_ONLY',
                'project_request': self.project, 'generation': prior['generation'] + 1 if prior else 1,
                'latest_attempt': {'status': 'FAILED', 'at': now, 'error_code': None, 'handoff_digest': None},
                'last_known_good': prior['last_known_good'] if prior else None,
                'previous_known_good': prior['previous_known_good'] if prior else None,
                'safe_to_resume': 'UNKNOWN', 'automatic_mutation_authorized': False}

    def publish(self, record, *, now, inspection=None):
        try:
            record = validate_record(record)
            if inspection is not None:
                inspection = copy.deepcopy(validate_inspection(inspection))
            state = self._next(now)
            slot = {'generation': state['generation'], 'published_at': state['latest_attempt']['at'],
                    'content_basis': 'OPERATOR_CURATED', 'record': record, 'inspection': inspection}
            slot['digest'] = _digest(slot)
            state['previous_known_good'] = state['last_known_good']
            state['last_known_good'] = slot
            state['latest_attempt'].update(status='PUBLISHED', handoff_digest=slot['digest'])
            return self._publish_state(state)
        except HandoffError:
            raise
        except (ValueError, TypeError, RecursionError, OverflowError):
            raise HandoffError() from None

    def record_failure(self, code, *, now):
        if type(code) is not str or code not in FAILURES:
            raise HandoffError()
        state = self._next(now)
        state['latest_attempt']['error_code'] = code
        return self._publish_state(state)

    def _publish_state(self, state):
        state = validate_state(state)
        data = _canonical(state)
        name = '.handoff-' + uuid.uuid4().hex + '.tmp'
        fd = None
        replaced = False
        try:
            # Existing corrupt/unsafe state is never erased to make publication succeed.
            self.read()
            fd = os.open(name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
                         0o600, dir_fd=self.fd)
            with os.fdopen(fd, 'wb') as stream:
                fd = None
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(name, 'handoff.json', src_dir_fd=self.fd, dst_dir_fd=self.fd)
            replaced = True
            os.fsync(self.fd)
            if self.read() != state:
                raise HandoffError('HANDOFF_PUBLICATION_UNCERTAIN')
            return state
        except (OSError, CacheError):
            raise HandoffError('HANDOFF_PUBLICATION_UNCERTAIN' if replaced else 'HANDOFF_WRITE_FAILED') from None
        finally:
            if fd is not None:
                os.close(fd)
            try:
                os.unlink(name, dir_fd=self.fd)
            except FileNotFoundError:
                pass
