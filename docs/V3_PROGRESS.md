# CREDID GUARDIAN CODEX — CGC V3 progress

## OVERALL STATUS

**PARTIAL.** V3 is active under [V3_MISSION.md](V3_MISSION.md). V1/V2 remain accepted.
[Acceptance](V3_ACCEPTANCE.md) distinguishes this completed inspection block from the
remaining preservation mission. THE GUARDIAN OBSERVES. CODEX PRESERVES.

## CURRENT SESSION BLOCK

2026-09-21: **bounded, non-mutating explicit project inspection — COMPLETE** within the
supported Linux ordinary-root/configuration contract. Before edits, clean main, fetched
origin/main and live refs/heads/main all equaled
`4299df1039b3cf18d263b1024278471fce5ee16a`. Recent history, source, tests and progress agreed:
attempt model/recovery/publication complete; inspector absent. No newer work was discarded.
Read the full active mission/contract/progress/acceptance and required repository records.
Executed the recorded inspection block; did not repeat recovery or start handoff writes.

## COMPLETE

- Previously published pure attempt model and 22 tests retained unchanged. Manual requests
  do not depend on Guardian state; automatic authority remains denied.
- New inspection.py explicit-root collector and `inspect --project PATH [--json]` CLI.
  Separate `cgc-inspection-v3.0-provisional` snapshot; attempt/V2 schemas unchanged.
- Owned, safe-mode, no-follow root and metadata validation; bounded same-device traversal;
  explicit rejection of special/hardlinked files, unsafe metadata, credential directories,
  Gitfiles, alternates/promisor/shared-index layouts and unreviewed Git configuration.
- Git HEAD/branch/unborn/detached/upstream/local ahead-behind, staged/unstaged/untracked/
  deleted/renamed/conflicted paths, operation markers, remote names, gitlinks, hidden index
  flags, nested boundaries, main linked-worktree presence and document candidates.
- No document content/URL/diagnostic export. Instructions NOT_READ, test_command UNKNOWN,
  remote_state NOT_QUERIED, submodule_worktrees NOT_INSPECTED. No project command execution.
- Fixed environment/executable, read-only Git command set, optional locks disabled;
  bounded output/time with process cleanup and SIGINT/SIGTERM cancellation. Repeat status,
  index and metadata checks refuse detected races. No atomic snapshot claim.
- Human/JSON views share validation and receipt digest. Receipt can populate the existing
  attempt's inspection_digest without granting preservation/resume/mutation authority.
- 29 new deterministic inspection tests; full 204-test regression passes.

## PARTIAL

Full V3 preservation remains PARTIAL. Snapshot evidence is local, bounded, observational
and non-atomic; no target was declared preserved. Attempt receipts still depend on trusted
adapters. Gitfile/linked-worktree targets are detected/refused rather than followed;
submodule and nested repository contents are outside this target's scope. Unknown test
commands/instructions require explicit curated knowledge in a later handoff block.
Remote names/counts are not verified publication identity or live remote state.

## NOT_STARTED

Handoff persistence, preservation executor/CLI, project test execution, deliberate staging,
local target commits, target push/remote verification, project writer exclusion, canonical
latest-attempt/last-known-good state, preservation idempotency, fresh-process handoff
resume, Guardian integration and automatic preservation. V4/cloud/GUI are not authorized.

## TESTS PASSED

Test-first inspection run: one expected loader error (missing cgc.inspection), zero new
bodies; resolved by implementation. First 14 tests passed in 0.427s; expanded 26 passed in
1.365s; final inspection suite **29 passed in 1.573s**, no failures/errors/skips.

Canonical final command:

```bash
TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -q
```

**204 tests passed in 15.936s; zero failures, errors or skips.** Includes all 153 V1/V2
regressions, 22 existing V3 attempt tests and 29 new inspection tests. No existing test
was changed or weakened. Inspection help also succeeds without a sensor/cache operation.
Git version tested: 2.55.0. Previous 175-test recovery run is historical, not repeated as
another work block. Publication static gates: **22 Python files parse, three JSON files parse, 115 local
Markdown targets resolve; 46 repository files screened.** One credential-URL pattern
finding in tests/test_inspection.py is the deliberate synthetic URL fixture used to prove
non-export; reviewed, no real credential involved. No other recognizable pattern findings.
Pattern screening is not proof of universal secrecy. Git whitespace passes. Existing
runtime (apart from additive CLI dispatch), all prior tests, both mission texts, V2 records
and exact directives match the entry checkpoint.

## TESTS REMAINING

Future handoff persistence/atomic last-known-good/writer/fresh-process tests, deliberate
staging/secrets/large-file policy, target commit/local bare-remote publication/failures,
crash/interruption throughout mutation, canonical Guardian integration and safe automation.
No live quota read is needed for the next block. No inspection test failure remains.

## KNOWN FAILURES / LIMITATIONS

No unresolved observed deterministic failures. Strict configuration/size/mode/layout
refusals are intentional compatibility limits. Native Windows/0777-mounted targets are
unsupported; do not weaken security to accept them. Full limits and error semantics:
[V3_CONTRACT.md](V3_CONTRACT.md#bounded-project-inspection).

Repeated observations do not protect against hostile concurrent same-UID mutation or
establish atomicity. Git can read/hash tracked content internally; no content is exported.
Reads may update atime. Metadata traversal includes ignored files and can refuse a large
ignored build tree. No hard memory/CPU sandbox or realtime blocked-kernel-call guarantee.
Remote URL values and user identity are discarded during config validation. Filenames
can themselves be sensitive; pattern rejection is not universal secret detection.
No automatic publication of inspection output. Inspection does not authorize mutation.

## IMPORTANT DISCOVERIES

A nominally read-only Git command needs configuration isolation: fsmonitor/filters and
includes can invoke helpers or access external data. This first collector refuses such
configuration before status rather than modifying it. Optional locks must be disabled to
avoid index refresh writes. Synthetic sentinel/FIFO tests prove selected config hazards
are not executed/followed. Local ahead/behind is not live remote verification. Hidden
index flags and ignored submodules must remain visible limitations, not an all-clean claim.

## NON-MUTATION / SECRET SAFETY EVIDENCE

Fixture comparisons cover every regular-file byte hash, mode, size and mtime, including
HEAD, refs, index, objects, config, hooks, ignored files and working-tree bytes. Clean,
dirty, conflict, symlink, index-flag, unsafe-helper and interrupted inspections preserve
those comparisons. Only test setup intentionally constructs dirty/conflicted Git states.
No inspected target is committed/staged/reset/cleaned/stashed by the inspector.
Synthetic content secrets, credential-bearing URL and helper/error strings do not enter
output. Known credential directory and external include FIFO tests refuse without opening
those contents. Recognizable credential-like filename produces no snapshot or receipt.

## FILES CREATED / MODIFIED

Created: src/cgc/inspection.py, tests/test_inspection.py.
Modified: src/cgc/__main__.py (isolated inspect dispatch), README.md, AGENTS.md,
docs/ARCHITECTURE.md, docs/DATA_MODEL.md, docs/PRESERVATION_POLICY.md,
docs/SECURITY_MODEL.md, docs/V3_CONTRACT.md, docs/V3_ACCEPTANCE.md,
docs/V3_PROGRESS.md, docs/DECISIONS.md, tests/README.md.
All existing tests, preservation.py, V1/V2 runtime except additive CLI dispatch, V2
records, active V3 mission and verbatim preservation directives remain unchanged.

## DO_NOT_REPEAT

Do not redo foundation/recovery/inspection blocks absent a demonstrated defect. Do not
repeat V1 discovery/live quota reads, infer current authority from supplied percentages,
scan unrelated projects/authentication stores, follow Gitfiles automatically, relax
security modes, blindly stage, force-push or begin V4. Inspection receipts are not
handoff/resume/publication receipts. No actual preservation operations ran in fixtures.

## NEXT_EXACT_ACTION

Verify current Git/source/test/progress reality. Implement one coherent **human + machine
handoff persistence** block using the existing validated attempt and inspection models,
explicit curated continuity input and an explicitly selected safe storage destination.
Prove bounded atomic publication, writer exclusion appropriate to handoff writes,
latest-attempt vs last-known-good retention, and fresh-process readback in disposable
Linux targets. Preserve COMPLETE/PARTIAL/NOT_STARTED, failures/tests/unknowns and exact
next action in both representations. Do not infer test commands or execute project
instructions automatically. No target staging/commits/push, Guardian automation or V4 in
that block. Define storage ownership/path/receipt semantics before writing fixtures;
validate, document, checkpoint, publish/verify and stop at coherent handoff acceptance.

## LAST SAFE CHECKPOINT

Entry published checkpoint: `4299df1039b3cf18d263b1024278471fce5ee16a`.
Inspection checkpoint: HEAD after normal commit/publication; resolved hash in final
report. No self-containing SHA. Preserve local checkpoint if publication fails.

## PUBLICATION STATE

Entry HEAD/tracking/live main equality verified. Inspection changes not yet published at
this pre-commit record. Publish only validated CGC main to the authorized
chatgptopenaiagi/CREDID-GUARDIAN-CODEX; verify actual local/tracking/live equality after
push. Record observed publication in a follow-up if needed; never infer it from push exit.

## OPERATIONS / INTEGRITY

Live quota reads: this session 0, V3 0, V2 0, historical V1 1. Human supplied approximate
capacity values are informational, not an independent Guardian observation/authority.
Target live remote operations: 0. CGC Git fetch/ls-remote and authorized checkpoint pushes
only; official Git reference pages read to verify porcelain/environment semantics.
Synthetic /tmp/cgc-v3-* repositories and executable peers created and cleaned by tests.
No dependency installs, persistent environment/system/security changes, default cache,
authentication inspection or unrelated/valuable-project writes. No target preservation,
no background process/service/monitor and no later version started.
