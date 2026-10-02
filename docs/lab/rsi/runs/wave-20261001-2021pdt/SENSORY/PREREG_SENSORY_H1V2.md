# PREREG SENSORY-H1V2 - frozen preregistration, committed BEFORE any H1v2 code exists

Wave: wave-20261001-2021pdt. Slot: sensory big-lever.
Branch: tnn-native-lab. Working copy: ~/workspace/tnn-rsi.
Lane dir: docs/lab/rsi/runs/wave-20261001-2021pdt/SENSORY/
Frozen: 2026-10-01 20:31 PDT. Status: PREREG ONLY. No H1v2 generator,
verifier, or render exists. Implementation begins only after this file
is written and committed alone by the coordinator. Commits are
forbidden to the worker this phase, so ordering evidence is file mtime
+ sha256 recorded in the lane NAMECHECK.md: this prereg file predates
every H1v2 implementation artifact. UNVERIFIABLE ORDERING voids the
prereg.

## Candidate: H1v2 TRANSPORT-ANCHORED LIT CLOUD DECK [NEW]

## What the discarded H1 established (re-derived background, frozen)

H1 LIT CLOUD DECK (wave-20261001-1721pdt) was DISCARDED on frozen
KB3-LIGHTLOGIC: sun-side mean dL +1.52, anti-sun mean dL +3.65,
difference -2.13 against a bar requiring difference >= 6.0 with
sun-side mean >= 3.0 (wrong sign). Seven other bars passed
(KB2 0.2916, KB4 64.33, KB5 0.65, KB6 0.00, KB7 0.00/0.1388,
KB8 1.036, KB9 0.89x cost). Full record:
docs/lab/rsi/runs/wave-20261001-1721pdt/SENSORY/VERDICT_H1_DISCARDED.md.

Re-derived cause (from the frozen H1 block and the verdict, not from
memory): the 2-tap self-shadow march sampled the density field along
the world sun azimuth (-0.628, -0.778) applied directly in (px, pz)
projective field space, where px = dx/(dy+0.18)*1.4. That projection
warps direction across the frame, so the march direction was
misaligned with the true sun direction and the self-shadow term sh
came out systematically lower on the sun side, darkening it relative
to the baseline's already-bright flat cirrus.

Re-derivation adds one finding the H1 verdict did not state: the
discarded block's two light terms contradicted each other on which
side is lit. The march term (sh = 1.15 - 1.3*(0.65*s1 + 0.35*s2),
s1/s2 sampled toward the sun) darkens the anti-sun flank of a density
blob and leaves the sun-facing flank bright: its lit side is the
sun-facing flank. The flank-shading term (slope = gx*-0.628 +
gz*-0.778, shade rising with slope) is positive where the density
gradient points toward the sun, which is the anti-sun flank of a blob
(there the gradient points sunward, toward the blob center): its lit
side is the anti-sun flank. So the block brightened anti-sun flanks
with one term while its shadow term darkened them with the other, and
both terms reused the world azimuth in field space. The KB3 wrong sign
is overdetermined by these two defects.

H1v2 is therefore a NEW mechanism, not a retune: it replaces the
constant-azimuth anchoring with a per-pixel sun direction derived from
the rendered geometry, and it unifies both light terms on one lit-side
convention. No constant is tuned against renders; every constant below
is frozen.

## The new anchoring (frozen mechanism definition)

The deck projection used by the mechanism is the map
P(vx, vy, vz) = (1.4*vx/(vy+0.18), 1.4*vz/(vy+0.18)),
evaluated at the pixel ray v = (dx, dy, dz).

The frozen T1 3D sun vector (from b_sunx/b_suny/b_sunz, deliberated,
in-tree) is S = (-0.617, 0.191, -0.764).

The H1v2 sun direction in field space is the TRANSPORT of S through P
at the pixel ray: with frozen epsilon E = 0.001,

T = (P(dx + E*Sx, dy + E*Sy, dz + E*Sz) - P(dx, dy, dz)) / E,

(mx, mz) = T / max(|T|, 1e-9).

(mx, mz) is the direction in (px, pz) field space produced by a
world-space step toward the sun. It is computed per pixel from the
camera ray, the projection, and the frozen sun vector. No source
constant in the H1v2 block encodes a field-space sun direction; the
anchoring is derived, not supplied. This is the mechanism change that
fixes the diagnosed cause: the march direction is no longer the world
azimuth reused in field space.

The same transported direction anchors the flank-shading term, and
both terms use one lit-side convention (the sun-facing flank of a
density blob is bright): slope = -(gx*mx + gz*mz). On the sun-facing
flank the density gradient points anti-sunward (toward the blob
center), so -(grad . m) is positive there and shade rises, agreeing
with the march term's lit side. The discarded block's sign
contradiction is removed.

## Frozen replacement block (exact)

Replaces the "thin cirrus, warm-lit on the sun side" block inside
b_sky (the `if (dy > 0.02)` block), nothing else. All arithmetic is
f64, deterministic, zero RNG. The implementation must contain this
block verbatim (modulo whitespace); any deviation is a prereg
violation, not a tuning opportunity.
```
if (dy > 0.02) {
    let px:f64 = dx / (dy + 0.18) * 1.4;
    let pz:f64 = dz / (dy + 0.18) * 1.4;
    let ex:f64 = dx + 0.001 * -0.617;
    let ey:f64 = dy + 0.001 * 0.191;
    let ez:f64 = dz + 0.001 * -0.764;
    let qx:f64 = ex / (ey + 0.18) * 1.4;
    let qz:f64 = ez / (ey + 0.18) * 1.4;
    let tx:f64 = (qx - px) / 0.001;
    let tz:f64 = (qz - pz) / 0.001;
    let tm:f64 = b_sqrt(tx * tx + tz * tz);
    let tmc:f64 = tm;
    if (tmc < 0.000000001) { tmc = 0.000000001; }
    let mx:f64 = tx / tmc;
    let mz:f64 = tz / tmc;
    let den:f64 = h1_dens(px, pz);
    let cov:f64 = b_ss((den - 0.52) / 0.14);
    let th:f64 = 0.35 + 0.65 * b_fbm2(px * 3.1 + 11.0, pz * 6.0 + 5.0, 604, 2);
    let hf:f64 = b_ss((dy - 0.02) / 0.15);
    let e:f64 = 0.06;
    let gx:f64 = (h1_dens(px + e, pz) - den) / e;
    let gz:f64 = (h1_dens(px, pz + e) - den) / e;
    let slope:f64 = -(gx * mx + gz * mz);
    let shade:f64 = 0.62 + 1.2 * slope * th;
    if (shade < 0.05) { shade = 0.05; }
    if (shade > 1.35) { shade = 1.35; }
    let s1:f64 = h1_dens(px + mx * 0.10, pz + mz * 0.10);
    let s2:f64 = h1_dens(px + mx * 0.22, pz + mz * 0.22);
    let sh:f64 = 1.15 - 1.3 * (0.65 * s1 + 0.35 * s2);
    if (sh < 0.15) { sh = 0.15; }
    if (sh > 1.0) { sh = 1.0; }
    let lit:f64 = shade * sh;
    if (lit > 1.2) { lit = 1.2; }
    let top_r:f64 = b_mix(0.62, 1.0, sunAmt);
    let top_g:f64 = b_mix(0.46, 0.72, sunAmt);
    let top_b:f64 = b_mix(0.50, 0.55, sunAmt);
    let hz_r:f64 = b_mix(0.45, 0.85, sunAmt);
    let hz_g:f64 = b_mix(0.32, 0.45, sunAmt);
    let hz_b:f64 = b_mix(0.44, 0.28, sunAmt);
    let lk:f64 = lit;
    if (lk < 0.0) { lk = 0.0; }
    if (lk > 1.0) { lk = 1.0; }
    let cr:f64 = b_mix(hz_r * 0.85, top_r, lk);
    let cg:f64 = b_mix(hz_g * 0.85, top_g, lk);
    let cb:f64 = b_mix(hz_b * 0.85, top_b, lk);
    let lining:f64 = b_ss((sunAmt - 0.55) / 0.2) * b_ss((0.30 - cov) / 0.14) * b_ss((cov - 0.04) / 0.06);
    cr = cr + lining * 0.72;
    cg = cg + lining * 0.50;
    cb = cb + lining * 0.36;
    let a:f64 = cov * hf;
    if (a > 1.0) { a = 1.0; }
    r = b_mix(r, cr, a);
    g = b_mix(g, cg, a);
    b = b_mix(b, cb, a);
}
```

Unchanged from the discarded block: the density field h1_dens (seeds
601/602, same placement language), coverage, thickness, height fade,
clamp ranges, warm-top / dust-glow-underlight colors, silver lining
term, alpha compositing. Changed: the sun direction is the transported
(mx, mz) instead of the constant (-0.628, -0.778); the flank-shading
dot uses the lit-side convention -(grad . m); the march taps step
along (mx, mz). b_sunamt (ray-space azimuth dot, geometrically valid
in the horizontal plane) is untouched.

## Why this is a new mechanism, not a parameter tweak

A parameter tweak would keep the same information pathway and adjust
gains, clamps, or step sizes. H1v2 changes the pathway: the discarded
mechanism read the sun's field-space direction from a source constant
(the world azimuth, valid only in world space); H1v2 computes it per
pixel from the rendered geometry (the pixel ray through the frozen
camera, the deck projection, the frozen 3D sun vector). The anchoring
moved from supplied to derived. The slope sign change is not a gain
tweak either: it repairs a sign contradiction between the block's two
light terms that the KB3 wrong sign exposed. Nothing here is tuned
against renders; the bar decides.

## Baseline (frozen)

- Source: docs/lab/imagination_discovery/img/r11_alien.zag (in-tree,
  unmodified for the baseline build).
- Toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
  sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (verified before use).
- IO substrate: the vendored copy from wave-20260924-1121pdt
  (candidates/g1/sub/R33_NATIVE_IO_V1.zag, sha256
  e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8)
  copied byte-identical into SENSORY/h1v2/sub/R33_NATIVE_IO_V1.zag
  (hash re-verified at copy time).
- The baseline is built FIRST: SENSORY/h1v2/r11_baseline.zag is a byte
  copy of r11_alien.zag with only the @import line repointed at
  ./sub/R33_NATIVE_IO_V1.zag (diff-verified: exactly one line differs).
- Baseline gate (same fixture as H1): (a) the one-line diff verifies;
  (b) two 1024 baseline renders are byte-identical, and should match
  the 1721pdt baseline sha
  72e66537357d676847a81d374c5dc67221f6dc2029ad8fc0186a7d70dda1ab8b
  (mismatch files a dated pre-change addendum and stops the wave; no
  baseline substitution); (c) the geometric validator keep-count
  asserts pass on the rebuilt baseline. If (a), (b), or (c) fails, the
  wave stops and files a dated pre-change addendum.
- Reference size: 1024x1024 (D-RES standard). A 256 smoke render times
  the pipeline first; the sealed pair uses 1024.

## Frozen point sets (verifier h1v2_verify.zag, pure Zag, on final BMPs)

Same cloud-deck fixture as H1 (sets, formulas, and keep-count asserts
frozen identical). The verifier copies the baseline world model
verbatim (camera basis, b_trace, b_moonhit) to classify pixels. Luma
L = (299R + 587G + 114B) / 1000 on final BMP bytes.
dL = L_variant - L_baseline. All sets at 1024x1024.

- SKYWIN (cloud region): k=0..47: x = 320 + (k*79 % 380),
  y = 40 + (k*53 % 160). Keep: trace < 0 and moonhit < 0.
  Assert kept >= 36 of 48.
- SUNHALF / ANTISUN: kept SKYWIN with x < 510 / x >= 510.
  Assert each >= 12.
- TERRAIN: k=0..63: x = 40 + (k*61 % 944),
  y = 700 + (k*37 % 250). Keep: trace > 0. Assert kept >= 56.
- MOON: 4x4 grid over dx,dy in {-33,-11,11,33} around the moon disc
  center, where the center is computed in the verifier from the frozen
  camera math (project the frozen moon world position through the
  frozen camera basis; no hand-placed constants). Keep: moonhit > 0.
  Assert kept >= 12 of 16.
- FULLSKY: k=0..143: x = 20 + (k*67 % 984),
  y = 10 + (k*41 % 300). Keep: trace < 0 and moonhit < 0.
  Assert kept >= 100.
- ACU (anti-grain): kept SKYWIN. Acutance A = mean over kept points
  of |L(x,y) - L(x+2,y)|, read from BMP bytes.

Geometric validator: the verifier's keep-count asserts run FIRST on
the rebuilt baseline, before any H1v2 code is compiled. If any assert
fails, that is a prereg-spec defect and the candidate is DISCARDED
(G1-v1 precedent); no set is re-aimed, no bar is tuned.

New in the verifier: the march-field conformance computation for
KB10 (defined under the bars) and the blowout scan for KB11.

## Frozen kill bars

- KB1-DET: 3 renders of the H1v2 variant at 1024, sha256 identical
  across all 3. Else FAIL.
- KB2-COVERAGE: fraction of kept SKYWIN with cloud alpha a > 0.15
  (a recomputed by the verifier from the frozen field math, unchanged
  from H1) in [0.08, 0.60]. The mechanism must fire without paving
  the sky.
- KB3-LIGHTLOGIC (corrected, re-frozen): mean(dL over SUNHALF kept) -
  mean(dL over ANTISUN kept) >= 6.0, AND mean(dL over SUNHALF kept)
  >= 3.0. Cloud light must obey the T1 sun's direction with the
  correct sign, measured against the baseline the variant replaces
  (the sun-side clause is the sign check against the baseline's own
  warm flat cirrus, per the H1 verdict lesson).
- KB4-STRUCTURE: variance of dL over SKYWIN kept >= 40.0. Lit tops
  and dark bases, not a uniform wash.
- KB5-NONREG-TERRAIN: mean |dL| over TERRAIN kept <= 1.0.
- KB6-NONREG-MOON: mean |dL| over MOON kept <= 1.0.
- KB7-SKYCALM: |mean(dL) over FULLSKY kept| <= 5.0, and fraction of
  FULLSKY kept with |dL| > 12 <= 0.35. No global sky regrade.
- KB8-ANTIGRAIN (honors the E3 rejection): acutance ratio
  variant/baseline over ACU <= 1.15. Clouds are soft structures.
- KB9-COST: variant 1024 wall time <= 2.0x baseline 1024 wall time
  (matched-contention pairing rule, same as H1), and extra fbm
  octave-evals per sky pixel reported. This is 2x tighter than H1's
  frozen 4.0x allowance: the transport adds projection arithmetic
  only, zero new fbm evals, so the free-lunch cost class is preserved.
  (The 2.0x headroom is the standing "genuine trade can cost more"
  allowance, justified here because the anchoring is computed rather
  than constant.)
- KB10-ALIGN (new: catches the azimuth-reuse bug directly): for each
  kept SKYWIN pixel, the verifier computes the mechanism's declared
  march field M (the frozen finite-difference transport with
  E = 0.001, normalized) and an independent geometry-derived
  reference R: the analytic Jacobian of P at the pixel ray,
  J = [[1.4/(dy+0.18), -1.4*dx/(dy+0.18)^2, 0],
       [0, -1.4*dz/(dy+0.18)^2, 1.4/(dy+0.18)]],
  dotted with S = (-0.617, 0.191, -0.764), taking the (x, z)
  components normalized. Alignment error err = 1 - (Mx*Rx + Mz*Rz).
  Pixels with |J*S| < 1e-6 are excluded as degenerate (none expected:
  the sun disc sits out of frame per the trace-integrity correction,
  so no sky ray looks along S). Bar: mean(err) over kept SKYWIN
  <= 0.02 AND max(err) <= 0.15. Else FAIL. The discarded H1 design's
  constant-azimuth march gives err approx 0.11 on a representative
  sky-band pixel (dx=0.5, dy=0.02, dz=-0.3), so this bar fails the old
  bug class at design level; the new design's expected mean err is
  ~1e-5 (finite-difference truncation only), so the bound is set two
  orders of magnitude above the new design and an order of magnitude
  below the old defect, not tuned on renders.
- KB11-DROPOUT (new: artifact red-team machine bar): fraction of kept
  FULLSKY with |dL| > 60 equals 0.0. Any hard blowout or dropout
  fails. Additionally, before any verdict, the verdict worker must
  document a knowledge-vs-architecture investigation of the renders
  for dropout, flicker, banding, or weirdness (data gap in the
  density field vs substrate flaw), per the standing red-team rule.
  Flicker across renders is already excluded by KB1; weirdness is the
  documented eye pass.
- VKB-EYE: a sealed blind A/B pair (baseline vs H1v2 variant, 1024
  PNG) is prepared for Micah ONLY if every frozen bar passes.
  Randomized, mapping sealed in SEALED_MAPPING. He is the judge.
  Nothing is adopted on metrics alone: a PASSing candidate is
  READY-FOR-JUDGE only.

## Frozen predictions (directional)

KB2 passes identical to H1 (the field math is unchanged; expected
0.2916). KB3 passes with the correct sign: the transported march now
samples density toward the true sun, so sun-facing flanks keep
sh near 1.0 while anti-sun flanks drop toward 0.15, and the
flank-shading term now agrees with the march term instead of fighting
it; the mechanism's full lit-to-dark swing is on the order of 80 dL
units, ample against the 6.0 bar. KB4 passes (tops brighten, bases
darken, lining adds edge variance). KB5/KB6 pass at 0.00 by
construction (the sky branch never runs for terrain or moon rays).
KB7 passes (alpha is coverage-gated; clear sky keeps the untouched
gradient). KB8 passes (all new terms are fbm-smooth or smooth
projection arithmetic; no hash, no RNG anywhere). KB9 passes (the
transport adds ~12 multiplies per sky pixel and zero fbm evals;
terrain raymarching still dominates frame cost). KB10 passes near
1e-5 mean err by construction. KB11 passes (clamps unchanged; no new
blowout pathway). KB1 passes (pure functions of pixel coordinates,
zero RNG). The risk is KB3's magnitude against the baseline's
already-warm sun-side flat cirrus: the corrected light logic must not
merely fix the sign but beat the baseline's own sun-side warmth by a
net 6.0.

## Provenance header (planned, machine-checkable, for JUDGE_BRIEF.md)

RENDER_SHA: <sha256 of the H1v2 variant BMP, filled at render time>
FIRST_RENDERED_WAVE: wave-20261001-2021pdt
COMPONENT_LINEAGE: wave-20261001-1721pdt H1 LIT CLOUD DECK:JUDGED-DISCARDED; r11-substrate(champion,ROUND11_VERDICT,committed); R9:QUEUED-UNJUDGED; C1:QUEUED-UNJUDGED; C2v3:QUEUED-UNJUDGED; S11-IMG:QUEUED-UNJUDGED; C12:QUEUED-UNJUDGED; S13:QUEUED-UNJUDGED; S14:QUEUED-UNJUDGED; whirlpool-planform:QUEUED-UNJUDGED; G1:STOOD-DOWN; DP-1:HELD; E3:REJECTED-BY-JUDGE
NEW_KNOWLEDGE_CLAIM: Anchoring the cloud deck self-shadow march and flank shading in the sun vector transported through the deck projection into field space (per-pixel geometry-derived march directions, one lit-side convention) replaces world-azimuth reuse with correct light logic at the same cost class.
Tag: [NEW]. This is not a re-certification of H1. The discarded
candidate is listed only as lineage so the judge queue stays honest.

## Levers considered and rejected (why this is the one)

- Volumetric crepuscular shafts: G1, tried twice, STOOD-DOWN. Not
  revived.
- Film grain / micro-grain: E3 rejected by Micah's eyes 2026-09-23.
  KB8 hard-codes that verdict. Never again.
- Contact occlusion: R9 sealed QUEUED-UNJUDGED. Re-proposing would
  re-surface the pending queue.
- Water specular glitter: r11 has no water body; adding one is a
  scene change needing new composition, not a mechanism on the frozen
  baseline.
- Depth-of-field camera: focus-plane work was decided on r8c (D19);
  a thin-lens accumulation pass is a camera change, not a world
  mechanism, and risks the crispness judges reward.
- Valley haze planes: real lever, but weaker information gain than
  clouds (the sky's painted look is the larger photo-tell in r11).
  Held as a follow-up, not this wave.
- New scene renderer: out of scope for a single-wave lever; the clean
  A/B needs the frozen r11 baseline.
- Audio: V11 is Micah's closed frontier; DP-1 is HELD in queue.
  This slot stays out of audio. His 35 reserved AMBIG video clips
  are untouched.
- A constant-azimuth retune of H1 (different gains, clamps, or step
  sizes on the same march): rejected as a parameter tweak of a
  disproven anchoring; the bar that killed H1 would still be measuring
  a misaligned march.

## Governance

- Pure Zag, literally: generator, verifier, analysis, and scratch are
  pure Zag compiled with the frozen toolchain. No Python anywhere.
  Any Python touch of a new wave artifact voids that wave's evidence
  on sight; there is no recovery path this wave.
- Safebin toolchain guard active (NAMECHECK.md Step 0); `which
  python3` prints nothing. Em/en dash byte checks use the shell-only
  snippet docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh.
- znc quirk honored: no `as *i32` + slice construction inside
  functions; u8-backed cells with little-endian pack/unpack helpers.
- No em-dashes in loop documentation (standing style rule).
- Commits stay local on tnn-native-lab. Nothing is pushed. This phase
  forbids worker commits; the coordinator commits this prereg alone,
  then authorizes implementation. Implementation begins only after
  that commit.
- Red-team: any dropout, flicker, artifact, or weirdness in the
  renders gets a knowledge-vs-architecture investigation (data gap in
  the density field or substrate flaw), documented in the verdict
  file before any verdict line. KB11 is the machine half of this
  rule; the documented investigation is the other half.

## Verdict: PROCEED (to coordinator commit)

H1v2 TRANSPORT-ANCHORED LIT CLOUD DECK is a new candidate: the first
cloud attempt whose sun direction is derived from the rendered
geometry instead of reused from the world azimuth, with the march and
flank-shading terms unified on one lit-side convention. Frozen bars:
the corrected KB3 with sign checked against the baseline it replaces,
a new KB10 march-alignment bar that fails the discarded design's bug
class at design level, a new KB11 dropout bar plus the mandatory
documented red-team investigation, determinism 3/3, and a cost bar 2x
tighter than H1's. Draft ends here; the coordinator commits this
prereg alone; implementation begins only after that commit.
