# R32 V18 — Live Nonstationary Hypothesis, Broadcast Integration

Status: **REFERENCE_ONLY / LATENT SIGNAL RETAINED / BROADCAST ROUTING REJECTED**

V18 restores the exact V16 developmental distribution: the full 2,200-episode checkpointed stream matches V16 counters exactly (2,200 normal starts, 1,708 resource starts, 682 source-7-only, 735 regret replays, 363 high-uncertainty delayed-unique, 139 high-uncertainty delayed-nonconvergent, 183 unique/source-7-only). The only new representation is a learned nonstationary/unresolved hypothesis mass trained from delayed grounded convergence vs non-convergence. The two R31 decision-relation features are excluded from that predictor.

On later held-out developmental rows the latent hypothesis reaches ROC-AUC **0.7000**, AP **0.5272**, with mean mass **0.3823** on non-convergent vs **0.2625** on convergent histories. This is informative and far from an oracle.

Broadcasting that mass into all V16 Q-functions improves reusable no-unique UNKNOWN **0.555 -> 0.655**, but damages useful commitment: reusable resolvable success **0.7725 -> 0.490**. Stable-weak is **0.77**, unstable-then-stable **0.43**, replacement **0.42**, reversal **0.34**. Cost-too-high UNKNOWN remains 1.00.

## Causal classification

**Representation-routing failure.** The nonstationary hypothesis itself carries useful future-nonconvergence signal, but allowing it to reshape KEEP, COMMIT, EPOCH and INSPECT simultaneously causes excessive abstention.

## Decision

- Retain the learned nonstationary/unresolved hypothesis mass.
- Reject broadcast integration into all action values.
- Restore untouched V16 KEEP/COMMIT/EPOCH/INSPECT values.
- Next add an isolated `UNRESOLVED_TEMPORAL` competing abstention action learned from delayed grounded regret. Standard UNKNOWN remains available; no fixed threshold is introduced.
- R27 remains canonical; native Zag qualification remains required.
