"""Real active commit interruption; fixture hooks never enable production hooks."""
import hashlib
import json
import os
from pathlib import Path
import selectors
import shlex
import signal
import subprocess
import sys
import unittest

from cgc import checkpoint as cp
from cgc.handoff import HandoffStore
import test_checkpoint as fixtures


class CommitInterruptionTests(unittest.TestCase):
    git = fixtures.CheckpointTests.git
    record = fixtures.CheckpointTests.record
    run_checkpoint = fixtures.CheckpointTests.run_checkpoint

    def setUp(self):
        fixtures.CheckpointTests.setUp(self)
        baseline = self.run_checkpoint()
        self.assertEqual(baseline['outcome'], 'LOCAL_CHECKPOINT')
        self.head = baseline['local_commit']
        (self.root / 'work.txt').write_text('next reviewed change\n')
        (self.root / 'unrelated.txt').write_text('untracked human work\n')
        self.control = Path(self.tmp.name) / 'control'
        self.control.mkdir(mode=0o700)
        (self.control / 'hooks').mkdir(mode=0o700)
        for name in ('ready', 'gate'): os.mkfifo(self.control / name, 0o600)

    def state(self):
        with HandoffStore(self.store_dir, project=str(self.root)) as store: return store.read()

    def line(self, stream):
        with selectors.DefaultSelector() as selector:
            selector.register(stream, selectors.EVENT_READ)
            self.assertTrue(selector.select(10), 'Fixture rendezvous timed out')
        data = stream.readline()
        self.assertTrue(data, 'Fixture exited before rendezvous')
        return json.loads(data)

    def args(self):
        return dict(project=str(self.root), expected_head=self.head, branch='main',
                    selected={'work.txt': hashlib.sha256((self.root / 'work.txt').read_bytes()).hexdigest()},
                    policy_reviewed=True, record=self.record(), store_dir=str(self.store_dir),
                    now=fixtures.STAMP)

    def interrupt(self, stage, mode):
        helper = Path('tests/helpers/commit_peer.py').resolve()
        hook = self.control / 'hooks' / stage
        hook.write_text('#!/bin/sh\nexec ' + shlex.join(
            [sys.executable, '-B', str(helper), 'hook', str(self.control)]) + '\n')
        hook.chmod(0o700)
        prior = self.state()['last_known_good']
        old_index = (self.root / '.git/index').read_bytes()
        work = {p.name: (p.read_bytes(), p.stat().st_mode, p.stat().st_mtime_ns)
                for p in self.root.iterdir() if p.is_file()}
        config = (self.root / '.git/config').read_bytes()
        ready = os.fdopen(os.open(self.control / 'ready', os.O_RDONLY | os.O_NONBLOCK), 'rb', buffering=0)
        peer = subprocess.Popen(
            [sys.executable, '-B', str(helper), 'worker', json.dumps(self.args()), str(self.control)],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env={'PATH': '/usr/bin:/bin', 'PYTHONPATH': str(Path('src').resolve())})
        commit = None
        try:
            commit = self.line(peer.stdout)['commit']
            gate = self.line(ready)
            self.assertEqual(gate['parent'], commit)
            self.assertEqual(gate['group'], commit)
            self.assertIn(b'commit', Path(f'/proc/{commit}/cmdline').read_bytes().split(b'\0'))
            os.kill(commit, 0)  # Git itself is alive, waiting for its actual hook.
            observed_head = self.git('rev-parse', 'HEAD').decode().strip()
            staged = (self.root / '.git/index').read_bytes()
            self.assertNotEqual(staged, old_index)
            entries = self.git('ls-files', '--stage', '-z')
            self.assertEqual(self.git('show', ':work.txt'), b'next reviewed change\n')
            self.assertNotIn(b'unrelated.txt', entries)
            accepted = stage == 'post-commit'
            if accepted:
                self.assertNotEqual(observed_head, self.head)
                self.assertEqual(self.git('rev-parse', 'HEAD^').decode().strip(), self.head)
                self.assertEqual(self.git('show', 'HEAD:work.txt'), b'next reviewed change\n')
            else:
                self.assertEqual(observed_head, self.head)
                self.assertEqual(staged, (self.control / 'dispatch-index').read_bytes())
                self.assertFalse((self.root / '.git/index.lock').exists())
            # A fresh expectation reaches the shared writer boundary even after
            # HEAD advances. Existing stale-HEAD refusal is not the lock proof.
            if mode == 'sigterm':
                before_contender = (self.store_dir / 'handoff.json').read_bytes()
                contender = self.run_checkpoint(expected_head=observed_head,
                                                store_dir=str(self.control / 'other-store'))
                self.assertEqual(contender['error_code'], 'WRITER_BUSY', contender)
                self.assertFalse(contender['staging_attempted'])
                self.assertFalse((self.control / 'other-store').exists())
                self.assertEqual((self.store_dir / 'handoff.json').read_bytes(), before_contender)
            if mode == 'release':
                with open(self.control / 'gate', 'wb') as stream: stream.write(b'G')
            elif mode == 'death':
                os.killpg(commit, signal.SIGKILL)
            elif mode != 'timeout':
                peer.send_signal(signal.SIGINT if mode == 'sigint' else signal.SIGTERM)
            result = self.line(peer.stdout)
            peer.wait(timeout=5)
            self.assertEqual(peer.returncode, 0)
            self.assertEqual(peer.stderr.read(), b'')
            self.assertTrue(result['fixture_commit_reaped'])
            self.assertTrue(result['fixture_handlers_restored'])
            self.assertEqual(result['fixture_attempts'], 1)
            for pid in (commit, gate['hook']):
                with self.assertRaises(ProcessLookupError): os.kill(pid, 0)
            self.assertEqual(config, (self.root / '.git/config').read_bytes())
            self.assertEqual(work, {p.name: (p.read_bytes(), p.stat().st_mode, p.stat().st_mtime_ns)
                                    for p in self.root.iterdir() if p.is_file()})
            self.assertEqual(self.git('ls-files', '--stage', '-z'), entries)
            if mode == 'release':
                self.assertEqual(result['outcome'], 'LOCAL_CHECKPOINT', result)
                self.assertEqual(result['local_commit'], self.git('rev-parse', 'HEAD').decode().strip())
                return
            error = {'timeout': 'TIMEOUT', 'death': 'GIT_FAILED'}.get(mode, 'CANCELLED')
            self.assertEqual(result['error_code'], error, result)
            self.assertEqual(result['outcome'], 'PARTIAL')
            self.assertTrue(result['commit_attempted'])
            self.assertIsNone(result['local_commit'])
            self.assertEqual(result['head_before'], self.head)
            self.assertEqual(result['safe_to_resume'], 'UNKNOWN')
            self.assertEqual(result['publication_status'], 'NOT_REQUESTED')
            self.assertEqual(self.git('rev-parse', 'HEAD').decode().strip(), observed_head)
            self.assertEqual((self.root / '.git/index').read_bytes(), staged)
            if accepted:
                self.assertEqual(self.git('rev-parse', 'HEAD^{tree}').decode().strip(), result['tree'])
                self.assertEqual(self.git('rev-list', '--parents', '-n', '1', 'HEAD').decode().split(),
                                 [observed_head, self.head])
            else:
                self.assertFalse((self.root / '.git/index.lock').exists())
            saved = self.state()
            self.assertEqual(saved['previous_known_good'], prior)
            pending = saved['last_known_good']['record']
            self.assertEqual(pending['phase'], 'CHECKPOINTING')
            self.assertIsNone(pending['evidence']['local_commit'])
            self.assertEqual(saved['latest_attempt']['error_code'],
                             'CANCELLED' if error == 'CANCELLED' else 'VERIFICATION_FAILED')
            self.assertEqual(saved['safe_to_resume'], 'UNKNOWN')
            fresh = subprocess.check_output(
                [sys.executable, '-B', '-m', 'cgc', 'handoff-status', '--json',
                 '--project', str(self.root), '--store-dir', str(self.store_dir)],
                env={'PATH': '/usr/bin:/bin', 'PYTHONPATH': str(Path('src').resolve())}, timeout=5)
            self.assertEqual(json.loads(fresh), saved)
            # These Git reads are fresh processes. No success receipt is backfilled.
            status = self.git('status', '--porcelain')
            self.assertIn(b'?? unrelated.txt', status)
            self.assertEqual(b'M  work.txt' in status, not accepted)
            # Explicit stale/repeated invocation refuses; no duplicate commit or
            # cleanup is authorized by a historical pending record.
            refused = self.run_checkpoint()
            self.assertEqual(refused['error_code'], 'TARGET_CHANGED' if accepted else 'EXISTING_STAGING')
            self.assertFalse(refused['commit_attempted'])
            self.assertEqual(self.state(), saved)
            self.assertEqual(self.git('rev-parse', 'HEAD').decode().strip(), observed_head)
            self.assertEqual((self.root / '.git/index').read_bytes(), staged)
            fd = cp.ins._open_root(str(self.root))
            try:
                with cp._writer(fd): pass
            finally: os.close(fd)
            with HandoffStore(self.store_dir, project=str(self.root)) as store, store.writer(): pass
        finally:
            if commit is not None:
                try: os.killpg(commit, signal.SIGKILL)
                except ProcessLookupError: pass
            if peer.poll() is None:
                peer.terminate()
                try: peer.wait(timeout=5)
                except subprocess.TimeoutExpired: peer.kill(); peer.wait(timeout=5)
            ready.close(); peer.stdout.close(); peer.stderr.close()

    def test_pre_acceptance_sigint(self): self.interrupt('pre-commit', 'sigint')
    def test_pre_acceptance_sigterm_and_contender(self): self.interrupt('pre-commit', 'sigterm')
    def test_pre_acceptance_timeout(self): self.interrupt('pre-commit', 'timeout')
    def test_pre_acceptance_process_group_death(self): self.interrupt('pre-commit', 'death')
    def test_post_acceptance_sigint(self): self.interrupt('post-commit', 'sigint')
    def test_post_acceptance_sigterm_and_contender(self): self.interrupt('post-commit', 'sigterm')
    def test_post_acceptance_timeout(self): self.interrupt('post-commit', 'timeout')
    def test_post_acceptance_process_group_death(self): self.interrupt('post-commit', 'death')
    def test_pre_acceptance_released_control(self): self.interrupt('pre-commit', 'release')
    def test_post_acceptance_released_control(self): self.interrupt('post-commit', 'release')
