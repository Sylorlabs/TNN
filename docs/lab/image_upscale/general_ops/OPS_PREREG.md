# OPS_PREREG — Crew C: TNN-directed general image operator (`azops.zag`)

Frozen 2026-09-27 before any run. Micah's order: generalize TNN's image
capability — "any image, upscaling, editing" — with operations chosen and
directed by TNN itself, all from learned atoms (no procedural drawing, no
bicubic in any generation path).

## What is built

`src/azops.zag` — the driver. Takes `(indir, outdir, goal-string)`.
TNN's deliberation: parse the goal (keyword hits, recorded) → inspect the
image (dimensions, measured survey energies, edge density, luminance
extrema) → consider candidate operations with reasons → choose ONE →
execute → emit a deliberation TRACE (`OPS_TRACE.txt`, first-person TNN
voice). "TNN involved in its own development."

`src/opgen.zag` — module 1: the MATCHER unit + the UPSCALE-2X unit.
- Matcher-agnostic by design: atom matching is a separable unit behind the
  `m_shapes_match` / `m_thin_match` interface, driven by a `matcher_cfg`
  (`cfg[0]` = discipline id, `cfg[1]` = take bar per value). Discipline 0
  = the current key-SSD best-wins discipline (identical to azgen's).
  Discipline 1 = reserved for the sibling crew's key-ambiguity fix; it
  slots in behind this interface with no driver rewrite.
- UPSCALE-2X = the azgen generation path as a callable unit
  (`op_upscale2x`: survey → affinity order → SHAPES/LINES cascade →
  render at 2x; construction = measured region mean + measured atom
  deviation). Bicubic is REMOVED entirely from the new binary (azgen kept
  it as a scoring baseline; here scoring happens outside the binary).

`src/opfill.zag` — module 2: the EDIT-FILL unit (`op_edit_fill`).
Given an input image and a mask rect (proposed by TNN, see below):
- Tier 1: each masked 8×8 cell's SURROUNDING CONTEXT (unmasked ring of a
  16×16 window centered on the cell) is matched against the S=32 atoms'
  16×16 keys via the matcher discipline (key-SSD, bar 9/value). Fill =
  measured ring mean + learned atom deviation (key recentered on its ring
  mean). Label 7 = CONSTRUCTED-EDIT-FILL.
- Tier 2 (ring has <24 unmasked px): nearest fully-unmasked 8×8 neighbor
  cell matched via `m_shapes_match` at S=16; fill = measured cell-context
  mean + learned atom deviation.
- Tier 3 (degenerate): measured global unmasked mean. Label 8 =
  CONSTRUCTED-EDIT-NOFIT (mean fill, honestly labeled).
- No procedural texture synthesis anywhere.

Mask proposal (TNN-directed, frozen mapping):
- Position words narrow the frame on a 3-col × 2-row zone grid, snapped to
  8px: "left"→col 0, "right"→col 2, "center"/"middle"→col 1 (default full
  width); "top"/"upper"→row 0, "bottom"/"lower"→row 1 (default full height).
  "top left" on 768×512 → rect (0,0,256,256).
- "brightest"/"darkest": measured max/min mean-luminance 16×16 block
  (8px scan step); mask = 48×48 rect centered on it, snapped to 8, clamped.
- No position/brightness words: TNN's own analysis proposes the interior
  64×64 cell (32px step) with max |cell mean lum − global mean lum|.
- Recorded limitation: TNN cannot see objects ("cloud", "tree" are words,
  not vision). When the goal names an object + a location, TNN masks the
  named location and the trace says so; the human judges coverage.

## Demonstration cases (all on real held-out photos)

**Case A — 4× upscale (numbers vs GT).** Fixture: 384×256 crop of the
held-out sky photo at (192,128). Input: 4× box-downscale to 96×64
(documented 2×2 box `(a+b+c+d+2)/4` applied twice — prep only, not
generation). Goal: "upscale it four times". Expected: `out_upscale4x.bmp`
at 384×256 = 2× applied twice (2× of the 2× output), all-learned. Scored
vs the GT crop: PSNR (metrics.py convention, mean of per-channel dB) +
SSIM. No win-claim vs any baseline (there is no baseline in this binary).

**Case B — object removal (eyes only, no dB claim).** Fixture: the full
768×512 held-out sky photo. Goal: "remove the cloud at top left".
Expected: TNN parses edit-intent + "top left" → EDIT-FILL, mask zone
(0,0,256,256) (covers the measured cloud streak at ~(80–240, 40–160)).
Outputs: `out_edit_masked.bmp` (mask visualization, magenta = proposed
mask — a viz aid, not a generation claim), `out_editfill.bmp`,
`editfill_labels.bin`. Judged by human eyes in the gallery: before /
masked / filled.

**Case C — TNN chooses the right op for two goals, same image.**
Fixture: the 96×64 input from Case A. Goal 1: "make it bigger" →
expected UPSCALE-2X (192×128). Goal 2: "remove the brightest spot" →
expected EDIT-FILL with TNN-proposed region (brightest-16×16-centered
48×48 mask). The two OPS_TRACE.txt files must differ sensibly: different
chosen op, different parameters, different recorded reasons.

## Bars (pass/fail, judged from evidence)

1. **Determinism:** every case run twice; all deterministic outputs
   (BMPs, label bins, traces) byte-identical by SHA-256. (Stdout excluded —
   may carry timing.)
2. **4× honesty:** PSNR/SSIM vs GT reported with the numbers; mechanism
   notes where it loses; no baseline invented inside the binary.
3. **Edit-fill integrity:** every filled pixel traces to (measured context
   mean + learned atom deviation) or measured mean; label census shows all
   mask pixels replaced (no untouched original pixels inside the rect);
   trace records per-cell tier/atom/gain decisions.
4. **Op-choice 2/2:** Case C goal 1 → UPSCALE-2X, goal 2 → EDIT-FILL, with
   traces that differ in op, params, and reasons.
5. **Stay-learned:** grep audit of the three sources for banned patterns
   (`bicubic`, `sin(`, `cos(`, `noise`, `rand`) returns nothing in a
   generation path; construction sites all read `measured … + … atom`.
6. **Matcher-agnostic:** the matcher cfg + `m_*` interface documented;
   driver never calls atom-matching internals directly.

## Known limitations (stated up front)

- The shared cross-image vocabulary is the same one whose honest result
  (HONEST_RESULT.md) showed key-ambiguity hallucinations: fills and 4×
  constructions may stamp scene-wrong textures. Expected; reported, not
  hidden.
- TNN has no object vision: mask placement from goal words is positional,
  not object-aware (recorded in every edit trace).
- Disk is at 98%: build in /tmp, delete binaries after; keep fixtures
  minimal (the three case inputs + GT crop).
