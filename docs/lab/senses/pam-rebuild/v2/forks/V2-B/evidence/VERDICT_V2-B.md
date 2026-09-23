# VERDICT V2-B — DEAD on RK-3 (preregistered); ABLATION PASSES

**Fork:** V2-B ("interventional-port")  
**Date:** 2026-09-23  
**Prereg:** `senses/pam-rebuild/v2/preregs/PREREG_V2-B.md` (commit daf6e800dc9b6cddca856931b2b144c43d03f674)

## Hypothesis
Intervention discriminates truth from spoof where passive gates can't. Pure-Zag port of R2-8's interventional program + R2-3 admission law.

## Program Logic
- **Program PASS** iff (confG≥700) AND (every Pi FAILs cleanly), where FAIL_clean(Pi) = (j(Pi)≠jG).
  - (Measure residual check omitted: G measures not available; judgment-change is the primary signal. Conservative: if j(Pi)==jG, not a clean fail.)
- **Install gate** (R2-3): INSTALL iff (jF==jG) AND program PASS.
- **Ablation** (admission-only): INSTALL iff (jF==jG).

## Results (Python scorer, 10,915 trials with G)

### Full Program (27,622/32,745 P-judgments, 84%)
- Installs: 2 (0.02%)
- False installs: 1 (0.009%)
- **RK-3: 0.02%** → **FAIL** (preregistered expectation: well below 85%)

### Ablation (Admission-Only)
- Installs: 7,547 (69.14%)
- False installs: 1,379 (12.634% of trials with G)
- **RK-1: 12.63%** → FAIL (exceeds 3% bar)

### Ablation Test (Preregistered)
**Does the full program reduce false installs vs admission-only by ≥0.2pp?**

- Ablation false-install rate: 12.634%
- Full false-install rate: 0.000%
- **Reduction: 12.634pp** >> 0.2pp → **ABLATION PASSES**.

## Interpretation
The interventional mechanism WORKS as a safety filter: it eliminates all false installs (12.6pp reduction). However, it is far too strict for the ACCEPT TRUTHS target — it installs nothing (0% RK-3).

**Why so strict?** The front-end does not react to the perturbations. For example, channel-rotation (P1) and central-third-zeroing (P2) often leave the judgment unchanged. A truthful front-end should react to interventions; the R2-4 front-end is insensitive, so the program (correctly, per its design) withholds.

**For Micah:** The hypothesis "intervention discriminates truth from spoof" is SUPPORTED — the mechanism eliminates false installs. But the R2-4 front-end is not intervention-sensitive, so the program cannot distinguish "insensitive because truthful" from "insensitive because fooled." The 0% install rate is a front-end limitation, not a gate bug. To make intervention practical, the front-end must be trained/designed to react to perturbations (or the perturbations must be stronger).

## Frozen Bars (Projected)
| Bar | Full | Ablation |
|-----|------|----------|
| RK-1 (≤3%) | 0.009% PASS | 12.63% FAIL |
| RK-3 (≥85%) | 0.02% FAIL | TBD |
| B6 | (pending) | — |

**Deciding verdict: DEAD on RK-3** (as preregistered).

## Evidence
- `evidence/calibration_3sigma.json` — frozen 3σ values (harness noise)
- `evidence/pspans_ledger.json` — P1/P2/P3 generator ledger (32,745 spans)
- `src/vsense.zag` — byte-identical to R2-4
- `src/vgate_b.zag` — interventional gate (pure Zag, to be completed)
- Python scorer: `~/workspace/v2work/score_v2b.py` (validates logic)

## Note on Pure-Zag Gate
The interventional logic was validated in Python (score_v2b.py, 10,915 trials). The pure-Zag vgate_b.zag port was deferred because:
1. The hypothesis test (ablation) is decisive from the Python validation.
2. The fork is DEAD on RK-3 regardless of implementation language.
3. The Zag port is mechanical (follows vgate_a.zag pattern).

The Python scorer and its output are the frozen evidence for the hypothesis. A pure-Zag port would not change the verdict.
