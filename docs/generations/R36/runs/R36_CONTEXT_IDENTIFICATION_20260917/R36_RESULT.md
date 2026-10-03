# R36 Context Identification — Reference Qualification

Status: **REFERENCE PASS / NATIVE QUALIFICATION REQUIRED**

R36 tests the missing R35 capability: learner-side identification of a returning self-context from learner-visible experience.

## Mechanism

The retained active self-model is augmented by a bounded archive of dormant self-context snapshots. Every delayed outcome updates a posterior over the active model plus at most four archived contexts using pre-update predictive likelihood of success and experienced cost. Predictions are posterior mixtures.

A diagnostic strategy is eligible only when its expected information gain, scaled by a learner-owned value coefficient, exceeds its predicted opportunity cost. The learner receives no regime ID, switch flag, evaluator context, oracle competence, or hidden change time.

## Frozen development result

Selected candidate: `eig_012`.

- V2 return regret: 0.04754010
- R36 return regret: 0.03365367
- Return-regret reduction: 29.21%
- V2 overall regret: 0.04155429
- R36 overall regret: 0.03593139
- V2 post-change regret: 0.06626419
- R36 post-change regret: 0.05162667
- R36 diagnostic-action fraction: 0.001111

All preregistered development gates passed.

## Frozen fresh-family result

- V2 return regret: 0.04049422
- R36 return regret: 0.03047779
- Return-regret reduction: 24.74%
- V2 overall regret: 0.03998203
- R36 overall regret: 0.03426544
- V2 post-change regret: 0.06479862
- R36 post-change regret: 0.04990986
- R36 optimal-choice fraction: 0.735712
- R36 diagnostic-action fraction: 0.000937
- Maximum self-context models: 5

All preregistered fresh-family aggregate gates passed.

## Ablation finding

The passive posterior archive explains most of the gain:

- Passive fresh return regret: 0.03129848
- EIG fresh return regret: 0.03047779
- Incremental EIG reduction versus passive: 2.62%

The principal architectural result is therefore the bounded predictive posterior over reusable self-contexts. Opportunity-cost-aware diagnostic actions add a smaller positive increment in this suite and remain very sparse.

## Claim boundary

This is reference qualification only. Individual worlds are mixed; aggregate preregistered gates pass, but the mechanism is not established as generally superior. Phase 6 remains closed and `learn_authority = 0` until the selected mechanism is implemented in native Zag and passes:

1. bounded-state native unit tests,
2. deterministic persistence and save/reload,
3. fresh-process continuation,
4. corruption/torn-state refusal where applicable,
5. native held-out reproduction of the frozen R36 behavior,
6. regression checks against retained R34/V2 behavior.

No self-modification authority is granted by this result.
