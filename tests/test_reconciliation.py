"""A-R reconciliation acceptance: disposable Git, no replay of crash experiments."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from cgc import reconciliation as rc
from cgc import inspection as ins
from cgc.handoff import HandoffStore
from cgc.preservation import advance, new_attempt
import test_checkpoint as fixtures
import test_publication as publication

STAMP = fixtures.STAMP


class ReconciliationTests(unittest.TestCase):
    setUp = fixtures.CheckpointTests.setUp
    git = fixtures.CheckpointTests.git
    record = fixtures.CheckpointTests.record

    def pending(self, tests='UNKNOWN'):
        observation = ins.inspect_project(str(self.root), now=STAMP)
        record = new_attempt(str(self.root), now=STAMP, mission='Reconciliation fixture',
                             next_exact_action='Read current state', requested_level='LOCAL_CHECKPOINT')
        notes = dict(files_changed=['work.txt'])
        if tests != 'UNKNOWN': notes.update(tests_run=['inert test'], test_results=['reported pass'])
        record = advance(record, 'DOCUMENTING', now=STAMP, notes=notes, test_status=tests)
        record = advance(record, 'CHECKPOINTING', now=STAMP,
                         evidence={'inspection_digest': observation['inspection_digest']})
        with HandoffStore(self.store_dir, project=str(self.root), create=True) as store, store.writer():
            store.publish(record, now=STAMP, inspection=observation)

    def snapshot(self):
        return {str(p.relative_to(self.tmp.name)): (p.read_bytes(), p.stat().st_mode, p.stat().st_size, p.stat().st_mtime_ns)
                for p in Path(self.tmp.name).rglob('*') if p.is_file()}

    def run_rc(self, **kwargs):
        before = self.snapshot()
        commands = []
        real = ins._run
        children = set()
        real_popen, real_killpg = subprocess.Popen, os.killpg
        def spawned(*args, **kw):
            child = real_popen(*args, **kw); children.add(child.pid); return child
        def killed(pid, sig):
            self.assertIn(pid, children, 'cleanup must not kill historical processes')
            return real_killpg(pid, sig)
        def observed(args, **kw):
            commands.append(args)
            return real(args, **kw)
        with patch.object(ins, '_run', side_effect=observed), \
             patch.object(subprocess, 'Popen', side_effect=spawned), \
             patch.object(os, 'killpg', side_effect=killed), \
             patch('cgc.checkpoint._writer', side_effect=AssertionError('writer')), \
             patch.object(HandoffStore, 'writer', side_effect=AssertionError('store writer')), \
             patch('cgc.publication.publish', side_effect=AssertionError('publish')):
            result = rc.reconcile(str(self.root), store_dir=str(self.store_dir), now=STAMP, **kwargs)
        self.assertEqual(self.snapshot(), before)
        self.assertLessEqual(len(commands), 48)
        for command in commands:
            self.assertFalse(set(command) & {'add','commit','reset','restore','checkout','clean','fetch','push','update-ref','write-tree','gc','prune'})
        self.assertEqual(result['safe_to_resume'], 'UNKNOWN')
        self.assertIs(result['mutation_allowed'], False)
        self.assertIs(result['automatic_mutation_authorized'], False)
        self.assertEqual(rc.validate_result(result), result)
        self.assertEqual(json.loads(rc.render_json(result)), result)
        self.assertIn(rc.canonical(result['next_exact_action']), rc.render_human(result))
        return result

    def reasons(self, result): return {i['reason'] for i in result['issues']}

    def test_a_old_index_lock(self):
        self.pending()
        old = (self.root / '.git/index').read_bytes()
        (self.root / '.git/index.lock').write_bytes(old)
        r = self.run_rc()
        self.assertEqual(r['collection_outcome'], 'OBSERVED')
        self.assertIn('MUTATION_ARTIFACT', self.reasons(r))
        self.assertEqual(r['evidence']['local_first']['head'], self.head)
        self.assertEqual(r['next_exact_action'], rc.ACTIONS['MUTATION'])

    def test_b_staged(self):
        self.pending(); self.git('add', '--', 'work.txt')
        r = self.run_rc()
        self.assertEqual(r['evidence']['local_first']['changes'][0]['index'], 'M')
        self.assertIsNone(r['evidence']['handoff']['last_known_good']['receipts']['local_commit'])

    def test_c_surviving_commit_structure(self):
        self.pending(); self.git('add', '--', 'work.txt'); self.git('commit', '-qm', 'surviving')
        tree = self.git('rev-parse', 'HEAD^{tree}').decode().strip()
        r = self.run_rc(expected_commit={'parent': self.head, 'tree': tree})
        self.assertEqual(r['checkpoint_relation'], 'MATCHES_SUPPLIED_EXPECTATION')
        self.assertIsNone(r['evidence']['handoff']['last_known_good']['receipts']['local_commit'])

    def test_d_changed_head(self):
        self.pending(); self.git('commit', '--allow-empty', '-qm', 'different')
        r = self.run_rc()
        self.assertIn('HEAD_DIFFERS_FROM_HISTORY', self.reasons(r))
        self.assertEqual(r['checkpoint_relation'], 'UNKNOWN')

    def test_h_legacy_pass_unchanged(self):
        self.pending('PASSED')
        r = self.run_rc()
        self.assertEqual(r['historical_test_result'], 'PASSED')
        self.assertEqual(r['test_applicability'], 'UNKNOWN')

    def test_i_reported_test_head_changed(self):
        self.pending('PASSED'); self.git('commit', '--allow-empty', '-qm', 'different')
        r = self.run_rc(tests=dict(result='PASSED', commands=['inert'], results=['pass'], bound_head=self.head))
        self.assertEqual(r['test_applicability'], 'STALE')
        self.assertEqual(r['historical_test_result'], 'PASSED')

    def test_j_missing_review(self):
        self.pending()
        r = self.run_rc()
        self.assertEqual(r['review_applicability'], 'UNKNOWN')
        self.assertIn('HISTORICAL_DIGESTS_MISSING', self.reasons(r))

    def test_k_matching_review_no_authority(self):
        self.pending()
        digest = hashlib.sha256((self.root / 'work.txt').read_bytes()).hexdigest()
        r = self.run_rc(review={'work.txt': digest}, requested_operation='CHECKPOINT')
        self.assertEqual(r['review_applicability'], 'CURRENT')
        self.assertEqual(r['authority_state'], 'NO_MUTATION_AUTHORITY')

    def test_review_mismatch(self):
        self.pending()
        r = self.run_rc(review={'work.txt': '0'*64})
        self.assertEqual(r['review_applicability'], 'CONTRADICTED')
        self.assertIn('CONTENT_CHANGED', self.reasons(r))

    def test_l_no_action(self):
        record = new_attempt(str(self.root), now=STAMP, mission='Observe', next_exact_action='Read')
        with HandoffStore(self.store_dir, project=str(self.root), create=True) as store, store.writer():
            store.publish(record, now=STAMP)
        r = self.run_rc()
        self.assertEqual(r['next_exact_action'], rc.ACTIONS['NONE'])
        self.assertEqual(r['remote_observation'], 'NOT_QUERIED')

    def test_m_timeout_history_retained(self):
        self.pending()
        with patch.object(ins, '_run', side_effect=ins.InspectionError('TIMEOUT')):
            r = self.run_rc()
        self.assertEqual(r['collection_outcome'], 'REFUSED')
        self.assertIsNotNone(r['evidence']['handoff']['last_known_good'])
        self.assertIsNone(r['evidence']['local_first'])

    def test_n_absent_store_not_created(self):
        r = self.run_rc()
        self.assertFalse(self.store_dir.exists())
        self.assertFalse((self.root / '.git/cgc-checkpoint.lock').exists())
        self.assertIn('UNSAFE_CACHE', self.reasons(r))

    def test_n_unsupported_handoff_untouched(self):
        self.pending()
        target = self.store_dir / 'handoff.json'
        value = json.loads(target.read_text()); value['schema_version'] = 'future'
        target.write_text(json.dumps(value))
        r = self.run_rc()
        self.assertIn('UNSUPPORTED_HANDOFF_SCHEMA', self.reasons(r))

    def test_o_repeated_index_change(self):
        self.pending()
        real = rc._local
        calls = 0
        def changed(*args):
            nonlocal calls
            calls += 1
            value = real(*args)
            if calls == 2: value['index_digest'] = 'f'*64
            return value
        # Inject inconsistent second evidence, rejected by strict projection validation.
        with patch.object(rc, '_local', side_effect=changed), self.assertRaises(rc.ReconciliationError):
            self.run_rc()

    def test_o_real_race(self):
        self.pending()
        real = rc._local
        calls = 0
        def changed(*args):
            nonlocal calls
            value = real(*args); calls += 1
            if calls == 1: (self.root / 'work.txt').write_text('external edit\n')
            return value
        with patch.object(rc, '_local', side_effect=changed):
            r = rc.reconcile(str(self.root), store_dir=str(self.store_dir), now=STAMP)
        self.assertEqual(r['collection_outcome'], 'REFUSED')
        self.assertIn('TARGET_CHANGED', self.reasons(r))
        self.assertEqual((self.root / 'work.txt').read_text(), 'external edit\n')

    def test_o_identity_contradiction_pure(self):
        self.pending()
        b = rc.collect(str(self.root), store_dir=str(self.store_dir), now=STAMP)
        b['handoff']['last_known_good']['base_identity']['inode'] += 1
        r = rc.classify(b)
        self.assertEqual(r['collection_outcome'], 'REFUSED')
        self.assertIn('PROJECT_MISMATCH', self.reasons(r))

    def test_q_inner_yes_does_not_promote(self):
        observation = ins.inspect_project(str(self.root), now=STAMP)
        record = new_attempt(str(self.root), now=STAMP, mission='Attributed receipt', next_exact_action='Read')
        record = advance(record, 'DOCUMENTING', now=STAMP)
        record = advance(record, 'VERIFYING', now=STAMP, evidence={
            'inspection_digest': observation['inspection_digest'], 'handoff_digest': '1'*64, 'resume_digest': '2'*64})
        record = advance(record, 'PRESERVED', now=STAMP)
        self.assertEqual(record['safe_to_resume'], 'YES')
        with HandoffStore(self.store_dir, project=str(self.root), create=True) as store, store.writer():
            store.publish(record, now=STAMP, inspection=observation)
        r = self.run_rc()
        self.assertEqual(r['evidence']['handoff']['last_known_good']['reported_safe_to_resume'], 'YES')
        self.assertEqual(r['safe_to_resume'], 'UNKNOWN')

    def test_r_unsafe_config(self):
        self.pending(); self.git('config', 'core.fsmonitor', 'forbidden')
        r = self.run_rc()
        self.assertEqual(r['collection_outcome'], 'REFUSED')

    def test_pure_determinism_strict_validator_and_no_io(self):
        self.pending()
        b = rc.collect(str(self.root), store_dir=str(self.store_dir), now=STAMP)
        with patch('builtins.open', side_effect=AssertionError('IO')), patch.object(ins, '_run', side_effect=AssertionError('Git')):
            r = rc.classify(b)
            self.assertEqual(rc.render_json(r), rc.render_json(rc.classify(copy.deepcopy(b))))
        for key, value in [('extra', True), ('schema_version', 'future'), ('safe_to_resume', 'YES'), ('mutation_allowed', True), ('review_applicability', 'INVALID')]:
            bad = copy.deepcopy(r); bad[key] = value
            with self.assertRaises(rc.ReconciliationError): rc.validate_result(bad)
        for mutate in (lambda x: x.update(project='/tmp/../bad'),
                       lambda x: x['local_first'].update(index_digest='bad'),
                       lambda x: x['handoff']['last_known_good'].update(paths=['x']*65),
                       lambda x: x.update(authority_description='x'*2049)):
            bad = copy.deepcopy(b); mutate(bad)
            with self.assertRaises(rc.ReconciliationError): rc.classify(bad)

    def test_shared_budget_refuses_before_spawn_and_restores(self):
        with ins.observation_budget(commands=1):
            ins._run(['rev-parse','--git-dir'], cwd=str(self.root), deadline=10**12)
            with patch.object(subprocess, 'Popen', side_effect=AssertionError('spawn')):
                with self.assertRaisesRegex(ins.InspectionError, 'RESOURCE_LIMIT'):
                    ins._run(['rev-parse','HEAD'], cwd=str(self.root), deadline=10**12)
        with ins.observation_budget(), patch.object(subprocess, 'Popen', side_effect=AssertionError('spawn')):
            with self.assertRaises(ins.InspectionError):
                ins._run(['fetch'], cwd=str(self.root), deadline=10**12)
        self.assertIsNone(ins._OBSERVATION_BUDGET.get())

    def test_corrupt_handoff_and_missing_project(self):
        self.pending()
        (self.store_dir / 'handoff.json').write_text('{invalid')
        r = self.run_rc()
        self.assertIn('CORRUPT_HANDOFF', self.reasons(r))
        missing = str(self.root) + '-absent'
        r = rc.reconcile(missing, store_dir=str(self.store_dir), now=STAMP)
        self.assertEqual(r['collection_outcome'], 'REFUSED')
        self.assertFalse(Path(missing).exists())

    def test_symlink_and_hardlink_refusal(self):
        self.pending()
        alias = Path(self.tmp.name) / 'alias'
        alias.symlink_to(self.root, target_is_directory=True)
        r = rc.reconcile(str(alias), store_dir=str(self.store_dir), now=STAMP)
        self.assertEqual(r['collection_outcome'], 'REFUSED')
        os.link(self.root / 'work.txt', self.root / 'hardlink.txt')
        r = self.run_rc()
        self.assertEqual(r['collection_outcome'], 'REFUSED')

    def test_handoff_race_preserves_both_observations(self):
        self.pending()
        real = rc._handoff
        calls = 0
        def changed(*args):
            nonlocal calls
            value = real(*args); calls += 1
            if calls == 2: value['digest'] = 'e'*64
            return value
        with patch.object(rc, '_handoff', side_effect=changed): r = self.run_rc()
        self.assertEqual(r['collection_outcome'], 'REFUSED')
        self.assertIn('TARGET_CHANGED', self.reasons(r))

    def test_budget_deadline_and_no_mutating_config(self):
        with ins.observation_budget() as budget, patch.object(subprocess, 'Popen', side_effect=AssertionError('spawn')):
            with patch.object(ins.time, 'monotonic', return_value=budget['deadline'] + 1):
                with self.assertRaisesRegex(ins.InspectionError, 'TIMEOUT'):
                    ins._run(['rev-parse','HEAD'], cwd=str(self.root), deadline=10**12)
            with self.assertRaises(ins.InspectionError):
                ins._run(['config','user.name','bad'], cwd=str(self.root), deadline=10**12)

    def test_output_bound_and_invalid_projection_inputs(self):
        self.pending()
        b = rc.collect(str(self.root), store_dir=str(self.store_dir), now=STAMP)
        with patch.object(rc, 'MAX_BYTES', 256), self.assertRaisesRegex(rc.ReconciliationError, 'RESOURCE_LIMIT'):
            rc.classify(b)
        for mutate in (lambda x: x.update(local_error='FAKE_ERROR'),
                       lambda x: x['handoff']['last_known_good'].update(phase='FAKE_PHASE'),
                       lambda x: x['handoff']['last_known_good'].update(digest='short'),
                       lambda x: x['local_first']['identity'].update(inode=True),
                       lambda x: x['local_first'].update(extra='not allowed')):
            bad = copy.deepcopy(b); mutate(bad)
            with self.assertRaises(rc.ReconciliationError): rc.classify(bad)

    def test_cancellation_retains_history(self):
        self.pending()
        with patch.object(rc, '_local', side_effect=KeyboardInterrupt): r = self.run_rc()
        self.assertEqual(r['collection_outcome'], 'REFUSED')
        self.assertIn('CANCELLED', self.reasons(r))
        self.assertEqual(r['evidence']['handoff']['last_known_good']['phase'], 'CHECKPOINTING')

    def test_same_head_dirty_test_binding_unknown(self):
        self.pending('PASSED')
        (self.root / 'work.txt').write_text('changed without a commit\n')
        r = self.run_rc(tests=dict(result='PASSED', commands=['inert'], results=['pass'], bound_head=self.head))
        self.assertEqual(r['test_applicability'], 'UNKNOWN')
        self.assertEqual(r['evidence']['local_first']['head'], self.head)

    def test_review_deletion_and_size_bound(self):
        self.pending(); (self.root / 'work.txt').unlink()
        r = self.run_rc(review={'work.txt': None})
        self.assertEqual(r['review_applicability'], 'CURRENT')
        self.assertIsNone(r['evidence']['review_first'][0]['oid'])
        (self.root / 'work.txt').write_bytes(b'a' * (rc.cp.MAX_FILE_BYTES + 1))
        r = self.run_rc(review={'work.txt': '0'*64})
        self.assertEqual(r['review_applicability'], 'UNKNOWN')
        self.assertIn('CONTENT_LIMIT', self.reasons(r))

    def test_review_bytes_shared_across_both_reads(self):
        self.pending()
        data = (self.root / 'work.txt').read_bytes()
        with patch.object(rc.cp, 'MAX_TOTAL_BYTES', len(data) * 2 - 1):
            r = self.run_rc(review={'work.txt': hashlib.sha256(data).hexdigest()})
        self.assertEqual(r['review_applicability'], 'UNKNOWN')
        self.assertIn('CONTENT_LIMIT', self.reasons(r))
        self.assertNotIn('TARGET_CHANGED', self.reasons(r))

    def test_review_projection_binding_rejected(self):
        self.pending()
        value = hashlib.sha256((self.root / 'work.txt').read_bytes()).hexdigest()
        r = self.run_rc(review={'work.txt': value})
        r['evidence']['review_last'][0]['path'] = 'different.txt'
        with self.assertRaises(rc.ReconciliationError): rc.validate_result(r)

    def test_fresh_process_read_only(self):
        self.pending(); before = self.snapshot()
        script = 'from cgc.reconciliation import reconcile,render_json; import sys; print(render_json(reconcile(sys.argv[1],store_dir=sys.argv[2],now=sys.argv[3])))'
        output = subprocess.check_output([sys.executable, '-B', '-c', script, str(self.root), str(self.store_dir), STAMP],
            env={'PATH':'/usr/bin:/bin','PYTHONPATH':str(Path('src').resolve())}, timeout=10)
        result = json.loads(output)
        self.assertEqual(result['safe_to_resume'], 'UNKNOWN')
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(result, self.run_rc())


class RemoteReconciliationTests(unittest.TestCase):
    setUp = publication.PublicationTests.setUp
    git = publication.PublicationTests.git
    record = publication.PublicationTests.record
    args = publication.PublicationTests.args
    publish = publication.PublicationTests.publish
    bare = publication.PublicationTests.bare
    tip = publication.PublicationTests.tip
    snapshot = ReconciliationTests.snapshot
    run_rc = ReconciliationTests.run_rc
    reasons = ReconciliationTests.reasons

    def request(self):
        return dict(path=str(self.remote), identity=self.remote_identity, ref='refs/heads/main',
                    tracking_ref='refs/remotes/origin/main', expected_commit=self.head)

    def interrupt_publication(self, after=False):
        real = publication.pub._git
        def fail(fd, deadline, *command):
            if command[0] == 'fetch' and (not after or os.fstat(fd).st_ino == self.identity['inode']):
                raise ins.InspectionError('GIT_FAILED')
            return real(fd, deadline, *command)
        with patch.object(publication.pub, '_git', side_effect=fail):
            self.publish()

    def test_e_pending_remote_unchanged(self):
        self.interrupt_publication()
        r = self.run_rc(remote=self.request())
        self.assertEqual(r['collection_outcome'], 'OBSERVED', r)
        self.assertEqual(r['evidence']['remote_first']['tip'], self.base)
        self.assertEqual(r['evidence']['handoff']['last_known_good']['phase'], 'PUBLISHING')

    def test_f_pending_remote_equal_stale_tracking(self):
        self.interrupt_publication(after=True)
        r = self.run_rc(remote=self.request())
        self.assertEqual(r['remote_observation'], 'CURRENT', r)
        self.assertEqual(r['evidence']['remote_first']['tip'], self.head)
        self.assertEqual(r['evidence']['remote_first']['tracking'], self.base)
        self.assertIn('TRACKING_DIFFERS_FROM_REMOTE', self.reasons(r))
        self.assertIsNone(r['evidence']['handoff']['last_known_good']['receipts']['remote_commit'])

    def test_g_historical_verified_remote_moved(self):
        self.assertEqual(self.publish()['publication_status'], 'VERIFIED')
        self.git('commit', '--allow-empty', '-qm', 'later')
        changed = self.git('rev-parse', 'HEAD').decode().strip()
        self.bare('fetch', '-q', '--no-write-fetch-head', str(self.root), changed)
        self.bare('update-ref', 'refs/heads/main', changed)
        r = self.run_rc(remote=self.request())
        self.assertIn('REMOTE_MOVED_SINCE_RECEIPT', self.reasons(r))
        self.assertEqual(r['evidence']['handoff']['last_known_good']['publication_status'], 'VERIFIED')

    def test_p_remote_failure_and_local_default(self):
        request = self.request(); request['path'] += '-missing'
        r = self.run_rc(remote=request)
        self.assertEqual(r['collection_outcome'], 'OBSERVED')
        self.assertEqual(r['remote_observation'], 'UNKNOWN')
        with patch.object(rc, '_remote', side_effect=AssertionError('remote query')):
            r = self.run_rc()
        self.assertEqual(r['remote_observation'], 'NOT_QUERIED')

    def test_remote_projection_cross_field_binding(self):
        r = self.run_rc(remote=self.request())
        for key, value in (('direct', '0'*40), ('identity', {'device': 0, 'inode': 0}), ('tracking_error', 'GIT_FAILED')):
            bad = copy.deepcopy(r)
            for stage in ('first', 'last'): bad['evidence']['remote_' + stage][key] = value
            with self.assertRaises(rc.ReconciliationError): rc.validate_result(bad)
