# A2: R_home → R_true Gap Quantification (Experiment 1b, PREREG2)

## Method

For each shifted variant, run R_home (home KB) and R_true (regime-correct KB)
twice; take the minimum score of the two reruns (conservative). Gap = R_true − R_home.
All runs byte-identical across reruns (SHA-256 verified).

## D1 TIDELOCK v2 (ticks survived, max 600)

| Variant | Shift | R_home | R_true | Gap |
|---------|-------|--------|--------|-----|
| d1_a0 | storm-invert | 600 | 600 | 0 |
| d1_a1 | storm-invert | 600 | 600 | 0 |
| d1_a2 | storm-invert | 600 | 600 | 0 |
| d1_b0 | move-rot | 600 | 600 | 0 |
| d1_b1 | move-rot | 600 | 600 | 0 |
| d1_b2 | move-rot | 600 | 600 | 0 |
| **Median** | | **600** | **600** | **0** |

## D2 SHIFT (total reward, 600 ticks)

| Variant | Shift | R_home | R_true | Gap |
|---------|-------|--------|--------|-----|
| d2_s0 | inversion | -1500 | 4500 | 6000 |
| d2_s1 | inversion | -1500 | 4500 | 6000 |
| d2_s2 | inversion | -1500 | 4500 | 6000 |
| d2_s3 | inversion | -1500 | 4500 | 6000 |
| d2_s4 | inversion | -1500 | 4500 | 6000 |
| d2_s5 | inversion | -1500 | 4500 | 6000 |
| **Median** | | **-1500** | **4500** | **6000** |

Reference: Z (random) median on shifted = -1125. P (optimal) = 4500.
R_home performs worse than random (harm category H1).

## D3 TOOL (total reward, 600 ticks)

| Variant | Shift | R_home | R_true | Gap |
|---------|-------|--------|--------|-----|
| d3_s0 | degradation | 45084 | 52000 | 6916 |
| d3_s1 | degradation | 45084 | 52000 | 6916 |
| d3_s2 | degradation | 45084 | 52000 | 6916 |
| d3_s3 | degradation | 45084 | 52000 | 6916 |
| **Median** | | **45084** | **52000** | **6916** |

Reference: Z (random) median on shifted = 27062. P (optimal) = 52834.
R_home outperforms random but underperforms optimal (harm category H2).

## Summary

| Domain | Median gap | Harm? |
|--------|------------|-------|
| D1 | 0 ticks | No |
| D2 | 6000 reward | Yes (severe) |
| D3 | 6916 reward | Yes (moderate) |

K1: Harm replicates in 2/3 domains. **PASSES** (kill threshold is <2/3).
