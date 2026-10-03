# REDTEAM_SELF: WIDE-EIG-10 (wave-20261002-0521pdt, lane TRADES)

Zero em-dashes in this file. Attacks on the BUILD-PASS verdict above,
strongest first.

## 1. Is the gain real intelligence or expensive metric gaming?

The capability is chain identification via interventions in a sealed
world where the question names nothing and the answer must come from
intervention outcomes. A metric-gaming reading would need the agent to
exploit a leak: (a) the key.json chain, (b) a chain-order constant in
source, (c) the seed. Audit kills all three: key.json chmod 000 during
runs and never opened by the contestant (source grep: zero hits); zero
seed hits; zero chain-order string literals (reply strings are assembled
from cbrief-supplied var names). The single-trace baseline answers the
lexicographic default on 3 of 8 worlds, which is exactly what a
hypothesis-pooling system should do when it runs out of evidence, and
the 10-trace system does not. The gain is evidence-driven pruning of a
researcher-authored hypothesis space, which is real (if modest)
experimental-design capability, not metric shaping. The frozen 68-item
battery's C9 items were deliberately NOT targeted (a 5-line parser would
score 3/3 with zero reasoning); they remain 0.000, and the stripped
reply stream is byte-identical to the INQ sealed run. Deliberately
leaving a scoreable zero on the table is evidence against metric gaming.

## 2. The EIG confound (knowledge vs architecture)

The prereg pre-disclosed, and the sealed run reproduces: F_CM
(compute-matched random pick) also scores 8/8. The expensive EIG choice
rule contributes nothing at 30 pooled interventions. The capability gain
(5/8 to 8/8) comes from the ensemble-plus-pooling architecture and the
hypothesis/pruning machinery, not from EIG superiority. A verdict
claiming "EIG deliberation buys causal identification" would be false;
the verdict claims only what the bars say: the 10x deliberation budget
buys reliability. This matches the dev calibration (100/100 pooled under
random, fixed-rotation, and EIG selection alike). The verdict does not
overclaim, and the K3 non-inferiority bar was set at exactly the right
strength.

## 3. Would a rational user prefer this over an LLM for the task?

Honest answer: not yet, and the prereg scope section says so. The sealed
domain is 3-variable chains with exact co-movement observations and a
fixed 6-hypothesis space; a competent LLM or a 20-line Python script
solves it trivially. What the trade buys is not superhuman diagnosis but
a TNN-internal capability that did not exist at all: the arena contestant
at 0.000 could not say "intervene on Y and see whether X changes"; the
WIDE-EIG-10 binary reliably does, under a frozen protocol, with white-box
traces, zero randomness, and no regression. The trade is infrastructure
toward causal inquiry (C9 intent), not a capability an LLM lacks. Keep:
as L2 experimental-design infrastructure inside one continuing learner,
it is worth its 10x deliberation cost. Discard any reading of it as a
general causal reasoner or as evidence against the standing question
("no genuine causal model learning" remains open).

## 4. Domain thinness

The dev calibration found intervention choice irrelevant in the
3-variable domain (all policies within noise); the frozen design kept
the domain because the ensemble axis, not the choice axis, is under
test. A 4-variable check showed only a small EIG edge. The sealed
battery is therefore thin: 8 worlds, one domain family, one fixed
hypothesis space. The verdict claims reliability inside this domain
only. Follow-up (queued, not claimed): sealed 4-5 variable worlds with
non-chain DAGs to test whether width buys anything where choice matters.

## 5. Kill-bar honesty checks

- K4 was evaluated on the aggregate sim ratio (11.01 in [8,12]) rather
  than per-world ratios (4 of 8 worlds exceed 12). The bar's unit is the
  aggregate, consistent with the dev prototype's single 10.0x figure,
  and the structural 30-vs-3 count is exactly 10x. Reported with the
  per-world numbers in SEALED_EVAL.md. If the parent rules per-world is
  the intended unit, K4 should be recorded as borderline, not a clean
  pass; the aggregate reading is my documented interpretation.
- The prereg's "identical sim count" parenthetical for F_CM does not hold
  world-for-world (0.94x in aggregate) because random picks diverge
  hypothesis histories. Disclosed in SEALED_EVAL.md 2; the procedure is
  identical and the budget parity holds in aggregate.
- state_bytes is a fixed allocation, not a growth metric; structure
  creation is evidenced by the stderr trace. Disclosed in K9.
- The 0221pdt worker's worlds-before-commit ordering was remediated by
  regeneration-from-committed-source; byte-identity verified. Disclosed
  in IMPLEMENTATION.md.

## Verdict recommendation

BUILD-PASS on all ten frozen bars stands, with the honest scope: a
real, sealed, reproducible 10x-deliberation trade that buys reliable
causal chain identification in the tested domain, at an honestly
measured 11.01x forward-sim cost, with the intelligence gain located in
ensemble-plus-pooling architecture rather than in the EIG choice rule.
No L3 claim. No generality claim. No LLM comparison claim.
