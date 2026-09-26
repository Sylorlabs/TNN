# GENERATION PATH — how the bytes were made (pure Zag)

## Pipeline (every media byte from one native binary)
1. `field.zag` — deterministic continuous-field imagination system:
   24×24 RGB/roughness visual cells, 48 time × 48 semitone audio cells,
   24×24 structural height field, deterministic coordinate hash (zero RNG).
2. New scenes added as `f3_video_key` v=3..6 (4 keyframes each) +
   `f3_video_audio` v=3..6 (event-timeline soundtracks), purely additive —
   no existing function body modified except two one-word sign fixes and
   three filename mappings.
3. `f3_vidfield` interpolates 4 keyframes → 24 frames @ 8 fps (linear).
4. `f3_emit_avi` writes uncompressed 240×240 RGB + 8 kHz mono 16-bit PCM
   into one RIFF AVI, all bytes emitted in Zag. New CLI: `f3navi <outdir>`
   renders v=3..6 AVIs + WAV siblings (`f3_emit_wav`, `which` 30–33).
5. Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
   (pinned), built from `imagination/src/` cwd (import layout preserved).

## What is deterministic
- Zero RNG anywhere: texture comes from a deterministic coordinate hash;
  reruns are byte-identical (proven: 2 full renders, 8/8 SHA-256 identical).

## What changed in the source (vs committed `tnn-native-lab` baseline)
1. `f3_video_key`: +4 scenes (v=3..6), inserted before the v==2 fallthrough.
2. `f3_video_audio`: +4 soundtracks (v=3..6), inserted before the v==2
   fallthrough.
3. `f3_aviname`: `nvid3..6.avi` mappings.
4. `f3_wavname`: `nvid3..6.wav` as `which` 30–33.
5. `main`: `f3navi` dispatch.
6. **Bug fixes (2 words):** `f3_emit_avi` + `f3_emit_wav` now read the mix
   with signed `f3_get32s` instead of unsigned `f3_get32` (half-wave
   rectification; hi-fi path already used the signed read).

## What is NOT in the media path
- `ffmpeg` 8.1.2: MP4 viewing conversions ONLY (disclosed in gallery +
  VERDICT). Native AVIs/WAVs are authoritative and untouched by it.
- Python/PIL: contact-sheet inspection + frame-diff measurement only.
- No upscaling, no model inference, no stock assets.

## Reproducibility
Commit `field.zag` + toolchain pin → `znc … field.zag -o field_bin_new` →
`./field_bin_new f3navi <dir>` twice → SHA-256 must match CHECKSUMS.md.
