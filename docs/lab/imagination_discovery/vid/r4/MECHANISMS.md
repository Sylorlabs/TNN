# D-VID-1 Round 4 — mechanism verdicts (2026-09-22)

Micah's law: every mechanism is LOGIC-DERIVED or COSMETIC. The flagship
advances on logic-derived mechanisms only. A cosmetic judging winner would
be reported as "COSMETIC WIN", never as imagination.

## Diagnosis (see DIAGNOSIS.md)

Three culprits behind the "Minecraft" read:
1. March-segment terracing — shading evaluated once per winning march step,
   hard color discontinuities at every segment boundary (mid-region
   vertical edge energy 22.48 vs horizontal 6.47).
2. Chunky foam breakup cells — 0.64 world units = 11–33 px near camera.
3. Oversized/impotent micro-normals — 187-px cells, ±2° tilts; no capillary
   structure for sun glitter.

## Per-mechanism results

| ID | Class | One-sentence scene truth | Blocky-read effect | Cost | Verdict |
|----|-------|--------------------------|--------------------|------|---------|
| Ma | LOGIC-DERIVED | Short gravity waves are real elevation; their finite-differenced tilt belongs in the shading normal. | Strong fine structure; harsh/noisy alone (mid V +5.0), needs per-pixel shading to read as texture. Tuned 360→240. | +3 noise evals/px | KEEP |
| Mb | LOGIC-DERIVED | Foam is fine lace, not blocks. | Subtle alone (fg dV −0.03); essential under Mg, where it stops the exposed foam cells reading as tiles. Evolved to Mb4: world-space two-scale breakup (fine 0.08wu lace in coarse 0.32wu patches, Mq fractional coords, distance fade). Mb2 1/wz "perspective-correct" scaling was degenerate (wx/wz both scale with wz, so the z-noise-input went constant and the breakup collapsed to 1D diagonal streaks); reverted to world-space. | +1 noise eval/px | KEEP |
| Mc | LOGIC-DERIVED | Surf breaks into spume at the spire bases; far field needs distance-appropriate breakup. | Weak positive: breaks the solid white waterline sheet into patches. First two implementations were no-ops (distance fade / saturated ring); third works. | +1 noise eval where sprox>60 | KEEP (weak) |
| Md | LOGIC-DERIVED | Sun glitter comes from cm-scale capillary facets. | Subtle extra sparkle in the glitter path; near-zero in metrics. | +2 noise evals where gfade>0 | KEEP (weak) |
| Me | BORDERLINE | Second fine normal octave. | ~zero at the tested amplitude (55/1000). A stronger Me would duplicate Ma with weaker scene logic — a normal wiggle with no elevation behind it, unlike Ma's true height derivative. | — | KILL (redundant) |
| Mf | COSMETIC | None — fog grain, the negative control. | Adds fine grain only (fg H +0.69); the tiles persist underneath. Behaves exactly as a cosmetic should: noise without structure. | — | KILL |
| Mg | LOGIC-DERIVED | The surface is continuous; shade every pixel from interpolated surface parameters, not once per march winner. | Core architectural fix: killed the horizontal band edges (mid crop: banding gone). Side effect: exposes the coarse foam cells sharply → needs Mb. Evolved to Mg2: synthetic nearer partner so the bottom segment interpolates instead of flat-shading. | ~1 extra o_height/col | KEEP (core) |
| Mh | LOGIC-DERIVED | Rock is a 3D solid: shade per row with cone-surface normals and blend silhouette pixels by sub-pixel coverage. | Subtle: slightly softer spire silhouette, per-row vertical shading. Near-zero metric movement. | ~0 | KEEP (weak) |
| Mq | LOGIC-DERIVED | Noise fields are continuous in world space; integer wx/wz quantize them near the camera (wx in {-1,0,1} across 256 px), so every noise field must be sampled in fractional (8-frac-bit) world coords. | THE near-field culprit: foam/normal debug channels showed giant quantized blocks; after Mq the blocks are gone (fg V +35). Unleashed too much at once — needs rebalancing (see Mb3). | ~0 | KEEP (core) |
| Mb3 | SUPERSEDED | Two-scale perspective-correct breakup. | Degenerate 1/wz scaling made 1D diagonal streaks; superseded by Mb4 world-space two-scale. | — | SUPERSEDED |
| Mb5 | LOGIC-DERIVED | Mid-field foam forms stormy patches, not a uniform white band. Coarse world-space octave (4wu) with far fade; fine breakup would alias at mid ranges. | Mid-field was a uniform white band (broad crestf + no breakup beyond wz=200). Coarse patches give large-scale organization. | +1 noise eval/px | KEEP |

## Combination status

R4 = Mg2 + Ma(120) + Mb4 + Mb5 + Mc + Md + Mh + Mq (Me/Mf killed, Mb2/Mb3 superseded, Ms reverted).
- Mid/far water: blocky read dead — fine mottled chop, no banding.
- Spire region: improved silhouette; waterline breakup slightly harsh
  (raised bup threshold thins it).
- Foreground: Mq killed the quantization blocks. Rebalancing: Ma 240→120
  (calmer micro-normals), bup threshold 430→560 (thinner foam), Mb3
  two-scale breakup (patchy clusters, not uniform dashes).
- REVERTED Ms: the march-array dhdx/dhdz were CORRECT all along
  (hsp[kk] is a valid surface height at a different x, not garbage).
  Lesson: ocean.zag heights are MILLI-world (camera at 13000 = 13 world);
  my finite-difference slope was 1000x too big. The dense foam is the
  broad crestf term (foams the upper ~50% of the wave field), organized
  by the two-scale breakup.

## Open diagnosis (foreground blocks)

The fg blocks survive per-pixel shading + perspective-correct breakup, so
they are not (only) foam cells or segment tiles. Candidates: macro
specular patches (s^8 nonlinearity on smooth swell normals), binary
macro-foam regions, or column-to-column march-winner jumps. Debug
channels (foam=6, normal=7) being rendered to decide.
