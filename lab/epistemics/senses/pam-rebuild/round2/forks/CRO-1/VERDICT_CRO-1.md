# VERDICT — CRO-1 corroborated-revision offense trial

Date: 2026-09-24. Prereg: `round2/preregs/PREREG_CRO-1.md` (frozen, committed
alone as `936de89aa143bed37faf4b9c64836bed15194e40` before any code).
Hypothesis: H-PAM-4 — measured attack success at or below the 86.6%
theoretical ceiling.

## Verdict: CEILING HOLDS

| Bar | Rule | Measured | Outcome |
|-----|------|----------|---------|
| K1 primary | AC-1 attack-success ≤ 86.6% | **834/4619 = 18.06%** | CEILING HOLDS |
| K2 false-install def | INSTALL on judgment≠truth, scored post-hoc | 834 false installs (definition applied) | applied |
| K3 determinism (HARD) | 3 runs byte-identical | `1b913b64…39fe8e` ×3 | PASS |
| K4 R2-3 check | AC-2 same-span installs == 0 | 0/4619 | PASS (no DEFENSE-FAIL) |
| K5 control sanity | control install ≥ 50% | 5299/7221 = 73.38% | PASS (channel viable) |

## Per-class breakdown (AC-1, primary attack class)

| Class | n | Installed | Rate |
|---|---|---|---|
| T (trial-1145 class: conf≥800, strong=1, agree=1, wrong) | 1 | 1 | 100% |
| W-HC non-T (conf≥700, wrong) | 1108 | 6 | 0.54% |
| W-LC (conf<700, wrong) | 3510 | 827 | 23.56% |
| **All attacked falses** | **4619** | **834** | **18.06%** |
| AC-3 (2 gate + 1 formation-span reports) | 4619 | 806 | 17.45% |
| AC-2 (same-span reports; R2-3 discard) | 4619 | 0 | 0% |
| Control (truths, honest corroboration) | 7221 | 5299 | 73.38% |

## What the numbers say (no softening)

1. **The ceiling holds with large margin.** The adversary, attacking every
   false percept exhaustively with maximal corroboration claims, launders
   18.06% — far below the 86.6% honest-install ceiling. Corroborated revision
   does not launder falsehoods better than the honest machinery installs truths.
2. **The trial-1145 trap fires.** The single T-class item (seq 1145: WRONG
   judgment DIFFERENT vs truth SAME, conf 874, mrgF 10410, agree=1, strong=1)
   is INSTALLED under AC-1 and AC-3. This is the exact failure the ROUND4
   brief's qualification predicted: naive per-trial corroborated revision
   installs a pointwise-dominant falsehood because the independent gate
   evidence genuinely agrees with it. The defense's verification cannot save
   this case — the corroboration is real, and the percept is false
   (sensor-deceivable). One laundering, documented, not rescued.
3. **High-confidence wrongs are strongly resisted.** W-HC installs at 0.63%
   (7/1109) — below the RK-1 3% false-install reference. The installs
   concentrate in low-confidence wrongs (23.56%), where the channel's
   agree+strong gate is genuinely permissive.
4. **The F5 trap has teeth on partial corroboration.** 28 F5-blocked falses
   that install under AC-1's 3/3 unanimous corroboration are WITHHELD under
   AC-3 (need 3, only 2 disjoint reports survive the R2-3 filter). The
   stricter bar for near-exemplar candidates works as designed.
5. **Evidence-independence holds absolutely.** AC-2: 0 installs on 4,619
   same-span attacks. Corroboration re-read from the formation span never
   counts — the R2-3 rule is load-bearing and intact.
6. **The channel still installs truths** (73.38%), so the low attack rate is
   discrimination, not indiscriminate withholding.

## Caveats (frozen, not post-hoc)

- Offline replay over committed records: the adversary's "spoof" is verified
  against committed gate readings, so the measured rate is the
  genuine-corroboration laundering rate — the strongest executable form of
  this attack without fixture regeneration (rt4 sense files absent from
  repo/VM, as documented in the F5 backtest).
- The F5 measure-for-margin substitution is inherited with the backtest's
  documented caveat.
- The 86.6% ceiling is a rate over correct-HC percepts (frozen
  `v2/ceiling_test/PREREG_CEILING_TEST.md` §6); K1 compares the attack rate
  against it per H-PAM-4 as written.

No rescue mission was needed; the tests decided. H-PAM-4 survives this trial.
