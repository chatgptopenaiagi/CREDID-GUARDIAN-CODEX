# CREDID GUARDIAN CODEX (CGC)

CREDID GUARDIAN CODEX (CGC) is a concept-first, local usage-awareness, quota-observation and intelligent project-preservation architecture for Codex workflows.

**THE GUARDIAN OBSERVES. CODEX PRESERVES.**

Long-running development can approach a usage boundary while discoveries, partial changes and next steps remain only in conversation context. CGC is intended to act like an aircraft fuel gauge: report available capacity, observation reliability and preservation policy. It does not fly the aircraft or take control of repositories.

## Current status

**CGC V2 — COMPLETE OFFLINE POSIX ACCEPTANCE: GUARDIAN ENGINE, POLICY, CACHE, STATUS CLI AND BOUNDED DAEMON**

| Classification | Status |
|---|---|
| IMPLEMENTED | Existing V1 reader, configurable policy with explicit per-window evidence, freshness/provenance, atomic last-known-good cache, cache-only status CLI, one-shot refresh CLI and finite foreground daemon |
| VERIFIED | 153 tests pass using Linux-native temporary storage; one historical V1 observation. See V2_PROGRESS.md |
| COMPLETE | V2 mission offline acceptance; see V2_ACCEPTANCE.md for evidence and limits |
| NOT IMPLEMENTED | Automatic preservation; hooks, GUI/tray and services |
| UNKNOWN | Backend sample age, complete bucket applicability, supported polling cadence and sustained live reliability |
| PLANNED | Preservation integration/hooks, desktop meter and native Windows support |

The authoritative specification is [V2 mission](docs/V2_MISSION.md). Resume from
[NEXT_EXACT_ACTION in V2 progress](docs/V2_PROGRESS.md#next_exact_action).
The Codex app-server source remains experimental. V2 consumed **zero live quota reads**.
Independent human `/status` comparison remains PENDING / NOT VERIFIED. The retained
V1 percentages are historical evidence, not current quota.

```bash
PYTHONPATH=src python3 -B -m cgc status --json
TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -v
```

Status reads only the shared cache and reports UNKNOWN if none exists. The finite daemon
requires explicit `--live`, `--bucket` and `--max-reads` arguments. No service is installed.
Read [V2 operation, safety limits and commands](docs/V2_OPERATIONS.md) before invoking it.
See [V1 source discovery](docs/QUOTA_SOURCE_DISCOVERY.md) for historical protocol evidence.

## Initial policy

These are CGC defaults, not claims about Codex limits or available quota fields. Evaluate the most constrained usable remaining percentage across any number of applicable windows.

| State | Remaining capacity | Intended response |
|---|---|---|
| GREEN | > 20% | Continue authorized development normally |
| AMBER | > 10% and <= 20% | Continue with awareness; consider checkpoint readiness |
| RED | > 5% and <= 10% | Stop starting major new work; prepare a resumable checkpoint |
| EMERGENCY | <= 5% | Minimum safe preservation only |

Policy inputs must be valid percentages in [0, 100]. The V1 reader clamps derived values as requested but marks out-of-range source values INVALID. Unknown, invalid or stale readings do not become 0% or GREEN. Incomplete window coverage cannot establish that all capacity is healthy. See [policy](docs/PRESERVATION_POLICY.md).

## Architecture (V2 engine/cache/CLI implemented; integrations planned)

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

The implemented default cache is `~/.codex/cgc/state.json`; it was not created during
development. `python -m cgc status` and `python -m cgc status --json` consume this same
state. The daemon uses one finite writer with an explicit selected bucket scope.
Selection is not applicability evidence: live windows currently remain UNKNOWN. Synthetic
contracts verify policy behavior offline; they cannot authorize live policy.
`hook-check` and desktop integration remain PLANNED, not working commands.

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

V2 is verified offline on POSIX, with private temporary caches and injected sensors.
No live daemon run, native Windows transport, supported polling cadence or preservation
hook is claimed. Unknown/partial coverage cannot establish global all-clear. CGC never
executes preservation actions. See the [V2 handoff](docs/V2_OPERATIONS.md#handoff).

Product name: **CREDID GUARDIAN CODEX**. Acronym: **CGC**. GitHub identifier: `CREDID-GUARDIAN-CODEX` (a space-free repository identifier only). Licensed under [Apache-2.0](LICENSE).

Freshness/provenance is IMPLEMENTED and VERIFIED OFFLINE: separate age, refresh health
and policy authority; failed refresh withholds current policy while retaining evidence.
See [V2 operations](docs/V2_OPERATIONS.md) for canonical semantics and schema details.

One-shot refresh CLI is IMPLEMENTED and VERIFIED OFFLINE. It requires --live and
--bucket, shares the daemon writer lock/configuration/cache path, and makes at most
one bounded read without retry. Unknown applicability remains UNKNOWN; no preservation
action is executed. See [V2 operations](docs/V2_OPERATIONS.md) for output and exit semantics.

Crash/interruption safety is VERIFIED OFFLINE with synchronized process tests: old/new
canonical state survives tested SIGKILL publication stages, locks release, and graceful
CLI signals preserve bounded read cleanup. Power-loss durability and descendant cleanup
after SIGKILL of CGC are not guaranteed. Default-target metadata preflight and final offline acceptance audit are complete.

Final V2 offline acceptance: [evidence matrix](docs/V2_ACCEPTANCE.md).
153 deterministic tests pass. Zero V2 live reads; optional live verification skipped.
V3 remains NOT_STARTED and requires separate authorization.
