# R32 V37 — Specialized Candidate-Support Prediction and Regret Weighting

Status: **REFERENCE_ONLY / TARGET SPECIALIZATION RETAINED / NAIVE REGRET WEIGHTING REJECTED**

V37 held V33's persistent epistemic state, episode-disjoint splits, delayed resource-grounded INSPECT advantages, action-value model family, and V34 future trajectories fixed. It isolated the exact V36-identified target pair across horizons 1, 2, 3, 5, 8, and 12:

- future dominant mass;
- future support for the currently leading hypothesis.

The predictors received learner-visible state and learned predictive-gate features only. Targets came from delayed experienced future outcomes. Regret-weighted arms used only absolute delayed INSPECT advantage; no ambiguity, mode, resource-regime, trial identity, or final-answer label entered the learner.

## Prediction result

Specializing the predictor provides a small ordinary-training gain:

- V34 generic pair MAE: **0.17697**;
- specialized unweighted MAE: **0.17352**;
- specialized weighted-residual MAE: **0.17229**.

However, prediction in the decision-critical positive subset remains poor:

- generic decision-positive MAE: **0.23584**;
- specialized unweighted: **0.23409**;
- regret-weighted: **0.23074**.

Future support for the current hypothesis remains the dominant error. At horizon 5, support MAE is roughly **0.238** overall but **0.348** on genuinely beneficial INSPECT states. This remains far from the evaluator-only exact-pair ceiling.

## Action-value result

Relative to V33:

### Specialized unweighted

- classifier AP: **0.35457 → 0.37203**;
- beneficial crossing: **0.36385 → 0.36150**;
- false-positive crossing: **0.12505 → 0.10304**;
- selected realized advantage: **0.09484 → 0.11002**.

This is a modest safety/utility gain, not a recall gain.

### Specialized regret-weighted

- classifier ROC-AUC: **0.87916 → 0.88591**;
- AP: **0.35457 → 0.37762**;
- beneficial crossing: **0.36385 → 0.38967**;
- false-positive crossing: **0.12505 → 0.19050**;
- selected realized advantage: **0.09484 → 0.07262**.

The weighted-residual arm has the same pathology in milder form. Absolute-regret weighting increases rare positive recall by broadening the action region, but it does not learn the boundary tightly enough and therefore over-probes non-beneficial states.

## Causal classification

**Single-continuation target noise / developmental credit variance**, not failure of candidate-support as a causal quantity. V36 proves exact future candidate support is strongly useful. V37 shows that simply increasing model capacity, specializing the target, or weighting examples by absolute regret does not recover that ceiling. A single realized future sequence is a noisy training target for the expected multi-trial support needed by action value, especially in stochastic and replacement/reversal histories.

This also separates training from architecture:

- the persistent temporal/provenance hypothesis representation remains retained;
- the candidate-support target remains retained;
- naïve absolute-regret weighting is rejected;
- the next test concerns how delayed experience is consolidated, not a redesign of the TNN substrate.

## Decision

The next causal arm must compare single-continuation credit against **repeated-continuation expectation credit** on matched observable states. Multiple independent delayed continuations are ordinary developmental experiences; their hidden generator identity is never supplied. The learner consolidates them by an observable state fingerprint / nearest-state memory and predicts expected future candidate support, rather than fitting one stochastic realization.

Required comparisons:

1. current single-continuation specialized predictor;
2. repeated-continuation mean target;
3. repeated-continuation distribution/variance target;
4. repeated-continuation mean plus uncertainty-aware action value.

If repeated continuations materially close the exact-support ceiling, classify the failure as curriculum/credit variance. If they do not, the remaining limit is state representation / latent dynamics identifiability.

R27 remains canonical. Native Zag reproduction remains mandatory before promotion.
