# PREREG D-VID-1/V3 - frozen preregistration, PRE-IMPLEMENTATION ONLY

Wave: 2026-09-24-2321pdt. Worker: Worker 3 (D-VID-1 geometry-churn video lever).
Branch: tnn-native-lab. Working copy: ~/workspace/tnn-rsi.
Run dir: docs/lab/rsi/runs/wave-20260924-2321pdt/dvid1_geomchurn/.
Frozen: 2026-09-24 23:45 PDT. Status: PREREG ONLY. No V3 generator,
verifier, manifest, or frame artifact exists. This document freezes the
mechanism, the metric, the trust gate, and the kill bars before any of
that work begins. It is committed ALONE, strictly before any
implementation file.

Baseline: docs/lab/imagination_discovery/vid/ocean.zag (D-VID-1 "alien
ocean", 48-frame 1024x1024 24-bit BMP generator, pure Zag, zero RNG),
with its frozen bars V-RES, V-SHARP, V-TEMP, V-DET, V-COMP (see
docs/lab/imagination_discovery/vid/VID-README.md; frozen prereg commit
988255e64dfc).

## Provenance header (frozen)

- RENDER_SHA: (to fill at implementation; sha256 of the frozen variant
  generator source ocean_dvid1_v3.zag, 64 hex chars)
- FIRST_RENDERED_WAVE: wave-20260924-2321pdt
- COMPONENT_LINEAGE:
  - D-VID-1 V1 (flow-advected foam breakup): DEAD [NEW],
    wave-20260923-2321pdt. Killed on frozen T1 bar: variant 606 vs
    baseline 580 per-mille foam flips, ratio 1.045 against bar <= 0.700.
  - D-VID-1 V2 (co-rotating foam breakup): DEAD [VOID],
    wave-20260924-0521pdt. Analytic no-op proof: bfade =
    o_clamp01k((200 - wz) * 1000 / 140) = 0 for wz >= 200; vortex disc
    wz 560..880, so every V2-retargeted term is gated dead (bupm = 1000,
    streak multiplier = 1, abupm dead code); ocean.zag diff exactly
    three hunks. Wave evidence VOID on a mid-wave python3 heredoc
    touching v2_verify.zag (frozen VKB5).
  - Whirlpool SCOOP: DISCARDED.
  - Whirlpool surface-planform: READY-FOR-JUDGE, QUEUED-UNJUDGED.
- NEW_KNOWLEDGE_CLAIM: In-plane deterministic displacement of disc foam
  geometry (not breakup sampling) raises screen-space foam boil by at
  least 30 percent over the rigid-sweep baseline while holding the
  V-TEMP, V-SHARP, determinism, and cost bars, giving the loop a live
  non-rigid churn lever for whirlpool foam.
- This prereg is the S8 return path for the 0521pdt debate M4 R3
  closure: "DEAD is the coordinate-retargeting of breakup sampling for
  disc foam churn (bfade = 0 kills every retargeted term). OPEN under a
  fresh prereg only: (a) disc foam churn via a DIFFERENT mechanism
  (geometry churn), or (b) a redefined goal." This document takes path
  (a). It is a genuinely new mechanism, not a re-freeze of V1/V2.
- No Python is authorized by this prereg. Not for the generator, not
  for the verifier, not for hashing, not for analysis, not for /tmp
  scratch. Any Python contact with a new wave artifact voids its wave
  evidence (M4 R1, prospective).

## The lever: V3 in-plane geometry churn of disc foam (turbulent churn)

Class: physically motivated motion change (non-rigid material churn).
Not a filter, not a post-process, not coordinate-retargeting of breakup
sampling, not a change to the bfade fade law.

Why geometry churn: the V2 verdict proved the disc foam churn measured
by T1 is pure geometry churn already: arm/crest/streak masks sweeping
through the rotating frame, with every breakup term multiplied out by
bfade = 0 in the disc (wz 560..880). That sweep is RIGID: the masks
rotate as one solid body at the frame phase mrad. Real whirlpool foam
is turbulent, not rigid: parcels churn relative to each other. V3 keeps
the foam structure exactly as the baseline computes it, but samples the
foam GEOMETRY at disc-plane positions displaced by a frozen
deterministic displacement field, so different parts of the disc churn
at different rates and directions. The breakup sampling coordinates
(bup seed 51, sbup seed 54, abup seed 52) keep their exact baseline
formulas; the bfade fade law keeps its exact baseline argument (wz).

## What changes (single mechanism, frozen formulas)

In o_shade_water, after the spire-ring term and before the foam clamp,
insert the frozen churn block. New top-level helpers (frozen):

```
// Bhaskara-I sine, X in [0, 3142] milliradians, returns sin*1000
fn o_sin_bh(X:i64) i64 {
    let p:i64 = X * (3142 - X);
    return 16 * p / (49348 - 4 * p / 1000);
}
// full-range sine, th in [0, 6283) milliradians, returns sin*1000
fn o_sin1000(th:i64) i64 {
    if (th > 3142) { return 0 - o_sin_bh(6283 - th); }
    return o_sin_bh(th);
}
```

Frozen churn block (inserted after `if (ringf > foam) { foam = ringf; }`,
before `if (foam > 1000) { foam = 1000; }`):

```
let gdx:i64 = wx - vwx;
let gdz:i64 = wz - vwz;
let gr:i64 = o_isqrt(gdx * gdx + gdz * gdz);
let churn_gate:i64 = o_clamp01k((190 - gr) * 1000 / 40);
let foam_d:i64 = foam;
if (churn_gate > 0) {
    let th1:i64 = 6283 * (wz * 9 + f * 35) / 1000;
    let th2:i64 = 6283 * (wx * 14 - f * 55) / 1000;
    let th3:i64 = 6283 * (wx * 11 + f * 45) / 1000;
    let th4:i64 = 6283 * (wz * 17 - f * 28) / 1000;
    th1 = th1 - (th1 / 6283) * 6283; if (th1 < 0) { th1 = th1 + 6283; };
    th2 = th2 - (th2 / 6283) * 6283; if (th2 < 0) { th2 = th2 + 6283; };
    th3 = th3 - (th3 / 6283) * 6283; if (th3 < 0) { th3 = th3 + 6283; };
    th4 = th4 - (th4 / 6283) * 6283; if (th4 < 0) { th4 = th4 + 6283; };
    let s1:i64 = o_sin1000(th1);
    let s2:i64 = o_sin1000(th2);
    let s3:i64 = o_sin1000(th3);
    let s4:i64 = o_sin1000(th4);
    let Dx:i64 = churn_gate * (22 * s1 + 14 * s2) / 1000000;
    let Dz:i64 = churn_gate * (20 * s3 + 12 * s4) / 1000000;
    let mwx:i64 = wx + Dx;
    let mwz:i64 = wz + Dz;
    let m2:i64 = 0; let fall2:i64 = 0; let arm2:i64 = 0; let sprox2:i64 = 0;
    let h2:i64 = o_height(mwx, mwz, f, vwx, vwz, rot, &m2, &fall2, &arm2, &sprox2);
    let e:i64 = 3;
    let a1:i64 = 0; let b1:i64 = 0; let c1:i64 = 0; let d1:i64 = 0;
    let a2:i64 = 0; let b2:i64 = 0; let c2:i64 = 0; let d2:i64 = 0;
    let hxp:i64 = o_height(mwx + e, mwz, f, vwx, vwz, rot, &a1, &b1, &c1, &d1);
    let hxm:i64 = o_height(mwx - e, mwz, f, vwx, vwz, rot, &a2, &b2, &c2, &d2);
    let dhdx2:i64 = (hxp - hxm) * 1000 / (2 * e);
    let hzp:i64 = o_height(mwx, mwz + e, f, vwx, vwz, rot, &a1, &b1, &c1, &d1);
    let hzm:i64 = o_height(mwx, mwz - e, f, vwx, vwz, rot, &a2, &b2, &c2, &d2);
    let dhdz2:i64 = (hzp - hzm) * 1000 / (2 * e);
    let steep2:i64 = dhdx2;
    if (steep2 < 0) { steep2 = 0 - steep2; }
    let st2b:i64 = dhdz2;
    if (st2b < 0) { st2b = 0 - st2b; }
    steep2 = steep2 + st2b;
    let crestf2:i64 = o_ss((h2 - capth) * 1000 / 900);
    let steepf2:i64 = o_ss((steep2 - 260) * 1000 / 220);
    foam_d = crestf2;
    if (steepf2 > foam_d) { foam_d = steepf2; }
    foam_d = foam_d * bupm / 1000;
    let armf2:i64 = o_ss((arm2 - 500) * 1000 / 300);
    if (armf2 > foam_d) { foam_d = armf2; }
    let mrdx:i64 = mwx - vwx;
    let mrdz:i64 = mwz - vwz;
    let mbx:i64 = (mrdx * cph - mrdz * sph) / 1000 + vwx;
    let mbz:i64 = (mrdz * cph + mrdx * sph) / 1000 + vwz;
    let strk2:i64 = o_ridge2(mbx * 36, mbz * 36, 2, 53);
    let streakf2:i64 = o_ss((strk2 - 660) * 1000 / 220) * fall2 / 1000;
    streakf2 = streakf2 * o_mix(1000, o_ss((sbup - 430) * 1000 / 270), bfade) / 1000;
    if (streakf2 > foam_d) { foam_d = streakf2; }
    let ringf2:i64 = sprox2 * 750 / 1000 * bupm / 1000;
    if (ringf2 > foam_d) { foam_d = ringf2; }
    if (foam_d > 1000) { foam_d = 1000; }
}
foam = o_mix(foam, foam_d, churn_gate);
```

Frozen constants: R_IN = 150, R_OUT = 190 world units (gate full at
r <= 150, zero at r >= 190); amplitudes A1 = 22, A2 = 14, A3 = 20,
A4 = 12 world units (max |D| = 48 world units, about 61 px at disc
depth); spatial frequencies P1 = 9, P2 = 14, P3 = 11, P4 = 17 per-mille
per world unit (wavelengths about 59..111 world units); temporal rates
Q1 = 35, Q2 = 55, Q3 = 45, Q4 = 28 per-mille per frame (about 1.3..2.6
cycles over the 48-frame clip, incommensurate); central-difference
epsilon e = 3 world units (matches the baseline dhdz edge convention).

What does NOT change, explicitly:
- bup, sbup, abup keep their exact baseline sampling coordinates and
  seeds (51, 54, 52). No breakup sampling coordinate is retargeted.
- bfade keeps its exact baseline formula and argument:
  bfade = o_clamp01k((200 - wz) * 1000 / 140). The fade law is untouched.
- The breakup multiplier values applied inside the displaced block
  (bupm; the o_mix(1000, o_ss((sbup-430)*1000/270), bfade) factor) are
  the baseline values, computed from the untouched sampling.
- capth, the streak ridge scale (36) and seed (53), the ring scale,
  the normal-perturbation block (bfade2), base color, specular, fog,
  dither: all untouched.
- Frame count (48), resolution (1024x1024), scene, camera: untouched.
- Outside the disc (churn_gate = 0) the variant is bit-identical to the
  baseline by construction: foam_d is unused and
  o_mix(foam, foam_d, 0) = foam.
- The variant lives in a new file ocean_dvid1_v3.zag in the run dir
  (with its own substrate copy); the baseline ocean.zag is not modified.
- No inverse transform is used anywhere in V3 (the metric is
  screen-space), so the V2 addendum's defective inverse is moot and is
  not reused.

Zero RNG: the displacement field is a pure function of (f, wx, wz)
through frozen integer arithmetic. Deterministic by construction.

## Metric: T1-GC geometry-churn boil (frozen)

T1-GC is the V1 screen-space foam boil operationalization, unchanged,
so the V1 baseline value (580 per-mille) is a cross-check on the new
verifier:

- Foam mask: pixel counts as foam iff L >= 200 and
  (max(R,G,B) - min(R,G,B)) <= 40, with L = (299R+587G+114B)/1000.
- Region: per frame f, vortex center (vwx, vwz) from the frozen
  o_scene; center height hc = o_height(vwx, vwz, f, ...); screen center
  (xc, yc) = (512 + vwx*920/vwz, o_sy(hc, vwz)); radius = 160*920/vwz px
  (160 world-unit influence radius at that depth).
- T1-GC = mean over the 47 consecutive pairs of
  (mask flips between f and f+1) / (foam pixels in region at f),
  in per-mille (integer: flips * 1000 / foam, summed over pairs, divided
  by 47).
- Frozen bar: T1-GC_variant >= 1.30 * T1-GC_baseline, evaluated in
  integer per-mille arithmetic as T1v_pm * 1000 >= T1b_pm * 1300.
- Direction rationale (frozen): V1/V2 tried to REDUCE boil by advecting
  foam with the water; both died. V3 accepts the V2 finding that disc
  foam churn is geometry-driven and replaces the rigid sweep with
  turbulent non-rigid churn. The intended effect is MORE churn, so the
  boil metric must move upward by a non-micro amount (>= 30 percent);
  a smaller move is a micro-tweak and fails. Whether the churn reads as
  more real is decided by VKB6 (eye) and, if reached, his blind judging,
  never by the metric alone.
- Validation gate: the fresh baseline render's T1-GC must reproduce the
  V1 recorded baseline (580 per-mille) within +-25 per-mille before any
  variant comparison is trusted. Failure voids the T1-GC measurement
  (UNVERIFIABLE on T1-GC), not a pass.

## Trust gate G-LIVE (frozen; analytic, from the committed source)

G-LIVE passes iff all three hold on the committed variant source; any
failure makes the wave UNVERIFIABLE (never DEAD-by-assumption):

- G1 (the V2 failure cannot recur): in the disc (wz >= 200),
  bfade = o_clamp01k((200 - wz) * 1000 / 140) = 0, hence
  bupm = o_mix(1000, X, 0) = 1000 (identity) and the streak breakup
  factor o_mix(1000, Y, 0)/1000 = 1. The displaced geometry terms reach
  foam_d through max() with no bfade-gated zero factor anywhere.
- G2 (dataflow): foam_d = max(crestf2, steepf2, armf2, streakf2,
  ringf2), each a pure function of the displaced position (mwx, mwz);
  foam = o_mix(foam, foam_d, churn_gate) with churn_gate = 1000 for
  r <= 150 world units, covering the metric region core.
- G3 (displacement is non-degenerate): amplitudes A1..A4 are all
  strictly positive and the four sine components have incommensurate
  spatial/temporal frequencies, so (mwx, mwz) != (wx, wz) on a dense
  set of disc pixels at every frame.
- Honest limitation, frozen: ringf2 is dead in the disc because
  sprox2 = 0 there (spires stand at wz 2500..3900, far outside the
  disc); liveness rests on crestf2, steepf2, armf2, streakf2. This is
  stated so the gate cannot be gamed by counting dead terms.
- Diagnostic D1 (no verdict weight): at f = 10, at least 5 percent of
  the metric-region pixels differ between variant and baseline
  (proves the churn is visibly live, corroborates G1..G3).

## Frozen kill bars VKB1..VKB7 and verdict mapping

- VKB1 byte-identical determinism: THREE independent full clean
  48-frame renders are sha256-equal to the frozen V3 manifest, frame by
  frame (pure-Zag hashing, validated against system sha256sum on
  samples). Any mismatch FAILS the candidate.
- VKB2 metric bars: T1-GC bar (>= 1.30x, with the 580 pm validation
  gate) AND T2 AND T3 all pass. Any part fails, the candidate is DEAD.
  - T2 (V-TEMP): per-pair mean |dL|/255 over all pixels,
    L = (299R+587G+114B+500)/1000, in percent x100; every one of the 47
    variant pairs in [50, 1500] (0.5% to 15%). Churn must not collapse
    into a frozen overlay (lower bound) or explode into strobing
    (upper bound).
  - T3 (V-SHARP): gradient ratio x1000 exactly as in V1/V2 (sum
    |dx|+|dy| over L divided by the same after 2x2 box downscale to
    512 and box upscale back), on f0 and f47. Validation gate: the
    fresh baseline f0/f47 ratios must reproduce the documented
    1607/1543 within rounding before any variant comparison is
    trusted. Bar: |variant - baseline| / baseline <= 5% on both frames.
- VKB3 tell-list non-regression vs the rebuilt D-VID-1 baseline,
  judged on frame sequences (not stills): (1) no new strobing or
  banding in the foam, (2) no frozen-overlay read (foam must evolve,
  just non-rigidly), (3) no texture swimming introduced outside the
  disc (variant is bit-identical to baseline there by construction;
  the verifier checks it), (4) spire foam rings still attached to the
  spires (ringf2 is dead in the disc; rings live in the far field
  where churn_gate = 0), (5) V-RES and V-COMP still pass. Any tell
  worse FAILS the candidate.
- VKB4 cost: per-frame render time within 2x the measured baseline
  mean per-frame time (baseline measured this wave by a fresh full
  48-frame render of unmodified ocean.zag; doubles as a pipeline
  reproducibility check). Total wave compute budget: 60 minutes wall
  (baseline rebuild + three variant renders + verifier + hashing).
  Over budget FAILS the candidate.
- VKB5 clean build: pinned compiler
  src/tools/toolchain/znc_linux_x86_64_abed8aa1 (sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef),
  zero RNG anywhere (grep-verified: no rand, random, srand, time, clock
  tokens), no slice over 2^25 bytes, pure Zag only. No Python touches
  any new wave artifact, at any step, for any reason. Any Python
  contact voids the wave evidence.
- VKB6 red-team eye review of the frame sequence (scrubbed f0..f47 and
  looped, plus the dbg foam channel): the foam must read as churning
  water, not sliding over it and not frozen onto it. New artifact class
  of any kind FAILS the candidate. Explicit metric-gaming check: T1-GC
  moves by construction if the displacement is implemented, so the eye,
  not the numbers, judges whether the churn reads as water.
- VKB7 sealed blind A/B video pair: two 48-frame sequences under
  randomized non-descriptive names; mapping recorded ONLY in the sealed
  mapping file; each frame verified pixel-genuine against the
  VKB1-frozen manifest. Prepared ONLY for READY-FOR-JUDGE.

Verdict mapping (frozen):
- READY-FOR-JUDGE [NEW] iff G-LIVE and VKB1 through VKB6 all pass
  (VKB7 then prepares the pair; judging is his, never the loop's).
- DEAD [NEW] with the killing evidence logged, iff G-LIVE passes and
  any of VKB1..VKB6 fails.
- UNVERIFIABLE [NEW] iff G-LIVE fails, a validation gate fails, or the
  evidence is compromised (including any Python contact). Never
  DEAD-by-assumption.
- No sealed pair is prepared unless the mapping says READY-FOR-JUDGE.

## Unit conventions (S10; dated 2026-09-24, pre-implementation)

- per-mille (pm): parts per thousand; 10 pm = 1 percent.
- T1-GC in per-mille; the 1.30x bar is T1v_pm * 1000 >= T1b_pm * 1300
  (integer arithmetic, no floats).
- T2 in percent x100 (pct_x100), per the V1/V2 convention: bar
  [50, 1500] = [0.5%, 15%].
- T3 in gradient ratio x1000, per the V1/V2 convention: frozen
  baseline values 1607/1543.
- Cost ratio as integer per-mille: variant_per_frame_pm <= 2000 means
  within 2x.
- Where this prereg and a prior D-VID record conflict on units, this
  dated pre-implementation section governs; the looser reading is never
  adopted post-run.

## Commit order (frozen)

1. This prereg (alone; no implementation file exists yet).
2. ocean_dvid1_v3.zag + substrate copy + verifier + sha tool
   (implementation).
3. Evidence: manifests, measurements, sealed pair if earned, verdict.
All commits local on tnn-native-lab, prefixed
"wave-20260924-2321pdt:". The frozen prereg commit strictly precedes
all of them (verified ancestor of HEAD before implementation begins).
