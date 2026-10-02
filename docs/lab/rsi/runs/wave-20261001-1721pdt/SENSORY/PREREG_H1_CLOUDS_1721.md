# PREREG H1-CLOUDS-1721 - frozen preregistration, committed BEFORE any H1 code exists

Wave: wave-20261001-1721pdt. Slot: sensory big-lever.
Branch: tnn-native-lab. Working copy: ~/workspace/tnn-rsi.
Lane dir: docs/lab/rsi/runs/wave-20261001-1721pdt/SENSORY/
Frozen: 2026-10-01 17:40 PDT. Status: PREREG ONLY. No H1 generator,
verifier, or render exists. Implementation begins only after this file
is written. Commits are forbidden this wave, so ordering evidence is
file mtime + sha256 recorded in the evidence log: this prereg file
predates every H1 implementation artifact.

## Candidate: H1 LIT CLOUD DECK [NEW]

The r11 champion's sky (ROUND11_VERDICT, 2026-09-26) is an analytic
gradient with a flat fbm cirrus MIX: the cirrus block in b_sky mixes
toward a sun-warmed color with zero light logic. No cloud has a lit
side and a dark side; no edge faces the T1 sun; nothing shadows
anything. In real dusk photographs the cloud deck is the strongest
"this is a photograph" signal in the sky: warm-lit tops and sun-facing
flanks, dark bases, pink dust-glow underlight, silver linings on thin
sun-side edges, self-shadowing across the deck.

H1 replaces the flat cirrus mix with a lit cloud layer: a frozen
density field with real light logic from the frozen T1 sun. This is a
different rendering pathway for the sky's cloud component (analytic
color mix becomes a lit participating layer), global rather than
dab-local, and no wave has ever tried it:

- G1 (1121pdt, 1421pdt) raymarched shafts through a density field that
  was explicitly NEVER rendered as visible cloud, on the r8c dab
  substrate. Both DISCARDED. Not revived here.
- r8c D12/D13 were dab-placed cirrus/haze streaks (micro-levers).
- r11's cirrus is a flat mix: m = fbm mask, color = mix toward warm,
  no shading, no shadow, no underlight. H1 keeps the frozen placement
  language (same projection, same seeds 601/602) and adds the light
  logic the baseline never had.

This honors the standing line directly:
- Big lever, not a micro-lever: per-pixel screen-space cloud layer with
  sun-driven shading, self-shadow march, and underlight. Untouched:
  terrain, moon, sky gradient, stars, dither, vignette.
- Free lunch: perceptual gain at the same cost class (bounded extra
  fbm evals on sky pixels only, no new data structures).
- E3 honored: every new term is fbm-smooth. Zero per-pixel hash, zero
  RNG. KB8 hard-codes the E3 verdict as an acutance ratio bar.
- The mechanism is explicit about what it does not do: it does not
  touch terrain or moon pixels by construction (the sky branch only
  runs when trace < 0 and moonhit < 0).

## Baseline (frozen)

- Source: docs/lab/imagination_discovery/img/r11_alien.zag (in-tree,
  unmodified for the baseline build).
- Toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
  sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
  (verified before use).
- IO substrate: src/tools/toolchain/R33_NATIVE_IO_V1.zag no longer
  exists in-tree; the vendored copy from wave-20260924-1121pdt
  (candidates/g1/sub/R33_NATIVE_IO_V1.zag, sha256
  e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8)
  is copied byte-identical into SENSORY/h1/sub/R33_NATIVE_IO_V1.zag
  (hash re-verified at copy time).
- The baseline is built FIRST: SENSORY/h1/r11_baseline.zag is a byte
  copy of r11_alien.zag with only the @import line repointed at
  ./sub/R33_NATIVE_IO_V1.zag (diff-verified: exactly one line differs).
- Baseline gate (no frozen r11-1024 hash exists on record; stated
  openly): (a) the one-line diff verifies; (b) two 1024 renders are
  byte-identical; (c) the geometric validator keep-count asserts pass
  on the rebuilt baseline. If (a), (b), or (c) fails, the wave stops
  and files a dated pre-change addendum; no baseline substitution.
- Reference size: 1024x1024 (D-RES standard). A 256 smoke render times
  the pipeline first; the sealed pair uses 1024.

## The lever: H1 lit cloud deck (frozen mechanism)

Replaces the "thin cirrus, warm-lit on the sun side" block inside
b_sky (the `if (dy > 0.02)` block), nothing else. All arithmetic is
f64, deterministic, zero RNG. Every constant below is frozen; the
implementation may not tune them against renders.

Frozen sun horizontal (from deliberated T1, matches b_sunamt's frozen
pair, unit length): SXH = -0.628, SZH = -0.778.

New function (pure, deterministic):
```
fn h1_dens(px:f64, pz:f64) f64 {
    let wx:f64 = b_fbm2(px * 1.1 + 3.7, pz * 1.1 + 9.2, 601, 3);
    return b_fbm2(px * 2.2 + (wx - 0.5) * 1.2, pz * 4.5, 602, 3);
}
```

Replacement block (frozen exactly):
```
if (dy > 0.02) {
    let px:f64 = dx / (dy + 0.18) * 1.4;
    let pz:f64 = dz / (dy + 0.18) * 1.4;
    let den:f64 = h1_dens(px, pz);
    let cov:f64 = b_ss((den - 0.52) / 0.14);
    let th:f64 = 0.35 + 0.65 * b_fbm2(px * 3.1 + 11.0, pz * 6.0 + 5.0, 604, 2);
    let hf:f64 = b_ss((dy - 0.02) / 0.15);
    let e:f64 = 0.06;
    let gx:f64 = (h1_dens(px + e, pz) - den) / e;
    let gz:f64 = (h1_dens(px, pz + e) - den) / e;
    let slope:f64 = gx * -0.628 + gz * -0.778;
    let shade:f64 = 0.62 + 1.2 * slope * th;
    if (shade < 0.05) { shade = 0.05; }
    if (shade > 1.35) { shade = 1.35; }
    let s1:f64 = h1_dens(px + -0.628 * 0.10, pz + -0.778 * 0.10);
    let s2:f64 = h1_dens(px + -0.628 * 0.22, pz + -0.778 * 0.22);
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

Reading of the mechanism: coverage from the frozen density field;
thickness from a second frozen fbm; sun-facing flanks brighten via the
density gradient dotted with the frozen sun azimuth; a 2-tap march
toward the sun self-shadows the deck; cloud tops take the warm
sun-side color while bases take the pink dust-glow horizon color at
0.85 (underlight); thin sun-side edges get a silver lining; the layer
composites over the untouched sky gradient by coverage alpha with the
existing height fade.

Data knob (measured, not judged): density/warp octaves are frozen at
3. If a 1024 render completes in under 600 s wall, an H1-OCT5 probe
(density 5 octaves, warp 5 octaves, all else frozen) is measured
against KB2..KB8 and reported as a data-amount observation. It is not
the candidate and never enters the sealed pair.

## Frozen point sets (verifier h1_verify.zag, pure Zag, on final BMPs)

The verifier copies the baseline world model verbatim (camera basis,
b_trace, b_moonhit) to classify pixels. Luma L = (299R + 587G + 114B)
/ 1000 on final BMP bytes. dL = L_variant - L_baseline. All sets at
1024x1024.

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
the rebuilt baseline, before any H1 code is compiled. If any assert
fails, that is a prereg-spec defect and the candidate is DISCARDED
(G1-v1 precedent); no set is re-aimed, no bar is tuned.

## Frozen kill bars

- KB1-DET: 3 renders of the H1 variant at 1024, sha256 identical
  across all 3. Else FAIL.
- KB2-COVERAGE: fraction of kept SKYWIN with cloud alpha a > 0.15
  (a recomputed by the verifier from the frozen field math) in
  [0.08, 0.60]. The mechanism must fire without paving the sky.
- KB3-LIGHTLOGIC: mean(dL over SUNHALF kept) - mean(dL over ANTISUN
  kept) >= 6.0, and mean(dL over SUNHALF kept) >= 3.0. Cloud light
  must obey the T1 sun's direction.
- KB4-STRUCTURE: variance of dL over SKYWIN kept >= 40.0. Lit tops
  and dark bases, not a uniform wash.
- KB5-NONREG-TERRAIN: mean |dL| over TERRAIN kept <= 1.0.
- KB6-NONREG-MOON: mean |dL| over MOON kept <= 1.0.
- KB7-SKYCALM: |mean(dL) over FULLSKY kept| <= 5.0, and fraction of
  FULLSKY kept with |dL| > 12 <= 0.35. No global sky regrade.
- KB8-ANTIGRAIN (honors the E3 rejection): acutance ratio
  variant/baseline over ACU <= 1.15. Clouds are soft structures.
- KB9-COST: variant 1024 wall time <= 4.0x baseline 1024 wall time
  (measured, reported); extra fbm octave-evals per sky pixel reported.
  The free-lunch claim is perceptual gain at the same cost class.
- VKB-EYE: a sealed blind A/B pair (baseline vs H1 variant, 1024 PNG)
  is prepared for Micah. Randomized, mapping sealed. He is the judge.
  Nothing is adopted on metrics alone.

## Frozen predictions (directional)

KB2 passes mid-range (coverage threshold 0.52/0.14 on a ~0.5-mean
field fires on roughly a third of the band). KB3 passes (silver
lining + warm tops fire on the sun side; anti-sun clouds take the dim
dust-glow base). KB4 passes with margin (tops brighten, bases darken,
lining adds edge variance). KB5/KB6 pass at 0.00 by construction (the
sky branch never runs for terrain or moon rays). KB7 passes (alpha is
coverage-gated; clear sky keeps the untouched gradient). KB8 passes
(all new terms are fbm-smooth; no hash anywhere). KB9 passes (extra
work is sky-pixels-only; terrain raymarching dominates frame cost).
KB1 passes (pure functions of pixel coordinates, zero RNG). The risk
is KB3's magnitude if the density gradient saturates the shade clamp;
the 1.2 gain was set from the fbm gradient scale, not from renders.

## Provenance header (planned, machine-checkable, for JUDGE_BRIEF.md)

RENDER_SHA: <sha256 of the H1 variant BMP, filled at render time>
FIRST_RENDERED_WAVE: wave-20261001-1721pdt
COMPONENT_LINEAGE: r11-substrate(champion,ROUND11_VERDICT,committed); R9:QUEUED-UNJUDGED; C1:QUEUED-UNJUDGED; C2v3:QUEUED-UNJUDGED; S11-IMG:QUEUED-UNJUDGED; C12:QUEUED-UNJUDGED; S11-AUD:QUEUED-UNJUDGED; S13:QUEUED-UNJUDGED; S14:QUEUED-UNJUDGED; whirlpool-planform:QUEUED-UNJUDGED; G1:STOOD-DOWN; DP-1:HELD; E3:REJECTED-BY-JUDGE
NEW_KNOWLEDGE_CLAIM: A frozen density field lit by the deliberated sun (sun-facing flank shading, 2-tap self-shadow, dust-glow underlight, silver linings) replaces r11's flat cirrus mix with structured dusk clouds at the same cost class.
Tag: [NEW]. This is not a re-certification. No pending queue item is
re-surfaced or re-presented here; they are listed only as lineage so
the judge queue stays honest.

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

## Governance

- Pure Zag, literally: generator, verifier, analysis, and scratch are
  pure Zag compiled with the frozen toolchain. No Python anywhere.
  Any Python touch of a new wave artifact voids that wave's evidence
  on sight; there is no recovery path this wave.
- znc quirk honored: no `as *i32` + slice construction inside
  functions; u8-backed cells with little-endian pack/unpack helpers.
- No em-dashes in loop documentation (standing style rule).
- Commits stay local on tnn-native-lab. Nothing is pushed. This wave
  forbids commits entirely; ordering evidence is file mtime + sha256.
- Red-team: any dropout, flicker, artifact, or weirdness in the
  renders gets a knowledge-vs-architecture investigation (data gap in
  the density field or substrate flaw), documented before any verdict.

## Verdict: PROCEED

H1 LIT CLOUD DECK is a genuinely new big-lever mechanism: the first
lit cloud layer on any adopted substrate, replacing r11's flat cirrus
mix with sun-driven shading, self-shadow, underlight, and silver
linings. Frozen realism bars his eyes will judge, machine bars that
discriminate lit structure from wash, grain, regrade, and terrain or
moon bleed. Draft ends here; implementation begins only after this
prereg is written.
