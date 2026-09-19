# R36 Endogenous Self-Context Identification Preregistration

Date: 2026-09-17

R36 tests the R35 frontier result: stored self-contexts are useful when the learner can identify a returning context from learner-visible evidence.

## Learner-visible inputs
- generic continuous features
- chosen internal strategy
- delayed success/failure
- experienced cost
- its own self-model predictions
- predictive likelihood / posterior over its own stored self-context models

## Evaluator-only information
- scenario name
- latent context identity and switch time
- true success/cost functions
- counterfactual outcomes
- oracle strategy

Evaluator-only information is never passed to candidates.

## Candidates
1. `v2`: retained R35 V2 baseline.
2. `passive`: bounded frozen self-context archive with prequential Bayesian posterior; no diagnostic action bonus.
3. `eig_006`, `eig_012`, `eig_020`: same archive, with expected-information-gain action selection. An action is diagnostic only when beta * expected information gain exceeds its predicted opportunity cost.

Development may choose among the three preregistered beta values only. No other tuning occurs after development results.

## Development worlds
Seeds 36101, 36107, 36113 across: A→B→A, A→B→C→A, A→B→C→B, cost-only recurrence, stationary false-alarm bursts.

Each life is 4,800 steps with delayed outcomes. Self-context storage is capped at four frozen snapshots plus one active model.

## Development admission gate
A non-V2 candidate must satisfy all:
- return-context regret at least 5% lower than V2;
- overall regret no more than 3% worse than V2;
- post-change regret no more than 5% worse than V2;
- false-alarm world overall regret no more than 5% worse than V2;
- archive size <= 5 total models;
- diagnostic probe fraction <= 20%.

If no candidate passes, R36 is NO-GO and no fresh challenge is exposed.

## Fresh challenge
If development passes, freeze the selected source hash and run once on seeds 36203, 36209, 36217 across new A→B→A→C→A, gradual A→B→A drift, success-only recurrence, and long-return A→B→C→D→A worlds.

Fresh admission requires the same directional constraints, with return-context regret at least 3% lower than V2 and overall regret no more than 3% worse.

No Phase-6 authority follows from reference success. Native persistence and fresh-process equivalence remain separate gates.
