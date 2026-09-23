"""Explicit local bare-remote publication; no credentials or network fixtures."""
import copy
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from cgc import publication as pub
from cgc import checkpoint as cp
from cgc.handoff import HandoffStore
from cgc.preservation import new_attempt, advance
import test_checkpoint as fixtures

STAMP = '2026-09-22T00:00:00Z'


class PublicationTests(unittest.TestCase):
    git = fixtures.CheckpointTests.git
    tree = fixtures.CheckpointTests.tree

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='cgc-publication-', dir='/tmp')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'project'; self.root.mkdir(mode=0o700)
        self.remote = Path(self.tmp.name) / 'remote.git'
        self.store_dir = Path(self.tmp.name) / 'handoff'
        self.git('init', '-q', '-b', 'main')
        self.git('config', 'user.name', 'Synthetic')
        self.git('config', 'user.email', 'synthetic@example.invalid')
        (self.root / 'work.txt').write_text('base\n')
        self.git('add', '--', 'work.txt'); self.git('commit', '-qm', 'base')
        self.base = self.git('rev-parse', 'HEAD').decode().strip()
        self.git('init', '--bare', '-q', str(self.remote))
        self.git('remote', 'add', 'origin', str(self.remote))
        self.git('push', '-q', 'origin', 'HEAD:refs/heads/main')
        self.git('fetch', '-q', 'origin')
        (self.root / 'work.txt').write_text('approved second revision\n')
        record = new_attempt(str(self.root), now=STAMP, mission='Synthetic checkpoint integration',
                             requested_level='LOCAL_CHECKPOINT', next_exact_action='Publish approved checkpoint')
        record = advance(record, 'DOCUMENTING', now=STAMP,
                         notes={'known_failures': ['One synthetic test failure'],
                                'tests_run': ['Synthetic test command'], 'test_results': ['One failure'],
                                'complete': ['Local implementation'], 'partial': ['V3'],
                                'not_started': ['Safe resume']}, test_status='FAILED')
        result = cp.checkpoint(str(self.root), expected_head=self.base, branch='main',
                               selected={'work.txt': hashlib.sha256((self.root / 'work.txt').read_bytes()).hexdigest()},
                               policy_reviewed=True, record=record, store_dir=self.store_dir, now=STAMP)
        self.assertEqual(result['outcome'], 'LOCAL_CHECKPOINT', result)
        self.head = result['local_commit']
        self.identity = pub.ins.inspect_project(str(self.root), now=STAMP)['snapshot']['repository_identity']
        st = self.remote.stat(); self.remote_identity = {'device': st.st_dev, 'inode': st.st_ino}

    def bare(self, *args):
        return self.git('--git-dir=' + str(self.remote), *args)

    def tip(self):
        return self.bare('rev-parse', 'refs/heads/main').decode().strip()

    def record(self):
        record = new_attempt(str(self.root), now=STAMP, mission='Synthetic explicit publication',
                             requested_level='REMOTE_VERIFIED', next_exact_action='Reconcile current Git and tests')
        return advance(record, 'DOCUMENTING', now=STAMP,
                       notes={'known_failures': ['One synthetic test failure'],
                              'tests_run': ['Synthetic test command'], 'test_results': ['One failure'],
                              'complete': ['Local checkpoint'], 'partial': ['V3'],
                              'not_started': ['Safe resume']}, test_status='FAILED')

    def args(self):
        return dict(project=str(self.root), source_identity=self.identity, expected_head=self.head,
                    branch='main', remote_name='origin', remote_path=str(self.remote),
                    remote_identity=self.remote_identity, expected_remote=self.base,
                    publication_reviewed=True, history_reviewed=True, record=self.record(),
                    store_dir=str(self.store_dir), now=STAMP)

    def publish(self, **overrides):
        args = self.args(); args.update(overrides)
        return pub.publish(**args)

    def state(self):
        with HandoffStore(self.store_dir, project=str(self.root)) as store: return store.read()

    def test_checkpoint_publish_independent_refs_and_continuity(self):
        index = (self.root / '.git/index').read_bytes()
        result = self.publish()
        self.assertEqual(result['publication_status'], 'VERIFIED', result)
        self.assertEqual(result['preservation_outcome'], 'REMOTE_VERIFIED')
        self.assertTrue(result['publication_attempted']); self.assertTrue(result['ref_update_succeeded'])
        self.assertTrue(result['handoff_saved'])
        for key in ('local_commit', 'remote_commit', 'tracking_commit'):
            self.assertEqual(result[key], self.head)
        self.assertEqual(self.tip(), self.head)
        self.assertEqual(self.git('rev-parse', 'origin/main').decode().strip(), self.head)
        self.assertEqual((self.root / '.git/index').read_bytes(), index)
        self.assertEqual(self.git('status', '--porcelain'), b'')
        saved = self.state()
        self.assertEqual(saved['safe_to_resume'], 'UNKNOWN')
        record = saved['last_known_good']['record']
        self.assertEqual(record['publication_status'], 'VERIFIED')
        self.assertEqual(record['phase'], 'PARTIAL')
        self.assertEqual(record['project_test_status'], 'FAILED')
        self.assertEqual(record['notes']['next_exact_action'], 'Reconcile current Git and tests')
        output = subprocess.check_output([sys.executable, '-B', '-m', 'cgc', 'handoff-status',
                                          '--project', str(self.root), '--store-dir', str(self.store_dir), '--json'],
                                         env={'PATH': '/usr/bin:/bin', 'PYTHONPATH': str(Path('src').resolve())})
        self.assertIn(self.head.encode(), output)
        self.assertIn(b'VERIFIED', output)

    def test_already_equal_verifies_without_push(self):
        self.git('push', '-q', 'origin', self.head + ':refs/heads/main')
        result = self.publish(expected_remote=self.head)
        self.assertEqual(result['publication_status'], 'VERIFIED', result)
        self.assertFalse(result['publication_attempted'])
        self.assertFalse(result['ref_update_succeeded'])

    def test_current_authority_and_history_review_required(self):
        before = self.tree(); remote = self.tip()
        for change in ({'publication_reviewed': False}, {'history_reviewed': False},
                       {'publication_reviewed': 1}):
            result = self.publish(**change)
            self.assertEqual(result['error_code'], 'CURRENT_PUBLICATION_AUTHORITY_REQUIRED')
        self.assertEqual(before, self.tree()); self.assertEqual(self.tip(), remote)

    def test_wrong_source_head_branch_or_remote_refuses(self):
        for change in ({'expected_head': self.base}, {'branch': 'other'},
                       {'source_identity': dict(self.identity, inode=self.identity['inode']+1)},
                       {'remote_identity': dict(self.remote_identity, inode=self.remote_identity['inode']+1)},
                       {'remote_name': 'missing'}, {'remote_path': str(self.remote) + '-missing'}):
            result = self.publish(**change)
            self.assertEqual(result['publication_status'], 'REFUSED', result)
            self.assertFalse(result['publication_attempted'])
            self.assertEqual(self.tip(), self.base)

    def test_dirty_staged_operation_and_detached_source_refused(self):
        (self.root / 'work.txt').write_text('newer work\n')
        self.assertEqual(self.publish()['error_code'], 'DIRTY_SOURCE')
        self.git('add', '--', 'work.txt')
        index = (self.root / '.git/index').read_bytes()
        self.assertEqual(self.publish()['error_code'], 'DIRTY_SOURCE')
        self.assertEqual(index, (self.root / '.git/index').read_bytes())
        (self.root / '.git/MERGE_HEAD').write_text(self.base + '\n')
        self.assertEqual(self.publish()['error_code'], 'UNSAFE_GIT_STATE')
        (self.root / '.git/MERGE_HEAD').unlink()
        self.git('checkout', '--detach', '-q')
        self.assertEqual(self.publish()['publication_status'], 'REFUSED')
        self.assertEqual(self.tip(), self.base)

    def test_remote_url_protocol_alias_permissions_and_hooks_refused(self):
        link = Path(self.tmp.name) / 'alias'; link.symlink_to(self.remote)
        self.git('remote', 'set-url', 'origin', str(link))
        self.assertEqual(self.publish(remote_path=str(link))['publication_status'], 'REFUSED')
        self.git('remote', 'set-url', 'origin', str(self.remote))
        for url in ['https://example.invalid/repo', 'file://' + str(self.remote), 'ext::never-run']:
            self.assertEqual(self.publish(remote_path=url)['publication_status'], 'REFUSED')
        hook = self.remote / 'hooks/pre-receive'; hook.write_text('#!/bin/sh\nexit 1\n'); hook.chmod(0o700)
        self.assertEqual(self.publish()['error_code'], 'REMOTE_HOOKS_UNSUPPORTED'); hook.unlink()
        self.remote.chmod(0o777)
        self.assertEqual(self.publish()['publication_status'], 'REFUSED'); self.remote.chmod(0o700)
        self.assertEqual(self.tip(), self.base)

    def test_wrong_pushurl_and_unsafe_remote_config_refused(self):
        self.git('config', 'remote.origin.pushurl', '/synthetic/never-send')
        self.assertEqual(self.publish()['error_code'], 'REMOTE_CONFIG_MISMATCH')
        self.git('config', '--unset', 'remote.origin.pushurl')
        self.bare('config', 'include.path', '/synthetic/never-read')
        self.assertEqual(self.publish()['error_code'], 'REMOTE_CONFIG_UNSUPPORTED')
        self.assertEqual(self.tip(), self.base)

    def test_remote_ahead_diverged_or_unexpected_tip_refused(self):
        # A synthetic commit with the approved HEAD as parent exists locally but
        # makes remote publication a rewind. It is created in this disposable fixture only.
        tree = self.git('rev-parse', 'HEAD^{tree}').decode().strip()
        ahead = self.git('commit-tree', tree, '-p', self.head, '-m', 'remote ahead').decode().strip()
        self.git('push', '-q', 'origin', ahead + ':refs/heads/main')
        self.assertEqual(self.publish()['error_code'], 'REMOTE_MOVED')
        self.assertEqual(self.publish(expected_remote=ahead)['error_code'], 'NON_FORWARD_OR_UNKNOWN_ANCESTRY')
        self.assertEqual(self.tip(), ahead)

    def test_missing_remote_branch_never_created(self):
        self.bare('update-ref', '-d', 'refs/heads/main')
        result = self.publish()
        self.assertEqual(result['error_code'], 'REMOTE_REF_MISSING_OR_AMBIGUOUS')
        self.assertFalse(result['publication_attempted'])
        self.assertEqual(self.bare('for-each-ref', 'refs/heads/main'), b'')

    def test_ref_update_failure_retains_previous_handoff_and_local_commit(self):
        previous = self.state()['last_known_good']
        real = pub._git
        def fail(fd, deadline, *args):
            if args[0] == 'update-ref' and args[2] == 'refs/heads/main': raise pub.ins.InspectionError('GIT_FAILED')
            return real(fd, deadline, *args)
        with patch.object(pub, '_git', side_effect=fail): result = self.publish()
        self.assertEqual(result['publication_status'], 'PUBLICATION_UNCERTAIN')
        self.assertEqual(result['preservation_outcome'], 'LOCAL_CHECKPOINT_ONLY')
        self.assertEqual(self.tip(), self.base)
        saved = self.state()
        self.assertEqual(saved['latest_attempt']['status'], 'FAILED')
        self.assertEqual(saved['previous_known_good'], previous)
        self.assertEqual(saved['last_known_good']['record']['evidence']['local_commit'], self.head)

    def test_accept_then_transport_error_is_uncertain(self):
        real = pub._git
        def fail(fd, deadline, *args):
            value = real(fd, deadline, *args)
            if args[0] == 'update-ref' and args[2] == 'refs/heads/main': raise pub.ins.InspectionError('GIT_FAILED')
            return value
        with patch.object(pub, '_git', side_effect=fail): result = self.publish()
        self.assertEqual(result['publication_status'], 'PUBLICATION_UNCERTAIN')
        self.assertEqual(self.tip(), self.head)
        self.assertIsNone(result['remote_commit'])

    def test_successful_publication_failed_verification_is_unverified(self):
        real = pub._git
        def fail(fd, deadline, *args):
            if args[0] == 'fetch' and os.fstat(fd).st_ino == self.identity['inode']: raise pub.ins.InspectionError('TIMEOUT')
            return real(fd, deadline, *args)
        with patch.object(pub, '_git', side_effect=fail): result = self.publish()
        self.assertEqual(result['publication_status'], 'PUBLISHED_UNVERIFIED')
        self.assertTrue(result['ref_update_succeeded'])
        self.assertEqual(self.tip(), self.head)
        self.assertFalse(result['handoff_saved'])

    def test_verification_disagreement_never_verified(self):
        real = pub._live; calls = 0
        def mismatch(*args):
            nonlocal calls
            calls += 1
            return self.base if calls == 3 else real(*args)
        with patch.object(pub, '_live', side_effect=mismatch): result = self.publish()
        self.assertEqual(result['error_code'], 'VERIFICATION_MISMATCH')
        self.assertEqual(result['publication_status'], 'PUBLISHED_UNVERIFIED')

    def test_remote_moves_after_handoff_refused(self):
        real = HandoffStore.publish
        def move(store, record, **kwargs):
            value = real(store, record, **kwargs)
            self.git('push', '-q', 'origin', self.head + ':refs/heads/main')
            return value
        with patch.object(HandoffStore, 'publish', move): result = self.publish()
        self.assertEqual(result['error_code'], 'REMOTE_OR_TRACKING_MOVED')
        self.assertFalse(result['publication_attempted'])

    def test_failed_final_handoff_does_not_downgrade_verified_remote(self):
        real = HandoffStore.publish
        def fail(store, record, **kwargs):
            if record['publication_status'] == 'VERIFIED': raise OSError('synthetic private diagnostic')
            return real(store, record, **kwargs)
        with patch.object(HandoffStore, 'publish', fail): result = self.publish()
        self.assertEqual(result['publication_status'], 'VERIFIED', result)
        self.assertEqual(result['preservation_outcome'], 'PARTIAL')
        self.assertFalse(result['handoff_saved'])
        self.assertEqual(self.tip(), self.head)
        self.assertNotIn('private diagnostic', str(result))

    def test_real_non_fast_forward_race_rejected_without_repair(self):
        real = pub._git
        tree = self.git('rev-parse', 'HEAD^{tree}').decode().strip()
        other = self.git('commit-tree', tree, '-p', self.base, '-m', 'divergent remote work').decode().strip()
        def move(fd, deadline, *args):
            if args[0] == 'update-ref' and args[2] == 'refs/heads/main':
                self.git('push', '-q', 'origin', other + ':refs/heads/main')
            return real(fd, deadline, *args)
        with patch.object(pub, '_git', side_effect=move): result = self.publish()
        self.assertEqual(result['publication_status'], 'PUBLICATION_UNCERTAIN')
        self.assertEqual(self.tip(), other)
        self.assertEqual(self.git('rev-parse', 'HEAD').decode().strip(), self.head)

    def test_config_changed_after_publication_blocks_fetch(self):
        real = pub._git
        commands = []
        def change(fd, deadline, *args):
            commands.append((args[0], os.fstat(fd).st_ino))
            data = real(fd, deadline, *args)
            if args[0] == 'update-ref' and args[2] == 'refs/heads/main':
                self.git('config', 'include.path', '/synthetic/never-read')
            return data
        with patch.object(pub, '_git', side_effect=change): result = self.publish()
        self.assertEqual(result['publication_status'], 'PUBLISHED_UNVERIFIED')
        self.assertNotIn(('fetch', self.identity['inode']), commands)
        self.assertEqual(self.tip(), self.head)

    def test_corrupt_handoff_blocks_publication_without_overwrite(self):
        path = self.store_dir / 'handoff.json'; path.write_text('{')
        result = self.publish()
        self.assertEqual(result['publication_status'], 'REFUSED')
        self.assertFalse(result['publication_attempted'])
        self.assertEqual(path.read_text(), '{')
        self.assertEqual(self.tip(), self.base)

    def test_source_hook_tracking_alias_and_path_overlap_refused(self):
        hook = self.root / '.git/hooks/pre-push'; hook.write_text('#!/bin/sh\nexit 1\n'); hook.chmod(0o700)
        self.assertEqual(self.publish()['error_code'], 'HOOKS_REQUIRE_SEPARATE_POLICY'); hook.unlink()
        self.assertEqual(self.publish(store_dir=str(self.remote / 'handoff'))['error_code'], 'OVERLAPPING_PATHS')
        self.git('symbolic-ref', 'refs/remotes/origin/main', 'refs/heads/main')
        self.assertEqual(self.publish()['publication_status'], 'REFUSED')
        self.assertEqual(self.tip(), self.base)

    def _crash(self, stage):
        import json
        import selectors
        import signal
        script = '''
import json,sys,os
from cgc import publication as p
args=json.loads(sys.argv[1]); stage=sys.argv[2]; real=p._git

def stop():
    print('READY', flush=True)
    sys.stdin.readline()

def run(fd, deadline, *command):
    if stage == 'before_push' and command[0] == 'update-ref' and command[2] == 'refs/heads/main': stop()
    if stage == 'before_verify' and command[0] == 'fetch' and os.fstat(fd).st_ino == args['source_identity']['inode']: stop()
    data=real(fd,deadline,*command)
    if stage == 'after_accept' and command[0] == 'update-ref' and command[2] == 'refs/heads/main': stop()
    return data
p._git=run
p.publish(**args)
'''
        prior = self.state()['last_known_good']
        peer = subprocess.Popen([sys.executable, '-B', '-c', script, json.dumps(self.args()), stage],
                                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                env={'PATH': '/usr/bin:/bin', 'PYTHONPATH': str(Path('src').resolve())})
        try:
            with selectors.DefaultSelector() as selector:
                selector.register(peer.stdout, selectors.EVENT_READ)
                self.assertTrue(selector.select(10), 'Stage not reached')
                self.assertEqual(peer.stdout.readline(), b'READY\n')
            peer.send_signal(signal.SIGKILL); peer.wait(timeout=5)
        finally:
            if peer.poll() is None: peer.kill(); peer.wait(timeout=5)
            peer.stdin.close(); peer.stdout.close(); peer.stderr.close()
        self.assertEqual(self.tip(), self.base if stage == 'before_push' else self.head)
        saved = self.state()
        self.assertEqual(saved['previous_known_good'], prior)
        self.assertEqual(saved['last_known_good']['record']['phase'], 'PUBLISHING')
        self.assertEqual(saved['safe_to_resume'], 'UNKNOWN')
        self.assertIsNone(saved['last_known_good']['record']['evidence']['remote_commit'])
        fd = cp.ins._open_root(str(self.root))
        try:
            with cp._writer(fd): pass
        finally: os.close(fd)
        with HandoffStore(self.store_dir, project=str(self.root)) as store, store.writer(): pass

    def test_sigkill_before_publication(self): self._crash('before_push')
    def test_sigkill_after_remote_acceptance(self): self._crash('after_accept')
    def test_sigkill_before_independent_verification(self): self._crash('before_verify')

    def test_checkpoint_lock_excludes_publication_and_releases(self):
        fd = cp.ins._open_root(str(self.root))
        try:
            with cp._writer(fd):
                result = self.publish()
                self.assertEqual(result['error_code'], 'WRITER_BUSY')
                self.assertFalse(result['publication_attempted'])
        finally: os.close(fd)
        self.assertEqual(self.publish()['publication_status'], 'VERIFIED')

    def test_equal_remote_with_stale_tracking_reconciles_forward(self):
        # Publish by path so the named tracking ref is deliberately untouched.
        self.git('push', '-q', str(self.remote), self.head + ':refs/heads/main')
        self.assertEqual(self.git('rev-parse', 'origin/main').decode().strip(), self.base)
        result = self.publish(expected_remote=self.head)
        self.assertEqual(result['publication_status'], 'VERIFIED', result)
        self.assertFalse(result['publication_attempted'])
        self.assertEqual(self.git('rev-parse', 'origin/main').decode().strip(), self.head)

    def test_branch_deleted_after_precheck_is_not_recreated(self):
        real = pub._git
        def remove(fd, deadline, *args):
            if args[0] == 'update-ref' and args[2] == 'refs/heads/main':
                self.bare('update-ref', '-d', 'refs/heads/main')
            return real(fd, deadline, *args)
        with patch.object(pub, '_git', side_effect=remove): result = self.publish()
        self.assertEqual(result['publication_status'], 'PUBLICATION_UNCERTAIN')
        self.assertEqual(self.bare('for-each-ref', 'refs/heads/main'), b'')
        self.assertEqual(self.git('rev-parse', 'HEAD').decode().strip(), self.head)
