# CREDID GUARDIAN CODEX — CGC V3 progress

## OVERALL STATUS

**PARTIAL.** Attempt, bounded inspection, durable handoff, manual checkpoint, local-bare
publication and independent verification remain accepted. Signal/ref-transaction, loose-object
transfer, real active commit pre/post-acceptance and current **active index-pack interruption
after temporary pack arrival are COMPLETE / VERIFIED OFFLINE within their scoped contracts**.
Broader crash safety and full safe resume remain PARTIAL. Network publication, automation and
Agent Fabric remain NOT_STARTED. V4 is ARCHITECTED / runtime NOT_STARTED and parked.
The [complete mission](V3_MISSION.md), all 100 architectural keypoints and current user
instructions remain authoritative. V1/V2 and [V4 mission](V4_MISSION.md) are unchanged.

THE GUARDIAN OBSERVES. CODEX PRESERVES. PRESERVE BEFORE EXPANDING.

## CURRENT SESSION BLOCK

Verified root, clean main, empty diff/whitespace, recent history and independent live remote.
Entry HEAD = origin/main = live refs/heads/main =
`4543a3739f09647bd54c45b2334f7937c6712dae` (V4 architecture documentation).
Last completed V3 evidence checkpoint: `fd1dbcabf10a748e0160f78f9311ae948a9a8260`;
its implementation is `1bc957dffb8ffd034289dea1415b92c5fbdcad83`. V4 was not reverted.

Reconciled all 14 authoritative documents with the exact versions read in the preceding task;
inspected publication/checkpoint/runner/signals/handoff and accepted interruption fixtures.
Recorded frontier still applied: **active local-bare index-pack interruption after temporary
pack arrival**. Earlier accepted coverage was neither duplicated as inherited test discovery
nor redesigned. Runtime, prior tests/helpers and schemas remain unchanged.

Before new tests, a disposable probe reused the real transfer gate with 128 additional small
blobs. Git 2.55.0 actually ran fetch → upload-pack/pack-objects → index-pack --stdin. At the gate,
a temporary pack contained 196544 bytes with PACK v2 header/count 147; remote tip remained old.
Released stream completed VERIFIED with final .pack/.idx/.rev files. Those exact size/count
observations describe the probe, not universal file-size or Git-version guarantees.

## CAPACITY

Included-capacity percentage **UNKNOWN**. No reliable current source or human percentage;
no estimated/extrapolated value, purchased-credit inference or account investigation.
Capacity preservation threshold activated: **NO**. No live quota read consumed.

## COMPLETE

- Six new tests in test_pack_interruption.py reuse the existing real-stream helper unchanged.
  Twelve large text blobs plus 128 small distinct blobs select index-pack without config overrides.
- The gate requires real active index-pack, a nonempty temporary PACK v2 file, count over 100,
  and an open receiver descriptor to that exact file. No final .pack/.idx or ref movement yet.
- SIGINT/SIGTERM to CGC return CANCELLED. Timeout, fetch SIGKILL and index-pack SIGKILL return
  TIMEOUT in this gated fixture because remaining pipeline processes retain pipes until cleanup.
  Production five-second command bound is unchanged; test helper uses four seconds.
- All interrupted cases dispatch one transfer, zero update-ref commands. PUBLICATION_UNCERTAIN /
  LOCAL_CHECKPOINT_ONLY, known local checkpoint, null remote/tracking receipts,
  ref_update_succeeded=false and SAFE_TO_RESUME=UNKNOWN remain truthful.
- Full source byte/mode/size/mtime snapshots match, including HEAD/tracking/index/config/worktree;
  all remote non-object bytes and old object bytes survive. Source must be clean under current
  publication rules; untracked-source mutation support is not claimed.
- Temporary pack survives with observed prefix intact; no final pack/index appears. No rollback,
  fragment deletion, GC/prune, repair, automatic retry, ref recreation or inferred publication.
- Previous good handoff survives beside pending PUBLISHING/local receipt. Latest failure is
  CANCELLED or VERIFICATION_FAILED; known failures and NEXT_EXACT_ACTION survive unchanged.
  Fresh-process handoff-status JSON equals saved state; fresh ls-remote confirms old remote tip.
- A later no-authority request refuses before mutation, preserving every object-store file,
  source snapshot, remote metadata and durable handoff. Historical intent grants no new authority.
- After either fetch or receiver death, a competing publisher with a different store receives
  WRITER_BUSY while the pipeline still holds pipes. No contender store/handoff/ref mutation.
- Existing runner reaps direct fetch and kills its group; sampled descendants terminate and both
  CGC locks reacquire. Existing fixture-only subreaper collects orphaned descendants without
  killing survivors before assertions. No runtime descendant-reaping guarantee is invented.
- Gate-release control completes real receiving/indexing, verifies the resulting pack with
  verify-pack, performs approved ref/tracking updates and independently reports VERIFIED;
  safe resume remains UNKNOWN. No runtime defect or change was necessary.

## PARTIAL

Overall V3, broader mutation/crash acceptance and evidence-based safe resume remain PARTIAL.
This proves temporary-pack arrival with receiving index-pack active, not every completed-pack,
index-finalization, delta-resolution or filesystem instruction. Active git add/index replacement,
hookless commit mutation syscalls, abrupt CGC-parent descendants and cross-source writers remain
unproven. Do not generalize one Git/Linux fixture to all environments or power-loss durability.

## NOT_STARTED

Full fresh-process Git/test/intent reconciliation and resume engine; project test runner;
Guardian authority integration/automation; general HTTPS/SSH/Git-push transport; valuable target
publication; automatic retry, rollback, GC, cleanup or repair; preserve CLI; Agent Fabric runtime.
V4 protocol/capsule/MCP/plugin/SDK/portable core/desktop/web/mobile/gateway remain NOT_STARTED.
No telemetry, quota reader change, new signal handling or lock framework.

## TESTS PASSED / DEVELOPMENT FAILURES

Historical baseline: 302 passed in 69.620s, not rerun as a baseline.
One disposable real-Git probe completed normally before adding tests.
Initial six new tests: **6 passed in 18.425s**. After adding exact receiver-descriptor ownership
and handling normal receiver reap during death observation, focused result:

```text
TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_pack_interruption -q
Ran 6 tests in 17.974s — OK
```

Publication/interruption integration:

```text
TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_pack_interruption test_publication test_mutation_interruption test_transfer_interruption test_commit_interruption -q
Ran 63 tests in 63.046s — OK
```

Relevant V3 regression:

```text
TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_preservation test_inspection test_handoff test_checkpoint test_publication test_mutation_interruption test_transfer_interruption test_commit_interruption test_pack_interruption -q
Ran 155 tests in 71.725s — OK
```

Full deterministic regression (once before publication):

```text
TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -q
Ran 308 tests in 85.581s — OK
```

**All runs passed with zero failures, errors or skips.** No development test failure observed.
Full regression ran once. Runtime and all 302 inherited tests/helpers are unchanged; no test
code changed after verification. Subsequent edits are documentation evidence only.

Static/documentation checks passed: 36 Python ASTs, three JSON files, 176 local Markdown
file/anchor links, all 100 V3 keypoints and unchanged V4 mission/boundary. Exact seven-file
scope checked; 54 other tracked files are byte-identical, including runtime, inherited tests/
helpers and schemas. All 61 tracked/new files screened; only the two unchanged known synthetic
credential-URL fixtures in test_handoff.py and test_inspection.py matched. No real credential
finding; pattern screening cannot establish universal secret absence. Exact new test and
documentation diff/status/whitespace reviewed. Approved CGC fetch/push destination verified.

## IMPORTANT DISCOVERIES

A pack fragment can outlive a gracefully cancelled CGC call because bounded group cleanup kills
Git without running its own temporary-file handlers. That file is not a remote receipt. Both
fetch death and receiving index-pack death can leave live pipeline processes holding pipes;
source writer authority must remain held until the runner finishes group cleanup. Existing
behavior meets the tested boundary without redesign. Artifact presence alone cannot answer
whether publication happened: read the approved ref and retain durable uncertainty separately.

## KNOWN FAILURES / LIMITATIONS

No known deterministic failure. Read-only evidence and refusal preserve artifacts; this block
neither declares every fragment reusable nor tests an authorized retry/repair protocol.
SIGKILL of CGC itself cannot execute handlers; descendants may continue after flock releases.
Only child death and caller graceful cancellation are exercised. Fixture subreaper is test
hygiene, not a production control. Polling waits for observed state rather than assuming readiness.
No hard syscall/RSS/decompressed-object, hostile same-user path/config race, native-Windows,
arbitrary filesystem/Git-version or power-loss guarantee. Existing quiescent-target rules apply.
Storage failure can prevent a new failure receipt; retain earlier durable intent truthfully.

## TESTS REMAINING / FRONTIER ASSESSMENT

Selected pack-arrival boundary is COMPLETE. Broader crash-hardening frontier is **PARTIAL**.
The existing untested active staging/index replacement boundary is material: git add changes
recoverable staged work before commit begins, so real-commit coverage cannot establish it.
Audit that single next boundary before claiming broad mutation acceptance. Abrupt-parent,
cross-source and later pack/index timing limitations remain explicit, not silently accepted.
Full fresh-process reconciliation remains a subsequent V3 goal; it is not implemented here.

## FILES CREATED / MODIFIED

Created: tests/test_pack_interruption.py.
Modified: README.md, AGENTS.md, docs/V3_PROGRESS.md, docs/V3_CONTRACT.md,
docs/V3_ACCEPTANCE.md, tests/README.md.
All runtime, inherited tests/helpers, schemas, V1/V2 records and V3/V4 mission texts unchanged.
Architecture/decision records need no runtime-design revision for this acceptance-only block.

## DO_NOT_REPEAT

Do not repeat accepted inspection/handoff/checkpoint/publication, ref/loose-transfer/commit or
this pack-arrival implementation/coverage without defect evidence. Do not guess receiving Git
path from size alone, infer publication from objects, or delete artifacts to make state look clean.
No quota discovery, credentials, automatic retry/rollback/repair/lock deletion, force push,
reset/clean, unrelated repository checks, networking, resume engine or V4 runtime work.

## NEXT_EXACT_ACTION

After verified publication, STOP. Next scoped block: **audit and test real active git add
interruption at an observable staging/index-write boundary in disposable Linux Git fixtures**.
Investigate observable Git behavior first, preserve staged/worktree evidence and prior continuity,
and do not extrapolate in-command coverage from dispatch/return mocks. No automatic rollback,
cleanup, resume engine, publication expansion or V4 implementation. Reconcile newer evidence first.

## LAST SAFE CHECKPOINT

Starting repository checkpoint: `4543a3739f09647bd54c45b2334f7937c6712dae`.
Previous V3 engineering evidence: `fd1dbcabf10a748e0160f78f9311ae948a9a8260`.
Current acceptance implementation: **HEAD after normal commit/publication**; resolved hash and
independent remote equality belong in the final report/evidence follow-up. No self-containing SHA.

## PUBLICATION STATE

Entry equality independently verified. Current coherent block is validated and awaits normal
forward commit/push with independent local/tracking/live verification. No remote claim for local
uncommitted work. If push fails, retain the local checkpoint and report the failure truthfully.

## OPERATIONS / INTEGRITY

Capacity UNKNOWN; live quota reads this session 0, V3 0, V2 0, historical V1 1. No auth files,
account scraping, default cache, installs, services or persistent system/environment changes.
All target mutations use disposable Linux /tmp repositories. Existing helper's process-local
subreaper ends with the worker; test teardown removes fixtures only after artifact assertions.
No unrelated project inspected or modified. CGC network use is entry live ref check and authorized
normal checkpoint publication/independent verification. No target network publication.
