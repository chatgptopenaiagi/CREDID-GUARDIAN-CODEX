"""SIGKILL of CGC, surviving real add, and independent refusal (Linux only)."""
import ctypes
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import unittest

from cgc import checkpoint as cp
from cgc.cache import CacheError
from cgc.handoff import HandoffStore
import test_add_interruption as add
import test_checkpoint as fixtures


FRESH_CALL = """
import json, subprocess, sys
from cgc.checkpoint import checkpoint
real = subprocess.Popen
mutations = []
def observed(command, **kwargs):
    if any(item in command for item in ('add', 'commit', 'update-ref', 'push',
                                        'reset', 'restore', 'clean', 'gc', 'prune')):
        mutations.append(command)
    return real(command, **kwargs)
subprocess.Popen = observed
result = checkpoint(**json.load(sys.stdin))
result['fixture_mutations'] = mutations
print(json.dumps(result))
"""


class ParentDeathTests(unittest.TestCase):
    git = add.AddInterruptionTests.git
    record = add.AddInterruptionTests.record
    run_checkpoint = add.AddInterruptionTests.run_checkpoint
    read_line = add.AddInterruptionTests.read_line
    state = add.AddInterruptionTests.state
    entries = add.AddInterruptionTests.entries
    work = add.AddInterruptionTests.work
    setUp = add.AddInterruptionTests.setUp

    @classmethod
    def setUpClass(cls):
        add.AddInterruptionTests.setUpClass.__func__(cls)

    def wait_orphan(self, pid):
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            found, status = os.waitpid(pid, os.WNOHANG)
            if found:
                return os.waitstatus_to_exitcode(status)
            time.sleep(.01)  # Bounded reap polling, never mutation-stage selection.
        self.fail('fixture orphan did not exit')

    def parent_death(self, stage):
        # Test hygiene only: adopt this fixture's orphan for explicit final reaping.
        # Restore the runner's original subreaper setting, even on assertion failure.
        libc = ctypes.CDLL(None, use_errno=True)
        previous = ctypes.c_int()
        self.assertEqual(libc.prctl(37, ctypes.byref(previous), 0, 0, 0), 0)
        self.assertEqual(libc.prctl(36, 1, 0, 0, 0), 0)
        self.addCleanup(lambda: self.assertEqual(libc.prctl(36, previous.value, 0, 0, 0), 0))
        args = dict(project=str(self.root), expected_head=self.head, branch='main',
                    selected=self.selected, policy_reviewed=True, record=self.record(),
                    store_dir=str(self.store_dir), now=fixtures.STAMP)
        env = {'PATH': '/usr/bin:/bin', 'PYTHONPATH': str(Path('src').resolve())}
        prior = self.state()['last_known_good']
        index, lock = self.root / '.git/index', self.root / '.git/index.lock'
        old_index, old_entries = index.read_bytes(), self.entries()
        work, config = self.work(), (self.root / '.git/config').read_bytes()
        ready = os.fdopen(os.open(self.control / 'ready', os.O_RDONLY | os.O_NONBLOCK), 'rb', buffering=0)
        peer = subprocess.Popen([sys.executable, '-B', 'tests/helpers/add_peer.py', json.dumps(args),
                                 str(self.control), self.library, stage], env=env,
                                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        child = None
        reaped = False
        try:
            child = self.read_line(peer.stdout)['add']
            self.assertEqual(self.read_line(ready), {'git': child, 'group': child})
            def topology():
                status = Path(f'/proc/{child}/status').read_text()
                ppid = int(next(line.split()[1] for line in status.splitlines() if line.startswith('PPid:')))
                return ppid, os.getpgid(child), os.getsid(child)
            self.assertEqual(topology(), (peer.pid, child, child))
            self.assertNotEqual(os.getpgid(peer.pid), child)
            self.assertIn(b'add', Path(f'/proc/{child}/cmdline').read_bytes().split(b'\0'))
            fd = cp.ins._open_root(str(self.root))
            try:
                with self.assertRaisesRegex(cp.CheckpointError, 'WRITER_BUSY'):
                    with cp._writer(fd): pass
            finally:
                os.close(fd)
            with HandoffStore(self.store_dir, project=str(self.root)) as store:
                with self.assertRaisesRegex(CacheError, 'WRITER_BUSY'):
                    with store.writer(): pass
            pending = self.state()
            handoff = (self.store_dir / 'handoff.json').read_bytes()
            self.assertEqual(pending['previous_known_good'], prior)
            record = pending['last_known_good']['record']
            self.assertEqual(record['phase'], 'CHECKPOINTING')
            self.assertEqual(record['notes']['files_changed'], sorted(self.selected))
            self.assertIsNone(record['evidence']['local_commit'])
            self.assertEqual(pending['safe_to_resume'], 'UNKNOWN')
            self.assertEqual(pending['latest_attempt']['status'], 'PUBLISHED')
            self.assertIsNone(pending['latest_attempt']['error_code'])
            at_gate = index.read_bytes()
            entries = self.entries()
            self.assertEqual(lock.exists(), stage == 'before')
            candidate = lock.read_bytes() if lock.exists() else at_gate
            intended = self.entries(lock) if lock.exists() else entries
            self.assertEqual(set(intended), (set(old_entries) - {b'delete.txt'}) | {b'new.txt'})
            self.assertNotEqual(intended[b'work.txt'], old_entries[b'work.txt'])
            self.assertEqual(intended[b'unrelated.txt'], old_entries[b'unrelated.txt'])
            if stage == 'before':
                self.assertEqual(at_gate, old_index)
                self.assertEqual(entries, old_entries)
            else:
                self.assertNotEqual(at_gate, old_index)
            peer.kill()
            self.assertEqual(peer.wait(timeout=5), -signal.SIGKILL)
            self.assertFalse(Path(f'/proc/{peer.pid}').exists())
            self.assertEqual(topology(), (os.getpid(), child, child))
            # Both CGC flock domains are available while real Git remains gated.
            fd = cp.ins._open_root(str(self.root))
            try:
                with cp._writer(fd): pass
            finally:
                os.close(fd)
            with HandoffStore(self.store_dir, project=str(self.root)) as store, store.writer(): pass
            for authority, code in ((False, 'CURRENT_AUTHORITY_REQUIRED'),
                                    (True, 'GIT_LOCK_PRESENT' if stage == 'before' else 'EXISTING_STAGING')):
                current = dict(args, policy_reviewed=authority)
                fresh = subprocess.check_output([sys.executable, '-B', '-c',
                    FRESH_CALL],
                    input=json.dumps(current).encode(), env=env, timeout=10)
                result = json.loads(fresh)
                self.assertEqual(result['error_code'], code, result)
                self.assertEqual(result['outcome'], 'REFUSED')
                self.assertEqual(result['fixture_mutations'], [])
                self.assertFalse(result['staging_attempted'])
                self.assertFalse(result['commit_attempted'])
                self.assertIsNone(result['local_commit'])
                self.assertEqual(result['publication_status'], 'NOT_REQUESTED')
                self.assertEqual(result['safe_to_resume'], 'UNKNOWN')
                self.assertEqual(topology(), (os.getpid(), child, child))
                self.assertEqual(index.read_bytes(), at_gate)
                self.assertEqual(self.entries(), entries)
                self.assertEqual(lock.exists(), stage == 'before')
                if lock.exists(): self.assertEqual(lock.read_bytes(), candidate)
                self.assertEqual((self.store_dir / 'handoff.json').read_bytes(), handoff)
                self.assertEqual(self.work(), work)
                self.assertEqual((self.root / '.git/config').read_bytes(), config)
                self.assertEqual(self.git('rev-parse', 'HEAD').decode().strip(), self.head)
            fresh = subprocess.check_output([sys.executable, '-B', '-m', 'cgc', 'handoff-status',
                '--json', '--project', str(self.root), '--store-dir', str(self.store_dir)], env=env, timeout=5)
            self.assertEqual(json.loads(fresh), pending)
            # Harness releases/reaps only AFTER all production refusal assertions.
            with open(self.control / 'gate', 'wb') as stream: stream.write(b'G')
            self.assertEqual(self.wait_orphan(child), 0)
            reaped = True
            self.assertEqual(self.entries(), intended)
            self.assertFalse(lock.exists())
            self.assertEqual(self.git('rev-parse', 'HEAD').decode().strip(), self.head)
            self.assertEqual(self.work(), work)
            self.assertEqual((self.store_dir / 'handoff.json').read_bytes(), handoff)
        finally:
            if peer.poll() is None: peer.kill(); peer.wait(timeout=5)
            if child is not None and not reaped:
                try: os.killpg(child, signal.SIGKILL)
                except ProcessLookupError: pass
                self.wait_orphan(child)
            ready.close(); peer.stdout.close(); peer.stderr.close()

    def test_parent_death_before_index_replacement(self): self.parent_death('before')
    def test_parent_death_after_index_replacement(self): self.parent_death('after')
