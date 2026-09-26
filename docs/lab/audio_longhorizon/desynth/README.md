# Audio De-Synth: Measured-Timbre Renderer

**Date:** 2026-09-26
**Status:** Renderer complete and validated. Planner integration compiles and passes smoke test. Full deliberative loop adaptation is future work.

## What this is

Micah ordered (2026-09-26): "get it completely out of synth world and generating audio world."

This workstream replaces the audio planner's synthetic renderer (oscillator + FM + exp10 envelopes + fmix32 jitter) with a **measured-timbre renderer** built from the phase-3 semantic model:

```
output = measured harmonic stack (period-averaged from real audio)
       + measured per-period amplitude (time-warped, NO exp10)
       + measured texture (residual, spectrally shaped, pitch-synchronous)
       + measured transients (peaks at measured positions)
```

**Zero oscillators. Zero FM. Zero synthetic envelopes. Zero RNG.**

## Files

| File | Description |
|------|-------------|
| `src/extract_atom.py` | Extracts a binary measured-timbre atom from a real corpus WAV. Contains: period-averaged harmonic waveform, per-period RMS trajectory, residual texture prototypes (spectrally shaped to waveform domain), transient peaks, LP coefficients (stored but not yet applied). |
| `src/desynth_render.zag` | Standalone pure-Zag renderer. Reads an atom, renders 2.0s PCM16 WAV. No cosr/sinr, no exp10, no fmix32, no FM. |
| `src/render_desynth.zag` | The renderer as a planner module (replaces `render_plan` in plan_main.zag). |
| `src/plan_main_desynth.zag` | Full planner with de-synth `render_plan` integrated. Compiles. Basic smoke test passes. |
| `src/waveform_check.py` | Waveform-first analyzer (F0, harmonics, envelope, ZC, DC, SHA). |

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
| Banned primitives | Zero (verified by grep: no cosr/sinr/exp10/fmix32) |

### Planner integration

| Test | Result |
|------|--------|
| Compiles | Yes (znc, 192KB binary) |
| Smoke test (`plan cal`) | Organ hears f0_mhz=220472 (target 220000), voiced 98.8% |
| Waveform of planner output | 220.5 Hz, +0.2% err, harmonics correct |

## Action semantics (new)

The old synth presets (vib1/vib2/jitter/contour as FM modulators) are replaced:

| amode | Meaning |
|-------|---------|
| 0 | atom0 (child voice), flat f0 |
| 1 | atom1 (speech voice), flat f0 |
| 2 | atom0 (child voice), f0 follows CON (16-pt measured contour) |
| 3 | atom1 (speech voice), f0 follows CON (16-pt measured contour) |

`p1` = amp_scale_pm (1,000,000 = 1.0). `p2..p4` unused.

The `env`/`slope_db` parameters are now coverage signals: if the atom's measured envelope doesn't match the reference, it's a vocabulary growth finding (need a different atom), not a parameter to synthesize.

## What remains (future work)

1. **Full calibration rewrite**: `cal_run` still contains FM-specific probe logic (depths, gains, tracking frontier). Needs replacement with atom f0-bias measurement.
2. **Vocabulary semantics**: `plan_case` and `growth_shootout` still use FM action selection. Need adaptation to atom selection (which timbre? flat or contour?).
3. **20-ref battery**: The full closed-loop battery has not been run with the new renderer. The applicable pass bars (hearability, determinism) are met; the FM-specific bars (vibrato gain, etc.) are obsolete.
4. **LP coefficients**: Stored in the atom but not applied. Either use them correctly or remove from the model.
5. **Texture mix**: The 0.5 texture weight and 0.3 normalization ratio are measured approximations; validate against more references.

## Mechanism notes

**Period validation**: The extractor validates that the period-averaged waveform contains exactly 2 zero-crossings (one true period). If not, it tries T0/2, T0/4. This fixed an octave-doubling bug where the autocorr locked onto 2x the true period.

**Texture domain**: The residual texture is converted to waveform-domain in the extractor by applying the harmonic's spectral envelope (FFT → multiply by H/mean(H) → IFFT). This ensures the texture is spectrally consistent with the harmonic. Adding residual-domain texture directly to waveform-domain harmonic created inharmonic beating (fixed).

**Pitch-synchronous texture**: The texture prototype changes once per period (not every 256 samples). Sample-sync cycling created a 172 Hz beating artifact (fixed).

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
