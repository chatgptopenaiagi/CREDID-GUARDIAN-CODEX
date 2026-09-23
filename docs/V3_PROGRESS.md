# CREDID GUARDIAN CODEX — CGC V3 progress

## OVERALL STATUS

**PARTIAL.** Explicit local-bare publication and independent remote verification are
**COMPLETE / VERIFIED OFFLINE within the restricted primitive contract**. General Git-push/
network transport, complete preservation/resume and automation remain unimplemented.
Attempt, inspection, durable handoff and deliberate local checkpoint foundations remain
accepted. [Complete V3 mission](V3_MISSION.md), including all 100 architectural keypoints,
and current user instructions remain authoritative. V1/V2 are unchanged and accepted.

THE GUARDIAN OBSERVES. CODEX PRESERVES. PRESERVE BEFORE EXPANDING.

## CURRENT SESSION BLOCK / RECOVERY

2026-09-23: preservation-only recovery after the preceding session hit its usage limit
before committing. Present inspection found main, origin/main and live remote main equal
to `509544147571dd57bf0ef3ed98be9ab4208c59a4`, with 12 modified documentation files and
untracked `src/cgc/publication.py` / `tests/test_publication.py`. All 14 files belong to the
existing coherent publication block; no unintended files found. Reviewed the full diff,
new source/tests, mission, contract and acceptance boundaries. No runtime or test edits,
redesign, new development, fresh-process resume work, automation or Fabric implementation.

The earlier test result had no retained file fingerprint proving equality to today's bytes,
so current focused and full tests were rerun. This recovery updates only continuity evidence
before normal CGC commit/push and independent remote verification, then stops.

## INTERRUPTED SESSION / HISTORICAL CAPACITY

2026-09-22, explicit publication continuation, exactly one coherent block. Verified clean
main and actual local HEAD = origin/main = live refs/heads/main =
`509544147571dd57bf0ef3ed98be9ab4208c59a4`. Recent commits, current source, tests and durable
progress agree with the historical handoff. No newer uncommitted work existed. Read current
mission/progress/acceptance and reconciled required records against their already-read content
and the preceding checkpoint diff; inspected checkpoint/handoff/inspection implementation and
checkpoint tests. No accepted V1/V2 experiment or earlier V3 block was repeated.

The user reports historical less-than-50% of the 5h window. No callable /status interface or
reliable live percentage is available to this process. No live value/threshold crossing is
invented, and no quota read substitutes for /status. Kept work to the local-bare primitive,
then stopped development for validation/documentation/publication reserve. No following phase.

## COMPLETE

- New `cgc.publication.publish`: explicit current publication and full-history review
  attestations, source/bare identities, expected checkpoint/remote tips, approved name/path/ref.
  A handoff, inspection, origin or authenticated tooling never grants publication authority.
- Clean-source, existing-branch/tracking-ref, ancestry, ownership, path, config, protocol,
  hook and layout prechecks. Local file transport only; unsupported network URLs refused.
- Approved object transfer without ref mappings, followed by forward-only expected-tip
  compare-and-swap of the existing bare ref. No force option, branch creation, rollback,
  history rewrite or automatic repair. Concurrent tip movement/deletion refuses atomically.
- Independent fetch without ref mappings, live ls-remote, direct bare-ref read, forward
  tracking-ref compare-and-swap/readback, final live/source/identity checks. VERIFIED requires
  observed expected local HEAD = tracking = live remote = direct bare ref.
- Already-equal remotes verified without publication; stale tracking may advance safely.
- Existing project writer lock and unchanged HandoffStore reused. PUBLISHING intent retains
  local receipt/context; failure records retain both pending and prior good continuity.
  Success stores equal-ref receipts, curated test failures and NEXT_EXACT_ACTION.
- Twenty-five tests, including checkpoint integration, fresh-process handoff readback,
  refusal/failure/race semantics, shared exclusion and three synchronized SIGKILL boundaries.

## PARTIAL

The coherent local-bare primitive is complete; broader V3 publication/preservation is PARTIAL.
This implementation transfers objects and updates refs using Git primitives, not git push.
General Git-push/network publication remains NOT_STARTED and is not claimed by local evidence.
Full project tests and history/secret review remain current caller responsibilities; recorded
tests are curated. Verified publication does not establish safe resume. Final attempt remains
PARTIAL and outer SAFE_TO_RESUME UNKNOWN. See [contract](V3_CONTRACT.md#explicit-local-bare-publication-and-independent-verification)
and [acceptance](V3_ACCEPTANCE.md).

## NOT_STARTED

General target Git-push/HTTPS/SSH transport; valuable real target publication; preserve CLI;
project test runner; full fresh-process Git/test reconciliation; Guardian autonomous authority;
automatic/background publication; resume generator; Agent Fabric/Gateway/Control/Data Plane/
Router/Event Bus runtime; networking/tunnels/shells; CWM/HHS/ARX integration; local/cloud AI
orchestration; GUI/mobile/V4. Dedicated active-command crash/signal hardening remains pending.

## TESTS PASSED

Initial focused publication: 15 tests in 3.444s, then 23 in 5.544s and 24 in 5.822s, all passed.
Initial integration: 47 in 8.690s; V3: 116 in 14.092s; preliminary full regression: 269 in
27.407s, all passed. Final review then tightened publication from ordinary push to atomic
expected-tip ref publication to avoid branch recreation after concurrent deletion.
No deterministic assertion failed; this was a safety-review finding and scope refinement.

Final focused primitive: **25 passed in 5.914s**. Added fresh source/bare checks between
object transfer and ref update, then validated the final implementation in this order:

```text
TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_checkpoint test_publication -q
Ran 48 tests in 9.425s — OK

TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_preservation test_inspection test_handoff test_checkpoint test_publication -q
Ran 117 tests in 14.401s — OK

TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -q
Ran 270 tests in 29.067s — OK
```

**Final full regression: 270 passed, zero failures, errors or skips.** All 245 inherited tests
and runtime modules unchanged. Linux-native /tmp fixtures only, no live quota source.
Recovery verification on 2026-09-23, against the recovered unchanged runtime/tests:

```text
TMPDIR=/tmp PYTHONPATH=src:tests python3 -B -m unittest test_checkpoint test_publication -q
Ran 48 tests in 9.554s — OK

TMPDIR=/tmp PYTHONPATH=src python3 -B -m unittest discover -s tests -q
Ran 270 tests in 28.800s — OK
```

Both runs: zero failures, errors or skips. Static checks passed: 28 Python ASTs, three JSON
files, 145 local Markdown file/anchor links, all 100 mission keypoints and six CLI help
commands without sensor access. All 52 tracked/new files screened; only two previously
reviewed synthetic credential-URL fixtures in test_handoff.py and test_inspection.py matched.
No real credential finding; pattern screening cannot prove universal absence. Inherited
runtime/tests and V2/V3 mission records are byte-identical to entry HEAD. Fetch/push destination
matches the expected CGC GitHub repository. Whitespace checks passed. Documentation-only
recovery/evidence updates do not require another runtime regression.

## TESTS REMAINING

In-command Git object-transfer/ref-update interruption, SIGINT/SIGTERM cleanup, overlapping
writers at active publication stages and durable recovery of uncertain attempts. Existing
before/after SIGKILL cases are accepted and need not be duplicated. Full future acceptance
also needs real project test receipts, fresh-process reconciliation and canonical Guardian
integration. General target Git-push/network transport needs a separately reviewed contract.
No live quota read is needed to continue.

## KNOWN FAILURES / LIMITATIONS

No unresolved observed deterministic failures. Only explicit existing local bare branches,
clean ordinary POSIX source repositories, bounded simple names and restricted configuration
are supported. No hooks are silently bypassed: executable hooks on either side are refused.
Current caller attestation is not a cryptographic capability, and no complete history content
or secret audit is performed by this adapter. Publication approval must cover the whole history.

Owner-controlled quiescent paths/configuration required. Expected-tip CAS protects ref movement
and deletion, not arbitrary hostile same-user filesystem/config races or bind-mount aliases.
No hard aggregate wall-time/RSS/decompression bound, universal power-loss guarantee or child
cleanup after SIGKILL during a running Git process. Interrupted operations may leave Git locks
or unreferenced objects; neither is automatically deleted. Windows-mounted modes are not weakened.

LOCAL_CHECKPOINT_ONLY means local evidence survives while remote preservation is unverified,
not proof that no remote update occurred. Accepted-but-interrupted operations remain uncertain;
no automatic retry/rollback. Durable pending intent can outlive acceptance without a verified
receipt. Generic latest failure is VERIFICATION_FAILED; detailed stage/error remains in the
returned result. Failed storage cannot guarantee failure persistence. If verification succeeds
but final handoff fails, return VERIFIED plus PARTIAL/handoff_saved=false; reconcile durable Git.

## IMPORTANT DISCOVERIES / ARCHITECTURE

An ordinary push may recreate a branch deleted between precheck and dispatch. Instead of
introducing any force-with-lease option, this first local-bare primitive transfers objects
without refs and then uses an exact nonzero expected-old-tip ref transaction. An ancestry
check plus compare-and-swap prevents a rewind and refuses disappearance/movement. The deletion
race is explicitly tested. This deliberately narrows transport support while satisfying the
current non-destructive boundary.

Fetch also does not map refs implicitly. After independent remote observations, only the
approved tracking ref advances by expected-old-tip comparison. A stale tracking ref is usable
if it is an ancestor; unexpected divergence is refused, never repaired. Source tests/index/
working files remain unchanged by publication.

No handoff/schema redesign or new capability framework. Existing attempt evidence allows
VERIFIED equal refs without claiming git push occurred; push_attempted stays false. Publication
method and approved identity/ref context are saved as bounded inert JSON in notes.decisions.
Information remains separate from authority; Fabric transport/events/control stay architecture
only. No local/cloud model or credential integration.

## FILES CREATED / MODIFIED

Created: `src/cgc/publication.py`, `tests/test_publication.py`.
Modified: `README.md`, `AGENTS.md`, `docs/ARCHITECTURE.md`, `docs/DATA_MODEL.md`,
`docs/PRESERVATION_POLICY.md`, `docs/SECURITY_MODEL.md`, `docs/ROADMAP.md`,
`docs/DECISIONS.md`, `docs/V3_CONTRACT.md`, `docs/V3_ACCEPTANCE.md`,
`docs/V3_PROGRESS.md`, `tests/README.md`.
All existing runtime modules, prior tests, V3 mission and V2 records unchanged.

## DO_NOT_REPEAT

No repeated quota reads, V1/V2 discovery, prior accepted blocks, blind staging, force options,
branch creation, automatic rollback/retry, credential access, unrelated mutation or Fabric/V4.
Do not infer current publication permission from saved records, configuration or tooling.
Do not treat object transfer/ref-update exit as VERIFIED, VERIFIED as SAFE_TO_RESUME, or a
pending PUBLISHING record as proof of whether the remote changed. Do not generalize local-bare
acceptance to general network Git push or valuable real project publication.

## NEXT_EXACT_ACTION

This recovery ends after verified publication; STOP and await the next scoped session.
At that session, reconcile actual Git/source/tests/mission/progress and publication.
Next coherent V3 block: **mutation/publication crash and concurrency hardening**, focused on
active Git object-transfer/ref-update interruption, SIGINT/SIGTERM cleanup, shared-writer
exclusion and truthful durable uncertainty/recovery. Audit the existing before/after SIGKILL
proof before adding missing cases. Preserve local checkpoints and previous good handoffs; no
blind retries, destructive cleanup or safe-resume claim. Do not incidentally add network push,
full resume engine, Guardian automation, Fabric or V4. STOP this session after publication.

## LAST SAFE CHECKPOINT

Entry published checkpoint: `509544147571dd57bf0ef3ed98be9ab4208c59a4`.
Recovered implementation checkpoint: `0e1d62a9741b616f0e0a8e9a39b399eb48c885f7`.
Final publication-evidence checkpoint: **HEAD after normal commit/publication**; its resolved
SHA belongs in the final report. Do not invent a self-containing commit hash.

## PUBLICATION STATE

Recovered implementation **REMOTE_VERIFIED** on 2026-09-23. Normal forward push to
chatgptopenaiagi/CREDID-GUARDIAN-CODEX main succeeded. A separate live remote query confirmed
local HEAD = origin/main = live refs/heads/main =
`0e1d62a9741b616f0e0a8e9a39b399eb48c885f7`; working tree clean.

This small documentation follow-up records the observed result in progress and acceptance
row 41. Its own HEAD is verified after normal commit/push and reported with the resolved SHA.
If that publication fails, retain the local evidence commit and report LOCAL_CHECKPOINT_ONLY.
Runtime/tests are unchanged from the 270-test recovery verification; no redundant regression.
Final changed-document link and staged whitespace checks pass before publication.

## OPERATIONS / INTEGRITY

Session live quota reads **0**; V3 **0**; V2 **0**; historical V1 **1**. No live /status value.
Target network operations **0**. Runtime source/remote mutations exercised only in disposable
Linux fixtures: object transfer, approved existing bare/tracking refs, project lock and external
handoff. Fixture setup deliberately seeds/moves/deletes synthetic refs for failure testing;
production primitive never deletes refs. No valuable external target publication.

CGC-only network operations: live remote-ref checks and authorized normal forward publication.
No installs, persistent environment/system/security changes, services, default cache creation,
authentication access or background monitoring. /tmp fixtures/processes cleaned by tests.
Historical preceding-session HHS check reported clean main at
`280b7090edf51aadf694db04d6d5f6bceff289a2`; not repeated or asserted current during recovery.
No unrelated repository inspected or modified during this recovery.
