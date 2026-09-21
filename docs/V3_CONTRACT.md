# CREDID GUARDIAN CODEX — initial V3 attempt contract

Status: IMPLEMENTED and VERIFIED with synthetic values, not a preservation executor.
Schema: `cgc-preservation-v3.0-provisional`.
Implementation: [preservation.py](../src/cgc/preservation.py).
Tests: [test_preservation.py](../tests/test_preservation.py).

This domain is separate from the accepted V2 Guardian cache. No V2 field/schema changes,
quota reader, filesystem operation, subprocess, CLI preserve command or project mutation
are introduced. Public Python functions are new_attempt, advance, validate_record,
render_json and render_human. Schema changes are provisional and must be deliberate.

## Lifecycle and conclusions

INSPECTING may advance to STABILIZING, TESTING or DOCUMENTING. STABILIZING may advance
to TESTING or DOCUMENTING; TESTING to DOCUMENTING. DOCUMENTING advances to CHECKPOINTING
or VERIFYING; CHECKPOINTING to PUBLISHING or VERIFYING; PUBLISHING to VERIFYING. VERIFYING
finishes PRESERVED or PARTIAL. Every active phase may terminate BLOCKED, FAILED or
CANCELLED. Terminal records cannot reenter the lifecycle. Each new attempt is separate.
Event timestamps must be canonical UTC, nondecreasing and consistent with the phase.

Configured levels: HANDOFF_ONLY, LOCAL_CHECKPOINT, REMOTE_VERIFIED. Actual outcomes are
IN_PROGRESS, HANDOFF_ONLY, LOCAL_CHECKPOINT, REMOTE_VERIFIED, REMOTE_PUSH_ATTEMPTED,
BLOCKED_UNSAFE, PARTIAL_PRESERVATION, FAILED or CANCELLED. More specific creation/no-op
outcomes require future action evidence; an observed commit ID alone cannot prove a
new commit was created. A push attempt cannot prove remote publication.

| Dimension | Rule |
|---|---|
| PROJECT_TEST_STATUS | UNKNOWN/PASSED/FAILED/SKIPPED. Passed/failed require command/result notes; failure requires known failures; skipped requires limitations |
| PRESERVATION_STATUS | Current lifecycle phase; only VERIFYING can finish PRESERVED |
| PUBLICATION_STATUS | NOT_REQUESTED, NOT_ATTEMPTED, PUSH_ATTEMPTED, FAILED, LOCAL_CHECKPOINT_ONLY or VERIFIED; derived independently |
| SAFE_TO_RESUME | YES only at PRESERVED with configured-level receipts; NO for unsafe/failed-without-surviving-evidence; PARTIAL for surviving evidence at incomplete terminal state; otherwise UNKNOWN |

YES means the configured continuity level has its required receipts, not that project
tests passed. A known failing test can be preserved accurately for repair. Requested
REMOTE_VERIFIED with failed publication stays requested REMOTE_VERIFIED and actual
LOCAL_CHECKPOINT_ONLY when a local receipt survives. No silent downgrade.

## Evidence boundary

`project_request` and curated notes are operator input, not observed filesystem facts.
Requested path is absolute/bounded and rejects parent traversal/control characters; this
is lexical validation only. Root identity, symlinks, permissions and Git state remain
unverified until the next inspection block. No automatic disk scanning occurs.

Evidence fields are exact and optional until supplied:

- inspection_digest, handoff_digest, resume_digest: lowercase SHA256 receipt references;
- local_commit, tracking_commit, remote_commit: full lowercase SHA1/SHA256 Git object IDs;
- unsafe_target and push_attempted: exact booleans;
- publication_error: null or a fixed safe error class.

A receipt is immutable within an attempt once supplied. Inspection is required before
handoff/local receipts; handoff before resume receipt. Remote receipts require a local
commit. Differing refs require explicit VERIFICATION_MISMATCH and cannot authorize
PRESERVED at REMOTE_VERIFIED level. Equal local/tracking/remote refs establish the model's
remote verification condition without implying a push was necessary or performed.

HANDOFF_ONLY success requires inspection, handoff and fresh-resume verification receipts.
LOCAL_CHECKPOINT additionally requires local commit receipt; REMOTE_VERIFIED additionally
requires matching remote/tracking receipts. The future verifier must establish receipt
truth and relevance to this exact project/attempt before constructing them. Phase A only
checks structural consistency: hashes are not signatures, an integrity proof or trusted
external observations by themselves. Test receipts are SYNTHETIC. Manual adapter receipts
are labeled ADAPTER_REPORTED, not independently verified by this pure module.

MANUAL does not depend on quota. SYNTHETIC is visibly distinct. Other triggers are refused
in this phase, and automatic_mutation_authorized is always false. This fixed denial is
not a completed Guardian integration. Actual Guardian gating is a later block and must
consume canonical V2 state; no UNKNOWN/stale/retained/synthetic state may authorize mutation.

## Continuity data and bounds

Notes contain mission, exact next action, COMPLETE/PARTIAL/NOT_STARTED items, changed-file
notes, tests run/results, known failures, important discoveries, decisions, do-not-repeat
items and limitations. They are curated operational records, never hidden chain-of-thought.
Commands and paths stored in notes are inert text. No command execution is implemented.

Exact key allowlists reject extra fields, including arbitrary credential keys. Strings are
1–2048 code points without control characters; lists at most 64 strings; events at most
64; total serialized record at most 256 KiB. Full object IDs are required. JSON/human output
validate the same record and recompute conclusions. Human data is quoted to avoid imitating
report headings. Validation errors are fixed and do not echo rejected data.

These bounds and allowlists do not prove arbitrary caller-supplied text is secret-free.
Future capture/staging adapters must minimize and screen content; no raw Git output,
remote URL or project file is accepted automatically here. Dangerous/unrepresentable
paths can be refused until the inspection model supplies safe structured/escaped handling.

`advance` validates/copies its input and never mutates it. A rejected update leaves the
previous in-memory record usable. Atomic publication, latest-attempt/last-known-good
storage, writer exclusion and fresh-process resume remain NOT_STARTED.
