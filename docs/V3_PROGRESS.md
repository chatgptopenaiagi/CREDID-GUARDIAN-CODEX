# CREDID GUARDIAN CODEX — CGC V3 progress

## OVERALL STATUS

**PARTIAL.** V3 remains active under the complete [V3 mission](V3_MISSION.md), including
its Agent Fabric / EXACTLY 100 ARCHITECTURAL KEYPOINTS directive. V1/V2 remain accepted.
The current **human + machine handoff persistence block is COMPLETE, VERIFIED OFFLINE**
within the [contract](V3_CONTRACT.md#durable-handoff-persistence). Full project preservation
is not implemented. THE GUARDIAN OBSERVES. CODEX PRESERVES.

## CURRENT SESSION BLOCK

2026-09-22, third continuation: recovered interrupted handoff work, completed and validated
this same block, and prepared its forward publication. Entry main/local HEAD/origin/main/
live remote main all equaled `a33fd3f0930ad65b23e502da9ff64d59eb98e282`. Working tree held
modified V3_MISSION.md and __main__.py plus untracked handoff.py and test_handoff.py.
The old progress record described handoff as NOT_STARTED; surviving code was newer.
Preserved that implementation, all eleven initial tests, CLI dispatch and full user mission
addition. No reset/restart or existing V1/V2/attempt/inspection source rewrite.

Read the complete active mission, all 100 keypoints, required project records and inherited
V2 mission/progress. Historical expected failure reproduced: 11 focused tests, 10 passed,
one failure in 0.524s. The data round-trip succeeded; the human renderer hid lowercase note
keys inside JSON instead of exposing the required uppercase continuity labels. Fixed labels
and deterministic rendering of equivalent mappings without changing the attempt schema.

## COMPLETE

- External HandoffStore with explicit project/store paths, private no-follow storage,
  nonblocking process-lifetime writer flock and atomic canonical handoff.json replacement.
- Versioned validated CONTINUITY_ONLY envelope, monotonic generation/time, latest attempt,
  last-known-good and previous-known-good, inspection/record/project/digest bindings.
- Deterministic JSON and human views from one validated state; required continuity notes,
  test failure state, publication receipts/unknowns and NEXT_EXACT_ACTION survive readback.
- Explicit failure recording preserves good slots; post-replace uncertainty retains the
  preceding good record. Corrupt/unsupported state is never silently migrated/overwritten.
- Distinct unsupported-schema errors, bounded input/output, fixed non-echoing errors,
  recognizable-secret rejection, project symlink-alias refusal before storage creation.
- Read-only handoff-status CLI with explicit --store-dir / --project; fresh-process human
  and JSON reconstruction including a failed latest attempt. Missing store is not created.
- Eighteen handoff tests including eight synchronized seeded/unseeded SIGKILL cases across
  four write stages, cross-process exclusion/release/restart and target non-mutation.
- Small Agent Fabric architecture cross-reference: stable language-neutral continuity state,
  information separate from authority, transport separate from persistence. No runtime fabric.

## PARTIAL

Full V3 preservation remains PARTIAL. Known-good handoff means valid saved continuity, not
verified target preservation. Stored records/receipts are operator-curated or adapter-reported;
outer SAFE_TO_RESUME remains UNKNOWN and automatic_mutation_authorized remains false.
Fresh-process readback is complete; present Git/test reconciliation and verified safe resume
are not. Current test commands/results are bounded inert curated notes, not executed commands
or a structured result-count adapter. [Acceptance](V3_ACCEPTANCE.md) keeps these gaps visible.

## NOT_STARTED

Preservation executor/CLI, project test execution, deliberate staging, target local commits,
target push/remote verification, target-project mutation locking/idempotency, Guardian authority
integration and automatic preservation. Agent Gateway, Capability Model runtime, Control Plane,
Data Plane, Router/Event Bus, networking/tunnels, CWM/HHS/ARX integration, local/cloud AI
orchestration, master orchestrator, resume prompt generation, GUI/mobile/V4 are NOT_STARTED
and NOT_AUTHORIZED in this block. Existing finite V2 observation daemon is unchanged.

## TESTS PASSED

Initial focused reproduction: 11 tests in 0.524s, 10 passed, one failure, zero errors/skips.
Expanded run: 18 tests in 2.553s, 17 passed, one test assertion error (expected ValueError
instead of HandoffError), zero failures/skips. Corrected that new assertion. Intermediate
18/69-test runs passed; final tests additionally check fresh human/failure/schema CLI results.

The first complete regression also passed 222 tests in 19.042s. Final security review then
added project/service-account-prefixed synthetic API-key fixtures to the existing test; a
single-test reproduction failed (1 test in 0.009s, one failure). Expanded the narrow recognizable
pattern and reran focused, V3 and full regression successfully. No real credential was used.

Final focused command:
`TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -p test_handoff.py -q`

```text
Ran 18 tests in 3.278s
OK
```

Final V3 command:
`TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_preservation test_inspection test_handoff -q`

```text
Ran 69 tests in 5.526s
OK
```

Canonical full regression:
`TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -q`

```text
Ran 222 tests in 19.259s
OK
```

Final runs: respectively 18/69/222 passed; **zero failures, errors or skips**.
All prior 204 tests unchanged. Linux /tmp used for POSIX-sensitive fixtures. No live sensor.
Publication gates: 24 Python files parse, three JSON files parse, 131 local Markdown targets
resolve; all 48 repository files screened. Two credential-URL matches are deliberate synthetic
fixtures in tests/test_handoff.py and tests/test_inspection.py, reviewed without real credentials.
No other recognizable pattern findings; not universal proof of secret absence. Exactly 100
numbered architectural keypoints verified. CLI help succeeds, whitespace checks pass, origin
identity is the authorized CGC repository. Final source/docs/diff reviewed; no unrelated files.

## TESTS REMAINING

No observed handoff-block failure remains. Future stages require target staging/secret and
large-file policy tests, real execution receipts, local checkpoint/bare-remote publication,
mutation-stage crashes, fresh Git/test reconciliation and canonical Guardian authority tests.
No live quota read is needed to resume development.

## KNOWN FAILURES / LIMITATIONS

No unresolved observed deterministic failures. Private native POSIX storage required; /mnt/c
mode behavior is not weakened. No universal power-loss guarantee, hostile same-user tamper/
path-race resistance, bind-mount alias detection, hard CPU/RSS/syscall deadlines or encrypted/
authenticated handoff. SHA256 is representation integrity, not proof of claimed actions.
Project paths are requested identity, not independently re-attested on readback. Missing
projects permit historical reads; renames do not automatically rebind a store.

Failed input is not automatically recorded. Call record_failure explicitly when storage is
healthy; a failed disk write/process death cannot promise durable latest-failure metadata.
Canonical state then remains old or new according to the replacement boundary. After-replace
fsync/readback failure is PUBLICATION_UNCERTAIN; prior good slot remains in the new state.
SIGKILL may leave private temporary siblings, ignored rather than deleted; repeated crashes
can accumulate disk usage. No handoff-write SIGINT/SIGTERM adapter is claimed. Pattern scanning
cannot prove arbitrary curated notes are secret-free; users must supply authorized context.

## IMPORTANT DISCOVERIES / ARCHITECTURE

The historical focused failure was human presentation, not a lost state/determinism failure.
A new mapping-order test proved both views now deterministic. Code review found schema errors
were collapsed into corruption and project symlink aliases could evade lexical storage overlap;
fixed both and added regression evidence. Also closed the reproduced prefixed API-key
screening gap with synthetic fixtures. Existing private Cache locking/I/O substrate reused
without changing V2. Two retained slots allow post-replace uncertainty to preserve older evidence.

All 100 keypoints were read as constraints, not feature authorization. Durable continuity now
supports future fresh-process consumers and bounded resume generation independent of transport.
A future generator must reconcile Git/tests, mission/version boundaries, preservation/publication
state and last-known-good before using NEXT_EXACT_ACTION. Information is not authorization.
Future Control Plane decides scoped capabilities; Data Plane transports authorized data; events
report facts; private context stays local and cloud context requires authorization. Those layers
are architecture only. See [architecture](ARCHITECTURE.md#agent-fabric-relationship).

## NON-MUTATION / SECRET SAFETY EVIDENCE

Bound inspection + handoff fixture compares every regular target file's SHA256, mode, size and
mtime including Git metadata before/after success and rejected candidates; unchanged. Storage
overlap and project/storage alias tests refuse before creating target children. No target
staging/commit/push or project instruction execution is implemented. Synthetic secret-note
fixtures are rejected without echo/write; fixed allowlists and size/schema checks fail closed.
No private source content collected. Real credential stores and unrelated repositories untouched.

## FILES CREATED / MODIFIED

Recovered/created: src/cgc/handoff.py, tests/test_handoff.py.
Modified: src/cgc/__main__.py; README.md; AGENTS.md; docs/V3_CONTRACT.md;
docs/V3_PROGRESS.md; docs/V3_ACCEPTANCE.md; docs/ARCHITECTURE.md; docs/DATA_MODEL.md;
docs/PRESERVATION_POLICY.md; docs/SECURITY_MODEL.md; docs/ROADMAP.md; docs/DECISIONS.md;
tests/README.md. The pre-existing user addition to docs/V3_MISSION.md is preserved unchanged.
V1/V2 runtime (except additive CLI dispatch), all prior tests, attempt/inspection code and V2
records remain unchanged. No dependencies added.

## DO_NOT_REPEAT

Do not redo accepted foundation/inspection/handoff blocks absent demonstrated defects. Do not
repeat live quota reads, scan credentials/unrelated projects, weaken POSIX permissions, infer
mutation authority from a saved record, blindly stage, force-push or implement Agent Fabric/V4.
Do not treat handoff.json, successful CLI exit, synthetic receipts or a saved next action as
proof of current Git/test reality, safe-to-close status or permission to act.

## NEXT_EXACT_ACTION

Start a new scoped session by reconciling Git/source/tests/mission/progress and publication.
The next V3 implementation candidate is **deliberate local checkpointing in disposable Linux
Git fixtures**: define explicit current target authority, staging/secret/large-file policy,
fresh prechecks, target writer exclusion and checkpoint receipts; then prove forward-only
local commits and truthful failures against handoff continuity. No target mutation is authorized
by this record alone; the current directive ends at handoff publication. Obtain the next scoped
user directive before implementing that block. Do not start target push, automation, Fabric or
resume generator as an incidental extension. STOP after this session's verified checkpoint.

## LAST SAFE CHECKPOINT

Entry published checkpoint: `a33fd3f0930ad65b23e502da9ff64d59eb98e282`.
Handoff implementation checkpoint: **HEAD after normal commit/publication**; resolved SHA and
local/tracking/live equality reported after operations. No invented self-containing hash.

## PUBLICATION STATE

Entry main/local/tracking/live equality verified. Current block publication is PENDING until
normal commit/push and independent live-ref comparison complete. A subsequent evidence entry
records the actual result. Preserve local checkpoint if remote publication fails.

## OPERATIONS / INTEGRITY

Session live quota reads 0; V3 0; V2 0; historical V1 1. No quota monitoring or observed threshold
crossing. Target live remote operations 0. CGC-only live ref checks and authorized forward Git
publication; exact publication results follow. Temporary /tmp fixtures/processes cleaned by tests.
No dependency installation, authentication access, default cache creation, persistent environment/
system/security changes, services, unrelated project mutation or background monitoring.
