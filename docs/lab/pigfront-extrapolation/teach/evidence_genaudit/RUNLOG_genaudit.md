# RUNLOG: pig-front generation audit (2026-09-26)

Task: Micah's standing correction — "TNN shouldn't draw it should generate."
Investigate why the taught pig-front kept 22 px head error; consult Fable + crew;
prototype the smallest honest step from drawing toward generating.

## White-box decomposition of the 22 px

- Read `teach/evidence/taught_trace.txt`, `taught_metrics.txt`: plan head (160,112),
  truth detector centroid (182,112) → dx=22, dy=0.
- Source inspection of the taught branch: `h_put64(PLAN, 0, 160)` — head x hardcoded
  to the frame midpoint. The comment explains only the learned *vertical* placement.
  Conclusion: the full 22 px nominal is the hardcode, not renderer rounding.
- Truth-detector sensitivity (local Python reproduction of the committed detector on
  `forka/forka_front.ppm`): nominal band 70..175 → (182,112); perturbations move x
  ±1–3 px near nominal, up to 16 px under broad threshold changes (60..185 → (166,114)).
- Renderer seed/noise contribution to the PLAN-vs-truth metric: 0 px (metric compares
  PLAN directly; nothing downstream moves PLAN).

## Fable consultation (~/workspace/skills/unorouter/bin/fable_stream.py)

- Attempt 1: EMPTY-CONTENT (46 streamed chars) → `fable_answer_gen.txt`.
- Attempt 2: 3,579-char answer, truncated mid-sentence → `fable_answer_gen2.txt`.
  Useful, TNN-aware: the pixel-value line test; patch/transition/layout atoms.
- Continuation request → `fable_answer_gen3.txt` (10,080 chars): drifted badly —
  normal-distribution sampling, PCA morphing, EfficientNet, learned inpainting.
  Violates zero-RNG and no-neural-machinery. Preserved verbatim, rejected in verdict §2.
- Prompts kept: `fable_prompt_gen.txt`, `fable_prompt_gen_cont.txt`.

## Prototype: gentex.zag (pure Zag, zero RNG)

Built `teach/gentex.zag` (~600 lines): measured-field texture transfer.
- Reads `fixtures/teach_front_0030.ppm` + `taught_run/front_construct.ppm`.
- Measures: head flood bbox, corner bg mean, per-region means, per-part color deltas.
- Renders bg fill + 4 parts as measured_source + measured_delta. No hash noise,
  no invented shading. Ellipse region boundaries documented as remaining drawing.
- Build fixes along the way: renamed `try` param (reserved keyword); removed an
  extra `}` in the hand-transcribed PPM parser; per-dir roots (nio_name_valid
  rejects `/` in child names); trace buffer flattened before file write.

Runs (cwd `teach/`):
- `./gentex_bin` → exit 0, `gentex done head_bbox=10,10-310,215`.
- Two runs → sha256 `8575e46acbafd591a53af3d0b7df5ca6ca844d73fbba03dc3510f919ffe86bc4`
  both times (byte-identical).
- Transfer exactness audit (independent Python, 3,000 sampled pixels):
  3,000/3,000 == measured_source + measured_delta exactly.
- Texture stats (Zag + independent Python cross-check, agree):
  photo std 12–14 lagH 0.66–0.82 lagV 0.51–0.59;
  old render std 1.1 lagH 0.34 lagV 0.39–0.46;
  new render std 18–19 lagH 0.57 lagV 0.60.
- Placement NOT fixed (by design): detector on new render (156.8,104.0) → ~25 px
  from truth, same hardcoded-x cause.
- Caveat found and documented: the teaching photo's band mask merges head and
  background into one flood component, so the head source region includes
  background pixels. Not hidden — listed in verdict §5.4.

## Deliverables

- `teach/gentex.zag` — prototype source
- `teach/evidence_genaudit/VERDICT_genaudit.md` — verdict + verbatim Fable transcripts
- `teach/evidence_genaudit/RUNLOG_genaudit.md` — this file
- `teach/evidence_genaudit/gentex_stats.txt` — prototype output log (evidence)
- NOT committed: `gentex_bin` (binary), `gentex_out/*.ppm` (reproducible renders),
  `/tmp/gentex_compare.png` (judgment render)

## Open follow-ups (specified in verdict §5, not built)

- Deliberated head-x rule replacing the 160 hardcode (candidates measured:
  ear-mid 163.5 → 18.5 px err; snout-x 186 → 4 px err; mean 174.75 → 7 px err).
- Patch atoms + transition atoms at finer granularity.
- Same generate-don't-draw audit for the other generation lines.
