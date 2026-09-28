# R32 V38 — Repeated-Continuation Expectation and Variance Credit

Status: **REFERENCE_ONLY / UNCERTAINTY TARGET RETAINED / POSITIVE-DYNAMICS INFERENCE STILL OPEN**

V38 held the V37 observable state, episode-disjoint splits, delayed resource-grounded INSPECT advantage, action-value learner, and candidate-support target family fixed. The only scientific change was developmental consolidation: each observable state received 128 independent delayed continuations of the same external world, and the learner was trained to predict the continuation mean and variance. Hidden generator mode produced experience but was never a learner feature or runtime input.

## Where repeated experience changes the target

The target change is correctly localized:

- balanced no-unique single-to-mean MAE: **0.17685**;
- biased no-unique: **0.17497**;
- stable, replacement, reversal, and costly-stable modes: effectively **0.00000**.

Mean repeated target variance is **0.06171** for balanced no-unique and **0.05663** for biased no-unique, while deterministic modes have essentially zero continuation variance. This is the expected causal signature rather than a global smoothing artifact.

## Prediction

Compared with V37 single-continuation specialized prediction:

- overall MAE improves **0.17352 → 0.14746**;
- R² improves **0.38007 → 0.44923**;
- nonpositive-state MAE improves **0.16878 → 0.14079**.

But decision-positive MAE is nearly unchanged:

- **0.23409 → 0.23289**.

At horizon 5, support-for-current prediction on positive INSPECT states remains roughly **0.347**, essentially the V37 level. Repeated stochastic continuations therefore reduce no-unique target noise but do not reveal deterministic replacement/reversal dynamics that are not yet inferred from the current state.

The continuation-variance model is learnable:

- overall variance MAE: **0.01814**;
- positive-state variance MAE: **0.01364**.

## Action value

### Predicted repeated mean only

This arm is rejected. It broadens probing without enough unresolved-mass information:

- false-positive crossing: **0.10304 → 0.16117**;
- selected realized advantage: **0.11002 → 0.08008**.

### Predicted repeated mean + variance

This arm is retained as an uncertainty/safety component:

- expected-value ROC-AUC: **0.65307 → 0.65885**;
- false-positive crossing: **0.10304 → 0.07462**;
- selected realized advantage: **0.11002 → 0.14719**;
- beneficial crossing: **0.36150 → 0.35446**.

It sharply improves evidence economics and protects UNKNOWN, but it does not recover additional resolvable cases.

### Exact repeated mean + variance ceiling

The evaluator-only ceiling remains strong:

- classifier ROC-AUC: **0.96493**;
- AP: **0.69096**;
- expected-value ROC-AUC: **0.82514**;
- beneficial crossing: **0.66432**;
- false-positive crossing: **0.08764**;
- selected realized advantage: **0.17801**.

This validates repeated expectation/variance as the correct information family. The learned gap is not caused by target invalidity.

## Causal classification

Two distinct failures are now separated:

1. **Single-continuation credit variance** was causal for stochastic/no-unique cases. Repeated-experience variance materially improves safe abstention and observation economics.
2. **Latent deterministic temporal-dynamics inference** remains causal for positive resolvable cases. Replacement, reversal, and unstable-then-stable targets are unchanged by resampling, and their decision-positive prediction error remains high.

The architecture decision is therefore not “more abstention.” Keep the persistent uncertainty population and add the predicted continuation-variance channel as explicit unresolved mass. The next mechanism must improve ordered temporal dynamics inference without exposing generator identity.

## Decision / next run

Retain:

- repeated-continuation mean and variance as learned epistemic state;
- predicted variance as an action-value input;
- V37 unweighted target specialization;
- raw ordered evidence and provenance.

Reject:

- repeated mean without variance;
- interpreting repeated experience as a complete ambiguity solution;
- any manually selected confidence/probe threshold.

Next causal arm: a **candidate-specific recurrent temporal PAM** over the retained ordered raw evidence prefix. It must be graph-free and non-transformer, maintain a persistent recurrent state, and predict repeated continuation mean/variance from delayed outcomes. Compare the same downstream action learner against V38 ExtraTrees summaries. If recurrent sequence state closes the positive-support gap, classify the residual as representation/routing; otherwise move to an explicit learned hazard/run-length hypothesis population.

R27 remains canonical. Native Zag reproduction remains mandatory before promotion.
