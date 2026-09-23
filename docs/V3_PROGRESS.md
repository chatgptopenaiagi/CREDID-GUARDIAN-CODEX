# CREDID GUARDIAN CODEX — CGC V3 progress

## OVERALL STATUS

**PARTIAL.** Attempt, bounded inspection, durable handoff, manual checkpoint, restricted
local-bare publication and independent verification remain accepted. Manual signal/ref-transaction
hardening and the current **active local-bare loose-object transfer interruption subset are
COMPLETE / VERIFIED OFFLINE**. Broader crash acceptance and full safe resume remain PARTIAL.
Network publication, Guardian automation and Agent Fabric runtime remain NOT_STARTED.
The [complete mission](V3_MISSION.md), including all 100 architectural keypoints, and current
user instructions remain authoritative. V1/V2 are unchanged and accepted.

THE GUARDIAN OBSERVES. CODEX PRESERVES. PRESERVE BEFORE EXPANDING.

## CURRENT SESSION BLOCK

Verified root, clean main, empty diff/whitespace, recent history and independent live remote.
Entry HEAD = origin/main = live refs/heads/main =
`4ef724adfb06485ec069bbaffd32803a62b794ca`. Historical equality was checked, not assumed.
Prior hardening implementation `3721dd022d14b0470dbde429483312f9cc6314be` remains accepted.

Read current instructions, progress, contract, acceptance and relevant source/tests; reconciled
previously read full mission/architectural/security/V1/V2 records byte-for-byte against the
verified checkpoint. No newer conflicting work. Selected only the recorded next action:
**active local-bare object-transfer interruption hardening**. No repeated implementation,
new transport, lock framework, quota investigation or unrelated repository operation.

The uncovered boundary was the existing bare-side fetch, while new objects are arriving but
before the adapter dispatches its approved remote update-ref. Real Git exercises that boundary
through a fixture-only upload-pack stream gate. Existing runtime satisfied the new assertions;
**no runtime edits or demonstrated runtime defect**. This is verified acceptance work.

## CAPACITY

Included-capacity percentage **UNKNOWN**. No supported current signal or human percentage
provided; no estimate, extrapolation or inference from purchased credits. Live quota reads
zero. The <=20% preservation trigger has **NOT** activated. Work is bounded to this block,
validation, normal publication, independent verification and STOP.

## COMPLETE

- Five new offline tests and one test-only helper exercise real fetch/upload-pack/unpack-objects
  in disposable Linux-native repositories. Twelve deterministic 128 KiB text files keep a real
  pack larger than the 256 KiB stream gate. New complete loose objects must actually exist
  while the receiver and pipeline remain alive; no synthetic object/packet/result stand-in.
- Gate-release control completes the identical real stream and verifies normal publication,
  proving the fixture is a working transfer, not a deliberately invalid stream.
- SIGINT/SIGTERM cancel the CGC caller during object arrival through the accepted signal scope.
  Fetch-child SIGKILL with live descendants and command timeout exercise existing group cleanup.
  The fixture uses a four-second command bound; production remains five seconds.
- Exactly one transfer and zero update-ref calls in interrupted cases. Bare ref and non-object
  file bytes unchanged; complete source file/directory byte/mode/size/mtime snapshots unchanged,
  including HEAD, tracking, index and worktree. No ref recreation or automatic retry.
- Unreferenced valid objects demonstrably arrive without publication. Existing object bytes and
  new complete objects survive; subsequent read-only reconciliation/authority refusal leaves
  every retained object-store file intact, including any temporary fragments.
- Previous good handoff and pending PUBLISHING local receipt survive. Signals persist CANCELLED;
  timeout persists generic VERIFICATION_FAILED. Return remains PUBLICATION_UNCERTAIN /
  LOCAL_CHECKPOINT_ONLY, with null remote/tracking receipts, false ref_update_succeeded and
  SAFE_TO_RESUME UNKNOWN. Fresh-process handoff-status exactly reconstructs that state.
- Narrow new concurrency proof: after direct fetch death but before descendant cleanup, a
  competing publisher with another store still receives WRITER_BUSY, with no new store or
  mutation. This is a transfer-specific dead-child/live-descendant interval, not duplicated
  active-ref writer-exclusion coverage.
- Production runner reaps the direct fetch child and kills its group. Sampled transfer
  descendants share that group and terminate. The test worker is a temporary Linux subreaper
  solely to reap orphaned fixture grandchildren, without masking surviving processes by killing
  them before assertions. Both CGC locks can be acquired after cleanup.
- Fresh read-only Git ls-remote independently confirms the old tip. Missing current publication
  approval still refuses despite saved intent/objects. No automatic second publication or repair.

## PARTIAL

Full V3, broader crash safety and end-to-end safe resume remain PARTIAL. This acceptance covers
actively receiving loose objects, not large-pack index-pack fragments or every transfer byte
boundary. In-command add/commit interruption, CGC-parent SIGKILL with live descendants,
different-source publishers sharing a remote and full fresh-process Git/test reconciliation
remain unproven. Existing accepted ref-transaction and checkpoint boundary tests are unchanged.

## NOT_STARTED

HTTPS/SSH/general Git-push transport; valuable real-target publication; automatic retry,
GC, lock deletion or repair; preserve CLI; project test runner; full resume engine; Guardian
autonomous authority; background/automatic publication; Agent Fabric/Gateway/Control/Data Plane/
Router/Event Bus runtime; CWM/HHS/ARX or local/cloud AI integration; GUI/mobile/V4.

## TESTS PASSED

Historical checkpoint: 65 focused tests in 18.920s and 287 full tests in 39.522s; zero failures,
errors or skips. Retained as historical evidence, not rerun as an unchanged baseline.

Current development:

```text
TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_transfer_interruption -v
Ran 5 tests in 12.459s — OK

TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_transfer_interruption test_mutation_interruption test_checkpoint test_publication -q
Ran 70 tests in 31.680s — OK
```

The integrated run includes final dead-child concurrency and retained-object-file assertions.
Relevant V3 and final full regression:

```text
TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_preservation test_inspection test_handoff test_checkpoint test_publication test_mutation_interruption test_transfer_interruption -q
Ran 139 tests in 36.944s — OK

TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -q
Ran 292 tests in 53.000s — OK
```

**All runs: zero failures, errors or skips.** All 287 inherited tests and all runtime files
unchanged. Full regression ran once; no runtime/test edits after that final verification.

Static/documentation checks passed: 33 Python ASTs, three JSON files, 150 local Markdown
file/anchor links and all 100 mission keypoints. All 57 tracked/new project files screened;
only the two known synthetic credential-URL fixtures in test_handoff.py and test_inspection.py
matched. No real credential finding; pattern screening cannot prove universal absence.
Expected CGC fetch/push destination verified without printing authentication data. Whitespace
checks passed. Exact new source/test content and documentation diff reviewed before staging.

## TESTS REMAINING

In-command local checkpoint staging/commit interruption; large-pack/index-pack interruption;
abrupt CGC-parent death while Git descendants remain active; different-source concurrency;
full fresh-process Git/test/intent reconciliation. No live quota read required. Do not generalize
this fixture's group termination/direct-child reaping to cleanup after CGC-parent SIGKILL.

## IMPORTANT DISCOVERIES

Killing fetch alone does not ensure EOF: a live upload/receiving pipeline can retain its pipes.
In this controlled fixture, the runner reports TIMEOUT rather than GIT_FAILED and then kills
the process group. The source lock remains held during that interval. This is truthful bounded
failure, not a demonstrated bug or reason to redesign error codes/transport.

Object presence is not ref publication. Ref publication is not verification. Verification is
not safe resume. Durable pending intent remains useful uncertainty, not proof of remote success
or permission to retry. Observational reconstruction reduces recovery guesswork without adding
automation, telemetry or a new reconciliation subsystem.

## KNOWN FAILURES / LIMITATIONS

No observed deterministic failure in this block. Linux-native /tmp fixtures only. The test
helper adds a fixture-only --upload-pack wrapper and subreaper; neither exists in production.
No universal Git-version/filesystem, decompressed-memory or power-loss guarantee.

SIGKILL of the CGC parent cannot execute handlers; descendants may survive and continue writing
after its process-owned flock releases. No parent-death safety claim. Existing quiescent path/
configuration, same-user race, alias and ownership restrictions remain. Native Windows or
Windows-mounted permission enforcement is not relaxed. No hard bound on blocking syscalls.

Graceful cleanup can leave unreferenced objects or temporary object files. No automatic GC,
lock deletion, rollback or retry. Known Git lock refusal from the previous block is unchanged.
Storage failure can leave only prior intent instead of a durable latest-failure record.
Current approval of project/destination/reachable history remains required for any later write.

## FILES CREATED / MODIFIED

Created: `tests/test_transfer_interruption.py`, `tests/helpers/transfer_peer.py`.
Modified: `AGENTS.md`, `README.md`, `docs/V3_PROGRESS.md`, `docs/V3_CONTRACT.md`,
`docs/V3_ACCEPTANCE.md`, `tests/README.md`.
All runtime, existing tests, schemas, V1/V2 records and mission texts unchanged. No architecture
or new capability introduced, so unrelated decision/architecture documents are not edited.

## DO_NOT_REPEAT

Do not repeat accepted publication/checkpoint implementation, signal/ref-transaction coverage
or this loose-object transfer suite without defect evidence. No live quota discovery, credential
access, automatic retry/repair/GC/lock deletion, blind staging, force push, reset/clean, unrelated
repository checks or Fabric/V4 work. Do not interpret saved intent, object presence, command exit,
purchased-credit balance or historical percentages as current authority/publication/capacity.

## NEXT_EXACT_ACTION

After verified publication, STOP this session. Next coherent scoped block: **audit and test
in-command local checkpoint commit interruption using real Git in disposable Linux fixtures**,
starting from the accepted dispatch/return boundary coverage. Determine the smallest missing
active commit boundary before changing runtime; preserve index/work/HEAD and durable uncertainty.
Do not expand into automatic recovery, general network transport, full resume or automation.

## LAST SAFE CHECKPOINT

Starting verified checkpoint: `4ef724adfb06485ec069bbaffd32803a62b794ca`.
Current acceptance implementation checkpoint: **HEAD after normal commit/publication**.
Its resolved hash and actual publication result are recorded in the final report/evidence
follow-up. No self-containing hash is invented. Earlier detailed evidence remains in Git history.

## PUBLICATION STATE

Entry local/tracking/live equality verified. Current block publication awaits final validation,
normal forward commit/push and independent ref equality. No remote claim for uncommitted work.

## OPERATIONS / INTEGRITY

Session live quota reads **0**; V3 **0**; V2 **0**; historical V1 **1**. No /status value.
Target network operations **0**. All target mutations are disposable Linux /tmp fixtures.
Processes and test directories cleaned by fixture teardown; no object/lock cleanup in runtime.
CGC-only network: entry live ref check and authorized normal final push/verification.
No dependencies, services, persistent system/environment/security changes, authentication
access, environment dumps, default cache creation, or unrelated repository inspection/mutation.
The subreaper setting exists only in disposable test worker processes and ends with them.
