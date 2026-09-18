# CREDID GUARDIAN CODEX — CGC V2 acceptance

2026-09-19. **COMPLETE — offline POSIX acceptance**, with publication of HEAD verified
at the end of the checkpoint workflow. Specification: [V2 mission](V2_MISSION.md).
Execution record, exact counts and checkpoint: [V2 progress](V2_PROGRESS.md).

Completion follows the mission's success criteria, including its explicit permission to
skip live verification and report unknown applicability. It does not mean production
readiness, live policy availability or complete knowledge of upstream semantics.

## Mission 63 acceptance matrix

All rows are satisfied by this checkpoint after its normal publication verification.

| Criterion | Evidence | Scope / limitation |
|---|---|---|
| 1. V1 tests pass | [test_quota.py](../tests/test_quota.py), [test_quota_protocol.py](../tests/test_quota_protocol.py): 32 original tests | Original reader/tests unchanged; no experiment repeated |
| 2. Policy engine | [engine.py](../src/cgc/engine.py), [test_engine.py](../tests/test_engine.py), [test_policy_config.py](../tests/test_policy_config.py) | Exact/fractional boundaries, configurable ordered thresholds |
| 3. Explicit applicability | [test_applicability.py](../tests/test_applicability.py) | UNKNOWN real source; only observation-bound synthetic assertions accepted |
| 4. Explicit freshness | [test_freshness.py](../tests/test_freshness.py) | FRESH/STALE/UNKNOWN/ERROR; local completion time, not backend age |
| 5. Canonical local state | [cache.py](../src/cgc/cache.py), engine validation, test_cache_daemon | cgc-state-v2.3; default target preflight below |
| 6. Atomic writes | [test_cache_daemon.py](../tests/test_cache_daemon.py), [test_interruption.py](../tests/test_interruption.py) | Replace/fsync and process-death stages; no universal power-loss guarantee |
| 7. Retained last-known-good | test_engine, test_freshness, test_refresh_cli, test_interruption | Failure retains evidence but cannot authorize current policy |
| 8. Human status | [__main__.py](../src/cgc/__main__.py), test_freshness, test_policy_config | Cache-only, shows uncertainty, origins and historical state |
| 9. JSON status | test_cache_daemon, test_freshness, test_refresh_cli | Allowlisted validated canonical projection; no source read |
| 10. One-shot refresh | [test_refresh_cli.py](../tests/test_refresh_cli.py): 18 tests | One bounded attempt; explicit --live/--bucket; synthetic acceptance |
| 11. Foreground daemon | [daemon.py](../src/cgc/daemon.py), test_cache_daemon | Finite max-reads, completion-based interval, no service |
| 12. Temporary errors | test_daemon_bounded_backoff_and_recovery; freshness failure/recovery tests | Capped backoff, retained history, no 0%/GREEN invention |
| 13. Clean shutdown | test_interruption SIGINT/SIGTERM cases and existing SIGTERM test | In-flight reads finish/timeout; TERM-ignoring synthetic transport killed/reaped |
| 14. Deterministic suite | 153 tests, zero failures/errors/skips | Linux-native /tmp; exact command/results in progress |
| 15. Security review | Source allowlists, corruption/alias/mode tests; bounded tracked-file scan | Zero credential-pattern matches; scan is not proof of universal secrecy |
| 16. Documentation | Mission/progress/operations/decisions and updated current-status documents | Historical V0/V1 proposals explicitly labeled |
| 17. At most one live V2 read | Zero consumed; explicitly SKIPPED | Offline evidence sufficient; no repeated monitoring |
| 18. No V3 automation | Runtime source review | No repository execution, hook, GUI or service subsystem |
| 19. HHS untouched | Read-only Git integrity check, recorded in progress | Clean at preserved 280b7090edf51aadf694db04d6d5f6bceff289a2 |
| 20. Publication | Normal forward commit/push; HEAD/tracking/live equality and clean-tree checks | HEAD self-reference; resolved hash in final report after verification |

## Default target and permission preflight (13, 17, 46)

Inspected only metadata along the exact /home/love/.codex/cgc path. /home was a non-symlink
0755 directory; home was owned 0700; .codex was owned, non-symlink 0755; cgc was absent.
No observed protected-path conflict. No sibling enumeration, authentication-file access,
default directory creation, permission changes or source calls. Metadata was obtained
relative to no-follow directory descriptors; inspection stopped at the absent target.
This is point-in-time local evidence, not a claim about all future installations.

[test_default_cache.py](../tests/test_default_cache.py) uses disposable synthetic homes.
It verifies only the CGC child is created, a missing Codex parent is not created, sibling
files are not opened/enumerated, default/explicit paths agree, and symlink/file/hardlink/
public-permission conflicts are refused without mutation. Runtime already enforces these
checks. Missing cache status does not create anything. No new marker/config file needed.

Default remains ~/.codex/cgc/state.json. Use a dedicated --cache-dir on private Linux-native
storage when appropriate. POSIX modes are not weakened for /mnt/c. Native Windows transport
and ACL support remain outside this accepted scope, as allowed by mission 46.

## Remaining mission coverage

| Mission sections | Acceptance evidence / disposition |
|---|---|
| 1–6 | Correct root/remote verified; preserved V1 evidence read; immutable identity and observer boundary retained |
| 7–12, 14–16 | Implemented engine, explicit evidence, canonical validation, age/health/origin separation and atomic retained state |
| 18–22, 25–33 | CLI/daemon/config tests; exact boundaries, malformed data, security fields and failure recovery |
| 23–24, 42, 45 | Live V2 verification skipped; zero reads; no V1 rediscovery or quota-driven traffic |
| 34–36, 64, 71 | Excluded integrations remain NOT_STARTED; no roadmap-derived authorization |
| 37–41 | Current docs updated; standard library; no package-wide version exported; provisional source/state/policy identifiers retained |
| 43–44, 65–70, 72–74 | Coherent validated checkpoints, progress and final publication workflow; no invented capacity observation |
| 47–54, 57–60 | Allowlisted source/value origins, UTC, reset data without replenishment inference, documented exit codes/bounds; no database/config-file sprawl |
| 55–56 | Synchronized process crash/CLI-signal tests and writer exclusion/release |
| 61–62 | status, status --json, refresh and finite daemon work via PYTHONPATH=src; canonical product identity |
| 63 | Twenty-row matrix above |

## Residual operational limits

- No verified live per-window applicability contract. Production reads yield UNKNOWN
  policy and no current directive; selection and ordinaryUsageAllowed are not evidence.
- Backend sample age, safe upstream cadence and sustained source reliability are UNKNOWN.
  Defaults (300s polling, 900s max age, 20s timeout) are local conservative bounds.
- Source protocol remains experimental. Historical V1 values are not current quota.
  Human /status comparison remains PENDING / NOT VERIFIED, expressly nonblocking.
- Unsigned cache cannot defeat coordinated same-user tampering. Unsupported schema is
  rejected without migration. Different cache directories have independent locks.
- Process-crash atomic visibility is not universal power-loss durability. SIGKILL of CGC
  cannot execute cleanup; arbitrary descendant lifetime is not guaranteed. Private temp
  siblings may remain, intentionally not deleted. No hard realtime guarantee.

No required V2 implementation item remains open under this acceptance scope. Stop after
publication. A future V3 mission needs explicit new authorization and must preserve
UNKNOWN/current-authority boundaries. Automatic project preservation is not enabled.
