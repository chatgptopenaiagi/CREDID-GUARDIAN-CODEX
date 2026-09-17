# CREDID GUARDIAN CODEX (CGC)

CREDID GUARDIAN CODEX (CGC) is a concept-first, local usage-awareness, quota-observation and intelligent project-preservation architecture for Codex workflows.

**THE GUARDIAN OBSERVES. CODEX PRESERVES.**

Long-running development can approach a usage boundary while discoveries, partial changes and next steps remain only in conversation context. CGC is intended to act like an aircraft fuel gauge: report available capacity, observation reliability and preservation policy. It does not fly the aircraft or take control of repositories.

## Current status

**CGC V0 — FOUNDATION**

**IMPLEMENTATION STATUS: NOT YET VERIFIED** — no supported live quota source has been established for CGC. No quota reader, daemon, CLI, hook or GUI is implemented. The only Python file is an inert package placeholder.

| Classification | What exists or is proposed |
|---|---|
| CONCEPT | Usage-aware preservation with explicit source validity and authorization |
| IMPLEMENTED | Foundation documents, repository safeguards and an inert package placeholder |
| VERIFIED | Foundation structure and policy/directive consistency are checked during genesis; no live quota functionality is verified |
| PLANNED | Source discovery, normalization, validation, atomic cache, policy evaluation, daemon, CLI, Codex integration and future desktop meter |

## Initial policy

These are CGC defaults, not claims about Codex limits or available quota fields. Evaluate the most constrained usable remaining percentage across any number of applicable windows.

| State | Remaining capacity | Intended response |
|---|---|---|
| GREEN | > 20% | Continue authorized development normally |
| AMBER | > 10% and <= 20% | Continue with awareness; consider checkpoint readiness |
| RED | > 5% and <= 10% | Stop starting major new work; prepare a resumable checkpoint |
| EMERGENCY | <= 5% | Minimum safe preservation only |

Values must first be valid percentages in [0, 100]. Unknown, invalid or stale readings do not become 0% or GREEN. Incomplete window coverage cannot establish that all capacity is healthy. See [policy](docs/PRESERVATION_POLICY.md).

## Proposed architecture

```text
Usage source → Quota reader → Normalizer → Validator
                                               ↓
                                 Policy engine + atomic state cache
                                               ↓
                  CLI / Codex hook / future desktop meter
                                               ↓
                    Codex preserves only when authorized
```

**ONE SENSOR. MULTIPLE CONSUMERS.** One normalized state supplies every consumer; interfaces do not independently fetch or recalculate quota. Multiple durations, quota buckets and future windows are supported by the design, without assuming a fixed window count.

The candidate cache is `~/.codex/cgc/state.json`; genesis does not create or inspect it. Future commands such as `python -m cgc status --json`, `python -m cgc daemon --interval 30` and `python -m cgc hook-check` are proposals, not working commands or supported Codex interfaces.

## Security and authority

CGC consumes usage information, never authentication material. It must not read or export authentication files, tokens, browser cookies or password stores. Authentication remains with its owner. A future reader must use a verified, permitted source without bypassing controls.

CGC reports policy; it does not autonomously edit, commit, push or otherwise modify external repositories. Codex remains the reasoning/preservation actor and must follow the current repository's rules and explicit authorization. A RED reading is not permission to publish.

## Documents and roadmap

- [Concept](docs/CONCEPT.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Preservation policy and exact directives](docs/PRESERVATION_POLICY.md)
- [Security model](docs/SECURITY_MODEL.md)
- [Provisional data model](docs/DATA_MODEL.md)
- [Staged roadmap](docs/ROADMAP.md)
- [Decisions and genesis evidence](docs/DECISIONS.md)
- [Future deterministic tests](tests/README.md)
- [Agent instructions](AGENTS.md)

## Limitations and next mission

This foundation cannot observe remaining capacity or automatically detect a threshold. Source availability, access, semantics, freshness and supported integration points are unverified. Cache failure behavior and policy evaluation are specified, not implemented. Examples are synthetic; none describes this account. No runtime tests or live quota requests are claimed.

The next separately authorized mission is **CGC V1 — QUOTA OBSERVATION**: discover and verify the safest supported usage-information source without inspecting credential material. Stop at V0 until that mission is authorized.

Product name: **CREDID GUARDIAN CODEX**. Acronym: **CGC**. GitHub identifier: `CREDID-GUARDIAN-CODEX` (a space-free repository identifier only). Licensed under [Apache-2.0](LICENSE).
