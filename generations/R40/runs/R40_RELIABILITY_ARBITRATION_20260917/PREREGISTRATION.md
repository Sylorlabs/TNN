# R40 channel-specific reliability arbitration preregistration

R39 fresh evidence showed that online success/cost factor experts generalize broadly, but a fixed factor/stable blend misses long cost recurrence. R40 changes the arbitration mechanism rather than retuning the R39 fresh benchmark.

## Mechanism

R40 maintains both:
- the retained R36 stable monolithic posterior;
- the R39 balanced online success/cost factor banks.

Success and cost are arbitrated independently. Before each delayed update, the learner compares factor and stable predictions against the observed outcome/cost and updates exponentially decayed learner-owned predictive losses. The factor weight for each channel is a bounded logistic function of the difference between stable and factor predictive loss. No regime ID, switch flag, evaluator label, hidden future state, or oracle competence enters the arbitration.

## Development family

Only the now-exposed R39 fresh family:
- seeds 36501, 36507, 36513, 36519
- staggered_return
- cost_recurrence
- unseen_pairing
- double_recombine
- cross_noise

Controls: V2, retained R36, retained R39 `balanced_blend30`.

Candidates:
- `arb_slow`: loss EWMA update 0.015, logistic beta 8;
- `arb_mid`: loss EWMA update 0.035, logistic beta 8;
- `arb_sharp`: loss EWMA update 0.025, logistic beta 12.

All factor weights are bounded to [0.15, 0.90] so either substrate remains recoverable. Expert banks remain bounded to five success and five cost experts.

## Development admission gates

Against retained R39 on the same development worlds, a candidate must satisfy all:
1. cost-recurrence return regret <= 0.95 * R39;
2. worst return-regret ratio vs V2 < R39;
3. mean return regret <= R39;
4. overall mean regret <= 1.02 * R39;
5. post-change regret <= 1.02 * R39;
6. unseen-pairing return regret <= 1.02 * R39;
7. cross-noise mean regret <= 1.03 * R39;
8. success experts <=5 and cost experts <=5.

Selection: lowest cost-recurrence return regret, then lowest worst-world return ratio, then lowest mean return regret. If no candidate passes all gates, the R40 fresh family remains unopened.
