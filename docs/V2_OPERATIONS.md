# CREDID GUARDIAN CODEX (CGC) — V2 operations

THE GUARDIAN OBSERVES. CODEX PRESERVES.
ONE SENSOR. MULTIPLE CONSUMERS.

## Status and boundaries

V2 is PARTIAL against [the full mission](V2_MISSION.md). See [progress](V2_PROGRESS.md)
for current test results, acceptance gaps and the exact next block. The schema is provisional.

IMPLEMENTED: pure policy engine, canonical versioned state, private POSIX atomic cache,
cache-only human/JSON status and finite foreground daemon. VERIFIED: 71 offline tests,
including the original 32 V1 tests. No V2 live source request or sustained live polling
was performed. The experimental V1 app-server reader is unchanged.

PLANNED: supported preservation integration, hook, GUI/tray and native Windows support.
No service, startup entry, registry change, dependency installation, external repository
action or preservation execution exists. The independent human `/status` comparison
remains PENDING / NOT VERIFIED and is not a V2 blocker.

## Commands

Run from the CGC root with Python 3 and `PYTHONPATH=src`; no installation is required.

```bash
PYTHONPATH=src python3 -B -m cgc --help
PYTHONPATH=src python3 -B -m cgc status
PYTHONPATH=src python3 -B -m cgc status --json
PYTHONPATH=src python3 -B -m unittest discover -s tests -v
```

Status only reads the cache. A missing cache reports UNKNOWN without creating a
directory or initiating Codex. Human output includes age, refresh health, coverage,
mode, per-window validity, remaining provenance and reset timestamps. JSON includes
the same observation plus canonical historical policy and current policy availability.

Default cache: `~/.codex/cgc/state.json`. Only this dedicated directory and fixed
CGC cache/lock basenames are accessed; authentication files are never opened.
No default cache was created during V2 development. `--cache-dir` selects another
CGC-owned private directory; its parent must exist. Use a dedicated Linux filesystem
directory with enforced POSIX owner permissions. Native Windows is unsupported.
WSL access to Windows-mounted filesystems may reject the permissions checks; CGC
fails closed rather than relaxing permissions or claiming Windows ACL protection.

A future operator-authorized live run can use this command; **it was not executed**:

```bash
PYTHONPATH=src python3 -B -m cgc daemon --live --bucket codex --max-reads 1 --interval 300
```

`--live`, at least one `--bucket`, and `--max-reads` are required. This initiates real
quota reads through the existing V1 reader. It performs no AI turn. A daemon invocation
is a foreground finite process, not a background service. Maximum reads: 1–100;
interval: integer 60–3600 seconds, default 300; timeout: integer 1–30 seconds,
default 20; maximum observation age: integer 1–86400 seconds, default 900.
These are local engineering bounds, **not verified upstream polling recommendations**.
Source polling constraints, backend sample age and sustained reliability remain UNKNOWN.

Each iteration makes one bounded read, normalizes/classifies, publishes one generation,
then waits from completion. Failure waits double (first failure: twice the configured
interval), capped at 3600 seconds; success resets backoff. No overlapping or catch-up
reads. At most the requested number of attempts are consumed. SIGINT/SIGTERM wakes
waiting immediately; an in-flight V1 read completes or times out before exit (up to
30 seconds plus bounded V1 process cleanup, subject to OS scheduling). The writer lock
covers the entire run, including source reads and waits. Locks coordinate only writers
sharing the same cache directory; separate explicitly selected directories are independent.

Status exit codes: 0 = fresh live scoped policy with successful last refresh;
1 = unavailable/stale/synthetic/blocked/missing data or last refresh failed; 2 = invalid
arguments, corrupt/unsafe cache or operational failure. **0 never means global all-clear**
and is independent of GREEN/AMBER/RED/EMERGENCY. Daemon: 0 after successful final
refresh, 1 with no observation or final refresh failure, 2 on operational/configuration
failure. Signal-stopped runs report `stopped: true` and the attempt count.
Errors use fixed diagnostics; raw source text, arbitrary arguments and paths are not echoed.

## Applicability, policy and freshness

Policy version `cgc-thresholds-v2.1` uses validated configurable thresholds, defaulting
to 20/10/5 without rounding. Operator-selected bucket identities define the scope; their selection is
explicitly labeled `explicit_operator_selection`, not verified universal applicability.
All recognized usable windows in that scope participate, including individual limits;
other buckets remain visible but do not lower the selected minimum. Missing buckets
and invalid/unknown selected windows are explicit. There is no duration-based applicability
guess. Coverage stays PARTIAL when usable windows exist, otherwise UNKNOWN. The source's
unrecognized-field coverage remains UNKNOWN. `global_all_clear` is always false.

A successful refresh requires at least one usable selected window. Empty, invalid,
failed or irrelevant observations retain the last usable observation and its original
timestamp, with new failure metadata. A partial observation may become the latest
usable observation; coverage never claims completeness. Reset passage never replenishes
capacity. Explicit `ordinaryUsageAllowed=false` withholds current policy/directive and
reports USAGE_BLOCKED. Unknown allowance is retained as unknown.

Age uses local completion time and the current clock. At age > max-age, current policy
is null and validity STALE; historical policy remains visible. Future observation/cache
write timestamps report CLOCK_SKEW with no current directive. There is no clock-skew
tolerance. Refresh timestamps older than retained observations are rejected without
replacing the cache. Fresh retained data after failure remains available with explicit
failed refresh health; it ages normally and cannot reset its timestamp on failure.

Synthetic observations remain labeled. They can demonstrate classification but never
expose a live directive or `live_policy_available=true`. Mixed live/synthetic cache
refreshes are rejected. A cache's bucket scope, thresholds and max-age cannot silently change during
a daemon run; use a separately designated private directory for a changed configuration.

## Cache security and failure behavior

`cgc-state-v2.1` stores generation, maximum age, last_valid_observation, canonical policy,
last_refresh_attempt_at/status, fixed error_code and cache_written_at. The V1 observation
must exactly reproduce through V1 normalization; altered provenance, validity, values,
extra identity fields, duplicate JSON keys and nonfinite numbers are rejected. Cached
policy must match the engine's policy. Maximum file size is 128 KiB.

Every path component is opened without following symlinks. The dedicated directory
must be owned by the effective user with no group/other permissions. Files must be
owner-only regular files, owned by the effective user, with exactly one hard link.
New directory/files use 0700/0600 subject to umask. The persistent lock inode is never
unlinked; POSIX flock releases automatically on process termination. A corrupt or
unsafe cache blocks the writer before a source request; it is not silently repaired.

Writes validate first, serialize to a unique sibling, flush/fsync it, atomically replace
state.json and fsync the directory. Readers see an old or new complete generation.
Before-replace failure retains the old generation; directory-fsync failure after replace
can leave the new complete generation while reporting failure. Atomic visibility is
not a universal power-loss durability guarantee. Abrupt process death before replacement
may leave a private temporary file; CGC does not automatically delete unknown artifacts.
Same-user malicious processes and privileged filesystem attackers are outside the
integrity guarantee; this is not a signed or tamper-proof quota attestation.

## Handoff

The full mission audit found missing requirements that the earlier implementation summary
had not accounted for. This is a partial checkpoint, not a V2 completion claim. The prior
safe commit is `45010646facbd75e17124e7e00572b8c34b6af27`; the current checkpoint is HEAD
after publication. [V2 progress](V2_PROGRESS.md) records tests, failures and next scope.
No live V2 quota read has been consumed. V1 values remain historical.

Do not invoke the optional live test before the offline acceptance gaps are resolved.
Do not repeat V1 discovery or start V3, services or GUI. Current status relies on explicit
operator bucket selection, not established per-window applicability. Thresholds are configurable; freshness is currently encoded in validity, and the refresh
subcommand is absent.
These gaps must be closed before claiming full mission acceptance.

## Threshold configuration (implemented and verified offline)

The immutable `PolicyConfig` in engine.py is the single threshold model. Daemon flags
`--amber-at`, `--red-at`, `--emergency-at` accept percentages, including fractions;
defaults are 20, 10, 5. Require `0 <= emergency_at < red_at < amber_at <= 100`.
Equal boundaries are rejected to avoid collapsing a policy band. Booleans, strings
in the Python/cache model, nonfinite and out-of-range values are rejected.
GREEN is above amber_at; AMBER is above red_at through amber_at; RED is above
emergency_at through red_at; EMERGENCY is at or below emergency_at. No rounding.

The canonical policy includes `thresholds: {amber_at, red_at, emergency_at}`.
Refresh, failed-refresh retention, cache validation and both status formats use that
configuration. Status has no override flags and performs no source read. Human status
prints boundaries; JSON exposes them under historical_policy even when current data
is stale. Invalid threshold CLI options return 2 before creating a cache.

The schema advances to `cgc-state-v2.1`; old `cgc-state-v2` caches are refused, preserved
and never silently migrated. A mismatched daemon configuration is rejected before a
source request or state replacement. To intentionally use a different configuration,
select a new dedicated private cache directory; retain the old cache. No config file,
installation or automatic cache deletion is introduced. These versions describe CGC's
experimental local contract, not an upstream API version or production-readiness claim.
