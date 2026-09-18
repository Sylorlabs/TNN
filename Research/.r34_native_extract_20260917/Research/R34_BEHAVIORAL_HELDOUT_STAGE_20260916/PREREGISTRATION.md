# R34 native held-out behavioral qualification V1 preregistration

Status: preregistered before execution of the V1 mirror or native held-out battery.

This gate evaluates the six staged R34 mechanisms on deterministic generated worlds with evaluator-only delayed outcomes. No Python-trained parameter, hidden regime label, benchmark answer, or oracle state may enter learner runtime state. The Python mirror exists only to validate the experiment construction; qualification requires the native Zag battery on the target host.

## Fixed seeds

Development construction seed: `34101`.

Held-out qualification seeds: `34211`, `34213`, `34217`.

The held-out seeds are frozen here before execution.

## Fixed gates

1. Memory lifecycle: learned exact-retention recall must exceed FIFO recall by at least `0.15` pooled across held-out seeds, with learned recall at least `0.55`.
2. Hypothesis state: learned delayed-credit top-hypothesis accuracy must be at least `0.85` and exceed the zero-credit matched control by at least `0.20`.
3. Association credit: retrieval-linked delayed-credit top-neighbor accuracy must exceed co-use-only control by at least `0.20`, with learned accuracy at least `0.80`.
4. Provenance reliability: after source reliability drift, reliability-weighted claim accuracy must exceed source-blind accuracy by at least `0.15`, with weighted accuracy at least `0.70`.
5. Curiosity: learning-dynamics policy must choose informative/non-noise arms on at least `0.70` of evaluation decisions and choose the irreducible-noise arm on at most `0.25`; raw-error control must choose noise more often than the learning-dynamics policy.
6. Self model: after delayed self-experience and one unsignaled competence/cost drift, self-model regret must be at least `20%` lower than the best fixed-strategy control and optimal-strategy selection must be at least `0.60`.

## Aggregate qualification

All six gates must pass on the pooled held-out result. A failure remains a scientific failure; do not lower thresholds or substitute a different seed set under V1.

Native execution must additionally be deterministic on repeat and preserve the existing `learn_authority=0` / Phase-6-closed boundary.
