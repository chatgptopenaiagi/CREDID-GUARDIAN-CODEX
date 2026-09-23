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
