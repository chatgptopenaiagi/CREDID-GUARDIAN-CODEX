"""CGC canonical state and pure policy. No I/O or preservation actions."""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import math
import json

from .quota import normalize, QuotaError, _identifier, ERRORS

POLICY_VERSION = 'cgc-applicability-v2.2'
SCHEMA_VERSION = 'cgc-state-v2.3'
MAX_AGE = 900
STATE_ERRORS = {'INVALID_STATE', 'NO_USABLE_DATA', 'MODE_MISMATCH', 'STALE_OBSERVATION', 'USAGE_BLOCKED'}
DIRECTIVES = {
    'GREEN': 'Continue authorized development. Coverage remains limited to selected observed windows.',
    'AMBER': 'Continue with awareness; consider checkpoint readiness.',
    'RED': 'Stop starting major work; prepare a resumable checkpoint only under current authorization.',
    'EMERGENCY': 'Stop development; minimum safe preservation only under current authorization.',
}


class StateError(Exception):
    def __init__(self, code='INVALID_STATE'):
        self.code = code
        super().__init__(code)


def timestamp(value):
    try:
        if not isinstance(value, str) or len(value) > 40:
            raise ValueError()
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if result.tzinfo is None:
            raise ValueError()
        return result.astimezone(timezone.utc)
    except (ValueError, TypeError, OverflowError):
        raise StateError() from None


def utcnow():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def percentage(value):
    if type(value) not in (int, float) or not 0 <= value <= 100 or not math.isfinite(value):
        raise StateError()
    return value


@dataclass(frozen=True)
class PolicyConfig:
    """Inclusive upper boundaries; strict ordering keeps every band meaningful."""
    amber_at: float = 20
    red_at: float = 10
    emergency_at: float = 5

    def __post_init__(self):
        for value in (self.amber_at, self.red_at, self.emergency_at):
            percentage(value)
        if not self.emergency_at < self.red_at < self.amber_at:
            raise StateError('INVALID_CONFIG')

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, value):
        if not isinstance(value, dict) or set(value) != {'amber_at', 'red_at', 'emergency_at'}:
            raise StateError('INVALID_CONFIG')
        return cls(**value)


DEFAULT_POLICY = PolicyConfig()


def classify(value, config=DEFAULT_POLICY):
    value = percentage(value)
    return ('GREEN' if value > config.amber_at else
            'AMBER' if value > config.red_at else
            'RED' if value > config.emergency_at else 'EMERGENCY')


def selection(buckets):
    try:
        if not isinstance(buckets, list) or not 1 <= len(buckets) <= 32:
            raise StateError()
        result = sorted({_identifier(b) for b in buckets})
        if len(result) != len(buckets):
            raise StateError()
        return result
    except QuotaError:
        raise StateError() from None


def validate_observation(obs):
    """Reconstruct V1 allowlisted semantics; require exact canonical projection.

    This rejects injected fields, altered provenance, conflicting values and forged
    validity labels without exporting any arbitrary cached string.
    """
    try:
        if not isinstance(obs, dict) or not isinstance(obs.get('buckets'), list):
            raise StateError()
        buckets = obs['buckets']
        if not 1 <= len(buckets) <= 32 or len(set(buckets)) != len(buckets):
            raise StateError()
        raw = {'rateLimits': {}, 'rateLimitsByLimitId': {b: {} for b in buckets},
               'ordinaryUsageAllowed': obs['ordinary_usage_allowed']}
        windows = obs['windows']
        if not isinstance(windows, list) or len(windows) > 96:
            raise StateError()
        for w in windows:
            kind = {'primary': 'primary', 'secondary': 'secondary', 'individual_limit': 'individualLimit'}[w['window_kind']]
            bucket = raw['rateLimitsByLimitId'][w['bucket_id']]
            if kind in bucket:
                raise StateError()
            item = {'resetsAt': int(timestamp(w['reset_at']).timestamp()) if w['reset_at'] is not None else None}
            if kind == 'individualLimit':
                item['remainingPercent'] = w['remaining_percent']
            else:
                duration = w['duration_seconds']
                if duration is not None and (type(duration) is not int or duration % 60):
                    raise StateError()
                item.update(usedPercent=w['used_percent'], windowDurationMins=duration // 60 if duration is not None else None)
            bucket[kind] = item
        canonical = normalize(raw, observed_at=obs['observed_at'], mode=obs['mode'])
        # JSON equality must distinguish booleans from integers.
        if json.dumps(canonical, sort_keys=True, allow_nan=False) != json.dumps(obs, sort_keys=True, allow_nan=False):
            raise StateError()
        return canonical
    except (KeyError, TypeError, ValueError, OverflowError, QuotaError):
        raise StateError() from None


def applicability_evidence(obs, entries):
    """Bounded evidence for this exact observation; no live contract is established.

    Synthetic assertions describe test facts only. No operator flag, bucket name,
    duration, value or ordinary-usage allowance can promote a live window.
    """
    if entries == ():
        entries = []
    if not isinstance(entries, list) or len(entries) > 96:
        raise StateError('INVALID_EVIDENCE')
    windows = {w['window_id'] for w in obs['windows']} if obs else set()
    result = {}
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {'window_id', 'applicability', 'basis', 'observed_at'}:
            raise StateError('INVALID_EVIDENCE')
        identity = entry['window_id']
        if (not isinstance(identity, str) or identity not in windows or identity in result
                or entry['applicability'] not in ('APPLICABLE', 'NOT_APPLICABLE', 'UNKNOWN')
                or entry['basis'] != 'SYNTHETIC_CONTRACT'
                or obs['mode'] != 'synthetic' or entry['observed_at'] != obs['observed_at']):
            raise StateError('INVALID_EVIDENCE')
        result[identity] = dict(entry)
    return [result[key] for key in sorted(result)]


def policy(obs, buckets, config=DEFAULT_POLICY, *, evidence=()):
    buckets = selection(buckets)
    if obs is not None:
        validate_observation(obs)
    evidence = applicability_evidence(obs, evidence)
    facts = {entry['window_id']: entry for entry in evidence}
    diagnostics = []
    for w in sorted(obs['windows'] if obs else [], key=lambda w: w['window_id']):
        fact = facts.get(w['window_id'])
        applies = fact['applicability'] if fact else 'UNKNOWN'
        selected = w['bucket_id'] in buckets
        exclusions = []
        if not selected:
            exclusions.append('OUTSIDE_SELECTED_SCOPE')
        if applies != 'APPLICABLE':
            exclusions.append('NOT_APPLICABLE' if applies == 'NOT_APPLICABLE' else 'UNKNOWN_APPLICABILITY')
        if w['validity'] != 'VALID':
            exclusions.append('INVALID_VALUE' if w['validity'] == 'INVALID' else 'UNKNOWN_VALUE')
        diagnostics.append({'window_id': w['window_id'], 'bucket_id': w['bucket_id'],
                            'selected': selected, 'applicability': applies,
                            'evidence_basis': fact['basis'] if fact else 'NO_EVIDENCE',
                            'validity': w['validity'], 'remaining_percent': w['remaining_percent'],
                            'exclusion_reasons': exclusions})
    usable = [w for w in diagnostics if not w['exclusion_reasons']]
    minimum = min((percentage(w['remaining_percent']) for w in usable), default=None)
    state = classify(minimum, config) if minimum is not None else None
    return {'policy_version': POLICY_VERSION, 'thresholds': config.to_dict(), 'selected_buckets': buckets,
            'applicability_basis': 'per_window_evidence', 'evidence': evidence,
            'window_diagnostics': diagnostics,
            'coverage': 'PARTIAL' if usable else 'UNKNOWN',
            'missing_buckets': sorted(set(buckets) - {w['bucket_id'] for w in diagnostics}),
            'usable_windows': len(usable), 'selected_windows': sum(w['selected'] for w in diagnostics),
            'most_constrained_remaining_percent': minimum, 'policy_state': state,
            'limiting_window_ids': [w['window_id'] for w in usable if w['remaining_percent'] == minimum],
            'reason': ('MINIMUM_KNOWN_APPLICABLE_SELECTED_WINDOW' if usable else
                       'NO_KNOWN_APPLICABLE_USABLE_WINDOW'),
            'directive': DIRECTIVES.get(state), 'global_all_clear': False}


def validate_max_age(value):
    if type(value) is not int or not 1 <= value <= 86400:
        raise StateError('INVALID_CONFIG')
    return value


def freshness(observed_at, *, now, max_age=MAX_AGE):
    """Age of local observation, independent of refresh health or applicability."""
    validate_max_age(max_age)
    result = {'state': 'UNKNOWN', 'age_seconds': None, 'observed_at': None,
              'evaluated_at': None, 'max_age_seconds': max_age,
              'basis': 'LOCAL_OBSERVATION_TIME', 'reason': 'NO_OBSERVATION_TIME'}
    try:
        current = timestamp(now)
        result['evaluated_at'] = current.isoformat().replace('+00:00', 'Z')
        if observed_at is None:
            return result
        observed = timestamp(observed_at)
        result['observed_at'] = observed.isoformat().replace('+00:00', 'Z')
        age = (current - observed).total_seconds()
        result['age_seconds'] = age
        if age < 0:
            result.update(state='ERROR', reason='FUTURE_OBSERVATION')
        elif age > max_age:
            result.update(state='STALE', reason='MAX_AGE_EXCEEDED')
        else:
            result.update(state='FRESH', reason='WITHIN_MAX_AGE')
    except StateError:
        result.update(state='ERROR', reason='INVALID_TIMESTAMP')
    return result


def temporal_state(state, *, now):
    """Reconstructed write-time snapshot or read-time assessment; no cached authority."""
    obs, good = state['last_observation'], state['last_valid_observation']
    latest = freshness(obs['observed_at'] if obs else None, now=now,
                       max_age=state['max_age_seconds'])
    historical = freshness(good['observed_at'] if good else None, now=now,
                           max_age=state['max_age_seconds'])
    if now is None and state['generation'] == 0:
        for item in (latest, historical):
            item.update(state='UNKNOWN', reason='NOT_EVALUATED')
    elif state['cache_written_at'] and timestamp(now) < timestamp(state['cache_written_at']):
        latest.update(state='ERROR', reason='CLOCK_BEFORE_CACHE_WRITE')
        historical.update(state='ERROR', reason='CLOCK_BEFORE_CACHE_WRITE')
    fresh = latest['state'] == 'FRESH'
    failed = state['last_refresh_status'] != 'OK'
    available = (fresh and not failed and state['policy']['policy_state'] is not None
                 and obs['ordinary_usage_allowed'] is not False)
    disposition = ('UNAVAILABLE' if obs is None else
                   'HISTORICAL' if latest['state'] == 'STALE' else
                   'RETAINED' if not fresh or (failed and state['error_code'] != 'NO_USABLE_DATA') else 'CURRENT')
    return {'evaluated_at': latest['evaluated_at'], 'freshness': latest['state'],
            'observation_freshness': latest, 'last_known_good_freshness': historical,
            'data_disposition': disposition, 'policy_available': bool(available)}


def provenance(obs, disposition):
    """Value origin and storage role are separate axes; preserve V1 projection unchanged."""
    origins = {'direct': 'DIRECT', 'derived': 'DERIVED', 'unknown': 'UNAVAILABLE'}
    return {'disposition': disposition if obs else 'UNAVAILABLE',
            'source_kind': obs['source_kind'] if obs else None,
            'source_maturity': obs['source_maturity'] if obs else None,
            'observed_at': obs['observed_at'] if obs else None,
            'observation_time_origin': obs['observation_time_origin'] if obs else 'UNAVAILABLE',
            'source_observed_at': obs['source_observed_at'] if obs else None,
            'source_time_origin': 'UNAVAILABLE',
            'windows': [{'window_id': w['window_id'],
                         'used_percent': origins[w['used_percent_origin']],
                         'remaining_percent': origins[w['value_origin']],
                         'duration_seconds': 'DERIVED' if w['duration_seconds'] is not None else 'UNAVAILABLE',
                         'reset_at': 'DERIVED' if w['reset_at'] is not None else 'UNAVAILABLE'}
                        for w in (obs['windows'] if obs else [])]}


def empty_state(buckets, max_age=MAX_AGE, *, config=DEFAULT_POLICY):
    validate_max_age(max_age)
    state = {'schema_version': SCHEMA_VERSION, 'generation': 0,
            'max_age_seconds': max_age, 'last_valid_observation': None,
            'last_observation': None, 'last_valid_policy': None,
            'policy': policy(None, buckets, config), 'last_refresh_attempt_at': None,
            'last_refresh_status': 'NEVER', 'error_code': None, 'cache_written_at': None}
    state['temporal'] = temporal_state(state, now=None)
    return state


def refresh(previous, result, *, now, evidence=()):
    validate_state(previous)
    now = timestamp(now).isoformat().replace('+00:00', 'Z')
    if previous['cache_written_at'] and timestamp(now) < timestamp(previous['cache_written_at']):
        raise StateError('CLOCK_REGRESSION')
    state = dict(previous)
    state.update(generation=previous['generation'] + 1,
                 last_refresh_attempt_at=now, cache_written_at=now)
    try:
        obs = validate_observation(result)
        if timestamp(obs['observed_at']) > timestamp(now):
            raise StateError()
        if previous['last_observation'] and timestamp(obs['observed_at']) < timestamp(previous['last_observation']['observed_at']):
            raise StateError()
        if previous['last_observation'] and obs['mode'] != previous['last_observation']['mode']:
            raise StateError('MODE_MISMATCH')
        p = policy(obs, previous['policy']['selected_buckets'],
                   PolicyConfig.from_dict(previous['policy']['thresholds']), evidence=evidence)
        state.update(last_observation=obs, policy=p)
        if p['policy_state'] is None:
            raise StateError('NO_USABLE_DATA')
        if freshness(obs['observed_at'], now=now, max_age=state['max_age_seconds'])['state'] != 'FRESH':
            raise StateError('STALE_OBSERVATION')
        if obs['ordinary_usage_allowed'] is False:
            raise StateError('USAGE_BLOCKED')
        state.update(last_valid_observation=obs, last_valid_policy=p,
                     last_refresh_status='OK', error_code=None)
    except StateError as error:
        code = error.code
        if isinstance(result, dict) and result.get('status') == 'ERROR':
            code = result.get('error_code')
        if not isinstance(code, str) or code not in ERRORS | STATE_ERRORS:
            code = 'INVALID_STATE'
        state.update(last_refresh_status='ERROR', error_code=code)
    state['temporal'] = temporal_state(state, now=now)
    validate_state(state)
    return state


def _same_json(left, right):
    return json.dumps(left, sort_keys=True, allow_nan=False) == json.dumps(right, sort_keys=True, allow_nan=False)


def validate_state(state):
    try:
        if not isinstance(state, dict) or state.get('schema_version') != SCHEMA_VERSION:
            raise StateError()
        config = PolicyConfig.from_dict(state['policy']['thresholds'])
        buckets = state['policy']['selected_buckets']
        template = empty_state(buckets, state['max_age_seconds'], config=config)
        if set(state) != set(template) or type(state['generation']) is not int or not 0 <= state['generation'] <= 10**12:
            raise StateError()
        obs = state['last_observation']
        good = state['last_valid_observation']
        for observation, evaluation in ((obs, state['policy']), (good, state['last_valid_policy'])):
            if evaluation is None:
                if observation is not None:
                    raise StateError()
                continue
            expected = policy(observation, buckets, config, evidence=evaluation['evidence'])
            if not _same_json(evaluation, expected):
                raise StateError()
        if good is None:
            if state['last_valid_policy'] is not None:
                raise StateError()
        else:
            if (obs is None or state['last_valid_policy']['policy_state'] is None
                    or good['mode'] != obs['mode']
                    or timestamp(good['observed_at']) > timestamp(obs['observed_at'])):
                raise StateError()
        if state['last_refresh_status'] == 'OK':
            if not _same_json(obs, good) or not _same_json(state['policy'], state['last_valid_policy']):
                raise StateError()
        if state['generation'] == 0:
            if not _same_json(state, template):
                raise StateError()
        else:
            written = timestamp(state['cache_written_at'])
            if timestamp(state['last_refresh_attempt_at']) != written:
                raise StateError()
            if obs and timestamp(obs['observed_at']) > written:
                raise StateError()
            if state['last_refresh_status'] == 'OK':
                if state['policy']['policy_state'] is None or state['error_code'] is not None:
                    raise StateError()
            elif state['last_refresh_status'] != 'ERROR' or state['error_code'] not in ERRORS | STATE_ERRORS:
                raise StateError()
        expected_temporal = temporal_state(state, now=state['cache_written_at'])
        if not _same_json(state['temporal'], expected_temporal):
            raise StateError()
        if state['last_refresh_status'] == 'OK' and not expected_temporal['policy_available']:
            raise StateError()
        return state
    except (KeyError, TypeError, ValueError, RecursionError):
        raise StateError() from None


def status(state, *, now):
    validate_state(state)
    now = timestamp(now).isoformat().replace('+00:00', 'Z')
    temporal = temporal_state(state, now=now)
    obs = state['last_observation']
    age = temporal['observation_freshness']['age_seconds']
    validity = {'FRESH': 'VALID', 'STALE': 'STALE', 'UNKNOWN': 'UNKNOWN', 'ERROR': 'CLOCK_SKEW'}[temporal['freshness']]
    if validity == 'VALID' and obs['ordinary_usage_allowed'] is False:
        validity = 'USAGE_BLOCKED'
    available = temporal['policy_available']
    p = state['policy']
    return {**temporal, 'schema_version': SCHEMA_VERSION, 'generation': state['generation'],
            'provenance': {'latest': provenance(obs, temporal['data_disposition']),
                           'last_known_good': provenance(state['last_valid_observation'], 'HISTORICAL')},
            'validity': validity, 'age_seconds': age, 'mode': obs['mode'] if obs else None,
            'policy_state': p['policy_state'] if available else None,
            'directive': p['directive'] if available and obs['mode'] == 'live' else None,
            'historical_policy': state['last_valid_policy'] or p,
            'evaluated_policy': p,
            'limiting_window_ids': p['limiting_window_ids'] if available else [],
            'most_constrained_remaining_percent': p['most_constrained_remaining_percent'] if available else None,
            'reason': p['reason'] if available or p['policy_state'] is None else 'CURRENT_POLICY_UNAVAILABLE',
            'last_valid_observation': state['last_valid_observation'], 'coverage': p['coverage'], 'global_all_clear': False,
            'last_refresh_status': state['last_refresh_status'], 'error_code': state['error_code'],
            'live_policy_available': available and obs['mode'] == 'live',
            'observation': obs}
