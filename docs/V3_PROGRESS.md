# CREDID GUARDIAN CODEX — CGC V3 progress

## OVERALL STATUS

**PARTIAL.** Attempt, bounded inspection, durable handoff, manual checkpoint, local-bare
publication and independent verification remain accepted. Signal/ref-transaction, loose-object
transfer and current **real active commit pre/post-acceptance interruption acceptance are
COMPLETE / VERIFIED OFFLINE within their scoped contracts**. Broader crash safety and full
safe resume remain PARTIAL. Network publication, automation and Agent Fabric remain NOT_STARTED.
The [complete mission](V3_MISSION.md), including all 100 architectural keypoints, and current
user instructions remain authoritative. V1/V2 are unchanged and accepted.

THE GUARDIAN OBSERVES. CODEX PRESERVES. PRESERVE BEFORE EXPANDING.

## CURRENT SESSION BLOCK

Verified root, clean main, empty diff, whitespace, recent history and independent live remote.
Entry HEAD = origin/main = live refs/heads/main =
`7e44417341daab653c5e2c9009552fa240944875`. Historical equality was independently checked.
Prior transfer acceptance implementation `586bd6bb1d627de39eadf19e2858876f12924af8` remains accepted.

Read current progress and relevant checkpoint/runner/signal/handoff paths. Reconciled already-read
instructions, full mission/architecture/security/V1/V2 records and relevant prior tests against
exact checkpoint bytes. No newer conflicting work. Selected only the recorded next action:
**in-command local checkpoint commit interruption**. Earlier dispatch/return, ref-transaction
and transfer coverage is retained, not duplicated or redesigned.

Uncovered boundary: real Git alive before acceptance versus alive after HEAD advances but before
normal process completion. Fixture-only pre/post-commit hook gates provide observable stages.
Git performs actual staging/commit operations; no mocked success, HEAD, index or receipt.
Existing runtime satisfies final assertions: **no runtime edits or demonstrated runtime defect**.

## CAPACITY

Included-capacity percentage **UNKNOWN**. No reliable current source or human percentage;
no estimation, extrapolation or purchased-credit inference. Live quota reads zero.
The <=20% preservation trigger has **NOT** activated. One block, validation, publication and STOP.

## COMPLETE

- Ten new tests plus a fixture helper use real Git commit processes in disposable Linux /tmp
  repositories. Hook PID/parent/process-group rendezvous and independent command-line/PID checks
  prove Git itself is still active. Two release controls complete verified real commits.
- Eight interrupted cases cover pre/post-commit SIGINT, SIGTERM, timeout and abrupt SIGKILL of
  the Git command process group. Parent signals reuse mutation_signals. Test command bound is
  four seconds; production remains five. No claim of CGC-parent SIGKILL cleanup.
- Before acceptance: old HEAD, reviewed change staged, unrelated untracked work intact. After
  acceptance: new commit with exactly the old HEAD as parent and exactly the intended tree,
  selected change committed, unrelated work intact. Accepted commit never rolled back.
- Both return commit_attempted=true, local_commit=null, outcome=PARTIAL, SAFE_TO_RESUME=UNKNOWN
  and publication_status=NOT_REQUESTED. Signals return CANCELLED, timeout TIMEOUT and abrupt
  command-group death GIT_FAILED. Exactly one commit dispatch; no automatic retry/publication.
- Index bytes at the gate survive interruption unchanged; logical staged entries equal reviewed
  bytes. Before acceptance index also matches dispatch bytes. Working file bytes/modes/mtimes
  and repository configuration survive unchanged. No automatic reset, lock deletion or repair.
- Prior good continuity survives beside CHECKPOINTING intent without a new local receipt.
  Latest failure records CANCELLED for signals, otherwise VERIFICATION_FAILED. Fresh-process
  handoff-status exactly reproduces saved state; fresh Git HEAD/status/parent/tree reads expose
  repository reality without changing the interrupted return value or fabricating a receipt.
- A contender with fresh observed HEAD and a different store receives WRITER_BUSY at both active
  commit stages, without staging or store creation. This tests the actual in-command interval,
  rather than confusing stale-HEAD refusal with lock exclusion.
- Existing runner kills the command group and reaps the direct Git child; hook terminates.
  Previous signal handlers restore, both CGC locks release. Test-only subreaper collects orphaned
  hooks without killing survivors before assertions; production descendant reaping is not claimed.
- A later explicit stale/repeated request refuses EXISTING_STAGING before acceptance or
  TARGET_CHANGED after acceptance. No duplicate commit, index change or handoff overwrite.

## PARTIAL

Overall V3, general crash acceptance and safe resume remain PARTIAL. The tested in-command
stages are real Git waiting on fixture hooks. They bracket acceptance but do not prove every
hookless object/index/ref mutation syscall, active add/index replacement, arbitrary Git versions,
filesystems, power loss, abrupt-parent descendants or cross-source writers.

Production continues to refuse executable hooks and core.hooksPath config. Only the test commit
subprocess receives a fixture-only hook override after preflight, with no source config or hook
file changes. This proves controlled Git lifecycle behavior, not support for production hooks.

## NOT_STARTED

General HTTPS/SSH/Git-push transport; valuable target publication; automatic retry, rollback,
GC, lock deletion or repair; preserve CLI; full resume engine; project test runner; Guardian
autonomous authority; automatic/background mutation; Agent Fabric/CWM/HHS/ARX/AI integration;
GUI/mobile/V4. No telemetry or new capability framework.

## TESTS PASSED / DEVELOPMENT FAILURES

Historical entry: 292 tests passed in 53.000s, zero failures/errors/skips. Not rerun as a baseline.
Initial new suite: **10 tests in 10.320s, five passed and five assertion failures, zero errors/skips**.
All failures were the same incorrect fixture expectation that pre-commit holds index.lock.
The real Git rendezvous showed that lock absent. Post-acceptance cases already passed.
Corrected tests to observed no-lock behavior and EXISTING_STAGING refusal; no runtime fix.

```text
TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_commit_interruption -q
Ran 10 tests in 15.094s — OK

TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_commit_interruption test_checkpoint test_mutation_interruption -q
Ran 50 tests in 27.688s — OK
```

Relevant V3 regression:

```text
TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_preservation test_inspection test_handoff test_checkpoint test_publication test_mutation_interruption test_transfer_interruption test_commit_interruption -q
Ran 149 tests in 52.192s — OK
```

Final full regression:

```text
TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -q
Ran 302 tests in 69.620s — OK
```

**All corrected/final runs: zero failures, errors or skips.** All 292 inherited tests and runtime
unchanged. Full regression ran once. No runtime/test edits after final verification; subsequent
changes are documentation evidence only.

Static/documentation checks passed: 35 Python ASTs, three JSON files, 153 local Markdown
file/anchor links and all 100 mission keypoints. All 59 tracked/new project files screened;
only two known synthetic credential-URL fixtures in test_handoff.py and test_inspection.py matched.
No real credential finding; pattern screening cannot prove universal absence. Expected CGC
fetch/push destination verified without credential output. Whitespace passed; exact new test/
helper contents and documentation diff reviewed. Runtime and mission texts are unchanged.

## IMPORTANT DISCOVERIES

A commit can be fully accepted while its Git process is still waiting on post-commit work.
Cancellation must not imply HEAD stayed old. The interrupted adapter correctly withholds a local
success receipt; fresh Git evidence establishes the surviving commit separately. Before acceptance,
staged reviewed bytes survive and prevent a blind repeat. The pre-commit gate has no index.lock
in this Git environment: lock artifacts must be observed, not extrapolated from other Git stages.

Durable uncertainty plus independent HEAD/index/status evidence answers whether work survived
without guessing, duplicate commits or destructive cleanup. No telemetry or automatic reconciliation
was needed. Current authority remains separate from all stored information.

## KNOWN FAILURES / LIMITATIONS

No unresolved deterministic failures. The five initial assertion failures were corrected as
fixture assumptions, not hidden or presented as production defects. Hook gates and temporary
worker subreaper are test-only. No production hook bypass, signal redesign or lock redesign.

SIGKILL of CGC itself cannot execute cleanup; descendants may continue after its flock releases.
Only command-group death, caller graceful cancellation and bounded timeout are tested here.
No universal power-loss, hard syscall deadline, native-Windows, hostile same-user filesystem/config
race or bind-mount guarantee. Existing strict owner-controlled/quiescent target rules remain.
Storage failure can retain only earlier intent; success/failure persistence remains best effort.
No automatic rollback, lock cleanup, duplicate commit, publication or SAFE_TO_RESUME claim.

## TESTS REMAINING

Large-pack/index-pack transfer interruption; active staging/index replacement; interruption
inside hookless commit mutation syscalls; abrupt CGC-parent death with descendants; cross-source
publication concurrency; full fresh-process Git/test/intent reconciliation. No live quota read
required. Accepted stage evidence is not a universal durability or recovery guarantee.

## FILES CREATED / MODIFIED

Created: `tests/test_commit_interruption.py`, `tests/helpers/commit_peer.py`.
Modified: `AGENTS.md`, `README.md`, `docs/V3_PROGRESS.md`, `docs/V3_CONTRACT.md`,
`docs/V3_ACCEPTANCE.md`, `tests/README.md`.
Runtime, existing tests, schemas, V1/V2 records and mission texts unchanged. No unrelated
architecture/decision documents edited because no runtime design changed.

## DO_NOT_REPEAT

Do not repeat accepted implementation, dispatch/return cancellation, ref/loose-transfer or these
real commit gate tests without defect evidence. Do not assume index.lock exists at every stage.
No live quota discovery, credential access, automatic retry/rollback/repair/lock deletion,
blind staging, force push, reset/clean, unrelated repository checks or Fabric/V4 work.
No success receipt from an attempt, no authority from a handoff, no safe resume from HEAD alone.

## NEXT_EXACT_ACTION

After verified publication, STOP. Next scoped acceptance block: **audit and test active
local-bare index-pack interruption after temporary pack arrival using real Git fixtures**.
The existing transfer proof explicitly covers loose objects only; examine that remaining pack
storage path without redesigning publication. Preserve refs, source work and all uncertain
artifacts. Do not implement GC/repair, automatic retry, network transport, full resume or automation.
Other staging/parent-death boundaries remain documented, not silently promoted to complete.

## LAST SAFE CHECKPOINT

Starting verified checkpoint: `7e44417341daab653c5e2c9009552fa240944875`.
Current acceptance implementation checkpoint: **HEAD after normal commit/publication**;
resolved hash and independent publication evidence belong in the final report/evidence follow-up.
No self-containing hash. Prior detailed acceptance evidence remains in Git history.

## PUBLICATION STATE

Entry local/tracking/live equality verified. Current block awaits final validation, normal forward
commit/push and independent ref equality. No remote preservation claim for uncommitted work.

## OPERATIONS / INTEGRITY

Session live quota reads **0**; V3 **0**; V2 **0**; historical V1 **1**. No /status percentage.
Target network operations **0**. Only disposable Linux /tmp targets/stores/hooks are used.
Test workers, groups and fixture directories cleaned by teardown. Subreaper settings die with
worker processes. No persistent system/environment/security changes, installs, services, auth
access, default cache creation or unrelated repository inspection/mutation. CGC-only network:
entry live ref check and authorized final normal publication/verification.
