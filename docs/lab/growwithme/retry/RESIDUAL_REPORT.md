# Residual Report — M3 Retry Miss Analysis

All misses classified per Crew 1's requirement: is each a coverage deficit (right fact absent from top-k), or something else?

## Summary

| Session | D misses | Withholds | Wrong-candidate | Coverage deficit |
|---------|----------|------------|-----------------|------------------|
| S1 | 1 | 0 | 1 | 0 |
| S2 | 5 | 4 | 1 | 0 |
| S3 | 7 | 6 | 1 | 0 |
| S4 | 2 | 1 | 1 | 0 |
| S5 | 13 | 5 | 8 | 0 |
| S6 | 14 | 5 | 9 | 0 |
| **Total** | **42** | **21** | **21** | **0** |

**Zero coverage deficits.** Every miss was either a tie-withhold (right fact in top-k but tied) or a wrong-candidate selection (right fact in top-k but outranked). Per Crew 1: "Any residual tie-break, unresolved/undiscriminatable outrank... kills M3."

## Case study 1: Wrong-candidate (F1-01 vs F1-20)

**Probe:** "Give the complete filesystem path where the pinned znc toolchain is installed."
**Key:** F1-01 ("The pinned znc toolchain lives at `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.")
**M3 trace:** Candidates F1-20:4, F1-01:3, ... Discriminators {pinned, installed, toolchain}. F1-20:3/3, F1-01:2/3. Verdict: single F1-20.
**Answer:** F1-20 text (policy, NO path). **WRONG.**

**Analysis:** F1-01 was rank 2 in the candidate set (score 3). Not a coverage deficit. M3 picked F1-20 because it matches "installed" (via "install" in "znc install"). The discriminator is spurious: F1-20 doesn't answer the question. M3 cannot understand that "path" in the question means the answer should contain a filesystem path. This is an **undiscriminatable outrank**: the wrong fact outranks the right fact on word overlap, and M3 has no mechanism to detect the semantic mismatch.

## Case study 2: Tie-withhold (F2-03 vs F2-07)

**Probe:** "What is the maximum tier movement promotion allows in a single step?"
**Key:** F2-03 ("Promotion moves a record up exactly one tier; it never skips tiers.")
**M3 trace:** Candidates F2-03:2, F2-07:2, ... Discriminators {single, tier, promotion}. F2-03:2/3, F2-07:2/3. Verdict: tie-withhold.
**Answer:** Withheld. **WRONG** (should have answered F2-03).

**Analysis:** Both candidates cover {tier, promotion}. Neither covers "single" distinctively. The tie is genuine per M3's definition, but F2-03 is clearly the right answer ("exactly one tier" vs F2-07's different content). M3 cannot discriminate because the distinguishing semantic ("one tier" = maximum movement) isn't captured by word overlap. This is a **residual tie-break** that kills M3.

## Scaling failure

The withhold rate increases with store size:
- S1 (20 facts): 0/18 withholds
- S2 (40 facts): 4/18 withholds
- S3 (60 facts): 6/18 withholds
- S5 (100 facts): 5/18 withholds (+ 8 wrong-candidate)
- S6 (120 facts): 5/18 withholds (+ 9 wrong-candidate)

As vocabulary saturates, discriminators lose power. M3 does not survive scale.

## Conclusion

M3, implemented faithfully to spec, fails calibration. The failures are mechanism-level (word-overlap discrimination is insufficient), not implementation bugs. Crew 1's kill conditions are met. M3 is dead.
