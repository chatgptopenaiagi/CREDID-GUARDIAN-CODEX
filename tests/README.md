# CREDID GUARDIAN CODEX (CGC) — future test theory

V0 has no runtime test suite or working quota/policy implementation. The cases below are specifications, NOT_TESTED as application behavior. Genesis checks documentation/fixture consistency only and must not be reported as runtime tests passing.

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
