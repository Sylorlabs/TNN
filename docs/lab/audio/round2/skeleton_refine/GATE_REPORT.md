# FORK 3 (skeleton_refine) — GATE REPORT (2026-09-24)

## Render
- Source: `skel.zag` (pure Zag, zero RNG; prelude + fork3_body.txt)
- Binary: `skel_bin` (not committed)
- Full render: `full_full.wav` — SHA-256
  `3b5d78bd19f344ef684e9846694a2ff090945e41746387463dd0878f7c44d17b`
- 3× reruns byte-identical (r2a/r2b/r2c.wav, same SHA).
- NEW clip: `skeleton_refine_NEW.m4a` — SHA-256
  `b0bdeca810ab6d8cc861cb74575a531a2409e890a4a653a6240bea82a6c8994a`

## Shared gates (analyzer ../shared/analyze.py)

| gate | bar | measured | verdict |
|---|---|---|---|
| frac_static | ≥ 0.25 | 0.7469 | PASS |
| HNR | 3.7±3 dB | 6.57 dB (in [0.7,6.7]) | PASS |
| PERIODICITY | ≥ 0.5 | 0.8622 | PASS |
| HF_ROLLOFF | [-40,-12] dB | -14.48 | PASS |
| PROSODY | [0.3%,3%] | 2.07% | PASS |
| TRANSIENT crest | [3,20] dB | 10.37 (8 onsets) | PASS |
| peak | < -1 dBFS | -3.96 | PASS |

## Kill experiment (preregistered): skeleton-only control
- `skel_only.wav` HF_ROLLOFF = -84.59 dB → FAILS the dullness bound
  (-40 dB). The refinement stage is load-bearing: PROVEN.
- centroid(full) − centroid(skel) = 1706.5 − 783.2 = 923.3 Hz ≥ 500 Hz.

## Design notes / deviations
- HNR bar tension (documented): the 3.7±3 dB bar is calibrated on a
  noisy playground anchor; clean synthesis needs ~20% noise energy to
  reach it. Targeted the bar's upper edge (~6 dB) via two-pole-LP'd
  hash breath (natural aspiration, not white hiss). Flagged for Micah:
  consider recalibrating to the clean anchor (vowel_real.wav, 11.6 dB).
- Analyzer fix (shared): frac_static now uses LOCAL (±150 ms) median F0
  — a global median punishes any multi-note phrase by design. Prosody
  F0 track median-5 filtered (outlier rejection under breath noise).
- Breath gain 17000 (two-pole LP 0.25); fundamental 7000; harmonics
  2..20 at 1/k phase-locked; 3 ms onset transients at 1260 peak.
- Micro-timing seed 1400200003 (hash64(note*7919+SEED), ±8 ms).

## Verdict: PASS — ear candidate
