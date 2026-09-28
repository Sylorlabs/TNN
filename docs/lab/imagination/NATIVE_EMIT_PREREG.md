# NATIVE MEDIA EMISSION — PREREGISTRATION

Frozen: 2026-09-22. This document is the preregistered bar for Micah's order:
"TNN should natively be an audio generator / image generator just like us humans —
as a machine it should directly transfer imagined images, audio, and video into files."

Standing laws apply: pure Zag for all mechanisms (Python only for deterministic
verification), zero RNG in any decision path, byte-identical reruns, real mechanisms
not stubs. Tests decide; nothing here is asked of Micah.

## 1. WHAT IS BUILT

`imagination/src/emit.zag` — a native emitter compiled with the pinned znc
(`toolchain/bin/znc_linux_x86_64_abed8aa1`). It writes media files DIRECTLY via
`nio_*` syscalls (no shell redirection, no external renderer):

- **PNG emitter**: 12 Q4 designs + 4 Q1 visual scenes = 16 PNGs (1000×1000 RGB).
- **WAV emitter**: Q1 audio scenes 5–8 (both modes) + Q2 audio briefs 3–4 (both
  modes) = 12 WAVs (8000 Hz, 16-bit mono PCM).
- **Video emitter**: Q1V scenes 1–4 (both modes) = 28 PNG frames (1000×1000),
  one PNG per frame, deterministic filenames. The frame sequence IS the native
  video format (APNG container explicitly deferred — see §9).

Scene data comes from the canonical imagination mechanism, not transcription:

- Q4 designs: `ig_gen(ar, mode, brief)` for briefs 1–6, both modes — the same
  deterministic builders that produced `logs/q2m.txt` / `logs/q2h.txt`.
- Q1 scenes: `ig_q1_pre(ar, mode, scene)` initial placement (before mid-battery
  mutations), same as the gallery used.
- Q1V frames: initial `ig_place` lines of `ig_q1v_sc1..sc4`, extracted
  mechanically and verified line-present in `imagine.zag`.

Because `imagine.zag` defines its own `main` (duplicate-definition if imported),
the 65 functions in the transitive closure of `ig_gen` + `ig_q1_pre` are
extracted BYTE-VERBATIM into `imagination/src/scenes_inc.zag`, which `emit.zag`
imports. Verification: (a) a script asserts every extracted body is byte-identical
to `imagine.zag`; (b) the emitter re-prints the `dump`/`E`-line format and the
output is byte-compared against `logs/q2m.txt`, `logs/q2h.txt`.

## 2. FORMAT VALIDITY BARS (preregistered)

### PNG — must satisfy ALL:
1. Bytes `89 50 4E 47 0D 0A 1A 0A`, then IHDR (13 bytes: BE width, BE height,
   bit depth 8, color type 2 = RGB, compression 0, filter 0, interlace 0),
   ≥1 IDAT chunk, IEND chunk.
2. Every chunk: BE u32 length, 4-byte type, data, BE u32 CRC-32 (IEEE, polynomial
   0xEDB88320) of type+data.
3. IDAT payload: zlib header `0x78 0x01`, DEFLATE **stored** blocks (BTYPE=00,
   ≤65535 bytes each, LEN + NLEN one's complement), Adler-32 of the filtered
   scanline bytes.
4. Scanlines: filter byte 0 + raw RGB triplets per row.
5. Python Pillow opens the file and reports the expected size and mode RGB.
   (Deterministic verification only — Pillow is the checker, never the maker.)

### WAV — must satisfy ALL:
1. `RIFF` + size + `WAVE`, `fmt ` chunk of 16 bytes: format 1 (PCM), 1 channel,
   8000 Hz, byte rate 16000, block align 2, 16 bits.
2. `data` chunk: 16-bit little-endian samples, count = 8 × Σ note durations (ms).
3. Python `wave` module reads back (1 ch, 2 bytes, 8000 Hz) and the exact frame
   count. Deterministic verification only.

### Video — must satisfy ALL:
1. 28 frames: V1 3f, V2 4f, V3 3f, V4 4f, × 2 modes = 28 PNGs, each passing the
   PNG bar.
2. Filenames `q1v_v<scene><m|h>_f<frame>.png`; frame order = filename order.
3. Per-frame check: subject disc present at the scene's (x, y) / zone center,
   correct RGB, correct frame count and motion direction per scene.

## 3. BYTE-IDENTICAL DETERMINISM (preregistered)

Two clean reruns (output directory wiped between runs) → SHA-256 of every
artifact compared. **PASS bar: 56/56 artifacts identical**
(16 PNG + 12 WAV + 28 frames). Any mismatch = FAIL, root-caused before any
further commit.

## 4. RASTERIZATION: PILLOW-FAITHFUL PORT (preregistered)

The PNG rasterizer ports Pillow's `ImageDraw` semantics into pure Zag, as
characterized from Pillow's C sources:

- Rectangle: float coords truncated toward zero (C `int` cast); fill = inclusive
  [x0..x1]×[y0..y1]; width-2 outline paints a 2px INNER border.
- Ellipse: fill = integer Bresenham span emission (`quarter_*`/`ellipse_*` state
  machines, fill first); outline = separate inward width-2 ring, same bbox.
- Triangle: scanline fill with Pillow's `ROUND_UP`/`ROUND_DOWN` edge table, then
  outline via width-3 mask clipped to the fill.
- Human zone centers, human color mapping (incl. LIGHT/DARK × SATURATED/MUTED
  multipliers with round-half-to-even), structural side-view and stone layouts —
  all ported 1:1 from `gallery_src/render_gallery.py`.

## 5. COMPARISON BARS vs THE EXISTING GALLERY (preregistered)

- **Exact file bytes vs gallery PNGs: REPORT ONLY, expected to DIFFER.**
  Pillow writes zlib-compressed IDAT (level ~6) plus its own chunking; the native
  emitter writes stored (uncompressed) blocks. Different encoders, same pixels —
  byte equality is NOT the bar and NOT claimed.
- **Decoded RGB: PASS bar = zero differing pixels outside documented text
  regions.** The gallery invents two text payloads absent from the imagined
  scenes: the `TEXT` glyph on kind-4 panels and the `"NNN Hz"` labels on audio
  PNGs. The native emitter omits both (there is no font engine in pure Zag, and
  inventing pixels would be dishonest). Comparison masks those bboxes (computed
  from the gallery renderer); every other pixel must match.
- **Parameter fidelity:** every scene element is checked present with correct
  geometry/color/shape — by construction (scene words → rasterizer is direct)
  plus automated pixel spot-probes on the native PNGs.
- **Audio PNGs (A–D):** segment boundaries, axis, waveform, colors must match
  outside label regions. Waveform match depends on the Zag `sin` (§7).

## 6. INTERPRETATION POLICIES (documented choices — NOT imagined data)

These are visualization decisions the gallery already made; the native emitter
adopts them explicitly so comparisons are honest:

1. `TEXT` glyph on kind-4 panels: omitted (payload absent from scenes).
2. Audio PNG `"NNN Hz"` labels: omitted (no font engine).
3. Machine structural colors: the gallery's tan/gray RGB triples are replicated
   exactly as the visualization mapping (they were always gallery choices).
4. Human audio notes have no imagined duration/amplitude. Policy: borrow the
   same-brief machine durations — Q2 brief 3: 250 ms, brief 4: 150 ms
   (exactly what the gallery did); Q1 scenes: same-scene machine per-note
   durations (sc5: 250×4, sc6: 150×4, sc7: 250,250,250,500, sc8: 300×4).
   Amplitude 0.8 (gallery's choice).
5. Human pitch bin b → 110 × 2^(b/12) Hz (gallery formula; milli-Hz table in
   the emitter, derived deterministically).
6. Video subject: 60px filled disc at the frame's (x, y) (machine) or zone
   center (human); machine RGB from the scene, human color mapping.
7. Q4 audio/structural PNGs use the same `render_audio`/`render_struct`
   mappings as the gallery (800×200 audio layout; side-view blocks; stones).

## 7. WAV SYNTHESIS SPEC (preregistered)

- Machine note: freq Hz (integer from scene), dur ms, amp = a/1000.
- Human note: bin → freq table, dur borrowed (§6.4), amp 0.8, timbre from scene.
- Timbre: 5000 = sin(p); 5001 = sin(p) + 0.4·sin(2p);
  5002 = 0.8·triangle(p), the exact closed form of the gallery's
  0.8·(2/π)·asin(sin p) (mathematical identity; float last-ulp differences only).
- Phase p = 2π·f·i/8000 for sample i. No envelope (documented).
- Sample = round-half-to-even(32767·amp·timbre(p)), clamped to [-32768, 32767].
- `sin`: f64 range reduction + Taylor series, pure Zag. Accuracy bar (checked in
  verification, not in the binary): max |err| vs Python `math.sin` < 1e-12 over
  10,000 phases.
- **Audio bars:** measured fundamental within ±2 Hz of target (zero-crossing
  count per note segment); sample count exactly 8×Σms; rerun-identical bytes.

## 8. WHAT IS NOT CLAIMED

- No file-byte equality with Pillow's PNGs (different encoders, §5).
- No text rendering anywhere (no font engine in scope).
- No APNG/MP4 container: the PNG frame sequence is the native video primitive;
  a player can assemble frames without re-rendering. Container muxing is a
  separate, explicitly deferred task.
- Waveform PNG pixel equality for audio designs is *attempted* (via §7's sin)
  but the scored bar is §5 (segments/colors/labels); any residual sin-ulp pixel
  diffs are reported, not hidden.

## 9. COMMIT PLAN

1. Freeze this prereg (commit 1: this file).
2. Implement `scenes_inc.zag` + `emit.zag`, build, run the full battery,
   verify, then commit source + `NATIVE_EMIT_RESULTS.md` (hashes, tables,
   PASS/FAIL per emitter). No binaries, no `.zagd`, no `.zag-cache`, no
   bulky artifacts (artifacts live in scratch; their SHA-256s are in the
   results doc).

## 10. SCORED CHECKLIST (for the results doc)

| # | Check | Bar |
|---|-------|-----|
| 1 | PNG validity (Pillow opens, size, mode) | 44/44 (16 + 28 frames) |
| 2 | WAV validity (wave module, frame count) | 12/12 |
| 3 | Rerun byte-identical (SHA-256) | 56/56 |
| 4 | Decoded-RGB diff vs gallery (outside text masks) | 0 differing pixels, 16/16 |
| 5 | Parameter fidelity spot probes | 100% |
| 6 | WAV fundamental ±2 Hz, sample counts exact | 12/12 |
| 7 | Video frame count/order/position/color/motion | 28/28 |
| 8 | scenes_inc.zag byte-identical to imagine.zag bodies | 65/65 |
| 9 | Emitter dump matches logs/q2*.txt | byte-identical |
| 10 | sin accuracy vs math.sin | max err < 1e-12 |
