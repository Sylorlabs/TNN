# Wall-3 residual #5 — root cause: NBINS > TEXLEN crash in `extract_atom_v2.py`

## One-line summary

`NBINS` is the **measured pitch-period length in samples** (`round(sr/f0)`), not a
fixed constant. The texture spectral-shaping step zero-pads the harmonic into a
**fixed 256-sample FFT buffer** (`TEXLEN=256`, the texture-prototype length). Any
source with F0 ≲ 171.9 Hz at 44.1 kHz has a period longer than 256 samples, so
`h_padded[:NBINS] = harm` tries to broadcast an `(NBINS,)` array into a `(256,)`
slice and dies with `ValueError`.

## The exact arithmetic

1. **F0 → T0 → NBINS.** The extractor measures f0 by autocorrelation, then
   `T0 = sr / f0` (measured pitch period, samples). The period-averaged harmonic
   waveform is resampled to `NBINS = int(round(T0))` bins — i.e. **bins per
   period at ~1-sample resolution** (it is a time-domain waveform, not a
   harmonic count; the name is misleading).
2. **The 172 Hz threshold.** All corpus WAVs are 44 100 Hz mono 16-bit.
   `NBINS > 256` ⟺ `round(44100/f0) ≥ 257` ⟺ `f0 < 44100/256.5 ≈ 171.9 Hz`.
   (Python `round()` is half-to-even, so exactly 256.5 rounds down; the
   effective boundary is f0 ≲ 171.9 Hz — the "~172 Hz" in the closure note.)
3. **Why TEXLEN=256 is the bound.** `TEXLEN` is the *texture prototype* length:
   K=8 measured 256-sample residual segments. To shape each prototype by the
   harmonic's spectral envelope, the code needs the harmonic's spectrum on the
   **same 256-point rfft bin grid** as the prototypes, so it zero-pads the
   harmonic into `h_padded = np.zeros(TEXLEN)`:
   ```python
   h_padded = np.zeros(TEXLEN)      # line 211 — fixed 256
   h_padded[:NBINS] = harm          # line 212 — CRASH when NBINS > 256
   H = np.abs(np.fft.rfft(h_padded * np.hanning(TEXLEN)))
   ```
   NumPy slice assignment clamps `h_padded[:551]` to 256 slots while `harm` has
   551 → `ValueError: could not broadcast input array from shape (551,) into
   shape (256,)`.
4. **The coupling is accidental.** NBINS is F0-determined (source property);
   TEXLEN is a texture-design choice. Nothing else in the pipeline couples
   them: the periods matrices, residual scatter loop, transient detection, and
   the atom writer (`struct.pack('<%dd' % NBINS, *harm)`) are all NBINS-agnostic.
   The pad buffer is the **single** point where the two lengths meet.

## Reproduced crash (base script, before fix)

| source | measured f0 | NBINS | base result |
|---|---|---|---|
| synth 80 Hz (deterministic, `test_wavs/synth_80hz.wav`) | 80.0 Hz | 551 | `ValueError: ... shape (551,) into shape (256,)` |
| synth 140 Hz | 140.1 Hz | 315 | `ValueError: ... shape (315,) into shape (256,)` |
| synth 172 Hz | 172.2 Hz | 256 | OK (boundary: fits exactly) |
| synth 200 Hz | 200.0 Hz | 220 | OK |

The crash fires **after** f0 estimation and harmonic averaging succeed — the
harmonic itself is fine; only the texture-shaping buffer overflows.

## Why the battery never hit it

Scanned all 31 `corpus/lowf0/*.wav` with the extractor's own f0 estimator: none
measures below 172 Hz (the stable-voicing window selector locks onto higher
stable regions, e.g. `lowf0-ptdb-000-M09_sa1.wav` → 311.9 Hz despite 82–98 Hz
ground truth in early frames, or fails outright on unvoiced regions). So the
defect is real but was unreachable with these sources — until a genuine
low-F0 voiced source arrives.

## The fix (mechanism-level, in `extract_atom_v2.py`)

Make the **spectral grid adaptive** instead of fixed at 256:

- `SPEC_N = 256` when `NBINS ≤ TEXLEN` — every floating-point op is then
  literally the old expression → **bit-identical output** for all existing atoms.
- Otherwise `SPEC_N` = next power of two ≥ NBINS (fits the harmonic, still ≥
  TEXLEN). The windowed 256-sample texture segment is zero-padded to `SPEC_N`
  (identical time-domain signal — zeros add nothing; the finer grid is just
  denser frequency sampling of the same DTFT), multiplied binwise by the
  harmonic envelope `H/mean(H)` on the common grid, inverse-transformed, and
  truncated back to `TEXLEN`.

`tex` stays K×256, `TEXLEN=256` is written to the atom unchanged, and the
period-averaged harmonic stack is untouched by the edit — **the atom binary
format is unchanged** (magic, version, T0, NBINS, harm, K, TEXLEN, tex, NAMP,
amp_traj, NIMP, imp_pos, imp_amp — same fields, same order).

### Alternatives rejected

- **Raise TEXLEN to 512:** changes `tex` bytes for every existing atom and the
  value the planner reads — violates the no-format-change constraint.
- **Resample the harmonic down to 256 bins before the FFT:** changes the
  envelope (and therefore bytes) for existing atoms; also discards measured
  low-F0 harmonic detail the planner is entitled to.
- **F0-relative binning of the texture:** same byte-change problem, larger
  blast radius.

The chosen fix is the smallest change at the actual coupling point: the FFT
grid exists only to put two spectra on one bin grid, so the grid — not the
data — adapts.

## Coverage

- Organ floor 80 Hz @ 44.1 kHz → NBINS=551 → SPEC_N=1024. ✓ (tested end-to-end)
- Extractor's own f0 floor 60 Hz → NBINS=735 → SPEC_N=1024. Any sample rate:
  SPEC_N grows as needed; memory is trivial (a few KB).
- The f0-estimation and period-validation stages are NBINS-agnostic and were
  already low-F0-safe (autocorr lag range covers 60–600 Hz).

## What this fix does NOT change

- The `estimate_f0_autocorr` / period-validation stages (their pre-existing
  quirks — e.g. some synthetic waveforms fail the 2-zero-crossing check
  identically before and after — are out of scope for this residual).
- The measured semantics: harmonic stack = period-averaged source waveform;
  texture = measured residual segments; mix level 0.15 and REF_RMS=619.8
  level-norm applied exactly as before, after the shaping step.
