# CREDID GUARDIAN CODEX — CGC V3 progress

## OVERALL STATUS

**PARTIAL.** The deliberate manual local-checkpoint block is **COMPLETE / VERIFIED
OFFLINE within its restricted contract**. Attempt, bounded inspection and external human/
machine handoff remain accepted. Full project preservation, publication and verified safe
resume are not complete. Authority comes from current user/project policy, never saved
continuity or quota alone. [Complete mission](V3_MISSION.md), including all 100 architectural
keypoints, remains authoritative. V1/V2 remain accepted.

THE GUARDIAN OBSERVES. CODEX PRESERVES. PRESERVE BEFORE EXPANDING.

## CURRENT SESSION BLOCK

2026-09-22, deliberate local checkpoint continuation. Before modifications, verified root,
clean main, recent implementation/docs commits and fetched/live publication. Local HEAD =
origin/main = live refs/heads/main = `d0c320fb9e4b722f3bfcaca10094c8a71a58c3c6`.
This confirms the prior handoff publication checkpoint; no recovery discrepancy existed.
Read complete V3 mission/progress, README, AGENTS, decisions, inherited V2 mission and
required architecture/security/policy/acceptance records. The current user's scoped
continuation authorizes the recorded local-checkpoint candidate; no new confirmation needed.

Completed only that coherent block: current explicit authority, deliberate staging/content
policy, fresh prechecks, project writer exclusion, normal local commit verification and
truthful handoff/failure behavior. All mutation fixtures are disposable Linux repositories.
No target publication or next architectural phase was begun.

## COMPLETE

- New `cgc.checkpoint.checkpoint` Python adapter: exact project, expected existing HEAD and
  branch, current `policy_reviewed=True`, reviewed file SHA256 mapping and MANUAL attempt.
  Caller approval is an attestation, not a cryptographic capability or persisted grant.
- Literal explicit file staging with 64-path/1 MiB-file/4 MiB-total bounds, no-follow regular
  text reads, sensitive/generated path and recognizable-content refusal. Whole staged index
  must equal original index plus approved blobs/modes. Unselected/ignored work stays in place.
- Refusal of existing staged/intent-to-add work, operation/conflict/hidden-index/complex
  layouts, executable hooks requiring separate policy, attribute transformations and foreign
  locks. No hook bypass, implicit identity, arbitrary shell, config rewrite or rollback.
- Persistent private project-level flock coordinates CGC peers across handoff-store choices;
  fresh identity/HEAD/branch/config/index/content checks surround Git mutation.
- Durable CHECKPOINTING handoff precedes staging. Normal commit verified by new HEAD, exact
  tree/index, unchanged branch and exactly one expected parent. Final local receipt persists
  with curated project test failures and NEXT_EXACT_ACTION; no false safe-resume claim.
- Failures preserve staged work, objects, commits and prior handoff evidence. Post-commit
  uncertainty is explicit; failed final handoff cannot erase the returned verified receipt.
- Twenty-three tests including four synchronized SIGKILL stages, cross-process lock exclusion,
  restart release, real Git identity failure, injected faults and fresh-process handoff reads.

## PARTIAL

Full V3 preservation remains PARTIAL. Local checkpoint evidence is real adapter observation;
project tests remain caller-curated and are not executed. A final saved attempt deliberately
ends PARTIAL, outer SAFE_TO_RESUME UNKNOWN. Full Git/test reconciliation and safe-to-close
proof are not implemented. See [exact contract](V3_CONTRACT.md#deliberate-manual-local-checkpoint)
and [acceptance matrix](V3_ACCEPTANCE.md). Selection may preserve only part of dirty work.

## NOT_STARTED

Target push/remote verification, preserve CLI, project test runner, full fresh-process
reconciliation, Guardian authority integration and automatic preservation. Dedicated executor
SIGINT/SIGTERM adapters and in-command Git crash acceptance remain pending. Agent Gateway,
Capability Model runtime, Control/Data Planes, Router/Event Bus, transport/tunnels, CWM/HHS/ARX
integration, local/cloud AI orchestration, master orchestrator, resume generator, GUI/mobile
and V4 remain NOT_STARTED; none was authorized as an extension of this block.

## TESTS PASSED

Baseline canonical suite: **222 passed in 20.210s**.
First focused discovery: **44 passed in 2.972s**, consisting of 15 new tests plus 29 imported
inspection tests accidentally recollected. Changed helper import to avoid duplicate discovery;
no existing test changed. Expanded focused runs: **20 passed in 2.814s**, **20 in 2.721s**,
then **23 in 2.871s**. No observed runtime assertion failure during this block.

Final canonical full regression after the final content-read safety adjustment:

```bash
TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -q
```

```text
Ran 245 tests in 22.042s
OK
```

**245 passed; zero failures, errors or skips.** Composition: 153 V1/V2 + 22 attempt +
29 inspection + 18 handoff + 23 checkpoint. All prior 222 tests and existing runtime files
are unchanged. All permission-sensitive fixtures use Linux-native /tmp; no live sensor.

Publication checks: 26 Python files parse, three JSON files parse, 138 local Markdown file
links resolve after the final progress rewrite. All 50 tracked/new CGC files screened.
Only two recognizable credential-URL findings: previously reviewed deliberate synthetic
fixtures in test_handoff.py and test_inspection.py. No real credentials used or displayed;
pattern screening is not proof of universal absence. Final documentation/link/whitespace,
CLI-help and diff checks passed; exact publication evidence follows Git operations. An initial
keypoint-check assertion counted every numbered mission list, not just the architectural
section. Corrected the checker scope: exactly keypoints 1 through 100 pass; mission unchanged.

## TESTS REMAINING

No observed failure remains for this scoped block. Future publication tests need local bare
remotes, explicit remote identity/branch/forward-only policy, push failures, independent ref
comparison and local-checkpoint-only outcomes. Later full acceptance needs actual project test
receipts, in-command mutation interruptions, fresh-process Git/test reconciliation and canonical
Guardian gating. No live quota read is needed for the next block.

## KNOWN FAILURES / LIMITATIONS

No unresolved observed deterministic failures. Native POSIX permissions required; /mnt/c
security is not weakened. Existing staged work is refused and preserved, including staging
left by a failed attempt; caller reconciliation is required before another attempt. Unborn,
detached, complex layouts and executable hooks/attributes are intentionally unsupported.

The lock coordinates CGC only. Owner-controlled quiescent targets required; no hostile
same-user/path-race or noncooperating-writer isolation, hard CPU/RSS/syscall deadline or
universal power-loss guarantee. SIGKILL during a Git child cannot promise child cleanup.
Crash boundaries tested around completed Git commands, not inside every Git transaction.

After commit-attempt failure/death, HEAD may have advanced without a verified receipt. Do
not retry blindly: inspect Git and durable CHECKPOINTING/latest-failure state. Failed storage
cannot guarantee a durable failure marker. Final receipt-write failure may leave a verified
commit only in Git and the returned result; retain/reconcile that checkpoint. Persistent lock
inode is never deleted. Common secret scanning cannot prove arbitrary text/history safe.

## IMPORTANT DISCOVERIES / ARCHITECTURE

Intent-to-add can look unstaged in porcelain; explicitly refuse it so unselected index state
cannot enter a checkpoint. Compare the entire index, not merely selected diff names. Content
digests and exact Git blob identities bind screened bytes without exporting their contents.
Do not read an existing file when the selection only authorized its deletion-as-absent.

Reuse inspection's restricted fixed-Git transport, private-file checks, attempt transitions
and HandoffStore. No V2 schema changes. Add a small manual adapter rather than a speculative
capability framework. Control Plane authorization, transport/Data Plane and factual events
remain architecture only. Private context stays local; cloud export requires separate policy.
Information is not authority, and a local Git receipt is not remote preservation/safe resume.

## FILES CREATED / MODIFIED

Created: `src/cgc/checkpoint.py`, `tests/test_checkpoint.py`.
Modified: `README.md`, `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/DATA_MODEL.md`,
`docs/PRESERVATION_POLICY.md`, `docs/SECURITY_MODEL.md`, `docs/ROADMAP.md`,
`docs/DECISIONS.md`, `docs/V3_CONTRACT.md`, `docs/V3_ACCEPTANCE.md`,
`docs/V3_PROGRESS.md`, `tests/README.md`.
Existing runtime, all prior tests, complete V3 mission and inherited V2 records unchanged.
No dependency added.

## DO_NOT_REPEAT

Do not redo accepted V1/V2 experiments or V3 blocks absent demonstrated defects. No repeated
live quota reads, authentication access, automatic retries/rollback, blind staging, force push,
security weakening or unrelated project mutation. Never treat stored approval text, a handoff,
a Git process exit, a synthetic record or NEXT_EXACT_ACTION as current execution authority.
Do not infer that LOCAL_CHECKPOINT means all dirty files, project tests or safe resume verified.

## NEXT_EXACT_ACTION

In the next scoped session, first reconcile actual Git/source/tests/mission/progress and
publication. The next coherent V3 candidate is **explicit target publication and independent
remote verification in disposable Linux repositories with local bare remotes**. Define
separate current publication authority, approved remote identity/branch and forward-only
prechecks; build on the local checkpoint receipt and project lock; prove matching local,
tracking and live remote refs, truthful push failure and retained local-checkpoint-only state.
Do not introduce a live target remote, Guardian automation, Fabric, resume generator or V4
as an incidental extension. This session ends after verified CGC checkpoint publication.

## LAST SAFE CHECKPOINT

Entry and prior published handoff checkpoint: `d0c320fb9e4b722f3bfcaca10094c8a71a58c3c6`.
Local-checkpoint implementation: `eb66ff297c9aac81ae2845bde5a9e24122f775eb`.
Final publication-evidence documentation checkpoint: **HEAD after normal commit/publication**.
Its resolved hash is reported after Git operations; no self-containing hash is fabricated.

## PUBLICATION STATE

Implementation checkpoint **REMOTE_VERIFIED** on 2026-09-22. Normal forward push to
chatgptopenaiagi/CREDID-GUARDIAN-CODEX main succeeded. Independent comparison found local HEAD,
origin/main and live refs/heads/main all equal `eb66ff297c9aac81ae2845bde5a9e24122f775eb`;
working tree clean. This documentation follow-up records that observed result. Its own HEAD
is checked after normal commit/push; resolved equality belongs in the final report.
No target-project network publication was exercised. If this follow-up cannot be published,
retain its local checkpoint and report LOCAL_CHECKPOINT_ONLY.

## OPERATIONS / INTEGRITY

Session live quota reads **0**; V3 **0**; V2 **0**; historical V1 **1**. No reliable available
capacity indicator or quota threshold crossing observed. Target network/publication operations
**0**; local staging/commits exercised only in disposable Linux fixtures. CGC-only network
operations are fetch/ref checks and authorized normal forward publication. Temporary /tmp
fixtures/processes cleaned by tests. No installations, persistent environment/system/security
changes, authentication inspection, default cache creation, services or background monitoring.
No unrelated repository writes. Inherited V2 read-only HHS integrity check found clean main
at unchanged `280b7090edf51aadf694db04d6d5f6bceff289a2`; no HHS file was opened or modified.

Publication-evidence follow-up modifies only V3 progress and acceptance row 41. Runtime/tests
match the 245-test implementation checkpoint; no redundant regression rerun. Changed-doc link
and whitespace checks pass before the normal forward documentation commit.
