# CREDID GUARDIAN CODEX (CGC) — roadmap

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


Roadmap entries describe future missions, not authorization to execute them.

| Stage | Scope | Acceptance evidence |
|---|---|---|
| CGC V0 — FOUNDATION | Repository, architecture, synthetic policy model | Reviewed foundation docs, exact identity/directives, synthetic boundary theory and verified publication; no working reader claimed |
| CGC V1 — QUOTA OBSERVATION | Discover and verify the safest supported local Codex usage source | Official/supportable source evidence, minimum privilege, field semantics and failure boundaries; explicitly record unavailable/unknown if no safe source exists |
| CGC V2 — GUARDIAN DAEMON | Reliable normalized cached usage state | Deterministic multi-window policy tests, atomic cache/failure/staleness tests, finite reads and a documented polling policy |
| CGC V3 — CODEX PRESERVATION INTEGRATION | RED/EMERGENCY policy reporting and directives | Verified supported integration point, authorization isolation, idempotence and no autonomous external-repository mutation |
| CGC V4 — INTEROPERABILITY, PORTABLE STATE & AGENT CONNECTIVITY | Language-neutral state, inert capsules, local service/plugin and authorized consumers; ARCHITECTED / runtime NOT_STARTED | Versioned semantics, integrity, authority isolation and per-platform evidence; see [V4 mission](V4_MISSION.md) |
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
after SIGKILL of CGC are not guaranteed. Default-target metadata preflight and final offline acceptance audit are complete.

Final V2 offline acceptance: [evidence matrix](V2_ACCEPTANCE.md).
153 deterministic tests pass. Zero V2 live reads; optional live verification skipped.
V3 remains NOT_STARTED and requires separate authorization.


## Active V3 and future architecture

The historical version boundaries above are superseded by the authorized
[V3 mission](V3_MISSION.md). V3 is PARTIAL: attempt, inspection and external handoff
persistence and the scoped manual local-checkpoint adapter are implemented/tested;
explicit local-bare publication/verification is verified offline; general push transport,
full safe resume and automation remain NOT_STARTED. The [Agent Fabric relationship](ARCHITECTURE.md#agent-fabric-relationship) is
ARCHITECTED/FUTURE, not runtime authorization. No gateway, control/data plane, event bus,
resume generator, AI orchestration, GUI or V4 implementation has begun.

## V4 roadmap reconciliation — 2026-09-23

The former **CGC V4 — DESKTOP GUARDIAN** entry proposed an always-on-top meter / tray
visualization. That history is retained here deliberately: Desktop Guardian becomes a
**V4 GUARDIAN SURFACE** within the broader [V4 mission](V4_MISSION.md), not a discarded
requirement. Its shared-state consumer, visible age/uncertainty and no-competing-sensor
acceptance remain. The existing V5 entry is historical future planning, not authority to
move unfinished V3 preservation/resume work to V5.

V1 = OBSERVE; V2 = UNDERSTAND; V3 = PRESERVE; V4 = CONNECT. V3 remains active and PARTIAL.
Complete V3 preservation/resume acceptance before implementing V4. Future dependency order:

1. V4.0 State Protocol and human representation.
2. V4.1 Inert `.cgcpack` export/import and integrity.
3. V4.2 Bounded local service / MCP, read-only first.
4. V4.3 Thin Codex/agent plugin with skill/MCP and optional trusted lifecycle hooks.
5. V4.4 Separately distributed SDKs and evidence-justified portable-core work.
6. V4.5 Desktop/web/mobile Guardian surfaces; remote console execution awaits the gateway.
7. V4.6 Optional authenticated remote enterprise/multi-device gateway.

Every V4 component is **ARCHITECTED / NOT_STARTED**, requiring a separately scoped task.
No runtime, package, listener, schema implementation or client is created by this roadmap.
The immediate [V3 NEXT_EXACT_ACTION](V3_PROGRESS.md#next_exact_action) remains authoritative.
