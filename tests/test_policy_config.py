"""Configurable policy acceptance: synthetic observations and private /tmp caches."""
import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cgc.engine import (PolicyConfig, StateError, classify, empty_state,
                        validate_state, status)
from cgc.cache import Cache, CacheError
from synthetic_support import run, refresh
from cgc.__main__ import main
from test_engine import observation, STAMP


class PolicyConfigTests(unittest.TestCase):
    def test_defaults_and_fractional_boundaries(self):
        self.assertEqual(PolicyConfig().to_dict(),
                         {'amber_at': 20, 'red_at': 10, 'emergency_at': 5})
        config = PolicyConfig(30.5, 15.5, 7.5)
        for value, expected in [(100, 'GREEN'), (30.501, 'GREEN'), (30.5, 'AMBER'),
                                (15.501, 'AMBER'), (15.5, 'RED'), (7.501, 'RED'),
                                (7.5, 'EMERGENCY'), (0, 'EMERGENCY')]:
            with self.subTest(value=value):
                self.assertEqual(classify(value, config), expected)

    def test_invalid_configuration(self):
        for field in ('amber_at', 'red_at', 'emergency_at'):
            for value in (True, False, None, '5', -1, 101, float('nan'),
                          float('inf'), -float('inf'), 10**1000):
                with self.subTest(field=field, value=type(value).__name__):
                    with self.assertRaises(StateError):
                        PolicyConfig(**{field: value})
        for values in [(10, 20, 5), (20, 5, 10), (20, 20, 5), (20, 5, 5)]:
            with self.assertRaises(StateError):
                PolicyConfig(*values)
        self.assertEqual(classify(0, PolicyConfig(100, 50, 0)), 'EMERGENCY')

    def test_strict_config_projection(self):
        for value in (None, [], {}, {'amber_at': 20, 'red_at': 10},
                      dict(PolicyConfig().to_dict(), token='synthetic-private')):
            with self.assertRaises(StateError) as caught:
                PolicyConfig.from_dict(value)
            self.assertNotIn('synthetic-private', str(caught.exception))

    def test_refresh_failure_and_status_keep_custom_policy(self):
        config = PolicyConfig(40, 25, 15)
        state = refresh(empty_state(['codex'], config=config), observation(80), now=STAMP)
        self.assertEqual(state['policy']['policy_state'], 'RED')
        failed = refresh(state, {'status': 'ERROR', 'error_code': 'TIMEOUT'}, now=STAMP)
        self.assertEqual(failed['policy'], state['policy'])
        self.assertEqual(status(failed, now=STAMP)['policy_state'], 'RED')
        self.assertEqual(state['policy']['thresholds'], config.to_dict())

    def test_tampered_and_old_cache_rejected(self):
        state = refresh(empty_state(['codex']), observation(), now=STAMP)
        for change in ('thresholds', 'label', 'version', 'schema'):
            bad = copy.deepcopy(state)
            if change == 'thresholds': bad['policy']['thresholds']['red_at'] = 25
            if change == 'label': bad['policy']['thresholds'] = PolicyConfig(40, 25, 15).to_dict()
            if change == 'version': bad['policy']['policy_version'] = 'unknown'
            if change == 'schema': bad['schema_version'] = 'cgc-state-v2'
            with self.subTest(change=change), self.assertRaises(StateError):
                validate_state(bad)

    def test_daemon_cache_cli_share_configuration(self):
        config = PolicyConfig(40, 25, 15)
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'cache'
            with Cache(path, create=True) as cache:
                run(cache, buckets=['codex'], max_reads=1, config=config,
                    reader=lambda **_: observation(), clock=lambda: STAMP)
                run(cache, buckets=['codex'], max_reads=1, config=PolicyConfig(40.0, 25.0, 15.0),
                    reader=lambda **_: observation(), clock=lambda: STAMP)
                before = (path / 'state.json').read_bytes()
                with self.assertRaisesRegex(StateError, 'CONFIG_MISMATCH'):
                    run(cache, buckets=['codex'], max_reads=1,
                        reader=lambda **_: self.fail('source must not run'))
                self.assertEqual((path / 'state.json').read_bytes(), before)
            for extra in (['--json'], []):
                output = io.StringIO()
                with patch('cgc.__main__.utcnow', return_value=STAMP), contextlib.redirect_stdout(output):
                    self.assertEqual(main(['status', '--cache-dir', str(path)] + extra), 1)
                if extra:
                    result = json.loads(output.getvalue())
                    self.assertEqual(result['policy_state'], 'RED')
                    self.assertEqual(result['historical_policy']['thresholds'], config.to_dict())
                else:
                    self.assertIn('policy: RED', output.getvalue())
                    self.assertIn('AMBER <= 40', output.getvalue())

    def test_cli_passes_custom_configuration(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'cache'
            def synthetic(cache, **kwargs):
                self.assertEqual(kwargs['config'], PolicyConfig(30.5, 15.5, 7.5))
                return run(cache, **kwargs, reader=lambda **_: observation(), clock=lambda: STAMP)
            with patch('cgc.__main__.run', side_effect=synthetic), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(['daemon', '--live', '--bucket', 'codex', '--max-reads', '1',
                                       '--cache-dir', str(path), '--amber-at', '30.5',
                                       '--red-at', '15.5', '--emergency-at', '7.5']), 0)

    def test_invalid_cli_thresholds_do_not_create_cache_or_read(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'cache'
            for value in ('nan', 'inf', '-1', '101', '5'):
                with patch('cgc.__main__.run', side_effect=AssertionError('source')), contextlib.redirect_stdout(io.StringIO()):
                    code = main(['daemon', '--live', '--bucket', 'codex', '--max-reads', '1',
                                 '--cache-dir', str(path), '--amber-at', value])
                self.assertEqual(code, 2)
                self.assertFalse(path.exists())

    def test_old_disk_cache_blocks_reader_and_is_preserved(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / 'cache'
            with Cache(path, create=True) as cache, cache.writer():
                cache.write(empty_state(['codex']))
            old = empty_state(['codex'])
            old['schema_version'] = 'cgc-state-v2'
            del old['policy']['thresholds']
            before = json.dumps(old).encode()
            (path / 'state.json').write_bytes(before)
            with Cache(path) as cache, self.assertRaises(CacheError):
                run(cache, buckets=['codex'], max_reads=1,
                    reader=lambda **_: self.fail('source must not run'))
            self.assertEqual((path / 'state.json').read_bytes(), before)
