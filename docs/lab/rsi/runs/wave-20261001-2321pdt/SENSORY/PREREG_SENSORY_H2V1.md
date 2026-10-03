# PREREG SENSORY-H2V1 - frozen preregistration, committed BEFORE any H2v1 code exists

Wave: wave-20261001-2321pdt. Slot: sensory big-lever.
Branch: tnn-native-lab. Working copy: ~/workspace/tnn-rsi.
Lane dir: docs/lab/rsi/runs/wave-20261001-2321pdt/SENSORY/
Frozen: 2026-10-01 23:55 PDT. Status: PREREG ONLY. No H2v1 generator,
verifier, or render exists. Implementation begins only after this file
is committed alone (with NAMECHECK.md and the design calculator
h2v1/design_calc.zag, whose frozen outputs this prereg cites).
Ordering evidence: file mtimes + sha256 in NAMECHECK.md; the prereg
commit contains no H2v1 implementation artifact. UNVERIFIABLE ORDERING
voids the prereg.

## Candidate: H2v1 FORWARD-SCATTER DECK FIELD (FSDF) [NEW]

## What the discarded H1v2 established (re-derived background, frozen)

H1v2 TRANSPORT-ANCHORED LIT CLOUD DECK (wave-20261001-2021pdt) was
BUILD-FAIL on frozen KB3-LIGHTLOGIC (sun mean +0.64 vs >= 3.0; diff
+0.72 vs >= 6.0) and KB9-COST (2.36x vs <= 2.0x). KB1/2/4/5/6/7/8/10/11
passed; KB11 = 0, no artifacts. Full record:
docs/lab/rsi/runs/wave-20261001-2021pdt/SENSORY/h1v2/IMPLEMENTATION.md.

Re-derived cause (from the frozen H1v2 block and verdict, not from
memory): H1v2 fixed the sign (transport-anchored march, one lit-side
convention; KB10 alignment error under 5e-7) but the mechanism
produced per-blob contrast (KB4 variance 89.58) that averaged to near
zero within each screen half. The frozen bar measures a systematic
half-level shift; per-blob light logic cannot move half-means. This is
a mechanism-level negative result: correct anchoring at blob scale is
insufficient; the effect must live at deck scale. H1v2 also cost +26
fbm octave-evals per sky pixel that its prereg prediction missed.

H2v1 is therefore a NEW mechanism, not a retune: it abandons per-blob
light logic entirely and operates a deck-scale angular luminance field
anchored in the sun vector. Different scale, different information
pathway (sun-amount gate, no density gradients, no march), different
fidelity path (deck luminance, not blob shading).

## The new mechanism (frozen definition)

The deck-scale forward-scatter field: cloud radiance is modulated by a
sun-anchored angular field computed per pixel from the ray and the
frozen T1 sun. Physical basis: forward scattering brightens clouds
toward the sun; the anti-solar deck dims. The anchoring uses samt =
b_sunamt(dx, dz), the per-pixel sun amount from the frozen sun azimuth
(the horizontal projection of the T1 sun vector (-0.617, 0.191,
-0.764); geometrically valid for the deck, elevation variation is
second-order across the fixture). The field is

fwd = b_ss((samt - 0.65) / 0.10)      (forward lobe, toward the sun)
anti = b_ss((0.70 - samt) / 0.10)     (anti-solar wing, away)
field = 1.0 + 0.10 * fwd - 0.50 * anti

Gate derivation (from frozen geometry, not renders): the pure-Zag
design calculator h2v1/design_calc.zag replicates the frozen camera
math, fixture point sets, and baseline cirrus block and reports the
sunAmt distribution over kept SKYWIN: sun half (x < 510) samt in
[0.698, 0.850], mean 0.777; anti half (x >= 510) samt in [0.518,
0.688], mean 0.607. The gates are placed on that distribution: fwd
rises across samt 0.65..0.75 (screen x approx 434..549, a smooth
115-pixel transition, no band edge); anti rises across samt 0.60..0.70
(x approx 491..606). Gain derivation: the calculator grids (LF, LA)
and predicts KB statistics; (0.10, 0.50) is the frozen choice, the
only grid point with margin on every bar (predictions below). The
gains are exaggerated relative to physical forward scattering (which
cannot move half-means at this sun distance); the honesty is in the
anchoring (derived per pixel, correct side), documented here, not in
physical exactness of the gain.

Density and alpha are lane-standard infrastructure, unchanged from
H1v2: h1_dens (seeds 601/602, verbatim), cov = b_ss((den - 0.52) /
0.14), a = cov * hf clamped to 1.0. KB2 is expected at 0.2916, the
H1v2-measured value. The baseline's own sparser alpha is NOT kept:
with the baseline alpha the clamp fundamentally limits per-point dL
and the half-means cannot reach the bar (derived in the lane notes);
the H1-family alpha is the lane's established cloud field.

Cost: the block evaluates h1_dens (6 fbm octave-evals, identical to
the baseline cirrus block's 6) plus ~15 flops per sky pixel for the
field. Zero new fbm evals. Free-lunch cost class (H1v2 added 26).

## Frozen replacement block (exact)

Replaces the "thin cirrus, warm-lit on the sun side" block inside
b_sky (the `if (dy > 0.02)` block), nothing else. All arithmetic is
f64, deterministic, zero RNG. The implementation must contain this
block verbatim (modulo whitespace); any deviation is a prereg
violation, not a tuning opportunity. h1_dens is defined verbatim from
H1v2 (seeds 601/602). sunAmt is the existing b_sky local.
```
if (dy > 0.02) {
    let px:f64 = dx / (dy + 0.18) * 1.4;
    let pz:f64 = dz / (dy + 0.18) * 1.4;
    let den:f64 = h1_dens(px, pz);
    let cov:f64 = b_ss((den - 0.52) / 0.14);
    let hf:f64 = b_ss((dy - 0.02) / 0.15);
    let a:f64 = cov * hf;
    if (a > 1.0) { a = 1.0; }
    let fwd:f64 = b_ss((sunAmt - 0.65) / 0.10);
    let anti:f64 = b_ss((0.70 - sunAmt) / 0.10);
    let field:f64 = 1.0 + 0.10 * fwd - 0.50 * anti;
    let cr:f64 = b_mix(0.55, 1.0, sunAmt) * field;
    let cg:f64 = b_mix(0.42, 0.72, sunAmt) * field;
    let cb:f64 = b_mix(0.48, 0.55, sunAmt) * field;
    r = b_mix(r, cr, a);
    g = b_mix(g, cg, a);
    b = b_mix(b, cb, a);
}
```

## Why this is a new mechanism, not a parameter tweak

A parameter tweak would keep H1v2's information pathway (density
gradients, sun march, per-blob shade) and adjust gains. H2v1 removes
that pathway entirely: no gradients, no march taps, no per-blob
terms. The new pathway is a deck-scale angular field from the sun
vector applied as a radiance multiplier. It answers the diagnosed
H1v2 failure (blob-scale effects average to zero at half level) by
operating at the scale the bar measures, and it restores the cost
class H1v2 lost (zero new fbm evals).

## Baseline (frozen)

- Source: docs/lab/imagination_discovery/img/r11_alien.zag (in-tree,
  unmodified for the baseline build).
- Toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
  sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (verified before use).
- IO substrate: the vendored copy from wave-20260924-1121pdt
  (candidates/g1/sub/R33_NATIVE_IO_V1.zag, sha256
  e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8)
  copied byte-identical into SENSORY/h2v1/sub/R33_NATIVE_IO_V1.zag
  (hash re-verified at copy time).
- The baseline is built FIRST: SENSORY/h2v1/r11_baseline.zag is a byte
  copy of r11_alien.zag with only the @import line repointed at
  ./sub/R33_NATIVE_IO_V1.zag (diff-verified: exactly one line differs).
- Baseline gate (same fixture as H1v2): (a) the one-line diff verifies;
  (b) two 1024 baseline renders are byte-identical, and should match
  the 1721pdt baseline sha
  72e66537357d676847a81d374c5dc67221f6dc2029ad8fc0186a7d70dda1ab8b
  (mismatch files a dated pre-change addendum and stops the wave; no
  baseline substitution); (c) the geometric validator keep-count
  asserts pass on the rebuilt baseline. If (a), (b), or (c) fails, the
  wave stops and files a dated pre-change addendum.
- Reference size: 1024x1024 (D-RES standard). A 256 smoke render times
  the pipeline first; the sealed pair uses 1024.

## Frozen point sets (verifier h2v1_verify.zag, pure Zag, on final BMPs)

Same cloud-deck fixture as H1v2 (sets, formulas, and keep-count asserts
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
the rebuilt baseline, before any H2v1 code is compiled. If any assert
fails, that is a prereg-spec defect and the candidate is DISCARDED
(G1-v1 precedent); no set is re-aimed, no bar is tuned.

New in the verifier: the KB10-ANCFIELD computation (defined under the
bars) and the KB2 alpha recomputation from the frozen H2v1 alpha
(H1-family, not the baseline's).

## Frozen kill bars (at least as strict as H1v2)

- KB1-DET: 3 renders of the H2v1 variant at 1024, sha256 identical
  across all 3. Else FAIL.
- KB2-COVERAGE: fraction of kept SKYWIN with cloud alpha a > 0.15
  (a recomputed by the verifier from the frozen H2v1 alpha math) in
  [0.08, 0.60]. Expected 0.2916 (H1v2-measured).
- KB3-LIGHTLOGIC: mean(dL over SUNHALF kept) -
  mean(dL over ANTISUN kept) >= 6.0, AND mean(dL over SUNHALF kept)
  >= 3.0. Same bar as H1v2, unchanged strictness.
- KB4-STRUCTURE: variance of dL over SKYWIN kept >= 40.0.
- KB5-NONREG-TERRAIN: mean |dL| over TERRAIN kept <= 1.0.
- KB6-NONREG-MOON: mean |dL| over MOON kept <= 1.0.
- KB7-SKYCALM: |mean(dL) over FULLSKY kept| <= 5.0, and fraction of
  FULLSKY kept with |dL| > 12 <= 0.35.
- KB8-ANTIGRAIN (honors the E3 rejection): acutance ratio
  variant/baseline over ACU <= 1.15.
- KB9-COST: variant 1024 wall time <= 2.0x baseline 1024 wall time
  (matched-contention pairing rule, same as H1v2), and extra fbm
  octave-evals per sky pixel reported (expected 0).
- KB10-ANCFIELD (replaces KB10-ALIGN; catches anchoring bugs at
  design level for the new mechanism): the verifier recomputes per
  kept SKYWIN pixel samt = b_sunamt(rdx, rdz) and the frozen field
  (fwd, anti, field with frozen gates and gains). Clause A: the kept
  pixel maximizing field has x < 512 (bright lobe on the sun side; a
  backwards or screen-constant field fails). Clause B: max(field) -
  min(field) over kept SKYWIN >= 0.40 (a degenerate constant field
  fails). Else FAIL.
- KB11-DROPOUT: fraction of kept FULLSKY with |dL| > 60 equals 0.0.
  Any hard blowout or dropout fails. Additionally, before any verdict,
  the verdict worker must document a knowledge-vs-architecture
  investigation of the renders for dropout, flicker, banding, or
  weirdness (data gap in the density field vs substrate flaw), per the
  standing red-team rule. Flicker across renders is already excluded
  by KB1; weirdness is the documented eye pass.
- VKB-EYE: a sealed blind A/B pair (baseline vs H2v1 variant, 1024
  PNG) is prepared for Micah ONLY if every frozen bar passes.
  Randomized, mapping sealed in SEALED_MAPPING. He is the judge.
  Nothing is adopted on metrics alone: a PASSing candidate is
  READY-FOR-JUDGE only.

## Frozen predictions (from the design calculator, geometry only)

design_calc.zag phase 1 (sunAmt distribution, coverage): SUNAMT_SUNHALF
mean 0.777 in [0.698, 0.850] (n=25); SUNAMT_ANTISUN mean 0.607 in
[0.518, 0.688] (n=23); COVERAGE_H1ALPHA 0.2916. Phase 2 grid over
(LF, LA); frozen choice (0.10, 0.50) predicts: KB3 sunmean 3.94,
antimean -5.85, diff 9.80; KB4 variance 196.13; KB7 |fsmean| 0.57,
bigfrac 0.2013; KB11 max|dL| 48.46; KB2 0.2916; KB10 range 0.60,
argmax x = 320. KB5 predicted small (dome-mean near zero; H1v2's
0.45 came with a larger dome-mean). KB6 0.00 by construction. KB8
passes (smooth field, no hash/RNG). KB9 passes (0 new fbm evals;
~15 flops per sky pixel). KB1 passes (pure functions of pixel
coordinates). Calculator limits documented: assumes 100% keep
(H1v2 measured 48/48 SKYWIN, 144/144 FULLSKY); ignores dither and
byte truncation (plus/minus 1, averages out); does not model the
ambient/reflection b_sky call sites (KB5/KB6 are the real guards).
The bars decide on real renders.

## Provenance header (planned, machine-checkable, for JUDGE_BRIEF.md)

RENDER_SHA: <sha256 of the H2v1 variant BMP, filled at render time>
FIRST_RENDERED_WAVE: wave-20261001-2321pdt
COMPONENT_LINEAGE: wave-20261001-1721pdt H1 LIT CLOUD DECK:JUDGED-DISCARDED; wave-20261001-2021pdt H2v1 (this wave's H1v2) TRANSPORT-ANCHORED LIT CLOUD DECK:BUILD-FAIL (KB3, KB9); h1_dens/h1_alpha (seeds 601/602):inherited lane infrastructure (H1 family); r11-substrate(champion,ROUND11_VERDICT,committed); R9:QUEUED-UNJUDGED; C1:QUEUED-UNJUDGED; C2v3:QUEUED-UNJUDGED; S11-IMG:QUEUED-UNJUDGED; C12:QUEUED-UNJUDGED; S13:QUEUED-UNJUDGED; S14:QUEUED-UNJUDGED; whirlpool-planform:QUEUED-UNJUDGED; G1:STOOD-DOWN; DP-1:HELD; E3:REJECTED-BY-JUDGE
NEW_KNOWLEDGE_CLAIM: A deck-scale sun-anchored angular luminance field (forward lobe plus anti-solar dimming wing, per-pixel from the frozen sun vector, zero new fbm evals) moves cloud-deck half-means where per-blob light logic provably could not.
Tag: [NEW]. This is not a re-certification of H1 or H1v2. Both
discarded candidates are listed only as lineage so the judge queue
stays honest.

## Levers considered and rejected (why this is the one)

- H1v2 retune (different gains on the transport-anchored march):
  rejected; the H1v2 verdict is a mechanism-level negative (blob
  scale cannot move half-means); retuning is the micro-tweak the
  standing owner rule forbids.
- 3D forward-scatter angle (cosang) field: derived and tested in the
  calculator; the sun's off-frame distance compresses the 3D angle
  across the fixture (means 0.882 vs 0.786), giving insufficient
  half-separation. The azimuthal gate separates (0.777 vs 0.607).
- Baseline-alpha field: derived and killed in the calculator; the
  sparse baseline alpha plus the byte clamp fundamentally cap
  per-point dL below what the half-means need. Documented negative.
- Sun-anchored coverage redistribution (denser deck toward the sun):
  real lever, but the coverage-change dL carries the wrong sign
  against the darker anti-solar sky and needs unphysical dimming to
  overcome; held, not this wave.
- Valley haze planes: real lever on terrain, but KB5 (frozen,
  unchanged strictness) forbids terrain changes; held as a follow-up
  under a future terrain-owning prereg, not this wave.
- Cloud shadows on terrain: same KB5 conflict; not this wave.
- Volumetric crepuscular shafts: G1, tried twice, STOOD-DOWN. Never
  revived.
- Film grain / micro-grain: E3 rejected by Micah's eyes 2026-09-23.
  KB8 hard-codes that verdict. Never again.
- Water specular glitter: r11 has no water body; scene change, not a
  mechanism on the frozen baseline.
- Depth-of-field camera: camera change, risks the crispness judges
  reward; not a world mechanism.
- New scene renderer: out of scope for a single-wave lever; the clean
  A/B needs the frozen r11 baseline.
- Audio: V11 is Micah's closed frontier; DP-1 is HELD. This slot
  stays out of audio.

## Governance

- Pure Zag, literally: design calculator, generator, verifier,
  analysis, and scratch are pure Zag compiled with the frozen
  toolchain. No Python anywhere. Any Python touch of a new wave
  artifact voids that wave's evidence on sight; there is no recovery
  path this wave.
- Safebin toolchain guard active (NAMECHECK.md Step 0); `which
  python3` prints nothing. Em/en dash byte checks use the shell-only
  snippet docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh.
- znc quirk honored: no `as *i32` + slice construction inside
  functions; u8-backed cells with little-endian pack/unpack helpers.
- No em-dashes in loop documentation (standing style rule).
- Commits stay local on tnn-native-lab. Nothing is pushed. This
  prereg is committed alone (with NAMECHECK.md and design_calc.zag);
  implementation begins only after that commit.
- Red-team: any dropout, flicker, artifact, or weirdness in the
  renders gets a knowledge-vs-architecture investigation (data gap in
  the density field or substrate flaw), documented in the verdict
  file before any verdict line. KB11 is the machine half of this
  rule; the documented investigation is the other half.

## Verdict: PROCEED (to commit)

H2v1 FORWARD-SCATTER DECK FIELD is a new candidate: the first cloud
attempt to operate at deck scale with a sun-anchored angular luminance
field, derived per pixel from the frozen sun vector, at zero new fbm
cost. Frozen bars: KB3 unchanged in strictness, KB9 at 2.0x with 0 new
fbm evals expected, KB10 redefined as ANCFIELD for the new mechanism,
KB11 dropout at 0.0 plus the mandatory documented red-team
investigation, determinism 3/3. Draft ends here; this prereg is
committed alone; implementation begins only after that commit.
