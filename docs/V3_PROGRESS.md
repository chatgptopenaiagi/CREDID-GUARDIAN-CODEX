# CREDID GUARDIAN CODEX — CGC V3 progress

## OVERALL STATUS

**PARTIAL.** V3 is authorized and active. V1/V2 remain accepted foundations.
Authoritative detailed specification: [V3_MISSION.md](V3_MISSION.md), read together with
current user instructions. [V3_ACCEPTANCE.md](V3_ACCEPTANCE.md) tracks remaining criteria.

THE GUARDIAN OBSERVES. CODEX PRESERVES.
PRESERVE BEFORE EXPANDING.

## CURRENT SESSION BLOCK

2026-09-21: reconciliation and preservation of the existing, uncommitted V3
foundation. This is one recovery block; project inspection is the next separate block.
Before edits, root was verified and main HEAD, origin/main and live remote main all
matched `1e3a1c54217101f87c8eb45baad354f7daec834a`. Eight tracked documentation files
were modified and six V3 files were untracked, including the implementation and tests.
No V3 commit existed in recent history. All existing work was retained.

The previous progress described an older 126-section mission and its hashes, while the
actual authoritative V3_MISSION.md now has three main sections (870 lines). The current
mission was read completely and is preserved byte-for-byte in this session. Old phase
and numbered-section references are not current requirements. The prior acceptance
claim that V3 publication was verified was unsupported by actual refs and is corrected.
The previous 175-test result is historical; validation below establishes current evidence.

The coherent frontier is the pure attempt contract, awaiting its first safe publication.
Reconcile and validate this foundation before expanding to filesystem/Git inspection.
No implementation or test was restarted or rewritten; no V1/V2 behavior changed.

## COMPLETE

- Pure versioned cgc-preservation-v3.0-provisional attempt contract in preservation.py.
  Exact fields, bounded notes/events/record size, UTC timestamps, replayed legal phase
  transitions, immutable receipt accumulation and terminal-state refusal to resume.
- MANUAL requests independent of Guardian availability; SYNTHETIC explicitly labeled.
  Automatic/RED/UNKNOWN/STALE/etc. are not accepted triggers in this first phase.
  automatic_mutation_authorized is always false. No duplicate quota reader.
- Separate PROJECT_TEST_STATUS, PRESERVATION_STATUS, PUBLICATION_STATUS and SAFE_TO_RESUME.
  YES requires terminal PRESERVED and inspection/handoff/fresh-resume receipts plus
  checkpoints appropriate to requested level. Failed tests need documented test evidence
  and known failures; accurate preservation of failing work can still be resumable.
- Requested level remains visible if only local work survives. Push attempt alone is
  insufficient; remote receipt equality is required. Explicit verification mismatch can
  retain diagnostic refs without claiming remote success. No claim that a commit was
  newly created merely because its identity exists.
- Bounded COMPLETE/PARTIAL/NOT_STARTED, test commands/results, failures, decisions,
  discoveries, changed-file notes, do-not-repeat and exact next action fields.
  Human/JSON renderers validate one model; human data is quoted rather than executable.
- 22 new pure synthetic tests. All inherited V1/V2 runtime and tests remain unchanged.

## PARTIAL

Phase A is an initial attempt contract, not the final complete preservation envelope.
Evidence receipts are typed assertions from a trusted future adapter, not externally
verified facts: current tests supply synthetic receipts. SAFE_TO_RESUME=YES in a fixture
proves model semantics only. No actual project was declared preserved by this code.
Project snapshot shape/collector and the latest-attempt/last-known-good persistence envelope
are deferred to their coherent blocks. Full V3 acceptance is PARTIAL.

## NOT_STARTED

Explicit project inspection CLI; filesystem/Git target validation; actual handoff writing;
project test execution; safe staging; local commit creation; push and remote verification;
project writer locks; canonical atomic preservation cache; idempotency; process resume;
Guardian integration and automatic preservation. V4/cloud/GUI/ARX work NOT_STARTED.
No preserve or preservation-status command exists yet.

## TESTS PASSED

Inherited checkpoint: 153 passing tests. Test-first new-module run failed at import
(one loader error, zero new bodies) because preservation.py did not yet exist.
Initial model: 19 new tests passed. Expanded 22-test run found two errors (bad phase
handling and verification-mismatch evidence); both resolved. Full suite reportedly reached 175
passing tests in 13.543s in the prior handoff. This is historical evidence only.
Current-session full regression result is recorded below.

Canonical command:

```bash
TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -q
```

Current recovery run: **175 tests passed in 15.270s; zero failures, errors or skips.**
This includes all 153 V1/V2 regressions and 22 existing V3 model tests. No new tests
were added and no completed experiment was repeated. The mission requires this
pre-publication regression run. No unresolved test failure was found.

Publication gates: 20 Python files parse, three JSON files parse, 106 local Markdown
targets resolve, and 44 candidate repository files pass bounded recognizable
credential-pattern screening (zero findings, not proof of universal secret absence).
Inherited runtime/tests, V2 mission/progress/acceptance and verbatim directives match
HEAD. Git whitespace passes. No configured custom hooksPath was found (Git query
exit 1 means unset, not a validation failure); no hooks were bypassed.

## TESTS REMAINING

All external-effect V3 acceptance: synthetic project inspection/path cases, actual
handoff publication/fresh-process resume, deliberate staging/secrets/large files,
local checkpoint, local bare remotes, failure/publication verification, project locks,
crash/signals/atomic last-known-good state, canonical Guardian integration. No live quota
read is required for the next block. See full acceptance matrix.

## KNOWN FAILURES

No unresolved observed deterministic failure. Structurally consistent receipts are not
proof of external effects; no signing or tamper-proof claim. Curated notes may contain
sensitive text if the caller supplies it; this model does not inspect files or implement
universal secret detection. Future capture/staging adapters must screen/minimize data.
Requested project path validation is lexical only (absolute, bounded, no parent traversal
or control characters); it is not filesystem identity, ownership or symlink validation.

## IMPORTANT DISCOVERIES

Preservation success and passing project tests are independent. A requested path is
OPERATOR_REQUESTED, not an observed root. Receipt identity does not prove a new Git action.
Phase A must not fabricate project snapshots or instantiate automatic mutation authority.
The failure of an advance operation leaves its input record unchanged; that is pure value
semantics, not yet last-known-good disk persistence. Unknown project test command remains
UNKNOWN; stored commands are inert curated notes and are never executed here.

## FILES CHANGED

Included existing user-supplied file: docs/V3_MISSION.md (unchanged this session).
Created: src/cgc/preservation.py, tests/test_preservation.py, docs/V3_PROGRESS.md,
docs/V3_ACCEPTANCE.md, docs/V3_CONTRACT.md.
Modified: README.md, AGENTS.md, docs/DECISIONS.md, docs/ARCHITECTURE.md,
docs/DATA_MODEL.md, docs/PRESERVATION_POLICY.md, docs/SECURITY_MODEL.md, tests/README.md.
V2 mission/progress/acceptance and all inherited runtime/tests unchanged.
This recovery session edited only README.md, docs/DECISIONS.md, docs/V3_PROGRESS.md
and docs/V3_ACCEPTANCE.md; the other listed changes were retained from entry.

## DO_NOT_REPEAT

Do not repeat V1 discovery/live reads, reopen V2 acceptance, discard newer work, trust an
old SHA over present evidence, or treat synthetic receipts as observed external actions.
Do not mutate real projects, add a second sensor or start automation before manual
preservation/resume proof. No blind staging, force push, destructive cleanup or V4.

## NEXT_EXACT_ACTION

Inspect current repository reality, read full V3 mission/progress/contract and reconcile
any newer work. Complete one **bounded non-mutating explicit project inspection** block
(current mission section 2, Explicit project identity, and section 3). Write tests first in disposable Git
repositories for explicit path/root validation, symlink/ownership boundaries, bounded
porcelain status, branch/HEAD/upstream, staged/unstaged/untracked/deleted/renamed paths,
conflicts/in-progress Git operations, worktree/submodule detection and safe remote metadata.
Preserve requested vs observed identity and UNKNOWN test-command/instruction knowledge.
Do not execute project instructions/tests/hooks, traverse unboundedly, inspect credentials,
write handoffs, stage/commit/push targets or enable Guardian automation in that block.
Expose safe human/JSON inspection via a narrowly named CLI if coherent. Version/extend
the provisional snapshot contract explicitly, validate/document/checkpoint/push, then stop.

## LAST SAFE CHECKPOINT

Starting published checkpoint: 1e3a1c54217101f87c8eb45baad354f7daec834a.
Recovery checkpoint: HEAD after normal commit/publication; resolved hash in
final report. No self-containing SHA. Preserve local checkpoint if publication fails.

## PUBLICATION STATE

At reconciliation, V3 was UNPUBLISHED; the prior success claim was unsupported.
Normal forward CGC main publication authorized. Verify HEAD = origin/main = live main
and clean tree after push. If unsuccessful, record LOCAL_CHECKPOINT_ONLY. No target
project checkpoint/publication feature was exercised or implemented.

## OPERATIONS / INTEGRITY

Live quota reads: V3 0; V2 0; historical V1 1. Real external project preservation: 0.
Synthetic end-to-end preservation operations: 0 (22 model tests are not operations).
CGC development checkpoint/publication only. No dependency installs, persistent system
changes, default cache creation, auth inspection or unrelated project writes. Tests use
Linux /tmp for inherited permission-sensitive cases. No capacity observation invented.
