# Phase-2 Verdict — Exact Audio Replication (v6 knowmap + lossless residual channel)

**Order:** Micah, 2026-09-26 ~09:38 PDT. Real audio in → **byte-identical PCM out**,
through a knowledge map, following the image-v3 commit `d64892bc3911...`:
the emitter reads the knowmap ONLY, never the original.

**Bar:** `cmp` on the WAV files — same PCM bytes, infinite PSNR. Run twice,
prove byte-identical determinism.

## What was built

Three pure-Zag binaries (pinned toolchain
`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`):

| Binary | Source | Role |
|---|---|---|
| `resid` | `phase2/src/resid.zag` | Hear-side: v5 model + original WAV → **v6 knowmap** (v5 knowledge + exactness extension) |
| `reemit6` | `phase2/src/reemit6.zag` | Emitter: reads ONLY the v6 knowmap. Mode 10 = exact, Mode 11 = semantic ceiling |
| `rb_longmem6` | `phase2/src/rb_longmem6.zag` | Legacy imagine (mode 0) + legacy re-emit (mode 9), v6-aware, gate-reconciled |

## The four mandated fixes (from DIAGNOSIS.md)

### 1. Phase anchor + seed-index slip (gaps #1, #2, #4, #5)

- **Hear** indexes PLM by residual index `j` (`harm_bin(j, T0, NBINS)`).
- **Emit** indexed by output index `i`. Fix: emitter computes `j = i - P` and
  uses `harm_bin(j, T0, NBINS)` — the phase bin is anchored to the residual
  timeline, not the output timeline.
- **Seeds:** emitter stored `seeds[i] = proto[q[i]]` (quantized score).
  Fix: `resid` stores the **true first P PCM samples** from the original WAV;
  emitter copies them verbatim into `out[0..P-1]`.
- **q[i] vs q[i-P]**: legacy re-emit read `q[i]` at output index. Fix:
  emitter reads `q[j]` at residual index `j = i - P`.

### 2. Viability-gate reconciliation (gap #9)

- The `(1.5, 10.0)` boost gate existed only in the re-emit path; imagine used
  a different, weaker check. The two paths disagreed on renderability.
- Fix: **the gate is decided ONCE**, at model-build time, inside `resid`
  (`use_h = (pT>0 and T0>0.0 and NBINS>0 and 1.5<boost<10.0)`), and stored in
  the v6 extension. `reemit6` (modes 10, 11) and `rb_longmem6` (modes 0, 9)
  **obey the stored flag**. No path recomputes it.

### 3. Harmonic representation (gap #6)

- Fixed-mean harmonic explained 3.4% of cry / 0.68% of vowel residual variance.
- Fix: `resid` fits a **per-period least-squares amplitude**
  `amp[per] = Σ(res·plm)/Σ(plm²)` (nper periods).
- Cry: r2 (variance explained) **0.034 → 0.096** (2.8×).
- The amp is stored knowledge, used in the exact path's decomposition.
  (Caveat: per-period amp CV = 1.36 — the fit is noisy where the harmonic is
  weak. It is NOT used in the semantic path because hear fitted `q` against
  `res - plm` (amp=1); using amp there would be inconsistent. See § Honest boundary.)

### 4. Lossless residual channel (the closure)

- `resid` stores the **full f64 noise residual** `nres[j] = res[j] - h[j]`
  (with the amp-aware harmonic), after the true seeds.
- Mode 10 adds it back: `rv = pred + nres[j] + h[j] = res[j] + pred`.
- `res[i] + pred[i]` is the analysis filter inverted — the sample is
  reconstructed to the LSB. This is the exactness layer, explicitly NOT
  semantic knowledge.

## v6 knowmap format (appended to the v5 bytes)

| Offset (from ext start) | Content |
|---|---|
| 0 | `n` (i64): source sample count |
| 8 | `use_h_stored` (i64): the single gate decision |
| 16 | `nper` (i64): number of periods |
| 24 | `amp[nper]` (f64): per-period harmonic amplitudes |
| 24+8·nper | `seeds[P]` (f64): true first P PCM samples |
| 24+8·nper+8·P | `nres[n-P]` (f64): full noise residual |
| 24+8·nper+8·P+8·(n-P) | `hdr_len` (i64): WAV header byte count |
| +8 | `header[hdr_len]` (bytes): the full WAV container header (all bytes up to and including the `data` tag+size — preserves LIST and other non-PCM chunks, so `cmp` on the whole file passes, not just the PCM) |
| end-16 | `n` again (i64), end-8: magic `V6EXACT!` (8 bytes) |

The v5 section is untouched → v6 files remain readable by legacy mode 9
(`rb_longmem6` handles the footer-aware `q_len`). The stored header means the
emitter reproduces the exact container without ever reading the original —
`resid` (which sees the original) stores it; `reemit6` (which doesn't) replays it.

## Results — the four proxy fixtures

| Clip | Mode 10 (exact) | Mode 10 run2 | Determinism | Mode 11 semantic RMS (LSB) | Mode 11 corr |
|---|---|---|---|---|---|
| strike | **BYTE-IDENTICAL** (`cmp` PASS) | PASS | PASS | 40.5 | 0.9984 |
| vowel | **BYTE-IDENTICAL** | PASS | PASS | 97.9 | 0.9899 |
| cry | **BYTE-IDENTICAL** | PASS | PASS | 136.0 | 0.9983 |
| clang | **BYTE-IDENTICAL** | PASS | PASS | 109.8 | 0.9965 |

- Mode 10: `cmp fixture.wav exact.wav` → identical on all 4. Two independent
  runs → `cmp` identical (deterministic).
- Mode 11 (knowledge only, all interface fixes, raw plm): reproduces the V5
  ceiling exactly (40.5 / 97.9 / 136.0 / 109.8 LSB RMS).
- Cry harmonic: `use_h=1`, 129 periods, amp mean 0.99, r2 0.096.

## Results — sealed corpus (359 clips, SEAL_MANIFEST-verified)

**359/359 byte-identical** (`cmp` PASS on the full WAV file, including headers).
**359/359 deterministic** (two independent mode-10 runs `cmp`-identical).
**359/359 seal_match** (SHA-256 verified against `SEAL_MANIFEST.json` before processing).

| Class | n | byte-identical | mean semantic RMS (LSB) | mean semantic corr |
|---|---|---|---|---|
| field | 100 | 100/100 | 214.4 | 0.9961 |
| child | 52 | 52/52 | 199.2 | 0.9963 |
| speech | 76 | 76/76 | 152.0 | 0.9976 |
| prosody | 100 | 100/100 | 212.0 | 0.9945 |
| lowf0 | 31 | 31/31 | 126.0 | 0.9923 |

- 25 clips carry non-PCM `LIST` chunks; the stored-header mechanism reproduces
  them (the one initial failure, `prosody-ravdess-1-03`, was the header-fidelity
  gap — fixed by storing the container bytes in v6).
- Semantic (mode 11) RMS ranges 11–1092 LSB across the corpus; correlation
  0.976–0.999. The knowledge gap varies by class and clip; the closure layer
  closes it to zero in every case.
- Per-clip evidence: `results/corpus_results.csv` (seal SHA, byte-identity,
  determinism, semantic RMS/corr, stored gate decision).

## Analyzer-first evidence

For every byte-identical output, the analyzer measurements (waveform RMS/peak/
zero-crossings, HNR, spectra, envelope stationarity, 50/60 Hz hum) are
**identical by construction** — identical PCM bytes necessarily produce
identical measurements. SHA-256 recorded per clip: source, knowmap, run1, run2
(see `results.jsonl`).

The semantic (mode 11) outputs are NOT byte-identical; their analyzer deltas
vs source are the knowledge gap, measured in RMS LSB and correlation above.

## The honest boundary

| | What it is | What it is not |
|---|---|---|
| LPC + proto + q + PLM + gate + amp | The **semantic audio knowledge**: what the system learned about the sound | — |
| seeds + nres (f64 residual) | The **lossless closure layer**: stored signal needed to reach the last LSB | Understanding. It is the exactness mechanism, not comprehension. |
| Mode 11 | What the knowledge alone reproduces (the semantic ceiling) | Exact |
| Mode 10 | Knowledge + closure → byte identity | Proof the system "heard" it losslessly |

A class can reach byte identity through the combined knowmap while the
semantic-only mode still shows a measurable gap (e.g. cry: 136 LSB RMS in
mode 11, 0 in mode 10). Both are reported. The residual bytes are never
called understanding.

## Reproducibility

- No RNG anywhere in the decision paths. All binaries deterministic.
- Exactness relies on hear-side and emit-side using identical f64 operation
  order (same accumulation loop). Verified by `cmp`, not by reasoning.
- If the toolchain or sources change, re-run `resid` + `reemit6` mode 10
  twice and `cmp` — the bar is mechanical.

## Files (repo-bound)

- `phase2/src/resid.zag`, `phase2/src/reemit6.zag`, `phase2/src/rb_longmem6.zag`
- `phase2/src/driver.py`, `phase2/src/measure.py`
- `phase2/VERDICT.md` (this file)
- `phase2/results/` — run manifest, summary CSV/JSON (compact; no WAVs, no binaries)
- Sealed fixtures stay in `~/workspace/audio_longhorizon/corpus/` (frozen, committed separately)

Excluded from the repo (per standing standard): ELF binaries, `.zag-cache`,
generated WAVs, NPZ intermediates, gallery renders (those go to `~/workspace/your_files/`).
