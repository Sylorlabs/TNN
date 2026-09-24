# PREREG_FS-F2T.md — frozen preregistration, crew FS-F2T

Status: FROZEN. Committed alone before any fresh evaluation result was generated.
Any change to mechanism, fixtures, bars, or protocol below requires a new
prereg commit; post-freeze edits are not permitted.

## 1. Identity and lineage

- Crew: FS-F2T (PAM rebuild round 2), depth 2/2. Goal: improve timbredisc
  formation accuracy from FS-E2 Phase-0 (38.89%) so it can earn FS-E2 install
  scope. Timbredisc is the only task whose formation function changes.
- Lineage: `f2t_form.zag` is a byte-faithful copy of
  `round2/forks/FS-E2/src/fs2_form.zag` (FS-E2 independent formation layer)
  EXCEPT the timbredisc path (`f_timbredisc`, `f_tbpower`, `f_tbcoeff`),
  which is replaced by the mechanism in §3. All five other formation
  functions (colordisc, colorconst, shapetrans, pitchdisc, motiondir), the
  batch driver, the header parsing, and the judgment vocabulary are
  unchanged, byte-for-byte semantically.
- Build: pure Zag, compiled with the pinned toolchain
  `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
  Python is glue/analysis only (fixture generation driver, scoring,
  hashing). Zero RNG in any AI decision path.

## 2. Frozen Phase-0 findings (FS-E2, unchanged by this prereg)

- Independent formation accuracy on the frozen 720 R2A timbredisc controls:
  280/720 = 38.89%.
- White-box defects diagnosed (reproduced 720/720 by an independent C replica):
  (i) 2x sample-rate/bin error: coefficients target ~220·m Hz, not 440·m Hz
  (fixtures are 16 kHz, N=32000); (ii) ÷1024 coefficient quantization;
  (iii) i64 overflow in the power expression and in `ps = raw*1048576/pmax`;
  (iv) wrong representation for the frozen truth: spectral-centroid
  classifier vs the R2A nearest-(p2/p1, p3/p1) harmonic-template truth.

## 3. Mechanism specification (frozen; the only permitted change)

The new `f_timbredisc` measures harmonic powers at the exact DFT bins for
440·h Hz (h=1,2,3) and classifies by nearest frozen theory template.

Constants (frozen):
- SR = 16000, N = 32000, bins k_h = 880·h for h = 1,2,3.
- S = 2^20 = 1048576.
- Q20 Goertzel coefficients c_h = round(2·cos(2π·880·h/32000)·2^20):
  c_1 = 2065924, c_2 = 1973170, c_3 = 1821652.
- Frozen theory templates (verbatim from `gen_r2a.py` TMB_TMPL):
  PURE (0,0), BRIGHT (1960,2560), DARK (78,6), RICH (640,384).

Algorithm (all i64; Zag `/` truncates toward zero):
1. For each h in {1,2,3}: read the 32000 signed 16-bit samples; run the
   Goertzel recurrence with input x = sample/32 (trunc division), state
   s1,s2 = 0:
     s0 = x + (c_h·s1)/S − s2; s2 = s1; s1 = s0.
2. Harmonic power: p_h = s1² + s2² − ((s1·s2)/S)·c_h; if p_h < 0, p_h = 0.
   (Division-before-multiply; the old overflow-prone order is gone.)
3. Ratios (per-mille): r2 = (p2·1000)/p1, r3 = (p3·1000)/p1, where
   p1 = max(p1, 1). Clamp r2, r3 to ≤ 1,000,000 (totality guard for the
   squared distances; unreachable — see §4).
4. Judgment: class minimizing (r2−T2)² + (r3−T3)² over the four templates.
   Ties: first minimum wins in the fixed order PURE, BRIGHT, DARK, RICH.
   Judgment vocabulary unchanged (PURE/BRIGHT/DARK/RICH).

Design-validation only (pre-prereg, on frozen 720 normals + 985 adversarial
fixtures; NOT the gating draw): an exact-integer prototype of §3 scores
720/720 = 100.00% on r2n and 980/985 = 99.49% on the adversarial battery
(5 misses: knife-edge TMB-3 sub-3 near-PURE distractors, integer r2=39 vs
PURE/DARK boundary 39.23 — within 1 template unit of the boundary).
These numbers are expectations, not bars; the gating draw is §5.

## 4. Overflow-freeness argument (frozen)

Analytic bound: |x| ≤ 32768/32 = 1024 (i16 range, worst case), DFT power
p_h ≤ (N·1024)² = (32000·1024)² = 1.074e15, so p·1000 ≤ 1.074e18 < 9.2e18
(i64 max). |c·s1| ≤ 2.07e6 · (N·1024) = 6.8e13. All other intermediates are
smaller products. Clamped r ≤ 1e6 gives (r−T)² ≤ 1e12.

Empirical maxima of |intermediate| over 720 r2n + 985 adv fixtures
(exact-integer prototype): |c·s1| = 7.2e13, |s| = 3.5e7, |s²| = 1.2e15,
|(s1·s2/S)·c| = 2.4e15, |p| = 3.6e13, |p·1000| = 1.11e16, max r = 16099.
Largest is |p·1000| = 1.11e16 = 0.12% of i64 range. No intermediate can
overflow on the frozen battery; the analytic bound covers all inputs.

## 5. Fresh gating draw (frozen; generated AFTER this prereg commits)

- Generator: frozen `round2/forks/R2-7/src/gen_r2a.py`, function
  `gen_timbredisc(rng)`; frozen truth = `_tmb_template_class(profile)`.
- Stream: `stream_seed(MASTER=20260923, STREAM_NORMAL+TIDX=404, i)`
  for i in 720..1719 (1000 fixtures), family=0 — the same deterministic
  stream as the frozen normals, at indices never used in any exploratory
  work. Rendering (profiles, ramps, SplitMix phases) is the frozen pipeline.
- Output: `forks/FS-F2T/fixtures_fresh/f2t_timbredisc_<i>.r2fx` + `.truth`
  sidecars. A manifest (path, sha256 of each .r2fx, truth) is written and
  its hash recorded in the evidence. The draw is generated ONCE;
  re-drawing or seed-shopping is prohibited.
- Class balance: i%4 cycles PURE/BRIGHT/DARK/RICH → 250 per class.
- n = 1000 ≥ 1000 as required.

## 6. Gating bars (all must pass; mechanical ALIVE/DEAD)

(a) Timbredisc formation accuracy on the fresh draw (§5): ≥ 85.00%
    (≥ 850/1000).
(b) No regression on the three unchanged tasks, full frozen R2A normal sets
    (same lists FS-E2 used: `r2n_colordisc.list` 1080, `r2n_pitchdisc.list`
    720, `r2n_motiondir.list` 564), floors = FS-E2 Phase-0 minus 1pp:
    colordisc ≥ 91.96% (baseline 92.96%), pitchdisc ≥ 96.92% (baseline
    97.92%), motiondir ≥ 95.63% (baseline 96.63%).
(c) Byte-identical determinism: the full evaluation (fresh timbredisc +
    all three regression batteries) is run TWICE; the concatenated stdout
    and the scored TSVs are byte-identical between runs (sha256 recorded).

Verdict: ALIVE iff (a) and (b) and (c) all pass. Otherwise DEAD.
No post-hoc tuning on the fresh draw for any reason.

## 7. Non-gating diagnostics (report only, cannot change the verdict)

- Per-class accuracy and confusion on the fresh draw; min margin (template
  units) to the nearest wrong template per class.
- Adversarial diagnostic: the frozen 985-fixture b_adv timbredisc battery
  scored with the same binary (expectation from prototype: ~99.5%; the 5
  known knife-edge misses are TMB-3 sub-3 distractors at the PURE/DARK
  boundary).
- High-harmonic diagnostic: breakdown of the fresh draw by harmonic family
  (R2A truth labels carry the family structure implicitly via templates).

## 8. RNG statement

Zero RNG in any AI decision path: formation is pure deterministic integer
arithmetic of the fixture bytes; the binary is run twice and compared
byte-for-byte. Fixture generation uses the frozen generator's deterministic
SplitMix streams (fixture-side determinism, not a decision path). Python
is used only for glue (batch driver, scoring, hashing, manifest).

## 9. Prohibited after freeze

No changes to coefficients, scaling, arithmetic order, guards, templates,
thresholds, or tie-break; no re-running the fresh draw with different
seeds/indices; no selecting fixtures by outcome. The fresh fixtures are
generated after this prereg commits, scored once, and reported as-is.

## 10. Evidence to be committed after evaluation

- This prereg (committed alone, before any fresh result).
- `src/f2t_form.zag` (+ native IO import), build log.
- `fixtures_fresh/` (1000 .r2fx + .truth), manifest + hash.
- `evidence/eval/` — both runs' stdout logs, scored TSVs, sha256s,
  margin/family diagnostics.
- `VERDICT_FS-F2T.md` with the mechanical ALIVE/DEAD verdict.
