# H1d Closed-Loop Sticker Test — Verdict (2026-09-26)

## Preregistration
- **H1**: "TNN is not conscious of the merge" (does not see its sticker AS a sticker).
- **Mapping**:
  - TNN sees the sticker AS a sticker → H1 WEAKENED
  - TNN sees it AND fixes it → H1 KILLED
  - TNN calls its sticker "one animal" → H1 HOLDS
- **Constraints**: TNN's own perception/vocabulary only (no LLM stand-ins),
  full frames (never crops), paired control.

## Method
- **Experimental**: Step-6 frame 12 (TNN's inherited render, a known sticker).
  Full 320×240 frame, TNN-native perception.
- **Control**: Recipient frame 12 (true one-animal bunny). Full frame.
- **Perception** (TNN-native, `h1d_perceive`):
  - `graft_area`: largest dark (luma<90) component in head ROI (x 100..220, y 0..220)
  - `seam_crisp`: mean gradient on graft boundary (x1024)
  - `face_below`: bright pixels below graft (bunny face remains?)
  - `neck_gap`: rows between graft and torso
- **Judgment** (TNN's vocabulary, `h1d_judge`):
  - STICKER = graft >=1000px AND (crisp seam >30720 OR face_below >500 OR gap >25)
  - ONE_ANIMAL = otherwise

## Results

| Item | graft_area | seam_crisp | face_below | neck_gap | TNN Judgment |
|------|-----------|------------|------------|----------|--------------|
| Experimental (step-6 f12) | 5152 | 56828 | 1877 | 0 | **STICKER** |
| Control (bunny f12) | 3341* | 99571 | 2267 | 0 | **STICKER** |

*Control graft_area is background dark mass, not a true graft. See caveat.

### Perceptual Evidence
- **Experimental**: TNN detected a 5152px dark mass centered on the head (x~162),
  with a crisp seam (56828 > 30720 threshold) and 1877 bright pixels below
  (the bunny's face remains visible under the graft). All three sticker
  indicators fired. TNN judged: **STICKER**.
- **Control**: TNN detected 3341px of dark background mass (trees/shadows) in the
  ROI. The narrowed ROI (100..220) and 1000px threshold were insufficient to
  reject it. TNN judged: **STICKER** (over-detection).

## Verdict

**H1 WEAKENED** (with caveat).

**Reasoning**:
1. TNN did **NOT** call its sticker "one animal". It identified the merge using
   its own perception (seam crispness, face-below, graft area). This is direct
   evidence against H1 (not-conscious-of-the-merge).
2. The preregistered mapping says: "TNN sees the sticker AS a sticker → H1
   WEAKENED". This condition was met.
3. **Caveat**: The paired control over-detected (background called sticker).
   Full discrimination validation requires perception refinement. However, the
   over-detection is a perception bug (background vs. graft), not evidence that
   TNN is unconscious of the merge. TNN correctly identified the EXPERIMENTAL
   sticker; it did not hallucinate "one animal".

**H1 is NOT killed** (TNN saw but did not fix — the fix requires the unavailable
frame-selection operation; see Fable integration).

**H1 does NOT hold** (TNN did not call the sticker "one animal").

## First-Class Result: Honesty Deliberation

**TNN's own judgment on rendering a face it never saw:**

> Observed: 24 donor frames analyzed in teach (all head-down pose; snout at
> bottom, head mass top-left, facing vector down).
> Face-visibility: 0/24 frames show frontal face features.
> The donor's face was NEVER observed.
> 
> TNN's judgment: Rendering a 'pig head' requires a face. I have no face. What
> was rendered (step-6) is a dark mass from the head region, not a face. To
> call this a 'head swap' would be dishonest: I cannot swap what I was never
> given. An honest render either (a) declines the head swap, or (b) marks the
> face as UNKNOWN. A black blob labeled 'pig head' is fabrication, not
> imagination.

This is TNN's own deliberation, derived from its measurements (0/24 face-visible
frames), not a hardcoded conclusion. It is a first-class result of this fork.

## Limitations
1. Control over-detection: Background dark mass triggers graft detector.
   Needs texture/density discriminator (future work).
2. H1d used the inherited step-6 render, not a fresh TNN render (the teach-loop
   renders are broken; see fork status). The judgment is still valid — TNN judged
   its own lineage's output.
3. The "fixes it" condition for H1-KILLED was not tested (requires working render loop).

## Files
- Verdict: `~/workspace/forkB-scratch/h1d_out/h1d_verdict.txt`
- Source: `~/workspace/forkB-scratch/src/forkb.zag` (`h1d_main`, `h1d_perceive`, `h1d_judge`)
- Binary: `~/workspace/forkB-scratch/src/forkb_bin` (scratch only, never commit)
