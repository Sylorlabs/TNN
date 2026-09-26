# Provenance - video-composer STEP 2 additional memories

## field (pig, second segment)
- **Source:** same `pig_source.webm` as the main pig memory
  (SHA-256 `b1dbe434629a1b02ffec629089be56dfe58b13d2cbc2f7e44bc205b9fb63540a`;
  see `~/workspace/video-combine/source/PROVENANCE.md`).
- **Segment:** t = 9.0 s -> 12.0 s (3.0 s window, different framing from the
  3.0-6.0 s pig memory: body/torso view vs head-at-fence).
- **Frames:** 24 at 8 fps, 320x240 Lanczos, PPM P6 `frame_00.ppm`..`frame_23.ppm`.
- **Command:** `ffmpeg -v error -ss 9.0 -i pig_source.webm -t 3.0 -vf
  "fps=8,scale=320:240:flags=lanczos" f_%02d.ppm` (renamed 01-24 -> 00-23).
- **Purpose:** content-sensitivity control for MERGE (same verb, similar
  content -> same plan [01], total 6543.20 vs 6544.20).

## hare (bunny, wide-shot segment)
- **Source:** same `bbb_source.mp4` as the main bunny memory
  (634.6 s; see `~/workspace/video-repro/source/PROVENANCE.md`).
- **Segment:** t = 120.0 s -> 123.0 s (3.0 s window; wide shot — small distant
  bunny, mostly grass/trees; a hard case for the saliency).
- **Frames:** 24 at 8 fps, 320x240 Lanczos, PPM P6.
- **Command:** `ffmpeg -v error -ss 120.0 -i bbb_source.mp4 -t 3.0 -vf
  "fps=8,scale=320:240:flags=lanczos" f_%02d.ppm` (renamed 01-24 -> 00-23).
- **Purpose:** content-sensitivity stress test for MERGE — the mechanism's
  saliency latched onto background trees (focus cell2), and the winner
  CHANGED to [15] SPLIT_H hare/pig (6435.40). Proves the choice follows the
  measurements, not the labels; also exhibits the saliency limitation
  honestly.
