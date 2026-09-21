"""V3 pure contract tests: no Git, source reads or project mutation."""
import copy
import json
import unittest

from cgc.preservation import (PreservationError, new_attempt, advance, validate_record,
                              render_json, render_human)

STAMP = '2026-09-19T00:00:00Z'
DIGEST = 'a' * 64
COMMIT = 'b' * 40


def record(level='HANDOFF_ONLY', trigger='SYNTHETIC'):
    return new_attempt('/synthetic/project', now=STAMP, mission='Preserve test work',
                       next_exact_action='Inspect the recorded failing test',
                       requested_level=level, trigger=trigger)


def verifying(level='HANDOFF_ONLY', evidence=None, **kwargs):
    state = advance(record(level), 'DOCUMENTING', now=STAMP)
    return advance(state, 'VERIFYING', now=STAMP, evidence=evidence, **kwargs)


def handoff():
    return {'inspection_digest': DIGEST, 'handoff_digest': DIGEST, 'resume_digest': DIGEST}


class PreservationContractTests(unittest.TestCase):
    def test_manual_independent_from_guardian(self):
        state = record(trigger='MANUAL')
        self.assertEqual(state['trigger'], 'MANUAL')
        self.assertEqual(state['safe_to_resume'], 'UNKNOWN')
        self.assertEqual(state['publication_status'], 'NOT_REQUESTED')
        self.assertFalse(state['automatic_mutation_authorized'])

    def test_untrusted_guardian_labels_cannot_be_triggers(self):
        for trigger in ['UNKNOWN', 'STALE', 'ERROR', 'RETAINED', 'HISTORICAL', 'RED', 'EMERGENCY', 'AUTOMATIC']:
            with self.subTest(trigger=trigger), self.assertRaises(PreservationError):
                record(trigger=trigger)

    def test_requested_path_is_not_verified_project(self):
        state = record()
        self.assertIsNone(state['evidence']['inspection_digest'])
        self.assertEqual(state['project_basis'], 'OPERATOR_REQUESTED')
        for path in ['', 'relative', '/x/../y', '/', '/x\x00y']:
            with self.assertRaises(PreservationError):
                new_attempt(path, now=STAMP, mission='m', next_exact_action='n')

    def test_allowed_lifecycle_and_terminal_no_reentry(self):
        state = record('REMOTE_VERIFIED')
        for phase in ['STABILIZING', 'TESTING', 'DOCUMENTING', 'CHECKPOINTING', 'PUBLISHING', 'VERIFYING']:
            state = advance(state, phase, now=STAMP)
        state = advance(state, 'PARTIAL', now=STAMP)
        for phase in ['INSPECTING', 'DOCUMENTING', 'PRESERVED']:
            with self.assertRaises(PreservationError):
                advance(state, phase, now=STAMP)

    def test_cannot_skip_to_preserved_or_forge_success(self):
        with self.assertRaises(PreservationError):
            advance(record(), 'PRESERVED', now=STAMP)
        with self.assertRaises(PreservationError):
            advance(verifying(), 'PRESERVED', now=STAMP)
        bad = record(); bad['safe_to_resume'] = 'YES'
        with self.assertRaises(PreservationError): validate_record(bad)

    def test_verified_handoff_resume_yes_and_json_human_agree(self):
        state = advance(verifying(evidence=handoff()), 'PRESERVED', now=STAMP)
        self.assertEqual(state['outcome'], 'HANDOFF_ONLY')
        self.assertEqual(state['safe_to_resume'], 'YES')
        self.assertEqual(json.loads(render_json(state)), state)
        human = render_human(state)
        for value in ['HANDOFF_ONLY', 'YES', '/synthetic/project', 'SYNTHETIC', 'Inspect the recorded failing test']:
            self.assertIn(value, human)

    def test_local_requires_verified_commit_receipt(self):
        state = verifying('LOCAL_CHECKPOINT', handoff())
        with self.assertRaises(PreservationError): advance(state, 'PRESERVED', now=STAMP)
        state = advance(state, 'PRESERVED', now=STAMP, evidence={'local_commit': COMMIT})
        self.assertEqual(state['outcome'], 'LOCAL_CHECKPOINT')

    def test_remote_requires_all_refs_equal_not_push_exit(self):
        evidence = dict(handoff(), local_commit=COMMIT, push_attempted=True)
        state = verifying('REMOTE_VERIFIED', evidence)
        with self.assertRaises(PreservationError): advance(state, 'PRESERVED', now=STAMP)
        state = advance(state, 'PRESERVED', now=STAMP,
                        evidence={'remote_commit': COMMIT, 'tracking_commit': COMMIT})
        self.assertEqual(state['publication_status'], 'VERIFIED')
        self.assertEqual(state['outcome'], 'REMOTE_VERIFIED')

    def test_push_failure_preserves_local_checkpoint_and_requested_level(self):
        evidence = dict(handoff(), local_commit=COMMIT, push_attempted=True,
                        publication_error='REMOTE_UNAVAILABLE')
        state = advance(verifying('REMOTE_VERIFIED', evidence), 'PARTIAL', now=STAMP)
        self.assertEqual(state['requested_level'], 'REMOTE_VERIFIED')
        self.assertEqual(state['local_checkpoint'], COMMIT)
        self.assertEqual(state['publication_status'], 'LOCAL_CHECKPOINT_ONLY')
        self.assertEqual(state['preservation_status'], 'PARTIAL')
        self.assertEqual(state['safe_to_resume'], 'PARTIAL')

    def test_ref_mismatch_cannot_claim_remote_success(self):
        evidence = dict(handoff(), local_commit=COMMIT, tracking_commit=COMMIT, remote_commit='c' * 40)
        with self.assertRaises(PreservationError): verifying('REMOTE_VERIFIED', evidence)

    def test_failed_tests_separate_from_preservation(self):
        state = verifying(evidence=handoff(), test_status='FAILED',
                          notes={'known_failures': ['Fixture test fails'], 'tests_run': ['python test.py'],
                                 'test_results': ['exit 1'], 'partial': ['Repair test']})
        state = advance(state, 'PRESERVED', now=STAMP)
        self.assertEqual(state['project_test_status'], 'FAILED')
        self.assertEqual(state['preservation_status'], 'PRESERVED')
        self.assertEqual(state['safe_to_resume'], 'YES')
        self.assertIn('Fixture test fails', render_human(state))
        self.assertEqual(state['notes']['partial'], ['Repair test'])

    def test_failed_and_skipped_tests_require_explanation(self):
        for status in ['FAILED', 'SKIPPED']:
            with self.assertRaises(PreservationError): verifying(test_status=status)
        state = verifying(test_status='SKIPPED', notes={'limitations': ['Emergency: tests not run']})
        self.assertEqual(state['project_test_status'], 'SKIPPED')

    def test_unsafe_block_and_cancel_never_yes(self):
        state = advance(record(), 'BLOCKED', now=STAMP, evidence={'unsafe_target': True})
        self.assertEqual(state['safe_to_resume'], 'NO')
        self.assertEqual(state['outcome'], 'BLOCKED_UNSAFE')
        cancelled = advance(verifying(evidence=handoff()), 'CANCELLED', now=STAMP)
        self.assertNotEqual(cancelled['safe_to_resume'], 'YES')
        self.assertEqual(cancelled['preservation_status'], 'CANCELLED')

    def test_timestamp_regression_and_naive_rejected(self):
        for now in ['2026-09-18T23:59:59Z', '2026-09-19', 'bad']:
            with self.assertRaises(PreservationError): advance(record(), 'DOCUMENTING', now=now)

    def test_input_aliases_do_not_mutate_record(self):
        original = record(); before = copy.deepcopy(original)
        notes = {'complete': ['A']}
        state = advance(original, 'DOCUMENTING', now=STAMP, notes=notes)
        notes['complete'].append('B')
        self.assertEqual(original, before)
        self.assertEqual(state['notes']['complete'], ['A'])

    def test_strict_schema_and_extra_secret_fields_rejected_without_echo(self):
        for key, value in [('schema_version', 'old'), ('secret', 'synthetic-private'),
                           ('automatic_mutation_authorized', True)]:
            bad = record(); bad[key] = value
            with self.assertRaises(PreservationError) as caught: validate_record(bad)
            self.assertNotIn('synthetic-private', str(caught.exception))
        with self.assertRaises(PreservationError):
            advance(record(), 'DOCUMENTING', now=STAMP, notes={'token': 'synthetic-private'})

    def test_text_list_and_receipt_bounds(self):
        for notes in [{'complete': ['x'] * 65}, {'mission': 'x' * 2049}, {'mission': '\x1b[31m'},
                      {'next_exact_action': ''}, {'complete': [True]}]:
            with self.assertRaises(PreservationError):
                advance(record(), 'DOCUMENTING', now=STAMP, notes=notes)
        for evidence in [{'local_commit': 'invalid'}, {'inspection_digest': 'a' * 63},
                         {'push_attempted': 1}, {'unsafe_target': 'false'},
                         {'publication_error': 'raw private message'}, {'unknown': True}]:
            with self.assertRaises(PreservationError): verifying(evidence=evidence)

    def test_event_tampering_and_illegal_transitions_rejected(self):
        state = verifying(evidence=handoff())
        bad = copy.deepcopy(state); bad['events'][1]['phase'] = 'PUBLISHING'
        with self.assertRaises(PreservationError): validate_record(bad)
        bad = copy.deepcopy(state); bad['events'] *= 65
        with self.assertRaises(PreservationError): validate_record(bad)

    def test_synthetic_result_always_identified_and_never_auto_authority(self):
        state = advance(verifying(evidence=handoff()), 'PRESERVED', now=STAMP)
        self.assertEqual(state['evidence_basis'], 'SYNTHETIC')
        self.assertFalse(state['automatic_mutation_authorized'])
        self.assertIn('SYNTHETIC', render_human(state))

    def test_reported_ref_mismatch_keeps_diagnostic_evidence(self):
        evidence = dict(handoff(), local_commit=COMMIT, tracking_commit=COMMIT,
                        remote_commit='c' * 40, publication_error='VERIFICATION_MISMATCH')
        state = advance(verifying('REMOTE_VERIFIED', evidence), 'PARTIAL', now=STAMP)
        self.assertEqual(state['evidence']['remote_commit'], 'c' * 40)
        self.assertEqual(state['publication_status'], 'LOCAL_CHECKPOINT_ONLY')
        self.assertEqual(state['safe_to_resume'], 'PARTIAL')

    def test_failed_new_transition_keeps_last_record_and_receipts(self):
        original = verifying('LOCAL_CHECKPOINT', dict(handoff(), local_commit=COMMIT))
        before = copy.deepcopy(original)
        with self.assertRaises(PreservationError):
            advance(original, 'PARTIAL', now=STAMP, evidence={'local_commit': None})
        self.assertEqual(original, before)

    def test_record_total_size_bound_and_safe_bad_phase(self):
        import cgc.preservation as contract
        from unittest.mock import patch
        with patch.object(contract, 'MAX_RECORD_BYTES', 1), self.assertRaises(PreservationError):
            validate_record(record())
        for phase in (None, [], {}, 'FORGED'):
            with self.assertRaises(PreservationError): advance(record(), phase, now=STAMP)
