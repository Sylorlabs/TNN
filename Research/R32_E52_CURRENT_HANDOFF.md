# R32 E52 Current Handoff — Joint Action-Value Frontier

Updated: 2026-08-29  
Canonical: **R27 step 60,423**  
Promotion: **none**

## What E51–E52 established

1. **Continuation has causal value.** E51B converted some no-unique wrong commits into grounded UNKNOWN, but over-observed and lost net utility.
2. **Continuation alone is structurally insufficient.** E51D found 179–183 no-unique episodes with no reachable UNKNOWN and 599 known episodes with no reachable correct commit under each frozen E50 terminal head.
3. **Learner-owned terminal geometry can improve utility.** E52A's generic pairwise Foundry selected eight commit-value interactions and improved terminal-only utility while reducing known wrong commits.
4. **Naive on-policy refitting is unstable.** E52B substantially increased known success and reduced wrong commits, but reached-state distributions oscillated and observation cost drove net utility negative.
5. **R27 still wins.** No candidate passed every-cell safety, net-utility superiority, confirmation, broad R27 regressions, or promotion.

## Do not repeat

- another fixed threshold or positive UNKNOWN value;
- continuation-only expansion against a frozen terminal head;
- another manually selected ambiguity/provenance feature;
- sampled interaction coefficients without exact full-development refit;
- naive unconstrained repeated on-policy refitting;
- E52B confirmation (not earned);
- claims based on E52B as fully independent validation, because subordinate simulator substreams overlap earlier reservations.

## Next bounded experiment: E53 conservative average-cost policy improvement

Keep the E52A learner-selected terminal basis and `UNKNOWN=0`. Compare:

1. terminal-only control;
2. E52B naive on-policy continuation;
3. conservative continuation with a replay ledger mixing current and prior reached-state distributions;
4. conservative joint terminal + continuation.

The generic protected optimizer may provide exact sufficient-statistic accumulation, replay storage, rollback, and resource accounting. TNN must learn proposal structure, coefficients, resource shadow price, and whether an update is retained from delayed net utility/regret. A policy update is accepted only when its complete-development net utility improves without violating the frozen known/no-unique safety constraints. Update magnitude/replay mixture must adapt from observed distribution instability rather than use evaluator labels.

Validation must use a new allocator namespace large enough to avoid component-level collisions; do not weaken independence again. Sealed confirmation is allocated only after the allocator passes.

## Required success before any R27 comparison

- deterministic native forward/reverse fit and byte-identical binaries;
- terminal reachability improvement;
- stable reached-state distribution across policy iterations;
- positive net utility after observation cost;
- known-success and wrong-commit non-inferiority;
- material no-unique safety improvement, including every-cell analysis;
- untouched sealed confirmation.

Only after those gates pass should R32 run the broad R27 capability/regression battery.
