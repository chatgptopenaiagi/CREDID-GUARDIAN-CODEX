# CREDID GUARDIAN CODEX — CGC V3 progress

## OVERALL STATUS

**PARTIAL.** Attempt, inspection, durable handoff, deliberate manual checkpoint and
restricted local-bare publication foundations remain accepted. The current **manual
cancellation / active ref-transaction concurrency subset is COMPLETE / VERIFIED OFFLINE**.
Broader mutation/publication crash hardening remains PARTIAL. General network publication,
full safe resume, automation and Agent Fabric runtime remain NOT_STARTED.
The [complete mission](V3_MISSION.md), including all 100 architectural keypoints, and current
user instructions remain authoritative. V1/V2 are unchanged and accepted.

THE GUARDIAN OBSERVES. CODEX PRESERVES. PRESERVE BEFORE EXPANDING.

## CURRENT SESSION BLOCK

2026-09-23: verified root, clean main, empty diff, recent history and independent live ref.
Entry HEAD = origin/main = live refs/heads/main =
`b12b7d05d82ac3affc90fa8fccda3488168f627b`. This confirms the historical checkpoint rather
than assuming it. Prior implementation `0e1d62a9741b616f0e0a8e9a39b399eb48c885f7` and recovery
evidence remain accepted; no repeated publication implementation or quota investigation.
Read required project records and audited existing command cleanup, writer locks and tests.

Selected the smallest coherent subset of the authorized crash/concurrency block:
caller-owned signal cancellation, real active ref transactions, same-source writer exclusion
and truthful durable uncertainty. Found no need to redesign the working Git runner or locks.
SIGTERM previously had no manual-adapter cancellation scope; inspection cancellation also
lost its classification at the checkpoint/publication boundary. Both gaps are addressed.

## CAPACITY

User context: Pro / 5X included capacity, separate from purchased credits. No reliable current
included-capacity percentage is available to this process. No percentage, exhaustion or
threshold crossing inferred. Live quota reads: zero. The <=20% preservation trigger has
**NOT** activated. Work is bounded to this subset, then validation, publication and STOP.

## COMPLETE

- New opt-in `cgc.signals.mutation_signals()` for one synchronous main-thread manual call.
  First SIGINT/SIGTERM cancels; repeated signals allow cleanup/failure persistence to finish.
  Previous handlers restore on normal/exceptional exit; worker-thread entry refuses safely.
- Checkpoint/publication retain CANCELLED through inspection, return and best-effort durable
  failure recording. Existing schemas, authority requirements and pending/good-slot retention
  remain intact. Saved intent never grants authority or establishes remote preservation.
- Real Git interactive ref transaction tests rendezvous after prepare (lock held) and commit
  acknowledgement (new ref accepted), while Git remains active. Actual runner timeout, group
  termination and direct-child reaping are exercised. SIGINT/SIGTERM never fabricate receipts.
- Active Git child SIGKILL and timeout retain old ref and pending continuity. Prepared Git
  locks survive termination and are refused on subsequent explicit calls, never unlinked.
- Checkpoint and publication contenders are refused at both active publication stages, even
  when using different handoff stores. No contender staging, store creation, ref or handoff
  changes. Both CGC locks release after cleanup; work, index and source HEAD survive.
- Fresh-process handoff-status reconstructs the exact failure state and previous continuity.
  Accepted-but-unverified remote work can be independently inspected and then explicitly
  reverified with current expected tip, without another publication attempt.
- Checkpoint SIGINT/SIGTERM dispatch/acceptance boundary tests preserve staged bytes or the
  accepted single-parent commit, with no unverified local receipt. These are boundary tests.
- Contract documents recovery evidence and remaining ambiguity, reducing repeated investigation
  without adding telemetry, a resume engine, monitoring or speculative infrastructure.

## PARTIAL

Overall V3 and broader mutation/publication crash/concurrency acceptance remain PARTIAL.
The accepted active-ref fixture uses real `git update-ref --stdin` transactions substituted
for one fixture command; it does not prove interruption at every syscall of the ordinary
one-shot command. Checkpoint cancellation tests are at dispatch/return, not inside add/commit.
Active transfer, in-command checkpoint mutation, abrupt-parent descendant lifetime and
multiple source repositories publishing to one bare target remain outside this subset.
Publication VERIFIED still does not establish SAFE_TO_RESUME; outer state remains UNKNOWN.

## NOT_STARTED

General target Git-push/HTTPS/SSH transport; valuable real target publication; preserve CLI;
project test runner; full fresh-process Git/test reconciliation; Guardian automatic authority;
automatic/background preservation; resume generator; Agent Fabric/Gateway/Control/Data Plane/
Router/Event Bus runtime; cloud/local AI integration; GUI/mobile/V4. No instrumentation added.

## TESTS PASSED

Historical entry evidence: 48 checkpoint/publication tests in 9.554s and 270 full tests in
28.800s, zero failures/errors/skips, at the prior recovered checkpoint. Not rerun as a baseline.

Current development runs:

- Initial 10 new tests: **10 passed in 6.530s**.
- Expanded focused integration: **63 passed in 19.005s**.
- Final focused integration after cancellation-classification correction:

```text
TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_mutation_interruption test_checkpoint test_publication -q
Ran 65 tests in 18.920s — OK
```

Final full regression:

```text
TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -q
Ran 287 tests in 39.522s — OK
```

**All current runs: zero failures, errors or skips.** Seventeen new tests; all 270 inherited
tests retained unchanged. No redundant full-suite runs after documentation-only changes.
Static/documentation checks passed: 31 Python ASTs, three JSON files, 147 local Markdown
file/anchor links and all 100 mission keypoints. Tracked/new project files screened for
recognizable credentials; only the two previously reviewed synthetic credential-URL fixtures
in test_handoff.py and test_inspection.py matched. No real credential finding; pattern
screening cannot prove universal absence. Fetch/push destination matches the expected CGC
GitHub repository. Git whitespace check passed. Exact source/tests and documentation diff
reviewed before staging; inherited runtime outside the two adapters and mission texts unchanged.

## TESTS REMAINING

Active object-transfer cancellation/process interruption; in-command add/commit crash behavior;
CGC-parent SIGKILL while a Git descendant runs; distinct source writers sharing a bare target.
Do not generalize tested direct-child cleanup to abrupt-parent cleanup. Full future acceptance
also needs fresh-process Git/test reconciliation and separately scoped Guardian integration.
No live quota read is needed to continue.

## KNOWN FAILURES / LIMITATIONS

No observed deterministic test failures in this block. Git lock files retained after a killed
prepared transaction are expected safety artifacts, not permission to repair automatically.
The existing runner terminates its process group with SIGKILL; it cannot ask Git to unlink a
prepared lock. The adapter refuses such locks before retry. CGC flock release does not prove
that arbitrary external or orphaned Git processes have stopped.

Signal handling is opt-in/main-thread and process-wide within the caller's short scope.
It grants no permission. Further SIGINT/SIGTERM are ignored until scope exit; SIGKILL still
kills the parent without cleanup. No hard bound on blocked filesystem syscalls or reaping,
universal power-loss durability, malicious same-user path/config races or bind-mount aliases.
Owner-controlled quiescent ordinary Linux repositories and restricted configuration remain
required. Native Windows/Windows-mounted mode enforcement is not relaxed.

Failure persistence is best effort: storage failure or process death may leave only the prior
pending intent. LOCAL_CHECKPOINT_ONLY means remote preservation is unverified, not untouched.
No automatic retries/rollback/unlink, safe-resume inference, project test execution or history
secret audit. Current caller approval must still cover policy, selected bytes and/or all
reachable publication history for the exact destination.

## FILES CREATED / MODIFIED

Created: `src/cgc/signals.py`, `tests/test_mutation_interruption.py`,
`tests/helpers/mutation_peer.py`.
Modified runtime: `src/cgc/checkpoint.py`, `src/cgc/publication.py`.
Modified docs: `AGENTS.md`, `README.md`, `docs/V3_CONTRACT.md`, `docs/V3_ACCEPTANCE.md`,
`docs/V3_PROGRESS.md`, `docs/DECISIONS.md`, `tests/README.md`.
Inherited tests, inspection/Git runner, V1/V2 runtime, schemas and mission texts unchanged.

## DO_NOT_REPEAT

Do not redo accepted publication/checkpoint implementation, before/after SIGKILL proof,
active prepared/accepted ref cancellation or same-source exclusion without defect evidence.
No repeated live quota reads, credential access, blind staging, force options, reset/clean,
automatic stale-lock deletion, rollback/retry, unrelated repository mutation or Fabric/V4.
Do not infer authority or remote equality from pending handoffs or successful command exits.
Do not conflate purchased credits with included capacity or invent a live percentage.

## NEXT_EXACT_ACTION

After this subset is published and independently verified, STOP this session.
Next scoped block: **test active local-bare object-transfer interruption with synchronized
Git/child-process fixtures**, first auditing the existing runner's process-group cleanup and
source-lock lifetime. Preserve pending/previous continuity and all partial objects; document
abrupt-parent descendant uncertainty. Do not add general network push, automatic repair,
full resume, Guardian automation, telemetry, Fabric or V4.

## LAST SAFE CHECKPOINT

Starting verified checkpoint: `b12b7d05d82ac3affc90fa8fccda3488168f627b`.
Current implementation checkpoint: `3721dd022d14b0470dbde429483312f9cc6314be`.
Final evidence checkpoint: **HEAD after normal commit/publication**; its resolved hash and
independent publication result belong in the final report.
Never invent a self-containing commit hash. Prior evidence remains accessible in Git history.

## PUBLICATION STATE

Implementation **REMOTE_VERIFIED** on 2026-09-23. Normal forward push to the approved CGC
origin/main succeeded. An independent live query confirmed local HEAD = origin/main = live
refs/heads/main = `3721dd022d14b0470dbde429483312f9cc6314be`; working tree clean.

This documentation-only follow-up records that observed equality and acceptance row 41.
Its own HEAD is committed/pushed normally and independently verified for the final report.
Runtime/tests are unchanged from the 287-test verification; no redundant regression required.
Final document targets and staged whitespace checked before publication. If follow-up push
fails, retain the local evidence commit and report LOCAL_CHECKPOINT_ONLY; never invent equality.

## OPERATIONS / INTEGRITY

Session live quota reads **0**; V3 **0**; V2 **0**; historical V1 **1**. No live /status value.
Target network operations **0**. All runtime mutation tests use disposable Linux /tmp Git
repositories and external stores. Test peers/processes are cleaned; retained Git locks stay
inside fixtures until fixture disposal. No valuable external repository publication.
CGC-only network: initial live ref check and authorized final normal publication/verification.
No installs, services, authentication access, environment dumps, default cache creation,
persistent system/security changes, unrelated repository inspection or mutation.
