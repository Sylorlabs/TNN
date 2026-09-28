# COMPARISON NOTE R2-4 → R2-5: does the self-result field carry load?

**Date:** 2026-09-23
**Status:** FINAL — R2-4 battery complete (11,840 trials, byte-identical across two independent runs)
**R2-4 verdict:** DEAD (RK-3: 9.4% vs 85% bar — H2's single-belief gate withholds correct conflicting percepts)

R2-5's preregistered decider (PREREG_R2-5.md §5): *if R2-5 matches or beats R2-4 on
RK-1, RK-3's analog (promotion recall ≥ 80%), and B4 with strictly less machinery
(no result field, no self-flag computation), the self-result field is declared
decorative and R2-4's RK-5 claim is closed as load-free. If R2-5 underperforms R2-4
on safety or recall, the field carries load and survives.*

## Head-to-head on the identical R2A fixture subset (10,915 trials: 5,100 normal + 5,815 adv)

R2-5's battery ran the 10,915 R2A fixtures (no harness). R2-4's numbers below are
computed on the same 10,915 fixture files with the same truths, from R2-4's
frozen battery (gate state from the full 11,840-trial stream, per the frozen
trial order). Same definitions both sides.

| Comparison axis | R2-5 (measured) | R2-4 (measured, same subset) | Winner |
|----------------|-----------------|------------------------------|--------|
| **RK-1 safety:** false permanent installs (normal) | 13% (663/5,100) — FAILED its ≤3% bar | **0.0% (0/5,100)** | R2-4 |
| **RK-1 safety:** false permanent installs (all R2A) | — | **0.0% (0/10,915)** | — |
| **Promotion recall** (correct high-conf → PASS-and-install, normal) | 98% — PASS | **1.7% (12/686)** | R2-5 |
| Promotion recall, reach-PASS only (normal) | — | 85.7% (588/686) | — |
| **Promotion precision** (normal) | 86% (4,286/4,949) — FAILED its ≥95% bar | **90.9%** of installed (3,009 installed) | R2-4 |
| **B4 contract delta** (adv) | 10.06% (585/5,815) — PASS | **22.1%** (1,286/5,815) | R2-4 |
| **B4 reduces false installs** (adv) | 3,498 → 3,293 — PASS | **392 → 36** | R2-4 |
| RK-5 independent-evidence self-flag (wrong high-conf) | n/a (no field) | **99.4%** (1,098/1,105) | R2-4 (uncontested) |
| Escalation rate | 2% (151/5,100, normal) | 0.06% (7/10,915) | R2-4 |

## Reading for R2-5's decider

The decider requires R2-5 to match-or-beat R2-4 on **all three** of RK-1,
promotion recall, and B4. Scorecard:

- **RK-1 (safety): R2-4 wins decisively** — 0 false permanent installs on 10,915
  R2A trials vs R2-5's 663/5,100 (13%). The self-result field + gate withholds
  what R2-5's withholding-first design installs.
- **Promotion recall: R2-5 wins** — 98% vs R2-4's 1.7% PASS-and-install.
  Caveat for the record: R2-4's recall failure is the **gate's** single-belief
  slot (CONFLICT_WITHHELD on mixed-truth streams — the RK-3 kill), not the
  self-result field: the field itself reaches PASS on 85.7% of correct
  high-confidence normal percepts. R2-5's recall advantage comes from having no
  conflicting-belief memory at all — which is also why it installs 663
  falsehoods.
- **B4 (contract load-bearing): R2-4 wins decisively** — 22.1% disposition delta
  vs 10.06%; residual false installs 36 vs 3,293. The contract does far more
  filtering work in R2-4.

**Conclusion for the decider:** R2-5 beats R2-4 on exactly one of the three
axes (promotion recall) and loses badly on the other two (safety 13% vs 0%,
B4 10.06%/3,293 vs 22.1%/36). The decider's condition (match-or-beat on all
three) is NOT met. **The self-result field is not decorative: it carries load
and survives.** R2-4's RK-5 claim (99.4% independent-evidence self-flagging,
the 38.9% → 99.4% repair) stands as load-bearing — R2-5 has no mechanism that
reproduces it.

Note: both forks are DEAD under their own frozen bars (R2-4 on RK-3, R2-5 on
promotion precision). The comparison above is informational per PREREG_R2-5.md
and does not resurrect either fork.
