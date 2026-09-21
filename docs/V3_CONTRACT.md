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
is lexical validation only. The attempt model alone does not verify root identity, symlinks, permissions or Git
state. The separate explicit inspection collector below supplies bounded local evidence.

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


## Bounded project inspection

IMPLEMENTED and VERIFIED OFFLINE on Linux with Git 2.55.0. Module
[inspection.py](../src/cgc/inspection.py), tests
[test_inspection.py](../tests/test_inspection.py). Snapshot envelope is separately
versioned `cgc-inspection-v3.0-provisional`; the attempt and V2 schemas are unchanged.
Public functions: inspect_project(project, now=...), validate_inspection, render_json,
render_human. CLI: `python -m cgc inspect --project /absolute/root [--json]`.

Only an exact explicitly selected ordinary working-tree root is accepted. No ancestor
repository search, path normalization through `..`, implicit cwd selection or target
mutation. Relative paths, root `/`, redundant components, missing/non-Git/nested-directory
targets are refused. Ancestors are opened descriptor-relatively without following links;
root must be owned by the current UID and not group/world writable. Root-owned sticky
ancestors such as /tmp are allowed. Target entries must be same-device, owned, safe-mode
regular files/directories or worktree symlink leaves. Hardlinked files, special files,
metadata symlinks and known credential directories (.codex/.ssh/.aws/.azure/.gnupg) are
refused. Native Windows and mounts that do not enforce these modes are unsupported.

The collector performs a bounded metadata-only preflight of this root including ignored
entries; it never opens worktree file contents in Python. Git itself can hash tracked
files and read local ignore/attribute rules to determine status. No file contents,
patches, object bodies, config values, identities, URLs or raw diagnostics enter output.
Worktree symlink destinations are neither read nor emitted. Nested repositories are
reported as boundaries and not traversed. Main-repository linked-worktree presence is
reported without opening other worktrees. A `.git` file target is refused as
UNSUPPORTED_GITFILE without reading its destination (covers linked worktrees and external
Git dirs). Submodules are identified from index gitlinks; their worktrees are explicitly
NOT_INSPECTED and their status changes are suppressed, not claimed clean.

The root snapshot contains:

- requested and observed root, device/inode identities for root and Git directory;
- caller-provided UTC observation time (CLI captures invocation time), LOCAL_OBSERVATION;
- HEAD or null for unborn, branch or null for detached HEAD, local upstream and optional
  ahead/behind counts; these use local tracking refs, never a live remote;
- sorted staged/unstaged/untracked/deleted/renamed/conflicted paths; rename source paths;
- paths with assume-unchanged/skip-worktree flags, whose contents Git may hide;
- fixed merge/cherry-pick/revert/rebase/sequencer/bisect marker presence, not file contents;
- remote names only, remote_state=NOT_QUERIED; no publication destination is authorized;
- gitlink paths, nested-repository boundaries and linked-worktree presence;
- presence of a fixed small set of instruction/handoff document candidates; contents
  NOT_READ and test_command=UNKNOWN, not invented or executed.

Git runs without a shell through fixed /usr/bin/git with an allowlisted environment,
no inherited Git overrides/global/system configuration, no prompts/lazy fetch/replace
objects/system attributes, and optional locks disabled. Only config parsing, rev-parse,
ls-files and porcelain-v2 status are used. Repository config is first parsed explicitly
with --no-includes from a no-follow descriptor outside repository discovery. Only basic
core settings, SHA object format, user name/email, remote URL/fetch settings, branch
remote/merge and submodule URL/active settings are accepted; their values are not exported.
Every other key is refused, including includes, filters, fsmonitor, hooksPath, external
attribute/exclude files and worktree redirection. Config is never changed and no mutation
hook is bypassed. Alternates, grafts, promisor and shared-index layouts are refused.
Unsupported configuration is a deliberate initial compatibility boundary, not permission
to rewrite a target's settings. Git status preserves repository ignore rules; global
ignore rules are excluded to avoid unrelated file reads.

| Bound | Limit and failure behavior |
|---|---|
| Metadata walk | 10,000 entries, depth 32, relative paths at most 4,096 bytes |
| Files examined by stat | 16 MiB per regular file, 64 MiB aggregate (includes Git metadata/ignored files) |
| Repository config | 64 KiB input; includes never followed |
| Git subprocess | 5 seconds per command, 256 KiB combined stdout/stderr; kill group and reap on failure/interruption |
| Whole inspection | 20-second cooperative deadline across scans/commands; no retry |
| Snapshot | 256 KiB serialized JSON; exact field allowlists; bounded lists |

Bounds fail closed without a truncated snapshot. They limit work, not hard CPU/RSS or
realtime kernel behavior: blocked filesystem syscalls and process reaping can exceed wall
budgets. Compressed Git objects can expand internally; no memory sandbox is claimed.
POSIX read access can update atime; file bytes, index, refs, HEAD, config and working-tree
state are not intentionally changed. Non-mutation tests compare all fixture file bytes,
modes, sizes and mtimes, including Git internals, before/after success and selected failures.

Status/index observations and metadata fingerprints repeat before success. Detected
change produces TARGET_CHANGED with no receipt. This is explicitly
REPEATED_OBSERVATION_NOT_ATOMIC: no lock against other writers, no snapshot isolation,
no defense against a hostile concurrent same-UID actor replacing config/paths between
checks. Use owner-controlled quiescent targets; future mutation needs fresh prechecks
and writer exclusion. The fingerprint excludes atime. Inspection is not a content backup,
a complete security audit or a guarantee that a later mutation is safe.

Both renderers validate the same envelope. JSON uses sorted keys and escaped text;
human output is explicitly INSPECTION ONLY plus that JSON, so filenames cannot become
report headings. An OBSERVED envelope carries a SHA256 digest of canonical snapshot JSON,
compatible with the existing attempt's inspection_digest receipt. The digest proves
representation integrity only, not authenticity, project preservation or fresh-process
resume. REFUSED includes a fixed error_code, null snapshot and null receipt; includes
unsupported targets, operational failures and CANCELLED. No raw path or stderr is echoed
on failure. CLI SIGINT/SIGTERM during inspection yields cancellation and cleanup.
SAFE_TO_RESUME remains UNKNOWN and automatic_mutation_authorized remains false always.
A successful inspection alone never advances an attempt to PRESERVED.

Recognizable credential-like metadata is refused, but arbitrary filenames/branch names
can themselves contain private information. Do not automatically publish inspection
output. No universal secret-detection guarantee. Tests use synthetic secrets only.

Git protocol references: [porcelain status and optional-lock guidance](https://git-scm.com/docs/git-status),
[Git environment controls](https://git-scm.com/docs/git). Live quota discovery was not repeated.
