"""Explicit per-window evidence; all observations are hand-authored offline."""
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cgc.engine import empty_state, policy, refresh, status, validate_state, StateError
from cgc.quota import normalize
from cgc.cache import Cache, CacheError
from cgc.daemon import run
from cgc.__main__ import main

STAMP = '2026-09-17T00:00:00Z'


def sample(first=70, second=98, mode='synthetic'):
    return normalize({'rateLimits': {'limitId': 'codex',
                      'primary': {'usedPercent': first, 'windowDurationMins': 300},
                      'secondary': {'usedPercent': second, 'windowDurationMins': 10080}}},
                     observed_at=STAMP, mode=mode)


def evidence(obs, window_id='codex:primary', applicability='APPLICABLE'):
    return {'window_id': window_id, 'applicability': applicability,
            'basis': 'SYNTHETIC_CONTRACT', 'observed_at': obs['observed_at']}


class ApplicabilityTests(unittest.TestCase):
    def test_unknown_low_window_does_not_force_emergency(self):
        obs = sample()
        p = policy(obs, ['codex'], evidence=[evidence(obs)])
        self.assertEqual(p['policy_state'], 'GREEN')
        self.assertEqual(p['limiting_window_ids'], ['codex:primary'])
        self.assertEqual(p['most_constrained_remaining_percent'], 30)
        self.assertEqual(p['reason'], 'MINIMUM_KNOWN_APPLICABLE_SELECTED_WINDOW')
        self.assertEqual(p['window_diagnostics'][1]['applicability'], 'UNKNOWN')
        self.assertEqual(p['window_diagnostics'][1]['evidence_basis'], 'NO_EVIDENCE')
        self.assertFalse(p['global_all_clear'])
        self.assertEqual(p['coverage'], 'PARTIAL')

    def test_not_applicable_is_distinct_from_unknown(self):
        obs = sample()
        p = policy(obs, ['codex'], evidence=[evidence(obs, applicability='NOT_APPLICABLE')])
        self.assertEqual([w['applicability'] for w in p['window_diagnostics']],
                         ['NOT_APPLICABLE', 'UNKNOWN'])
        self.assertIsNone(p['policy_state'])
        self.assertIsNone(p['most_constrained_remaining_percent'])
        self.assertEqual(p['limiting_window_ids'], [])
        self.assertEqual(p['reason'], 'NO_KNOWN_APPLICABLE_USABLE_WINDOW')

    def test_selection_duration_name_and_allowance_are_not_evidence(self):
        for mode in ['live', 'synthetic']:
            for used in [0, 98, 100]:
                obs = sample(used, used, mode)
                obs['ordinary_usage_allowed'] = True
                p = policy(obs, ['codex'])
                self.assertIsNone(p['policy_state'])
                self.assertTrue(all(w['applicability'] == 'UNKNOWN' for w in p['window_diagnostics']))

    def test_invalid_selected_window_remains_diagnostic(self):
        obs = sample(101)
        p = policy(obs, ['codex'], evidence=[evidence(obs)])
        self.assertIsNone(p['policy_state'])
        self.assertEqual(p['window_diagnostics'][0]['validity'], 'INVALID')
        self.assertEqual(p['window_diagnostics'][0]['exclusion_reasons'], ['INVALID_VALUE'])
        self.assertEqual(p['window_diagnostics'][0]['applicability'], 'APPLICABLE')

    def test_out_of_scope_known_window_cannot_limit_and_ties_are_stable(self):
        obs = sample(90, 90)
        ev = [evidence(obs), evidence(obs, 'codex:secondary')]
        p = policy(obs, ['other'], evidence=ev)
        self.assertIsNone(p['policy_state'])
        self.assertEqual(p['window_diagnostics'][0]['exclusion_reasons'], ['OUTSIDE_SELECTED_SCOPE'])
        p = policy(obs, ['codex'], evidence=list(reversed(ev)))
        self.assertEqual(p['limiting_window_ids'], ['codex:primary', 'codex:secondary'])
        self.assertEqual(p['policy_state'], 'RED')

    def test_evidence_bounds_types_scope_and_safe_rejection(self):
        obs = sample()
        good = evidence(obs)
        bad = [None, {}, [good] * 97, [good, good], [dict(good, token='synthetic-private')],
               [dict(good, basis='OPERATOR_SELECTION')], [dict(good, basis='SOURCE_CONTRACT')],
               [dict(good, applicability=True)], [dict(good, window_id='absent:primary')],
               [dict(good, observed_at='2026-09-16T00:00:00Z')]]
        for entries in bad:
            with self.subTest(entries=type(entries).__name__), self.assertRaises(StateError) as caught:
                policy(obs, ['codex'], evidence=entries)
            self.assertNotIn('synthetic-private', str(caught.exception))
        with self.assertRaises(StateError):
            policy(sample(mode='live'), ['codex'], evidence=[good])

    def test_unknown_refresh_retains_good_but_withholds_current_limit(self):
        obs = sample()
        before = refresh(empty_state(['codex']), obs, now=STAMP, evidence=[evidence(obs)])
        after = refresh(before, sample(98), now=STAMP)
        self.assertEqual(after['last_valid_observation'], before['last_valid_observation'])
        self.assertEqual(after['last_valid_policy'], before['policy'])
        result = status(after, now=STAMP)
        self.assertIsNone(result['policy_state'])
        self.assertEqual(result['limiting_window_ids'], [])
        self.assertEqual(result['historical_policy']['limiting_window_ids'], ['codex:primary'])
        self.assertEqual(result['evaluated_policy']['window_diagnostics'][0]['applicability'], 'UNKNOWN')
        failed = refresh(after, {'status': 'ERROR', 'error_code': 'TIMEOUT'}, now=STAMP)
        self.assertIsNone(status(failed, now=STAMP)['policy_state'])
        recovered = refresh(failed, obs, now=STAMP, evidence=[evidence(obs)])
        self.assertEqual(recovered['last_refresh_status'], 'OK')
        self.assertEqual(status(recovered, now=STAMP)['policy_state'], 'GREEN')

    def test_transport_failure_retains_evidence_and_stale_hides_limit(self):
        obs = sample()
        state = refresh(empty_state(['codex']), obs, now=STAMP, evidence=[evidence(obs)])
        failed = refresh(state, {'status': 'ERROR', 'error_code': 'TIMEOUT'}, now=STAMP)
        self.assertEqual(failed['policy'], state['policy'])
        old = status(failed, now='2026-09-17T00:16:00Z')
        self.assertIsNone(old['policy_state'])
        self.assertEqual(old['limiting_window_ids'], [])
        self.assertEqual(old['historical_policy']['limiting_window_ids'], ['codex:primary'])

    def test_cache_tampering_rejected(self):
        obs = sample()
        state = refresh(empty_state(['codex']), obs, now=STAMP, evidence=[evidence(obs)])
        for key, value in [('limiting_window_ids', ['codex:secondary']),
                           ('reason', 'synthetic-private'), ('evidence', []),
                           ('window_diagnostics', []), ('global_all_clear', True)]:
            bad = copy.deepcopy(state)
            bad['policy'][key] = value
            with self.subTest(key=key), self.assertRaises(StateError):
                validate_state(bad)
        bad = copy.deepcopy(state)
        bad['schema_version'] = 'cgc-state-v2.1'
        with self.assertRaises(StateError): validate_state(bad)

    def test_daemon_cache_and_cli_evidence_agree(self):
        obs = sample()
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'cache'
            with Cache(path, create=True) as cache:
                run(cache, buckets=['codex'], max_reads=1, reader=lambda **_: obs,
                    clock=lambda: STAMP, evidence_provider=lambda result: [evidence(result)])
                state = cache.read()
                self.assertEqual(state['policy']['limiting_window_ids'], ['codex:primary'])
            for json_mode in [True, False]:
                output = io.StringIO()
                with contextlib.redirect_stdout(output), patch('cgc.__main__.utcnow', return_value=STAMP), \
                        patch('cgc.quota.app_server_read', side_effect=AssertionError('live read')):
                    code = main(['status', '--cache-dir', str(path)] + (['--json'] if json_mode else []))
                self.assertEqual(code, 1)
                if json_mode:
                    result = json.loads(output.getvalue())
                    self.assertEqual(result['evaluated_policy'], state['policy'])
                    self.assertEqual(result['limiting_window_ids'], ['codex:primary'])
                else:
                    self.assertIn('Most constrained applicable: codex:primary', output.getvalue())
                    self.assertIn('applicability=UNKNOWN', output.getvalue())
                    self.assertIn('SYNTHETIC_CONTRACT', output.getvalue())

    def test_invalid_and_unknown_values_do_not_hide_valid_limit(self):
        obs = normalize({'rateLimits': {}, 'rateLimitsByLimitId': {
            'codex': {'primary': {'usedPercent': 101}, 'secondary': {'usedPercent': 70},
                      'individualLimit': {'remainingPercent': None}}}},
                        observed_at=STAMP, mode='synthetic')
        ev = [evidence(obs, w['window_id']) for w in obs['windows']]
        p = policy(obs, ['codex'], evidence=ev)
        self.assertEqual(p['policy_state'], 'GREEN')
        self.assertEqual(p['limiting_window_ids'], ['codex:secondary'])
        diagnostics = {w['window_id']: w for w in p['window_diagnostics']}
        self.assertEqual(diagnostics['codex:primary']['exclusion_reasons'], ['INVALID_VALUE'])
        self.assertEqual(diagnostics['codex:individual_limit']['exclusion_reasons'], ['UNKNOWN_VALUE'])

    def test_evidence_is_not_reused_for_newer_observation(self):
        obs = sample()
        state = refresh(empty_state(['codex']), obs, now=STAMP, evidence=[evidence(obs)])
        newer = sample()
        newer['observed_at'] = '2026-09-17T00:01:00Z'
        unknown = refresh(state, newer, now=newer['observed_at'])
        self.assertIsNone(unknown['policy']['policy_state'])
        self.assertEqual(unknown['policy']['evidence'], [])
        self.assertEqual(unknown['last_valid_observation']['observed_at'], STAMP)
        self.assertEqual(unknown['last_observation']['observed_at'], newer['observed_at'])
        regressed = refresh(unknown, obs, now=newer['observed_at'], evidence=[evidence(obs)])
        self.assertEqual(regressed['last_observation'], newer)
        self.assertIsNone(regressed['policy']['policy_state'])

    def test_unknown_and_invalid_diagnostics_survive_cache(self):
        obs = sample()
        state = refresh(empty_state(['codex']), obs, now=STAMP, evidence=[evidence(obs)])
        invalid = sample(101)
        state = refresh(state, invalid, now=STAMP, evidence=[evidence(invalid)])
        with tempfile.TemporaryDirectory() as root:
            with Cache(Path(root) / 'cache', create=True) as cache, cache.writer():
                cache.write(state)
                result = status(cache.read(), now=STAMP)
        self.assertIsNone(result['policy_state'])
        self.assertEqual(result['observation']['windows'][0]['validity'], 'INVALID')
        self.assertEqual(result['last_valid_observation'], obs)

    def test_old_schema_and_live_evidence_cannot_enter_cache(self):
        obs = sample(mode='live')
        state = refresh(empty_state(['codex']), obs, now=STAMP)
        bad = copy.deepcopy(state)
        bad['policy']['evidence'] = [evidence(obs)]
        with self.assertRaises(StateError): validate_state(bad)
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'cache'
            with Cache(path, create=True) as cache, cache.writer(): cache.write(state)
            state['schema_version'] = 'cgc-state-v2.1'
            before = json.dumps(state).encode()
            (path / 'state.json').write_bytes(before)
            with Cache(path) as cache, self.assertRaises(CacheError):
                run(cache, buckets=['codex'], max_reads=1,
                    reader=lambda **_: self.fail('source must not run'))
            self.assertEqual((path / 'state.json').read_bytes(), before)

    def test_maximum_window_evidence_and_retained_state_fit_bounded_cache(self):
        buckets = [('b' + str(i)).ljust(64, 'x') for i in range(32)]
        raw = {'rateLimits': {}, 'rateLimitsByLimitId': {
            b: {'primary': {'usedPercent': 70, 'windowDurationMins': 5256000, 'resetsAt': 253402300799},
                'secondary': {'usedPercent': 70, 'windowDurationMins': 5256000, 'resetsAt': 253402300799},
                'individualLimit': {'remainingPercent': 30, 'resetsAt': 253402300799}} for b in buckets}}
        obs = normalize(raw, observed_at=STAMP, mode='synthetic')
        ev = [evidence(obs, w['window_id']) for w in obs['windows']]
        state = refresh(empty_state(buckets), obs, now=STAMP, evidence=ev)
        self.assertEqual(len(state['policy']['limiting_window_ids']), 96)
        with tempfile.TemporaryDirectory() as root:
            with Cache(Path(root) / 'cache', create=True) as cache, cache.writer():
                cache.write(state)
                unknown = refresh(state, obs, now=STAMP,
                                  evidence=[dict(e, applicability='NOT_APPLICABLE') for e in ev])
                cache.write(unknown)
                self.assertEqual(cache.read(), unknown)

    def test_multiple_known_applicable_windows_use_configured_minimum(self):
        for first, second, expected in [(80, 50, 'GREEN'), (30, 15, 'AMBER'),
                                        (8, 70, 'RED'), (4, 80, 'EMERGENCY')]:
            obs = sample(100 - first, 100 - second)
            p = policy(obs, ['codex'], evidence=[evidence(obs), evidence(obs, 'codex:secondary')])
            self.assertEqual(p['policy_state'], expected)
            self.assertEqual(p['most_constrained_remaining_percent'], min(first, second))
