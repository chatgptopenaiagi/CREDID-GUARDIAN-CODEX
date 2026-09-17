# CREDID GUARDIAN CODEX (CGC) — V1 quota source discovery

Date: 2026-09-17. Starting commit: `8968cad670ce344226ebccaf4974d624594e5605` (clean main). Scope: read-only source discovery, one bounded protocol experiment and the smallest reader/normalizer. No daemon, hooks, GUI, repeated polling, direct private-backend requests or external-repository preservation.

**Result: a genuine quota source was observed through Codex app-server.** Source verification is scoped to this installed CLI/account/context and one successful read. Independent current-session `/status` correspondence remains NOT_VERIFIED; the human was asked for quota-only values and none were available at publication. Do not fabricate that comparison or issue another read to fill it.

THE GUARDIAN OBSERVES. CODEX PRESERVES.

## Evidence sources

- Installed `codex-cli 0.154.0`: bounded `--version`, top-level help, login help, app-server help, proxy help and daemon help. No login/logout/credential operation ran.
- `codex app-server generate-json-schema --out <temporary-directory-inside-CGC>`: exit 0. Generated schema inspected locally, then the temporary generated bundle was removed. This is developer tooling, not an account read. Relevant types: InitializeParams, InitializeResponse, GetAccountRateLimitsResponse, RateLimitSnapshot, RateLimitWindow, SpendControlLimitSnapshot and NullableGetAccountRateLimitsParams. No authentication files were opened.
- [Official app-server documentation](https://learn.chatgpt.com/docs/app-server): describes initialization, stdio JSONL and account/rateLimits/read; documents percentage/duration/reset fields and multi-bucket responses. It labels app-server experimental, not production-supported. This is a documented protocol, not a production stability guarantee.
- [Official developer-command documentation](https://learn.chatgpt.com/docs/developer-commands?surface=cli): login status describes authentication mode, not quota. An initial official-domain search returned unrelated API model limits; these were not treated as Codex quota evidence. Opening the separate slash-command page returned an internal documentation error; no unsupported claim was inferred.

## Candidate inventory (in requested investigation order)

### 1. Standalone Codex CLI usage command

SOURCE NAME: CLI command surface. LOCATION / INTERFACE: installed `codex --help`. DOCUMENTED OR UNDOCUMENTED: built-in supported help, with individual commands carrying their own maturity labels. READ-ONLY: help/version yes. AUTH HANDLING: no authentication required to read help. DATA AVAILABLE: no standalone quota command listed. RESET INFORMATION: unavailable here. WINDOW INFORMATION: unavailable here. FRESHNESS: installed 0.154.0 help. STABILITY: version-scoped. SECURITY RISK: low for help only. SUITABILITY FOR CGC: not a quota source; no invented `codex usage` command attempted.

### 2. Login status / human-visible status

SOURCE NAME: authentication status and current-session `/status`. LOCATION / INTERFACE: `codex login --help` exposes status; `/status` is the human-visible cross-check requested by the user. DOCUMENTED OR UNDOCUMENTED: login status documented; no machine-readable `/status` contract established here. READ-ONLY: status intended as observation. AUTH HANDLING: remains in Codex. DATA AVAILABLE: login status is not quota; actual `/status` quota values were requested from the human, not obtained. RESET INFORMATION / WINDOW INFORMATION: NOT_VERIFIED for the current-session display. FRESHNESS: dependent on the UI snapshot. STABILITY: presentation format is unsuitable as an API. SECURITY RISK: unnecessary account information if scraping the whole display. SUITABILITY FOR CGC: independent human cross-check only, never the production reader. No TUI AI task was started and no status scraper was implemented.

### 3. App-server rate-limit snapshot — SELECTED

SOURCE NAME: `account/rateLimits/read`. LOCATION / INTERFACE: transient `codex app-server --listen stdio://`, newline-delimited JSON RPC. DOCUMENTED OR UNDOCUMENTED: official documentation and installed generated schema agree. READ-ONLY: selected read method; initialization changes only connection state. AUTH HANDLING: Codex owns authentication; CGC does not read, parse, copy, print or forward credential material. DATA AVAILABLE: metered bucket identities, primary/secondary windows, used percentage, optional duration/reset, optional direct individual-limit remaining percentage and ordinaryUsageAllowed. RESET INFORMATION: Unix seconds, converted to UTC for normalized output. WINDOW INFORMATION: duration in minutes, not inferred from primary/secondary position. FRESHNESS: local response receipt known; backend sample timestamp/age unavailable. STABILITY: experimental; version pin/revalidation needed. SECURITY RISK: full response can contain unrelated account metadata; project an allowlist in memory and never persist raw response. SUITABILITY FOR CGC: best candidate; live access verified once, structured and reproducible request framing, bounded client, no AI task required. Repeated-poll reliability and cadence are NOT_TESTED.

A connection via an already-running managed app-server was considered first. Read-only `codex app-server daemon version` returned exit 1; diagnostic text was withheld and no specific cause is inferred. No daemon was started, restarted or installed. The transient stdio mechanism succeeded instead. CGC V1 supports this POSIX subprocess transport only.

### 4. Structured notifications / local state

SOURCE NAME: `account/rateLimits/updated` notifications and possible local event/state data. LOCATION / INTERFACE: app-server notification documented/generated; local session/state files not inspected. DOCUMENTED OR UNDOCUMENTED: notification schema documented/generated; a standalone local cache contract was not established. READ-ONLY: notifications can be read, but originating a model turn solely for quota is excluded. AUTH HANDLING: Codex-owned. DATA AVAILABLE: schema describes sparse rate-limit updates; they are not guaranteed full snapshots. RESET INFORMATION / WINDOW INFORMATION: optional update fields. FRESHNESS: event-dependent. STABILITY: experimental protocol and possible historical file formats. SECURITY RISK: session/state files may contain unrelated content; unnecessary inspection avoided. SUITABILITY FOR CGC: full snapshot preferred; sparse notifications would need tested merge semantics and freshness rules in a later scope. No history/session scan was performed.

### 5. Other supported account usage interfaces

SOURCE NAME: documented app-server `account/usage/read` and account usage displays. LOCATION / INTERFACE: official app-server reference; no live invocation. DOCUMENTED OR UNDOCUMENTED: token-activity summaries documented; no alternative local machine-readable quota source was established. READ-ONLY: documented read, not exercised. AUTH HANDLING: would remain with Codex. DATA AVAILABLE: token activity is not remaining quota percentage. RESET INFORMATION / WINDOW INFORMATION: not established as a substitute for rate-limit windows. FRESHNESS: NOT_VERIFIED. STABILITY: source-specific. SECURITY RISK: unnecessary account/activity data. SUITABILITY FOR CGC: inferior for the requested question; not selected. No direct OpenAI backend endpoint or private `/api/codex/usage` request was made.

### 6. Other mechanisms

SOURCE NAME: hypothetical log scraping/browser scraping/private backend access. LOCATION / INTERFACE: none inspected or invoked. DOCUMENTED OR UNDOCUMENTED: no supported candidate established. READ-ONLY: not a sufficient safety guarantee. AUTH HANDLING: any credential extraction is prohibited. DATA / RESET / WINDOW / FRESHNESS / STABILITY: UNKNOWN. SECURITY RISK: elevated and unnecessary. SUITABILITY FOR CGC: rejected; do not bypass the selected owner-controlled interface.

## Ranking and selection rationale

1. Documented/generated app-server snapshot: structured, current request, owner-controlled auth, explicit field provenance; selected despite experimental maturity.
2. App-server notifications: same trust boundary but sparse/event-dependent; not selected for initial read.
3. Human-visible status: useful comparison, unsuitable as canonical machine input.
4. Authentication status / token-activity interfaces: answer different questions.
5. Local file scraping and private endpoints: no verified need or suitable contract; not used.

Polling is technically possible through the same method without model generation, but V1 demonstrates only one read. V2 must determine responsible cadence, authentication-failure handling, upstream freshness and sustained reliability rather than assuming a thirty-second interval is approved.

## Exact experiment and limits

One temporary stdio process: `codex app-server --listen stdio:// -c analytics.enabled=false`. No persistent daemon, socket listener, service, model turn or account settings change requested. Codex may perform its ordinary internal startup/authentication bookkeeping; CGC neither inspects nor controls those internals.

Wire sequence:

```json
{"id":1,"method":"initialize","params":{"clientInfo":{"name":"cgc","title":"CREDID GUARDIAN CODEX","version":"0.1.0"},"capabilities":{"experimentalApi":false}}}
{"method":"initialized","params":{}}
{"id":2,"method":"account/rateLimits/read","params":{"excludeResetCreditDetails":true,"supportsLunaReserve":false}}
```

The client waits for initialization before sending the other two messages. Reset-credit details are excluded; no reset, authentication, account update, notification-email or turn method is called. Token-refresh/attestation requests are refused rather than handled by CGC. Exact parameter meanings were read from the installed schema; false reserve support avoids requesting that optional behavior.

Experiment limit: 20 seconds; at most 512 KiB combined stdout/stderr, 128 KiB per buffered frame, 100 frames and 32 buckets. No retries. Data captured only in memory, credential-key checks and quota projection before display/write. Initialization output and stderr discarded. stdin closed and the child reaped; timeout cleanup terminates its POSIX process group. Prototype cleanup permits up to an additional 1.5 seconds; OS process creation/reaping is not a hard realtime guarantee.

## Live result

Started: `2026-09-17T00:50:34.447068+00:00`. Response recorded: `2026-09-17T00:50:35.462546+00:00`. Exactly **one** quota request sent, successful. See [sanitized experiment](v1-app-server-observation.json) and [normalized projection](v1-normalized-observation.json).

| Bucket | Role | Observed duration | Used (direct) | Remaining (derived) | Reset (UTC, converted from Unix seconds) |
|---|---|---|---|---|---|
| codex | primary | 300 minutes / 5 hours | 64% | 36% | 2026-09-17T05:15:51Z |
| codex | secondary | 10080 minutes / 7 days | 42% | 58% | 2026-09-20T17:57:44Z |

`ordinaryUsageAllowed=true`; limitName and individualLimit were null. Exactly one bucket appeared in the returned mapping. No claim that every account/model has only one bucket or two windows. Plan, credits, account identifiers, banners and other unrelated values were deliberately omitted; their absence from this artifact is not proof they were absent upstream. No credential or raw response persisted.

The normalized artifact was produced OFFLINE from the retained sanitized quota fields, after the reader tests passed; it is not a second live read. Percentages remain 36/58, clamping made no change, both windows are VALID. Backend freshness and global applicability remain UNKNOWN. One could compute a 36% minimum within this observed codex bucket, but V1 does not implement global policy aggregation or preservation state.

## Independent `/status` comparison

Requested quota-only human reading for the current session. PENDING / NOT_VERIFIED at publication: percentages, windows and reset correspondence cannot be asserted. Do not scrape a new TUI session, conflate observation times, or claim equality based solely on shared backend documentation. The structured schema is richer in bucket and provenance fields than a percentage-only display, but actual display differences remain unverified.

## Prototype and test evidence

`src/cgc/quota.py` implements a bounded one-shot POSIX transport, `read_quota`, `normalize` and fixed safe error classes. No CLI entry point, daemon, cache or hooks. Only existing Codex executable authentication is used. Unexpected fields are omitted; sensitive credential keys fail closed. Bucket identifiers are constrained and credential-like identifiers rejected. Raw source messages do not enter exceptions/reports.

Each percentage has origin metadata. `remaining = clamp(100 - usedPercent, 0, 100)` is DERIVED. Direct remaining is supported for the installed schema's individualLimit, which has UNKNOWN duration; it is not mislabeled a rolling window. Out-of-range used percentages remain marked INVALID even after clamping; invalid direct remaining percentages are rejected so a changed value is never mislabeled direct. This V1 rule follows the later explicit user instruction and differs from V0's proposed reject-before-clamp policy. Unknown is null; duration labels use observed minutes only.

Test chronology: 20 initial test methods written before source; first run failed at import with `ModuleNotFoundError: No module named 'cgc.quota'`, zero bodies ran. The human then explicitly prioritized one protocol experiment before the abstraction; that single experiment succeeded. Implementation plus clamp test: 21 passed. Added ten protocol/transport tests using synthetic subprocess peers, never real Codex, followed by a direct-value validation regression: **32 tests passed** with `PYTHONPATH=src python3 -B -m unittest discover -s tests -v`. No live read was repeated. Tests cover all requested normalization cases, exact one-read framing, no secret echo, duplicate-key/invalid JSON, byte/frame limits, timeout and child termination.

## Stop and next scope

The one live-read authorization is consumed. No repeated polling, daemon, hook or GUI began. HHS was inspected read-only only for the later human-requested integrity check; it remains clean at `280b7090edf51aadf694db04d6d5f6bceff289a2`. No HHS or other repository was modified. No installs or security-control changes occurred. Commit and push only this repository after publication checks; latest commit self-reference is HEAD, exact hash in final report.

Recommended future CGC V2 mission, only if separately authorized: one canonical normalized state, bucket applicability, versioned policy, atomic last-known-good cache and bounded daemon with tested staleness/failure recovery and a source-appropriate polling interval. Resolve the independent UI comparison before treating it as verified. Do not start V2 now.
