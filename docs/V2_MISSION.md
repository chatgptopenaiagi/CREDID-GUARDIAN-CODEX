# CREDID GUARDIAN CODEX — CGC V2

## RESUME MISSION: GUARDIAN ENGINE, POLICY, CACHE, STATUS CLI AND BOUNDED DAEMON

Resume work on the existing standalone project:

**CREDID GUARDIAN CODEX**

Canonical acronym:

**CGC**

The software name and acronym are immutable.

Do NOT rename:

`CREDID GUARDIAN CODEX`

Do NOT correct the spelling of `CREDID`.

Do NOT replace `CGC` with another acronym.

The GitHub repository already exists:

`chatgptopenaiagi/CREDID-GUARDIAN-CODEX`

Local Windows path:

`C:\Codex-Projects\CREDID-GUARDIAN-CODEX`

WSL path:

`/mnt/c/Codex-Projects/CREDID-GUARDIAN-CODEX`

This mission resumes from the successfully preserved CGC V1 checkpoint.

Expected V1 commit:

`45010646facbd75e17124e7e00572b8c34b6af27`

Expected commit message:

`feat: add verified CGC quota observation reader`

CGC V1 has already been completed and preserved.

Do NOT redo CGC V1 from scratch.

Do NOT repeat already-consumed live experiments merely to rediscover facts already preserved in the repository.

---

# 1. FIRST ACTION: ENTER THE CORRECT REPOSITORY

The previous Codex UI footer sometimes displayed the HHS directory even while CGC commands used an explicit work directory.

Therefore, before any modification, explicitly enter:

```bash
cd /mnt/c/Codex-Projects/CREDID-GUARDIAN-CODEX
```

Then verify:

```bash
pwd
git rev-parse --show-toplevel
git status --short --branch
git rev-parse HEAD
git remote -v
```

Expected repository root:

`/mnt/c/Codex-Projects/CREDID-GUARDIAN-CODEX`

Expected current baseline commit:

`45010646facbd75e17124e7e00572b8c34b6af27`

If HEAD differs from that commit because legitimate newer CGC work exists, inspect it carefully before proceeding.

Do NOT reset, force checkout, discard, or overwrite newer user work.

If the repository contains unexpected modifications, preserve them and report the discrepancy before making destructive changes.

---

# 2. VERIFY REMOTE BASELINE

Read-only verify:

```bash
git fetch origin
git rev-parse HEAD
git rev-parse origin/main
git ls-remote origin refs/heads/main
```

The previous session reported that local HEAD, origin/main, and remote main all matched.

If they still match, continue.

If they differ, inspect the divergence safely.

Do NOT force-push.

Do NOT rewrite published history.

---

# 3. PROTECT HHS AND OTHER PROJECTS

CGC is independent.

Do NOT modify:

* `/mnt/c/Codex-Projects/huggingface-helper-scanner`
* HHS
* ARX
* SWAMI OS
* VIGILIA
* BETBOY-X
* any unrelated repository

Inspect HHS only if needed to confirm integrity.

Previous preserved HHS commit:

`280b7090edf51aadf694db04d6d5f6bceff289a2`

Do not restore, reset, clean, or modify HHS unless an accidental CGC write is conclusively identified.

---

# 4. READ THE PRESERVED CGC KNOWLEDGE BEFORE CODING

Read these files completely before implementation:

```text
README.md
AGENTS.md
docs/CONCEPT.md
docs/ARCHITECTURE.md
docs/PRESERVATION_POLICY.md
docs/SECURITY_MODEL.md
docs/DATA_MODEL.md
docs/ROADMAP.md
docs/DECISIONS.md
docs/QUOTA_SOURCE_DISCOVERY.md
docs/v1-app-server-observation.json
docs/v1-normalized-observation.json
tests/README.md
src/cgc/quota.py
tests/test_quota.py
tests/test_quota_protocol.py
```

Treat these files as the authoritative preserved handoff from V1.

Do not rely on memory when the repository contains the evidence.

---

# 5. PRESERVED V1 FACTS

CGC V1 successfully established the following:

## Verified source

Codex app-server.

Verified method:

`account/rateLimits/read`

Installed CLI during V1:

`codex-cli 0.154.0`

The source is documented but experimental.

Do NOT describe it as a guaranteed stable production API.

---

## One bounded live observation was already consumed

The successful V1 live observation returned one Codex quota bucket with:

```text
300-minute window
64% used
36% remaining
remaining value DERIVED

10,080-minute window
42% used
58% remaining
remaining value DERIVED
```

Reset timestamps recorded in the preserved evidence:

```text
300-minute:
2026-09-17T05:15:51Z

10,080-minute:
2026-09-20T17:57:44Z
```

Also observed:

`ordinaryUsageAllowed = true`

Those values are historical V1 evidence.

They are NOT current quota readings.

Do not present them as current.

---

## Security result

The V1 implementation did NOT retain:

* raw authentication material
* account identifiers
* bearer tokens
* cookies
* browser credentials
* private backend credentials
* raw app-server payload containing unrelated fields

The normalized reader intentionally exposes only allowlisted quota information.

Maintain this security boundary.

---

## V1 reader

The existing reader is:

`src/cgc/quota.py`

It provides a bounded one-shot app-server reader and normalization logic.

Do not throw it away and rewrite it unnecessarily.

Review it first.

Extend it only where V2 requires changes.

---

## V1 deterministic tests

The final V1 suite passed:

`32 tests`

These tests include coverage for:

* normalization
* request framing
* multiple buckets
* direct vs derived percentages
* malformed values
* out-of-range values
* clamping behavior
* sensitive-field rejection
* timeouts
* output bounds
* synthetic app-server peers

All V2 work must preserve these passing tests.

---

## V1 limitation

The independent human `/status` cross-check remained:

`PENDING / NOT VERIFIED`

Do NOT treat that as a blocker for V2.

Do NOT automatically start an extra Codex session merely to perform that comparison.

Do NOT scrape `/status` as the production data source.

---

# 6. CORE DESIGN LAW

Preserve:

`THE GUARDIAN OBSERVES. CODEX PRESERVES.`

Also preserve:

`ONE SENSOR. MULTIPLE CONSUMERS.`

CGC should have one canonical normalized quota state.

Future components must consume that shared state instead of independently calculating quota.

---

# 7. CGC V2 MISSION

CGC V2 should transform the verified V1 sensor into a reliable local guardian engine.

The V2 goal is:

```text
V1 verified quota reader
        ↓
canonical observation model
        ↓
applicability evaluation
        ↓
policy engine
        ↓
atomic state cache
        ↓
human-readable status CLI
        ↓
machine-readable status CLI
        ↓
bounded daemon
```

CGC V2 must NOT yet perform repository preservation automatically.

CGC V2 observes, classifies and reports.

Codex preservation integration belongs to a later mission.

---

# 8. V2 COMPONENTS TO IMPLEMENT

Create or extend these conceptual components:

```text
src/cgc/quota.py
src/cgc/policy.py
src/cgc/state.py
src/cgc/daemon.py
src/cgc/cli.py
src/cgc/__main__.py
```

You may adapt names slightly only if the existing repository architecture already establishes a better consistent structure.

Do not unnecessarily create a complex framework.

Prefer Python standard library where practical.

No heavy dependency should be introduced without a clear technical need.

---

# 9. POLICY ENGINE

Implement deterministic policy evaluation.

Default thresholds:

```text
GREEN:
remaining > 20%

AMBER:
remaining > 10% and <= 20%

RED:
remaining > 5% and <= 10%

EMERGENCY:
remaining <= 5%
```

These thresholds must be configurable.

Do not hard-code them in many places.

Use one canonical policy configuration model.

---

# 10. IMPORTANT APPLICABILITY RULE

Do NOT blindly take the minimum percentage across every returned bucket.

V1 deliberately avoided calculating a global minimum because some future buckets may not apply to ordinary Codex usage.

V2 must explicitly distinguish:

```text
applicable quota windows
non-applicable quota windows
unknown applicability
invalid windows
stale windows
```

Only windows that are known to govern the relevant Codex work should influence the main preservation state.

If applicability cannot be established safely:

report:

`UNKNOWN`

Do not invent GREEN.

Do not turn unknown into EMERGENCY.

Do not silently choose the most pessimistic or optimistic value.

---

# 11. VALIDITY RULES

A quota observation used for policy must be:

* structurally valid
* within expected numeric ranges
* associated with a known observation time
* sufficiently fresh
* applicable to the relevant Codex usage
* free from credential material

An invalid window must never produce a normal policy decision.

A missing window is not zero.

An unknown window is not 100%.

A stale GREEN reading must not remain GREEN forever.

---

# 12. STALENESS MODEL

Introduce explicit freshness handling.

State must distinguish:

```text
FRESH
STALE
UNKNOWN
ERROR
```

Make freshness thresholds configurable.

Do not invent aggressive defaults without documentation.

A reasonable initial configurable model may include:

```text
fresh_for_seconds
stale_after_seconds
```

Document the chosen defaults and rationale.

Policy state and observation freshness must remain separate concepts.

Example:

```json
{
  "policy_state": "AMBER",
  "freshness": "FRESH"
}
```

or:

```json
{
  "policy_state": null,
  "freshness": "STALE"
}
```

Do not claim a stale historical observation is current.

---

# 13. CANONICAL STATE CACHE

Implement a local canonical cache.

Candidate path from architecture:

`~/.codex/cgc/state.json`

Before using that exact location, verify that it does not conflict with Codex-owned authentication or other protected files.

CGC must create only its own subdirectory:

`~/.codex/cgc/`

Do not inspect unrelated files in `~/.codex`.

Do not read authentication files.

Do not enumerate credential material.

If another safer standard user-state location is clearly preferable, document the reasoning before changing the architecture.

---

# 14. STATE MODEL

The cache should conceptually preserve:

```json
{
  "schema_version": "...",
  "generation": 1,
  "last_refresh_attempt_at": "...",
  "last_successful_observation_at": "...",
  "source": {
    "kind": "codex_app_server",
    "maturity": "experimental"
  },
  "refresh_status": "SUCCESS",
  "freshness": "FRESH",
  "policy_state": "GREEN",
  "most_constrained_applicable_remaining_percent": 36,
  "buckets": [],
  "windows": [],
  "error": null
}
```

This is conceptual.

Align it with the existing V1 data model.

Do not introduce unnecessary incompatibility.

---

# 15. LAST-KNOWN-GOOD RULE

This is critical.

If a refresh succeeds:

```text
new validated observation
        ↓
evaluate
        ↓
atomic state update
```

If a refresh fails:

DO NOT erase the previous valid observation.

Instead preserve:

```text
last known good observation
+
new refresh failure metadata
```

For example:

```json
{
  "last_successful_observation_at": "...",
  "last_refresh_attempt_at": "...",
  "refresh_status": "ERROR",
  "last_refresh_error": {
    "code": "..."
  }
}
```

Do not preserve raw secret-bearing error strings.

Use bounded safe error codes/messages.

---

# 16. ATOMIC WRITES

State cache writes must use atomic replacement.

Conceptual approach:

```text
write temporary file
        ↓
flush
        ↓
replace canonical state.json
```

Avoid partial JSON files if the process crashes.

Test atomic replacement deterministically.

Avoid deleting a valid cache before a replacement is ready.

---

# 17. FILE PERMISSIONS

Use sensible user-only permissions where supported.

Do not require root.

Do not modify system-wide permissions.

Do not weaken Codex security.

Document POSIX behavior.

Windows-specific permission hardening can remain future work if necessary, but ordinary Windows compatibility must not be falsely claimed.

---

# 18. STATUS CLI

Implement:

```bash
python -m cgc status
```

Human-readable output should be concise and useful.

Example concept:

```text
CREDID GUARDIAN CODEX

Source: Codex app-server
Observation: 2026-...
Freshness: FRESH

5-hour:
  remaining: 36%
  reset: ...

weekly:
  remaining: 58%
  reset: ...

Guardian state: GREEN
```

Do not show account identity.

Do not print raw app-server responses.

Do not print authentication information.

---

# 19. MACHINE-READABLE STATUS

Implement:

```bash
python -m cgc status --json
```

This should emit canonical safe state JSON.

Output should be suitable for future:

* Codex hooks
* desktop meter
* tray application
* monitoring scripts
* future local integrations

Machine-readable output must be stable enough to test.

Document that the schema is still provisional if it is not yet frozen.

---

# 20. REFRESH COMMAND

Consider implementing:

```bash
python -m cgc refresh
```

Behavior:

1. perform one bounded quota read;
2. normalize;
3. validate;
4. evaluate applicability;
5. evaluate policy;
6. atomically update cache;
7. report safe result;
8. exit.

This should be a one-shot operation.

It must never modify other repositories.

---

# 21. DAEMON

Implement a small foreground daemon:

```bash
python -m cgc daemon --interval 60
```

The daemon should:

```text
refresh
↓
validate
↓
evaluate policy
↓
update canonical state
↓
sleep
↓
repeat
```

Requirements:

* finite polling interval
* graceful Ctrl+C shutdown
* no busy loop
* bounded read timeout
* temporary errors tolerated
* last-known-good preserved
* no credential printing
* no arbitrary repository modifications

---

# 22. POLLING SAFETY

Do NOT assume that polling every 30 seconds is safe simply because the design originally mentioned it.

First determine a conservative default.

Because the app-server interface is experimental, use a configurable interval.

Prefer a conservative default such as:

`60 seconds`

or longer if evidence supports it.

Document the reasoning.

Do not create excessive app-server traffic.

---

# 23. LIVE TEST AUTHORIZATION

V1 consumed one live read.

For V2, do not begin with repeated live polling.

First:

1. implement using synthetic data;
2. build deterministic tests;
3. test daemon against a synthetic/local fake quota source;
4. verify cache behavior;
5. verify error behavior;
6. verify staleness behavior.

Only after all offline/synthetic tests pass may you perform a bounded live verification.

For V2, you are authorized to perform:

**at most ONE additional bounded live quota read**

solely to verify the complete V2 pipeline.

Do NOT run the daemon against the live account for an extended period during validation.

Do NOT consume quota deliberately.

Do NOT launch AI tasks to change percentages.

One live V2 refresh is enough.

If that live read is unnecessary because reliable preserved evidence can validate all V2 behavior, you may skip it and report that no live read was consumed.

---

# 24. LIVE TEST MUST NOT BECOME A MONITORING SESSION

If performing the single authorized V2 live read:

Run:

```text
one read
↓
normalize
↓
policy
↓
cache
↓
status
↓
STOP LIVE TEST
```

Do not leave the daemon running.

Do not perform repeated reads.

---

# 25. SYNTHETIC TEST MATRIX

Create deterministic tests covering at minimum:

## Policy boundaries

```text
100% → GREEN
21%  → GREEN
20%  → AMBER
11%  → AMBER
10%  → RED
6%   → RED
5%   → EMERGENCY
0%   → EMERGENCY
```

## Multiple windows

Test:

```text
5h 80%
weekly 50%
→ GREEN

5h 30%
weekly 15%
→ AMBER

5h 8%
weekly 70%
→ RED

5h 4%
weekly 80%
→ EMERGENCY
```

Only use windows marked applicable.

---

# 26. UNKNOWN APPLICABILITY TESTS

Test:

```text
known applicable 30%
unknown bucket 2%
```

The unknown 2% bucket must not automatically force EMERGENCY.

Its presence must be visible in diagnostics.

Coverage may be incomplete/unknown.

---

# 27. INVALID DATA TESTS

Test:

* negative used percentage
* used > 100
* invalid remaining percentage
* malformed duration
* malformed reset timestamp
* missing fields
* excessive bucket count
* excessive payload size
* unexpected types

Fail safely.

---

# 28. CACHE TESTS

Test:

* initial cache creation
* atomic replacement
* valid cache read
* malformed cache
* unsupported schema version
* temporary write failure
* failed refresh preserving last good state
* generation increment
* stale observation
* missing cache
* interrupted temporary write

Never fabricate a valid GREEN state after corruption.

---

# 29. DAEMON TESTS

Use synthetic sources.

Test:

* one successful iteration
* multiple iterations
* temporary source failure
* recovery after failure
* Ctrl+C / termination
* interval validation
* no busy loop
* bounded timeout
* state persistence
* no duplicate overlapping refreshes

Do not use the real Codex account for these repetitive tests.

---

# 30. SECURITY TESTS

Verify normalized/cache/CLI output cannot contain fields with obvious sensitive names such as:

```text
token
authorization
cookie
password
secret
api_key
access_token
refresh_token
```

Do not merely redact values after accepting arbitrary raw structures.

Prefer allowlisting expected quota fields.

Preserve the V1 security philosophy.

---

# 31. FAILURE BEHAVIOR

A failed refresh must NEVER produce:

```text
0% remaining
```

unless the source genuinely returned a valid zero.

A failed refresh must NEVER produce:

```text
GREEN
```

merely because no windows were returned.

Failure should be represented explicitly.

Example:

```text
REFRESH ERROR
LAST KNOWN GOOD: 14 minutes old
POLICY STATE: AMBER
FRESHNESS: STALE
```

or, if no known-good state exists:

```text
REFRESH ERROR
POLICY STATE: UNKNOWN
```

---

# 32. CONFIGURATION

Create a simple configuration model.

Potential settings:

```text
poll_interval_seconds
read_timeout_seconds
green_threshold
amber_threshold
red_threshold
stale_after_seconds
cache_path
```

Do not create a giant configuration framework.

Defaults must be documented.

Validate configuration values.

Reject nonsensical settings.

---

# 33. THRESHOLD ORDER VALIDATION

Ensure configurable thresholds cannot be inconsistent.

For example reject configurations where:

```text
emergency boundary > red boundary
red boundary > amber boundary
```

Preserve the intended ordering.

---

# 34. NO AUTOMATIC PRESERVATION YET

CGC V2 must NOT:

* edit another repository
* stage another repository
* commit another repository
* push another repository
* create handoff files in another repository
* inject instructions into active Codex jobs
* stop active Codex jobs automatically

Those behaviors belong to CGC V3.

For V2, RED and EMERGENCY are reported states only.

---

# 35. FUTURE HOOK CONTRACT

You MAY document the future interface expected by V3.

Example machine output:

```json
{
  "policy_state": "RED",
  "preservation_recommended": true
}
```

But do not implement automatic repository actions.

Do not implement a working Codex hook unless required purely as an inert interface placeholder.

---

# 36. NO GUI

Do not build:

* desktop meter
* tray icon
* GUI
* Windows widget
* web dashboard

Those belong to a later version.

CGC V2 is engine-first.

---

# 37. DOCUMENTATION UPDATES

Update at minimum:

```text
README.md
AGENTS.md
docs/ARCHITECTURE.md
docs/DATA_MODEL.md
docs/PRESERVATION_POLICY.md
docs/ROADMAP.md
docs/DECISIONS.md
```

Create additional documents only if they add real value.

Potential:

`docs/V2_GUARDIAN_ENGINE.md`

Do not create documentation merely to inflate file count.

---

# 38. README CURRENT STATUS

When V2 is complete, README should clearly distinguish:

```text
IMPLEMENTED
VERIFIED
PLANNED
NOT IMPLEMENTED
```

Do not claim V3 functionality.

Example:

```text
IMPLEMENTED:
- one-shot quota reader
- normalization
- policy engine
- canonical local state
- status CLI
- bounded foreground daemon

NOT IMPLEMENTED:
- automatic project preservation
- Codex preservation injection
- GUI
- tray icon
- Windows service
- systemd service
```

---

# 39. CODE QUALITY

Prefer:

* small functions
* explicit data boundaries
* type hints where useful
* deterministic logic
* standard library
* bounded input sizes
* safe failure behavior
* testable pure functions

Avoid:

* unnecessary async complexity
* unnecessary frameworks
* premature plugin architecture
* global mutable state
* giant monolithic files
* undocumented magic constants

---

# 40. VERSIONING

If the package exposes a version, advance it consistently.

Document what version means.

Do not claim production readiness.

CGC remains experimental software.

---

# 41. TEST COMMAND

Establish one canonical deterministic test command.

For example:

```bash
PYTHONPATH=src python3 -B -m unittest discover -s tests -v
```

All tests must pass before publication.

Report exact test count.

---

# 42. OFFLINE FIRST

The majority of V2 development and testing must be offline/synthetic.

Reuse sanitized V1 fixtures.

Do not rely on live quota state for deterministic tests.

Historical V1 quota values should remain clearly labeled historical.

---

# 43. PRESERVATION DURING THE SESSION

CGC exists to prevent lost work.

Therefore apply CGC principles to its own development.

Create meaningful checkpoints if the task becomes large.

Do not leave all important progress only in transient conversation context.

Maintain:

`docs/DECISIONS.md`

with significant architectural decisions.

If remaining Codex capacity becomes low during this mission:

STOP new development and preserve the current state.

---

# 44. SELF-PRESERVATION THRESHOLDS DURING THIS JOB

If Codex visibly reports:

## Below 20%

Do not begin optional large refactors.

Focus on completing the current coherent unit.

## Below 10%

Stop starting new features.

Run necessary tests.

Update handoff documentation.

Prepare commit/push.

## Below 5%

Immediately enter preservation mode.

Do not continue implementation.

Checkpoint safe work.

Push if authorized and validation allows.

Report remaining unfinished work.

STOP.

---

# 45. DO NOT REPEAT V1 DISCOVERY

Do NOT spend time rediscovering:

* whether app-server exists
* whether `account/rateLimits/read` exists
* whether V1 performed a successful read
* whether 300-minute and 10,080-minute windows existed in V1
* whether `ordinaryUsageAllowed` was present
* whether authentication was handled by Codex

These are preserved facts.

Only revisit them if current code or installed CLI evidence contradicts the repository.

---

# 46. COMPATIBILITY

The existing V1 reader was implemented for POSIX stdio use.

Native Windows transport was reported unsupported/not implemented.

Do not pretend native Windows support exists.

For V2, WSL is an acceptable primary execution environment.

Document Windows-native limitations.

Do not block V2 solely because Windows-native transport is incomplete.

---

# 47. PROVENANCE

Every current observation must preserve:

```text
source kind
observation time
source maturity
bucket identity
window identity
duration
used percentage
remaining percentage
direct/derived origin
reset time
validity
applicability
freshness
```

Do not blur historical and current observations.

---

# 48. RESET TIMES

Treat reset timestamps as data from a specific observation.

Do not use old V1 reset times as current future resets.

Each fresh live observation must supply its own reset data.

Synthetic tests may use arbitrary deterministic fixtures.

---

# 49. POLICY OUTPUT

The policy engine should return structured reasoning, not merely a label.

Conceptual output:

```json
{
  "policy_state": "AMBER",
  "reason": "most constrained applicable fresh window is 15%",
  "window_id": "codex:weekly",
  "remaining_percent": 15
}
```

Do not include unrestricted raw source data.

---

# 50. HUMAN STATUS OUTPUT

Make the CLI useful without being noisy.

Example:

```text
CREDID GUARDIAN CODEX — CGC

Guardian state: AMBER
Freshness: FRESH
Last refresh: 2026-...

5-hour window
  remaining: 31%
  resets: ...

weekly window
  remaining: 15%
  resets: ...

Most constrained applicable window:
  weekly — 15%

Recommendation:
  Continue with awareness. Avoid unnecessary large optional work.
```

Do not yet tell Codex to automatically act.

---

# 51. MACHINE STATUS OUTPUT

Machine output must be suitable for V3 without needing to parse human text.

Do not rely on ANSI output.

Do not mix logs with JSON stdout when `--json` is requested.

Use stderr for safe operational diagnostics where appropriate.

---

# 52. EXIT CODES

Define useful, documented exit codes.

For example:

```text
0 = valid state available
1 = operational failure
2 = invalid configuration
3 = no valid observation available
```

If policy-specific exit codes are useful for future automation, document them carefully.

Do not create surprising shell behavior.

---

# 53. LOGGING

Keep logging minimal.

Do not create verbose logs containing raw responses.

No authentication material.

No full environment dumps.

If persistent logs are not required for V2, prefer stderr and state metadata.

---

# 54. RESOURCE BOUNDS

Preserve or strengthen V1 bounds.

The reader already used explicit limits for:

* output size
* frame size
* frame count
* timeout
* bucket count

Do not remove these protections.

Extend bounded behavior to cache and daemon logic.

---

# 55. CRASH SAFETY

Test what happens if CGC terminates:

* before refresh
* during refresh
* after valid observation
* during cache temp write
* before atomic replace

The existing state must remain coherent.

---

# 56. DUPLICATE DAEMON SAFETY

Consider whether two daemon instances could overwrite the cache simultaneously.

For V2, either:

* implement a simple safe single-writer lock

or

* document that multiple simultaneous daemon instances are unsupported and detect/refuse obvious duplication

Do not silently encourage competing daemons.

Keep implementation simple.

---

# 57. CLOCK HANDLING

Use timezone-aware timestamps.

Store canonical machine timestamps in UTC.

Human output may display UTC initially.

Do not rely on naive local datetime values.

Detect obvious clock anomalies where practical.

Do not over-engineer distributed clock synchronization.

---

# 58. HISTORICAL STATE

V2 does not need a full telemetry database.

Do not build SQLite or a time-series database yet unless clearly necessary.

The first goal is:

`current canonical guardian state`

A tiny optional previous-state reference may be acceptable, but avoid scope creep.

---

# 59. PRIVACY

CGC's core state should contain only what is necessary for quota awareness.

Avoid retaining:

* email addresses
* account IDs
* organization IDs
* plan metadata unless technically necessary
* credits/payment details unless explicitly needed in future scope
* unrelated server response fields

Quota state, not identity state.

---

# 60. CONFIG FILE

If a config file is introduced, use something simple and inspectable.

Potential:

`~/.config/cgc/config.json`

or an equivalent documented path.

But do not proliferate hidden directories unnecessarily.

If configuration can remain command-line/default-based in V2, that is acceptable.

Make the simplest defensible choice.

---

# 61. PACKAGE COMMANDS

Target commands may include:

```bash
python -m cgc status
python -m cgc status --json
python -m cgc refresh
python -m cgc daemon --interval 60
```

If the existing package structure supports them cleanly, implement them.

Do not require installation simply to run tests.

Support:

`PYTHONPATH=src`

during development.

---

# 62. USER-FACING LANGUAGE

Human status output should use the canonical product name:

`CREDID GUARDIAN CODEX`

and acronym:

`CGC`

Do not rename the program.

---

# 63. V2 SUCCESS CRITERIA

CGC V2 is COMPLETE only when all of these are true:

1. V1 tests still pass.
2. policy engine exists.
3. applicability is explicit.
4. freshness/staleness is explicit.
5. canonical local state exists.
6. state writes are atomic.
7. last-known-good survives refresh failure.
8. human status command works.
9. JSON status command works.
10. refresh command works against synthetic input/tests.
11. foreground daemon works against synthetic source.
12. daemon handles temporary errors.
13. daemon stops cleanly.
14. deterministic test suite passes.
15. security review finds no credential material.
16. documentation is updated.
17. at most one authorized live V2 verification read occurred.
18. no V3 preservation automation exists.
19. HHS remains untouched.
20. repository is committed, pushed and verified.

---

# 64. DO NOT IMPLEMENT DURING V2

Do NOT implement:

* automatic repository commits
* automatic repository pushes
* arbitrary project mutation
* Codex task injection
* GUI
* tray icon
* browser extension
* Windows service
* systemd service
* cloud telemetry
* remote monitoring server
* database backend
* multi-user server
* payment tracking
* OpenAI credential management
* browser scraping
* credential extraction
* secret interception
* TLS interception
* binary patching
* private backend reverse engineering

Stay focused.

---

# 65. FINAL VALIDATION BEFORE COMMIT

Run the complete deterministic suite.

Run:

```bash
git diff --check
git status --short --branch
```

Review changed files.

Perform a bounded credential-pattern scan over tracked/changed CGC files.

Do NOT scan unrelated home directories.

Do NOT inspect auth stores.

Validate JSON files.

Validate documentation links where practical.

---

# 66. GIT COMMIT

When V2 is complete:

Suggested commit message:

`feat: add CGC guardian state and policy engine`

If the implementation includes the daemon and CLI as intended, another suitable message is:

`feat: add CGC V2 guardian engine and daemon`

Use one coherent commit unless multiple commits are genuinely useful.

Do not manufacture unnecessary history.

---

# 67. PUSH

Push only to:

`chatgptopenaiagi/CREDID-GUARDIAN-CODEX`

branch:

`main`

Do not push to HHS.

Do not create unrelated repositories.

---

# 68. VERIFY PUBLICATION

After push, verify:

```bash
git rev-parse HEAD
git rev-parse origin/main
git ls-remote origin refs/heads/main
git status --short --branch
```

Require:

`local HEAD == origin/main == live remote main`

Working tree should be clean.

---

# 69. HHS INTEGRITY CHECK

At the end, inspect HHS read-only:

```bash
git --no-optional-locks \
  -C /mnt/c/Codex-Projects/huggingface-helper-scanner \
  status --short --branch
```

If appropriate, also verify its commit.

Expected preserved commit from previous session:

`280b7090edf51aadf694db04d6d5f6bceff289a2`

Report if it changed.

Do not repair unrelated HHS changes automatically.

---

# 70. V2 PRESERVATION REPORT

Before stopping, report:

1. repository root verified
2. starting commit
3. remote baseline
4. V1 evidence reviewed
5. files created
6. files modified
7. policy engine behavior
8. applicability logic
9. freshness logic
10. cache path
11. atomic write behavior
12. last-known-good behavior
13. CLI commands implemented
14. daemon behavior
15. daemon default interval
16. configuration implemented
17. deterministic tests completed
18. exact final test count
19. security tests completed
20. live V2 requests consumed
21. live V2 result if one was performed
22. limitations
23. Windows-native limitations
24. known failures
25. work COMPLETE
26. work PARTIAL
27. work NOT_STARTED
28. Git commit hash
29. remote verification
30. HHS integrity
31. exact recommended V3 mission

---

# 71. V3 MUST REMAIN NOT STARTED

The next future mission will be:

**CGC V3 — CODEX PRESERVATION INTEGRATION**

That future version may consume CGC state and advise Codex when RED or EMERGENCY occurs.

Do NOT begin it during this task.

Do NOT modify other repositories automatically.

---

# 72. MOST IMPORTANT V2 PRINCIPLE

CGC is being created to protect finite human and computational time.

Therefore reliability is more important than feature count.

A tiny guardian that tells the truth is better than a sophisticated guardian that guesses.

Never fabricate quota state.

Never hide uncertainty.

Never erase the last known good observation because one refresh failed.

Never expose authentication material.

Never confuse historical readings with current readings.

Never let roadmap text become implicit authorization.

---

# 73. SELF-PRESERVATION RULE

If Codex usage becomes critically low while developing V2:

apply CGC philosophy to CGC itself.

When remaining capacity is low:

`PRESERVE BEFORE EXPANDING.`

Checkpoint completed coherent work.

Document:

```text
COMPLETE
PARTIAL
NOT_STARTED
TESTS PASSED
TESTS REMAINING
KNOWN FAILURES
FILES CHANGED
NEXT EXACT ACTION
```

Push a safe resumable checkpoint if validation and authorization permit.

Then stop.

Do not sacrifice preserved work trying to squeeze in one more feature.

---

# 74. START NOW

Begin with:

```text
1. enter correct CGC repository
2. verify HEAD and remote
3. read all preserved V1 evidence
4. summarize V1 implementation internally
5. design the smallest defensible V2 architecture
6. implement synthetic tests first
7. implement policy/state/cache
8. implement CLI
9. implement daemon
10. validate offline
11. optionally perform at most one bounded live V2 verification
12. finalize documentation
13. commit
14. push
15. verify
16. STOP
```

Do not ask for confirmation for ordinary implementation decisions already covered by this mission.

If a genuinely safety-critical ambiguity appears, choose the conservative behavior and document it.

Do not expand scope.

---

# FINAL SUCCESS MESSAGE

If V2 completes successfully, end with:

`CREDID GUARDIAN CODEX — CGC V2 COMPLETE.`

`GUARDIAN STATE, POLICY ENGINE, ATOMIC CACHE, STATUS CLI AND BOUNDED DAEMON VERIFIED.`

`AUTOMATIC PROJECT PRESERVATION NOT YET ENABLED.`

`CGC V3 NOT STARTED.`

`THE GUARDIAN OBSERVES. CODEX PRESERVES.`

If V2 cannot safely complete, preserve all valid work and end with:

`CREDID GUARDIAN CODEX — CGC V2 PARTIAL CHECKPOINT PRESERVED.`

Then state exactly:

* what is complete
* what remains
* what failed
* what must not be repeated
* exact next action
* commit hash
* remote state
* HHS integrity

Then STOP.
