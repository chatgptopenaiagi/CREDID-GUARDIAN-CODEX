# CREDID GUARDIAN CODEX — CGC V3 acceptance

Overall: **PARTIAL**. Attempt, inspection and external handoff persistence complete within their offline contracts; manual local checkpointing and explicit local-bare publication/verification are verified; general push transport and full preservation/resume remain pending. This matrix preserves all 43
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
| 14 | Last-known-good preservation is retained. | PARTIAL | Publication failure retains pending local receipt and previous good slot via record_failure; full preservation/resume transaction remains pending. |
| 15 | Local checkpoint behavior is correct. | COMPLETE | Scoped adapter verifies exact staged tree, branch and single expected parent; test_checkpoint. Full workflow remains partial. |
| 16 | Git staging is bounded and deliberate. | COMPLETE | Explicit reviewed paths/digests; literal staging; full index comparison; existing staging refused; subset/ignored/rename/deletion tests. |
| 17 | Secret-risk protections exist. | PARTIAL | Handoff and selected-content screening, sensitive/generated path refusal, UTF-8/size bounds and no-follow reads tested. No universal detector or history audit. |
| 18 | Destructive Git actions are absent. | COMPLETE | Mutation adapter uses deliberate add, write-tree and normal commit only. No reset/clean/restore/stash/rebase/force push or rollback. |
| 19 | Forward-only normal commit behavior works. | COMPLETE | New HEAD/tree/branch and exactly one expected parent independently read after normal commit; no empty/repeated commits. |
| 20 | Local bare-remote publication works. | COMPLETE | Explicit approved local bare object transfer plus forward expected-tip CAS; test_publication. No general Git-push/network adapter claimed. |
| 21 | Push failure is truthful. | PARTIAL | Local transfer/ref-update failures and accept-then-error remain uncertain; real Git expected-tip rejection tested. General Git-push transport NOT_STARTED. |
| 22 | Remote verification works. | COMPLETE | Separate fetch, live ls-remote, direct bare-ref read, approved tracking CAS/readback and final live/source checks; mismatch never VERIFIED. |
| 23 | LOCAL_CHECKPOINT_ONLY works. | COMPLETE | Known local commit retained on refused/failed/unverified publication; LOCAL_CHECKPOINT_ONLY is a knowledge claim, not proof remote untouched. |
| 24 | Project writer exclusion works. | PARTIAL | Shared source lock excludes writers during prepared/accepted ref transactions and after fetch-child death while transfer descendants remain alive. Real pre/post-commit stages also exclude a contender with fresh HEAD and a different store. Fetch/index-pack child-death intervals with live pack pipeline also exclude a contender. Active git add before/after index replacement also excludes a checkpoint contender. After parent SIGKILL both CGC flocks release while Git survives; fresh calls independently refuse Git lock/existing staging. Cross-source concurrency remains pending. |
| 25 | Crash/interruption tests pass. | PARTIAL | Prior boundaries/ref transactions plus real active loose-object arrival SIGINT/SIGTERM, fetch-child death and timeout pass. Real commit pre/post-hook SIGINT/SIGTERM, timeout and command-group death also pass. Real active index-pack temporary arrival SIGINT/SIGTERM, timeout, fetch death and receiver death pass; retained fragments never imply publication. Real add before/after index rename signals, timeout and child death pass; old index/retained lock or complete new staging survives. Parent SIGKILL at both add gates preserves intent; fresh authorized calls refuse without mutation even after lock disappearance. Earlier writes, other internal timings and general orphan recovery remain outside this proof. |
| 26 | Atomic canonical preservation state works. | PARTIAL | Atomic canonical handoff tested with live readers and killed writers; target preservation transaction pending. |
| 27 | Repeated invocation is safe/idempotent where applicable. | PARTIAL | Already-equal remote verified without re-publication; stale tracking can advance safely. Missing/moved refs refuse; no blind retries or rollback. |
| 28 | SAFE_TO_RESUME semantics are evidence-based. | PARTIAL | Outer handoff UNKNOWN/false never upgrades curated attempt receipts. External proof obligations specified in V3_RECONCILIATION.md; end-to-end verification pending. |
| 29 | Resume from a fresh CGC process works. | PARTIAL | Fresh process reconstructs validated human/JSON handoff including latest failure; Git/test reconciliation contract SPECIFIED in V3_RECONCILIATION.md; engine and safe resume execution pending. |
| 30 | Manual preservation is independent from live quota availability. | PARTIAL | Explicit MANUAL local-checkpoint adapter independent of quota; full preservation/resume workflow pending. |
| 31 | Synthetic Guardian policy integration works. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 32 | UNKNOWN Guardian state cannot authorize automatic mutation. | PARTIAL | All automatic triggers denied in Phase A; Guardian integration pending. |
| 33 | Automatic preservation consumes canonical V2 policy only. | NOT_STARTED | Required future implementation and deterministic acceptance tests. |
| 34 | Resource bounds are tested. | PARTIAL | Publication reuses bounded Git/scan/config operations and adds bounded names/refs/path; no hard syscall/RSS or decompressed object guarantee. |
| 35 | Security/path tests pass. | PARTIAL | Source/bare identity, path, modes, protocols, config, hooks, refs and overlap refusal tests; general transport security/hardening remains. |
| 36 | No unrelated project was modified. | COMPLETE | Only CGC development files and disposable Linux test repositories changed; no valuable external target mutated. |
| 37 | No V1/V2 semantics were weakened. | COMPLETE | Inherited runtime/tests and V2 records unchanged. |
| 38 | No secret material was intentionally committed. | COMPLETE | Development publication scan; no secret input used. Not universal proof. |
| 39 | Documentation is complete. | PARTIAL | Mission/contract/progress preserved; later implementation docs pending. |
| 40 | Canonical deterministic test command passes. | COMPLETE | 320 tests pass (318 inherited unchanged + two real parent-death tests); historical exact commands/output in checkpoint 1edbe5a; documentation-only reconciliation specification did not rerun them. |
| 41 | Git publication of CGC V3 itself is verified. | COMPLETE | Reconciliation specification 09cb46fc8df4ba95034d6fe44d113498a52675e6 pushed normally; local/tracking/live main equality and clean tree independently verified. Evidence follow-up HEAD checked after publication; final report carries its resolved SHA. No new runtime acceptance claimed. |
| 42 | The final V3 checkpoint is resumable. | PARTIAL | Development handoff and runtime fresh-process continuity readback exist; complete V3 safe-resume workflow pending. |
| 43 | V4 or cloud work has not begun without authorization. | COMPLETE | No V4/cloud/GUI/ARX implementation. |


Inspection, handoff, local checkpoints and local-bare publication have run only with
disposable synthetic Linux fixtures. No valuable target publication, target network transport,
project test execution, Guardian automation or resume generator has run. Handoff is durable continuity evidence, not preserved project content or authority.
The full 100-keypoint mission directive is architecturally acknowledged in
[architecture](ARCHITECTURE.md#agent-fabric-relationship); future components are NOT_STARTED.
See [handoff scope and limitations](V3_CONTRACT.md#durable-handoff-persistence) and V3_PROGRESS.


## Reconciliation contract acceptance boundary

[Reconciliation specification](V3_RECONCILIATION.md): audited design COMPLETE; engine and
cases A–R (18 cases) NOT_STARTED. The 11-scenario matrix traces existing interruption evidence,
not newly executed tests. No runtime acceptance row is promoted because a design was written.
Read-only non-mutation, deterministic classification, missing review/test evidence, strict
compatibility, local-first remote scope and UNKNOWN safety are mandatory future acceptance.
