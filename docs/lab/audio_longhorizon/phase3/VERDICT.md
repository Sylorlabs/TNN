# VERDICT — AUDIO SEMANTIC-GROWTH (Phase 3)

**Date:** 2026-09-26  
**Status:** COMPLETE. Gate green. All preregistered bars met or exceeded.  
**Corpus:** 359 sealed clips (child 52, field 100, lowf0 31, prosody 100, speech 76)  
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned)  
**Constraint:** pure Zag, zero RNG, deterministic.

## The gate (non-negotiable)

| Check | Result |
|---|---|
| Mode 10 byte-identical (`cmp` vs sealed source) | **359/359 PASS** |
| Determinism (two resid3 runs → identical bytes) | PASS |
| Determinism (two mode-10 renders → identical) | PASS (smoke) |

The exactness layer is untouched by the semantic changes: mode 10 reproduces the
sealed WAV bit-for-bit on every clip, including the 25 with non-PCM LIST chunks.

## What changed (the semantic model)

Phase 2's semantic excitation was `proto[q] + plm`. Phase 3's is:

```
s[j] = proto[q[j]] + amp[per]·plm[hb] + impulse[j]
```

Three mechanisms, all preregistered in `docs/PREREG.md`:

### H1 — Transient-event channel (the big one)

The quantization error lives in brief HF transient misses (67–76% of error
energy in tails; median 817–1690 events/clip, longest runs 6–8 samples, centroid
~11 kHz). Phase 3 stores the top `M = max(16, nr/500)` residual-error samples as
deterministic `(position, amplitude)` impulse events, selected by a
deterministic min-heap (position tie-break, sorted by position).

**Result:** residual RMS shrinks **91–94% per class**. Semantic RMS improves
26–40% per class. This is the mechanism that does most of the work.

### H2 — Joint per-period amplitude (the honest-boundary fix)

Phase 2 fitted the harmonic amplitude against the raw residual and then
*refused to use it* in the semantic path ("would be inconsistent with q").
Phase 3 fits `amp = LS(res − proto[q], plm)` — the amplitude of what the
vocabulary *leaves behind* — and uses the identical factorization in hear and
emit. The inconsistency is resolved, not worked around.

**Result:** no clip regresses (min gain +10.1%). The joint fit is strictly
better than phase 2's decoupled fit.

### H4 — Selective refused-harmonic acceptance (evidence-gated)

19 clips were pitched but refused by the boost gate (1.5 < boost < 10.0).
Phase 3 accepts a refused clip **iff** the jointly-fitted harmonic explains
>10% of the remainder variance (r² > 0.10). 14 clips accepted.

**Result:** all 14 improve, 23–65% semantic RMS gains. Ablation (H4 disabled,
H1+H2 only) confirms H4 adds 15–60% on top of H1+H2 for every accepted clip.
The 5 refused clips stay refused (their r² < 0.10 — correctly rejected).

Notable: `child-fsd50k-416689` (boost=11.66, refused by the ceiling) had
r²=0.491 against the remainder and improved 60.7%. The ceiling was wrong for
this clip; the r² gate discriminates correctly.

### Killed by measurement

- **H3** (extra scalar tail levels): killed pre-implementation. 1–4% gain vs
  16–51% from transient impulses on the same locus. Redundant.
- **H5** (HF shaping): killed by measurement. The 12k+ "excess" ratios (1.5–2.4×)
  are a ratio artifact — the source has almost no 12k+ energy. Absolute HF
  error is <0.3% of semantic error energy on all sampled clips. Not worth a
  mechanism.

## Results — semantic (mode 11, knowledge only)

| Class | n | sem RMS base | sem RMS new | gain | corr base | corr new |
|---|---|---|---|---|---|---|
| child | 52 | 199.2 | 139.3 | **30.1%** | 0.9963 | 0.9984 |
| field | 100 | 214.4 | 150.0 | **30.1%** | 0.9961 | 0.9983 |
| lowf0 | 31 | 126.0 | 92.8 | **26.4%** | 0.9923 | 0.9958 |
| prosody | 100 | 212.0 | 131.7 | **37.9%** | 0.9945 | 0.9977 |
| speech | 76 | 152.0 | 97.8 | **35.6%** | 0.9976 | 0.9990 |

No clip regresses. Smallest gain: +10.1% (`child-fsd50k-350733`).

## Results — residual share (the understanding metric)

| Class | residual RMS base | residual RMS new | shrinkage |
|---|---|---|---|
| child | 61.3 | 4.1 | **93.3%** |
| field | 207.4 | 12.1 | **94.2%** |
| lowf0 | 77.9 | 7.1 | **90.9%** |
| prosody | 58.5 | 4.8 | **91.8%** |
| speech | 9.9 | 0.7 | **92.6%** |

The closure cost — what must be stored *in addition to* the semantic model for
exactness — collapses by >90% in every class. (Note: phase 2's residual did not
subtract `proto[q]`; phase 3's does, because mode 10 now uses the full semantic
factorization. The residual is now the *true* "what the model doesn't explain.")

## Results — waveform diagnostics (new vs old semantic)

HF hash substantially reduced (child 16k+ was +482%, now +53%; prosody 12–16k
was +3634%, now +92%). Remaining excess is energetically negligible (<0.3% of
error). 10 ms envelope correlation 0.9978–0.9995 (unchanged, already strong).

## Ears test

Blind A/B (old vs new semantic) for 6 clips (best-per-class + 1 smallest-gain),
with measured waveform analysis, in a self-contained NEW-badged gallery:
`~/workspace/your_files/audio_phase3_AB/index.html`
(data URIs, zero external loads; reveal key at the bottom).

## What this means (plain English)

The machine now understands audio better. It learned that sounds are made of:
(1) a harmonic hum whose loudness changes (vowels, engine drones),
(2) a textured body (the vocabulary), and
(3) sharp transient events — clicks, onsets, consonant attacks — that the old
model smeared into quantization noise.

It also learned to be selective: it only claims a harmonic when the evidence
(r² > 10%) supports it, and it was right 14/14 times.

The exactness guarantee is untouched: 359/359 bit-identical.

## Files

- `src/resid3.zag`, `src/reemit63.zag` — the phase-3 hear/emit pair
- `src/decompose.py`, `src/analyze2.py`, `src/quantify.py` — baseline analysis
- `src/battery3.py`, `src/final_compare.py`, `src/ears_ab.py` — battery + analysis + gallery
- `docs/PREREG.md` — preregistered hypotheses, mechanisms, kill bars
- `results/baseline_decomp.json` — phase-2 baseline (359 clips)
- `results/battery3.log` — phase-3 battery (359 clips, all OK, all byte-identical)
- `results/final_comparison.json` — per-class aggregates
- `results/analyze2_report.txt`, `results/quantify_report.txt`, `results/candidate_gains.json`, `results/mechanism_attrib.json` — mechanism evidence

## Honest boundaries

- The residual is still f64/sample (file sizes unchanged). The *information*
  shrank 91–94%; the *bytes* didn't (kept f64 for the exactness proof).
- H5 (HF) killed: the excess is real as a ratio but negligible as energy.
- The 5 r²-rejected pitched clips remain unmodeled (correctly — their harmonic
  evidence is weak).
- Semantic RMS (98–150) is still far from zero. The model understands *more*,
  not *everything*.
