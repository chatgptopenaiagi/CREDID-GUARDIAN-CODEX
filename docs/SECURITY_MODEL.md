# CREDID GUARDIAN CODEX (CGC) — security model

## Minimum privilege

THE GUARDIAN OBSERVES. CODEX PRESERVES.

CGC should need only a permitted usage-information interface and its own tiny cache. Authentication remains under the control of the software that owns it. Prefer an already-authenticated supported local/internal usage interface if one is verified; its existence is NOT YET VERIFIED. Do not obtain credential material to make an otherwise inaccessible source work.

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
