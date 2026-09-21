# CREDID GUARDIAN CODEX — CGC V3 acceptance

Overall: **PARTIAL**. Phase A attempt contract only. This matrix preserves all 43
implementation checks mapped to [V3 mission](V3_MISSION.md) sections 2 and 3.
The 43-row decomposition is retained from the prior handoff; these are not numbered
criteria in the current mission. Its full requirements remain authoritative. Current session
evidence: [contract](V3_CONTRACT.md), [tests](../tests/test_preservation.py), and
[progress](V3_PROGRESS.md). COMPLETE rows describe this checkpoint's evidence, not a
claim that future external-effect implementations already satisfy them.

| # | Criterion | Status | Evidence / remaining work |
|---|---|---|---|
| 1 | V1 tests remain passing. | COMPLETE | Inherited 32 V1 tests unchanged. |
| 2 | V2 tests remain passing. | COMPLETE | All 153 inherited V1/V2 tests unchanged and passing. |
| 3 | V3 preservation schema exists and is validated. | PARTIAL | Initial attempt schema validated; snapshot and persistence envelope pending. |
| 4 | Explicit project targeting works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 5 | Project root validation works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 6 | Non-mutating project snapshot works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
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
| 17 | Secret-risk protections exist. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 18 | Destructive Git actions are absent. | COMPLETE | No Git execution in new module; future mutation stages need review. |
| 19 | Forward-only normal commit behavior works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 20 | Local bare-remote publication works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 21 | Push failure is truthful. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 22 | Remote verification works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 23 | LOCAL_CHECKPOINT_ONLY works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 24 | Project writer exclusion works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 25 | Crash/interruption tests pass. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 26 | Atomic canonical preservation state works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 27 | Repeated invocation is safe/idempotent where applicable. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 28 | SAFE_TO_RESUME semantics are evidence-based. | PARTIAL | Consistent receipt-derived model; trusted receipt collection/verification pending. |
| 29 | Resume from a fresh CGC process works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 30 | Manual preservation is independent from live quota availability. | PARTIAL | Manual record independent of quota; end-to-end manual preservation pending. |
| 31 | Synthetic Guardian policy integration works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 32 | UNKNOWN Guardian state cannot authorize automatic mutation. | PARTIAL | All automatic triggers denied in Phase A; Guardian integration pending. |
| 33 | Automatic preservation consumes canonical V2 policy only. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 34 | Resource bounds are tested. | PARTIAL | Record/text/list/event bounds tested; project/subprocess bounds pending. |
| 35 | Security/path tests pass. | PARTIAL | Strict schema/lexical path checks; actual target/security tests pending. |
| 36 | No unrelated project was modified. | COMPLETE | Only CGC development files changed; no external target preserved. |
| 37 | No V1/V2 semantics were weakened. | COMPLETE | Inherited runtime/tests and V2 records unchanged. |
| 38 | No secret material was intentionally committed. | COMPLETE | Development publication scan; no secret input used. Not universal proof. |
| 39 | Documentation is complete. | PARTIAL | Mission/contract/progress preserved; later implementation docs pending. |
| 40 | Canonical deterministic test command passes. | COMPLETE | 175 tests pass; final exact result recorded in progress. |
| 41 | Git publication of CGC V3 itself is verified. | COMPLETE | Foundation `0edee399f2f4411a413956929f2be012e8b32e35` pushed; local/tracking/live main equality and clean tree verified on 2026-09-21. See progress. |
| 42 | The final V3 checkpoint is resumable. | PARTIAL | This development checkpoint has exact handoff; V3 runtime fresh-process resume pending. |
| 43 | V4 or cloud work has not begun without authorization. | COMPLETE | No V4/cloud/GUI/ARX implementation. |

No external project inspection or mutation, actual V3 handoff publication, local target
checkpoint, remote target publication, V3 crash test, or fresh-process resume has run.
Pure synthetic records do not count as end-to-end synthetic preservation. Stop after
this block; resume bounded non-mutating inspection from V3_PROGRESS.
