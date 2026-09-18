"""One-shot CLI acceptance using injected sensors and private Linux temporary caches."""
import contextlib
import io
import json
from pathlib import Path
import signal
import tempfile
import unittest
from unittest.mock import Mock, patch

from cgc.__main__ import main
from cgc.cache import Cache
from cgc.daemon import refresh_once
from cgc.engine import PolicyConfig, empty_state, status
from cgc.quota import QuotaError
from synthetic_support import fixture_evidence
from test_engine import observation, populated, STAMP


class RefreshCLITests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.path = Path(temp.name) / 'cache'
        self.addCleanup(patch.stopall)
        patch('cgc.quota.app_server_read', side_effect=AssertionError('live read forbidden')).start()

    def invoke(self, result=None, *, extra=(), evidence=False, human=False):
        reader = Mock(return_value=observation() if result is None else result)
        def injected(cache, **kwargs):
            return refresh_once(cache, **kwargs, reader=reader, clock=lambda: STAMP,
                                evidence_provider=fixture_evidence if evidence else None)
        output = io.StringIO()
        args = ['refresh', '--live', '--bucket', 'codex', '--cache-dir', str(self.path)]
        with patch('cgc.__main__.refresh_once', side_effect=injected), \
             patch('cgc.__main__.utcnow', return_value=STAMP), contextlib.redirect_stdout(output):
            code = main(args + list(extra) + ([] if human else ['--json']))
        return code, output.getvalue(), reader

    def seed(self):
        with Cache(self.path, create=True) as cache, cache.writer():
            cache.write(populated())
        return (self.path / 'state.json').read_bytes()

    def test_one_read_and_status_agreement(self):
        code, text, reader = self.invoke(evidence=True, extra=['--timeout', '7'])
        reader.assert_called_once_with(timeout=7)
        self.assertEqual(code, 1)  # Synthetic never authorizes a live policy.
        with Cache(self.path) as cache:
            state = cache.read()
        self.assertEqual(state['generation'], 1)
        self.assertEqual(json.loads(text), status(state, now=STAMP))
        self.assertEqual(state['last_refresh_status'], 'OK')
        self.assertEqual(self.path.stat().st_mode & 0o777, 0o700)
        self.assertEqual((self.path / 'state.json').stat().st_mode & 0o777, 0o600)

    def test_selection_does_not_establish_applicability(self):
        code, text, reader = self.invoke()
        reader.assert_called_once()
        out = json.loads(text)
        self.assertEqual(code, 1)
        self.assertIsNone(out['policy_state'])
        self.assertEqual(out['error_code'], 'NO_USABLE_DATA')
        self.assertEqual(out['freshness'], 'FRESH')
        self.assertFalse(out['live_policy_available'])

    def test_failure_preserves_history_without_retry(self):
        self.seed()
        code, text, reader = self.invoke({'status': 'ERROR', 'error_code': 'TIMEOUT'})
        reader.assert_called_once()
        out = json.loads(text)
        self.assertEqual(code, 1)
        self.assertEqual(out['generation'], 2)
        self.assertEqual(out['last_valid_observation'], populated()['last_valid_observation'])
        self.assertIsNone(out['policy_state'])
        self.assertEqual(out['data_disposition'], 'RETAINED')
        self.assertEqual(out['error_code'], 'TIMEOUT')

    def test_failure_without_history_is_unknown(self):
        code, text, reader = self.invoke({'status': 'ERROR', 'error_code': 'SOURCE_ERROR'})
        self.assertEqual(code, 1)
        reader.assert_called_once()
        self.assertEqual(json.loads(text)['data_disposition'], 'UNAVAILABLE')
        self.assertIsNone(json.loads(text)['policy_state'])

    def test_human_result_shows_uncertainty(self):
        code, text, reader = self.invoke(human=True)
        self.assertEqual(code, 1)
        self.assertIn('CREDID GUARDIAN CODEX', text)
        self.assertIn('Freshness: FRESH', text)
        self.assertIn('policy: UNKNOWN', text)
        self.assertIn('applicability=UNKNOWN', text)
        reader.assert_called_once()

    def test_custom_configuration_persisted(self):
        code, text, _ = self.invoke(evidence=True, extra=['--amber-at', '40', '--red-at', '25',
                                                       '--emergency-at', '15', '--max-age', '60'])
        self.assertEqual(code, 1)
        with Cache(self.path) as cache:
            state = cache.read()
        self.assertEqual(state['max_age_seconds'], 60)
        self.assertEqual(state['policy']['thresholds'], PolicyConfig(40, 25, 15).to_dict())
        self.assertEqual(json.loads(text)['policy_state'], 'RED')

    def test_mismatch_blocks_read_and_preserves_bytes(self):
        before = self.seed()
        for extra in (['--max-age', '60'], ['--amber-at', '30'], ['--bucket', 'other']):
            code, _, reader = self.invoke(extra=extra)
            self.assertEqual(code, 2)
            reader.assert_not_called()
            self.assertEqual((self.path / 'state.json').read_bytes(), before)

    def test_corrupt_and_old_cache_block_read(self):
        self.seed()
        old = empty_state(['codex']); old['schema_version'] = 'cgc-state-v2.2'
        for data in ('synthetic-private', json.dumps(old)):
            (self.path / 'state.json').write_text(data)
            code, text, reader = self.invoke()
            self.assertEqual(code, 2)
            reader.assert_not_called()
            self.assertNotIn('synthetic-private', text)
            self.assertEqual((self.path / 'state.json').read_text(), data)

    def test_shared_writer_lock_blocks_before_read(self):
        before = self.seed()
        with Cache(self.path) as cache, cache.writer():
            code, _, reader = self.invoke()
        self.assertEqual(code, 2)
        reader.assert_not_called()
        self.assertEqual((self.path / 'state.json').read_bytes(), before)
        self.invoke()  # Released lock is reusable.

    def test_invalid_config_before_cache_creation(self):
        for extra in (['--timeout', '0'], ['--timeout', '31'], ['--max-age', '-1'],
                      ['--amber-at', 'nan'], ['--bucket', '../outside']):
            code, _, reader = self.invoke(extra=extra)
            self.assertEqual(code, 2)
            reader.assert_not_called()
            self.assertFalse(self.path.exists())

    def test_explicit_live_and_scope_required_no_loop_options(self):
        for args in ([], ['--live'], ['--bucket', 'codex'],
                     ['--live', '--bucket', 'codex', '--max-reads', '2'],
                     ['--live', '--bucket', 'codex', '--interval', '60']):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
                main(['refresh', '--cache-dir', str(self.path)] + args)
            self.assertEqual(caught.exception.code, 2)
            self.assertFalse(self.path.exists())

    def test_write_failure_reports_error_and_preserves_previous(self):
        before = self.seed()
        with patch('cgc.cache.os.replace', side_effect=OSError('synthetic-private')):
            code, text, reader = self.invoke(evidence=True)
        self.assertEqual(code, 2)
        reader.assert_called_once()
        self.assertNotIn('synthetic-private', text)
        self.assertEqual((self.path / 'state.json').read_bytes(), before)

    def test_signal_handlers_restored(self):
        before = {s: signal.getsignal(s) for s in (signal.SIGINT, signal.SIGTERM)}
        self.invoke()
        self.assertEqual(before, {s: signal.getsignal(s) for s in before})

    def test_one_shot_does_not_wait_and_returns_own_published_state(self):
        stop = Mock()
        stop.is_set.return_value = False
        reader = Mock(return_value=observation())
        with Cache(self.path, create=True) as cache:
            state = refresh_once(cache, buckets=['codex'], reader=reader, clock=lambda: STAMP,
                                 stop=stop, evidence_provider=fixture_evidence)
            self.assertEqual(state, cache.read())
            with cache.writer():
                pass
        reader.assert_called_once()
        stop.wait.assert_not_called()

    def test_production_reader_path_normalizes_only_allowlisted_fields(self):
        raw = {'rateLimits': {'limitId': 'codex', 'primary': {'usedPercent': 64}},
               'accountId': 'synthetic-private-identity'}
        output = io.StringIO()
        with patch('cgc.quota.app_server_read', return_value=raw) as transport, \
             contextlib.redirect_stdout(output):
            code = main(['refresh', '--live', '--bucket', 'codex', '--cache-dir',
                         str(self.path), '--json'])
        transport.assert_called_once_with(20)
        result = json.loads(output.getvalue())
        self.assertEqual(code, 1)
        self.assertEqual(result['observation']['windows'][0]['remaining_percent'], 36)
        self.assertEqual(result['observation']['mode'], 'live')  # Simulated, never real source.
        self.assertIsNone(result['policy_state'])
        self.assertNotIn('synthetic-private-identity', output.getvalue())
        self.assertNotIn('synthetic-private-identity', (self.path / 'state.json').read_text())

    def test_production_reader_timeout_no_retry(self):
        output = io.StringIO()
        with patch('cgc.quota.app_server_read', side_effect=QuotaError('TIMEOUT')) as transport, \
             contextlib.redirect_stdout(output):
            code = main(['refresh', '--live', '--bucket', 'codex', '--cache-dir',
                         str(self.path), '--json'])
        transport.assert_called_once()
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(output.getvalue())['error_code'], 'TIMEOUT')

    def test_unsafe_cache_path_blocks_source(self):
        target = self.path.parent / 'target'
        target.mkdir(mode=0o700)
        self.path.symlink_to(target)
        code, _, reader = self.invoke()
        self.assertEqual(code, 2)
        reader.assert_not_called()
        self.assertEqual(list(target.iterdir()), [])

    def test_cancel_before_read_leaves_cache_unpublished(self):
        stop = Mock()
        stop.is_set.return_value = True
        reader = Mock()
        with Cache(self.path, create=True) as cache:
            state = refresh_once(cache, buckets=['codex'], reader=reader, stop=stop)
            self.assertEqual(state['generation'], 0)
            self.assertIsNone(cache.read())
        reader.assert_not_called()
        stop.wait.assert_not_called()
