# CREDID GUARDIAN CODEX (CGC) — provisional data model

Status: CONCEPT. These fields are CGC design proposals, not a verified upstream schema. No live field availability or account quota is asserted. No stable API or JSON Schema is frozen in V0.

## Observation envelope

Proposed fields: schema_version, observed_at, source, source_confidence, validity, coverage, windows, most_constrained_remaining_percent, policy_state and policy_version. Window count is unrestricted by the concept; a future implementation must impose a documented input-size bound without silently treating truncated coverage as complete.

- `source` is a non-secret identifier/method description, never a token-bearing URL or credential file contents.
- `observed_at` is a timezone-aware observation timestamp. It must not be refreshed merely because old data was reread.
- `source_confidence` describes DIRECT_SUPPORTED, DERIVED_FROM_SUPPORTED, SYNTHETIC or UNKNOWN provenance (provisional vocabulary), not a statistical guarantee.
- `validity` distinguishes VALID, UNKNOWN, INVALID and STALE; `coverage` distinguishes COMPLETE, PARTIAL and UNKNOWN.
- `most_constrained_remaining_percent` is the minimum among usable applicable windows, or null if none is usable. Partial coverage remains visible.
- `policy_state` is GREEN, AMBER, RED or EMERGENCY only when a usable current observation permits classification; otherwise null. A historical policy can remain inside last_valid_observation.

## Quota window

| Field | Intended meaning |
|---|---|
| window_id | Stable source-scoped identifier; do not key solely by duration |
| duration_seconds | Duration if known; null otherwise |
| used_percent | Valid source usage if available; null otherwise |
| remaining_percent | Direct or derived remaining percentage; null if unknown |
| reset_at | Source reset timestamp if available; null otherwise |
| observed_at | Observation timestamp, preserving per-window differences |
| source | Provenance identifier |
| value_origin | DIRECT, DERIVED or UNKNOWN |
| derivation | Formula and referenced inputs when derived; null otherwise |
| validity / confidence | Whether usable and why; no invented confidence |
| applicability | APPLICABLE, NOT_APPLICABLE or UNKNOWN for the selected budget context |

Validate finite percentages in [0,100]; reject NaN, infinity, booleans and malformed numbers. Unknown is not zero. Preserve disagreements between direct and derived values as invalid/conflicting input with safe diagnostics. Duration/reset alone must not be used to invent remaining capacity. Any interpretation of source semantics needs V1 evidence.

## Synthetic example only

The following is hand-authored fixture theory. It is NOT a live account observation, NOT a verified source format and NOT output from working CGC software.

```json
{
  "schema_version": "0.0.0-concept",
  "observed_at": "2026-01-01T00:00:00Z",
  "source": "synthetic-example",
  "source_confidence": "SYNTHETIC",
  "validity": "VALID",
  "coverage": "COMPLETE",
  "windows": [
    {
      "window_id": "synthetic:short-window",
      "duration_seconds": 18000,
      "used_percent": 91,
      "remaining_percent": 9,
      "reset_at": null,
      "observed_at": "2026-01-01T00:00:00Z",
      "source": "synthetic-example",
      "value_origin": "DERIVED",
      "derivation": {"formula": "100 - used_percent", "input_fields": ["used_percent"]},
      "validity": "VALID",
      "confidence": "SYNTHETIC",
      "applicability": "APPLICABLE"
    },
    {
      "window_id": "synthetic:long-window",
      "duration_seconds": 604800,
      "used_percent": null,
      "remaining_percent": 71,
      "reset_at": "2026-01-08T00:00:00Z",
      "observed_at": "2026-01-01T00:00:00Z",
      "source": "synthetic-example",
      "value_origin": "DIRECT",
      "derivation": null,
      "validity": "VALID",
      "confidence": "SYNTHETIC",
      "applicability": "APPLICABLE"
    }
  ],
  "most_constrained_remaining_percent": 9,
  "policy_state": "RED",
  "policy_version": "cgc-default-v0"
}
```

VALID here means structurally usable synthetic test data, not a factual verification. Synthetic sources must never drive live preservation triggers. Window labels/durations are examples, not evidence about this account.

## Cache envelope and failure semantics

Candidate state.json carries last_valid_observation plus last_refresh_attempt_at, last_refresh_status, safe error_code, cache_written_at and freshness metadata. Compute observation age from observed_at and the current clock at read time; never reset it on failed refresh. Persisted age is only age at cache write and cannot stand alone as current freshness.

If refresh fails, retain last_valid_observation unchanged while recording failure metadata. If no prior valid observation exists, keep it null and report UNKNOWN. Do not replace good data with empty results. Readers must assess stale state and clock anomalies and avoid presenting historical GREEN as current capacity.

Atomic replacement writes one validated envelope, so windows, policy and refresh status belong to the same cache generation. A future cache revision/generation identifier supports consistency. Crash durability, permissions, retention, maximum age and source-specific polling are open design questions for V1/V2, not implemented guarantees.
