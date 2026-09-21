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
