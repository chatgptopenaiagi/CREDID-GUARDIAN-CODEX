# CREDID GUARDIAN CODEX — CGC V3 acceptance

Overall: **PARTIAL**. Attempt contract plus bounded explicit inspection; preservation execution remains pending. This matrix preserves all 43
implementation checks mapped to [V3 mission](V3_MISSION.md) sections 2 and 3.
The 43-row decomposition is retained from the prior handoff; these are not numbered
criteria in the current mission. Its full requirements remain authoritative. Current session
evidence: [contract](V3_CONTRACT.md), [attempt tests](../tests/test_preservation.py), [inspection tests](../tests/test_inspection.py), and
[progress](V3_PROGRESS.md). COMPLETE rows describe this checkpoint's evidence, not a
claim that future external-effect implementations already satisfy them.

| # | Criterion | Status | Evidence / remaining work |
|---|---|---|---|
| 1 | V1 tests remain passing. | COMPLETE | Inherited 32 V1 tests unchanged. |
| 2 | V2 tests remain passing. | COMPLETE | All 153 inherited V1/V2 tests unchanged and passing. |
| 3 | V3 preservation schema exists and is validated. | PARTIAL | Attempt and inspection schemas validated; persistence envelope pending. |
| 4 | Explicit project targeting works. | COMPLETE | Explicit inspect --project required; exact root only. test_explicit_root_only_and_safe_failures and CLI tests. |
| 5 | Project root validation works. | COMPLETE | Owned no-follow root, metadata and device/mode boundaries; unsafe/unsupported layouts refused. Scoped Linux contract, not universal Git-layout support. |
| 6 | Non-mutating project snapshot works. | COMPLETE | Bounded local collector; clean/dirty/rename/conflict/upstream/index flags and repeated observation tests. Full fixture byte/metadata comparisons. |
| 7 | Manual preservation works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 8 | Human handoff works. | PARTIAL | Pure human renderer exists; actual project handoff pending. |
| 9 | Machine-readable handoff works. | PARTIAL | Pure JSON renderer exists; stored handoff pending. |
| 10 | COMPLETE/PARTIAL/NOT_STARTED are preserved. | PARTIAL | Bounded notes round-trip; disk persistence pending. |
| 11 | NEXT_EXACT_ACTION is preserved. | PARTIAL | Required exact next-action text; external handoff pending. |
| 12 | Known failures are preserved. | PARTIAL | Failure notes required for failed tests; persistence pending. |
| 13 | Relevant tests/results are preserved. | PARTIAL | Separate status and command/result notes; execution adapters pending. |
| 14 | Last-known-good preservation is retained. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 15 | Local checkpoint behavior is correct. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 16 | Git staging is bounded and deliberate. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 17 | Secret-risk protections exist. | PARTIAL | No content/URL export; fixed errors, config helper/include refusal, synthetic secret tests. Staging protections remain pending. |
| 18 | Destructive Git actions are absent. | COMPLETE | Inspector executes only config/read metadata/status commands; non-mutation comparisons. No target Git mutation command exists. |
| 19 | Forward-only normal commit behavior works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 20 | Local bare-remote publication works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 21 | Push failure is truthful. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 22 | Remote verification works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 23 | LOCAL_CHECKPOINT_ONLY works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 24 | Project writer exclusion works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 25 | Crash/interruption tests pass. | PARTIAL | Inspection SIGINT/SIGTERM, bounded peers and race refusal tested. Preservation-write/commit/publication crash cases pending. |
| 26 | Atomic canonical preservation state works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 27 | Repeated invocation is safe/idempotent where applicable. | PARTIAL | Repeated inspection deterministic with fixed time and no target mutation; preservation idempotency pending. |
| 28 | SAFE_TO_RESUME semantics are evidence-based. | PARTIAL | Consistent receipt-derived model; trusted receipt collection/verification pending. |
| 29 | Resume from a fresh CGC process works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 30 | Manual preservation is independent from live quota availability. | PARTIAL | Manual record independent of quota; end-to-end manual preservation pending. |
| 31 | Synthetic Guardian policy integration works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 32 | UNKNOWN Guardian state cannot authorize automatic mutation. | PARTIAL | All automatic triggers denied in Phase A; Guardian integration pending. |
| 33 | Automatic preservation consumes canonical V2 policy only. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 34 | Resource bounds are tested. | PARTIAL | Attempt and inspection count/depth/file/config/output/time bounds tested. Persistence/mutation stage bounds pending. |
| 35 | Security/path tests pass. | PARTIAL | Inspection path/ownership/symlink/hardlink/special-file/config and schema tests pass; future mutation security acceptance pending. |
| 36 | No unrelated project was modified. | COMPLETE | Only CGC development files changed; no external target preserved. |
| 37 | No V1/V2 semantics were weakened. | COMPLETE | Inherited runtime/tests and V2 records unchanged. |
| 38 | No secret material was intentionally committed. | COMPLETE | Development publication scan; no secret input used. Not universal proof. |
| 39 | Documentation is complete. | PARTIAL | Mission/contract/progress preserved; later implementation docs pending. |
| 40 | Canonical deterministic test command passes. | COMPLETE | 204 tests pass (153 V1/V2 + 22 attempt + 29 inspection); exact result in progress. |
| 41 | Git publication of CGC V3 itself is verified. | COMPLETE | Foundation `0edee399f2f4411a413956929f2be012e8b32e35` pushed; local/tracking/live main equality and clean tree verified on 2026-09-21. See progress. |
| 42 | The final V3 checkpoint is resumable. | PARTIAL | This development checkpoint has exact handoff; V3 runtime fresh-process resume pending. |
| 43 | V4 or cloud work has not begun without authorization. | COMPLETE | No V4/cloud/GUI/ARX implementation. |

Inspection has run only against disposable synthetic Linux repositories. No actual V3
handoff publication, target checkpoint, target remote publication, preservation-write
crash test or fresh-process handoff resume has run. Inspection is not preservation.
Next coherent block: human/machine handoff persistence; see V3_PROGRESS.
