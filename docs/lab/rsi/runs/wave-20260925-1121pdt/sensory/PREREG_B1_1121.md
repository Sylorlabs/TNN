# PREREG B1-BOUNCE-1121: frozen preregistration, committed BEFORE any B1 code exists

Wave: wave-20260925-1121pdt. Lane: sensory. Branch: tnn-native-lab.
Working copy: ~/workspace/tnn-rsi.
Lane dir: docs/lab/rsi/runs/wave-20260925-1121pdt/sensory/
Frozen: 2026-09-25 11:45 PDT. Status: PREREG ONLY. No B1 generator,
verifier, or render exists. Implementation is explicitly deferred until
after this prereg is committed. The prereg commit must strictly precede
the first implementation commit (commit-order self-check); a failure
cannot be adopted this wave.

## Candidate: B1 BOUNCE (two-bounce indirect illumination) [NEW]

The single biggest photo-vs-painting tell left in the r8c land tiers is
that shadows are filled with one flat color. Pass 3 of r8c_alien.zag
multiplies land pigment by the shadowed light factor and then adds a
constant cool fill (120,140,190 scaled by shadow depth) everywhere. In
real dusk photographs a shadow is never filled flat: it carries the
color of its surroundings, warm dust glow from below, cool skylight
from above, pooling differently in every concavity. The substrate does
one direct light only. B1 adds the missing second story: spatially
varying indirect illumination computed from the scene's own albedo.

B1 is a new world mechanism, not a dab tweak, not grain, not a relight,
not a local patch:

- It operates on no dab primitive. It is a per-pixel pass over the
  land tiers that recolors existing pigment with arithmetic only.
- It is global: every shadowed land pixel is re-anchored to the color
  of the world around it.
- It is the light-transport counterpart of G1: G1 put a volume in the
  sky; B1 puts interreflection on the ground. G1 stands down (sky
  mechanism, untouched). B1 touches sky pixels never.
- Prior-art grep over docs/lab/rsi/runs (2026-09-25, *.md, cache dirs
  excluded): the tokens bounce, ambient light, color bleed, colour
  bleed, indirect illumination, global illumination, albedo return zero
  hits. No wave has ever proposed, frozen, or tested indirect
  illumination. The incumbent flat fill lives only in the r8c source
  (pass 3 land branch), which B1 supersedes rather than tunes.

This honors the standing line directly:

- Big lever, not a micro-lever: one new pass changes every shadow in
  the frame. The dab micro-lever program (D15/D17/D18/D19) is untouched.
- Free lunch: perceptual gain at the same cost class. One bounded extra
  per-pixel pass plus a 64x64 albedo field; no new data structures
  beyond small integer tables; no new input data.
- E3 honored: the bounce field is band-limited (bilinear from 64x64),
  so no high-frequency static is added anywhere. KB3 measures this.
- Data amount is varied and measured: the frozen default mixes at
  k=384/1024. Evidence reports the metric bars for the frozen default
  and for one alternate k=192 (data-amount trial, evidence only, never
  a queue item). The sealed-pair question does not arise this wave
  (standing rule 6: the judge queue is untouched).

## Baseline (frozen)

- Source: b1/b1_baseline.zag in the lane dir: byte copy of
  docs/lab/imagination_discovery/img/r8c_alien.zag with only the
  @import line repointed at the vendored substrate
  b1/sub/R33_NATIVE_IO_V1.zag (sha256
  e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8,
  pinned equal to the G1 wave's vendored copy).
- Toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1, sha256
  498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
- The baseline was rebuilt BEFORE this prereg was written and renders a
  BMP with sha256
  e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d,
  identical to the committed r8c baseline record, byte-identical across
  two reruns (evidence: b1/evidence/base_r1.bmp, base_r2.bmp). If any
  later rebuild fails to reproduce this hash, the wave stops and files
  a dated pre-change addendum; no baseline substitution is permitted.
- Reference render time T_base: 1.03 s wall (measured 2026-09-25 on this
  VM, two runs: 1.028 s, 0.984 s). KB2 is frozen against this number.

## The lever: B1 bounce (frozen mechanism)

New pass 3b (b1_pass) runs after r8c_pass3, before r8c_pass4
(fixations). Rationale, frozen: bounce is light that has already
touched the world, so it belongs after the direct-light pass; the
fixations then read a canvas whose shadows already carry their
surroundings, the way eyes do.

All arithmetic is integer, per-mille fixed point. Zero RNG anywhere.
Every constant below is frozen; the implementation may not tune them
against renders.

Pre-pass (in main, before r8c_pass3, from the pre-light canvas):

- A0: unlit albedo field, 64x64x3 bytes (12 KiB). Cell (cx,cy) holds
  the mean BGR of its 16x16 pixel block. Box average, integer.

Variant pass 3 (same pixel math as baseline pass 3, unchanged):

- The variant's pass 3 keeps the blurred shadow map shadb (128x128)
  alive and hands it to b1_pass instead of freeing it. No pixel formula
  changes; the direct-light result is identical to baseline by
  construction.

b1_pass (new, frozen):

- For each pixel (x,y) with pass 3's land mask true (in_sky == 0,
  computed exactly as pass 3 computes it, arch opening excluded):
  - Luma gate: skip if luma < 24 (crushed blacks stay crushed; no new
    black-region weirdness).
  - sh = r8c_sample128(shadb, x, y), 0..1024 (the same blurred shadow
    value pass 3 used).
  - below0 = bilinear sample of A0 at (x, min(y+192, h-1)): the ground
    beneath, warm dust bounce.
  - above0 = bilinear sample of A0 at (x, max(y-192, 0)): the air
    above, cool skylight.
  - bounce = (below0 + above0) / 2 per channel: the color of the
    world around the pixel, from its own unlit albedo.
  - mix m = 384 * sh / 1024 / 1024 (k=384 frozen; deep shadow gets the
    full mix, lit pixels get none).
  - pixel = pixel + (bounce - pixel) * m.
- Sky pixels, gas giant, moon, arch opening: untouched.
- No placement primitives are used (D-COMP holds); the change field is
  bilinear-smooth by construction.

Trace: b1_pass writes a PASS 3B block in the program's own trace style
(B1..B8 decisions), and the variant's decision-count line reads 270
(269 + 1). KB7 checks this.

## Frozen kill bars (never moved after this commit)

- KB1 determinism: two variant reruns (frozen k=384) produce
  byte-identical BMPs (sha256 equal). Any mismatch kills the candidate.
- KB2 cost: variant wall time <= 1.5 * T_base = 1.55 s.
- KB3 anti-grain (E3 honored): HF(var) <= 1.02 * HF(base), where HF is
  the sum over all pixels and channels of |p - boxblur3(p)|.
- KB4 effect size, measured by the frozen verifier over land pixels
  with sh > 512:
  - KB4a: mean per-channel |delta| >= 3.5 (units of 8-bit channel).
  - KB4b: at least 25 percent of those pixels have mean |delta| >= 3.5.
  - KB4c: max per-pixel per-channel |delta| <= 80 (no posterization).
- KB5 no flattening, no new crush: std(luma(var)) >= 0.90 *
  std(luma(base)); count of pixels with all channels < 8 does not
  increase vs base.
- KB6 no new edges (D-COMP): max 4-neighbor gradient of the |delta|
  field <= 8 per channel.
- KB7 trace integrity: variant trace contains a PASS 3B block and the
  decision-count line reads 270.

Human-eye/ear protocol: the worker converts base and variant BMPs to
PNG crops (ffmpeg, no Python) and records a visual read in EVIDENCE
(worker eyes only, not a judgment). The final perceptual verdict is
Micah's alone; per standing rule 6 nothing enters his sealed judge
queue this wave even on a full PASS. A full PASS banks B1 as
queue-eligible and held.

Verdict mapping (frozen): ADOPT-as-eligible only on clean PASS of all
seven bars with zero regressions. DISCARD on any bar failure, with the
killing evidence named. PARTIAL is not available: the bars are
conjunctive.

## Consistency check (DF-1 lesson), recorded before implementation

The frozen mechanism and the frozen kill bars are jointly satisfiable;
the check is analytic, per terrain, at k=384, deep shadow (sh=1024):

- Dark umber ground N=(90,70,58): post-pass-3 P=(74,63,60); bounce=N;
  delta=0.375*(16,7,2)=(6.0,2.6,0.8); mean|delta|=3.1. Worst cell.
- Rust hills N=(154,110,86): P=(118,90,79); delta=(13.5,7.5,2.6);
  mean|delta|=7.9.
- Dust breach N=(202,172,142): P=(151,133,117); delta=(19.1,14.6,9.4);
  mean|delta|=14.4.
- Crater rim N=(112,96,132): P=(89,81,111); delta=(8.6,5.6,7.9);
  mean|delta|=7.4.
- Population mean over sh>512 pixels is a mix of these terrains; the
  arch's long shadow falls substantially on dust and plain, so the
  population mean sits well above the 3.1 worst cell. KB4a (>=3.5) and
  KB4b (>=25% of pixels) are satisfiable with margin. KB4c (<=80):
  maximum possible delta is 0.375*(176,156,136)=(66,59,51) for the
  darkest gated pixel against the brightest plausible A0 neighborhood;
  80 bounds it with margin.
- KB1: all functions are pure integer maps of frozen constants; no RNG,
  no clock, no input. Byte-identical reruns follow by construction.
- KB2: the variant adds one 1M-pixel read loop (A0 build) and one 1M
  per-pixel loop with bilinear samples (no shadow-map recompute; the
  variant pass 3 hands shadb over). Estimated +0.2..0.3 s on top of
  1.03 s; the 1.55 s bar has margin.
- KB3: the bounce field is bilinear from 64x64, so its spatial
  frequencies sit far below the 3x3 HF probe; the ratio stays ~1.00.
- KB5: only shadowed pixels move, and only partway (<=38%) toward
  their neighborhood mean; global luma std cannot drop 10%.
- KB6: the |delta| field is sh/1024 (blurred, bilinear) times a smooth
  color difference; per-pixel gradient <= ~1 unit, far under 8.
- KB7: the variant writes its own trace; the check is textual.

No bar contradicts another: KB4 wants visible movement (satisfied in
shadow populations), KB5/KB6/KB3 cap it (satisfied by the 384 mix and
the smooth field). The DF-1 failure mode (bars jointly unsatisfiable)
does not apply.

## Data-amount trial (evidence only)

One alternate variant with k=192 (half the frozen mix) is built and
measured with the same verifier, to show how the effect scales with
the data knob. It is not a candidate, never a queue item, and its bars
are reported for context only.

## Commit order

1. This prereg commits ALONE (git add of this file only).
2. Implementation (b1_bounce.zag, b1_k192.zag, b1_verify.zag,
   run_b1.sh, renders) commits only after.
3. A sibling red-team worker reviews the committed evidence afterward;
   everything needed for the verdict is committed and citable.
