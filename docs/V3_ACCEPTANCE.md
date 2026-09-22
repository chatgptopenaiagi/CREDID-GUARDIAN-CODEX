# CREDID GUARDIAN CODEX — CGC V3 acceptance

Overall: **PARTIAL**. Attempt, inspection and external handoff persistence complete within their offline contracts; preservation execution remains pending. This matrix preserves all 43
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
| 7 | Manual preservation works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 8 | Human handoff works. | COMPLETE | Human handoff renders validated persisted state, with quoted uppercase continuity fields; fresh-process output equality tested. |
| 9 | Machine-readable handoff works. | COMPLETE | Versioned canonical handoff.json; fresh-process JSON readback and unsupported schema refusal tested. |
| 10 | COMPLETE/PARTIAL/NOT_STARTED are preserved. | COMPLETE | Curated complete/partial/not_started persist in the validated attempt inside the handoff. |
| 11 | NEXT_EXACT_ACTION is preserved. | COMPLETE | notes.next_exact_action survives disk and fresh-process reconstruction; no execution implied. |
| 12 | Known failures are preserved. | COMPLETE | Known failures retained with failed test state through publication, failure and recovery. |
| 13 | Relevant tests/results are preserved. | PARTIAL | Curated test status/command/results persist; automatic test selection/execution and structured result counts remain future adapters. |
| 14 | Last-known-good preservation is retained. | PARTIAL | Continuity latest failure preserves both good slots; post-replace uncertainty retains previous. Target preservation not implemented. |
| 15 | Local checkpoint behavior is correct. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 16 | Git staging is bounded and deliberate. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 17 | Secret-risk protections exist. | PARTIAL | Handoff allowlists, non-echoing recognizable-secret refusal and no content collection; inspection safeguards retained. Target staging protections pending. |
| 18 | Destructive Git actions are absent. | COMPLETE | Inspector executes only config/read metadata/status commands; non-mutation comparisons. No target Git mutation command exists. |
| 19 | Forward-only normal commit behavior works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 20 | Local bare-remote publication works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 21 | Push failure is truthful. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 22 | Remote verification works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 23 | LOCAL_CHECKPOINT_ONLY works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 24 | Project writer exclusion works. | PARTIAL | Handoff-store flock excludes competing processes and releases on death; target-project mutation lock remains pending. |
| 25 | Crash/interruption tests pass. | PARTIAL | Inspection signals plus handoff SIGKILL at four synchronized write stages, seeded/unseeded, and injected I/O failures. Target mutation stages pending. |
| 26 | Atomic canonical preservation state works. | PARTIAL | Atomic canonical handoff tested with live readers and killed writers; target preservation transaction pending. |
| 27 | Repeated invocation is safe/idempotent where applicable. | PARTIAL | Reads are inert and deterministic; each explicit publish increments generation. Preservation operation idempotency remains pending. |
| 28 | SAFE_TO_RESUME semantics are evidence-based. | PARTIAL | Outer handoff UNKNOWN/false never upgrades curated attempt receipts. End-to-end external verification pending. |
| 29 | Resume from a fresh CGC process works. | PARTIAL | Fresh process reconstructs validated human/JSON handoff including latest failure; Git/test reconciliation and safe resume execution pending. |
| 30 | Manual preservation is independent from live quota availability. | PARTIAL | Manual record independent of quota; end-to-end manual preservation pending. |
| 31 | Synthetic Guardian policy integration works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 32 | UNKNOWN Guardian state cannot authorize automatic mutation. | PARTIAL | All automatic triggers denied in Phase A; Guardian integration pending. |
| 33 | Automatic preservation consumes canonical V2 policy only. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 34 | Resource bounds are tested. | PARTIAL | Handoff file/read/write/human bounds, field/list/record limits tested; inherited inspection bounds retained. Mutation bounds pending. |
| 35 | Security/path tests pass. | PARTIAL | Handoff overlap/alias/no-follow/private-file/schema refusal and inherited inspection security pass; target mutation security pending. |
| 36 | No unrelated project was modified. | COMPLETE | Only CGC development files changed; no external target preserved. |
| 37 | No V1/V2 semantics were weakened. | COMPLETE | Inherited runtime/tests and V2 records unchanged. |
| 38 | No secret material was intentionally committed. | COMPLETE | Development publication scan; no secret input used. Not universal proof. |
| 39 | Documentation is complete. | PARTIAL | Mission/contract/progress preserved; later implementation docs pending. |
| 40 | Canonical deterministic test command passes. | COMPLETE | 222 tests pass (153 V1/V2 + 22 attempt + 29 inspection + 18 handoff); exact output in progress. |
| 41 | Git publication of CGC V3 itself is verified. | COMPLETE | Handoff `7d1ca1e3335b13e6e2a5eba8d821d2e25b887400` pushed; local/tracking/live main equality and clean tree verified on 2026-09-22. Follow-up HEAD verification reported after publication. See progress. |
| 42 | The final V3 checkpoint is resumable. | PARTIAL | Development handoff and runtime fresh-process continuity readback exist; complete V3 safe-resume workflow pending. |
| 43 | V4 or cloud work has not begun without authorization. | COMPLETE | No V4/cloud/GUI/ARX implementation. |


Inspection and handoff writes have run only with disposable synthetic Linux fixtures.
No target checkpoint/push, project test execution, Guardian automation or resume generator
has run. Handoff is durable continuity evidence, not preserved project content or authority.
The full 100-keypoint mission directive is architecturally acknowledged in
[architecture](ARCHITECTURE.md#agent-fabric-relationship); future components are NOT_STARTED.
See [handoff scope and limitations](V3_CONTRACT.md#durable-handoff-persistence) and V3_PROGRESS.
