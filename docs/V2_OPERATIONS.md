# CREDID GUARDIAN CODEX — CGC V2 operations

THE GUARDIAN OBSERVES. CODEX PRESERVES.
ONE SENSOR. MULTIPLE CONSUMERS.

## Status and boundaries

V2 is PARTIAL against [the full mission](V2_MISSION.md). See [progress](V2_PROGRESS.md)
for current test results, remaining acceptance and the exact next block.

IMPLEMENTED and VERIFIED OFFLINE: configurable policy, explicit per-window applicability
and limiting-window reasoning, canonical state, private POSIX atomic cache, cache-only
human/JSON status and finite foreground daemon. **87 deterministic tests pass**, including
unchanged original V1 tests. No V2 live source read was consumed. Source remains experimental.
Actual live applicability is UNKNOWN: no preserved source contract proves which individual
windows govern the work. The production CLI therefore cannot currently report a live policy.

NOT IMPLEMENTED: refresh CLI, separate freshness vocabulary, preservation integration,
hooks, GUI/tray, services or native Windows transport. Human `/status` comparison remains
PENDING / NOT VERIFIED and is not a V2 blocker. No external-repository action exists.

## Commands

Run in CGC with Python 3; no installation required:

```bash
PYTHONPATH=src python3 -B -m cgc --help
PYTHONPATH=src python3 -B -m cgc status
PYTHONPATH=src python3 -B -m cgc status --json
TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -v
```

Status reads the cache only. Missing cache means UNKNOWN, with no directory creation or
source read. Human output includes source/time, observation age, policy, threshold values,
window values/reset/provenance, applicability, selection and exclusion reasons. JSON exposes
`evaluated_policy` with matching diagnostics; `historical_policy` and `last_valid_observation`
retain last-known-good. Top-level `limiting_window_ids`, minimum and policy describe current
availability only. Unknown or stale state does not advertise a current limiting window.

Default cache: `~/.codex/cgc/state.json`, not created during development. Before actual
use, the mission's default-path conflict preflight remains required. `--cache-dir` selects
a dedicated private directory whose parent exists. Use Linux-native storage for POSIX
0700/0600 enforcement. The current Windows-mounted workspace cannot enforce these modes;
CGC refuses unsafe permissions rather than weakening them. Native Windows is unsupported.

Example for a future separately authorized live operation, **not executed here**:

```bash
PYTHONPATH=src python3 -B -m cgc daemon --live --bucket codex --max-reads 1 --interval 300
```

`--live`, one or more `--bucket` and `--max-reads` are required. Selection restricts scope;
it is never proof of applicability. A live observation is retained with UNKNOWN policy
and NO_USABLE_DATA until a verified contract is implemented. Do not repeatedly poll to
resolve a missing semantic contract. No AI turn is generated.

Limits: max-reads 1–100; integer interval 60–3600 seconds (default 300); integer timeout
1–30 (default 20); maximum observation age 1–86400 (default 900). These are local bounds,
not verified upstream cadence recommendations. Foreground finite daemon only, no service.
Each iteration makes one bounded read, evaluates, atomically publishes, then waits from
completion. Failure doubles delay, capped at 3600; success resets backoff. No overlapping
or catch-up reads. SIGINT/SIGTERM interrupts waiting; in-flight reads finish or time out
before shutdown, with bounded V1 cleanup subject to OS scheduling. Writer lock covers reads
and waits within one cache directory; different directories are independent.

Status exit codes: 0 = available fresh live policy and successful last refresh; 1 = unavailable,
unknown/stale/synthetic/blocked/missing policy or refresh failure; 2 = argument/configuration,
corrupt/unsafe cache or operational error. Zero never means global all-clear. With no live
applicability contract, status cannot currently return zero for real source data.
Daemon: 0 after usable final refresh, 1 after no usable observation/final refresh failure,
2 for configuration/operational error. Diagnostics never echo raw input or exception text.

## Applicability and reasoning

`policy_version: cgc-applicability-v2.2` evaluates per-window evidence separately from scope
and validity. Operator selection, source names, bucket IDs, durations, percentages and
ordinaryUsageAllowed do not establish applicability. All observed windows have diagnostics:

- window_id and bucket_id;
- selected (boolean), applicability (APPLICABLE / NOT_APPLICABLE / UNKNOWN);
- evidence_basis (SYNTHETIC_CONTRACT / NO_EVIDENCE), numeric validity and remaining percent;
- exclusion_reasons: OUTSIDE_SELECTED_SCOPE, NOT_APPLICABLE, UNKNOWN_APPLICABILITY,
  INVALID_VALUE or UNKNOWN_VALUE, including multiple applicable exclusions.

Only selected, VALID, APPLICABLE windows enter the minimum. All tied limiting IDs are
returned in sorted order. If none qualify, policy/minimum are null, limiting IDs empty,
reason NO_KNOWN_APPLICABLE_USABLE_WINDOW. Otherwise reason is
MINIMUM_KNOWN_APPLICABLE_SELECTED_WINDOW. A 30% applicable window plus a 2% unknown
window yields scoped GREEN at 30%, PARTIAL coverage, and visible UNKNOWN diagnostics.
Coverage is never COMPLETE; `global_all_clear` always false.

Evidence is a list of at most 96 unique entries, each with exactly `window_id`,
`applicability`, `basis`, `observed_at`. IDs must occur in the normalized observation;
the timestamp must match exactly. Only SYNTHETIC_CONTRACT for synthetic observations
is accepted. Extra fields, duplicates, stale evidence, arbitrary proof text and live
synthetic evidence are rejected. The daemon's Python evidence-provider injection exists
for offline tests; no CLI flag can assert a live contract. Evidence is supplied anew per
observation and never inherited from last-known-good. V1 normalization is unchanged.

## Current and retained data

`last_observation` plus `policy` describe the latest structurally valid evaluated data,
including UNKNOWN applicability or invalid windows. `last_valid_observation` plus
`last_valid_policy` retain the most recent usable evaluation. Both pairs preserve original
observation times and independent evidence. A newer unknown/no-usable evaluation updates
diagnostics and reports NO_USABLE_DATA, without erasing last-known-good or presenting it
as the new current policy. Transport/malformed-data failures leave both pairs unchanged
and update safe refresh metadata. Mode changes and timestamp regression are rejected.

Existing freshness behavior is retained: age uses local completion time; age > max-age
withholds current policy/limit as STALE. Future timestamps give CLOCK_SKEW; explicit
ordinaryUsageAllowed=false gives USAGE_BLOCKED. Historical reasoning remains labeled.
No replenishment is inferred from reset passage. Backend sample age is unknown. A separate
freshness model is the next block. Synthetic observations never expose a live directive.

## Threshold configuration

One immutable PolicyConfig defines inclusive upper boundaries. Daemon flags `--amber-at`,
`--red-at`, `--emergency-at` accept finite percentages including fractions; defaults 20/10/5.
Require `0 <= emergency_at < red_at < amber_at <= 100`; no collapsed bands, booleans,
nonfinite/out-of-range values or rounding. GREEN is above amber_at; AMBER above red_at
through amber_at; RED above emergency_at through red_at; EMERGENCY at/below emergency_at.

Thresholds are persisted in each canonical policy. Status uses cached settings without
overrides. Invalid threshold CLI arguments are rejected before cache creation. Bucket
scope, thresholds or max-age mismatch blocks a daemon before any source read. For an
intentional configuration change, choose a new dedicated private cache directory and
retain the old cache. No config file or automatic deletion is introduced.

## Cache security and schema

Provisional schema `cgc-state-v2.2` rejects older schemas, including v2.1, without migration
or replacement. The schema/policy versions describe CGC's experimental local contract.
Each observation must reproduce exactly through V1 normalization, and each policy must
reproduce through applicability evaluation with its own evidence and common configuration.
Altered identities, diagnostics, limiting IDs, reason, values, provenance, booleans-as-numbers,
extra fields, duplicate keys and nonfinite JSON fail closed. Maximum cache size is **256 KiB**,
increased from 128 KiB for two observation/evidence pairs and tested with all 96 windows.
Source bounds remain unchanged; cache limits still fail rather than truncate state.

Every path component opens without following symlinks. Directory must be owned by the
effective user with no group/other permissions. Files must be owner-only regular files,
same owner, exactly one hard link. Creation modes 0700/0600 subject to umask. Persistent
flock inode is never unlinked; kernel releases locks on process termination. Corrupt/unsafe
cache blocks the sensor and is not repaired automatically.

Writes validate, serialize to a unique sibling, flush/fsync, atomically replace state.json,
then fsync the directory. Before-replace failure retains the old generation; post-replace
sync failure can leave the complete new generation while reporting error. This is not a
universal power-loss durability guarantee. Abrupt death may leave private temporary files;
CGC does not delete unknown artifacts. Same-user coordinated tampering is outside the
unsigned-cache integrity guarantee.

## Handoff

This is a validated applicability checkpoint, not full V2 acceptance. Current checkpoint
is HEAD after publication; exact hash and next action are in the final report and
[V2 progress](V2_PROGRESS.md). Do not redo V1 experiments, run live polling, or start V3.
Next coherent block: separate freshness/provenance. Refresh CLI remains subsequent work.
