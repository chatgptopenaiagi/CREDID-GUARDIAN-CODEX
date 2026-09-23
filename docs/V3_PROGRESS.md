# CREDID GUARDIAN CODEX — CGC V3 progress

## OVERALL STATUS

**PARTIAL.** V3 remains the active preservation mission. Inspection, durable handoff, manual
checkpoint, local-bare publication/verification and scoped ref/transfer/commit/pack/staging
interruption acceptance remain accepted. **Abrupt CGC-parent death at both active staging
rename gates, including fresh-invocation refusal, is COMPLETE / VERIFIED OFFLINE.**
Broader crash guarantees and full safe resume remain PARTIAL. V4 remains ARCHITECTED /
runtime NOT_STARTED, byte-unchanged. All 100 [V3 mission](V3_MISSION.md) keypoints remain intact.

## STARTING VERIFIED CHECKPOINT

Clean main; empty diff/stat/whitespace; recent history reconciled. Independent local HEAD,
origin/main and live remote main all equalled `294ac10677af0990281cf655aa0e8c414306653d`.
Previous staging implementation: `dd02dd81cf92d5e4436f759b1cf55d17cdb7e08a`.
Authoritative documents and runtime/prior fixture evidence reconciled with that accepted state.
No accepted block repeated as new work, no V4 commit reverted, no unrelated repository touched.
Historical detailed staging evidence remains in the starting checkpoint and contract.

## CAPACITY

Current weekly and five-hour capacity **UNKNOWN**. Historical human planning value 92% weekly
is not current observation; purchased credits do not determine included capacity. No quota read,
account scrape or credential access. Capacity preservation activated: **NO**.

## CURRENT COHERENT BLOCK / COMPLETE

Only abrupt CGC-parent death with a real active mutation child and fresh refusal was selected.
Two new tests reuse unchanged add_peer.py/add_gate.c. Installed Git's real index.lock → index
rename is gated before and after the actual rename in disposable Linux /tmp repositories.
No mocked Git result, new production abstraction or runtime defect was needed.

- Before death: real CGC PID is Git's PPID; Git PID equals its process-group/session IDs and
  differs from the parent's group. Both CGC source and handoff-store flocks reject contenders.
- Parent receives actual SIGKILL, is waited/reaped with exit -9 and disappears from /proc.
  Git survives in its original session/group, blocked at the FIFO. Its observed new PPID is
  the explicitly configured fixture subreaper. General host reparenting is not assumed.
- Both CGC flocks can now be reacquired while Git remains active. Persistent CGC lock files
  are not deleted. These domains are distinct from Git's index lock, process and durable intent.
- Before rename: old installed index bytes/entries survive; complete candidate index.lock
  exists. After rename: complete new index is installed and index.lock absent with Git alive.
  Selected modification/addition/deletion and unrelated index entry are inspected. No partial
  installed subset is observed at these gates; not a universal atomicity/power-loss guarantee.
- Independent fresh Python checkpoint invocations refuse CURRENT_AUTHORITY_REQUIRED without
  current approval. With current review/authority they refuse GIT_LOCK_PRESENT before rename
  or EXISTING_STAGING afterward. No add/commit/ref-update/push/reset/restore/clean/gc/prune
  command is dispatched. No child killing, re-stage, automatic retry or repair is performed.
- Pending handoff stays byte-identical, previous_known_good survives, CHECKPOINTING and
  selected paths remain. latest_attempt stays PUBLISHED/error null: continuity persistence,
  not operation completion. No dead-parent CANCELLED/TIMEOUT/GIT_FAILED receipt is invented.
  Current intent local_commit is null; publication NOT_REQUESTED; SAFE_TO_RESUME UNKNOWN.
- Fresh handoff-status exactly reproduces saved state. HEAD stays unchanged. Index and retained
  candidate bytes, worktree bytes/modes/sizes/mtimes and Git config remain unchanged across
  refusals. Unrelated tracked modification and untracked human file survive.
- After assertions ONLY, harness releases/reaps orphan Git. Real staging finishes successfully
  without a parent checkpoint receipt; HEAD and handoff still unchanged. Fallback harness
  cleanup kills/reaps disposable orphan; original subreaper setting is restored. This is test
  hygiene, not production recovery. Prior successful controls remain unchanged.

## PARTIAL / LIMITATIONS

Overall V3, general crash safety and full reconciliation remain PARTIAL. This proves two real
staging windows on Linux/dynamically linked Git with fixture libc rename interception and cc.
It does not establish universal orphan detection/cleanup, arbitrary later mutation timing,
cross-source writers, hostile same-user concurrency, other platforms/index formats or power loss.
No Git ref-lock or publication-parent-death window is newly claimed here. Runtime remains as-is.

SIGKILL cannot be caught, run finally/cleanup or persist a new failure from its victim. Process
death proves neither success nor failure. Lock availability is not safety. Postmortem facts come
from durable evidence plus fresh observation. The fixture subreaper changes only test-process
adoption temporarily; CGC does not supervise or kill historical children on fresh invocation.

Pending intent saves paths, not the caller's complete reviewed SHA256 mapping. Fresh approval
and selected digests in the test are supplied anew, never reconstructed from durable intent.
Historical intent is not current authority. Later evidence-based reconciliation must explicitly
address that gap; no automatic safe-resume decision is added here.

## NOT_STARTED

Full fresh-process reconciliation/resume engine, project test runner, Guardian automation,
preserve CLI, general network publication, automatic repair/retry/rollback/orphan cleanup,
Agent Fabric runtime. V4 protocol/capsule/MCP/plugin/SDK/Rust/desktop/web/mobile/gateway runtime
remains NOT_STARTED. No unrelated project changes, dependency installation or telemetry.

## TESTS ACTUALLY RUN

Historical baseline: 318 tests, not rerun before development.
Initial focused run: 2 passed in 2.314s. Final focused run after negative-command assertions:

```text
TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_parent_death -q
Ran 2 tests in 2.152s — OK

TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_parent_death test_add_interruption test_checkpoint test_commit_interruption test_mutation_interruption -q
Ran 62 tests in 44.641s — OK
```

Relevant V3:

```text
TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_preservation test_inspection test_handoff test_checkpoint test_publication test_mutation_interruption test_transfer_interruption test_commit_interruption test_pack_interruption test_add_interruption test_parent_death -q
Ran 167 tests in 87.139s — OK
```

Full deterministic regression, once before publication:

```text
TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -q
Ran 320 tests in 104.129s — OK
```

All runs passed: zero failures, errors or skips. No test/runtime changes after validation.
Existing C fixture compilation passed -shared -fPIC -Wall -Wextra -Werror -ldl; all generated
libraries are temporary /tmp artifacts, not installed or committed.

Static/documentation checks passed: 39 Python ASTs, three JSON files, 180 local Markdown
file/anchor links and exactly 100 preserved V3 keypoints. Exact seven-file scope reviewed;
58 other files are byte-identical, including V3/V4 missions, runtime, schemas and inherited
tests/helpers. All 65 tracked/new files pattern-screened; only the two known unchanged
synthetic credential-URL fixtures matched (test_handoff.py:153, test_inspection.py:144).
No real credential finding; this is not universal secret proof. Diff/status and whitespace
review passed. CGC fetch/push destination independently checked against the authorized repo.
No persistent system/environment changes, dependencies or services. Temporary test-only
subreaper adoption restores the original setting; only disposable fixtures are released/reaped.
No test/development failures observed. A post-commit validation helper initially compared the
seven-file session scope against moving HEAD and rejected the two-file evidence follow-up;
its scope comparison was corrected to the fixed starting SHA and passed. No product defect.
No production runtime, inherited test/helper or schema edits.

## FRONTIER ASSESSMENT

**YES, within the selected practical pre-reconciliation acceptance scope.** The last recorded
material gap now has real parent-death/refusal evidence, including the no-index.lock window.
This does not promote broader crash safety to universal COMPLETE. Remaining platform/internal
write/cross-source/power-loss limitations remain explicit; no endless timing-test ladder starts.
The next separately authorized block is full evidence-based fresh-process reconciliation.

## FILES CREATED / MODIFIED

Created: tests/test_parent_death.py.
Modified: README.md, AGENTS.md, docs/V3_PROGRESS.md, docs/V3_CONTRACT.md,
docs/V3_ACCEPTANCE.md, tests/README.md.
Runtime, inherited helpers/tests, V3/V4 missions, schemas and V1/V2 records unchanged.

## DO_NOT_REPEAT

Do not redo accepted staging, commit, transfer, pack/ref or these parent-death windows without
new defect evidence. Do not infer quiescence from flock/index.lock availability, reuse dead-parent
authority, invent a failure/success receipt, delete evidence, retry, repair or kill old processes
automatically. No live quota discovery, credential access, destructive Git commands or V4 runtime.

## NEXT_EXACT_ACTION

After publication STOP. Next separately scoped V3 block: **audit and specify full evidence-based
fresh-process reconciliation of durable intent against current Git/checkpoint/publication/test
reality, beginning with interrupted attempts and missing durable review digests**. Determine the
bounded reconciliation contract before implementation; retain UNKNOWN until evidence justifies
otherwise. No automatic mutation, retry or V4. Reconcile present repository evidence first.

## LAST SAFE CHECKPOINT / PUBLICATION

Starting verified checkpoint: `294ac10677af0990281cf655aa0e8c414306653d`.
Acceptance implementation: `f57fe1df85c84fea08d51410dcd6ffbc6497cc41` — **REMOTE_VERIFIED**.
Normal forward push succeeded. Independent local HEAD, origin/main and live remote main all
equalled that SHA; working tree clean. This documentation-only follow-up records the observed
publication and acceptance row 41. Its own HEAD must be pushed and independently verified;
the final report carries its resolved SHA. No self-containing hash, no repeated runtime tests.
If follow-up publication fails, retain the local evidence commit and report its actual status.
