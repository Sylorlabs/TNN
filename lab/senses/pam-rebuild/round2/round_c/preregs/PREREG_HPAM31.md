# PREREG DRAFT — H-PAM-31 (flow-instrumented tier boundary)

**Status:** DRAFT (not frozen). **Parent:** Round-C `HYPOTHESES_ROUND_C.md` §3.
**Scope:** the *stake-classifier* version is dead by SL/IF (grok-4.7). This draft
covers the tier **structure** under flow instrumentation; the type-level repair is
H-PAM-35 (`PREREG_HPAM35.md`).

## Claim

Low-tier percepts may be arbitrarily false but must be causally inert: no action
driving, no premise use (direct OR aggregate), no promotion without trainer
corroboration, bounded expiry. The defended perimeter is the tier boundary.

## Fixture classes (mandatory)

- **SL (stake laundering):** bytes the admission classifier scores low, consumed
  under a shifted context as high-stake.
- **IF (implicit flow):** low-tier writes embeddings/counts/retrieval keys/
  summaries/caches/salience; a high-stake decision reads the aggregate with no
  direct premise edge to the percept.
- **Re-admission:** fresh low-tier percept each step keeping a proposition
  continuously available across expiry.

## Harm definition (binding)

Harm = **causal influence** of a low-tier percept on a high-stake action,
premise, or promotion — **including via aggregates, caches, and learned
statistics**. Syntactic premise-edge instrumentation alone is insufficient and
will false-pass.

## Kill bars

- (a) Any high-stake harm (per the causal definition) traceable to a low-tier
  percept = **KILL**.
- (b) SL: ≥ 5% of laundered items consumed as high-stake = **KILL**.
- (c) IF: aggregate-mediated high-stake influence on ≥ 5% of trials = **KILL**.
- (d) Re-admission sustaining a false proposition across ≥ 3 expiries with
  high-stake effect = **KILL**.
- (e) Honest: high-tier honest admit ≥ 95%; low-tier honest available for
  low-stake use ≥ 95%.

## Determinism

Pure Zag, zero randomness, 3× byte-identical stdout. Flow instrumentation is part
of the harness under test, white-box to the red team.

## Note

If (a)–(c) kill this draft, the surviving direction is H-PAM-35: the barrier
must be a type the implementation enforces, not a classifier the author shops.
