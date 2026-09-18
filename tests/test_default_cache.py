"""Default path integration in synthetic homes; never inspect the actual Codex store."""
import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

from cgc.__main__ import main
from cgc.cache import Cache
from cgc.daemon import refresh_once
from synthetic_support import fixture_evidence
from test_engine import observation, STAMP


class DefaultCacheTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.home = Path(temp.name)
        self.parent = self.home / '.codex'
        self.target = self.parent / 'cgc'
        self.reader = Mock(return_value=observation())
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch('cgc.__main__.Path.home', return_value=self.home))
        self.stack.enter_context(patch('cgc.quota.app_server_read', side_effect=AssertionError('live forbidden')))
        self.stack.enter_context(patch('cgc.__main__.utcnow', return_value=STAMP))
        def synthetic(cache, **kwargs):
            return refresh_once(cache, **kwargs, reader=self.reader, clock=lambda: STAMP,
                                evidence_provider=fixture_evidence)
        self.stack.enter_context(patch('cgc.__main__.refresh_once', side_effect=synthetic))

    def command(self, command='refresh', extra=()):
        output = io.StringIO()
        args = [command, '--json'] + (['--live', '--bucket', 'codex'] if command == 'refresh' else [])
        with contextlib.redirect_stdout(output):
            code = main(args + list(extra))
        return code, json.loads(output.getvalue())

    def test_missing_parent_status_does_not_create(self):
        code, result = self.command('status')
        self.assertEqual(code, 1)
        self.assertEqual(result['error_code'], 'CACHE_MISSING')
        self.assertFalse(self.parent.exists())
        self.reader.assert_not_called()

    def test_missing_parent_refresh_refuses_without_creating_codex(self):
        code, _ = self.command()
        self.assertEqual(code, 2)
        self.assertFalse(self.parent.exists())
        self.reader.assert_not_called()

    def test_default_creates_only_cgc_and_never_enumerates_or_reads_siblings(self):
        self.parent.mkdir(mode=0o755)
        sibling = self.parent / 'unrelated.guard'
        sibling.write_bytes(b'SYNTHETIC_PRIVATE_SENTINEL')
        sibling.chmod(0o600)
        before = sibling.stat()
        original_open = os.open
        def guarded_open(path, flags, *args, **kwargs):
            self.assertNotEqual(str(path), sibling.name)
            self.assertNotEqual(str(path), str(sibling))
            return original_open(path, flags, *args, **kwargs)
        with patch('os.listdir', side_effect=AssertionError('enumeration forbidden')), \
             patch('os.scandir', side_effect=AssertionError('enumeration forbidden')), \
             patch('os.open', side_effect=guarded_open):
            code, result = self.command()
        self.assertEqual(code, 1)  # Explicit synthetic evidence, never live authority.
        self.reader.assert_called_once_with(timeout=20)
        self.assertEqual(result['generation'], 1)
        after = sibling.stat()
        self.assertEqual((before.st_ino, before.st_size, before.st_mtime_ns, before.st_atime_ns),
                         (after.st_ino, after.st_size, after.st_mtime_ns, after.st_atime_ns))
        self.assertEqual(sibling.read_bytes(), b'SYNTHETIC_PRIVATE_SENTINEL')
        self.assertEqual(self.target.stat().st_mode & 0o777, 0o700)
        self.assertEqual(set(p.name for p in self.parent.iterdir()), {'cgc', 'unrelated.guard'})
        self.assertEqual(self.command('status'), self.command('status', ['--cache-dir', str(self.target)]))
        self.assertNotIn('SYNTHETIC_PRIVATE_SENTINEL', json.dumps(result))

    def test_parent_symlink_never_followed(self):
        other = self.home / 'other'
        other.mkdir(mode=0o700)
        (other / 'cgc').mkdir(mode=0o700)
        self.parent.symlink_to(other)
        for command in ('status', 'refresh'):
            self.assertEqual(self.command(command)[0], 2)
        self.reader.assert_not_called()
        self.assertEqual(list((other / 'cgc').iterdir()), [])

    def test_target_regular_file_preserved(self):
        self.parent.mkdir()
        self.target.write_bytes(b'SYNTHETIC_PRIVATE_SENTINEL')
        for command in ('status', 'refresh'):
            code, out = self.command(command)
            self.assertEqual(code, 2)
            self.assertNotIn('SYNTHETIC_PRIVATE_SENTINEL', json.dumps(out))
        self.assertEqual(self.target.read_bytes(), b'SYNTHETIC_PRIVATE_SENTINEL')
        self.reader.assert_not_called()

    def test_target_dangling_symlink_preserved(self):
        self.parent.mkdir()
        outside = self.home / 'absent'
        self.target.symlink_to(outside)
        for command in ('status', 'refresh'):
            self.assertEqual(self.command(command)[0], 2)
        self.assertTrue(self.target.is_symlink())
        self.assertFalse(outside.exists())
        self.reader.assert_not_called()

    def test_public_target_directory_refused_without_chmod(self):
        self.parent.mkdir()
        self.target.mkdir(mode=0o755)
        for command in ('status', 'refresh'):
            self.assertEqual(self.command(command)[0], 2)
        self.assertEqual(self.target.stat().st_mode & 0o777, 0o755)
        self.assertEqual(list(self.target.iterdir()), [])
        self.reader.assert_not_called()

    def test_state_alias_cannot_read_or_overwrite_sibling(self):
        self.parent.mkdir()
        self.target.mkdir(mode=0o700)
        sibling = self.parent / 'unrelated.guard'
        sibling.write_bytes(b'SYNTHETIC_PRIVATE_SENTINEL')
        sibling.chmod(0o600)
        state = self.target / 'state.json'
        for alias in ('symlink', 'hardlink'):
            with self.subTest(alias=alias):
                if alias == 'symlink':
                    state.symlink_to(sibling)
                else:
                    os.link(sibling, state)
                for command in ('status', 'refresh'):
                    self.assertEqual(self.command(command)[0], 2)
                self.assertEqual(sibling.read_bytes(), b'SYNTHETIC_PRIVATE_SENTINEL')
                state.unlink()
        self.reader.assert_not_called()
