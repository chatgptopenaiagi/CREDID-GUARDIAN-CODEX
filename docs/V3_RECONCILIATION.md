# CGC V3 — evidence-based fresh-process reconciliation contract

Status: **First read-only engine IMPLEMENTED; scoped acceptance and limits are recorded below and in V3_PROGRESS.**
This is the authoritative V3 reconciliation design, subordinate to the complete
[V3 mission](V3_MISSION.md) and compatible with the implemented [V3 contract](V3_CONTRACT.md).
It separates knowledge reconstruction from recovery execution. It does not change any existing
schema, receipt, adapter or CLI. V4 remains architecture only and may later expose these meanings.

## 1. Scope and implementation gate

A new process observes, compares, classifies and explains one explicitly selected project and
one explicitly selected external handoff. It does not inherit conversational knowledge or
historical authority. Its first implementation MUST be read-only, with SAFE_TO_RESUME=UNKNOWN,
mutation_allowed=false and automatic_mutation_authorized=false for every result, including a
fully explained project. These are capability boundaries, not assertions that every project is
unsafe. The original specification did not implement an API; section 14 records the separately authorized implementation. No reconcile CLI exists.

The contract is ready for a minimal engine implementing the pipeline and acceptance cases below.
A later verifier may address the YES proof obligations in section 9 under separate authorization;
the first engine must not silently become that verifier. No recovery, preservation orchestration,
automatic tests, fresh authority service, full resume engine or V4 component is in the first slice.

## 2. Audit of available evidence

| Domain | Existing evidence and source | What it can establish; what it cannot |
|---|---|---|
| Durable handoff | HandoffStore, latest_attempt, last_known_good, previous_known_good, validated attempt and optional inspection | Bytes/generation/digest are structurally consistent with an explicitly bound project. Slots contain OPERATOR_CURATED / ADAPTER_REPORTED or SYNTHETIC evidence, not authenticated history. Last-known-good means successfully saved continuity, not necessarily completed preservation. |
| Local Git | inspect_project: root/Git device+inode, HEAD/branch/upstream, change categories, unsupported states, repeated observations | Bounded present metadata facts. No atomic snapshot, complete worktree content identity, live remote query, test command or authority. The inspection digest includes observed_at; it is not a reusable source-tree hash. |
| Remote Git | Publication context in notes.decisions, runtime receipt, local tracking ref | Historical destination/expected-tip claims and observed receipts where actually saved. Tracking is local state, never a fresh remote read. Remote identity requires new explicit observation scope. |
| Checkpoint | local_commit receipt; current-call expected HEAD, selected SHA256 map, in-memory intended index/tree | Receipt is historical claim until re-observed. The full selected digest map, intended index/tree and dispatch flags are NOT durably structured in pending checkpoint intent. Parent/tree matching alone cannot authenticate who created a commit. |
| Publication | Saved PUBLISHING includes local_commit and JSON context in a decisions string; completed record can include matching local/tracking/remote IDs | Does not persist every result field: publication_attempted/ref_update_succeeded/verification_method are runtime result facts, not guaranteed saved flags. Do not derive them from phase or objects. |
| Tests | project_test_status and notes.tests_run/test_results/known_failures/limitations | Curated reports, not structured command/environment/state-bound execution receipts. PASSED proves neither present applicability nor that a command actually ran. |
| Review | notes.files_changed; selected mapping supplied to checkpoint by current caller | Paths identify candidates; they do not identify reviewed bytes. An externally supplied digest remains an attributed claim until compared, and still grants no authority. |
| Authority | Explicit invocation under project policy; policy_reviewed or publication_reviewed/history_reviewed on existing adapters | Current scoped caller attestation, not a persisted cryptographic grant. Neither handoff, config, quota, PID, hash nor a plugin can renew it. |

Audited implementation: [handoff](../src/cgc/handoff.py), [inspection](../src/cgc/inspection.py),
[checkpoint](../src/cgc/checkpoint.py), [publication](../src/cgc/publication.py),
[signals](../src/cgc/signals.py), [pure attempt](../src/cgc/preservation.py),
[observational CLIs](../src/cgc/__main__.py).

Critical distinctions:

- Handoff latest_attempt=PUBLISHED means a continuity document was saved. Its embedded phase
  can still be CHECKPOINTING/PUBLISHING. It is not a Git success receipt.
- An embedded pure attempt can derive safe_to_resume=YES from structurally supplied receipts.
  The handoff/inspection envelopes and real adapters still report UNKNOWN. The new reconciler
  must never copy that inner YES into externally verified safety.
- Existing publish() verification fetches objects and updates tracking with compare-and-swap.
  Calling it, even when the remote is already equal, is NOT read-only reconciliation.
- Saved publication context is inert notes text, not authority or a stable transport schema.
  The first collector uses explicit current destination inputs; it does not execute/auto-route
  from notes or treat parsing that text as independent evidence.

## 3. Evidence identity, precedence and freshness

Every claim has a subject (project identity/ref/path/attempt), observation scope, provenance,
observation time, value and evidence reference. Identity is what a claim concerns; evidence
supports a claim; reconciled state is a derived description; authority permits an action.
These four concepts must not be collapsed.

There is no universal total ordering of all evidence. Compare only the SAME subject and claim:

1. Valid, current, direct bounded observations establish current facts within their coverage.
2. Historical adapter receipts establish attributed past claims; structural validation and
   matching hashes alone cannot authenticate them. Synthetic evidence stays synthetic.
3. Historical intent establishes what was recorded as intended, never execution/completion.
4. Curated narrative is retained as quoted context, never parsed into authority or executable work.

A fresh observation cannot erase historical intent or prove who performed an operation. A stale
receipt cannot override current Git. Two disagreeing current observations establish a race or
conflict, not permission to choose one. Missing/failed observation never defeats prior evidence
by replacing it with zero, false, empty/clean or a newly dated success.

Use these conceptual freshness labels per claim (not new existing-schema enums):

| Label | Meaning |
|---|---|
| CURRENT | Directly observed within this invocation and stable under the declared repeated checks, or historical applicability explicitly re-established against every required dependency |
| HISTORICAL | Structurally valid attributed past evidence; not claimed current or authenticated merely by validation |
| STALE | Known dependency/state change makes an earlier claim inapplicable to the current question; it can remain valid history |
| CONTRADICTED | Evidence values cannot both satisfy the same claimed subject/time scope; preserve both references and explain the mismatch |
| UNKNOWN | Missing, unsupported, failed, ambiguous or insufficiently covered evidence |

A remote moving from A yesterday to C today is not proof yesterday's receipt was false. The
receipt is HISTORICAL; reusing it as a claim about today is contradicted/stale. Likewise HEAD B
does not delete a historical checkpoint A. A generation/time orders records, not truth or authority.

State relationships govern freshness: root/Git identity, branch/HEAD, tracking/destination/ref,
index entries and flags, worktree bytes/modes including relevant untracked inputs, reviewed paths,
test inputs and environment scope. Timestamp equality and repeated porcelain output alone are
insufficient for content equality. Equal device/inode values are scoped local identity evidence,
not a global identity or protection against inode reuse/hostile same-user replacement. Moving a
repository to another path/device requires explicit rebinding, not silent continuity acceptance.

Historical inspection digests cannot be compared as timeless fingerprints. Compare validated
semantic fields and separately collected content identities, preserving timestamps/provenance.
Where content identity is unavailable, emit UNKNOWN rather than claiming project unchanged.
A report is valid only for its observation window and explicit coverage; any later action must
re-observe relevant state. No TTL guarantees a stable repository or future permission. Current mutation attestation is
limited to its exact invocation, operation, project, selected state and destination/history where
applicable; process replacement, invocation completion, relevant state change or scope expansion
requires new validation/authority. No unimplemented expiration/token service is assumed.

## 4. Review decision and compatibility

**Selected solution for the next implementation: require fresh review/digests after uncertain
interruption (option B), without changing durable schemas.** Observation of current content is
not itself review. The engine may compare explicit current review evidence; it cannot invent it.

| Alternative | Assessment |
|---|---|
| Persist hashes and reuse them as approval | Rejected: replay/staleness and authority violation; a digest is not a grant |
| Require fresh review with current digests | Selected now: compatible with current strict schemas and adapter call contract; honest about missing evidence; may cost a human one new review |
| Persist historical hashes plus require fresh authority | Useful possible later optimization, NOT_STARTED: reduces repeated content comparison but needs explicit versioning, provenance/privacy and persistence acceptance |
| Infer reviewed content from paths/current index/HEAD | Rejected: different bytes can share a path; present Git objects do not establish past review |

For a future persisted review extension, the minimum conceptual binding would include source
identity, base commit, relative path, operation (including explicit deletion), SHA256 of raw
reviewed bytes where present, file mode, review provenance/time and schema version. Git object ID
and raw SHA256 have different encodings/algorithms and must not be substituted. Intended tree
proof additionally needs the prior complete index/base and unselected entries; hashes for selected
files alone are insufficient. This is a design constraint, not a new field accepted today.

Reuse current candidate restrictions: at most 64 explicit paths, 2,048 characters per path,
1 MiB/file and 4 MiB aggregate, no-follow/ownership/type checks, sensitive/generated path and
content refusals. Deletion is explicit absence, not missing digest. No file contents enter a
handoff or result. Hashes can leak equality or low-entropy content through guessing; paths can
be private. Keep private storage, minimize fields, screen allowed outputs, never inspect known
credential paths, and do not claim hashing makes sensitive material safe for export. Canonical
sorted serialization and versioned validators would be mandatory before such an extension.

Compatibility: accept only the exact supported current handoff/inspection/attempt versions with
their existing strict key allowlists and integrity checks. Missing required fields or extra fields
in those schemas are invalid, not optional extensions. A valid old record lacking capabilities it
never defined (review map, test fingerprint) yields UNKNOWN in the reconciliation projection.
Unknown future/older unsupported schemas are refused without migration or rewrite. An unreadable
handoff can coexist with independently observed local facts, but cannot supply recovered intent.
Do not retrofit fields into notes and silently reinterpret them as authenticated structured data.

## 5. Bounded read-only pipeline and output

Conceptually: reconcile(validated durable evidence, bounded current observations, explicit scope,
current review/test evidence, current authority description) -> one explanation. Separate the
collector with I/O from a pure classifier. Identical complete inputs (including observation times,
failures, provenance and scope) MUST produce identical sorted canonical JSON and derived human text.
No random IDs, implicit current clock, hidden environment queries or action execution in classification.

Pipeline for the first implementation:

1. Validate explicit project/store paths, requested claim scope and bounded inputs. Read handoff
   with create=false, without writer lock, migration, publish or record_failure. Read-only scope
   follows existing inspection authority: explicit project, permitted ownership/layout and current
   user task; no mutation approval is needed merely to inspect permitted local state.
2. Obtain current bounded local inspection. Preserve its refusal unchanged if unsafe/unsupported.
   Do not use a refused snapshot as partial valid observation. Historical evidence stays separate.
3. For an accepted target, gather bounded supplemental facts: current full index-entry/flag identity,
   HEAD commit type/tree/parent IDs, explicitly relevant historical commit IDs, and Git lock/operation
   marker presence via safe metadata. Use existing fixed Git runner/environment/path checks. No
   index write-tree (it can write objects), hash-object -w, fetch, refresh-index or mutation helpers.
   Compare at most current HEAD and one relevant historical checkpoint/base; ambiguity is UNKNOWN,
   never an unbounded reflog/history search. Commit existence does not prove reviewed intent.
4. Optional current review comparison hashes only explicitly selected safe files under section 4
   bounds. No arbitrary content crawl. Without such evidence, dirty-content equality and review
   applicability remain UNKNOWN. Untracked/ignored inputs outside coverage stay explicit unknowns.
5. Optional explicit local-bare remote observation follows section 7. Default is NOT_QUERIED.
6. Repeat relevant local observations/index/identity/config/lock metadata and reread handoff
   generation/digest. Any observed change invalidates current cross-domain conclusions; return
   TARGET_CHANGED/refusal, preserve historical references, do not retry. No atomicity claim.
7. Classify facts, differences, unknowns, required observations and one safe next action. Return
   output only; no handoff writes or receipt promotion. An explicit future persistence workflow
   requires separate authorization and compatibility design.

Never acquire checkpoint._writer or HandoffStore.writer as a read-only safety probe: both can
create lock files. Existing lock availability could not prove quiescence anyway. Known Git locks,
operations, prior unresolved mutation and any supplied live-process evidence block quiescence
claims. A PID alone can be reused; absence of a lock/PID is not proof no child can still mutate.
The first engine does not scan the machine or act as an orphan supervisor. Exact process evidence
may be supplied by a bounded trusted observer; absent coverage remains UNKNOWN. Killing/reaping
only the reconciler's own observation subprocesses on timeout/cancellation follows the existing
runner contract; never kill a prior invocation's children.

The conceptual result is a NEW versioned projection, not an extension of existing handoff JSON:

| Group | Required meaning |
|---|---|
| Scope/provenance | Explicit project, requested continuity level/claim, observation window, coverage and supported projection version |
| Evidence references | Handoff generation/digest and slot references, validated observation digests, exact subject/value/source for each conclusion; minimize rather than duplicate the whole handoff |
| Domain facts | Project/local Git/checkpoint/publication/test/review/authority facts, with freshness and historical/current separation |
| Reasons | Bounded contradictions, unknowns, stale dependencies, observation failures and proof obligations not satisfied |
| Required work | Required observations and human actions, exactly one safe next_exact_action; all inert descriptions, not executable commands |
| Safety | safe_to_resume=UNKNOWN, mutation_allowed=false, automatic_mutation_authorized=false; retain existing adapter errors as attributed reasons, not forged prior-operation errors |

The first implementation must choose one explicit projection version and strict validator before
adding its tests, without migrating current schemas. Use existing OBSERVED/REFUSED for collection
outcome. OBSERVED does not mean safe or complete; a readable report can contain unknown domains.
Failure of required local observation gives REFUSED; failure of optional remote observation can
leave local facts OBSERVED with remote UNKNOWN. No generic “all good” boolean.

Choose next_exact_action deterministically from unmet dependencies of the requested claim:
unsafe/mismatched target first; unreadable required durable evidence second; unresolved active
mutation/locks third; conflicting HEAD/index/ref observations fourth; missing review/test bindings
fifth; missing requested remote evidence sixth; otherwise report no action required now. Within
a category sort by domain then subject/path. Return all other reasons in bounded sorted lists;
do not hide them because only one next action is selected. Request authority only for a requested
future action, not simply because a read-only report lacks write permission. Operator notes can
inform quoted context but cannot override this ordering, choose new targets or execute commands.

## 6. Checkpoint reconciliation

Always distinguish current commit identity, historical receipt and attribution to the interrupted
operation. A valid surviving commit with expected parent/tree can support a structural relationship
if those expectations were independently supplied with sufficient provenance. It does not backfill
local_commit in the old attempt or prove a new process received normal completion. If intended
content/tree is unavailable, report the commit and missing relation explicitly; do not manufacture
an intended tree from the present index. A new valid commit need not be CGC's commit.

An unchanged HEAD proves no net HEAD movement between the observations, not that no commit was
created/moved away in between or no unreachable object exists. Likewise staged paths do not prove
which add invocation staged them. Use “observed old HEAD/new index,” not unsupported causal stories.
No reset, deletion, duplicate checkpoint, reuse of pending intent as authority or automatic staging.
Dirty work can be well explained; clean work can conceal unexplained history or missing evidence.

## 7. Publication and local-first observation

Only query remote state when the requested claim depends on it AND current explicit read scope
identifies the destination/ref. Remote read scope is not history/publication approval. Historical
notes/config alone do not authorize new access. Pure local continuity does not require network.
The initial collector supports only the accepted explicit local-bare path/layout/config/identity
boundary; HTTPS/SSH/general transport remain NOT_STARTED.

Within that boundary, bounded ls-remote and direct bare-ref/commit-type reads may compare the live
approved ref with expected checkpoint and existing local tracking ref. Repeat the live read and
identity/config checks to detect movement. Do NOT call publish(), fetch objects, update tracking,
create a missing branch or repair artifacts. If objects required for a local comparison are absent,
report UNKNOWN rather than fetching. Keep historical VERIFIED receipt separate from current ref
agreement. Read-only agreement is a current observation, not a retroactive successful publication,
not proof which process moved it and not the existing adapter's FETCH_TRACKING_LS_REMOTE_DIRECT_BARE_REF
verification method. First engine never issues a new publication receipt.

Pack/loose-object presence is not ref publication; absence of a tracked receipt is not proof nothing
arrived. No object-store crawl, pack validation/repair, gc or prune. A temporary pack can force the
current accepted scan/layout bounds to refuse; preserve that refusal and artifacts. Remote tip
unchanged means observed net tip unchanged, not universal proof that no transient update occurred.
If current tracking differs, report it; authorized publication re-verification is a separate action,
never this reconciler's hidden next step. Current remote failure cannot erase an older receipt.

## 8. Test evidence

Keep project tests independent from preservation, publication and resume status. Current records
store curated command/result strings, not a durable tested-state binding. Even HEAD equality plus
clean porcelain cannot upgrade those notes into a current verified PASS. Retain the historical
reported PASSED/FAILED/SKIPPED/UNKNOWN and mark current applicability UNKNOWN when binding is absent.

A future reusable bounded test receipt needs trusted execution provenance, project identity,
HEAD/branch plus semantic index identity (entries/modes/stages/flags), relevant worktree bytes/modes
and untracked/generated/dependency inputs, exact command, result, observation interval and declared
environment/dependency identity. A declared finite input/environment scope is essential; no claim
of universal reproducibility or full-machine capture. Same HEAD with dirty changes, dependency
updates, changed test command/environment or missing input coverage cannot establish applicability.
Timestamps alone never establish it. Index byte equality is useful crash evidence but index
stat-cache byte differences need not imply changed semantic test inputs; preserve the distinction.

For independently validated, sufficiently bound historical receipts: compare all declared inputs
and environment under fresh observations. Matching dependencies supports CURRENT applicability
within that explicit scope, with the original execution time unchanged. Known mismatch is STALE;
missing dependency/environment coverage is UNKNOWN. A receipt already contradicting its own bound
state is rejected as invalid. Test failure remains a truthful result and can support a deliberate
repair continuation; it is not automatically a preservation failure. Do not auto-rerun tests or
invent commands from notes. No structured test producer is implemented or promised in the first
engine; it must conservatively classify the legacy reports it actually receives.

## 9. SAFE_TO_RESUME proof obligations

Keep existing vocabulary YES / PARTIAL / NO / UNKNOWN; do not introduce SAFE as an alias.
The first read-only engine always emits UNKNOWN. Later external promotion to YES requires a
separately accepted verifier, with a precisely stated continuation action and preservation level:

1. Explicit project identity and relevant layout/config are freshly validated; no unexplained rebinding.
2. Covered repository state is sufficiently quiescent under the accepted owner-controlled scope;
   no unresolved lock, operation, active-mutation evidence or unexplained prior child. Repeated
   reads and available flock alone do not discharge this obligation.
3. HEAD, branch, semantic index, selected/unselected work and relevant unfinished human files are
   reconciled with intent. Dirty is allowed when understood and within continuation scope.
4. Historical intent, missing receipts and contradictions affecting that action are resolved or
   bounded with explicit evidence. Missing review cannot be silently waived by a digest or path.
5. The requested preservation level is actually established: continuity content/readback for
   HANDOFF_ONLY; independently validated local checkpoint for LOCAL_CHECKPOINT; fresh approved
   remote/tracking/local evidence for REMOTE_VERIFIED. Do not force publication for local-only work.
6. Test evidence applicability and failures are explicitly accounted for. A known failure or stale
   result may permit a scoped diagnostic/repair continuation; never a claim that current tests pass.
   Policy-required test evidence for the specific action must be satisfied, not silently waived.
7. Any new mutation has NEW scoped current authority and review. Pure observation needs only its
   existing inspection/read scope; a no-mutation request need not obtain invented write approval.
   No exported YES is a capability token; the action must revalidate authority and state at use.
8. Fresh-resume verification binds exact evidence/provenance, requested scope and unresolved limits
   to the existing receipt/lifecycle requirements before a future PRESERVED record can be issued.
   Historical structurally valid resume_digest/inner YES is not that external proof.

NO/PARTIAL external decisions also require later defined action-scoped rules; do not infer them
from missing fields in this first slice. Preserve clear blockers separately while returning UNKNOWN.
All evidence reconciled with no current mutation requested is useful OBSERVED knowledge, not a
reason to manufacture a checkpoint, approval request or a YES. The first engine can be complete
without claiming the overall V3 safe-resume workflow complete.

## 10. Interrupted-attempt matrix

These rows derive from already accepted tests, not new crash experiments. Each row requires a
fresh explicit project identity/local observation; every mutation is outside reconciliation and
requires new authority. U means SAFE_TO_RESUME=UNKNOWN and mutation_allowed=false in ALL rows.
“Next” is read-only or a human request, never automatic repair. No row proves an unobserved negative.

| # / accepted evidence | Durable evidence | Fresh observations required | Supported conclusion / forbidden inference | Refusal and authority / next exact action |
|---|---|---|---|---|
| 1. Add before rename ([tests](../tests/test_add_interruption.py)) | CHECKPOINTING, paths, old inspection; possible failure record | HEAD, installed index, lock presence, work | Old index/lock observed; candidate completeness only if independently observed, not inferred from filename | U; new checkpoint refuses GIT_LOCK_PRESENT; establish lock/process ownership without deleting it |
| 2. Add after rename ([tests](../tests/test_add_interruption.py)) | Same intent, no commit receipt | HEAD, semantic index, lock metadata/work | Staging exists, no receipt; cannot claim checkpoint or exact historical review | U; existing adapter refuses EXISTING_STAGING; obtain fresh content review |
| 3. Commit before acceptance ([tests](../tests/test_commit_interruption.py)) | CHECKPOINTING plus possible failure | HEAD/index/locks and relevant base relationship | Old HEAD/staging observed, not proof no unreachable commit was created | U; inspect unresolved staging/locks before any new action |
| 4. Commit survives interruption ([tests](../tests/test_checkpoint.py)) | Pending intent; local receipt possibly absent | Valid current commit, parent/tree vs independently known expectations, work/index | Commit exists; intended match may be UNKNOWN; no retroactive adapter success | U; establish missing intended-content relation with fresh review |
| 5. Parent dies, Git survives ([tests](../tests/test_parent_death.py)) | Unchanged CHECKPOINTING; no death receipt | Index/lock facts; supplied live-child evidence and its limits | CGC flock release does not establish safety; lock may already be absent | U; refuse continuation through unresolved mutation; request explicit quiescence investigation, never kill old child |
| 6. Loose objects arrived ([tests](../tests/test_transfer_interruption.py)) | PUBLISHING/local receipt/context, possible failure | Local identity/HEAD; explicitly scoped current remote ref | Observed ref unchanged or moved; object existence cannot imply publication | U; compare current approved ref, do not retry transfer |
| 7. Temporary pack/index-pack ([tests](../tests/test_pack_interruption.py)) | Same pending intent, possible failure | Safe bounded artifact metadata if available; ref and layout checks | Artifact retained or observation refused; no corruption/success inference from filename | U; report artifacts and observation limits, no cleanup/repair |
| 8. Ref transaction before acceptance ([tests](../tests/test_mutation_interruption.py)) | PUBLISHING; pending receipt / failure | Remote ref/locks, source/tracking | Ref state now, not dispatch/acceptance reconstructed from intent | U; independently inspect approved ref; preserve lock refusal |
| 9. Remote now equals expected ([tests](../tests/test_publication.py)) | Pending PUBLISHING with expected/local context | Explicit identity/ref, direct/live comparisons, local/tracking | Present equality; causality/old completion unknown; tracking may differ | U; report equality/mismatch; separate authority for any adapter re-verification |
| 10. Historical VERIFIED ([tests](../tests/test_publication.py)) | Matching saved receipt | Relevant current local/tracking/remote if current remote claim requested | Historical verification retained; current agreement only when re-observed | U; observe missing dependencies; never inherit old safety |
| 11. Local-only checkpoint ([tests](../tests/test_checkpoint.py)) | local_commit, publication NOT_REQUESTED | Current local commit/work/index and receipt binding | Local checkpoint may be present; no remote preservation claim needed | U; reconcile local unfinished work; do not query/publish remote by default |

## 11. Future acceptance cases

**First-engine cases A–R are implemented; section 14 distinguishes accepted scope from future extensions.** Existing
interruption tests establish the source scenarios only. Every case asserts zero mutation commands,
no source/store/config/index/ref/artifact writes or deletion, no old-child kill, no automatic test
execution, no receipt rewrite, deterministic classification and human/machine agreement.
All cases require safe_to_resume=UNKNOWN and mutation_allowed=false. “Authority” below means for
a later mutation, never for invoking an already authorized local read. Fresh evidence is collected
once per call, not an automatic retry. Common constraints apply to every row.

| Case | Facts | Unknowns / contradictions | Fresh observation required | Fresh authority required | Next exact action |
|---|---|---|---|---|---|
| A | Pending CHECKPOINTING + old index + index.lock | Lock owner/liveness and intended content can be unknown; no contradiction solely from pending state | Identity, HEAD/index/lock/work | Yes for later mutation; cannot override lock refusal | Establish lock/quiescence facts |
| B | Pending CHECKPOINTING + complete staged index | Missing receipt/review; staging is not success | Index entries, HEAD, work bytes within approved scope | Yes; existing checkpoint still refuses staged state | Re-establish reviewed content identity |
| C | Pending CHECKPOINTING + surviving valid commit | Attribution/intent match unknown without tree/base/review; no invented failure or success | Commit type, parents/tree and supplied expected relation | Yes for new mutation | Explain commit-to-intent relation |
| D | Pending CHECKPOINTING + unexpected HEAD B | Expected A/current B mismatch; preserve both, no rollback | Identity/branch/HEAD, bounded relation | Yes; mismatch blocks inferred continuation | Ask human to explain changed history |
| E | Pending PUBLISHING + current remote still old | Dispatch/transient updates may be unknown; objects irrelevant | Explicit remote identity/ref and local/tracking | Yes for publication | Report current tip without retry |
| F | Pending PUBLISHING + remote expected commit | Attribution and old normal completion unknown; stale tracking may contradict present equality | Direct/live ref, local/tracking, destination identity | Yes for any re-verification that writes | Report agreement and remaining tracking gap |
| G | Historical VERIFIED A + remote now C | Past proof remains history; its current reuse is contradicted | Explicit current remote plus local/tracking | Yes; no overwrite to restore A | Explain remote movement |
| H | Historical test PASS + apparently unchanged project | Legacy receipt lacks binding: applicability UNKNOWN; fully bound trusted fixture may be CURRENT in declared scope | All receipt dependencies, not HEAD alone | Only for later mutation/test execution | Acquire missing binding, or report scoped applicable history |
| I | Historical test PASS + changed input/environment | STALE applicability, not erased historical PASS | Changed dependencies and scope | Only for subsequent action | Identify changed tested inputs; no rerun |
| J | Saved paths, no reviewed digests | Historical reviewed bytes UNKNOWN | Fresh explicitly scoped content/review | Yes for mutation | Request fresh review/digest mapping |
| K | Historical digests match current bytes, authority absent | Content equality known within coverage; permission absent | Identity/content/mode and current authority input | Yes for mutation; digest cannot supply it | Report authority needed only if mutation requested |
| L | All supplied required facts explained; no mutation requested | No forced contradiction; external safety verification still absent | Current local scope, remote only if requested | No write authority needed for observation | Return explanation; no action required now |
| M | Local observation times out/fails | Current domain UNKNOWN; historical state retained | Failure code/coverage, not fabricated snapshot | No automatic retry authority | Report failed observation and ask for bounded follow-up |
| N | Handoff unsupported/corrupt/missing | Intent UNKNOWN; absent file differs from invalid required fields | Safe read outcome; independent local inspection if permitted | No inheritance | Report continuity unavailable, preserve original bytes |
| O | Repository identity mismatch or changes during observation | Old/new identities or snapshots conflict | Repeated identities/local observations | New explicit binding required, not automatic migration | Stop comparison and ask to confirm target |
| P | Remote unavailable/not authorized to query | Current remote UNKNOWN/NOT_QUERIED; local facts retained | Only explicitly scoped remote reads if permitted | Remote read scope distinct from publication authority | Return local report and missing remote observation |
| Q | Valid embedded attempt says YES; envelope UNKNOWN | Structural receipt claims are not independent proof | Validate both and current scope | No authority from YES | Keep outer UNKNOWN; list proof gaps |
| R | Bound exceeded or unsafe path/config | Required coverage incomplete; no truncated all-clear | Fixed refusal and limit | No escalation by inference | Explain narrower permitted scope needed |

Implementation tests must additionally cover deterministic ordering and failure codes; unsupported
projection versions/extra keys; symlink/hardlink/config refusal; bounded output; before/after full
fixture byte/mode/mtime comparison; no absent lock/store creation; cancellation of own observation
children only; stale remote tracking left untouched; timestamps not renewing old receipts; same
HEAD with dirty or environment changes; no remote query for local-only scope. Do not repeat the
entire synchronized crash suite to implement these classification cases.

## 12. Failure and resource contract

| Failure | Required degradation |
|---|---|
| Git timeout/cancellation/output limit | Existing fixed code; failed domain UNKNOWN, no partial valid snapshot, no retry; cleanup only own observation group |
| Permission/path/I/O failure or missing repository | REFUSED current-local collection, safe diagnostic; no directory creation, permission fix or fallback target |
| Identity mismatch / observed race | TARGET_CHANGED or existing identity reason; no combined coherent current snapshot |
| Handoff unreadable/invalid/unsupported | Durable domain UNKNOWN/refused with original bytes untouched; independent local facts may still be reported |
| Remote unavailable/unsupported/moved | Local facts retained; current remote UNKNOWN or explicit changed tip, historical receipt remains historical |
| Missing review/test binding | UNKNOWN applicability, never false approval or automatic rerun |

Proposed first-engine limits (new orchestration caps are SPECIFIED, not current runtime constants):

| Resource | Bound |
|---|---|
| Scope | One explicit project, one external store, at most one explicit local-bare destination and exact existing ref |
| Handoff | Existing 2 MiB envelope, 256 KiB attempt, two retained slots; no historical archive search |
| Inspection | Reuse 10,000 entries/depth 32/4,096-byte relative path; 16 MiB/file metadata bound and 64 MiB aggregate; 64 KiB config; 256 KiB snapshot |
| Time/commands | At most 48 Git subprocesses total including nested inspection/config reads; 5 seconds and 256 KiB combined output per command; 60-second cooperative invocation deadline, inspection calls at most 20 seconds each and capped by remaining invocation budget |
| Supplemental local reads | At most two relevant commit IDs, bounded index output; initial/final comparison only, no automatic retry or history walk |
| Remote | At most two ls-remote calls and two direct ref reads; other bare validation/type/config reads count against the same 48-command budget; no fetch |
| Content/review | At most 64 explicit paths, 2,048 characters each, 1 MiB/file, 4 MiB aggregate under current candidate rules; no broad content crawl |
| Test evidence | At most 64 bounded command/result entries inherited from notes, 2,048 characters each; no raw logs, environment dump or dependency scan |
| Result | At most 256 KiB canonical JSON; at most 64 entries per reasons/required-work list, text at most 2,048 characters; overflow refuses, never silently truncates coverage |

All collectors, including reused helpers, must share/enforce the outer command/deadline budget in
the future implementation. Do not assume existing helpers already implement that orchestration.
Filesystem syscalls, Git decompression and cleanup are not hard realtime/RSS sandbox guarantees.
Reading may update atime; read-only prohibits intentional content/index/ref/config/store changes,
not kernel access bookkeeping. No remote credentials/account discovery or unrelated-root traversal.

## 13. Human view and implementation decision

This section retains the original contract-only decision; section 14 records implementation.

Human text derives from the same validated projection, quoting inert operator text and paths.
Explain saved/unsaved work, known failures, uncertainty, what was observed versus reported, remote
verification scope, missing permission and one next action. Do not require Git jargon to act safely.
For example (conceptual, NOT output from an implemented engine):

```text
PROJECT: current local identity matches the recorded project
SAVED INTENT: checkpoint requested; completion receipt missing
LOCAL WORK: a valid commit exists; its relation to the reviewed work is not proven
REMOTE: not requested or queried
TESTS: historical reported PASS; current applicability unknown
REVIEW: saved paths exist; reviewed content hashes are missing
AUTHORITY: fresh approval required if a new mutation is requested
SAFE_TO_RESUME: UNKNOWN
NEXT_EXACT_ACTION: re-establish the reviewed content identity
```

Use durable evidence to avoid repeated archaeology and accepted crash investigations, but never
trade stale assumptions for fewer tokens. No telemetry or model reasoning capture is added.

**Ready to implement: YES, for the minimal bounded read-only engine defined here.** The review
choice is settled; current schemas remain strict; current safety remains UNKNOWN. Full external
safe-resume promotion, persisted review/test extensions and action execution are separate future
acceptance blocks. Next action: implement this minimal engine against cases A–R in disposable
fixtures, beginning with interrupted intent/current local state and explicit missing evidence.
That contract-only session stopped before implementation; section 14 records the subsequent authorized block.

## 14. First engine implementation and conformance

The specification above is retained as the implementation contract. The first-engine API is
implemented in [reconciliation.py](../src/cgc/reconciliation.py), with acceptance in
[test_reconciliation.py](../tests/test_reconciliation.py). Full external safety verification,
structured reusable test receipts, durable review extensions and all recovery remain NOT_STARTED.

Python interface (no reconcile CLI added):

```python
from cgc.reconciliation import reconcile, render_json, render_human
result = reconcile(project, store_dir=external_store, now=explicit_utc_timestamp)
```

`collect` performs bounded I/O; `classify` is pure; `reconcile` composes them. `validate_result`
strictly validates nested evidence and recomputes every derived field; both renderers use it.
Projection version: `cgc-reconciliation-v3.0-provisional`. The new projection does not migrate
or modify any existing attempt/inspection/handoff schema. All three safety fields are fixed
UNKNOWN/false/false, even if a valid saved pure attempt reports YES.

The projection stores bounded `evidence`, sorted `issues`, claim-specific freshness, current
review/test applicability, checkpoint structural relation, remote observation status, required
observations/human actions and one next_exact_action. Evidence includes both local observations,
both optional remote observations, historical summaries of both handoff slots and the final
handoff generation/digest/error reference. Summaries retain phase, provenance, receipts, test
notes, known failures and original next action without duplicating the entire handoff envelope.
An inspection digest references the collected snapshot; it is not a portable content hash.
Observation time is explicitly caller-supplied, as in existing inspection; first/last readings
identify the bounded non-atomic observation window rather than inventing a trusted wall clock.

Optional arguments:

- `review`: current explicit path → SHA256 mapping (None means reviewed deletion), under existing
  candidate restrictions. Matching bytes establishes current scoped content evidence, not approval.
- `tests`: strict caller-attributed `{result, commands, results, bound_head}`. HEAD mismatch can
  establish STALE applicability; HEAD match still cannot establish complete dirty/environment
  applicability and remains UNKNOWN. Legacy saved test notes remain separately preserved.
- `remote`: explicit `{path, identity: {device, inode}, ref, tracking_ref, expected_commit}` for
  one approved local bare read scope. Defaults to no remote query. Source/store/remote cannot
  overlap; protected paths and unsupported configs/layouts/symbolic refs are refused.
- `expected_commit`: explicit caller-supplied `{parent, tree}` for structural comparison only.
  Matching that relation never backfills a receipt or authenticates historical review.
- `requested_operation`: OBSERVE (default), CHECKPOINT or PUBLISH, plus optional inert
  `authority_description`. These describe the question, never permit mutation. Only a requested
  future mutation produces a fresh-authority requirement; observation never demands write approval.

Collection refuses required-local failures and detected races; optional remote failures retain
local observations with remote UNKNOWN. Both sides of observed changes remain in evidence or
issue references. Metadata includes safe config fingerprints and Git lock paths; no lock probe
creates a file. No machine process scan; quiescence remains UNKNOWN. Artifact presence is a fact,
not proof of an active owner. Own Git observation groups are bounded/cleaned by the existing runner.

The shared invocation budget is a ContextVar in inspection: 48 commands, 60 cooperative seconds,
existing five-second/256-KiB command limits, nested budget replacement refused, and reset in finally.
It applies to nested inspection/config/remote helpers without global monkeypatching. Outside the
scope, existing mutation adapters retain their behavior. The existing candidate reader accepts
an optional shared byte budget; reconciliation uses it across BOTH review reads: at most 4 MiB
accepted content total (plus the usual one-byte overflow probe, never hashed/exported). Therefore
repeated review may exhaust the limit with more than 2 MiB of distinct content; it reports the
limit, never silently expands the contract to 8 MiB. No installation or new dependency is needed.

Malformed API/projection input raises fixed validation errors. A report that exceeds 256 KiB or
64 issues raises ReconciliationError(RESOURCE_LIMIT), without truncated output or handoff writes.
Observation failures otherwise remain fixed codes in a validated report. No raw subprocess
stderr, file contents, remote configuration values or environment dump enter the projection.
Pure classification/validation establishes consistency, not authenticity of externally supplied
input evidence. Rendered operator text is JSON-quoted and remains inert.

Cases A–R are covered for the first-engine scope (see named tests and progress). H's hypothetical
fully bound independently trusted test-receipt reuse is NOT_STARTED: no accepted producer/input
schema for complete environment/content binding exists. H's required legacy PASS/UNKNOWN behavior
is accepted. I uses an explicitly supplied historical HEAD binding to establish a known mismatch;
without a binding the engine cannot fabricate one. L returns no action when no relevant evidence
obligation is present, but never upgrades safety. Q uses a structurally valid stored inner YES.
No interruption test block is reimplemented; fixtures recreate its observable end states.


## 15. External verifier contract boundary

[V3_SAFE_TO_RESUME](V3_SAFE_TO_RESUME.md) now specifies the separate future verifier. Section 9
remains the foundation: actual mutation needs fresh review, authority and state revalidation.
The new contract explicitly separates P12 authority from evidence-plane aggregation; a future
scoped YES never grants execution. Captured in-memory analysis needs no live-writer quiescence
claim, whereas continuation that touches the repository still does. This is an explicit future
proof-scope refinement, not a change to the accepted reconciler or preservation lifecycle.

The reconciler continues to emit UNKNOWN/false/false for every result. Genuine repeated-observation
races remain valid uncertainty reports; the verifier's tamper harness rejects false stability
claims, not truthful race evidence. Full contextual review and trusted test/writer coverage cannot
be inferred from this projection's current summaries. No runtime/schema change accompanies the
verifier specification; its own acceptance cases and producers remain NOT_STARTED.
