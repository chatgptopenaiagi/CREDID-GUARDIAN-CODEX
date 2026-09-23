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
