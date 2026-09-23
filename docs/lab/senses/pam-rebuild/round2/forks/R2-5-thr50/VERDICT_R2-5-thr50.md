# VERDICT_R2-5-thr50: colordisc threshold recalibration probe

**Date:** 2026-09-23. **Crew:** PAMs v2 gap crew D (calibration claim + benchmark integrity).
**Status:** EXPERIMENTAL FORK — additive only. R2-5 is untouched.

## Question

The autopsy death-board (v2/autopsy/AUTOPSY_DEATHBOARD.md, §R2-5) claims R2-5's
colordisc threshold of 15 ("calibrated") is miscalibrated vs an optimal 5.0 on
the same data, with 268/720 DIFFERENT judgments "missed avoidably," verdict
KNOWLEDGE (calibration failure). This fork tests the claim end-to-end: change
ONLY the threshold constant 15 → 5.0, rerun the frozen battery in pure Zag,
and measure the effect on judgments, promotion bars, and false installs.

## What changed (exact)

File: `src/sense.zag`, function `x_colordisc` (Task 1, colordisc), lines 127–130.
Byte-identical to R2-5's committed `src/sense.zag` (sha256
`4542471a0bb4a7c91366ca01ae0a16b4187a323fc829751bf70f113b1d42023f`)
except:

```diff
-    // dist>15: DIFFERENT (calibrated: hard DIFFERENT de=2.4-4.0; sampling noise)
-    if(dist > 15) { ji = 1; }
+    // dist>5: DIFFERENT (R2-5-thr50: recalibrated from 15 to 5.0; see VERDICT_R2-5-thr50.md)
+    if(dist > 5) { ji = 1; }
     t_put32(jout, 0, ji);
-    let mg:i64 = iabs(dist - 15);
+    let mg:i64 = iabs(dist - 5);
     t_put32(cout, 0, (1000 * mg / (mg + 60)) as i32);
```

New file sha256: `a410fc52dde183c7dfe456a6ea015ff1bb815b30de7fd3595bfec0cac5916f2a`.
(`dist` is an integer (isqrt of squared panel-mean RGB distance), so the
threshold 5.0 is implemented as the integer constant 5. The margin term
`iabs(dist - 15)` is part of the same threshold constant — it is the
distance-from-threshold that drives the confidence
`1000*mg/(mg+60)` — and was changed with it.)

Everything else (all six front ends, predictive contract, deliberation,
ledger, native IO/sha256 modules) is byte-identical. Built with the pinned
toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Zero RNG in decision paths. Byte-identical reruns: 8/8 paired single-fixture
runs (4 fixtures × full/ablate) produced byte-identical stdout.

## Method

Frozen battery = the R2A fixture set on this VM (5,100 normal r2n_*, 5,815
adversarial r2a_*), run through the same harness logic as R2-5's
run_battery.py (12 workers; subprocess per fixture; truth from
`<fixture>.truth`). Two binaries, both built from committed sources:

- **orig**: R2-5 committed `src/` rebuilt verbatim (threshold 15) — clean A/B baseline.
- **thr50**: identical except the constant above (threshold 5.0).

Batteries: `evidence/thr50_full_r2n.txt`, `evidence/thr50_full_r2a.txt`,
`evidence/thr50_ablate_r2n.txt`, `evidence/thr50_ablate_r2a.txt`;
baselines: `evidence/orig_full_r2n.txt`, `evidence/orig_ablate_r2n.txt`.

## Results (clean A/B on identical frozen fixtures)

### Colordisc front-end (the recalibrated mechanism)

| Metric | orig (thr 15) | thr50 (thr 5.0) | Delta |
|---|---|---|---|
| DIFFERENT recall | 61% (440/720) | 94% (679/720) | **+33pp, −239 FN** |
| DIFFERENT false negatives | 280/720 | 41/720 | −239 |
| SAME false positives | 0/360 | 18/360 | +18 |
| Promoted precision (colordisc) | 86% (710/819) | 99% (521/522) | +13pp |
| Escalated (colordisc) | 261 | 558 | +297 |
| False installs, ablate (colordisc) | 280/1080 | 59/1080 | −221 |

The death-board's headline is **CONFIRMED in substance**: ~280 DIFFERENT
judgments were missed avoidably at threshold 15 (their figure: 268/720 —
the 12-fixture gap is float-vs-integer distance rounding; see note below).
Threshold 5.0 recovers 239 of them at a cost of 18 new SAME false positives.

Note on numbers: the death-board reports "SAME median 0.5 (max 15.4);
DIFFERENT median 21.7 (min 2.4); 1/360 SAME FP; best threshold 5.0 → 95.65%
accuracy." Direct integer measurement of the front-end's `dist` on the frozen
fixtures: SAME n=360 min=0 max=15 median=1; DIFFERENT n=720 min=2 max=123
median=21. thr>15: 0 FP / 280 FN (74% acc). thr>5: 18 FP / 41 FN (94.5% acc).
Best integer threshold is actually >4 (96.2%), not >5 — the qualitative claim
(threshold 15 is far from optimal; ~5 is near-optimal) holds either way.

### Kill-bar state changes (VERDICT_R2-5.md bars, normal/full battery)

| Bar | Required | orig (rebuild) | thr50 | State change |
|---|---|---|---|---|
| Promotion precision (normal) | ≥95% | 94% (4476/4758) | **96% (4287/4461)** | **FAIL → PASS** |
| Promotion recall (normal) | ≥80% | 96% | 88% | PASS → PASS |
| Escalation (normal) | ≤5% | 6.7% (342/5100) | 12.5% (639/5100) | FAIL → FAIL (worse) |
| RK-1 false installs (normal) | ≤3% | 9.4% (480/5100) | 5.1% (259/5100) | FAIL → FAIL (improved) |
| RK-4 ablation installs (adv) | ≥100 | 5810/5815 (thr50) | 5810/5815 | PASS |
| B4 reduces false installs (adv) | yes | — | 2654 < 2818 | PASS |
| B4 contract delta (adv) | ≥10% | — | 2.8% (164/5815) | **was 10.06% PASS → 2.8% FAIL** |

(Adversarial/full reference: accuracy 51% (2992/5815), precision 45%,
recall 73%, escalation 16% — improved accuracy/precision vs the verdict's
39%/36%, at higher escalation.)

**The fork still dies, but the death cause changes.** The precision bar that
killed R2-5 now PASSES — the threshold claim is vindicated as far as it goes.
But the threshold is coupled to the confidence margin: with threshold 5,
fixtures near the boundary get low confidence (`1000*mg/(mg+60)`), so the
contract/deliberation pipeline withholds far more — escalation more than
doubles (6.7% → 12.5%, bar ≤5%) and RK-1 still fails (5.1% > 3%). The
threshold constant alone is not the fix; the confidence calibration is part
of the same miscalibration. **This strengthens the KNOWLEDGE verdict**: the
signal and the fix were both knowable from the data, but the fix requires
recalibrating the confidence model with the threshold, not swapping one
constant.

## Fidelity caveat (material)

The committed R2-5 evidence (`evidence/battery_full_r2n.txt`: prec 86%,
esc 151/5100) is **not reproduced** by rebuilding the committed `src/`
(rebuild: prec 94%, esc 342/5100; 247/5100 judgment diffs; colordisc
confidence differs on all 1,080 fixtures, 2× off — e.g. 400 vs 200).
Either the fixtures were regenerated after the evidence run or the evidence
came from an older build. The A/B above is clean (both binaries from
committed src on identical fixtures); the absolute numbers differ from the
verdict's, but every bar-state *change* was verified on the clean A/B pair,
and the precision flip (86%→96% vs 94%→96%) holds against the committed
evidence baseline too.

## Conclusion

- Death-board claim CONFIRMED: threshold 15 vs optimal ~5.0 is a genuine
  calibration failure; 280/720 DIFFERENT judgments (their 268, rounding)
  were missed avoidably; verdict KNOWLEDGE stands.
- The single-constant fix flips the precision bar to PASS but doubles
  escalation and leaves RK-1 failing — the fork still DIES. A correct fix
  must recalibrate the confidence margin with the threshold.
- Additive only: R2-5 untouched. No frozen state modified.

## Evidence

- `src/sense.zag` (+ native modules, byte-identical to R2-5's)
- `evidence/thr50_full_r2n.txt`, `evidence/thr50_full_r2a.txt`,
  `evidence/thr50_ablate_r2n.txt`, `evidence/thr50_ablate_r2a.txt`
- `evidence/orig_full_r2n.txt`, `evidence/orig_ablate_r2n.txt` (A/B baselines)
- This verdict.
