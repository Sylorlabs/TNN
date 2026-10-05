# PREREG -- PHASE 16: DOES COUNTING'S DOMINANCE SURVIVE AT LARGE N?

Branch `ownership`. Written **before** any code for this phase.
Follows the discipline that killed Phases 6-9: state the prediction
that can fail.

## THE QUESTION (C1634, from RED_TEAM.md A1)

Four learner mechanisms tied or lost to `argmax frequency`, and PHASE
15's lane was compromised. The red team's objection: every one of those
tests ran with **at most 5 candidate structures**, where `argmax
frequency` is close to optimal by construction. So "counting wins" may
be an artifact of substrate size, not a fact about learning.

This phase builds a world that is large enough for that objection to
have teeth.

## THE STRUCTURAL CLAIM UNDER TEST

> With **binary** outcome feedback, frequency counting is not merely
> hard to beat -- it is *sufficient*. Any selection rule computed from
> 0/1 outcomes is a function of the counts, so it cannot outrank
> argmax over the counts.

If that is right, counting's dominance is not a small-N artifact at
all: it follows from the **granularity of feedback**, and it will
persist at any N. This phase is designed so that the N-artifact
explanation and the feedback-granularity explanation make *opposite*
predictions, and we can tell them apart.

## SUBSTRATE (declared, minimal)

- **36 candidate structures**, each an affine map `f(s) = a*s + b`,
  `a` in {1,2,3,4}, `b` in {0..8}. Index `k = (a-1)*9 + b`.
  Affine maps are closed under composition and give each query a
  unique consistent structure from two points, so correctness is
  unambiguous.
- **Query** = two constraints `(x1,y1),(x2,y2)`. The target structure
  `k_t` determines both `y` values, so exactly one structure is
  consistent. No ambiguity, no unsolvable queries.
- `k_t = (t*7) % 36` -- 7 is coprime with 36, so targets cycle through
  **all 36 structures**.
- 108 training queries (each structure targeted ~3x), 36 held-out
  queries (each targeted exactly once).
- Every arm **evaluates all 36 candidates** on every training query and
  accumulates permitted statistics. Selection is over the candidate
  set. This is a **selection** experiment, not a search experiment --
  declared scope limit: it says nothing about candidate generation.

## FREQUENCY REGIMES (how counting is fed)

`count_k = (#training queries targeting k) + noise_k`

| regime | `noise_k` | what counting faces |
|---|---|---|
| R1 UNIFORM | `0` for all k | 36-way tie, no signal |
| R2 DILUTED | `1` if `(k*13)%36 < 12` else `0` | weak, partly spurious |
| R3 MISLEADING | `3` if `(k*5)%36 < 10` else `0` | actively points at wrong structures |

All three are non-vacuous by construction: the correct answer is never
identifiable from the count alone in R1, and is contradicted in R3.

## FEEDBACK GRANULARITY (the experimental factor)

- **BINARY**: the learner observes only `f(x) == y` (0/1). This is
  what TNN actually has today.
- **GRADED**: the learner additionally observes `f(x) - y`.

Same world, same candidates, same arms. Only feedback granularity
differs.

## ARMS

1. `ORACLE` -- selects the structure consistent with both points.
   Upper bound. **Positive control.**
2. `COUNT` -- argmax `count_k`, lowest-index tie-break.
3. `FIXED_FIRST` -- always structure 0. Fixed control.
4. `AFFINITY` -- argmax `count_k + transition_k` (generic co-occurrence
   bonus from prior selections).
5. `RESID_CREDIT` -- argmax of `-|mean signed residual|` over training.
   Under BINARY every residual is 0 by definition, so this arm is
   *forced by the substrate* to tie `COUNT`. Under GRADED it is free
   to use signed error.
6. `VALUE_SCOPED` -- memorises training `x1 -> target`; cannot transfer
   to new `x1`. Control for memorisation.

## PREDICTIONS (the part that can fail)

- **P16-A**: `ORACLE` scores 36/36 held-out in every regime. If not,
  the harness is broken and the phase is void.
- **P16-B**: `COUNT` scores far below `ORACLE` in R1. If `COUNT` scores
  36/36, the world is not the one we think and the phase is void.
- **P16-C** *(the discriminating prediction)*: under **BINARY**,
  `RESID_CREDIT` **ties** `COUNT` exactly, and no arm beats `COUNT`.
- **P16-D**: under **GRADED**, `RESID_CREDIT` **beats** `COUNT` in all
  three regimes.

If P16-C holds and P16-D holds, the answer to C1634 is: *counting's
dominance is not a small-N artifact. It is a consequence of binary
feedback, and the missing ingredient is error granularity, not a
better selection rule.*

If P16-C **fails** -- if something beats counting under binary
feedback -- that is a genuine positive result and the most valuable
outcome available.

## VALIDITY GATES (phase is VOID unless all pass)

- **V1** all 36 structures are the target at least once in training AND
  at least once held-out. *(PHASE 15's failure: only 4 structures
  learned, one collapsed to identity.)*
- **V2** `ORACLE` == 36/36 held-out. *(PHASE 15's failure: one held-out
  query was unsolvable.)*
- **V3** targets are not predictable from any single count: the correct
  structure is **not** the argmax of `count_k` for more than a quarter
  of held-out queries.
- **V4** `COUNT` < `ORACLE` in R1. *(guards against a vacuous world)*
- **V5** if every arm scores 0 in every cell, the harness is suspect
  and results are reported as void.
- **V6** training and held-out `x` ranges are disjoint.

## FALSIFIABILITY NOTE

P16-C is a prediction of *no improvement*. It is registered in advance
precisely so that if a mechanism does beat counting under binary
feedback, that cannot be quietly reclassified as a harness artifact.
If P16-D fails, the honest report is that graded error did **not**
help, and the "feedback granularity" explanation is wrong.

## SCOPE LIMITS (declared up front)

- Selection only; candidate generation is not tested.
- Structures are affine maps, not programs. This is a *selection*
  experiment by design.
- The learner is a hand-written scorer over a candidate set, not TNN's
  own selection code. Nothing here measures TNN. *(Per
  `INDEPENDENCE_AUDIT.md`, that remains true of every phase.)*