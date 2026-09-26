# Raw-Byte Audio Imagination — Method

**Branch:** `tnn-native-lab`. **Date:** 2026-09-26.
**Standing rule (Micah):** audio imagination is raw PCM bytes that TNN manipulates however it wants. No oscillators, partials, envelopes, or filters in the generative path. The old synth (`imagination/src/field.zag`, `emit.zag`) remains as labeled control only.

## Mechanism (`src/rb.zag`, pure Zag, zero RNG)

**Hear** (`hear <wav> <model>`): read mono PCM16 → order-64 LPC via autocorrelation + Levinson-Durbin → residuals → 64-prototype deterministic K-means → residual unigram + order-2 transition table → energy-trajectory prior (mean|res| per 10 ms frame) → pitch period via residual autocorrelation + phase histogram (prototype distribution per pitch-cycle phase). Serialized to a ~2.1 MB `.model` (v4).

**Re-emit** (`reemit`): stored residual-index sequence through the learned LPC filter. Near-transparent (waveform corr 0.99).

**Imagine** (`imagine <model> <dur> <mode>`): TNN's own walk over the transition graph — argmax with row-scaled novelty ledger, energy-trajectory mask + gain, phase-histogram pitch bias — driving the learned LPC filter. Decay mode self-terminates at the learned energy floor; sustain mode holds.

**Scene** (`scene <spec> <wav>`): event timeline → imagined byte blocks → saturated integer mix.

**Selftest** (`selftest`): deterministic reruns + fixture correlation. Returns 129905 on pass.

## Bugs fixed (all found by measurement, not review)

1. Levinson-Durbin in-place coefficient clobber → NaN filter. Fixed with snapshot array; added loud |kk|≥1 guard (rc −17).
2. Model tail f64-view misalignment when residual count ≢ 0 mod 8 → corrupt fields. Fixed with zeroed padding.
3. Predictor state clamped inside the IIR feedback loop → latched −32768. Fixed with separate unclamped float state.

## Evidence

- `~/workspace/your_files/imagination_rawbyte/` — 6 WAVs, `index.html` gallery, `VERDICT.md`, `SHA256SUMS`.
- `~/workspace/rawbyte/abatt.py` — analyzer battery (waveform, HNR, spectra, envelope, drift, loop, onsets, hum, DC, ZCR, closeness).
- `~/workspace/rawbyte/full_battery.json` — full measurements.
- All deliverables byte-identical across rerenders (verified by SHA-256).

## Honest limits

- Imagined strike duller than source (centroid 1310 vs 3252 Hz).
- Imagined cry pitched but "too perfect" (no natural jitter); f0 estimator max-peak artifact (115.7 vs true 347 Hz).
- Walk's 2-sample memory can't natively span pitch periods — phase histogram is a patch. Next step: longer-memory residual model.
