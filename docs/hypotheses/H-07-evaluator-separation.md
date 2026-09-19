---
id: H-07
title: "Evaluation stays outside cognition"
status: PROVISIONAL
hypotheses: [H-07]
updated: 2026-09-19
---

# H-07 — Evaluation stays outside cognition

## Claim
Ground truth, benchmark labels, mode identifiers, hidden-set membership, and
answer keys belong to the evaluator. Teachers may select lessons with their own
knowledge, but that knowledge is not credited to the learner and must be
withdrawn before qualification.

## Why it matters
Without it, every positive result is suspect — the program treats evaluator
leakage as the default suspect behind any good number.

## Evidence
Methodologically load-bearing, with a clean causal demonstration. E45's first
two native runs collapsed to zero beneficial episodes *because the evaluator was
broken*: a single scalar `grounded_outcome` made "replacement/reversal" change
evidence without changing hidden world state; historical state equaled final
truth so KEEP was already correct; targets used clairvoyant ex-post best-of
labels; warrant read evaluator correctness (circular). After repair, the *same*
battery produced valid negatives instead of invalid collapses — i.e., the
program can now distinguish "the learner failed" from "the test was broken."

The resulting discipline — truth_by_time trajectories, frozen terminal
controllers, nonzero oracle-positive prevalence gates, evaluator-blind helpers
that take no mode/truth/seed/target arguments, fresh-seed discipline, sealed
partitions, matched controls (E51AJ: 6,480 unique training + 6,480 unique probe
trajectories; consumed probes never reused as fresh validation) — is arguably
the program's most transferable product.

## Open questions
- None structural; this is enforced as process. The open question is whether
  any cognitive claim can survive it — so far the native cognitive results are
  negatives.
