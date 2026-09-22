# CREDID GUARDIAN CODEX — CGC V3 acceptance

Overall: **PARTIAL**. Attempt, inspection and external handoff persistence complete within their offline contracts; scoped manual local checkpointing is verified; full preservation/resume remains pending. This matrix preserves all 43
implementation checks mapped to [V3 mission](V3_MISSION.md) sections 2 and 3.
The 43-row decomposition is retained from the prior handoff; these are not numbered
criteria in the current mission. Its full requirements remain authoritative. Current session
evidence: [contract](V3_CONTRACT.md), [attempt tests](../tests/test_preservation.py), [inspection tests](../tests/test_inspection.py), [handoff tests](../tests/test_handoff.py), and
[progress](V3_PROGRESS.md). COMPLETE rows describe this checkpoint's evidence, not a
claim that future external-effect implementations already satisfy them.

| # | Criterion | Status | Evidence / remaining work |
|---|---|---|---|
| 1 | V1 tests remain passing. | COMPLETE | Inherited 32 V1 tests unchanged. |
| 2 | V2 tests remain passing. | COMPLETE | All 153 inherited V1/V2 tests unchanged and passing. |
| 3 | V3 preservation schema exists and is validated. | COMPLETE | Three explicit provisional validated schemas: attempt, inspection and durable handoff. Future evolution remains deliberate. |
| 4 | Explicit project targeting works. | COMPLETE | Explicit inspect --project required; exact root only. test_explicit_root_only_and_safe_failures and CLI tests. |
| 5 | Project root validation works. | COMPLETE | Owned no-follow root, metadata and device/mode boundaries; unsafe/unsupported layouts refused. Scoped Linux contract, not universal Git-layout support. |
| 6 | Non-mutating project snapshot works. | COMPLETE | Bounded local collector; clean/dirty/rename/conflict/upstream/index flags and repeated observation tests. Full fixture byte/metadata comparisons. |
| 7 | Manual preservation works. | PARTIAL | Manual Python checkpoint adapter works without quota in disposable fixtures; full preserve CLI/test/resume workflow pending. |
| 8 | Human handoff works. | COMPLETE | Human handoff renders validated persisted state, with quoted uppercase continuity fields; fresh-process output equality tested. |
| 9 | Machine-readable handoff works. | COMPLETE | Versioned canonical handoff.json; fresh-process JSON readback and unsupported schema refusal tested. |
| 10 | COMPLETE/PARTIAL/NOT_STARTED are preserved. | COMPLETE | Curated complete/partial/not_started persist in the validated attempt inside the handoff. |
| 11 | NEXT_EXACT_ACTION is preserved. | COMPLETE | notes.next_exact_action survives disk and fresh-process reconstruction; no execution implied. |
| 12 | Known failures are preserved. | COMPLETE | Known failures retained with failed test state through publication, failure and recovery. |
| 13 | Relevant tests/results are preserved. | PARTIAL | Curated test status/command/results persist; automatic test selection/execution and structured result counts remain future adapters. |
| 14 | Last-known-good preservation is retained. | PARTIAL | Continuity latest failure preserves both good slots; post-replace uncertainty retains previous. Target preservation not implemented. |
| 15 | Local checkpoint behavior is correct. | COMPLETE | Scoped adapter verifies exact staged tree, branch and single expected parent; test_checkpoint. Full workflow remains partial. |
| 16 | Git staging is bounded and deliberate. | COMPLETE | Explicit reviewed paths/digests; literal staging; full index comparison; existing staging refused; subset/ignored/rename/deletion tests. |
| 17 | Secret-risk protections exist. | PARTIAL | Handoff and selected-content screening, sensitive/generated path refusal, UTF-8/size bounds and no-follow reads tested. No universal detector or history audit. |
| 18 | Destructive Git actions are absent. | COMPLETE | Mutation adapter uses deliberate add, write-tree and normal commit only. No reset/clean/restore/stash/rebase/force push or rollback. |
| 19 | Forward-only normal commit behavior works. | COMPLETE | New HEAD/tree/branch and exactly one expected parent independently read after normal commit; no empty/repeated commits. |
| 20 | Local bare-remote publication works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 21 | Push failure is truthful. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 22 | Remote verification works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 23 | LOCAL_CHECKPOINT_ONLY works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 24 | Project writer exclusion works. | PARTIAL | Project-level private persistent flock excludes CGC peers across stores; four killed-writer stages release it. Noncooperating writers not excluded; future publication stages pending. |
| 25 | Crash/interruption tests pass. | PARTIAL | Inherited inspection/handoff crashes plus four synchronized checkpoint SIGKILL boundaries and pre/post-commit injected failures. In-command mutation signals/transactions pending. |
| 26 | Atomic canonical preservation state works. | PARTIAL | Atomic canonical handoff tested with live readers and killed writers; target preservation transaction pending. |
| 27 | Repeated invocation is safe/idempotent where applicable. | PARTIAL | Stale expected HEAD, unchanged selection and existing staging refuse repeat mutation. No automatic rollback/retry; interrupted-commit reconciliation remains manual. |
| 28 | SAFE_TO_RESUME semantics are evidence-based. | PARTIAL | Outer handoff UNKNOWN/false never upgrades curated attempt receipts. End-to-end external verification pending. |
| 29 | Resume from a fresh CGC process works. | PARTIAL | Fresh process reconstructs validated human/JSON handoff including latest failure; Git/test reconciliation and safe resume execution pending. |
| 30 | Manual preservation is independent from live quota availability. | PARTIAL | Explicit MANUAL local-checkpoint adapter independent of quota; full preservation/resume workflow pending. |
| 31 | Synthetic Guardian policy integration works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 32 | UNKNOWN Guardian state cannot authorize automatic mutation. | PARTIAL | All automatic triggers denied in Phase A; Guardian integration pending. |
| 33 | Automatic preservation consumes canonical V2 policy only. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 34 | Resource bounds are tested. | PARTIAL | Inherited bounds plus 64 explicit paths, 1 MiB/file, 4 MiB selected text and bounded Git commands; no hard RSS/syscall guarantee. |
| 35 | Security/path tests pass. | PARTIAL | Checkpoint aliases/locks/hooks/config/attributes/index/content/authority refusals tested; broader publication security remains pending. |
| 36 | No unrelated project was modified. | COMPLETE | Only CGC development files and disposable Linux test repositories changed; no valuable external target mutated. |
| 37 | No V1/V2 semantics were weakened. | COMPLETE | Inherited runtime/tests and V2 records unchanged. |
| 38 | No secret material was intentionally committed. | COMPLETE | Development publication scan; no secret input used. Not universal proof. |
| 39 | Documentation is complete. | PARTIAL | Mission/contract/progress preserved; later implementation docs pending. |
| 40 | Canonical deterministic test command passes. | COMPLETE | 245 tests (153 V1/V2 + 22 attempt + 29 inspection + 18 handoff + 23 checkpoint); exact final result in progress. |
| 41 | Git publication of CGC V3 itself is verified. | COMPLETE | Entry d0c320fb9e4b722f3bfcaca10094c8a71a58c3c6 local/tracking/live equality verified. This block HEAD is published/verified after validation; exact result in final report. |
| 42 | The final V3 checkpoint is resumable. | PARTIAL | Development handoff and runtime fresh-process continuity readback exist; complete V3 safe-resume workflow pending. |
| 43 | V4 or cloud work has not begun without authorization. | COMPLETE | No V4/cloud/GUI/ARX implementation. |


Inspection, handoff and manual local checkpoints have run only with disposable synthetic
Linux fixtures. No target push, project test execution, Guardian automation or resume generator
has run. Handoff is durable continuity evidence, not preserved project content or authority.
The full 100-keypoint mission directive is architecturally acknowledged in
[architecture](ARCHITECTURE.md#agent-fabric-relationship); future components are NOT_STARTED.
See [handoff scope and limitations](V3_CONTRACT.md#durable-handoff-persistence) and V3_PROGRESS.
