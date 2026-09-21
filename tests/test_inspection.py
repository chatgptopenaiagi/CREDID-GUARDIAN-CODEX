"""Offline V3 inspection fixtures; every target is disposable Linux storage."""
import copy
import contextlib
import io
import signal
import sys
import time
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from cgc.inspection import inspect_project, render_json, render_human

STAMP = '2026-09-21T00:00:00Z'


class InspectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='cgc-v3-', dir='/tmp')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'project'
        self.root.mkdir(mode=0o700)
        self.git('init', '-q', '-b', 'main')
        self.git('config', 'user.name', 'Synthetic')
        self.git('config', 'user.email', 'synthetic@example.invalid')

    def git(self, *args, check=True):
        return subprocess.run(['/usr/bin/git', '-C', str(self.root), *args],
                              env={'PATH': '/usr/bin:/bin', 'GIT_CONFIG_NOSYSTEM': '1',
                                   'GIT_CONFIG_GLOBAL': '/dev/null', 'GIT_OPTIONAL_LOCKS': '0'},
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=check).stdout

    def commit(self):
        (self.root / 'tracked').write_text('base\n')
        self.git('add', '--', 'tracked')
        self.git('commit', '-qm', 'fixture')

    def inspect(self):
        result = inspect_project(str(self.root), now=STAMP)
        self.assertEqual(result['status'], 'OBSERVED', result)
        return result

    def tree(self):
        # Includes index, refs, config, hooks, objects, ignored files and working bytes.
        result = {}
        for p in self.root.rglob('*'):
            st = p.lstat()
            result[str(p.relative_to(self.root))] = (
                st.st_mode, st.st_size, st.st_mtime_ns,
                os.readlink(p) if p.is_symlink() else
                hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None)
        return result

    def test_clean_identity_determinism_and_no_mutation(self):
        self.commit()
        before = self.tree()
        result = self.inspect()
        snap = result['snapshot']
        self.assertEqual(snap['root'], str(self.root))
        self.assertEqual(snap['head'], self.git('rev-parse', 'HEAD').decode().strip())
        self.assertEqual(snap['branch'], 'main')
        self.assertEqual(snap['changes'], [])
        self.assertEqual(result, self.inspect())
        self.assertEqual(before, self.tree())
        self.assertEqual(json.loads(render_json(result)), result)
        self.assertIn('INSPECTION ONLY', render_human(result))
        self.assertEqual(result['safe_to_resume'], 'UNKNOWN')
        self.assertFalse(result['automatic_mutation_authorized'])

    def test_dirty_staged_unstaged_untracked_deleted_rename_and_ignored(self):
        self.commit()
        (self.root / 'delete').write_text('delete\n')
        self.git('add', '--', 'delete'); self.git('commit', '-qm', 'second')
        self.git('mv', 'tracked', 'renamed')
        (self.root / 'renamed').write_text('changed\n')
        (self.root / 'delete').unlink()
        (self.root / 'new\nname').write_bytes(b'\x00synthetic-content-never-exported')
        (self.root / '.gitignore').write_text('ignored\n')
        (self.root / 'ignored').write_text('synthetic-secret')
        before = self.tree()
        snap = self.inspect()['snapshot']
        changes = {x['path']: x for x in snap['changes']}
        self.assertEqual(changes['renamed']['original_path'], 'tracked')
        self.assertEqual(changes['renamed']['index'], 'R')
        self.assertEqual(changes['renamed']['worktree'], 'M')
        self.assertEqual(changes['delete']['worktree'], 'D')
        self.assertEqual(changes['new\nname']['index'], '?')
        self.assertNotIn('ignored', changes)
        self.assertEqual(before, self.tree())
        self.assertNotIn('synthetic-content-never-exported', json.dumps(snap))
        self.assertNotIn('synthetic-secret', json.dumps(snap))

    def test_unborn_and_detached(self):
        snap = self.inspect()['snapshot']
        self.assertIsNone(snap['head']); self.assertEqual(snap['branch'], 'main')
        self.commit(); self.git('checkout', '--detach', '-q')
        snap = self.inspect()['snapshot']
        self.assertIsNone(snap['branch']); self.assertTrue(snap['detached'])

    def test_explicit_root_only_and_safe_failures(self):
        (self.root / 'nested').mkdir()
        for path in [None, '', '.', '/', str(self.root / 'nested'),
                     str(self.root / '..' / 'project'), str(self.root / 'absent')]:
            with self.subTest(path=path):
                result = inspect_project(path, now=STAMP)
                self.assertNotEqual(result['status'], 'OBSERVED')
                self.assertIsNone(result['snapshot'])
                self.assertIsNone(result['inspection_digest'])

    def test_symlink_root_metadata_and_special_file_refused(self):
        link = Path(self.tmp.name) / 'link'; link.symlink_to(self.root)
        self.assertEqual(inspect_project(str(link), now=STAMP)['error_code'], 'UNSAFE_PATH')
        (self.root / 'pipe').touch(); (self.root / 'pipe').unlink()
        os.mkfifo(self.root / 'pipe')
        self.assertEqual(inspect_project(str(self.root), now=STAMP)['error_code'], 'UNSAFE_FILE')
        (self.root / 'pipe').unlink()
        (self.root / '.git' / 'HEAD').unlink()
        (self.root / '.git' / 'HEAD').symlink_to('/nonexistent')
        self.assertEqual(inspect_project(str(self.root), now=STAMP)['error_code'], 'UNSAFE_FILE')

    def test_worktree_symlink_is_not_followed(self):
        self.commit()
        (self.root / 'link').symlink_to('/nonexistent/synthetic-secret')
        self.git('add', '--', 'link')
        before = self.tree(); result = self.inspect()
        self.assertNotIn('synthetic-secret', render_json(result))
        self.assertEqual(before, self.tree())

    def test_config_execution_and_includes_refused_before_status(self):
        for key in ['core.fsmonitor', 'filter.fixture.clean', 'include.path', 'core.worktree']:
            self.git('config', key, '/never-run-or-read-synthetic')
            result = inspect_project(str(self.root), now=STAMP)
            self.assertEqual(result['error_code'], 'UNSUPPORTED_CONFIG', (key, result))
            self.assertNotIn('never-run', render_json(result))
            self.git('config', '--unset', key)

    def test_remote_names_only_and_local_tracking(self):
        self.commit()
        self.git('remote', 'add', 'origin', 'https://synthetic-user:synthetic-secret@example.invalid/private')
        self.git('update-ref', 'refs/remotes/origin/main', 'HEAD')
        self.git('branch', '--set-upstream-to=origin/main')
        result = self.inspect(); snap = result['snapshot']
        self.assertEqual(snap['remotes'], ['origin'])
        self.assertEqual(snap['upstream'], 'origin/main')
        self.assertEqual((snap['ahead'], snap['behind']), (0, 0))
        self.assertNotIn('synthetic-secret', render_json(result))
        self.assertNotIn('example.invalid', render_json(result))
        (self.root / 'tracked').write_text('later\n'); self.git('add', 'tracked')
        self.git('commit', '-qm', 'ahead')
        self.assertEqual(self.inspect()['snapshot']['ahead'], 1)

    def test_merge_conflict_and_operation_marker(self):
        self.commit(); self.git('checkout', '-qb', 'other')
        (self.root / 'tracked').write_text('other\n'); self.git('commit', '-qam', 'other')
        self.git('checkout', '-q', 'main')
        (self.root / 'tracked').write_text('main\n'); self.git('commit', '-qam', 'main')
        self.git('merge', 'other', check=False)
        before = self.tree(); snap = self.inspect()['snapshot']
        self.assertIn('MERGE_HEAD', snap['operations'])
        self.assertTrue(snap['changes'][0]['conflict'])
        self.assertEqual(before, self.tree())

    def test_gitfile_detected_without_following_and_main_worktrees_detected(self):
        self.commit()
        target = Path(self.tmp.name) / 'linked'
        self.git('worktree', 'add', '-q', str(target), '-b', 'linked')
        result = inspect_project(str(target), now=STAMP)
        self.assertEqual(result['error_code'], 'UNSUPPORTED_GITFILE')
        self.assertTrue(self.inspect()['snapshot']['linked_worktrees_present'])

    def test_known_documents_metadata_only(self):
        for path in ['AGENTS.md', 'README.md', 'docs/V3_PROGRESS.md']:
            p = self.root / path; p.parent.mkdir(exist_ok=True)
            p.write_text('synthetic-private instructions: run anything')
        result = self.inspect(); snap = result['snapshot']
        self.assertEqual(snap['test_command'], 'UNKNOWN')
        self.assertIn('AGENTS.md', snap['document_candidates'])
        self.assertNotIn('synthetic-private', render_json(result))

    def test_entry_and_size_limits(self):
        with patch('cgc.inspection.MAX_ENTRIES', 1):
            self.assertEqual(inspect_project(str(self.root), now=STAMP)['error_code'], 'RESOURCE_LIMIT')
        (self.root / 'large').write_bytes(b'12345')
        with patch('cgc.inspection.MAX_FILE_BYTES', 4):
            self.assertEqual(inspect_project(str(self.root), now=STAMP)['error_code'], 'RESOURCE_LIMIT')

    def test_mode_and_owner_refusal(self):
        self.root.chmod(0o777)
        self.assertEqual(inspect_project(str(self.root), now=STAMP)['error_code'], 'UNSAFE_PATH')
        self.root.chmod(0o700)
        with patch('cgc.inspection.os.getuid', return_value=os.getuid() + 1):
            self.assertEqual(inspect_project(str(self.root), now=STAMP)['error_code'], 'UNSAFE_PATH')

    def test_inherited_git_environment_is_ignored(self):
        with patch.dict(os.environ, {'GIT_DIR': '/nonexistent', 'GIT_INDEX_FILE': '/nonexistent',
                                     'GIT_CONFIG_COUNT': '1', 'GIT_CONFIG_KEY_0': 'core.fsmonitor',
                                     'GIT_CONFIG_VALUE_0': 'never-execute'}):
            self.inspect()

    def test_submodule_gitlink_and_nested_repository_boundaries(self):
        self.commit()
        head = self.git('rev-parse', 'HEAD').decode().strip()
        self.git('update-index', '--add', '--cacheinfo', '160000,' + head + ',module')
        nested = self.root / 'module'; nested.mkdir()
        (nested / '.git').write_text('gitdir: /never-follow')
        os.mkfifo(nested / 'never-read')
        snap = self.inspect()['snapshot']
        self.assertEqual(snap['submodules'], ['module'])
        self.assertEqual(snap['submodule_worktrees'], 'NOT_INSPECTED')
        self.assertEqual(snap['nested_repositories'], ['module'])

    def test_other_operation_markers_are_metadata_only(self):
        self.commit()
        for name in ['CHERRY_PICK_HEAD', 'REVERT_HEAD', 'BISECT_LOG']:
            (self.root / '.git' / name).write_text('synthetic-private')
        for name in ['rebase-merge', 'rebase-apply', 'sequencer']:
            (self.root / '.git' / name).mkdir()
        snap = self.inspect()['snapshot']
        self.assertEqual(len(snap['operations']), 6)
        self.assertNotIn('synthetic-private', json.dumps(snap))

    def test_behind_diverged_and_missing_upstream(self):
        self.commit()
        self.git('remote', 'add', 'origin', 'https://example.invalid/repository')
        self.git('checkout', '-qb', 'other')
        (self.root / 'other').write_text('other')
        self.git('add', 'other'); self.git('commit', '-qm', 'other')
        self.git('update-ref', 'refs/remotes/origin/main', 'HEAD')
        self.git('checkout', '-q', 'main')
        self.git('branch', '--set-upstream-to=origin/main')
        snap = self.inspect()['snapshot']
        self.assertEqual((snap['ahead'], snap['behind']), (0, 1))
        (self.root / 'main').write_text('main')
        self.git('add', 'main'); self.git('commit', '-qm', 'main')
        snap = self.inspect()['snapshot']
        self.assertEqual((snap['ahead'], snap['behind']), (1, 1))
        self.git('update-ref', '-d', 'refs/remotes/origin/main')
        snap = self.inspect()['snapshot']
        self.assertEqual(snap['upstream'], 'origin/main')
        self.assertIsNone(snap['ahead']); self.assertIsNone(snap['behind'])

    def test_race_has_no_snapshot_or_receipt(self):
        import cgc.inspection as module
        original = module._scan
        calls = []
        def changing(fd, deadline):
            if calls:
                (self.root / 'raced').write_text('new')
            calls.append(True)
            return original(fd, deadline)
        with patch.object(module, '_scan', side_effect=changing):
            result = inspect_project(str(self.root), now=STAMP)
        self.assertEqual(result['error_code'], 'TARGET_CHANGED')
        self.assertIsNone(result['snapshot']); self.assertIsNone(result['inspection_digest'])

    def test_alternates_hardlinks_and_depth_refused(self):
        alternate = self.root / '.git/objects/info/alternates'
        alternate.write_text('/never-read')
        self.assertEqual(inspect_project(str(self.root), now=STAMP)['error_code'], 'UNSUPPORTED_LAYOUT')
        alternate.unlink()
        (self.root / 'a').write_text('fixture'); os.link(self.root / 'a', self.root / 'b')
        self.assertEqual(inspect_project(str(self.root), now=STAMP)['error_code'], 'UNSAFE_FILE')
        (self.root / 'b').unlink()
        with patch('cgc.inspection.MAX_DEPTH', 0):
            self.assertEqual(inspect_project(str(self.root), now=STAMP)['error_code'], 'RESOURCE_LIMIT')

    def test_config_and_total_byte_limits(self):
        with patch('cgc.inspection.MAX_CONFIG_BYTES', 1):
            self.assertEqual(inspect_project(str(self.root), now=STAMP)['error_code'], 'RESOURCE_LIMIT')
        with patch('cgc.inspection.MAX_TOTAL_BYTES', 1):
            self.assertEqual(inspect_project(str(self.root), now=STAMP)['error_code'], 'RESOURCE_LIMIT')

    def test_malformed_git_and_permission_failure_are_safe(self):
        (self.root / '.git/index').write_bytes(b'synthetic-secret-invalid-index')
        result = inspect_project(str(self.root), now=STAMP)
        self.assertEqual(result['error_code'], 'GIT_FAILED')
        self.assertNotIn('synthetic-secret', render_json(result))
        with patch('cgc.inspection._scan', side_effect=PermissionError('synthetic-secret')):
            result = inspect_project(str(self.root), now=STAMP)
        self.assertEqual(result['error_code'], 'FILESYSTEM_ERROR')
        self.assertNotIn('synthetic-secret', render_json(result))

    def test_sensitive_filename_is_not_emitted(self):
        secret = 'ghp_' + 'A' * 40
        (self.root / secret).write_text('synthetic')
        result = inspect_project(str(self.root), now=STAMP)
        self.assertEqual(result['error_code'], 'SENSITIVE_METADATA')
        self.assertNotIn(secret, render_json(result))

    def test_result_validation_and_attempt_receipt(self):
        from cgc.inspection import InspectionError, validate_inspection
        from cgc.preservation import new_attempt, advance
        result = self.inspect()
        attempt = new_attempt(str(self.root), now=STAMP, mission='Fixture', next_exact_action='Write handoff')
        attempt = advance(attempt, 'DOCUMENTING', now=STAMP,
                          evidence={'inspection_digest': result['inspection_digest']})
        self.assertEqual(attempt['safe_to_resume'], 'UNKNOWN')
        for key, value in [('safe_to_resume', 'YES'), ('secret', 'synthetic'), ('inspection_digest', 'f' * 64)]:
            bad = copy.deepcopy(result); bad[key] = value
            with self.assertRaises(InspectionError): validate_inspection(bad)
        bad = copy.deepcopy(result); bad['snapshot']['changes'] = [{'secret': 'synthetic'}]
        with self.assertRaises(InspectionError): render_json(bad)

    def test_subprocess_output_and_timeout_bounds_cleanup(self):
        from cgc.inspection import _run, InspectionError
        peer = Path(self.tmp.name) / 'peer'
        for body, expected in [
                ('import os\nwhile True: os.write(1, b"x" * 8192)', 'RESOURCE_LIMIT'),
                ('import os\nwhile True: os.write(2, b"x" * 8192)', 'RESOURCE_LIMIT'),
                ('import time\ntime.sleep(60)', 'TIMEOUT')]:
            peer.write_text('#!' + sys.executable + '\n' + body + '\n'); peer.chmod(0o700)
            start = time.monotonic()
            with patch('cgc.inspection.GIT', str(peer)), patch('cgc.inspection.COMMAND_SECONDS', 0.3):
                with self.assertRaises(InspectionError) as caught:
                    _run([], cwd='/', deadline=time.monotonic() + 2)
            self.assertEqual(caught.exception.code, expected)
            self.assertLess(time.monotonic() - start, 2)

    def test_cli_explicit_target_json_and_human_no_cache_or_sensor(self):
        from cgc.__main__ import main
        for json_mode in (False, True):
            out = io.StringIO()
            with contextlib.redirect_stdout(out), patch('cgc.__main__.Cache', side_effect=AssertionError), \
                    patch('cgc.__main__.refresh_once', side_effect=AssertionError):
                code = main(['inspect', '--project', str(self.root)] + (['--json'] if json_mode else []))
            self.assertEqual(code, 0)
            if json_mode: self.assertEqual(json.loads(out.getvalue())['status'], 'OBSERVED')
            else: self.assertIn('INSPECTION ONLY', out.getvalue())
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as caught:
            main(['inspect'])
        self.assertEqual(caught.exception.code, 2)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main(['inspect', '--project', '/nonexistent']), 1)

    def test_cli_sigint_sigterm_during_inspection(self):
        # Synchronize a real CLI child inside _scan, then interrupt. No target writes.
        for sig in (signal.SIGINT, signal.SIGTERM):
            code = """import os, signal, sys
from cgc import inspection
from cgc.__main__ import main
def waiting(*args):
    os.write(1, b'READY\\n')
    signal.pause()
inspection._scan = waiting
raise SystemExit(main(['inspect', '--project', sys.argv[1], '--json']))
"""
            before = self.tree()
            proc = subprocess.Popen([sys.executable, '-B', '-c', code, str(self.root)],
                                    env={**os.environ, 'PYTHONPATH': str(Path('src').resolve())},
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                import selectors
                with selectors.DefaultSelector() as selector:
                    selector.register(proc.stdout, selectors.EVENT_READ)
                    self.assertTrue(selector.select(5), 'CLI rendezvous timeout')
                self.assertEqual(proc.stdout.readline(), b'READY\n')
                proc.send_signal(sig)
                out, err = proc.communicate(timeout=5)
                self.assertEqual(proc.returncode, 1, err)
                self.assertEqual(json.loads(out)['error_code'], 'CANCELLED')
                self.assertEqual(before, self.tree())
            finally:
                if proc.poll() is None: proc.kill()
                proc.communicate()

    def test_assume_unchanged_and_skip_worktree_visible_without_changing_flags(self):
        self.commit()
        for flag in ('--assume-unchanged', '--skip-worktree'):
            self.git('update-index', flag, 'tracked')
            (self.root / 'tracked').write_text('hidden change')
            before = self.tree()
            snap = self.inspect()['snapshot']
            self.assertEqual(snap['hidden_index_paths'], ['tracked'])
            self.assertEqual(before, self.tree())
            self.git('update-index', '--no-assume-unchanged', '--no-skip-worktree', 'tracked')

    def test_known_credential_directory_boundary_without_opening(self):
        directory = self.root / '.codex'; directory.mkdir()
        os.mkfifo(directory / 'auth.json')
        result = inspect_project(str(self.root), now=STAMP)
        self.assertEqual(result['error_code'], 'UNSAFE_FILE')
        self.assertIsNone(result['snapshot'])

    def test_external_helper_sentinel_never_executed(self):
        marker = Path(self.tmp.name) / 'executed'
        helper = Path(self.tmp.name) / 'helper'
        helper.write_text('#!/bin/sh\ntouch "' + str(marker) + '"\n')
        helper.chmod(0o700)
        self.git('config', 'core.fsmonitor', str(helper))
        before = self.tree()
        self.assertEqual(inspect_project(str(self.root), now=STAMP)['error_code'], 'UNSUPPORTED_CONFIG')
        self.assertFalse(marker.exists()); self.assertEqual(before, self.tree())
        self.git('config', '--unset', 'core.fsmonitor')
        fifo = Path(self.tmp.name) / 'include'; os.mkfifo(fifo)
        self.git('config', 'include.path', str(fifo))
        start = time.monotonic()
        self.assertEqual(inspect_project(str(self.root), now=STAMP)['error_code'], 'UNSUPPORTED_CONFIG')
        self.assertLess(time.monotonic() - start, 2)


if __name__ == '__main__':
    unittest.main()
