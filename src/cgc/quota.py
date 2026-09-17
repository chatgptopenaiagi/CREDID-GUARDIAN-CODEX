"""CREDID GUARDIAN CODEX (CGC): bounded, read-only app-server quota reader.

No auth-file access, direct HTTP, AI turns, polling, cache or preservation actions.
"""
from datetime import datetime, timezone
import json
import math
import os
import re
import selectors
import signal
import subprocess
import time

SOURCE = 'codex app-server: account/rateLimits/read'
MAX_BYTES = 524288
MAX_FRAME = 131072
MAX_BUCKETS = 32
ERRORS = {'SOURCE_ERROR', 'TIMEOUT', 'SOURCE_CLOSED', 'OUTPUT_LIMIT', 'FRAME_LIMIT',
          'FRAME_COUNT_LIMIT', 'MALFORMED_INPUT', 'SENSITIVE_FIELD_REJECTED',
          'SERVER_REQUEST_REFUSED', 'UNSUPPORTED_PLATFORM', 'START_FAILED',
          'SHUTDOWN_FAILED', 'IDENTITY_CONFLICT'}


class QuotaError(Exception):
    """Fixed diagnostics only: never echo source messages, keys or values."""
    def __init__(self, code):
        self.code = code if code in ERRORS else 'MALFORMED_INPUT'
        super().__init__(self.code)


def _utc():
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def _check_sensitive(data):
    sensitive = {'authorization', 'accesstoken', 'refreshtoken', 'idtoken', 'apikey',
                 'cookie', 'cookies', 'password', 'sessionsecret', 'bearertoken',
                 'clientsecret', 'authtoken', 'token', 'secret', 'setcookie'}
    count = 0
    def visit(value, depth):
        nonlocal count
        count += 1
        if depth > 24 or count > 10000:
            raise QuotaError('MALFORMED_INPUT')
        if isinstance(value, dict):
            for key, item in value.items():
                if not isinstance(key, str): raise QuotaError('MALFORMED_INPUT')
                if re.sub('[^a-z]', '', key.lower()) in sensitive:
                    raise QuotaError('SENSITIVE_FIELD_REJECTED')
                visit(item, depth + 1)
        elif isinstance(value, list):
            for item in value: visit(item, depth + 1)
    visit(data, 0)


def _identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,63}', value):
        raise QuotaError('MALFORMED_INPUT')
    if re.search(r'(?i)(bearer|gh[pousr]_|github_pat_|hf_|sk-|token|secret)', value):
        raise QuotaError('SENSITIVE_FIELD_REJECTED')
    return value


def _integer(value, *, minimum=None, maximum=None):
    if value is None: return None
    if type(value) is not int or (minimum is not None and value < minimum) or (maximum is not None and value > maximum):
        raise QuotaError('MALFORMED_INPUT')
    return value


def _window(raw, bucket_id, kind):
    if not isinstance(raw, dict): raise QuotaError('MALFORMED_INPUT')
    individual = kind == 'individual_limit'
    used = None if individual else _integer(raw.get('usedPercent'))
    # The installed schema supplies direct remainingPercent only for individualLimit.
    direct = _integer(raw.get('remainingPercent'), minimum=0, maximum=100) if individual else None
    minutes = None if individual else _integer(raw.get('windowDurationMins'), minimum=1, maximum=5256000)
    resets = _integer(raw.get('resetsAt'), minimum=0, maximum=253402300799)
    try:
        reset_at = datetime.fromtimestamp(resets, timezone.utc).isoformat().replace('+00:00', 'Z') if resets is not None else None
    except (ValueError, OverflowError, OSError):
        raise QuotaError('MALFORMED_INPUT') from None
    value = direct if individual else (100 - used if used is not None else None)
    remaining = max(0, min(100, value)) if value is not None else None
    origin = 'unknown' if value is None else 'direct' if individual else 'derived'
    invalid = (used is not None and not 0 <= used <= 100) or (direct is not None and not 0 <= direct <= 100)
    return {
        'window_id': bucket_id + ':' + kind, 'bucket_id': bucket_id,
        'name': '5-hour' if minutes == 300 else 'weekly' if minutes == 10080 else 'UNKNOWN',
        'window_kind': kind, 'duration_seconds': minutes * 60 if minutes is not None else None,
        'used_percent': used, 'used_percent_origin': 'direct' if used is not None else 'unknown',
        'remaining_percent': remaining, 'value_origin': origin,
        'derivation': 'clamp(100 - usedPercent, 0, 100)' if origin == 'derived' else None,
        'clamped': value is not None and remaining != value,
        'reset_at': reset_at, 'reset_origin': 'derived_from_unix_seconds' if resets is not None else 'unknown',
        'validity': 'INVALID' if invalid else 'UNKNOWN' if remaining is None else 'VALID',
    }


def normalize(raw, *, observed_at, mode='live'):
    """Project an app-server result into quota-only data; raw response is not retained.

    Remaining is clamped per the V1 task. Out-of-range source values are also marked
    INVALID so clamping cannot manufacture trustworthy policy input.
    """
    if mode not in ('live', 'synthetic'): raise ValueError('invalid observation mode')
    try:
        stamp = datetime.fromisoformat(observed_at.replace('Z', '+00:00'))
        if stamp.tzinfo is None: raise ValueError()
    except (ValueError, TypeError, AttributeError):
        raise QuotaError('MALFORMED_INPUT') from None
    if not isinstance(raw, dict) or not isinstance(raw.get('rateLimits'), dict):
        raise QuotaError('MALFORMED_INPUT')
    _check_sensitive(raw)
    mapping = raw.get('rateLimitsByLimitId')
    if mapping is not None and not isinstance(mapping, dict): raise QuotaError('MALFORMED_INPUT')
    # Prefer the full mapping. An empty mapping falls back to the legacy view.
    buckets = mapping or {raw['rateLimits'].get('limitId') or 'legacy-unidentified': raw['rateLimits']}
    if len(buckets) > MAX_BUCKETS: raise QuotaError('MALFORMED_INPUT')
    windows, identities = [], []
    for key, bucket in buckets.items():
        key = _identifier(key)
        if not isinstance(bucket, dict): raise QuotaError('MALFORMED_INPUT')
        claimed_id = bucket.get('limitId')
        if claimed_id is not None and _identifier(claimed_id) != key:
            raise QuotaError('IDENTITY_CONFLICT')
        identities.append(key)
        for source_key, kind in [('primary', 'primary'), ('secondary', 'secondary'), ('individualLimit', 'individual_limit')]:
            if bucket.get(source_key) is not None:
                windows.append(_window(bucket[source_key], key, kind))
    permitted = raw.get('ordinaryUsageAllowed')
    if permitted is not None and type(permitted) is not bool: raise QuotaError('MALFORMED_INPUT')
    usable = [w for w in windows if w['validity'] == 'VALID']
    return {
        'schema_version': '0.1.0-provisional', 'mode': mode,
        'observed_at': stamp.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z'),
        'observation_time_origin': 'local_read_completion', 'source_observed_at': None,
        'source': SOURCE, 'source_kind': 'codex_app_server', 'source_supported': True,
        'source_maturity': 'experimental', 'source_confidence': 'SYNTHETIC' if mode == 'synthetic' else 'DOCUMENTED_LOCAL_PROTOCOL',
        'status': 'OK' if windows and len(usable) == len(windows) else 'PARTIAL' if usable else 'UNKNOWN',
        'coverage': 'UNKNOWN', 'buckets': identities, 'windows': windows,
        'ordinary_usage_allowed': permitted,
        'limitations': ['Backend observation age is unavailable.',
                        'Coverage is limited to recognized fields in returned buckets.',
                        'Bucket applicability is not inferred; no global policy state is calculated.'],
    }


def _decode(line):
    def reject_constant(_): raise QuotaError('MALFORMED_INPUT')
    def unique_pairs(pairs):
        out = {}
        for key, value in pairs:
            if key in out: raise QuotaError('MALFORMED_INPUT')
            out[key] = value
        return out
    try:
        obj = json.loads(line, parse_constant=reject_constant, object_pairs_hook=unique_pairs)
    except (ValueError, UnicodeError, RecursionError):
        raise QuotaError('MALFORMED_INPUT') from None
    if not isinstance(obj, dict): raise QuotaError('MALFORMED_INPUT')
    return obj


def _exchange(send, receive):
    """Exactly one initialized connection and one read, no retry or AI request."""
    send({'id': 1, 'method': 'initialize', 'params': {
        'clientInfo': {'name': 'cgc', 'title': 'CREDID GUARDIAN CODEX', 'version': '0.1.0'},
        'capabilities': {'experimentalApi': False}}})
    def response(request_id):
        for _ in range(100):
            msg = receive()
            if not isinstance(msg, dict): raise QuotaError('MALFORMED_INPUT')
            if 'method' in msg and 'id' in msg:
                # Never answer token refresh/attestation or execute server requests.
                raise QuotaError('SERVER_REQUEST_REFUSED')
            if type(msg.get('id')) is int and msg['id'] == request_id:
                if 'error' in msg: raise QuotaError('SOURCE_ERROR')
                if 'result' not in msg: raise QuotaError('MALFORMED_INPUT')
                return msg['result']
            # Notifications and unrelated data are discarded, not persisted.
        raise QuotaError('FRAME_COUNT_LIMIT')
    response(1)  # Initialization response may contain local identity/path: discard it.
    send({'method': 'initialized', 'params': {}})
    send({'id': 2, 'method': 'account/rateLimits/read', 'params': {
        'excludeResetCreditDetails': True, 'supportsLunaReserve': False}})
    return response(2)


def _validate_timeout(timeout):
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or not 0 < timeout <= 30:
        raise ValueError('timeout must be finite and between 0 and 30 seconds')


def app_server_read(timeout=20):
    """One transient stdio connection. POSIX only in V1; no daemon installed.

    Authentication is owned by the installed Codex process. Its environment is
    inherited without CGC reading values. No credential arguments or config copies.
    """
    _validate_timeout(timeout)
    if os.name != 'posix': raise QuotaError('UNSUPPORTED_PLATFORM')
    deadline = time.monotonic() + timeout
    try:
        proc = subprocess.Popen(['codex', 'app-server', '--listen', 'stdio://', '-c', 'analytics.enabled=false'],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                start_new_session=True)
    except OSError:
        raise QuotaError('START_FAILED') from None
    selector = selectors.DefaultSelector()
    selector.register(proc.stdout, selectors.EVENT_READ, 'stdout')
    selector.register(proc.stderr, selectors.EVENT_READ, 'stderr')
    buffer = bytearray()
    total, frames = 0, 0
    def send(msg):
        if time.monotonic() >= deadline: raise QuotaError('TIMEOUT')
        try:
            proc.stdin.write((json.dumps(msg) + '\n').encode())
            proc.stdin.flush()
        except OSError: raise QuotaError('SOURCE_CLOSED') from None
    def receive():
        nonlocal total, frames
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0: raise QuotaError('TIMEOUT')
            if b'\n' in buffer:
                line, _, rest = buffer.partition(b'\n')
                buffer[:] = rest
                frames += 1
                if frames > 100: raise QuotaError('FRAME_COUNT_LIMIT')
                if len(line) > MAX_FRAME: raise QuotaError('FRAME_LIMIT')
                return _decode(line)
            for key, _ in selector.select(min(remaining, 0.2)):
                try: block = os.read(key.fileobj.fileno(), 8192)
                except OSError: raise QuotaError('SOURCE_CLOSED') from None
                if not block:
                    selector.unregister(key.fileobj)
                    if key.data == 'stdout': raise QuotaError('SOURCE_CLOSED')
                    continue
                total += len(block)
                if total > MAX_BYTES: raise QuotaError('OUTPUT_LIMIT')
                if key.data == 'stdout':
                    buffer.extend(block)
                    if len(buffer) > MAX_FRAME: raise QuotaError('FRAME_LIMIT')
                # stderr is discarded in memory without decoding or logging.
            if not selector.get_map(): raise QuotaError('SOURCE_CLOSED')
    try:
        return _exchange(send, receive)
    finally:
        selector.close()
        try: proc.stdin.close()
        except OSError: pass
        try: proc.wait(timeout=0.5)
        except subprocess.TimeoutExpired:
            try: os.killpg(proc.pid, signal.SIGTERM)
            except ProcessLookupError: pass
            try: proc.wait(timeout=0.5)
            except subprocess.TimeoutExpired:
                try: os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError: pass
                try: proc.wait(timeout=0.5)
                except subprocess.TimeoutExpired: raise QuotaError('SHUTDOWN_FAILED') from None
        proc.stdout.close()
        proc.stderr.close()


def read_quota(*, timeout=20, transport=None):
    """Normalized result or fixed failure; no raw diagnostics or automatic retry."""
    _validate_timeout(timeout)
    started = _utc()
    try:
        raw = (transport or app_server_read)(timeout)
        return normalize(raw, observed_at=_utc())
    except QuotaError as error:
        return {'schema_version': '0.1.0-provisional', 'source': SOURCE,
                'status': 'ERROR', 'error_code': error.code, 'attempted_at': started,
                'observed_at': None, 'windows': [], 'coverage': 'UNKNOWN'}
