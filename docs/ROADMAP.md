# CREDID GUARDIAN CODEX (CGC) — roadmap

## V2 current status

The configurable-threshold block (mission 9, 32, 33) is COMPLETE: one validated
PolicyConfig, persisted thresholds, daemon configuration checks and cache-only status.
The applicability/limiting-window block (10, 26, 47, 49) is also COMPLETE offline.
Per-window evidence is distinct from selection; live applicability remains UNKNOWN.
Schema cgc-state-v2.3 preserves latest diagnostics and last-known-good separately and
rejects older caches without replacing them. Full V2 remains PARTIAL.

V2 is PARTIAL. The earlier 62-test POSIX run is historical verification of the existing
implementation, not full mission acceptance. See [current progress](V2_PROGRESS.md) for current validation and remaining requirements.
See [V2 operations and handoff](V2_OPERATIONS.md) for the canonical state, scoped policy, atomic cache, status CLI,
finite daemon, security limits and validation evidence. No V2 live quota request ran.
The V0/V1 descriptions and future proposals below are retained as historical context;
V2 operations supersedes their statements that policy/cache/CLI/daemon are unimplemented.
Hooks, GUI and preservation execution remain unimplemented.


Roadmap entries describe future missions, not authorization to execute them.

| Stage | Scope | Acceptance evidence |
|---|---|---|
| CGC V0 — FOUNDATION | Repository, architecture, synthetic policy model | Reviewed foundation docs, exact identity/directives, synthetic boundary theory and verified publication; no working reader claimed |
| CGC V1 — QUOTA OBSERVATION | Discover and verify the safest supported local Codex usage source | Official/supportable source evidence, minimum privilege, field semantics and failure boundaries; explicitly record unavailable/unknown if no safe source exists |
| CGC V2 — GUARDIAN DAEMON | Reliable normalized cached usage state | Deterministic multi-window policy tests, atomic cache/failure/staleness tests, finite reads and a documented polling policy |
| CGC V3 — CODEX PRESERVATION INTEGRATION | RED/EMERGENCY policy reporting and directives | Verified supported integration point, authorization isolation, idempotence and no autonomous external-repository mutation |
| CGC V4 — DESKTOP GUARDIAN | Always-on-top meter / tray visualization | Shared-state consumer, visible uncertainty/age and no competing sensor |
| CGC V5 — ADVANCED PRESERVATION INTELLIGENCE | Repository-aware preservation plans | Explicit project authorization, truthful resumability, bounded work and separate reasoning/execution authority |

## Current boundary

V0 foundation complete. V1 observed a real quota snapshot via documented experimental Codex app-server and added the bounded reader/normalizer plus 32 synthetic tests. Independent current-session `/status` comparison remains NOT_VERIFIED; no production stability, polling cadence or global bucket applicability is claimed. See [V1 discovery](QUOTA_SOURCE_DISCOVERY.md). The one live-read authorization is consumed.

## Historical next mission after V1

**CGC V2 — GUARDIAN DAEMON:** one canonical normalized state, applicable-bucket policy, atomic last-known-good cache and bounded observation loop with tested source failures, staleness, concurrency and shutdown. Establish source-appropriate cadence and resolve the independent status comparison without extracting credentials or invoking AI tasks for test traffic.

V2 requires a new explicit task. No daemon, cache, preservation hooks, GUI or repeated polling was started during V1.

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
after SIGKILL of CGC are not guaranteed. Default-target preflight/final audit remain pending.
