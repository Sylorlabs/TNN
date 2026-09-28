# No-bridges composer — PROVENANCE.md

## Inputs (all pre-existing, none created by this task)

- Bunny memory store: `~/workspace/video-composer/runs/ingest_bunny_A/store.bin`
  (24 frames, 320×240, from `~/workspace/video-repro/source/frames/frame_*.ppm`)
- Pig memory store: `~/workspace/video-composer/runs/ingest_pig_A/store.bin`
  (24 frames, 320×240, from `~/workspace/video-combine/source/frames/frame_*.ppm`;
  provenance: `~/workspace/video-combine/source/PROVENANCE.md`)
- Instruction: `~/workspace/video-composer/instr/merge.txt`
  ("merge the pig and the bunny together")
- Step-3 baseline (comparison only): repo commit `5a669742bdcf`
  (`composer step 3: realistic fusion organ`),
  video `~/workspace/video-fusion/mp4/fuse_A.mp4`,
  frames `~/workspace/video-fusion/runs/fuse_A/`

## Build

- Assembled by `src/build_nb.sh`:
  `composer_base_head.zag` (vendored exact build input: step-3's committed
  `composer_base.zag` minus its `main()` dispatcher, which `nb5.zag`
  provides; ingest/recall/parse/trace helpers, reused) + `nb0.zag`
  (neutral measurement primitives extracted unchanged from step-3's fusion
  organ; step-3's percentile/threshold/morphology segmentation functions
  deliberately excluded) + `nba.zag` (generic adaptation/graft operators
  from step-3, reused unchanged) + `nb1.zag`–`nb4.zag` (invention organ,
  new) + `nb5.zag` (orchestration, new).
- Compiler (pinned): `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
- MP4 encoding: `ffmpeg` (libx264, crf 14, 8 fps) — encoding only, not part
  of the mechanism.

## Runs (2026-09-26)

- Run A (`runs/fuse_nb_A`): first successful run after two bug fixes
  (trace-buffer overflow on highly fragmented winners; misaligned
  histogram-slot offsets in `nb_modality`). 24/24 frames + `trace_fuse_nb.txt`.
- Run B (`runs/fuse_nb_B`): independent rerun. Trace byte-identical;
  all 24 frames byte-identical. (Scratch dir removed after verification.)
- Run C: rerun after extracting `nb0.zag`/`nba.zag` (replacing wholesale
  `fz1`/`fz2` copies). Trace and all 24 frames byte-identical to run A —
  the extraction changed nothing behaviorally. (Scratch dir removed.)

## Determinism evidence

- trace sha256: `7b25d3892323f623` (first 16 hex; full value in run log)
- frame_12 sha256: `b023b466dd00d2e5` (first 16 hex)
- Method: two (three, counting C) fully independent process runs; `cmp` on
  trace + all 24 frames. Zero RNG in any decision path (no RNG priming,
  no stochastic tie-breaks anywhere in the organ).

## Gallery (user-facing)

- `~/workspace/your_files/video_composer_nobridges/gallery.html` — NEW-badged,
  self-contained (all media as data URIs; verified zero external `src` via
  `grep -P 'src="(?!data:)'`), embeds the no-bridges fusion video, the step-3
  video, 8 key-frame PNGs, the full invention trace, and the verdict.
