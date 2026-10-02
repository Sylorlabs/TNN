# PREREG D-VID-1/V2 - frozen preregistration, PRE-IMPLEMENTATION ONLY

Wave: 2026-09-24-0521pdt. Worker: D-VID-1 re-prereg (sensory headspace,
video lane).
Branch: tnn-native-lab. Working copy: ~/workspace/tnn-rsi.
Frozen: 2026-09-24 05:40 PDT. Status: PREREG ONLY. No V2 generator or
verifier code exists. Implementation is explicitly deferred to a future
wave; this document freezes the mechanism, the metric, and the kill bars
before any of that work begins.

Scope: D-VID-1 only. MOTION4 (FAIL K2, repair needing his sign-off) is
a separate lever and is not addressed or re-litigated here. Micah's
morning verdicts are closed.

## Provenance and the S8 return path

D-VID-1 V1 (flow-advected foam breakup) was tried in wave-20260923-2321pdt
and killed on its frozen T1 bar: variant 606 vs baseline 580 per-mille
foam flips, ratio 1.045 against bar <= 0.700. Frozen prereg
docs/lab/rsi/runs/wave-20260923-2021pdt/sensory-levers/PREREG_DVID1.md
(commit a4a42758abe46e6d3f6c2b44c19626d9066957); frozen addendum
docs/lab/rsi/runs/wave-20260923-2321pdt/sensory-levers/PREREG_DVID1_ADDENDUM.md
(commit c6db78f2a); implementation 037c31ae210bbd28ecda2316470db8f26c6f2f8e;
evidence 888ac69f4. The 2321pdt debate (M2) upheld DEAD: the T1
measurement was trustworthy, and the leading alternative hypothesis
(wrong arm-frame sign) was classed as candidate death under VKB6, not
metric invalidity. A wrong sign is a mechanism failure.

The debate carried an explicit S8 recommendation: a future wave may
re-prereg under S8 with the co-rotating (streak bx/bz) sign convention
and a boil metric measured in the rotating frame, under a NEW frozen
prereg in a later wave; the V1 mechanism as frozen is dead and is not
revived by re-interpretation. This document is that new frozen prereg.
It satisfies the S8 return condition: new mechanism (co-rotating sign)
plus new frozen metric (rotating-frame boil), frozen before any V2
implementation exists.

### What is new versus inherited

New in V2:
- Sign convention: foam breakup sampled in the co-rotating arm frame
  (the streak bx/bz convention), with the arm inward-drift law, applied
  to all three breakup terms. Explicit formula below.
- T1 metric: foam boil measured in the rotating (co-moving) frame, so
  intended rigid rotation with the water does not count as boiling. The
  V1 screen-space flip count is retired as a kill bar for V2.
- Metric trust gate: a frozen rigid-rotation control with a frozen
  noise-floor cap, bound in the implementation addendum before coding.
- VKB6 eye criterion now tests the mechanism's core visual claim: foam
  riding the water in the direction of arm rotation.

Inherited from V1 and the baseline:
- The ocean.zag baseline (docs/lab/imagination_discovery/vid/ocean.zag),
  untouched and git clean at the new HEAD; 48 frames, 1024x1024.
- The frozen V-* bars: V-RES, V-SHARP, V-TEMP, V-DET, V-COMP (see
  docs/lab/imagination_discovery/vid/VID-README.md; frozen prereg
  commit 988255e64dfc).
- Foam mask definition, sampling scales (400/70), seeds (51/54/52),
  inward drift law inw = 1000 - f*2, frame phase mrad = rot*6283/4000
  with rot = 8f from o_scene.
- The frozen battery structure: T2 (V-TEMP), T3 (V-SHARP within 5%),
  cost (<= 2x baseline), VKB1 through VKB7, and the verdict rule shape.
- Pure-Zag rule, no Python anywhere, commits local only, no adoption
  without blind video judging.

## The lever: V2 co-rotating flow-advected foam breakup

Class: physically motivated motion change (material advection). Not a
filter, not a post-process: the foam is part of the water and must move
with it, in the direction the water moves.

Why the sign changes: V1 advected bup and sbup into the arm-foam rx/rz
frame, which the frozen addendum's own red-team watch item showed places
a fixed texture feature at world angle (phi - mrad): counter-rotating
relative to the arm ridges. The arm ridges are features of
(ang*4000/6283 + r*8 - rot) with rot = 8f (see o_height and o_scene), so
ridge features move toward increasing o_atan2 angle as f increases. The
streak term's bx/bz convention is the inverse rotation: a fixed texture
feature sits at world angle (phi + mrad), co-rotating with the ridges.
The debate ruled the wrong sign a mechanism failure. V2 keeps V1's scope
(all foam breakup terms ride the water) and fixes the sign, so the foam
rides the water in the direction of arm rotation.

## What changes (single mechanism, new decision V2)

Only the noise-sample coordinates of the foam breakup terms change; the
foam structure (crest, steepness, arm, streak, spire ring, distance fade)
is untouched. In o_shade_water, the rotating-frame block below the bup
line is replaced by the co-rotating block (same phase law, flipped sign
convention), hoisted above the bup line:

```
let mrad:i64 = rot * 6283 / 4000;
let cph:i64 = 0;
let sph:i64 = 0;
o_cos_sin(mrad, &cph, &sph);
let rdx:i64 = wx - vwx;
let rdz:i64 = wz - vwz;
let cx:i64 = (rdx * cph - rdz * sph) / 1000;
let cz:i64 = (rdz * cph + rdx * sph) / 1000;
let inw:i64 = 1000 - f * 2;
cx = cx * inw / 1000 + vwx;
cz = cz * inw / 1000 + vwz;
```

Then:
- bup: was o_vn2(wx*400 - f*250, wz*400 + f*114, 51); becomes
  o_vn2(cx*400, cz*400, 51). Scale 400 and seed 51 preserved.
- sbup: was o_vn2(bx*70, bz*70, 54); becomes o_vn2(cx*70, cz*70, 54).
  Scale 70 and seed 54 preserved. (The baseline bx/bz sampling was
  co-rotating but lacked the inward drift; V2 adds the drift law so all
  terms follow the same flow.)
- abup: was o_vn2(rx*70, rz*70, 52); becomes o_vn2(cx*70, cz*70, 52).
  Scale 70 and seed 52 preserved; the counter-rotating convention is
  replaced by the co-rotating one.
- The old rx/rz statements are removed (abup was their only consumer).
  The streak ridge term keeps its existing bx/bz sampling; it is not a
  foam breakup term and is untouched.
- The spire-ring term keeps multiplying by bupm (now computed from the
  co-rotating bup); per the V1 default it is left as is, with VKB3 tell
  4 (rings stay attached, no pulsing) as the judge.
- Frame count (48), resolution (1024x1024), scene, colors, dither, and
  every other statement are untouched. The variant lives in a new file
  ocean_dvid1_v2.zag; the baseline ocean.zag is not modified.

Zero RNG: the sampling is a pure function of (f, wx, wz) through the
existing analytic flow. mrad peaks at 590 millirad (f=47), inside the
o_cos_sin small-angle domain.

Sign check (frozen): at f=0, rot=0, mrad=0, cph=1000, sph=0, inw=1000,
so cx=wx and cz=wz exactly; bup, sbup, and abup sample at the identical
coordinates as the baseline. V2 frame f0 is byte-identical to baseline
f0 by construction (pipeline check P4).

## Metrics (to be measured by a pure-Zag v2_verify.zag at implementation)

Foam mask (inherited, unchanged): pixel counts as foam iff L >= 200 and
(max(R,G,B) - min(R,G,B)) <= 40 (near-white, low saturation), with
L = (299R+587G+114B)/1000.

- T1 rotating-frame foam boil (NEW): the verifier reconstructs the
  rotating frame per frame f from the frozen phase law mrad(f) =
  rot(f)*6283/4000 (rot(f) = 8f), (cph, sph) = o_cos_sin(mrad), vortex
  center (vwx(f), vwz(f)) from the same o_scene laws, and inw(f) =
  1000 - f*2. The implementation addendum binds these as the exact
  algebraic inverse of the frozen sampling transform above; no
  independent constants are permitted. A fixed co-rotating cell grid
  covers the influence disc (160 world-unit radius about the vortex
  center, the same physical radius V1 used, fixed in the rotating
  frame). For each frame, each cell center maps to the frame's screen
  pixel through the inverse transform (nearest pixel); the cell's mask
  state is the foam mask at that pixel. T1 = mean over the 47
  consecutive pairs of (cells whose mask state flips between f and
  f+1) / (cells masked foam at f). Baseline and variant are measured by
  the same verifier code. Bar: T1_variant <= 0.700 * T1_baseline.
  Rationale: foam that rigidly rotates with the water is stationary in
  the co-moving frame and contributes zero flips by construction; what
  remains is genuine boiling (texture creation and destruction).
- Metric trust gate (frozen form; the numeric cap is bound in the
  implementation addendum before coding): a pure-Zag rigid-rotation
  control (baseline f0's foam mask analytically rotated by the exact
  inter-frame phase about the migrating center) must score at or below
  the frozen noise-floor cap, with the cap frozen to satisfy
  cap <= 0.250 * T1_baseline, before any variant comparison is
  trusted. The ruler's noise floor must sit well below the signal it
  must resolve (a 30 percent reduction).
- T1 screen-space (the V1 metric) is RETIRED as a kill bar for V2. It
  may be reported as a diagnostic with no verdict weight; it can
  neither pass nor kill the candidate.
- T2 no frozen video (inherited): the V-TEMP bar (per-pair mean
  |dL|/255 in [0.5%, 15%]) must still pass; advection must not collapse
  into a static texture.
- T3 sharpness (inherited): V-SHARP gradient ratios on f0 and f47
  within 5 percent of the baseline values (validation gate inherited:
  baseline f0/f47 ratios must reproduce the documented 1.607/1.543
  within rounding before any variant comparison is trusted).

Neither metric is an adoption criterion. Adoption needs blind judging of
the video pair (V-BLIND, separate crew). The eye decides whether the
foam reads as riding the water in the direction of arm rotation.

## Frozen predictions (directional, set before any implementation exists)

- P1: T1_variant <= 0.700 * T1_baseline. Co-rotating advection removes
  genuine boiling as seen in the co-moving frame; intended rigid
  rotation contributes zero flips by construction.
- P2: T2 passes on all 47 pairs. The texture keeps evolving; it does
  not freeze into a static overlay.
- P3: T3 passes: f0/f47 V-SHARP within 5 percent of baseline; no
  smearing from the coordinate change.
- P4: cost within 2x baseline per-frame (the co-rotating block adds one
  rotation plus drift per pixel to three noise terms, same order as
  V1); variant f0 byte-identical to baseline f0 (sign check above).
- P5: VKB6 eye review: the foam reads as riding the rotating water in
  the direction of arm rotation, not sliding over it, not frozen onto
  it, and not counter-rotating against the arms.

## Red-team confounds to attack (frozen list)

1. Remap quantization floor: nearest-pixel remapping of a rigid
   texture still flips edge cells. Defense: the trust gate; if the
   floor is high the ruler is unfit (see verdict mapping).
2. Inverse-transform identity: any independent constant or sign slip
   in the verifier's frame transform reintroduces the V1 failure mode.
   Defense: the addendum must exhibit the inverse derivation as the
   exact algebraic inverse of the frozen sampling formulas, plus the
   f0 byte-identity pipeline check.
3. Metric gaming by freezing: T1_rot is zero for a frozen texture too.
   Defense: T2 (V-TEMP lower bound 0.5 percent), VKB3 tell 2 (no
   frozen-overlay read), and VKB6 close this path together.
4. Inward-drift mismatch: if the true water motion is not the analytic
   inw law, the co-moving frame misaligns and T1_rot overcounts. The
   bar compares variant to baseline under the same frame, so
   misalignment hurts the variant; P1 bets the analytic law is close.
   The eye (VKB6) arbitrates the visual claim.
5. Spire-ring coupling: ringf multiplies bupm (now co-rotating); rings
   could detach or pulse. VKB3 tell 4 is the judge.
6. Region asymmetry: the influence disc is fixed in the rotating frame;
   the verifier must use the identical disc and code path for baseline
   and variant.

## Cost budget

- Per-frame render time within 2x the measured baseline per-frame time
  (baseline re-measured by the implementation wave via a fresh full
  48-frame render of unmodified ocean.zag; doubles as a pipeline
  reproducibility check, as V1 did).
- Full 48-frame build plus verify within the implementation wave's
  budget (to be written in the implementation addendum before coding;
  this prereg requires the budget to be written before implementation).

## Frozen kill bars

- VKB1 byte-identical determinism: a full clean 48-frame rerun is
  sha256-equal to the frozen V2 manifest, frame by frame. Any mismatch
  FAILS the candidate. (Same standard as V-DET.)
- VKB2 temporal metric: the metric trust gate passes first; then T1
  AND T2 AND T3 bars all pass. Gate failure voids the T1 measurement
  (see verdict mapping). Any part fails, the candidate is DEAD.
- VKB3 tell-list non-regression vs the rebuilt D-VID-1 baseline,
  judged on frame sequences (not stills): (1) no new strobing or banding
  in the foam, (2) no frozen-overlay read (foam must evolve, just
  coherently), (3) no texture swimming elsewhere introduced by the
  coordinate change, (4) spire foam rings still attached to the spires
  (the ring term uses bupm: verify the rings do not detach or pulse),
  (5) V-RES and V-COMP still pass. Any tell worse FAILS the candidate.
- VKB4 cost: per-frame render within 2x baseline. Over budget FAILS the
  candidate (free-lunch mandate extends to video: no cost regressions).
- VKB5 clean build: pinned compiler, zero RNG anywhere (grep-verified:
  no rand, random, srand, time, clock tokens), no slice over 2^25 bytes,
  pure Zag only. Standing owner rule: no Python anywhere in loop work.
  Any Python touch of a new wave artifact voids its wave evidence.
- VKB6 red-team eye review of the frame sequence (scrubbed f0-f47 and
  looped): the foam must read as riding the rotating water in the
  direction of arm rotation, not sliding over it, not frozen onto it,
  and not counter-rotating against the arms. New artifact class of any
  kind FAILS the candidate. Explicit metric-gaming check: T1_rot moves
  by construction for rigid rotation, so the eye, not the numbers,
  judges whether the motion reads as water; T2, VKB3 tell 2, and this
  bar together close the freeze-gaming path.
- VKB7 blind A/B video pair prepared with randomized non-descriptive
  names; mapping recorded ONLY in the sealed mapping file; pair verified
  pixel-genuine to the KB1-verified frames. Prepared only for
  READY-FOR-JUDGE.

## Verdict rule (for the future implementation wave)

READY-FOR-JUDGE only if VKB1 through VKB7 all pass. Otherwise DEAD,
with the killing evidence logged. UNVERIFIABLE only if the frozen
metric trust gate fails (the T1 question cannot be answered with the
frozen ruler); the candidate is then neither passed nor convicted on
T1, and return requires a new frozen prereg in a later wave.
UNVERIFIABLE is not available for any bar that measured cleanly: the
V1 debate's ruling stands (no post-hoc reinterpretation of a frozen
bar to change a verdict). No adoption without blind video judging,
whatever the metrics say.

## Commit order (S8 governance)

This prereg's first commit strictly precedes any V2 implementation
commit. The implementation wave's addendum (if any) strictly precedes
implementation; evidence follows. The prereg commit-order self-check
applies: the prereg's first commit must strictly precede the
implementation's. Failures cannot be adopted that wave. Frozen bars
cannot be weakened to force a pass.

## Open questions for the implementation wave (not decisions)

- The implementation addendum binds, before coding and without changing
  the mechanism or metric definition above: the exact algebraic inverse
  of the frozen sampling transform, the co-rotating cell grid geometry,
  the noise-floor cap (satisfying cap <= 0.250 * T1_baseline), and the
  rigid-rotation control result. It may not change the mechanism above.

## Provenance

Source prereg: this document is a verbatim re-freeze of
docs/lab/rsi/runs/wave-20260924-0221pdt/preregs/PREREG_DVID1_V2.md from
commit 681a0a3e, with only wave identifiers and dates updated to
wave-20260924-0521pdt / 2026-09-24. No mechanism, metric, or kill-bar
text was altered.

V1 provenance: frozen prereg a4a42758abe46e6d3f6c2b44c19626d9066957
(docs/lab/rsi/runs/wave-20260923-2021pdt/sensory-levers/PREREG_DVID1.md),
frozen addendum c6db78f2a
(docs/lab/rsi/runs/wave-20260923-2321pdt/sensory-levers/PREREG_DVID1_ADDENDUM.md),
implementation 037c31ae210bbd28ecda2316470db8f26c6f2f8e, evidence
888ac69f4. V1 verdict: DEAD (T1 ratio 1.045 against bar <= 0.700), upheld
by the wave-20260923-2321pdt debate (M2). S8 return condition satisfied:
new mechanism (co-rotating sign) plus new frozen metric (rotating-frame
boil), frozen before any V2 implementation exists.
