# PREREG R2-13 — FS-F "Signature-Ceiling Falsifier"

**Status: FROZEN 2026-09-23. Committed alone — before any build output exists.**
**Source debate:** `../debates/DEBATE_D_new_fronts.md` §7 (front f), committed.
Hypothesis and KILL BARS below are copied from the debate's FS-F spec; adaptations
to the frozen fixture pool are documented in §6 and are NOT post-hoc (no results exist).

## 1. Hypothesis under test (verbatim from DEBATE_D §7 FS-F)

> *Hypothesis:* the relational-signature property's ceiling is above the 1% bar once
> features are attack-aware — i.e., the ceiling claim is false.

The debate's RULING on front (f) was AGAINST ("the property is the ceiling") with the
preregistered falsifier: if novelty still kills at >2%/family after genuine feature
work, the property is the ceiling and signature contracts are retired. This fork IS
that falsifier. Either outcome is a program-level result:
- **Bars pass** → the ceiling claim DIES; signature contracts are revived with
  attack-aware features as the closing argument.
- **Bars fail** → the ceiling claim STANDS; the program stops spending on signature
  contracts (debate D §10 rank-3 consequence).

## 2. What is built

Pure-Zag binary `fsf` (zero RNG in any decision path, integer math only,
deterministic), reading the frozen R2FX fixture containers (`round2/forks/R2-7/fixtures_R2A`).
Per trial it reads ONLY the F (formation) span — never the G (challenge) span.

**Mechanism (FULL variant):** G3/R2-2-style two-sided relational-signature contract —
INSTALL iff `dist(percept, nearest true exemplar) + 150 < dist(percept, nearest false-bank
entry)` (milli-units, margin 150, same as R2-2) — computed on REBUILT attack-aware
features (§4), PLUS explicit attack-feature clauses (§5) that WITHHOLD when a
design-family attack signature fires unless a preregistered tight-match escape holds.

**Ablation (COARSE variant):** G3's original contract form — ONE-SIDED,
INSTALL iff `dt_coarse < 300` — on coarse features (§4). This is the honest historical
baseline (G3 died at 4.36% in exactly this form). The two-sided form is NOT used for
the coarse variant: on coarse features the bank's attack entries read identically to
the percept (e.g. TMB-2 reads DARK on coarse bins for both), so `dt+150<df` degenerates
into withhold-everything and the ablation would be vacuous. The comparison therefore
tests refined-features+tow-sided-clauses vs the G3 baseline as a whole; the
preregistered ≥50% bar (§7.3) is on design-family false installs.

**Diagnostic (NOCLAUSE variant):** FULL minus the attack clauses (two-sided on refined
features). Reported only; isolates the clauses' contribution.

Mode selected by argv[5]: `full` | `coarse` | `noclause` | `stage1` (stage-1 emits the
feature vector for enrollment; same code path as evaluation).

## 3. Fixtures (all frozen before this prereg)

- Battery: `round2/forks/R2-7/fixtures_R2A/` (R2A frozen suite, MANIFEST.sha256 committed
  by the R2-7 crew; family taxonomy in `R2_FIXTURE_SET.md`).
  - Enrollment + recall: `r2n/` — 5,100 normal fixtures (family 0).
  - Adversarial eval pool: `r2a/` (4,776) + `r2a2/` (5,149) = **9,925 fixtures** (see §6).
- Enrollment: ~60 exemplars per (task, class) from `r2n/` in ledger order
  (≈1,380 total; exact counts committed with the enrollment ledger). Noise-free
  build step: stage-1 binary emits features; Python only assembles the committed
  `.zag` tables (same pattern as R2-2's enroll2.py — Python never touches a decision).
- False bank (FULL/NOCLAUSE): 12 frozen entries — 4 per design family, lowest `r2a/`
  indices: TMB-2 (timbredisc family 2), SHP-1 (shapetrans family 1), MOT-1 (motiondir
  family 1). These fixtures are inside the eval pool; they must self-withhold.

## 4. Features (frozen here; thresholds calibrated per §5 procedure)

Feature vector: 8×i32 per task. REFINED (FULL/NOCLAUSE):

- **t0 colordisc** (F = 2× 32×32 RGB patches): f0 chromaticity distance A-vs-B (milli),
  f1 luminance distance, f2 min strip-vs-B chromaticity (ramp robustness), f3 strip
  spread, f4–f7 = 0.
- **t1 colorconst** (F = 2× 48×48 RGB views): f0–f2 white-patch-normalized A appearance
  (r,g,b), f3–f5 |A−B|, f6 illuminant asymmetry, f7 = 0.
- **t2 shapetrans** (F = 96×96 u8): bright = v>160; bar detection = contiguous ≥8-row
  dark band splitting bright rows (R2-2's algorithm); visible set = bar-excluded bright
  pixels. f0 bar flag (0/1000), f1 circularity 1000·A/(π·rmax²), f2 radial variance
  (milli), f3 corners·250, f4 area fraction, f5 components·100, f6 bar-row position
  (milli), f7 hidden fraction 1000·(1 − nv_visible/nv_total).
- **t3 pitchdisc** (F = 32000 int16; toneA [0,14400), toneB [16000,30400)): f0 endpoint
  ratio 1000·fB_end/fA_end/2 (truth is the endpoint ratio), f1 start ratio, f2/f3 glide
  amounts, f4–f7 = 0.
- **t4 timbredisc** (F = 32000 int16, 2 s tone @440 Hz): harmonic sieve on samples
  [800,12800) (R2-2's algorithm). f0–f2 power ratios p2,p3,p4 = 1000·e_h/e_1, f3
  |centroid − nearest TMB bin boundary| (milli), f4 template-class id of (p2,p3) in the
  generator's TMB_TMPL space (0..3 — the space the truth labels are defined in), f5
  boost-band flag (1000 iff p2∈[300,470] and p3∈[90,160] — the TMB-2 collision region),
  f6 octave-correction flag, f7 = 0.
- **t5 motiondir** (F = 50 frames 32×32 u8): 8 sampled frames (0,7,…,49), 16×16
  downsample, pairwise block-match votes + global frame0→frame49 displacement. f0 dx,
  f1 dy (milli), f2 reversal-seam marker, f3 minority, f4 magnitude, f5 still flag,
  f6 frame0-vs-frame49 mean-brightness delta, f7 = 0.

COARSE (ablation; G3-flavored):
- t0: 4-bit/channel bin SAME/DIFF flag; t1: normalized-bin SAME/DIFF flag;
- t2: classbin (TRI/SQU/CIR from 1000·area/(π·Rmax²) @526/819), area_bin, rmax_bin,
  cx_bin, cy_bin;
- t3: f0-ratio 10-cent-bin label; t4: centroid bin class via TMB_BINS (the bins TMB-2 defeats);
- t5: 8-way octant of global displacement.

## 5. Attack-feature clauses (FULL only; frozen predicates, calibrated thresholds)

Calibration procedure (frozen): thresholds are set from (a) the enrolled `r2n/`
distribution and (b) DESIGN-family fixtures only (§8). Holdout families (§8) are
never inspected during design or calibration — only scored at final evaluation.

- **TMB-2 clause:** if f5 (boost-band) fires → INSTALL only if template-class f4 ==
  nearest-exemplar class AND dt < 400 (tight escape). Otherwise the two-sided rule.
- **SHP-1 clause:** if f0 (bar) fires → INSTALL only if dt < 250 on the bar-excluded
  features (tight escape). Otherwise the two-sided rule.
- **MOT-1 clause:** NONE — documented null probe. The reversed-video attack is
  information-theoretically invisible in F: F = fwd[49::-1] has window offsets
  (sx+dx·49)%16, (sx+dx·48)%16, … — statistically identical to a genuine
  reverse-direction fixture (random start phase, ±3 integer per-frame noise in both).
  No feature of F can distinguish them. The prereg PREDICTS the two-sided margin +
  bank cannot beat this family; its measured rate is the ceiling measurement itself.

## 6. Evaluated pool and the debate's "10,000" (documented, pre-results)

The debate's bar (1) says "10,000 adversarial trials". The frozen R2A battery's full
adversarial complement is **9,925 fixtures** (r2a 4,776 + r2a2 5,149 — counted from the
committed gen_ledger.jsonl); no fixtures may be generated post-freeze. Bar (1) is
therefore evaluated on 9,925 trials, threshold ≤1% (≤99 false installs). The 75-trial
shortfall vs the debate text is recorded here, not adjusted after results.

False install := `install==1 AND class != truth` (R2-2's definition). Judgment classes
are the harness vocabularies (SAME/DIFFERENT, SAME_SURFACE/DIFFERENT,
CIRCLE/SQUARE/TRIANGLE, SAME/HIGHER/LOWER, PURE/DARK/RICH/BRIGHT, N/NE/E/SE/S/SW/W/NW/STILL).

## 7. KILL BARS (copied from DEBATE_D §7 FS-F; §6 adaptation applies to bar 1)

1. **Overall:** false installs ≤1% on the 9,925-fixture adversarial pool (r2a + r2a2).
2. **NOVEL-FAMILY HOLDOUT:** 6 families frozen out of feature design — COL-1, COL-2,
   CCN-1, PTC-1, TMB-1, SHP-3 — ≤2% false installs per family AND pooled ≤1%.
   Any exceedance kills.
3. **Feature ablation:** on the 3 design families (TMB-2, SHP-1, MOT-1), FULL must cut
   false installs ≥50% vs COARSE (pooled over the 3 families). Below → the features
   are decorative → dies.

**Validity gate (hard):** the full battery runs TWICE; the two runs' ledgers must be
byte-identical (`cmp`), and every hash chain must verify. A non-deterministic or
unverifiable run invalidates the verdict.

Reported (not kill bars): recall on r2n/ (install rate, judgment accuracy, retrieval
accuracy installed-correct/installed); per-family false-install table for all 17
families; NOCLAUSE diagnostic; ops/bytes vs Approach A (B3-style); B1-style primary
judgment accuracy on r2n/.

## 8. Design-visibility declaration (frozen)

- **DESIGN families** (feature design + threshold calibration may inspect):
  TMB-2, SHP-1, MOT-1 — the collision families named in DEBATE_D §7.
- **HOLDOUT families** (never inspected until final scoring; bar 2):
  COL-1, COL-2, CCN-1, PTC-1, TMB-1, SHP-3.
- **POOL-ONLY families** (in bar 1's denominator; per-family numbers reported, no
  per-family bar; not inspected during design): COL-3, CCN-2, SHP-2,
  PTC-2, PTC-3, TMB-3, MOT-2, MOT-3.
- Normals (r2n/) are visible for enrollment and recall throughout.

## 9. Verdict interpretation (frozen)

- All 3 bars pass → ceiling claim FALSIFIED; signature contracts revived (ALIVE).
- Bar 3 passes but bar 1 and/or 2 fails → "the property is the ceiling": attack
  features did genuine work on design families, but novelty still installs → DEAD,
  signature contracts retired per DEBATE_D §10.
- Bar 3 fails → the features were decorative; the falsifier is inconclusive about the
  property (the engineering, not the property, failed) → DEAD with that distinction
  stated plainly.
- Any single bar fails → DEAD (bars are conjunctive).

## 10. Commit map

- This prereg: `senses/pam-rebuild/round2/preregs/PREREG_R2-13.md` (committed ALONE —
  no src, no evidence, no binaries).
- Then: `senses/pam-rebuild/round2/forks/R2-13/` = src/ (fsf.zag, R33 natives,
  enroll.py, run.py, score.py, verify_chain.py), evidence/ (enrollment ledger,
  bank manifest, 2 run ledgers, score tables), VERDICT_R2-13.md. No binaries, no
  .zagd caches committed.
