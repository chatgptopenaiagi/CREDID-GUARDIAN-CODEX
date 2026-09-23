"""Active Git transaction cancellation/concurrency, using Linux-native fixtures."""
import hashlib
import json
import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import threading
import unittest
from unittest.mock import patch

from cgc import checkpoint as cp
from cgc.handoff import HandoffStore
from cgc.preservation import advance, new_attempt
from cgc.signals import mutation_signals
import test_publication as fixtures
import test_checkpoint as checkpoint_fixtures

STAMP = fixtures.STAMP


class MutationInterruptionTests(unittest.TestCase):
    # Reuse fixture methods without inheriting/collecting accepted tests again.
    setUp = fixtures.PublicationTests.setUp
    git = fixtures.PublicationTests.git
    tree = fixtures.PublicationTests.tree
    bare = fixtures.PublicationTests.bare
    tip = fixtures.PublicationTests.tip
    args = fixtures.PublicationTests.args
    record = fixtures.PublicationTests.record
    publish = fixtures.PublicationTests.publish
    state = fixtures.PublicationTests.state

    def line(self, peer):
        with selectors.DefaultSelector() as selector:
            selector.register(peer.stdout, selectors.EVENT_READ)
            self.assertTrue(selector.select(10), 'Fixture rendezvous timed out')
        value = peer.stdout.readline()
        self.assertTrue(value, 'Fixture exited before rendezvous')
        return value

    def active(self, stage='prepared', mode='signal', sig=signal.SIGTERM, compete=False):
        prior = self.state()['last_known_good']
        index = (self.root / '.git/index').read_bytes()
        work = (self.root / 'work.txt').read_bytes()
        peer = subprocess.Popen(
            [sys.executable, '-B', 'tests/helpers/mutation_peer.py',
             json.dumps(self.args()), stage, mode],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env={'PATH': '/usr/bin:/bin', 'PYTHONPATH': str(Path('src').resolve())})
        child = None
        try:
            ready = json.loads(self.line(peer)); child = ready['pid']
            self.assertEqual(ready['ready'], stage)
            expected = self.base if stage == 'prepared' else self.head
            self.assertEqual(self.tip(), expected)
            lock = self.remote / 'refs/heads/main.lock'
            if stage == 'prepared':
                self.assertTrue(lock.exists(), 'Real Git must hold its prepared ref lock')
            if compete:
                saved = (self.store_dir / 'handoff.json').read_bytes()
                remote_before = {str(p.relative_to(self.remote)): p.read_bytes()
                                 for p in self.remote.rglob('*') if p.is_file()}
                # Both adapters must refuse under the shared source lock even with
                # a different external store; neither can erase pending continuity.
                loser = self.publish(store_dir=str(Path(self.tmp.name) / 'other-store'))
                self.assertEqual(loser['error_code'], 'WRITER_BUSY', loser)
                self.assertFalse(loser['publication_attempted'])
                record = advance(new_attempt(str(self.root), now=STAMP, mission='Competing writer',
                                             requested_level='LOCAL_CHECKPOINT',
                                             next_exact_action='Inspect pending writer'),
                                 'DOCUMENTING', now=STAMP)
                loser = cp.checkpoint(str(self.root), expected_head=self.head, branch='main',
                                      selected={'work.txt': hashlib.sha256(work).hexdigest()},
                                      policy_reviewed=True, record=record, now=STAMP,
                                      store_dir=str(Path(self.tmp.name) / 'other-store'))
                self.assertEqual(loser['error_code'], 'WRITER_BUSY', loser)
                self.assertFalse(loser['staging_attempted'])
                self.assertFalse((Path(self.tmp.name) / 'other-store').exists())
                self.assertEqual((self.store_dir / 'handoff.json').read_bytes(), saved)
                self.assertEqual(remote_before, {str(p.relative_to(self.remote)): p.read_bytes()
                                                for p in self.remote.rglob('*') if p.is_file()})
            if mode == 'child_death':
                os.kill(child, signal.SIGKILL)
            elif mode != 'timeout':
                peer.send_signal(sig)
            if mode == 'repeat':
                self.assertEqual(self.line(peer), b'CLEANUP\n')
                peer.send_signal(signal.SIGINT if sig == signal.SIGTERM else signal.SIGTERM)
                peer.stdin.write(b'continue\n'); peer.stdin.flush()
            result = json.loads(self.line(peer))
            peer.wait(timeout=5)
            self.assertEqual(peer.returncode, 0)
            self.assertEqual(peer.stderr.read(), b'')
            error = {'timeout': 'TIMEOUT', 'child_death': 'GIT_FAILED'}.get(mode, 'CANCELLED')
            self.assertEqual(result['error_code'], error, result)
            self.assertEqual(result['publication_status'], 'PUBLICATION_UNCERTAIN')
            self.assertEqual(result['preservation_outcome'], 'LOCAL_CHECKPOINT_ONLY')
            self.assertIsNone(result['remote_commit'])
            self.assertFalse(result['ref_update_succeeded'])
            self.assertTrue(result['handlers_restored']); self.assertTrue(result['child_reaped'])
            with self.assertRaises(ProcessLookupError): os.kill(child, 0)
            self.assertEqual(self.tip(), expected)
            self.assertEqual(self.git('rev-parse', 'HEAD').decode().strip(), self.head)
            self.assertEqual(self.git('rev-parse', 'origin/main').decode().strip(), self.base)
            self.assertEqual((self.root / '.git/index').read_bytes(), index)
            self.assertEqual((self.root / 'work.txt').read_bytes(), work)
            saved = self.state()
            self.assertEqual(saved['previous_known_good'], prior)
            self.assertEqual(saved['last_known_good']['record']['phase'], 'PUBLISHING')
            self.assertIsNone(saved['last_known_good']['record']['evidence']['remote_commit'])
            self.assertEqual(saved['latest_attempt']['error_code'],
                             'CANCELLED' if error == 'CANCELLED' else 'VERIFICATION_FAILED')
            self.assertEqual(saved['safe_to_resume'], 'UNKNOWN')
            fresh = subprocess.check_output(
                [sys.executable, '-B', '-m', 'cgc', 'handoff-status', '--json',
                 '--project', str(self.root), '--store-dir', str(self.store_dir)],
                env={'PATH': '/usr/bin:/bin', 'PYTHONPATH': str(Path('src').resolve())}, timeout=5)
            self.assertEqual(json.loads(fresh), saved)
            fd = cp.ins._open_root(str(self.root))
            try:
                with cp._writer(fd): pass
            finally:
                os.close(fd)
            with HandoffStore(self.store_dir, project=str(self.root)) as store, store.writer(): pass
            if stage == 'prepared':
                # SIGKILL cleanup cannot ask Git to unlink its prepared lock.
                # A new call must refuse it, never delete it or silently retry.
                self.assertTrue(lock.exists())
                after = (self.store_dir / 'handoff.json').read_bytes()
                retry = self.publish()
                self.assertEqual(retry['error_code'], 'UNSAFE_REMOTE_LAYOUT', retry)
                self.assertFalse(retry['publication_attempted'])
                self.assertTrue(lock.exists())
                self.assertEqual((self.store_dir / 'handoff.json').read_bytes(), after)
            else:
                # Fresh current authority/expectation after independently reading
                # Git permits verify-only reconciliation, without republishing.
                reconciled = self.publish(expected_remote=self.head)
                self.assertEqual(reconciled['publication_status'], 'VERIFIED', reconciled)
                self.assertFalse(reconciled['publication_attempted'])
        finally:
            if child is not None:
                try: os.killpg(child, signal.SIGKILL)
                except ProcessLookupError: pass
            peer.stdin.close()
            if peer.poll() is None:
                peer.terminate()
                try: peer.wait(timeout=5)
                except subprocess.TimeoutExpired: peer.kill(); peer.wait(timeout=5)
            peer.stdout.close(); peer.stderr.close()

    def test_sigint_during_prepared_transaction(self): self.active(sig=signal.SIGINT)
    def test_sigterm_during_prepared_transaction(self): self.active()
    def test_sigint_after_acceptance_before_process_exit(self): self.active('committed', sig=signal.SIGINT)
    def test_sigterm_after_acceptance_before_process_exit(self): self.active('committed')
    def test_active_git_process_death(self): self.active(mode='child_death')
    def test_active_git_timeout(self): self.active(mode='timeout')
    def test_repeated_signal_does_not_interrupt_failure_persistence(self): self.active(mode='repeat')
    def test_active_publication_excludes_both_writers(self): self.active(compete=True)
    def test_accepted_publication_still_excludes_both_writers(self): self.active('committed', compete=True)

    def test_publication_inspection_cancellation_stays_cancelled(self):
        prior = self.state()
        with patch.object(cp.ins, 'inspect_project', return_value={'status': 'REFUSED', 'error_code': 'CANCELLED'}):
            result = self.publish()
        self.assertEqual(result['error_code'], 'CANCELLED')
        self.assertFalse(result['publication_attempted'])
        self.assertEqual(self.state(), prior)
        self.assertEqual(self.tip(), self.base)


class CheckpointCancellationTests(unittest.TestCase):
    setUp = checkpoint_fixtures.CheckpointTests.setUp
    git = checkpoint_fixtures.CheckpointTests.git
    record = checkpoint_fixtures.CheckpointTests.record
    run_checkpoint = checkpoint_fixtures.CheckpointTests.run_checkpoint

    def cancel_commit(self, sig, accepted=False):
        real = cp.ins._run
        def run(args, **kwargs):
            if 'commit' not in args: return real(args, **kwargs)
            if accepted: real(args, **kwargs)
            os.kill(os.getpid(), sig)
            self.fail('Cancellation must interrupt the adapter')
        # Actual signals at dispatch/return boundaries; active Git transaction
        # process cleanup is exercised separately above, not claimed here.
        with mutation_signals(), patch.object(cp.ins, '_run', side_effect=run):
            result = self.run_checkpoint()
        self.assertEqual(result['error_code'], 'CANCELLED', result)
        self.assertEqual(result['outcome'], 'PARTIAL')
        self.assertTrue(result['commit_attempted'])
        self.assertIsNone(result['local_commit'])
        self.assertEqual((self.root / 'work.txt').read_text(), 'reviewed change\n')
        current = self.git('rev-parse', 'HEAD').decode().strip()
        if accepted:
            self.assertNotEqual(current, self.head)
            self.assertEqual(self.git('rev-parse', 'HEAD^').decode().strip(), self.head)
            self.assertEqual(self.git('status', '--porcelain'), b'')
        else:
            self.assertEqual(current, self.head)
            self.assertIn(b'M  work.txt', self.git('status', '--porcelain'))
        with HandoffStore(self.store_dir, project=str(self.root)) as store, store.writer():
            saved = store.read()
        self.assertEqual(saved['latest_attempt']['error_code'], 'CANCELLED')
        self.assertEqual(saved['last_known_good']['record']['phase'], 'CHECKPOINTING')
        self.assertIsNone(saved['last_known_good']['record']['evidence']['local_commit'])
        fd = cp.ins._open_root(str(self.root))
        try:
            with cp._writer(fd): pass
        finally:
            os.close(fd)

    def test_sigint_at_commit_dispatch(self): self.cancel_commit(signal.SIGINT)
    def test_sigterm_at_commit_dispatch(self): self.cancel_commit(signal.SIGTERM)
    def test_sigint_after_commit_acceptance(self): self.cancel_commit(signal.SIGINT, accepted=True)
    def test_sigterm_after_commit_acceptance(self): self.cancel_commit(signal.SIGTERM, accepted=True)

    def test_checkpoint_inspection_cancellation_stays_cancelled(self):
        with patch.object(cp.ins, 'inspect_project', return_value={'status': 'REFUSED', 'error_code': 'CANCELLED'}):
            result = self.run_checkpoint()
        self.assertEqual(result['error_code'], 'CANCELLED')
        self.assertFalse(result['staging_attempted'])
        self.assertFalse(self.store_dir.exists())
        self.assertEqual(self.git('rev-parse', 'HEAD').decode().strip(), self.head)


class MutationSignalScopeTests(unittest.TestCase):
    def test_restores_custom_handlers_on_exception(self):
        previous = {s: signal.getsignal(s) for s in (signal.SIGINT, signal.SIGTERM)}
        handler = lambda *_: None
        try:
            for s in previous: signal.signal(s, handler)
            with self.assertRaisesRegex(RuntimeError, 'synthetic'):
                with mutation_signals(): raise RuntimeError('synthetic')
            for s in previous: self.assertIs(signal.getsignal(s), handler)
        finally:
            for s, old in previous.items(): signal.signal(s, old)

    def test_worker_thread_refused_before_changing_handlers(self):
        before = {s: signal.getsignal(s) for s in (signal.SIGINT, signal.SIGTERM)}
        errors = []
        def worker():
            try:
                with mutation_signals(): errors.append('ENTERED')
            except ValueError as error: errors.append(str(error))
        thread = threading.Thread(target=worker); thread.start(); thread.join(timeout=5)
        self.assertFalse(thread.is_alive())
        self.assertEqual(errors, ['SIGNAL_SCOPE_REQUIRES_MAIN_THREAD'])
        self.assertEqual(before, {s: signal.getsignal(s) for s in before})
