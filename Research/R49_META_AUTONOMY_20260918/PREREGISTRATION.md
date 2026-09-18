# R49 curiosity and self-model correction — preregistration

Date: 2026-09-18  
Status: **FROZEN BEFORE FRESH EXECUTION**

R48 passed all integrated packet gates except curiosity and self-model calibration. This follow-up changes only those two mechanisms.

## Curiosity hypothesis

R48 used positive one-step error decreases and was attracted to random noise because random fluctuations repeatedly look like short-lived improvement. R49 replaces that signal with generic structured learnability:

- a transition predictor estimates outcome predictability from experience;
- outcome entropy measures whether the region contains nontrivial structure;
- learning progress uses two non-overlapping rolling error windows;
- persistent value is high only when a region has both nontrivial variation and prediction skill above chance;
- visitation novelty decays with experience;
- no region identity has a hardcoded bonus.

The frozen test contains a deterministic learnable process, a constant process, and an unpredictable process under randomized region identifiers. The learned policy passes only if the learnable process receives the largest tail allocation, while both constant and noise regions become lower-priority.

## Self-model hypothesis

R48's greedy posterior-mean policy under-explored strategy alternatives. R49 uses generic UCB exploration over strategy/context outcome histories. It receives only context identifiers, chosen strategy, outcome, and cost. It does not receive the evaluator's competence table.

The test uses fresh evaluator-generated competence tables after source freeze. A pass requires >= 80% correct best-strategy identification across contexts and at least +0.25 absolute accuracy versus update-disabled state.

No threshold may be revised after fresh execution. `learn_authority=0`; canonical R27 remains unchanged.

