# SEE-ITS-RESULT LOOP — Verification Report

Date: 2026-09-27 (overnight). Verifier: A5 see-its-result line.
Micah's law: **"no blind imagining — TNN renders, looks at its own result
with its own eyes, deliberates on what it sees, and re-renders."**
He had to re-issue this law because fork briefs weren't carrying it.
This report verifies, line by line, whether each imagination/generation
line actually closes the loop — or imagines blind.

## The four-stage test

For each line: (a) is there a render step? (b) does TNN's own machinery
OBSERVE the rendered output (what sensor/analysis reads it back)?
(c) does a deliberation step consume that observation? (d) does a
re-render step exist that is conditioned on the deliberation? All four
must be present and causally connected. Causality check: neuter the
observation — does the re-render change?

## Verdicts

| Line | (a) render | (b) observe own output | (c) deliberate | (d) re-render | Verdict |
|---|---|---|---|---|---|
| Audio planner/vocabulary (`audio_longhorizon/planner_vocab`) | yes — probe tones + ITER renders via own WAV path | yes — frozen organ+guard, HEARD tags | yes — R4/R5/R7/R8, DELIBERATED/PREDICT journal | yes — ITER n RENDERED, corrections gated on predicted improvement; R8 hold fires | **CLOSED** |
| Image zoom fork (`image_zoom_fork`) | yes — structure render, in-place motif eval, final emit | yes — D = pix − structure render; E_after measured from in-place render | yes — deliberate_zoom sets z1/z2 from measured block residual energy | yes — zoom_stamp_blocks applies finer motifs only where flagged | **CLOSED** (exactness-driven; deliberation is threshold-based) |
| Image exact_work v3 (`image_exact_work/v3`) | yes — renderA (ingest), renderB (emit) | partial — residual deltas computed from renderA vs original | no — deltas recorded mechanically, no judgment | no — emit applies deltas deterministically; renderB never observed by TNN | **PARTIAL** (break at c/d) |
| Image generation azgen.zag (`image_upscale/generation`) | yes — constructed 2× pixels | partial — in-binary per-label/tile SSE of own output vs GT | no — scores written to file, feed nothing | no | **PARTIAL** (break at c/d) |
| Upscale azupscale.zag (`image_upscale`) | yes — upscale_tnn.bmp | no — GT loaded "for MEASUREMENT ONLY, never fed to construction"; scoring by crew metrics.py | no | no | **BLIND** |
| Video composer step5 (`imagination/video-fusion-step5`) | yes — 24 PPM frames | no — nothing reads output frames back | no — deliberation is over the PLAN, never the rendered frames | no | **BLIND** |
| Imagination trial (`imagination/` VERDICT) | no render step | — | — | — | **OUT-OF-SCOPE** (internal scene, designs as specs; law applies when pixels render) |

## Evidence per line

### 1. Audio planner/vocabulary — CLOSED

`audio_longhorizon/planner_vocab/PLANNER_DESIGN.md`:
- R1 SELF-CALIBRATION: "renders probe tones through its own renderer, hears
  them through its own organ+guard, records (param → heard quantity) curves."
- R4 PREDICT-BEFORE-CORRECT: "A correction is applied ONLY if predicted ERR
  < measured ERR (strict)."
- R8 NO-PROGRESS HOLD: correction with no measured improvement forces a hold,
  "journaled like every other decision."
- Journal tags: TARGET / HEARD / CONSULTED / PLANNED / RENDERED /
  ITER n PLANNED / ITER n RENDERED / ITER n DEVIATION (+ CAL/DELIBERATED/PREDICT).
- `VERDICT.md` (2026-09-26): R8 "fires correctly... verified in smoke +
  battery journals: `reason=no-progress-hold`". ERR(3)/ERR(0): 0.965→0.710
  (fresh), 0.944→0.559 (deep). Trial verdict PARTIAL PASS (11/20, 13/20 vs
  16/20 bar) — the LOOP is closed; the trial's strict bars are a separate
  matter.
- Causality: neuter the HEARD measurement → DEVIATION changes → R4/R8 flip
  corrections to holds → the re-render changes. The hold behavior is the
  neuter proof: observation off ⇒ no corrective re-render.
- The desynth line (`audio_longhorizon/desynth`, plan_main_desynth.zag) is
  built on the same unified hear/emit machinery (same journal tags, same
  organ+guard) — covered by this verdict.

### 2. Image zoom fork — CLOSED (exactness-driven)

`image_zoom_fork/zoom.zag`, `ingest.zag`, `emit.zag`:
- `deliberate_zoom` (zoom.zag:183): measures per-block residual energy of
  TNN's own intermediate structure render (D = pix − s), sets z1/z2 zoom
  flags where residual "earns a deeper look" (tauz1/tauz2).
- `zoom_eval_inplace` (zoom.zag:528, called ingest.zag:201): renders motif
  substitution into the framebuffer, measures post-render energy
  (ZOOMLEDGER: E_detail=119291319 → E_after_L0=3426420).
- `zoom_stamp_blocks` (zoom.zag:572, called emit.zag:234): final emit applies
  finer L1/L2 motifs ONLY where z-flags are set.
- Neuter test: zero the z-flags → L1/L2 motifs not applied → final render
  changes. Causally connected.
- Caveat: the "deliberation" is a measured-threshold decision, not a
  recorded-reasons judgment. It satisfies the loop wiring; the depth of the
  deliberation is a separate authorship question.

### 3. Image exact_work v3 — PARTIAL (break at c/d)

`image_exact_work/v3/ingest.zag`, `emit.zag`:
- ingest renders layers 0..2 (renderA.bmp), compares against the original,
  records sparse residual deltas — "TNN's deliberated knowledge of its own
  reconstruction error."
- emit reads ONLY knowmap.bin, synthesizes layers, applies deltas →
  renderB.bmp. Deterministic application, not a deliberative re-render.
- renderB (the FINAL output) is never read back by TNN's machinery;
  byte-identity is checked by the crew's external diff.
- Break: (c) the residual recording is mechanical, not judgment; (d) no
  conditional re-render of the final output.

### 4. Image generation azgen.zag — PARTIAL (break at c/d)

`image_upscale/generation/src/azgen.zag` (main:668):
- One-pass construction (teach → partition fit → construct pixels).
- In-binary, AFTER construction (~1154): loads gt.bmp, computes per-label
  SSE and 8×8 tile SSE of its OWN constructed buffer, writes scores file.
- The observation stage EXISTS (TNN's machinery reads its own output) but
  is disconnected: scores feed no deliberation, no re-render follows.
- Break: (c)/(d) absent. Note: the measurement is GT-dependent.

### 5. Upscale azupscale.zag — BLIND

`image_upscale/src/azupscale.zag` (main:534):
- One-pass: deliberate layers → construct → `bmp_write(... "upscale_tnn.bmp")`
  (line ~1092), labelmap, trace.
- Header comment (line 4-5): "TNN observes ONLY input_256x92.bmp...
  gt_512x184.bmp is loaded for MEASUREMENT ONLY — it is never fed to the
  construction." Scoring is the crew's external metrics.py.
- No in-binary read-back of the constructed output, no deliberation over
  it, no re-render. BLIND.
- Note: upscale round 3 is running under the mega-plan (genuinely new broad
  mechanism required). The loop-closing work below should be routed to that
  coordinator, not duplicated.

### 6. Video composer step5 — BLIND

`imagination/video-fusion-step5/src/composer_base.zag`:
- CLI (main:1583): `ingest | recall | stillingest | stillrecall | compose | render`.
- `do_render` (1521): executes the plan, writes frames; trace says
  "comparison render only; NOT selected by deliberation."
- Nothing reads the 24 output PPM frames back into TNN's machinery. The
  deliberation (anatomical reasoning — snout/neck/flip/photometric) operates
  on the PLAN over source perception, never on rendered output.
- The lead judged the output himself ("black blob sticker"); TNN never
  looked at its own render. BLIND.
- Note: step6 was analysis-only (no new render); v4 is BLOCKED (crash before
  render). The video line is parked on the lead's eyes per program state.

### 7. Imagination trial — OUT-OF-SCOPE

`imagination/VERDICT.md` (2026-09-22): "no external rendering" — scenes held
internally, designs emitted as text specs. The law governs rendering
pipelines; if pixel rendering is ever added to this line, the loop must be
built then.

## Work orders (for every non-CLOSED line)

### WO-1 — Video composer (BLIND → CLOSED)
Missing: (b) read-back, (c) deliberation over own frames, (d) conditional re-render.
1. Add a `judge` stage to `imagination/video-fusion-step5/src/composer_base.zag`:
   ingest the rendered frames back (reuse the existing frame-ingest path),
   run TNN's own perception over them, and deliberate with native checks,
   e.g.: does the merged frame still show the recipient's face below the
   graft? is the graft attached at the measured neck point (lmf 80..112)?
   seam-vs-identity tradeoff measured ON THE OUTPUT.
2. Add a `revise` path: adjust plan parameters (placement anchor, flip,
   photometric candidate) from the judgment and re-render; iterate to
   acceptance or a bounded iteration count, all journaled.
3. Wire into main() CLI (now at line 1583) as `judge` / `revise` commands.
4. Causal proof required: neuter the judge's observation (feed it the
   pre-render plan scores instead of the rendered frames) — the re-render
   must change.
ROUTING: video is parked on the lead's eyes; queue WO-1 behind his verdict,
do not start unprompted.

### WO-2 — Upscale azupscale.zag (BLIND → CLOSED)
Missing: (b), (c), (d).
1. In-binary read-back of the constructed `upscale_tnn.bmp` after
   construction (`image_upscale/src/azupscale.zag`, main at 534;
   construction ~1087–1116).
2. GT-free self-judgment from native measurements only: 2×2 pixel-grid
   artifact detection (the lead previously caught visible grid rectangles),
   region-boundary seam visibility, label-consistency checks.
3. Conditional re-construction: flagged regions re-constructed with a
   different operator chosen BY THE DELIBERATION per region (not a crew-set
   global switch).
4. Causal proof: neuter the grid/seam detectors — flagged regions must stop
   being re-constructed.
ROUTING: upscale round 3 is in flight under the mega-plan; hand WO-2 to
that coordinator instead of running a separate line.

### WO-3 — Image generation azgen.zag (PARTIAL → CLOSED)
The observation stage exists; connect it.
1. Feed the in-binary per-label/tile SSE (`image_upscale/generation/src/azgen.zag`,
   main at 668, measurement ~1154) into a deliberation stage: which labels/
   tiles failed, which atom choice caused it, recorded reasons.
2. Conditional re-fit: re-fit failed tiles with different atom candidates;
   iterate to acceptance or bound.
3. Develop the GT-free production judgment in parallel: the native
   round-trip check — does the constructed high-res downscale back to the
   observed low-res input? (GT-free, uses only the input TNN was given.)
   Record where the round-trip check is blind (the super-resolution
   ambiguity: many high-res patches downscale to the same key) and what
   additional native constraint is needed.
4. Causal proof: neuter the tile-SSE feed — failed tiles must stop being re-fit.

### WO-4 — Image exact_work v3 (PARTIAL → CLOSED)
1. Add a native verify stage: TNN's own machinery reads renderB.bmp back
   and checks byte-identity against the original (both are already in the
   pipeline — ingest reads the original, emit writes renderB).
   Files: `image_exact_work/v3/ingest.zag`, `v3/emit.zag`.
2. A mismatch triggers a recorded re-deliberation (which layer's commit
   failed? re-commit the layer or re-record the residual?) — not a silent
   pass, and not left for the crew's external diff to discover.
3. Honest note: for exactness the check is a byte-compare; the deeper gap
   is the residual layer being verbatim error correction rather than
   understanding — record that as a separate finding, don't dress the
   checksum as deliberation.

## Second-opinion status

z.ai (GLM-5.3) skeptic review requested 2026-09-27 ~01:20 PDT on (i) the
seven classifications and (ii) the four work-order designs
(`~/workspace/zai_relay/INBOX/see-its-result-q1.txt`, `-q2.txt`).
**[PENDING at commit time — answers to be incorporated as an amendment if
they change any verdict.]**

## Method note

Verify-only: no pipelines rebuilt, no renders run (disk at 99% — read-only
analysis on committed sources). All verdicts trace to committed code and
docs cited above. Stage presence was checked in source (function names,
call order, CLI surface); causal claims cite journaled behavior (R8 holds)
or code structure (flag-gated emit paths) where neuter experiments were
not re-run.
