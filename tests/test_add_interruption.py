"""Real Git staging before/after index replacement; shim is fixture-only."""
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import unittest

from cgc import checkpoint as cp
from cgc.handoff import HandoffStore
import test_checkpoint as fixtures
import test_transfer_interruption as transfer


class AddInterruptionTests(unittest.TestCase):
    git = fixtures.CheckpointTests.git
    record = fixtures.CheckpointTests.record
    run_checkpoint = fixtures.CheckpointTests.run_checkpoint
    read_line = transfer.TransferInterruptionTests.read_line

    @classmethod
    def setUpClass(cls):
        cls.build = tempfile.TemporaryDirectory(prefix='cgc-add-shim-', dir='/tmp')
        cls.addClassCleanup(cls.build.cleanup)
        cls.library = str(Path(cls.build.name) / 'add_gate.so')
        subprocess.run(['cc', '-shared', '-fPIC', '-Wall', '-Wextra', '-Werror',
                        '-o', cls.library, 'tests/helpers/add_gate.c', '-ldl'],
                       check=True, timeout=20, capture_output=True)

    def setUp(self):
        fixtures.CheckpointTests.setUp(self)
        (self.root / 'delete.txt').write_text('approved deletion candidate\n')
        (self.root / 'unrelated.txt').write_text('tracked baseline\n')
        self.git('add', '--', 'work.txt', 'delete.txt', 'unrelated.txt')
        self.git('commit', '-qm', 'synthetic staging baseline')
        self.head = self.git('rev-parse', 'HEAD').decode().strip()
        (self.root / 'work.txt').write_text('seed known-good checkpoint\n')
        result = self.run_checkpoint()
        self.assertEqual(result['outcome'], 'LOCAL_CHECKPOINT', result)
        self.head = result['local_commit']
        (self.root / 'work.txt').write_text('reviewed next modification\n')
        (self.root / 'new.txt').write_text('reviewed new file\n')
        (self.root / 'delete.txt').unlink()
        (self.root / 'unrelated.txt').write_text('unrelated human modification\n')
        (self.root / 'human.txt').write_text('untracked human work\n')
        self.selected = {name: hashlib.sha256((self.root / name).read_bytes()).hexdigest()
                         for name in ('work.txt', 'new.txt')}
        self.selected['delete.txt'] = None
        self.control = Path(self.tmp.name) / 'control'
        self.control.mkdir(mode=0o700)
        for name in ('ready', 'gate'):
            os.mkfifo(self.control / name, 0o600)

    def state(self):
        with HandoffStore(self.store_dir, project=str(self.root)) as store:
            return store.read()

    def entries(self, index=None):
        env = {'PATH': '/usr/bin:/bin', 'GIT_CONFIG_NOSYSTEM': '1',
               'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_OPTIONAL_LOCKS': '0'}
        if index is not None:
            env['GIT_INDEX_FILE'] = str(index)
        data = subprocess.check_output(['/usr/bin/git', '-C', str(self.root),
                                        'ls-files', '--stage', '-z'], env=env, timeout=5)
        return dict(row.split(b'\t', 1)[::-1] for row in data.split(b'\0') if row)

    def work(self):
        return {p.name: (p.read_bytes(), p.stat().st_mode, p.stat().st_size, p.stat().st_mtime_ns)
                for p in self.root.iterdir() if p.is_file()}

    def interrupt(self, stage, mode):
        prior = self.state()['last_known_good']
        index = self.root / '.git/index'
        lock = self.root / '.git/index.lock'
        before_bytes, before_entries, work = index.read_bytes(), self.entries(), self.work()
        config = (self.root / '.git/config').read_bytes()
        intended = dict(before_entries)
        del intended[b'delete.txt']
        for name in ('new.txt', 'work.txt'):
            data = (self.root / name).read_bytes()
            oid = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            intended[name.encode()] = ('100644 ' + oid + ' 0').encode()
        args = dict(project=str(self.root), expected_head=self.head, branch='main',
                    selected=self.selected, policy_reviewed=True, record=self.record(),
                    store_dir=str(self.store_dir), now=fixtures.STAMP)
        ready = os.fdopen(os.open(self.control / 'ready', os.O_RDONLY | os.O_NONBLOCK),
                          'rb', buffering=0)
        peer = subprocess.Popen([sys.executable, '-B', 'tests/helpers/add_peer.py',
                                 json.dumps(args), str(self.control), self.library, stage],
                                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                env={'PATH': '/usr/bin:/bin', 'PYTHONPATH': str(Path('src').resolve())})
        child = None
        try:
            child = self.read_line(peer.stdout)['add']
            gate = self.read_line(ready)
            self.assertEqual(gate, {'git': child, 'group': child})
            self.assertIn(b'add', Path(f'/proc/{child}/cmdline').read_bytes().split(b'\0'))
            os.kill(child, 0)
            self.assertEqual(self.git('rev-parse', 'HEAD').decode().strip(), self.head)
            installed = stage == 'after'
            self.assertEqual(lock.exists(), not installed)
            self.assertEqual(self.entries(), intended if installed else before_entries)
            if installed:
                self.assertNotEqual(index.read_bytes(), before_bytes)
                candidate = index.read_bytes()
            else:
                self.assertEqual(index.read_bytes(), before_bytes)
                self.assertEqual(self.entries(lock), intended)
                candidate = lock.read_bytes()
            self.assertEqual(candidate[:4], b'DIRC')
            at_gate = index.read_bytes()
            if mode == 'sigterm':
                pending = (self.store_dir / 'handoff.json').read_bytes()
                contender = self.run_checkpoint(selected=self.selected,
                                                store_dir=str(self.control / 'contender'))
                self.assertEqual(contender['error_code'], 'WRITER_BUSY', contender)
                self.assertFalse(contender['staging_attempted'])
                self.assertFalse((self.control / 'contender').exists())
                self.assertEqual((self.store_dir / 'handoff.json').read_bytes(), pending)
            if mode == 'release':
                with open(self.control / 'gate', 'wb') as stream:
                    stream.write(b'G')
            elif mode == 'death':
                os.kill(child, signal.SIGKILL)
            elif mode != 'timeout':
                peer.send_signal(signal.SIGINT if mode == 'sigint' else signal.SIGTERM)
            result = self.read_line(peer.stdout)
            peer.wait(timeout=5)
            self.assertEqual(peer.returncode, 0)
            self.assertEqual(peer.stderr.read(), b'')
            self.assertTrue(result['fixture_child_reaped'])
            self.assertTrue(result['fixture_handlers_restored'])
            self.assertEqual(result['fixture_adds'], 1)
            with self.assertRaises(ProcessLookupError):
                os.kill(child, 0)
            self.assertEqual(self.work(), work)
            self.assertEqual((self.root / '.git/config').read_bytes(), config)
            self.assertEqual(result['safe_to_resume'], 'UNKNOWN')
            self.assertEqual(result['publication_status'], 'NOT_REQUESTED')
            if mode == 'release':
                self.assertEqual(result['outcome'], 'LOCAL_CHECKPOINT', result)
                self.assertEqual(result['fixture_commits'], 1)
                self.assertEqual(self.entries(), intended)
                self.assertFalse(lock.exists())
                self.assertEqual(result['local_commit'], self.git('rev-parse', 'HEAD').decode().strip())
                self.assertEqual(self.git('rev-parse', 'HEAD^').decode().strip(), self.head)
                return
            expected = {'timeout': 'TIMEOUT', 'death': 'GIT_FAILED'}.get(mode, 'CANCELLED')
            self.assertEqual(result['error_code'], expected, result)
            self.assertEqual(result['outcome'], 'PARTIAL')
            self.assertTrue(result['staging_attempted'])
            self.assertFalse(result['commit_attempted'])
            self.assertEqual(result['fixture_commits'], 0)
            self.assertIsNone(result['local_commit'])
            self.assertEqual(self.git('rev-parse', 'HEAD').decode().strip(), self.head)
            self.assertEqual(index.read_bytes(), at_gate)
            self.assertEqual(self.entries(), intended if installed else before_entries)
            self.assertEqual(lock.exists(), not installed)
            if not installed:
                self.assertEqual(lock.read_bytes(), candidate)
            saved = self.state()
            self.assertEqual(saved['previous_known_good'], prior)
            pending = saved['last_known_good']['record']
            self.assertEqual(pending['phase'], 'CHECKPOINTING')
            self.assertEqual(pending['notes']['files_changed'], sorted(self.selected))
            for key in ('known_failures', 'next_exact_action'):
                self.assertEqual(pending['notes'][key], self.record()['notes'][key])
            self.assertIsNone(pending['evidence']['local_commit'])
            self.assertEqual(saved['latest_attempt']['error_code'],
                             'CANCELLED' if expected == 'CANCELLED' else 'VERIFICATION_FAILED')
            self.assertEqual(saved['safe_to_resume'], 'UNKNOWN')
            fresh = subprocess.check_output([sys.executable, '-B', '-m', 'cgc', 'handoff-status',
                                             '--json', '--project', str(self.root),
                                             '--store-dir', str(self.store_dir)],
                                            env={'PATH': '/usr/bin:/bin',
                                                 'PYTHONPATH': str(Path('src').resolve())}, timeout=5)
            self.assertEqual(json.loads(fresh), saved)
            status = self.git('status', '--porcelain')
            self.assertIn(b' M unrelated.txt', status)
            self.assertIn(b'?? human.txt', status)
            self.assertEqual(b'M  work.txt' in status, installed)
            refused = self.run_checkpoint(selected=self.selected)
            self.assertEqual(refused['error_code'], 'EXISTING_STAGING' if installed else 'GIT_LOCK_PRESENT')
            self.assertFalse(refused['staging_attempted'])
            self.assertEqual(self.state(), saved)
            self.assertEqual(index.read_bytes(), at_gate)
            self.assertEqual(self.work(), work)
            if not installed:
                self.assertEqual(lock.read_bytes(), candidate)
            fd = cp.ins._open_root(str(self.root))
            try:
                with cp._writer(fd): pass
            finally:
                os.close(fd)
            with HandoffStore(self.store_dir, project=str(self.root)) as store, store.writer(): pass
        finally:
            if child is not None:
                try: os.killpg(child, signal.SIGKILL)
                except ProcessLookupError: pass
            if peer.poll() is None:
                peer.terminate()
                try: peer.wait(timeout=5)
                except subprocess.TimeoutExpired: peer.kill(); peer.wait(timeout=5)
            ready.close(); peer.stdout.close(); peer.stderr.close()

    def test_before_index_rename_sigint(self): self.interrupt('before', 'sigint')
    def test_before_index_rename_sigterm_and_contender(self): self.interrupt('before', 'sigterm')
    def test_before_index_rename_timeout(self): self.interrupt('before', 'timeout')
    def test_before_index_rename_child_death(self): self.interrupt('before', 'death')
    def test_after_index_rename_sigint(self): self.interrupt('after', 'sigint')
    def test_after_index_rename_sigterm_and_contender(self): self.interrupt('after', 'sigterm')
    def test_after_index_rename_timeout(self): self.interrupt('after', 'timeout')
    def test_after_index_rename_child_death(self): self.interrupt('after', 'death')
    def test_before_index_rename_released_control(self): self.interrupt('before', 'release')
    def test_after_index_rename_released_control(self): self.interrupt('after', 'release')
