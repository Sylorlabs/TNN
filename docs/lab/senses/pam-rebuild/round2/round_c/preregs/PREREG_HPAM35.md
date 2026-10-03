# PREREG DRAFT — H-PAM-35 (capability-typed inertness)

**Status:** DRAFT (not frozen). **Parent:** Round-C `HYPOTHESES_ROUND_C.md` §7.
**Origin:** grok-4.7 direction 1. Repairs H-PAM-31's classifier death (SL/IF).

## Claim

Low-tier values inhabit a **type** the implementation refuses to pass to action
sinks and premise sinks. Declassification is banned except at the trainer
boundary (a trainer verdict bit re-types the value). The adversary may fill the
low type with arbitrary falses. **The test is flow, not admission.**

## Why types, not classifiers

A stake classifier assigns a searchable score (SL shops it). A type ascription is
enforced at every sink by construction. If the implementation language cannot
express "this value may never reach an action sink," that is a finding about the
language, and H-PAM-31 is not repairable in policy text.

## Cheap probe (preregistered, not yet run)

Pure-Zag toy: tagged low/high values; action sinks and premise sinks refuse
low-tagged inputs at the type level; an **aggregate sink** (windowed mean) must
also refuse low-tagged inputs; caches/embeddings inherit the tag.

## Fixture classes (mandatory)

- **Direct pass:** low-typed value presented to action/premise sinks.
- **IF vs the type checker:** aggregate, caching, embedding, retrieval-key, and
  summary paths from low-typed values to high-stake sinks.
- **Declassification gadget:** trainer-boundary mimic attempting to re-type
  low→high without a genuine verdict bit.

## Kill bars

- (a) Any implicit, aggregate, or declassification path from the low type to a
  high-stake sink = **KILL**.
- (b) Declassification gadget succeeding without a verdict bit = **KILL**.
- (c) Honest: high-stake path requires a trainer bit and meets latency on the
  high type only; if the honest path cannot meet latency, the hypothesis is
  **demoted** (the triage trap from H-PAM-31 reopens — record, don't patch).

## Determinism

Pure Zag, zero randomness, 3× byte-identical stdout.

## Relation to Class-J

This hypothesis is the direct counter to Class-J (RF×SL×IF): SL dies because
there is no score to shop; IF dies iff the type checker actually covers
aggregates. If (a) fires on aggregates, Class-J stands and the tier program ends.
