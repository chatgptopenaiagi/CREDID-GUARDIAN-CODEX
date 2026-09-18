# CREDID GUARDIAN CODEX — CGC V2 progress

Overall: **PARTIAL**. Authoritative specification: [V2_MISSION.md](V2_MISSION.md).

THE GUARDIAN OBSERVES. CODEX PRESERVES.
PRESERVE BEFORE EXPANDING.

## Session block

2026-09-18: explicit per-window applicability and limiting-window reasoning (mission
10, 26, 47, 49), exactly the previous NEXT_EXACT_ACTION. No subsequent unit started.
Verified clean root `/mnt/c/Codex-Projects/CREDID-GUARDIAN-CODEX`; fetched origin and
verified local HEAD = origin/main = live remote main =
`939961cdd2dc06cb7c03ad2591f25807ae1bfdcd` before modifications.
Read mission, progress and preserved handoff. Configurable thresholds were retained.

## COMPLETE

- Per-window APPLICABLE / NOT_APPLICABLE / UNKNOWN and evidence basis, separate from
  operator selection and numeric validity. No inference from names, duration, quota
  percentages, ordinaryUsageAllowed or operator bucket selection.
- Bounded allowlisted evidence: at most 96 unique observed window IDs, exact observation
  timestamp, fixed applicability enum and SYNTHETIC_CONTRACT basis. Only synthetic
  observations accept that basis; absent evidence means UNKNOWN. No unverified live
  contract or arbitrary source-proof claim is accepted.
- Minimum over valid, selected, known applicable windows only. Sorted limiting-window
  identities include all ties; fixed reasoning codes and exclusion diagnostics retain
  invalid, unknown and out-of-scope windows. Global all-clear remains false.
- Latest evaluated observation/policy separate from last-known-good observation/policy.
  A newer UNKNOWN or invalid-window evaluation withholds current policy/limit without
  deleting last-known-good. Transport/structural failure preserves both retained pairs.
  Evidence is never silently reused on another refresh. Timestamp regression is checked
  against the latest observation, including UNKNOWN evaluations.
- Cache validation reconstructs both policies from normalized observations and evidence.
  Schema cgc-state-v2.2, policy cgc-applicability-v2.2; old schemas rejected, not migrated.
- Human/JSON status reports matching applicability, limiting identities/reason and source/
  observation time. Current limiting data is withheld when existing stale/skew/blocked
  checks disallow policy; historical reasoning remains explicitly historical.
- Daemon synthetic evidence injection for offline acceptance; production CLI supplies no
  evidence and honestly reports live applicability UNKNOWN. Existing finite bounds,
  backoff, writer lock, last-known-good behavior and threshold validation retained.
- V1 normalization and its original two test modules remain byte-for-byte unchanged.

## PARTIAL

| Mission items | Existing behavior | Remaining acceptance work |
|---|---|---|
| 11, 12, 14, 47 | Existing max-age and skew logic; applicability provenance added | Separate FRESH / STALE / UNKNOWN / ERROR field and freshness provenance |
| 13, 17, 46 | Private POSIX directory enforcement | Default target-path conflict preflight before actual use; native Windows unsupported |
| 18, 19, 50–52 | Human/JSON applicability, thresholds, limiting reasoning, source/time | Align output with separate freshness model in next block |
| 25–30, 55 | 87 passing deterministic tests | Refresh CLI, Ctrl+C and remaining crash stages; final mission matrix audit |
| 37, 38, 63 | Current docs/handoff | Full V2 acceptance remains pending |

The applicability mechanism is implemented and verified offline. Actual live source
applicability is **UNKNOWN**, not verified by the historical V1 snapshot. Any future live
contract needs preserved evidence and dedicated tests; do not invent one to make policy
GREEN. No live policy/directive is currently available through the production CLI.

## NOT_STARTED

- Separate freshness redesign and one-shot `python -m cgc refresh` CLI.
- Optional V2 live verification: **0 consumed**. Defer until offline acceptance;
  may be skipped with explicit rationale. No live monitoring session.
- CGC V3 — CODEX PRESERVATION INTEGRATION; requires separate authorization after V2.
- Hooks, automatic preservation, injection, GUI/tray, services, native Windows support.

## TESTS PASSED

```bash
TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -v
```

Final: **87 tests passed in 2.048 seconds; zero failures, errors or skips.**
Baseline: 71 passed in 1.970s. Test-first applicability run: 10 tests, one failure and
10 errors (subtest reporting included); missing evidence interfaces and the old selection
assumption were exposed. After implementation/adapting V2 fixtures: 81 passed in 1.996s.
A 96-window retained-state test exposed CACHE_SIZE_LIMIT at 128 KiB. Bounded cache size
advanced to 256 KiB for two observation/evidence pairs; 86 passed in 2.054s, then the final
multi-window boundary test brought the suite to 87. All observed failures are resolved.

Sixteen new applicability tests cover mixed 30% applicable / 2% unknown, explicit
non-applicability, no inference, invalid/unknown values, scope, deterministic ties,
all four policy bands, evidence shape/types/count/duplicates/timestamp/live isolation,
unknown refresh and recovery, transport failure, stale current-limit suppression,
cache tampering/old schemas, daemon/CLI agreement, retained diagnostics, and 96-window
cache capacity. Existing V2 fixtures now supply explicit synthetic evidence rather than
relying on selection; the old simulated-live all-clear assertion now expects UNKNOWN.
No V1 tests were modified. No source call was made by status tests.

Publication checks: Python syntax, JSON parsing, local Markdown links, CLI help,
unchanged V1 bytes/mission/verbatim directives, bounded credential-pattern screening,
Git whitespace and diff review. Results recorded below after execution.

## TESTS REMAINING

Add tests with the separate freshness block, then refresh CLI and outstanding crash/
Ctrl+C cases. Final acceptance must review the full mission matrix, not just test count.

## KNOWN_FAILURES AND DISCOVERIES

- No unresolved deterministic failure in this block.
- Selection was previously used as applicability; corrected. The preserved source
  evidence does not justify a real per-window contract, so live applicability stays UNKNOWN.
- Latest diagnostics must not erase or masquerade as last-known-good. Separate pairs
  retain both, with UNKNOWN current policy after a newer unusable evaluation.
- Expanded provenance requires more cache space: fixed 256 KiB bound, verified with 96
  long-identity windows and retained history. Source bounds and private modes unchanged.
- Unsupported old cache schemas are preserved; no automatic migration or deletion.
- Windows-mounted workspace cannot enforce required 0700; use Linux /tmp. No weakening.
- Freshness still uses the existing validity vocabulary. Backend sample age, supported
  cadence and live reliability remain UNKNOWN. Human `/status` comparison is still
  PENDING / NOT VERIFIED and is not a blocker.
- Earlier threshold-block history remains in DECISIONS.md and checkpoint 939961c.

## FILES_CHANGED

Created: `tests/test_applicability.py`, `tests/synthetic_support.py`.

Modified runtime: `src/cgc/engine.py`, `src/cgc/cache.py`, `src/cgc/daemon.py`,
`src/cgc/__main__.py`.

Modified V2 tests: `tests/test_engine.py`, `tests/test_cache_daemon.py`,
`tests/test_policy_config.py` (explicit fixture evidence; preserve their original purposes).

Modified documentation: `README.md`, `AGENTS.md`, `docs/ARCHITECTURE.md`,
`docs/DATA_MODEL.md`, `docs/PRESERVATION_POLICY.md`, `docs/ROADMAP.md`,
`docs/SECURITY_MODEL.md`, `docs/DECISIONS.md`, `docs/V2_OPERATIONS.md`,
`docs/V2_PROGRESS.md`, `tests/README.md`.

## NEXT_EXACT_ACTION

Verify this published checkpoint, then implement one **separate freshness/provenance
block** (mission 11, 12, 14, 47 plus aligned status output). Write deterministic tests
first for FRESH / STALE / UNKNOWN / ERROR, exact age boundaries, missing observations,
failed refresh with fresh/stale last-known-good, future timestamps and latest UNKNOWN
applicability distinct from historical usable data. Define and document the relationship
between observation freshness, refresh health, validity and policy availability; do not
conflate a transport error with the age of retained data. Keep existing max-age defaults
unless evidence justifies a change. Carry explicit freshness/source-time provenance
through canonical validation and human/JSON status, versioning incompatible cache changes.
Preserve applicability evidence, threshold behavior, last-known-good, synthetic isolation,
V1 normalization and cache security. Complete/test/document/checkpoint/push that unit only.
Do not implement refresh CLI, perform live reads or begin V3 in the freshness block.

## LAST_SAFE_COMMIT

Starting published checkpoint: `939961cdd2dc06cb7c03ad2591f25807ae1bfdcd`.
Current applicability checkpoint: **HEAD after commit/publication**, with resolved hash
and verified local/tracking/live equality reported after Git operations. Normal forward
push to `chatgptopenaiagi/CREDID-GUARDIAN-CODEX` main only. If publication fails, record
LOCAL_CHECKPOINT_ONLY; do not claim remote equality without checking.

## Operations and integrity

Live reads: V1 historical **1**; V2 this session **0**, V2 total **0**.
No live API/source rediscovery, default ~/.codex cache creation, auth inspection,
installation, persistent environment/system changes or unrelated repository writes.
Used disposable /tmp caches and synthetic child processes. A temporary test-result log
was used for the final test summary and is removed before stopping. No usage indicator
or threshold crossing was observed. Preservation is scope-driven.
Git author identity uses existing public commit metadata per command if needed; no
persistent configuration changes. HHS integrity checked read-only per mission item 69;
result recorded below. CGC V3 remains NOT_STARTED.

Final publication gates passed: 13 Python files parse, three JSON files parse, 43 local
Markdown targets resolve, top-level/status CLI help succeeds without source access.
V1 reader/tests, mission text and verbatim preservation directives are unchanged.
Bounded recognizable credential-pattern screening found zero matches (not proof of
universal secret absence). Changed runtime/tests/docs reviewed; Git whitespace passed.
HHS read-only integrity check: clean main at unchanged
`280b7090edf51aadf694db04d6d5f6bceff289a2`. No HHS modifications.
