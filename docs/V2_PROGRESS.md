# CREDID GUARDIAN CODEX — CGC V2 progress

Overall: **PARTIAL**. This file records observed evidence, not a completion claim.
Authoritative specification: [V2_MISSION.md](V2_MISSION.md).

THE GUARDIAN OBSERVES. CODEX PRESERVES.
PRESERVE BEFORE EXPANDING.

## Session block

Recovery, mission audit, validation and preservation of the previously uncommitted V2
implementation. No new runtime feature was added. On entry this file contained only
bare headings, with no NEXT_EXACT_ACTION or LAST_SAFE_COMMIT value. Therefore there
was no exact action to resume; the conservative recovery action was to audit and
preserve existing work before expanding it. This block addresses mission preservation
items 43 and 65–68, not a new implementation phase.

Repository root verified: `/mnt/c/Codex-Projects/CREDID-GUARDIAN-CODEX`.
Starting HEAD, fetched origin/main and live remote main all matched
`45010646facbd75e17124e7e00572b8c34b6af27` (V1). Existing modifications were preserved.
The newly supplied mission file was read completely and retained without text edits (CRLF line endings normalized to LF for Git whitespace validation).

## COMPLETE

- V1 reader/evidence retained; original reader and two V1 test modules match HEAD.
- Initial deterministic 20/10/5 classifier and normalized observation validation.
- Canonical last-known-good state with refresh failure metadata and generation counter.
- POSIX private cache with atomic replacement, bounded decoding and writer lock.
- Cache-only human/JSON status and finite foreground daemon with injected test sensor,
  timeout bounds, backoff and stop handling. These exist; limitations below still apply.
- Full mission audit and honest PARTIAL labels replace earlier broad completion claims.
- Recovered progress record, documented remaining work and checkpoint scope.

## PARTIAL

| Mission items | Existing behavior | Remaining acceptance work |
|---|---|---|
| 9, 32, 33 | Fixed thresholds; validated individual runtime options | Canonical configurable thresholds, ordering validation and CLI/cache consistency tests |
| 10, 26, 47, 49 | Explicit selected buckets; partial coverage; excluded buckets retained in observation | Per-window APPLICABLE / NOT_APPLICABLE / UNKNOWN with evidence, diagnostics and limiting-window reasoning; selection alone is not verified applicability |
| 11, 12, 14, 47 | Structural validation, max-age and clock-skew handling | Separate FRESH / STALE / UNKNOWN / ERROR field; preserve applicability/freshness provenance |
| 13, 17, 46 | Default path specified; private POSIX directory enforcement | Target-path conflict preflight before actual default-cache use; workspace mount rejects private modes; native Windows unsupported |
| 18, 19, 50–52 | Human and JSON commands with documented exit codes | Align output with updated policy/freshness schema; test human output, source/time and constrained-window reasoning |
| 25–30, 55 | 62 deterministic tests exist; original 32 included | Complete mission matrix: custom configuration, unknown vs non-applicable windows, refresh CLI, unsupported schema, Ctrl+C and remaining crash stages |
| 37, 38, 63 | Operating docs and progress recovered | Final full-mission acceptance and final completion report remain pending |

## NOT_STARTED

- One-shot `python -m cgc refresh` CLI (mission 20 and success criterion 63.10).
- Optional single V2 live verification: **0 consumed**. Defer until offline acceptance;
  may be skipped with an explicit rationale. No live polling session authorized here.
- CGC V3 — CODEX PRESERVATION INTEGRATION. No automatic preservation, injection,
  external-repository mutation, hook, GUI/tray, service or installation.

## TESTS

Historical prior-session evidence: 62 tests passed using POSIX temporary caches.
Current-session workspace-contained command:

```bash
TMPDIR="$PWD/.cgc/test-tmp" PYTHONPATH=src python3 -B -m unittest discover -s tests -v
```

Result: **62 run; 48 passed, 13 errors, 1 failure**. All 32 V1 tests and 15 engine tests
passed; cache-missing status passed. The other 14 cache/daemon tests could not exercise
their intended behavior because the workspace mount did not honor owner-only directory
creation. The signal test failed waiting for a peer that had already refused its cache.
No real Codex process or live quota read was used.

A bounded synthetic directory probe confirmed `mkdir(mode=0700)` yields mode `0777`
on this workspace mount. No security checks or mount settings were weakened. Temporary
probe/test directories were cleaned by their context managers; ignored `.cgc/test-tmp`
is the test root. Authorization to use disposable Linux /tmp test caches was requested,
because the current instruction limits work to CGC. No such outside write has occurred
in this session while that question is pending.

Other checks passed: Python AST, JSON parsing, 42 local Markdown targets, unchanged exact
preservation directives, unchanged V1 reader/tests, CLI help and Git diff whitespace. The initial staged whitespace check rejected the
user-supplied mission CRLF endings; normalizing only line endings to LF resolved this.
Bounded recognizable credential/private-key/credential-URL screening of CGC candidate
files found no matches; this is not proof of universal secret absence.

Tests remaining: rerun all 62 on a permitted filesystem enforcing POSIX modes, then add
tests alongside each remaining acceptance unit listed above. Current failed execution
must not be replaced by a claim that the historical 62-pass run happened this session.

## KNOWN_FAILURES

- Workspace-only cache validation is blocked by the Windows mount's permission semantics.
- No NEXT_EXACT_ACTION existed in the supplied initial progress stub; recovered here.
- Earlier docs overclaimed V2 completion against the now-complete mission; corrected.
- Configurable thresholds, full applicability/freshness output and refresh CLI are gaps,
  not completed features. Source stability/cadence and backend sample age remain UNKNOWN.
- Independent human `/status` comparison remains PENDING / NOT VERIFIED; not a blocker.

## FILES_CHANGED

Preserved new implementation files: `src/cgc/engine.py`, `src/cgc/cache.py`,
`src/cgc/daemon.py`, `src/cgc/__main__.py`, `tests/test_engine.py`,
`tests/test_cache_daemon.py`, `docs/V2_OPERATIONS.md`.

Preserved prior modifications and updated handoff: `README.md`, `AGENTS.md`,
`docs/ARCHITECTURE.md`, `docs/DATA_MODEL.md`, `docs/DECISIONS.md`,
`docs/PRESERVATION_POLICY.md`, `docs/ROADMAP.md`, `docs/SECURITY_MODEL.md`,
`tests/README.md`, `src/cgc/__init__.py`.

New user-supplied files included in this checkpoint: `docs/V2_MISSION.md` (text unchanged; LF line endings)
and `docs/V2_PROGRESS.md` (expanded from the empty heading stub).
No runtime source/test edits were made in this recovery session.

## NEXT_EXACT_ACTION

First resolve the permitted location for POSIX synthetic cache validation and rerun the
complete deterministic suite without weakening cache security. If all tests pass, finish
normal checkpoint publication and verify HEAD = origin/main = remote main.

After that preservation gate, the next implementation block is **canonical configurable
policy thresholds** (mission 9, 32, 33): add tests first for defaults, alternate/fractional
boundaries, ordering, booleans/nonfinite/out-of-range values; implement one validated
configuration carried through classification, cache validation, daemon and CLI without
changing V1 normalization; reject incompatible cached configuration; update docs and
checkpoint. Stop at that coherent unit. Keep applicability/freshness redesign and refresh
CLI as subsequent blocks. No live reads or V3 work in that configuration block.

## LAST_SAFE_COMMIT

Verified published baseline: `45010646facbd75e17124e7e00572b8c34b6af27`.
The recovery checkpoint refers to **HEAD after commit**; its resolved hash and actual
publication result must be reported after Git operations, never invented here.
Local recovery checkpoint: HEAD after commit. Push is withheld because the full current-session
suite did not pass under workspace-only storage. origin/main and remote main remain at
the verified V1 baseline; local HEAD will be ahead by one. No remote equality claim is made.

## Operations and integrity

V1 live reads consumed historically: **1**. V2 live reads consumed total: **0**.
Do not redo V1 discovery, repeat live experiments, scrape `/status`, or launch AI tasks
for quota testing. No capacity threshold was observed; preservation is scope-driven.

HHS and all other repositories were neither inspected nor modified in this session.
The newer workspace-only instruction takes precedence over mission item 69's external
read-only check. HHS integrity is therefore **NOT independently reverified**, not claimed
clean or restored. No credentials, authentication files or unrelated home directories
were inspected. V3 remains NOT_STARTED; future mission name only:
CGC V3 — CODEX PRESERVATION INTEGRATION, after completed V2 and separate authorization.

Checkpoint creation initially failed because this environment had no Git author identity.
Resolved using the existing V1 commit's public author name and GitHub noreply address
as per-command Git options; no global or persistent identity configuration changed.
