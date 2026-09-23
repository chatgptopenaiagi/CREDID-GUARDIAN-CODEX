"""Active object arrival without ref publication in disposable Linux fixtures."""
import hashlib
import json
import os
from pathlib import Path
import selectors
import signal
import subprocess
import sys
import time
import unittest

from cgc import checkpoint as cp
from cgc.handoff import HandoffStore
import test_publication as fixtures


class TransferInterruptionTests(unittest.TestCase):
    git = fixtures.PublicationTests.git
    tree = fixtures.PublicationTests.tree
    bare = fixtures.PublicationTests.bare
    tip = fixtures.PublicationTests.tip
    args = fixtures.PublicationTests.args
    record = fixtures.PublicationTests.record
    publish = fixtures.PublicationTests.publish
    state = fixtures.PublicationTests.state

    def setUp(self):
        fixtures.PublicationTests.setUp(self)
        # Small object count selects Git's ordinary unpack-objects path. Enough
        # deterministic incompressible text keeps a real pack larger than the gate.
        for number in range(12):
            (self.root / f'payload-{number}.txt').write_text(
                hashlib.shake_256(str(number).encode()).hexdigest(64 * 1024))
        self.git('add', '--', *[f'payload-{n}.txt' for n in range(12)])
        self.git('commit', '-qm', 'synthetic transfer payload')
        self.head = self.git('rev-parse', 'HEAD').decode().strip()
        self.control = Path(self.tmp.name) / 'control'
        self.control.mkdir(mode=0o700)
        for name in ('ready', 'gate'):
            os.mkfifo(self.control / name, 0o600)

    def read_line(self, stream):
        with selectors.DefaultSelector() as selector:
            selector.register(stream, selectors.EVENT_READ)
            self.assertTrue(selector.select(10), 'Fixture rendezvous timed out')
        line = stream.readline()
        self.assertTrue(line, 'Fixture exited before rendezvous')
        return json.loads(line)

    def loose(self):
        return {p.relative_to(self.remote / 'objects').as_posix(): p.read_bytes()
                for p in (self.remote / 'objects').glob('[0-9a-f][0-9a-f]/*')
                if len(p.name) == 38 and all(c in '0123456789abcdef' for c in p.name)}

    def metadata(self):
        return {p.relative_to(self.remote).as_posix(): p.read_bytes()
                for p in self.remote.rglob('*') if p.is_file()
                and 'objects' not in p.relative_to(self.remote).parts}

    def pipeline(self, pid):
        result = {}
        pending = [pid]
        while pending:
            current = pending.pop()
            proc = Path('/proc') / str(current)
            try:
                command = (proc / 'cmdline').read_bytes().split(b'\0')
                pending.extend(int(p) for p in (proc / 'task' / str(current) / 'children').read_text().split())
                result[current] = command
            except FileNotFoundError:
                pass  # Short-lived pack-objects may have finished writing its pipe.
        return result

    def transfer(self, mode):
        before = self.tree()
        remote_metadata = self.metadata()
        old_objects = self.loose()
        prior = self.state()['last_known_good']
        readyfd = os.open(self.control / 'ready', os.O_RDONLY | os.O_NONBLOCK)
        ready = os.fdopen(readyfd, 'rb', buffering=0)
        peer = subprocess.Popen(
            [sys.executable, '-B', 'tests/helpers/transfer_peer.py', 'worker',
             json.dumps(self.args()), str(self.control)],
            stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            env={'PATH': '/usr/bin:/bin', 'PYTHONPATH': str(Path('src').resolve())})
        fetch = None
        try:
            fetch = self.read_line(peer.stdout)['fetch']
            paused = self.read_line(ready)
            self.assertEqual(paused['group'], fetch)
            self.assertEqual(paused['forwarded'], 256 * 1024)
            # Synchronize on materialized complete objects, not a sleep/timing guess.
            deadline = time.monotonic() + 2
            while not (arrived := self.loose().keys() - old_objects.keys()):
                self.assertLess(time.monotonic(), deadline, 'No partial object arrival')
                time.sleep(0.01)
            pipeline = self.pipeline(fetch)
            self.assertIn(paused['proxy'], pipeline)
            self.assertIn(paused['upload'], pipeline)
            self.assertTrue(any(b'unpack-objects' in cmd for cmd in pipeline.values()),
                            'Real receiving Git child must still be active')
            for pid in pipeline:
                self.assertEqual(os.getpgid(pid), fetch)
            self.assertEqual(self.tip(), self.base)
            self.assertEqual(self.metadata(), remote_metadata)
            self.assertEqual(self.tree(), before)
            # At least one newly arrived object is valid/readable but unreferenced.
            oid = sorted(arrived)[0].replace('/', '')
            self.assertIn(self.bare('cat-file', '-t', oid).strip(), (b'commit', b'tree', b'blob'))
            if mode == 'release':
                with open(self.control / 'gate', 'wb') as gate:
                    gate.write(b'G')
            elif mode == 'child_death':
                os.kill(fetch, signal.SIGKILL)
                deadline = time.monotonic() + 1
                while Path(f'/proc/{fetch}/stat').read_text().split()[2] != 'Z':
                    self.assertLess(time.monotonic(), deadline, 'Fetch death not observed')
                    time.sleep(0.01)
                # New transfer-specific concurrency surface: the direct child
                # is dead but its descendants still own pipes. The source lock
                # must remain held until bounded group cleanup completes.
                saved_pending = (self.store_dir / 'handoff.json').read_bytes()
                contender = self.publish(store_dir=str(self.control / 'contender-store'))
                self.assertEqual(contender['error_code'], 'WRITER_BUSY', contender)
                self.assertFalse(contender['publication_attempted'])
                self.assertFalse((self.control / 'contender-store').exists())
                self.assertEqual((self.store_dir / 'handoff.json').read_bytes(), saved_pending)
                self.assertEqual(self.tip(), self.base)
            elif mode != 'timeout':
                peer.send_signal(signal.SIGINT if mode == 'sigint' else signal.SIGTERM)
            result = self.read_line(peer.stdout)
            peer.wait(timeout=5)
            self.assertEqual(peer.returncode, 0)
            self.assertEqual(peer.stderr.read(), b'')
            self.assertTrue(result['fixture_fetch_reaped'])
            self.assertEqual(result['fixture_transfers'], 1)
            for pid in pipeline:
                with self.assertRaises(ProcessLookupError): os.kill(pid, 0)
            if mode == 'release':
                self.assertEqual(result['publication_status'], 'VERIFIED', result)
                self.assertEqual(self.tip(), self.head)
                self.assertEqual(result['fixture_ref_updates'], 2)
                return
            self.assertEqual(self.tree(), before)
            self.assertEqual(result['publication_status'], 'PUBLICATION_UNCERTAIN', result)
            self.assertEqual(result['preservation_outcome'], 'LOCAL_CHECKPOINT_ONLY')
            expected = 'CANCELLED' if mode in ('sigint', 'sigterm') else 'TIMEOUT'
            self.assertEqual(result['error_code'], expected, result)
            self.assertEqual(result['fixture_ref_updates'], 0)
            self.assertFalse(result['ref_update_succeeded'])
            self.assertIsNone(result['remote_commit']); self.assertIsNone(result['tracking_commit'])
            self.assertEqual(result['safe_to_resume'], 'UNKNOWN')
            self.assertEqual(self.tip(), self.base)
            self.assertEqual(self.metadata(), remote_metadata)
            survivors = self.loose()
            self.assertTrue(arrived <= survivors.keys())
            for name, data in old_objects.items(): self.assertEqual(survivors[name], data)
            # Retain every object-store file, including any incomplete temporary
            # object. Read-only reconciliation and authority refusal must not GC it.
            object_files = {str(p.relative_to(self.remote)): p.read_bytes()
                            for p in (self.remote / 'objects').rglob('*') if p.is_file()}
            saved = self.state()
            self.assertEqual(saved['previous_known_good'], prior)
            pending = saved['last_known_good']['record']
            self.assertEqual(pending['phase'], 'PUBLISHING')
            self.assertEqual(pending['evidence']['local_commit'], self.head)
            self.assertIsNone(pending['evidence']['remote_commit'])
            self.assertEqual(saved['latest_attempt']['error_code'],
                             'CANCELLED' if expected == 'CANCELLED' else 'VERIFICATION_FAILED')
            self.assertEqual(saved['safe_to_resume'], 'UNKNOWN')
            fresh = subprocess.check_output(
                [sys.executable, '-B', '-m', 'cgc', 'handoff-status', '--json',
                 '--project', str(self.root), '--store-dir', str(self.store_dir)],
                env={'PATH': '/usr/bin:/bin', 'PYTHONPATH': str(Path('src').resolve())}, timeout=5)
            self.assertEqual(json.loads(fresh), saved)
            # Fresh read-only Git process establishes the unchanged remote tip;
            # no resume engine, repair or automatic second publication is invoked.
            live = self.git('ls-remote', '--refs', str(self.remote), 'refs/heads/main')
            self.assertEqual(live, (self.base + '\trefs/heads/main\n').encode())
            refused = self.publish(publication_reviewed=False)
            self.assertEqual(refused['error_code'], 'CURRENT_PUBLICATION_AUTHORITY_REQUIRED')
            self.assertEqual(self.state(), saved)
            self.assertEqual(self.loose(), survivors)
            self.assertEqual(object_files, {str(p.relative_to(self.remote)): p.read_bytes()
                                           for p in (self.remote / 'objects').rglob('*') if p.is_file()})
            fd = cp.ins._open_root(str(self.root))
            try:
                with cp._writer(fd): pass
            finally:
                os.close(fd)
            with HandoffStore(self.store_dir, project=str(self.root)) as store, store.writer(): pass
        finally:
            if fetch is not None:
                try: os.killpg(fetch, signal.SIGKILL)
                except ProcessLookupError: pass
            if peer.poll() is None:
                peer.terminate()
                try: peer.wait(timeout=5)
                except subprocess.TimeoutExpired: peer.kill(); peer.wait(timeout=5)
            ready.close(); peer.stdout.close(); peer.stderr.close()

    def test_real_transfer_control_released(self): self.transfer('release')
    def test_sigint_during_object_arrival(self): self.transfer('sigint')
    def test_sigterm_during_object_arrival(self): self.transfer('sigterm')
    def test_fetch_death_with_live_transfer_descendants(self): self.transfer('child_death')
    def test_timeout_during_object_arrival(self): self.transfer('timeout')
