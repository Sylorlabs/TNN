# R32 V14-B — Ordered-History Change-Point Representation Test

Status: **REFERENCE_ONLY / REPRESENTATION_NOT_REACHED / PRE-PROBE OPTION-VALUE BOTTLENECK**

V14-B used exactly the V14-A dynamic consequence curriculum and added only generic continuous features computed from retained ordered evidence: best two-segment change gain, change recency, post-change stability, top-hypothesis change, post-segment fraction, and return-to-prior/reversal evidence. No condition/mode label, fixed threshold, or fixed runtime probe count entered cognition.

The forced seed-9714 result is effectively unchanged from V14-A: no-unique UNKNOWN **0.960**, resolvable success **0.010**, cost-too-high UNKNOWN **0.980**, mean reusable trials **0.0086**. The policy almost never initiates the repeated observation sequence, so the added temporal features are rarely instantiated.

Training diagnostics show the recursive INSPECT target mean is ~**-0.215** while UNKNOWN is exactly neutral at **0.0**. Thus the fitted-Bellman controller predicts negative option value at the pre-probe state and abstains before evidence can reveal whether the world is stochastic, replaced, reversed, or merely weak.

## Causal classification

**Active-observation option-value bootstrap / credit assignment.** This result does not reject ordered temporal-state representation; it shows that representation cannot help if the policy never pays to reach an informative future state. The next mechanism should propagate delayed grounded value through actually experienced multi-trial trajectories (episodic backward return / multi-step regret), rather than relying only on fitted one-step model bootstraps. Observation cost remains explicit and UNKNOWN remains neutral.
