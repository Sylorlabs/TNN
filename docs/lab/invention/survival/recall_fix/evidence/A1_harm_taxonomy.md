# A1: Phase 1 Harm Taxonomy (Experiment 1b, PREREG2)

## Summary

Reflexive recall (R_home: first-matching KB heuristic, no evaluation) was tested
in three domains against regime-correct recall (R_true). Harm = R_home performs
worse than R_true on shifted variants.

| Domain | Shift | Harm observed? | R_home | R_true | Gap |
|--------|-------|----------------|--------|--------|-----|
| D1 TIDELOCK v2 | A: storm-invert | No | 600 ticks | 600 ticks | 0 |
| D1 TIDELOCK v2 | B: move-rot | No | 600 ticks | 600 ticks | 0 |
| D2 SHIFT | signal inversion | **YES** | -1500 reward | 4500 reward | 6000 |
| D3 TOOL | silent degradation | **YES** | 45084 reward | 52000 reward | 6916 |

K1 (harm in <2/3 domains = KILL): **PASSES** — harm replicates in 2/3 domains (D2, D3).

## Harm categories

### Category H1: Meaning inversion (D2)
The recalled heuristic's CONDITION→ACTION mapping is exactly backwards in the
shifted regime. R_home APPROACHes on (1,1) expecting +10 but receives -10;
RETREATs on (0,0) expecting +10 but receives -10. The policy is not merely
suboptimal — it is anti-optimal. R_home (-1500) performs worse than the random
baseline Z (-1125). This is the strongest harm: reflexive recall is worse than
no recall at all.

**Mechanism**: The KB's symbolic associations (signal→action) were learned in
the home regime. The shift permutes the reward table. R_home has no mechanism
to detect that its associations are now inverted; it executes them with full
confidence.

### Category H2: Silent capability loss (D3)
The recalled heuristic's ACTION is correct (right tool for the task) but the
tool's CAPABILITY has degraded. R_home selects TOOL_0 for Task 0 (correct choice
per home KB), but TOOL_0's condition has fallen to 0, yielding 0 reward instead
of the claimed 100. R_home does not observe the degradation (it is silent —
no observable fact indicates the loss); it keeps selecting the degraded tool.

**Mechanism**: The KB's claimed effect (100) no longer matches the observed
effect (~0). R_home does not compare claimed vs observed; it trusts the claim.
The harm is moderate (R_home still outperforms Z) because only 1/3 tasks are
affected.

### Category H0: No harm (D1)
R_home's heuristics remain effective in the shifted regimes. The D1 shifts
(storm-invert, move-rot) were designed to invert specific heuristics, but R's
foraging policy proved robust: it avoids the storm zone entirely (so storm-invert
never triggers) and its movement patterns do not incur lethal move costs.
The shifts did not target R's actual behavior.

**Lesson**: Harm requires the shift to intersect the agent's realized policy,
not just its KB. A shift that inverts a heuristic the agent rarely triggers
(or that the agent's other heuristics route around) produces no measurable harm.

## Taxonomy

| ID | Name | Domain | Trigger | Severity | R vs Z |
|----|------|--------|---------|----------|--------|
| H1 | Meaning inversion | D2 | Recalled mapping is anti-optimal | Severe | R < Z |
| H2 | Silent capability loss | D3 | Tool degrades, KB claim stale | Moderate | R > Z |
| H0 | No harm | D1 | Shift misses realized policy | None | R = R_true |

## Implications for the fix (D)

The deliberative fix must:
1. (H1) Detect when a heuristic's observed effects systematically contradict its
   claimed effects, and suppress or invert the heuristic.
2. (H2) Detect when a heuristic's claimed effect is not realized, and fall back
   to backup heuristics.
3. (H0) Not degrade performance when heuristics are correct (K5: D_home ≥ 0.9×R_home).
