# CREDID GUARDIAN CODEX - CGC V3 MISSION

## CODEX PRESERVATION INTEGRATION

**V1 = OBSERVE**
**V2 = UNDERSTAND**
**V3 = PRESERVE**

**THE GUARDIAN OBSERVES. CODEX PRESERVES.**

**PRESERVE BEFORE EXPANDING.**

**COMPUTATION MAY STOP. HUMAN CONTINUITY MUST NOT.**

**ONE SENSOR. MULTIPLE CONSUMERS.**

Work in:

```text
/mnt/c/Codex-Projects/CREDID-GUARDIAN-CODEX
```

V1 and V2 are preserved foundations.

V3 is the active mission.

Do not begin a later version unless separately authorized.

---

# 1. RESUME FROM PRESENT EVIDENCE, NOT FROM A HARDCODED CHECKPOINT

Every time Codex begins or resumes work on CGC V3, first determine the actual present state of the repository.

Do not assume that any commit SHA, previous completion percentage, previous NEXT_EXACT_ACTION, previous chat message, or historical progress record is still current.

Do not mechanically return to an old checkpoint.

A checkpoint is evidence of where preservation succeeded at a particular time. It is not a permanent starting instruction.

At session start, inspect and reconcile at least:

```text
repository root
current branch
working tree
local HEAD
tracking branch
origin/main or applicable upstream
live remote branch when available
recent relevant commits
existing V3 implementation
existing V3 tests
existing V3 documentation
existing preserved progress
existing acceptance evidence
```

Read completely, when present:

```text
docs/V3_MISSION.md
docs/V3_PROGRESS.md
docs/V3_ACCEPTANCE.md
README.md
AGENTS.md
docs/DECISIONS.md
docs/ARCHITECTURE.md
docs/DATA_MODEL.md
docs/PRESERVATION_POLICY.md
docs/SECURITY_MODEL.md
```

Read the V2 mission, progress, acceptance and operations records when needed to understand inherited contracts and boundaries.

Determine dynamically:

```text
What is actually COMPLETE?
What is actually PARTIAL?
What is actually NOT_STARTED?
What implementation already exists?
What tests already exist?
What tests currently pass?
What documentation is current?
What documentation is stale?
What work exists in the working tree but is not yet preserved?
What is the latest coherent safe state?
What is already published remotely?
What is only local?
What is the real current V3 frontier?
What is the safest NEXT_EXACT_ACTION now?
```

`docs/V3_PROGRESS.md` is the primary continuity handoff, but it is evidence, not absolute authority.

If Git state, implementation, tests and progress documentation disagree:

```text
inspect
reconcile
preserve valuable newer work
document the discrepancy
determine the safest evidence-supported state
continue from that state
```

Do not destroy valid newer work merely because an older document points somewhere else.

Do not redo completed V1 or V2 work.

Do not repeat completed V3 blocks unless regression evidence, corruption, or a demonstrated defect requires it.

Do not perform repeated live quota reads merely to rediscover percentages.

Resume from the latest coherent, evidence-supported and safely recoverable V3 frontier.

For each working session, complete one coherent architectural block. Do not mechanically execute a fixed number of requirements when that would split one logical unit or cross into another phase.

Operate autonomously for ordinary engineering work.

Use the safest robust engineering choice when several reasonable choices exist and document important decisions.

You are authorized to use the development environment required for CGC, including:

```text
CGC repository
Linux /tmp
Linux home
WSL filesystems
Windows-mounted filesystems when appropriate
temporary directories
synthetic repositories
local bare Git remotes
Python
Git
GitHub CLI
test runners
compilers
debuggers
network access
package tooling when technically necessary
filesystem/process/system inspection required for CGC
```

Do not repeatedly ask permission for ordinary CGC development actions.

Full access does not authorize random modification of unrelated projects or user data.

Do not expose or commit:

```text
authentication tokens
API keys
passwords
cookies
private keys
authentication stores
unrelated personal secrets
```

For POSIX ownership, locking and permission-sensitive tests, prefer Linux-native temporary storage such as `/tmp`.

Do not weaken CGC security merely to accommodate Windows-mounted filesystem behavior.

---

# 2. V3 MUST TURN GUARDIAN AWARENESS INTO VERIFIED PROJECT PRESERVATION

The purpose of V3 is to connect trustworthy Guardian state to real project continuity.

The target flow is:

```text
Guardian observes
        ↓
preservation becomes authorized
        ↓
identify explicit project
        ↓
inspect project safely
        ↓
understand current work
        ↓
stop unnecessary expansion
        ↓
stabilize the smallest coherent unit
        ↓
run relevant verification
        ↓
preserve operational handoff
        ↓
create a safe local checkpoint when appropriate
        ↓
publish when authorized and safe
        ↓
verify actual remote state
        ↓
leave an exact resumable state
```

Preservation does NOT mean simply:

```text
save files
```

and does NOT mean blindly:

```text
git add .
git commit
git push
```

Preservation means:

> Leave enough verified state that a fresh Codex session, another compatible AI agent, or the human operator can continue without reconstructing the previous work.

V3 must separate three responsibilities:

```text
DETECT
Determine whether preservation is requested or safely authorized.

PRESERVE
Convert current project state into a coherent recoverable checkpoint.

VERIFY
Prove what was preserved, what was not preserved, and what remains uncertain.
```

Manual preservation comes first.

V3 should support an explicit bounded preservation operation conceptually equivalent to:

```text
cgc preserve --project <PATH>
```

The exact CLI may evolve according to the existing architecture.

A human must be able to request preservation independently of live quota availability.

Do not require the operator to fabricate RED or EMERGENCY state.

V3 must consume the canonical Guardian model established by V1/V2.

Do not create another quota reader.

**ONE SENSOR. MULTIPLE CONSUMERS.**

Guardian states such as:

```text
UNKNOWN
STALE
ERROR
UNAVAILABLE
HISTORICAL
RETAINED
SYNTHETIC
```

must not silently authorize automatic external project mutation.

Automatic preservation may only occur when the existing Guardian contract provides sufficient current authority.

Synthetic Guardian states are allowed for deterministic tests, but must remain explicitly synthetic.

## Explicit project identity

Never search the whole machine to guess which project is active.

A preservation target must come from trusted explicit context such as:

```text
--project PATH
registered project
known current repository
explicit configuration
trusted future session metadata
```

Before mutation, establish project identity and safe boundaries.

A bounded project snapshot should be capable of representing relevant state such as:

```text
project root
repository identity
branch
HEAD
upstream
remote
tracked modifications
staged changes
unstaged changes
untracked work
deleted or renamed work where safely detectable
merge/rebase/cherry-pick state
conflicts
detached HEAD
worktree state
submodule state where relevant
known project instructions
known test command
existing progress/handoff documents
```

The snapshot is evidence.

The snapshot itself is not preservation.

## Preservation state and outcome

Do not reduce preservation to one success boolean.

Maintain explicit operational states, conceptually such as:

```text
IDLE
REQUESTED
PRECHECK
INSPECTING
BLOCKED
STABILIZING
TESTING
DOCUMENTING
CHECKPOINTING
PUBLISHING
VERIFYING
PRESERVED
PARTIAL
FAILED
CANCELLED
```

Maintain meaningful outcomes such as:

```text
NO_ACTION_REQUIRED
BLOCKED_UNSAFE
HANDOFF_ONLY
LOCAL_CHECKPOINT
REMOTE_VERIFIED
PARTIAL
FAILED
CANCELLED
```

A crash or exception must never silently appear as PRESERVED.

Expose an evidence-based resume result:

```text
SAFE_TO_RESUME =
YES
PARTIAL
NO
UNKNOWN
```

`YES` must require evidence.

A successful process exit alone is not evidence.

## Preservation record

Every meaningful preservation handoff should make clear:

```text
PROJECT
TRIGGER / AUTHORITY

COMPLETE
PARTIAL
NOT_STARTED

FILES CHANGED
TESTS RUN
TEST RESULTS
KNOWN FAILURES
IMPORTANT DISCOVERIES
DO_NOT_REPEAT

LAST SAFE LOCAL CHECKPOINT
REMOTE PUBLICATION STATE
NEXT_EXACT_ACTION
SAFE_TO_RESUME
```

Provide human-readable and machine-readable forms derived from the same validated preservation model.

Preserve decisions, requirements, evidence, commands, observable outcomes, test results, known failures and next actions.

Do not attempt to preserve private model chain-of-thought.

## Preservation behavior

Once preservation begins:

```text
STOP EXPANDING
STABILIZE
VERIFY
DOCUMENT
CHECKPOINT
```

Do not start new features while preserving the current coherent unit.

Normal preservation may perform:

```text
inspect
stabilize
run relevant tests
document
checkpoint
publish if authorized
verify
```

Emergency preservation may use a reduced path:

```text
stop expansion
capture current state
write minimum handoff
preserve work safely
create the safest possible checkpoint
attempt publication only if bounded and safe
record everything not verified
stop
```

Emergency mode may do less.

It may never claim more than it actually verified.

## Testing and project awareness

Do not invent project test commands.

Determine them from trustworthy sources such as:

```text
AGENTS.md
README
project configuration
package metadata
existing progress records
explicit operator configuration
```

If no trustworthy test command exists, record that truthfully.

A failing project test does not automatically mean preservation failed.

Keep separate:

```text
PROJECT_TEST_STATUS
PRESERVATION_STATUS
PUBLICATION_STATUS
RESUME_STATUS
```

A failing but accurately preserved checkpoint may be safer than destroying valuable work to obtain a green test result.

## Git safety

V3 preservation must protect work, not erase it.

Do not automatically perform destructive actions such as:

```text
git reset --hard
git clean -fd
git clean -fdx
git checkout -- .
git restore --source ...
automatic rebase
history rewriting
force push
```

Do not blindly use:

```text
git add .
```

Build a deliberate staging decision.

Treat untracked files carefully because they may contain valuable new work or secrets/generated data.

Respect `.gitignore`.

Avoid unexpectedly committing model weights, large archives, caches, databases, build trees or other large generated artifacts.

Do not silently bypass project hooks.

Preserve existing branch/history unless an explicitly authorized project policy says otherwise.

A preservation handoff may be valid even when no new commit is necessary.

Do not manufacture meaningless commits merely to satisfy workflow.

## Publication and verification

Before publication:

```text
verify remote identity
verify branch relationship
verify forward-only intent
```

Never force push.

A successful `git push` process exit is not sufficient evidence of remote preservation.

After publication, verify actual remote state.

Where applicable compare:

```text
local HEAD
tracking ref
live remote ref
```

Only claim remote preservation after equivalent evidence is established.

If publication fails but a valid local checkpoint exists:

```text
preserve the local checkpoint
record its identity
record LOCAL_CHECKPOINT_ONLY
record why remote verification is incomplete
```

Never discard a safe local checkpoint because the network or remote failed.

## Concurrency, interruption and atomicity

Only one preservation writer should mutate a project at a time.

Use safe writer exclusion.

A dead process must not permanently block future preservation.

Test interruption at meaningful stages such as:

```text
before inspection
during inspection
before handoff write
during handoff write
after handoff write
before staging
after staging
before commit
after commit
before publication
during publication simulation
after publication
before remote verification
after remote verification
```

Use atomic canonical preservation-state publication where practical.

A failed new preservation attempt must not erase the previous valid last-known-good preservation state.

Distinguish:

```text
latest attempt
last successful preservation
```

## Offline-first development

Test primarily with:

```text
synthetic Guardian states
synthetic Git repositories
Linux-native temporary storage
local bare Git remotes
injected subprocess failures
SIGINT
SIGTERM
```

Do not use valuable real repositories as early V3 mutation fixtures.

Prove capabilities in this order:

```text
manual preservation
        ↓
project snapshot
        ↓
handoff correctness
        ↓
local checkpoint
        ↓
publication semantics
        ↓
remote verification
        ↓
crash/concurrency safety
        ↓
fresh-process resume
        ↓
Guardian integration
        ↓
safe automation
```

Automation is the final layer, not the first.

---

# 3. V3 CONTINUITY, ACCEPTANCE AND WORKING METHOD

CGC development itself must obey CGC principles.

At the beginning of every new working session:

```text
inspect current repository reality
read V3_MISSION
read V3_PROGRESS when present
inspect existing V3 implementation and tests
reconcile documentation with current evidence
determine the latest coherent safe state
determine the current V3 frontier
determine whether the recorded NEXT_EXACT_ACTION is still valid
resume from the evidence-supported frontier
```

Do not depend on a commit SHA embedded in an old prompt.

Do not depend on previous conversation memory.

The repository must be able to explain itself.

If `docs/V3_PROGRESS.md` is missing, stale, incomplete, or contradicts the implementation:

```text
reconstruct the current frontier from Git, source, tests and documentation
preserve that reconstructed state
write/update V3_PROGRESS
then continue
```

A sensible V3 evolution is:

```text
preservation contract/state model
        ↓
explicit non-mutating project inspection
        ↓
human + machine handoff
        ↓
local checkpoint
        ↓
publication + remote verification
        ↓
crash/concurrency hardening
        ↓
fresh-process resume proof
        ↓
Guardian authority integration
        ↓
automatic preservation
        ↓
final acceptance
```

This is guidance, not a command to redo work already completed.

Always judge present repository reality first.

At each coherent milestone:

```text
run relevant deterministic tests
run regression tests
review failures
fix demonstrated in-scope problems
update V3 documentation
update docs/V3_PROGRESS.md
record COMPLETE / PARTIAL / NOT_STARTED
record tests passed and remaining
record known failures
record important discoveries
record files changed
record DO_NOT_REPEAT
record exact NEXT_EXACT_ACTION
create a safe Git checkpoint when justified
push validated CGC work when safe
verify actual publication
```

`docs/V3_PROGRESS.md` should remain a complete continuity handoff and contain at least:

```text
OVERALL STATUS
CURRENT SESSION BLOCK
COMPLETE
PARTIAL
NOT_STARTED
TESTS PASSED
TESTS REMAINING
KNOWN FAILURES
IMPORTANT DISCOVERIES
FILES CHANGED
DO_NOT_REPEAT
NEXT_EXACT_ACTION
LAST SAFE CHECKPOINT
PUBLICATION STATE
OPERATIONS / INTEGRITY
```

If available Codex capacity becomes low:

```text
STOP NEW DEVELOPMENT
COMPLETE OR STABILIZE CURRENT COHERENT UNIT
TEST
DOCUMENT
CHECKPOINT
PUSH WHEN SAFE
VERIFY
LEAVE NEXT_EXACT_ACTION
STOP
```

Do not sacrifice completed work trying to finish one more feature.

## V3 acceptance

Before V3 can be declared COMPLETE, evidence must demonstrate at minimum that:

```text
V1 regression remains passing
V2 regression remains passing

explicit project targeting works
unsafe targets are refused
project inspection is bounded
manual preservation works

COMPLETE / PARTIAL / NOT_STARTED survive
known failures survive
NEXT_EXACT_ACTION survives
fresh-process resume works

safe local checkpointing works
staging is deliberate
destructive Git behavior is absent
secret-risk protections exist

publication semantics work
publication failure remains truthful
remote verification works
LOCAL_CHECKPOINT_ONLY works

concurrent writers are controlled
crash/interruption behavior is tested
last-known-good preservation survives newer failure
SAFE_TO_RESUME is evidence-based

Guardian UNKNOWN cannot authorize automatic mutation
synthetic Guardian integration works
automatic preservation consumes canonical V2 Guardian state only

resource bounds exist
security/path tests pass
no unrelated project was modified
no V1/V2 semantics were silently weakened
documentation is complete
the final CGC V3 checkpoint itself is resumable
```

Before declaring V3 complete, create and maintain:

```text
docs/V3_ACCEPTANCE.md
```

Map the actual V3 mission to:

```text
implementation evidence
test evidence
scope
limitations
status
```

Use truthful states such as:

```text
COMPLETE
PARTIAL
NOT_STARTED
NOT_APPLICABLE
```

Do not hide residual limitations.

Do not claim V3 complete merely because:

```text
a preserve command exists
a commit can be created
a handoff file exists
a push succeeded once
```

The decisive acceptance question is:

> Can a fresh session determine what happened, what survived, what remains, what checkpoint is safe, what publication status is real, and exactly what to do next without reconstructing the previous session?

Before stopping each working session, report:

```text
1. work completed
2. work partial
3. work not started
4. files created/modified
5. tests performed
6. exact test results
7. environment/system changes
8. live operations consumed
9. preservation operations performed
10. known limitations
11. Git checkpoint
12. remote verification
13. NEXT_EXACT_ACTION
```

Do not begin V4, cloud control plane, ARX cloud integration, GUI, mobile application, distributed continuity, or unrelated future expansion as part of V3 unless separately authorized.

When all mandatory V3 acceptance requirements are actually satisfied and the final preservation state is verified, V3 may state:

```text
CREDID GUARDIAN CODEX — CGC V3 COMPLETE

CODEX PRESERVATION INTEGRATION VERIFIED.

THE GUARDIAN OBSERVES.
CODEX PRESERVES.
```

Then STOP and await the next explicitly authorized mission.

**PRESERVE BEFORE EXPANDING.**

**THE GUARDIAN OBSERVES. CODEX PRESERVES.**

**COMPUTATION MAY STOP. HUMAN CONTINUITY MUST NOT.**
# CREDID GUARDIAN CODEX — AGENT FABRIC / PRESERVATION ARCHITECTURE DIRECTIVE

Continue working inside:

```text
/mnt/c/Codex-Projects/CREDID-GUARDIAN-CODEX
```

This directive introduces a long-term architectural vision that must be understood and incorporated into the design of CREDID GUARDIAN CODEX.

It does NOT automatically authorize premature implementation of networking, autonomous mutation, cloud control, background daemons, unrestricted remote execution or V4 work.

The current repository, current CGC mission documents, Git state, tests and evidence remain authoritative.

First determine the real current project state.

Then integrate the following concepts into the CGC architecture in the safest coherent way.

The architectural chain CGC is ultimately intended to support is:

```text
DETECT RISK
    ↓
INSPECT
    ↓
UNDERSTAND
    ↓
CHECKPOINT
    ↓
RUN TESTS
    ↓
SAVE HANDOFF
    ↓
VERIFY GIT / REMOTE
    ↓
RECORD NEXT_EXACT_ACTION
    ↓
RESUME SAFELY
```

CGC should also evolve toward participation in a common secure AI Agent Fabric connecting local AI, cloud AI, Codex, Guardian systems and future specialized agents.

The design principle is:

```text
DO NOT BUILD A DIFFERENT BRIDGE BETWEEN EVERY TWO AGENTS.

BUILD A COMMON, CONTROLLED, CAPABILITY-BASED COMMUNICATION FABRIC.
```

## EXACTLY 100 ARCHITECTURAL KEYPOINTS

1. Treat CGC's primary responsibility as preserving human continuity when AI computation, sessions, quotas, processes or machines stop.

2. Preserve the core lifecycle: `DETECT → INSPECT → UNDERSTAND → PRESERVE → VERIFY → RESUME`.

3. Risk detection must remain logically distinct from preservation actions.

4. Observation of a project must never automatically grant authority to modify that project.

5. Every preservation action must originate from explicit authority, an approved policy or a precisely defined capability.

6. CGC must understand the difference between a project being dirty, unsafe, incomplete, divergent, corrupted or merely active.

7. Project inspection should produce structured evidence rather than vague textual assumptions.

8. Preservation decisions should consume evidence generated by bounded inspection.

9. A checkpoint must represent a coherent recoverable state, not merely an arbitrary Git commit.

10. CGC must record whether a work unit is `COMPLETE`, `PARTIAL` or `NOT_STARTED`.

11. CGC must preserve an exact `NEXT_EXACT_ACTION` whenever work stops.

12. `NEXT_EXACT_ACTION` should eventually become machine-readable rather than existing only as prose.

13. Test state must be considered part of continuity state.

14. Git state must be considered part of continuity state.

15. Remote publication state must be considered separately from local commit state.

16. A successful `git commit` does not prove remote preservation.

17. A successful `git push` message alone does not prove remote preservation.

18. Final verification should be capable of proving `local HEAD == tracking branch == live remote branch` when that invariant applies.

19. Test results associated with a checkpoint should include exact pass, fail, error and skip information when available.

20. CGC should distinguish a checkpoint that is structurally valid from one that is fully validated.

21. Handoff information must survive the death of the current Codex process.

22. Handoff information must survive the loss of conversational memory.

23. Handoff information should eventually survive machine restart where technically practical.

24. The repository and durable CGC records must remain the source of truth, not historical prompts.

25. Resume prompts should eventually be generated automatically from durable evidence.

26. Future resume-prompt generation should combine at least `NEXT_EXACT_ACTION + Git state + test state`.

27. Future resume-prompt generation may additionally incorporate quota state, preservation state and mission boundaries.

28. Generated resume prompts must never silently override newer repository evidence.

29. Resume logic must reconcile stale progress records against actual Git and filesystem state.

30. Valid newer work must be preserved rather than rolled back to match an older handoff.

31. CGC should evolve from a standalone Guardian into a participant in a broader AI Agent Fabric.

32. The Agent Fabric should provide one common communication model rather than many pairwise custom integrations.

33. Avoid architectures where every agent directly implements protocols for every other agent.

34. Avoid an uncontrolled `A ↔ B ↔ C ↔ D` mesh that scales toward connection spaghetti.

35. Prefer agents connecting through a shared Gateway, Router, Bus or equivalent abstraction.

36. The common Agent Fabric must not require every participating component to use the same programming language.

37. Communication contracts should be language-neutral and serializable.

38. Agent messages should have explicit schemas.

39. Every message should identify its sender.

40. Every message should identify its intended capability or action.

41. Messages should support correlation identifiers so requests and responses can be reliably matched.

42. Messages should support versioned schemas so the protocol can evolve safely.

43. The Agent Fabric should distinguish identity from authorization.

44. Knowing which agent sent a request must not automatically mean the request is permitted.

45. Authorization should be capability-based wherever practical.

46. Agents should receive narrow capabilities rather than blanket machine authority.

47. Example capabilities may include `inspect_project`, `read_git_status`, `run_tests`, `read_file`, `write_project_file`, `create_checkpoint`, `verify_remote` and `call_local_model`.

48. Dangerous capabilities must remain separately controlled from observational capabilities.

49. CGC should be able to possess inspection capabilities without automatically possessing mutation capabilities.

50. Destructive capabilities such as deleting repositories or rewriting published Git history should not be normal Guardian primitives.

51. Capability grants should be explicit, inspectable and auditable.

52. Capabilities should have scope, including which project, path, repository or resource they apply to.

53. Capabilities should support expiration or revocation where appropriate.

54. The architecture should distinguish the Control Plane from the Data Plane.

55. The Control Plane should determine who may perform which operation.

56. The Control Plane should determine which project or resource the operation may target.

57. The Control Plane should be able to consider quota and policy state.

58. The Control Plane should eventually support capability discovery.

59. The Data Plane should transport actual prompts, responses, events, tool results and authorized data.

60. Control decisions must not be hidden inside arbitrary Data Plane payloads.

61. Local AI should be treated as a first-class participant in the Agent Fabric.

62. Local AI may include Ollama, local LLMs, embeddings, GPU inference and local analysis engines.

63. Sensitive information should remain local whenever cloud processing is unnecessary.

64. Cloud AI should receive only the context required for an authorized task.

65. Local-to-cloud transitions should support sanitization or filtering boundaries.

66. Cloud AI must not automatically receive unrestricted control of the host machine.

67. Cloud systems should invoke defined capabilities through the Gateway instead of arbitrary local commands.

68. Remote communication should use authenticated encrypted transport when eventually implemented.

69. A secure tunnel should transport structured authorized requests rather than expose unrestricted shell access.

70. The architecture should conceptually support signed or authenticated message envelopes.

71. Message validation must occur before capability execution.

72. Policy validation must occur before capability execution.

73. Input validation must treat agent-generated input as untrusted until validated.

74. Agent identity should be verifiable independently from natural-language claims inside a prompt.

75. Secrets must not become normal Agent Fabric message payloads.

76. Authentication tokens, API keys, passwords, private keys and credential stores must never be logged merely for debugging convenience.

77. The Fabric should eventually support security-aware logging without recording sensitive payloads unnecessarily.

78. Communication should support classic request/response interactions.

79. Communication architecture should also permit streaming where long model output or incremental data genuinely requires it.

80. The architecture should support an event model for asynchronous state changes.

81. Example events may include `codex.capacity.low`, `tests.completed`, `project.dirty`, `checkpoint.created`, `checkpoint.verified` and `preservation.failed`.

82. Events must describe facts or state transitions rather than directly granting arbitrary execution authority.

83. Event reception should pass through policy before resulting in mutation.

84. `codex.capacity.low` may eventually trigger a preservation decision workflow, but it must not imply unrestricted automatic commits by itself.

85. CGC should support preservation policy separately from transport implementation.

86. The Fabric should not force CGC itself to become a giant monolithic server.

87. Prefer modular components such as Gateway, Policy Engine, Router, Event Bus, Capability Registry and Guardian Core where separation is justified.

88. Do not create independent full networking stacks for CGC, CWM, HHS, ARX, local AI and every future agent if a reusable common Fabric can serve them.

89. Future systems such as CWM, HHS, ARX, local AI engines and other agents should be able to participate through the same protocol family.

90. The architecture should allow a future master orchestrator to coordinate agents without bypassing Guardian policy.

91. No orchestrator should automatically become an all-powerful root authority merely because it coordinates other agents.

92. CGC should remain capable of refusing an unsafe operation even when another authorized agent requests it.

93. Guardian decisions should be explainable from evidence, capabilities and policy.

94. All major preservation operations should produce structured receipts suitable for later verification.

95. Failed preservation attempts must remain distinguishable from last-known-good preservation state.

96. The architecture should eventually support atomic publication semantics where practical.

97. Concurrent preservation writers must eventually be controlled so two agents cannot independently corrupt one preservation transaction.

98. Fresh-process resume must eventually reconstruct continuity from durable state without relying on conversational memory.

99. Architect these concepts incrementally according to the current CGC mission: document and design future layers now where appropriate, but do not prematurely implement live networking, autonomous mutation, daemonization, cloud tunnels or later-version functionality merely because this directive describes them.

100. The final engineering principle is: `PRESERVE BEFORE EXPANDING`; CGC must ensure that computation may stop while human continuity remains recoverable, verifiable and safe.

---

# ENGINEERING INSTRUCTION

Use the 100 keypoints as architectural requirements and design constraints, not as an instruction to implement 100 features immediately.

First inspect:

```text
docs/V3_MISSION.md
docs/V3_PROGRESS.md
docs/V3_ACCEPTANCE.md
docs/V3_CONTRACT.md
README.md
AGENTS.md
docs/DECISIONS.md
docs/ARCHITECTURE.md
docs/DATA_MODEL.md
docs/SECURITY_MODEL.md
docs/PRESERVATION_POLICY.md
docs/ROADMAP.md
current source
current tests
current Git state
current remote state
```

Determine what portion of this architecture:

```text
A. already exists
B. is partially represented
C. should be documented now
D. belongs later in V3
E. belongs after V3
F. must remain explicitly NOT_STARTED
```

Do not distort the current V3 mission merely to fit this vision.

Instead, reconcile the vision with the current architecture.

If appropriate, create or update an architectural document such as:

```text
docs/AGENT_FABRIC_ARCHITECTURE.md
```

or choose a better repository-consistent name.

That document should explain at minimum:

```text
Guardian Core
Agent Gateway
Control Plane
Data Plane
Capability Model
Policy Engine
Router
Event Model
Local AI boundary
Cloud AI boundary
secure transport boundary
preservation lifecycle
handoff lifecycle
resume lifecycle
trust boundaries
future integration points
```

You may update:

```text
docs/ARCHITECTURE.md
docs/ROADMAP.md
docs/DECISIONS.md
docs/SECURITY_MODEL.md
docs/PRESERVATION_POLICY.md
docs/V3_PROGRESS.md
README.md
AGENTS.md
```

only where the changes accurately reflect the architecture.

Do not claim implementation where only architecture exists.

Use explicit labels such as:

```text
IMPLEMENTED
PROVISIONAL
ARCHITECTED
FUTURE
NOT_STARTED
NOT_AUTHORIZED
```

where useful.

---

# CRITICAL CURRENT-VERSION BOUNDARY

If the active CGC V3 mission currently authorizes only inspection or another narrower coherent block, respect that boundary.

Do NOT use this prompt as permission to suddenly implement:

```text
network listeners
internet-facing services
remote shells
cloud tunnels
automatic commits
automatic stash
automatic branch creation
automatic project repair
background monitoring
background preservation daemons
cross-project mutation
unrestricted orchestration
secret collection
V4
```

Architecture may anticipate these capabilities.

Implementation must follow the authorized project sequence.

---

# DESIRED LONG-TERM CGC FLOW

Architect CGC so that the future system can eventually support:

```text
RISK DETECTED
      ↓
Guardian evaluates evidence
      ↓
explicit project identified
      ↓
bounded inspection
      ↓
current coherent work understood
      ↓
tests selected
      ↓
checkpoint candidate prepared
      ↓
tests executed
      ↓
handoff state generated
      ↓
COMPLETE / PARTIAL / NOT_STARTED recorded
      ↓
NEXT_EXACT_ACTION recorded
      ↓
checkpoint created
      ↓
remote publication attempted
      ↓
remote publication independently verified
      ↓
last-known-good state recorded
      ↓
Codex/session may stop
      ↓
new session starts
      ↓
CGC reads durable evidence
      ↓
Git state reconciled
      ↓
test state reconciled
      ↓
NEXT_EXACT_ACTION reconciled
      ↓
resume prompt generated
      ↓
Codex continues safely
```

---

# DESIRED LONG-TERM AGENT FABRIC

Conceptually architect toward:

```text
                     CLOUD AI
                        │
                 secure transport
                        │
                        ▼
                ┌───────────────┐
                │ AGENT GATEWAY │
                └───────┬───────┘
                        │
            ┌───────────┼───────────┐
            │           │           │
        POLICY        ROUTER      EVENT BUS
            │           │           │
            └───────────┼───────────┘
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
       CODEX            CGC        LOCAL AI
        Agent         Guardian      Engine
          │                           │
          ▼                           ▼
         Git                    Ollama / GPU
          │
          ▼
       Projects
```

Future master coordination may conceptually become:

```text
                  MASTER ORCHESTRATOR
                         │
        ┌────────────────┼────────────────┐
        │                │                │
      CODEX             CGC              CWM
        │             Guardian             │
        └────────────────┼─────────────────┘
                         │
                    AGENT FABRIC
                         │
                ┌────────┴────────┐
                │                 │
            LOCAL AI          CLOUD AI
```

But the orchestrator must operate through policy and capabilities rather than bypassing them.

---

# ARCHITECTURAL QUESTION CODEX MUST ANSWER

Think as a senior systems engineer.

Do not blindly implement my proposed names or topology if the repository evidence suggests a better design.

You are explicitly allowed to improve the conceptual architecture.

Ask internally:

```text
What belongs inside CGC?
What belongs in a reusable Agent Fabric?
What should remain external?
What interfaces should exist?
Where are the trust boundaries?
Which components require durable state?
Which components should remain stateless?
What must be synchronous?
What benefits from events?
What must never be automatic?
How should capabilities be represented?
How can transport remain replaceable?
How can local AI remain private?
How can cloud AI be useful without becoming unrestricted?
How can CGC survive process death?
How can CGC prove preservation rather than merely claim it?
How can a future beginner use this safely?
```

Prefer small stable primitives over a large speculative framework.

Avoid needless complexity.

Do not create infrastructure merely because the architecture diagram contains a box.

---

# BEGINNER EXPERIENCE MUST REMAIN A DESIGN REQUIREMENT

Although internals may become sophisticated, the final Windows user experience should eventually be capable of becoming approximately:

```text
Choose project
      ↓
START CODEX SAFELY
      ↓
Guardian observes
      ↓
Guardian warns when continuity is at risk
      ↓
PRESERVE
      ↓
tests run
      ↓
checkpoint verified
      ↓
SAFE TO CLOSE
      ↓
later:
RESUME PROJECT
      ↓
CGC reconstructs state
      ↓
resume prompt generated
      ↓
Codex continues
```

The beginner should not be forced to understand Git internals, WSL internals, protocol internals or Agent Fabric internals merely to receive continuity protection.

Complexity should live inside the architecture, not inside the user's head.

---

# SESSION OUTPUT

For this session, perform only the coherent architectural work allowed by the current CGC frontier.

Before stopping:

```text
run relevant tests
run regressions if implementation changed
validate documentation
update continuity records
record COMPLETE / PARTIAL / NOT_STARTED
record architecture-only vs implemented elements
record DO_NOT_REPEAT
record NEXT_EXACT_ACTION
create a safe Git checkpoint when justified
push validated work when safe
verify remote publication
STOP
```

Final report must state:

```text
1. CURRENT CGC FRONTIER
2. ARCHITECTURE ADDED
3. EXISTING CONCEPTS REUSED
4. NEW CONCEPTS INTRODUCED
5. IMPLEMENTED COMPONENTS
6. ARCHITECTURE-ONLY COMPONENTS
7. FUTURE COMPONENTS
8. EXPLICITLY NOT AUTHORIZED COMPONENTS
9. TRUST BOUNDARIES
10. CAPABILITY MODEL
11. CONTROL PLANE MODEL
12. DATA PLANE MODEL
13. EVENT MODEL
14. LOCAL AI BOUNDARY
15. CLOUD AI BOUNDARY
16. PRESERVATION / RESUME FLOW
17. FILES CREATED / MODIFIED
18. TESTS PERFORMED
19. EXACT TEST RESULTS
20. SECURITY FINDINGS
21. KNOWN LIMITATIONS
22. GIT CHECKPOINT
23. REMOTE VERIFICATION
24. FINAL WORKING TREE
25. NEXT_EXACT_ACTION
```

Do not begin another development block after producing the checkpoint.

Do not confuse architecture with implementation.

Do not confuse communication with authority.

Do not confuse inspection with preservation.

Do not confuse preservation with verification.

Do not confuse successful computation with durable human continuity.

**PRESERVE BEFORE EXPANDING.**

**THE GUARDIAN OBSERVES. CODEX PRESERVES.**

**AGENTS COMMUNICATE THROUGH CAPABILITIES, NOT THROUGH UNCONTROLLED ACCESS.**

**LOCAL WHEN PRIVATE. CLOUD WHEN JUSTIFIED. POLICY BETWEEN THEM.**

**COMPUTATION MAY STOP. HUMAN CONTINUITY MUST NOT.**
