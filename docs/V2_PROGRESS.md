# CREDID GUARDIAN CODEX — CGC V2 progress

Overall: **PARTIAL**. Authoritative specification: [V2_MISSION.md](V2_MISSION.md).

THE GUARDIAN OBSERVES. CODEX PRESERVES.
PRESERVE BEFORE EXPANDING.

## Session block

2026-09-18: one-shot refresh CLI (mission 20, 61, 63.10), exactly the previous
NEXT_EXACT_ACTION. Verified repository root and clean main; fetched origin and verified
local HEAD = origin/main = live remote main =
`b170491e8d2afad320517370d3f3006b48733f8f` before modifying anything.
Read the complete authoritative mission, progress and required preserved project memory.

## COMPLETE

- `python -m cgc refresh --live --bucket codex` performs at most one bounded reader
  attempt, validates/evaluates and atomically publishes through the shared daemon path.
  No retry, polling interval, sleep or catch-up. --max-reads/--interval are rejected.
- Same private writer lock spans cache validation, source read and publication. Lock,
  corruption, old schema, configuration mismatch and unsafe paths block source access.
- Existing bucket, threshold, max-age and timeout configuration reused; invalid scope,
  age, timeout and thresholds rejected before cache creation. Explicit --live and
  --bucket required. No CLI applicability override or synthetic source argument added.
- Human/JSON output shares status rendering and exit semantics. Reports this writer's
  resulting snapshot, avoiding a post-unlock reread of another writer's generation.
  Status remains cache-only. Production applicability remains UNKNOWN.
- Failure metadata preserves last-known-good and withholds current authority. Synthetic
  state never becomes live policy. Pre-read cancellation skips read/publication; signal
  handlers are restored. In-flight reads retain the existing bounded completion behavior.
- Cache schema cgc-state-v2.3, policy cgc-applicability-v2.2, 256 KiB bound, private modes,
  normalization, freshness and applicability rules unchanged. All prior tests preserved.

## PARTIAL

Overall V2 acceptance is PARTIAL: remaining crash/Ctrl+C coverage, default-path conflict
preflight and final mission matrix audit remain pending. Real applicability, backend
sample age and sustained live reliability remain UNKNOWN. Native Windows unsupported.
Human /status comparison remains PENDING / NOT VERIFIED, not a V2 blocker.

## NOT_STARTED

Optional V2 live verification (zero consumed); V3 preservation integration; automatic
external preservation; hooks; GUI/tray; service installation; native Windows transport.

## TESTS PASSED

Baseline: **115 tests passed in 2.193s**. Test-first import failed because refresh_once
was not yet implemented (one loader error, zero new test bodies). After implementation,
129 tests passed in 2.279s. Added four production-reader-path/path/cancellation cases.

```bash
TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -q
```

Final: **133 tests passed in 2.234s; zero failures, errors or skips.**
18 new tests cover one read/no wait, safe human/JSON output, synthetic isolation,
UNKNOWN applicability, retained failure with/without history, configuration forwarding,
pre-creation rejection, cache mismatch/corruption/old schema, shared locking, write
failure preservation, signal handler restoration, simulated production normalization/
timeout, unsafe path refusal and pre-read cancellation. No prior tests changed/deleted.
No live source was used; injected transport data labeled live is explicitly simulated.

## TESTS REMAINING

Remaining deterministic crash-stage and real-process Ctrl+C coverage, default-path
conflict preflight, then complete V2 acceptance matrix review. Optional bounded live
verification remains unused; it is not needed to validate this CLI block.

## KNOWN_FAILURES

None unresolved in this block. The expected test-first missing-interface error is resolved.
Older cache schemas intentionally fail closed. Unknown applicability is not a successful
policy result, even when the source supplied valid percentages.

## IMPORTANT_DISCOVERIES

Refresh should report its own published state, not reread after releasing writer exclusion.
The shared runner now returns a state snapshot internally; the public daemon run function
retains its attempt-count return. CLI exits match status (0 current usable live policy,
1 unavailable/unknown/synthetic policy or refresh failure, 2 argument/config/cache errors).
Thus a successful source read can still exit 1 and publish useful UNKNOWN diagnostics;
this must not trigger automatic repeated reads. Production has no verified live contract.

## FILES_CHANGED

Created: tests/test_refresh_cli.py.
Modified runtime: src/cgc/__main__.py, src/cgc/daemon.py.
Modified docs: README.md, AGENTS.md, docs/ARCHITECTURE.md, docs/DATA_MODEL.md,
docs/PRESERVATION_POLICY.md, docs/ROADMAP.md, docs/DECISIONS.md,
docs/V2_OPERATIONS.md, docs/V2_PROGRESS.md, tests/README.md.
Engine, cache, V1 reader and all previous tests unchanged.

## DO_NOT_REPEAT

Do not redo completed threshold/applicability/freshness/refresh blocks. Do not repeat
V1 live experiments, poll to resolve applicability, inspect credentials, weaken private
permissions, silently migrate/delete caches, touch unrelated projects or begin V3.

## NEXT_EXACT_ACTION

Verify the published checkpoint and read the full mission/handoff. Complete one bounded
**crash and interruption safety** block (mission 28, 29, 55, 56): audit existing tests,
then add deterministic synthetic process tests for missing termination stages before/
during refresh, after observation and during temporary write/before replace, plus real
SIGINT/Ctrl+C shutdown for daemon and one-shot refresh. Verify coherent old-or-new cache,
retained history, bounded child cleanup and writer-lock release. Fix only demonstrated
in-scope failures; do not weaken POSIX permissions or use live quota. Validate/document/
checkpoint/push that unit only. Leave default-target conflict preflight and final full
mission acceptance audit for the subsequent coherent block. Do not begin V3.

## LAST_SAFE_COMMIT

Starting published checkpoint: `b170491e8d2afad320517370d3f3006b48733f8f`.
Current refresh checkpoint: **HEAD after commit/publication**; resolved hash and
local/tracking/live equality reported after Git operations. Normal forward push only.
If publication fails, record LOCAL_CHECKPOINT_ONLY.

## Operations and integrity

V1 historical live quota reads: 1. V2 session and total live quota reads: **0**.
No installs, persistent system/environment changes, default ~/.codex cache creation,
authentication inspection or unrelated repository writes. Disposable Linux /tmp test
storage only. Temporary documentation/validation scripts removed before stopping.
No reliable capacity indicator or threshold crossing observed; preservation is scoped.
Public Git author metadata may be supplied per command without persistent configuration.
Publication gate results follow after execution.

Publication gates passed: 15 Python files parse; three JSON files parse; 56 local
Markdown targets resolve. Refresh CLI help succeeds without source access. All previous
Python tests, V1 reader, engine, cache, mission text and verbatim preservation directives
match the starting checkpoint byte-for-byte. Bounded recognizable credential-pattern
scan found zero matches (not proof of universal secret absence). Changed runtime/tests
and documentation reviewed; Git whitespace checks passed.
HHS read-only integrity check: clean main at unchanged
`280b7090edf51aadf694db04d6d5f6bceff289a2`. No unrelated repository writes.
