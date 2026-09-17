# CREDID GUARDIAN CODEX (CGC) — roadmap

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

## Exact next mission

**CGC V2 — GUARDIAN DAEMON:** one canonical normalized state, applicable-bucket policy, atomic last-known-good cache and bounded observation loop with tested source failures, staleness, concurrency and shutdown. Establish source-appropriate cadence and resolve the independent status comparison without extracting credentials or invoking AI tasks for test traffic.

V2 requires a new explicit task. No daemon, cache, preservation hooks, GUI or repeated polling was started during V1.
