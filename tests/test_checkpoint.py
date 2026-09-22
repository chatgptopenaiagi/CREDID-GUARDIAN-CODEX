"""Manual checkpoint acceptance in disposable Linux Git repositories only."""
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from cgc import checkpoint as cp
from cgc.handoff import HandoffStore
from cgc.preservation import new_attempt, advance
import test_inspection as fixtures

STAMP = '2026-09-22T00:00:00Z'


class CheckpointTests(unittest.TestCase):
    git = fixtures.InspectionTests.git
    tree = fixtures.InspectionTests.tree

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='cgc-checkpoint-', dir='/tmp')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'project'
        self.root.mkdir(mode=0o700)
        self.store_dir = Path(self.tmp.name) / 'handoff'
        self.git('init', '-q', '-b', 'main')
        self.git('config', 'user.name', 'Synthetic')
        self.git('config', 'user.email', 'synthetic@example.invalid')
        (self.root / 'work.txt').write_text('base\n')
        self.git('add', '--', 'work.txt'); self.git('commit', '-qm', 'base')
        self.head = self.git('rev-parse', 'HEAD').decode().strip()
        (self.root / 'work.txt').write_text('reviewed change\n')

    def record(self):
        record = new_attempt(str(self.root), now=STAMP, mission='Synthetic local checkpoint',
                             requested_level='LOCAL_CHECKPOINT', next_exact_action='Reconcile Git and continue tests')
        return advance(record, 'DOCUMENTING', now=STAMP,
                       notes={'complete': ['Reviewed change'], 'partial': ['Project'],
                              'not_started': ['Remote publication'], 'tests_run': ['Synthetic project test'],
                              'test_results': ['One failure'], 'known_failures': ['Known synthetic failure']},
                       test_status='FAILED')

    def run_checkpoint(self, paths=('work.txt',), **overrides):
        selected = {p: hashlib.sha256((self.root / p).read_bytes()).hexdigest()
                    if (self.root / p).is_file() else None for p in paths}
        args = dict(expected_head=self.head, branch='main', selected=selected,
                    policy_reviewed=True, record=self.record(), store_dir=self.store_dir, now=STAMP)
        args.update(overrides)
        return cp.checkpoint(str(self.root), **args)

    def test_commit_exact_tree_parent_and_handoff_fresh_process(self):
        result = self.run_checkpoint()
        self.assertEqual(result['outcome'], 'LOCAL_CHECKPOINT', result)
        head = self.git('rev-parse', 'HEAD').decode().strip()
        self.assertEqual(result['local_commit'], head)
        self.assertEqual(self.git('rev-parse', 'HEAD^').decode().strip(), self.head)
        self.assertEqual(self.git('status', '--porcelain'), b'')
        self.assertEqual(result['publication_status'], 'NOT_REQUESTED')
        self.assertEqual(result['safe_to_resume'], 'UNKNOWN')
        with HandoffStore(self.store_dir, project=str(self.root)) as store:
            saved = store.read()
        self.assertEqual(saved['last_known_good']['record']['evidence']['local_commit'], head)
        self.assertEqual(saved['last_known_good']['record']['project_test_status'], 'FAILED')
        env = {'PATH': '/usr/bin:/bin', 'PYTHONPATH': str(Path('src').resolve())}
        output = subprocess.check_output([sys.executable, '-B', '-m', 'cgc', 'handoff-status',
                                          '--project', str(self.root), '--store-dir', str(self.store_dir)], env=env)
        self.assertIn(head.encode(), output)
        self.assertIn(b'Reconcile Git and continue tests', output)

    def test_subset_leaves_unselected_work_and_ignored_files(self):
        (self.root / 'other.txt').write_text('unselected\n')
        (self.root / '.gitignore').write_text('ignored\n')
        (self.root / 'ignored').write_text('never collect\n')
        result = self.run_checkpoint()
        self.assertEqual(result['outcome'], 'LOCAL_CHECKPOINT', result)
        self.assertEqual(self.git('ls-tree', '--name-only', 'HEAD'), b'work.txt\n')
        self.assertEqual((self.root / 'other.txt').read_text(), 'unselected\n')
        self.assertEqual((self.root / 'ignored').read_text(), 'never collect\n')

    def test_add_delete_rename_as_explicit_paths_and_literal_pathspec(self):
        (self.root / 'work.txt').unlink()
        (self.root / 'renamed.txt').write_text('base\n')
        (self.root / ':literal.txt').write_text('literal\n')
        result = self.run_checkpoint(('work.txt', 'renamed.txt', ':literal.txt'))
        self.assertEqual(result['outcome'], 'LOCAL_CHECKPOINT', result)
        self.assertEqual(self.git('ls-tree', '--name-only', 'HEAD'), b':literal.txt\nrenamed.txt\n')

    def test_authority_and_stale_expectations_refused(self):
        before = self.tree()
        for override in ({'policy_reviewed': False}, {'policy_reviewed': 1},
                         {'expected_head': 'a' * 40}, {'branch': 'other'}):
            result = self.run_checkpoint(**override)
            self.assertEqual(result['outcome'], 'REFUSED', result)
            self.assertFalse(result['staging_attempted'])
        self.assertEqual(before, self.tree())
        record = self.record(); record['trigger'] = 'SYNTHETIC'; record['evidence_basis'] = 'SYNTHETIC'
        self.assertEqual(self.run_checkpoint(record=record)['error_code'], 'INVALID_CURRENT_RECORD')

    def test_existing_staging_preserved_byte_for_byte(self):
        self.git('add', '--', 'work.txt')
        index = (self.root / '.git/index').read_bytes()
        result = self.run_checkpoint()
        self.assertEqual(result['error_code'], 'EXISTING_STAGING')
        self.assertEqual((self.root / '.git/index').read_bytes(), index)
        self.assertEqual(self.git('rev-parse', 'HEAD').decode().strip(), self.head)

    def test_sensitive_names_content_binary_and_bounds(self):
        for name, data in [('credentials.json', b'fixture'), ('weights.gguf', b'fixture'),
                           ('content.txt', ('sk-proj-' + 'x' * 32).encode()),
                           ('content.txt', b'password = synthetic'), ('content.txt', b'\0binary'),
                           ('content.txt', b'x' * (cp.MAX_FILE_BYTES + 1))]:
            with self.subTest(name=name, size=len(data)):
                (self.root / name).write_bytes(data)
                result = self.run_checkpoint((name,))
                self.assertEqual(result['outcome'], 'REFUSED', result)
                self.assertFalse(result['staging_attempted'])
                self.assertNotIn('x' * 32, str(result))
                (self.root / name).unlink()
        self.assertEqual(self.run_checkpoint(selected={})['error_code'], 'INVALID_SELECTION')
        self.assertEqual(self.run_checkpoint(selected={'../other': None})['error_code'], 'INVALID_SELECTION')
        with patch.object(cp, 'MAX_TOTAL_BYTES', 1):
            self.assertEqual(self.run_checkpoint()['error_code'], 'CONTENT_LIMIT')

    def test_changed_digest_ignored_and_nonchanged_selection(self):
        self.assertEqual(self.run_checkpoint(selected={'work.txt': 'a' * 64})['error_code'], 'CONTENT_CHANGED')
        (self.root / '.gitignore').write_text('ignored\n')
        (self.root / 'ignored').write_text('ignored\n')
        self.assertEqual(self.run_checkpoint(('ignored',))['error_code'], 'SELECTION_NOT_CHANGED_OR_IGNORED')
        result = self.run_checkpoint(); self.assertEqual(result['outcome'], 'LOCAL_CHECKPOINT')
        self.head = result['local_commit']
        again = self.run_checkpoint()
        self.assertEqual(again['error_code'], 'SELECTION_NOT_CHANGED_OR_IGNORED')
        self.assertEqual(self.git('rev-parse', 'HEAD').decode().strip(), self.head)

    def test_hooks_attributes_and_operation_refused_without_execution(self):
        hook = self.root / '.git/hooks/pre-commit'
        hook.write_text('#!/bin/sh\ntouch must-not-run\n'); hook.chmod(0o700)
        self.assertEqual(self.run_checkpoint()['error_code'], 'HOOKS_REQUIRE_SEPARATE_POLICY')
        self.assertFalse((self.root / 'must-not-run').exists()); hook.unlink()
        attrs = self.root / '.gitattributes'; attrs.write_text('* text\n')
        self.assertEqual(self.run_checkpoint()['error_code'], 'ATTRIBUTES_UNSUPPORTED'); attrs.unlink()
        marker = self.root / '.git/MERGE_HEAD'; marker.write_text(self.head + '\n')
        self.assertEqual(self.run_checkpoint()['error_code'], 'UNSAFE_GIT_STATE')

    def test_symlink_hardlink_and_git_lock_refused(self):
        (self.root / 'link').symlink_to('work.txt')
        self.assertEqual(self.run_checkpoint(('link',))['outcome'], 'REFUSED')
        (self.root / 'link').unlink()
        os.link(self.root / 'work.txt', self.root / 'alias')
        self.assertEqual(self.run_checkpoint()['error_code'], 'INSPECTION_REFUSED')
        (self.root / 'alias').unlink()
        (self.root / '.git/index.lock').write_text('foreign lock')
        self.assertEqual(self.run_checkpoint()['error_code'], 'GIT_LOCK_PRESENT')
        self.assertEqual((self.root / '.git/index.lock').read_text(), 'foreign lock')

    def test_failed_commit_preserves_staging_and_failure_handoff(self):
        real = cp.ins._run
        def fail(args, **kwargs):
            if 'commit' in args:
                raise cp.ins.InspectionError('GIT_FAILED')
            return real(args, **kwargs)
        with patch.object(cp.ins, '_run', side_effect=fail):
            result = self.run_checkpoint()
        self.assertEqual(result['outcome'], 'PARTIAL', result)
        self.assertTrue(result['commit_attempted'])
        self.assertEqual(self.git('rev-parse', 'HEAD').decode().strip(), self.head)
        self.assertIn(b'M  work.txt', self.git('status', '--porcelain'))
        with HandoffStore(self.store_dir, project=str(self.root)) as store:
            state = store.read()
        self.assertEqual(state['latest_attempt']['status'], 'FAILED')
        self.assertIsNotNone(state['last_known_good'])
        self.assertEqual(self.run_checkpoint()['error_code'], 'EXISTING_STAGING')

    def test_failure_after_commit_reports_uncertainty_never_rolls_back(self):
        real = cp.ins._run
        def fail(args, **kwargs):
            data = real(args, **kwargs)
            if 'commit' in args:
                raise cp.ins.InspectionError('GIT_FAILED')
            return data
        with patch.object(cp.ins, '_run', side_effect=fail):
            result = self.run_checkpoint()
        self.assertEqual(result['outcome'], 'PARTIAL')
        self.assertIsNone(result['local_commit'])
        self.assertTrue(result['commit_attempted'])
        self.assertNotEqual(self.git('rev-parse', 'HEAD').decode().strip(), self.head)
        self.assertEqual(self.git('rev-parse', 'HEAD^').decode().strip(), self.head)

    def test_handoff_failure_after_verified_commit_retains_receipt(self):
        real = HandoffStore.publish
        def fail(store, record, **kwargs):
            if record['evidence']['local_commit']:
                raise OSError('synthetic private diagnostic')
            return real(store, record, **kwargs)
        with patch.object(HandoffStore, 'publish', fail):
            result = self.run_checkpoint()
        self.assertEqual(result['outcome'], 'PARTIAL')
        self.assertEqual(result['local_commit'], self.git('rev-parse', 'HEAD').decode().strip())
        self.assertFalse(result['handoff_saved'])
        self.assertNotIn('private diagnostic', str(result))

    def test_writer_exclusion_cross_process_and_release(self):
        fd = cp.ins._open_root(str(self.root))
        env = {'PATH': '/usr/bin:/bin', 'PYTHONPATH': str(Path('src').resolve())}
        code = ('import sys; from cgc import checkpoint as c; '
                'fd=c.ins._open_root(sys.argv[1]); '
                '\nwith c._writer(fd): print("acquired")')
        try:
            with cp._writer(fd):
                peer = subprocess.run([sys.executable, '-B', '-c', code, str(self.root)],
                                      env=env, capture_output=True, timeout=5)
                self.assertNotEqual(peer.returncode, 0)
                self.assertIn(b'WRITER_BUSY', peer.stderr)
        finally:
            os.close(fd)
        self.assertEqual(self.run_checkpoint()['outcome'], 'LOCAL_CHECKPOINT')

    def test_changed_content_between_handoff_and_stage_refused(self):
        real = HandoffStore.publish
        def change(store, record, **kwargs):
            state = real(store, record, **kwargs)
            (self.root / 'work.txt').write_text('newer user work\n')
            return state
        with patch.object(HandoffStore, 'publish', change):
            result = self.run_checkpoint()
        self.assertEqual(result['outcome'], 'REFUSED')
        self.assertFalse(result['staging_attempted'])
        self.assertEqual((self.root / 'work.txt').read_text(), 'newer user work\n')

    def test_hidden_index_detached_and_config_refused(self):
        self.git('update-index', '--assume-unchanged', 'work.txt')
        self.assertEqual(self.run_checkpoint()['error_code'], 'UNSAFE_GIT_STATE')
        self.git('update-index', '--no-assume-unchanged', 'work.txt')
        self.git('config', 'core.hooksPath', '/synthetic/never-execute')
        self.assertEqual(self.run_checkpoint()['error_code'], 'INSPECTION_REFUSED')

    def _crash(self, stage):
        import json
        import selectors
        import signal
        selected = {'work.txt': hashlib.sha256((self.root / 'work.txt').read_bytes()).hexdigest()}
        payload = dict(project=str(self.root), expected_head=self.head, branch='main',
                       selected=selected, policy_reviewed=True, record=self.record(),
                       store_dir=str(self.store_dir), now=STAMP)
        script = '''
import json, sys
from cgc import checkpoint as c
payload=json.loads(sys.argv[1]); stage=sys.argv[2]; real=c.ins._run

def stop():
    print('READY', flush=True)
    sys.stdin.readline()

def run(args, **kwargs):
    if stage == 'before_stage' and 'add' in args: stop()
    if stage == 'before_commit' and 'commit' in args: stop()
    value=real(args, **kwargs)
    if stage == 'after_stage' and 'add' in args: stop()
    if stage == 'after_commit' and 'commit' in args: stop()
    return value
c.ins._run=run
c.checkpoint(**payload)
'''
        peer = subprocess.Popen([sys.executable, '-B', '-c', script, json.dumps(payload), stage],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                env={'PATH': '/usr/bin:/bin', 'PYTHONPATH': str(Path('src').resolve())})
        try:
            with selectors.DefaultSelector() as selector:
                selector.register(peer.stdout, selectors.EVENT_READ)
                self.assertTrue(selector.select(10), 'No synchronized stage reached')
                self.assertEqual(peer.stdout.readline(), b'READY\n')
            peer.send_signal(signal.SIGKILL); peer.wait(timeout=5)
        finally:
            if peer.poll() is None: peer.kill(); peer.wait(timeout=5)
            peer.stdin.close(); peer.stdout.close(); peer.stderr.close()
        head = self.git('rev-parse', 'HEAD').decode().strip()
        self.assertEqual(head == self.head, stage != 'after_commit')
        self.assertEqual((self.root / 'work.txt').read_text(), 'reviewed change\n')
        with HandoffStore(self.store_dir, project=str(self.root)) as store:
            state = store.read()
        self.assertEqual(state['last_known_good']['record']['phase'], 'CHECKPOINTING')
        self.assertIsNone(state['last_known_good']['record']['evidence']['local_commit'])
        fd = cp.ins._open_root(str(self.root))
        try:
            with cp._writer(fd): pass
        finally: os.close(fd)
        if stage in ('after_stage', 'before_commit'):
            self.assertEqual(self.run_checkpoint()['error_code'], 'EXISTING_STAGING')
        elif stage == 'before_stage':
            self.assertEqual(self.run_checkpoint()['outcome'], 'LOCAL_CHECKPOINT')
        else:
            self.assertEqual(self.git('rev-parse', 'HEAD^').decode().strip(), self.head)
            self.assertEqual(self.run_checkpoint()['error_code'], 'TARGET_CHANGED')

    def test_sigkill_before_stage(self): self._crash('before_stage')
    def test_sigkill_after_stage(self): self._crash('after_stage')
    def test_sigkill_before_commit(self): self._crash('before_commit')
    def test_sigkill_after_commit(self): self._crash('after_commit')

    def test_index_tampering_after_stage_never_committed(self):
        real = cp.ins._run
        def change(args, **kwargs):
            value = real(args, **kwargs)
            if 'add' in args:
                (self.root / 'unselected.txt').write_text('not approved\n')
                self.git('add', '--', 'unselected.txt')
            return value
        with patch.object(cp.ins, '_run', side_effect=change):
            result = self.run_checkpoint()
        self.assertEqual(result['error_code'], 'STAGING_MISMATCH')
        self.assertFalse(result['commit_attempted'])
        self.assertEqual(self.git('rev-parse', 'HEAD').decode().strip(), self.head)
        self.assertIn(b'unselected.txt', self.git('diff', '--cached', '--name-only'))

    def test_intent_to_add_is_existing_staging(self):
        (self.root / 'intent.txt').write_text('not selected\n')
        self.git('add', '-N', '--', 'intent.txt')
        index = (self.root / '.git/index').read_bytes()
        result = self.run_checkpoint()
        self.assertEqual(result['error_code'], 'EXISTING_STAGING')
        self.assertEqual((self.root / '.git/index').read_bytes(), index)

    def test_real_git_identity_failure_is_partial(self):
        self.git('config', 'user.name', '')
        self.git('config', 'user.email', '')
        result = self.run_checkpoint()
        self.assertEqual(result['outcome'], 'PARTIAL')
        self.assertEqual(result['error_code'], 'GIT_FAILED')
        self.assertEqual(self.git('rev-parse', 'HEAD').decode().strip(), self.head)
        self.assertIn(b'M  work.txt', self.git('status', '--porcelain'))

    def test_corrupt_store_blocks_before_staging(self):
        self.store_dir.mkdir(mode=0o700)
        state = self.store_dir / 'handoff.json'; state.write_text('{'); state.chmod(0o600)
        result = self.run_checkpoint()
        self.assertEqual(result['outcome'], 'REFUSED')
        self.assertFalse(result['staging_attempted'])
        self.assertEqual(state.read_text(), '{')
        self.assertEqual(self.git('rev-parse', 'HEAD').decode().strip(), self.head)
