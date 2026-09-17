# CREDID GUARDIAN CODEX (CGC)

CREDID GUARDIAN CODEX (CGC) is a concept-first, local usage-awareness, quota-observation and intelligent project-preservation architecture for Codex workflows.

**THE GUARDIAN OBSERVES. CODEX PRESERVES.**

Long-running development can approach a usage boundary while discoveries, partial changes and next steps remain only in conversation context. CGC is intended to act like an aircraft fuel gauge: report available capacity, observation reliability and preservation policy. It does not fly the aircraft or take control of repositories.

## Current status

**CGC V1 — QUOTA OBSERVATION**

A documented Codex app-server quota source was successfully read once with installed `codex-cli 0.154.0`. V1 provides a Python standard-library, one-shot reader and normalizer. The protocol remains **experimental**; no production stability or polling cadence is claimed. Independent current-session `/status` comparison is **NOT_VERIFIED**.

| Classification | What exists or is proposed |
|---|---|
| CONCEPT | Usage-aware preservation with explicit validity and authorization |
| IMPLEMENTED | Bounded POSIX stdio reader, quota-only normalization and synthetic tests |
| VERIFIED | One `account/rateLimits/read` experiment; 32 synthetic tests; offline normalization of the retained sanitized quota projection |
| PLANNED | Applicability/policy aggregation, atomic cache, daemon, CLI, preservation hooks and desktop meter |

See [source discovery and live evidence](docs/QUOTA_SOURCE_DISCOVERY.md). At the recorded time, the `codex` bucket reported 64% used over 300 minutes and 42% used over 10080 minutes; 36%/58% remaining were **derived**, not directly supplied. These are historical observations, not current readings.

The library interface is `from cgc.quota import read_quota` with `PYTHONPATH=src`. An explicit `read_quota(timeout=20)` invocation initiates a fresh read through Codex. **Do not run it automatically:** the V1 session's single live-read authorization is consumed. Deterministic verification is `PYTHONPATH=src python3 -B -m unittest discover -s tests -v`; tests use synthetic peers, never live Codex.

## Initial policy

These are CGC defaults, not claims about Codex limits or available quota fields. Evaluate the most constrained usable remaining percentage across any number of applicable windows.

| State | Remaining capacity | Intended response |
|---|---|---|
| GREEN | > 20% | Continue authorized development normally |
| AMBER | > 10% and <= 20% | Continue with awareness; consider checkpoint readiness |
| RED | > 5% and <= 10% | Stop starting major new work; prepare a resumable checkpoint |
| EMERGENCY | <= 5% | Minimum safe preservation only |

Policy inputs must be valid percentages in [0, 100]. The V1 reader clamps derived values as requested but marks out-of-range source values INVALID. Unknown, invalid or stale readings do not become 0% or GREEN. Incomplete window coverage cannot establish that all capacity is healthy. See [policy](docs/PRESERVATION_POLICY.md).

## Architecture (reader implemented; later stages planned)

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

V1 observes one snapshot only when explicitly invoked; it does not monitor usage or trigger preservation. Native Windows transport is not implemented. Backend observation age, sustained polling reliability, full bucket applicability and current-session `/status` correspondence remain unknown. No raw response, authentication material or unrelated account fields are retained.

The next separately authorized mission is **CGC V2 — GUARDIAN DAEMON**: canonical state, applicable-bucket policy, atomic last-known-good cache and bounded polling with tested failure/staleness behavior. No daemon, cache, hooks or GUI has begun. See the [roadmap](docs/ROADMAP.md).

Product name: **CREDID GUARDIAN CODEX**. Acronym: **CGC**. GitHub identifier: `CREDID-GUARDIAN-CODEX` (a space-free repository identifier only). Licensed under [Apache-2.0](LICENSE).
