# RUNLOG — new imagined videos, set 2

## 2026-09-26 ~04:30 UTC — setup
- Located native infra: `~/workspace/tnn-lab/imagination/src/field.zag`,
  toolchain `znc_linux_x86_64_abed8aa1`, existing binary `field_bin`
  (sha256 `144cfba0…670588578e4`). Backed up binary → `~/workspace/video_new/field_bin.orig`.
- Read AGENTS.md + TOOLS.md rules (import cwd, commit scripts, /tmp limits).

## ~04:45 — scene design
- Read `f3_video_key`, `f3_video_audio`, `f3_emit_avi`, `f3_aviname`,
  `f3_wavname`, main dispatch. Decided: purely additive v=3..6 (never touch
  v=1/v=2 code paths), new CLI mode `f3navi`, new filenames `nvid3-6.avi`,
  WAV siblings `which` 30-33.
- Designed 4 event timelines with shared scene/sound schedules (strike=bin 24,
  thunder delayed ~6 bins post-flash, gull cries with gull on screen, crackles
  on flame bursts).

## ~04:52 — build 1 + render 1
- Compiled → `field_bin_new` (329,227 bytes main). Rendered `f3navi` twice →
  8/8 byte-identical.
- Old-scene check: new binary's f3vid1/2 differ from Sep 22 committed bytes.
  Investigated: original `field_bin.orig` reproduces Sep 22 bytes exactly;
  raw-frame compare new-vs-old binary → VIDEO FRAMES IDENTICAL. Difference is
  audio-only, from the pre-existing 2026-09-24 gamma repair in current source.
  My edits proven clean.

## ~05:00 — full-eyes judging, round 1
- Extracted all frames, built 6×4 contact sheets, inspected every frame.
- PASS: nvid3 (forge), nvid4 (storm). FAIL: nvid5 (boats/gull invisible),
  nvid6 (fire tiny blob). Closed the loop → redesigned v5/v6 (bigger elements).

## ~05:05 — the corruption incident
- Scripted Python replace of the v5/v6 blocks used anchor `    if (v == 5) {`
  which ALSO prefixes `    if (v == 5) { return "nvid5.avi"; }` in
  `f3_aviname`. Replaced 42,262 chars: destroyed `f3_aviname` tail + ALL of
  `f3_video_key`.
- Recovery: fetched pristine `field.zag` from `tnn-native-lab` via gh-api
  (103,007 bytes; verified: gamma repair present, zero of my edits), copied
  over corrupted file, re-applied all 5 edits with unique anchors, verified
  structure (every fn defined exactly once).

## ~05:15 — build 2 + render 2, judging round 2
- Rebuilt, rendered twice → 8/8 byte-identical. Contact sheets v2: all four
  PASS with full eyes (forge strike, storm arc, harbor dawn with visible
  boats/gull/sun, campfire with gust lean).

## ~05:20 — audio analysis finds the rectification bug
- Waveform analysis: DC ≈ +20,000, ~4 zero-crossings, min = 0 → half-wave
  rectified. Root cause: `f3_emit_avi` + `f3_emit_wav` read the mix with
  unsigned `f3_get32` (the AGENTS.md "dollar tree mic" pitfall); the hi-fi
  path already used signed `f3_get32s`.
- Fix: two-word change (`f3_get32` → `f3_get32s`) in both emitters. Rebuilt,
  re-rendered twice → 8/8 byte-identical.
- Re-analysis: bipolar (DC < 130, ~5,200 zero-crossings), hum < 0.7%, no
  looping, transients on designed events, spectral peaks match planned
  partials within documented synth tuning (8 kHz path runs ~9.5 cents/sharp
  per semitone — measured 570 Hz vs planned bin-26 ≈ 570 Hz sharp-adjusted).

## ~05:30 — stream verification
- ffprobe: 4× (240×240 rawvideo, 24 frames, 3.0 s; pcm_s16le 8 kHz mono,
  26,400 samples). Frame analysis: 0 exact-dup pairs, 0 row tears, all
  frame-diffs > 0.

## ~05:35 — deliverables
- `~/workspace/your_files/imagination_video_new/`: 4× AVI (native,
  authoritative) + 4× MP4 (ffmpeg, disclosed convenience) + 4× WAV (native)
  + `index.html` gallery (marked NEW, honest caveats inline).
- SHA-256 of all 12 deliverables → CHECKSUMS.md.

## Next
- Commit to `tnn-native-lab`: source `field.zag` (lab-relative
  `imagination/src/field.zag` → repo `docs/lab/imagination/src/field.zag`),
  VERDICT.md, RUNLOG.md, ANALYSIS.md, CHECKSUMS.md, GENERATION_PATH.md.
  Exclude: binaries, `.zagd`, `.zag-cache`, renders (regenerable; AVIs/WAVs/
  MP4s live in your_files).
