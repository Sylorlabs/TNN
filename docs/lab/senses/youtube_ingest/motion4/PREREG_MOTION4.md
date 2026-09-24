# PREREG — MOTION4: multi-scale coherence-field motion (fast/complex real-motion coverage)

Frozen 2026-09-24. This prereg is frozen at commit time; any change to the
design, constants, batteries, or bars below requires a new prereg version,
never a silent edit.

## 1. Problem

M3 (VERDICT_MOTION3.md, 2026-09-23) is READY as a no-false-memory motion
sensor: 60/60 synthetic primary, 30/30 adversarial no-error (zero
false-STILL), zero errors on real footage, 13/13 held-out, byte-identical
reruns, 749,568 ops/clip (under the 1.5M ceiling; block-match method2 was
~2.8M). Its recorded limitations are this experiment's scope:

- **L5: ±2px search cannot track fast motion.** Any true displacement
  >2px per frame-pair is outside M3's SAD grid. Fine-scale evidence stays
  near the quantization floor, so M3 honestly WITHHOLDs — zero coverage
  of fast uniform translation (timelapse, sports, vehicle/drone footage).
- **L1: real-motion DIRECTION tested at n=1.** The only genuine
  real-motion direction test in the program is B3a's OQSNhk5ICTI_w065
  (sub-perceptual E drift). The B3b long-baseline attempt (timelapse
  clouds) was relabeled all-AMBIG: conflicting cloud layers, no uniform
  translation (B3_LABELS.md REVISION).
- **L4: high withhold on real footage** (28/44 AMBIG by design) — honest,
  but coverage is thin.

M3 verdict conclusion: "coverage of fast/complex real motion remains
future work." The rematch verdict adds the mechanism reason: motiondir was
catastrophic for both fitted families (A 33.3%, B 16.7→18.3%) — "the
fitted families cannot express the task." More fitting is exhausted (both
approaches plateaued at T1; 100× training changed nothing). The next step
is architectural, not more data.

## 2. Hypothesis

**H:** A coarse-to-fine coherence-field extension of the frozen M3
primitive — identical per-scale pipeline at three scales (S0 full-res,
S1 2×2-averaged, S2 4×4-averaged) with cross-scale direction agreement
(P5) — detects uniform translation up to 8px/frame-pair on real video
textures with **zero false judgments**, covering the fast-motion range
where M3 is blind, while preserving M3's never-false record on every
existing battery and staying within the 1.5M ops ceiling.

**Falsification:** any false CANDIDATE judgment on any battery (K1/K2/K4/
K5), or <40% correct-direction on the RM1 6px subset (K3), or any
determinism failure (K6), or ops > 1.5M/window (K7).

## 3. Physics basis (frozen principles)

P1–P4 inherited unchanged from PREREG_MOTION3.md §2:

- **P1 — motion is coherent displacement of texture.** Evidence per
  patch = SAD(0,0) − SAD(best) ≥ 0. No per-pixel difference gates.
- **P2 — stillness is a positive claim.** STILL requires exact digital
  stillness or sub-floor evidence with no directional consensus. Absence
  of detection is WITHHOLD, never STILL.
- **P3 — sub-pixel honesty.** No direction claim below 0.5px mean
  displacement per voting block, measured in the claiming scale's own
  pixels.
- **P4 — incoherence is withhold, not guess.** Cuts, expansion flow,
  shake, multi-motion → WITHHOLD.
- **P5 — scale coherence (new).** A direction claim at displacement d
  must be confirmed by coherent evidence at a scale that resolves d. A
  scale whose search range cannot see d may WITHHOLD but never vetoes a
  scale that can. Two scales that both resolve d and disagree on
  direction → WITHHOLD (incoherent). Stillness claimed by one scale while
  another claims coherent direction → WITHHOLD (contradiction).

## 4. Design — method4 (frozen)

Pure Zag, integer arithmetic only, zero RNG. One binary:
`motion4 <fixture.vid>`; stdout key=value lines in the motion3 form:
`approach=M4, task=motiondir, judgment=<STILL|N|NE|E|SE|S|SW|W|NW|WITHHOLD>,
confidence=0..1000, decision=<CANDIDATE|WITHHOLD>, reason=<code>,
debug_vec=<per-scale win/coh_pm/G_pm/Ebar>, ops=<n>`.

Fixture: `.vid`, header = nf,w,h (i32 LE), then nf frames of w×h RGB
(identical to M3).

Algorithm (all integer, i64):

1. Luminance planes L = r+g+b per pixel, all frames (as M3).
2. Deterministic pyramid: S0 = full plane; S1 = 2×2 block average
   (floor division); S2 = 4×4 block average (floor division). No
   rounding modes, no interpolation — exact integer means.
3. At each scale, the M3 pipeline runs VERBATIM (8×8 blocks, stride 8,
   pairs (0,1)..(nf−2,nf−1), SAD over 25 offsets ox,oy ∈ {−2,…,2}
   edge-clamped, e_b = SAD(0,0) − SAD(best) ≥ 0, voting iff e_b > 0,
   octant binning, aggregates E_total/E_bin[9]/N_vote/G_num/N_tot,
   coh_pm/G_pm/Ebar, M3 §3.6 decision rules) with scale-local constants:
   - BLOCK 8, STRIDE 8, R 2, COH_DIR 667, COH_STILL_MAX 667,
     G_MIN_PM 500, VOTE_FRAC 1/4, E_FLOOR 64 — the same numbers at every
     scale, interpreted in that scale's own pixel units. (E_FLOOR = 1
     luminance quantum per pixel of an 8×8 block in the scale's plane;
     G_MIN_PM = 0.5 scale-px honesty per P3, so the effective full-res
     honesty threshold grows with coarseness, as it must.)
   - Effective full-res search range: S0 ±2px, S1 ±4px, S2 ±8px.
4. Cross-scale resolution (frozen):
   - DirCands = scales with decision=CANDIDATE and an 8-way judgment;
     StillCands = scales with decision=CANDIDATE and judgment=STILL.
   - DirCands ≠ ∅ AND StillCands ≠ ∅ → WITHHOLD, reason=
     `still_dir_conflict`, confidence=0.
   - DirCands with ≥2 distinct direction bins → WITHHOLD, reason=
     `scale_disagree`, confidence=0.
   - DirCands with exactly one bin B → judgment=B, decision=CANDIDATE,
     confidence = min over DirCands of scale confidences (weakest
     confirming scale bounds the claim), reason=`coherent_multiscale`.
   - Elif StillCands ≠ ∅ → judgment=STILL, decision=CANDIDATE,
     confidence = min over StillCands, reason = finest still reason.
   - Else → WITHHOLD, reason = S0's reason code, confidence=0.
   - Rationale (P5): a blind scale's WITHHOLD never vetoes; any
     scale's positive claim must survive every other scale's positive
     claims.
5. ops = Σ over scales of SAD inner-loop pixel comparisons
   (px-visits), reported as ops=<n>. Estimated ≈ 749,568 (S0) +
   179,200 (S1) + 44,800 (S2) ≈ 973k < 1.5M ceiling.

## 5. Frozen constants

| name | value | meaning |
|---|---|---|
| SCALES | S0, S1, S2 | full, 2×2 avg, 4×4 avg (floor) |
| BLOCK / STRIDE / R | 8 / 8 / 2 | per scale, scale-local px |
| COH_DIR | 667 | per-mille supermajority for DIRECTION (per scale) |
| COH_STILL_MAX | 667 | coh below this + sub-floor evidence → STILL (per scale) |
| G_MIN_PM | 500 | 0.5 scale-px mean displacement for DIRECTION (per scale) |
| VOTE_FRAC | 1/4 | min fraction of block-pairs voting (per scale) |
| E_FLOOR | 64 | mean SAD improvement per voting block, scale-local units |
| CONF_AGG | min | confidence = weakest confirming scale |
| TIE_BIN_ORDER | STILL,N,NE,E,SE,S,SW,W,NW | deterministic argmax ties (as M3) |

## 6. Batteries (frozen)

- **B1 — M3 synthetic primary (regression).** The 60 clips
  `fixtures_testfresh/t6_motiondir/primary/p000..p059.vid`. M4 must not
  regress M3's record.
- **B2 — M3 synthetic adversarial (regression).** The 30 clips
  (1px/frame, 0.25 contrast). M3: 30/30 no-error, 25/26 moving caught.
- **B3a — M3 real-footage labeled windows (regression).** The 12 STILL +
  1 MOTION-E labeled windows from B3_LABELS.md. (B3b is all-AMBIG;
  excluded from scoring by the rubric, distribution reported.)
- **RM1 — fast translated real textures (new, exact truth).**
  Construction (frozen, deterministic, zero RNG): 12 texture sources =
  the 12 verified pixel-STILL B3a windows (B3_LABELS.md):
  0_jNjpVxUt0_w000; Eoo4HzILB-M_w000, _w002, _w004, _w006, _w008,
  _w010, _w012, _w014; uKNQCPXDNdc_w015, _w077, _w093 (frame0, 64×64
  real RGB). Motions: 8 directions × {3px/frame, 6px/frame} + STILL =
  17 variants × 12 textures = **204 clips**, 8 frames, integer shifts,
  edge-clamp (documented). Truth exact by construction (shift vector).
  Generator script committed with the fixtures; per-clip sha256
  manifest. Exploratory (reported, not kill): 48 clips at 8px/frame
  (12 textures × 4 cardinal directions) — stress probe, strip-survival
  noted.
- **RM2 — genuine real motion (new).** The crew mines the 7-video corpus
  for uniform-translation windows at 16/24/32-frame baselines (every
  2nd/3rd/4th source frame → 8-frame .vid), labeled under the frozen
  B3_LABELS.md rubric + the REVISION pair-level vote-analysis
  procedure. Labels are fixed by viewing BEFORE motion4 is run on RM2
  and committed with the fixtures (commit-order enforced in §8); the
  method never sees them during development. AMBIG excluded from
  scoring, distribution reported.
- **B4 — YT1 held-out (regression).** M3's 13-fixture probe
  (`probe_heldout/`). Run ONCE, after RM1/RM2, binary and source
  frozen. Never used in development.

## 7. Bars (frozen)

Kill bars (any one fails → FAIL, declared repair round, no silent
tuning):

- **K1 (B1):** correct ≥ 45/60 AND zero false CANDIDATE judgments.
  (M3: 60/60, 0 false.)
- **K2 (B2):** zero false CANDIDATE judgments; moving-catch
  (correct direction on the 26 moving clips) ≥ 25/26 — no regression
  vs M3's measured 25/26.
- **K3 (RM1 fast motion):** zero false CANDIDATE judgments on all 204
  clips AND correct-direction rate on the 96-clip 6px/frame subset
  ≥ 40%. (M3 baseline on this subset: measured once with the frozen
  motion3 binary, expected ≈0% — the bar requires the extension to
  actually see fast motion, not merely not-lie about it.)
- **K4 (genuine footage honesty):** zero false CANDIDATE judgments on
  all labeled windows of B3a + RM2. (WITHHOLD is never an error.)
- **K5 (B4 held-out):** zero false CANDIDATE judgments on the 13
  fixtures.
- **K6 (determinism):** 3 runs on one RM1 fixture → byte-identical
  stdout; full B1+B2+RM1 rerun from wiped caches → identical result
  digest. Zero RNG in the decision path (source grep for
  rand/random/time/clock/seed: zero matches; integer arithmetic only).
  Rebuild with the pinned toolchain → byte-identical binary.
- **K7 (cost):** ops ≤ 1,500,000 px-visits per 8-frame window
  (M3's frozen ceiling).

Targets (reported, not kill):

- T1: RM1 6px correct-direction ≥ 60%.
- T2: RM2 MOTION-D catch rate ≥ 50% (thin denominators expected).
- T3: RM1 withhold rate ≤ 30%; B1 withhold ≤ 10% (as M3).

Withhold honesty: every WITHHOLD carries a reason code (§4: finest-scale
code, `scale_disagree`, or `still_dir_conflict`) and installs nothing.

## 8. Commit plan

1. This prereg (frozen, alone).
2. Frozen M3 source commit: `motion3.zag` (385 lines, the exact source
   behind VERDICT_MOTION3.md — currently local-only, never committed;
   loose end closed here) + RM1 generator + RM1 fixtures/manifests +
   RM2 labels. RM2 labels committed BEFORE any motion4 run on RM2.
3. `motion4.zag` source + BUILD_NOTES.md + determinism evidence
   (K6 artifacts).
4. Results: per-battery tables, digests, VERDICT_MOTION4.md.
No binaries, no `.zagd` caches in the repo (rebuild via the pinned
toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`;
build command and binary sha recorded, never the binary).

## 9. What this does NOT do

- Not a memory-integration trial: CANDIDATE judgments only, no installs;
  memory wiring is a separate prereg.
- Not the TNN-self-selected-corroboration trial (READINESS.md
  follow-up #1 stays open).
- Does not re-litigate B3b: timelapse clouds stay AMBIG
  (multi-directional by relabel).
- Does not change P1–P4 or any M3 constant at S0: the S0 pipeline is
  the frozen M3 algorithm verbatim; the only new mechanism is the
  pyramid + P5 resolution.

## Appendix A — RM1 texture list (frozen)

Frame0 of each (64×64 real RGB, verified pixel-STILL in B3_LABELS.md):

1. 0_jNjpVxUt0_w000
2. Eoo4HzILB-M_w000
3. Eoo4HzILB-M_w002
4. Eoo4HzILB-M_w004
5. Eoo4HzILB-M_w006
6. Eoo4HzILB-M_w008
7. Eoo4HzILB-M_w010
8. Eoo4HzILB-M_w012
9. Eoo4HzILB-M_w014
10. uKNQCPXDNdc_w015
11. uKNQCPXDNdc_w077
12. uKNQCPXDNdc_w093

Source windows: `docs/lab/senses/youtube_ingest/windows/<id>.vid`
(frame0 extracted; byte-exact slice, verified by sha against the
window file).

## Appendix B — RM1 motion set (frozen)

8 frames per clip. Integer shift per frame (dx,dy) px, edge-clamp,
applied cumulatively from frame0 (frame k shifted by k·(dx,dy)).

- 8 directions × 3px/frame: (3,0) E, (−3,0) W, (0,−3) N [y grows
  downward], (0,3) S, (3,−3) NE, (3,3) SE, (−3,3) SW, (−3,−3) NW.
- 8 directions × 6px/frame: same eight at 6px.
- STILL: (0,0).
- Exploratory 8px/frame (reported only): (8,0), (−8,0), (0,−8), (0,8).

Truth label = the shift vector (exact by construction). Filenames:
`rm1_t<NN>_<dir><px>.vid` + `.vid.truth`.
