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
