"""Deterministic freshness, provenance and current-policy authority."""
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cgc.engine import (empty_state, refresh, status, freshness, validate_state, StateError)
from cgc.cache import Cache, CacheError, MAX_CACHE_BYTES
from cgc.__main__ import main
from cgc.quota import normalize
from synthetic_support import fixture_evidence
from test_engine import observation, populated, STAMP

LATER = '2026-09-17T00:01:00Z'
STALE = '2026-09-17T00:15:01Z'
ERROR = {'status': 'ERROR', 'error_code': 'TIMEOUT'}


class FreshnessTests(unittest.TestCase):
    def test_fresh_valid_current(self):
        result = status(populated(), now=STAMP)
        self.assertEqual(result['freshness'], 'FRESH')
        self.assertTrue(result['policy_available'])
        self.assertEqual(result['data_disposition'], 'CURRENT')
        self.assertEqual(result['evaluated_at'], STAMP)

    def test_stale_withholds_current_and_keeps_history(self):
        result = status(populated(), now=STALE)
        self.assertEqual(result['freshness'], 'STALE')
        self.assertFalse(result['policy_available'])
        self.assertIsNone(result['policy_state'])
        self.assertEqual(result['data_disposition'], 'HISTORICAL')
        self.assertEqual(result['historical_policy']['policy_state'], 'AMBER')
        self.assertEqual(result['provenance']['last_known_good']['disposition'], 'HISTORICAL')

    def test_exact_boundary_and_fractional_age(self):
        for now, expected in [('2026-09-17T00:15:00Z', 'FRESH'),
                              ('2026-09-17T00:15:00.000001Z', 'STALE')]:
            self.assertEqual(status(populated(), now=now)['freshness'], expected)

    def test_missing_time_is_unknown_never_guessed(self):
        result = freshness(None, now=STAMP)
        self.assertEqual(result['state'], 'UNKNOWN')
        self.assertIsNone(result['age_seconds'])
        bad = observation(); del bad['observed_at']
        result = refresh(empty_state(['codex']), bad, now=STAMP)
        self.assertEqual(result['last_refresh_status'], 'ERROR')
        self.assertIsNone(result['last_observation'])

    def test_malformed_time_is_safe_error(self):
        for value in ['synthetic-private', '2026-09-17T00:00:00', 42, {}, True]:
            result = freshness(value, now=STAMP)
            self.assertEqual(result['state'], 'ERROR')
            self.assertNotIn('synthetic-private', json.dumps(result))
            bad = observation(); bad['observed_at'] = value
            failed = refresh(populated(), bad, now=STAMP)
            self.assertEqual(failed['last_valid_observation'], populated()['last_valid_observation'])
            self.assertIsNone(status(failed, now=STAMP)['policy_state'])

    def test_future_timestamp_and_clock_rollback(self):
        self.assertEqual(freshness(LATER, now=STAMP)['state'], 'ERROR')
        obs = observation(stamp=LATER)
        failed = refresh(populated(), obs, now=STAMP, evidence=fixture_evidence(obs))
        self.assertEqual(failed['last_refresh_status'], 'ERROR')
        self.assertIsNone(status(failed, now=STAMP)['policy_state'])
        result = status(populated(), now='2026-09-16T23:59:59Z')
        self.assertEqual(result['freshness'], 'ERROR')
        self.assertFalse(result['policy_available'])

    def test_newer_observation_and_older_rejection(self):
        obs = observation(95, stamp=LATER)
        new = refresh(populated(), obs, now=LATER, evidence=fixture_evidence(obs))
        self.assertEqual(status(new, now=LATER)['policy_state'], 'EMERGENCY')
        rejected = refresh(new, observation(), now=LATER, evidence=fixture_evidence(observation()))
        self.assertEqual(rejected['last_observation'], obs)
        self.assertIsNone(status(rejected, now=LATER)['policy_state'])

    def test_failure_with_fresh_last_good_is_retained_not_current(self):
        state = refresh(populated(), ERROR, now=LATER)
        result = status(state, now=LATER)
        self.assertEqual(result['freshness'], 'FRESH')
        self.assertEqual(result['last_refresh_status'], 'ERROR')
        self.assertEqual(result['data_disposition'], 'RETAINED')
        self.assertFalse(result['policy_available'])
        self.assertIsNone(result['policy_state'])
        self.assertEqual(result['historical_policy']['policy_state'], 'AMBER')
        self.assertEqual(result['age_seconds'], 60)

    def test_failure_without_last_good(self):
        result = status(refresh(empty_state(['codex']), ERROR, now=STAMP), now=STAMP)
        self.assertEqual(result['freshness'], 'UNKNOWN')
        self.assertEqual(result['last_refresh_status'], 'ERROR')
        self.assertEqual(result['data_disposition'], 'UNAVAILABLE')
        self.assertIsNone(result['most_constrained_remaining_percent'])

    def test_failure_with_stale_last_good(self):
        result = status(refresh(populated(), ERROR, now=STALE), now=STALE)
        self.assertEqual(result['freshness'], 'STALE')
        self.assertEqual(result['data_disposition'], 'HISTORICAL')
        self.assertEqual(result['last_known_good_freshness']['state'], 'STALE')
        self.assertIsNone(result['policy_state'])

    def test_stale_arrival_does_not_replace_last_good(self):
        before = populated()
        obs = observation(95, stamp=LATER)
        state = refresh(before, obs, now='2026-09-17T00:20:00Z', evidence=fixture_evidence(obs))
        self.assertEqual(state['last_observation'], obs)
        self.assertEqual(state['last_valid_observation'], before['last_valid_observation'])
        self.assertEqual(state['error_code'], 'STALE_OBSERVATION')
        self.assertIsNone(status(state, now='2026-09-17T00:20:00Z')['policy_state'])

    def test_value_origin_separate_from_retention(self):
        obs = normalize({'rateLimits': {'limitId': 'codex', 'primary': {'usedPercent': 64},
                         'individualLimit': {'remainingPercent': 42}}}, observed_at=STAMP, mode='synthetic')
        state = refresh(empty_state(['codex']), obs, now=STAMP, evidence=fixture_evidence(obs))
        state = refresh(state, ERROR, now=LATER)
        provenance = status(state, now=LATER)['provenance']['latest']
        self.assertEqual(provenance['disposition'], 'RETAINED')
        windows = {w['window_id']: w for w in provenance['windows']}
        self.assertEqual(windows['codex:primary']['remaining_percent'], 'DERIVED')
        self.assertEqual(windows['codex:primary']['used_percent'], 'DIRECT')
        self.assertEqual(windows['codex:individual_limit']['remaining_percent'], 'DIRECT')
        self.assertEqual(windows['codex:individual_limit']['used_percent'], 'UNAVAILABLE')
        self.assertEqual(provenance['source_kind'], 'codex_app_server')
        self.assertEqual(provenance['source_time_origin'], 'UNAVAILABLE')

    def test_fresh_unknown_applicability_is_not_policy(self):
        state = refresh(empty_state(['codex']), observation(), now=STAMP)
        result = status(state, now=STAMP)
        self.assertEqual(result['freshness'], 'FRESH')
        self.assertIsNone(result['policy_state'])
        self.assertFalse(result['policy_available'])

    def test_new_unknown_has_independent_last_good_age(self):
        unknown = refresh(populated(), observation(stamp=LATER), now=LATER)
        result = status(unknown, now='2026-09-17T00:15:30Z')
        self.assertEqual(result['freshness'], 'FRESH')
        self.assertEqual(result['last_known_good_freshness']['state'], 'STALE')
        self.assertEqual(result['provenance']['last_known_good']['disposition'], 'HISTORICAL')
        self.assertIsNone(result['policy_state'])

    def test_fresh_invalid_values_do_not_authorize_policy(self):
        obs = observation(101)
        state = refresh(empty_state(['codex']), obs, now=STAMP, evidence=fixture_evidence(obs))
        result = status(state, now=STAMP)
        self.assertEqual(result['freshness'], 'FRESH')
        self.assertIsNone(result['policy_state'])
        self.assertEqual(result['observation']['windows'][0]['validity'], 'INVALID')

    def test_max_age_validation_and_custom_boundary(self):
        for value in [-1, 0, 86401, None, True, '900', 1.5, float('nan'), float('inf')]:
            with self.assertRaises(StateError): empty_state(['codex'], value)
        obs = observation()
        state = refresh(empty_state(['codex'], 60), obs, now=STAMP, evidence=fixture_evidence(obs))
        self.assertEqual(status(state, now=LATER)['freshness'], 'FRESH')
        self.assertEqual(status(state, now='2026-09-17T00:01:01Z')['freshness'], 'STALE')

    def test_temporal_snapshot_roundtrip_and_read_time_recalculation(self):
        state = populated()
        self.assertEqual(state['temporal']['freshness'], 'FRESH')
        with tempfile.TemporaryDirectory() as root:
            with Cache(Path(root) / 'cache', create=True) as cache, cache.writer():
                cache.write(state)
                before = (Path(root) / 'cache/state.json').read_bytes()
                result = status(cache.read(), now=STALE)
                self.assertEqual(result['freshness'], 'STALE')
                self.assertEqual((Path(root) / 'cache/state.json').read_bytes(), before)

    def test_temporal_and_origin_tampering_rejected(self):
        for field, value in [('freshness', 'STALE'), ('policy_available', False),
                             ('evaluated_at', LATER), ('token', 'synthetic-private')]:
            bad = copy.deepcopy(populated()); bad['temporal'][field] = value
            with self.assertRaises(StateError): validate_state(bad)
        bad = copy.deepcopy(populated())
        bad['last_observation']['windows'][0]['value_origin'] = 'direct'
        with self.assertRaises(StateError): validate_state(bad)

    def test_old_schema_refused(self):
        bad = populated(); bad['schema_version'] = 'cgc-state-v2.2'
        with self.assertRaises(StateError): validate_state(bad)

    def test_human_json_consistency_for_fresh_stale_and_retained(self):
        for state, now, label in [(populated(), STAMP, 'CURRENT'), (populated(), STALE, 'HISTORICAL'),
                                  (refresh(populated(), ERROR, now=LATER), LATER, 'RETAINED')]:
            with tempfile.TemporaryDirectory() as root:
                path = Path(root) / 'cache'
                with Cache(path, create=True) as cache, cache.writer(): cache.write(state)
                outputs = []
                for flags in [['--json'], []]:
                    out = io.StringIO()
                    with contextlib.redirect_stdout(out), patch('cgc.__main__.utcnow', return_value=now):
                        self.assertEqual(main(['status', '--cache-dir', str(path)] + flags), 1)
                    outputs.append(out.getvalue())
                result = json.loads(outputs[0])
                self.assertEqual(result, status(state, now=now))
                self.assertIn('Freshness: ' + result['freshness'], outputs[1])
                self.assertIn('Data: ' + label, outputs[1])
                self.assertIn('DERIVED', outputs[1])

    def test_missing_and_corrupt_cli_report_freshness(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'cache'
            out = io.StringIO()
            with contextlib.redirect_stdout(out): main(['status', '--cache-dir', str(path), '--json'])
            self.assertEqual(json.loads(out.getvalue())['freshness'], 'UNKNOWN')
            self.assertFalse(path.exists())
            with Cache(path, create=True) as cache, cache.writer(): cache.write(populated())
            (path / 'state.json').write_text('{bad')
            out = io.StringIO()
            with contextlib.redirect_stdout(out): self.assertEqual(main(['status', '--cache-dir', str(path), '--json']), 2)
            self.assertEqual(json.loads(out.getvalue())['freshness'], 'ERROR')

    def test_cache_bound_stays_enforced(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'cache'
            with Cache(path, create=True) as cache, cache.writer():
                cache.write(populated())
                p = path / 'state.json'
                p.write_bytes(b' ' * (MAX_CACHE_BYTES + 1))
                with self.assertRaises(CacheError): cache.read()
        self.assertEqual(MAX_CACHE_BYTES, 262144)

    def test_maximum_windows_keep_freshness_and_origin_after_retention(self):
        buckets = [('b' + str(i)).ljust(64, 'x') for i in range(32)]
        obs = normalize({'rateLimits': {}, 'rateLimitsByLimitId': {
            b: {'primary': {'usedPercent': 64, 'windowDurationMins': 300, 'resetsAt': 253402300799},
                'secondary': {'usedPercent': 64, 'windowDurationMins': 10080},
                'individualLimit': {'remainingPercent': 42}} for b in buckets}},
                        observed_at=STAMP, mode='synthetic')
        state = refresh(empty_state(buckets), obs, now=STAMP, evidence=fixture_evidence(obs))
        state = refresh(state, ERROR, now=LATER)
        with tempfile.TemporaryDirectory() as root:
            with Cache(Path(root) / 'cache', create=True) as cache, cache.writer():
                cache.write(state)
                result = status(cache.read(), now=STALE)
        for role in ['latest', 'last_known_good']:
            self.assertEqual(len(result['provenance'][role]['windows']), 96)
            self.assertEqual(result['provenance'][role]['disposition'], 'HISTORICAL')
        self.assertEqual(result['freshness'], 'STALE')
        self.assertIsNone(result['policy_state'])

    def test_oversized_write_preserves_previous_generation(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'cache'
            with Cache(path, create=True) as cache, cache.writer():
                cache.write(populated())
                before = (path / 'state.json').read_bytes()
                with patch('cgc.cache.MAX_CACHE_BYTES', 1), self.assertRaisesRegex(CacheError, 'CACHE_SIZE_LIMIT'):
                    cache.write(populated(95))
                self.assertEqual((path / 'state.json').read_bytes(), before)

    def test_clock_rollback_before_cache_write_and_invalid_evaluation(self):
        state = refresh(populated(), ERROR, now=LATER)
        result = status(state, now=STAMP)
        self.assertEqual(result['freshness'], 'ERROR')
        self.assertEqual(result['observation_freshness']['reason'], 'CLOCK_BEFORE_CACHE_WRITE')
        self.assertFalse(result['policy_available'])
        with self.assertRaisesRegex(StateError, 'CLOCK_REGRESSION'):
            refresh(state, observation(), now=STAMP)
        with self.assertRaises(StateError): status(state, now='synthetic-private')

    def test_custom_max_age_cli_and_daemon_mismatch_before_read(self):
        from synthetic_support import run
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'cache'
            for value in ['-1', '0', '86401']:
                with contextlib.redirect_stdout(io.StringIO()), patch('cgc.__main__.run', side_effect=AssertionError('read')):
                    self.assertEqual(main(['daemon', '--live', '--bucket', 'codex', '--max-reads', '1',
                                           '--cache-dir', str(path), '--max-age', value]), 2)
                self.assertFalse(path.exists())
            with Cache(path, create=True) as cache:
                run(cache, buckets=['codex'], max_reads=1, max_age=60,
                    reader=lambda **_: observation(), clock=lambda: STAMP)
                self.assertEqual(status(cache.read(), now=STALE)['freshness'], 'STALE')
                with self.assertRaisesRegex(StateError, 'CONFIG_MISMATCH'):
                    run(cache, buckets=['codex'], max_reads=1, max_age=900,
                        reader=lambda **_: self.fail('read'))

    def test_temporal_error_and_provenance_cannot_inject_fields(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'cache'
            with Cache(path, create=True) as cache, cache.writer(): cache.write(populated())
            bad = copy.deepcopy(populated()); bad['temporal']['secret'] = 'synthetic-private'
            (path / 'state.json').write_text(json.dumps(bad))
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(main(['status', '--cache-dir', str(path), '--json']), 2)
            self.assertNotIn('synthetic-private', out.getvalue())
            self.assertEqual(json.loads(out.getvalue())['freshness'], 'ERROR')

    def test_recovery_requires_a_new_accepted_refresh(self):
        state = refresh(populated(), ERROR, now=LATER)
        self.assertIsNone(status(state, now=LATER)['policy_state'])
        obs = observation(95, stamp=LATER)
        recovered = refresh(state, obs, now=LATER, evidence=fixture_evidence(obs))
        self.assertTrue(status(recovered, now=LATER)['policy_available'])
        self.assertEqual(status(recovered, now=LATER)['data_disposition'], 'CURRENT')
        self.assertEqual(recovered['temporal']['freshness'], 'FRESH')
