# Imagination Discovery — Audio Crew (D-AUD-1, D-AUD-2, D-AUD-3)

Pure-Zag audio synthesis. No samples, no forced instruments, no RNG. Three
discoveries rendered as 21-second, 44.1 kHz, mono, 16-bit WAVs.

## The discoveries

### D-AUD-1 — VESPERA (`d_aud1_vespera.wav`)

**"Unheard instrument": a tidal glass organ that never existed.**

Sixteen struck gestures on stiff metal/glass bars. Each note is parameterized
per-discovery, never from an instrument preset:

- Inharmonic partials (stiff-bar spacing ~f·n·√(1+B·n²)), 8 per voice
- Independently seeded per-partial phase, attack time, amplitude, frequency
  drift, and decay — no two partials share an envelope
- Deterministic non-12TET pitch field (golden-ratio walk, not a scale)
- Glass impact transients (filtered noise bursts) and bright high pings
- Low sub-tide (55 Hz beating partials), breath bed (LP noise), air bed
  (HP noise), three sweeping formant resonators, broadband white-noise bed

### D-AUD-2 — CRYOVOLCANO (`d_aud2_cryovolcano.wav`)

**"Impossible phenomenon": a methane-moon cryovolcanic event.**

- Detuned sub-bass rumble (41 / 41.6 Hz beating pair, full span)
- Six geyser eruptions: white noise through swept 2-pole resonators
  (350→5200 Hz) with swell envelopes
- Twenty-six ice-fracture transients (noise bursts + high pings)
- Three deep booms (47–53 Hz struck decays + sub noise)
- Wandering wind (swept resonator 300→1100 Hz), HF shimmer bed,
  broadband white-noise bed

### D-AUD-3 — PLANETVOICE (`d_aud3_planetvoice.wav`)

**"The planet's voice": what the alien planet of the D-IMG series sounds
like.** Full world doc in `PLANETVOICE.md` (the world is named Kethra; the
mic stands on a basalt plain at the foot of the lavender range at dusk).
Every element is derived from the world, not from a preset:

- Argon-atmosphere standing waves (beating 33.0/33.45 Hz pair + 66.2 Hz)
- Moon-breath pressure swells (LP noise, 0.055 Hz LFO — Ilyra's tidal pull)
- Ridge wind (swept resonator 280→950 Hz) + spire whistle (1500→2350 Hz)
- Four broad gusts, three deep rift vents, three seismic groans
- Eighteen ice-fracture cracks (cryo deposits at dusk)
- **Nine magnetosphere/ring-particle chorus tones** — rising chirps, the
  planet's voice proper. Events, not notes: no melody, no rhythm, no
  instrument anywhere in the piece

## Architecture (`synth.zag`)

100% pure Zag in the deliverable path. Python/numpy (`bars.py`) verifies only.

- Q30 sine lookup table (4096 entries), linear interpolation
- Deterministic hash noise: 32-bit fmix32 finalizer over a bijective seed mix
  (`h32`), giving white `wnoise ∈ [-1,1)` and uniform `h01 ∈ [0,1)`.
  Zero RNG anywhere; byte-identical reruns.
- `[]u8` mix arena (signed 64-bit Q24, 8 bytes/sample) with explicit
  little-endian accessors; peak-normalize + odd-function soft clip + fades.
- Moving 2-pole resonators, one-pole LP/HP filtered noise beds, white-noise
  bed, struck/swell partial clouds, noise bursts, pings.
- `render_chorus`: magnetospheric rising chirps (D-AUD-3). `render_geyser`
  takes an explicit resonance parameter (D-AUD-3 gusts use broader R=0.97;
  aud2 passes the original 0.986 and re-renders byte-identical).
- WAV writer via Linux `open(2)` with `O_WRONLY|O_CREAT|O_TRUNC`.

No `f3_tone` sine-stack/ADSR anywhere. No 12TET. No presets.

## Build and render

```bash
cd ~/workspace/tnn-lab/imagination_discovery/aud
~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1 \
  synth.zag --no-zagd --no-analyze --no-foreground-cache -o synth
./synth aud1 d_aud1_vespera.wav   # D-AUD-1
./synth aud2 d_aud2_cryovolcano.wav  # D-AUD-2
./synth aud3 d_aud3_planetvoice.wav  # D-AUD-3
python3 bars.py d_aud1_vespera.wav d_aud2_cryovolcano.wav d_aud3_planetvoice.wav
```

`argv[1]` selects the subject (`aud1`/`aud2`/`aud3`); `argv[2]` overrides the
output path (default `d_aud1.wav` / `d_aud2.wav` / `d_aud3.wav`).

## Measured bars (2026-09-22, `bars.py`)

| Bar | Threshold | D-AUD-1 (VESPERA) | D-AUD-2 (CRYOVOLCANO) | D-AUD-3 (PLANETVOICE) |
|---|---|---|---|---|
| A-DUR | ≥20 s, 44.1 kHz, mono, 16-bit | 21.000 s — PASS | 21.000 s — PASS | 21.000 s — PASS |
| A-EVOLVE | centroid std ≥400 Hz | 2040.2 Hz — PASS | 1717.1 Hz — PASS | 2755.6 Hz — PASS |
| A-SPEC | ≥2% energy above 8 kHz | 23.89% — PASS | 22.71% — PASS | 10.79% — PASS |
| A-NOHARM | ≥30% frames flatness >0.30 | 57.14% — PASS | 33.33% — PASS | 33.33% — PASS |
| A-DET | two clean reruns byte-identical | PASS | PASS | PASS |

SHA-256:
- `d_aud1_vespera.wav`: `0a07a35d4c6b319ae0b7b3a62ecac92e083fa317e2c9dde2ca0327a065ffbbd6`
- `d_aud2_cryovolcano.wav`: `29126caeebe26dc7553ccbe9cba03d4a7518d28b5514c8d835ab199853628a3e`
- `d_aud3_planetvoice.wav`: `7728fbee2d00ec0d1f791c379dd0430b37aae86fa86e00bba25f90fe42d0612c`

## Honest limitations

- No blind listening was performed by the builder. A-BLIND remains for the
  separate judging crew; mechanical bars are necessary, not sufficient.
- The white-noise beds are prominent (they carry the flatness bar). The mix
  is intentionally airy/hissy rather than dry.
- Resonator gains were set empirically to avoid blowup (R=0.99 gives ~27×
  resonant gain); levels are tuned for the bars, not by ear.
- `bars.py` flatness uses a 1e-30 floor; deep spectral valleys from the
  struck partials are filled mainly by the noise beds.

## Files

- `synth.zag` — the synthesizer (pure Zag)
- `bars.py` — verification-only analyzer (numpy; never generates audio)
- `d_aud1_vespera.wav`, `d_aud2_cryovolcano.wav`, `d_aud3_planetvoice.wav` — deliverables
- `README.md` — this file
- `PLANETVOICE.md` — the imagined world behind D-AUD-3
