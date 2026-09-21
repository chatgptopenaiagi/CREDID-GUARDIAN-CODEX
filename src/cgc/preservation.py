"""Pure V3 attempt contract. No filesystem, Git, quota reads or mutation authority.

Receipts are supplied by trusted adapters (synthetic fixtures today). Validation
checks consistency, not whether a claimed external action actually happened.
"""
import copy
import json
import re

from .engine import timestamp, StateError

SCHEMA_VERSION = 'cgc-preservation-v3.0-provisional'
MAX_RECORD_BYTES = 262144
FAILURE_PHASES = {'BLOCKED', 'FAILED', 'CANCELLED'}
TERMINAL = FAILURE_PHASES | {'PRESERVED', 'PARTIAL'}
NEXT = {
    'INSPECTING': {'STABILIZING', 'TESTING', 'DOCUMENTING'},
    'STABILIZING': {'TESTING', 'DOCUMENTING'},
    'TESTING': {'DOCUMENTING'},
    'DOCUMENTING': {'CHECKPOINTING', 'VERIFYING'},
    'CHECKPOINTING': {'PUBLISHING', 'VERIFYING'},
    'PUBLISHING': {'VERIFYING'},
    'VERIFYING': {'PRESERVED', 'PARTIAL'},
}
NOTE_LISTS = ('complete', 'partial', 'not_started', 'files_changed', 'tests_run',
              'test_results', 'known_failures', 'important_discoveries', 'decisions',
              'do_not_repeat', 'limitations')
NOTE_TEXT = ('mission', 'next_exact_action')
DIGESTS = ('inspection_digest', 'handoff_digest', 'resume_digest')
COMMITS = ('local_commit', 'tracking_commit', 'remote_commit')
PUBLICATION_ERRORS = {'REMOTE_UNAVAILABLE', 'REMOTE_MISSING', 'PUSH_REJECTED',
                      'AUTHENTICATION_FAILED', 'HOOK_REJECTED', 'VERIFICATION_MISMATCH'}
DERIVED = {'preservation_status', 'publication_status', 'safe_to_resume', 'outcome',
           'local_checkpoint', 'automatic_mutation_authorized'}
FIELDS = {'schema_version', 'project_request', 'project_basis', 'trigger', 'requested_level',
          'evidence_basis', 'phase', 'events', 'evidence', 'project_test_status', 'notes'} | DERIVED


class PreservationError(ValueError):
    def __init__(self):
        super().__init__('INVALID_PRESERVATION_RECORD')


def _text(value):
    if (not isinstance(value, str) or not 1 <= len(value) <= 2048
            or not value.strip() or any(ord(c) < 32 or ord(c) == 127 for c in value)):
        raise PreservationError()


def _stamp(value):
    try:
        return timestamp(value).isoformat().replace('+00:00', 'Z')
    except StateError:
        raise PreservationError() from None


def _derived(record):
    e, phase, level = record['evidence'], record['phase'], record['requested_level']
    handoff = all(e[k] is not None for k in DIGESTS)
    local = e['local_commit'] is not None
    remote = local and e['local_commit'] == e['tracking_commit'] == e['remote_commit']
    sufficient = handoff and (level == 'HANDOFF_ONLY' or local) and (level != 'REMOTE_VERIFIED' or remote)
    if e['unsafe_target']:
        sufficient = False
    if phase == 'PRESERVED' and not sufficient:
        raise PreservationError()
    publication = ('NOT_REQUESTED' if level != 'REMOTE_VERIFIED' else
                   'VERIFIED' if remote else 'LOCAL_CHECKPOINT_ONLY' if local and phase in TERMINAL else
                   'FAILED' if e['publication_error'] else 'PUSH_ATTEMPTED' if e['push_attempted'] else 'NOT_ATTEMPTED')
    survived = e['handoff_digest'] is not None or local
    resume = ('NO' if e['unsafe_target'] else 'YES' if phase == 'PRESERVED' else
              'PARTIAL' if phase in TERMINAL and survived else
              'NO' if phase in FAILURE_PHASES else 'UNKNOWN')
    outcome = ('BLOCKED_UNSAFE' if e['unsafe_target'] else
               'REMOTE_VERIFIED' if phase == 'PRESERVED' and remote else
               'LOCAL_CHECKPOINT' if phase == 'PRESERVED' and local else
               'HANDOFF_ONLY' if phase == 'PRESERVED' else
               'PARTIAL_PRESERVATION' if phase in TERMINAL and survived else
               phase if phase in {'FAILED', 'CANCELLED'} else
               'BLOCKED_UNSAFE' if phase == 'BLOCKED' else
               'PARTIAL_PRESERVATION' if phase == 'PARTIAL' else
               'REMOTE_PUSH_ATTEMPTED' if e['push_attempted'] else 'IN_PROGRESS')
    return {'preservation_status': phase, 'publication_status': publication,
            'safe_to_resume': resume, 'outcome': outcome,
            'local_checkpoint': e['local_commit'], 'automatic_mutation_authorized': False}


def validate_record(record):
    """Strict bounded allowlist, replayed lifecycle, and recomputed conclusions."""
    try:
        if type(record) is not dict or set(record) != FIELDS or record['schema_version'] != SCHEMA_VERSION:
            raise PreservationError()
        _text(record['project_request'])
        path = record['project_request']
        if not path.startswith('/') or path == '/' or '..' in path.split('/'):
            raise PreservationError()
        if record['project_basis'] != 'OPERATOR_REQUESTED' or record['trigger'] not in ('MANUAL', 'SYNTHETIC'):
            raise PreservationError()
        if record['evidence_basis'] != ('SYNTHETIC' if record['trigger'] == 'SYNTHETIC' else 'ADAPTER_REPORTED'):
            raise PreservationError()
        if record['requested_level'] not in ('HANDOFF_ONLY', 'LOCAL_CHECKPOINT', 'REMOTE_VERIFIED'):
            raise PreservationError()
        events = record['events']
        if type(events) is not list or not 1 <= len(events) <= 64:
            raise PreservationError()
        previous = None
        for event in events:
            if type(event) is not dict or set(event) != {'phase', 'at'} or _stamp(event['at']) != event['at']:
                raise PreservationError()
            if previous is None:
                if event['phase'] != 'INSPECTING': raise PreservationError()
            elif (previous['phase'] in TERMINAL
                  or event['phase'] not in NEXT[previous['phase']] | FAILURE_PHASES
                  or timestamp(event['at']) < timestamp(previous['at'])):
                raise PreservationError()
            previous = event
        if record['phase'] != previous['phase']:
            raise PreservationError()
        notes = record['notes']
        if type(notes) is not dict or set(notes) != set(NOTE_LISTS + NOTE_TEXT):
            raise PreservationError()
        for key in NOTE_TEXT: _text(notes[key])
        for key in NOTE_LISTS:
            if type(notes[key]) is not list or len(notes[key]) > 64: raise PreservationError()
            for item in notes[key]: _text(item)
        test = record['project_test_status']
        if test not in ('UNKNOWN', 'PASSED', 'FAILED', 'SKIPPED'):
            raise PreservationError()
        if test in ('PASSED', 'FAILED') and not (notes['tests_run'] and notes['test_results']):
            raise PreservationError()
        if test == 'FAILED' and not notes['known_failures']: raise PreservationError()
        if test == 'SKIPPED' and not notes['limitations']: raise PreservationError()
        e = record['evidence']
        if type(e) is not dict or set(e) != set(DIGESTS + COMMITS + ('unsafe_target', 'push_attempted', 'publication_error')):
            raise PreservationError()
        for key in DIGESTS + COMMITS:
            value = e[key]
            pattern = '[0-9a-f]{64}' if key in DIGESTS else '(?:[0-9a-f]{40}|[0-9a-f]{64})'
            if value is not None and (not isinstance(value, str) or not re.fullmatch(pattern, value)):
                raise PreservationError()
        if type(e['unsafe_target']) is not bool or type(e['push_attempted']) is not bool:
            raise PreservationError()
        if e['publication_error'] is not None and e['publication_error'] not in PUBLICATION_ERRORS:
            raise PreservationError()
        if (e['handoff_digest'] or e['local_commit']) and not e['inspection_digest']: raise PreservationError()
        if e['resume_digest'] and not e['handoff_digest']: raise PreservationError()
        refs = [e[k] for k in COMMITS if e[k] is not None]
        if len(set(refs)) > 1 and e['publication_error'] != 'VERIFICATION_MISMATCH':
            raise PreservationError()
        if (e['remote_commit'] or e['tracking_commit']) and not e['local_commit']:
            raise PreservationError()
        if record['requested_level'] != 'REMOTE_VERIFIED' and (e['push_attempted'] or e['publication_error'] or e['remote_commit'] or e['tracking_commit']):
            raise PreservationError()
        if e['publication_error'] and e['remote_commit'] == e['tracking_commit'] == e['local_commit'] and e['local_commit']:
            raise PreservationError()
        expected = _derived(record)
        if json.dumps({k: record[k] for k in DERIVED}, sort_keys=True) != json.dumps(expected, sort_keys=True):
            raise PreservationError()
        if len(json.dumps(record, ensure_ascii=True, allow_nan=False).encode()) > MAX_RECORD_BYTES:
            raise PreservationError()
        return copy.deepcopy(record)
    except (KeyError, TypeError, ValueError, RecursionError, OverflowError):
        raise PreservationError() from None


def new_attempt(project, *, now, mission, next_exact_action, requested_level='HANDOFF_ONLY', trigger='MANUAL'):
    record = {'schema_version': SCHEMA_VERSION, 'project_request': project,
              'project_basis': 'OPERATOR_REQUESTED', 'trigger': trigger,
              'requested_level': requested_level, 'evidence_basis': 'SYNTHETIC' if trigger == 'SYNTHETIC' else 'ADAPTER_REPORTED',
              'phase': 'INSPECTING', 'events': [{'phase': 'INSPECTING', 'at': _stamp(now)}],
              'evidence': dict.fromkeys(DIGESTS + COMMITS), 'project_test_status': 'UNKNOWN',
              'notes': {k: [] for k in NOTE_LISTS}}
    record['notes'].update(mission=mission, next_exact_action=next_exact_action)
    record['evidence'].update(unsafe_target=False, push_attempted=False, publication_error=None)
    record.update(_derived(record))
    return validate_record(record)


def advance(record, phase, *, now, evidence=None, test_status=None, notes=None):
    """Produce a new record; caller retains previous valid record on any rejection."""
    if not isinstance(phase, str) or phase not in set(NEXT) | TERMINAL:
        raise PreservationError()
    result = validate_record(record)
    if evidence is not None:
        if type(evidence) is not dict or not set(evidence) <= set(result['evidence']): raise PreservationError()
        for key, value in evidence.items():
            previous = result['evidence'][key]
            if previous not in (None, False) and previous != value: raise PreservationError()
        result['evidence'].update(copy.deepcopy(evidence))
    if notes is not None:
        if type(notes) is not dict or not set(notes) <= set(result['notes']): raise PreservationError()
        result['notes'].update(copy.deepcopy(notes))
    if test_status is not None: result['project_test_status'] = test_status
    result['phase'] = phase
    result['events'].append({'phase': phase, 'at': _stamp(now)})
    result.update(_derived(result))
    return validate_record(result)


def render_json(record):
    return json.dumps(validate_record(record), ensure_ascii=True, sort_keys=True, allow_nan=False)


def render_human(record):
    record = validate_record(record)
    # Quote all data, including paths and notes, so it cannot impersonate report headings.
    return '\n'.join(['CREDID GUARDIAN CODEX (CGC) — preservation record'] +
                     [key.upper() + ': ' + json.dumps(value, ensure_ascii=True, sort_keys=True)
                      for key, value in record.items()])
