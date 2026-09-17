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

V0 is foundation only. The synthetic policy model consists of documented ranges, examples and future test cases; no executable policy engine is implemented. Services, GUI/tray, installers and quota collection are absent.

## Exact next mission

**CGC V1 — QUOTA OBSERVATION: discover and verify the safest supported local Codex usage-information source, without extracting credentials or modifying authentication.**

Begin with authoritative supported-interface documentation and permitted usage data. Determine availability, provenance, window identity/applicability, percentages, reset semantics, freshness, limits and errors. Do not scrape tokens or browser sessions, guess private endpoints, or promise a reader before evidence supports one. If no safe supported source can be established, report that result explicitly and stop at the source gate.

V1 requires a new explicit task. Do not perform source discovery during V0 or automatically begin daemon, hook or UI work.
