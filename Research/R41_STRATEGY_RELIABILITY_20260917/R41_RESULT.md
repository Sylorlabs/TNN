# R41 strategy-specific reliability arbitration — closeout

Status: **DEVELOPMENT NO-GO / FRESH UNOPENED**

R41 learned factor-vs-stable predictive reliability separately for each strategy and separately for success/cost, using only delayed learner-visible evidence.

All 120 preregistered development jobs completed with zero harness errors. No candidate cleared all eight gates; the already-frozen R41 fresh family was never opened.

Best observations:
- `strat_slow` improved cost recurrence to 0.018782623348201456 and mean return to 0.02793948978650504, but failed post-change and unseen-pairing gates.
- `strat_mid` produced a worst return ratio below 1.0 vs V2 on development, but failed mean return, post-change, and unseen-pairing.
- factor/stable weights still averaged close to 0.5 despite per-strategy granularity.

Conclusion: scalar reliability memories, even strategy-specific, do not provide enough state information to decide which substrate is locally trustworthy. The next architecture must condition routing on the learner-visible operating state / feature trajectory rather than only channel or strategy identity.

`learn_authority = 0`. Phase 6 remains closed. R41 fresh remains unopened.
