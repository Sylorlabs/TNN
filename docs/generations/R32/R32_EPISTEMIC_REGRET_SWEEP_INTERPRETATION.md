# R32 Epistemic D Regret Sweep — Diagnostic

Status: **REFERENCE_ONLY / SCALAR_REGRET_FIX_INSUFFICIENT**

On the same matched development seed, changing only the delayed-regret semantics improved D as unnecessary UNKNOWN became more expensive, but did not restore the R31 hard frontier. Current asymmetric regret gave core hard 0.7176 / ambiguity UNKNOWN 0.8056. Symmetric wrong-commit and unnecessary-UNKNOWN regret gave core hard 0.8287 / ambiguity 0.6944. Intermediate variants remained between those endpoints.

## Causal classification

**Decision-policy formulation**, not persistent uncertainty representation. A scalar regret ratio shifts the expected commitment/abstention tradeoff but cannot repair the larger confound: D replaces R31's qualified decision with separately estimated safe/resolvable probabilities.

## Decision

Do not tune another threshold or scalar ratio. Replace the probability-policy formulation with residual action-value learning over KEEP_R31, COMMIT_CURRENT, INSPECT(source), and UNKNOWN. Train every Q target from delayed grounded outcomes/regret and observation cost. This preserves R31 as an available action rather than hardcoded authority: the epistemic policy may override it whenever learned expected utility is higher.
