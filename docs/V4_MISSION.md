# CGC V4 — INTEROPERABILITY, PORTABLE STATE & AGENT CONNECTIVITY

CREDID GUARDIAN CODEX (CGC). Working mission title and authoritative future design record.
Design status: **ARCHITECTED**. All V4 runtime components: **NOT_STARTED**.
Authorization for this record covers architecture, documentation and future acceptance planning
only. It does not authorize implementation, installation, a listener or a plugin package.

```text
V1 = OBSERVE
V2 = UNDERSTAND
V3 = PRESERVE
V4 = CONNECT

ONE VERIFIED CGC STATE
        ↓
MANY AUTHORIZED CONSUMERS
```

## 1. Version boundary and authority of this mission

[V3](V3_MISSION.md) remains the active implementation mission and is PARTIAL; its actual
frontier is recorded in [V3 progress](V3_PROGRESS.md#next_exact_action). V3 owns inspection,
handoff, checkpoint, publication, verification, crash/interruption safety, resume semantics
and human continuity. V4 consumes stable V3 state and MUST NOT redefine preservation to
mean successful export, a connected agent, an imported archive or an acknowledged event.

This mission governs future portability, interfaces, consumers and their boundaries. It
extends the [Agent Fabric relationship](ARCHITECTURE.md#agent-fabric-relationship) and retains
all [100 V3 architectural constraints](V3_MISSION.md#exactly-100-architectural-keypoints).
It neither moves unfinished V3 acceptance into V4 nor authorizes a generic Agent Fabric
runtime. Existing [V3 contracts](V3_CONTRACT.md), [data model](DATA_MODEL.md),
[preservation policy](PRESERVATION_POLICY.md) and [security model](SECURITY_MODEL.md) remain
authoritative for their domains. A conflict requires explicit reconciliation, not silent
schema migration or a client-side reinterpretation.

V4 makes CGC state portable, queryable, interoperable, agent-readable, human-readable,
multi-platform and multi-client. Candidate consumers include Codex, ChatGPT, local AI,
future cloud AI, desktop/web CGC, Android, iOS, tablets, servers, enterprise tools and other
authorized agents. This list does not assert present platform support.

CGC is the canonical state authority for its own validated evidence, not an oracle about
current external reality. Every claim retains its project, scope, provenance, observation
time, generation and uncertainty. A past remote verification is historical evidence; Git
must be observed again to establish current remote reality. Reading never creates truth.
"One verified state" means one coherent semantic source per project/authority domain,
not one global database or a claim that every field is known or independently verified.

## 2. Local-first architecture and responsibility split

The CGC core owns semantic validation and canonical evidence. Platform adapters obtain
bounded Git, filesystem and process evidence under existing policy. Local handoffs,
checkpoints and publication receipts remain usable without any plugin or cloud service.
A future bounded local service exposes selected core operations through local MCP / IPC;
transport does not define preservation semantics. Read-only access comes first.

```text
            CODEX / AUTHORIZED AGENT
                       │
                 CGC Plugin
              ┌────────┴────────┐
            Skill             MCP
              └────────┬────────┘
                       │
               LOCAL CGC SERVICE
                       │
                   CGC CORE
                       │
       local state / Git / process evidence
       handoff / checkpoints / publication receipts
```

All new boxes are ARCHITECTED / NOT_STARTED. Existing V1–V3 primitives remain their own
accepted implementations; they are not retroactively labeled a V4 service.

An optional authenticated remote gateway may later expose narrowly scoped capabilities.
Basic CGC operation must never require uploading private project state. A cloud-hosted
consumer cannot be assumed to reach local IPC: unsupported access remains unavailable
until a separately authorized gateway exists. No automatic tunnel or cloud fallback.

## 3. Skill, MCP, hooks and plugin

| Mechanism | Future CGC responsibility | Authority boundary |
|---|---|---|
| Skill | Workflow instructions: discover state, explain uncertainty, select the approved sequence, report evidence | Instructions grant no system permissions |
| MCP | Structured current/historical data with explicit provenance; separately controlled action capabilities | Connectivity grants neither write nor publication authority |
| Hook | Bounded lifecycle notification/integration, only at supported and explicitly trusted points | Notification is not authorization or guaranteed crash cleanup |
| Plugin | Thin translator, adapter and workflow distribution layer | Installation and enablement grant no project mutation permission |
| Core | Validate state and evaluate requests under the applicable CGC policy | Evidence authority is distinct from action authorization |

The plugin retrieves the verified project frontier, current attempt, risk, checkpoint,
publication/test state and NEXT_EXACT_ACTION. It may request capability decisions and,
in a later separately accepted stage, authorized actions. It never invents receipts,
recalculates independent Guardian truth or becomes the CGC brain.

Candidate conceptual tool names, **not implemented APIs or callable commands**:

```text
cgc.status()                 cgc.current_project()
cgc.current_attempt()        cgc.risk()
cgc.last_checkpoint()        cgc.publication_state()
cgc.test_state()             cgc.next_exact_action()
cgc.can_mutate()             cgc.can_publish()
```

Project discovery uses explicit trusted project/session context, never a whole-machine
search. Queries are project-scoped and bounded. Missing or stale evidence remains visible.
The last two names evaluate a concrete request against current policy; a cached boolean
is not a grant. Any later execution must revalidate authority and expected repository
state. Unsupported capabilities refuse explicitly; they do not fall back to a shell.

Hooks may notify session start, approved transitions or impending shutdown where the host
supports them. Missing, duplicate, late or reordered notifications must be tolerated without
automatic mutation. Session-end delivery and SIGKILL cleanup cannot be assumed. Recovery
still comes from durable V3 evidence, not a hook's memory or an agent conversation.

## 4. Plugin packaging and external platform compatibility

Candidate distribution shape, not files created by this task:

```text
cgc-plugin/
├── plugin.json
├── skills/
├── mcp.json
├── hooks/
└── assets/
```

Official OpenAI documentation reviewed on 2026-09-23 describes skills, MCP and lifecycle
hooks as plugin components, with capabilities depending on the execution surface.
See [Plugin architecture](https://developers.openai.com/plugins/concepts/plugins).
The [packaging guide](https://developers.openai.com/plugins/build/plugins) describes a
portable root manifest and a Codex compatibility layout. These are external versioned
dependencies, not immutable CGC contracts. At implementation, verify then-current official
specifications, supported surfaces, hook trust requirements and distribution rules; record
tested host/plugin versions. No listing, submission approval or account availability is claimed.

Plugin updates must not silently expand CGC capabilities. Hook code belongs in a separately
reviewed software distribution, never a state capsule. The core remains independently usable;
plugin disconnection, disablement or removal must not destroy continuity or block local use.

## 5. CGC State Protocol and V3 compatibility

Define a language-neutral, versioned protocol of inert JSON snapshots, NDJSON events,
schemas, hashes and receipts. No programming language is authoritative. Python, Rust, Go,
TypeScript, Kotlin, Swift and future languages should consume the same semantics.

The initial design must map existing records explicitly rather than invent a second
preservation model. Preserve the following without silent promotion:

| V3 evidence | Required V4 interpretation |
|---|---|
| Current/latest attempt | Separate intent, attempted action, observed outcome and failed completion |
| last_known_good / previous_known_good | Retained continuity slots; not proof of preserved project content |
| Handoff and inspection | Curated/observed scope and original schema/digests survive |
| Git/checkpoint | Observed HEAD is distinct from an operation's verified local receipt |
| Publication | Object arrival, ref update, independent verification and safe resume remain separate |
| Test evidence | Preserve command, scope, result, counts when available and relation to tested revision; missing counts remain unknown |
| NEXT_EXACT_ACTION | Inert guidance reconciled against present reality before action |
| SAFE_TO_RESUME | Preserve scope and UNKNOWN/NO/PARTIAL/YES semantics; no upgrade on import or rendering |

In particular, the current V3 handoff's outer UNKNOWN must not be replaced with YES from
an inner structurally valid attempt. A V4 adapter cannot manufacture missing V3 receipts.
Read-only observation of an accepted commit after interruption does not backfill the
interrupted operation's success result.

Future envelope requirements include schema/protocol version, explicit project identity,
source instance, generation/snapshot identifier, observation and capture times, evidence
basis, coverage, errors/uncertainty and referenced receipt identities. Re-reading does not
refresh observation time. A generation is scoped to its producer, not a global clock.
Path portability needs explicit mapping and fresh identity checks; an archived absolute
path must never select a mutation target on another machine automatically.

Define strict sizes, depth, numeric ranges, time encoding, Unicode handling, duplicate-key
rejection and canonical serialization before freezing a schema. Preserve absence versus
unknown versus known false. Unknown required fields/versions/enums must cause explicit
incompatibility, not a permissive default. Future optional extensions need a bounded
namespace and documented preservation/ignore rules; ignored data cannot influence authority.
This does not relax V3's existing exact-field validators. Migrations are explicit, tested,
non-destructive and retain originals and provenance; no in-place rewrite on read.

## 6. CGC State Capsule

Working extension: `*.cgcpack`, for example `project.cgcpack`.
Working concept: **PORTABLE VERIFIED SNAPSHOT**, meaning a snapshot carrying scoped
verification evidence, not a guarantee that all contents are true, current or safe to resume.
A capsule is neither a live CGC engine nor an executable application package.

Candidate archive contents, subject to later schema and container-format acceptance:

```text
project.cgcpack
├── manifest.json
├── state.json
├── guardian.json
├── git.json
├── checkpoint.json
├── publication.json
├── tests.json
├── authority.json
├── next-action.json
├── events/
│   └── timeline.ndjson
├── evidence/
│   ├── hashes.json
│   ├── commands.json
│   └── provenance.json
├── schemas/
│   └── cgc-state-v1.schema.json
├── integrity/
│   ├── SHA256SUMS
│   └── signature.json
└── HUMAN-STATUS.txt
```

This is not a requirement to emit every file or a new schema filename promise. Start with
the smallest profile supported by real V3 evidence. The manifest declares required/optional
members, versions, project identity, snapshot scope, omissions and integrity coverage.
Domain files are projections/references of one canonical generation, not independent truth
stores. `authority.json` records historical decisions only; it contains no reusable grants,
credentials or bearer tokens. `commands.json` contains bounded inert evidence text.

Separate live and archival state:

```text
LIVE CGC STATE
  ├── current snapshot
  ├── event stream
  └── active evidence
          ↓ explicit bounded export
     project.cgcpack
     archival snapshot
```

Capture a coherent generation and event cutoff; concurrent changes must produce an explicit
incomplete/refused capture rather than mixed generations. A ZIP container is a candidate,
not a live event engine. Define deterministic member ordering, metadata and serialization
so identical input snapshots and export profiles produce identical unsigned capsule bytes.
Capture timestamps belong to the input snapshot; optional signatures may have separately
defined determinism. Container version, canonicalization and signature profile remain open.

### Inert import and integrity boundary

Default payload is **INERT DATA**. Do not embed executable Rust, Go, JavaScript, Python,
shell or binary programs. Import MUST NOT execute stored commands, scripts, hooks, schemas,
links or suggested next actions. An executable extension would require a separate future
design and authorization; it is not part of this mission's default capsule profile.

Bound compressed/uncompressed bytes, member count, nesting and parsing work. Reject traversal,
absolute paths, links, special files, duplicate names and platform-dependent path collisions.
Do not extract over a repository, live handoff store or existing valuable files. Validate in
isolation; failed import leaves existing state intact. Schemas bundled by an untrusted sender
cannot replace trusted validators or trigger network resolution. Rendering must escape untrusted
text; AI consumers must treat it as evidence, never higher-priority instructions.

Hashes establish covered-byte consistency, not sender authenticity or factual truth. A signature,
if supported, requires an explicit trusted signer/key, algorithm/version, signed-byte scope and
revocation policy. Unsigned, untrusted, invalid and unverifiable signatures stay distinct. No
private signing keys travel in the archive. Integrity metadata must define exclusions to avoid
self-referential hashes/signatures. Tampering, omitted required members or ambiguous coverage
must refuse verification. A valid signature does not make old data current or authorize mutation.

Import creates an isolated historical view, not replacement live state. Any later promotion,
project rebinding, reconciliation or mutation requires separate current authority and V3
verification. The capsule may describe saved work without containing its Git objects or files;
the manifest and human view must disclose that it is not necessarily a source-code backup.

## 7. Machine, human and AI representations

Machine JSON, HUMAN-STATUS.txt and AI-facing structured evidence derive from the same validated
snapshot. Verify a stored human rendering against that snapshot; a mismatch is explicit, not
silently accepted. All views retain age, scope, omissions, failed attempts and uncertainty.

The human view must answer plainly: What was saved? What was not saved? What failed? What is
uncertain? Was GitHub (or the configured destination) verified, and when? Can I safely continue?
What must happen next? "Verified at capture time; current remote not checked" is a valid answer.
An unavailable resume verdict must say UNKNOWN, not offer a misleading all-clear. Humans should
not need Git, WSL, MCP or archive internals to understand these answers.

## 8. Append-oriented event model

Candidate `events/timeline.ndjson` records factual events such as:

```text
TEST_STARTED           TEST_COMPLETED
CHECKPOINT_CREATED     PUBLICATION_STARTED
PUBLICATION_VERIFIED   PRESERVATION_FAILED
AUTHORITY_GRANTED      AUTHORITY_REFUSED
RESUME_STARTED         RESUME_RECONCILED
```

Future events need version, event ID, producer/project/attempt identity, correlation ID,
producer sequence, observed/recorded times, evidence references and bounded typed payload.
TEST_COMPLETED carries the actual result, not an assumed pass. AUTHORITY_GRANTED describes a
scoped historical decision; event receipt is never a reusable grant. RESUME_RECONCILED cannot
stand in for evidence required by V3. Missing events cannot prove that no operation happened.

Specify atomic append/capture behavior and recovery for a truncated final line, duplicates,
gaps, out-of-order delivery and crashes. Preserve incomplete-tail diagnostics; no silent repair
or successful projection from invalid history. Do not claim global order or exactly-once
delivery. Snapshots and event cutoffs must agree; the stream transports observations, not an
independent authority ledger or a second mutation engine. Retention/export requires explicit
bounds and privacy policy, not indefinite collection.

## 9. Generated SDKs and optional portable core

```text
CGC SCHEMA → GENERATED BINDINGS
              Python / Rust / Go / TypeScript / Kotlin / Swift
```

SDKs are separate software artifacts, never implementations bundled inside each report.
Generated types alone do not enforce semantics: validators and conformance fixtures must
agree on unknown values, number precision, canonical bytes, timestamps and refusal behavior.
Do not promise all six targets at once; accept each against the same corpus when authorized.

A future split may comprise semantic core, platform adapters, protocol and clients. Evaluate
Rust for deterministic validation, hashing, schema handling or a bounded service only if
measured portability, performance or maintenance needs justify it. No mandatory Rust rewrite,
new language runtime or duplicated policy engine. Existing Python remains valid until evidence
supports a change; ports require semantic parity tests before adoption.

## 10. Capability profiles and Guardian surfaces

| Profile | Candidate capabilities | Required restriction |
|---|---|---|
| Desktop / server | Git, filesystem/process inspection, tests, checkpoint, publication, verification, Codex integration | Only supported platform adapters and separately authorized project operations; no blanket host access |
| Mobile / tablet | Status, handoff, evidence, warnings, project progress, signed capsule consumption, approve/refuse requests | App sandbox and scoped control console; no root Guardian daemon or assumed Git/process access |
| Web / agent client | Authorized projections and action requests | No ambient local filesystem authority; private data export requires approval |

A capability profile states what a device can support, not what it may currently do. Unsupported
features are explicit. Windows, Linux and macOS need their own accepted adapters; existing Linux
evidence does not establish native Windows/macOS parity. Android/iOS must respect app-scoped
storage, background limits and platform security. Desktop Guardian meter/tray becomes a
**V4 GUARDIAN SURFACE**, retaining one sensor and visible freshness/uncertainty.

A future mobile screen may show a selected project's work status, test result, saved checkpoint,
remote verification time and a specific "Publish checkpoint?" request with APPROVE / DENY.
This is a conceptual control console, not an implemented UI. Approval must bind to the exact
project, destination, revision, requested action and validity window; a changed request/state
requires reevaluation. Offline viewing does not authorize later execution automatically.

## 11. Human authority and multi-device architecture

```text
                       HUMAN / APPROVED POLICY
                                │
                           CGC CONTROL
                                │
                          CGC AUTHORITY
                                │
                 ┌──────────────┼──────────────┐
               CODEX         LOCAL AI       CLOUD AI
                 └──────── CGC PLUGIN/MCP ─────┘
                                │
                            CGC CORE
                                │
                 ┌──────────────┼──────────────┐
              LIVE STATE      EVENTS        EVIDENCE
                 └──────────────┼──────────────┘
                                ▼
                           CGC CAPSULE
                          project.cgcpack
                                │
             Windows / Linux / macOS / server / laptop
                  Android / iOS / tablet / web
```

This diagram is future architecture, not implementation status. AI may observe, explain,
recommend and request. Scoped human/policy authority controls mutation; CGC can still refuse
an authorized request when its safety preconditions fail. Control decisions remain separate
from data-plane payloads. Transport, agent identity and coordination do not confer root power.

Action requests must bind principal, capability, project/resource, arguments, expected state,
request ID, expiry and applicable policy version. Approval must be revocable and auditable;
execution rechecks authority and state within the V3 writer boundary. Cross-device duplicate,
expired or replayed approvals must not cause repeated mutation. A lost response means outcome
uncertain until reconciled, not permission to retry. Exact grant/envelope design is future work.

## 12. Privacy and optional remote gateway

Observe authorized computational work and approved project, agent, machine, checkpoint,
publication, authorization and risk state. Machine/process observation stays bounded to the
approved work. No default secret keystroke logging, personal behavior tracking, hidden employee
monitoring, private-message surveillance or continuous human profiling. Enterprise use must
preserve explicit user/org authority boundaries, data minimization, visible collection scope,
retention limits and project/tenant separation. No hidden chain-of-thought or credential capture.

The optional gateway is ARCHITECTED / NOT_STARTED. It may serve remote mobile consoles,
multi-machine/enterprise use and approved cloud agents only after earlier local phases pass.
Require authentication, encrypted transport, least privilege, capability scoping, revocation,
auditability, explicit project identity, version negotiation and replay protection. Validate
both request shape and current policy; record bounded safe diagnostics without secrets.

No blanket remote shell, arbitrary command endpoint, unbounded host control or automatic cloud
exfiltration. Local agents do not receive private state by identity alone either. Export/access
scope is distinct from mutation scope; a denied remote request cannot become a local bypass.
Disconnect/revocation must fail closed for new actions without destroying local evidence.
Keep private work local; share only necessary, explicitly authorized context. A generic enterprise
orchestrator remains separate future software, subject to the same refusal and capability rules.

## 13. Internal phases and dependency gates

Every row is **ARCHITECTED / NOT_STARTED** for V4 implementation. A phase name is not permission.

| Phase | Future scope | Entry / exit gate |
|---|---|---|
| V4.0 — CGC STATE PROTOCOL | Stable schemas, portable semantics, human status | Finish V3 preservation/resume acceptance first; explicit version/compatibility rules and round-trip corpus |
| V4.1 — CGC STATE CAPSULE | Inert export/import, deterministic capture, integrity | Accepted protocol; hostile-archive and unchanged-live-state evidence |
| V4.2 — LOCAL CGC SERVICE | Bounded local API / MCP, read-only first | Accepted capsule/protocol; scoped access and no hidden side effects |
| V4.3 — CODEX CGC PLUGIN | Skill, MCP adapter, optional trusted lifecycle hooks | Accepted local service; then-current official specifications and trust tests |
| V4.4 — PORTABLE SDKs | Selected bindings and measured portable-core experiments | Stable protocol and accepted integration; cross-language semantic parity |
| V4.5 — GUARDIAN SURFACES | Desktop, web, Android, iOS/tablet console | Accepted SDK/profile contracts; local/offline views first; remote control awaits V4.6 |
| V4.6 — OPTIONAL REMOTE GATEWAY | Enterprise, multi-device, approved cloud-agent connectivity | Accepted local capabilities/surfaces; authenticated scoped transport and replay/revocation evidence |

Order: finish V3 → stable protocol → capsule → local service/MCP → plugin → SDK/portable-core
work → desktop/mobile/web clients → optional remote enterprise gateway much later. Do not
reverse dependencies without a documented evidence-based decision and explicit authorization.
The mobile design does not smuggle an early gateway into V4.5. Every runtime milestone requires
its own bounded task and acceptance; optional platforms are never silently declared supported.

## 14. Future acceptance matrix

All checks below are **NOT_STARTED**. They define evidence required later, not tests run now.
Maintain a future implementation-to-test matrix with exact versions, fixtures, results,
limitations and COMPLETE / PARTIAL / NOT_STARTED per component and platform.

| ID | Required evidence |
|---|---|
| A01 | V3 semantics and regression evidence remain intact; no receipt or SAFE_TO_RESUME upgrade through adapters |
| A02 | Protocol round-trip retains attempts, both good slots, provenance, unknowns, failures and exact next action |
| A03 | Version mismatch, unknown required fields/enums, duplicate keys and bounds fail explicitly; optional extensions cannot grant authority |
| A04 | Identical accepted snapshot/profile yields deterministic unsigned capsule bytes; generation and event cutoff are coherent |
| A05 | Hash/member tampering, missing required members and inconsistent manifest coverage are detected |
| A06 | Signature policy distinguishes unsigned/untrusted/invalid/revoked evidence; authenticity never implies freshness or authority |
| A07 | Malicious paths, links, duplicate/colliding members, archive expansion and parser limits are tested; failed import preserves existing state |
| A08 | Import/render never executes commands, scripts, hooks, bundled schemas or prompt-injected instructions; no implicit network fetch |
| A09 | Human, machine and AI views agree, including UNKNOWN safe resume, historical remote verification and excluded source content |
| A10 | Event duplicates, missing entries, reordered delivery, truncated tails and capture interruption cannot fabricate successful state |
| A11 | Local MCP cannot exceed read/project policy, leak unauthorized data or execute unexposed capabilities; stale decisions fail on execution |
| A12 | Plugin cannot invent evidence; missing service/hooks, updates and disconnect preserve core usability and grant no authority |
| A13 | Mobile approval cannot expand target/action/destination; changed state, expired/revoked/replayed approvals and lost replies are handled safely |
| A14 | Offline CGC works without plugin, cloud or gateway; multiple consumers use the same canonical semantics without competing sensors |
| A15 | Separately accepted language/platform clients pass the same conformance corpus, including numeric/path/time edge cases |
| A16 | Privacy/export minimization, safe diagnostics and tenant/project isolation are tested with synthetic data, never real credentials |
| A17 | Optional gateway authentication, encryption, least privilege, revocation, replay protection and protocol mismatch are verified |
| A18 | Service/export/import crashes and concurrent readers preserve old/new coherent evidence; no unsafe retry, overwrite or universal SIGKILL/power-loss claim |

Feature presence, a working demo or an installable package does not satisfy these checks.
Unsupported surfaces and untested timing remain explicit. Protocol validity, integrity,
authenticity, fresh observation, action authorization and safe resume are distinct conclusions.

## 15. Human time returned and unresolved design choices

Reduce time lost finding state, translating between tools, reconstructing context, changing
devices, re-explaining work to agents, reading raw logs, resolving permissions and repeating
completed work. Future measures may include TIME_TO_RESUME, RECOVERY_TIME,
DUPLICATE_WORK_AVOIDED, MANUAL_INTERVENTIONS, TIME_TO_VERIFIED_CHECKPOINT and
HUMAN_TIME_RETURNED. No telemetry or invasive monitoring is authorized by this document.

Open decisions for separately authorized design/implementation: minimal protocol/profile and
extension rules; project identity mapping; canonical serialization/container/signature coverage;
trusted-key lifecycle; resource and retention bounds; event recovery; local transport and peer
identity; capability grant enforcement; platform matrix and measured need for a portable core.
Do not create infrastructure merely because a diagram contains a box.

## 16. Status, continuity and stop boundary

Mission definition, boundaries, roadmap reconciliation and future acceptance planning are
**ARCHITECTED**. Implementation status for V4 runtime, State Protocol runtime, capsule
exporter/importer, event stream, local service/MCP server, Codex plugin/hooks, generated SDKs,
portable core, mobile clients, desktop V4 client, web client, remote gateway and enterprise
orchestration is **NOT_STARTED**. No implementation acceptance is claimed.

DO_NOT_START_YET: any V4 runtime, package, schema implementation, MCP server, exporter/importer,
Rust/Go/TypeScript service/client, GUI/mobile app, networking, gateway or orchestration.
DO_NOT_REPEAT: accepted V3 work without defect evidence, quota discovery or speculative rewrite.

NEXT_EXACT_ACTION remains the actual V3 frontier: **audit and test active local-bare index-pack
interruption after temporary pack arrival using real Git fixtures**, subject to fresh repository
reconciliation and a new scoped task. This documentation task does not begin that block.
Future sessions must use [current V3 progress](V3_PROGRESS.md#next_exact_action), not freeze
this historical next action after newer evidence advances it.

## Core CGC platform law

```text
V1 OBSERVES.
V2 UNDERSTANDS.
V3 PRESERVES.
V4 CONNECTS.

ONE VERIFIED STATE.
MANY AUTHORIZED CONSUMERS.

THE PLUGIN IS NOT THE BRAIN.
THE CGC CORE IS THE STATE AUTHORITY.
DATA IS NOT CODE.
INFORMATION IS NOT AUTHORITY.
IDENTITY IS NOT AUTHORITY.
CAPABILITY IS NOT AUTHORIZATION.

THE MACHINE MAY KNOW.
THE AI MAY RECOMMEND.
THE HUMAN OR POLICY AUTHORIZES.

THE GUARDIAN OBSERVES. CODEX PRESERVES.
PRESERVE BEFORE EXPANDING.
COMPUTATION MAY STOP. HUMAN CONTINUITY MUST NOT.
THE PRODUCT IS NOT MORE CODE.
THE PRODUCT IS HUMAN TIME RETURNED.
```
