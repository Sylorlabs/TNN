# R32 V43 — Evidence-Count Stage Specialist Diagnostic

Status: **REFERENCE_ONLY / FIXED STAGE SPECIALIZATION REJECTED**

V43 held V40 evidence, horizon-hazard state, repeated variance, resource shadow price, delayed advantage targets, train/calibration/test splits, and action-value model family fixed. It replaced the global action-value learner with four diagnostic specialists routed only by learner-visible acquired-evidence count:

- trial 0;
- trials 1–2;
- trials 3–5;
- trials 6–11.

The bins are an evaluator diagnostic, not a promotable runtime design.

## Result

Combined stage-specialist policy versus global V40:

- expected-value ROC-AUC: **0.693649 → 0.677037**
- beneficial crossing: **0.436620 → 0.417840**
- false crossing: **0.079941 → 0.189219**
- selected realized advantage: **0.152146 → 0.070004**

The trial-zero specialist is not a repair:

- ROC-AUC **0.6281**
- beneficial crossing **0.2159**
- false crossing **0.0945**
- selected realized advantage **0.1429**

Later specialists become increasingly overactive; the trials 6–11 specialist crosses zero on **0.2439** of non-beneficial states.

## Causal classification

**Global action-model interference is rejected as the primary early-option failure.** Explicitly separating learner-visible stages does not recover the missing initial option value and substantially damages later calibration. The initial state still lacks sufficient evidence about latent future dynamics, and later specialists overfit rare positive continuations.

This negative result strengthens the V31/V35/V36 conclusion: the remaining error is not generic model capacity, stage routing, or hidden undertraining. It is the interaction between observationally aliased future dynamics and resource-grounded multi-step utility.

## Decision

- Reject fixed evidence-count specialist routing.
- Retain the global V40 horizon-hazard action model as the stronger reference.
- Do not promote any fixed trial bins or minimum evidence count.
- Next diagnostic: on the exact fresh V41 episodes, calculate evaluator-only optimal initial multi-trial option advantage under actual opportunity loss. Measure V38/V40 initial acquisition recall and final success specifically among episodes where continued evidence is genuinely beneficial. This separates economically correct abstention from failure to recognize or complete a valuable evidence option.

R27 remains canonical. Native Zag reproduction remains mandatory before promotion.
