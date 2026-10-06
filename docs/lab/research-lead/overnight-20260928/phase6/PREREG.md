# PREREG -- PHASE 6/7: TRANSFER AND REVISION OF GENERATIVE STATE

Branch `ownership`. Frozen before code. Follows `phase4/REPORT.md`.

## WHY THIS DESIGN CHANGES

Phase 4 failed Condition 3 (facts-only tied the experienced learner at
cost 1) and its regime 1 failed Condition 1 (fresh uniform sampling
succeeded at 225/400). Diagnosis recorded there: **budget was the binding
constraint, not competence.** So:

* **Budget is swept**, not fixed at 400.
* **The target is made unreachable by uniform sampling** by construction,
  so Condition 1 holds by design rather than by luck.
* A **harness positive control** regime is added where the target IS
  reachable by fresh sampling, proving the metric detects success when
  success occurs.
* Facts-only is given the **same raw facts** as the experienced learner
  and is charged the **reconstruction cost** of rebuilding state each
  episode. That is the honest version of Condition 3: the question is not
  whether facts determine the answer (they do -- that is the point), but
  whether the *distilled* generative state is cheaper than re-deriving it.

## SUBSTRATE

Sequences of `LEN=6` ops over an alphabet of `OPS=10`. Uniform random
probability of an exact hit is `10^-6`, so at any budget up to ~2000 a
fresh sampler essentially never succeeds. **Condition 1 holds by
construction.**

Learner state is ONE generic buffer of bigram counts, `ST2[(OPS+1)*OPS]`,
where row `OPS` is the START row. No modes, no routers, no
per-domain anything.

## QUESTIONS

* **6 Transfer.** Learn generation for A, then present structurally
  related unseen B where the exact winning sequence never appeared.
  Relevant prior should make B cheap. Irrelated C should not. Misleading
  D should hurt or be revised.
* **7 Revision.** Change the world so the prior generation bias becomes
  wrong. Require: old behaviour fails -> consequence exposes failure ->
  structural state changes -> generation changes -> recovery.
  **No hardcoded `RESET`.** Revision is driven by generic consequences:
  emitted-but-wrong ops are decremented, correct ops incremented.

## ARMS

| arm | state |
|---|---|
| A experienced | ST2 from relevant prior |
| B fresh | ST2 uniform |
| C facts_only | replays raw facts each episode, charged per replay |
| F irrelevant | ST2 from unrelated prior |
| G misleading | ST2 anti-weighted |
| H shuffled | ST2 with permuted op labels |
| I oracle | declared bound |

## METRICS

Proposals to hit, facts replayed, and (for C) total acquisition cost =
replays + proposals.

## HARNESS POSITIVE CONTROL

Regime 3 uses a short target (`LEN=2`), reachable by uniform sampling.
**Requirement: fresh sampler must succeed there.** If it does not, the
metric is broken and all regimes are void.

## FALSIFIABILITY

* If C's total acquisition cost is comparable to A's, the distilled
  generative state confers no advantage over re-derivation from facts.
  That is a **negative for generative ownership** and must be reported
  as such, not reframed.
* If B succeeds in the main regimes, Condition 1 failed and the sweep
  must extend rather than the result being read.
* If H matches A, the effect is identifier layout.