# CREDID GUARDIAN CODEX (CGC) — security model

## V2 current status

V2 is COMPLETE under offline POSIX acceptance. The earlier 62-test POSIX run is historical verification of the existing
implementation, not full mission acceptance. See [current progress](V2_PROGRESS.md) for current validation and remaining requirements.
See [V2 operations and handoff](V2_OPERATIONS.md) for the canonical state, scoped policy, atomic cache, status CLI,
finite daemon, security limits and validation evidence. No V2 live quota request ran.
The V0/V1 descriptions and future proposals below are retained as historical context;
V2 operations supersedes their statements that policy/cache/CLI/daemon are unimplemented.
Hooks, GUI and preservation execution remain unimplemented.


## Minimum privilege

THE GUARDIAN OBSERVES. CODEX PRESERVES.

CGC should need only a permitted usage-information interface and its own tiny cache. Authentication remains under the control of the software that owns it. Prefer an already-authenticated supported local/internal usage interface if one is verified; V1 verified one such app-server read (experimental protocol; see QUOTA_SOURCE_DISCOVERY.md). Do not obtain credential material to make an otherwise inaccessible source work.

## Absolute prohibitions

CGC must never expose or print GitHub/OpenAI/other authentication tokens; commit credentials; read/export Codex authentication files; modify Codex authentication; inspect browser password databases; scrape cookies; steal session tokens; inspect unrelated credentials; send credentials to external services; disable security software; or bypass authorization controls.

Do not dump environment variables or raw authentication responses. No browser-profile inspection, credential-store enumeration, credential copying, interception or private endpoint reverse engineering is authorized by this foundation. A source unavailable within these boundaries remains unavailable.

## Boundaries and threats

| Boundary/threat | Required design |
|---|---|
| Source may be malformed, stale or misleading | Bounded reads, strict validation, explicit timestamps, source provenance and uncertainty |
| Returned strings may contain instructions or secrets | Treat data as inert; allowlist normalized fields; omit raw bodies and sanitize diagnostics |
| Cache may be corrupted or tampered with | Revalidate structure/provenance; do not execute cached content; report corruption |
| Credential leakage through logs/errors | No credential collection; safe error classes, not raw responses; review public artifacts |
| Concurrent/crashed writer | Single-writer policy and atomic replacement; retain last-known-good observation |
| False GREEN from missing windows | Explicit coverage and validity; no all-clear for unknown/stale/partial information |
| Policy signal mistaken for permission | Hook reports only; current project policy/user authorization controls Codex actions |
| Arbitrary repository mutation | Guardian has no external-repository editing, Git commit/push or repair subsystem |

Redaction is defense in depth, not a substitute for collecting less. Never claim a pattern scan proves no secrets exist. Future tests must verify representative leak paths without using real credentials.

## Cache and integration

The proposed ~/.codex/cgc/state.json contains normalized quota information only, not identities/tokens/raw account responses. Use owner-restricted access where supported and document Windows/WSL filesystem limitations. Path safety, symlinks, concurrency and atomic replacement must be validated before implementation claims. Observation failure preserves last valid data while reporting current failure/age.

CGC does not autonomously edit arbitrary projects. Codex may act on a directive only within its current task and repository policy. A plan, cached state or hook output cannot authorize commits, pushes, history rewrites or deletion.

## Genesis operational scope

The human authorized GitHub account verification through the existing CLI, repository existence checking, creation of a new public repository and normal publication. Authentication status output is withheld rather than logging token fields. No new token is requested. This output workflow is distinct from CGC runtime behavior.

No live quota investigation, authentication-file inspection, installations, services, registry changes, GUI/tray, browser access or unrelated repository modifications occur in genesis. V1 must be explicitly authorized before source discovery.


## V1 observed boundary

CGC executed one initialize/initialized/account/rateLimits/read exchange over a transient stdio child. No raw response, initialization identity/path data or stderr was retained. Quota fields were screened/projected in memory first. Codex handled its own authentication; CGC did not inspect, copy, parse or change any authentication file or token. No private HTTP endpoint, browser state, environment dump, AI turn, services or external-repository operation was used. Ordinary internal Codex startup/authentication bookkeeping is not an audited zero-write guarantee.

The prototype refuses server requests (including external token refresh/attestation); it never answers them with credentials. It reports fixed failure codes, rejects recognized sensitive field names, constrains identifiers and discards unneeded fields. Tests use synthetic secret strings, not credentials. No filter proves universal secrecy; minimized collection/export remains primary. POSIX time/byte/frame/process-termination behavior is tested with synthetic peers; native Windows is unsupported. The one allowed live experiment is consumed.


## V2 applicability evidence boundary

Schema cgc-state-v2.3 accepts at most 96 unique evidence entries for windows actually
present in the associated normalized observation. Exact fields: window_id,
applicability, basis, observed_at. Applicability is a fixed enum; the only accepted
basis is SYNTHETIC_CONTRACT, and only for synthetic observations with the exact same
timestamp. Arbitrary descriptions, URLs, proof strings, identities and extra keys are
rejected. Operator selection and ordinaryUsageAllowed never establish applicability.
No live contract is verified; live windows remain UNKNOWN and no live directive results.
The daemon's injectable evidence provider is an offline Python test seam, not a CLI
proof override. New observations do not inherit evidence from earlier observations.
Cache reconstruction validates current and retained historical policies independently;
no cached label or limiting ID is trusted without recomputation. Cache bound is 256 KiB
for two bounded observations/evaluations, tested with all 96 windows. POSIX modes,
no-follow path checks, locking and atomic replacement are unchanged. Same-user coordinated
tampering remains outside the unsigned cache guarantee; synthetic data cannot prove live facts.

Freshness/provenance is IMPLEMENTED and VERIFIED OFFLINE: separate age, refresh health
and policy authority; failed refresh withholds current policy while retaining evidence.
See [V2 operations](V2_OPERATIONS.md) for canonical semantics and schema details.

Final V2 offline acceptance: [evidence matrix](V2_ACCEPTANCE.md).
153 deterministic tests pass. Zero V2 live reads; optional live verification skipped.
V3 remains NOT_STARTED and requires separate authorization.

## V3 current frontier

V3 is authorized and PARTIAL. The initial pure preservation attempt contract and lifecycle
are implemented/tested; project inspection, handoff writes, Git mutation and automation
are NOT_STARTED. There is no preserve CLI yet. V1/V2 remain accepted and unchanged.
Resume by present repository evidence and [V3 progress](V3_PROGRESS.md), under the complete
[V3 mission](V3_MISSION.md) and current user instructions. Historical V2 notes
that V3 was not authorized describe the earlier boundary; this explicit V3 mission
supersedes that boundary without authorizing unrelated project mutation or V4.
