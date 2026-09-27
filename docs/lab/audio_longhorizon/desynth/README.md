# Audio De-Synth: Measured-Timbre Renderer

**Date:** 2026-09-27 (correction of the 2026-09-27 "full complete" claim)
**Status:** Built and tested. NOT quality-passing. See `evidence/BATTERY_VERDICT.md`.

Micah ordered (2026-09-26): "we still gotta redo the things not done yet, make it fully built and test."
This is that work: the five assigned gaps are closed with evidence. What remains is documented as known defects, not claimed as done.

## What this is

The audio planner's synthetic renderer (oscillator + FM + exp10 envelopes + fmix32 jitter) is replaced with a **measured-timbre renderer** built from the phase-3 semantic model:

```
output = measured harmonic stack (period-averaged from real audio)
       + measured per-period amplitude (time-warped, NO exp10)
       + measured texture (residual, spectrally shaped, pitch-synchronous)
       (+ measured transients — DISABLED, see note)
```

**Zero oscillators. Zero FM. Zero synthetic envelopes. Zero RNG** in the planner production path.

## Files

| File | Description |
|------|-------------|
| `src/extract_atom.py` | Extracts a binary measured-timbre atom (format v2) from a real corpus WAV: period-averaged harmonic waveform, per-period RMS trajectory, residual texture prototypes (spectrally shaped), transient peaks (stored but not rendered). v2 REMOVES the LP coefficients. |
| `src/desynth_render.zag` | Standalone pure-Zag renderer (corrected 2026-09-27: requires v2 atoms, unity texture mix, transients honestly disabled, rejects v1). Reads an atom, renders 2.0s PCM16 WAV. No cosr/sinr, no exp10, no fmix32, no FM. |
| `src/render_desynth.zag` | The renderer as a planner module (v2 parser, unity texture mix). |
| `src/render_main.zag` | Minimal driver used to verify the planner-integrated renderer (fixed-plan render byte-identical to battery output). |
| `src/plan_main_desynth.zag` | Full planner with de-synth `render_plan` integrated. Atom-selection semantics (no FM). |
| `src/waveform_check.py` | Basic waveform analyzer (F0, harmonics, envelope, ZC, DC, SHA). |
| `src/waveform_full.py` | Full waveform analyzer used for the verdict (peak/RMS/DC/clipping, 10 ms envelope stats, autocorr f0+HNR, spectrum+peaks, spectral drift, 50/60 Hz bands, ZCR, onsets). |
| `src/find_child_source.py` | Utility that identified the child atom's source WAV (deterministic corpus scan). |
| `evidence/` | Calibration record, target manifest, battery verdict, waveform table, run logs, atom provenance. |

## Atom format v2

v2 removes the 16 LP coefficients. Rationale: the direct period-averaged harmonic waveform already carries the source's spectral coloration; filtering it through LPC would color it twice. The harmonic IS the measured spectral model.

v2 layout: magic, version=2 (u32), T0 (f64), NBINS, harm[NBINS], K, TEXLEN, tex[K*TEXLEN], NAMP, amp_traj[NAMP], NIMP, imp_pos[NIMP], imp_amp[NIMP].

## Completed 2026-09-27 (the five gaps)

### 1. Calibration rewritten (atom f0-bias)
The FM-specific probe logic (depths, gains, tracking frontier) is replaced with an 80-byte, two-timbre table:
- Per timbre: f0-hearing bias at 90, 220, 1010 Hz (measured ppm)
- Measured CV yield at 220 Hz
- Voiced fraction

Calibration results:
- Timbre 0 (child): bias@220Hz = +2054 ppm (+0.21%), voiced 98.8%
- Timbre 1 (speech): bias@220Hz = +5045 ppm (+0.50%), voiced 61.1%

Honesty note: the 90 Hz point is degenerate — the organ hears nothing at 90 Hz for either atom, so `bias90_ppm = 0` is a placeholder. Low-pitch calibration is unanchored. See `evidence/CALIBRATION.md`.

### 2. Planner rebuilt on atom semantics
- `growth_shootout` compares 4 atom candidates (atom0-flat, atom1-flat, atom0-contour, atom1-contour) by predicted error. No FM depth/rate/jitter.
- `plan_case` selects based on atom coverage and contour availability.
- Closed-loop correction adjusts flat f0 or contour mean; envelope mismatch is a coverage finding (not a synth parameter).
- Vocabulary init: A1 = atom0-flat (measured null hypothesis).
- Growth converged: 19/20 targets selected atom0-contour; one (t20) atom0-flat.

### 3. 20-reference closed-loop battery (deep ×2, fresh ×2)
Exact result: `SUMMARY match=0 loop=20 targets=20 actions_grown=2` + `PLAN_DONE`.
`match` counts open-loop M-kind targets; the manifest holds 20 L (loop) targets.
**This is the exact run result, not a quality pass.** Determinism: 80/80 WAVs byte-identical between deep runs; fresh runs likewise. See `evidence/BATTERY_VERDICT.md`.

Per-target final native error: 0–1593 per mille (1 target at 0, 14 carry envelope-mismatch).

### 4. LP coefficients removed (honest)
v1 stored 16 LP coefficients but never applied them. v2 removes the LP block entirely. The measured harmonic waveform is the spectral model; LPC would double-color.

### 5. Texture constants: honest resolution
**Finding:** The period-synchronous residual does NOT isolate a valid texture level. Residual RMS exceeds the source (29–244x ratios, nonsensical) due to harmonic leakage — the subtraction doesn't cancel. A source-measured texture ratio is not obtainable from this decomposition.

**Resolution:** The texture prototypes ARE real source audio (measured segments, spectrally shaped). Their LEVEL is a chosen mix parameter (0.15), not a measured source ratio. v1 used 0.3 (extractor) × 0.5 (renderer) = 0.15 effective. v2 uses 0.15 (extractor) × 1.0 (renderer) = 0.15 effective, preserving the behavior while removing the 0.5 magic number from the render path.

### 6. Transients disabled (honest)
The transient peaks were extracted from the broken residual (170x harmonic RMS for speech). Rendering them as impulses broke voicing detection. Transients are stored in the atom but NOT rendered. Transient extraction requires a fixed residual isolator (future work).

## Validation results

### Standalone renderer

| Test | Result |
|------|--------|
| f0 accuracy @ 220 Hz | 220.5 Hz measured (+0.2% err) |
| Harmonic richness | H1 0dB, H2 -8dB, H3 -18dB (rich, NOT a pure sine) |
| Zero crossings | 882 vs 882 expected (correct voicing) |
| 60 Hz band | −66.9 dB (renderer is clean; no mains hum) |
| Clipping / DC | 0 clipped samples; max \|DC\| 1.61 samples (20 renders) |
| Two runs | byte-identical |

### Battery waveform analysis (20 renders vs 20 refs)

Full table: `evidence/waveform_battery2.tsv`. Analyzer: `src/waveform_full.py`.

| Measure | Renders | References |
|---|---|---|
| Envelope CV (10 ms) | 0.359–0.414 (all targets — the atom's own trajectory) | 0.298–1.922 |
| HNR | −1.3…13.5 dB | −4.2…12.4 dB, mean 2.8 dB |
| ZCR/sec | 114–1950 | 962–8796 |

## Known defects (measured — the actual residual work)

1. **The organ mis-hears low-f0 contour renders, and the closed loop chases the mis-hearing.** Decisive: t17 commanded contour mean 152.5 Hz; independent FFT shows the render's strongest peak at 88 Hz, but the organ heard 221–243 Hz. The `f0-contour-mean-rescale` correction then rescales by the wrong ratio (t1: true render mean 132 → 96 Hz, AWAY from the 150 Hz target). The growth "bias" (+37.5%) is this hearing error misattributed to the timbre. The native `err_pm` scoreboard is compromised for contour actions. Recommended fix: calibrate hearing bias separately from render bias; use the analytically-known contour mean instead of re-hearing render f0.
2. **Render achieves below commanded contour level** (t17: commanded 152.5 Hz mean, achieved ~88 Hz dominant). Contour dips + f0base fallback drag the effective mean down; the level-anchor doesn't fully correct it.
3. **t20: organ octave error on the reference** (true ~105 Hz heard at 890 Hz; the planner faithfully rendered the phantom).
4. **Assembled-runtime trig:** planner sources are clean, but the assembled binary still links `cosr` from `organ_lib.zag` (Hann/DFT tables for the organ's `analyze()`). Strict zero-trig compliance needs a trig-free hearing path. No exception approved.
5. **Envelope mismatch on 14/20 targets:** the 2-atom vocabulary cannot cover the references' envelope variety; no envelope actuator exists by design (synthetic envelopes are banned).
6. **Texture level (0.15) is chosen, not measured.** The residual decomposition cannot validate it.
7. **Transients absent.** Disabled due to broken extraction.

## Atom provenance

- `atom1_speech.bin` (v2): extracted from `audio_longhorizon/corpus/speech/speech-e22-000.wav` — SHA-256 `8ea7e03d8e497c0a517da94f9938241fb4e03b3843b56ec63381a2174af3783f`. Deterministic (identical SHA-256 on rerun).
- `atom0_child.bin` (v2): extracted from `audio_longhorizon/corpus/child/child-fsd50k-171101.wav` — SHA-256 `05f95cf1e225d55073520681452bc6a849e33d55e95214c96f0004aa92d8aeea`. Source identified by deterministic scan of all 52 child-corpus WAVs (harmonic-shape correlation 1.000000; fresh extraction byte-identical). The earlier "source unrecoverable" note was wrong; corrected here.
- Regeneration: `python3 src/extract_atom.py <corpus-wav> <out.atom>`. See `evidence/ATOM_PROVENANCE.md`.

## Action semantics

| amode | Meaning |
|-------|---------|
| 0 | atom0 (child voice), flat f0 |
| 1 | atom1 (speech voice), flat f0 |
| 2 | atom0 (child voice), f0 follows CON (16-pt measured contour) |
| 3 | atom1 (speech voice), f0 follows CON (16-pt measured contour) |

`p1` = amp_scale_pm (1,000,000 = 1.0). `p2..p4` unused.

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
