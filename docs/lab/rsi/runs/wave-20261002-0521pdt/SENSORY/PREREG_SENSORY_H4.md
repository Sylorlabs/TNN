# PREREG SENSORY-H4 - frozen preregistration, committed BEFORE any H4 code exists

Wave: wave-20261002-0521pdt. Slot: sensory big-lever (image).
Branch: tnn-native-lab. Working copy: ~/workspace/tnn-rsi.
Lane dir: docs/lab/rsi/runs/wave-20261002-0521pdt/SENSORY/
Frozen: 2026-10-02. Status: PREREG ONLY. No H4 generator, verifier,
or render exists. Implementation begins only after this file is
committed alone (with NAMECHECK.md already committed). UNVERIFIABLE
ORDERING voids the prereg.

## Candidate: H4 CLOUD SHADOWS ON TERRAIN (CSHTERRAIN) [NEW]

## What the prior waves established (re-derived background, frozen)

H1 LIT CLOUD DECK (wave-20261001-1721pdt) DISCARDED on KB3 (diff -2.13
vs >= 6.0, wrong sign). H1v2 TRANSPORT-ANCHORED LIT CLOUD DECK
(wave-20261001-2021pdt) BUILD-FAIL on KB3 (sun +0.64 vs >= 3.0) and KB9
(2.36x vs <= 2.0x). H2v1 FORWARD-SCATTER DECK FIELD
(wave-20261001-2321pdt) UNJUDGED-OPEN (no verdict recorded; read-only
analysis: KB3 PASS on renders, KB5 1.03 near-miss via terrain ambient
leak). H3 SUN-ANCHORED SKY-DOME LUMINANCE GRADIENT
(wave-20261002-0221pdt) UNJUDGED-OPEN (implemented, smoke renders
exist, no verdict recorded, no sealed pair prepared).

All four operated on the SKY (cirrus block or dome). NONE touched the
terrain light-transport path. The H3 prereg explicitly held "cloud
shadows on terrain" as a real lever blocked only by H3's own KB5
terrain non-regression bar. This prereg OWNS terrain: its bars permit
terrain changes and forbid sky/moon changes instead.

The missing path, verified in source
(docs/lab/rsi/runs/wave-20261002-0221pdt/SENSORY/h3/r11_baseline.zag):
b_shadow marches the sun ray testing ONLY b_sdfc (terrain SDF). The
cirrus field is never tested along the sun path. Clouds therefore
cast no shadows: a terrain point under a visible cloud gets full
direct sun. This is a real missing light-transport path, not a tuning
knob, and it is the largest unbuilt realism lever in the frame
(cloud-ground light coherence is a first-order photo-vs-CG cue).

## The new mechanism (frozen definition)

Sun-anchored cirrus shadows on terrain, sampled camera-relative so
each shadow aligns with the cloud the viewer sees.

Two new pure functions (f64, deterministic, zero RNG), inserted before
b_tshade:

```
// H4: cirrus density for a view direction, using the IDENTICAL field
// math as b_sky's cirrus block (seeds 601/602, same warp, same gates).
// Returns 0..1. b_sky itself is untouched.
fn b_cirrus_d(dx:f64, dy:f64, dz:f64) f64 {
    if (dy <= 0.02) { return 0.0; }
    let px:f64 = dx / (dy + 0.18) * 1.4;
    let pz:f64 = dz / (dy + 0.18) * 1.4;
    let wx:f64 = b_fbm2(px * 1.1 + 3.7, pz * 1.1 + 9.2, 601, 3);
    let cm:f64 = b_fbm2(px * 2.2 + (wx - 0.5) * 1.2, pz * 4.5, 602, 3);
    let d:f64 = b_ss((cm - 0.56) / 0.16) * b_ss((dy - 0.02) / 0.15);
    return d;
}

// H4: cloud shadow factor for a terrain point. Marches the SUN ray
// through 3 fixed heights; at each, takes the view direction from
// the CAMERA (coy = 45.0, the frozen b_render camera height) to the
// sample point and reads the cirrus density there. The shadow a
// viewer sees at P therefore corresponds to the cloud the viewer sees
// above P. Returns 0..1 attenuation for the DIRECT SUN term only.
fn b_cshadow(px:f64, py:f64, pz:f64, camx:f64, camz:f64) f64 {
    let sx:f64 = b_sunx();
    let sy:f64 = b_suny();
    let sz:f64 = b_sunz();
    let acc:f64 = 0.0;
    let i:i64 = 0;
    while (i < 3) {
        let H:f64 = 250.0 + (i as f64) * 100.0;
        let t:f64 = (H - py) / sy;
        if (t > 0.0) {
            let qx:f64 = px + sx * t;
            let qz:f64 = pz + sz * t;
            let dx:f64 = qx - camx;
            let dy:f64 = H - 45.0;
            let dz:f64 = qz - camz;
            let dl:f64 = b_sqrt(dx * dx + dy * dy + dz * dz);
            if (dl > 0.0001) {
                acc = acc + b_cirrus_d(dx / dl, dy / dl, dz / dl);
            }
        }
        i = i + 1;
    }
    let csh:f64 = 1.0 - 0.45 * (acc / 3.0);
    if (csh < 0.0) { csh = 0.0; }
    if (csh > 1.0) { csh = 1.0; }
    return csh;
}
```

Frozen constants: heights {250.0, 350.0, 450.0}, 3 samples,
max attenuation 0.45, camera height 45.0 (== b_render coy, frozen).

Frozen call-site change, inside b_tshade, immediately after the
`let sh = b_shadow(...)` line:
```
    let csh:f64 = b_cshadow(px, py, pz, camx, camz);
```
and the three direct-sun lines
```
    let lr:f64 = ar * 1.0 * dif * sh * 1.35;
    let lg:f64 = ag * 0.66 * dif * sh * 1.35;
    let lb:f64 = ab * 0.42 * dif * sh * 1.35;
```
become
```
    let lr:f64 = ar * 1.0 * dif * sh * csh * 1.35;
    let lg:f64 = ag * 0.66 * dif * sh * csh * 1.35;
    let lb:f64 = ab * 0.42 * dif * sh * csh * 1.35;
```
Nothing else in b_tshade changes: ambient (askr/askg/askb), glint,
aerial perspective, dust, and the sky/moon paths are untouched. The
cirrus block in b_sky is byte-identical (density is re-derived from
the same field math, not moved).

Why this is a new mechanism: no prior candidate modified b_tshade,
b_shadow's callers, or any terrain light path. H1/H1v2/H2v1 replaced
cirrus lighting; H3 graded the dome. H4 adds a previously absent
occluder test to the sun path.

Diff contract (machine-checked): h4_terrain.zag vs r11_baseline.zag
differs in exactly: the two added functions above (verbatim modulo
whitespace) and the four changed lines in b_tshade (one added call,
three multiplied lines). Any other delta is a prereg violation.

## Baseline (frozen)

- Source: docs/lab/rsi/runs/wave-20261002-0221pdt/SENSORY/h3/r11_baseline.zag
  (the committed r11, itself a one-line-import copy of
  docs/lab/imagination_discovery/img/r11_alien.zag), copied byte-identical
  to SENSORY/h4/r11_baseline.zag with only the @import line repointed
  at ./sub/R33_NATIVE_IO_V1.zag (diff-verified: exactly one line).
- IO substrate: the vendored h3/sub/R33_NATIVE_IO_V1.zag copied
  byte-identical to SENSORY/h4/sub/R33_NATIVE_IO_V1.zag (hash verified).
- Toolchain: the pinned znc at
  src/tools/toolchain/znc_linux_x86_64_abed8aa1 (same binary the H3
  lane used).
- Baseline gate: (a) the one-line diff verifies; (b) two 1024 baseline
  renders are byte-identical. If either fails, the wave stops and files
  a dated pre-change addendum; no baseline substitution.
- Reference size 1024x1024. A 256 smoke render times the pipeline
  first; the sealed pair uses 1024.

## Frozen point sets (verifier h4_verify.zag, pure Zag, on final BMPs)

Inherited from the H3 prereg verbatim (same cloud-deck fixture, same
formulas, same keep-count asserts): SKYWIN (48, keep >= 36), SUNHALF /
ANTISUN (>= 12 each), TERRAIN (64, keep >= 56), MOON (16, keep >= 12),
FULLSKY (144, keep >= 100), ACU. Luma L = (299R + 587G + 114B) / 1000
on BMP bytes. dL = L_variant - L_baseline. The verifier copies the
baseline world model verbatim (camera basis, b_trace, b_moonhit) to
classify pixels, and re-implements the FROZEN b_cshadow math verbatim
to recompute csh_expected per kept TERRAIN pixel (white-box check).

Geometric validator: keep-count asserts run FIRST on the rebuilt
baseline. Any failure DISCARDS the candidate (G1-v1 precedent); no
set is re-aimed, no bar tuned.

## Frozen kill bars

- H4-KB1-DET: 3 renders of the H4 variant at 1024, sha256 identical
  across all 3. Else FAIL.
- H4-KB2-SKY-NONREG: mean |dL| over kept SKYWIN <= 1.0. The mechanism
  touches only b_tshade's direct term; any sky change is a
  construction violation: FAIL.
- H4-KB3-MOON-NONREG: mean |dL| over kept MOON <= 1.0. Same rule.
- H4-KB4-SHADOW-EXISTS: fraction of kept TERRAIN with
  csh_expected < 0.97 in [0.03, 0.60]. Shadows must exist (lower
  bound) without blanketing the terrain (upper bound).
- H4-KB5-DARKEN-TRACKS: Pearson correlation between measured dL and
  (csh_expected - 1.0) over kept TERRAIN > 0.60. The darkening must
  track the recomputed shadow field (white-box causality); a
  decorrelated darkening is a bug, not a shadow: FAIL.
- H4-KB6-BOUNDED: mean(dL) over kept TERRAIN in [-25.0, -0.5]
  (shadows only darken, bounded), AND fraction of kept TERRAIN with
  |dL| > 60 equals 0.0 (no blowout/dropout).
- H4-KB7-COST: variant 1024 wall time <= 2.5x baseline 1024 wall time
  (matched-contention pairing), and extra fbm octave-evals per
  terrain pixel reported (expected 18: 3 samples x 2 fbm2 x 3
  octaves; 0 on sky pixels).
- H4-KB8-ANTIGRAIN (honors the E3 rejection): acutance ratio
  variant/baseline over ACU <= 1.15.
- VKB-EYE: a sealed blind A/B pair (baseline vs H4 variant, 1024 PNG)
  is prepared for Micah ONLY if every frozen bar passes. Randomized,
  mapping sealed in SEALED_MAPPING.md. He is the sole judge. Nothing
  is adopted on metrics alone: a PASSing candidate is READY-FOR-JUDGE
  only.

## Frozen predictions

- H4-KB4: cirrus coverage (H3 KB2) measured 0.1250 of sky points with
  alpha > 0.15; the shadow field uses the same density gates, so the
  terrain shadow fraction is predicted in [0.05, 0.30].
- H4-KB5: predicted > 0.85 (the renderer and verifier implement the
  same frozen math; residual decorrelation comes only from byte
  truncation and the dither, both +-1).
- H4-KB6: predicted mean(dL) in [-12, -2] (0.45 max attenuation on
  the direct term only; ambient and haze dilute it).
- H4-KB1/KB2/KB3/KB8: pass by construction (pure coordinate
  functions; sky/moon paths untouched; smooth fbm field, no hash).
- H4-KB7: pass (terrain-only cost; sky pixels pay 0).

## Provenance header (for JUDGE_BRIEF.md, machine-checkable)

RENDER_SHA: <sha256 of the H4 variant BMP, filled at render time>
FIRST_RENDERED_WAVE: wave-20261002-0521pdt
COMPONENT_LINEAGE: H1 LIT CLOUD DECK (wave-20261001-1721pdt):JUDGED-DISCARDED; H1v2 TRANSPORT-ANCHORED LIT CLOUD DECK (wave-20261001-2021pdt):BUILD-FAIL (KB3, KB9); H2v1 FORWARD-SCATTER DECK FIELD (wave-20261001-2321pdt):UNJUDGED-OPEN (no verdict recorded); H3 SUN-ANCHORED SKY-DOME LUMINANCE GRADIENT (wave-20261002-0221pdt):UNJUDGED-OPEN (implemented, smoke renders only, no verdict recorded); baseline r11_alien.zag (imagination_discovery/img):inherited substrate; b_sky cirrus block (r11):inherited field math (re-derived, not moved); R33_NATIVE_IO_V1.zag (wave-20260924-1121pdt):inherited IO substrate; R9:QUEUED-UNJUDGED; C1:QUEUED-UNJUDGED; C2v3:QUEUED-UNJUDGED; S11-IMG:QUEUED-UNJUDGED; C12:QUEUED-UNJUDGED; S13:QUEUED-UNJUDGED; S14:QUEUED-UNJUDGED; whirlpool-planform:QUEUED-UNJUDGED; G1:STOOD-DOWN; DP-1:HELD; E3:REJECTED-BY-JUDGE
NEW_KNOWLEDGE_CLAIM: <one sentence, filled at verdict time; draft: Testing the cirrus density field along the sun path darkens terrain under visible clouds with a shadow field that tracks the recomputed occluder, adding the scene's missing cloud-ground light coherence at terrain-only cost.>
Tag: [NEW]. Not a re-certification of H1, H1v2, H2v1, or H3.

## Levers considered and rejected

- Cirrus-block relighting (H1/H1v2/H2v1 family): three waves tried;
  rejected as re-litigation.
- Sky-dome grading (H3 family): the 0221pdt lane owns it; rejected as
  another candidate's mechanism.
- Chromatic cloud tinting: hue risk under blowout bars; rejected.
- Sun disc/glow changes: the sun is the honesty anchor; never a knob.
- Terrain albedo/texture detail: micro-tweak class; not a new
  light path.
- Stronger aerial perspective: exists (b_expneg(t*0.0011)); tuning
  its constant is a parameter tweak, not a mechanism.
- Volumetric god-rays: no participating-medium machinery in the
  trace; would be a new renderer, not a lever.
- Water/specular: no water body in the frozen scene.
- Depth of field: camera change, rejected in the H3 prereg.
- Film grain: E3 rejected by Micah. KB8 hard-codes that verdict.
- Audio: out of this slot (V11 closed, DP-1 HELD).

## Governance

- Pure Zag, literally: generator, verifier, analysis pure Zag with
  the pinned znc. No Python. Any Python touch of a new wave artifact
  voids that wave's evidence on sight.
- Safebin toolchain guard active (NAMECHECK.md Step 0).
- znc quirks honored: no `as *i32` + slice construction; the
  name/layout-dependent _zag_print miscompile (AGENTS.md 2026-10-02)
  avoided via single-buffer cursor emits where printing matters;
  `as []f64` length quirk noted (never trust .len on a cast slice).
- No em-dashes in loop documentation (check_no_dash.sh before commit).
- Commits stay local on tnn-native-lab. Nothing is pushed. This
  prereg is committed ALONE; implementation begins only after that
  commit.
- Red-team: any dropout, flicker, artifact, or weirdness gets a
  knowledge-vs-architecture investigation in REDTEAM_ARTIFACTS.md
  before any verdict line. H4-KB6 is the machine half.
- The skeptic's provenance probe is mandatory in any debate
  transcript before surfacing; surfacing messages quote the
  provenance header verbatim.

## Verdict: PROCEED (to commit)

H4 CLOUD SHADOWS ON TERRAIN is a new candidate: the first mechanism
to test an occluder along the sun path other than the terrain SDF,
camera-relative so shadows align with visible clouds, direct-sun-term
only, sky and moon byte-identical by construction, terrain-owning
bars. Frozen: heights {250,350,450}, 3 samples, 0.45 max attenuation,
bars H4-KB1..KB8 + VKB-EYE. This prereg is committed alone;
implementation begins only after that commit.
