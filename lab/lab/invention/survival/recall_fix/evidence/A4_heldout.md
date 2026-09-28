# A4: Held-out Scoring (Experiment 1b, PREREG2)

## Sealed family

Before the fix was implemented (commit a4a8358b48), a held-out shift family
was frozen and committed:
- 4 D2 variants (d2_hs0..d2_hs3): ROTATION shift (different from in-sample INVERSION)
- 4 D3 variants (d3_hs0..d3_hs3): TOOL_2 degrades (different from in-sample TOOL_0)

SHA-256 log committed in `worlds/sealed/SHA_LOG.txt`. The fix was developed
without access to these variants.

## Results

### D2 held-out (ROTATION)

| Variant | R_home | D | Optimal (P) | Closure |
|---------|--------|---|-------------|---------|
| d2_hs0 | -1500 | 3900 | 4500 | 90.0% |
| d2_hs1 | -1500 | 3900 | 4500 | 90.0% |
| d2_hs2 | -1500 | 3900 | 4500 | 90.0% |
| d2_hs3 | -1500 | 3900 | 4500 | 90.0% |
| **Median** | **-1500** | **3900** | **4500** | **90.0%** |

In-sample closure: 90.0%. Held-out / in-sample = 100%.

### D3 held-out (TOOL_2 degrades)

| Variant | R_home | D | Optimal (P) | Closure |
|---------|--------|---|-------------|---------|
| d3_hs0 | 45056 | 50906 | 52620 | 77.3% |
| d3_hs1 | 45056 | 50906 | 52620 | 77.3% |
| d3_hs2 | 45056 | 50906 | 52620 | 77.3% |
| d3_hs3 | 45056 | 50906 | 52620 | 77.3% |
| **Median** | **45056** | **50906** | **52620** | **77.3%** |

In-sample closure: 80.7%. Held-out / in-sample = 95.8%.

## K4 Verdict

K4: "held-out closure under 50% of in-sample closure" = KILL.

- D2: 100% of in-sample. **PASSES**.
- D3: 95.8% of in-sample. **PASSES**.

The shared deliberation module generalizes to unseen shifts without domain-specific
tuning. The mechanism (distrust on observed<<claimed, systematic exploration) is
genuinely general, not overfitted to the in-sample shifts.
