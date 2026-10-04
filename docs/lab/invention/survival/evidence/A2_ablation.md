# A2 — Ablation (causal)

## Method
The prereg requires: "replay the winning trace deterministically with each
novel-composition step replaced by the best taught single-step alternative;
measure survival drop."

I's "novel-composition steps" are the exploration actions driven by the novelty
bonus (trying untried plan sketches). The ablation disables the novelty drive
(NOV=0), leaving the deliberation machinery intact but with no bonus for untried
compositions (it only exploits tried plans by their experienced mean). This is
the closest implementable analog to "replacing novel steps with the best taught
alternative" — without novelty, I falls back to exploitation + safety heuristics.

## Results (9 variants where I-survive beat R by ≥60)

| Variant | I (NOV=30) | I (NOV=0) | Drop |
|---------|------------|-----------|------|
| v00 | 248 | 220 | 28 |
| v01 | 250 | 220 | 30 |
| v02 | 220 | 242 | -22 |
| v03 | 250 | 226 | 24 |
| v05 | 220 | 246 | -26 |
| v06 | 250 | 244 | 6 |
| v07 | 220 | 208 | 12 |
| v08 | 220 | 237 | -17 |
| v10 | 250 | 232 | 18 |
| **Median** | **250** | **232** | **18** |

## Interpretation
Removing the novelty drive reduces median survival by 18 ticks (7%). On 3 of 9
variants, survival IMPROVES without novelty (v02, v05, v08). The effect is
small and inconsistent.

Per §2, "genuine invention" requires that the novelty "causally contributes to
survival — proven by ablation". An 18-tick (7%) median drop with 3/9 variants
improving does NOT constitute strong evidence that the novel compositions are
doing the work. The survival is primarily driven by the safety layer (taught
heuristics) and the avoidance of R's harmful COMBINE, not by the novelty-driven
exploration discovering a better strategy.

**K6 assessment:** The ablation does not show a substantial survival drop when
novel-composition steps are removed. K6 (novelty not causal) is SUPPORTED by
this evidence. The invention claim is not causally grounded.
