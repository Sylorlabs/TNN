# VERDICT — Raw-Byte Audio Imagination

**Date:** 2026-09-26. **Mechanism:** pure Zag (`rb.zag`), deterministic, zero RNG.
**Rule:** raw 16-bit PCM bytes only. No oscillators, partials, envelopes, or filters in the generative path.

## The ladder

### (a) Hear / re-emit sealed real sounds — PASS

| Source | Waveform corr | Log-spectral dist | Envelope corr | Onsets | Timing err |
|---|---|---|---|---|---|
| field-fsd50k-10000.wav (strike) | 0.9983 | 0.43 dB | 0.9996 | 1/1 | 0.000 s |
| child-fsd50k-416689.wav (vowel) | 0.9948 | 2.22 dB | 0.9994 | 5/5 | 0.001 s |

The machinery carries raw bytes faithfully. Re-emission is near-transparent.

### (b) Imagine single events — PASS with honest gaps

**Strike** (decay mode): attack 0.07 s (src 0.04), peak 3948 (src 3797), natural decay to silence, self-terminates at 0.358 s (src 0.428). **Gap:** duller — centroid 1310 vs 3252 Hz. The walk favors lower-frequency prototypes.

**Cry** (sustain mode, 1.2 s): peak 11997 (src 12316), attack 0.15 s (src 0.17), HNR +2.21 dB (src +3.68) — genuinely pitched. 347 Hz present (autocorr 0.62 at lag 127). **Gaps:** (1) the analyzer's max-peak f0 estimator reports 115.7 Hz — a harmonic artifact of strong multiples; (2) the periodicity is "too perfect" — harmonic multiples stay flat (0.62/0.62/0.63/0.61) while the source's decay with multiple (0.70/0.64/0.56/0.41) from natural pitch jitter. The phase prior enforces an exact 127-sample period with no jitter.

**Clang** (decay mode): centroid 7438 vs 7657 Hz, attack 0.07 s both, 3/3 onsets, peak 17356 vs 14992. Strong match.

### (c) Forge scene from event timeline — PASS

strike → clang → strike → clang → strike at 0.0/0.3/1.0/1.3/2.0 s. 3.0 s, no clipping, DC inaudible. Events are byte-identical across renders (deterministic), placed as raw byte blocks, saturated integer mix.

## Determinism

All six deliverables re-rendered byte-identical (SHA-256 match). `selftest` returns 129905 (deterministic reruns + fixture correlation 0.99).

## What raw bytes can and cannot do

**Can:** re-emit heard sounds transparently; imagine transient events with learned attack/decay/termination; imagine pitched events via learned periodicity; compose scenes from timelines.

**Cannot yet:** match source high-frequency brightness (walk biases low); produce natural pitch jitter; invent timbres outside the learned set; represent pitch-period structure natively (needs the phase-prior patch).

## White-box reason

The residual walk is order-2 Markov (2-sample memory). Pitch lives at 127 samples, jitter at 100s of samples — both far beyond the walk's memory. The energy-trajectory prior and phase histogram are learned patches over this structural memory gap. The LPC(64) filter captures formants but not pitch (P=64 < 127), so periodicity must be carried by the excitation walk. Fixing this properly needs a longer-memory residual model (skip-order Markov or hierarchical walk) — the defined next step.

## Bugs found and fixed (white-box)

1. **Levinson in-place clobber:** the coefficient update read already-mutated values → NaN filter → railed output. Fixed with a snapshot array + loud |kk|≥1 guard.
2. **Model tail misalignment:** residual count not a multiple of 8 → f64 view wrote to wrong bytes → corrupt onsets. Fixed with zeroed padding.
3. **Predictor feedback clamp:** clamping inside the IIR loop latched the state to −32768. Fixed with separate unclamped float state.

## Raw-vs-synth delta

| Capability | Raw-byte | Synth (oscillator control) |
|---|---|---|
| Learn from real audio | Yes | No |
| Re-emit heard sound | Yes (corr 0.99) | No |
| Transient events | Yes (learned) | Weak (unlearned noise) |
| Pitched events | Partial (too perfect) | Yes (designed) |
| HF brightness | Weak (duller) | Yes (precise partials) |
| Novel timbres | Limited (recombination) | Yes (new strokes) |

The synth was never designed for strike/cry/forge events (its outputs are sustained fields/moods); the comparison is at the capability level. The two paths are complementary, not competing.

## Files

All WAVs + `index.html` + `SHA256SUMS` in this directory. Code: `~/workspace/tnn-lab/imagination_rawbyte/src/rb.zag` (branch `tnn-native-lab`). Analyzer: `~/workspace/rawbyte/abatt.py`. Battery JSON: `~/workspace/rawbyte/full_battery.json`.
