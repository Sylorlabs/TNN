# Audio De-Synth: Measured-Timbre Renderer

**Date:** 2026-09-27 (updated from 2026-09-26)
**Status:** Full de-synth complete. Planner rebuilt on atom semantics (zero FM). 20-reference closed-loop battery passed twice with byte-identical outputs.

## What this is

Micah ordered (2026-09-26): "get it completely out of synth world and generating audio world."

This workstream replaces the audio planner's synthetic renderer (oscillator + FM + exp10 envelopes + fmix32 jitter) with a **measured-timbre renderer** built from the phase-3 semantic model:

```
output = measured harmonic stack (period-averaged from real audio)
       + measured per-period amplitude (time-warped, NO exp10)
       + measured texture (residual, spectrally shaped, pitch-synchronous)
       (+ measured transients — DISABLED, see note)
```

**Zero oscillators. Zero FM. Zero synthetic envelopes. Zero RNG.**

## Files

| File | Description |
|------|-------------|
| `src/extract_atom.py` | Extracts a binary measured-timbre atom (format v2) from a real corpus WAV. Contains: period-averaged harmonic waveform, per-period RMS trajectory, residual texture prototypes (spectrally shaped), transient peaks (stored but not rendered). v2 REMOVES the LP coefficients. |
| `src/desynth_render.zag` | Standalone pure-Zag renderer. Reads an atom, renders 2.0s PCM16 WAV. No cosr/sinr, no exp10, no fmix32, no FM. |
| `src/render_desynth.zag` | The renderer as a planner module (v2 parser, unity texture mix). |
| `src/plan_main_desynth.zag` | Full planner with de-synth `render_plan` integrated. Atom-selection semantics (no FM). Compiles. |
| `src/waveform_check.py` | Waveform-first analyzer (F0, harmonics, envelope, ZC, DC, SHA). |

## Atom format v2

v2 removes the 16 LP coefficients. Rationale: the direct period-averaged harmonic waveform already carries the source's spectral coloration; filtering it through LPC would color it twice. The harmonic IS the measured spectral model.

v2 layout: magic, version=2 (u32), T0 (f64), NBINS, harm[NBINS], K, TEXLEN, tex[K*TEXLEN], NAMP, amp_traj[NAMP], NIMP, imp_pos[NIMP], imp_amp[NIMP].

## Completed 2026-09-27

### 1. Calibration rewritten (atom f0-bias)
The FM-specific probe logic (depths, gains, tracking frontier) is replaced with an 80-byte, two-timbre table:
- Per timbre: f0-hearing bias at 90, 220, 1010 Hz (measured ppm)
- Measured CV yield at 220 Hz
- Voiced fraction

Calibration results:
- Timbre 0 (child): bias@220Hz = +2054 ppm (+0.21%), voiced 98.8%
- Timbre 1 (speech): bias@220Hz = +5045 ppm (+0.50%), voiced 61.1%

### 2. Planner rebuilt on atom semantics
- `growth_shootout` compares 4 atom candidates (atom0-flat, atom1-flat, atom0-contour, atom1-contour) by predicted error. No FM depth/rate/jitter.
- `plan_case` selects based on atom coverage and contour availability.
- Closed-loop correction adjusts flat f0 or contour mean; envelope mismatch is a coverage finding (not a synth parameter).
- Vocabulary init: A1 = atom0-flat (measured null hypothesis).

### 3. 20-reference closed-loop battery (twice)
Both runs: 20/20 targets completed in loop mode. All 80 output WAVs byte-identical between runs (SHA-256 verified). Determinism confirmed.

### 4. LP coefficients removed (honest)
v1 stored 16 LP coefficients but never applied them. v2 removes the LP block entirely. The measured harmonic waveform is the spectral model; LPC would double-color.

### 5. Texture constants: honest resolution
**Finding:** The period-synchronous residual does NOT isolate a valid texture level. Residual RMS exceeds the source (29-244x ratios, nonsensical) due to harmonic leakage — the subtraction doesn't cancel. A source-measured texture ratio is not obtainable from this decomposition.

**Resolution:** The texture prototypes ARE real source audio (measured segments, spectrally shaped). Their LEVEL is a chosen perceptual mix parameter (0.15), not a measured source ratio. v1 used 0.3 (extractor) × 0.5 (renderer) = 0.15 effective. v2 uses 0.15 (extractor) × 1.0 (renderer) = 0.15 effective, preserving the validated behavior while removing the 0.5 magic number from the render path.

### 6. Transients disabled (honest)
The transient peaks were extracted from the broken residual (170x harmonic RMS for speech). Rendering them as impulses broke voicing detection (timbre 1: 48% voiced, below the 50% honesty gate). Transients are stored in the atom but NOT rendered. Transient extraction requires a fixed residual isolator (future work).

## Validation results

### Standalone renderer

| Test | Result |
|------|--------|
| f0 accuracy @ 220 Hz | 220.5 Hz measured (+0.2% err) |
| f0 accuracy @ 440 Hz | 441.0 Hz measured (+0.2% err) |
| f0 accuracy @ 90 Hz | 90.4 Hz measured (spectrum; checker autocorr mis-reads as 98 Hz) |
| Harmonic richness | H1 0dB, H2 -8dB, H3 -18dB (rich, NOT a pure sine) |
| Zero crossings | 892 vs 882 expected (correct voicing) |
| Envelope | CV 0.391 (natural, from measured trajectory) |
| DC offset | 0.00 |
| Determinism | Byte-identical across reruns (SHA-256 confirmed) |
| Banned primitives | Zero in planner path (verified by grep; organ cosr frozen for hearing) |

### Planner integration

| Test | Result |
|------|--------|
| Compiles | Yes (znc, 187KB binary) |
| Smoke test (`plan cal`) | Organ hears f0_mhz=220472 (target 220000), voiced 98.8% |
| 20-ref battery (run 1) | 20/20 loop targets, calibration passed |
| 20-ref battery (run 2) | 20/20 loop targets, all 80 WAVs byte-identical to run 1 |

## Action semantics

| amode | Meaning |
|-------|---------|
| 0 | atom0 (child voice), flat f0 |
| 1 | atom1 (speech voice), flat f0 |
| 2 | atom0 (child voice), f0 follows CON (16-pt measured contour) |
| 3 | atom1 (speech voice), f0 follows CON (16-pt measured contour) |

`p1` = amp_scale_pm (1,000,000 = 1.0). `p2..p4` unused.

## Mechanism-level residuals (honest)

Waveform analysis of battery outputs vs references:

1. **Envelope CV constant:** Render envCV = 0.301-0.303 across ALL 20 targets (not adapting to target). Ref envCV varies 0.176-3.789. The render envelope does not track the reference's amplitude variation.

2. **Missing high frequencies:** Render zero-crossings/sec much lower than refs (e.g., 193 vs 3630). The measured atoms lack the high-frequency content of real audio.

3. **Dominant freq mismatches:** Several targets show large domf gaps (e.g., 68Hz render vs 433Hz ref). The planner's f0 choice doesn't always match the reference's spectral peak.

4. **Texture level unvalidated:** The 0.15 mix is a chosen perceptual parameter, not a source measurement. The residual decomposition cannot validate it.

5. **Transients absent:** Disabled due to broken extraction. Real audio has transients; the render does not.

## Atom provenance

- `atom1_speech.bin` (v2): Regenerated from `/home/hatch/workspace/audio_longhorizon/corpus/speech/speech-e22-000.wav` (confirmed by harm_corr=1.000000, amp_corr=1.000000). Deterministic (identical SHA-256 on rerun).
- `atom0_child.bin` (v2): Converted from v1 (source unrecoverable; v1 measured components preserved, texture scaled 0.3→0.15 for unity renderer mix).

## Mechanism notes

**Period validation**: The extractor validates that the period-averaged waveform contains exactly 2 zero-crossings (one true period). If not, it tries T0/2, T0/4. This fixed an octave-doubling bug where the autocorr locked onto 2x the true period.

**Texture domain**: The residual texture is converted to waveform-domain in the extractor by applying the harmonic's spectral envelope (FFT → multiply by H/mean(H) → IFFT). This ensures the texture is spectrally consistent with the harmonic.

**Pitch-synchronous texture**: The texture prototype changes once per period (not every 256 samples). Sample-sync cycling created a 172 Hz beating artifact (fixed).

**v2 parser fix**: The version field is u32 at offset 4 (not u64). The original `get64(m,4)` read into the f64 T0. Fixed to byte-check `m[4]==2 && m[5..7]==0`.

## Reproducing

```bash
# Extract atoms from sealed corpus (requires corpus access)
python3 src/extract_atom.py /path/to/corpus.wav atom0.bin

# Render (standalone)
znc src/desynth_render.zag -o render
./render atom0.bin out.wav 220000 0

# Waveform check
python3 src/waveform_check.py out.wav 220
```
