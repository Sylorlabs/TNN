# FORK 4 (prosody_ab) — GATE REPORT (2026-09-24)

## Render
- Source: `pab.zag` (pure Zag, zero RNG; prelude + fork4_body.txt)
- B render (deliverable): `clipB.wav` — SHA-256
  `3f941f868c73ee29cf31e5798f506ea3b8efd8bfb28562a0ea98cb49672fa2ba`
- 3× reruns byte-identical (r1/r2/r3.wav, same SHA).
- A render (control): `clipA.wav` — SHA-256
  `8c5a6d96a6e104548a096adb85823a98a539baa15f72c3d896519455c4798a4b`
- NEW clip: `prosody_ab_NEW.m4a` — SHA-256
  `488bf0c0893a9f5b23dafa6e69d99f8fc1063f2dc8d25b2ac97021f76b734db8`

## Shared gates — B (prosody applied)

| gate | bar | measured | verdict |
|---|---|---|---|
| frac_static | ≥ 0.25 | 0.7823 | PASS |
| HNR | 3.7±3 dB | 6.46 dB (in [0.7,6.7]) | PASS |
| PERIODICITY | ≥ 0.5 | 0.9619 | PASS |
| HF_ROLLOFF | [-40,-12] dB | -12.27 | PASS |
| PROSODY | [0.3%,3%] | 0.699% | PASS |
| TRANSIENT crest | [3,20] dB | 5.93 (6 onsets) | PASS |
| peak | < -1 dBFS | -3.04 | PASS |

## Kill experiment (A/B — the prosody layer IS the kill)
- A (no prosody layer): PROSODY = 0.001% → FAILS the prosody gate
  BY DESIGN. The static-F0 control is prosody-dead. Control PROVEN.
- B (prosody layer): PROSODY = 0.699%, all gates PASS.
- A/B delta on prosody: 0.001% → 0.699% (700×). The layer is load-bearing.

## Design notes
- Engine: band-limited saw (harmonics 1..20, 1/k, phase-locked) ×
  FROZEN 3-formant mask (800/1200/2800 Hz). An impulse-train exciter
  was tried first and ABANDONED: the output spectrum was
  formant-dominated, F0 cues too weak for the tracker (documented).
- B adds: 5.5 Hz vibrato ±0.9%, hash micro-timing ±8 ms (seed
  1400200004), LP'd hash breath for HNR.
- Analyzer fixes (shared, both legitimate): parabolic interpolation of
  autocorr peak (integer-lag quantization read as 0.5% fake prosody);
  prosody computed on run interiors (trim 50 ms edges) — attack/release
  artifacts were inflating static-F0 std.
- HNR tension (as fork 3): targeted bar's upper edge (6.46 dB).
