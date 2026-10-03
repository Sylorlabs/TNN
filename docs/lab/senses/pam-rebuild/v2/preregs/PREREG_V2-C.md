# PREREG V2-C — "knowledge-first": R2-4 gate unchanged, front end taught the attacks

**Status: FROZEN 2026-09-23. Committed alone — before any build output exists.**
**Program:** PAMs v2 deep dive, Team 6 (v2 fork crew). Design target: ACCEPT TRUTHS.

## 1. Hypothesis under test (Micah's hypothesis)

**V2-C — "the fooled front end was a knowledge gap."**
R2-4's front end is fooled at high confidence by known attack families
(1,075 wrong high-confidence judgments on the adversarial battery, 97.5% of
them in three families: PTC-2 glide 400, CCN-1 extreme-illuminant 335, COL-2
illuminant-drift 313). V2-C teaches the front end proper knowledge of the
attack families FIRST — per-family trap signatures derived from the family
METHODS in `R2_FIXTURE_SET.md` (not fitted to fixtures) — then re-runs the
identical battery through the UNCHANGED R2-4 gate. When a trap signature fires,
the front end caps its confidence below the install threshold (it knows it is
in a trap, so it does not claim high confidence). *What it tests:* whether the
safety failure is a knowledge gap in the front end rather than a gate gap.

**Predicted outcome (pre-registered):** the fork is EXPECTED to DIE on RK-3
(~9.4%, gate unchanged — the gate, not the front end, blocks correct installs).
The knowledge hypothesis itself is decided by the preregistered diagnostic
KD-1: if teaching does not cut adversarial wrong-high-conf by ≥50%, the
"knowledge gap" hypothesis DIES by measurement. A KD-1 pass with an RK-3 death
would show knowledge fixes safety but not liveness — the two gaps are separate.

## 2. What is built (pure Zag; Python only for glue/analysis)

- `src/vsense_c.zag` — R2-4's `sense_r24.zag` front-end PLUS `vknow.zag`
  (family-knowledge detectors). Everything else byte-identical (judges,
  confidence formula, G self-checks). When a knowledge detector fires on the F
  span, confidence is capped at 650 (below the 700 install threshold) and the
  `program` text records `K=<family>` (ledger-audited). No other change.
- `src/vknow.zag` — trap signatures, each derived from the family method:
  - K-COL-2 (illuminant-drift): top-half vs bottom-half mean-RGB illuminant
    estimates; drift = L1(est_top, est_bot)/brightness; fire if > frozen thr.
  - K-CCN-1 (extreme illuminant): max channel mean / min channel mean > 3.0.
  - K-CCN-2 (mixed illuminant): left-half vs right-half illuminant estimates
    differ > frozen thr.
  - K-PTC-2 (glide-through-threshold): f0 estimated on early vs late window of
    each tone; fire if relative change > 5%.
  - K-PTC-1 (near-threshold): |Δf|/f inside the trap band around the
    discrimination threshold → abstain (cap).
  - K-SHP-1 (occlusion-bar): dark run spanning >80% of frame width → cap.
  - K-TMB-1 (boundary-straddling): centroid within ±12% of a class boundary
    → abstain (cap).
  - K-SHP-3 / K-MOT-3 (low-contrast): contrast below frozen floor → cap.
  - K-PTC-3 / K-TMB-2 (harmonic-distractor/boost): harmonic-energy
    inconsistency vs f0 → cap.
  - Documented UNTEACHABLE from the available bytes (knowledge-limit cases,
    expected ~0 reduction): K-COL-1 (metamer — RGB-identical by construction),
    K-MOT-1 (reversed video — the clip genuinely shows the motion).
  Detector thresholds are calibrated on the harness NOISE split (370 fixtures;
  in no kill bar) and FROZEN before R2A evaluation — never fitted to R2A.
- `src/memgate.zag` — R2-4's gate COPIED BYTE-IDENTICAL (SHA256 verified in
  evidence; `cmp` against `round2/forks/R2-4/src/memgate.zag` clean). The gate
  is the control variable: UNCHANGED.
- `src/deliberate.zag`, `src/R33_NATIVE_*` — copied byte-identical.
- Glue (Python): run vsense_c on 11,840 trials, build records, run memgate,
  score bars. No decisions in Python.

## 3. Fixtures and trial plan (frozen, shared)

Same 11,840-trial battery and order as V2-A §3. No new fixtures. No R2H.

## 4. Bars (frozen; applied mechanically)

- **RK-1**: false permanent installs / 11,840 ≤3%.
- **RK-2**: wrong high-confidence percepts reaching permanent installation ≤1%.
- **RK-3**: correct high-confidence percepts reaching PASS-and-install ≥85%.
  (Expected ~9.4% — the pre-registered death.)
- **RK-5**: ≥90% of wrong high-conf percepts reach FAIL/UNRESOLVED over
  independent evidence.
- **B5**: false permanent installs on the adversarial battery ≤3%.
- **B6** (HARD KILL): 3 full runs byte-identical, ledger verified.
- **B1**: frozen-370 primary judgment accuracy ≥60%. (Knowledge caps must not
  degrade clean judgments: B1 is the guardrail.)
- **KD-1 (knowledge diagnostic, deciding for the hypothesis)**: adversarial
  wrong-high-conf count ≤537 (50% of R2-4's frozen baseline 1,075, measured on
  `round2/forks/R2-4/evidence/clean`). Pass → the knowledge gap is real and
  teachable. Fail → the "knowledge gap" hypothesis DIES by measurement.
- **KD-2 (reported)**: per-family wrong-high-conf reduction; the documented
  unteachable families (COL-1, MOT-1) are expected to show ~0 reduction.

## 5. Kill criteria

- Fail any of RK-1, RK-2, RK-3, RK-5, B5 → DEAD (deciding bar named;
  RK-3 is the expected decider).
- Fail B6 or B1 → DEAD (hard kills).
- KD-1 fail → the knowledge hypothesis DIES by measurement (reported as the
  deciding finding for Micah's hypothesis even though RK-3 is the fork killer).
- No retroactive bar changes. Amendments go to Micah.

## 6. Commit map

- This prereg: `senses/pam-rebuild/v2/preregs/PREREG_V2-C.md` (committed ALONE).
- Build: `senses/pam-rebuild/v2/forks/V2-C/`: PREREG copy, src/ (incl.
  vknow.zag + threshold calibration), evidence/, RUNLOG.md, VERDICT_V2-C.md.
- Branch `tnn-native-lab`, repo `sylorlabs/TNN`. Via
  `~/workspace/commit_racefree.py`, TMPDIR=`~/workspace/tmp_commit`,
  lab-relative paths. No binaries, no `.zagd`.

**Laws:** pure Zag for mechanisms/learners/verification; Python only for
glue/analysis. Zero RNG in any decision path. Byte-identical reruns required.
