# CGC V3 — bounded positive quiescence evidence contract

Status: **SPECIFICATION COMPLETE; producer runtime NOT_STARTED**.
Contract revision: **V3 quiescence contract 1**. CREDID GUARDIAN CODEX (CGC).
Subordinate to [V3 mission](V3_MISSION.md), [verifier section 6](V3_SAFE_TO_RESUME.md#6-quiescence-what-can-actually-be-proven)
and [reconciliation](V3_RECONCILIATION.md). This defines a new evidence domain, not permission
for a supervisor, recovery, execution, schema migration or V4 runtime.

## 1. Audit and decision

Starting verified checkpoint: `61993cddeff2b4c8afc7526b9c87648684841a02`, clean main,
local HEAD = origin/main = live remote main. Accepted verifier implementation:
`993f347acc2cc2db2f233db4adbd8f6dd15d1855`. Its real positive scope remains captured
READ_ONLY_ANALYSIS / HANDOFF_ONLY, with both mutation flags false. The reconciler still
returns UNKNOWN/false/false. No runtime defect requiring correction was found.

Audited sources: [reconciler](../src/cgc/reconciliation.py),
[verifier](../src/cgc/safe_resume.py), [capture](../src/cgc/verification_capture.py),
[registry](../src/cgc/verifier_registry.py), [inspection](../src/cgc/inspection.py),
[handoff](../src/cgc/handoff.py), [checkpoint](../src/cgc/checkpoint.py),
[publication](../src/cgc/publication.py), [attempt](../src/cgc/preservation.py),
[signals](../src/cgc/signals.py). Accepted evidence:
[parent death](../tests/test_parent_death.py), [staging](../tests/test_add_interruption.py),
[commit](../tests/test_commit_interruption.py), [reconciliation tests](../tests/test_reconciliation.py),
[verifier tests](../tests/test_safe_resume.py). These experiments were not rerun.

The source flock and handoff-store flock coordinate cooperating CGC parents. They are not
inherited guarantees covering every mutation child. Parent-death acceptance shows both flocks
can release while real Git remains alive, before or after index replacement. A process group
is not descendant containment. Existing inspection command cleanup signals its own process
group and reaps its direct child; it does not establish absence of escaped or orphaned writers.

Bounded platform observations in this audit: `uname -sr` reported
`Linux 6.18.33.2-microsoft-standard-WSL2`; filesystem type at this project was `v9fs`.
No machine process scan, Windows observer, isolation setup or capability experiment was run.
No actual Windows writer was asserted present or absent.

**Decision: PARTIAL feasibility; current production-positive target is D: NONE.**
The existing shared `/mnt/c` environment and current CGC producers cannot discharge P3.
P3 remains UNKNOWN, not UNSATISFIED merely because coverage is missing. A finite closed model
is specified below, but its admission/containment and filesystem-exclusivity prerequisites
are not implemented or experimentally accepted. No JSON profile name can establish them.

One conditional future candidate is **CGC_EXCLUSIVE_LINUX_CHECKPOINT**, limited to one
CREATE_CHECKPOINT action, source repository and handoff store in an externally established
exclusive Linux workspace. It is a design candidate, NOT an accepted operational profile.
A registered CGC-only subset can have complete subset coverage without satisfying action P3.

## 2. Meaning and writer universe

QUIESCENT_WITHIN_ACCEPTED_SCOPE means positive finite evidence accounts for every potential
writer relevant to the declared project, action, domains and interval, within an explicitly
validated environment boundary. It does not mean no process anywhere could modify anything.

A closed world requires independently established admission/exclusion, not a list labeled
complete. For the candidate profile, the finite universe comprises admitted CGC mutation
roots, their Git workers and every descendant/helper capable of touching the source or store.
The coordinator is itself a relevant writer if it can change handoff or admission state.
Its own mutation activity must be excluded during capture. Fixed versioned worker policy
must account for executable helpers; current hook/filter/layout refusals remain in force.
Unregistered shells, editors, agents and offloaded services are not silently excluded.

In an open shared desktop repository, IDEs, shells, host programs, containers and other agents
may have relevant access outside CGC's lifecycle record. Coverage is UNKNOWN. An operator
statement, empty registration table, elapsed quiet time or repeated stable state cannot close
this world. Registration is useful attribution, not enforcement against uncooperative writers.

Evaluate three mechanisms separately:

| Mechanism | Establishes if validated | Does not establish |
|---|---|---|
| Cooperative registration | Named writer instance, declared project/domain, lifecycle attribution | Completeness of filesystem writers or descendants |
| Exclusive CGC admission gate | No new admitted CGC operation during a bound gate epoch | No external writer; existing flock alone is insufficient |
| Environment closure plus descendant containment | All relevant admitted mutation paths belong to the controlled domain | Universal safety against privileged host/kernel compromise |

The trusted computing base includes the accepted kernel, owner-controlled coordinator and
validated isolation configuration. Host administrators are not adversaries this V3 model
claims to defeat. Ordinary host/editor/container access, however, cannot be waved away as
privileged compromise. The environment producer must prove its exclusions within that model.

## 3. Process identity and descendant closure

A command name or path is context, not identity. A PID is namespace-relative and reusable.
A diagnostic process tuple binds boot identity, PID-namespace identity, PID, start observation
and producer epoch. It is not a portable capability or an unconditional non-reuse guarantee.

The candidate requires a launch-bound, retained kernel process handle for each registered root
and any individually claimed terminal instance. Acquisition must identify the intended process
without a registration race. Linux pidfds can expose termination through polling; acquiring a
pidfd after fork has documented child-reaping conditions. A process-level handle must cover
all threads, not merely one exiting thread. These primitives do not prove descendant exit.
See [Linux pidfd documentation](https://man7.org/linux/man-pages/man2/pidfd_open.2.html).

A serialized file-descriptor number cannot restore a handle after restart. Reopening a recycled
PID cannot authenticate the old instance. Missing handle continuity gives UNKNOWN. A new process
with the same PID but different start identity is a different instance; neither inherits the
other's terminal evidence. Start-time metadata is corroboration, not replacement for acquisition
provenance. Exec keeps the process instance but may change permitted execution scope; an
unaccounted executable transition invalidates coverage. Parent links describe observations at
specific times, not a permanent ownership tree.

Fork, pipelines and helper launch extend the writer domain. Double-fork, setsid, daemonization
and reparenting must not escape it. Parent terminal, PPID change or empty original process group
is insufficient. A one-time /proc or ps scan cannot prove closure across races/namespaces.
No global scan or command-name matching is proposed.

A candidate containment primitive is an externally controlled cgroup-v2 domain established
before workers can execute/fork, with migration and new admission prevented during capture.
The kernel's recursive `cgroup.events` populated state reports whether the subtree has live
processes. This is useful setwise evidence, not filesystem exclusivity or a lifecycle log.
See [kernel cgroup-v2 documentation](https://docs.kernel.org/admin-guide/cgroup-v2.html).

Acceptance must prove membership cannot escape and no new worker can enter during the window.
A zero populated observation without those conditions is insufficient. Setwise termination
may cover unenumerated short-lived descendants only when continuous containment is proven;
it must not invent individual exit receipts. All known identities still require consistent
lifecycle accounting. Unsupported/threaded domain layouts, lost controller continuity,
migration authority or an escaped child yield UNKNOWN. This audit did not test cgroup access.

A process namespace alone restricts visibility, not access to shared files. Containers sharing
bind mounts, passed writable descriptors, alternate mounts, hardlinks or delegated IPC workers
can reopen the writer universe. Queued asynchronous writes/offloaded jobs require completion
coverage or explicit exclusion by the accepted execution profile. Process exit alone does not
prove those operations complete. Logical repository stability is not power-loss durability.

## 4. WSL and filesystem closure

Microsoft documents Windows-drive paths mounted under `/mnt` and Windows access to Linux
files through `\\wsl$`. Therefore even moving a fixture to Linux-native storage does not by
itself prove host-writer exclusion. See [WSL filesystem interoperability](https://learn.microsoft.com/en-us/windows/wsl/filesystems).

For this `/mnt/c` project, Linux-only process evidence cannot establish Windows Git/editor
absence. Another distribution, Docker bind mount or network/shared backing store must also be
accounted for if it exposes the same objects. No such closure evidence exists in current CGC.
WSL restart or boot/namespace change invalidates retained process evidence. A dedicated directory,
container, PID namespace or Linux filesystem label alone is not an accepted isolation proof.

The conditional candidate needs independently validated exclusive access to source, Git metadata
and store, including aliases and delegated writes. A future host integration or isolated runner
might provide this; neither is implemented or authorized here. Missing closure cannot be hidden
by narrowing a profile to just the convenient visible processes.

## 5. Action and mutation-domain binding

| Requested action | Required relevant coverage |
|---|---|
| READ_ONLY_ANALYSIS of captured inert evidence | P3 NOT_APPLICABLE; do not invoke this producer |
| CONTINUE_EDITING | Selected/context worktree writers, index/ref/config/operation state relevant to the base, continuity store |
| RUN_TESTS | Declared test inputs and outputs plus all executable test/helper descendants; arbitrary test code requires its own accepted profile |
| CREATE_CHECKPOINT | Reviewed/unrelated worktree preservation, index, HEAD/refs, objects, config, operation markers and handoff store; first conditional candidate |
| PUBLISH_CHECKPOINT | Source metadata/objects/refs, source-work preservation, store and approved local-bare destination objects/refs/config plus receiver descendants |
| REPAIR_KNOWN_FAILURE | Unsupported; no generic repair or quiescence shortcut |

Domain exclusions need a structured relevance derivation. An unrelated-project writer is irrelevant
only if identities and aliases establish disjoint access. A claimed worktree-only writer cannot
be excluded from index coverage merely because its registration says so; enforced scope matters.
Local-only action never requires remote observation. Destination coverage is NOT_STARTED here.

## 6. Producer boundary and budgets

The future observer consumes already established coordination evidence. It must not establish
coordination by acquiring writer locks, creating registrations, changing permissions, moving
processes, mounting filesystems or creating cgroups/namespaces. Those are a separate future
coordination/environment layer requiring explicit authorization and acceptance.

| Property | Contract ceiling / rule |
|---|---|
| Inputs | Validated reconciliation capture; exact project/store/action; accepted environment/gate epoch evidence; retained process/domain handles and lifecycle records with current trusted provenance |
| Outputs | Strict fact/derivation receipt, per-domain coverage, blockers and P3 contribution; no authority or whole SAFE_TO_RESUME verdict |
| Commands | ZERO Git commands, ZERO subprocesses; no call to inspection._run or collect from inside this producer |
| Process scope | One pre-admitted writer domain; at most 64 named instances and 128 relationships; no machine scan |
| Observation operations | At most 512 bounded read/poll operations, two sweeps, no automatic retry or wait-for-exit loop |
| Time | 10 seconds total observation deadline; deadline failure UNKNOWN; no claim of hard kernel-I/O cancellation |
| Bytes | 16 KiB per scalar read, 4 MiB aggregate raw observations, 256 KiB canonical receipt |
| Structured input | At most 512 KiB combined canonical input, depth 32, 2048 characters/string, 64 items per claim/reference/blocker list |
| Handles | At most 128 simultaneously held supplied/opened read-only handles including anchors; exceeding any limit refuses coverage |
| Filesystem scope | Exact prevalidated source/Git/store anchors, declared metadata and admitted process/domain pseudo-files; no repository crawl, file contents, environment or credential reads |
| Network | ZERO; no HTTP/SSH, remote discovery or transport |
| Side effects | READ_ONLY observation; no signals, stop, kill, reap, lock creation/deletion, Git writes, recovery or persisted receipt |
| Failure | Preserve collected facts, mark affected coverage UNKNOWN; never synthesize zero writers from an error |

These are new proposed acceptance limits, not measurements or changes to existing collector
budgets. Repository identities/stability arrive from separately accepted bounded collection
within the same protected epoch. The observer validates those bindings; it does not secretly
refresh Git. The integration must account for the sum of both domains' budgets.

Read-only permits ephemeral observer-owned memory/descriptors, not target mutation. An underlying
primitive that cannot satisfy bounded observation must be unsupported; the observer must not
spawn a worker and signal it on timeout to evade the no-signal rule. Hard real-time guarantees
under a hung kernel/filesystem remain unproven. The pure classifier consumes explicit observations
and performs no I/O, clock read, environment discovery or randomness.

## 7. Window, freshness and invalidation

Bind window start/end, ordered observation sequence, producer instance, boot/namespace identity,
project/Git/store identity, request and gate epoch. Both process/domain sweeps and repeated
relevant repository/handoff evidence must lie inside one proven closed admission interval.
A capture made before that interval cannot silently satisfy stability. Wall-clock equality or
elapsed time is not ordering proof. Lost sequence/clock provenance leaves the affected claim UNKNOWN.

Claim-local CURRENT/HISTORICAL/STALE/CONTRADICTED/UNKNOWN follows reconciliation semantics.
Fresh receipt creation does not refresh old lifecycle evidence. Preserve historical and current
claims with their references. A valid report of contradictory source evidence is not malformed
merely because it is contradictory; a forged derived SATISFIED result is malformed.

Invalidate on new registration/spawn/admission, membership migration, observer/controller restart
or continuity loss, boot/namespace change, project/alias/config change, relevant HEAD/index/worktree
change, Git lock/operation marker appearance, handoff generation change, or relevant destination
ref/state change. A changed action/domain/profile also invalidates applicability. Receipt expiry
is event/state based, not a timer that grants safety until it rings.

At future execution, independently revalidate the protected epoch, writer universe, exact state
and current authority at the mutation boundary. A read-only observer does not hold that exclusion
for an executor. No executor exists in this block. QUIESCENCE != AUTHORITY; P3 satisfaction cannot
satisfy P12, supply review/test proof or authorize a new mutation.

## 8. Conceptual receipt and strict derivation

Draft identifier: `cgc-quiescence-v3.0-provisional`; **schema/runtime NOT_STARTED**. This is a
separate evidence receipt, not an extension of handoff or reconciliation schemas. Before runtime
admission every concrete leaf must receive a type, bound, role and dependency entry.

| Group | Typed content and origin |
|---|---|
| Binding | Version/profile, project/Git/store identities, one requested action, domain IDs; validated semantic inputs |
| Window | Producer epoch, boot/namespace reference, ordered start/end and gate evidence references |
| Universe | Environment-closure reference, admission reference, finite domain identity, declared coverage boundary |
| Instances | Unique writer ID, bound process instance, observed parent link, registration source, enforced domains, lifecycle/terminal references |
| Containment | Typed membership/closure observations and known descendant relationships; no arbitrary evidence bag |
| Stability | References to initial/final repository/config/lock/operation and handoff observations, optional relevant destination only |
| Claims | Per-domain coverage, freshness, active known instances or UNKNOWN, contradictions and missing evidence |
| Result | Derived SATISFIED/UNSATISFIED/UNKNOWN/NOT_APPLICABLE, reason IDs and inert required observations |
| Invalidation | Fixed profile conditions plus exact evidence-state preconditions; never a capability token |
| Context | Optional inert bounded labels; no full command line, environment dump, file contents or free-form instructions |

Evidence references must resolve to typed supplied observations. Process handles/provenance are
external current-call capabilities, not serialized booleans. Imported JSON with `trusted=true`
or a matching hash cannot authenticate itself. Follow the existing trusted owner-controlled
Python-caller boundary; do not claim protection against hostile code inside that caller.

Coverage states: COMPLETE_WITHIN_PROFILE, PARTIAL, UNKNOWN, CONTRADICTED. Complete subset coverage
must identify the subset and cannot substitute for complete action coverage. Known active count
is derived; an unobserved universe has no fabricated count of zero. Canonical FACT needs direct
provenance; DERIVATION lists sources. HYPOTHESIS is forbidden. No guessed causal history.

P3 derivation after strict validation:

1. Captured READ_ONLY_ANALYSIS: NOT_APPLICABLE by fixed verifier profile, not caller choice.
2. Unambiguous current evidence of a relevant active writer: UNSATISFIED; retain coverage gaps.
3. Otherwise any missing/contradictory required coverage, terminal proof, closure, stability,
   provenance or unresolved operation evidence: UNKNOWN.
4. SATISFIED only when all action domains have complete accepted coverage, all known relevant
   instances are terminal, continuous contained descendant closure is proven, admission remains
   closed, repeated bound state is stable and no unresolved relevant lock/operation remains.

A lock alone need not prove a live process. Retained locks can independently violate existing
P2 adapter policy while P3 stays UNKNOWN. No lock deletion or stale-lock guess. Conflicting current
terminal/active claims remain contradictory rather than choosing a convenient one; trustworthy
unambiguous active evidence can block while the contradiction is retained. Project mismatch is
an explicit P1 violation; mismatched receipt binding is rejected, never P3 satisfaction.

Observation failures, permission errors, missing identities, disappeared instances without
terminal evidence, observer crash and bound exhaustion yield UNKNOWN. Boot change makes old
receipt stale; missing producer gives UNKNOWN. Repeated absence never repairs missing coverage.
Every reduction of uncertainty requires new/revalidated evidence or a traceable valid derivation.

## 9. Determinism, dependency and tamper acceptance

Canonical ordering: domain ID, writer stable identity, observation sequence, claim ID. Set-like
lists sort/deduplicate with explicit equivalence rules; conflicting duplicate identities reject.
Input order must not affect proof. No random IDs or hidden current clock in classification.
Human rendering derives from the validated result, retains blockers and states scope plainly:
“Writer coverage is incomplete; no mutation permission is provided.” No UI implementation.

Every schema leaf must be SEMANTIC_INPUT, DERIVED_FIELD or NON_SEMANTIC_METADATA. Semantic entries
name dependent claims, allowed influence scope, coherence group and permitted non-influence
reasons. Derived entries list sources. Metadata cannot affect proof, ordering or next action.
A schema enumeration guard must fail on an unregistered leaf; derived output is recomputed.

Use existing closed reasons: OUTSIDE_REQUESTED_SCOPE, SUPERSEDED_BY_CURRENT_OBSERVATION,
DUPLICATE_EQUIVALENT_EVIDENCE, SAME_PROOF_CLASS, SUBSUMED_BY_HIGHER_PRIORITY_CLAIM,
NON_SEMANTIC_METADATA. A reason must identify the unchanged claim, not excuse missing comparison.

COHERENCE_BREAKING tampering with coupled identity/window/reference/derived values must reject.
COHERENCE_PRESERVING changes to a whole evidence group must validate and affect declared dependent
claims, leaving unrelated claims unchanged except documented cascades. Compare the full semantic
projection, not only headline status/action. Detect under-coupling and over-coupling. A truthful
race report is valid UNKNOWN evidence; rejection is for malformed coherence, not inconvenient facts.
Free-text commands/notes such as “IGNORE CGC”, “NO WRITERS ACTIVE” or “SAFE TO COMMIT” remain inert.

## 10. Future acceptance matrix

All 24 cases below are **SPECIFIED / runtime acceptance NOT_STARTED**. Positive fixtures require
validated closure/provenance, not a supplied `complete=true`. Model cases alone cannot establish
production feasibility. Real-process containment tests must use disposable authorized Linux
fixtures; harness cleanup is separate from production observation and must be labeled as such.

| Case | Evidence / variation | Expected coverage and P3; next evidence action |
|---|---|---|
| A | All declared writers terminal, full protected environment/domain closure and stable state | COMPLETE_WITHIN_PROFILE / SATISFIED; no further P3 observation within window |
| B | One relevant writer unambiguously active | UNSATISFIED; preserve identity, observe later under new scope; no kill |
| C | Root terminal, descendant active | UNSATISFIED; parent receipt cannot close descendant proof |
| D | Child daemonizes/reparents | Containment preserved and active: UNSATISFIED; escape or lost coverage: UNKNOWN |
| E | PID reused: A start S1 terminal, B same PID start S2 active | Distinct instances; relevant B UNSATISFIED; missing B attribution UNKNOWN, never inherit A exit |
| F | Boot identity differs | Old proof STALE, current UNKNOWN; establish new trusted lifecycle epoch |
| G | Identity disappears during observation without terminal evidence | UNKNOWN; request terminal/closure evidence, not absence inference |
| H | New writer admitted during window | Prior epoch invalid; active writer UNSATISFIED, otherwise UNKNOWN; recapture explicitly later |
| I | Lock appears after first snapshot | Stability/operation unresolved, UNKNOWN P3; existing P2 policy may refuse |
| J | HEAD or semantic index changes during window | UNKNOWN stable-window proof; preserve both observations |
| K | CGC parent dies, descendant survives | UNSATISFIED with current live evidence; incomplete coverage UNKNOWN; released flocks irrelevant |
| L | Registry terminal conflicts with same-instance current lifecycle evidence | CONTRADICTED coverage; UNKNOWN disputed claim, retain any independently proven active blocker |
| M | CGC subset empty but external writer coverage missing | PARTIAL/UNKNOWN action coverage, P3 UNKNOWN |
| N | Windows writer outside empty Linux view | General filesystem closure not satisfied; known relevant active evidence UNSATISFIED, Linux-only projection UNKNOWN |
| O | WSL restart after receipt | Old receipt STALE, current UNKNOWN; no replay of process handles |
| P | Two independent registered roots | Both and all descendants required; one live UNSATISFIED, one unobserved UNKNOWN, fully closed terminal set SATISFIED |
| Q | Unrelated-project writer | Exclude only with proven disjoint scope/aliases; otherwise UNKNOWN relevance |
| R | Writer domain outside requested action | OUTSIDE_REQUESTED_SCOPE only from enforced, validated domain separation; unsupported label UNKNOWN |
| S | Imported/missing producer provenance | UNKNOWN; serialized claims cannot authenticate lifecycle evidence |
| T | Coherent complete positive receipt | Strict validation accepts and recomputation yields scoped SATISFIED; no authority |
| U | Single coupled field or derived status forged | Validator rejects; no accepted receipt |
| V | Whole coupled evidence set coherently changes | Validator accepts; declared dependent full-projection claims change, unrelated claims stable |
| W | Malicious free text | Semantic result identical; text inert |
| X | Identical evidence / reordered nonsemantic enumeration | Identical canonical result; no hidden time, randomness or uncertainty compression |

E must include deterministic model PID reuse plus real retained-handle identity integration;
forcing OS PID exhaustion is unnecessary. C/D/K require actual surviving grandchildren in future
containment acceptance, not mocked parent-death flags. N is an explicit cross-OS coverage model;
no unrelated Windows repository needs mutation to demonstrate the missing observation domain.
A and T must remove one required proof at a time and lose SATISFIED. No current crash acceptance
is relabeled as acceptance of a containment primitive that it never tested.

## 11. Completion, limits and next dependency

COMPLETE: contract, finite/open-world distinction, conceptual receipt, bounds, process/host trust
boundaries, invalidation, dependency/tamper rules and 24 future acceptance cases.
PARTIAL: feasibility of positive production P3. A closed model is logically defined, but neither
filesystem exclusivity nor launch-bound nonescaping descendant coverage is accepted in current CGC.
NOT_STARTED: producer, environment/coordination layer, registry/gate runtime, schema, executor,
review/test evidence producers, recovery, benchmark and all V4 runtime. No prototype was needed.

Smallest next experiment: **validate launch-bound descendant containment and closed admission
feasibility in disposable Linux-native fixtures before implementing any production producer**.
Evaluate the cgroup-v2 candidate's availability, race-free admission and descendant non-escape
with bounded evidence; unavailable required capabilities must be reported, not installed or
bypassed. This experiment does not prove filesystem exclusivity and cannot produce real-project P3
SATISFIED. That independent closure obligation remains a gate for any later production profile.
No supervisor/service or current repository reconfiguration is implied by this next action.

Do not repeat accepted crash/verifier experiments or implement a general process scanner. Do not
start a producer simply to emit UNKNOWN under a new name. Do not mistake an empty CGC domain for
an exclusive workspace. Preserve current verifier behavior until an accepted new producer exists.

Future benchmark remains parked: fresh agent + git status/log + normal docs/simple handoff versus
same inputs plus CGC reconciliation/verifier evidence. Later measure wrong actions, duplicate
commands/tests, recovery time, tokens, human interventions, unsafe recovery and CGC overhead before
aggressive V4 runtime expansion. No results claimed. INTERNAL RIGOR MUST NOT BECOME EXTERNAL
COGNITIVE LOAD. THE PRODUCT IS HUMAN TIME RETURNED.
