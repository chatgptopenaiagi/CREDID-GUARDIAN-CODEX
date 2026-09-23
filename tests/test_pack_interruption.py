"""Real active index-pack interruption after temporary pack arrival."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import unittest

from cgc import checkpoint as cp
from cgc.handoff import HandoffStore
import test_transfer_interruption as fixtures


class PackInterruptionTests(unittest.TestCase):
    # Reuse fixture utilities, not inherited test methods/discovery.
    git = fixtures.TransferInterruptionTests.git
    tree = fixtures.TransferInterruptionTests.tree
    bare = fixtures.TransferInterruptionTests.bare
    tip = fixtures.TransferInterruptionTests.tip
    args = fixtures.TransferInterruptionTests.args
    record = fixtures.TransferInterruptionTests.record
    publish = fixtures.TransferInterruptionTests.publish
    state = fixtures.TransferInterruptionTests.state
    read_line = fixtures.TransferInterruptionTests.read_line
    metadata = fixtures.TransferInterruptionTests.metadata
    pipeline = fixtures.TransferInterruptionTests.pipeline

    def setUp(self):
        fixtures.TransferInterruptionTests.setUp(self)
        # Observed Git 2.55.0 selects index-pack with this real object count.
        # No unpack-limit override or fabricated receiving command is used.
        for number in range(128):
            (self.root / f'count-{number}.txt').write_text(f'synthetic object {number}\n')
        self.git('add', '--', *[f'count-{n}.txt' for n in range(128)])
        self.git('commit', '-qm', 'synthetic pack count')
        self.head = self.git('rev-parse', 'HEAD').decode().strip()

    def objects(self):
        return {p.relative_to(self.remote / 'objects').as_posix(): p.read_bytes()
                for p in (self.remote / 'objects').rglob('*') if p.is_file()}

    def transfer(self, mode):
        before = self.tree()
        remote_metadata = self.metadata()
        old_objects = self.objects()
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
            # Real receiver + actual nonempty temporary pack are the rendezvous.
            # Polling observes state; elapsed time never stands in for readiness.
            deadline = time.monotonic() + 2
            while True:
                pipeline = self.pipeline(fetch)
                receivers = [pid for pid, cmd in pipeline.items() if b'index-pack' in cmd]
                packs = list((self.remote / 'objects/pack').glob('tmp_pack_*'))
                if receivers and packs and packs[0].stat().st_size > 12:
                    break
                self.assertLess(time.monotonic(), deadline, 'No active index-pack/temporary pack')
                time.sleep(0.01)
            self.assertEqual(len(receivers), 1)
            self.assertEqual(len(packs), 1)
            receiver = receivers[0]
            receiver_files = [os.readlink(p) for p in Path(f'/proc/{receiver}/fd').iterdir()]
            self.assertIn(str(packs[0]), receiver_files)
            partial = packs[0].read_bytes()
            self.assertEqual(partial[:4], b'PACK')
            self.assertEqual(int.from_bytes(partial[4:8], 'big'), 2)
            self.assertGreater(int.from_bytes(partial[8:12], 'big'), 100)
            self.assertFalse(list((self.remote / 'objects/pack').glob('*.idx')))
            self.assertFalse(list((self.remote / 'objects/pack').glob('*.pack')))
            self.assertIn(paused['proxy'], pipeline)
            self.assertIn(paused['upload'], pipeline)
            self.assertFalse(any(b'unpack-objects' in cmd for cmd in pipeline.values()))
            for pid in pipeline:
                self.assertEqual(os.getpgid(pid), fetch)
            self.assertEqual(self.tip(), self.base)
            self.assertEqual(self.metadata(), remote_metadata)
            self.assertEqual(self.tree(), before)
            if mode == 'release':
                with open(self.control / 'gate', 'wb') as gate:
                    gate.write(b'G')
            elif mode in ('child_death', 'receiver_death'):
                killed = fetch if mode == 'child_death' else receiver
                os.kill(killed, signal.SIGKILL)
                deadline = time.monotonic() + 1
                while True:
                    try:
                        state = Path(f'/proc/{killed}/stat').read_text().split()[2]
                    except FileNotFoundError:
                        break  # The real fetch may already have reaped index-pack.
                    if state == 'Z':
                        break
                    self.assertLess(time.monotonic(), deadline, 'Git child death not observed')
                    time.sleep(0.01)
                # The real pack pipeline still owns pipes after child death.
                # Source authority must remain held until group cleanup finishes.
                os.kill(paused['proxy'], 0)
                self.assertIsNone(peer.poll())
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
                self.assertFalse(list((self.remote / 'objects/pack').glob('tmp_pack_*')))
                indexes = list((self.remote / 'objects/pack').glob('*.idx'))
                self.assertEqual(len(indexes), 1)
                self.assertTrue(indexes[0].with_suffix('.pack').is_file())
                self.bare('verify-pack', str(indexes[0]))
                self.assertEqual(result['remote_commit'], self.head)
                self.assertEqual(result['tracking_commit'], self.head)
                self.assertEqual(result['safe_to_resume'], 'UNKNOWN')
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
            # SIGKILL group cleanup cannot run Git's temporary-file cleanup.
            # The observed partial pack survives, without being called corruption
            # or publication. Additional Git-managed artifacts are retained too.
            self.assertTrue(packs[0].is_file())
            self.assertTrue(packs[0].read_bytes().startswith(partial))
            self.assertFalse(list((self.remote / 'objects/pack').glob('*.idx')))
            self.assertFalse(list((self.remote / 'objects/pack').glob('*.pack')))
            object_files = self.objects()
            for name, data in old_objects.items(): self.assertEqual(object_files[name], data)
            saved = self.state()
            self.assertEqual(saved['previous_known_good'], prior)
            pending = saved['last_known_good']['record']
            self.assertEqual(pending['phase'], 'PUBLISHING')
            self.assertEqual(pending['notes']['next_exact_action'], self.record()['notes']['next_exact_action'])
            self.assertEqual(pending['notes']['known_failures'], self.record()['notes']['known_failures'])
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
            self.assertEqual(object_files, self.objects())
            self.assertEqual(self.tree(), before)
            self.assertEqual(self.metadata(), remote_metadata)
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

    def test_real_index_pack_released_control(self): self.transfer('release')
    def test_sigint_during_temporary_pack_arrival(self): self.transfer('sigint')
    def test_sigterm_during_temporary_pack_arrival(self): self.transfer('sigterm')
    def test_fetch_death_with_active_index_pack(self): self.transfer('child_death')
    def test_index_pack_death_with_live_pipeline(self): self.transfer('receiver_death')
    def test_timeout_during_temporary_pack_arrival(self): self.transfer('timeout')
