# CREDID GUARDIAN CODEX (CGC) — offline tests and preserved test theory

## V2 current status

V2 is PARTIAL. The earlier 62-test POSIX run is historical verification of the existing
implementation, not full mission acceptance. See [current progress](../docs/V2_PROGRESS.md) for current validation and remaining requirements.
See [V2 operations and handoff](../docs/V2_OPERATIONS.md) for the canonical state, scoped policy, atomic cache, status CLI,
finite daemon, security limits and validation evidence. No V2 live quota request ran.
The V0/V1 descriptions and future proposals below are retained as historical context;
V2 operations supersedes their statements that policy/cache/CLI/daemon are unimplemented.
Hooks, GUI and preservation execution remain unimplemented.


V1 has 32 passing synthetic normalization/protocol tests: `PYTHONPATH=src python3 -B -m unittest discover -s tests -v`. test_quota.py uses hand-authored quota data; test_quota_protocol.py substitutes local Python peers for Codex, so tests make no live quota requests. The policy/cache/hook cases below remain future specifications, NOT_TESTED as application behavior; V1 implements none of those components.

## Deterministic thresholds

| Remaining | Expected |
|---|---|
| 100% | GREEN |
| 21% | GREEN |
| 20% | AMBER |
| 11% | AMBER |
| 10% | RED |
| 6% | RED |
| 5% | EMERGENCY |
| 0% | EMERGENCY |

Add fractional boundary cases without preclassification rounding. Reject invalid percentages, booleans, NaN and infinity rather than clamping values.

## Future behavioral cases

- Multiple quota windows: minimum across usable applicable windows; stable identities; arbitrary window count; incomplete coverage remains explicit.
- Missing reset timestamp: preserve null without inventing a reset or invalidating unrelated valid fields.
- Unknown remaining percentage: null stays unknown; no 0% or GREEN default.
- Malformed source response: safe error class, no raw payload logging, no cache corruption.
- Temporary source failure: retain prior observation/timestamp and update only refresh-health metadata.
- Stale cache: age grows across failed reads; historical GREEN is not current all-clear; no reset inference.
- Atomic replacement: fault injection before/during replacement leaves an old or new complete generation; test concurrency separately.
- Credential redaction: synthetic secrets never escape through source fields, errors, cache, CLI or hook; no real credentials in tests.
- Direct versus derived percentages: preserve value_origin, formula/input provenance and conflicts; do not relabel derived data as direct.
- No prior valid data: explicitly UNKNOWN and no fabricated observation.
- Clock anomalies: future timestamps/skew handled explicitly.
- Single source of truth: human/JSON/hook/UI consumers agree on one normalized generation.
- Authorization isolation: RED/EMERGENCY hook returns policy/directive but never edits, commits or pushes external repositories.
- Synthetic isolation: fixture observations cannot drive a live trigger.

Use deterministic fixtures/mocks before any separately authorized live source validation. No installation, account quota request or credential access is needed for V0.


V1 clamp behavior follows the later user instruction: clamped out-of-range source values remain INVALID, not valid future policy input. The initial missing-module failure and the single successful live experiment are recorded in docs/QUOTA_SOURCE_DISCOVERY.md. A current-session `/status` cross-check has not been supplied.

## Filesystem-sensitive test execution

Use `TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -v` on WSL
when the checkout is on a Windows mount that does not enforce POSIX 0700/0600 modes.
The full suite passes with Linux-native temporary caches. Workspace-contained caches
are intentionally refused on the current Windows mount; do not weaken the checks.

## Configurable-threshold block

71 deterministic tests now pass, including nine tests in test_policy_config.py for
fractional boundaries, invalid configuration, cache schema/policy rejection, custom
refresh/failure retention, daemon mismatch before reads, equivalent numeric configuration,
CLI forwarding and human/JSON consistency. V1 code and its original 32 tests are unchanged.
The initial test-first invocation failed to import the not-yet-implemented PolicyConfig;
that expected failure is resolved. Full mission acceptance remains pending.
