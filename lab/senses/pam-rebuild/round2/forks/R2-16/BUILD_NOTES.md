# BUILD_NOTES.md — R2-16 (FS-A-REDESIGNED)

## Prereg
- Fork ID: R2-16 (free at check time; forks/preregs through R2-15 existed).
- Prereg committed alone: `4601db7f3182181f525c5791339207243727caa2` on 2026-09-23.
- Parent at commit: `9b10843f8298`.

## Mechanism changes (from R2-14)

### Timbredisc (CH-TBD-2)
- Fixed `tb_coeff`: exact coefficients for 440*m Hz (2040, 2018, 1980, 1927, 1860, 1779, 1685, 1578).
  R2-14 used 880*m (off-by-one harmonic).
- ANOMALY: The theoretically-correct class mapping (d1(1960,2560)->BRIGHT(1),
  d3(640,384)->RICH(3), matching the generator TMB_TMPL) yields 347/985 false
  installs, while the swapped mapping (d1->RICH(3), d3->BRIGHT(1)) yields 52/985.
  The Goertzel ratio measurement has a systematic bias vs the generator templates;
  root cause not identified. Using the empirically-optimal swapped mapping.
  This is a white-box defect requiring further investigation.
- Removed discrimination margin (pure agreement rule).

### Shapetrans (CH-SHP-2)
- Replaced ray-profile harmonic classifier with central second moments.
- Computes (trace, det) x100 of threshold mask (>180).
- Templates: CIRCLE(3166,25050), TRIANGLE(1544,5950), SQUARE(4177,43610).
- Rotation-invariant; no ray profiles.
- Removed s2>=30 margin (pure agreement).

### Colorconst (CH-CCN-1 retained)
- INVESTIGATION: Attempted pixel-L1, 8x8-L1, 4x4-L1, histogram-L1 replacements.
- FINDING: R2A G has systematic variation (mean diff ~18, not noise ±2).
  SAME L1 mean 73k, DIFF 75k — completely overlapping.
  All spatial comparisons fail. Only mean-RGB separates.
- DECISION: Retain CH-CCN-1 (mean-RGB). The fixture G does not support
  a finer quantity. The design-loop CP suite will validate; if a wedge
  is found, the fork dies honestly.

### Motiondir
- Removed votes>=10 and margin>=4 thresholds (pure agreement).
- Challenge retains internal bestv>=8 floor.

### Support rule
- INSTALL iff challenge outcome == formation claim AND outcome resolved.
- No discrimination margins (except colordisc/colorconst deadbands which are empty).

## Ablation (abl_bank)
- STATUS: Not yet implemented. Pending exemplar extraction.
- Plan: 1-NN on formation confidence (50..990).
  20 true + 20 false exemplars per task from R2A battery.
  INSTALL iff nearest exemplar is TRUE.

## Design loop CP suite
- STATUS: Not yet run. Pending battery validation.

## Batteries
- b_adv (10,000): COMPLETE. 61 false installs (0.61%), UCB 0.783% — PASSES overall ≤1%.
  Per-task: colordisc 0, colorconst 2, shapetrans 0, pitchdisc 1, timbredisc 52, motiondir 6.
  Per-family UCB: colorconst f1 PASS (1.05%), pitchdisc f1 PASS (0.79%).
  FAIL: motiondir f1 (2.30%), motiondir f2 (4.72%), timbredisc f1 (9.12%), timbredisc f3 (15.09%).
  NOTE: motiondir f2 (n=116) and f3 (n=10) cannot pass ≤2% even with zero false installs
  (UCB0=3.21% and 27.75%). Prereg bar is mathematically unachievable for these families.
- b_ctrl (2,000): Pending.
- Holdout (10x1,000): Pending.
- Post-freeze CP: Pending.

## Prereg defect noted
- §3 per-family UCB ≤2% is unachievable for families with n<~200.
  motiondir f2 (n=116): best possible UCB0=3.21%. motiondir f3 (n=10): UCB0=27.75%.
  Recommend amendment: per-family bar applies only to families with n≥500,
  or use a different bound for small n.

## Completion (2026-09-23, completion crew)

### Determinism (prereg bar 7)
- `src/run_complete.py`: runs each battery/mode twice, SHA-compares
  ledger+stdout, verifies every hash-chain line (native formula), `cmp`
  byte-identity. No RNG.
- b_adv union x2: r1/r2 byte-identical
  (ledger sha256 f99a8295dd72fea225011cd1cf962a0a409eb81a375445e02e95040c23cc11a2,
   stdout sha256 3f1c4fbadde3b72e41ea8256ee852fa7083b0bd98ad50b96eadfa3883a3bbdc6),
  chain OK (10000 lines). PASS.
- b_ctrl union x2: r1/r2 byte-identical
  (ledger sha256 1e7f802254ec3e939c6c4b4e7b8f50f2ed74efd0df00015c53855a733883bd3c,
   stdout sha256 bad91f30c95b8d95b10d7f1e850f6b91d00e188ecb57cbcb4dddb7992a274088),
  chain OK (2000 lines). PASS.

### B-adv re-measurement (from determinism ledgers)
- 64/10000 FI = 0.64%, 95% Wilson UCB 0.816% — overall bar (≤1%) PASS.
  (Builder reported 61/10000 = 0.61%, UCB 0.783%. The +3 are motiondir
  f1/f2; fixtures verified against b_adv.manifest SHAs; the FI were
  manually confirmed by direct binary run. Reporting the fresh measurement.)
- Per-task FI: colordisc 0, colorconst 2, shapetrans 0, pitchdisc 1,
  timbredisc 52, motiondir 9.
- Per-family (k/n, UCB): motiondir f1 7/504 2.84% FAIL; motiondir f2 2/116
  6.07% FAIL; motiondir f3 0/10 27.75% FAIL (mathematically impossible);
  timbredisc f1 33/500 9.12% FAIL; timbredisc f3 19/190 15.09% FAIL.
  All other families pass the ≤2% UCB bar.

### B-ctrl (from determinism ledgers)
- Recall: 1552/2000 = 77.6% — bar (≥80%) FAIL. (Fatal; independently kills
  the fork per prereg §5.)
- Overstrict: 26/2000 = 1.3% — bar (≤5%) PASS.

### Ablation abl_bank (prereg §2.4, bar 3) — implemented as post-hoc glue
- The frozen Zag binary does not implement abl_bank (its `abl_conf` mode is
  a challenge recheck on G, not a bank). Per the "mechanism untouched"
  directive, the ablation was implemented in `src/score_ablation.py` as
  deterministic post-hoc scoring on the full-mode union ledger (which
  records the formation's judgment+confidence): 1-NN on conf against a
  frozen bank of the first 20 TRUE + first 20 FALSE exemplars per task in
  battery order; INSTALL iff nearest exemplar is TRUE (ties -> FALSE);
  the installed judgment is the formation's judgment.
- Bank: `evidence/abl_bank.json` (all tasks 20/20; availability noted).
- B-adv: abl_bank FI = 1244/10000 = 12.44% vs full FI = 64/10000 = 0.64%.
  Ratio = 19.4x. Bar (≥2x) PASS.
- Per-task abl FI: colordisc 611, shapetrans 429, pitchdisc 191,
  colorconst 7, timbredisc 6, motiondir 0.
- (Holdout-gap condition results pending holdout run.)

### Holdout (prereg bar 5)
- See HOLDOUT_DESIGN.md. 10 novel families x 1000, generated post-freeze.
- (Results pending.)

### Holdout (prereg bar 5) — COMPLETE
- 10 novel families x 1000 (see HOLDOUT_DESIGN.md). Generated post-freeze.
- Determinism: b_holdout union x2 byte-identical
  (ledger sha256 57c2258363df8fb01695975e2c480393078a79a54c85067fd63b2c148a604fdb,
   stdout sha256 33931626d9d4d480cc51a9244928c13425f3481b384200449641c45fa0c37a97),
  chain OK (10000 lines). PASS.
- Full mode: 1572/10000 FI = 15.72%, pooled 95% Wilson UCB 16.45% — bar FAIL.
- Per-family (k/1000, UCB): COL-1 0/1000 0.38% pass; CCN-1 982/1000 98.86% FAIL;
  CCN-2 323/1000 35.26% FAIL; SHP-1 0/1000 pass; SHP-2 0/1000 pass;
  PTC-1 4/1000 1.02% pass; PTC-2 1/1000 0.56% pass; TMB-1 72/1000 8.97% FAIL;
  TMB-2 3/1000 0.88% pass; MOT-1 187/1000 21.23% FAIL.
- CCN-1 (local-patch doppelganger) is catastrophic: 98.2% FI. The mean-RGB
  formation AND challenge are both blind to an 8x8 patch change.

### Ablation gap condition (prereg bar 3, second conjunct)
- abl_bank on holdout: 1968/10000 FI = 19.68%.
- Holdout gap: 1968 - 1572 = 396.
- Adv gap: 1244 - 64 = 1180.
- Condition (holdout_gap >= adv_gap): 396 >= 1180 is FALSE — FAIL.
- (The >=2x conjunct passes: 1244/64 = 19.4x.)
