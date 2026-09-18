# CREDID GUARDIAN CODEX (CGC) — decisions and genesis record

Date: 2026-09-17. Session: CGC repository genesis / V0 foundation.

| Decision | Rationale / consequence |
|---|---|
| Immutable product identity: CREDID GUARDIAN CODEX; CGC | Preserve the human's exact naming, including CREDID |
| GitHub identifier CREDID-GUARDIAN-CODEX | Space-free representation only; not a renamed product |
| Standalone public repository | No edits to HHS or other repositories |
| THE GUARDIAN OBSERVES. CODEX PRESERVES. | Sensor/policy does not acquire arbitrary repository authority |
| ONE SENSOR. MULTIPLE CONSUMERS. | CLI, hook and future UI share one normalized state |
| Extensible quota windows | No assumption of exactly one or two upstream windows |
| Default thresholds at 20%, 10%, 5% | Preserve exact requested policy boundaries |
| Unknown and stale are not healthy capacity | No fabricated zeros, resets or all-clear from missing data |
| Last-known-good cache plus refresh health | Survive source failures without erasing useful evidence |
| Atomic cache replacement planned | Prevent partial generations; durability still needs verification |
| Credential non-collection | Authentication remains with the owning software |
| Apache-2.0 selected by the human | Official Apache License 2.0 text included unchanged in LICENSE |
| Concept-first V0 | No fake reader, unsupported quota API or working-command claims |

## Evidence and implementation status

Authenticated account: chatgptopenaiagi, obtained through the existing GitHub CLI. gh auth status succeeded; its captured output was withheld to avoid exposing credential fields. Exact repository lookup returned HTTP 404 before creation. The requested new workspace did not exist. No authentication tokens or environment values were printed or inspected.

Sources for the architecture: the human's genesis specification. No live Codex quota, source mechanism or integration capability has been investigated or verified. Official-documentation workflow guidance was read only to avoid unsupported claims; source discovery remains deferred to V1. No upstream feature claim depends on assumed APIs.

IMPLEMENTATION STATUS: NOT YET VERIFIED for quota observation. The sole Python file is an inert package placeholder; no module command entry point, runtime policy evaluator, daemon, cache writer, hook or UI exists. No runtime test suite is claimed. Synthetic example data and expected boundaries are documentation only.

## Genesis validation and publication

Before publication, validate required files, immutable README identity, local Markdown targets, exact preservation directives, documented boundary cases, synthetic JSON syntax/consistency, Python placeholder syntax and staged whitespace. Review file contents and recognizable secret patterns without printing matching values. Validate ignore behavior for representative credential/cache paths. These checks establish foundation consistency, not live quota functionality.

Create a normal initial foundation commit and push main to the new repository; verify live remote refs/heads/main equals local HEAD and the working tree is clean. The commit cannot contain its own hash: latest foundation commit is HEAD after publication, with the resolved hash/push result in the final human report. Do not claim remote publication before verification.

## Open decisions and next scope

Supported usage source/access and schema; applicability of windows; freshness/clock-skew limits; exact source polling policy; cross-platform cache durability/permissions; integration protocol/exit codes. None blocks documenting an honest foundation.

STOP after V0 publication. Next mission: separately authorized CGC V1 source discovery and verification. No automatic service, quota request, GUI, external-repository preservation or V1 implementation.


## Genesis validation results

Completed during genesis: all 13 requested files present; README first line and canonical identity correct; 14 local Markdown links resolve; both directives match the requested text verbatim; all eight threshold examples appear consistently in policy and test theory; embedded synthetic JSON parses and its minimum/derivation agree; package AST contains only its docstring; eight representative ignore cases pass. Recognizable token/private-key/credential-URL patterns found zero matches. No runtime or live quota tests ran because no runtime implementation exists.

Apache-2.0 was explicitly selected by the human. LICENSE was retrieved unchanged from https://www.apache.org/licenses/LICENSE-2.0.txt (11,358 bytes); no dependency was installed.

HHS preservation checked read-only with Git optional locks disabled: clean main at `280b7090edf51aadf694db04d6d5f6bceff289a2`, matching its preceding checkpoint. All CGC writes used the explicit new workspace. No HHS or other project content was modified. No usage source discovery, quota request, service, registry change, model download or credential inspection occurred. Final staged whitespace, clean-tree and remote equality checks are reported after publication.


## CGC V1 — quota-source discovery and minimal reader

2026-09-17. Explicitly authorized from clean `8968cad670ce344226ebccaf4974d624594e5605`. Installed CLI 0.154.0 help and locally generated protocol schema inspected; no authentication files opened. Official documentation confirms account/rateLimits/read. Existing-daemon version check exited 1; transient stdio selected instead, without installing a daemon.

The human narrowed the experiment to exactly one app-server read before factoring the abstraction. At 2026-09-17T00:50:35.462546+00:00 that read succeeded: codex bucket, 300-minute used=64 (derived remaining=36), 10080-minute used=42 (derived remaining=58), both resets present, ordinaryUsageAllowed=true. Raw response/account identifiers/credits/plan omitted; only sanitized quota fields retained. Source is documented/experimental, not production-stable. No private backend endpoint, AI task, credential extraction or repeated polling.

Initial test-first run failed to import cgc.quota (zero test bodies ran). After the authorized experiment, implemented the smallest standard-library reader/normalizer; 21 normalization tests passed, then 31 tests including bounded synthetic transport peers passed. No second live read. Offline normalization of the retained sanitized projection succeeded. During document validation, two manually typed reset-time renderings disagreed with the code-converted Unix timestamps; corrected them to 2026-09-17T05:15:51Z and 2026-09-20T17:57:44Z before publication. No source change or further read was needed for that correction.

Later user instruction supersedes the V0 reject-before-clamp proposal for reader output: derive clamp(100-used,0,100), mark derived, retain INVALID state for out-of-range source values. Multiple buckets stay distinct; no global minimum/permission is inferred. Direct remaining exists for individualLimit in installed schema, tested synthetically but not observed live. Source sample timestamp is unavailable; local observation time is explicit.

Current-session `/status` cross-check requested from the human, NOT_VERIFIED at publication. No screenshot, account scrape or new TUI session substituted. This limitation does not erase the genuine structured read, but correspondence must not be claimed. Full evidence/candidate inventory: QUOTA_SOURCE_DISCOVERY.md. Live read authorization is consumed; stop before V2.

Created: src/cgc/quota.py; tests/test_quota.py; tests/test_quota_protocol.py; tests/fixtures/quota.json; docs/QUOTA_SOURCE_DISCOVERY.md; docs/v1-app-server-observation.json; docs/v1-normalized-observation.json. Updated: README.md, AGENTS.md, src/cgc/__init__.py, tests/README.md, docs/ARCHITECTURE.md, docs/SECURITY_MODEL.md, docs/DATA_MODEL.md, docs/PRESERVATION_POLICY.md, docs/ROADMAP.md and this decisions journal. No installs, services, GUI, hooks, daemon or HHS/other-repository operations.

Publication: inspect diff and tracked content for secrets, validate tests/docs/JSON, normal forward commit and push only CGC main, then verify HEAD/origin/main/live remote equality and clean tree. Latest commit is HEAD after publication; exact hash belongs in the final human report. Recommended next authorized mission is CGC V2 canonical cache/policy and bounded daemon, not an automatic continuation.


Final human-requested workspace integrity gate: pwd and git show-toplevel both resolve to /mnt/c/Codex-Projects/CREDID-GUARDIAN-CODEX; realpath confirms quota.py and both test modules under that root. HHS inspected read-only with optional Git locks disabled, clean at unchanged `280b7090edf51aadf694db04d6d5f6bceff289a2`. No files needed moving or restoring. The shell command workdir was explicit throughout despite the UI footer retaining HHS. No additional live quota request was made.

Final review added rejection of invalid direct remaining percentages (only derived values are clamped) and clarified local observation time as read completion, not an upstream sample timestamp. A corresponding regression brings the deterministic suite to 32 tests. Independent /status values were not provided; cross-check remains PENDING. No V2 functionality was added.

Final acceptance checks passed: 32 synthetic tests; 20 text files reviewed; three JSON files parse; Python syntax valid; 24 local Markdown targets resolve; exact preservation directives unchanged; normalized live projection reproduces offline and reset timestamps agree; recognizable credential/private-path patterns found zero matches. Pattern checks are not proof of universal secret absence. Git diff whitespace passed; origin is the CGC repository and remote main still matched the starting commit before publication. No further live request.

## CGC V2 — engine, policy, cache, status CLI and bounded daemon

2026-09-17. Explicit V2 resume mission. Entered and verified the CGC root before changes.
Clean HEAD, fetched origin/main and read-only remote main all matched
`45010646facbd75e17124e7e00572b8c34b6af27`. Read all requested V1 handoff files before
implementation. Preserved quota.py and both V1 test files unchanged. Baseline 32 tests
passed; first V2 suite passed 56; expanded safety/shutdown suite passed 60; final timestamp/cache-consistency regressions brought the suite to 62. No test
failures occurred during these runs.

Implemented engine.py, cache.py, daemon.py and __main__.py; added test_engine.py and
test_cache_daemon.py. Updated README, AGENTS, package description, architecture, data
model, security, policy, roadmap and tests documentation; added V2_OPERATIONS.md.
Thresholds remain 20/10/5, versioned cgc-default-v2. Bucket applicability requires explicit
operator selection; coverage never claims global completeness. Status is cache-only.
Failure retains last usable data, stale/skewed state loses current policy, synthetic
state cannot produce a live directive. Explicit ordinary-usage denial withholds current
policy. POSIX private cache uses no-follow paths, bounded strict decoding, atomic replace,
fsync and a process-lifetime single-writer flock. Same-user tampering is not cryptographically
prevented. Foreground daemon requires --live and a finite max-reads; default 300-second
spacing, 900-second max age and capped backoff are local engineering choices, not verified
source cadence. SIGTERM wait interruption and cross-process exclusion tested offline.

No live reads, default ~/.codex cache creation, services, installs, hooks, GUI, authentication
inspection, HHS inspection or unrelated-repository changes. Independent human /status
comparison remains PENDING / NOT VERIFIED; it did not block V2. Source maturity remains
experimental. No V2 commit or push requested/performed; modifications remain local for
review. Exact next scope and runtime limitations: V2_OPERATIONS.md. Do not automatically
run a live validation, repeat V1 discovery or advance to V3.

Final local validation: 62 tests passed in 1.917 seconds; top-level and daemon CLI help
worked without a source request. Python AST/JSON checks passed; 31 local Markdown targets
resolved; exact preservation directives and V1 reader/test bytes match the baseline.
Recognizable credential/private-key/credential-URL pattern screening found no matches
(not proof of universal absence). Git diff whitespace passed. HEAD remains the V1 baseline;
V2 consists of 10 modified tracked files and seven new files, uncommitted for review.

## V2 recovery block — full mission audit and preservation

Resumed from unchanged V1 HEAD `45010646facbd75e17124e7e00572b8c34b6af27`; fetch and
live remote main matched. The user supplied the full V2_MISSION.md and an empty-heading
V2_PROGRESS.md, so no exact next action was recorded. Chose one preservation/audit block
before feature expansion. Retained all existing code/tests and the mission text, corrected
broad completion claims to PARTIAL, and wrote the detailed acceptance gaps and next
configuration unit in V2_PROGRESS.md. No new runtime feature or V3 action.

Workspace-contained test run: 62 attempted, 48 passed, 13 errors and 1 failure. A synthetic
probe confirmed this Windows mount returns 0777 for requested 0700 creation; cache refusal
is the expected security boundary. The signal-test peer also refused its cache. All V1
and engine tests passed. Did not relax permissions, alter mount settings or silently skip
tests. Requested permission for disposable Linux /tmp synthetic cache files because the
new user instruction confines work to CGC. Publication remains conditional on validation.
Historical 62-pass evidence is retained, not presented as this session's result.

Python/JSON, local links, exact directives, unchanged V1 code/tests, bounded recognizable
credential-pattern screening, CLI help and whitespace checks passed. No live V2 quota
read occurred; no default cache or authentication path inspected. HHS was not accessed:
the current workspace-only instruction supersedes the older mission's external integrity
check. Its current state is not independently verified. Full resumable record and exact
next action are in V2_PROGRESS.md. A local partial checkpoint is authorized; normal push
requires successful validation and remote verification.

The initial staged whitespace check rejected CRLF endings in the newly supplied mission.
Normalized only its line endings to LF; mission text is unchanged. Local checkpoint
publication is withheld while supported-filesystem validation permission is pending;
remote main remains the verified V1 commit. No successful push is claimed.

Checkpoint creation initially failed because this environment had no Git author identity.
Resolved using the existing V1 commit's public author name and GitHub noreply address
as per-command Git options; no global or persistent identity configuration changed.

The subsequent full-access authorization superseded the workspace-only restriction.
Reran the complete suite with TMPDIR=/tmp: 62 passed in 1.918 seconds, zero failures,
errors or skips. Temporary cache files cleaned by tests; no dependency installation,
mount/permission weakening, system setting change or live read. HHS inspected read-only
per mission item 69: clean main at unchanged 280b7090edf51aadf694db04d6d5f6bceff289a2.
Local recovery commit d953acaab3e1024b3c099ea68cee0acb34a6c3b6 is retained; create a
normal follow-up documenting resolved validation, push both forward to CGC main, verify
local/tracking/live refs and clean tree, then stop this preservation block. Next work:
canonical configurable thresholds (mission 9, 32, 33), not V3. Final checkpoint self-reference
is HEAD; exact resolved hash/publication outcome is reported after the Git operations.


## V2 configurable thresholds — 2026-09-18

Verified clean CGC root and local/fetched/live main at
b4c05229e4d8b5210bd99821c77e46f0c0257267 before changes. Resumed the recorded
NEXT_EXACT_ACTION only: mission 9, 32, 33. Baseline 62 tests passed in 1.953s on /tmp.
Test-first import failed because PolicyConfig did not yet exist; implemented it and
70 tests passed in 1.976s, then added an old-cache disk-preservation regression.

One immutable PolicyConfig stores inclusive amber/red/emergency boundaries, default
20/10/5. Require strict ordering in [0,100] so bands cannot collapse; fractions work
without rounding. Range checking precedes isfinite to reject huge integers safely.
Persist threshold values with policy version cgc-thresholds-v2.1; advance provisional
state schema to cgc-state-v2.1 instead of silently upgrading ambiguous old caches.
Daemon mismatch blocks the sensor and preserves state; status uses cached configuration.
CLI-only settings suffice; no new hidden config file. Same-user coordinated tampering
remains outside the unsigned cache integrity guarantee.

New file: tests/test_policy_config.py. Runtime edits: engine.py, daemon.py, __main__.py.
Documentation changes and final validation are enumerated in V2_PROGRESS.md. V1 reader
and tests remain unchanged. No source/API research, live read, dependency installation,
system setting change, default cache creation or external repository mutation.
This threshold block is COMPLETE; overall V2 PARTIAL; V3 NOT_STARTED.
Checkpoint self-reference: HEAD after normal commit/publication; report resolved hash
and local/tracking/live equality after the operations. Next block is explicit per-window
applicability and constrained-window reasoning, not refresh CLI or V3.


## V2 applicability and limiting-window block — 2026-09-18

Verified clean CGC root and local/fetched/live main at
939961cdd2dc06cb7c03ad2591f25807ae1bfdcd. Resumed the exact applicability block only,
mission 10/26/47/49. Baseline 71 tests passed in 1.970s. The test-first run exposed
selection-based classification and missing evidence interfaces (10 tests: one failure,
10 errors including subtest reporting). After implementation, 81 passed in 1.996s.
The new 96-window retained-state test failed at the old 128 KiB cache bound. Raised the
fixed bound to 256 KiB to accommodate two bounded observation/evidence pairs without
weakening modes or source bounds: 86 passed in 2.054s. Final 87 passed in 2.048s.

No preserved live source evidence establishes per-window applicability. Chose honest
UNKNOWN for every live window, rather than invent a bucket/duration/selection rule.
Implemented fixed per-window applicability states with observation-bound, allowlisted
SYNTHETIC_CONTRACT assertions for offline fixtures only. No CLI proof override, arbitrary
source-contract claim or automatic inheritance. Future live applicability needs reviewed
source evidence and tests, not more polling by default.

Policy considers only valid, selected APPLICABLE windows; all other windows remain
explicit diagnostics. Tied minima include all sorted window IDs. Fixed reason codes,
thresholds and evidence reconstruct exactly through cache validation. V1 normalization
unchanged. Existing V2 tests now supply explicit fixture facts; simulated-live policy
without evidence is UNKNOWN, not an all-clear. No V1 test edits.

Schema cgc-state-v2.2 / policy cgc-applicability-v2.2 separate latest evaluated data from
last-known-good. A new unusable evaluation reports no current limit yet retains the prior
usable observation/policy. Transport failures retain both pairs; timestamp/mode checks
use latest observation even if applicability is unknown. Status gates current limits by
existing age/skew/usage checks and labels retained reasoning historical. Freshness redesign
was not started. No refresh CLI or V3 work; zero V2 live reads and no system installs.

Full inventory, validation, limitations and exact next freshness block are in
V2_PROGRESS.md. Publish a normal forward checkpoint; self-reference HEAD, resolved hash
and equality verified after publication. HHS check is read-only. Stop after preservation.

## 2026-09-18 — Freshness and provenance checkpoint

Implemented independent FRESH / STALE / UNKNOWN / ERROR age assessments and refresh
health, with CURRENT / RETAINED / HISTORICAL / UNAVAILABLE storage roles separate from
DIRECT / DERIVED / UNAVAILABLE value origins. Local completion time is the only known
age basis; backend sample time remains unavailable. Existing integer max-age 1–86400,
default 900, is inclusive at the boundary; future timestamps have no tolerance.

Failed refresh now withholds current policy even for fresh retained evidence. Stale
arrivals preserve last-known-good. Read-time age is recalculated without cache writes.
Schema cgc-state-v2.3 adds a validated temporal snapshot; incompatible older caches are
rejected without migration. Policy cgc-applicability-v2.2 and V1 normalization stay intact.
Provenance views derive from validated normalized origin fields, avoiding duplicated
cache payloads. The private 256 KiB bound remains sufficient for all 96 windows.

Test-first failures exposed missing interfaces/output, then resolved. Final 115 tests
pass; 28 added, one old failed-refresh assertion intentionally updated to require
historical rather than current RED. No live reads or persistent environment changes.
Refresh CLI remains the next separate block; full V2 remains PARTIAL.
