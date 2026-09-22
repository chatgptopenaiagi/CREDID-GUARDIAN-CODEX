# CREDID GUARDIAN CODEX (CGC) — preservation policy

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


Initial policy identifier: `cgc-default-v0` (conceptual, not an implemented API).

**THE GUARDIAN OBSERVES. CODEX PRESERVES.**

## Valid input and aggregation

A remaining percentage must be finite and within [0, 100]. Reject booleans, malformed values and out-of-range numbers rather than clamping them. `null` means unknown, never zero. A direct remaining percentage is labeled DIRECT. A remaining value computed as `100 - used_percent` is DERIVED and retains its input provenance. Do not derive from an absent/invalid used value. Disagreement between supplied used/remaining values is a validation conflict, not permission to pick the more convenient number.

Use the minimum remaining percentage across usable, applicable windows. Do not assume exactly two windows. Applicability and coverage come from verified source semantics, not duration guesses. Missing reset timestamps do not automatically invalidate otherwise usable capacity; retain null and unknown reset semantics. Freshness must be assessed independently.

If no window is usable, `policy_state` is null and overall validity is UNKNOWN or INVALID; there is no healthy default. If only some applicable windows are known, the minimum and state apply to that observed subset and coverage is PARTIAL. Report that limitation prominently; a subset GREEN must not be presented as global all-clear. Source confidence describes evidence quality, not a fabricated probability.

On stale data, retain the last-known policy as historical information, but current policy availability becomes unknown until refreshed. Never infer a replenished budget just because a reset timestamp passed. A future integration may conservatively prepare preservation on uncertainty, but it must label that choice as precautionary rather than a measured threshold crossing. Freshness intervals and clock-skew tolerance remain source-specific V1/V2 decisions.

## Thresholds and intended behavior

| State | Exact valid range | Behavior |
|---|---|---|
| GREEN | remaining > 20% | Normal authorized development; no preservation intervention |
| AMBER | remaining > 10% and <= 20% | Continue useful work with awareness; avoid expensive optional operations and consider checkpoint readiness |
| RED | remaining > 5% and <= 10% | Stop beginning major development phases; identify COMPLETE/PARTIAL/NOT_STARTED work, discoveries, failures, completed/remaining tests, files and consumed operations; update handoff; checkpoint/push only if allowed; verify and stop |
| EMERGENCY | remaining <= 5% | Minimum safe checkpoint only; no new feature, broad refactor, optional research or large exploratory operation |

These thresholds do not grant additional task authority. CGC supplies the state/directive. Codex decides how to preserve authorized work safely under the repository's rules. Publication requires its own authorization; local preservation can be appropriate when remote publication is unavailable or forbidden. Never claim a push succeeded without verification.

## Primary directive (verbatim)

```text
CREDID GUARDIAN CODEX PRESERVATION DIRECTIVE

Usage safety threshold reached.

Stop starting new development.

Preserve the current authorized project state.

Record clearly:

1. current mission
2. work complete
3. work partial
4. work remaining
5. tests completed
6. tests remaining
7. important discoveries
8. known failures
9. files created or modified
10. live operations already consumed
11. operations that should not be repeated
12. exact next recommended action

Create a safe resumable checkpoint if repository policy and authorization permit.

Verify publication if publication was authorized.

Do not begin a new development phase after preservation.
```

## Emergency directive (verbatim)

```text
CGC EMERGENCY.

Usage capacity is critically low.

Stop development.

Record the minimum complete resumable state.

Preserve current changes safely if authorized.

Record the exact next action.

Do not start another task.
```

## Boundary test theory

| Remaining | Expected state |
|---|---|
| 100% | GREEN |
| 21% | GREEN |
| 20% | AMBER |
| 11% | AMBER |
| 10% | RED |
| 6% | RED |
| 5% | EMERGENCY |
| 0% | EMERGENCY |

Also test fractional values around each threshold, unknown/stale input and partial coverage. No rounding before classification. These are deterministic future expectations, not results from an implemented policy engine. See [test plan](../tests/README.md).


## V1 reader clarification

The human subsequently specified clamping for the observation prototype: derive remaining with `clamp(100 - usedPercent, 0, 100)`. V1 preserves the original used value and labels out-of-range source input INVALID even if the result is clamped. Thus clamping cannot admit invalid input into future policy. No policy engine or preservation action is implemented in V1; all threshold behavior above remains a future contract. See [V1 data model](DATA_MODEL.md).

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
OFFLINE. Handoff state is continuity evidence, not project preservation or mutation
authority. Target Git mutation and automation are NOT_STARTED. The inspect and
handoff-status CLIs are observational; there is no preserve CLI. V1/V2 remain accepted.
Resume by present repository evidence and [V3 progress](V3_PROGRESS.md), under the complete
[V3 mission](V3_MISSION.md) and current user instructions. Historical V2 notes
that V3 was not authorized describe the earlier boundary; this explicit V3 mission
supersedes that boundary without authorizing unrelated project mutation or V4.
