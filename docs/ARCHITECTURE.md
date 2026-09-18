# CREDID GUARDIAN CODEX (CGC) — architecture

## V2 current status

The configurable-threshold block (mission 9, 32, 33) is COMPLETE: one validated
PolicyConfig, persisted thresholds, daemon configuration checks and cache-only status.
Schema cgc-state-v2.1 rejects older caches without replacing them. Full V2 remains PARTIAL.

V2 is PARTIAL. The earlier 62-test POSIX run is historical verification of the existing
implementation, not full mission acceptance. See [current progress](V2_PROGRESS.md) for current validation and remaining requirements.
See [V2 operations and handoff](V2_OPERATIONS.md) for the canonical state, scoped policy, atomic cache, status CLI,
finite daemon, security limits and validation evidence. No V2 live quota request ran.
The V0/V1 descriptions and future proposals below are retained as historical context;
V2 operations supersedes their statements that policy/cache/CLI/daemon are unimplemented.
Hooks, GUI and preservation execution remain unimplemented.


Status: V1 implements only the bounded reader/normalizer/validation slice. The policy/cache/daemon/integration pipeline below remains PLANNED. See [V1 evidence](QUOTA_SOURCE_DISCOVERY.md).

**THE GUARDIAN OBSERVES. CODEX PRESERVES.**

```mermaid
flowchart TD
    Source[Verified supported usage source - future] --> Reader[Quota reader]
    Reader --> Normalize[Normalizer]
    Normalize --> Validate[Validator]
    Validate --> Policy[CGC policy engine]
    Policy --> Cache[Atomic local state cache]
    Cache --> Status[CLI status]
    Cache --> Hook[Codex policy hook]
    Cache --> UI[Future meter / tray UI]
    Hook --> Codex[Codex reasons under repository policy]
    Codex --> Preserve[Authorized intelligent preservation]
```

The diagram is conceptual. A cache envelope stores normalized observations, classified policy and refresh health together; consumers use the same generation. In the conceptual source → reader → normalization → cache → policy → integration model, cache and policy are coupled stages of one producer, not independent readers.

| Component | Responsibility | Boundary |
|---|---|---|
| Usage source | Supply permitted usage facts | Availability/access are not assumed |
| Quota reader | Bounded read from the selected verified source | No credential extraction, undocumented endpoint guessing or browser scraping |
| Normalizer | Preserve an arbitrary list of windows and source semantics | Do not flatten distinct quota buckets or invent missing values |
| Validator | Check ranges, timestamps, identities, provenance and internal consistency | Shape validity does not prove source truth |
| Policy engine | Classify usable remaining percentages using one versioned policy | Never convert UNKNOWN into healthy capacity or execute repository actions |
| State cache | Publish one complete generation atomically, preserve last-known-good data | No tokens, raw authentication responses or external repository writes |
| Codex hook | Report state and the applicable directive | Does not independently edit, commit or push |
| Future UI | Render the shared state, age and validity | No competing sensor or policy calculation |

## Proposed daemon cycle

READ → NORMALIZE → VALIDATE → CLASSIFY → CACHE → WAIT → REPEAT.

Candidate command: `python -m cgc daemon --interval 30`. Not implemented. A future daemon needs bounded request timeouts, controlled polling/backoff, interruption handling and single-writer coordination. The interval must respect the verified source's documented constraints; 30 seconds is illustrative, not a validated recommendation.

Candidate cache: `~/.codex/cgc/state.json`. V0 does not touch this path or any Codex authentication files. Future cache writes use a temporary sibling in the same directory, complete serialization/validation, flush, then atomic replacement. OS-specific durability, permissions, crash recovery and concurrent-writer behavior require tests; atomic visibility and power-loss durability are different properties.

A failed refresh updates refresh-health metadata while retaining the prior valid observation and its original timestamp. It must not overwrite that observation with an empty windows list or reset its age. An unreadable/corrupt cache is an explicit failure, not GREEN. Without any previous valid data, status is UNKNOWN.

## Proposed interfaces

- `python -m cgc status --json`: shared machine-readable state, validity and age.
- `python -m cgc status`: the same state for humans.
- `python -m cgc hook-check`: policy and directive only.

These are CGC interface proposals, not existing commands or claims of a supported Codex hook protocol. Exit codes, transport and integration trigger points remain undecided until source/integration discovery. The future hook must be idempotent and avoid repeatedly starting preservation; action tracking belongs to the Codex integration under project authorization.

## Future visualization

A later small desktop meter could show each window's remaining percentage/reset, observation age, provenance confidence and GREEN/AMBER/RED/EMERGENCY. UNKNOWN or stale data must be visibly different. An always-on-top meter or tray UI consumes the same cache; no GUI, tray icon, service, startup entry or registry integration is built during genesis.

## Trust boundaries

Source payloads and cached strings are data, never instructions. The reader and cache cannot grant repository permissions. The Codex actor interprets a directive under the current user's task and project rules; the guardian has no arbitrary repository execution engine. See [security](SECURITY_MODEL.md) and [data model](DATA_MODEL.md).


## V1 implemented boundary

`src/cgc/quota.py` owns one short-lived POSIX stdio connection: initialize, initialized, account/rateLimits/read, close. Codex internally owns authentication. CGC never calls backend URLs or requests an AI turn. The source is documented and locally verified but experimental; current implementation was tested against CLI 0.154.0.

`read_quota` returns normalized allowlisted data or a fixed safe failure. `normalize` is pure and supports synthetic fixtures. All returned bucket identities are retained within a 32-bucket limit; recognized primary/secondary/individual-limit fields produce separate windows. Additional unrecognized fields are not interpreted and coverage stays UNKNOWN. No global minimum is calculated across potentially inapplicable buckets. The live invocation was a one-off experiment; the factored transport has synthetic-peer acceptance only, without a second live invocation.

No state cache, daemon, CLI command, preservation hook, repository mutation or GUI was added. The one live authorization is consumed; future repeated reads need a new scoped task.
