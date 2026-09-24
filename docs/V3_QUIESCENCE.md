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

## 12. Windows-controlled Fedora containment feasibility — 2026-09-24

This is experimental evidence, not producer acceptance or a change to contract revision 1.
Starting clean Windows main: HEAD = origin/main = independently queried live main =
`9f5f11681e552fcc8e6aa978cf90dbe1def6b9b7`. One native Windows controller used
`wsl.exe -d FedoraLinux-44 -- ...`; no second Codex agent ran. No project runtime was imported.

**DERIVATION: containment PARTIAL; admission OPEN for the tested same-UID cgroup profile.**
The stronger claim that this profile prevents descendant escape is CONTRADICTED by a real
migration. Stronger namespace/privilege-separated combinations remain UNKNOWN, not impossible.
Real-project P3 remains UNKNOWN. **PRODUCTION QUIESCENCE PRODUCER = NOT_STARTED.**

### Environment and available capability evidence

OBSERVED_FACT from bounded commands, without installation/configuration changes:

- Windows WSL 2.7.14.0; FedoraLinux-44 is a WSL2 distribution. It was initially Stopped;
  the first Linux command started it. Windows version reported by WSL: 10.0.19045.7725.
- Kernel `6.18.33.2-microsoft-standard-WSL2`, x86_64; Python 3.14.7; UID/GID 1000.
  `/proc` stat field 22, PID namespace links and kernel boot identity were readable.
  Python `os.pidfd_open` and `signal.pidfd_send_signal` worked; polling a live self handle
  was not readable. No command-line/environment/credential collection or machine scan.
- `/tmp` reported tmpfs, not /mnt/c. The fixture was
  `/tmp/cgc-v3-quiescence-2wwpj3ua/experiment.py`, with private gate/JSON files beside it.
- cgroup2 mounted rw with nsdelegate. Root controllers: cpuset, cpu, io, memory, hugetlb,
  pids, rdma. Initial WSL command membership was root-owned `/init.scope`; its cgroup.procs
  was not writable by this user (UNAVAILABLE_CAPABILITY for direct unprivileged control there).
- Existing systemd user manager was active, reported degraded, with Delegate=yes at
  `/user.slice/user-1000.slice/user@1000.service`. Its directory and cgroup.procs were
  UID-1000-owned/writable; available/enabled subtree controllers were cpu, memory, pids.
  Degraded manager cause was not investigated; it did not prevent the tested transient scopes.
- `unshare` 2.41.5: both `--user --map-root-user true` and
  `--user --map-root-user --pid --fork true` exited 0. This proves namespace creation only;
  namespace escape denial, admission isolation and namespace-based empty proof NOT_EXECUTED.
  No mount/namespace policy, sysctl, controller setting or persistent service was changed.

An unprivileged `systemd-run --user --scope --quiet --unit=cgc-v3-quiescence-probe
-p Delegate=yes /usr/bin/cat /proc/self/cgroup` succeeded. The experiment used the same
foreground transient-scope mechanism with unit `cgc-v3-quiescence-experiment` and
`/usr/bin/python3 -B /tmp/cgc-v3-quiescence-2wwpj3ua/experiment.py`. These were temporary
scope objects in the existing manager, not installed/enabled services or a production supervisor.
Inside its own scope the harness created only two child cgroups, `domain` and `escape`;
`cgroup.type` was domain. It never migrated unrelated processes or wrote existing controller knobs.

### Fixture protocol and observed cases

One execution, exit 0. The controller was PID 570; it became a fixture-only subreaper for
cleanup/accounting. A forked direct root waited in a bounded trusted bootstrap gate. With
SIGCHLD default and no competing reaper, the parent retained a pidfd before release, recorded
start identity, moved only that child into domain, checked membership and released the workload.
This binds launch to the intended unreaped child; it is not atomic clone-into-cgroup support or
containment of arbitrary code running before the gate. Later named descendants stayed gated
while handles were acquired and start identities compared. These fixture rendezvous are an
oracle, not a production registry or proof of discovering every uncooperative short-lived child.

Each gate had a 12-second timeout, each worker a 20-second self-exit alarm, terminal waits five
seconds, and failure cleanup a 22-second owned-child drain. Normal cleanup released gates,
reaped only owned/adopted fixture children and removed the two empty cgroups. No kill was needed.
These are experimental bounds, not the future read-only producer's budget or signal behavior.

All rows below are OBSERVED_FACT, except the explicitly labeled model derivation in I.
Event names identify the captured command-output records; IDs are historical namespace-local
integers, never reusable handles. Boot identity was `4586e164-9a4c-4a05-9840-b06f8d53e63d`,
PID namespace `pid:[4026532219]`; start values are kernel ticks, not wall-clock timestamps.

| Case / output event | Traceable observation | Limit / implication |
|---|---|---|
| Root / launch-bound | Root 574, start 1242; retained live pidfd before gate release; start unchanged after admission | Stable current-launch handle, not portable identity after restart |
| A / A-direct | Root 574 and child 575 (start 1243) in domain; child PPID/PGID 574 | Direct child membership observed |
| B / B-F-J-multigeneration-detach | Child called setsid; grandchild 576 (start 1244), PPID 575; domain members 574/575/576 | Full three-generation fixture captured; no universal ancestry crawler |
| C / C-root-terminal-descendants-live | Root pidfd terminal; child and grandchild handles live; populated 1 | PARENT_DEATH != DESCENDANT_DEATH |
| D / D-exec | Grandchild exec into installed Python: PID 576, start 1244 and cgroup unchanged; retained pidfd still live | Process identity survives this exec; permitted executable policy is separate |
| E / E-reparent | Grandchild PPID became subreaper 570 after child exit; membership retained | Reparenting did not remove cgroup membership; old parent traversal loses ancestry |
| F / B-F-J-multigeneration-detach | Fork, setsid, second fork, original parents exit; grandchild PGID/SID 575, outside original group 574 | Detachment escapes original group/session, but alone did not escape cgroup |
| G / G-new-descendant | After observation began, grandchild forked late child 577 (start 1248); members changed [576] to [576,577] | Fork inherited membership; enumeration is not a complete lifecycle journal |
| H / H-empty-with-live-escape | After migration and late-child exit: domain populated 0, escape populated 1, grandchild pidfd live | Positive current cgroup emptiness is not empty launch-descendant universe |
| I / I-identity-model | Retained handles all terminal after reap; same integer with changed start or boot rejected by tuple comparison | DERIVATION: distinct model instances. Real integer PID reuse NOT_EXECUTED; no PID exhaustion |
| J / J-cgroup-escape | Grandchild wrote its own PID to fixture sibling escape/cgroup.procs; domain lost 576, escape contained 576, handle live | Escape succeeded and was detected for this known, gated instance; prevention contradicted |
| J / J-roundtrip | Grandchild migrated domain -> escape -> domain between endpoint samples while late child remained in domain | Fixture reports expose excursion; endpoint membership/populated checks cannot prove continuous non-escape |
| Admission / admission-bypass | Independent owned root 578 began outside domain, then self-migrated in after populated 0; populated became 1 | Same-UID ingress bypasses a coordinator-only launch registry/gate |
| Final / H-final-empty, cleanup | Both groups populated 0; 574/575/576/577/578 reaped with exit 0; all retained handles terminal; groups removed | Entire scripted finite fixture completed; no filesystem-writer or production closure proof |

A separate two-child handle probe exited 0: old child 550 was reaped; its retained pidfd was
readable and signal-0 probe returned ESRCH while new child 551's handle remained live and its
signal-0 probe succeeded. Both owned children were released/reaped. OBSERVED_FACT: old terminal
handle did not become the new live instance. Real same-integer reuse still NOT_EXECUTED.
Diagnostic start/boot/namespace/epoch tuples corroborate handles; tick granularity alone is not
an unconditional identity guarantee. No serialized descriptor integer is a restart capability.

### Candidate assessment and closed admission

The following capability judgments are DERIVATION from the observations above and the contract.
No accepted closed profile is established by this block.

| Candidate | Observes / tracks | Contains / prevents escape | Detects escape / proves empty |
|---|---|---|---|
| PPID traversal / registry | Sampled known relationships | No; reparenting breaks original ancestry | No complete escape detection or positive empty-domain proof |
| PGID / session | Current group membership | No; tested setsid detachment succeeds | Known change detectable; empty original group is insufficient |
| Start/boot/namespace tuple | Diagnostic instance correlation | No descendant containment | Different tuple rejects identity reuse; absence is not terminal proof |
| Retained launch pidfd | Bound instance lifecycle across tested exec/exit | Holds identity, not descendants | Terminal instance proof; cannot discover escaped/unregistered descendants |
| Delegated cgroup v2 | Kernel membership; fork/exec/reparenting accounting | Membership domain exists, but worker migration authority defeats confinement | Known migration detected; populated proves current subtree empty, not closed launch universe |
| Fixture subreaper | Adopts/reaps these orphan descendants | No admission or migration enforcement | Cleanup/lifecycle evidence only; not a CGC runtime promise |
| User/PID namespace | Creation available | Stronger composed restriction UNKNOWN here | Namespace-domain acceptance NOT_EXECUTED |

The kernel documents inherited fork membership and recursive live-process populated semantics;
pidfds provide instance lifetime observation subject to acquisition/reaping conditions. These
explain the scoped observations; neither primitive alone establishes the missing policy boundary.
Sources consulted: [kernel cgroup v2](https://docs.kernel.org/admin-guide/cgroup-v2.html),
[Linux pidfd_open](https://man7.org/linux/man-pages/man2/pidfd_open.2.html),
[Linux PID namespaces](https://man7.org/linux/man-pages/man7/pid_namespaces.7.html).

CLOSED_ADMISSION would require an enforced boundary, established before untrusted workload
execution, which denies unauthorized ingress and egress throughout a bound epoch, or supplies
complete trusted violation evidence. Fork inheritance must persist through detach/exec/reparent;
controller continuity and shutdown must be accounted for. Holding a Python gate or closing a
registration list cannot stop a same-UID process that can write migration interfaces. Enlarging
the domain to the entire user manager would include unrelated processes and still lack the
required launch-bound admission proof; that experiment was not performed.

Missing proof is **enforced separation of worker migration/admission authority from the trusted
controller**, not absence of pidfds, cgroup v2 or basic unprivileged namespaces. No inaccessible
kernel primitive was installed or bypassed. HYPOTHESIS: a carefully constrained namespace and
control-access profile may supply that separation without persistent configuration. This is not
accepted V3 truth; alternate access paths, same-UID peers, delegated IPC and controller death
need explicit analysis/acceptance. The current environment supports useful primitives, but
sufficient composed closure remains UNKNOWN. Continuous escape detection is also UNKNOWN for
unregistered/uncooperative descendants; the round-trip witness defeats endpoint-only inference.

### Side effects, cleanup, limits and next dependency

OBSERVED_FACT: the harness removed both cgroups and reaped its five workers normally. Both
temporary scope units later reported LoadState=not-found / ActiveState=inactive. The exact fixture
directory was already absent at the subsequent filesystem check (stat reported missing), so no
recursive deletion was issued. The reason for that disappearance is UNKNOWN; it is not evidence
that the harness deleted its files or that a kernel reboot occurred. A later boot-ID read matched
the experiment. Raw temporary files are not retained; the bounded command-output evidence above
is the durable curated record. No experimental script/log entered Git. Transient scope/WSL startup
may cause ordinary manager bookkeeping; no zero-host-write claim is made.

No packages, persistent settings, enabled services, Windows policy, WSL configuration, Git
configuration, unrelated processes/repos, credentials, quota reads or production modules changed.
No prior crash/verifier regression was repeated. Namespace restriction combinations, clone3 atomic
admission, threaded domains, hostile same-UID races, controller crash, offloaded/asynchronous work,
Windows writers and filesystem exclusivity were NOT_EXECUTED or remain UNKNOWN. The actual
repository is Windows-accessible by this controller; Linux-native fixture placement does not
prove exclusive access even to that fixture. PROCESS_CONTAINMENT != FILESYSTEM_EXCLUSIVITY.
LINUX_PROCESS_QUIESCENCE != FILESYSTEM_WRITER_QUIESCENCE. Nothing here changes real-project P3.

NEXT_EXACT_ACTION: **specify and audit the smallest disposable profile that separates worker
cgroup migration/admission authority from its controller, including namespace/alternate-interface
and same-UID ingress threats, before another containment experiment or production producer.**
Use these negative witnesses as requirements; do not repeat A–J merely to obtain a green result.
If no profile can be justified under existing unprivileged capabilities, record closure unavailable
under that scope. Filesystem exclusivity remains a separate unproven gate. No production runtime,
environment reconfiguration, recovery or V4 implementation is authorized by this next-action record.

## 13. Controller and worker authority-separation audit — 2026-09-24

**Decision D: CLOSURE UNAVAILABLE UNDER CURRENT UNPRIVILEGED SCOPE.** This is a DERIVATION
about the evidenced, authorized environment, not a theorem that every possible unprivileged
Linux isolation composition is impossible. No available candidate below establishes all required
properties. No minimal operational profile is selected; further combinations remain UNKNOWN.
The missing boundary is enforced exclusive control-plane authority, including exclusion of
external peers sharing the controller's underlying UID, not merely a different worker UID label.

Starting clean Windows main: local HEAD = origin/main = live main =
`6902579cbcde6aa3aa91b0aa75385404da7c5499`. This block is audit/specification only. No Fedora
command, capability probe, new scope, namespace, account, fixture or runtime test was executed.
Section 12 remains historical OBSERVED_FACT evidence; its egress, ingress and round-trip
counterexamples are preserved, not rerun. No new live Fedora availability claim is made.
The previously read foundation/mission/contracts remain unchanged; current evidence and scope
are reconciled against them. Windows Codex is the sole repository worker. A proposed Linux
TRUSTED_CONTROLLER is a separate process role, not another Codex agent or Windows visibility.

### Source-grounded premises and evidence limits

The following are documented mechanisms, not new Fedora acceptance results. Sources were
consulted on 2026-09-24; upstream documentation does not prove installed configuration parity.

- The kernel's [cgroup v2 delegation rules](https://docs.kernel.org/admin-guide/cgroup-v2.html#delegation-containment)
  require migration write authority at destination and common ancestor. Namespace delegation
  also constrains source/destination reachability in the writer's cgroup namespace. This is a
  real enforcement candidate, beyond pathname hiding; it does not confine an outside writer
  still acting from an ancestor namespace with sufficient permissions. Thread migration has
  its own domain constraints and must be considered separately.
- [User namespaces](https://man7.org/linux/man-pages/man7/user_namespaces.7.html) map IDs for
  permission checks; relabeling the caller as namespace root does not alone separate underlying
  file ownership. Capabilities are namespace-relative. A matching namespace-owner EUID in the
  parent has capabilities in the child namespace. Thus controller-owner peers cannot simply be
  assumed excluded by creating another user namespace. Different mapped host identities need
  evidenced mapping authority; no subordinate-ID allocation/helper policy was established here.
- [PID namespaces](https://man7.org/linux/man-pages/man7/pid_namespaces.7.html) affect PID views
  and namespace-init lifecycle. They are not a cgroup-file authorization mechanism. A host-side
  actor's control authority is not removed by a worker's restricted PID view.
- [systemd delegation](https://systemd.io/CGROUP_DELEGATION/) allocates subtree management to
  a delegate. It is not authentication of one process among every process using that user ID.
  The [upstream manager interface](https://raw.githubusercontent.com/systemd/systemd/main/man/org.freedesktop.systemd1.xml)
  includes transient-unit and process-attachment operations. Local availability/authorization
  of each operation is UNKNOWN; the earlier user-scope launch is the only relevant live evidence.
  Treat manager access as another control path requiring policy, not an assumed exploit or denial.
- [chmod](https://man7.org/linux/man-pages/man2/chmod.2.html) distinguishes ownership from
  process identity. Owner-only modes do not distinguish two unrestricted processes sharing that
  owner. [Open descriptors](https://man7.org/linux/man-pages/man2/open.2.html) and descriptor-relative
  access survive pathname changes; close-on-exec is not close-on-fork. A preopened cgroup FD may
  still face operation-specific kernel checks: neither universal bypass nor revocation is assumed.
- [No-new-privileges](https://man7.org/linux/man-pages/man2/PR_SET_NO_NEW_PRIVS.2const.html)
  constrains privilege gains through exec and is inherited. It does not revoke existing file
  authority or establish IPC isolation. It is a possible future requirement, not configured here.

Some freedesktop rendered manual URLs failed to load; systemd's project documentation/source
supplied the cited material instead. No undocumented Fedora helper behavior is inferred.

### Roles, trust and failure boundaries

All role restrictions below are SPECIFIED requirements, not implemented protections. The kernel
and correctly configured system manager are in the trusted computing base; malicious administrator
or kernel compromise is outside this model. Ordinary same-UID peers are explicitly inside it.

| Role | Allowed role / forbidden effect | Required evidence and assumption; UNKNOWN trigger |
|---|---|---|
| TRUSTED_CONTROLLER | Bind launches and domain; exclusively administer membership before capture; no new admission during protected capture | Retained instance/domain handles, kernel credentials, delegation and epoch provenance; correctness assumed, peer-injection resistance required; lost continuity invalidates proof |
| UNTRUSTED_OR_SEMI_TRUSTED_WORKER | Execute admitted fixture workload; must not alter membership/control policy or invoke a privileged deputy | Enforced credential/namespace/FD/IPC restrictions before release; cooperation is never evidence; uncovered route gives UNKNOWN |
| WORKER_DESCENDANT | Fork/exec only under inherited restrictions; cannot gain controller rights | Inheritance and executable-transition proof for complete subtree; unaccounted helper/transition invalidates coverage |
| EXTERNAL_SAME_UID_PEER | Continue unrelated work outside domain; may not enter, move workers or impersonate/inject into controller | Separately consider worker-UID peers and controller-UID peers; lack of enforced controller-peer distinction is the present blocker |
| EXTERNAL_OTHER_UID_PEER | Unrelated execution; no domain writes/delegated admission | Ownership, supplementary groups, ACL/capability and broker policy coverage; UID difference alone is insufficient |
| SYSTEM_MANAGER | Maintain specified boundary and lifecycle under fixed policy; not admit on arbitrary peer request | Independently administered delegation/API policy and generation binding; restart, policy change or ambiguous authorization gives UNKNOWN |
| KERNEL | Enforce accepted credentials/namespaces/domain and expose lifecycle evidence | Supported semantics/configuration assumed, observed boot/namespace identity required; change or unsupported layout invalidates continuity |

The controller must also be protected against peer changes to its executable/configuration and
where applicable ptrace, signal, descriptor or IPC access. These are control-plane integrity
requirements, not a new audit of project filesystem writers. Peer-caused controller death must
fail closed even if denial of service is not prevented. Existing trusted Python caller semantics
are unchanged; they do not become a same-UID isolation proof for a future Linux controller.

### Candidate comparison

All judgments are DERIVATION except availability explicitly attributed to section 12. 'Conditional'
means additional evidence/enforcement required, not SATISFIED. Continuity is UNKNOWN in every
candidate: no authority-separated controller lifetime/epoch has been accepted. Same-UID ingress
includes peers sharing the controller UID, not just the worker UID. No ranking by convenience.

| Profile | Authority separation | Self-egress prevention | Descendant-egress prevention | Same-UID ingress prevention | Alternate-interface coverage | Controller continuity | Available now | Proof status |
|---|---|---|---|---|---|---|---|---|
| A: same UID + delegated cgroup | Absent in tested profile | Contradicted | No general protection; grandchild escaped | Contradicted by owned peer | Round-trip gap witnessed | UNKNOWN | PROVEN_IN_EXISTING_EVIDENCE for primitive only | CONTRADICTED closure; admission OPEN |
| B: user namespace | Different namespace alone insufficient; mappings matter | UNKNOWN | UNKNOWN | Parent/controller-owner peer gap | UNKNOWN | UNKNOWN | Basic creation historically proven; separation UNKNOWN | UNKNOWN |
| C: PID namespace composition | Does not separate cgroup authorization | UNKNOWN | Visibility/lifecycle alone insufficient | Outside controller peer unaffected | UNKNOWN | UNKNOWN | Basic creation historically proven | UNKNOWN |
| D: distinct underlying worker UID/GID | SPECIFIABLE if mapping/launch authority supplied | Conditional on complete access denial | Conditional on inherited denial | Worker-peer case conditional; controller-peer gap remains | UNKNOWN | UNKNOWN | No accepted distinct-ID launch mechanism | REQUIRES_ENVIRONMENT_CHANGE for new provisioning; existing availability UNKNOWN |
| E: controller-owned delegated subtree | Same owner UID is not controller-process exclusivity | Contradicted for unchanged same-UID access | Same gap | Controller-peer gap remains | UNKNOWN | UNKNOWN | Delegation historically proven | CONTRADICTED as sufficient alone |
| F: namespace + distinct UID + cgroup | CONDITIONALLY_FEASIBLE component separation; not full profile | Conditional on enforced boundary | Conditional on inheritance | Needs independently enforced controller-peer exclusion | UNKNOWN | UNKNOWN | Full composition UNKNOWN | UNKNOWN; not selected |
| G: transient systemd scope/service | Scope lifetime is not identity separation; user service not automatically stronger | No denial proven | No denial proven | User-manager/delegation peer gap | Manager API policy UNKNOWN | UNKNOWN | User scope historically proven; service isolation untested | UNKNOWN; privileged policy would require separate scope |
| H: controller-created child with restricted access | Same-owner chmod/path hiding insufficient | UNKNOWN if composed; unchanged access contradicted | Same gap | Owner peers not distinguished | Inherited FDs/aliases/API unresolved | UNKNOWN | Child creation proven; asymmetric access not proven | CONTRADICTED as sufficient alone |

A cgroup namespace with nsdelegate deserves explicit consideration within B/F: a worker confined
to that namespace can face kernel migration reachability restrictions even if a pathname is known.
However, the external controller-UID peer remains outside that restriction. Neither a private
mount view nor a worker-only syscall restriction constrains that peer automatically. Restricting
all such peers would itself require an accepted environment-wide boundary, absent here.
No syscall-filter, LSM or broker composition is declared impossible; none is evidenced sufficiently
to select a minimal closed profile. Moving to the whole user subtree would change the finite
universe, include unrelated processes and still need admission closure; it is not a solution here.

Distinct UID means different underlying kernel credentials, with supplementary groups and relevant
capabilities accounted for, not simply different numbers displayed in namespaces. It would make
controller-owned control files potentially inaccessible to workers. It would also require a trusted
launch/credential transition and observation/teardown design across that boundary. New accounts,
subordinate-ID provisioning or privileged broker policy are REQUIRES_ENVIRONMENT_CHANGE if needed;
none is authorized or performed. Already-present mappings/helper authority remain UNKNOWN rather
than asserted absent. Even their discovery alone would not resolve the controller-UID peer gap.

### Threat and alternate-interface ledger

Every row is a proof obligation. 'UNKNOWN' describes unaccepted mitigation, not a newly observed
attack. The earlier migration counterexamples remain the only executed adversarial witnesses.

| Threat / interface class | Required boundary and falsifier | Present result |
|---|---|---|
| Worker self-migration via cgroup.procs | Deny every destination/ancestor route or enforce non-escape independently; any successful out-of-domain move falsifies closure | A contradicted; replacement UNKNOWN |
| Child/grandchild migration | Same denial must hold after fork, detach and reparent | Earlier grandchild escaped; inheritance of a new boundary UNKNOWN |
| Worker moving another worker or admitting peers | Audit authority of writer and target binding, not only who owns target PID; peer movement must not bypass controller | UNKNOWN mitigation; no assumption that self-only testing covers it |
| Same-UID ingress | Exclude both worker-UID and controller-UID outside peers throughout epoch | A OPEN; distinct worker UID alone leaves controller-peer gap |
| cgroup.threads / threaded layouts | Cover thread moves and layout-changing authority; initial candidate must refuse unsupported threaded topology | No threaded acceptance; UNKNOWN |
| Parent/sibling/delegated child interfaces | Account for cgroup.procs, threads, type, subtree controls, ownership/mode changes and further delegation | Parent/common-ancestor authority cannot be omitted; UNKNOWN replacement |
| Bind mounts / alternate paths / namespace views | Denial must follow effective authority across aliases; prevent namespace re-entry or newly exposed control views | PATH_DENIAL != CAPABILITY_DENIAL; UNKNOWN |
| Inherited or transferred descriptors | No writable control FD, ancestor dirfd, namespace FD or broker socket may reach untrusted code; inspect fixed allowlist before fork workload release, not only exec | UNKNOWN; later hiding/chmod cannot be assumed to revoke a handle |
| Controller /proc, ptrace, signal, FD access | Protect controller from impersonation/injection/capability theft; death must invalidate epoch | No hostile same-UID controller protection accepted |
| Exec | Bound executable/helper policy and credential/capability transitions; privilege gain or restored control route invalidates profile | Earlier identity continuity does not prove authority continuity |
| Fork / new namespaces | Descendants receive only allowed descriptors and restrictions; no inherited control authority or namespace escape route | Required inheritance proof UNKNOWN |
| Reparenting | Adoption must not transfer controller descriptors/authority; lifecycle accounting survives ancestry loss | Earlier membership survives; new authority model untested |
| systemd D-Bus / controller IPC | Only the bound authorized controller can request admission/policy changes; authenticate each operation and seal epoch against new requests | Installed per-method policy UNKNOWN; a unit name or same UID is not sufficient proof |
| Privileged helpers / delegated IPC | No migration deputy accessible through filesystem or abstract sockets, descriptor passing or permitted offload | Higher-authority helper availability/denial UNKNOWN; no credential/helper inventory performed |
| PATH / shell / systemd-run / sudo-like routes | Fixed launch policy, no uncontrolled interpreter/helper substitution, no inherited manager channel; existence is neither permission nor an exploit | Earlier systemd-run route known; other local routes UNKNOWN, not invoked |
| Controller death / manager restart | Invalidate epoch immediately; surviving workers remain possible; no fallback from missing observer to empty domain | Parent death evidence preserved; no cleanup guarantee or automatic recovery |

A closed design must account for preopened descriptors separately from reopening through an alias.
Kernel checks may reject a specific FD-mediated migration, but this requires exact documented and
accepted semantics, not an assumption that a hidden mount revoked access. Worker cooperation,
denying one pathname, and an empty registry cannot discharge any omitted row.

### Refined closed-admission predicate

CLOSED_ADMISSION_WITHIN_PROFILE is a proposed conceptual predicate, not a schema field or emitted
result. All fourteen obligations must be supported by fresh, bound evidence:

| ID | Required evidence |
|---|---|
| CA1 | Controller instance/credentials/control authority bound to current retained provenance |
| CA2 | Each admitted root bound to race-safe launch identity before untrusted execution |
| CA3 | Exact finite domain identity, supported topology and complete declared scope |
| CA4 | Worker self-egress prevented by enforced authority boundary |
| CA5 | Descendant egress prevented across fork/exec/detach/reparent transitions |
| CA6 | Unrelated worker-UID, controller-UID and other-UID peer ingress excluded |
| CA7 | Workers cannot admit/move peers through direct or deputy operations |
| CA8 | Alternate control paths, namespaces and broker interfaces excluded or accounted for |
| CA9 | Inherited/transferred descriptors, credentials and capabilities accounted for |
| CA10 | Controller and enforcing-manager continuity maintained throughout interval |
| CA11 | Violation/lost coverage invalidates affected claims immediately, without waiting for expiry |
| CA12 | Ordered start/end of a sealed admission epoch; all contributing observations inside it |
| CA13 | Claim-local freshness and dependencies; old evidence remains historical |
| CA14 | Current trusted provenance; serialized labels/digests cannot authenticate themselves |

Fork inheritance within an established domain can be an enforced admission path for descendants;
it is not permission for arbitrary external roots. Any such fork invalidates an earlier empty
claim and requires new observation. For the section-7 protected quiescence capture, admission
must remain closed and active/new writers cannot be promoted to quiescence. A known denied
attempt can be recorded without pretending the boundary failed; a successful forbidden transition
contradicts closure. Pure detection after escape does not satisfy CA4/CA5: it only invalidates
proof. No runtime watcher or guarantee of zero-latency physical detection is implemented here.

Failure rules: missing proof/observer continuity -> UNKNOWN; trustworthy prohibited ingress/egress
-> closure UNSATISFIED and coverage CONTRADICTED, with affected writer coverage UNKNOWN. These are
conceptual claim states, not new verifier enums or a blanket SAFE_TO_RESUME=NO. Real-project P3
is still UNKNOWN. For any later closed-domain experiment, teardown requires positive owned-instance
terminal evidence plus valid domain-empty/continuity evidence, then removal only of owned empty
objects. Controller death cannot authorize orphan killing, lock deletion or forced teardown.

### Decision, stopping boundary and next exact action

The smallest missing prerequisite is an independently enforced distinction between the admitted
controller and every untrusted actor able to wield its UID/control interfaces. Worker-only
namespacing, distinct worker UID, modes or a transient scope do not supply that distinction in
the evidence available here. This is why D is selected, rather than accepting a conditional
profile whose essential security boundary is merely assumed. No contradiction requires revising
the existing producer contract or V3/V4 missions; their missing-evidence rule already applies.

An owner-provisioned separate control identity, protected manager policy or other independently
enforced boundary could be considered in a separately authorized environment design. These are
alternatives requiring proof, not a selected minimal profile or instructions to create users,
enable services, reconfigure WSL or install tooling. An operator assertion that peers are absent
is insufficient. If provisioning is necessary, label it REQUIRES_ENVIRONMENT_CHANGE and stop
before execution. No filesystem-exclusivity or Windows-writer work is folded into this dependency.

Future falsification, only after that prerequisite is supplied and a profile is selected: use one
disposable domain, one controller-bound root/child and one outside peer representing each relevant
credential class. Challenge the claimed boundary through allowed interface classes, especially
an outside controller-UID peer, a retained control FD and a manager request during a sealed epoch.
Any successful prohibited admission/egress falsifies the profile; denial of one route is not full
acceptance. Controller death or authority-changing exec must invalidate proof as specified. Do not implement this now,
repeat A–J, or narrow away controller peers just to produce a positive result.

NEXT_EXACT_ACTION: **obtain an explicit owner decision and evidence for an independently enforced
Linux controller-control-plane boundary that excludes untrusted controller-UID peers, including
its delegation/manager IPC policy and any required environment change, before selecting a profile
or authorizing a new disposable experiment.** If that prerequisite is declined or unavailable,
retain CLOSURE UNAVAILABLE UNDER CURRENT SCOPE; no producer follows. This is the unresolved audit
dependency, not a new implementation roadmap or permission to change the environment.

Audit COMPLETE; process containment PARTIAL; tested admission OPEN; filesystem exclusivity UNKNOWN;
real-project P3 UNKNOWN. **PRODUCTION QUIESCENCE PRODUCER = NOT_STARTED.** V4 runtime NOT_STARTED.
PROCESS_CONTAINMENT != FILESYSTEM_EXCLUSIVITY; LINUX_PROCESS_QUIESCENCE != FILESYSTEM_WRITER_QUIESCENCE.
No source/schema/test/mission change, quota read, Fedora side effect or production behavior change.

## 14. Owner-approved protected broker boundary design — 2026-09-24

**Decision C: CONDITIONAL BOUNDARY SPECIFIED; ONE OR MORE CAPABILITIES REQUIRE PROOF.**
Selected design candidate: **ROOT_OWNED_BROKER_WITH_BOUND_CONTROLLER**, disposable Linux lab only.
This is a specification, not implemented containment, an accepted producer profile or production
authorization. Section 13's D remains correct for its earlier unprivileged scope. The owner has
now approved designing the independent boundary and planning its minimum environment changes:

```text
OWNER_DECISION = APPROVED
SEPARATE_LINUX_CONTROLLER_IDENTITY_DESIGN = APPROVED
CONTROLLED_ENVIRONMENT_CHANGE_PLANNING = APPROVED
```

Provenance: current explicit owner instruction, after independently verifying clean Windows main
at `23f953b1870870500c04e0a60e41fed007680374` against tracking and live remote. These durable labels
record that instruction; loading them later grants no action authority. Design approval does not
authorize privileged provisioning, production runtime or V4. Windows Codex remains sole project
worker; the Linux controller below is an experimental process, never another repository agent.

### Bounded read-only discovery

OBSERVED_FACT through Windows-originated `wsl.exe -d FedoraLinux-44 -- ...`, without elevation:

- Kernel 6.18.33.2-microsoft-standard-WSL2; systemd 259.8-1.fc44, system manager reported running;
  Python 3.14.7; python3, systemd-run and setpriv were present. No privileged manager method ran.
- Caller UID/GID 1000, supplementary groups 10/1000, initial-namespace identity UID/GID maps,
  membership `/init.scope`. Effective/permitted/inheritable/ambient capability masks zero;
  bounding mask nonzero. NoNewPrivs=0, Seccomp=0 in the discovery Python process. These values
  do not attest proposed workers, nor authorize privileged launch.
- `/sys/fs/cgroup` and `system.slice` were root-owned; their cgroup.procs files root:root 0644.
  This establishes particular metadata, not a complete ACL/alias/control-policy audit.
- `kernel.yama.ptrace_scope=0`; `fs.suid_dumpable=2`. Do not assume a globally restrictive
  same-UID ptrace policy. Neither value was changed.
- Reads of `/sys/fs/selinux/enforce` and `/sys/kernel/security/lsm` returned ENOENT. Active LSM
  protection is UNKNOWN, not proved absent by missing interfaces or present by +SELINUX build
  flags. This candidate does not depend on enabling SELinux or changing WSL/kernel settings.
- Current namespace links were readable (user 4026531837, PID 4026532221, mount 4026532218,
  cgroup 4026531835, IPC 4026532206, network 4026531833). They are invocation-local context;
  no old namespace/handle continuity is inferred from integer equality.

No account database, authentication files, sudo credentials, polkit configuration, process list
or environment dump was collected. No user, unit, cgroup, temporary file or namespace was created
by the discovery. WSL invocation may start Fedora and ordinary manager bookkeeping; no zero-host-
write claim. Earlier A–J and all accepted crash/verifier tests were not repeated.

### Selection and trust allocation

DERIVATION: keeping raw migration rights with root-owned enforcement, while granting a single
unprivileged controller only a narrow process-bound request channel, addresses the controller-UID
peer hole without claiming a UID uniquely identifies a process. A dedicated UID alone cannot do
that. The broker is required for this candidate; it is not claimed necessary for every Linux design.

Rejected as sufficient alone: user-manager delegation; a dedicated controller owning cgroup files;
PID/user namespaces; a root-running generic controller. A system service with only a dedicated
unprivileged UID still needs exclusive request authorization. An LSM process-domain solution may
be viable, but enforcement/configuration is unevidenced and would add policy dependencies here.
DynamicUser could avoid permanent account entries, but ID lifetime/reuse, cross-unit FD transfer
and worker launch coordination need a separate proof. It is not silently substituted into this
first design. This is a minimum selected mechanism set, not a proof of globally minimal setup cost.

| Component | Identity | Trust | Authority | Control interfaces | Inherited rights | Failure mode | Proof source |
|---|---|---|---|---|---|---|---|
| Windows Codex | Existing Windows operator | Sole repository worker | Documentation/Git and authorized lab orchestration only | wsl.exe, Git | No Linux root right inferred | Stop/reconcile repository evidence | Current owner scope and Git gate |
| System manager / authorized administrator | Linux UID/GID 0 | TCB | Establish exact transient root-owned lab unit and policy | System manager only | No worker delegation | Restart/policy change invalidates epoch | Installed manager observed; launch/policy acceptance pending |
| One-shot broker B | UID/GID 0; fixed reviewed image | Small privileged TCB | Own one subtree, launch fixed bootstrap, attach only own unreaped gated children, seal, observe, remove owned empty objects | Root-owned FDs; private controller channel | Never forwards raw control FDs | Death/protocol error -> UNKNOWN; no automatic restart | Specification plus future acceptance |
| Controller C | Dedicated nonroot UID_C/GID_C | Trusted fixed program | Request bounded operations on this broker's own domain | One inherited private connected socket | No raw cgroup/manager FD; no capabilities | Death/exec/injection gap invalidates epoch | Retained launch pidfd and per-message credentials, pending |
| Worker W | Dedicated nonroot UID_W/GID_W, different from C | Untrusted fixture | Execute reviewed bounded workload and fork within domain | Fixture data and narrow data-only gates | No controller channel or control FD | Forbidden transition contradicts closure | Credential/FD/syscall preflight and future negative tests |
| Descendants | W credentials/restrictions | Untrusted | In-domain fork/approved exec only | Same data-only interface set | Restrictions inherited | Lost coverage -> UNKNOWN | Future inheritance tests |
| Outside C/W/other-UID peers | No relevant administrative capabilities/grants | Untrusted | Unrelated execution; no raw control or authenticated broker operation | May attempt visible paths and public manager APIs | No valid C process identity | Denial of service may invalidate; cannot inherit authority | Future peer/IPC tests and policy evidence |

UID_C/GID_C and UID_W/GID_W are required distinct concrete values in the later manifest, not
numbers invented now. Resolve collision-free identities before provisioning; record exact values
and allocation provenance. Propose two dedicated locked, non-login lab accounts with no home,
supplementary groups, sudo/polkit grants, user-manager session or lingering. New account entries
are a reversible persistent change, not needed or created in this design block. Account exclusivity
is hygiene, not proof: an adversarial peer with UID_C is explicitly tested and remains in scope.

For C/W: real/effective/saved/fs IDs must agree with their manifest identity; supplementary groups
empty; effective/permitted/inheritable/ambient/bounding capabilities empty after bootstrap;
no_new_privs set. Keep C in the initial user namespace: a peer cannot gain capabilities over C
merely by becoming root in a child user namespace. W must not regain B/C credentials or escape
via helper/manager authority. B needs bootstrap credential transitions, cgroup access and owned
child observation; exact minimal retained capability/syscall set is proof gate R3, not a guessed
production hardening claim. Root administrative compromise remains outside the established TCB
model. An untrusted root-equivalent peer would invalidate that assumption; the design does not
solve it by calling it a nonroot controller peer. No generic root agent is authorized.

### Controller-UID peers and manager mediation

C does not own writable cgroup controls. Its authority is a broker channel tied to its retained
launch instance, not its UID. Propose a connected socketpair with message boundaries and kernel
per-message credentials; retain C unreaped for the channel lifetime and close/retire the channel
before reaping. Validate PID namespace, credential triple, exact bound PID/handle liveness, epoch,
monotonic request sequence and a fixed operation grammar. Never reopen a PID to restore authority.
Reject ancillary FDs from requests and truncated/missing credentials. SO_PEERCRED captured at
socketpair creation alone is insufficient to identify a subsequently forked child sender.

C must be nondumpable before any peer-injectable interval or authority release, with root-owned
immutable executable/configuration, no untrusted loader/PATH inputs, no post-seal exec and no
operation that reenables dumpability. Same-UID signals may still kill/stop it: availability is
not promised; B invalidates on terminal/timeout/channel failure. A stolen/duplicated endpoint
alone must not authenticate a different sender; attempted ptrace/proc-FD/pidfd_getfd access is
also part of acceptance. Socket credentials cannot prevent an already injected C from issuing
requests, so bootstrap integrity is a hard prerequisite, not optional defense in depth.

System-manager policy must deny C, W and all in-scope untrusted peers mutation of the lab and
indirect launch/attachment/delegation on its behalf, through every applicable unit/manager route.
No interactive authorization fallback or inherited bus socket. A user manager has no delegation
into this root-owned system subtree; its unrelated scopes cannot supply a writable common ancestor.
Unit name, same UID, a polkit action name or a successful read is not authorization proof. Exact
installed v259 methods, policy ordering, peer credentials and default permissions require R2.
Manager/admin configuration is trusted but must remain fixed throughout the epoch; no unnoticed
restart/reload/policy replacement is accepted. General control by another authorized administrator
invalidates the lab epoch; it cannot preserve an old positive receipt.

### Cgroup control and action boundary

One transient system-owned lab unit would delegate only to B/root, never to C/W. B uses private
control/worker children under that unit; only its worker child is the accepted process domain.
No threaded topology or worker-created subgroups. All files/directories remain root-owned with
no write ACL/group grant to C/W/peers. Do not modify global cgroup settings or unrelated siblings.
Reading public kernel metadata is harmless to authority; the profile does not require secrecy.

| Interface | Read | Write / move / delegate / topology authority |
|---|---|---|
| domain cgroup.procs | B; kernel-permitted observer reads allowed | B attaches only its own gated launch, before seal; no write/delegation to C/W/peers |
| cgroup.threads | B; ordinary permitted reads | No profile thread migration; no C/W/peer write; unsupported threaded layout refuses |
| cgroup.subtree_control / cgroup.type | B audits | Fixed supported domain layout; no in-epoch changes; C/W/peers denied |
| parent and control child | B/manager as appropriate | Manager owns unit boundary; B owns its private children, never permits worker escape into control child |
| siblings outside lab | Only bounded required metadata | No broker operation targets these; C/W/peer cannot obtain lab admission through them |
| delegated descendants | None in initial profile | No further delegation, topology creation or worker ownership |

In the table below 'B-only' means C can request a fixed operation, but only B performs it after
instance/state validation. 'TCB' is separately administered infrastructure, not worker authority.

| Action | Controller C | Worker | Descendant | Outside peer | System manager / B |
|---|---|---|---|---|---|
| Create domain | B-only, once before seal | Denied | Denied | Denied | Exact owned domain |
| Enter domain | B-only for prebound root | Bootstrap attach; then fork inheritance | Inherited birth only | Denied | No arbitrary PID attachment |
| Leave domain | No request operation | Denied | Denied | Cannot move workers | No live-worker egress operation |
| Move another process | No arbitrary PID API | Denied | Denied | Denied for lab | Only owned unreaped gated root before seal |
| Delegate child | Denied | Denied | Denied | Denied | Fixed setup only; no further delegation |
| Change topology | Denied after setup | Denied | Denied | Denied | Setup only; later change invalidates |
| Request manager operation | No privileged manager operation | Denied mutation | Denied mutation | Denied lab mutation | TCB launch/control with bound policy |
| Open control FD | Read-only observation if explicitly supplied | No writable FD | No writable FD | No writable FD | B owns writable FDs |
| Inherit control FD | Only bound broker socket, no raw FD | Denied | Denied | Denied | B bootstrap privately, close before untrusted release |
| Destroy domain | B-only after positive empty/terminal evidence | Denied | Denied | Denied | Exact owned empty objects only |

### Descriptor and namespace policy

Use an allowlist, not a filename denylist. B retains cgroup/ancestor directory FDs, root manager
connections, controller/worker pidfds and its endpoint. C receives only data output, a bootstrap
gate and its dedicated connected broker endpoint. W receives only explicit fixture data FDs and
data-only gate pipes, with no capability-bearing ancillary transfer. No cgroup, namespace, manager,
broker or unrelated pidfd crosses W's launch. Close all other FDs in the trusted child before
untrusted code; CLOEXEC at creation is additional protection, not a substitute for fork closure.
No writable control FD is made safe merely by later mount hiding. A deliberately injected FD
must cause pre-release refusal; if released, the profile is already violated even if one write fails.

| Namespace | Purpose / proof sought | Not provided / initial choice |
|---|---|---|
| User | None needed for selected credential separation | Keep initial mapping; deny worker creation/entry initially; no mapped-root shortcut |
| PID | None needed for launch pidfds/accounting | No new PID namespace; hiding PIDs would not remove raw/deputy authority |
| Cgroup | Optional later defense; not needed if raw write authority is denied | No new namespace initially; aliases must be safe by authorization, not concealment |
| Mount | Isolate minimal worker fixture view and hide manager/helper endpoints | Required for bounded helper surface if chosen at R4; root-only private nonpropagating setup; no filesystem-exclusivity claim |
| IPC | Not required if the fixed worker interface/syscall profile excludes offload | No automatic addition; SysV IPC/helper paths must be denied or explicitly covered |
| Network | Not required if networking/new sockets are denied and inherited channels exhausted | No new namespace initially; filesystem socket hiding alone does not cover abstract UNIX sockets |

The initial worker is purpose-built fixed fixture code, not arbitrary shell/Python/project code.
An explicit Linux syscall/FD plan must allow its required fork/wait/data I/O and approved exec
without granting new socket connections, namespace changes, credential changes or uncontrolled
helper offload. seccomp/no_new_privs is a candidate enforcement mechanism, not a tested filter;
R4 requires an exact syscall/architecture policy. Unexpected syscalls refuse, never broadening
the policy automatically. Controller likewise remains fixed, non-execing after authentication.
No generic test runner or Git execution is part of this lab.

### Launch sequence, races and sealed epoch

1. Authorized root launch validates an exact protected manifest/image, identities, policy and
   domain parent; creates one transient lab unit and B. No public broker listener, arbitrary
   argv/path/UID selection or shell. Root launch mechanism itself is R1, not assumed authorized.
2. B creates root-owned domain/control objects and retains their identities/handles. It launches
   trusted C bootstrap as its own child and acquires a pidfd without another reaper. C code and
   policy cannot be changed by UID_C. Drop supplementary groups and all credential/capability
   paths as specified; establish dumpability protection before accepting any control request.
3. Bootstrap race gate R3 must prove no interval permits a same-UID peer to inject into C between
   credential changes and nondumpability. Current suid_dumpable=2 is an observation, not this
   proof; credential changes/exec can reset the attribute. Refuse on a policy/configuration
   mismatch. Do not solve the race by silently treating UID_C peers as trusted.
4. B establishes the private instance-bound channel, accepts only the fixed readiness sequence
   and binds C to this epoch. Neither a caller-supplied PID nor channel possession alone suffices.
   No C fork/exec or transfer of authority is allowed after this binding.
5. B forks its own trusted, gated W bootstrap; retains an unreaped-child pidfd before migration.
   Only trusted bootstrap code executes before attachment. Bind it to the worker cgroup before
   workload release; close forbidden FDs, establish fixed credentials/restrictions and verify
   the configured boundary. A launch failure means no positive profile or blind retry.
6. ADMISSION_OPEN ends at B's serialized SEAL transition after validation and all prebound root
   admissions. B records ordered epoch start and irrevocably disables create/attach/delegate/
   topology mutations for that epoch. Pending requests are drained/refused by sequence before
   acknowledging seal. There is no UNSEAL/rebind operation; a new experiment requires a new domain.
7. Release the pre-admitted W root through its data gate. Descendant fork is the kernel-inherited
   admission path inside the domain, never external-root admission. Seal is not quiescence:
   workers may now be active; any previous empty observation is invalidated. A later quiescence
   capture still requires the separate contract's stable closed interval and filesystem proof.
8. End the valid epoch on explicit retirement, identity/policy/topology change, authority-changing
   exec, control-channel violation, controller/broker death, timeout or manager continuity loss.
   Detectable queued operations cannot revive a retired epoch. Observation/detection latency is
   not a lease for stale proof; every eventual consumer must independently check continuity.

Remaining races are explicit: credential/dumpability bootstrap; PID reaping/reuse; descriptor
leakage across fork/exec; manager-policy replacement; queued requests at seal; death between a
liveness check and dispatch; cgroup replacement/removal; ID reuse during teardown. B must serialize
state/requests, retain launch/domain identity and refuse uncertainty. Membership changes are
impossible through the protocol after seal, regardless of a concurrent controller death. Before
seal, any uncertain setup is invalid rather than an accepted partial epoch. No atomic whole-host
snapshot, crash-safe broker or zero-latency observer is claimed.

Approved fixed W exec must preserve restrictions/FD policy; identity preservation alone is not
authority preservation. Authority-changing or unreviewed exec invalidates coverage. Reparenting
does not confer B/C rights. Controller death revokes request authority; it does not terminate W
or transfer the channel to another UID_C process. No auto-restart/recovery. Teardown needs owned
terminal evidence and empty subtree under valid cleanup provenance; otherwise retain artifacts
for separately authorized review. No arbitrary kill, recursive host cleanup or Git-lock deletion.

### Minimum proposed changes and rollback

Nothing in this table was executed. Every later change needs a concrete manifest with exact names,
paths, IDs, pre-state digests and owner-scoped execution approval. Existing suitable resources may
be reused only after equivalent evidence; do not overwrite or delete an existing identity/policy.

| Change / classification | Purpose, scope and privilege | Persistence / rollback | Security impact; proof enabled / not enabled |
|---|---|---|---|
| Two dedicated C/W UID/GID assignments: NEW_IDENTITY_REQUIRED; REVERSIBLE_PERSISTENT_CHANGE if new accounts | Root provisions only manifest-named non-login identities, empty groups/no grants; concrete numbers collision-checked | Account entries persist; retire only after every owned process/FD/IPC/artifact is resolved, never immediate numeric reuse; remove only newly created accounts | Removes default interactive/wheel identity exposure; does not distinguish a C peer by itself |
| Protected lab files: TEMPORARY_CHANGE | Root-owned private Linux-native lab directory, reviewed B/C/bootstrap/fixture and manifest; no real project mounted | Remove only exact owned paths after safe teardown; retain failure evidence privately if needed | Prevents image/config substitution; does not prove runtime correctness |
| One foreground transient system unit: TEMPORARY_CHANGE; NEW_SERVICE_REQUIRED for this lab instance only | Authorized system manager launches root B, delegates only its subtree to root; no enablement/install/autorestart | Unit disappears after controlled completion; inspect descendants before stop/removal; no blind systemctl stop that kills unknown survivors | Provides managed root-owned parent; not caller authorization or automatic closure |
| Exact manager mutation-denial policy if existing policy cannot prove it: PRIVILEGED_CONFIGURATION_CHANGE; REVERSIBLE_PERSISTENT_CHANGE | Narrow C/W/in-scope peer denial for lab and privileged proxy routes; verify installed policy precedence; no broad allow rule | Record original state; remove only new rule or restore exact owned edit after no active epoch; policy drift invalidates all epochs | Blocks manager bypass; not a claim that all helpers are covered |
| Private mount/bootstrap FD/syscall/credential restrictions: TEMPORARY_CHANGE | B sets restrictions only in owned future lab children; no global sysctl/mount change | Die with owned processes; restore no global settings; cleanup only owned mount/domain objects | Closes specified direct/deputy paths; exact filter and launch race still require proof |
| Existing kernel/systemd/Python tooling: NO_CHANGE_REQUIRED for design | Read-only evidence sufficient to plan, not execute | Nothing to roll back | No package, WSL, Windows policy or kernel change proposed |

No persistent broker daemon, installed listener, sudo grant, new global delegation or production
service is proposed. Root-owned file access and B's credential-transition privilege increase risk;
keep B's operation grammar closed: CREATE_OWN_DOMAIN, ATTACH_OWN_GATED_CHILD, SEAL, QUERY, and
REMOVE_OWN_EMPTY_DOMAIN. Launch is a fixed bootstrap operation specified by root-reviewed manifest,
not arbitrary shell execution. Query is bounded and redacted. No raw PID attach, arbitrary path,
user management, Git, network, arbitrary filesystem write, arbitrary kill or policy-edit RPC.
The administrator provisions; B cannot provision accounts or manager rules. Exact implementation
review must demonstrate these restrictions before a privileged experimental run is approved.

### Outstanding proof gates and next falsification block

| Gate | Required evidence before accepting the boundary |
|---|---|
| R1 | Exact authorized root launch, protected manifest and concrete noncolliding C/W identities; current root access is NOT_VERIFIED and was not exercised |
| R2 | Installed system-manager method/policy authorization, no C/W/controller-peer bypass, fixed unit/delegation lifetime; no assumption from upstream docs alone |
| R3 | Bootstrap integrity with current dumpability rules, nondumpable C, launch pidfds, per-message sender binding, minimal B privilege; no injectable same-UID interval |
| R4 | Exact worker/controller descriptor and syscall/helper policy, namespace necessity, aliases and capability transitions; purpose-built fixture only |
| R5 | Seal serialization, queued-request rejection, death/restart invalidation and cleanup/UID-reuse discipline |
| R6 | Bounded independent negative-test observations for every required CA1–CA14 dependency, including raw and deputy interfaces |

Future experiment design (NOT_EXECUTED): one domain, one B/C pair, one W root and one descendant,
plus bounded adversarial peers with UID_W and UID_C (not dismissed because accounts are dedicated).
Challenge self/descendant egress and peer ingress through procs/threads/ancestor/sibling aliases;
attempt a retained raw-FD launch and require refusal before release; separately test direct write
semantics without promoting that deliberately violated setup. Try duplicate channel access,
wrong-sender messages, ptrace/proc-FD access and manager attachment/transient-unit requests without
interactive approval. Exercise approved versus authority-changing exec, fork inheritance, stale
requests across seal, C death and B/manager continuity loss. Same-UID signals may cause UNKNOWN,
never transferred authority. Any accepted forbidden migration or broker request falsifies the
profile; failure to collect trustworthy evidence also prevents acceptance. Normal-path success
alone is insufficient. Bound fixtures and recovery/retention plan before launch; no A–J rerun.

Primary references consulted: [Linux UNIX credentials](https://man7.org/linux/man-pages/man7/unix.7.html)
for per-message versus connection-time credentials; [dumpability](https://man7.org/linux/man-pages/man2/PR_SET_DUMPABLE.2const.html)
and [ptrace access checks](https://man7.org/linux/man-pages/man2/ptrace.2.html) for the injection gate;
[cgroup delegation](https://docs.kernel.org/admin-guide/cgroup-v2.html#delegation-containment),
[systemd delegation](https://systemd.io/CGROUP_DELEGATION/),
[v259 manager API](https://raw.githubusercontent.com/systemd/systemd/v259/man/org.freedesktop.systemd1.xml)
and [v259 execution policy](https://raw.githubusercontent.com/systemd/systemd/v259/man/systemd.exec.xml).
[No-new-privileges](https://man7.org/linux/man-pages/man2/PR_SET_NO_NEW_PRIVS.2const.html) and
[seccomp](https://man7.org/linux/man-pages/man2/seccomp.2.html) inform future restrictions. These
document mechanism semantics, not completed Fedora proof or current operational permission.

NEXT_EXACT_ACTION: **prepare and review the exact disposable-lab manifest and minimal fixed
broker/controller/bootstrap design for R1–R5, resolving concrete identity allocation, privileged
launch, manager policy and the same-UID bootstrap race before requesting scoped execution of the
R6 falsification experiment.** Owner design/change-planning approval is already recorded; do not
ask for it again. Actual privileged changes and the experiment require their exact bounded scope,
not a repeat of the broad authority audit. No implementation of a production producer follows.

Current process containment PARTIAL; previous same-UID admission OPEN; candidate boundary unproven.
Filesystem exclusivity UNKNOWN; real-project P3 UNKNOWN. PRODUCTION QUIESCENCE PRODUCER = NOT_STARTED.
V4 runtime NOT_STARTED. PROCESS_CONTAINMENT != FILESYSTEM_EXCLUSIVITY. Stop after this design block.

## 15. Disposable lab manifest and R1–R5 review — 2026-09-24

**Decision B: R1R5 MANIFEST PARTIAL; SPECIFIC CAPABILITY EVIDENCE STILL REQUIRED.**
This section narrows section 14 into a reviewable future lab contract, not a runnable approval.
All MUST/denied entries below are DESIGN requirements, not observations of enforcement.
No provisioning, image implementation, privileged launch or R6 execution occurred. Owner design
and environment-change planning approval remains recorded. No repeat approval for design is needed.

Starting clean Windows main independently matched tracking/live main at
`5c9b6254a0e96731e45152e0dde9fffd3879be75`. Windows Codex remains sole project worker.
Fedora discovery originated only through wsl.exe; no second agent or repository controller.

### Evidence and explicit blockers

OBSERVED_FACT: a bounded unprivileged Python subprocess probe read suid_dumpable=2 and
ptrace_scope=0 again. System-bus Manager introspection exited 0 and exposed StartTransientUnit
(signature ssa(sv)a(sa(sv))), AttachProcessesToUnit (ssau), SetUnitProperties (sba(sv)), GetUnit,
GetUnitByPIDFD, Subscribe, StopUnit, Reload and Reexecute. No mutating method was called.
pkaction returned implicit any/inactive=auth_admin and active=auth_admin_keep for manage-units,
manage-unit-files and reload-daemon. This reports advertised defaults, not effective caller
authorization: custom rules, cached authorizations and alternate privileged deputies remain UNKNOWN.
No authentication challenge was requested. Ordinary D-Bus/WSL activation/bookkeeping is possible.

| Blocker | Exact missing evidence / resolution gate |
|---|---|
| M1 | Root launch executor and explicit future execution scope; collision-free account allocation with NSS, service/session and namespace review; no root route tried |
| M2 | Installed effective system-manager/polkit/deputy policy, including attachment and unit-object aliases; defaults and introspection are insufficient |
| M3 | Reviewed native image/build identity and uninterrupted credential/dumpability transition; current-value observations do not prove invariant stability |
| M4 | Compiled per-role seccomp/FD policy and exact ABI behavior, bounded peer harness and resource limits; no executable artifact exists yet |
| M5 | Installed unit death/cleanup behavior and manager continuity evidence, including reexec that can preserve PID; no restart test performed |

R6 is blocked until these have explicit evidence or a reviewed, scoped prerequisite test.
Do not improvise missing values during execution. Unsupported prerequisites refuse before launch.

### Exact symbolic manifest

Manifest revision `CGC_LAB_R1R5_1`; inert design, no production schema. Expressions below are
deterministic substitutions, never shell expansion. Reject unknown fields, duplicate keys,
symlinks, existing objects and unresolved required values. One invocation runs exactly one T case.

| Field | Exact value or resolution rule |
|---|---|
| LAB_ID | `cgcq-` plus 32 lowercase hexadecimal characters from fresh 128-bit OS randomness; exclusive creation must also succeed |
| BROKER_ID / CONTROLLER_ID / WORKER_ID | B / C / W |
| UID_B / GID_B | 0 / 0 in initial Linux user namespace; empty supplementary groups |
| C account / W account | `cgcqc_` / `cgcqw_` plus first 12 hex characters of LAB_ID suffix; collision refuses this LAB_ID |
| UID_C / GID_C | Same unused numeric value selected by allocation rule below; no reservation claimed now |
| UID_W / GID_W | Next distinct unused value under the same rule |
| BROKER_UNIT | `LAB_ID.service`, system manager, system.slice |
| CONTROLLER_UNIT | NONE: C is B's child in the same unit; no user manager or second service |
| CGROUP_PARENT | `/sys/fs/cgroup/system.slice/LAB_ID.service`; prepend `/sys/fs/cgroup` to manager ControlGroup and require exact equality |
| WORKER_DOMAIN / CGROUP_DOMAIN | `workers` / `CGROUP_PARENT/workers` |
| Control / adversary children | `CGROUP_PARENT/control` and `CGROUP_PARENT/peers`; peers are outside the accepted workers domain |
| LAB_ROOT | `/run/cgc-quiescence/LAB_ID`; Linux-native, root-owned 0700, all ancestors verified |
| MANIFEST_PATH | `LAB_ROOT/manifest.json`, root:root 0600, at most 64 KiB |
| Executable | `LAB_ROOT/bin/cgc-lab`, root:root 0500, single reviewed static native x86-64 ELF, no interpreter/dynamic loader/file capabilities/set-ID bits |
| STATE_DIRECTORY | `LAB_ROOT/state`, root:root 0700; only events.jsonl, observations.jsonl and cleanup.json, each root:root 0600 and at most 1 MiB |
| BROKER_SOCKET / CONTROLLER_CHANNEL | B endpoint / C endpoint of one unnamed AF_UNIX SOCK_SEQPACKET socketpair; no bind/listen/path/abstract socket |
| OBSERVATION_EPOCH | Bound tuple below; generated in memory, no receipt reanimation |
| Test selector / bounds | One enum T1–T14; at most 16 lab tasks, 64 FDs per process, 10 seconds per protocol phase, 120 seconds overall |
| Build/policy bindings | Exact SHA256 of image, manifest bytes and reviewed filter description; unit properties and policy evidence digest; all UNRESOLVED until review |

Numeric allocation: future administrator supplies a reviewed permitted allocation interval from
local account policy; absent interval BLOCKS. Under an exclusive provisioning transaction select
the lowest two IDs unused as UID or GID in complete configured NSS, local/subordinate mappings,
active process credentials and allocated lab reservations. Repeat collision checks at creation;
no fallback to a guessed conventional number. Incomplete NSS enumeration blocks. Accounts must
be locked, non-login, no home, no supplementary groups, grants, user-manager sessions or lingering.
Review only relevant metadata; never collect password/authentication material.

Before launch, bounded privileged preflight checks all real/effective/saved/fs IDs for these two
values, active sessions and service use, plus subordinate mappings. Record counts and identities
only for matching lab IDs. Existing unrelated use aborts; never take ownership of it. Preserve an
allocation ledger until cleanup is independently established. Concurrent administrator allocation
is a trusted-control-plane assumption requiring an exclusive provisioning window. One-time absence
is not lasting isolation: deliberately introduced UID_C/UID_W peers remain adversaries. Unexpected
later use invalidates the epoch, never permits killing the new process.

### R1 launch and minimal trusted image

Future requester: human-authorized Windows operator. Executor: separately authenticated Linux
administrator UID 0 over a specifically approved WSL invocation; current WSL root capability is
NOT_VERIFIED. There is no sudo grant, unprivileged launch RPC or controller-supplied command string.

The administrator uses the system Manager StartTransientUnit with mode `fail`, empty auxiliary
units, exact BROKER_UNIT and one ExecStart vector:
`[LAB_ROOT/bin/cgc-lab, "--manifest", MANIFEST_PATH]`. No other arguments or executable are accepted.
No shell or PATH search. Root provisions and verifies image/manifest before this request; B checks
the same bytes/ownership from no-follow handles before use. Bind device/inode/mount identity,
digest and manager InvocationID; path or hash alone grants no authority. Root control-plane
immutability during the run is an explicit TCB assumption; arbitrary hostile root is out of scope.

Proposed typed unit properties: Type=exec, User=0, Group=0, SupplementaryGroups empty,
Slice=system.slice, Delegate=yes to root only, Restart=no, ExitType=cgroup, KillMode=process,
SendSIGKILL=no, SendSIGHUP=no, WatchdogUSec=0, RuntimeMaxUSec=infinity, LimitCORE=0,
LimitNOFILE=64, TasksMax=16, UMask=0077; no ExecStop/ExecStopPost, socket activation,
FileDescriptorStore, PAMName, EnvironmentFile or automatic cleanup hook. Installed acceptance of
these properties and TasksMax controller availability is M5/M4, not assumed. No unit stop while
survivors exist. KillMode=process deliberately avoids automatic descendant cleanup in this lab;
it is not a general service recommendation. OOM or host shutdown always invalidates evidence.

Launch environment: empty application environment except LANG=C and LC_ALL=C; no HOME, PATH,
loader variables or manager-exported application settings. A fixed root bootstrap clears extras
before any C/W branch; manager identity is captured separately. Exact environment filtering by
the approved launcher/unit is M1, not a promise that systemd supplies no implicit variables.
cwd=/; umask=0077. Image and manifest directories must not be writable by C/W or their groups.

Use one reviewed native image: B forks fixed in-image C/W branches without post-drop exec.
No generic plugin, Python interpreter, shell, dlopen, user-selected function or script. C/W
real/effective/saved/fs UID/GID become their exact IDs, groups empty, all capability sets including
bounding/ambient empty, no_new_privs=1. Proposed B bootstrap capability bound is SETUID, SETGID,
SETPCAP and SYS_PTRACE only; root ownership supplies cgroup DAC access. SYS_PTRACE is solely for
owned-child proc/FD verification, not a ptrace/injection RPC. No SYS_ADMIN, DAC_OVERRIDE or KILL.
Whether these suffice with installed LSM/proc policy is M3; do not add capabilities automatically.
After all children/gates are verified, B drops SETUID/SETGID/SETPCAP; after seal B retains at most
SYS_PTRACE for bounded observation. B itself remains root TCB with a fixed syscall/operation set;
this proposal does not claim an implemented sandbox against a compromised root broker.

### R2 manager authorization contract

| Operation/interface | Expected authorized caller | Expected denied caller | Evidence and lifetime |
|---|---|---|---|
| StartTransientUnit exact lab unit | Approved administrator only, once | B/C/W/descendants and untrusted outside peers | Exact property readback, installed authorization review; no interactive fallback |
| GetUnit, GetUnitByPIDFD, Properties.Get, Subscribe | Administrator observer/B where needed | No secrecy requirement for metadata | Bind manager bus owner, unit InvocationID, ControlGroup and B instance; reads confer no mutation right |
| AttachProcessesToUnit / service AttachProcesses | NONE for lab workflow | C/W/peers and B protocol | Existing method observed; effective denial must be proved; B uses owned cgroup FDs instead |
| SetUnitProperties, unit Start/Stop/Restart, bind-mount/mount-image routes | Admin setup or empty-unit final retirement only | C/W/peers | manage-units policy plus installed method/deputy audit |
| Unit-file changes, environment changes, Reload/Reexecute | No in-epoch authorized operation | All lab principals/untrusted peers | manage-unit-files, set-environment, reload-daemon and aliases reviewed; any actual change invalidates |

System manager owns parent and unit lifecycle. B owns fixed child topology and C/W lifecycle;
the user manager has no role/delegation here. No runtime policy editing by B. Advertised auth_admin
defaults are not a deny proof, particularly with active-session cached grants. If existing effective
policy cannot prove denial, M2 requires a separately reviewed deny rule for the dedicated identities
covering all systemd mutation actions, not just one unit name. Exact rule location/order/content
cannot safely be invented without inspecting applicable rules. That rule is conditional future
configuration, not installed. All other in-scope peers must lack equivalent administrative/deputy
grants; an untrusted root-equivalent principal invalidates the TCB assumption.

Policy lifetime starts before bootstrap and extends through cleanup. Snapshot plus endpoint
comparison cannot prove continuous non-change: accept only a controlled administrator window
with no concurrent policy mutation, monitored manager continuity, and no evidence loss.
Unobservable continuity is UNKNOWN. Manager restart/reexec/reload requires a new lab generation.

### R3 bootstrap state machine and race analysis

B is single-threaded and sets PR_SET_CHILD_SUBREAPER before any lab fork for owned descendant
adoption/reaping; this is fixture accounting, not escape prevention. Failed adoption/accounting
invalidates cleanup evidence. SIGCHLD is not ignored, no SA_NOCLDWAIT and no other child reaper. B retains
each child unreaped until its channel is retired. Fork then pidfd_open of that owned child can
bind a live/zombie instance under those conditions; failure refuses, not a PID-number fallback.
No controller or worker code runs from writable storage.

| State / transition | Required action | Atomicity / race treatment |
|---|---|---|
| C0 CREATED | Trusted fork branch inherited root credentials; B root image already nondumpable | Fork kernel event, no user-code atomicity across following calls |
| C1 INSTANCE_BOUND | B retains pidfd, boot/start identity, namespace, unit and generation; child waits on private gate | Parent/child handshake; early exit retained as zombie, never accepted |
| C2 PROTECTED | Child PR_SET_DUMPABLE(0), core limit 0; no exec thereafter | Individual prctl is a syscall, not an atomic bootstrap transaction |
| C3 FDS_CLOSED | Child closes B manager/cgroup/log/other endpoint FDs and all non-allowlisted descriptors | Sequential close/remap; root trusted bootstrap only, no peer authority released |
| C4 CREDENTIALS_DROPPED | setgroups(empty), drop bounding/ambient sets while privileged, setresgid, setresuid, clear remaining caps, set no_new_privs | Credential-changing calls can reset dumpability; require invariant below at each step |
| C5 VERIFIED | Immediately set dumpable 0 again; verify all IDs/groups/caps, initial namespaces and FD inventory | B inspection plus fixed bootstrap self-check; any gap/failed inspection aborts |
| C6 CHANNEL_BOUND | Install C filter; send fixed READY with kernel credentials and nonce; B validates exact instance | No reliance on SO_PEERCRED's socketpair creator; no authority before validation |
| C7 POLICY_SEALED | B verifies domain/control layout, C liveness and policy; serializes seal after W preflight | Multiple observations are not atomic; missing protected-window evidence blocks |
| C8 RELEASE_ALLOWED | Only B sends W release byte after SEAL acknowledgement | Already admitted root only; no post-seal attach; C never gets W gate write end |

DERIVATION / CONDITIONAL race argument: until final UID transition, a capability-free UID_C peer
does not match root credentials. At credential transitions the observed suid_dumpable=2 would
reset dumpability to a value other than 1; documented ptrace access checks reject such a target
without CAP_SYS_PTRACE in its user namespace. An explicit dumpable=0 follows, and no C exec can
reset it later. This removes the assumed need for a new global ptrace sysctl, **if** the reviewed
sequence, kernel behavior, lack of prior tracer and stable sysctl/TCB window are established.
A prior tracer, suid_dumpable=1, unexpected credential path, executable replacement, syscall failure
or post-drop exec blocks release. Values read before/after are not proof against privileged
mid-transition changes. R3 remains unaccepted; no same-UID racing experiment ran.

W follows the same trusted no-exec bootstrap, additionally gated until membership and filter
verification. Reparenting confers no rights. C is not permitted to fork, exec, change credentials,
reenable dumpability or receive FDs after READY. Same-UID signals can deny service; they do not
authenticate a replacement C. No availability guarantee or automatic orphan killer is added.

### Live-instance/channel binding and fixed grammar

B creates socketpair(AF_UNIX, SOCK_SEQPACKET|SOCK_CLOEXEC, 0), enables SO_PASSCRED before READY,
and never binds/listens. No filesystem socket ownership or abstract namespace authentication.
Each privileged request requires exactly one SCM_CREDENTIALS matching C's fixed real UID/GID
and PID in B's PID namespace, retained unreaped pidfd nonterminal, expected namespace/unit,
no executable transition, current generation/state and next sequence. B and C have no capability
to be lent to a peer; a forged/stolen endpoint must still fail sender checks. A root forger is TCB
compromise, not solved by SCM_CREDENTIALS. SO_PEERCRED is diagnostic only.

Protocol v1: one packet at most 1024 bytes, UTF-8 JSON containing exactly the seven tuple keys
listed below, uppercase as written. Canonical encoding sorts keys lexically, uses no whitespace,
BOM, escapes or trailing newline. Values are ASCII strings except REQUEST_SEQUENCE, an unsigned
decimal JSON integer (no leading zero, sign, exponent or fraction). Reject duplicate keys before
canonical comparison, nesting, nulls and any extra field. No paths, argv, raw PIDs or numeric FDs.
Generation/DOMAIN_ID values are 32 lowercase hex characters; LAB_ID follows its manifest rule;
SEAL_EPOCH is the string "0" before seal, otherwise 32 lowercase hex characters. DOMAIN_ID is
an opaque random identifier mapped to retained kernel handles in B, never a serialized FD.
READY is a distinct fixed bootstrap packet with exactly NONCE (32 lowercase hex characters),
TYPE ("READY") and VERSION (integer 1), same canonical rules; accepted once before normal requests.
Replies echo the full validated tuple with exactly RESULT (OK or INVALIDATED); a SEAL OK reply
uses the newly allocated epoch. No arbitrary error text. Decoder/filter implementation proof is M4.
Tuple fields: LAB_ID, BROKER_GENERATION (fresh 128 bits), CONTROLLER_GENERATION (fresh 128 bits),
DOMAIN_ID (B-owned handle identity plus fresh generation), SEAL_EPOCH (0 before seal, fresh
128 bits at seal), REQUEST_SEQUENCE (unsigned 64-bit starting 1), OP (five enums).
C inherits the immutable initial tuple from B's pre-fork memory; B allocates DOMAIN_ID as an
empty launch slot before CREATE, then binds it to kernel handles without changing that ID.
C contributes a fresh 128-bit READY nonce; B binds it to its launch generation. Nonces and
serialized start times are correlation, not authentication. Sequence wrap refuses.

recvmsg must detect MSG_TRUNC/MSG_CTRUNC; reject unknown ancillary types, duplicate credentials,
SCM_RIGHTS and extra fields. Close all unexpectedly received FDs before invalidation to avoid
leaks. No FDs in replies. Every request revalidates sender and lifecycle; no connection-level
authorization cache. Any wrong generation/sender/malformed privileged packet retires the channel
and invalidates proof. No retry, reconnect, inherited session or replay after restart.

| OP | Input / caller | Preconditions | Effect / postcondition | Failure / audit |
|---|---|---|---|---|
| CREATE_OWN_DOMAIN | Tuple only; bound C | BOOTSTRAPPING, no domain yet; protected parent verified | B creates exact workers child using parent FD, records identity; one creation | Any preexisting object or partial error INVALIDATED; owned-object ledger before/after |
| ATTACH_OWN_GATED_CHILD | Tuple only; bound C | OPEN_FOR_CONTROLLED_ADMISSION; fixed W launch slot, own unreaped child, gate closed | B writes only its bound W PID to exact domain cgroup.procs; checks membership/handle | No arbitrary PID accepted; lost identity/mismatch INVALIDATED; launch and readback evidence |
| SEAL | Tuple only; bound C | All R1–R5 preconditions, W gate closed; one root bound | Serialized irreversible state change; retire epoch 0 and allocate seal epoch; no topology/attach afterward | Queued epoch-0 packet invalidates if received later; log sequence barrier and ACK |
| QUERY | Tuple only; bound C | Valid current state/generation | B bounded read of owned handles/events; no migration | Lost continuity INVALIDATED; log observations separately from derivations |
| REMOVE_OWN_EMPTY_DOMAIN | Tuple only; bound C | TEARDOWN, W subtree proven empty, owned launch/descendant accounting terminal | Remove exact empty workers child; verify disappearance of retained object, never recursive removal | EBUSY/identity mismatch retains artifacts; no kill/retry sweep |

CREATE follows B's setup of its own control/peers children and relocation of B into control;
C inherits control membership, which B verifies. Gated W starts there, then B attaches it to
workers. Test peers are attached to peers before credential drop. No resource controller is
enabled by B; manager-provided TasksMax availability is checked separately. C/W no delegation.
B enters TEARDOWN internally only after the fixed test completes and all W/peer launch evidence
is terminal with empty domains, or after separately authorized invalidated-state review.
Final C exit and empty peers removal are fixed B shutdown housekeeping after protocol retirement,
not extra RPCs. B cannot remove its own occupied control cgroup: the administrator removes that
exact child only after B is terminal and the child is independently observed empty.
After C death, no new controller may use REMOVE: cleanup becomes a separately approved admin task.
ARBITRARY_EXEC, ARBITRARY_ATTACH_PID, ARBITRARY_KILL, ARBITRARY_CGROUP_PATH, ARBITRARY_FILE_WRITE,
USER_MANAGEMENT, POLICY_EDIT, GIT_OPERATION, NETWORK_PROXY and SHELL are forbidden grammar.

### R4 descriptor and syscall policy

| Release FD / class | C | W and descendants | B / bootstrap treatment |
|---|---|---|---|
| 0 | Read-only /dev/null | Read-only /dev/null | Open as root, verify device, no tty |
| 1 / 2 | Data-only output pipes to B | Data-only output pipes to B | B reads bounded framed bytes; never interprets output as operations |
| 3 | C endpoint of private broker socket | W read end of release pipe; EOF is abort, one fixed byte permits run | Never give W a write end or C endpoint; close W FD 3 after release |
| 4 and above | NONE | NONE | B retains own cgroup/dir/pidfd/bus/log handles, never crosses release |
| cgroup/dir/proc/namespace/pidfd | NEVER | NEVER | Child closes before entering C/W logic |
| manager/D-Bus/broker-B socket | NEVER | NEVER | B-only; all socketpair opposite ends closed in children |
| memfd/shm/received SCM_RIGHTS | NONE | NONE | No pass-through, no hidden loader descriptor |
| unused pipe ends / other child FDs | NONE | NONE | Close before each child leaves root bootstrap; all newly created B FDs CLOEXEC |

B cannot close every authority FD before fork because it needs them; root bootstrap necessarily
inherits some briefly and must close them before credential handoff/untrusted code. Each later
fork re-audits inherited ends. W descendants inherit only 0–2 after release. CLOEXEC supplements,
but does not replace, this closure. No subsequent exec in this minimal profile. B verifies FD
inventory before release; a supplied raw FD makes setup invalid even if later writes would fail.

Minimal initial profile uses preloaded native code and no pathname access after release. This
narrows section 14's optional approved exec: **all post-bootstrap C/W exec is denied**. It does not
claim arbitrary project workloads are covered. Direct migration attempts by W first encounter
syscall/FD denial; separate unrestricted UID peers must also challenge underlying DAC/manager
authorization, so syscall denial is never presented as proof of the latter.

| Category | C | W/descendants | Reason / unresolved detail |
|---|---|---|---|
| read/write/close, poll/ppoll, clock_gettime, exit/exit_group, necessary signal return | MUST_ALLOW on fixed descriptors/arguments | MUST_ALLOW on fixed descriptors/arguments | Exact native ABI/filter compile and signal behavior M4 |
| fork / wait4 | MUST_DENY fork; no children | MUST_ALLOW native fork and wait4 only | No clone flags; task ceiling independently enforced; descendants same filter |
| clone/clone3/vfork | MUST_DENY | MUST_DENY | No namespace/thread variants; libc fallback must not widen filter |
| setuid/setgid/setres*/setfs*/setgroups, capset, privilege-changing prctl | MUST_DENY after bootstrap | MUST_DENY after bootstrap | no_new_privs and empty caps additionally required |
| unshare/setns/mount/pivot_root/chroot | MUST_DENY | MUST_DENY | Namespace aliases cannot be newly created |
| ptrace/process_vm_*/pidfd_getfd | MUST_DENY | MUST_DENY | Outside UID_C peers independently challenge C nondumpability |
| open/openat/openat2/creat, handle-based opens | MUST_DENY | MUST_DENY | No pathname authority; inherited FD audit remains necessary |
| socket/connect/bind/listen/accept/socketpair | MUST_DENY | MUST_DENY | No new manager/helper/abstract socket route |
| sendmsg/recvmsg | MUST_ALLOW only FD 3, fixed protocol | MUST_DENY | Seccomp cannot inspect ancillary buffers; B validates C messages |
| execve/execveat | MUST_DENY | MUST_DENY | T11 is expected refusal, not successful safe exec evidence |
| dup*/fcntl FD duplication, ioctl, memfd_create, shm*, keyctl/add_key/request_key, bpf, io_uring*, perf_event_open, userfaultfd | MUST_DENY | MUST_DENY | Eliminate unreviewed FD/async/helper paths |
| Memory allocation/runtime startup syscalls | UNKNOWN_PENDING_EXPERIMENT | UNKNOWN_PENDING_EXPERIMENT | Prefer preallocation; exact compiled image may require bounded additions before approval |
| Any unlisted syscall or ABI (including x32/compat) | MUST_DENY | MUST_DENY | Default EPERM; reject wrong architecture; never auto-allow after failure |

NOT_RELEVANT applies only to a proven absent image dependency; no helper class is dismissed just
because the fixture does not normally use it. B has a distinct reviewed syscall set for bootstrap,
cgroup operations and observation; its compiled policy is also M4. Seccomp is not a pathname
authorization engine and cannot alone prove manager policy, root TCB integrity or filesystem
exclusivity. No cooperative self-report substitutes for installed filter evidence.

| Namespace | Choice | R1–R5 purpose / limit |
|---|---|---|
| USER | NOT_NEEDED; initial mapping required | Credential/DAC separation; no nested mapped-root path |
| PID | NOT_NEEDED | Retained launch handles; same PID view for credential checks |
| MOUNT | NOT_NEEDED for this no-open/no-exec profile | Avoid mount privilege; outside peers still attack existing aliases |
| CGROUP | NOT_NEEDED | Authorization, not hidden topology, supplies proposed boundary |
| IPC | NOT_NEEDED | SysV/shared-memory/helper syscalls denied |
| NETWORK | NOT_NEEDED | No new sockets; inherited endpoints exhausted by allowlist |
| UTS | NOT_NEEDED | Hostname isolation proves no relevant authority property |

### Control-interface ledger

All entries are future R6 obligations. Denial errno may be EPERM/EACCES or a precisely recorded
manager authorization error; an unexplained failure/timeout is UNKNOWN, not accepted denial.

| Path class | Authorized actor | Denied actor / expected failure | Evidence required |
|---|---|---|---|
| cgroup.procs / cgroup.threads | B own pre-seal procs attach only | W/descendants/peers denied; no threads moves | Syscall result, source/destination identity and membership |
| Ancestors / siblings / delegated children | Manager or B exact setup only | No lab migration or new delegation by peers | Ownership/ACL/common-ancestor checks plus independent peer attempts |
| Manager IPC / transient-unit APIs / unit-object aliases | Admin exact launch only | C/W/peers no mutation/deputy launch | Installed policy and method result, no prompt/cached grant acceptance |
| Broker socket / controller socket | Same unnamed pair, bound C only | Wrong sender/generation invalidates | Per-message credentials, retained instance, state transition |
| Retained raw FD / proc-fd aliases | B only | Pre-release leak refuses; peer acquisition denied | FD inventory, ptrace/proc access result, no release after leak |
| Namespace aliases / existing bind mounts | Admin TCB only | Alias cannot grant C/W/peers write authority | Same object permission evidence; W namespace calls denied |
| Descriptor transfer | No operational receiver except C credential channel | SCM_RIGHTS rejected/closed; W recvmsg denied | Ancillary flags/FD cleanup and unchanged membership |
| Helper/deputy | No worker-accessible control deputy | No manager/session/sudo/helper bypass | Exact installed routes review M2/M4; absent evidence blocks |

### R5 states, generations and death

Legal success path:
UNINITIALIZED -> PROVISIONED -> BOOTSTRAPPING -> OPEN_FOR_CONTROLLED_ADMISSION ->
SEALING -> SEALED -> QUIESCENCE_OBSERVATION -> TEARDOWN -> CLOSED.
SEALED -> TEARDOWN is permitted without any quiescence claim. Observation begins only after
release and verified worker-domain empty transition within intact authority/continuity.
Any nonterminal state -> INVALIDATED. INVALIDATED -> TEARDOWN needs independently established
cleanup authority/provenance, never renewed proof. No backward edge, unseal, same-generation
restart, second create/attach or CLOSED reuse. Invalid setup can reach teardown without release.

One B event loop owns request dispatch and state. SEAL is the local linearization point;
all earlier accepted mutations complete and verify before it. C waits for each ACK, never pipelines.
Epoch-0 queued packets cannot execute after seal. SEAL reply binds the new epoch; subsequent
sequence remains increasing. Post-seal CREATE/ATTACH, duplicate sequence, old generation or
topology mismatch rejects and invalidates rather than returning a harmless success.
Sealing changes protocol authority, not kernel permissions by magic: the R2–R4 boundary must
already exclude alternate writers. An empty label or file cannot certify that exclusion.

| Event | Exact consequence / required evidence |
|---|---|
| C terminal pidfd, channel EOF/error, timeout | B marks INVALIDATED, closes request channel, never reopens admission; W may continue; no automatic freeze/kill |
| B death | All proof invalid; C must cease requests on EOF/timeout; domain/C/W can survive; manager is not a replacement B |
| Manager bus-owner loss, Reloading, reexec/restart, policy change or missed observation interval | Invalidate regardless of same PID, unit name or boot ID; no silent rebind; continuity coverage itself M5 |
| WSL shutdown/restart or boot-ID change | Retire all generations/FD numbers; stored receipts historical only; WSL restart can share kernel boot identity, so boot ID equality alone never restores authority |
| Worker unexpected exit, syscall denial, budget exhaustion | Record exact result; invalidation where required evidence is lost; never infer whole-domain empty from root death |
| Domain removal/recreation or changed mount/inode binding | Invalidate; identical pathname cannot restore domain identity |

No post-death queue may revive authority. Death between liveness check and dispatch is an explicit
race: before seal it leaves invalid setup; after seal no membership mutation is legal at all.
No zero-latency death detector or atomic whole-host proof is claimed. Every consumer must validate
current continuity rather than trust a historical SEALED label.

Cleanup order: retire proof and requests; verify lab ledger/handles/credentials; wait boundedly
for the fixed cooperative fixture to terminate; record unresolved survivors; verify empty owned
worker/peer domains plus terminal launch accounting; remove exact empty children; C exits after
channel retirement; B closes handles and exits; administrator confirms unit subtree empty before
StopUnit/collection. Only then remove exact new policy/files and retire new accounts/reservations.
No recursive cgroup deletion, generic lock deletion, borrowed PID kill, or immediate UID reuse.
Timeout leaves a retained FAILED/UNKNOWN lab requiring separately scoped survivor handling.
After B death a fresh admin review must reconstruct provenance; logs alone cannot authorize
cleanup. No automatic account/file deletion on unit failure. Log retention is bounded and private.

### Future environment changes

Nothing below was executed; root already exists, so no broker account or socket service is needed.

| CHANGE_ID | Object / change | Privilege / persistence | Purpose / proof enabled | Rollback | Risk | Required for R6 |
|---|---|---|---|---|---|---|
| LAB-C1 | Dedicated C UID/GID, locked non-login account | Root; NEW_IDENTITY_REQUIRED, reversible persistent | Distinct credential class | Retire only new account after complete provenance/termination | Reuse, grants, concurrent allocation | Yes, or proven equivalent reserved identity |
| LAB-C2 | Dedicated W UID/GID, same restrictions | Root; NEW_IDENTITY_REQUIRED, reversible persistent | Worker/descendant credentials | Same conservative retirement | Unrelated UID reuse | Yes |
| LAB-C3 | LAB_ROOT/bin and exact manifest/image | Root; temporary Linux-native files | Immutable fixed launch binding | Remove only manifest-owned files after teardown | Root code/build integrity | Yes |
| LAB-C4 | One transient BROKER_UNIT and three child cgroups | System manager/root; temporary NEW_SERVICE_REQUIRED | Root-owned control plane, owned domain and peers | Empty-only retirement; never enable/install | Privileged bootstrap and surviving children | Yes |
| LAB-C5 | Exact deny rule only if existing effective policy insufficient | Root; conditional privileged persistent configuration | Exclude manager deputy bypass | Restore only attributable rule after epochs retired | Policy precedence/collateral denial | Conditional, M2 unresolved |
| LAB-C6 | STATE_DIRECTORY, pipes, unnamed pair, private handles | B/root; temporary | Bound evidence and request channel | Close endpoints, bounded private log retention, exact file removal | FD leakage, stale generation | Yes |

No LAB-C7 socket path/ownership rule is needed: there is no listener. No namespace, global
sysctl, WSL configuration, package installation or persistent broker daemon is proposed.
Compiled image availability is M3/M4; lack of a toolchain cannot authorize installing one.

### R1–R5 acceptance matrix

'Yes' in SPECIFIED means the required behavior is defined; it does not mean executable acceptance.

| Gate | SPECIFIED | SUPPORTED_BY_DOCUMENTATION | CURRENT_ENVIRONMENT_EVIDENCE | REQUIRES_ENVIRONMENT_CHANGE | REQUIRES_R6_TEST | BLOCKED |
|---|---|---|---|---|---|---|
| R1 identity + launch | Symbolic contract/allocation; numeric/build fields unresolved | Manager launch / pidfd semantics | Existing system manager; root route not tried | C1–C4/C6 | Yes | M1, M3 |
| R2 manager policy | Required actors/method classes/lifetime | v259 API security model | Methods and advertised defaults only | C5 conditional | Yes, T7/T8 and aliases | M2 |
| R3 bootstrap integrity | Ordered no-exec state machine and conditional race argument | dumpability/ptrace/credentials/pidfd | suid_dumpable=2, ptrace_scope=0; sequence untested | C1–C4 | Yes, hostile UID_C race | M3 |
| R4 restrictions/interfaces | FD allowlist and syscall categories; compiled filters absent | seccomp/no_new_privs/UNIX credentials | Installed support from earlier discovery, not filters | C3/C6 | Yes | M4 |
| R5 sealing/lifecycle | Legal transitions, generations, death/cleanup | systemd lifetime and pidfd semantics | Manager methods only; no death/continuity tests | C4/C6 | Yes, T10/T12/T13 | M5 |

### R6 pre-authorization test manifest — NOT_EXECUTED

One fresh LAB_ID/generation per T case, serialized cases, at most B+C+W+one W descendant+two
bounded peer processes plus administrative observer; ceiling 16 includes any helper. No interactive
authentication, package install, generic hostile shell or unrestricted workload. Under the exact
admin-reviewed test manifest, B's root bootstrap creates the predeclared peers in peers child,
then drops each to UID_C/UID_W; peers retain no
root rights. They are intentionally less syscall-restricted where needed to challenge external
authorization, and are never counted as contained workers. Exact peer code/filter is M4.

Common evidence E: actor launch pidfd/credentials, exact target object, attempted syscall or
method/result, membership before/after, B protocol state/sequence, terminal handles and owned
cleanup ledger. Endpoint sampling alone cannot rule out transient escape; prevention-policy
evidence and explicit syscall outcome are both required. Common cleanup K: fixed actor exits,
bounded waits, conservative cleanup order above; unresolved survivor retains lab and blocks next
case. Every unexpected allowed forbidden action falsifies its claim, even if later restored.

| Test | Setup / actor / exact action | Expected denial or invalidation | Evidence / cleanup / falsification |
|---|---|---|---|
| T1 | Sealed W attempts open/write of sibling control cgroup.procs for self PID | open denied by W filter; no FD to bypass | E/K; successful migration falsifies egress; syscall refusal alone not DAC proof |
| T2 | W forks one child; child repeats T1 | Same inherited denial | E/K plus child credentials/filter; changed membership falsifies inheritance |
| T3 | External UID_W peer opens workers/procs and threads, attempts self-attach | DAC/delegation denial, no admission | E/K; any ingress falsifies independent peer exclusion |
| T4 | External UID_C peer repeats T3; attempts C ptrace/proc-FD acquisition during bootstrap and after READY | Denied or C death/UNKNOWN; never authority transfer | E/K; injected C or writable control access falsifies boundary |
| T5 | Trusted test setup inserts one writable sibling control FD into W bootstrap inventory | Refusal BEFORE W release | E/K and gate still closed; release with FD falsifies launch contract, regardless of write result |
| T6 | External peers address same cgroup via existing mount aliases and proc-fd paths; W attempts unshare/setns | Alias no extra authority; W calls denied | E/K; inaccessible alias NOT_EXECUTED rather than assumed covered; alias migration falsifies |
| T7 | External peers call AttachProcessesToUnit and service AttachProcesses for own PID into workers | Authorization denied without prompt | E/K plus exact D-Bus result; attach success falsifies R2 |
| T8 | External peers request a transient unit executing the fixed lab image or SetUnitProperties on lab | Denied; no new unit/process | E/K plus unit absence, not just client error; accepted mutation falsifies R2 |
| T9 | Deliberately supplied duplicate C endpoint to UID_C peer sends valid-looking tuple | Per-message wrong PID rejects and invalidates | E/K; peer operation accepted falsifies instance authentication |
| T10 | C test branch queues epoch-0 attach behind SEAL, then duplicate/current malformed sequence | Never executes post-seal; INVALIDATED | E/K, ordering and membership; any late effect falsifies serialization |
| T11 | W attempts execve/execveat of fixed reviewed test target, including authority-changing form if safely available | EPERM by filter, no exec; no new authority | E/K; actual post-release exec falsifies this no-exec profile; no set-ID file provisioning implicit |
| T12 | Fixed C test branch exits after seal while W remains alive | B INVALIDATED; admission stays sealed; W survival allowed | E/K, terminal C handle; replacement authority/positive proof falsifies death semantics |
| T13 | Fixed B test branch exits after seal | All proof invalid; no restart; C/W may survive | Independent admin E/K; no manager auto-kill assumption; resumed generation falsifies |
| T14 | C test branch sends SCM_RIGHTS on channel; W attempts recvmsg/descriptor transfer | B closes received FDs, invalidates; W denied | E/K plus FD inventory; usable transferred authority/accepted request falsifies |

T4 must exercise the credential-transition window; testing only settled nondumpability does not
close M3. Test-only branches are fixed image/manifest enums, never new operational RPCs. Deliberate
leaks in T5/T9 are adversarial setups, not accepted profile states. Installed manager/WSL restart
is NOT authorized even by this test table; continuity-loss injection can test refusal logic, but
actual restart semantics remain UNKNOWN until separately scoped. No R6 execution approval is
requested now while M1–M5 remain unresolved.

### Sources, disposition and next exact action

Primary mechanism references: [dumpability](https://man7.org/linux/man-pages/man2/PR_SET_DUMPABLE.2const.html),
[ptrace access checks](https://man7.org/linux/man-pages/man2/ptrace.2.html),
[pidfd acquisition](https://man7.org/linux/man-pages/man2/pidfd_open.2.html),
[UNIX credentials](https://man7.org/linux/man-pages/man7/unix.7.html),
[seccomp](https://man7.org/linux/man-pages/man2/seccomp.2.html),
[no_new_privs](https://www.kernel.org/doc/html/latest/userspace-api/no_new_privs.html),
[v259 manager API](https://raw.githubusercontent.com/systemd/systemd/v259/man/org.freedesktop.systemd1.xml),
[v259 service lifetime](https://raw.githubusercontent.com/systemd/systemd/v259/man/systemd.service.xml)
and [v259 kill policy](https://raw.githubusercontent.com/systemd/systemd/v259/man/systemd.kill.xml).
Rendered systemd manual fetches returned 403; upstream v259 source was available. These references
support mechanism reasoning, never installed-policy acceptance or proof of a new executable.

Design review complete for this block; manifest PARTIAL as executable handoff. Do not resolve
missing image/policy/identity fields by engineer invention. NEXT_EXACT_ACTION: **resolve M1–M5
with a concrete identity/launch preflight plan, installed effective manager-policy review and
reviewable native bootstrap/filter/protocol artifact specification; validate the no-exec
credential sequence and unit survivor behavior before requesting scoped R6 execution.**
If a necessary observation needs privilege, list its exact read-only scope for approval rather
than executing it under this design authorization. No production or broad provisioning follows.

Historical containment PARTIAL and same-UID admission OPEN unchanged. Filesystem exclusivity
UNKNOWN; real-project P3 UNKNOWN. PRODUCTION QUIESCENCE PRODUCER = NOT_STARTED; V4 runtime
NOT_STARTED. DESIGN_COMPLETE != PROOF_COMPLETE. BROKER_DEATH != DOMAIN_TEARDOWN.

## 16. M1–M5 installed evidence and native contract — 2026-09-24

**Decision C: M1M5 PARTIAL; NATIVE ARTIFACT / FILTER / PROTOCOL DESIGN STILL INCOMPLETE.**
Starting clean Windows main independently matched tracking/live main at
`2f763a0da8ba29a08a2d641058386d5ef78d7130`. Windows Codex remained sole worker.
This block performed unprivileged metadata reads and two bounded analogues, not R6 or provisioning.
Owner design approval remains unchanged. The mechanical
[native ABI companion](V3_QUIESCENCE_LAB_ABI.md) is the sole new document; it avoids embedding
another long syscall/FD/wire specification in this already lengthy evidence chain.

### M1 identity preflight and launch

OBSERVED_FACT: Fedora caller UID 1000, x86_64. /etc/nsswitch.conf selects `files systemd`
for passwd and `files [SUCCESS=merge] systemd` for group. Therefore local account files alone
are incomplete identity evidence. Configured ordinary UID/GID range is 1000–60000, system range
201–999. No local passwd/group names matched cgcqc_/cgcqw_. No identities were allocated.
Subuid/subgid each had one range, 524288–589823; names were not collected. Current UID/GID maps
were identity mappings 0..4294967294. /var/lib/systemd/linger contained zero entries; this does
not prove absence of sessions/services or future lingering.

Installed nss-systemd can resolve manager-backed identities; DynamicUser support is a design
route available in systemd, not a currently allocated CGC account. No DynamicUser unit was created.
The selected profile retains dedicated accounts because it needs explicit lifecycle/peer tests.

Exact allocation algorithm (future privileged preflight, no account mutation in this block):

1. Validate manifest LAB_ID/name syntax and obtain an administrator-approved interval within
   observed system range 201–999. No fallback to ordinary or DynamicUser ranges. If exhausted,
   REFUSE_IDENTITY_ALLOCATION; owner must choose a new scoped policy, not install/change one here.
2. ALLOCATE_C_IDENTITY scans ascending candidates. For each, resolve both names and numeric IDs
   through getpwnam_r/getpwuid_r/getgrnam_r/getgrgid_r against **all configured NSS sources**;
   record only collision booleans. NSS timeout/unavailable/incomplete source -> refuse.
3. Check candidate against local UID/GID records, subordinate ranges, manager dynamic identities,
   active process real/effective/saved/fs IDs, active service User/Group/SupplementaryGroups,
   login/session/linger state and reservation ledger. Unreadable coverage -> refuse.
4. Require no supplemental/admin membership or sudo/polkit grant; specifically exclude wheel
   and empower, not only numeric primary group. Check namespace mappings exposing candidate.
5. Under a single administrator-controlled provisioning window, reserve the selected UID=GID
   pair in the lab ledger. ALLOCATE_W_IDENTITY repeats with C pair excluded. Return candidates
   plus snapshot/coverage provenance; **not yet collision-free allocated identities**.
6. Recheck immediately before actual account creation, then verify locked/non-login/no-home/
   empty groups/no session/no lingering and new NSS resolution. No check can exclude concurrent
   privileged modification without the explicit TCB window. Unrelated use never authorizes cleanup.

M1 is PARTIALLY_RESOLVED_WITH_EXACT_REMAINING_GATE. Readable ranges and NSS are known; active
ownership, complete policy grants and root executor are not. No sudo, su, root WSL invocation
or authentication challenge ran. Prefix absence is a point-in-time fact, not reservation.

Future executor is exactly a separately approved administrator invoking the **system**
org.freedesktop.systemd1.Manager.StartTransientUnit, not a user manager or B RPC. The root route
would be Windows wsl.exe with explicit -d FedoraLinux-44 -u root and one reviewed native launch
client, no shell; that route is NOT_TRIED and not authorized to execute by this block.
The launch client is a separate administrative artifact, not a new generic operation in cgc-lab.

Review record: name=LAB_ID.service, mode=fail, aux=[], ExecStart signature a(sasb) containing
one (absolute LAB_ROOT/bin/cgc-lab, [same path,"--manifest",MANIFEST_PATH], false);
User/Group strings "0", SupplementaryGroups empty string array, Environment=["LANG=C","LC_ALL=C"],
WorkingDirectory="/", Type="exec", Restart="no", ExitType="cgroup", KillMode="process",
SendSIGKILL=false, SendSIGHUP=false, Delegate=true, Slice="system.slice", TasksMax uint64=16,
LimitNOFILE/LimitNOFILESoft uint64=64, LimitCORE/LimitCORESoft uint64=0, UMask uint32=63,
WatchdogUSec uint64=0 and RuntimeMaxUSec uint64=max. No ExecStop or inherited application FDs.
Exact handling of manager-injected environment and capability property encoding remains artifact
review, not hidden launch discretion. Store image/source/manifest digests and full typed property
list in approval record. Fresh readback must match InvocationID (observed, never invented),
ControlGroup=/system.slice/LAB_ID.service and MainPID bound to a live pidfd plus start identity.
Failure before binding refuses all subsequent lab operations. Same PID alone is insufficient.

### M2 installed policy and deputy review

OBSERVED_FACT: systemd 259.8-1.fc44; polkit 127-2.fc44.2. Relevant installed action XML advertised
auth_admin for any/inactive, auth_admin_keep for active for manage-units, manage-unit-files,
set-environment and reload-daemon. D-Bus systemd policy allows transport of mutation methods
to manager/service/scope interfaces; authorization is still evaluated by the destination.
Installed action digest: 05b867df07111f0693828fce4db65e6d14d653244952f7a598f4a4b600164d3b.
Installed systemd bus policy digest: 42529cc9b571a23e0e28ec96c7855bb8c2ccb277e626c3dd305bc5b5bd485af5.

The vendor rules directory contained seven active .rules plus one .rules.example. Relevant
observations: 50-default.rules identifies wheel as administrator group; empower.rules grants all
actions to empower members. Other readable vendor rules targeted specific unrelated services;
their presence does not prove absence of further deputies. /etc/dbus-1/system.d was empty.
Reading /etc/polkit-1/rules.d failed with PermissionError. No elevation or workaround followed.
No raw rules, unrelated account list or security-policy contents are committed; only these
scope-relevant findings and digests. Active rules can override advertised defaults.

| ROUTE | EXISTS | CALLER AUTH MODEL | CAN MUTATE LAB | EFFECTIVE POLICY KNOWN? | R6 MUST ATTACK? / STATUS |
|---|---|---|---|---|---|
| systemctl / systemd-run | Yes | Caller bus credentials + manager checks | If authorized | No | Yes, API equivalent; frontend not extra authority by itself |
| System Manager/Service/Scope D-Bus | Yes | Transport allows calls; manager/polkit decides | Attach, transient units, properties, stop/restart, unit files, environment | Partial installed evidence | Yes T7/T8 and aliases |
| PolicyKit | Yes | Ordered local/vendor rules, admin identity, subject/session/cache | Indirect grant | No: local directory unreadable | Privileged read-only confirmation |
| sudo | Yes, root-owned mode 4111 | sudoers/plugins/session policy | Potential root deputy | No; not invoked, config not read | Preflight policy review, no credential challenge |
| pkexec | Yes, root-owned mode 4755 | Polkit/application policy | Potential privileged execution | No | Deny access/grants; no execution in this block |
| run0 | Yes | systemd/PolicyKit route; empower rule observed | Potential privileged launch | No | Include policy review; never infer exploitability |
| Other service/deputy routes | Bounded vendor metadata only | Service-specific | UNKNOWN | No exhaustive proof | Fixed worker no-exec/no-socket helps; outside peers still require policy coverage |

**M2_REQUIRES_PRIVILEGED_READ_ONLY_POLICY_CONFIRMATION.** Do not claim effective denial.
If confirmation finds grants, future policy must deny dedicated lab identities all relevant
manager/deputy mutations without interactive fallback or cached authorization reuse. Exact rule
content/order cannot be selected safely yet; no rule installed. Privileged read permission itself
would not authorize calling AttachProcesses/StartTransientUnit as a test.

### M3/M4 safe native evidence

OBSERVED_FACT: gcc/cc/clang/ld/readelf available; GCC 16.2.1-2.fc44, ld 2.46.1-1.fc44.
glibc 2.43-8.fc44 x86_64 and i686 installed, glibc-static absent. pkg-config libsystemd failed:
development metadata unavailable, not proof that runtime systemd libraries are absent.
Installed x86-64 syscall header supplied ABI numbers recorded in the companion.
No package installed. Selected future image is freestanding C11 plus assembly, with fixed branches;
full broker/controller/worker code and role-filter binaries do not exist.

A disposable raw-syscall C smoke artifact was built under Linux-native tmpfs
/tmp/cgc-m1m5-ngplw4x0. Flags: -std=c11 -O2 -Wall -Wextra -Werror -ffreestanding -fno-builtin
-fno-stack-protector -fno-pie -mno-red-zone -nostdlib -static -no-pie -Wl,--build-id=none.
readelf program headers had no INTERP. Native exit 0 checked:

- Current nonroot UID remained unchanged after setresuid(uid,uid,uid); PR_SET_DUMPABLE(0)
  followed by that same-ID operation still yielded PR_GET_DUMPABLE=0.
- A gated owned child was bound using pidfd_open, released and reaped normally.
- An unprivileged no_new_privs/seccomp filter returned EPERM for getppid in parent and fork child.

This smoke filter allowed other calls after architecture/x32 checks: **not** the proposed
deny-by-default role filter, and no security acceptance claim. No ptrace, hostile peer, identity
change, manager mutation attack or R6 case ran. Same-ID setresuid does not exercise the
root-to-C transition or its dumpability reset; M3_BOOTSTRAP_SEQUENCE_REQUIRES_PRIVILEGED_ACCEPTANCE.
Future sequence remains root gated fork -> retained pidfd -> nondumpability/FD closure ->
empty groups/bounding/ambient drops -> GID then UID transition -> explicit dumpable=0 ->
zero remaining caps/no_new_privs -> verified exact FD inventory -> role filter -> READY -> seal.
No exec follows drop. All multi-syscall transitions remain non-atomic; privileged policy stability
and no prior tracer are prerequisites. Current sysctl values are not continuous proof.

Smoke source SHA256: 7db36cb77d09eddd6e3fdf1665dd57f16bb90596caf499b89cbbe03851dbc2d7.
Smoke binary SHA256: a9263a838a5be9da01302ffedea79a87c84e0ef0d3199998e1dc9beb3b6c892a.
First compilation failed because source transport altered escaped newlines; corrected by hex
transport without changing system settings. Successful run's three diagnostic labels were
truncated by incorrect literal lengths; exit status/internal checks, not those label strings,
support the observations. No repeat run was used to conceal this diagnostic defect. Artifacts
were deleted after evidence capture as required; hashes do not promise retained replay sources.

### M5 user-manager analogue and continuity

A separate branch of the same unprivileged smoke artifact forked one child that slept three
seconds and exited; its parent exited normally immediately. Existing user manager reported
degraded, but accepted one transient unit cgc-m1m5-ngplw4x0.service with Type=exec, Restart=no,
ExitType=cgroup, KillMode=process, SendSIGKILL=no, SendSIGHUP=no, TasksMax=16, LimitNOFILE=64.
InvocationID ec780e75d2644585a7366adb2e3aa5f2. No system-manager mutation, kill or restart occurred.

OBSERVED_FACT after 0.5 seconds: ActiveState=active, SubState=running, MainPID=0,
ExecMainStatus=0, Result=success; unit cgroup events populated=1/frozen=0.
After another four seconds: inactive/dead, MainPID=0, success, empty ControlGroup property.
Independent final read: LoadState=not-found / ActiveState=inactive and exact old cgroup path absent.
Thus main-process exit did not immediately end this unit/domain. This is a user-manager,
same-UID normal-exit analogue, not proof of root/system-manager policy, crash survival or cleanup
under attack. Actual B/C death, system manager restart/reexec and WSL restart remain NOT_EXECUTED.

DERIVATION: ExitType=cgroup tracks remaining processes; MainPID, active state, cgroup existence
and empty evidence must be observed separately. KillMode=process limits configured stop targeting,
not host/OOM behavior. No automatic descendant cleanup is promised. Manager reexec can preserve
PID; continuity must bind live bus owner, manager process/start/boot context, unit InvocationID,
bound event stream and absence of missed reload/reexec interval. None alone proves generation
continuity. A gap, Reloading, bus owner change or known reexec invalidates; no silent rebind.
How to independently exclude an unobserved same-PID reexec remains an M5 acceptance gate.
No system restart is requested merely to test it.

### PRIVILEGED_OBSERVATION_REQUEST

**NOT EXECUTED.** This is a review package, not permission or a root shell recipe. All rows are
bounded read-only interfaces for an approved administrator; they must never trigger authentication
or dump credentials. No shadow/gshadow, tokens, cookies, environment dump or unrelated file content.
Per-row deadline 10 seconds, total 60 seconds; exceeding limit returns INCOMPLETE, not truncation PASS.
Administrator returns curated fields locally; policy bodies stay out of Git and the final report.

| ID / blocker | EXACT COMMAND / API SCOPE | WHY / expected output | Required privilege; sensitivity; max output | Mutation/side-effect risk / alternative if declined |
|---|---|---|---|---|
| RO-1 / M1 | lstat and read-only parse /etc/nsswitch.conf, /etc/login.defs, /etc/subuid, /etc/subgid; getpwnam_r/getgrnam_r for exact proposed names and getpwuid_r/getgrgid_r for approved candidate IDs; systemd Manager.GetDynamicUsers | NSS coverage, ranges and collision booleans; no allocation | Admin visibility as needed; account-metadata sensitivity; 8 KiB projected | NSS may contact configured provider/manager; no writes; refuse allocation if incomplete |
| RO-2 / M1 | For only approved candidate IDs: enumerate /proc/[0-9]*/status Uid/Gid/Groups and uid_map/gid_map; login1 Manager.ListSessions/ListUsers then matching records; lstat matching linger entries; systemd ListUnits then relevant User/Group/SupplementaryGroups properties | Existing process/service/session use, mappings and coverage-error counts | Root visibility; process/account metadata; 8 KiB matches/counts, no cmdline/environ | Read-only scan can race; does not reserve IDs; decline -> M1 blocked |
| RO-3 / M2 | lstat/getdents of /etc/polkit-1/rules.d and /usr/share/polkit-1/rules.d; no-follow read regular *.rules, <=64 KiB/file, <=64 files; inspect action-relevant predicates/order locally | Effective rule coverage, grants/denials for future C/W and admin groups, file digests | Root read of inaccessible local rules; policy-sensitive; 8 KiB curated summary only | File reads/atime; no evaluation mutation, CheckAuthorization or prompts; decline -> M2 UNKNOWN |
| RO-4 / M2 | Locally inspect /etc/sudoers and only its declared include graph, metadata/parsed grants for exact C/W names/groups; inventory applicable pkexec/run0 policy and D-Bus includes affecting systemd service/scope/manager | Deputy grants and include coverage; do not run sudo/pkexec/run0 | Root config visibility; authorization-policy sensitivity; 8 KiB summary, <=128 KiB input/file and <=64 files | Reads only; external policy backends unresolved -> UNKNOWN; decline -> no deputy-closure claim |
| RO-5 / M3/M5 | Read /proc/sys/fs/suid_dumpable, /proc/sys/kernel/yama/ptrace_scope; read accessible LSM status; systemd Properties.Get of Version/Features; bus GetNameOwner(systemd1); /proc/1/stat and namespace links; review installed v259 unit/reexec configuration metadata | Preconditions/continuity sources, not credential-transition or crash proof | Root only for denied status sources; kernel/config metadata; 4 KiB | Read-only, possible bus activation; no Reload/Reexecute; decline -> retain conditional model |

PRIVILEGED_READ_ONLY_REQUEST_M1 = RO-1 + RO-2. Exact candidate names/IDs must be supplied in
the reviewed request record; absent values refuse, not wildcard account dumping. Root launch
capability itself needs separate explicit execution approval later; this package does not test it.
RO-3 stops at regular policy files; symlink/unbounded include graph is a coverage refusal, not
permission to traverse arbitrary files. RO-4 is local administrator review, not publication of
sudo configuration. No persisted cache or temporary authorization is revoked/changed.

Read-only observations cannot discharge actual privilege-drop behavior, compiled filter conformance,
system-unit death semantics or hostile R6 acceptance. Those need separately authorized disposable
tests after design completion. No privilege request is hidden inside the next design step.

### Disposition and remaining gates

| Blocker | This block's classification | Exact remainder |
|---|---|---|
| M1 | PARTIALLY_RESOLVED_WITH_EXACT_REMAINING_GATE | RO-1/2, concrete allocation/provisioning transaction and launch client property encoding |
| M2 | REQUIRES_PRIVILEGED_OBSERVATION | RO-3/4; effective local rules/deputies unknown; configuration only if review proves necessary |
| M3 | PARTIALLY_RESOLVED_WITH_EXACT_REMAINING_GATE | Full native image review/build and root-to-nonroot transition acceptance; RO-5 gives prerequisites only |
| M4 | PARTIALLY_RESOLVED_WITH_EXACT_REMAINING_GATE | Bootstrap filter specialization and fixed D-Bus encoding/decoder vectors remain incomplete; smoke is not full filter |
| M5 | PARTIALLY_RESOLVED_WITH_EXACT_REMAINING_GATE | System-manager parity, crash/cleanup and uninterrupted reexec coverage; normal user analogue insufficient |

Changes actually performed: owned temporary C source/binary and one short-lived user transient unit;
all processes exited normally, exact source/binary/directory removed, unit not-found and cgroup absent.
No account, root unit, policy, persistent service, package, configuration, production or unrelated
repository change. Ordinary WSL/D-Bus/user-manager bookkeeping may persist. No zero-host-write claim.

NEXT_EXACT_ACTION: **complete the fixed native bootstrap/filter specialization and D-Bus
launch/peer codec specification with deterministic vectors, then review RO-1–RO-5 for separately
scoped privileged read-only approval. Keep R6 blocked until artifact and environment proof gates
are satisfied.** Do not request broad design approval again or execute the observation package now.
Historical containment PARTIAL, admission OPEN, filesystem exclusivity UNKNOWN, real-project P3 UNKNOWN.
R6 = NOT_EXECUTED. PRODUCTION QUIESCENCE PRODUCER = NOT_STARTED. V4 RUNTIME = NOT_STARTED.

Sources: [nss-systemd v259](https://raw.githubusercontent.com/systemd/systemd/v259/man/nss-systemd.xml),
[systemd service v259](https://raw.githubusercontent.com/systemd/systemd/v259/man/systemd.service.xml),
[systemd kill v259](https://raw.githubusercontent.com/systemd/systemd/v259/man/systemd.kill.xml).
Installed observations above, not upstream pages, support the local-policy statements.
