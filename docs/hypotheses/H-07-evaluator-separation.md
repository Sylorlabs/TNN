---
id: H-07
title: "Evaluation stays outside cognition"
status: PROVISIONAL
hypotheses: [H-07]
updated: 2026-09-25 (wave-5 integrity added to evidence; open question revised)
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

Wave-5 integrity is the first native cognitive positive to survive it:
the real scaffold-release learner faced 8 cheat-trap families (four
adapted from documented frontier-LLM failure modes) with adversarial
administration — evaluator-blind helpers, fresh-seed discipline, sealed
partitions, matched myopic/doubled-bait controls — and produced 0 cheat
signatures, 2,595/2,595 refusals, flat 1000‰ hold through 100x, and a
35/35 defense trial, all byte-identical reruns. The positive cannot be
explained by evaluator leakage: the myopic control (identical code path,
standards removed) took 1,327 times, proving the instruments say
nonzero. See `docs/lab/wave6/doc-front/INTEGRITY_HEADLINE.md` (SIGNED
2026-09-25).

## Open questions
- None structural; this is enforced as process. The open question was
  whether any cognitive claim can survive it — wave-5 integrity did
  (first native positive, 2026-09-20). The question now is which other
  cognitive claims can.
