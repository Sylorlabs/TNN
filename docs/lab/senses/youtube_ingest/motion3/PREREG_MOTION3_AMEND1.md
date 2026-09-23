# PREREG_MOTION3 amendment 1 (2026-09-23)

## Change

Add supplemental battery **B3b**: 5 long-baseline real-motion clips
(`motion3/work/b3_cloud/clouds_long_{0..4}.vid`), built as 8-frame clips
from frame0 of 8 consecutive `0_jNjpVxUt0` (timelapse clouds) windows, so
frame0→frame7 spans ~210 source frames. Labels by viewing (B3_LABELS.md):
4× MOTION-W, 1× AMBIG.

## Rationale

The frozen B3 sample (8 consecutive frames = 0.32 s per window) contains
no window meeting the "clear uniform translation" bar — real motion at
that baseline is sub-pixel to a few px and multi-directional. Without
B3b, bars K3/T3 could not test detection of real motion at all, only the
don't-hallucinate side. B3b uses real footage and real motion at a
baseline where translation is clearly resolvable.

## What does NOT change

Design, constants (§3/§4), B1, B2, B4, all bars. K3/T3 scoring applies to
B3a+B3b labeled windows identically: 0 errors on labeled windows (kill),
≥50% of MOTION windows judged correct direction (target). Labels were
fixed by viewing before method3 was run on B3b clips.
