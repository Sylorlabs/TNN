# PREREG SENSORY-H5 - frozen preregistration, committed BEFORE any H5 code exists

Wave: wave-20261002-1121pdt. Slot: sensory big-lever (image).
Branch: lane-sensory-20261002-1121pdt. Working copy:
~/workspace/tnn-rsi-work/wave-20261002-1121pdt/sensory/.
Lane dir: docs/lab/rsi/runs/wave-20261002-1121pdt/sensory/.
Frozen: 2026-10-02. Status: PREREG ONLY. No H5 generator, verifier,
or render exists. Implementation begins only after this file is
committed alone (with NAMECHECK.md already committed). UNVERIFIABLE
ORDERING voids the prereg.

## Candidate: H5 PENUMBRA-DILATED CIRRUS SHADOW FIELD (PDSH) [NEW]

## What the prior waves established (re-derived background, frozen)

H1 LIT CLOUD DECK (wave-20261001-1721pdt) DISCARDED on KB3 (diff -2.13
vs >= 6.0, wrong sign). H1v2 TRANSPORT-ANCHORED LIT CLOUD DECK
(wave-20261001-2021pdt) BUILD-FAIL on KB3 (sun +0.64 vs >= 3.0) and KB9
(2.36x vs <= 2.0x). H2v1 FORWARD-SCATTER DECK FIELD
(wave-20261001-2321pdt) UNJUDGED-OPEN (no verdict recorded; KB3 PASS on
renders, KB5 1.03 near-miss via terrain ambient leak). H3 SUN-ANCHORED
SKY-DOME LUMINANCE GRADIENT (wave-20261002-0221pdt) UNJUDGED-OPEN
(implemented, smoke renders exist, no verdict recorded, no sealed pair
prepared). H4 CLOUD SHADOWS ON TERRAIN (wave-20261002-0521pdt)
BUILD-FAIL: the mechanism fired correctly (21,032 bytes darker, all
darkening, terrain-confined, zero sky/moon change, no artifacts) but
the cirrus field was too sparse at the point-sampled sun-ray
crossings: 0.67% of pixels, failing KB4/KB5/KB6.

The failure is named: CIRRUS-FIELD SPARSITY at point-sampled
sun-ray crossings. The sampling math, camera-relative alignment, and
direct-sun-only application were judged SOUND (REDTEAM_ARTIFACTS_H4.md);
the knowledge gap was the field's thinness at the sampled directions.

## The new mechanism (frozen definition)

Penumbra-dilated cirrus shadow field. Physical claim: the sun is an
extended source and clouds have vertical extent, so a cloud casts a
shadow with a finite penumbra; point-sampling a thin field at the
sun-ray crossing underestimates shadow coverage. H5 keeps the
IDENTICAL cirrus field math (b_cirrus_d byte-identical to H4's: seeds
601/602, same warp, same gates) and the IDENTICAL sun-ray march
geometry (same 3 heights, same camera-relative directions, same
0.45 max attenuation), but replaces the point density sample with a
5-tap angular kernel: the density at the crossing is the MAX over the
center direction and 4 taps at frozen angular radius R_P = 0.03 rad in
the camera-relative perpendicular frame (a morphological dilation of
the cloud field). This is a new mechanism (extended-source shadow
capture), not a re-tune: the 0.45 attenuation, the heights, and the
field are untouched; only the capture geometry changes.

Three pure functions (f64, deterministic, zero RNG):

```
// H5: IDENTICAL field math to b_sky's cirrus block (seeds 601/602,
// same warp, same gates). Unchanged from H4.
fn b_cirrus_d(dx:f64, dy:f64, dz:f64) f64 {
    if (dy <= 0.02) { return 0.0; }
    let px:f64 = dx / (dy + 0.18) * 1.4;
    let pz:f64 = dz / (dy + 0.18) * 1.4;
    let wx:f64 = b_fbm2(px * 1.1 + 3.7, pz * 1.1 + 9.2, 601, 3);
    let cm:f64 = b_fbm2(px * 2.2 + (wx - 0.5) * 1.2, pz * 4.5, 602, 3);
    let d:f64 = b_ss((cm - 0.56) / 0.16) * b_ss((dy - 0.02) / 0.15);
    return d;
}

// H5: penumbra-dilated density for a unit view direction.
// Max over 5 taps: center + 4 at angular radius R_P = 0.03 rad in the
// perpendicular frame (right = cross(d, up); up2 = cross(right, d)).
// Degenerate vertical directions use right = (1,0,0). Each tap is
// renormalized before sampling b_cirrus_d.
fn b_cirrus_dp(dx:f64, dy:f64, dz:f64) f64 {
    let rx:f64 = 0.0 - dz;
    let rz:f64 = dx;
    let rl:f64 = b_sqrt(rx * rx + rz * rz);
    if (rl < 0.000001) { rx = 1.0; rz = 0.0; rl = 1.0; }
    rx = rx / rl;
    rz = rz / rl;
    let ux:f64 = 0.0 - rz * dy;
    let uy:f64 = rz * dx - rx * dz;
    let uz:f64 = rx * dy;
    let RP:f64 = 0.03;
    let m:f64 = b_cirrus_d(dx, dy, dz);
    // tap helper: d +/- RP * axis, renormalized, max with m
    // (+right)
    let tx:f64 = dx + RP * rx;
    let ty:f64 = dy;
    let tz:f64 = dz + RP * rz;
    let tl:f64 = b_sqrt(tx * tx + ty * ty + tz * tz);
    let v:f64 = b_cirrus_d(tx / tl, ty / tl, tz / tl);
    if (v > m) { m = v; }
    // (-right)
    tx = dx - RP * rx; ty = dy; tz = dz - RP * rz;
    tl = b_sqrt(tx * tx + ty * ty + tz * tz);
    v = b_cirrus_d(tx / tl, ty / tl, tz / tl);
    if (v > m) { m = v; }
    // (+up2)
    tx = dx + RP * ux; ty = dy + RP * uy; tz = dz + RP * uz;
    tl = b_sqrt(tx * tx + ty * ty + tz * tz);
    v = b_cirrus_d(tx / tl, ty / tl, tz / tl);
    if (v > m) { m = v; }
    // (-up2)
    tx = dx - RP * ux; ty = dy - RP * uy; tz = dz - RP * uz;
    tl = b_sqrt(tx * tx + ty * ty + tz * tz);
    v = b_cirrus_d(tx / tl, ty / tl, tz / tl);
    if (v > m) { m = v; }
    return m;
}

// H5: cloud shadow factor for a terrain point. Identical march to
// H4's b_cshadow (3 fixed heights 250/350/450, camera-relative view
// directions from camera height 45.0), but the density accumulator
// uses b_cirrus_dp (5-tap max) instead of b_cirrus_d. Attenuation
// form unchanged: 1.0 - 0.45 * (acc / 3.0), clamped [0, 1].
fn b_cshadow5(px:f64, py:f64, pz:f64, camx:f64, camz:f64) f64 {
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
                acc = acc + b_cirrus_dp(dx / dl, dy / dl, dz / dl);
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

Frozen call-site change, inside b_tshade, immediately after the
`let sh = b_shadow(...)` line:
```
    let csh:f64 = b_cshadow5(px, py, pz, camx, camz);
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
Nothing else in b_tshade changes: ambient, glint, aerial perspective,
dust, and the sky/moon paths are untouched. The cirrus block in b_sky
is byte-identical (density is re-derived from the same field math,
not moved).

Frozen constants: heights {250.0, 350.0, 450.0}, 3 samples,
max attenuation 0.45, camera height 45.0, R_P = 0.03, 5 taps.

Diff contract (machine-checked): h5_terrain.zag vs r11_baseline.zag
differs in exactly: the three added functions above (verbatim modulo
whitespace) and the four changed lines in b_tshade (one added call,
three multiplied lines). Any other delta is a prereg violation.

## Baseline (frozen)

- Source: the same r11_baseline.zag the H4 wave used (itself a
  one-line-import copy of docs/lab/imagination_discovery/img/r11_alien.zag),
  copied byte-identical to SENSORY/h5/r11_baseline.zag with only the
  @import line repointed at ./sub/R33_NATIVE_IO_V1.zag (diff-verified:
  exactly one line).
- IO substrate: the vendored h3/sub/R33_NATIVE_IO_V1.zag copied
  byte-identical to SENSORY/h5/sub/R33_NATIVE_IO_V1.zag (hash verified).
- Toolchain: the pinned znc at src/tools/toolchain/znc_linux_x86_64_abed8aa1
  (same binary the H3/H4 lanes used).
- Baseline gate: (a) the one-line diff verifies; (b) two 1024 baseline
  renders are byte-identical. If either fails, the wave stops and files
  a dated pre-change addendum; no baseline substitution.
- Reference size 1024x1024. A 256 smoke render times the pipeline
  first; the sealed pair uses 1024.

## Frozen point sets (verifier h5_verify.zag, pure Zag, on final BMPs)

Inherited from the H4 prereg verbatim (same cloud-deck fixture, same
formulas, same keep-count asserts): SKYWIN (48, keep >= 36), SUNHALF /
ANTISUN (>= 12 each), TERRAIN (64, keep >= 56), MOON (16, keep >= 12),
FULLSKY (144, keep >= 100). Luma L = (299R + 587G + 114B) / 1000
on BMP bytes. dL = L_variant - L_baseline. The verifier copies the
baseline world model verbatim (camera basis, b_trace, b_moonhit) to
classify pixels, and re-implements the FROZEN b_cshadow5 + b_cirrus_dp
math verbatim to recompute csh5_expected per kept TERRAIN pixel
(white-box check). It also recomputes csh_center_expected (the H4
point-sample math: b_cirrus_d at the center tap only) per kept
TERRAIN pixel for KB9.

Geometric validator: keep-count asserts run FIRST on the rebuilt
baseline. Any failure DISCARDS the candidate (G1-v1 precedent); no
set is re-aimed, no bar tuned.

## Frozen kill bars

- H5-KB1-DET: 3 renders of the H5 variant at 1024, sha256 identical
  across all 3. Else FAIL.
- H5-KB2-SKY-NONREG: mean |dL| over kept SKYWIN <= 1.0. The mechanism
  touches only b_tshade's direct term; any sky change is a
  construction violation: FAIL.
- H5-KB3-MOON-NONREG: mean |dL| over kept MOON <= 1.0. Same rule.
- H5-KB4-SHADOW-EXISTS: fraction of kept TERRAIN with
  csh5_expected < 0.97 in [0.03, 0.60]. Shadows must exist (lower
  bound) without blanketing the terrain (upper bound).
- H5-KB5-DARKEN-TRACKS: Pearson correlation between measured dL and
  (csh5_expected - 1.0) over kept TERRAIN > 0.60. The darkening must
  track the recomputed shadow field (white-box causality); a
  decorrelated darkening is a bug, not a shadow: FAIL.
- H5-KB6-BOUNDED: mean(dL) over kept TERRAIN in [-25.0, -0.5];
  fraction of kept TERRAIN with |dL| > 60 is 0.0.
- H5-KB7-COST: median H5 variant 1024 wall time <= 2.0x median
  baseline 1024 wall time (same machine). (The 5-tap kernel is ~5x
  the shadow-field portion; H4 measured 0.93x total.)
- H5-KB8-ANTIGRAIN: acutance ratio (variant/baseline) over kept
  SKYWIN <= 1.15.
- H5-KB9-PENUMBRA-SPECIFICITY (mechanism-specific): among kept
  TERRAIN pixels with csh5_expected < 0.97, the fraction with
  csh_center_expected > 0.995 is > 0.50. A majority of the shadows
  must exist ONLY via the penumbra taps: this proves the new
  mechanism did the work. If the shadows would have existed with
  H4's point sampling, H5 is a re-tune, not a new mechanism: FAIL.
- H5-KB10-JUDGE-GATE: ONLY if KB1-KB9 all pass, prepare the sealed
  blind A/B pair (baseline vs H5 variant, order fixed by sorting
  SHA-256 hex, mapping sealed in SEALED_MAPPING.md) plus
  JUDGE_BRIEF.md with the full provenance header (RENDER_SHA,
  FIRST_RENDERED_WAVE, COMPONENT_LINEAGE with JUDGED/QUEUED-UNJUDGED
  status, NEW_KNOWLEDGE_CLAIM one sentence), artifact label NEW.
  Micah judges; no metric-only adoption, ever.

## Red-team plan (knowledge vs architecture)

- T1 construction violation: any sky or moon change (KB2/KB3) is a
  kill; the mechanism is contractually confined to b_tshade's direct
  term.
- T2 structure artifacts: the difference map is inspected for
  banding, grid, scanlines, or block structure. The 5-tap kernel must
  not introduce regular structure; any such artifact kills.
- T3 re-tune signature: KB9 fails but KB4 passes means the penumbra
  taps added nothing; verdict "re-tune, not a new mechanism".
- T4 dropout / weirdness: any validator anomaly (NaN, keep-count
  collapse, dL explosion) gets a knowledge-vs-architecture writeup,
  never silently dropped.
- T5 white-box audit: if KB5 fails while shadows exist, audit the
  verifier's recompute against the renderer's frozen math before any
  verdict; a recompute mismatch is a process bug, not a mechanism
  kill, and is fixed transparently with a dated addendum (the frozen
  mechanism math itself is not changed).

## 10. Queued next (not this wave)

- If KB4 fails on sparsity again: the honest conclusion is that the
  cirrus field as built cannot carry terrain shadows at the frozen
  0.45 depth; the next mechanism question is a sun-side low-slab
  shadow march (different geometry), never an attenuation re-tune.
- If KB1-KB9 pass: sealed judge pair for Micah; then scaling and
  transfer questions per the standing execution rule.

## 11. Amendments

None. Any change to the frozen definition, point sets, or bars after
this commit invalidates the freeze; the experiment would be
re-preregistered, never amended in place.
