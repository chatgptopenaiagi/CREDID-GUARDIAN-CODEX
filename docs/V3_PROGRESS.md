# CREDID GUARDIAN CODEX — CGC V3 progress

## OVERALL STATUS

**PARTIAL.** Attempt, inspection, durable handoff, manual checkpoint, local-bare publication
and independent verification remain accepted. Scoped ref-transaction, loose-object, commit,
index-pack and current **real active git add index-replacement interruption acceptance are
COMPLETE / VERIFIED OFFLINE**. Broader crash safety and full safe resume remain PARTIAL.
Network publication, automation and Agent Fabric remain NOT_STARTED. V4 remains ARCHITECTED /
runtime NOT_STARTED and parked; its mission is unchanged. V1/V2 remain accepted and unchanged.
The [V3 mission](V3_MISSION.md), all 100 architectural keypoints and current instructions govern.

THE GUARDIAN OBSERVES. CODEX PRESERVES. PRESERVE BEFORE EXPANDING.

## CURRENT SESSION BLOCK

Verified root, clean main, empty diff/whitespace and recent history. Independent reads proved
HEAD = origin/main = live remote main = `35e1e5f8c683d23d4a8a3d294a5e95f4ec215ed8`.
Preceding pack acceptance implementation: `cf804e34e45e6d3728185468f9746cac3c349f53`.
Reconciled all 14 authoritative records against the exact versions read in preceding tasks;
reviewed checkpoint staging, runner, signals, handoff/publication and prior interruption evidence.
The recorded frontier still applied. No accepted block or V4 documentation was reverted.

Selected only **real active git add interruption at the staging/index replacement boundary**.
Checkpoint uses one literal git add for all reviewed paths, including deletions, not git rm.
Installed Git 2.55.0 imports libc rename; installed cc is available, strace is unavailable.
A disposable probe with a fixture-only loader shim observed old index + complete 118-byte lock
before rename and new index + no lock afterward. Released probes both staged successfully.
That size describes the small probe, not an index-size contract.

## CAPACITY

Human-reported planning-time **weekly shared included capacity: 92% remaining**. This is historical
human evidence, not a continuously observed current value. Current weekly/5-hour percentages are
UNKNOWN; no extrapolation, purchased-credit inference, account scrape or credential access.
Capacity preservation threshold activated: **NO**. Session live quota reads: **0**.

## COMPLETE

- Ten new tests use real Git add, index and staging in disposable Linux /tmp repositories.
  Three selected changes cover modification, addition and deletion; unrelated tracked changes
  and untracked human work remain outside selection.
- A test-only C shared library gates the exact fixture index.lock → index rename before the
  real call or after its successful completion. The PID/group must match live git add. No fake
  index bytes, command result, staging command or successful rename. No production override.
- Eight interrupted cases cover SIGINT/SIGTERM to CGC, timeout and direct Git add SIGKILL at
  both gates. Signals return CANCELLED; timeout TIMEOUT; child death GIT_FAILED. Exactly one
  add, zero commit dispatches; staging_attempted=true, commit_attempted=false, local_commit=null.
- Before rename: old index bytes/entries unchanged; lock contains the complete intended index.
  After rename: complete new intended index installed; lock absent. No partially installed
  subset observed at these two stages. All selected changes and unselected entries compared.
- Interrupted result stays PARTIAL, publication NOT_REQUESTED and SAFE_TO_RESUME UNKNOWN.
  HEAD remains old, all worktree file bytes/modes/sizes/mtimes and config bytes remain unchanged.
  Reviewed deletion stays absent; unrelated tracked modifications and untracked human files survive.
- Retained index.lock bytes are preserved; no index replacement/rollback/deletion, re-stage,
  automatic cleanup or retry. A later explicit checkpoint refuses GIT_LOCK_PRESENT before
  replacement or EXISTING_STAGING afterward, without changing state or overwriting the handoff.
- Previous good continuity survives beside CHECKPOINTING intent with selected paths, known
  failures and NEXT_EXACT_ACTION. Latest failure records CANCELLED or VERIFICATION_FAILED.
  Fresh-process handoff-status returns identical state; fresh Git HEAD/status/index reads
  establish actual staging independently of the interrupted adapter result.
- Competing checkpoint using a different store receives WRITER_BUSY at both active stages;
  no staging or contender store creation. Dirty source already excludes publication, so no
  redundant publication contender is claimed as new lock proof.
- Existing runner kills the group, reaps the direct child and releases both CGC writer locks;
  tests reacquire them and check restored previous signal handlers. No SIGKILL handler claim.
- Two released controls finish real staging and verified single-parent local checkpoints while
  preserving unrelated work. No runtime defect or runtime/schema/signal/locking change required.

## PARTIAL

Overall V3 and broader crash/reconciliation acceptance remain PARTIAL. The gates prove old versus
complete new index installation, not earlier partial index writes, every internal instruction,
arbitrary index formats/Git versions/filesystems, power loss or CGC-parent SIGKILL cleanup.
The shim requires Linux dynamic loading, the observed libc rename path and installed cc.
It is a test artifact, not a portable production dependency or acceptance of loader overrides.

Current pending handoff records selected paths but NOT the reviewed SHA256 mapping supplied by
the caller. That mapping is current-call input, not durable authority. Observable lock/index blob
IDs and retained work survive here; full intent/review reconstruction remains a reconciliation
requirement. Do not claim saved digests or silently infer approval on a new invocation.

## NOT_STARTED

Full fresh-process Git/test/intent reconciliation, resume engine, project test runner, Guardian
integration/automation, preserve CLI, general HTTPS/SSH/Git-push transport and valuable target
publication. No automatic rollback, lock deletion, re-stage, repair, retry or telemetry.
V4 protocol/capsule/MCP/plugin/SDK/Rust core/desktop/web/mobile/gateway and Agent Fabric runtime
remain NOT_STARTED. No unrelated project inspected or modified.

## TESTS PASSED / DEVELOPMENT FAILURES

Historical baseline: 308 passed in 85.581s; not rerun as a baseline.
Two disposable before/after-rename probes completed normally before the acceptance tests.

```text
TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_add_interruption -q
Ran 10 tests in 14.247s — OK

TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_add_interruption test_checkpoint test_commit_interruption test_mutation_interruption -q
Ran 60 tests in 42.358s — OK
```

Relevant V3:

```text
TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_preservation test_inspection test_handoff test_checkpoint test_publication test_mutation_interruption test_transfer_interruption test_commit_interruption test_pack_interruption test_add_interruption -q
Ran 165 tests in 87.694s — OK
```

Full deterministic regression, once before publication:

```text
TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -q
Ran 318 tests in 107.522s — OK
```

**All runs passed with zero failures, errors or skips.** No development failure observed.
Full regression ran once; no test/runtime changes followed verification. C shim compiles with
-shared -fPIC -Wall -Wextra -Werror -ldl; generated library stays in private /tmp and is removed
by test cleanup. No binary is committed or installed. Runtime and inherited tests/helpers unchanged.

Static/documentation checks passed: 38 Python ASTs, three JSON files, 179 local Markdown
file/anchor links, all 100 V3 keypoints and unchanged V4 mission/boundary. Nine-file scope
confirmed; 55 other tracked files are byte-identical, including all runtime, inherited tests/
helpers and schemas. All 64 tracked/new files screened; only two known unchanged synthetic
credential-URL fixtures matched in test_handoff.py and test_inspection.py. No real credential
finding; pattern screening does not prove universal absence. Exact new helpers/test and
documentation diff/status reviewed; staged whitespace passed. Approved CGC fetch/push
destination verified without credential output.

## IMPORTANT DISCOVERIES

An active add process can already have installed the complete new index while CGC has no successful
staging completion. Staging is not a checkpoint, and Git index installation cannot manufacture a
local_commit receipt. Conversely, before replacement, the old index and complete candidate lock
coexist. CGC graceful cancellation kills Git; Git cannot run its own lock cleanup after SIGKILL.
Keeping the lock and refusing a later attempt preserves evidence rather than hiding uncertainty.
No partial subset was observed; do not extrapolate these gates to every interrupted write.

## KNOWN FAILURES / LIMITATIONS

No unresolved deterministic failure. Static Git/alternate loaders/native Windows are outside
this fixture; unsupported environments are not silently skipped. Git may close index.lock before
rename, so existence is not represented as proof of an open descriptor. The synchronized boundary
is the real rename call, not a timing guess or a dispatch/return wrapper around git add.
Test timeout is four seconds; production remains five. No hard syscall/RSS or power-loss bound.
Owner-controlled/quiescent target assumptions remain; hostile same-user races are not solved.
Storage failure can prevent fresh failure persistence; earlier intent must remain truthful.
CGC-parent SIGKILL cannot run cleanup; active children may outlive it and its writer lock.

## TESTS REMAINING / FRONTIER ASSESSMENT

This staged-index replacement block is COMPLETE. Broader crash hardening remains **PARTIAL**.
One material practical gap remains before broad fresh-process reconciliation: abrupt death of
CGC itself can release source flock while its Git child is alive. Existing child-death/cancellation
proof does not establish what a replacement caller can safely observe or refuse in that interval.
Audit that one boundary next. Do not promise impossible SIGKILL cleanup or add an unbounded list
of timing experiments. Other internal-write, later-pack, cross-source and power-loss limitations
remain scoped limitations requiring future acceptance decisions, not automatic next features.

## FILES CREATED / MODIFIED

Created: tests/test_add_interruption.py, tests/helpers/add_peer.py, tests/helpers/add_gate.c.
Modified: README.md, AGENTS.md, docs/V3_PROGRESS.md, docs/V3_CONTRACT.md,
docs/V3_ACCEPTANCE.md, tests/README.md.
Runtime, inherited tests/helpers, schemas, V1/V2 records and V3/V4 missions unchanged.
No runtime design revision requires an architecture/decision journal change.

## DO_NOT_REPEAT

Do not redo accepted ref/loose-transfer/commit/pack or these real add replacement cases without
defect evidence. Do not infer partial staging, lock absence, successful checkpoint or safe resume
from a subprocess attempt. No live quota discovery, credentials, automatic rollback/cleanup/
lock deletion/re-stage/retry, force push, reset/clean, unrelated repository changes or V4 runtime.
Do not treat selected paths in saved intent as persisted reviewed digests or renewed authority.

## NEXT_EXACT_ACTION

After verified publication, STOP. Next scoped block: **audit and test abrupt CGC-parent death
while a real Git mutation child remains active, including fresh-invocation refusal evidence**.
Observe child/process-group, Git/source locks and durable intent under disposable Linux fixtures;
do not assume SIGKILL cleanup or automatically delete retained artifacts. Determine the bounded
reconciliation boundary before expanding recovery. Do not begin the full resume engine or V4.
Reconcile newer repository evidence before acting.

## LAST SAFE CHECKPOINT

Starting verified checkpoint: `35e1e5f8c683d23d4a8a3d294a5e95f4ec215ed8`.
Previous implementation: `cf804e34e45e6d3728185468f9746cac3c349f53`.
Acceptance implementation: `dd02dd81cf92d5e4436f759b1cf55d17cdb7e08a`.
Final evidence checkpoint: **HEAD after normal commit/publication**; its resolved hash and
independent equality belong in the final report. No self-containing SHA.

## PUBLICATION STATE

Acceptance implementation **REMOTE_VERIFIED** on 2026-09-23. Normal forward push succeeded.
Independent reads established local HEAD = origin/main = live remote main =
`dd02dd81cf92d5e4436f759b1cf55d17cdb7e08a`; working tree clean.

This documentation-only follow-up records that equality and acceptance row 41. Its own HEAD
must be committed/pushed normally and independently verified for the final report. Runtime/tests
remain unchanged from the 318-test result; no redundant regression. Final links and staged
whitespace are checked. If publication fails, retain the local evidence commit and report
LOCAL_CHECKPOINT_ONLY; never invent remote equality.

## OPERATIONS / INTEGRITY

No quota reads, credentials, account scraping, default cache, dependency installation, service,
registry or persistent system/environment changes. Installed cc compiles only temporary fixture
libraries; LD_PRELOAD is passed only to each test's real Git add process. Tests remove owned
/tmp fixtures after integrity/artifact assertions. No unrelated project touched. Only network
operations are CGC's entry ref check and authorized normal publication/independent verification.
