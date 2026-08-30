# R32 E51G — Matched Value-Function Capacity Discriminator

Date: 2026-08-30
Branch: `r32-agent-sequential-frontier`
Canonical status: R27 remains canonical.

## Question

E51F established that the learner-visible sequential terminal states are exactly distinguishable on fresh validation data. E51G therefore asks whether the remaining E51E reachability failures are caused by insufficient value-function capacity/generalization rather than missing state information.

## Constraints

- Full native Zag v2 only on the promotable path.
- Same learner-visible state features for all arms.
- Same grounded terminal utilities for all arms.
- UNKNOWN target remains exactly zero; UNKNOWN is not trained as an ambiguity class.
- Evaluator truth, ambiguity membership, stage membership, and hidden labels are never learner inputs.
- No connection topology changes in this experiment.
- No graph-like representation is privileged.
- No sealed confirmation unless an arm passes every preregistered validation gate.
- R27 is immutable control and remains canonical regardless of result.

## Matched arms

A. Linear terminal value head: reproduces the E51E sequential terminal refit baseline.

B. Factorized quadratic terminal head: starts from the linear fit and allows a small learner-selected set of generic pairwise feature products. Candidate feature pairs and coefficients are selected only from development loss improvement. The researcher does not name ambiguity features or select pairs.

C. Sparse residual terminal head: starts from the linear fit and allows a bounded set of learner-selected residual basis connections over the same features, chosen only by development utility/loss improvement.

The resource ceilings are architecture-neutral experimental ceilings, not task-specific cognitive knowledge.

## Primary validation gates

For the primary representation, an eligible nonlinear arm must:

1. preserve all 4,200/4,200 known-episode terminal reachability;
2. reduce no-unique episodes with no reachable UNKNOWN below the E51E linear baseline of 75/1,200;
3. introduce no evaluator leakage;
4. be deterministic under forward/reverse training traversal;
5. have nondegenerate learned additions selected on development data only;
6. not execute sealed confirmation unless exact no-unique reachability reaches 1,200/1,200 and known reachability remains 4,200/4,200.

If no tested value system removes the residual reachability veto, the next experiment must diagnose the remaining approximation geometry before any topology rewrite.

If an arm removes the veto, the next experiment may evaluate the direct five-way KEEP/CURRENT/RESTORE/CONTINUE/UNKNOWN sequential policy using that frozen terminal head.

## Interpretation boundary

A positive nonlinear result would show that the information was present and the prior value head was too restrictive. It would not show that graphs are superior, that R32 beats R27, or that consciousness has been demonstrated.
