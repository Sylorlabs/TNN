# VERDICT — Audio Intake Fidelity (2026-09-26)

**Question:** how faithfully does TNN take in real PCM audio — what samples go in
vs what the intake holds — before any imagination or reasoning.
**Branch:** `tnn-native-lab`. **Method:** analyzer-first (every claim below is a
waveform/spectrum measurement; SHAs recorded).

## 1. Intake machinery found

Two intake paths exist. Both were measured; the long-memory line is primary
because the coordinator's question (the strike/cry gaps) belongs to it.

### 1a. Long-memory v5g intake (the line behind the strike/cry numbers)

- **PCM parse:** `read_wav` in `~/workspace/rawbyte_longmem/proto5b.py`
  (chunk-aware RIFF walk, asserts PCM16/mono/44.1k, `np.int16` signed,
  channel-0 if stereo). **Sample-exact: no sign trap, no resampling, no
  dither, no normalization.** DC and peak levels preserved.
- **Hearing:** `hear()` in `~/workspace/rawbyte_longmem/proto5g.py` —
  fixture WAV → LPC(64) (Levinson) → residual → pitch (autocorr lags
  50..sr/20) → fractional T0 (spectral refine) → phase-locked mean `plm`
  (NBINS bins) → period-jitter PMF (17 bins) → K-means K=64 on the noise
  residual → bigram(64³), onset bigram, envelope profile, floor/attack →
  boost bisection calibration.
- **Held representation:** `m5g_{strike,vowel,cry,clang}.bin`
  (format `RBLMEMv5`; built via `npz_to_bin.py`): a[64] f64, proto[64] f64,
  bg[64³] u64, ob0/ob1, floor/attack f64, EP frames, pT u64, T0 f64,
  NBINS u64, plm[NBINS] f64, PMF[17] f64, boost f64, score q (u64 per
  residual sample).
- **Read-back (pure Zag):** `rb_longmem.zag` mode 9
  (`~/workspace/rawbyte_longmem/rb_longmem.zag`), rebuilt from source with
  the pinned toolchain `znc_linux_x86_64_abed8aa1` → **byte-identical binary
  (SHA-256 7206eae3adb82f81c6fff5da7f1e2f53b9d34116a844310be851a2c918f51824)**.
  Mode-9 re-emits are byte-identical across runs (4/4 clips, r1==r2 SHAs).
  A Python replication of the exact mode-9 algorithm is **sample-identical**
  (max|diff| = 0.0) to the Zag binary — the read-back path is verified.

### 1b. Crew-P input organ (the standing forward sense)

- **PCM parse:** `wav_parse` + `get_s16` in
  `~/workspace/audio_principles/crew_p/organ.zag` (pure Zag). Chunk-aware,
  requires PCM16/mono/44100, **correct sign extension**
  (`v>=32768 → v−65536`; the f3_get32 unsigned trap is NOT present),
  sample-exact `dsamp=(off+8)/2` bookkeeping. Intake holds full 16-bit
  samples as i64; loss enters only at the descriptor stage (f0/rms/zcr/bands/
  envelope/onsets) — by design, it is a perceptual organ, not a store.

## 2. Fidelity measurements

Source = `fixture_{clip}.wav` (the v5 "source proxies"; SHAs below).
Held = mode-9 re-emit from `m5g_*.bin` via the Zag binary (2 runs, SHA-pinned).
Downstream = `*_imagined.wav` from the delivered gallery
(`~/workspace/your_files/rawbyte_longmem_NEW/`).

### 2a. Is the round-trip bit-exact? No — and here is exactly how lossy.

| clip | samples | max\|diff\| (LSB) | RMS diff | correlation |
|---|---|---|---|---|
| strike | 18,856 | 503 | 41.3 | 0.99836 |
| cry | 16,487 | 14,972 | 1070.2 | 0.89618 |
| clang | 17,608 | 2,814 | 118.1 | 0.99596 |
| vowel | 29,988 | 560 | 97.9 | 0.98985 |

### 2b. The coordinator's question: intake vs downstream for the long-memory gaps

Spectral centroid (Hz), same FFT method on all three legs:

| clip | fixture (source) | re-emit (intake-held) | imagined | intake Δ | downstream Δ | verdict |
|---|---|---|---|---|---|---|
| strike | 3245.9 | 3231.4 | 3351.3 | **−14.5** | **+119.9** | gap is downstream |
| cry | 1940.4 | 1976.5 | 1555.6 | **+36.1** | **−420.9** | gap is downstream |
| clang | 7665.1 | 7670.9 | 7498.9 | **+5.8** | **−172.0** | gap is downstream |
| vowel | 1652.0 | 1676.1 | (refused) | **+24.1** | — | intake only |

F0 via YIN (Hz):

| clip | fixture | re-emit | imagined | intake Δ | downstream Δ |
|---|---|---|---|---|---|
| cry | 346.8 | 346.8 | 345.0 | **0.0** | −1.8 |
| strike | 577.7 | 577.5 | 575.7 | −0.2 | −1.8 |
| vowel | 319.1 | 319.0 | — | −0.1 | — |
| clang | 68.9 | 68.9 | 130.6 | 0.0 | octave-class error |

**F0 intake is essentially perfect (≤0.2 Hz on every clip). Every F0 gap is
downstream** (the imagine walk's jitter PMF / period redraw / bigram statistics).

Peak (int16):

| clip | fixture | re-emit (intake-held) | imagined |
|---|---|---|---|
| strike | 3305 | 3126 | 3254 |
| **cry** | **12442** | **23834 (1.92×)** | 23771 |
| clang | 14220 | 15245 | 14981 |
| vowel | 4463 | 4317 | — |

**The cry peak overshoot is already baked into the held representation**
(re-emit 23834 ≈ imagined 23771). It is an INTAKE-side defect, not a renderer
defect — see §3.

### 2c. Band-energy fingerprints (fraction of total power)

- **Strike:** intake holds the spectrum (0–2k .4815→.4845, 2–8k .4841→.4815,
  8–16k .0343→.0340). Downstream brightens 2–8k (.4815→.5058): the walk's
  prototype draws carry more mid-band energy than the source noise → +120 Hz.
- **Cry:** intake holds it (2–8k .5578→.6032). Downstream collapses 2–8k
  (.6032→.1969) into 0–2k (.3965→.8031): the harmonic boost concentrates
  energy in low harmonics while the walk's noise part is too dull → −421 Hz.
- **Clang:** intake holds it (8–16k .3786→.3797). Downstream shaves 8–16k
  (.3797→.3475) → −172 Hz.

Hum/tonal (50/60 Hz + harmonics energy fraction): ≤0.0033 on all legs, no
mains contamination introduced by intake or renderer.

## 3. White-box: every lossy point, with mechanism and class

Ranked by measured contribution (cry, the worst clip):

### L1. Fabricated 64-sample head — MACHINERY BUG (dominant for cry peak)

`hear()` computes residuals only for samples P..n−1; the first P=64 samples
are never quantized or stored. Mode-9 re-emit fills samples 0..63 with
`proto[q[0..63]]` — indices fit to samples 64..127, a different signal region
(attack transient vs settled tone for the cry). The cry's LPC(64) is highly
resonant (impulse peak gain **8.93**); the wrong initial state rings into a
transient that peaks at **23834 vs the 12442 fixture peak (1.92×)**.

**Proof by ablation** (Python, exact Zag algorithm, sample-identical to binary):

| variant | peak | corr vs fixture | err RMS |
|---|---|---|---|
| A. as built | 23834 | 0.89618 | 1070 |
| B. plm phase fixed only | 23580 | 0.98581 | 400 |
| C. phase fixed + TRUE head samples | **12406** | **0.99827** | 136 |
| D. oracle (true residual) | 12442 | 1.00000 | 0 |

Fixing the head restores the peak. **Correction to the v5 VERDICT's gap #1:**
the stated mechanism ("harmonic boost 8.22× matches correlation not crest")
is refuted — re-emit adds `plm×1.0` (no boost) and already peaks at 23834.
The boost is innocent; the missing head is guilty. Fix: store the first P
residuals/samples in the model (mechanical, no new knowledge needed).

### L2. plm phase-convention mismatch — MACHINERY BUG

`hear()` bins the residual **relative to the residual frame**
(`arange(nr)/T0`), but `reemit()` (Python and Zag mode 9 alike) bins by
**absolute sample index** (`arange(n)/T0`). For cry (P=64, T0=127.49) that is
a **0.502-period shift** — the harmonic waveform is added back half a period
out of phase. Measured: phase-error RMS **19.7 vs quantization-error RMS 5.1
(3.9×)**. Fixing it alone: corr 0.896→0.986, err RMS 1070→400. (It does not
drive the peak — see ablation B — but it is the largest *fidelity* error.)
Fix: one phase convention everywhere (mechanical).

### L3. 64-prototype residual quantization — BY-DESIGN REPRESENTATION

K-means (40 iterations) on the noise residual. Residual-domain SNR:
strike 24.8 dB, cry 23.1 dB, clang 20.8 dB, vowel 19.6 dB. After L1+L2 are
fixed, the remaining cry error is err RMS 136 / corr 0.99827 — that is the
honest floor of this representation. Class: **knowledge-representation
choice, not a bug**; the floor is measured and small.

### L4. LPC(64) order — BY-DESIGN, proven adequate

Oracle-residual re-emit (ablation D) is **bit-exact** (corr 1.00000, err 0):
the analysis/synthesis filter pair is consistent and lossless. The filter is
not the ceiling; what is fed into it is.

### L5. WAV parse — LOSSLESS

No sign-extension trap (both paths sign-extend correctly), chunk-aware,
no resampling/dither/normalization on intake; RMS preserved within 0.1–2.7%,
DC preserved (strike 5.9→6.0 LSB). The parse contributes zero loss.

## 4. Answer to the coordinator

| long-memory gap | total | intake share | downstream share |
|---|---|---|---|
| strike centroid 3252→3351 (+99) | +105.4* | −14.5 (≈0%) | +119.9 (≈100%+) |
| cry centroid 1942→1556 (−386) | −384.8* | +36.1 (≈0%) | −420.9 (≈100%+) |
| clang centroid 7657→7499 (−158) | −166.2* | +5.8 (≈0%) | −172.0 (≈100%+) |
| cry F0 347.2→344.5 (−2.7) | −1.8* | 0.0 (**0%**) | −1.8 (100%) |
| strike F0 580.3→572.7 | −2.0* | −0.2 (≈10%) | −1.8 (≈90%) |
| **cry peak 12316→23771 (+11455)** | **+11392*** | **+11392 (≈100%)** | −63 (≈0%) |

\*Totals differ trivially from the v5 VERDICT's rounded numbers (same FFT/YIN
method applied to all three legs here).

**Bottom line:** the spectral/F0 gaps Micah asked about are **downstream**
(the imagine walk), **except the cry peak overshoot, which is intake** — two
machinery bugs (fabricated 64-sample head; half-period plm phase mismatch),
both fixable without new knowledge. The intake's honest representation floor
(after those fixes) is corr ≈ 0.998 on the hardest clip. The v5 VERDICT's
white-box gap #1 misattributes the peak to the harmonic boost; the boost is
innocent (re-emit never applies it).

## 5. Method and provenance

- Fixture SHAs (source proxies): strike `cca99cda…`, cry `6a3309a8…`,
  clang `eaafb5dd…`, vowel `11e01d18…` (full SHAs in evidence/).
- Toolchain: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`;
  rebuilt `rb_longmem.zag` → byte-identical binary
  (`7206eae3adb82f81c6fff5da7f1e2f53b9d34116a844310be851a2c918f51824`).
- Re-emits: 2 runs each, r1==r2 SHA-256 on all 4 clips.
- Python replication of Zag mode 9: sample-identical (max|diff|=0.0).
- Analyzers: `analyze.py` (leg metrics), `whitebox.py` (residual-domain),
  ablation/counterfactual scripts — committed under `evidence/`.
- Standing rules honored: pure Zag in the read-back path, zero RNG,
  byte-identical reruns proven by SHA, analyzer-first throughout, no
  binaries/.zagd in the commit.

## Files committed

- `docs/lab/audio_intake/VERDICT_INTAKE.md` (this file)
- `docs/lab/audio_intake/analyze.py`, `whitebox.py` (measurement code)
- `docs/lab/audio_intake/evidence/metrics.json` (leg-by-leg measurements + SHAs)
- `docs/lab/audio_intake/evidence/whitebox.json` (residual-domain analysis)
- `docs/lab/audio_intake/evidence/counterfactual.json` (ablation A–D results)
- `docs/lab/audio_intake/evidence/SHA_MANIFEST.txt` (fixtures, models, binary, re-emits)
