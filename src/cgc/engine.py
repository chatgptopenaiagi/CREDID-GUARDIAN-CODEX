"""CGC canonical state and pure policy. No I/O or preservation actions."""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import math
import json

from .quota import normalize, QuotaError, _identifier, ERRORS

POLICY_VERSION = 'cgc-thresholds-v2.1'
SCHEMA_VERSION = 'cgc-state-v2.1'
MAX_AGE = 900
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


def policy(obs, buckets, config=DEFAULT_POLICY):
    buckets = selection(buckets)
    selected = [w for w in obs['windows'] if w['bucket_id'] in buckets] if obs else []
    usable = [w for w in selected if w['validity'] == 'VALID']
    minimum = min((percentage(w['remaining_percent']) for w in usable), default=None)
    state = classify(minimum, config) if minimum is not None else None
    return {'policy_version': POLICY_VERSION, 'thresholds': config.to_dict(), 'selected_buckets': buckets,
            'applicability_basis': 'explicit_operator_selection',
            'coverage': 'PARTIAL' if usable else 'UNKNOWN',
            'missing_buckets': sorted(set(buckets) - {w['bucket_id'] for w in selected}),
            'usable_windows': len(usable), 'selected_windows': len(selected),
            'most_constrained_remaining_percent': minimum, 'policy_state': state,
            'directive': DIRECTIVES.get(state), 'global_all_clear': False}


def empty_state(buckets, max_age=MAX_AGE, *, config=DEFAULT_POLICY):
    if type(max_age) is not int or not 1 <= max_age <= 86400:
        raise StateError()
    return {'schema_version': SCHEMA_VERSION, 'generation': 0,
            'max_age_seconds': max_age, 'last_valid_observation': None,
            'policy': policy(None, buckets, config), 'last_refresh_attempt_at': None,
            'last_refresh_status': 'NEVER', 'error_code': None, 'cache_written_at': None}


def refresh(previous, result, *, now):
    validate_state(previous)
    timestamp(now)
    state = dict(previous)
    state.update(generation=previous['generation'] + 1,
                 last_refresh_attempt_at=now, cache_written_at=now)
    try:
        obs = validate_observation(result)
        if timestamp(obs['observed_at']) > timestamp(now):
            raise StateError()
        if previous['last_valid_observation'] and timestamp(obs['observed_at']) < timestamp(previous['last_valid_observation']['observed_at']):
            raise StateError()
        if previous['last_valid_observation'] and obs['mode'] != previous['last_valid_observation']['mode']:
            raise StateError('MODE_MISMATCH')
        p = policy(obs, previous['policy']['selected_buckets'],
                   PolicyConfig.from_dict(previous['policy']['thresholds']))
        if p['policy_state'] is None:
            raise StateError('NO_USABLE_DATA')
        state.update(last_valid_observation=obs, policy=p, last_refresh_status='OK', error_code=None)
    except StateError as error:
        code = error.code
        if isinstance(result, dict) and result.get('status') == 'ERROR':
            code = result.get('error_code')
        if not isinstance(code, str) or code not in ERRORS | {'MODE_MISMATCH', 'NO_USABLE_DATA'}:
            code = 'INVALID_STATE'
        state.update(last_refresh_status='ERROR', error_code=code)
    validate_state(state)
    return state


def validate_state(state):
    try:
        if not isinstance(state, dict) or state.get('schema_version') != SCHEMA_VERSION:
            raise StateError()
        config = PolicyConfig.from_dict(state['policy']['thresholds'])
        template = empty_state(state['policy']['selected_buckets'], state['max_age_seconds'], config=config)
        if set(state) != set(template) or type(state['generation']) is not int or not 0 <= state['generation'] <= 10**12:
            raise StateError()
        obs = state['last_valid_observation']
        if obs is not None:
            validate_observation(obs)
        if json.dumps(state['policy'], sort_keys=True, allow_nan=False) != json.dumps(policy(obs, state['policy']['selected_buckets'], config), sort_keys=True, allow_nan=False):
            raise StateError()
        if obs is not None and state['policy']['policy_state'] is None:
            raise StateError()
        if state['generation'] == 0:
            if state != template:
                raise StateError()
        else:
            written = timestamp(state['cache_written_at'])
            if timestamp(state['last_refresh_attempt_at']) != written:
                raise StateError()
            if obs and timestamp(obs['observed_at']) > written:
                raise StateError()
            if state['last_refresh_status'] == 'OK':
                if obs is None or state['error_code'] is not None:
                    raise StateError()
            elif state['last_refresh_status'] != 'ERROR' or state['error_code'] not in ERRORS | {'INVALID_STATE', 'NO_USABLE_DATA', 'MODE_MISMATCH'}:
                raise StateError()
        return state
    except (KeyError, TypeError, ValueError, RecursionError):
        raise StateError() from None


def status(state, *, now):
    validate_state(state)
    current = timestamp(now)
    obs = state['last_valid_observation']
    age = (current - timestamp(obs['observed_at'])).total_seconds() if obs else None
    skew = (age is not None and age < 0) or (state['cache_written_at'] is not None and current < timestamp(state['cache_written_at']))
    validity = 'CLOCK_SKEW' if skew else 'UNKNOWN' if age is None else 'STALE' if age > state['max_age_seconds'] else 'VALID'
    if validity == 'VALID' and obs['ordinary_usage_allowed'] is False:
        validity = 'USAGE_BLOCKED'
    available = validity == 'VALID'
    p = state['policy']
    return {'schema_version': SCHEMA_VERSION, 'generation': state['generation'],
            'validity': validity, 'age_seconds': age, 'mode': obs['mode'] if obs else None,
            'policy_state': p['policy_state'] if available else None,
            'directive': p['directive'] if available and obs['mode'] == 'live' else None,
            'historical_policy': p, 'coverage': p['coverage'], 'global_all_clear': False,
            'last_refresh_status': state['last_refresh_status'], 'error_code': state['error_code'],
            'live_policy_available': available and obs['mode'] == 'live',
            'observation': obs}
