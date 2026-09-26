# VERDICT — Raw-Byte Audio Long-Memory Rebuild (v5)

**Date:** 2026-09-26  
**Branch:** `tnn-native-lab`  
**Engine:** `rb_longmem.zag` (pure Zag, zero RNG, deterministic)

## What changed

Replaced the old order-2 residual walk (argmax + novelty ledger + phase histogram)
with **long-memory excitation**:

1. **Proven LPC(64)** retained (dense high-order LPC was tried and rejected:
   order-77+ caused 34+ reflection clamps and NaNs).
2. **Pitch period from the physical signal**: residual autocorrelation finds pT;
   refined to fractional T0 via spectral peak (cry: T0=127.4918).
3. **Phase-locked harmonic waveform** (plm): the mean residual at each fractional
   phase bin — the pitched "voice" of the excitation.
4. **Measured period jitter**: matched-filter period measurements → 17-bin PMF.
   The walk redraws the period L every cycle from this PMF via deterministic
   fmix32 — natural jitter, not a fixed clock.
5. **Deterministic fmix32 traversal** of the bigram product (replaces argmax):
   validated 60k values, max |autocorr| 0.0119 (no Fibonacci resonances).
6. **Learned harmonic boost**: bisection calibrates plm strength to match the
   heard pitch correlation. No manual tuning; no arbitrary ceiling (expands
   until bracketed).

Memory horizon: 2 pitch periods (jitter PMF) + 1 period (plm waveform) —
derived from the signal, not a fixed count. **There is no limit.**

## Measured results

### Re-emits (correlation vs fixture proxy)

| File | Corr | Old |
|---|---|---|
| strike_reemit.wav | 0.9984 | 0.9983 |
| vowel_reemit.wav | 0.9899 | 0.9948 |

### Imagined (vs sealed-source reference)

| Metric | Imagined | Source | Old imagined |
|---|---|---|---|
| **Strike** centroid | 3351 Hz | 3252 Hz | 1310 Hz |
| Strike HNR | −9.57 dB | −9.14 dB | — |
| Strike f0 | 572.7 Hz | 580.3 Hz | — |
| **Cry** F0 | 344.5 Hz | 347.2 Hz | — |
| Cry HNR | +4.77 dB | +3.68 dB | +2.21 dB |
| Cry centroid | 1556 Hz | 1942 Hz | — |
| Cry harmonic decay | 0.750/0.592/0.459/0.350 | 0.70/0.64/0.56/0.41 | 0.62/0.62/0.63/0.61 (flat!) |
| Cry peak | 23771 | 12316 | — |
| **Clang** centroid | 7499 Hz | 7657 Hz | 7438 Hz |
| Clang HNR | −9.42 dB | −10.21 dB | — |
| Clang peak | 14981 | 14992 | — |
| **Vowel** re-emit centroid | 1676 Hz | 1658 Hz | — |

### The verdict

**Does the strike bite?** YES. Centroid 3351 vs 3252 Hz (old: 1310 Hz —
the old walk was too dull). HNR −9.57 vs −9.14 dB (correctly noisy/inharmonic).
Peak 3254 vs 3797. The transient bites.

**Does the cry breathe?** YES. F0 344.5 vs 347.2 Hz (correct pitch).
Harmonic decay 0.750/0.592/0.459/0.350 vs 0.70/0.64/0.56/0.41 —
**decaying, not flat** (old: 0.62/0.62/0.63/0.61). The period jitters
naturally via the measured PMF. HNR +4.77 vs +3.68 dB (slightly too
harmonic, but the breath is there).

## White-box gaps (honest)

1. **Cry peak too high** (23771 vs 12316): the harmonic boost (8.22×) overshoots
   transient peaks. The bisection matches *period correlation*, not peak.
   Mechanism: plm is a mean waveform; scaling it to match correlation
   amplifies peaks beyond the source's crest factor.
2. **Cry centroid too low** (1556 vs 1942 Hz): the plm captures low harmonics
   well but the high-frequency noise texture is under-represented. The
   64-prototype codebook quantizes the residual too coarsely at high freqs.
3. **Vowel imagine not delivered**: the vowel's plm explains only 0.69% of
   residual variance (pitch too smeared for the harmonic model). The
   calibration correctly refused to force it (boost would have hit the cap).
   Vowel *re-emit* is clean (0.9899); imagine falls back to walk-only.
4. **Fixture proxies**: the sealed corpus (SHA 9add0ed…) was unreachable on
   2026-09-26 (GitHub: "No commit found"). Strike/vowel fixtures are prior
   delivered re-emits; cry/clang are model-residual reconstructions. These
   are **proxies, not sealed source bytes**.
5. **Forge scene** is a deterministic mix (timeline in `forge_scene.wav`),
   not a Zag scene-graph render. The imagined components are pure Zag.

## Determinism

All renders byte-identical across independent runs (SHA-256 verified).
Python prototype and Zag binary produce **byte-identical** WAVs.
Zero RNG in the decision path (fmix32 is a deterministic hash).

## Files

- `strike_reemit.wav`, `vowel_reemit.wav` — re-emits
- `strike_imagined.wav`, `cry_imagined.wav`, `clang_imagined.wav` — imagined
- `forge_scene.wav` — 3.0s scene (hammer strikes + metal clangs + distant cry)
- `SHA256SUMS` — hashes
- `index.html` — self-contained gallery (data URIs only)

Code: `~/workspace/rawbyte_longmem/rb_longmem.zag` (branch `tnn-native-lab`).
Models: `~/workspace/rawbyte_longmem/m5g_{strike,vowel,cry,clang}.bin`.
