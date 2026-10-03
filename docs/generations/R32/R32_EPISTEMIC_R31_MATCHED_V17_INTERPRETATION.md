# R32 V17 — Balanced Non-Convergence Replay Causal Result

Status: **REFERENCE_ONLY / TRAINING IMBALANCE CONFIRMED BUT GLOBAL BALANCE REJECTED**

V17 keeps V16 architecture, current-epoch hypothesis, episodic backward credit, action set, observation costs, and runtime policy unchanged. The only scientific manipulation is extra replay for high-current-uncertainty histories whose later grounded windows remain non-convergent. Checkpointed generation preserved RNG state and global replay counters exactly; at 500 episodes it matched monolithic V17 counters exactly. The full 2,200-episode dataset reached **365 delayed-unique vs 327 non-convergent** high-uncertainty starts (ratio **0.8959**), compared with V16 **363 vs 139**.

On the identical seed-9714 forced battery, reusable genuine no-unique UNKNOWN improves from V16 **0.555 -> 0.665**. This confirms inadequate negative/non-convergence developmental support contributed to the V16 ambiguity error.

The tradeoff is unacceptable: reusable resolvable success falls **0.7725 -> 0.7225**, wrong commitment rises **0.1571 -> 0.2100**, mean trials rises **9.0786 -> 11.9286**, and safety-loop exhaustion rises **0.0186 -> 0.1086**. Stable-weak is **0.89**, unstable-then-stable **0.86**, replacement **0.65**, reversal **0.49**. Cost-too-high UNKNOWN remains **1.00**.

## Causal classification

**Training curriculum overcorrection / excessive persistence**, not rejection of V16's separate current-epoch hypothesis. Replay-count balancing teaches caution but does not represent the distinction between a sustained new epoch and an intrinsically nonstationary/unresolved process. It therefore makes the learner linger/oscillate on real replacements and reversals.

## Decision

- Retain V16 separate historical + current-epoch hypotheses.
- Reject V17's indiscriminate global non-convergence replay balancing as the solution.
- Retain the causal finding that non-convergence support matters.
- Next add a separate live **nonstationary/unresolved temporal hypothesis** whose mass is learned from ordered evidence dynamics and delayed regret. It must coexist with historical and current-epoch hypotheses; it must not be a hidden ambiguity label or fixed volatility threshold.
- R27 remains canonical; all results remain REFERENCE_ONLY until native Zag qualification.
