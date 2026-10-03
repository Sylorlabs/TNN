# PREREG SENSORY-H3 - frozen preregistration, committed BEFORE any H3 code exists

Wave: wave-20261002-0221pdt. Slot: sensory big-lever.
Branch: tnn-native-lab. Working copy: ~/workspace/tnn-rsi.
Lane dir: docs/lab/rsi/runs/wave-20261002-0221pdt/SENSORY/
Frozen: 2026-10-02 02:55 PDT. Status: PREREG ONLY. No H3 generator,
verifier, or render exists. Implementation begins only after this file
is committed alone (with NAMECHECK.md and the design calculator
h3/design_calc.zag, whose frozen outputs this prereg cites).
Ordering evidence: file mtimes + sha256 in NAMECHECK.md; the prereg
commit contains no H3 implementation artifact. UNVERIFIABLE ORDERING
voids the prereg.

Naming: the task text asked for PREREG_SENSORY_H2.md, but the prior
wave froze PREREG_SENSORY_H2V1.md for its own candidate. To keep the
provenance record collision-free this candidate is H3. Recorded in
NAMECHECK.md; this is not a re-certification of any prior candidate.

## Candidate: H3 SUN-ANCHORED SKY-DOME LUMINANCE GRADIENT (SDLGRAD) [NEW]

## What the prior waves established (re-derived background, frozen)

H1 LIT CLOUD DECK (1721pdt) DISCARDED on KB3 (diff -2.13 vs >= 6.0,
wrong sign; projection-warped sun march). H1v2 TRANSPORT-ANCHORED LIT
CLOUD DECK (2021pdt) BUILD-FAIL on KB3 (sun +0.64 vs >= 3.0, diff +0.72
vs >= 6.0; mechanism-level negative: per-blob light logic averages to
zero at half level) and KB9 (2.36x vs <= 2.0x; +26 fbm octave-evals per
sky pixel). H2v1 FORWARD-SCATTER DECK FIELD (2321pdt) has NO RECORDED
VERDICT: the prior wave ended mid-pipeline (h2v1c stalled at row
704/960, blind/ empty, no verdict file). Its status is UNJUDGED-OPEN.
This lane ran the prior lane's frozen verifier binary read-only over
its existing renders as design input (NOT a verdict): base1 vs h2v1a
gives KB3 sun +3.92 / diff +9.92 PASS (deck-scale fields DO move
half-means where per-blob logic could not), KB4 198.34 PASS, KB5 1.03
vs <= 1.0 (a terrain leak, not a cloud failure: the FSDF field sits
inside b_sky's cirrus block, and b_tshade calls b_sky for its
hemisphere ambient samples, so the field fires for terrain pixels;
the prereg calculator admitted it did not model the ambient call
sites), KB6 0.00, KB7 -0.54 / 0.2013, KB8 1.090, KB10 argx 320 /
range 0.60, KB11 0, KB1 indeterminate (third render incomplete).
Lineage claims nothing more than this analysis.

## The new mechanism (frozen definition)

A sun-anchored luminance gradient applied to the CLEAR-SKY DOME on the
direct-sky path only. Physical basis: on the deliberated dusty 0.6-bar
world, forward scattering brightens the clear sky toward the sun
across the whole dome and the anti-solar sky cools and dims. The
baseline already does this at the horizon ring (T2: hz colors mix by
sunAmt) but the k1/k2 zenith mixes wash sunAmt out above dy ~ 0.18,
leaving the upper dome azimuthally flat, a classic CG tell. H3 extends
the sun-anchored gradient through the dome. The gradient is
achromatic (all three channels multiplied equally; hue untouched), and
it is placed BEFORE the sun disc/glow block (the sun itself is never
re-graded) and BEFORE the cirrus block (clouds sit in the graded sky;
the cirrus block stays byte-identical).

Placement (the KB5-leak fix by construction): the gradient lives in a
NEW function b_skydome whose body is b_sky's body byte-identical
except the inserted H3 block. Only the 3 direct-sky main-loop call
sites switch from b_sky to b_skydome. b_tshade's two ambient calls
keep calling the original b_sky byte-identical; the moon path is
untouched. Therefore KB5 and KB6 are 0.00 by construction. A nonzero
KB5/KB6 measurement above the bar is a construction violation and
kills the candidate.

## Frozen H3 block (exact, inserted verbatim)

Inserted inside b_skydome immediately after the three horizon/zenith
mix lines (the sr/sg/sb k1/k2 lines) and before the `if (dy < 0.0)`
branch. All arithmetic is f64, deterministic, zero RNG. The
implementation must contain this block verbatim (modulo whitespace);
any deviation is a prereg violation, not a tuning opportunity.
```
    // H3 DOME GRADIENT (frozen): sun-anchored luminance field on the
    // clear-sky dome. Applied to the dome color only, before the sun
    // disc/glow and before the cirrus block. dy-gated: the
    // below-horizon flat color is untouched.
    if (dy >= 0.0) {
        let dg_w:f64 = b_ss((sunAmt - 0.62) / 0.12);
        let dg_c:f64 = b_ss((0.68 - sunAmt) / 0.12);
        let dg:f64 = 1.0 + 0.15 * dg_w - 0.20 * dg_c;
        if (dg < 0.60) { dg = 0.60; }
        if (dg > 1.40) { dg = 1.40; }
        r = r * dg;
        g = g * dg;
        b = b * dg;
    }
```
Frozen gains (GW, GC) = (0.15, 0.20), the grid point with margin on
every predicted bar (design_calc.zag phase 2). Frozen gates:
dg_w rises across sunAmt 0.62..0.74, dg_c rises across sunAmt
0.68..0.56; both derived from the fixture's sunAmt distribution
(sun half [0.698, 0.850] mean 0.777; anti half [0.518, 0.688] mean
0.607; the gates sit on the separation between the halves).
Frozen clamps [0.60, 1.40] are the KB11 backstop.

## Why this is a new mechanism, not a parameter tweak or a repair

H1, H1v2, and H2v1 all replaced the cirrus block's cloud lighting; none
touched the clear-sky dome itself. H3 leaves the cirrus block
byte-identical and modulates a different scene layer (the background
the whole scene is judged against) through a different pathway (dome
luminance multiplier from sunAmt; no cloud density, no alpha, no
march). Repairing H2v1's KB5 leak was considered and rejected: it is a
repair of another candidate, not a new mechanism, and the standing
rule for this wave demands structural difference.

## Frozen call-site change (exact)

In the main render loop, the three direct-sky lines
```
                    cr = b_sky(rdx, rdy, rdz, 0);
                    cg = b_sky(rdx, rdy, rdz, 1);
                    cb = b_sky(rdx, rdy, rdz, 2);
```
become
```
                    cr = b_skydome(rdx, rdy, rdz, 0);
                    cg = b_skydome(rdx, rdy, rdz, 1);
                    cb = b_skydome(rdx, rdy, rdz, 2);
```
All other b_sky call sites (b_tshade lines 659-661) remain b_sky.

Diff contract (machine-checked at implementation): r11_baseline.zag vs
r11_alien.zag differs in exactly one line (the @import repoint, same
as every prior wave). h3_dome.zag vs r11_baseline.zag differs in
exactly: the added b_skydome function (b_sky body byte-identical plus
the frozen H3 block) and the three call-site lines. Any other delta
is a prereg violation.

Cost: the block is ~12 flops per direct-sky pixel, zero b_fbm2 calls,
zero new fbm octave-evals per sky pixel (free-lunch cost class; the
per-sky-pixel fbm count stays 6, identical to the baseline).

## Baseline (frozen)

- Source: docs/lab/imagination_discovery/img/r11_alien.zag (in-tree,
  unmodified for the baseline build).
- Toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
  sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (verified before use).
- IO substrate: the vendored copy from wave-20260924-1121pdt
  (candidates/g1/sub/R33_NATIVE_IO_V1.zag, sha256
  e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8)
  copied byte-identical into SENSORY/h3/sub/R33_NATIVE_IO_V1.zag
  (hash re-verified at copy time).
- The baseline is built FIRST: SENSORY/h3/r11_baseline.zag is a byte
  copy of r11_alien.zag with only the @import line repointed at
  ./sub/R33_NATIVE_IO_V1.zag (diff-verified: exactly one line differs).
- Baseline gate (same fixture as prior waves): (a) the one-line diff
  verifies; (b) two 1024 baseline renders are byte-identical, and must
  match the 1721pdt baseline sha
  72e66537357d676847a81d374c5dc67221f6dc2029ad8fc0186a7d70dda1ab8b
  (mismatch files a dated pre-change addendum and stops the wave; no
  baseline substitution); (c) the geometric validator keep-count
  asserts pass on the rebuilt baseline. If (a), (b), or (c) fails, the
  wave stops and files a dated pre-change addendum.
- Reference size: 1024x1024 (D-RES standard). A 256 smoke render times
  the pipeline first; the sealed pair uses 1024.

## Frozen point sets (verifier h3_verify.zag, pure Zag, on final BMPs)

Same cloud-deck fixture as H1v2/H2v1 (sets, formulas, and keep-count
asserts frozen identical). The verifier copies the baseline world
model verbatim (camera basis, b_trace, b_moonhit) to classify pixels.
Luma L = (299R + 587G + 114B) / 1000 on final BMP bytes.
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
the rebuilt baseline, before any H3 code is compiled. If any assert
fails, that is a prereg-spec defect and the candidate is DISCARDED
(G1-v1 precedent); no set is re-aimed, no bar is tuned.

New in the verifier: the KB10-ANCDOME computation (defined under the
bars) and the KB2 baseline-alpha recomputation (H3 does not change
clouds; alpha is the verbatim r11 cirrus alpha).

## Frozen kill bars (at least as strict as H2v1)

- KB1-DET: 3 renders of the H3 variant at 1024, sha256 identical
  across all 3. Else FAIL.
- KB2-COVERAGE: fraction of kept SKYWIN with cloud alpha a > 0.15
  (a recomputed by the verifier from the VERBATIM r11 cirrus alpha
  math, seeds 601/602, baseline offsets) in [0.08, 0.60]. Expected
  0.1250 (design calculator phase 1).
- KB3-LIGHTLOGIC: mean(dL over SUNHALF kept) -
  mean(dL over ANTISUN kept) >= 6.0, AND mean(dL over SUNHALF kept)
  >= 3.0. Same bar as H1v2/H2v1, unchanged strictness.
- KB4-STRUCTURE: variance of dL over SKYWIN kept >= 40.0.
- KB5-NONREG-TERRAIN: mean |dL| over TERRAIN kept <= 1.0. Expected
  0.00 by construction (b_tshade calls the original b_sky). A
  nonzero measurement above the bar is a construction violation:
  FAIL.
- KB6-NONREG-MOON: mean |dL| over MOON kept <= 1.0. Expected 0.00 by
  construction (moon path untouched).
- KB7-SKYCALM: |mean(dL) over FULLSKY kept| <= 5.0, and fraction of
  FULLSKY kept with |dL| > 12 <= 0.35.
- KB8-ANTIGRAIN (honors the E3 rejection): acutance ratio
  variant/baseline over ACU <= 1.15.
- KB9-COST: variant 1024 wall time <= 2.0x baseline 1024 wall time
  (matched-contention pairing rule, same as H1v2/H2v1), and extra fbm
  octave-evals per sky pixel reported (expected 0; the H3 block
  contains no b_fbm2/b_vn2 calls).
- KB10-ANCDOME (replaces KB10-ANCFIELD; catches anchoring bugs at
  design level for the new mechanism): the verifier recomputes per
  kept SKYWIN pixel samt = b_sunamt(rdx, rdz) and the frozen dome
  field dg = clamp(1 + 0.15*ss((samt-0.62)/0.12) -
  0.20*ss((0.68-samt)/0.12), 0.60, 1.40). Clause A: the kept pixel
  maximizing dg has x < 512 (bright lobe on the sun side; a
  backwards or screen-constant field fails). Clause B: max(dg) -
  min(dg) over kept SKYWIN >= 0.20 (a degenerate constant field
  fails). Else FAIL.
- KB11-DROPOUT: fraction of kept FULLSKY with |dL| > 60 equals 0.0.
  Any hard blowout or dropout fails. Additionally, before any verdict,
  the verdict worker must document a knowledge-vs-architecture
  investigation of the renders for dropout, flicker, banding, or
  weirdness (data gap in the density field vs substrate flaw), per the
  standing red-team rule. Flicker across renders is already excluded
  by KB1; weirdness is the documented eye pass.
- VKB-EYE: a sealed blind A/B pair (baseline vs H3 variant, 1024
  PNG) is prepared for Micah ONLY if every frozen bar passes.
  Randomized, mapping sealed in SEALED_MAPPING. He is the judge.
  Nothing is adopted on metrics alone: a PASSing candidate is
  READY-FOR-JUDGE only.

## Frozen predictions (from the design calculator, geometry only)

design_calc.zag phase 1: SUNAMT_SUNHALF mean 0.777 in [0.698, 0.850]
(n=25); SUNAMT_ANTISUN mean 0.607 in [0.518, 0.688] (n=23);
COVERAGE_BASEALPHA 0.1250. Phase 2 grid over (GW, GC); frozen choice
(0.15, 0.20) is one of four all-pass grid points and maximizes the
minimum bar margin (KB3 3.3x, KB7-bigfrac 1.26x, KB4 2.2x, KB11 3.8x).
Predictions at (0.15, 0.20): KB3 sunmean 9.87, antimean -6.12, diff
15.99; KB4 variance 86.10; KB7 fsmean +0.18, bigfrac 0.2777; KB11
max|dL| 15.91; KB2 0.1250; KB10 range 0.349, argmax x = 320; KB5 0.00
by construction; KB6 0.00 by construction; KB8 passes (smooth field,
no hash/RNG); KB9 passes (0 new fbm evals, ~12 flops per sky pixel);
KB1 passes (pure functions of pixel coordinates). Calculator limits
documented: assumes 100% keep (prior lanes measured 48/48 SKYWIN,
144/144 FULLSKY); ignores dither and byte truncation (plus/minus 1,
averages out); ignores star pixels (faint additive); does not model
terrain/moon call sites (KB5/KB6 are construction, measured on real
renders). The bars decide on real renders.

## Provenance header (planned, machine-checkable, for JUDGE_BRIEF.md)

RENDER_SHA: <sha256 of the H3 variant BMP, filled at render time>
FIRST_RENDERED_WAVE: wave-20261002-0221pdt
COMPONENT_LINEAGE: H1 LIT CLOUD DECK (wave-20261001-1721pdt):JUDGED-DISCARDED; H1v2 TRANSPORT-ANCHORED LIT CLOUD DECK (wave-20261001-2021pdt):BUILD-FAIL (KB3, KB9); H2v1 FORWARD-SCATTER DECK FIELD (wave-20261001-2321pdt):UNJUDGED-OPEN (verdict never recorded; lane read-only analysis: KB3 PASS on renders, KB5 1.03 near-miss via terrain ambient leak, KB1 indeterminate); baseline cirrus block (r11_alien.zag):inherited substrate; R33_NATIVE_IO_V1.zag (wave-20260924-1121pdt):inherited IO substrate; R9:QUEUED-UNJUDGED; C1:QUEUED-UNJUDGED; C2v3:QUEUED-UNJUDGED; S11-IMG:QUEUED-UNJUDGED; C12:QUEUED-UNJUDGED; S13:QUEUED-UNJUDGED; S14:QUEUED-UNJUDGED; whirlpool-planform:QUEUED-UNJUDGED; G1:STOOD-DOWN; DP-1:HELD; E3:REJECTED-BY-JUDGE
NEW_KNOWLEDGE_CLAIM: <one sentence, filled at verdict time; draft: A sun-anchored luminance gradient extended through the clear-sky dome (not the cloud deck) moves sky half-means at zero new fbm cost while leaving terrain and moon byte-identical by construction.>
Tag: [NEW]. This is not a re-certification of H1, H1v2, or H2v1.
Discarded and open candidates are listed only as lineage so the judge
queue stays honest.

## Levers considered and rejected (why this is the one)

- H2v1 FSDF repair (fixing its KB5 ambient leak): rejected; a repair
  of another candidate's leak is not a new mechanism; the standing
  rule demands structural difference.
- Any further cirrus-block lighting change: rejected; three waves
  attacked the cloud deck and the read-only H2v1 analysis shows
  deck-scale fields work there; the untried layer is the dome.
- Chromatic (warm/cool) dome shift: rejected in favor of achromatic
  luminance; chromatic risks hue weirdness under KB11 and the eye.
- Sun-disc/glow changes: rejected; the sun is the scene's honesty
  anchor, never a tuning knob.
- Below-horizon sky gradient: gated out (dy >= 0.0); below-horizon
  pixels are unmeasured and unseen; minimal blast radius.
- Terrain atmospheric perspective / valley haze: real lever, but
  KB5 (frozen, unchanged strictness) forbids terrain changes; held
  for a future terrain-owning prereg, not this wave.
- Cloud shadows on terrain: same KB5 conflict; not this wave.
- Star-field changes: the trace-integrity correction already found
  the stars over-populated off-zenith; not a realism lever.
- Film grain / micro-grain: E3 rejected by Micah's eyes 2026-09-23.
  KB8 hard-codes that verdict. Never again.
- Water specular glitter: r11 has no water body; scene change, not
  a mechanism on the frozen baseline.
- Depth-of-field camera: camera change, risks the crispness judges
  reward; not a world mechanism.
- New scene renderer: out of scope for a single-wave lever; the
  clean A/B needs the frozen r11 baseline.
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
  prereg is committed alone (with NAMECHECK.md, h3/design_calc.zag,
  and h3/evidence/calc output); implementation begins only after that
  commit.
- Red-team: any dropout, flicker, artifact, or weirdness in the
  renders gets a knowledge-vs-architecture investigation (data gap in
  the density field or substrate flaw), documented in
  REDTEAM_ARTIFACTS.md before any verdict line. KB11 is the machine
  half of this rule; the documented investigation is the other half.

## Verdict: PROCEED (to commit)

H3 SUN-ANCHORED SKY-DOME LUMINANCE GRADIENT is a new candidate: the
first attempt to operate on the clear-sky dome itself rather than the
cloud deck, derived per pixel from the frozen sun vector, achromatic,
at zero new fbm cost, with the terrain leak eliminated by
construction. Frozen bars: KB3 unchanged in strictness, KB9 at 2.0x
with 0 new fbm evals expected, KB10 redefined as ANCDOME for the new
mechanism, KB2 recomputed from the verbatim baseline alpha, KB5/KB6
expected 0.00 by construction, KB11 dropout at 0.0 plus the mandatory
documented red-team investigation, determinism 3/3. Draft ends here;
this prereg is committed alone; implementation begins only after that
commit.
