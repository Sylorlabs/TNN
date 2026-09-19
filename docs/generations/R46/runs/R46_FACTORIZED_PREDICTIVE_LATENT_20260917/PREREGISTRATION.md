# R46 factorized predictive latent residual — preregistration

Date: 2026-09-17  
Status: **FROZEN BEFORE DEVELOPMENT RESULTS**

## Motivation

The current verified branch establishes three failures of increasingly fine scalar arbitration:

- R40: global success/cost channel reliability did not generalize;
- R41: strategy-specific scalar reliability did not generalize;
- R42: learner-visible state conditioned on recent error/feature trajectory still failed when its only action was to perturb one factor-vs-stable mixture coefficient.

An earlier temporal predictive self-state experiment also showed that temporal state could beat its own state-disabled ablation while still losing to passive memory when it replaced the retained memory predictor. The older Phase-5 closeout reserved R46 for a continuous, factorized predictive latent process rather than further context-bank threshold tuning.

R46 therefore preserves the retained R39 predictor and changes only the level at which learner-visible state enters prediction.

## Hypothesis

The retained R39 predictor remains the exact fixed 70% online-factor / 30% stable-memory blend. R46 learns bounded additive corrections to success and cost predictions:

`p_success = clip(p_R39 + residual_success(state, features))`

`p_cost = clip(c_R39 + residual_cost(state, features))`

The residuals are strategy-specific, but their state is continuous and factorized. They receive only learner-visible information available at decision time:

- fast and slow delayed success residual state;
- fast and slow delayed cost residual state;
- fast-vs-slow adaptation differences;
- recent absolute prediction-error state as an observation-reliability signal;
- current factor-vs-stable disagreement;
- current factor-bank posterior/evidence;
- stable-memory posterior concentration;
- similarity between the current feature vector and learner-owned residual-weighted feature traces.

Delayed feedback trains the residual using the exact state and R39 prediction cached at action time. No latent context ID, scenario label, evaluator state, change flag, future outcome, oracle competence, or counterfactual result is available to the learner.

## Development family

Development reuses the exact already-exposed R39/R42 paired family so comparisons can use immutable controls:

- seeds: `36501, 36507, 36513, 36519`
- scenarios: `staggered_return, cost_recurrence, unseen_pairing, double_recombine, cross_noise`
- 4,800 steps per life
- inherited delayed-feedback schedule
- decision RNG: `seed * 13007 + scenario-code sum`, matching R42

The immutable R41 V2/R36/R39 rows are paired controls. R42's completed state-conditioned scalar candidates are historical controls only and do not set admission thresholds.

## Frozen R46 candidates

All candidates begin with exactly zero residual, so their initial prediction is exactly R39.

| candidate | residual LR | success residual cap | cost residual cap | fast trace | slow trace |
|---|---:|---:|---:|---:|---:|
| `latent_cautious` | 0.008 | 0.10 | 0.035 | 0.060 | 0.010 |
| `latent_balanced` | 0.015 | 0.14 | 0.045 | 0.080 | 0.012 |
| `latent_fast` | 0.025 | 0.18 | 0.060 | 0.120 | 0.018 |

The R39 success and cost expert banks remain bounded to five each. Residual parameter vectors are fixed-size for the lifetime.

## Development admission gates

A candidate must pass **every** gate against paired retained R39:

1. cost-recurrence return regret `<= 0.95 * R39`;
2. worst paired return-regret ratio vs V2 `< R39`;
3. mean return regret `<= R39`;
4. overall mean regret `<= 1.01 * R39`;
5. post-change regret `<= 1.00 * R39`;
6. unseen-pairing return regret `<= 1.02 * R39`;
7. cross-noise mean regret `<= 1.02 * R39`;
8. bounded and behaviorally exercised: success/cost expert banks `<=5`, at least 100 delayed residual updates in every row, and mean absolute utility-prediction correction `>=0.003`.

Selection among passing candidates is by lowest cost-recurrence return regret, then lowest worst paired return ratio vs V2, then lowest mean return regret.

If no candidate passes all gates, the frozen R46 fresh family remains unopened.

## Fresh boundary

`r46_fresh_worlds.py`, `run_fresh_jobs.py`, `aggregate_fresh.py`, and `FRESH_CONTRACT.md` are frozen before development execution. Fresh seeds/scenarios must not be executed or inspected through candidate outcomes unless development selects a candidate.

## Authority boundary

`learn_authority = 0`. Phase 6 remains closed. A reference result cannot authorize architecture mutation or promotion without the separate native qualification boundary.

