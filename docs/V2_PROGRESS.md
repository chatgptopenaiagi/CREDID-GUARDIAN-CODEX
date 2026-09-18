# CREDID GUARDIAN CODEX — CGC V2 progress

Overall: **PARTIAL**. Authoritative specification: [V2_MISSION.md](V2_MISSION.md).

THE GUARDIAN OBSERVES. CODEX PRESERVES.
PRESERVE BEFORE EXPANDING.

## Session block

2026-09-18: crash and interruption safety (mission 28, 29, 55, 56), exactly the prior
NEXT_EXACT_ACTION. Verified clean repository root, fetched origin, and verified
local HEAD = origin/main = live remote main =
`36197f33a6437e44c6c95b01815c159628133704` before modifications.
Read the complete mission, current handoff, README, AGENTS and decisions; preserved
project memory and V1 source/tests were already read during this resumed conversation.
Audited existing exception-injection, exclusion, timeout and SIGTERM tests before additions.

## COMPLETE

- Real-process SIGKILL at six deterministic rendezvous points: before refresh, during
  synthetic refresh, after valid observation/evaluation, during partial temporary write,
  before atomic replace and immediately after replace. Each runs with absent and existing
  state. Before replace, old bytes (or absence) survive; after replace, complete new state.
- Competing writer refused while each crash peer holds its lock. Kernel releases the lock
  after death. Restart validates and publishes successfully in the same directory.
- Partial/complete abandoned temporary siblings retain private 0600 permissions, are never
  interpreted as canonical state, and remain untouched by later publication.
- Actual CLI SIGINT during daemon wait, daemon read and one-shot refresh read; in-flight
  successful synthetic result finishes/publishes exactly once, with no second read.
- SIGINT during daemon/refresh transport timeouts and SIGTERM during refresh timeout:
  actual V1 transport runs a synthetic Python child. Explicit child startup handshake
  confirms TERM-ignore handler installed; cleanup escalates to SIGKILL and reaps it.
  Failure publication retains last-known-good; no fabricated exhaustion or live policy.
- Runtime already satisfied these tests: no source changes or schema changes necessary.
  Existing 133 tests preserved unchanged. No live source or default-cache access.

## PARTIAL

Overall V2 acceptance remains PARTIAL pending default-target conflict preflight and full
mission acceptance audit. Live applicability, backend sample age and sustained reliability
remain UNKNOWN. Native Windows remains unsupported. Human /status comparison is
PENDING / NOT VERIFIED and is not a V2 blocker.

## NOT_STARTED

Optional V2 live verification (zero consumed); V3; automatic external preservation;
hooks; GUI/tray; services; native Windows transport.

## TESTS PASSED

Baseline: **133 tests passed in 2.258s**. New test-first process suite:
**12 passed in 11.306s**, with no runtime modification or test failure.
Strengthened synthetic transport startup synchronization and verified SIGKILL reaping.

```bash
TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -q
```

Final: **145 tests passed in 13.539s; zero failures, errors or skips.**
12 new test methods include 12 crash cases (six stages with/without prior state) and six
signal cases. Parent/child pipe rendezvous replaces timing guesses; waits have bounded
test deadlines. Tests use disposable Linux-native temporary directories and local Python
processes only. Existing policy, freshness, provenance, refresh CLI and V1 tests unchanged.

## TESTS REMAINING

Default-target conflict preflight and full mission matrix audit. Review any gaps identified
by that audit before claiming V2 COMPLETE. No repeated live experiment needed.

## KNOWN_FAILURES

No deterministic failures occurred in this block. No unresolved runtime regression found.

## IMPORTANT_DISCOVERIES

Atomic visibility survives abrupt process death at the tested stages. This is not a
power-loss durability guarantee. A crash before publication leaves no new failure record;
consumers still assess retained observation age. Temporary crash artifacts may accumulate;
CGC deliberately does not guess ownership or delete unknown files. Graceful SIGINT/SIGTERM
allows a bounded in-flight read to finish and publish; it does not instantly abort it.
SIGKILL cannot run CGC cleanup: descendant lifetime after abrupt parent death is not
promised or tested as bounded. Crash-stage fixtures use an in-process synthetic sensor;
separate graceful-signal tests verify real transport child cleanup. OS scheduling prevents
hard realtime guarantees. Preserve these limits rather than claiming universal recovery.

## FILES_CHANGED

Created: tests/test_interruption.py; tests/helpers/interruption_peer.py.
Modified documentation: README.md, AGENTS.md, docs/ARCHITECTURE.md, docs/DATA_MODEL.md,
docs/PRESERVATION_POLICY.md, docs/ROADMAP.md, docs/DECISIONS.md,
docs/V2_OPERATIONS.md, docs/V2_PROGRESS.md, tests/README.md.
All src/cgc runtime files and previous tests unchanged.

## DO_NOT_REPEAT

Do not redo completed policy/applicability/freshness/refresh or crash tests without new
regression evidence. Do not repeat V1 experiments, poll to infer applicability, inspect
authentication stores, weaken cache permissions, delete unknown crash artifacts, mutate
unrelated projects or start V3.

## NEXT_EXACT_ACTION

Verify the published checkpoint, then read the complete mission/handoff. Complete one
bounded **default-cache target preflight and V2 acceptance audit** block (mission 13, 17,
46, 63): inspect only metadata for the exact proposed ~/.codex/cgc target and necessary
ancestors; never enumerate/open unrelated Codex or authentication files. Verify no protected
path conflict before actual default-path use, and add synthetic conflict/path tests if the
audit shows missing enforcement. Keep actual quota reads at zero unless separately needed
under the mission's one-read ceiling; prefer explicitly skipping live verification with
rationale. Audit every V2 success criterion against preserved implementation/tests and
record COMPLETE/PARTIAL with exact evidence and residual limits. Fix only demonstrated
in-scope gaps, then test/document/checkpoint/push and stop. V3 requires separate authorization.

## LAST_SAFE_COMMIT

Starting checkpoint: `36197f33a6437e44c6c95b01815c159628133704`.
Crash/interruption checkpoint: **HEAD after commit/publication**, resolved hash and
local/tracking/live equality reported after Git operations. Normal forward push only.
If publication fails, record LOCAL_CHECKPOINT_ONLY.

## Operations and integrity

V1 historical live reads: 1. V2 session and total live quota reads: **0**.
No installations, persistent system/environment changes, default cache creation, auth
inspection or unrelated repository writes. Used disposable /tmp caches and synthetic
processes. Temporary documentation/validation scripts removed before stopping.
No reliable capacity indicator or threshold crossing observed; preservation is scoped.
Git public author identity may be supplied per command without persistent configuration.
Publication gate results follow after execution.

Publication gates passed: 17 Python files parse, three JSON files parse and 56 local
Markdown targets resolve. All runtime files, prior tests, mission text and verbatim
preservation directives match the starting checkpoint. Bounded recognizable credential-
pattern screening found zero matches (not a universal secrecy guarantee). Test harness
and documentation diff reviewed; Git whitespace passed. HHS read-only integrity check:
clean main at unchanged `280b7090edf51aadf694db04d6d5f6bceff289a2`.
