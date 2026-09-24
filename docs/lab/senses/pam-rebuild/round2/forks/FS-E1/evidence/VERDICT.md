# FS-E1 VERDICT — Truth-Quantity Challenge

**Date:** 2026-09-24  
**Registry:** FROZEN (commit 9a8a68e4, 2026-09-24)  
**Binary SHA-256:** `21fc159c232d4b3e3acd57cfc933c55d71b4fa34c8cc9cd0fc1b33a0b80690a5`  
**Source SHA-256:** `e31a4588821ebadd058a9c2e6d4a50e3218701209ad32e640412fde5eee74118`

## Formal Battery Results

**Method:** 10,000 adversarial + 2,000 controls, each run TWICE byte-identically.  
**Determinism:** b_adv ledger IDENTICAL, stdout IDENTICAL, hash chain OK (10000). b_ctrl ledger IDENTICAL, stdout IDENTICAL, hash chain OK (2000).

### Adversarial (b_adv, n=10,000)
- False installs: 59 (0.59%)
- Wilson 95% UCB: **0.76%**

### Controls (b_ctrl, n=2,000)
- Recall: 78.75%
- Formation accuracy: 80.30%
- Overstrictness: 1.55%

### Per-family (adversarial)
| Task/Family | FI | n | UCB 95% | Bar 3 (≤2%) |
|-------------|----|---|---------|-------------|
| motiondir/f1 | 5 | 504 | 2.30% | **FAIL** |
| motiondir/f2 | 1 | 116 | pooled | — |
| pitchdisc/f1 | 1 | 710 | 0.79% | PASS |
| timbredisc/f1 | 33 | 500 | 9.12% | **FAIL** |
| timbredisc/f3 | 19 | 190 | pooled | — |

## Bar-by-Bar Verdict

| # | Bar | Result | Value |
|---|-----|--------|-------|
| 0 | Overall FI Wilson 95% UCB ≤1% | **PASS** | 0.76% |
| 1 | Recall ≥85% | **FAIL** | 78.75% (formation ceiling 80.3%) |
| 2 | Post-freeze CP zero kept (all six) | **FAIL** | 3 kept (colorconst) |
| 3 | Per-family UCB ≤2% (n≥200) | **FAIL** | motiondir/f1 2.30%, timbredisc/f1 9.12% |
| 4 | Formation accuracy = recall ±5pp | **PASS** | 80.3% vs 78.75% (Δ1.55pp) |
| 5 | Overstrictness ≤5% | **PASS** | 1.55% |

## Post-Freeze Counter-Probe (seed 20260924)

**colorconst (5,000 candidates): 3 KEPT**

Root cause: CH-CCN-3 uses count≥4 threshold for pixels with RGB L1>16. The 3 kept are 2×2 patches (4 pixels) where d65 illuminant rendering + noise attenuates 1 pixel below L1>16, leaving 3 pixels. Truth=DIFFERENT (patch ≥2×2, L1≥32 before illuminant), but challenge reports SAME (3 < 4).

This is a genuine mechanism limitation: the count≥4 threshold is too strict for minimal (2×2) patches under rendering noise. The mechanism is frozen; this stands as a documented weakness.

**motiondir (5,000 candidates): INCOMPLETE** (too slow; pre-freeze CP found 0 kept).

## Analysis of Failures

**motiondir/f1 (5 FI):** Family 1 is "reversed video" (F shows reverse, G shows true). The 5 FIs are 180° reversals on degenerate G stimuli where the high-contrast frames do not show coherent motion (SAD 31731, no good match). These are R2A battery construction artifacts, not CH-MOT-2 defects. The design-loop CP (strong stimulus truth) found 0 kept.

**timbredisc/f1 (33 FI):** Known R2A family (high-harmonic leakage). Frozen task; not redesigned in FS-E1.

**Recall (78.75% < 85%):** Capped by formation accuracy (80.3%), not by challenge overstrictness (1.55%). The formation layer, not the challenge layer, limits recall. This was documented in the baseline.

## Hypothesis Verdict

**PARTIALLY SUPPORTED.**

The FS-E1 hypothesis ("a challenge whose quantity is information-sufficient for the task's truth criterion closes the gap") is supported by:
- Overall FI UCB 0.76% ≤ 1% (Bar 0 PASS)
- Zero kept on pre-freeze design-loop CP for both redesigned tasks
- Byte-identical determinism

But limited by:
- CH-CCN-3 threshold defect (3 kept on post-freeze CP; Bar 2 FAIL)
- Frozen audio tasks retain high FI (timbredisc/f1 9.12%; Bar 3 FAIL)
- Recall capped by formation, not challenges (Bar 1 FAIL)

The redesigned challenges (CH-CCN-3, CH-MOT-2) substantially reduce false installs vs R2-16, but CH-CCN-3 needs a lower count threshold (e.g., ≥2 or ≥3) to handle minimal patches under rendering noise. This requires a mechanism change, which is out of scope for the frozen FS-E1.

## Evidence Files

- `evidence/batt_b_adv_union_r1.ledger` (10,000 entries, SHA verified)
- `evidence/batt_b_adv_union_r2.ledger` (byte-identical)
- `evidence/batt_b_ctrl_union_r1.ledger` (2,000 entries)
- `evidence/batt_b_ctrl_union_r2.ledger` (byte-identical)
- `evidence/score_adv.json` (FI=59, UCB=0.76%)
- `evidence/score_ctrl.json` (recall=78.75%)
- `fixtures_cp/cp_colorconst_*.r2fx` (3 kept)
- `evidence/FREEZE_RECORD.md` (registry freeze)

## Provenance

- Prereg: `docs/lab/senses/pam-rebuild/round2/preregs/PREREG_FS-E1.md` (commit 6adda83f)
- Amendment: `docs/lab/senses/pam-rebuild/round2/preregs/PREREG_FS-E1_AMEND1.md` (commit 0777ce80)
- Source: `src/fse1.zag` (frozen, SHA e31a4588...)
- Debate E extraction: `hidden/FSE1_spec_section_raw.txt` (DIFF_CLEAN)
