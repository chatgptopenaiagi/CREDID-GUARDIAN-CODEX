"""Private external stores and curated synthetic handoffs only; no target mutation."""
import copy
import json
import os
import hashlib
import selectors
import signal
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from cgc.cache import CacheError
from cgc.handoff import HandoffStore, HandoffError, render_json, render_human, validate_state, MAX_HANDOFF_BYTES
from cgc.preservation import new_attempt, advance

STAMP = '2026-09-21T00:00:00Z'


def record(project, next_action='Implement the next bounded step'):
    value = new_attempt(str(project), now=STAMP, mission='CGC V3 handoff fixtures',
                        next_exact_action=next_action, trigger='SYNTHETIC')
    return advance(value, 'DOCUMENTING', now=STAMP,
                   notes={'complete': ['Inspection'], 'partial': ['V3'],
                          'not_started': ['Target Git mutation'], 'limitations': ['No atomic Git snapshot'],
                          'do_not_repeat': ['No live reads'], 'known_failures': ['Synthetic failing test'],
                          'tests_run': ['inert synthetic test command'], 'test_results': ['One failure']},
                   test_status='FAILED')


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='cgc-v3-handoff-', dir='/tmp')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.project = self.base / 'project'
        self.project.mkdir(mode=0o700)
        (self.project / 'work').write_text('unchanged synthetic work')
        self.path = self.base / 'handoff'

    def store(self, create=True):
        return HandoffStore(self.path, project=str(self.project), create=create)

    def seed(self):
        with self.store() as store, store.writer():
            return store.publish(record(self.project), now=STAMP)

    def test_roundtrip_determinism_human_and_modes(self):
        state = self.seed()
        with self.store(False) as store:
            self.assertEqual(store.read(), state)
        self.assertEqual(json.loads(render_json(state)), state)
        human = render_human(state)
        for text in ['COMPLETE', 'PARTIAL', 'NOT_STARTED', 'NEXT_EXACT_ACTION', 'One failure']:
            self.assertIn(text, human)
        self.assertEqual(state['safe_to_resume'], 'UNKNOWN')
        self.assertEqual(state['scope'], 'CONTINUITY_ONLY')
        self.assertEqual((self.path / 'handoff.json').read_text(), render_json(state) + '\n')
        self.assertEqual(self.path.stat().st_mode & 0o777, 0o700)
        for file in ['handoff.json', 'writer.lock']:
            self.assertEqual((self.path / file).stat().st_mode & 0o777, 0o600)

    def test_latest_failure_retains_known_good_and_recovery(self):
        first = self.seed()
        with self.store(False) as store, store.writer():
            failed = store.record_failure('INPUT_REJECTED', now=STAMP)
            self.assertEqual(failed['latest_attempt']['status'], 'FAILED')
            self.assertEqual(failed['last_known_good'], first['last_known_good'])
            final = store.publish(record(self.project, 'New exact action'), now=STAMP)
        self.assertEqual(final['generation'], 3)
        self.assertEqual(final['previous_known_good'], first['last_known_good'])
        self.assertEqual(final['last_known_good']['record']['project_test_status'], 'FAILED')

    def test_pre_replace_failure_preserves_bytes(self):
        self.seed(); before = (self.path / 'handoff.json').read_bytes()
        with self.store(False) as store, store.writer(), patch('cgc.handoff.os.replace', side_effect=OSError('synthetic-private')):
            with self.assertRaises(HandoffError) as caught:
                store.publish(record(self.project, 'Later'), now=STAMP)
        self.assertEqual(str(caught.exception), 'HANDOFF_WRITE_FAILED')
        self.assertEqual(before, (self.path / 'handoff.json').read_bytes())
        self.assertEqual(list(self.path.glob('*.tmp')), [])

    def test_post_replace_failure_is_uncertain_retains_previous(self):
        first = self.seed()
        with self.store(False) as store, store.writer():
            real = os.fsync
            def fail_directory(fd):
                if fd == store.fd: raise OSError('synthetic-private')
                return real(fd)
            with patch('cgc.handoff.os.fsync', side_effect=fail_directory), self.assertRaises(HandoffError) as caught:
                store.publish(record(self.project, 'Later'), now=STAMP)
            self.assertEqual(str(caught.exception), 'HANDOFF_PUBLICATION_UNCERTAIN')
            state = store.read()
            self.assertEqual(state['previous_known_good'], first['last_known_good'])
            self.assertEqual(state['last_known_good']['record']['notes']['next_exact_action'], 'Later')

    def test_writer_required_exclusion_and_release(self):
        with self.store() as one, self.store(False) as two:
            with self.assertRaises(HandoffError): one.publish(record(self.project), now=STAMP)
            with one.writer():
                with self.assertRaises(CacheError):
                    with two.writer(): pass
            with two.writer(): two.publish(record(self.project), now=STAMP)

    def test_target_storage_overlap_and_protected_paths_refused_before_create(self):
        for path in [self.project, self.project / 'handoff', self.base,
                     self.base / '.git' / 'handoff', self.base / '.codex' / 'handoff']:
            with self.subTest(path=path), self.assertRaises(HandoffError):
                with HandoffStore(path, project=str(self.project), create=True): pass
        self.assertEqual(list(self.project.iterdir()), [self.project / 'work'])

    def test_symlink_hardlink_modes_and_fifo_refused(self):
        self.seed()
        file = self.path / 'handoff.json'; saved = file.read_bytes()
        file.unlink(); file.symlink_to(self.project / 'work')
        with self.store(False) as store, self.assertRaises(HandoffError): store.read()
        self.assertEqual((self.project / 'work').read_text(), 'unchanged synthetic work')
        file.unlink(); os.mkfifo(file)
        with self.store(False) as store, self.assertRaises(HandoffError): store.read()
        file.unlink(); file.write_bytes(saved); file.chmod(0o600)
        os.link(file, self.path / 'alias')
        with self.store(False) as store, self.assertRaises(HandoffError): store.read()
        (self.path / 'alias').unlink(); file.chmod(0o644)
        with self.store(False) as store, self.assertRaises(HandoffError): store.read()

    def test_corrupt_duplicate_unknown_schema_size_refused_without_overwrite(self):
        self.seed()
        for raw in [b'{', b'{"x":1,"x":2}', b'{"schema_version":"old"}', b'x' * (2*1024*1024+1)]:
            (self.path / 'handoff.json').write_bytes(raw)
            with self.store(False) as store, store.writer():
                with self.assertRaises(HandoffError): store.read()
                with self.assertRaises(HandoffError): store.publish(record(self.project), now=STAMP)
            self.assertEqual((self.path / 'handoff.json').read_bytes(), raw)

    def test_model_digest_project_binding_and_no_input_aliasing(self):
        state = self.seed()
        bad = copy.deepcopy(state); bad['last_known_good']['record']['notes']['mission'] = 'forged'
        with self.assertRaises(HandoffError): validate_state(bad)
        with HandoffStore(self.path, project=str(self.base / 'other')) as store:
            with self.assertRaises(HandoffError): store.read()
        candidate = record(self.project)
        with self.store(False) as store, store.writer():
            saved = store.publish(candidate, now=STAMP)
            candidate['notes']['complete'].append('changed input')
            self.assertEqual(store.read(), saved)

    def test_recognizable_secret_notes_rejected_without_echo_or_write(self):
        self.seed(); before = (self.path / 'handoff.json').read_bytes()
        for value in ['ghp_' + 'A'*40, 'sk-proj-' + 'A'*40, 'sk-svcacct-' + 'A'*40,
                      '-----BEGIN ' + 'PRIVATE KEY-----',
                      'https://fixture:private@example.invalid/repo']:
            candidate = record(self.project); candidate['notes']['complete'] = [value]
            with self.store(False) as store, store.writer(), self.assertRaises(HandoffError) as caught:
                store.publish(candidate, now=STAMP)
            self.assertNotIn(value, str(caught.exception))
            self.assertEqual((self.path / 'handoff.json').read_bytes(), before)

    def test_fresh_process_readback_and_missing_status_no_creation(self):
        state = self.seed()
        command = [sys.executable, '-B', '-m', 'cgc', 'handoff-status', '--store-dir', str(self.path),
                   '--project', str(self.project), '--json']
        child = subprocess.run(command, capture_output=True, timeout=5)
        self.assertEqual(child.returncode, 0, child.stderr)
        self.assertEqual(json.loads(child.stdout), state)
        child = subprocess.run(command[:-1], capture_output=True, timeout=5)
        self.assertEqual(child.returncode, 0, child.stderr)
        self.assertEqual(child.stdout.decode().rstrip('\n'), render_human(state))
        with self.store(False) as store, store.writer():
            failed = store.record_failure('VERIFICATION_FAILED', now=STAMP)
        child = subprocess.run(command, capture_output=True, timeout=5)
        self.assertEqual(child.returncode, 0, child.stderr)
        self.assertEqual(json.loads(child.stdout), failed)
        missing = self.base / 'absent'; command[6] = str(missing)
        child = subprocess.run(command, capture_output=True, timeout=5)
        self.assertEqual(child.returncode, 1); self.assertFalse(missing.exists())


    def test_equivalent_mapping_order_has_identical_representations(self):
        state = self.seed()
        def reverse(value):
            if isinstance(value, dict):
                return {k: reverse(v) for k, v in reversed(list(value.items()))}
            if isinstance(value, list):
                return [reverse(v) for v in value]
            return value
        self.assertEqual(render_json(state), render_json(reverse(state)))
        self.assertEqual(render_human(state), render_human(reverse(state)))

    def test_schema_failure_distinct_from_malformed_and_never_migrated(self):
        state = self.seed()
        for version in ['cgc-handoff-v2', 'cgc-handoff-v99']:
            state['schema_version'] = version
            raw = json.dumps(state).encode()
            (self.path / 'handoff.json').write_bytes(raw)
            with self.store(False) as store, store.writer():
                with self.assertRaisesRegex(HandoffError, '^UNSUPPORTED_HANDOFF_SCHEMA$'):
                    store.read()
                with self.assertRaises(HandoffError):
                    store.record_failure('INPUT_REJECTED', now=STAMP)
            self.assertEqual((self.path / 'handoff.json').read_bytes(), raw)
            child = subprocess.run([sys.executable, '-B', '-m', 'cgc', 'handoff-status',
                    '--store-dir', str(self.path), '--project', str(self.project), '--json'],
                    capture_output=True, timeout=5)
            self.assertEqual(child.returncode, 1)
            self.assertEqual(json.loads(child.stdout)['error_code'], 'UNSUPPORTED_HANDOFF_SCHEMA')

    def test_field_list_record_and_render_bounds(self):
        state = self.seed()
        before = (self.path / 'handoff.json').read_bytes()
        for changes in [{'mission': 'x'*2049}, {'complete': ['x']*65},
                        {'complete': ['x'*2048]*64, 'partial': ['x'*2048]*64},
                        {'complete': [['nested']]}]:
            candidate = record(self.project)
            candidate['notes'].update(changes)
            with self.store(False) as store, store.writer(), self.assertRaises(HandoffError):
                store.publish(candidate, now=STAMP)
            self.assertEqual((self.path / 'handoff.json').read_bytes(), before)
        with patch('cgc.handoff.MAX_HANDOFF_BYTES', len(before)-1):
            with self.assertRaises(HandoffError): validate_state(state)
            with self.store(False) as store, self.assertRaisesRegex(HandoffError, 'HANDOFF_SIZE_LIMIT'):
                store.read()
        # An independently bounded human renderer must refuse rather than truncate.
        with patch('cgc.handoff.MAX_HANDOFF_BYTES', len(before)):
            with self.assertRaisesRegex(HandoffError, 'HANDOFF_SIZE_LIMIT'):
                render_human(state)
        self.assertLess(len(render_human(state).encode()), MAX_HANDOFF_BYTES)

    def test_failure_without_prior_success_and_monotonic_generation(self):
        with self.store() as store, store.writer():
            first = store.record_failure('CANCELLED', now=STAMP)
            self.assertIsNone(first['last_known_good'])
            self.assertEqual(first['latest_attempt']['error_code'], 'CANCELLED')
            with self.assertRaises(HandoffError):
                store.record_failure('CANCELLED', now='2026-09-20T00:00:00Z')
            self.assertEqual(store.read(), first)
            state = store.publish(record(self.project), now=STAMP)
            self.assertEqual(state['generation'], 2)
            self.assertIsNone(state['previous_known_good'])

    def test_project_symlink_alias_refused_before_storage_creation(self):
        alias = self.base / 'alias'
        alias.symlink_to(self.project, target_is_directory=True)
        destination = self.project / 'new-store'
        with self.assertRaises(HandoffError):
            with HandoffStore(destination, project=str(alias), create=True): pass
        self.assertFalse(destination.exists())
        # Storage path aliases are also refused by inherited no-follow traversal.
        with self.assertRaises(CacheError):
            with HandoffStore(alias / 'new-store', project=str(self.base / 'other'), create=True): pass
        self.assertFalse(destination.exists())

    def test_inspection_binding_and_target_nonmutation(self):
        from cgc.inspection import inspect_project
        subprocess.run(['/usr/bin/git', 'init', '-q', '-b', 'main', str(self.project)],
                       check=True, capture_output=True)
        def tree():
            return {str(p.relative_to(self.project)): (p.stat().st_mode, p.stat().st_size,
                    p.stat().st_mtime_ns, hashlib.sha256(p.read_bytes()).hexdigest())
                    for p in self.project.rglob('*') if p.is_file()}
        before = tree()
        inspection = inspect_project(str(self.project), now=STAMP)
        self.assertEqual(inspection['status'], 'OBSERVED', inspection)
        candidate = advance(new_attempt(str(self.project), now=STAMP, mission='V3',
                            next_exact_action='Reconcile current reality'), 'DOCUMENTING', now=STAMP,
                            evidence={'inspection_digest': inspection['inspection_digest']})
        with self.store() as store, store.writer():
            saved = store.publish(candidate, now=STAMP, inspection=inspection)
            self.assertEqual(store.read()['last_known_good']['inspection'], inspection)
            for bad in [None, dict(inspection, inspection_digest='0'*64)]:
                with self.assertRaises(HandoffError):
                    store.publish(candidate, now=STAMP, inspection=bad)
            self.assertEqual(store.read(), saved)
            store.record_failure('INSPECTION_FAILED', now=STAMP)
        self.assertEqual(tree(), before)
        self.assertNotIn('unchanged synthetic work', render_json(saved))
        # A historical handoff remains readable after the target goes missing.
        moved = self.base / 'moved-project'
        self.project.rename(moved)
        with self.store(False) as store:
            self.assertEqual(store.read()['last_known_good'], saved['last_known_good'])

    def test_process_death_atomicity_exclusion_and_restart(self):
        code = r"""
import json, os, signal, sys
from unittest.mock import patch
from cgc.handoff import HandoffStore
path, project, stage, candidate, stamp = sys.argv[1:]
def park():
    print('READY', flush=True)
    signal.pause()
real_replace, real_fdopen = os.replace, os.fdopen
class PartialWriter:
    def __init__(self, stream): self.stream = stream
    def __enter__(self): return self
    def __exit__(self, *args): return self.stream.__exit__(*args)
    def write(self, data):
        self.stream.write(data[:31]); self.stream.flush(); park()
def fdopen(fd, mode):
    stream = real_fdopen(fd, mode)
    return PartialWriter(stream) if mode == 'wb' and stage == 'partial_write' else stream
def replace(*args, **kwargs):
    if stage == 'before_replace': park()
    result = real_replace(*args, **kwargs)
    if stage == 'after_replace': park()
    return result
with HandoffStore(path, project=project, create=True) as store, store.writer():
    if stage == 'before_write': park()
    with patch('cgc.handoff.os.replace', replace), patch('cgc.handoff.os.fdopen', fdopen):
        store.publish(json.loads(candidate), now=stamp)
"""
        for stage in ['before_write', 'partial_write', 'before_replace', 'after_replace']:
            for seeded in [False, True]:
                with self.subTest(stage=stage, seeded=seeded):
                    self.path = self.base / (stage + str(seeded))
                    first = self.seed() if seeded else None
                    child = subprocess.Popen([sys.executable, '-B', '-c', code, str(self.path),
                            str(self.project), stage, json.dumps(record(self.project, 'After crash')), STAMP],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    try:
                        with selectors.DefaultSelector() as selector:
                            selector.register(child.stdout, selectors.EVENT_READ)
                            self.assertTrue(selector.select(5), 'rendezvous timeout')
                            self.assertEqual(child.stdout.readline(), b'READY\n')
                        with self.store(False) as store:
                            with self.assertRaises(CacheError):
                                with store.writer(): pass
                            # Even while a temp write is incomplete, readers see old or new.
                            live = store.read()
                            if stage != 'after_replace': self.assertEqual(live, first)
                        child.kill()
                        _, stderr = child.communicate(timeout=5)
                        self.assertEqual(child.returncode, -signal.SIGKILL)
                        self.assertEqual(stderr, b'')
                        with self.store(False) as store, store.writer():
                            survived = store.read()
                            if stage == 'after_replace':
                                self.assertEqual(survived['last_known_good']['record']['notes']['next_exact_action'], 'After crash')
                                self.assertEqual(survived['previous_known_good'], first['last_known_good'] if first else None)
                            else: self.assertEqual(survived, first)
                            leftovers = list(self.path.glob('.handoff-*.tmp'))
                            for file in leftovers:
                                self.assertEqual(file.stat().st_mode & 0o777, 0o600)
                            recovered = store.record_failure('CANCELLED', now=STAMP)
                            self.assertEqual(recovered['last_known_good'], survived['last_known_good'] if survived else None)
                            self.assertEqual(store.read(), recovered)
                            self.assertEqual(list(self.path.glob('.handoff-*.tmp')), leftovers)
                    finally:
                        if child.poll() is None: child.kill()
                        child.communicate(timeout=5)


if __name__ == '__main__': unittest.main()
