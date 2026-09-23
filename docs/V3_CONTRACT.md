# CREDID GUARDIAN CODEX — initial V3 attempt contract

Status: IMPLEMENTED and VERIFIED with synthetic values, not a preservation executor.
Schema: `cgc-preservation-v3.0-provisional`.
Implementation: [preservation.py](../src/cgc/preservation.py).
Tests: [test_preservation.py](../tests/test_preservation.py).

This domain is separate from the accepted V2 Guardian cache. No V2 field/schema changes,
quota reader, filesystem operation, subprocess, CLI preserve command or project mutation
are introduced. Public Python functions are new_attempt, advance, validate_record,
render_json and render_human. Schema changes are provisional and must be deliberate.

## Lifecycle and conclusions

INSPECTING may advance to STABILIZING, TESTING or DOCUMENTING. STABILIZING may advance
to TESTING or DOCUMENTING; TESTING to DOCUMENTING. DOCUMENTING advances to CHECKPOINTING
or VERIFYING; CHECKPOINTING to PUBLISHING or VERIFYING; PUBLISHING to VERIFYING. VERIFYING
finishes PRESERVED or PARTIAL. Every active phase may terminate BLOCKED, FAILED or
CANCELLED. Terminal records cannot reenter the lifecycle. Each new attempt is separate.
Event timestamps must be canonical UTC, nondecreasing and consistent with the phase.

Configured levels: HANDOFF_ONLY, LOCAL_CHECKPOINT, REMOTE_VERIFIED. Actual outcomes are
IN_PROGRESS, HANDOFF_ONLY, LOCAL_CHECKPOINT, REMOTE_VERIFIED, REMOTE_PUSH_ATTEMPTED,
BLOCKED_UNSAFE, PARTIAL_PRESERVATION, FAILED or CANCELLED. More specific creation/no-op
outcomes require future action evidence; an observed commit ID alone cannot prove a
new commit was created. A push attempt cannot prove remote publication.

| Dimension | Rule |
|---|---|
| PROJECT_TEST_STATUS | UNKNOWN/PASSED/FAILED/SKIPPED. Passed/failed require command/result notes; failure requires known failures; skipped requires limitations |
| PRESERVATION_STATUS | Current lifecycle phase; only VERIFYING can finish PRESERVED |
| PUBLICATION_STATUS | NOT_REQUESTED, NOT_ATTEMPTED, PUSH_ATTEMPTED, FAILED, LOCAL_CHECKPOINT_ONLY or VERIFIED; derived independently |
| SAFE_TO_RESUME | YES only at PRESERVED with configured-level receipts; NO for unsafe/failed-without-surviving-evidence; PARTIAL for surviving evidence at incomplete terminal state; otherwise UNKNOWN |

YES means the configured continuity level has its required receipts, not that project
tests passed. A known failing test can be preserved accurately for repair. Requested
REMOTE_VERIFIED with failed publication stays requested REMOTE_VERIFIED and actual
LOCAL_CHECKPOINT_ONLY when a local receipt survives. No silent downgrade.

## Evidence boundary

`project_request` and curated notes are operator input, not observed filesystem facts.
Requested path is absolute/bounded and rejects parent traversal/control characters; this
is lexical validation only. The attempt model alone does not verify root identity, symlinks, permissions or Git
state. The separate explicit inspection collector below supplies bounded local evidence.

Evidence fields are exact and optional until supplied:

- inspection_digest, handoff_digest, resume_digest: lowercase SHA256 receipt references;
- local_commit, tracking_commit, remote_commit: full lowercase SHA1/SHA256 Git object IDs;
- unsafe_target and push_attempted: exact booleans;
- publication_error: null or a fixed safe error class.

A receipt is immutable within an attempt once supplied. Inspection is required before
handoff/local receipts; handoff before resume receipt. Remote receipts require a local
commit. Differing refs require explicit VERIFICATION_MISMATCH and cannot authorize
PRESERVED at REMOTE_VERIFIED level. Equal local/tracking/remote refs establish the model's
remote verification condition without implying a push was necessary or performed.

HANDOFF_ONLY success requires inspection, handoff and fresh-resume verification receipts.
LOCAL_CHECKPOINT additionally requires local commit receipt; REMOTE_VERIFIED additionally
requires matching remote/tracking receipts. The future verifier must establish receipt
truth and relevance to this exact project/attempt before constructing them. Phase A only
checks structural consistency: hashes are not signatures, an integrity proof or trusted
external observations by themselves. Test receipts are SYNTHETIC. Manual adapter receipts
are labeled ADAPTER_REPORTED, not independently verified by this pure module.

MANUAL does not depend on quota. SYNTHETIC is visibly distinct. Other triggers are refused
in this phase, and automatic_mutation_authorized is always false. This fixed denial is
not a completed Guardian integration. Actual Guardian gating is a later block and must
consume canonical V2 state; no UNKNOWN/stale/retained/synthetic state may authorize mutation.

## Continuity data and bounds

Notes contain mission, exact next action, COMPLETE/PARTIAL/NOT_STARTED items, changed-file
notes, tests run/results, known failures, important discoveries, decisions, do-not-repeat
items and limitations. They are curated operational records, never hidden chain-of-thought.
Commands and paths stored in notes are inert text. No command execution is implemented.

Exact key allowlists reject extra fields, including arbitrary credential keys. Strings are
1–2048 code points without control characters; lists at most 64 strings; events at most
64; total serialized record at most 256 KiB. Full object IDs are required. JSON/human output
validate the same record and recompute conclusions. Human data is quoted to avoid imitating
report headings. Validation errors are fixed and do not echo rejected data.

These bounds and allowlists do not prove arbitrary caller-supplied text is secret-free.
Future capture/staging adapters must minimize and screen content; no raw Git output,
remote URL or project file is accepted automatically here. Dangerous/unrepresentable
paths can be refused until the inspection model supplies safe structured/escaped handling.

`advance` validates/copies its input and never mutates it. A rejected update leaves the
previous in-memory record usable. The separate handoff store below now supplies atomic continuity publication, retained
known-good state, writer exclusion and fresh-process readback. It does not verify project
preservation or authorize resume.


## Bounded project inspection

IMPLEMENTED and VERIFIED OFFLINE on Linux with Git 2.55.0. Module
[inspection.py](../src/cgc/inspection.py), tests
[test_inspection.py](../tests/test_inspection.py). Snapshot envelope is separately
versioned `cgc-inspection-v3.0-provisional`; the attempt and V2 schemas are unchanged.
Public functions: inspect_project(project, now=...), validate_inspection, render_json,
render_human. CLI: `python -m cgc inspect --project /absolute/root [--json]`.

Only an exact explicitly selected ordinary working-tree root is accepted. No ancestor
repository search, path normalization through `..`, implicit cwd selection or target
mutation. Relative paths, root `/`, redundant components, missing/non-Git/nested-directory
targets are refused. Ancestors are opened descriptor-relatively without following links;
root must be owned by the current UID and not group/world writable. Root-owned sticky
ancestors such as /tmp are allowed. Target entries must be same-device, owned, safe-mode
regular files/directories or worktree symlink leaves. Hardlinked files, special files,
metadata symlinks and known credential directories (.codex/.ssh/.aws/.azure/.gnupg) are
refused. Native Windows and mounts that do not enforce these modes are unsupported.

The collector performs a bounded metadata-only preflight of this root including ignored
entries; it never opens worktree file contents in Python. Git itself can hash tracked
files and read local ignore/attribute rules to determine status. No file contents,
patches, object bodies, config values, identities, URLs or raw diagnostics enter output.
Worktree symlink destinations are neither read nor emitted. Nested repositories are
reported as boundaries and not traversed. Main-repository linked-worktree presence is
reported without opening other worktrees. A `.git` file target is refused as
UNSUPPORTED_GITFILE without reading its destination (covers linked worktrees and external
Git dirs). Submodules are identified from index gitlinks; their worktrees are explicitly
NOT_INSPECTED and their status changes are suppressed, not claimed clean.

The root snapshot contains:

- requested and observed root, device/inode identities for root and Git directory;
- caller-provided UTC observation time (CLI captures invocation time), LOCAL_OBSERVATION;
- HEAD or null for unborn, branch or null for detached HEAD, local upstream and optional
  ahead/behind counts; these use local tracking refs, never a live remote;
- sorted staged/unstaged/untracked/deleted/renamed/conflicted paths; rename source paths;
- paths with assume-unchanged/skip-worktree flags, whose contents Git may hide;
- fixed merge/cherry-pick/revert/rebase/sequencer/bisect marker presence, not file contents;
- remote names only, remote_state=NOT_QUERIED; no publication destination is authorized;
- gitlink paths, nested-repository boundaries and linked-worktree presence;
- presence of a fixed small set of instruction/handoff document candidates; contents
  NOT_READ and test_command=UNKNOWN, not invented or executed.

Git runs without a shell through fixed /usr/bin/git with an allowlisted environment,
no inherited Git overrides/global/system configuration, no prompts/lazy fetch/replace
objects/system attributes, and optional locks disabled. Only config parsing, rev-parse,
ls-files and porcelain-v2 status are used. Repository config is first parsed explicitly
with --no-includes from a no-follow descriptor outside repository discovery. Only basic
core settings, SHA object format, user name/email, remote URL/fetch settings, branch
remote/merge and submodule URL/active settings are accepted; their values are not exported.
Every other key is refused, including includes, filters, fsmonitor, hooksPath, external
attribute/exclude files and worktree redirection. Config is never changed and no mutation
hook is bypassed. Alternates, grafts, promisor and shared-index layouts are refused.
Unsupported configuration is a deliberate initial compatibility boundary, not permission
to rewrite a target's settings. Git status preserves repository ignore rules; global
ignore rules are excluded to avoid unrelated file reads.

| Bound | Limit and failure behavior |
|---|---|
| Metadata walk | 10,000 entries, depth 32, relative paths at most 4,096 bytes |
| Files examined by stat | 16 MiB per regular file, 64 MiB aggregate (includes Git metadata/ignored files) |
| Repository config | 64 KiB input; includes never followed |
| Git subprocess | 5 seconds per command, 256 KiB combined stdout/stderr; kill group and reap on failure/interruption |
| Whole inspection | 20-second cooperative deadline across scans/commands; no retry |
| Snapshot | 256 KiB serialized JSON; exact field allowlists; bounded lists |

Bounds fail closed without a truncated snapshot. They limit work, not hard CPU/RSS or
realtime kernel behavior: blocked filesystem syscalls and process reaping can exceed wall
budgets. Compressed Git objects can expand internally; no memory sandbox is claimed.
POSIX read access can update atime; file bytes, index, refs, HEAD, config and working-tree
state are not intentionally changed. Non-mutation tests compare all fixture file bytes,
modes, sizes and mtimes, including Git internals, before/after success and selected failures.

Status/index observations and metadata fingerprints repeat before success. Detected
change produces TARGET_CHANGED with no receipt. This is explicitly
REPEATED_OBSERVATION_NOT_ATOMIC: no lock against other writers, no snapshot isolation,
no defense against a hostile concurrent same-UID actor replacing config/paths between
checks. Use owner-controlled quiescent targets; future mutation needs fresh prechecks
and writer exclusion. The fingerprint excludes atime. Inspection is not a content backup,
a complete security audit or a guarantee that a later mutation is safe.

Both renderers validate the same envelope. JSON uses sorted keys and escaped text;
human output is explicitly INSPECTION ONLY plus that JSON, so filenames cannot become
report headings. An OBSERVED envelope carries a SHA256 digest of canonical snapshot JSON,
compatible with the existing attempt's inspection_digest receipt. The digest proves
representation integrity only, not authenticity, project preservation or fresh-process
resume. REFUSED includes a fixed error_code, null snapshot and null receipt; includes
unsupported targets, operational failures and CANCELLED. No raw path or stderr is echoed
on failure. CLI SIGINT/SIGTERM during inspection yields cancellation and cleanup.
SAFE_TO_RESUME remains UNKNOWN and automatic_mutation_authorized remains false always.
A successful inspection alone never advances an attempt to PRESERVED.

Recognizable credential-like metadata is refused, but arbitrary filenames/branch names
can themselves contain private information. Do not automatically publish inspection
output. No universal secret-detection guarantee. Tests use synthetic secrets only.

Git protocol references: [porcelain status and optional-lock guidance](https://git-scm.com/docs/git-status),
[Git environment controls](https://git-scm.com/docs/git). Live quota discovery was not repeated.


## Durable handoff persistence

IMPLEMENTED and VERIFIED OFFLINE on Linux-native storage. Implementation:
[handoff.py](../src/cgc/handoff.py); evidence: [handoff tests](../tests/test_handoff.py).
Schema `cgc-handoff-v3.0-provisional` is separate from unchanged attempt, inspection and
V2 schemas. Public API: HandoffStore, validate_state, render_json, render_human.
No transport, agent identity protocol, project command runner or preservation executor.

One explicitly selected private external directory holds `handoff.json` and a persistent
`writer.lock` inode. The directory binds to one exact absolute requested project path.
Storage cannot be the project, its descendant or ancestor, or contain .git/.codex/.ssh/
.aws/.azure/.gnupg components. Project symlink components and storage symlink components
are refused before creation; missing project paths permit historical recovery. Project
checks open directory metadata only. No source content or credential store is collected.
This is a lexical identity plus no-follow path contract, not project identity attestation:
renames, bind-mount aliases and hostile same-user path replacement are not reconciled.
Use an owner-controlled dedicated external store and quiescent paths; mounts must not alias
storage into the project. Native Windows and filesystems without private POSIX modes are
unsupported. Parent directories must already exist; only the final store is created.

The validated canonical state includes:

- schema_version, CONTINUITY_ONLY scope, project_request and monotonic generation;
- latest_attempt: PUBLISHED/FAILED, caller-supplied canonical UTC time, fixed failure code,
  and successful slot digest or null;
- last_known_good and previous_known_good: at most two complete validated slots with
  generation, publication time, OPERATOR_CURATED basis, attempt record, optional bound
  inspection and SHA256 digest of canonical slot content;
- outer safe_to_resume=UNKNOWN and automatic_mutation_authorized=false, always.

Known-good means a valid saved continuity record, **not** a verified preserved project.
A stored attempt may accurately report failed tests, incomplete work or adapter-reported
receipts. Those claims remain historical/curated, never upgraded to independently verified
facts. Inspection must be OBSERVED, match the exact project and attempt inspection digest,
and not postdate publication. Missing inspection is explicit; an attempt that claims its
digest must include that inspection. Event/publication times and generations are validated.
Digests provide representation integrity, not authentication or external action proof.

Both representations derive from validate_state. Machine JSON uses sorted keys, ASCII
escaping, compact separators and one canonical disk newline. Human output includes schema,
quoted continuity fields (including COMPLETE/PARTIAL/NOT_STARTED/NEXT_EXACT_ACTION), the
reported attempt and inspection, with explicit outer UNKNOWN status. It is rendered on
read, not maintained as a second independent file that could disagree with machine state.
Equivalent mapping insertion orders produce identical human and machine output. Rendering
adds no timestamps/random IDs. Publication time and generation are intentionally state;
repeated publish calls create new generations rather than being idempotent.

Writes require the inherited nonblocking POSIX flock. Validate candidate, serialize,
write a private exclusive temporary sibling, flush/fsync file, atomic replace, fsync
store directory, then validate readback. Readers need no writer lock. Before replacement,
a failed write leaves canonical bytes untouched. After replacement, a reported failure is
HANDOFF_PUBLICATION_UNCERTAIN: the new complete state may be visible and contains the
previous known-good slot. Inspect durable state before deciding what to do next.

`record_failure(code, now=...)` explicitly publishes a bounded failed latest attempt while
retaining both good slots. Codes: INPUT_REJECTED, INSPECTION_FAILED, WRITE_FAILED,
VERIFICATION_FAILED, CANCELLED. It can also record failure with no prior good state.
Rejected candidates are not automatically persisted. If storage itself fails or the
process dies, latest_attempt may remain the prior durable attempt: no mechanism can promise
a durable failure receipt on failed storage. Corrupt or unsupported canonical state is
refused without overwrite/migration. Unsupported schema has a distinct fixed error code;
malformed state is CORRUPT_HANDOFF. Size and project mismatch also have distinct read errors.
The status CLI exposes safe codes; missing/unopenable storage is HANDOFF_UNAVAILABLE,
while lexical/project alias rejection is UNSAFE_HANDOFF_PATH.

Bounds: paths at most 2048 code points; inherited record strings at most 2048, note lists
and events at most 64, attempt and inspection at most 256 KiB each; two retained slots;
generation 1..2^53-1; canonical file/read/write and human output at most 2 MiB. Read uses
limit+1, strict duplicate-key decoding and canonical-byte comparison. Excess fails closed;
no truncation. No arbitrary nested payload is accepted. These are data bounds, not hard
CPU/RSS or filesystem syscall deadlines. Repeated process deaths can leave private temporary
siblings; they are ignored and never automatically deleted. Disk accumulation is not bounded
across arbitrary crashes. Ordinary completed/failed writes clean their temporary file.

Recognizable GitHub/OpenAI token forms, private-key headers and credential-bearing HTTP(S)
URLs are refused with fixed non-echoing errors. Exact field allowlists reject arbitrary
credential fields. Curated text can still contain unrecognized secrets: this is defense in
depth, not a universal detector or permission to export data to cloud consumers. No private
source content, credentials or hidden reasoning should be supplied as continuity notes.

Eighteen tests cover round-trip/modes; mapping-order determinism; explicit failure retention
and recovery; pre/post-replace injected failures; exclusion/release; unsafe paths/files;
malformed/duplicate/schema/size refusal; digest/project binding; recognizable secret refusal;
fresh-process human/JSON readback (including failed latest attempt); field/list/record/output
bounds; failed first attempt/time ordering; project alias refusal; bound inspection and full
fixture file-byte/mode/size/mtime non-mutation; and synchronized SIGKILL at before-write,
partial-write, before-replace and after-replace, each with/without existing state. Competing
process writers are refused and restart can acquire the lock after death. This proves tested
process-crash visibility, not universal power-loss durability, hostile tamper resistance or
end-to-end safe resume. SIGINT/SIGTERM handoff-write-specific adapters are not implemented.

Future consumers must reconcile current Git/test/mission reality before using historical
NEXT_EXACT_ACTION. Information does not grant capabilities. See
[Agent Fabric architecture relationship](ARCHITECTURE.md#agent-fabric-relationship).

## Deliberate manual local checkpoint

IMPLEMENTED / VERIFIED OFFLINE: [checkpoint.py](../src/cgc/checkpoint.py),
[test_checkpoint.py](../tests/test_checkpoint.py). Public Python `checkpoint` is a
bounded manual adapter, not an automatic Guardian action or a preserve CLI. It creates
normal local commits only. No target network operation or project test execution exists.

The current trusted caller must provide the exact project, expected existing HEAD and
branch, `policy_reviewed=True`, and a reviewed mapping of exact relative file paths to
SHA256 content digests (`None` means an approved deletion). This is a current caller
attestation of user/project-policy authority, not a cryptographically enforced capability
or a value to deserialize as authority from a handoff. A digest binds reviewed bytes; it
does not prove coherence, secrecy or test success. The caller must establish those facts
and supply an honest MANUAL, LOCAL_CHECKPOINT attempt at DOCUMENTING with no receipts.
The adapter supplies actual selected paths as files_changed, retains curated test status,
known failures and NEXT_EXACT_ACTION, and adds inspection/local-commit evidence itself.

Initial compatibility deliberately requires an ordinary existing branch with an existing
commit, the inspector's restricted configuration/layout, no operations/conflicts, hidden
index flags, nested repositories, submodules or linked worktrees. Any existing staging,
including intent-to-add, is refused without replacing the user's index. All local
.gitattributes and .git/info/attributes are refused to exclude content transformations.
Executable project hooks are refused for a separately reviewed policy; they are neither
run nor silently disabled. Hook sample files are inert. User identity comes from approved
repository-local config; global/system config is excluded, and no identity is invented.

Selection is literal (no wildcard/pathspec expansion), at most 64 paths of 2048 characters.
Only selected files are opened for content screening, descriptor-relatively without links.
They must be owned, safe-mode, singly linked regular UTF-8 text files, at most 1 MiB each
and 4 MiB total. Common credential paths/names, generated directories, model/archive/database
extensions, binary content, recognizable credentials and obvious credential assignments are
refused. No contents, patches or raw Git diagnostics are returned. Scanning cannot prove
universal secrecy, and existing history is not content-audited. Unselected and ignored work
is preserved in place; unselected dirty work is not claimed checkpointed. Global ignore
configuration remains excluded by the inspection contract; project .gitignore is honored.
Deletions and renames are explicit selected paths, not automatic discovery/staging decisions.

A persistent private `.git/cgc-checkpoint.lock` inode, never unlinked, holds nonblocking
flock throughout fresh inspection, handoff, staging, commit and receipt publication. Lock
creation is itself an authorized metadata write and may survive a later precheck refusal.
It coordinates CGC writers even when they choose different handoff stores. Kernel process
exit releases it. Git's own foreign lock files are refused, not removed. Noncooperating
Git/editor processes and hostile same-user races are not excluded; use quiescent targets.
The adapter rechecks root/Git identity, HEAD/branch, configuration, content and index at
meaningful boundaries but does not claim an atomic filesystem transaction.

Before staging, a validated CHECKPOINTING handoff is saved under the external store's lock.
The adapter then runs only explicit `git add -- <selected paths>`, `write-tree` and a normal
`commit` with a fixed message. It compares the entire staged index to the original index
plus exactly the approved blobs/modes, then verifies the new HEAD, exactly one expected
parent, branch, tree and index. No reset, clean, restore, stash, rebase, branch creation,
history rewrite, force push or rollback exists. Repeated requests with stale HEAD or no
selected changes refuse rather than manufacture empty commits.

The returned outcome is REFUSED, PARTIAL or LOCAL_CHECKPOINT, with fixed error_code,
head_before, tree, local_commit, staging_attempted, commit_attempted and handoff_saved.
`local_commit` is populated only after verification. `publication_status=NOT_REQUESTED`
and `safe_to_resume=UNKNOWN` always. Successful receipt storage ends the attempt PARTIAL:
local Git evidence exists, but full fresh-process reconciliation and safe resume do not.
`handoff_saved` indicates the most recent record publication attempted by this call succeeded;
a true value on failure can refer to the pre-staging CHECKPOINTING record, not a final receipt.
Read durable latest_attempt and good slots to distinguish them.

Any failed mutation leaves staged files, objects and commits intact. No automatic retry or
index rollback can discard user work. When possible, an explicit latest failure is recorded
without erasing prior good continuity. If a commit exits unsuccessfully/times out or the
process dies after updating HEAD, a commit may exist without a returned verified receipt:
commit_attempted plus missing local_commit requires fresh Git reconciliation, never a blind
retry. A verified local receipt survives in the return value if the final handoff write
fails; older durable handoffs remain. Crash-before-recording cannot record its own failure.

Uses existing bounded fixed-Git transport (5 seconds/256 KiB per command, isolated environment,
no shell) and inspection bounds. The mutation sequence has a 60-second cooperative deadline;
individual full inspections retain their own 20-second bound. These are not hard aggregate
wall-time, CPU/RSS, syscall or power-loss guarantees. SIGKILL of CGC during a running Git
child cannot guarantee descendant cleanup. Four synchronized SIGKILL boundaries before/after
staging and commit prove old/new HEAD, preserved work/index and restart lock release; they
do not prove interruption inside Git's ref transaction or every mutation syscall. The opt-in
signal scope below now covers graceful cancellation; broader active-command and abrupt-parent
death acceptance remains partial.

Test coverage also includes exact tree/parent and fresh-process handoff readback, failed
project test notes, subset/ignored preservation, literal names, additions/deletions/renames,
current authority/stale HEAD refusal, pre-staged and intent-to-add preservation, secret/binary/
size limits, hooks/config/attributes/operation refusal, path aliases/foreign locks, content
and index changes, real missing-identity Git failure, injected post-commit uncertainty,
post-commit handoff failure, corrupt-store refusal and cross-process exclusion.

## Explicit local bare publication and independent verification

IMPLEMENTED / VERIFIED OFFLINE: [publication.py](../src/cgc/publication.py),
[test_publication.py](../tests/test_publication.py). `publish` is a manual Python primitive
for an explicitly approved, existing local bare repository and existing branch. It is not
an HTTPS/SSH/Git-push adapter, publication CLI, autonomous consumer or full preservation
workflow. General remote transport remains NOT_STARTED.

The trusted current caller must supply exact source path and device/inode/Git-directory
identity; expected checkpoint commit; current branch; approved remote name; exact absolute
bare path and device/inode identity; expected existing remote commit; a fresh MANUAL /
REMOTE_VERIFIED / DOCUMENTING attempt with no receipts; explicit `publication_reviewed=True`
and `history_reviewed=True`. History approval covers all reachable content at expected_head
for this destination, not merely a checkpoint's selected files. Approval is an in-process
caller attestation, not a cryptographic grant or a field to load as authority from storage.
Neither origin, credentials, configuration, a saved record nor a local commit grants it.

The source must pass checkpoint inspection/policy, be clean (including staging/untracked work),
match the approved identity/HEAD/branch and have exactly one configured URL for the approved
remote, matching the approved path. A pushurl, if present, must match it too. Instructions,
project tests and history-secret review remain caller responsibilities. Source hooks requiring
execution, attributes, unsupported config/layouts, unsafe modes and operation/conflict states
are refused. The pre-existing checkpoint lock coordinates both adapters for the same project.
No authentication is used, protocols other than explicit local file access are disabled,
and arbitrary remote URL/config/diagnostic text is never emitted.

The bare target receives its own bounded no-follow metadata/config preflight. It must be owned,
non-writable by others, actually bare, non-overlapping with source/store, and have the approved
identity. Symlinks, hardlinks, alternate object stores, shallow/promisor/nested layouts, foreign
locks, executable hooks and all unreviewed config keys are refused. Only basic bare core/object
format config is accepted; includes are parsed without following them and rejected. Protected
credential directories are refused. No hook or security setting is bypassed/rewritten.

Only the same explicitly named source/remote branch is supported. The remote branch and the
approved `refs/remotes/<name>/<branch>` tracking ref must already exist and be direct commit
refs. Missing refs are not created. Branch spelling is deliberately restricted to bounded
ASCII letters/digits/underscore/hyphen/slash. The exact remote tip must match expected_remote;
the tracking tip must be an ancestor of that tip, which must be an ancestor of expected_head.
Unknown/divergent/ahead relationships refuse rather than fetching to guess or repairing them.

Publication method is **LOCAL_BARE_OBJECT_TRANSFER_REF_CAS**:

1. Save a PUBLISHING intent with observed local commit, inspection, approved identities,
   expected tips and exact destination/tracking refs in the external HandoffStore.
2. Recheck source/remote configuration, identities and tips under the source writer lock.
3. If remote already equals expected_head, skip publication and still verify independently.
4. Otherwise fetch the approved history into the bare object store with no ref mapping,
   tags, FETCH_HEAD write, recursion or automatic maintenance. No branch changes yet.
5. Recheck safety, then update exactly the approved remote ref with `git update-ref --no-deref`
   and the explicit nonzero expected old tip. The earlier ancestry check proves forward intent;
   the atomic expected-tip comparison refuses a concurrent move or deletion. This cannot
   silently recreate a deleted branch. No force option or history rewrite is used.
6. In separate bounded Git processes, fetch without ref mapping into the source, read the
   live remote with ls-remote and read the bare ref directly. Require the approved HEAD.
7. Advance only the approved existing tracking ref by expected-old-tip comparison; read it
   back, query the live remote again, and recheck source/remote identity/state. Require
   local HEAD = tracking = live remote = directly observed bare ref = expected_head.
8. Persist the actual equal-ref receipts, retaining curated tests/known failures/next action.
   The attempt ends PARTIAL, with publication VERIFIED but SAFE_TO_RESUME never YES.

Ordinary Git push was excluded from this first primitive after review identified that a
branch deleted between precheck and push can be recreated. Atomic expected-tip publication
avoids that gap without introducing a force-with-lease option. A general push adapter needs
its own separately scoped safety contract. `push_attempted` in the existing attempt schema
remains false because this primitive does not execute git push; equal observed receipts
can still establish the existing model's VERIFIED publication state. No schema changes.

Returned publication_status is NOT_ATTEMPTED initially, REFUSED on pre-dispatch error,
ATTEMPTED while transferring/updating, PUBLICATION_UNCERTAIN on an incomplete attempted
operation, PUBLISHED_UNVERIFIED after successful ref-update exit but before verification,
or VERIFIED only after independent equality checks. Already-equal verification needs no
publication attempt. Fixed fields also include publication_method, local_commit, remote_before,
remote_commit, tracking_commit, publication_attempted, ref_update_succeeded, verification_method,
error_code, preservation_outcome, handoff_saved and safe_to_resume=UNKNOWN.

LOCAL_CHECKPOINT_ONLY means local evidence survives while remote preservation is unverified;
it does not assert the remote was untouched. Transfer failure can leave harmless unreferenced
objects; failed/accepted-but-interrupted ref updates can leave the old or new tip. Nothing is
rolled back, deleted or retried. A ref-update process exit is never proof of remote equality.
If remote verification succeeds but the final handoff write fails, returned publication remains
VERIFIED with preservation_outcome PARTIAL and handoff_saved=false; retain and reconcile Git.

Failure calls record_failure rather than publishing another good slot: the pending local
receipt and prior good continuity both survive. Durable latest failure uses CANCELLED for caught
KeyboardInterrupt, otherwise the existing generic VERIFICATION_FAILED code; detailed stage/error
remains in the return value. After process death,
the durable PUBLISHING record is intent, not proof that transfer/ref update occurred. Its
push_attempted=false is literal (no git push), not proof no publication occurred. Fresh Git
reconciliation is required. No successful remote receipt is fabricated from that pending state.

Bounds reuse 10,000 entries/depth 32/16 MiB file/64 MiB metadata-scan size limits, 64 KiB config,
5-second/256 KiB Git commands and a 60-second cooperative operation budget; full inspections
retain their own bounds. Remote path is at most 512 characters, remote name 64 and branch 128.
No hard aggregate wall-time, decompressed-object memory, power-loss, malicious same-user or
filesystem-alias guarantee. Paths/configuration must remain owner-controlled and quiescent.
Expected-tip CAS protects ref movement/deletion; it is not a filesystem snapshot or distributed
transaction. Git may leave locks/objects after abrupt death; never automatically remove them.
SIGKILL during an active child cannot guarantee descendant cleanup.

Twenty-five tests cover checkpoint integration, fresh-process continuity, all equal refs,
already-equal/stale-tracking reconciliation, missing approval/history review, wrong source/tip/
branch/remote, dirty/staged/detached/operation states, aliases/protocols/modes/hooks/config,
ahead/diverged/moved/deleted remote, real expected-tip rejection, ref-update/verification
failures, after-accept uncertainty, failed final handoff, corruption, overlap, shared writer
exclusion and three synchronized SIGKILL boundaries before ref update, after acceptance and
before verification. No valuable repository or target network is used. In-command crash,
object-transfer interruption and broader concurrency hardening remain pending; the following
section records the accepted active-ref transaction subset.


## Manual mutation cancellation and active ref transactions

IMPLEMENTED / VERIFIED OFFLINE within this scope: [signals.py](../src/cgc/signals.py),
[interruption tests](../tests/test_mutation_interruption.py) and their
[test-only Git transaction peer](../tests/helpers/mutation_peer.py).
The current caller may opt into process signal ownership for one synchronous adapter call:

```python
from cgc.signals import mutation_signals

with mutation_signals():
    result = publish(**currently_approved_arguments)
```

The same scope supports `checkpoint`. All existing current-approval, selection, history,
identity and destination requirements still apply. This example supplies no authority.
No CLI or automatic invocation was introduced. The main thread is required; worker-thread
entry raises SIGNAL_SCOPE_REQUIRES_MAIN_THREAD before changing handlers. Previously installed
SIGINT/SIGTERM handlers are restored on normal and exceptional exit. Handlers are installed
only inside this explicit scope, never on import or silently by a library adapter.

The first SIGINT/SIGTERM raises KeyboardInterrupt. The existing Git runner kills its command
process group and reaps the direct child before adapter locks unwind. Subsequent SIGINT/SIGTERM
in the same scope are ignored to let cleanup and best-effort failure persistence finish.
Use the scope around one call and exit promptly; it is not a reusable cancellation loop.
Interrupted inspection remains CANCELLED rather than being relabeled INSPECTION_REFUSED.
Caught cancellation after pending intent records latest_attempt.error_code=CANCELLED when
storage permits, retaining both good slots. Other operational failures remain VERIFICATION_FAILED.
An interruption before intent exists cannot promise a new durable failure receipt.

The synchronized publication tests replace only one fixture update-ref invocation with a
real `git update-ref --stdin` transaction. They wait for Git's `prepare: ok` or `commit: ok`
acknowledgement, with Git still alive waiting on stdin. The production runner supplies the
actual timeout, signal cleanup and process reaping. This is a controlled real Git transaction
fixture, not proof of interrupting every syscall in the ordinary one-shot update-ref command.

| Observed interruption | Surviving Git evidence | Returned / durable conclusion |
|---|---|---|
| SIGINT/SIGTERM after prepare | Old bare tip, prepared Git lock retained; source HEAD/index/work unchanged | PUBLICATION_UNCERTAIN, LOCAL_CHECKPOINT_ONLY; CANCELLED latest attempt; pending PUBLISHING intent and prior continuity retained |
| SIGINT/SIGTERM after commit acknowledgement but before exit | New bare tip, old tracking tip, unchanged source checkpoint | Same uncertainty; no fabricated remote receipt or safe-resume claim |
| Active prepared Git child SIGKILL or command timeout | Old tip and Git lock retained | GIT_FAILED or TIMEOUT return; generic failed latest attempt; prior continuity retained |
| Competing checkpoint/publication at either active stage | No contender staging, ref update, store creation or handoff replacement | WRITER_BUSY, even with a different handoff store |

Fresh-process handoff-status JSON exactly matches durable state after these failures.
Both CGC locks can be reacquired after command cleanup. Git's retained prepared lock is
not a stale CGC lock: a subsequent explicit publication refuses UNSAFE_REMOTE_LAYOUT and
leaves it untouched. Human Git reconciliation is required; no automatic unlink, retry or
rollback. After accepted-but-unverified publication without a retained Git lock, a separately
approved call using the independently observed current tip verifies equality without
republishing. That is the existing manual path, not a resume engine or restored authority.

Checkpoint tests also deliver real SIGINT/SIGTERM at commit dispatch and immediately after
real commit acceptance. Staged bytes or the accepted single-parent commit survive; no unverified
local receipt is manufactured. These are boundary tests, not in-command commit crash proof.

LIMITATIONS / PARTIAL: active object-transfer interruption; in-command add/commit interruption;
SIGKILL of the CGC parent while descendants run; different-source writers sharing a remote;
full fresh-process Git/test reconciliation and power-loss durability remain outside this
accepted subset. SIGKILL cannot run the cancellation scope or guarantee descendant cleanup.
A repeated signal cannot impose a hard bound on blocked filesystem/reaping syscalls. Paths
and config must remain owner-controlled and quiescent; existing same-user race limits apply.
No schema, V1/V2 runtime, test command runner, telemetry or Fabric component was added.
