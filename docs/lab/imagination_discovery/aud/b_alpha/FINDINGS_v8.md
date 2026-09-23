# FINDINGS_v8 — tremolo/wander fix (NEW clip for Micah's ears)

**Date:** 2026-09-23
**Clip (NEW):** `clips/b_alpha_kids_1e_h_v8_notremolo.wav`
**SHA-256:** `6b0913860a5c7ecf628c38c4fa76e41cb8d6c4ae1729280c8d8be432b3983528`
**Source:** `src/render_v8.zag` (pure Zag; Python only for forensic measurement)
**Determinism:** two renders byte-identical (`cmp` clean)

Micah's ears decide. This document is the measurement record; the clip is the verdict target.
Micah's complaint (v7): "sounds like its shifting around like a tremelo which it
should never do unless I ask for it."

## Root cause (measured, not guessed)

v7's bed hash-scattered EVERY grain's source position white (`gpos = h01(7107,k)*span`,
new unrelated chunk every 93 ms). Forensic bed-only measurement:

| metric | v7 bed | real aporee anchor | v7 full mix |
|---|---|---|---|
| 0.5–2 Hz modulation share | **30.3%** | 1.9% | 18.2% |
| peak modulation freq (2–20 Hz) | 2.76 Hz | 5.68 Hz | 2.72 Hz |
| 93 ms RMS std | 1.98 dB | 1.41 dB | 3.92 dB |

The envelope did a random walk with correlation time ~one grain (0.74 s): a
tremolo-like restless shifting. No LFO existed anywhere; the flutter came from
replacing every grain with an unrelated chunk 10.7×/s.

Contributing cause: v7 built its bed from tx0+tx1+tx2, and the stationarity audit
showed tx0 ramps 39 dB and tx2 fades 15 dB across 2 s — two of three bed sources
were swells, not ambience. The 1 s-window gate bars (G-STA/G-LURCH) could not see
either mechanism: the gate passed v7 while ears convicted it.

## Fix (v8, pure Zag)

1. **Steady sources only, chosen by modulation spectrum** (not block-RMS):
   catalog3 tx12/tx10/tx1/tx11/tx4 + catalog.bin tx4 — all ≤6.8% in 0.5–2 Hz.
   catalog2's "steady" textures excluded: they carry 20–50% 2–5 Hz AM a 0.75 s
   follower cannot iron out (measured poison).
2. **Seamless ring**: the six joined by 0.25 s EQUAL-POWER (sin/cos) crossfades,
   last→first closed. A linear crossfade would dip 3 dB per junction.
3. **Contiguous traversal** wrapping the ring (no overrun event); **rare hash
   reseeds** (mean ~9 s, 1/96 grains) crossfaded over the full 0.74 s Hann grain
   break the ring's periodicity for G-PER. 7 of 8 overlapping grains still carry
   contiguous content through a reseed.
4. **Zero-phase one-pole macro-envelope follower** (tau 0.75 s, gain clamped
   [0.5, 2.0]) irons residual drift; both ring copies flattened identically so
   wraps stay seamless.
5. Unchanged from v7: events, -37 dBFS bed target, two-pass scale, transparent
   mastering (limiter engaged on 0 samples), deterministic hash streams, no RNG.

## Measured v7 → v8 (bed-only forensic)

| metric | v7 bed | v8 bed | aporee anchor |
|---|---|---|---|
| 0.5–2 Hz share | 30.3% | **3.0%** | 1.9% |
| 0.1–0.5 Hz share | 9.1% | **1.3%** | 1.1% |
| 2–5 Hz share | 9.5% | 4.4% | 4.5% |
| 93 ms RMS std | 1.98 dB | **1.15 dB** | 1.41 dB |
| 1 s RMS std | 0.83 dB | **0.32 dB** | 0.72 dB |

Full mix 0.5–2 Hz: 18.2% → 9.2%. (0.1–0.5 Hz stays ~35%: sparse composed
events with natural onsets/gaps, same as v7 — that is the composition, not the bed.)

## Frozen nine-bar gate (unchanged bars, v8 full mix)

| bar | v8 | bar limit | v7 |
|---|---|---|---|
| G-PER | **0.204** PASS | ≤ 0.35 | 0.265 |
| G-STA | 2.68 dB PASS | ≤ 3.0 dB | 2.82 |
| G-LURCH | 4.59 dB PASS | ≤ 5.0 dB | 4.10 |
| G-DRIFT | 585 Hz PASS | ≤ 800 Hz | — |
| G-FLUXm | 271 PASS | ≤ 350 | — |
| G-SIL1 | 0.000 PASS | ≤ 0.02 | 0 |
| G-SIL2 | 0.000 PASS | ≤ 0.5 s | 0 |
| G-CLIP | 0.149 PASS | ≤ 0.95 | — |
| G-CREST | 7.96 PASS | ≤ 14 | — |
| **GATE** | **PASS** | | PASS |

No bar was weakened. The gate still cannot see inside its 1 s/50 ms windows —
the new anti-wander diagnostic (modulation spectrum above) is recorded here as
the instrument that caught what the gate missed.

## Rejected forks

- Contiguous traversal of tx0+tx1+tx2 (v7's swells): reproduced the swells — worse.
- 0.5 s block-RMS flattening: gain kinks injected ~2 Hz — rejected.
- One-pole flattening on v7's sources: insufficient.
- 5 steady textures, linear, 1/32 reseeds: 0.5–2 Hz 19.9% (overrun reseeds).
- 9-texture ring incl. catalog2: catalog2's 2–5 Hz AM poisoned the bed (14.7%).
- Reseed sweeps on the final 6-texture ring: 1/32 → 1/96 all pass G-PER;
  1/96 chosen (0.5–2 Hz 3.0%, G-PER 0.204).

## Files

- `src/render_v8.zag` — the renderer (committed)
- `clips/b_alpha_kids_1e_h_v8_notremolo.wav` — NEW clip (committed, big-file)
- `FINDINGS_v8.md` — this file (committed)
- `measure_tremolo.py` — forensic measurement only (not committed; Python)
