# CREDID GUARDIAN CODEX (CGC) — concept

## Problem

Long-running Codex development can approach a usage boundary while important discoveries, unfinished changes, test results and continuation instructions remain only in transient context. An abrupt stop can make the next session repeat expensive operations or misinterpret incomplete work as complete.

CREDID GUARDIAN CODEX introduces usage-aware preservation: observe capacity when a supported source is available, retain provenance and uncertainty, then make a clear preservation policy available to Codex.

## The fuel gauge

CGC acts as an aircraft fuel gauge. It observes the remaining operational resource and the reliability of the reading. It does not fly the aircraft. Codex remains responsible for understanding the authorized mission and making an appropriate checkpoint.

**THE GUARDIAN OBSERVES. CODEX PRESERVES.**

A threshold is a signal, not a grant of authority. A project that prohibits publication still prohibits it at RED. The useful outcome is a truthful, resumable handoff, not an automatic commit at any cost.

## Questions and non-goals

The intended system asks: how much usable capacity remains, how reliable and fresh is that observation, which window constrains progress, and should Codex continue, prepare preservation or perform minimum preservation?

It does not allocate Codex quota, bypass limits, control subscriptions, acquire credentials, take over projects or guarantee completion before exhaustion. Unobserved windows and uncertain reset semantics must remain explicit. No amount of documentation substitutes for a supported live source.

## One observation path

**ONE SENSOR. MULTIPLE CONSUMERS.** The reader, normalizer and policy engine produce one canonical cached state. CLI, hook and future UI consume that state instead of competing with independent readers or threshold implementations.

The windows collection is extensible. Five-hour/session and weekly windows are illustrative possibilities, not an assertion of account entitlements or a fixed source schema. Independent quota buckets should remain distinct; applicability must be established before aggregating them.

## Genesis boundary

V0 preserves architecture, policy and future test theory. It does not access live account quota or implement a daemon, hook, CLI, cache or visualization. Implementation and source discovery require subsequent authorization.
