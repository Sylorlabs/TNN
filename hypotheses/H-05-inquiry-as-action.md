---
id: H-05
title: "Inquiry is an action; UNKNOWN is an action"
status: NEGATIVE
hypotheses: [H-05]
updated: 2026-09-19
---

# H-05 — Inquiry is an action; UNKNOWN is an action

## Claim
When evidence is insufficient, the response is not "probability below
threshold." The learner should keep a best hypothesis plus alternatives,
identify a predicted difference, weigh the cost of checking, and choose commit,
UNKNOWN, or a discriminating observation in comparable utility/regret units.
UNKNOWN means *no available commit has positive grounded value right now* —
not a permanent ambiguity class, confidence bucket, or evaluator-visible label.

## Why it matters
This is the decision-theoretic core: abstention must be earned from grounded
value, and curiosity must be priced.

## Evidence
The most empirically embattled hypothesis in the repo. Two-sided:

**Positive (shadow, REFERENCE_ONLY):** R31's sequential evidence policy with
learned stopping reached hard-correct 0.9698 / near-twin 0.9421 /
confidently-wrong 0.9162 with mean 1.396 physical probes; active physical probes
lifted hard acoustic mean from 0.6668 (acoustic-only) to 0.9523;
context-disagreement-triggered reinspection (0.9017) beat always-reinspect
(0.8439) — "always asking again is not the answer."

**Negative (native):** E45–E50 are six consecutive **valid native negatives**
on safe terminal control. The repaired evaluator notwithstanding, the terminal
controller made wrong commitments on *every* no-unique episode in E45; order
schedules (E46), grounded representation additions (E47), batch fitting (E48),
quadratic features (E49), and provenance/contention features (E50) all failed
the every-cell no-unique safety gate. The mechanism is revealing: the UNKNOWN
target was grounded zero on every training record, so its head stayed exactly
zero and abstention required every commit value to go negative — which the
tested geometries never achieved.

**Boundary (shadow):** R31's best policy abstained on only ~57% of deliberately
no-unique-answer cases; global probe-budget and generic RF stopping policies
were rejected (over-conservative, ~0.68 hard correct).

The repo names **epistemic ambiguity over time** — distinguishing
temporarily-difficult-but-resolvable from genuinely-no-unique-referent — as the
highest-value unsolved capability. The gap between H-05-as-stated (grounded
economic decision) and H-05-as-tested (zero-initialized linear head, zero
target) is genuinely unresolved.

## Open questions
- Can a grounded *nonzero* UNKNOWN value (delayed
  investigation/termination action value) break the abstention/resolution
  tradeoff? Proposed next mechanism after E50.
- The abstention/resolution tradeoff: every mechanism that increases safe
  abstention degrades resolution, and vice versa. Nothing tested breaks it.
