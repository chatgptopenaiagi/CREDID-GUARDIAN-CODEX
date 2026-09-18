# CREDID GUARDIAN CODEX — CGC V2 progress

Overall: **PARTIAL**. Authoritative specification: [V2_MISSION.md](V2_MISSION.md).

THE GUARDIAN OBSERVES. CODEX PRESERVES.
PRESERVE BEFORE EXPANDING.

## Session block

2026-09-18: freshness + provenance (mission 11, 12, 14, 47 and aligned status),
exactly the previous NEXT_EXACT_ACTION. Verified clean repository, fetched origin,
and verified local HEAD = origin/main = live remote main =
`54b51bf1b2e7dd3b1510f0b6703199ea9130785d` before implementation.
Read the complete mission, handoff and required project memory. No next unit started.

## COMPLETE

- Canonical FRESH / STALE / UNKNOWN / ERROR assessments, with local observation and
  evaluation times, age, configured maximum age and fixed reason codes. Freshness is
  independent of applicability and refresh health. Exactly maximum age is FRESH;
  greater age is STALE. Future time is ERROR; missing time UNKNOWN; malformed time ERROR.
- Existing max_age_seconds / --max-age configuration retained: integer 1–86400,
  default 900, rejecting booleans, fractions, nonfinite values and invalid types.
- Current policy requires fresh, usable, applicable data and a successful refresh.
  Failed refresh retains evidence but withholds current policy even while its age is fresh.
  Stale arrivals cannot replace last-known-good. Clock/observation regression is rejected.
- Latest and last-known-good assessments are independent. CURRENT / RETAINED /
  HISTORICAL / UNAVAILABLE describe storage role; DIRECT / DERIVED / UNAVAILABLE
  describe value origin. Source/backend time stays unavailable rather than guessed.
- Human/JSON output agrees on freshness, disposition, origins and historical evidence.
  Read-time evaluation recomputes age without writing or reading the source.
- Schema cgc-state-v2.3 persists a reconstructed, validated write-time temporal snapshot.
  Older caches are rejected without migration/deletion. Policy cgc-applicability-v2.2
  and V1 normalization remain unchanged. Atomic publication, 256 KiB bound and private
  permission checks remain intact; maximum 96-window retained state is tested.

## PARTIAL

V2 acceptance remains PARTIAL. Real source applicability, backend sample age and live
reliability remain UNKNOWN. No real live policy is currently available through the CLI.
Default-path conflict preflight, remaining crash/Ctrl+C coverage and final mission matrix
acceptance remain pending. Native Windows is unsupported; Linux-native storage is required
for private POSIX cache permissions. Human /status comparison remains PENDING / NOT VERIFIED.

## NOT_STARTED

One-shot refresh CLI; optional V2 live verification (zero consumed); V3; hooks;
automatic external preservation; GUI/tray; services; native Windows transport.

## TESTS PASSED

Baseline: 87 tests passed in 2.065s. Final command:

```bash
TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -q
```

**115 tests passed in 2.184s; zero failures, errors or skips.** 28 new tests cover
fresh/stale/boundary/missing/malformed/future times, independent historical age, newer and
regressing observations, refresh failure with/without history, recovery, direct/derived
origins, unknown applicability, invalid values, configuration, human/JSON consistency,
cache round-trip/tampering/old schema, clock rollback, 96 windows and read/write size bounds.
One existing expectation intentionally changed: failed refresh no longer authorizes a
current RED conclusion; historical RED remains visible. No tests or V1 coverage removed.

Test-first run exposed missing freshness interface (one import error). Intermediate
22-test run exposed missing CLI fields/labels (one failure, one error). All resolved;
109 then 115 tests passed. No unresolved deterministic failure.

## TESTS REMAINING

Refresh CLI tests first in its own block; remaining crash/Ctrl+C cases; default-path
preflight and full mission acceptance audit. No live test is needed for freshness.

## KNOWN_FAILURES

None unresolved in this block. Source applicability and backend age are evidence limits,
not inferred successes. Old cache versions intentionally fail closed.

## IMPORTANT_DISCOVERIES

Freshness of retained bytes can remain FRESH after a refresh ERROR; policy authority is
still withheld. Calculation origin must remain separate from retention role. Persisted
age is only a write-time snapshot, never read-time authority. No clock tolerance is
introduced. Local completion time is not proof of backend sample freshness.

## FILES_CHANGED

Created: tests/test_freshness.py.
Modified runtime: src/cgc/engine.py, src/cgc/__main__.py, src/cgc/daemon.py.
Modified existing test: tests/test_policy_config.py.
Modified docs: README.md, AGENTS.md, docs/ARCHITECTURE.md, docs/DATA_MODEL.md,
docs/PRESERVATION_POLICY.md, docs/ROADMAP.md, docs/SECURITY_MODEL.md,
docs/DECISIONS.md, docs/V2_OPERATIONS.md, docs/V2_PROGRESS.md, tests/README.md.
Cache implementation and original V1 reader/tests unchanged.

## DO_NOT_REPEAT

Do not redo thresholds, applicability or freshness blocks; do not repeat V1 live
experiments or poll quota to learn semantics. Do not migrate/delete old caches silently,
weaken permissions, touch unrelated repositories or begin V3.

## NEXT_EXACT_ACTION

Verify the latest published checkpoint and read the complete mission/handoff. Implement
one separate **one-shot refresh CLI** block (mission 20 and 63.10): write synthetic
failure/success/configuration/lock/cache tests first, reuse the existing bounded reader,
configuration, engine and private atomic cache with shared writer exclusion. Preserve
freshness, provenance, applicability evidence, retained history and synthetic isolation.
Do not claim unverified live applicability. Complete/test/document/checkpoint/push only
that unit; no live quota reads, V3 or automatic external preservation. Then record the
remaining crash/Ctrl+C/default-path preflight/final acceptance work for a later block.

## LAST_SAFE_COMMIT

Starting published checkpoint: `54b51bf1b2e7dd3b1510f0b6703199ea9130785d`.
Freshness checkpoint: **HEAD after commit/publication**; resolved hash and verified
local/tracking/live equality are reported after Git operations. Normal forward push only.
If publication fails, record LOCAL_CHECKPOINT_ONLY.

## Operations and integrity

V1 historical live reads: 1. V2 session and total live quota reads: **0**.
No installs, persistent system/environment changes, default cache creation, credential
inspection or unrelated repository writes. Synthetic tests use disposable Linux /tmp
storage. Temporary documentation/validation scripts are removed before stopping.
No reliable capacity indicator or threshold crossing was observed; preservation is scoped.
Public Git author metadata may be supplied per command without persistent configuration.
Publication gate results follow after execution.

Publication gates passed: 14 Python files parsed, three JSON files parsed, 50 local
Markdown targets resolved; top-level/status/daemon help passed without source access.
V1 reader and original tests, mission text and verbatim preservation directives remain
byte-for-byte unchanged. Bounded recognizable credential-pattern scan: zero matches
(not a guarantee of universal secret absence). Git diff whitespace passed. Runtime and
test diff reviewed. HHS read-only check: clean main at unchanged
`280b7090edf51aadf694db04d6d5f6bceff289a2`; no unrelated repository was modified.
