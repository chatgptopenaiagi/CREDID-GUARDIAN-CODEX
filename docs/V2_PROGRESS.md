# CREDID GUARDIAN CODEX — CGC V2 progress

Overall: **COMPLETE — offline POSIX acceptance**, subject to final publication verification
for this HEAD. Authoritative specification: [V2_MISSION.md](V2_MISSION.md).
Full evidence matrix and residual limits: [V2_ACCEPTANCE.md](V2_ACCEPTANCE.md).

THE GUARDIAN OBSERVES. CODEX PRESERVES.
PRESERVE BEFORE EXPANDING.

## Session block

2026-09-19: default-cache target preflight and final V2 acceptance audit (mission 13, 17,
46, 63), exactly the previous NEXT_EXACT_ACTION. Verified clean repository, fetched origin,
and checked local HEAD = origin/main = live remote main =
`9d002936c145a758fb2c6a1893f7c4a4df0517ba` before modifications. Reread complete mission,
progress, README, AGENTS and decisions; audited preserved source, tests and project memory.

## COMPLETE

- Exact default-target metadata preflight: /home/love/.codex is an owned non-symlink
  directory (0755), home is owned 0700, ancestors are directories with no symlink in
  the checked chain, and ~/.codex/cgc is absent. No observed protected-path conflict.
  No directory enumeration, unrelated/authentication file open, default cache creation
  or mode change. This is point-in-time evidence; runtime no-follow checks still apply.
- Eight new synthetic-home tests: absent parent status/read behavior, refusal to create
  the Codex parent, creation of only CGC child, no sibling read/enumeration, default vs
  explicit path status equivalence, parent symlink, file/dangling-link/public-directory
  target conflicts and state symlink/hardlink aliases. Existing enforcement passed;
  no production change or security relaxation was necessary.
- Mission 63's twenty acceptance criteria audited with named implementation/test evidence.
  Offline policy/applicability/freshness/cache/status/refresh/daemon/crash/security acceptance
  is complete. Normal publication and live-ref equality are checked after this commit.
- All V2 components and their limits documented. No schema change: cgc-state-v2.3,
  policy cgc-applicability-v2.2. Source normalization remains 0.1.0-provisional.
- Optional V2 live verification explicitly SKIPPED: synthetic coverage and preserved V1
  evidence validate this implementation; another percentage snapshot would not prove
  window applicability, backend age or sustained reliability. V2 live reads remain zero.

## PARTIAL

No required V2 implementation/test block remains partial after this audit. Operational
knowledge remains limited: actual live applicability, backend sample age, supported
polling cadence and sustained live reliability are UNKNOWN. Human /status comparison
is PENDING / NOT VERIFIED, explicitly permitted by the mission. These are not fabricated
successes or production-readiness claims. See acceptance limits below and in V2_ACCEPTANCE.

## NOT_STARTED

V3 — CODEX PRESERVATION INTEGRATION; automatic external project preservation; hooks;
GUI/tray; services; native Windows transport. They require separate authorization.
Optional live verification is SKIPPED, not consumed or silently deferred as required work.

## TESTS PASSED

Baseline: **145 tests passed in 13.818s**. Eight new test-first default-path tests all
passed in 0.024s against unchanged runtime; no regression exposed.

```bash
TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -q
```

Final: **153 tests passed in 13.630s; zero failures, errors or skips.**
All prior 145 tests unchanged. Original V1 reader and 32 tests unchanged. No source read
was made except synthetic peers/injected fixtures. Permission-sensitive storage uses /tmp.

## TESTS REMAINING

None required by this V2 offline acceptance matrix. Future upstream compatibility/live
applicability investigations, native Windows support and V3 integration need separately
scoped authorization and tests. No automatic repeat of V1 or live monitoring.

## KNOWN_FAILURES

No deterministic failures in this block. Old cache schemas intentionally fail closed.
The Windows-mounted workspace cannot enforce private POSIX modes; use Linux-native storage.
No universal power-loss durability, same-user tamper resistance or bounded descendant
cleanup after SIGKILL of CGC is claimed. Private crash temp files may remain.

## IMPORTANT_DISCOVERIES

The exact default target is absent and does not collide with an observed protected path.
Existing descriptor-relative no-follow/private-file checks already enforce the tested
conflict boundaries; new preflight runtime/configuration machinery was unnecessary.
Completion means the stated V2 offline success criteria are satisfied, not that live
windows are known applicable. UNKNOWN is the required truthful result without evidence.
The production CLI currently cannot produce a live policy/directive; selection is not proof.

## FILES_CHANGED

Created: tests/test_default_cache.py; docs/V2_ACCEPTANCE.md.
Modified docs: README.md, AGENTS.md, docs/ARCHITECTURE.md, docs/DATA_MODEL.md,
docs/PRESERVATION_POLICY.md, docs/ROADMAP.md, docs/SECURITY_MODEL.md,
docs/DECISIONS.md, docs/V2_OPERATIONS.md, docs/V2_PROGRESS.md, tests/README.md.
All runtime files and previous tests unchanged.

## DO_NOT_REPEAT

Do not redo completed V1/V2 blocks, repeat live quota reads, infer applicability from
selection/names/percentages, inspect auth stores, weaken permissions, delete unknown
crash artifacts, mutate unrelated projects or infer V3 authorization from this handoff.

## NEXT_EXACT_ACTION

Verify this final V2 checkpoint and its publication, then **STOP**. No V2 implementation
block remains scheduled. Await a separately scoped authorized mission. The proposed next
version is CGC V3 — CODEX PRESERVATION INTEGRATION, but it is NOT_STARTED and is not
authorized by this handoff. Any future live-applicability investigation must preserve
explicit UNKNOWN until supported evidence exists; do not repeat reads merely to guess.

## LAST_SAFE_COMMIT

Starting published checkpoint: `9d002936c145a758fb2c6a1893f7c4a4df0517ba`.
Final V2 acceptance checkpoint: **HEAD after commit/publication**. Resolved hash and
verified local HEAD = origin/main = live remote main belong in the final report.
Normal forward push only. If publication fails, record LOCAL_CHECKPOINT_ONLY and do not
claim criterion 63.20 or overall publication complete.

## Operations and integrity

V1 historical quota reads: 1. V2 session and total live quota reads: **0**.
No installations, persistent environment/system changes, default cache creation or unrelated
repository writes. Actual default-path inspection was metadata-only on necessary ancestors
and exact target. No Codex directory listing or authentication-file inspection.
Synthetic private /tmp caches removed by tests; temporary scripts removed before stopping.
No reliable capacity indicator or threshold crossing observed. Per-command public Git
author metadata only, no persistent configuration change. Publication gate results follow.

Publication gates passed: 18 Python files parse; three JSON files parse; 82 local
Markdown targets resolve; top-level/status/refresh/daemon help succeeds without source
access. All runtime, prior tests, mission text and verbatim preservation directives
match the starting checkpoint. Bounded recognizable credential-pattern screening found
zero matches (not proof of universal secret absence). New test and acceptance/documentation
changes reviewed; Git whitespace passed. HHS read-only check: clean main at unchanged
`280b7090edf51aadf694db04d6d5f6bceff289a2`. No unrelated project was modified.
