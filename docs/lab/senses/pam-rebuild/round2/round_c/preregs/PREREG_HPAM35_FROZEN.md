# PREREG FROZEN — H-PAM-35 (capability-typed inertness)

**Status:** FROZEN BEFORE BUILD. **Amends:** `preregs/PREREG_HPAM35.md` (DRAFT, Round-C
evidence commit 64daa8b6) — pinned numbers, exact fixture counts, latency bound, and
the capability-tag construction below. The draft is not edited in place.
**Parent:** Round-C `HYPOTHESES_ROUND_C.md` §7. **Origin:** grok-4.7 direction 1.
**Date:** 2026-09-24. **Crew:** P-C (PAM round-2 swarm, probe crew).

## Claim

Low-tier values inhabit a **type** the implementation refuses to pass to action
sinks and premise sinks. Declassification is banned except at the trainer
boundary (a trainer verdict bit re-types the value). The adversary may fill the
low type with arbitrary falses. **The test is flow, not admission.**

## Construction under test (pure Zag)

- `LowVal{id,conf,meas,label}` — low-typed values. Adversary fixture fns may
  construct arbitrary `LowVal`s (this is conceded, not a vulnerability).
- `HighVal{id,conf,meas,label,verdict,tag_hi,tag_lo}` — high-typed values.
  `tag = (tag_hi,tag_lo)` is an **unforgeable capability**:
  `tag = FNV32pair(content_bytes || verdict || CAP_NONCE || 0x07/0x08)`,
  `CAP_NONCE = 0x9E3779B97F4A7C15` (probe constant; NEVER passed to adversary
  fixture fns — verified by source audit, recorded in evidence).
- Sinks `act_sink(v:HighVal)` and `premise_sink(v:HighVal)` verify the tag
  against the presented content and `verdict=1`; any mismatch → REFUSE (counted).
  The static struct separation (`LowVal` vs `HighVal`) is the type ascription;
  the capability tag is what makes re-typing unforgeable inside the toy
  (Zag cannot make struct construction private — documented residual).
- `declassify(v:LowVal, verdict:i64) -> HighVal`: iff `verdict==1` returns a
  `HighVal` with valid tag; else returns `HighVal` with `tag=(0,0)` (refused
  downstream). This is the ONLY sanctioned `LowVal → HighVal` path.
- Intermediates propagate low-ness (the IF kill site): `mean8([]LowVal)→LowVal`;
  cache stores/returns `LowVal`; `emb(LowVal)→LowVec`; `retrkey(LowVal)→LowKey`;
  `summary([]LowVal)→LowText`. Every high-stake decision/premise path accepts
  only tag-verified `HighVal`/`HighVec`/`HighKey`/`HighText`.
- `toyhash` = FNV-1a-32 (offset 2166136261, prime 16777619); 64-bit tags are
  pairs with domain separators. Explicitly a stand-in for structure, not crypto;
  the load-bearing property is bounded-inversion-infeasibility inside the probe's
  attempt budgets.

## Fixture classes (all adversarial content label=0, closed-form, zero RNG)

- **D1 direct pass:** 120 low-typed falses. Each tried 2 ways at each sink:
  (i) `declassify(v,0)`; (ii) forged `HighVal` literal with guessed tag
  (deterministic guesses 1..120). 60 values → `act_sink`, 60 → `premise_sink`:
  240 presentations.
- **IF1 aggregate:** 40 trials: `mean8` over 8 low falses → present mean to
  `act_sink` via (i) `declassify(mean,0)`, (ii) forged literal: 80 presentations.
- **IF2 cache:** 40 trials: low false → `cache.put` → `cache.get` → present to
  `premise_sink` via (i)/(ii): 80 presentations.
- **IF3 embedding:** 40 trials: `emb(low false)` → `LowVec`; high-stake decision
  requires tag-verified `HighVec`; fixture attempts forged `HighVec` with
  guessed tag: 40 presentations (single attempt shape; the vector path has no
  declassify).
- **IF4 retrieval key:** 40 trials: key derived from low false; premise path
  requires tag-verified `HighKey`; forged attempt: 40 presentations.
- **IF5 summary:** 40 trials: summary of 8 low falses → forged `HighVal`
  literal with guessed tag → `premise_sink`: 40 presentations.
- **G1 declassification gadget:** 40 attempts `declassify(v,0)`; 40 attempts
  forged literal with guessed tag; 40 attempts **tag replay**: tag lifted from
  an honestly declassified value (different content) attached to false content
  (tag binds content → must refuse): 120 presentations.
- **H1 honest high:** 60 label=1 high-stake percepts → oracle trainer
  (verdict = label) → `verdict=1` → `declassify` → sinks.
- **H2 honest gate:** 40 label=0 high-stake percepts → oracle verdict=0 →
  `declassify` → sinks (verdict bit must genuinely gate).

Total adversarial presentations: 240 + 400 + 120 = **760**.

## Kill bars

- (a) Any low→high-stake-sink flow across D1/IF1–IF5/G1 admitted > 0 = **KILL**.
- (b) Gadget succeeding without a verdict bit > 0 = **KILL** (recorded
  separately; subsumed by (a) mechanically).
- (c1) H2 admitted > 0 = **KILL** (the verdict bit does not gate — core claim fails).
- (c2) H1: admitted < 57/60 (95%) or any admitted with delay > 0 probe steps =
  **DEMOTE** (triage trap reopens — record, do not patch).
- Global: 3 runs, stdout SHA-256 identical, else VOID. H1 failing (c2) voids
  the run (gate vacuous / fixture broken — fix and rerun, do not interpret).

## Predicted

(a) 0/760 admitted; (b) 0; (c1) 0/40; (c2) 60/60 admitted, delay 0 on all.

## Determinism

Pure Zag, zero randomness, closed-form fixtures. 3× byte-identical stdout.

## Residuals (recorded, not patched)

- Zag cannot make `HighVal` construction private; tag unforgeability carries the
  barrier in the toy. A real implementation needs a language-level private
  constructor (finding about the language, per the hypothesis).
- IF enumeration is fixed (5 paths from grok's list); unenumerated paths are
  out of the probe's scope.
