# CREDID GUARDIAN CODEX (CGC) — provisional data model

## V2 current status

The configurable-threshold block (mission 9, 32, 33) is COMPLETE: one validated
PolicyConfig, persisted thresholds, daemon configuration checks and cache-only status.
The applicability/limiting-window block (10, 26, 47, 49) is also COMPLETE offline.
Per-window evidence is distinct from selection; live applicability remains UNKNOWN.
Schema cgc-state-v2.3 preserves latest diagnostics and last-known-good separately and
rejects older caches without replacing them. Full V2 offline acceptance is complete; live semantic limits remain explicit.

V2 is COMPLETE under offline POSIX acceptance. The earlier 62-test POSIX run is historical verification of the existing
implementation, not full mission acceptance. See [current progress](V2_PROGRESS.md) for current validation and remaining requirements.
See [V2 operations and handoff](V2_OPERATIONS.md) for the canonical state, scoped policy, atomic cache, status CLI,
finite daemon, security limits and validation evidence. No V2 live quota request ran.
The V0/V1 descriptions and future proposals below are retained as historical context;
V2 operations supersedes their statements that policy/cache/CLI/daemon are unimplemented.
Hooks, GUI and preservation execution remain unimplemented.


Status: V0 conceptual model retained below; V1 implemented projection is specified in the appended section. The provisional format is not frozen. See [source discovery](QUOTA_SOURCE_DISCOVERY.md) for verified upstream fields and limits.

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


## V1 implemented projection (0.1.0-provisional)

The V0 cache/policy envelope above remains future design. V1 outputs observed_at (local post-read time), source_observed_at=null (backend age unknown), source_kind=codex_app_server, source_supported=true (documented interface, NOT a production-support claim), source_maturity=experimental, mode, source_confidence, status, coverage=UNKNOWN, buckets, windows and optional ordinary_usage_allowed. It omits account identity, plan, credit balances, banners and raw error messages. No policy_state/global minimum is implemented.

Each returned map key is retained as bucket identity. The legacy rateLimits view is used only when the mapping is absent/empty; it is not duplicated into a populated mapping. Within each bucket, primary and secondary have usedPercent, windowDurationMins and resetsAt. Duration, not slot position, determines the optional 5-hour/weekly label. individualLimit uses direct remainingPercent and has unknown duration; it is a separate spend-control kind. Unknown fields are not invented or guessed. Coverage remains UNKNOWN even on a successful read.

Window fields: window_id, bucket_id, name, window_kind, duration_seconds, used_percent, used_percent_origin, remaining_percent, value_origin, derivation, clamped, reset_at, reset_origin and validity. Used is direct. Remaining is derived as clamp(100-usedPercent,0,100) for rolling windows; individual-limit remaining is direct. This follows the later explicit V1 user instruction. Out-of-range source values retain INVALID validity after clamping so they cannot become trustworthy policy inputs. Missing values remain null/unknown. Dates converted from Unix seconds are labeled derived_from_unix_seconds.

V1 has fixed limits of 32 buckets, 512 KiB combined process output, 128 KiB buffered frame, 100 frames and a configurable finite timeout up to 30 seconds (default 20), plus bounded cleanup. All limits fail closed; no silent truncated all-clear. Errors contain a fixed code, attempted_at, observed_at=null and empty windows, explicitly ERROR rather than a fabricated empty observation. No cache exists to overwrite.

[Retained normalized live projection](v1-normalized-observation.json) was normalized offline from the already-sanitized experiment artifact; it did not consume another live read. [Synthetic fixture](../tests/fixtures/quota.json) is hand-authored and contains no actual account data. Synthetic normalizer calls use mode=synthetic and source_confidence=SYNTHETIC. Publication of test results does not make them live observations.

Freshness/provenance is IMPLEMENTED and VERIFIED OFFLINE: separate age, refresh health
and policy authority; failed refresh withholds current policy while retaining evidence.
See [V2 operations](V2_OPERATIONS.md) for canonical semantics and schema details.

One-shot refresh CLI is IMPLEMENTED and VERIFIED OFFLINE. It requires --live and
--bucket, shares the daemon writer lock/configuration/cache path, and makes at most
one bounded read without retry. Unknown applicability remains UNKNOWN; no preservation
action is executed. See [V2 operations](V2_OPERATIONS.md) for output and exit semantics.

Crash/interruption safety is VERIFIED OFFLINE with synchronized process tests: old/new
canonical state survives tested SIGKILL publication stages, locks release, and graceful
CLI signals preserve bounded read cleanup. Power-loss durability and descendant cleanup
after SIGKILL of CGC are not guaranteed. Default-target metadata preflight and final offline acceptance audit are complete.

Final V2 offline acceptance: [evidence matrix](V2_ACCEPTANCE.md).
153 deterministic tests pass. Zero V2 live reads; optional live verification skipped.
V3 remains NOT_STARTED and requires separate authorization.

## V3 current frontier

V3 is authorized and PARTIAL. The pure attempt contract, bounded non-mutating project
inspection, and external human/machine handoff persistence are IMPLEMENTED and VERIFIED
OFFLINE. A deliberate manual local-checkpoint Python adapter is also IMPLEMENTED and
VERIFIED OFFLINE in disposable Linux Git fixtures. Handoff state grants no mutation
authority. Explicit local-bare publication and independent verification are also verified
offline; general push/network transport, full safe resume and automation remain pending.
The inspect and handoff-status CLIs are observational; there is no preserve CLI.
V1/V2 remain accepted. See the local-checkpoint contract in docs/V3_CONTRACT.md.
Resume by present repository evidence and [V3 progress](V3_PROGRESS.md), under the complete
[V3 mission](V3_MISSION.md) and current user instructions. Historical V2 notes
that V3 was not authorized describe the earlier boundary; this explicit V3 mission
supersedes that boundary without authorizing unrelated project mutation or V4.

V3 uses a separate `cgc-preservation-v3.0-provisional` record; see [contract](V3_CONTRACT.md).
V2 caches do not acquire V3 fields. Typed receipts are not externally verified by the model.


`cgc-inspection-v3.0-provisional` is a separate validated OBSERVED/REFUSED envelope with
snapshot/digest or a fixed failure code. Root identity, Git state, scope limitations and
unknown instruction/test knowledge remain explicit. See [inspection contract](V3_CONTRACT.md#bounded-project-inspection).


`cgc-handoff-v3.0-provisional` stores CONTINUITY_ONLY state with latest_attempt,
last_known_good and previous_known_good. Both renderers reconstruct this validated state;
notes.next_exact_action is a bounded machine field, not an executable command. Known-good
means saved continuity, not preserved Git state. See [handoff contract](V3_CONTRACT.md#durable-handoff-persistence).


The V3 manual local-checkpoint adapter now separates current caller approval from saved
continuity, verifies an explicit selected tree and normal single-parent commit, and retains
truthful failure state without rollback. The Guardian does not invoke it. Its narrow POSIX,
hook, staging, content and concurrency boundaries are specified in the
[local checkpoint contract](V3_CONTRACT.md#deliberate-manual-local-checkpoint).
Local-bare publication now has a separate manual adapter; general push/network transport,
full resume reconciliation and automatic policy integration remain future.


The manual local-bare publication adapter separates current destination/history approval,
object transfer, expected-tip ref update, independent verification and continuity persistence.
No attempt/handoff/V2 schema change. A saved PUBLISHING intent grants no authority or proof
of remote preservation. See the [publication contract](V3_CONTRACT.md#explicit-local-bare-publication-and-independent-verification).
General push/network transport and Fabric runtime remain NOT_STARTED.


## V3 reconciliation projection

The [reconciliation contract](V3_RECONCILIATION.md) defines a separate bounded projection
of durable/current facts, provenance, freshness, contradictions and required observations.
No existing schema is extended or migrated by that specification. In particular, current
handoffs lack reviewed SHA256 mappings and structured tested-state/environment bindings;
valid missing capabilities project to UNKNOWN, not false or permission. Current authority
remains external to historical evidence. Projection cgc-reconciliation-v3.0-provisional and its strict pure validator are implemented;
all results retain UNKNOWN safety and false mutation flags. Existing handoff schema is unchanged.
