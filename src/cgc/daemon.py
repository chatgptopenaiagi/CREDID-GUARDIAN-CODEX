"""Finite foreground CGC observation loop. No service or background installation."""
import threading

from .engine import empty_state, refresh, selection, StateError, utcnow, DEFAULT_POLICY, MAX_AGE
from .quota import read_quota, _validate_timeout


def run(cache, *, buckets, max_reads, interval=300, max_age=MAX_AGE, timeout=20, config=DEFAULT_POLICY,
        reader=read_quota, clock=utcnow, stop=None, evidence_provider=None):
    """At most max_reads attempts, completion-to-start spacing and capped backoff.

    Reader and evidence-provider injection are for offline tests. Evidence must be
    observation-bound and synthetic; production has no verified applicability contract.
    The production reader has V1 bounds.
    Hold the writer lock across reads and waits, preventing competing sensors.
    """
    buckets = selection(buckets)
    if type(max_reads) is not int or not 1 <= max_reads <= 100:
        raise StateError('INVALID_CONFIG')
    if type(interval) is not int or not 60 <= interval <= 3600:
        raise StateError('INVALID_CONFIG')
    _validate_timeout(timeout)
    initial = empty_state(buckets, max_age, config=config)
    stop = stop if stop is not None else threading.Event()
    attempts = failures = 0
    with cache.writer():
        state = cache.read() or initial
        if (state['policy']['selected_buckets'] != buckets or state['max_age_seconds'] != max_age
                or state['policy']['thresholds'] != config.to_dict()):
            raise StateError('CONFIG_MISMATCH')
        for _ in range(max_reads):
            if stop.is_set():
                break
            result = reader(timeout=timeout)
            attempts += 1
            evidence = evidence_provider(result) if evidence_provider else ()
            state = refresh(state, result, now=clock(), evidence=evidence)
            cache.write(state)
            failures = failures + 1 if state['last_refresh_status'] == 'ERROR' else 0
            if attempts < max_reads and stop.wait(min(3600, interval * 2 ** min(failures, 6))):
                break
    return attempts
