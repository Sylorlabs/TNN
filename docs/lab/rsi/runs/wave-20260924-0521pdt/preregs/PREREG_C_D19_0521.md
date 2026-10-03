# PREREG C-D19 - frozen preregistration, committed BEFORE any D19 code exists

Wave: wave-20260924-0521pdt. Worker: C (free-lunch slot).
Branch: tnn-native-lab. Working copy: ~/workspace/tnn-rsi.
Run dir: docs/lab/rsi/runs/wave-20260924-0521pdt/freelunch/
Frozen: 2026-09-24 05:50 PDT. Status: PREREG ONLY. No D19 generator,
verifier, or render exists. Implementation is explicitly deferred until
after this commit.

## Candidate slot and why it is the strongest free lunch

D19 FOCUS-PLANE DETAIL on the r8c Fork C substrate. The standing
sensory-headspace line hunts free lunches: perceptual-quality gains at
the same or lower cost, with big realism levers, after Micah rejected
E3 film grain in a blind A/B. The single biggest photo-vs-painting tell
left in the r8c renders is uniform softness: no focus plane, no fine
detail anywhere, so the image reads as a digital painting. D19 adds
structured fine detail (crack accents and sunlit edge ticks) at the
frozen focal point and on the foreground stones and arch, with density
falling off the focus plane. This is depth of field as a world
mechanism, not a filter.

It is also a fulfillment, not an invention: frozen world decision D14
already states "my eye lands on the lit shoulder of the great peak, at
(430,400). Detail will gather there." The current renderer never
delivers that detail. D19 delivers it. Cost is a fixed budget of 208
small dabs, same cost class as the existing pass-4 fixations: a free
lunch if the bars pass.

This is not a micro-grain tweak (Micah's E3 rejection is honored by an
explicit anti-grain kill bar, KB4) and not a local patch on the gas
giant (D15/D17/D18 territory). It is the first candidate to address
sharpness and focus as a global mechanism.

## Baseline (frozen)

- Source: docs/lab/imagination_discovery/img/r8c_alien.zag (in-tree,
  unmodified for the baseline build).
- Toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
  sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef.
- IO substrate: Linux-ported raw-syscall R33_NATIVE_IO_V1.zag (blob
  from wave commit 72ef158fc), vendored inside the wave run dir; the
  in-tree docs/lab/toolchain/ copy is absent from this working copy,
  so the vendored copy keeps the wave self-contained.
- The rebuild was verified BEFORE this prereg was written: a byte copy
  of r8c_alien.zag with only the @import line repointed at the vendored
  substrate renders a BMP with
  sha256 e4f6555700ad6983e323177573ea66cb0a16c5d121a7b32a34fff5735afecb0d,
  identical to the committed r8c baseline (S14 record). Render time
  about 1 s at 1024x1024. If the wave rebuild ever fails to reproduce
  this hash, the wave stops and files a dated pre-change addendum; no
  baseline substitution is permitted.

## The lever: D19 focus-plane detail (frozen mechanism)

Slot: after r8c_pass3 (light logic), before r8c_pass4 (fixations), the
same slot D15/D17/D18 used, so the fixations may respond to the detail
the way eyes would. Only the r8c_dab pigment primitive is used
(D-COMP holds: no axis-aligned primitive calls, no banned names).
Zero RNG anywhere: every position derives from r8c_h01 integer hashes
with frozen seeds. Colors are (r,g,b) triples, alpha 0..1024.

F1 - sailstone detail, 120 dabs. For stone i in 0..39, with
sx = r8c_stone_x(i), sy = r8c_stone_y(i), sr = r8c_stone_r(i):
- crack1: center (sx + ox1, sy - sr/2 + oy1), rad 3, (48,40,34),
  alpha 220, where ox1 = h01(i,201,9121)*sr/512 - sr/2 and
  oy1 = h01(i,202,9122)*sr/512 - sr/2.
- crack2: center (sx + ox2, sy + oy2), rad 2, (58,48,40),
  alpha 200, where ox2 = h01(i,203,9123)*sr/512 - sr/2 and
  oy2 = h01(i,204,9124)*sr/512 - sr/2.
- sunlit edge tick: center (sx - sr + 1, sy - sr/2), rad 2,
  (235,190,150), alpha 240. The sun sits low left, so the lit edge
  is the left edge, matching D9's warm rims.

F2 - arch detail, 48 dabs:
- 24 dark ticks down the left pillar edge: k in 0..23,
  px = 257 + (k % 3), py = 790 + k*4, rad 3, (40,32,26), alpha 210.
  All 24 points lie inside r8c_arch_body by construction
  (x 257..259 within 256..288, y 790..882 within 786..900).
- 24 bright ticks along the lintel top edge: k in 0..23,
  px = 252 + k*5, py = 764 + (k % 2), rad 2, (245,205,165),
  alpha 230. x 252..367 within 248..392, y 764..765 within 762..802.

F3 - focal cluster, 40 dabs, the D14 promise. k in 0..39:
dx = h01(k,207,9127)*120/1024 - 60, dy = h01(k,208,9128)*80/1024 - 40,
px = 430 + dx, py = 400 + dy. Even k: rad 2, (70,58,48), alpha 200.
Odd k: rad 3, (225,185,145), alpha 180. The cluster sits on the lit
peak shoulder (ridge_y near x=430 is about 283..363, so y 360..440 is
far-rim tier, tier 1).

Total: exactly 208 dabs. The binary prints "D19 dabs: 208" and aborts
nonzero if the counter differs. D19 writes its decision lines to the
elaboration trace like the other D-decisions.

## Metrics (measured by s19_verify.zag, pure Zag, on final BMPs)

Luma L = (299R + 587G + 114B) / 1000. Acutance
A(x,y) = |L(x,y)-L(x-2,y)| + |L(x,y)-L(x+2,y)| + |L(x,y)-L(x,y-2)|
+ |L(x,y)-L(x,y+2)|. The 2px step sees past the per-pixel pass-5
grain. Ratios are variant mean / baseline mean over the frozen point
sets. All point sets are frozen here, before any render exists.

- KB1-DET: 3 variant renders, sha256 identical across all 3. Else FAIL.
- KB2-FOCUS: acutance at the 40 F3 cluster centers (recomputed in the
  verifier with the frozen hash formulas above). Ratio >= 1.30.
- KB3-STONE: acutance at the 40 crack1 centers plus the 40 sunlit edge
  tick positions (80 points, frozen formulas). Ratio >= 1.20.
- KB4-SKY (anti-grain guard, honors the E3 rejection): acutance at 12
  frozen sky points (80+72k, 60+15*(k%4)) for k in 0..11, all with
  tier_at == 0 by construction. Ratio <= 1.10. D19 paints no sky dabs;
  any uniform high-frequency lift fails the candidate.
- KB5-NONREG: mean |L_variant - L_baseline| over all 1048576 pixels
  <= 8.0. The change must stay local, not a global regrade.
- KB6-COST: program-asserted D19 dab count == 208, and variant render
  wall time <= 1.25x baseline wall time (measured, reported). The free
  lunch claim is perceptual gain at the same cost class.
- VKB-EYE: a sealed blind A/B pair (baseline vs variant) is prepared
  for Micah. He is the judge. Nothing is adopted on metrics alone.

## Frozen predictions (directional)

KB1 passes (the pipeline is deterministic; the baseline rebuild
already reproduced byte-identically). KB2 passes strongly (the focal
cluster is dense over its sample points). KB3 passes moderately (80
points, small radii). KB4 holds near 1.00 (no sky dabs exist). KB5
lands small, a few luma levels (about 10k of 1M pixels touched).
KB6 holds exactly (fixed dab budget; render dominated by per-pixel
passes). VKB-EYE is prepared regardless of metric margins.

## Cost

208 dabs against a baseline that paints thousands across five passes.
Render-time delta is expected under 2 percent. No new passes, no new
buffers, no RNG, no Python, no network, no new dependencies.

## Red-team confounds to attack

1. Detail is disguised grain (Micah rejected grain): KB4 plus
   structured placement (accents sit on stone edges, arch edges, and
   the focal shoulder; dark/light pairs follow the sun side) plus a
   human eye review of a 256px crop at 1x in the evidence.
2. Sharpening halos: radii are 2..3 px with moderate alpha; the
   red-team checks the crop for light fringes around dark accents.
3. Metric gaming by point selection: every sample point is frozen
   above, derived from the frozen hash formulas or fixed sky
   coordinates, not chosen after seeing renders.
4. Baseline mismatch: the wave rebuild must reproduce e4f65557...;
   any mismatch voids the wave (pre-change addendum, no silent swap).
5. Program-level critique (another dab iteration on the r8c
   substrate): disclosed. Defense: D19 is a global focus/depth-of-field
   mechanism that fulfills frozen D14 and attacks the sharpest
   painting-vs-photo tell; no prior candidate touched focus. The
   verdict will carry this critique either way.
6. Knowledge-vs-architecture: the gain must come from the D19
   mechanism, not from the verifier knowing the dab positions. The
   verifier recomputing positions is measurement, not signal; the
   blind pair given to Micah carries no position information.

## Verdict mapping

- ADOPT (as READY-FOR-JUDGE): KB1..KB6 all PASS, sealed pair prepared
  and committed, red-team crop review shows no halos or grain-like
  spread. Final adoption is Micah's blind verdict only; this wave
  claims metric success, never aesthetic success.
- DISCARD: any of KB1..KB6 FAILs, with the killing number cited.
  A KB4 fail (sky acutance lift) kills on the E3 line even if KB2/KB3
  pass: grain by another name is still grain.
- PARTIAL: KB2 and KB3 pass but KB5 is marginal (8.0..12.0), or the
  crop review finds mild fringing: narrow by cutting F3 alpha 180->140
  and F1 alpha 220->170, re-render, re-run all bars under a dated
  addendum. One narrowing only; a second miss is DISCARD.

## Commit-order statement

This prereg is committed alone, before any D19 implementation file
exists in the run dir. The implementation commit will strictly follow
this commit. No Python touches any wave artifact at any point; any
such touch voids the wave evidence on sight.

## Sealed blind A/B governance

If the bars pass: two 1024x1024 24-bit BMPs, baseline (rebuilt r8c,
sha256 e4f65557...) vs variant (r8c + D19), copied under
freelunch/d19_blind/ with randomized non-descriptive names
(pair_<8 hex of file sha256>.bmp), mapping sealed in
SEALED_MAPPING_D19.md (the only place recording which is which; never
copied into evidence, briefs, or commit messages), plus
JUDGE_BRIEF.md carrying the machine-checkable provenance header:
RENDER_SHA for both files, FIRST_RENDERED_WAVE wave-20260924-0521pdt,
COMPONENT_LINEAGE (D19 new this wave; r8c substrate from 2026-09-22;
D15/R9, D17/S13, D18/S14 are QUEUED-UNJUDGED and none are stacked into
this variant), NEW_KNOWLEDGE_CLAIM in one sentence. Provenance honesty:
the renders are new this wave; no recycled render is presented as a
fresh judgment; the baseline is the plain r8c rebuild, not any
unjudged variant (S11 precedent).

Pure Zag only. No Python anywhere: not in the generator, verifier,
runner, or analysis. Static grep verification (no rand, random, srand,
time, clock in new sources) is part of the evidence.
