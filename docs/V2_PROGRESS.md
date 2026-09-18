# CREDID GUARDIAN CODEX — CGC V2 progress

Overall: **PARTIAL**. Authoritative specification: [V2_MISSION.md](V2_MISSION.md).

THE GUARDIAN OBSERVES. CODEX PRESERVES.
PRESERVE BEFORE EXPANDING.

## Session block

2026-09-18: completed the recorded NEXT_EXACT_ACTION, canonical configurable policy
thresholds (mission 9, 32, 33). One coherent configuration block; no later phase started.
Read the complete mission, progress and preserved V1/V2 handoff before implementation.
Verified root `/mnt/c/Codex-Projects/CREDID-GUARDIAN-CODEX`, clean main and equality of
HEAD, fetched origin/main and live remote main at
`b4c05229e4d8b5210bd99821c77e46f0c0257267` before modifications.

## COMPLETE

- Configurable thresholds through one immutable validated PolicyConfig: defaults 20/10/5,
  fractional boundaries without rounding, strict ordering and finite [0,100] values.
- Configuration persisted in canonical policy; refresh, failed-refresh retention,
  cache validation, daemon and human/JSON status agree. Status has no threshold override.
- Daemon flags --amber-at, --red-at, --emergency-at. Invalid thresholds are rejected
  before cache creation; incompatible existing configuration blocks source reads.
- Provisional schema cgc-state-v2.1 and policy cgc-thresholds-v2.1. Old schemas are refused
  without replacing/deleting their files. Choose a new private directory for an
  intentionally changed configuration; no silent migration.
- Prior engine/cache/status/finite-daemon work retained, with POSIX atomic replacement,
  last-known-good retention, writer lock, bounded reader, backoff and stop handling.
- V1 reader and its original 32 tests unchanged; no V1 experiment repeated.

## PARTIAL

| Mission items | Existing behavior | Remaining acceptance work |
|---|---|---|
| 10, 26, 47, 49 | Explicit selected buckets; partial coverage; excluded buckets retained | Per-window APPLICABLE / NOT_APPLICABLE / UNKNOWN with evidence, diagnostics and limiting-window reasoning; selection alone is not verified applicability |
| 11, 12, 14, 47 | Structural validation, max-age and clock-skew handling | Separate FRESH / STALE / UNKNOWN / ERROR field; preserve applicability/freshness provenance |
| 13, 17, 46 | Private POSIX directory enforcement | Target-path conflict preflight before actual default-cache use; Windows mount refuses private modes; native Windows unsupported |
| 18, 19, 50–52 | Cache-only human/JSON status, including thresholds and documented exit codes | Align output with later applicability/freshness schema, source/time and constrained-window reasoning |
| 25–30, 55 | 71 deterministic tests including configuration and unsupported cache schema | Unknown vs non-applicable windows, refresh CLI, Ctrl+C and remaining crash stages |
| 37, 38, 63 | Current docs and exact progress handoff | Final full-mission acceptance remains pending |

## NOT_STARTED

- One-shot `python -m cgc refresh` CLI (mission 20 and success criterion 63.10).
- Optional single V2 live verification: **0 consumed**. Defer until offline acceptance;
  may be skipped with explicit rationale. No live polling session.
- CGC V3 — CODEX PRESERVATION INTEGRATION. Requires separate authorization after V2.
- Automatic preservation/injection, external-repository mutation, hooks, GUI/tray,
  services, installation and native Windows support.

## TESTS PASSED

Canonical command on this Windows-mounted WSL checkout:

```bash
TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -v
```

Final: **71 tests passed in 1.991 seconds; zero failures, errors or skips.**
Baseline: 62 passed in 1.953s. First test-first invocation failed to import the not-yet
implemented PolicyConfig (one loader error, zero new test bodies); resolved by implementation.
Intermediate: 70 passed in 1.976s, followed by a disk-cache preservation regression.

Nine new tests cover defaults, alternate/fractional boundaries, invalid ordering,
booleans/nonfinite/out-of-range/huge integers, strict configuration projection, custom
refresh/failure retention, cache tampering/schema rejection, daemon mismatch before source
reads, equivalent integer/float configuration, CLI forwarding and human/JSON consistency.
Original synthetic protocol, privacy, atomic-write, locking and SIGTERM tests still pass.
Tests use disposable Linux-native caches and synthetic peers only.

Additional publication checks: Python AST, JSON syntax, local Markdown targets, CLI help,
unchanged V1 reader/tests and verbatim preservation directives, bounded recognizable
credential-pattern screening, Git whitespace and changed-content review. Exact results
are recorded below after validation. Pattern screening is not proof of universal secrecy.

## TESTS REMAINING

Add deterministic tests alongside the remaining applicability/freshness, refresh command,
crash-stage and Ctrl+C acceptance work. Full V2 acceptance is not claimed by 71 passing tests.

## KNOWN_FAILURES AND DISCOVERIES

- No unresolved test failure in this block. Expected initial missing-class import resolved.
- Windows-mounted workspace cannot enforce required 0700 semantics. Earlier recovery run
  had 48 passes, 13 errors and one failure; Linux /tmp resolved that validation blocker.
  Do not weaken private-cache checks. Historical details remain in DECISIONS.md and
  checkpoint b4c05229e4d8b5210bd99821c77e46f0c0257267.
- Strict threshold ordering intentionally rejects equal boundaries, preventing collapsed bands.
- Huge integer percentage validation must check range before math.isfinite conversion.
- Old cache schema is intentionally incompatible and preserved; no automatic migration.
- Applicability is still operator selection, freshness still encoded in validity.
  Backend sample age, supported cadence and complete applicability remain UNKNOWN.
- Independent human `/status` cross-check remains PENDING / NOT VERIFIED, not a blocker.

## FILES_CHANGED

Created: `tests/test_policy_config.py`.

Modified runtime: `src/cgc/engine.py`, `src/cgc/daemon.py`, `src/cgc/__main__.py`.

Modified documentation: `README.md`, `AGENTS.md`, `docs/ARCHITECTURE.md`,
`docs/DATA_MODEL.md`, `docs/PRESERVATION_POLICY.md`, `docs/ROADMAP.md`,
`docs/DECISIONS.md`, `docs/V2_OPERATIONS.md`, `docs/V2_PROGRESS.md`, `tests/README.md`.

No V1 normalization change; no cache permission weakening; no unrelated project changes.

## NEXT_EXACT_ACTION

Verify this published checkpoint, then implement one explicit **per-window applicability
and limiting-window reasoning** block (mission 10, 26, 47, 49). Write synthetic tests first:
known applicable 30% plus unknown 2% must not force EMERGENCY; distinguish explicitly
non-applicable from unknown; no known applicable usable window must yield UNKNOWN;
invalid selected windows must remain diagnostic. Define a bounded, allowlisted evidence
model without inferring applicability from duration or bucket name and without treating
operator selection as verified source semantics. Carry applicability and constrained-window
identity/reason consistently through canonical cache validation and human/JSON status.
Preserve V1 normalization and last-known-good; version the provisional cache if required.
Stop at that coherent unit, document/test/checkpoint/push. Keep separate freshness redesign
and refresh CLI for subsequent blocks. No live reads or V3 work in that applicability block.

## LAST_SAFE_COMMIT

Starting published checkpoint: `b4c05229e4d8b5210bd99821c77e46f0c0257267`.
Current configurable-threshold checkpoint: **HEAD after commit/publication** (a document
cannot contain its own commit hash). Normal forward push only to
`chatgptopenaiagi/CREDID-GUARDIAN-CODEX` main. Verify local HEAD = origin/main = live
remote main and clean tree; resolved hash and outcome belong in the final report.

## Operations and integrity

Live reads: V1 historical **1**; V2 this session **0**, V2 total **0**.
No source/API rediscovery, default ~/.codex cache creation, credential inspection,
package installation, persistent system/environment changes, services or GUI.
Only disposable /tmp synthetic test caches were used and cleaned by test context managers.
No capacity indicator or threshold crossing was observed; preservation is scope-driven.
Git author identity, if needed, uses existing public commit metadata via per-command
options, without persistent configuration changes. HHS integrity is checked read-only
under mission item 69; outcome recorded below. No unrelated repository is modified.

Final publication gates passed: 11 Python files parse; three JSON files parse;
43 local Markdown targets resolve; daemon help exposes threshold flags without a
source read; V1 reader/test bytes and verbatim directives are unchanged; recognizable
credential-pattern scan found zero matches; Git whitespace passed. HHS is clean on
main at unchanged `280b7090edf51aadf694db04d6d5f6bceff289a2` (read-only check).
The user's emergency-preservation steering arrived after these gates; no new work
was started. Proceed only with the coherent local checkpoint and verified publication.

User-added change preserved: docs/V2_MISSION.md now includes the supplied LOW-CAPACITY
EMERGENCY PRESERVATION instructions. Reviewed this concurrent documentation addition
and include it unchanged in the checkpoint; it is also part of FILES_CHANGED.
