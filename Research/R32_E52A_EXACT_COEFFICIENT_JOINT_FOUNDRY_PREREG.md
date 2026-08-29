# R32 E52A — Exact-Coefficient Joint Decision Foundry

Date: 2026-08-29
Status: `PREREGISTERED NATIVE REPAIR — FROZEN BEFORE EXECUTION`
Parent: E52 native diagnostic negative
Canonical: R27 step 60,423

## Why this is a new experiment

E52's generic Foundry used a deterministic strided development sample both to rank a candidate interaction and estimate its coefficient. Every proposed terminal and continuation interaction then failed the required full-development loss check, leaving zero accepted growth and making C identical to A and D identical to B. E52 therefore did not test the intended joint capacity.

E52A changes only coefficient estimation after proposal selection. Candidate pairs remain ranked by the same deterministic generic strided residual-correlation search. Once the best pair is selected, its coefficient is recomputed from the complete current development residual ledger. The candidate is still accepted only when exact full-development loss strictly decreases. No validation information participates.

All E52 arms, protected UNKNOWN=0 geometry, action set, validation gates, and disallowed rescue tactics remain unchanged. E52A reuses the frozen E52 development stream because the repair was selected from a development-only fitting failure. It does **not** reuse E52 validation. E52's 1,080 preallocated sealed-confirmation episodes—never executed by E52—become E52A's fresh diagnostic validation set (4 episodes per base-mode-resource cell). E52's already executed 2,700 validation episodes are explicitly reserved and skipped. The current one-million-state effective-seed namespace has no capacity for another full sealed set after these reservations, so E52A cannot promote even if it passes; a pass would require a new, preregistered expanded seed namespace before confirmation. Forward/reverse pair selection, exact coefficient, full loss, and trace identity remain mandatory.
