"""Deterministic process rendezvous at crash/signal boundaries; no live source."""
import json
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import tempfile
import unittest

from cgc.cache import Cache, CacheError
from cgc.engine import empty_state
from synthetic_support import refresh
from test_engine import populated, observation, STAMP

HELPER = Path(__file__).parent / 'helpers' / 'interruption_peer.py'


class InterruptionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'cache'

    def seed(self):
        with Cache(self.path, create=True) as cache, cache.writer():
            cache.write(populated())
        return (self.path / 'state.json').read_bytes()

    def spawn(self, mode, stage):
        child = subprocess.Popen([sys.executable, '-B', str(HELPER), str(self.path), mode, stage],
                                 stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        def cleanup():
            if child.poll() is None:
                child.kill()
            child.communicate(timeout=8)
        self.addCleanup(cleanup)
        with selectors.DefaultSelector() as selector:
            selector.register(child.stdout, selectors.EVENT_READ)
            self.assertTrue(selector.select(8), 'checkpoint timed out')
            self.assertEqual(child.stdout.readline(), b'READY\n')
        return child

    def crash(self, stage):
        for seeded in (False, True):
            with self.subTest(seeded=seeded):
                # Each case gets a separate cache, including separate abandoned temp files.
                self.path = Path(self.temp.name) / str(seeded)
                before = self.seed() if seeded else None
                child = self.spawn('crash', stage)
                with Cache(self.path) as cache:
                    with self.assertRaises(CacheError):
                        with cache.writer():
                            pass
                child.kill()
                _, stderr = child.communicate(timeout=8)
                self.assertEqual(child.returncode, -signal.SIGKILL)
                self.assertEqual(stderr, b'')
                with Cache(self.path) as cache, cache.writer():
                    current = cache.read()
                    if stage == 'after_replace':
                        previous = populated() if seeded else empty_state(['codex'])
                        self.assertEqual(current, refresh(previous, observation(95), now=STAMP))
                    elif seeded:
                        self.assertEqual((self.path / 'state.json').read_bytes(), before)
                        self.assertEqual(current, populated())
                    else:
                        self.assertIsNone(current)
                    leftovers = list(self.path.glob('.state-*.tmp'))
                    self.assertEqual(len(leftovers), int(stage in ('partial_write', 'before_replace')))
                    for file in leftovers:
                        self.assertEqual(file.stat().st_mode & 0o777, 0o600)
                    # Restart can publish while leaving unowned crash artifacts alone.
                    state = refresh(current or empty_state(['codex']), observation(95), now=STAMP)
                    cache.write(state)
                    self.assertEqual(cache.read(), state)
                    self.assertEqual(list(self.path.glob('.state-*.tmp')), leftovers)

    def test_kill_before_refresh(self):
        self.crash('before_read')

    def test_kill_during_refresh(self):
        self.crash('during_read')

    def test_kill_after_valid_observation(self):
        self.crash('after_observation')

    def test_kill_during_partial_temp_write(self):
        self.crash('partial_write')

    def test_kill_before_atomic_replace(self):
        self.crash('before_replace')

    def test_kill_after_atomic_replace(self):
        self.crash('after_replace')

    def interrupted(self, mode, stage, sig):
        self.seed()
        child = self.spawn(mode, stage)
        child.send_signal(sig)
        # Release in-flight read only after delivering signal. Event-setting handlers
        # return to the blocked read; a second iteration must never start.
        stdout, stderr = child.communicate(input=b'x', timeout=8)
        self.assertEqual(child.returncode, 0)
        self.assertEqual(stderr, b'')
        result = json.loads(stdout)
        self.assertEqual(result['children_reaped'], int(stage == 'timeout'))
        with Cache(self.path) as cache, cache.writer():
            state = cache.read()
        self.assertEqual(state['generation'], 2)
        if stage == 'timeout':
            self.assertEqual(state['error_code'], 'TIMEOUT')
            self.assertEqual(state['last_valid_observation'], populated()['last_valid_observation'])
            self.assertEqual(result['exit'], 1)
        else:
            self.assertEqual(state['last_refresh_status'], 'OK')
            self.assertEqual(state['policy']['policy_state'], 'EMERGENCY')
        if mode == 'daemon':
            self.assertEqual(result['output'], {'attempts': 1, 'stopped': True})
        else:
            self.assertEqual(result['exit'], 1)  # Synthetic policy never live.
            self.assertFalse(result['output']['live_policy_available'])

    def test_sigint_daemon_wait(self):
        self.interrupted('daemon', 'wait', signal.SIGINT)

    def test_sigint_daemon_read(self):
        self.interrupted('daemon', 'read_success', signal.SIGINT)

    def test_sigint_refresh_read(self):
        self.interrupted('refresh', 'read_success', signal.SIGINT)

    def test_sigint_daemon_transport_timeout_cleanup(self):
        self.interrupted('daemon', 'timeout', signal.SIGINT)

    def test_sigint_refresh_transport_timeout_cleanup(self):
        self.interrupted('refresh', 'timeout', signal.SIGINT)

    def test_sigterm_refresh_transport_timeout_cleanup(self):
        self.interrupted('refresh', 'timeout', signal.SIGTERM)
