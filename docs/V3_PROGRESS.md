# CREDID GUARDIAN CODEX — CGC V3 progress

## OVERALL STATUS

**PARTIAL. V3 remains active.** Prior inspection, durable handoff, checkpoint, local-bare
publication/verification and scoped crash acceptance remain intact. The **minimal bounded
read-only fresh-process reconciliation engine is IMPLEMENTED and accepted within its first-engine
scope**. Full external safe resume, recovery execution and automation remain NOT_STARTED.
V4 remains ARCHITECTED / runtime NOT_STARTED; V3/V4 missions and all 100 keypoints are unchanged.

## VERIFIED STARTING CHECKPOINT

Before editing: root, clean status, empty diff/stat/whitespace, fourteen-entry history checked.
Independent local HEAD = origin/main = live remote main =
`de0ffbc6fb52930c0e324eea7dc1c4bb2ff2bc60`.
Specification commit: `09cb46fc8df4ba95034d6fe44d113498a52675e6`.
Read the complete accepted reconciliation contract; reconciled current authoritative records,
existing evidence-model runtime and relevant A–R interruption fixtures. No accepted crash block
was repeated as new work, no valid work reverted, no other repository touched.

## CAPACITY

Current weekly/five-hour capacity UNKNOWN. Human planning value 87% weekly remains historical.
No quota/account/credential read or estimate. Capacity preservation activated: NO.

## COMPLETE — THIS ONE BLOCK

- New reconciliation.py separates bounded collect() from pure classify(); reconcile() composes
  them. Explicit version cgc-reconciliation-v3.0-provisional, strict nested validation and replayed
  derived output. render_json/render_human use exactly that validated model. Python API only;
  no reconcile CLI, service, daemon, database or package dependency.
- Pending intent is the primary fixture: historical paths/receipts/phase/test notes and both
  continuity slots survive, with final handoff generation/digest compared. No create/writer/
  migration/failure-publication calls. PUBLISHED remains a continuity-store status, not Git success.
- Current local observation plus repeated semantic index (path/mode/stage/flag/OID), config and
  metadata fingerprints, locks/operations, HEAD/branch and at most two relevant commit identities.
  Surviving commit parent/tree comparison is explicitly against supplied expectations, never
  inferred review or a backfilled local_commit receipt. No reflog/history crawl or process scanner.
- Optional fresh review under existing candidate protections; raw SHA256 inputs checked against
  safe file bytes, resulting Git blob/mode evidence compared twice. Deletion is explicit None.
  Missing historical digests remain UNKNOWN. No file content export or authority inferred.
- Legacy test PASS/FAIL retained separately from UNKNOWN current applicability. Optional attributed
  current test reports can supply HEAD binding: mismatch proves STALE; equality cannot establish
  dirty-input/environment applicability. Fully bound trusted test-receipt reuse remains future.
- Optional explicit approved local-bare reads use ls-remote/direct ref/type and existing layout/
  identity checks, never publish(), fetch or update-ref. Tracking remains untouched. No remote
  query by default; failed optional observation preserves local facts and UNKNOWN remote scope.
- Fixed output invariants: SAFE_TO_RESUME UNKNOWN; mutation_allowed=false;
  automatic_mutation_authorized=false. Valid inner-attempt YES never upgrades them. Current
  authority descriptions are inert; a requested future mutation requires fresh scoped authority.
- Claim-scoped CURRENT/HISTORICAL/STALE/CONTRADICTED/UNKNOWN explanations retain both sides.
  Ordered issues follow target → durable → pending/locks → Git conflict → review/tests → remote;
  deterministic domain/subject tie-breaks and exactly one safe next action. No hidden I/O in classifier.
- Shared 48-Git-command/60-second budget encompasses nested helpers, reset with ContextVar finally;
  command five-second/output bounds unchanged. Mutation commands and mutating config forms refused
  before spawn within this scope. Existing adapters outside it retain their behavior.
- Candidate reader's optional shared budget limits both review reads together to 4 MiB accepted
  content, not 8 MiB. More than 2 MiB distinct content may exhaust repeated review; truthful limit
  refusal is intentional. Output >256 KiB or >64 issues refuses without truncated all-clear.
- Negative tests snapshot source/store/remote files (bytes/modes/sizes/mtimes), prohibit writer
  helpers and mutation dispatch, and restrict cleanup to PIDs spawned for current observations.
  Independent Python process returns the same validated projection without changing fixtures.

## ACCEPTANCE A–R

| Cases | Status / evidence |
|---|---|
| A / B | COMPLETE: old index+lock / complete staged index, pending intent, no mutation |
| C / D | COMPLETE: surviving structural match without receipt / changed HEAD contradiction |
| E / F / G | COMPLETE: old remote / equal remote with stale tracking / historical VERIFIED then moved ref |
| H | COMPLETE for first-engine legacy PASS + UNKNOWN. Fully bound trusted receipt reuse NOT_STARTED, as allowed by contract section 8 |
| I | COMPLETE: supplied historical HEAD mismatch -> STALE; same HEAD with dirty bytes still UNKNOWN |
| J / K | COMPLETE: absent durable review / matching current review without authority |
| L | COMPLETE: observation-only state with no required action still UNKNOWN safety |
| M / N | COMPLETE: timeout/cancellation; absent/corrupt/unsupported handoff preserved |
| O | COMPLETE: target identity mismatch, local race, handoff-generation race and malformed second evidence |
| P / Q / R | COMPLETE: remote unavailable/default no query; valid embedded YES; config/path/size/budget refusal |

Additional checks: fresh process, pure deterministic rendering, unknown fields/version/enums,
reference formats/bindings, list/string/output bounds, unsafe paths, symlink/hardlink refusal,
review mismatch/deletion, shared byte/deadline/command budgets. These recreate observable states;
they do not repeat synchronized crash fixtures or claim universal process-death coverage.

## TESTS ACTUALLY RUN / DEVELOPMENT CORRECTIONS

Historical baseline: 320 tests, not rerun before development.
Initial focused run: 25 tests, two failures and one error. Corrected missing historical branch
being treated as a mismatch, normalized handoff validation exceptions, and aligned the missing-store
expectation with the existing UNSAFE_CACHE refusal. Subsequent focused runs passed:
25 in 3.099s; 25 in 2.851s; 33 in 4.001s; 33 in 4.370s; 33 in 3.597s.

Integration before final shared review-byte refinement:

```text
TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_reconciliation test_handoff test_inspection test_checkpoint test_publication -q
Ran 128 tests in 20.732s — OK
```

Focused reconciliation/checkpoint scope, including the shared-byte test:

```text
TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_reconciliation test_checkpoint -q
Ran 57 tests in 7.163s — OK
```

Relevant V3 suite covers all integration surfaces before the final projection-binding tightening:

```text
TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_preservation test_inspection test_handoff test_checkpoint test_publication test_mutation_interruption test_transfer_interruption test_commit_interruption test_pack_interruption test_add_interruption test_parent_death test_reconciliation -q
Ran 201 tests in 96.851s — OK
```

First full deterministic regression: 354 tests in 109.369s — OK. Final code review then found
that externally supplied projection evidence needed cross-field validation of remote direct/live
agreement and review-path coverage. Added those checks plus two tampering tests; this justified
one repeated full regression after the final change rather than publishing the validator gap.

Final focused reconciliation run:

```text
TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_reconciliation -q
Ran 36 tests in 3.792s — OK
```

Final full deterministic regression:

```text
TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -q
Ran 356 tests in 106.918s — OK
```

Zero failures, errors or skips. This includes all 203 current V3 tests after the final tightening;
the earlier separate 201-test V3 run is not misrepresented as a post-change run. No runtime/test
edits followed this final validation. Full suite ran twice only because final review found a
material projection-validator defect after the first successful run.

Static validation PASS: 41 Python ASTs, three JSON files, 208 local Markdown file/anchor links,
100 V3 keypoints, 11 scenario rows and 18 A–R case definitions. Exact thirteen-file scope checked;
55 other files byte-identical, including existing schemas, inherited tests/helpers, V3/V4 missions
and unrelated runtime. All 68 tracked/new files pattern-screened; only the two known unchanged
synthetic credential-URL fixtures matched (test_handoff.py:153, test_inspection.py:144). No real
credential finding; pattern screening is not universal proof. Exact diff/status reviewed and
whitespace checks pass. Inherited C fixture warnings-as-errors compilation passes in regression.
No unresolved deterministic failures. No inherited tests were modified.

## LIMITATIONS / PARTIAL / NOT_STARTED

Overall V3 remains PARTIAL. Repeated observation is not an atomic snapshot or hostile same-user
race defense. Process quiescence remains UNKNOWN; no historical children are killed. Read access
can update atime. Filesystem calls, Git decompression and cleanup lack hard realtime/RSS guarantees.
Bounds/config/layout restrictions remain deliberate, with Linux fixtures only. Projection validation
proves consistency, not authenticity of caller-supplied evidence. Observation time is caller supplied.
Malformed inputs and unrepresentable oversized results raise fixed validation/resource errors;
no partial snapshot is promoted to valid evidence. Complete test-environment binding is absent.
No external YES verifier, authority inheritance, automatic tests, rollback, retry, orphan repair,
lock deletion, network publication, Guardian automation, preserve CLI, full resume engine, Agent
Fabric or V4 runtime. Existing handoff/inspection/attempt schemas are unchanged.

## FILES CREATED / MODIFIED

Created: src/cgc/reconciliation.py; tests/test_reconciliation.py.
Modified: src/cgc/inspection.py (invocation-local observation budget), src/cgc/checkpoint.py
(optional shared content-read budget); AGENTS.md, README.md, docs/DATA_MODEL.md, docs/DECISIONS.md,
docs/V3_ACCEPTANCE.md, docs/V3_CONTRACT.md, docs/V3_RECONCILIATION.md, docs/V3_PROGRESS.md,
tests/README.md. No handoff/publication/preservation/signals/CLI runtime or inherited tests changed.
No dependencies, services, persistent environment/system changes or unrelated project changes.

## DO_NOT_REPEAT

Do not redo accepted crash blocks, quota discovery or reconciliation A–R without defect evidence.
Do not mistake model validation for authenticity, old PASS for current PASS, observed ref equality
for a new publication receipt, matching digests for authority, or UNKNOWN for permission.
No writer-lock probes, fetch/update-ref, automatic tests/repair, hidden schema migration or V4.

## NEXT_EXACT_ACTION

**Audit and specify the external SAFE_TO_RESUME verifier against the implemented reconciliation
projection, beginning with unresolved quiescence and tested-state/review evidence obligations.**
Determine what additional evidence can actually discharge the proof before implementing YES.
Reconcile current repository reality first. Do not start verifier implementation, recovery execution
or V4 in this completed read-only-engine session.

## LAST SAFE CHECKPOINT / PUBLICATION

Starting verified checkpoint: `de0ffbc6fb52930c0e324eea7dc1c4bb2ff2bc60`.
Implementation is pending normal commit/push and independent local/tracking/live verification.
Commit self-reference is HEAD; the final report records its resolved SHA after verification.
