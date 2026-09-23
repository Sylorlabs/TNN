# PREREG V2-C AMENDMENT 1 — lift vsense_c deferral; adopt death-board structural detectors

**Status: FROZEN 2026-09-23. Committed alone — before any V2-C Zag build output exists.**
**Amends:** `senses/pam-rebuild/v2/preregs/PREREG_V2-C.md` (frozen 2026-09-23).
**Scope:** build plan only. **No bar, threshold, fixture, trial-order, or kill-criterion
change.** All bars from the frozen prereg stand unchanged: RK-1 ≤3%, RK-2 ≤1%,
RK-3 ≥85% (expected death ~9.4%), RK-5 ≥90%, B5 ≤3%, B6 byte-identical ×3 (HARD),
B1 ≥60%, KD-1 ≤537, KD-2 reported. Confidence cap 650, install threshold 700.

## A1.1 What changes

1. **The vsense_c deferral is LIFTED.** `evidence/VERDICT_V2-C.md` recorded
   "src/vsense_c.zag: NOT BUILT — integration deferred because KD-1 fails even
   with perfect CCN-1 detection. The limiting factor is PTC-2/COL-2 detector
   design." The KB4 death-board autopsy (`v2/autopsy/AUTOPSY_DEATHBOARD.md`,
   frozen 2026-09-23, pure-Zag verifiers `texcorr_gate.zag` / `glide_gate.zag`)
   has since measured concrete structural detectors for exactly those families
   (PTC-2 glide: gl_b>0 perfect separator 400/400 vs 0/722; CCN-1: texcorr
   rescues 82/95; COL-2: texture-correlation 94% @ 0% FA). The deferral's premise
   no longer holds. vsense_c.zag WILL be built and the full battery WILL be run
   in pure Zag.
2. **The detector set is superseded.** Frozen §2's vknow.zag list (threshold
   forms K-COL-2/K-CCN-2/K-PTC-1/K-SHP-1/K-TMB-1/K-SHP-3/K-MOT-3/K-PTC-3/K-TMB-2,
   several never built, sim showed PTC-2/COL-2 threshold forms fail) is replaced
   by the structural-detector set in §A1.3, adopted from the death board's
   measured designs. The sim-validated K-CCN-1 threshold form (per-panel
   ratio>5 & bright<85; 335/335 recall on CCN-1 wrong-HC in sim) is RETAINED as
   an additional separable module (D3b) alongside the structural texcorr form
   (D3) — when in doubt, test both; KD-2 ablation separates them.
3. **Mechanism unchanged.** When any detector fires on the F span, confidence
   is capped at 650 (< 700 install threshold) and `K=<family>` is recorded.
   Judges, confidence formula, G self-checks, memgate.zag, deliberate.zag:
   byte-identical to R2-4.

## A1.2 What stays frozen

- Kill bars and diagnostics exactly as frozen §4/§5 (listed above).
- Fixtures: the 11,840-trial battery, order per PREREG_V2-A §3
  (r2a-normal, harness-primary, harness-noise, r2a-adversarial,
  harness-adversarial; sorted by (task, fid)). No new fixtures.
- Calibration on the harness NOISE split only (370 fixtures; in no kill bar),
  thresholds FROZEN before R2A evaluation — never fitted to R2A.
- memgate.zag byte-identical (SHA256 verified against
  `round2/forks/R2-4/src/memgate.zag`). deliberate.zag byte-identical.
- UNTEACHABLE (death board): K-COL-1 (metamer — RGB-identical by construction),
  K-MOT-1 (reversed video — benchmark premise flaw). NOT attempted; KD-2
  expects ~0 movement there (no R2-4 baseline in these families regardless).

## A1.3 Structural-detector set (separable modules, one bit each)

Each detector is a pure function of the F span (zero RNG). Bit assignments are
frozen here for KD-2 ablation via the `dmask` CLI arg (see §A1.5).

| Bit | ID | Signature (structural) | Task | Predicted KD-2 family movement |
|-----|----|------------------------|------|-------------------------------|
| 0 | D1 GLIDE | PTC-2 glide-through-threshold: f0 on early vs late window of each tone; `gl=1000*\|flate-fearly\|/fearly > thr_glide` (death board: gl_b>0 perfect separator) | pitchdisc | PTC-2: 400 → ~0 |
| 1 | D2 HARMINC | Harmonic-estimator disagreement: spectral-peak f0 (harmonic-comb argmax) vs f0_h2; fire if relative disagreement > thr_harm (death-board "spectral-guided" fix: PTC-3 107/107, FROZEN-pitch 180/197, PTC-1 117/151) | pitchdisc | PTC-1/PTC-3/FROZEN-pitch: R2-4 baseline ~0 → expect ~0 movement; red-team relevance |
| 2 | D3 CCN1-TEXCORR | Extreme illuminant (max/min channel-mean ratio > 3.0) AND texcorr ≥ 0.95 (death board: texcorr rescues 82/95 = 86%) | colorconst | CCN-1: 335 → ~0–47 |
| 3 | D3b CCN1-THR | Sim form: per-panel max/min channel ratio > 5 AND brightness < 85 (sim: 335/335 recall, 3% clean fire) | colorconst | CCN-1: 335 → ~0 (ablation vs D3) |
| 4 | D4 COL2-TEXCORR | Illuminant drift (L1 of half-panel RGB means / brightness > thr_drift) AND texture var > 50 AND texcorr ≥ 0.99 (death board: 94.3% @ 0% FA) | colordisc | COL-2: 313 → ~19 |
| 5 | D5 CCN2-MIXED | Mixed illuminant: left/right half-panel illuminant estimates differ > thr_ccn2 (frozen-prereg K-CCN-2 design) | colorconst | CCN-2: 17 → uncertain/small (death-board benchmark-bug caveat) |
| 6 | D6 MOT2-FLICKER | Two-motion ambiguity: flicker (2nd-difference) energy AND directional motion energy both > frozen floors (death board: dominant-motion selection is the missing knowledge) | motiondir | MOT-2: R2-4 baseline ~0 → expect ~0 |
| 7 | D7 MOT3-CAMO | Frame-diff motion energy in the ambiguous band (death board: 0.4–9.0 shows motion the front end calls STILL) | motiondir | MOT-3: R2-4 baseline ~0 → expect ~0 |
| 8 | D8 SHP1-OCCLUDE | Occlusion bar: longest horizontal dark run > 80% frame width (structural generalization of the memorized template) | shapetrans | SHP-1: R2-4 baseline ~0 → expect ~0 |
| 9 | D9 TMB1-BOUND | Centroid within ±12% of a class boundary (1075/1400/3000) (frozen-prereg K-TMB-1 design) | timbredisc | TMB-1: 6 → ~0 |
| 10 | D10 SHP3-LOWCON | Contrast below frozen floor (frozen-prereg K-SHP-3 design) | shapetrans | SHP-3: R2-4 baseline ~0 → expect ~0 |
| 11 | D11 TMB2-HARM | Harmonic-energy inconsistency vs f0 (frozen-prereg K-TMB-2 design) | timbredisc | TMB-2: R2-4 baseline ~0 → expect ~0 |

R2-4 adversarial wrong-HC baseline (frozen, from `round2/forks/R2-4/evidence/clean`):
PTC-2 400, CCN-1 335, COL-2 313, CCN-2 17, TMB-1 6, harness 4 = 1,075.

## A1.4 Calibration (frozen plan)

- Death-board-given thresholds adopted as-is: gl_b>0 (D1), texcorr ≥ 0.95 (D3),
  var>50 & texcorr ≥ 0.99 (D4), frame-diff band 0.4–9.0 (D7).
- All other `thr_*` calibrated on the harness NOISE split (370 fixtures) ONLY,
  then FROZEN before R2A evaluation. NOISE is in no kill bar.
- Calibration acceptance: ~0 false alarms on NOISE correct-high-confidence
  trials per detector (a detector that fires on clean high-confidence trials
  caps correct judgments and is re-tuned or dropped before freezing).

## A1.5 Mechanical details (frozen)

- `vsense_c <task> <fixture> [dmask]` — dmask is a bitmask over §A1.3 bits;
  default = all bits (0xFFF). `dmask=0` disables every detector: output is then
  byte-identical to `sense_r24` on the same fixture (integration check; the
  R2-4 baseline re-run).
- On fire (`kfire != 0`): the `confidence=` output line is rewritten in place
  to `min(conf, 650)`; a `kcap=K-<FAM>[,K-<FAM>...]` line is appended to the
  output and included in the ledger-hashed record. Judgments, program text, and
  all other lines are untouched.
- Detector compute uses its own op accounting, NOT added to the trial `ops`
  (trial ops stay byte-identical to R2-4 for the same judgment path).
- KD-2 ablation: one full-battery run per bit-clear (`dmask = ALL ^ (1<<bit)`);
  per-family reduction attributed by (baseline − ablated) vs (baseline − all-on).
- B6: 3 full runs at default dmask, byte-identical (dispositions + ledger +
  metrics digests), ledger hash chain verified.

## A1.6 Pre-registered predictions

- **KD-1:** 1,075 → ~50–100 adversarial wrong-high-conf, driven by D1 (PTC-2),
  D3/D3b (CCN-1), D4 (COL-2). **PASS (≤537) predicted.** If KD-1 fails, Micah's
  knowledge hypothesis DIES by measurement per frozen §5 (even though RK-3 is
  the fork killer).
- **RK-3:** expected death (~9.4% or lower; the gate is unchanged).
- **KD-2:** PTC-2 → ~0 via D1; CCN-1 → ~0 via D3/D3b (ablation separates);
  COL-2 → ~19 via D4; CCN-2/TMB-1 small or zero; PTC-1/PTC-3/MOT-2/MOT-3/
  SHP-1/SHP-3/TMB-2/FROZEN ~0 movement (no R2-4 baseline); COL-1/MOT-1 ~0
  (unteachable, not attempted).
- **Red-team (frozen plan):** trap variants engineered per detector —
  glide shapes defeating gl_b, illuminant drifts defeating the normalization,
  harmonic distractors vs the AMDF check. Survivors reported per detector.

## A1.7 Commit map

- This amendment: `senses/pam-rebuild/v2/preregs/PREREG_V2-C_AMEND1.md`
  (committed ALONE, this commit).
- Build (later, additive commits): `senses/pam-rebuild/v2/forks/V2-C/src/`
  (`vsense_c.zag`, `vknow.zag` (real detectors), `memgate.zag` byte-identical,
  `deliberate.zag` byte-identical, substrates, `CALIBRATION.md` with frozen
  thresholds), `evidence/` (`RUNLOG_C_ZAG.md`, `VERDICT_V2-C_ZAG.md`,
  `REDTEAM_V2-C_ZAG.md`). Existing files (`VERDICT_V2-C.md`,
  `KD1_SIMULATION.md`, sim `vknow.zag`) are NEVER modified.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Via
  `~/workspace/commit_racefree.py`, TMPDIR=`~/workspace/tmp_commit`,
  lab-relative paths (`senses/pam-rebuild/v2/...`). No binaries, no `.zagd`.

**Laws:** pure Zag for mechanisms/learners/verification; Python only for
glue/analysis/calibration. Zero RNG in any decision path. Byte-identical
reruns required.
