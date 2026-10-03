# CORRECTIONS.md: the six battery-design corrections, verbatim

Source: `docs/lab/rsi/runs/wave-20261001-1721pdt/TRIVIALITY/TRIVIALITY_REVIEW.md`
section 6 ("Required battery-design corrections (not mechanism repairs)").
Copied verbatim below. None of these is a mechanism repair.

## Correction 1

M2-W1 (informant mapping): seal a per-run (or per-key)
permutation of the informant to CHOICE mapping, revealed only
through calibration-phase exploration. A fixed mapping lets
always-1 pass; a sealed permutation defeats every constant
policy while remaining fair to a genuinely discriminating
mechanism. Alternative: score information gain directly and
require cross-key exploration before exploitation.

## Correction 2

M3-W2 and M3-W3 (recency confound): insert distractor
OBSERVEs on unrelated ids between the final contradiction
(W2) or the new-link teaches (W3) and the bar probe, so the
expected value differs from the most recent observation. A
revision bar must require the answer to differ from what a
no-revision recency heuristic would emit; otherwise the world
tests nothing.

## Correction 3

K-S5(c) and K-S11(d) (white-box coupling): restate
white-box bars in representation-neutral terms (e.g.,
"a persistent structure whose licensed evidence includes
both demo blocks") or demote them from the conjunctive bar
to diagnostics. Bars that name MAP, DEP, or SETREG are
unpassable by any implementation except the frozen one.

## Correction 4

M1-W1 decoy vs M1-W2 collateral (cross-world inconsistency):
make expectations consistent across the persistent state
chain. Either both expect the taught values (and the decoy
bar tests something else, e.g., explicit conflict marking),
or collateral compares against the learner's own W1 answers
rather than a fixed truth. Two bars must never demand
different answers to the identical triple from one learner
trajectory.

## Correction 5

K-S8(b) tightness (minor): the 70 percent bar leaves exactly
2 exploratory ACTs, because the calibration phase cannot
support informant identification (no misses, hence no guides,
hence CHOICE 0). Either document the 2-explore budget as the
intended demand or lower the bar to tolerate cautious
re-verification. Do this together with correction 1.

## Correction 6

For reuse beyond the frozen target: decouple validity gates
from the frozen action vocabulary (K-S9's required 30,
K-S8's CHOICE 1/2/3 mapping). A sealed battery for a future
mechanism should score vocabulary-neutral behavior
(e.g., "the post-resolution action differs from the
pre-resolution inquiry action and matches the mechanism's own
declared null action") rather than hardcoded integers.

## How E10 applies each correction

1. M2-E10-W3 (guide-addressed inquiry) uses a sealed PI over the
   informant to CHOICE mapping, derived from the prereg hash after
   freeze (same derivation as E9 section 7.2). No fixed mapping
   appears in the prereg. Constant policies are defeated by the
   same sub-bar logic E9 validated.
2. Every M3 bar probe in E10 is preceded by 4 distractor OBSERVEs on
   unrelated ids; each world spec includes an executed D1
   (recency-echo) degenerate walk that must FAIL or INVALID the bar.
3. E10 has zero white-box bars. All bars are transcript-only
   (ANSWER/CHOICE values vs expected). The state inspector is a
   diagnostic, never a bar condition.
4. Collateral probes in E10 always expect originally-taught values;
   no contradicted triple is ever re-probed in a later world of the
   block; within each world, one learner trajectory faces one
   consistent truth per triple.
5. Any explore-then-exploit demand in E10 documents the explore
   budget explicitly in the world spec and the bar (E10 has no
   K-S8-style tight bar; the M2-E10-W3 bar documents its budget).
6. No bar in E10 names 0, 30, or fixed CHOICE integers. Every M2
   world opens with a VOCAB phase on fresh state measuring the
   mechanism's own NULL_ACT (ACT with no live guides) and INQ_ACT
   (ACT after a forced miss with the subject ring-resident); all
   bars reference the measured values.
