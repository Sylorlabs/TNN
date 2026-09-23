# PREREG — MOTION3: coherence-field motion-direction primitive

Frozen 2026-09-23. This prereg is frozen at commit time; any change to the
design, constants, batteries, or bars below requires a new prereg version,
never a silent edit.

## 1. Problem

Vision ingestion is GATED. Mechanism of the failure (READINESS.md):

- Centroid-track (`sense motiondir`, fitted rule STILL iff mag<1) scores
  **33.3%** on the TEST-FRESH t6 primary battery (measured 2026-09-23:
  20/60; errors are wrong-direction, e.g. SE→S, E→W).
- On the 30-clip adversarial battery (1px/frame, 0.25 contrast) it scores
  9/30 = 30% with **7 false-STILL judgments** — motion judged STILL with
  confidence 428. Sub-threshold motion is invisible to per-pixel
  difference thresholding, and the method reports STILL (a positive claim)
  from zero information.
- Block-match (`method2`, ±3px SAD) scores 100% on both synthetic
  batteries, but on real YouTube footage it is a forced-choice
  confabulator: 0/175 STILL on the static talking-head video
  (OQSNhk5ICTI), scattered directions on FPV footage. Its fitted rule
  (STILL iff vote-mag < 1) turns any stray block vote into a direction
  judgment (observed: sx=0,sy=-1,mag=1 → "N", confidence 0).

What is missing is a primitive that (a) detects real motion on real
footage, (b) catches or honestly withholds on sub-threshold adversarial
motion, and (c) never installs a false STILL or false direction.

## 2. Physics basis (frozen principles)

- **P1 — motion is coherent displacement of texture.** Evidence for motion
  at a patch = how much better a displaced patch explains the next frame
  than the undisplaced patch: e = SAD(0,0) − SAD(best) ≥ 0. Per-pixel
  difference thresholds are abandoned: sub-threshold adversarial motion is
  *real motion* and must be decided by coherent evidence, not pixel gates.
- **P2 — stillness is a positive claim.** STILL requires evidence:
  (a) exact digital stillness (nothing anywhere beats zero displacement),
  or (b) all displacement evidence below the quantization floor with no
  directional consensus. Absence of detection is WITHHOLD, never STILL.
- **P3 — sub-pixel honesty.** No direction claim below 0.5 px mean
  displacement per voting block. Coherent but unresolvable signal is
  WITHHOLD (`weak`/`subpixel`), never a guessed direction.
- **P4 — incoherence is withhold, not guess.** Cuts, expansion flow,
  camera shake, multi-directional scenes (waves, crowds) produce
  incoherent displacement fields. The honest output is WITHHOLD, which
  installs nothing.

## 3. Design — method3 (frozen)

Pure Zag, integer arithmetic only, zero RNG. One binary:
`motion3 <fixture.vid>`; stdout key=value lines:
`approach=M3, task=motiondir, judgment=<STILL|N|NE|E|SE|S|SW|W|NW|WITHHOLD>,
confidence=0..1000, decision=<CANDIDATE|WITHHOLD>, reason=<code>,
debug_vec=..., ops=<n>`.

Fixture: `.vid`, header = nf,w,h (i32 LE), then nf frames of w×h RGB.

Algorithm (all integer, i64):

1. Luminance planes: L = r+g+b per pixel (u16 LE arena), all frames.
2. Blocks 8×8, stride 8 → nb = (w/8)×(h/8) per frame-pair; pairs =
   (0,1)..(nf−2,nf−1). Remainder pixels ignored (documented).
3. Per block-pair: SAD over 25 offsets ox,oy ∈ {−2,…,2} (edge-clamped).
   best = argmin SAD; ties broken deterministically toward stillness:
   smaller (|ox|+|oy|), then smaller ox, then smaller oy.
4. e_b = SAD(0,0) − SAD(best) ≥ 0. Voting block iff e_b > 0.
   Bin of (ox,oy) by the frozen sense.zag octant rule:
   |ox|≥2|oy| → E/W; |oy|≥2|ox| → S/N (N = up, y grows downward);
   else diagonal; (0,0) → STILL bin (note: the STILL bin always has
   E=0, since best=(0,0) implies e_b=0).
5. Aggregates over all pairs: E_total = Σe_b; E_bin[9] (evidence per
   bin); N_vote = #{e_b>0}; G_num = Σ_{voting} isqrt(ox²+oy²);
   N_tot = nb×(nf−1).
   coh_pm = 1000 × max(E_bin) / E_total (E_total > 0);
   G_pm = 1000 × G_num / max(N_vote,1) (milli-px mean displacement);
   Ebar = E_total / max(N_vote,1) (mean evidence per voting block).
6. Decision (frozen constants §4):
   - E_total == 0 → judgment=STILL, decision=CANDIDATE,
     confidence=1000, reason=`exact_still`.
   - Else let win = argmax E_bin (ties → fixed bin order
     STILL,N,NE,E,SE,S,SW,W,NW — deterministic):
     - DIRECTION iff win is a direction bin AND coh_pm ≥ 667 AND
       G_pm ≥ 500 AND N_vote ≥ N_tot/4 AND Ebar ≥ 64:
       judgment=win, decision=CANDIDATE,
       confidence = (coh_pm − 667) × 1000 / 333 clamped to [1,1000],
       reason=`coherent`.
     - STILL iff Ebar < 64 AND coh_pm < 667: judgment=STILL,
       decision=CANDIDATE,
       confidence = 1000 × (64 − Ebar)/64, halved (integer) if
       coh_pm ≥ 334, reason=`subnoise_still`.
     - Else WITHHOLD: judgment=WITHHOLD, decision=WITHHOLD,
       confidence=0, reason = first of:
       `sparse` (N_vote < N_tot/4), `subpixel` (G_pm < 500),
       `weak` (Ebar < 64), `incoherent` (otherwise).
       debug_vec still reports win/coh_pm/G_pm/Ebar for audit.

Rationale for constants (§4): supermajority 2/3 for a direction claim;
1/2 px sub-pixel honesty (P3); 1/4 of blocks must vote (non-triviality);
1 luminance quantum per pixel of an 8×8 block as the quantization-noise
floor (P2: below this, displacement "evidence" is not evidence).

## 4. Frozen constants

| name | value | meaning |
|---|---|---|
| BLOCK | 8 | block size px |
| STRIDE | 8 | block stride px |
| R | 2 | search radius px (±2) |
| COH_DIR | 667 | per-mille supermajority for DIRECTION |
| COH_STILL_MAX | 667 | coh below this + sub-floor evidence → STILL |
| G_MIN_PM | 500 | 0.5 px mean displacement for DIRECTION |
| VOTE_FRAC | 1/4 | min fraction of block-pairs voting |
| E_FLOOR | 64 | mean SAD improvement per voting block (1 quantum/px) |

## 5. Batteries (frozen)

- **B1 — synthetic primary.** 60 whole clips
  `fixtures_testfresh/t6_motiondir/primary/p000..p059.vid`, truth from
  `pNNN.vid.truth` (4 STILL, 7× each of 8 directions; 2px/frame,
  full contrast).
- **B2 — synthetic adversarial.** 30 whole clips reconstructed
  byte-exactly as header(8,64,64)+w1_pixels+w2_pixels from
  `subclips/adversarial/pNNN_{w1,w2}.vid` (verified layout (4,64,64));
  truth from `runs/adversarial_pNNN.json` → `truth` field
  (1px/frame, 0.25 contrast; 8 directions + STILL).
- **B3 — real footage.** 56 windows from `windows/`: per video, indices
  floor(i·W/8), i=0..7 (deterministic). Labels by viewing frame0 vs
  frame7 (2× upscale side-by-side, 4-up montages): STILL (no discernible
  change), MOTION-<D> (clear uniform translation, 8-way), AMBIG
  (zoom/expansion, rotation, cuts, multi-motion, complex deformation —
  excluded from scoring, distribution reported). Conservative labeling:
  unsure → AMBIG.
- **B4 — YT1 held-out.** `probe_heldout/adv_*.vid` (9) + `pri_*.vid`
  (4); truth from `probe_manifest.tsv`. Run ONCE, after B1–B3, binary
  and source frozen. Never used in development.

## 6. Bars (frozen)

Kill bars (any one fails → program FAIL, declared repair round, no
silent tuning):

- **K1 (B1):** correct ≥ 45/60 (75%). (Baseline: centroid 33.3%.)
- **K2 (B2):** zero false judgments: every CANDIDATE judgment must equal
  truth. In particular zero false-STILL. (Baseline: centroid 7
  false-STILL; block-match 0 false but forced-choice.)
- **K3 (B3):** zero errors on labeled windows: no STILL and no wrong
  direction on MOTION windows; no direction on STILL windows.
  (WITHHOLD is never an error.)
- **K4 (B4):** zero false CANDIDATE judgments on the held-out probe.
- **K5 (determinism):** 3 runs on one B1 fixture byte-identical stdout;
  full B1+B2 rerun → identical result digest. Zero RNG in the decision
  path (source grep: no random/time-seed; integer arithmetic only).

Targets (reported, not kill):

- T1: B1 correct ≥ 51/60 (85%).
- T2: B2 catch rate (correct direction on the 26 moving adv clips)
  ≥ 50%.
- T3: B3 ≥ 50% of MOTION windows judged correct direction.
- T4: ops ≤ 1.5M px-visits per 8-frame window (method2: 2.8M).

Withhold honesty: every WITHHOLD carries a reason code from §3.6 and
installs nothing. Withhold counts on B1 reported (expected ≤ 10%).

## 7. Commit plan

1. This prereg (frozen, alone).
2. `motion3.zag` source + build notes + determinism evidence.
3. Results: per-battery result tables, digests, `VERDICT_MOTION3.md`.
No binaries, no `.zagd` caches in the repo (rebuild via pinned
toolchain `toolchain/bin/znc_linux_x86_64_abed8aa1`; build command and
binary sha recorded).
