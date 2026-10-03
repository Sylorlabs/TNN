# Provenance - video COMBINATION experiment, second clip (pig)

## Source work
- **Title:** "2024-06-01 LJUBLJANA ZOO LJUBLJANA - pig" (26 s, 3840x2160, VP9/Opus)
- **Author:** "NaIzletuSi (TM)" (YouTube channel; imported to Commons from
  https://www.youtube.com/watch?v=W-f5Dn3LE3w by Commons user Sporti)
- **License:** Creative Commons Attribution 3.0 (CC BY 3.0) - the video was
  released under YouTube's CC license option before August 2025 (per the
  Commons file page; adaptation and use with attribution allowed)
- **Commons file page:** https://commons.wikimedia.org/wiki/File:2024-06-01_LJUBLJANA_ZOO_LJUBLJANA_-_pig.webm
- **Download URL:** https://commons.wikimedia.org/wiki/Special:FilePath/2024-06-01_LJUBLJANA_ZOO_LJUBLJANA_-_pig.webm
  (redirects to the upload.wikimedia.org original; fetched 2026-09-26)

## SHA-256
- `pig_source.webm` (the actual file all frames derive from):
  `b1dbe434629a1b02ffec629089be56dfe58b13d2cbc2f7e44bc205b9fb63540a`
  (90,068,718 bytes)

## Extraction (this directory)
- **Segment:** t = 3.0 s -> 6.0 s of the source (3.0 s window; scene-cut check
  over 0-12 s via ffmpeg scene detection showed no cut inside 3.0-6.0 s)
- **Frames:** 24 frames at 8 fps (exactly 3.0 s)
- **Resolution:** 320x240 (Lanczos downscale from 3840x2160)
- **Format:** raw PPM P6 binary, zero-padded names `frames/frame_00.ppm` ...
  `frames/frame_23.ppm` (each 230415 bytes = 15-byte header + 320*240*3)
- **Frame extraction command:**
  `ffmpeg -v error -ss 3.0 -i pig_source.webm -t 3.0 -vf "fps=8,scale=320:240:flags=lanczos" frames/frame_%02d.ppm`
  (ffmpeg's image2 muxer numbers from 1; files were renamed 01-24 -> 00-23)
- **Reference video:** `pig_reference.mp4` - H.264, yuv420p, 320x240, 8 fps,
  24 frames, 3.0 s, crf 14 (same encoding as the bunny reference):
  `ffmpeg -v error -framerate 8 -i frames/frame_%02d.ppm -c:v libx264 -pix_fmt yuv420p -r 8 -crf 14 pig_reference.mp4`
- **Visual check:** probe frames at t=2/6/10/14/18 viewed as PNG - the 3.0-6.0 s
  window shows the pig's head at the fence, chewing/moving, no cut, no blur;
  all 24 frames byte-verified as distinct (real motion).

## Why this clip
A real pig (black-and-white, Ljubljana Zoo), head at the fence, small
continuous motion across the window - comparable in difficulty to the bunny
close-up (fur/feather texture, a moving animal subject) and a fair second
memory for the combination attempt.
