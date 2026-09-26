# Video Fusion v4 — Provenance

## Sources

### Pig frames
- Path: `~/workspace/video-combine/source/frames/frame_00.ppm` … `frame_23.ppm`
- SHA-256 (source): `b1dbe434629a1b02ffec629089be56dfe58b13d2cbc2f7e44bc205b9fb63540a`
- Provenance: Ljubljana Zoo pig, Wikimedia/YouTube CC BY 3.0.
- Source segment: 3.0–6.0 seconds.
- Format: 320×240 PPM, 24 frames, 8 fps, 3.0 seconds.
- Store: `~/workspace/video-composer/runs/ingest_pig_A/store.bin`

### Bunny frames
- Path: `~/workspace/video-repro/source/frames/frame_00.ppm` … `frame_23.ppm`
- Store: `~/workspace/video-composer/runs/ingest_bunny_A/store.bin`
- Note: Do NOT use `video-composer/hare_frames`; it is a different stress clip.

### Instruction
- Path: `~/workspace/video-composer/instr/merge.txt`
- Content: "merge the pig and the bunny together"

## Toolchain
- Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)
- Language: Pure Zag, zero RNG.

## Prior work (Step 3)
- Commit: `5a669742bdcf`
- Workdir: `~/workspace/video-fusion/`
- Gallery: `~/workspace/your_files/video_fusion_new/gallery.html`
- Verdict: Tracked graft, not realistic fusion.
- Known issues addressed in v4:
  - Donor frame frozen at 12 → v4 uses live corresponding donor frame.
  - 3× gain clamp → v4 proposes T1-T4 and selects via metrics.
  - No pose normalization → v4 measures landmarks and normalizes.
  - No stabilization → v4 deliberates its own stabilization.

## Diagnostic measurements (2026-09-26)
- Raw slot/donor luminance gap: 5.96×.
- Bright-reference illumination ratio: 1.24×.
- Residual albedo ratio: 4.79× (blind 6× gain would be dishonest).
- Pig camera drift (full-res): frame 12 (0,36), frame 18 (-7,55), frame 23 (-19,45).
- All 24 pig frames distinct with real motion.
- No hard bunny scene cut confirmed.
