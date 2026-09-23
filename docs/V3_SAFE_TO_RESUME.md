# CGC V3 — external SAFE_TO_RESUME verifier contract

Status: **SPECIFIED / implementation NOT_STARTED**. Contract revision: **V3 verifier contract 1**.
CREDID GUARDIAN CODEX (CGC). Subordinate to the [V3 mission](V3_MISSION.md),
[reconciliation contract](V3_RECONCILIATION.md) and existing [adapter contracts](V3_CONTRACT.md).
This document specifies proof evaluation; it adds no runtime, schema migration, CLI or recovery.
V3 remains PARTIAL. V4 remains ARCHITECTED / runtime NOT_STARTED.

## 1. Separation and audited foundation

| Layer | Responsibility | Does not establish |
|---|---|---|
| Collector | Bounded permitted observations, explicit provenance and coverage | Atomicity, universal quiescence or permission |
| Reconciler | Reconstruct evidence-supported state; preserve history and contradictions | External safety; its UNKNOWN/false/false invariants remain unchanged |
| Verifier | Pure deterministic evaluation for an exact continuation and preservation scope | Authority, execution, permanent capability or a new historical receipt |
| Authority layer | Current project/action/state-scoped decision | Evidence truth or unchanged preconditions |
| Executor | Separately authorized action with fresh boundary checks | Permission from an old YES or historical intent |

Audit baseline: `3b0e439f5a6f4769957899e4b6416986bafc69d3`; implementation
`0ee3ab2a78e1cb3f2ad88075a4908c6a88bb8d80`. Sources:
[reconciliation](../src/cgc/reconciliation.py), [inspection](../src/cgc/inspection.py),
[handoff](../src/cgc/handoff.py), [checkpoint](../src/cgc/checkpoint.py),
[publication](../src/cgc/publication.py), [attempt](../src/cgc/preservation.py),
[signals](../src/cgc/signals.py), [reconciliation acceptance](../tests/test_reconciliation.py).
Accepted interruption evidence is indexed in [reconciliation section 10](V3_RECONCILIATION.md#10-interrupted-attempt-matrix).
Those experiments are not repeated by this design.

Current evidence has important limits:

- `validate_result` recomputes derived fields and checks shape/coherence; it does not authenticate
  supplied evidence. A consistently fabricated projection is not an external observation.
- `collect` reads two local snapshots and handoff references; their equality is not atomicity.
  Metadata/inspection digests are not full worktree content identities. Some inspection boundary
  detail is summarized out of the projection; missing coverage cannot be recovered from a digest.
- Current review CURRENT means supplied SHA256 matched safe bytes, with mode/blob observations.
  It does not attest a review event, complete context or human approval.
- Legacy notes and optional `{result, commands, results, bound_head}` cannot establish current
  test applicability. Matching HEAD leaves dirty inputs/environment unknown.
- Parent-death tests prove a Git child can survive both CGC flocks releasing, with or without
  index.lock. Process quiescence is intentionally UNKNOWN in every reconciliation result.
- Saved inner attempt YES is a structural receipt calculation, not external verification.
  Continuity PUBLISHED means handoff saved, not successful Git publication.

No runtime defect requiring a change was established by this audit. These are documented coverage
limits to enforce at the new boundary. Existing schemas, adapters and all safety invariants stay intact.

## 2. Input, provenance and strict boundary

Conceptual pipeline: **COLLECT → RECONCILE → VERIFY**, with authority and execution separate.
The pure verifier receives a validated `cgc-reconciliation-v3.0-provisional` projection, exact
request and explicit evidence bundle. It does not read Git, storage, processes, a clock or environment.
Same complete input produces identical canonical result and human rendering. Verification itself
never writes a handoff/resume receipt or advances an attempt to PRESERVED.

A request binds project path plus root/Git identities, action, preservation level, selected scope,
expected state, observation reference and a versioned policy profile. Time at evaluation, when needed
for a supplied decision's validity, is explicit input with provenance; no hidden TTL renewal.
Only one project/store and optionally one explicitly approved local-bare destination/ref are supported.
No reading from destination strings embedded in notes. No network required for local continuity.

Provenance must identify how evidence reached this invocation. Initially acceptable production
observation provenance is a result returned directly by the accepted collector in the trusted
owner-controlled caller's current execution, bound to its exact canonical bytes and request.
This is the existing trusted Python caller boundary, not protection against hostile same-user code.
An imported JSON field saying LOCAL_OBSERVATION, a hash, timestamp or caller-written source label
cannot establish that delivery. Serialized/offline evidence without independently established
provenance may be analyzed as attributed history but cannot supply a current external proof.
Synthetic fixtures use an explicit test-only provenance mode and never assert real-project YES.
No cryptographic signing/key infrastructure is required or implemented here.

Strict validation must reject unknown versions/fields/enums, duplicate keys, booleans as numbers,
unsafe/ambiguous identities, invalid references, oversized data and contradictory derived output.
Missing optional capability evidence becomes UNKNOWN; malformed required evidence is not silently
converted to a valid empty snapshot. Unsupported input returns a fixed validation refusal, no YES
result. Valid failed observations yield a valid verification result with affected obligations UNKNOWN.
A failure to observe is different from an observed policy violation.

## 3. Exact actions and preservation scope

The initial verifier implementation profile is intentionally small. An action names what is being
continued, not what a caller hopes will eventually happen.

| Action | Exact scope / applicability | Initial proof availability |
|---|---|---|
| READ_ONLY_ANALYSIS | Analyze the already captured, validated in-memory evidence for the bound project/window; no further repository reads, command execution or writes; quote uncertainties as such | Existing trusted collector evidence can suffice for this narrow scope |
| CONTINUE_EDITING | Proposed bounded file edits against named base/content/context, preserving unrelated work | Quiescence and complete review/context proof are not currently produced |
| RUN_TESTS | A named bounded test plan; tests may write files or run arbitrary code and are not read-only by assumption | Needs separate accepted execution/input/environment policy; no runner supplied here |
| CREATE_CHECKPOINT | One exact selection under the accepted checkpoint adapter's constraints | Existing staging, unsupported hooks/layouts and other adapter refusals remain hard constraints |
| PUBLISH_CHECKPOINT | One existing commit/history to one approved existing local-bare ref | Existing source/history/destination/forward-update constraints remain; no network transport |
| REPAIR_KNOWN_FAILURE | Reserved category requiring a separately accepted repair plan | Unsupported; UNKNOWN, never generic repair authority |

READ_ONLY_ANALYSIS is explicitly NOT “all read commands are safe,” “resume editing,” or “the
repository is quiescent.” Adding fresh reads requires a new permitted collection, then verification.
Its YES does not certify contents of files never collected. A dirty tree can be accurately analyzed;
a clean tree does not prove a mutation scope safe. No action is inferred from saved NEXT_EXACT_ACTION.

Levels are requirements about state already preserved at verification time, not promises to produce
that level later. Thus CREATE_CHECKPOINT may start with HANDOFF_ONLY; PUBLISH_CHECKPOINT normally
requires LOCAL_CHECKPOINT. Requesting REMOTE_VERIFIED before the remote matches fails that level;
the verifier must not silently lower it. The desired outcome of a future action is separate.

| Level | Required established evidence (P11) | Exclusions |
|---|---|---|
| HANDOFF_ONLY | Valid current collector readback of project-bound continuity generation/slot digest; initial/final reference agreement; requested captured continuity facts trace to that read | No source backup, completed checkpoint or full historical-intent attribution implied |
| LOCAL_CHECKPOINT | HANDOFF_ONLY plus independently observed exact designated commit/type/tree and relevant parent/base relation; declared saved scope accounted for | No claim that unselected dirty work is saved; commit existence does not prove adapter completion |
| REMOTE_VERIFIED | LOCAL_CHECKPOINT plus fresh approved local-bare identity/ref/type observations, local checkpoint = local tracking = live ref = direct ref, repeated stable reads | No object-presence shortcut, synthetic receipt upgrade, fetch/tracking update or new publication receipt |

A projection summary can support captured continuity facts from trusted collection; requesting
full handoff content coverage requires the separately validated actual handoff, not inference from
its summary/digest. Missing designated commit/base/input evidence is UNKNOWN, not invented intent.

## 4. Proof obligations and action policy

Each obligation carries ID, plane, requiredness, subject/scope, status, evidence references and fixed
reason. Status vocabulary: **SATISFIED / UNSATISFIED / UNKNOWN / NOT_APPLICABLE**.
NOT_APPLICABLE requires an explicit action-profile rule; the caller cannot switch obligations off.
UNSATISFIED requires positive, valid evidence of a rule violation. Missing provenance/coverage is UNKNOWN.

| ID | Plane | Satisfaction condition; material failure or gap |
|---|---|---|
| P1 | Evidence | Requested project identity matches trusted observations, supported layout/config and explicit binding; observed different identity is UNSATISFIED, unavailable identity UNKNOWN |
| P2 | Evidence | Relevant state has coherent bounded observations and declared coverage; changes/races prevent claiming a stable current state; opaque digests alone cannot prove omitted content |
| P3 | Evidence | Quiescence sufficient for the requested action under section 6; NOT_APPLICABLE only for analysis of captured inert data; unresolved process coverage UNKNOWN |
| P4 | Evidence | Relevant pending intent explained without fabricated completion; for analysis, faithful presentation of incomplete intent satisfies explanation, not resolution for mutation |
| P5 | Evidence | Designated checkpoint relationship established when level/action depends on it; no backfilled adapter receipt; otherwise NOT_APPLICABLE |
| P6 | Evidence | Relevant publication state explained, keeping history and present ref observations separate; outside local-only scope NOT_APPLICABLE |
| P7 | Evidence | Fresh remote identity/ref/type and comparison where requested level/action requires it; NOT_QUERIED then UNKNOWN, observed different expected ref UNSATISFIED |
| P8 | Evidence | Fresh applicable review event/content/context coverage for proposed changes/history under section 7; analysis NOT_APPLICABLE |
| P9 | Evidence | Test policy accounted for under section 8; analysis may preserve reported PASS with UNKNOWN applicability, without requiring current PASS |
| P10 | Evidence | No unresolved contradiction material to the requested conclusion; contradictory evidence of uncertain truth is UNKNOWN, not selectively resolved |
| P11 | Evidence | Exact required preservation level established by section 3; missing proof UNKNOWN, positive contrary facts UNSATISFIED |
| P12 | Authority | Current project/action/state-scoped authority independently checked; NOT_APPLICABLE to mutation for captured analysis; missing authority UNKNOWN, explicit denial UNSATISFIED |

**P12 is a separate execution gate, not an evidence-plane YES obligation.** This explicitly
refines the future-layer reading of reconciliation section 9 item 7: any actual new mutation
still needs NEW authority and review; neither inspection nor a verifier grants it. The existing
reconciler/attempt/adapter behavior is unchanged. P8 evaluates review applicability; P12 evaluates
permission. An evidence YES with P12 UNKNOWN is possible and MUST say authority is required.
No future executor may proceed from that combination. Authority revocation changes P12/decision,
not historical evidence truth. This separation avoids both inherited authority and a misleading
claim that unavailable permission makes otherwise known repository facts unknown.

Initial fixed profiles (versioned in implementation, never inferred from notes): analysis uses
ACCOUNT_ONLY test policy; repository mutation requires an explicit supported policy stating whether
current applicable PASS is mandatory or known failures are permitted for the named scope. Omitted
mutation test policy is UNKNOWN. Such a policy cannot waive adapter restrictions or quiescence.


- READ_ONLY_ANALYSIS: P1/P2/P4/P9/P10/P11 required; P5 required at LOCAL_CHECKPOINT or above;
  P6/P7 required at REMOTE_VERIFIED; P3/P8/P12 NOT_APPLICABLE. P2 means coherent captured facts,
  not a current content snapshot. Initial implementation requires OBSERVED collection and stable
  identity/handoff references; it does not issue YES from a refused collection.
- CONTINUE_EDITING / CREATE_CHECKPOINT: P1–P4, P8–P11 required; P5 required for checkpoint creation
  or LOCAL_CHECKPOINT level; P6/P7 only when remote level is requested. P12 is required execution gate.
- PUBLISH_CHECKPOINT: all P1–P11 required, P12 required execution gate. P8 covers entire reachable
  history and destination, not just selected-file hashes. Current source must meet existing clean
  source and adapter constraints. Unknown ancestry or omitted adapter-policy evidence stays UNKNOWN.
- RUN_TESTS: P1–P4/P9–P11 required; P5–P7 according to level. P8 is required review of the explicit
  execution plan/input/output scope, not proof that the unexecuted tests pass. P12 required gate.
  Without a supported test-plan profile, P8/P9 UNKNOWN; no invented default command or sandbox.
- REPAIR_KNOWN_FAILURE: unsupported profile; UNKNOWN with scope blocker, no YES or execution.

All repository-touching profiles also require applicable adapter restrictions as P2/P8 subclaims
(hooks, attributes, hidden index flags, nested/worktree/submodule coverage, path/layout/config,
staging and publication ancestry/destination rules). Current projection omits some of these facts:
there is no inference of their absence. Additional accepted evidence is a future dependency.
The minimal verifier may evaluate supplied evidence gaps but cannot claim those profiles implemented
as executable workflows. A caller-supplied policy cannot waive hard safety restrictions.

## 5. Composition, uncertainty and decisions

For one supported indivisible action, apply these rules in order after input validation:

1. Any required evidence-plane UNSATISFIED gives NO; retain every UNKNOWN alongside it.
2. Otherwise any required UNKNOWN gives UNKNOWN.
3. Otherwise all required evidence obligations SATISFIED, and every omission justified as
   NOT_APPLICABLE, gives YES. No voting, score, probability or optimistic aggregation.

Conflicting untrusted accounts do not create positive UNSATISFIED. A directly observed lock
violates the accepted checkpoint “no foreign Git locks” rule and can give NO even if its owner
is unknown. A missing process observer gives UNKNOWN. Requested versus freshly observed different
project identities give NO; incomplete identity observation gives UNKNOWN.

PARTIAL is allowed only for an explicitly requested set of 2–6 independent action scopes evaluated
individually, with at least one YES and at least one NO/UNKNOWN. Report each child's exact level
and verdict. No unsafe dependent sequence may be decomposed (editing then publishing is a sequence,
not independently safe subsets). All YES gives YES; no YES gives NO if any child is NO, else UNKNOWN.
A single action never yields PARTIAL. No implicit downgrade of action, preservation level or coverage.
The first implementation may support only one action and refuse compound requests explicitly;
compound PARTIAL acceptance is a later bounded extension, not required to ship a single-action core.

UNKNOWN resolution class (closed conceptual vocabulary):

| Class | Meaning / typical missing evidence |
|---|---|
| RESOLVABLE_NOW | A permitted bounded existing local observation can supply it; still not automatically run |
| RESOLVABLE_WITH_COST | New scoped test execution or substantive bounded analysis is needed; no fabricated time/token estimate |
| REQUIRES_EXTERNAL_EVIDENCE | A distinct approved remote observer, trusted producer or missing provenance is required |
| REQUIRES_HUMAN_REVIEW | Content/context, intended scope or changed history needs explicit review |
| IRREDUCIBLE_UNDER_CURRENT_SCOPE | No currently accepted producer/model covers it; not globally unknowable |

Each blocker states exact missing subject/claim, evidence needed, class and scope limitation.
When several dependencies are missing, list separate blockers. Classification follows the required
producer, not an optimistic guess: an unimplemented quiescence source is IRREDUCIBLE_UNDER_CURRENT_SCOPE;
a supported local observation not yet taken is RESOLVABLE_NOW. Evidence trust depends on provenance,
relevance, validation and scope, never age, newness or repetition alone. More valid relevant evidence
may reduce uncertainty; new conflicting evidence may increase it. Missing evidence must not increase
certainty. Removing a redundant equivalent source can leave a claim unchanged only with an explanation.

Decision plane uses **NO_ACTION_REQUESTED / AUTHORITY_REQUIRED / REFUSED / ACCEPTED_RISK** initially.
A valid verification result does not emit “authorized to execute.” Captured analysis reports
NO_ACTION_REQUESTED (no mutation requested). Mutation requests normally report AUTHORITY_REQUIRED,
even if current authority evidence was supplied: an executor must independently revalidate it.
Explicit denial or an unwaivable known violation reports REFUSED. Unsupported/missing evidence alone
is not relabeled a known unsafe state; it blocks execution while verification remains UNKNOWN.

ACCEPTED_RISK is retained as future decision semantics only, not a proof state or runtime capability.
A separately validated current decision must bind project, exact action/selection, expected state,
named uncertainty IDs, principal/policy provenance, bounded validity/scope and revocation condition.
It cannot transfer to another action/agent/invocation, waive a known hard refusal, authorize prohibited
repair or count as P3/P8/P9 proof. UNKNOWN + ACCEPTED_RISK remains UNKNOWN; “proceed under accepted
risk” is an external decision requiring separate authority/execution policy, never an engine command.
Invalid/expired/revoked decisions cannot become ACCEPTED_RISK. The initial verifier only reports
NO_ACTION_REQUESTED/AUTHORITY_REQUIRED/REFUSED; risk-decision ingestion is NOT_STARTED and separate.

## 6. Quiescence: what can actually be proven

Define QUIESCENT_WITHIN_ACCEPTED_SCOPE as positive coverage of potential writers relevant to the
specific action, for a stated observation interval and owner-controlled repository. It is not
“no process anywhere can mutate.” Repeated HEAD/index/config/handoff identities support stability
but cannot independently discharge P3. Lock/PID absence and available flock are not coverage.
Neither elapsed time nor SIGKILL of the old parent establishes descendant termination.

For a future positive producer, require ALL:

1. Exact project/Git identities, relevant mutation domains and observation interval.
2. Trusted operation provenance with stable process identity (PID plus start/boot identity or
   equivalent non-reuse handle), complete known descendant coverage and observed terminal state.
3. Explicit finite writer coverage: explain how relevant owner-controlled editors, CGC/Git workers,
   background tools and destination writers are accounted for. Missing/escaped descendants,
   unknown writers or uncertain coverage remain UNKNOWN. A declaration “nothing running” alone
   is not proof. No full-machine scan is proposed.
4. No unresolved Git lock/operation marker, unexplained pending operation or conflicting observation;
   stable repeated relevant repository/store/config observations over that interval.
5. Provenance accepted for that coverage model; expiry on writer launch, state/scope change or lost
   observer continuity; fresh execution-boundary exclusion/revalidation remains required.

No existing V3 producer meets items 2–3 for general resumed mutation. Current P3 is UNKNOWN there;
future producer design/acceptance must precede claiming SATISFIED. An isolated test harness can
supply synthetic complete-writer evidence to test composition but cannot prove production coverage.
A known retained Git lock gives an explicit adapter refusal without guessing whether it is stale.
No automatic orphan kill, lock deletion, process supervisor or repair is specified.

Captured READ_ONLY_ANALYSIS does not touch the live repository, so P3 is NOT_APPLICABLE with reason
OUTSIDE_REQUESTED_SCOPE. This is the one presently supportable YES scope, not a quiescence loophole
for additional file reads or edits. If analysis needs facts outside the captured coverage, obtain a
new bounded collection under existing inspection scope; the previous YES does not authorize it.

## 7. Review proof and persistence decision

Separate PATH_IDENTITY, CONTENT_IDENTITY, REVIEW_EVENT, REVIEW_SCOPE and AUTHORITY. For P8:

- Require explicit current review provenance/event, exact project/base commit, selected relative
  paths and operations (deletion explicit), raw SHA256 and file mode, declared context/input scope,
  review time and applicable requirement/policy version.
- Compare fresh bytes/modes, base, and every declared context dependency, including relevant neighboring
  inputs or generated inputs. Missing dependency coverage UNKNOWN; known changed context STALE and
  a current-review requirement is UNSATISFIED until reviewed again. A digest alone is not an event.
- Review coverage must be appropriate to the action. Proposed future edits cannot be pre-approved as
  reviewed output: approval concerns the edit plan/start state; eventual checkpoint needs new review
  of the produced changes. Publication additionally needs entire reachable-history/destination review.
- Current `review_applicability=CURRENT` discharges only content comparison within collector coverage,
  not this stronger contextual P8. Old paths, Git object IDs and present trees never reconstruct approval.

Continue requiring fresh review/digests after uncertain interruption. Durable review persistence is
a useful later optimization, **not the next dependency**: it would preserve historical identity and
review context but cannot create quiescence, provenance or current authority. Candidate future receipt:
version, project/base, path, operation, SHA256, mode, provenance/time, declared context and policy.
It needs a separate versioned schema/producer, deterministic sorted serialization, explicit absence,
no-follow/path restrictions, private storage and compatibility acceptance. No schema extension now.
Reuse 64 paths, 2,048 characters/path, 1 MiB/file, 4 MiB aggregate collection budget; bounds include
repeated reads. Never persist file contents. Paths/hashes may leak private names or guessed low-entropy
content; hashes are not secret-free by definition. No credential collection or automatic export.

## 8. Test proof and receipt decision

P9 is “tests accounted for under the exact action policy,” not “all tests pass.” For captured analysis,
retain historical results and explicitly UNKNOWN applicability; that accounting can satisfy P9.
For a policy requiring current PASS before checkpoint/publication, legacy notes cannot satisfy it.
RUN_TESTS may start from a known failure; future diagnosis/repair must not rewrite history as PASS.
No test policy is guessed from free text; absent required policy/input scope is UNKNOWN.

A future reusable receipt must bind: version; project identity; HEAD/branch/tree; semantic index;
declared worktree/untracked/generated input paths, bytes/modes and dependency manifest identities;
exact argv/cwd; exit code, result and counts when available; start/end state observations; finite
allowlisted environment/tool/dependency fingerprint; trusted execution provenance; test-policy scope.
Capture changes during execution explicitly: no applicable PASS from an unstable tested-input set.
Do not dump the environment, capture credentials, crawl the machine or imply universal reproducibility.
Nondeterministic/external dependencies need explicit coverage; absent coverage stays UNKNOWN.

Future claim vocabulary is scoped to this proof, not a replacement for existing test enums:

| Claim | Required proof |
|---|---|
| CURRENTLY_APPLICABLE_PASS | Trusted completed PASS/exit semantics; all declared and policy-required dependencies freshly match within accepted coverage |
| STALE_PASS | Historical PASS with a known relevant input/environment/command/policy mismatch |
| HISTORICAL_PASS_WITH_UNKNOWN_APPLICABILITY | PASS reported but provenance, binding or current comparison incomplete |
| CURRENT_FAILURE | Trusted failure with applicable current bindings; known failures preserved independently |

Historical failure without current binding remains historical failure/UNKNOWN applicability.
Missing counts are unknown, not zero. HEAD/timestamp equality is insufficient. All required test
receipts must satisfy policy; one PASS cannot mask another failure/unknown. Receipt parsing and
production require separate acceptance; **NOT_STARTED**, not required for the first captured-analysis
verifier. It is a later dependency for scopes requiring current test proof. No automatic test rerun.

## 9. Preconditions, output and bounds

A YES binds project P, action A, level L, exact evidence digest/generation G, policy version and
observation window W. It is not permanent. Future execution must recheck applicable project/Git
identity, HEAD/branch/tree, semantic index, relevant work/context/modes, config, handoff generation,
review/test bindings, quiescence coverage, remote identity/ref/tracking and current authority under
its accepted mutation boundary. Any relevant change invalidates reuse: return to observation and
verification, no silent retry or repair. Revalidation narrows TOCTOU; it cannot promise exclusion of
hostile/noncooperating writers. A boolean can_mutate cannot bypass expected-state comparison.

Conceptual new result groups below are **specified, not implemented runtime schema fields**.
Implement one strict separately versioned projection; do not modify reconciliation or handoff schema.

| Group | Meaning / field class |
|---|---|
| verifier_version, policy_profile | Supported semantic rules/version, SEMANTIC_INPUT |
| request | Project/action/level/selection/expected state, SEMANTIC_INPUT |
| evidence | Validated reconciliation plus optional explicit proof bundles/provenance/window, SEMANTIC_INPUT; referenced inherited derived fields retain their DERIVED_FIELD role |
| proof_obligations | P1–P12 statuses, requiredness, references/reasons, DERIVED_FIELD |
| blockers, unknowns, resolution_plan | Unmet proof dependencies with scope/class/next observation, DERIVED_FIELD |
| safe_to_resume, decision_state, authority_required | Separate evidence verdict and decision/gate explanation, DERIVED_FIELD |
| mutation_allowed, automatic_mutation_authorized | Fixed false capability boundary of this observational verifier, DERIVED_FIELD |
| preconditions_for_future_action | Exact state bindings needed at use; inert, DERIVED_FIELD |
| non_influence_reasons | Justifications tied to changed field/claim/fixture, DERIVED_FIELD |
| next_exact_action | Highest-priority safe resolution item or no further action for this captured scope, DERIVED_FIELD |
| presentation_annotation | Optional inert quoted label only, NON_SEMANTIC_METADATA; initial implementation may omit it |

Semantic “window” is evidence provenance, not a decoration. Raw notes/argv/results are inert and
only a validated fixed field may have declared proof influence. Command text never executes.
No blanket arbitrary JSON evidence bag. Every concrete leaf must be registered before schema entry.
Strict validation recomputes all derived fields from validated inputs; no imported verdict is trusted.
No implicit migration, automatic source lookup or writing of a new preservation/resume receipt.
The existing lifecycle requirement for a future PRESERVED record remains separate: a verifier result
is not that lifecycle transition or a self-authorizing resume_digest.

Initial pure verifier bounds: one action; 12 obligation rows; at most 64 blockers/resolution/precondition
entries per list; 64 supplemental evidence references; 2,048 characters/string; 64 review paths;
64 test command/result entries; depth at most 32; canonical input/output each at most 512 KiB
(includes up to 256 KiB existing reconciliation, bounded supplements, no duplicated raw logs).
Overflow/unknown fields fail explicitly without truncated all-clear. No subprocess/I/O budget is
needed for pure evaluation: zero I/O. Any future collector uses existing 48-command/60-second,
5-second/256-KiB command and content/metadata bounds, never a second hidden budget. No hard CPU/RSS
claim; tests must exercise maximal accepted shapes. Full raw handoff up to 2 MiB is not embedded:
independently validated evidence is referenced/minimized or the requested scope is unsupported.

Human rendering derives from this exact validated result: “YES for analysis of this captured report;
repository mutation is not authorized; process quiescence not assessed for this action.” For UNKNOWN,
show missing proof, its resolution class and next action. Quote all historical free text/paths; no
text from notes, test output, commit messages, repository or previous agents becomes current instructions.
Structured validity itself is not authority. Future AI views must preserve these trust labels.

## 10. Semantic dependency registry and tamper acceptance

Every concrete input/output leaf (including nested optional/list elements) must declare one class:
SEMANTIC_INPUT, DERIVED_FIELD or NON_SEMANTIC_METADATA. Schema admission requires a complete registry;
unclassified fields are a validation/design failure. Semantic entries declare dependent_claims,
allowed_influence_scope, coherence_group and allowed_non_influence_reasons. Derived entries declare
all derivation_sources; metadata cannot affect proof, decisions, ordering or authority.

The following normative group map must be expanded to concrete leaves during implementation;
it is not permission for undocumented wildcard behavior. Downstream verdict/resolution/precondition
changes follow only through listed obligations and explicit aggregation edges.

| Semantic input group | Direct dependent claims | Coherence group / required relationships |
|---|---|---|
| Rule version, requested action/level/policy | Requiredness P1–P12, supported scope, aggregation/authority requirement | Request: exact single project, action and policy applicability; no caller-chosen N/A |
| Project identity, layout/config coverage, provenance | P1/P2; provenance of every referenced obligation | Identity: request and both observations, explicit old/current distinction |
| Local HEAD/branch/commit/tree/parents | P2/P4/P5/P10/P11; P8/P9 only through declared base dependencies | Local: current HEAD commit evidence, expected relation and canonical references |
| Semantic index, relevant work/context identities | P2/P4/P8/P9/P10; P3 stability component | Index: entries/modes/stages/flags and canonical digest; review/test declared input coverage |
| Handoff generation/digest/slots/intent/receipts | P2/P4/P5/P6/P10/P11 | Durable: slot references, generation order, summary/full-record reference, original history preserved |
| Locks, operation markers, trusted process/writer coverage | P2/P3/P4/P10 | Quiescence: project/process identity, interval, descendant/coverage evidence; absence is not coverage |
| Remote request/identity/expected tip/direct/live/tracking | P6/P7/P10/P11; P3 only if destination writer coverage supplied | Remote: same ref/identity, comparisons and repeated observations; historical/current kept separate |
| Review bytes/modes/event/base/context/provenance | P8; P10 on relevant disagreement | Review: exact path coverage, deletion absence, raw hashes distinct from Git OIDs, context bindings |
| Test execution/input/environment/argv/result/provenance | P9; P10 on relevant disagreement | Tests: execution/result semantics and complete declared binding; current versus past distinct |
| Authority scope/decision/revocation/validity | P12 and decision/authority requirement only; never P1–P11 | Authority: request/project/state/principal/window; serialized description is not permission |
| Risk decision and covered blocker IDs (future) | Decision only, never evidence verdict or P1–P11 | Risk: exact current request/unknown references/expiry/revocation; no hard-refusal waiver |
| Observation/evaluation times | Evidence applicability only where interval/decision validity uses time | Window: original observation time retained, explicit caller/producer provenance, no freshness by repetition |

Preserved notes are context; their text does not resolve P4 or select an action. Structured phase,
receipts and validated observations support P4. Non-semantic free text may change the quoted view
but not the semantic projection. Evidence-reference digests can change for serialization reasons
without claiming altered factual truth; dependency tests must distinguish reference identity and value.

Mandatory future generic harness:

1. Start with valid coherent fixtures and enumerate every registered leaf, including missing/nullable,
   empty/nonempty and bounded-limit forms. Record complete semantic output, not just next_exact_action.
2. COHERENCE_BREAKING: alter one coupled field while retaining an incompatible dependent value or
   derived claim. Reject inconsistent index digest, review path coverage, direct/live equality claims,
   slot/generation references, stale asserted SATISFIED or forged derived verdict.
3. COHERENCE_PRESERVING: change the full coupled set to another valid input, recompute integrity
   references using fixture constructors, then classify. Validator MUST accept the resulting correct
   projection. Dependent facts/reasons/obligations change as declared; unrelated claims stay unchanged.
   Merely copying changed input into output is not enough to satisfy the dependent-claim test.
4. Compare all semantic facts, freshness, contradictions, secondary reasons, obligations, verdicts,
   decisions and preconditions. A higher-priority issue may keep the same headline action.
5. Detect under-coupling (declared influence absent without justification) and over-coupling (unrelated
   claims change outside documented cascade). A validator rejecting all variants fails acceptance.

**Race clarification:** first/second remote observations disagreeing can be a valid report of a real
race in the accepted reconciler. Do not change that validator to reject truthful evidence. A tampered
report that still claims CURRENT/SATISFIED/equality is rejected; a coherent race report is accepted
and produces UNKNOWN for the affected stable-state proof. Direct/live disagreement inside one
purported successful atomic comparison remains invalid under the current projection schema.
Validity, evidence truth and satisfaction are separate. Unsupported provenance cannot be repaired by
recomputing a hash in a production caller; synthetic harness mutations test semantics only.

Closed non-influence reason vocabulary:

- OUTSIDE_REQUESTED_SCOPE: domain not required for this exact action/level; retain its facts.
- SUPERSEDED_BY_CURRENT_OBSERVATION: old claim cannot override current same-subject proof; retain history.
- DUPLICATE_EQUIVALENT_EVIDENCE: removing/reordering redundant identical coverage leaves proof intact.
- SAME_PROOF_CLASS: a valid change stays within one defined predicate (two different changed digests
  both fail equality); facts/references still change. Required to avoid impossible “every value changes verdict.”
- SUBSUMED_BY_HIGHER_PRIORITY_CLAIM: permits unchanged aggregate/headline only; never hides changed domain proof.
- NON_SEMANTIC_METADATA: reserved for registered metadata, never an excuse for ignored semantic input.

Each explanation binds changed leaf, unaffected claim and predicate/scope rationale. No blanket
explanation can waive all dependent-claim tests. Unexplained semantic no-op is a validator/classifier
defect. Version changes require updated dependency and discrimination acceptance.

## 11. Resolution ordering and future acceptance

Keep one next_exact_action plus bounded resolution_plan. Rank by existing reconciliation priorities:
unsafe/mismatched target; unreadable required continuity; active mutation/locks; conflicting Git facts;
review/test bindings; required remote evidence. Add unsatisfied current authority after evidence work
for requested mutation only; otherwise no action for this scope. Within a category sort domain,
subject/path and fixed reason. Resolution class does not override safety priority; no numeric cost.
Each item names an observation/review to obtain, not an executable command or automatic approval request.
Unsupported-profile/provenance failures belong to target/scope priority. Quiescence evidence work is
mutation priority. Proof obligations outside requested scope remain visible as N/A without forced work.

All cases below are **SPECIFIED / runtime tests NOT_STARTED**. E = evidence plane, A = authority plane.
Unless overridden, assume remaining required obligations satisfied with accepted provenance; mutating
positive fixtures use explicit synthetic future proof, never claim existing producers provide it.
For mutation cases without supplied authority, A=P12 UNKNOWN, decision AUTHORITY_REQUIRED. Analysis
has P12 N/A, decision NO_ACTION_REQUESTED. A known unwaivable violation instead sets decision REFUSED.

| Case | Fixture / obligations | Expected safety / decision / authority | Resolution class / next exact action |
|---|---|---|---|
| A | Clean reconciled local captured analysis, HANDOFF_ONLY; P1/P2/P4/P9/P10/P11 satisfied | YES / NO_ACTION_REQUESTED / no mutation authority needed | None / no further action within captured scope |
| B | Proven live mutation relevant to proposed checkpoint, P3 UNSATISFIED | NO / REFUSED / fresh authority cannot waive | RESOLVABLE_WITH_COST / establish completion under separately scoped observation, never kill |
| C | Unresolved index.lock, checkpoint policy P2 UNSATISFIED, owner unknown P3 UNKNOWN | NO / REFUSED / no lock override | REQUIRES_HUMAN_REVIEW / establish lock ownership without deleting |
| D | Parent-death history, no lock, incomplete child/writer coverage P3 UNKNOWN | UNKNOWN / AUTHORITY_REQUIRED / fresh required | IRREDUCIBLE_UNDER_CURRENT_SCOPE / define accepted bounded quiescence evidence |
| E | Missing current review/event/context P8 UNKNOWN for checkpoint | UNKNOWN / AUTHORITY_REQUIRED / fresh required | REQUIRES_HUMAN_REVIEW / obtain current scoped review |
| F | Matching digests only leaves P8 UNKNOWN; matching fresh event/base/context and bytes satisfies P8 | UNKNOWN for digests only; YES with all other E proof / AUTHORITY_REQUIRED / fresh required | Human review for missing event; otherwise validate authority at use |
| G | Policy requires PASS; legacy PASS with unknown binding P9 UNKNOWN | UNKNOWN / AUTHORITY_REQUIRED / fresh required | IRREDUCIBLE_UNDER_CURRENT_SCOPE / establish supported test-receipt producer |
| H | Fully bound trusted applicable PASS satisfies P9 | YES if all E satisfied / AUTHORITY_REQUIRED / fresh required | None for tests / validate authority at use; synthetic future fixture |
| I | Known changed test dependency, required current PASS P9 UNSATISFIED | NO / REFUSED / fresh test authority separate | RESOLVABLE_WITH_COST / request separately authorized tests for current inputs |
| J | REMOTE_VERIFIED analysis with remote NOT_QUERIED, P7/P11 UNKNOWN | UNKNOWN / NO_ACTION_REQUESTED / explicit read scope needed | RESOLVABLE_NOW for approved available local-bare read, otherwise REQUIRES_EXTERNAL_EVIDENCE / obtain scoped remote observation |
| K | Current local/tracking/live/direct equality at approved commit, P5–P7/P11 satisfied | YES for otherwise complete REMOTE_VERIFIED captured analysis / NO_ACTION_REQUESTED | None / no further action within scope; no new publication receipt |
| L | Historical VERIFIED A, current remote C, required preservation of A P7/P11 UNSATISFIED | NO / REFUSED / no permission to restore A | REQUIRES_HUMAN_REVIEW / explain remote movement, retain history |
| M | Conflicting credible required-domain observations, P10 UNKNOWN | UNKNOWN / AUTHORITY_REQUIRED for mutation | RESOLVABLE_NOW if bounded new comparison exists / collect coherent evidence, no selective choice |
| N | Required observation timeout/permission failure, P2 UNKNOWN | UNKNOWN / NO_ACTION_REQUESTED for analysis | RESOLVABLE_NOW if permitted source available / report failed observation and request bounded follow-up |
| O | Positively observed project identity mismatch P1 UNSATISFIED | NO / REFUSED / no inherited scope | REQUIRES_HUMAN_REVIEW / confirm exact target; never rebind automatically |
| P | Perfect-looking analysis fixture, explicit full required proof chain below | YES / NO_ACTION_REQUESTED / P12 N/A | None / no action for captured analysis; no repository-wide safety claim |
| Q | CONTINUE_EDITING all E proof satisfied, current authority absent P12 UNKNOWN | YES / AUTHORITY_REQUIRED / mandatory before execution | REQUIRES_HUMAN_REVIEW / establish current scoped authority; no execution |
| R | Prior YES, relevant state changes before mutation | Old proof stale; new mismatched precondition UNSATISFIED gives NO / REFUSED | RESOLVABLE_NOW / recollect and reverify; no retry under old result |
| S | Evidence UNKNOWN plus valid future scoped risk decision | UNKNOWN / ACCEPTED_RISK / separate current authority still required | Underlying blocker class unchanged / preserve missing-proof resolution; no bypass |
| T | Coherence-breaking mutations with stale derived claims | Validation REJECTED; no valid safety/decision output | Correct malformed evidence, no default false/YES |
| U | Coherence-preserving valid mutations | Validation ACCEPTED; dependent claims change or registered non-influence explains; unrelated claims stable | According to newly evaluated blockers; compare full semantic result |
| V | Explicit independent analysis YES and editing UNKNOWN requests | PARTIAL only in later compound profile; per-action decisions retained | Mutation blocker resolution; no blanket permission |
| W | Inert notes or presentation annotation contain instructions | Same proof and decision; quoted context only | No semantic next-action change |
| X | Structurally valid imported projection without trusted current provenance | UNKNOWN on relevant external proof / no execution | REQUIRES_EXTERNAL_EVIDENCE / obtain accepted current provenance/collection |

Perfect-looking P fixture must specify: trusted current collector call for exact root/Git identity;
OBSERVED stable first/last facts/config/handoff generation/digest; readable bound continuity containing
no unresolved fact needed to interpret the captured scope; explicit HANDOFF_ONLY level; no commit or
remote preservation claim; test policy ACCOUNT_ONLY retaining legacy applicability UNKNOWN; no live
reads/edits requested. P1 identity, P2 captured coverage, P4 faithful intent explanation, P9 truthful
test accounting, P10 no material conflict, P11 continuity readback each cite distinct evidence.
P3/P5/P6/P7/P8/P12 are N/A by that exact profile. Cleanliness is neither necessary nor sufficient:
a dirty-but-explained variant with identical required proofs must also pass. Remove required handoff
readback/provenance and verdict becomes UNKNOWN; add editing and P3/P8 become required/UNKNOWN.
A SHA-only “perfect” fixture is insufficient. No embedded inner YES is used as proof.

Additional mandatory acceptance: zero I/O and input mutation in pure verifier; deterministic ordering
and mapping-order invariance; byte-preserved reconciler result; no receipt writes; unsupported versions,
bounds/depth/duplicate-key refusals; failure/provenance and all four verdict rules; authority/risk
changes never promote E proof; expiry/revocation and state-change invalidation; all leaf dependency
coverage; shared human/machine semantics. Existing crash tests are evidence sources, not new work.
Initial single-action implementation covers A–U/W/X with unsupported future evidence explicitly UNKNOWN;
H/Q positive composition fixtures are synthetic, S risk ingestion and V compound aggregation remain
separately NOT_STARTED. Missing future producers must not be replaced by production trust booleans.

## 12. Benchmark gate and decisions

Future controlled experiment only: use identical disposable interruption end states, model/version,
task/scope and allowed tools. Randomize/counterbalance runs A without CGC projection and B with
reconciliation/verifier evidence; prevent cross-run memory leakage. Predefine correctness oracle,
resource bounds, stopping rule, sample size and failure adjudication before measuring. Include cost
of collecting/validating CGC evidence, not just agent tokens after receiving it.
Measure tokens, time to correct scoped continuation, duplicate commands/tests, wrong Git actions,
fabricated completion, unsafe recovery attempts and human interventions. Report failures and variance;
protect private data, collect no hidden reasoning or invasive telemetry. No benchmark ran and no
improvement numbers are claimed. Human time returned is a hypothesis to test, not a feature-count metric.

Decision gates:

1. **Contract ready: YES for a minimal pure external verifier**, with current-evidence captured-analysis
   YES and explicit UNKNOWN/refusal for unsupported wider proof. Future producers and execution are not
   prerequisites for honestly reporting those limits. Concrete strict schema and leaf registry/tests
   must be implemented together under this contract; no alternative safety aggregation is left open.
2. **Current V3 evidence can support YES for at least one scope: YES**, READ_ONLY_ANALYSIS of captured
   evidence at HANDOFF_ONLY under the stated trusted-call chain. No verifier exists yet; this is a
   proof-feasibility decision, not an emitted current YES or completed end-to-end safe resume.
3. **Primary mutation blocker: quiescence coverage**, followed by action-policy/coverage detail,
   contextual review and structured test bindings where required. No available flock/digest closes it.
4. **Next block: implement the minimal pure external verifier**, starting with exact single-action
   READ_ONLY_ANALYSIS/HANDOFF_ONLY proof, strict semantic dependency registry and discriminating tamper
   tests. Wider mutation verdicts retain UNKNOWN where proof is unavailable. This provides a useful
   evaluable proof graph before adding optional persistence or new evidence producers.

Durable review persistence is deferred: fresh review remains the accepted approach. Structured test
receipts and positive mutation-quiescence producers need separate later contracts/acceptance, selected
from actual proof blockers. No implementation is authorized by this document alone. No executor,
risk-decision runtime, recovery, automatic tests, authority inheritance, networking or V4 work begins.

RECONCILED != SAFE_TO_RESUME. SAFE_TO_RESUME=YES != MUTATION_AUTHORIZED.
MUTATION_AUTHORIZED != PRECONDITIONS_STILL_TRUE_AT_USE_TIME.
UNKNOWN is not failure or permission. ACCEPTED_RISK is not knowledge.
The product is verified continuity and human time returned.
