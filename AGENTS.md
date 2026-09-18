# CREDID GUARDIAN CODEX (CGC) — agent instructions

The immutable product name is CREDID GUARDIAN CODEX. The immutable acronym is CGC. Never correct CREDID, reorder the name or introduce another acronym. CREDID-GUARDIAN-CODEX is only the GitHub-safe repository identifier.

Read README.md, docs/DECISIONS.md, docs/ROADMAP.md, docs/SECURITY_MODEL.md and docs/PRESERVATION_POLICY.md before work.

THE GUARDIAN OBSERVES. CODEX PRESERVES.
ONE SENSOR. MULTIPLE CONSUMERS.

V0 foundation and V1 quota-source experiment are complete. Read docs/QUOTA_SOURCE_DISCOVERY.md before continuation. One live app-server read is consumed; do not repeat it without a new task. V2 is PARTIAL: engine, configurable thresholds, explicit per-window applicability/limiting reasoning, cache, status CLI and finite foreground daemon exist. The provisional cache schema is cgc-state-v2.3; older caches are refused without migration. Only bounded observation-bound synthetic applicability evidence is accepted; live applicability remains UNKNOWN. Operator selection is not proof. Read the complete docs/V2_MISSION.md and docs/V2_PROGRESS.md before resuming; resume from NEXT_EXACT_ACTION. docs/V2_OPERATIONS.md describes current behavior, not full mission acceptance. No V2 live quota read was consumed. No hook or GUI exists. The V2 mission permits at most one optional bounded live verification after offline acceptance; none has been consumed. Do not repeat live reads. V3 requires separate authorization and remains NOT_STARTED. Do not fabricate a reader/API or claim unimplemented commands work. Roadmap entries are not authorization. Distinguish CONCEPT, IMPLEMENTED, VERIFIED and PLANNED; missing information remains UNKNOWN.

This repository is standalone. Do not modify HHS, huggingface-helper-scanner, ARX, SWAMI OS, VIGILIA, BETBOY-X or unrelated repositories. CGC must not autonomously modify external repositories. Preserve user changes; never reset, force-push, amend published history or discard work.

Never inspect, print, copy, commit or export tokens, Codex authentication files, browser cookies/passwords or unrelated credentials. Do not alter authentication or security controls. A supported reader should consume usage information under owner-controlled authentication. Do not dump the environment. Report security findings by class/location, never by secret value.

No services, registry changes, GUI/tray, dependency installation, live account quota investigation or broad implementation during genesis. No cache under ~/.codex is created in V0. GitHub authentication verification and this repository's normal initial publication are authorized output operations; they do not authorize other system/repository changes.

Future preservation is policy reporting, not execution permission. Codex may checkpoint/push only under the target repository's policy and current authorization. Validate tracked content before public publication. Record tests actually run, failures, live operations consumed and exact next scope. Use HEAD for a commit's self-reference and report its resolved hash after publication; never invent a self-containing hash.

Preserve current work when the human requests a checkpoint. Do not claim to monitor an inaccessible usage indicator or fabricate a threshold crossing. Future budget-trigger behavior depends on an actual usable observation.

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
after SIGKILL of CGC are not guaranteed. Default-target preflight/final audit remain pending.
