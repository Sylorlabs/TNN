# R32 V15-B — Delayed Non-Convergence Replay

Status: **REFERENCE_ONLY / STOPPING IMPROVED / CURRENT-STATE REPLACEMENT BOTTLENECK**

V15-B keeps V15-A's episodic backward multi-step observation credit unchanged. The only training change is that high-uncertainty histories whose delayed grounded evidence remains non-convergent receive the same regret/resource replay opportunity as later-unique histories. No ambiguity/condition label is visible to the learner.

On the identical forced seed-9714 battery, reusable no-unique UNKNOWN improves from V15-A **0.25** to **0.655**, and wrong commitment falls **0.347 -> 0.159**. Reusable resolvable success remains substantially above one-shot (**0.57 vs 0.20**); stable-weak reaches **0.90** and unstable-then-stable **0.66**. Cost-too-high UNKNOWN is **1.00**.

The remaining failure is concentrated in temporal state changes: replacement success **0.40**, reversal **0.32**, with mean trial counts **16.03** and **13.81** and 13% safety-loop exhaustion in each. Balanced/biased no-unique cases also require ~8 trials.

## Causal classification

**Stopping curriculum is materially repaired, but current-state representation/decision remains sticky.** V14-B stores change-point evidence as features, yet the commit candidate is still the argmax of a fixed global/recent blend. Thus old evidence remains inside the candidate itself even when the controller recognizes temporal change. The policy can keep observing but has no separate commit action for a post-change/current-epoch hypothesis.

## Next mechanism

Keep V15-B credit and replay fixed. Preserve the global historical hypothesis, but add a separate current-epoch hypothesis constructed from the best ordered evidence split and expose `COMMIT_CURRENT_EPOCH` as an additional action-value option. The Q learner chooses between R31 KEEP, blended/global commit, current-epoch commit, INSPECT, and UNKNOWN using delayed grounded regret. No hard change threshold or state label is added.
