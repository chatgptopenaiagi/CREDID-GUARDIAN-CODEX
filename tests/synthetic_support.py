"""Explicit fixture contract used by legacy V2 tests, never by runtime code.

These tests define every fixture window as governing their synthetic workload.
No assertion is supplied for observations labeled live or for transport failures.
"""
from cgc.engine import refresh as engine_refresh
from cgc.daemon import run as daemon_run


def fixture_evidence(obs):
    if not isinstance(obs, dict) or obs.get('mode') != 'synthetic':
        return []
    return [{'window_id': w['window_id'], 'applicability': 'APPLICABLE',
             'basis': 'SYNTHETIC_CONTRACT', 'observed_at': obs['observed_at']}
            for w in obs.get('windows', [])]


def refresh(previous, result, *, now):
    return engine_refresh(previous, result, now=now, evidence=fixture_evidence(result))


def run(cache, **kwargs):
    return daemon_run(cache, **kwargs, evidence_provider=fixture_evidence)
