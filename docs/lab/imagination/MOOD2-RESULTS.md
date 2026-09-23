# MOOD-2 results: hi-fi synth (Phase 1 COMPLETE) + mood probe (Phase 2 READY)

Date: 2026-09-22. Task: Micah's correction — the 8 kHz audio sounded distorted
("dollar tree mic") and the horror quality was suspected to be distortion, not composition.

## Phase 1 verdict: PASS — clean 44.1 kHz synth built, verified, shipped

### What was wrong with the old audio (measured, not guessed)

| # | Defect | Evidence | Likely audible effect |
|---|---|---|---|
| B1 | **Half-wave rectification**: `f3_get32` reads mix words unsigned; emitters used it for peak/abs/scale, so negative half of every sine mapped to near-full-scale positive, positive half crushed to ~0 | Legacy f3song.wav: min=0, max=28000, **zero** zero-crossings, DC mean 0.42 | Harsh, buzzy, "cheap mic" — the dominant distortion |
| B2 | **Mistuned semitone constant**: 1117040/1048576 = +9.5¢/semitone, compounding (octave rendered 235 Hz not 220; fifth 66¢ sharp) | Computed from source; contradicted the file's own "bin b → 110·2^(b/12)" contract | Eerie, detuned, "horror" intervals |
| B3 | 8 kHz sample rate, Nyquist 4000 Hz | By design | Telephone muffle |
| — | 62.5 ms energy stair-steps (16 Hz zipper) | Code inspection (metric inconclusive: legacy 0.39 vs hi-fi 0.06–0.89) | Roughness on swells |
| — | Sine-LUT | **Exonerated**: correct values, −90 dB quantization, Nyquist-capped harmonics | Not a distortion source |

B1+B2 together explain both halves of Micah's report: "dollar tree mic" (B1 rectification)
and "horror movie" (B2 stretched intervals + B1 harshness). The creepy quality of f3song
was, as he suspected, substantially caused by the synth — not purely the composition.

### The hi-fi path (pure Zag, native, deterministic)

- `f3_synth_hifi` / `f3_emit_wav_hifi` in `imagination/src/field.zag`; legacy 8 kHz path
  untouched (AVI determinism preserved).
- 44100 Hz / 16-bit / mono; per-sample envelope interpolation; sub-unit phase
  (<0.5¢ detune); exact 12-TET tuning (1110928); Nyquist cap 22050 Hz; sign-extending
  mix reads (`f3_get32s`); peak normalize to 24000 (0.73 FS) — clipping impossible by
  construction; 0.125 s release tail.
- Command: `mood_bin f3hifi <dir>` → f3song_hifi.wav + 3 mood pieces.

### Verification (all PASS)

| Bar | Check | Result |
|---|---|---|
| H1 | Byte-identical reruns (SHA-256) | 4/4 files identical across 2 clean runs |
| H2 | WAV headers | 44100 Hz / 16-bit / mono, exact frame counts |
| H3 | No clipping | 0 rail samples; peak exactly 24000 on all 4 |
| H4a | Correct tuning | Rendered peaks at exact 12-TET: 130.8 / 261.6 / 349.2 / 392.0 / 523.3 / 659.3 / 784.0 Hz |
| H4b | Voice separation | Peak prominence 19.8 / 31.1 dB (bar ≥12) |
| H4c | No 16 Hz zipper sideband | 0.06–0.89 (bar <1.0) |
| H5 | Bipolar, no DC | 53k–69k negative samples/file; DC mean ≤0.0002 |

### Shipped artifacts (deterministic, hashes verified after copy)

| File | SHA-256 | Duration |
|---|---|---|
| `imagination_audio/f3song_hifi.wav` | `0af6a284942f7a0eae23321a7c8bbc8c3eba80e14217f3b873c8813cadc48a08` | 2.63 s |
| `imagination_audio/f3mood_happy.wav` | `d774f4a4b6f76def9827e876893f63eaa7e79ceab20e3d5209df74d7e71d8dba` | 2.94 s |
| `imagination_audio/f3mood_scary.wav` | `8f7466e94576c0f4ca2ef065e7fe980174d3f4b2fb2214a79017eb29b74cde15` | 3.13 s |
| `imagination_audio/f3mood_calm.wav` | `b582ff7be98ba4be1f6e851ef0c1f10dc5ae78a824667cde7587c924174e6428` | 3.13 s |

## Phase 2: READY — awaiting Micah's ears (binding)

Question (a) — *did the hi-fi re-render change the perceived mood of f3song?*
→ Only Micah can answer. The composition is identical (same field strokes, same bins);
only the synth changed. If f3song_hifi no longer sounds creepy, the horror was B1+B2.

Question (b) — *can TNN hit intended moods through a clean synth?*
→ The three mood pieces use the same preregistered compositions as MOOD-1
(intent frozen in MOOD-PREREG.md), rendered through the clean synth. Blind rating:
which file is HAPPY / SCARY / CALM? Bars: 3/3 = PASS, 2/3 = PARTIAL, ≤1/3 = FAIL.

Note: MOOD-1's acoustic measurements (centroid order etc.) were taken on the rectified
synth and are discarded; only the compositions and intent labels carry over.

## Known defect left for follow-up (not silently changed)

Legacy `f3_emit_wav` and `f3_emit_avi` still half-wave-rectify (B1). All previously
shipped 8 kHz WAVs and the 8 AVI soundtracks carry the distortion. Recommended:
re-render AVIs through the hi-fi path + re-verify, on Micah's word (changes shipped bytes).
