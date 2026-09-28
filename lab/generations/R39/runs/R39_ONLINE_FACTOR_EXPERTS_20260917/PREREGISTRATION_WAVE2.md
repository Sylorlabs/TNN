# R39 wave 2 preregistration — confirmed online factors

Wave 1 demonstrated that online factor experts materially improve recurrence and cost-factor reuse, but immediate factor commitment creates too many experts under transient noise and slightly harms unseen recombination. The fresh R39 family remains unopened.

Wave 2 tests two structural changes:

1. **Provisional factor confirmation.** A surprise event creates a provisional expert. It must beat the incumbent's pre-update predictive loss over a fixed learner-visible confirmation window before becoming a permanent factor. Rejected provisional experts leave no permanent context.
2. **Stable-model blend.** A small retained R36 posterior contribution is tested as a stability control while the confirmed factor experts handle recombination.

Candidates:
- confirm128: 128-observation confirmation, no stable blend;
- confirm256: 256-observation confirmation, no stable blend;
- confirm128_blend25: 75% confirmed factors + 25% retained R36 predictions;
- balanced_blend25: 75% wave-1 expert_balanced + 25% retained R36 predictions.

The development worlds and all R39 admission gates are unchanged. Selection remains lowest worst-world return ratio, then lowest mean return regret. The fresh generator and fresh preregistration hashes remain frozen and unseen.
