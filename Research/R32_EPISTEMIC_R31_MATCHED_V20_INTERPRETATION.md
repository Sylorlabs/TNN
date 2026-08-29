# R32 V20 — Learned Future WAIT Option

Status: **REFERENCE_ONLY / DIRECTION RETAINED / NOT QUALIFIED**

V20 keeps V19's isolated `UNRESOLVED_TEMPORAL` action and untouched V16 base Q values, then adds a separate state-level `WAIT` option trained from actual episodic backward multi-step observation return net of cost. No fixed probe count or ambiguity label is used.

The direct WAIT regressor generalizes only moderately on later developmental rows (future-convergence ROC-AUC **0.6229**). Despite that, it improves V19 temporal resolution while retaining most ambiguity gain: reusable no-unique UNKNOWN **0.620**, resolvable success **0.6625** vs V19 0.6425 and V16 0.7725. Stable-weak **0.88**, unstable-then-stable **0.57**, replacement **0.67**, reversal **0.53**. Cost-too-high UNKNOWN remains 1.00.

## Causal classification

The WAIT mechanism is useful, but its **training objective/generalization is currently weak**. The raw continuous return target mixes sign (whether waiting is useful) with noisy magnitude/cost, and the held-out predictor only weakly separates later-convergent from persistent-nonconvergent states. This must be tested before another architecture change.

## Next

Hold V20 architecture fixed. Train a matched WAIT model on the same states using delayed **beneficial-wait vs non-beneficial-wait** outcomes, then convert its probability into expected wait utility using training-set conditional return means. This changes training objective only, not representation/runtime. If that fails, then escalate to a richer explicit time-to-resolution process model.

R27 remains canonical; native Zag qualification remains mandatory.
