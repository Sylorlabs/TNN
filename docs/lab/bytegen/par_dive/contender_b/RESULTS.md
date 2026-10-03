# Contender B: Results

All results from final binary (2026-09-24), pure Zag, pinned toolchain
`znc_linux_x86_64_abed8aa1`. Binary size: 87,086 bytes (optimized).

## DET (Determinism)
- Clean mix rerender: byte-identical.
  SHA-256: `d1a6c83b0e549507cca92dceb814c1c3698ce92df14f4f65a59015c604ac0a6c`
- Region order: seq / rev / stride all byte-identical. `ORDER_OK`.
- Important modes rerun: seqmix PASS, rev PASS.

## QUALITY (9 gates, V10)
| Gate | B | Bar | Result |
|------|---|-----|--------|
| G-PER | 0.336 | ≤0.350 | PASS |
| G-STA | 1.840 | ≤3.000 | PASS |
| G-LURCH | 2.373 | ≤5.000 | PASS |
| G-DRIFT | 451.195 | ≤800.000 | PASS |
| G-FLUXm | 235.714 | ≤350.000 | PASS |
| G-SIL1 | 0.000 | ≤0.020 | PASS |
| G-SIL2 | 0.000 | ≤0.500 | PASS |
| G-CLIP | 0.915 | ≤0.950 | PASS |
| G-CREST | 3.860 | ≤14.000 | PASS |
All 9 PASS. (PAR: 9/9, G-PER 0.340.)

## CHOP-1/2/3
- Complete event list: 294 timestamps (onsets, offsets, release-tail ends, vibrato extrema).
- CHOP-1 hard discontinuities: 0 PASS
- CHOP-2 silent gaps ≥150ms: NONE PASS
- CHOP-3 flux spikes: 33 total, 0 unexplained (all explained by event list).

## COHERENCE (motif 2.0–5.4s vs 24.0–27.4s)
| Metric | B | PAR |
|--------|---|-----|
| Zero-lag normalized xcorr | 1.000000 | 1.000000 |
| Max xcorr ±50ms | 1.000000 @ 0ms | 1.000000 |
| Pitch-contour correlation | 1.000000 | 1.000000 |
| IOI-contour correlation | 1.0 (by construction) | 1.0 |
| Spectral-centroid correlation | 0.999996 | 1.000000 |
B ≥ PAR on coherence (tie).

## COST (same machine)
| | Wall | Peak RSS |
|--|------|----------|
| B (optimized) | 8.54s | 20.1MB |
| PAR | 9.03s | 20.1MB |
B is slightly faster (hot-loop hoisting). No COST regression.

## RT-LONG
- Cue 440Hz @ t=1s, RESPOND nominal 880Hz @ t=28s.
- Latch: k=-1 (plan ratio 440/880=0.5) → renders 440Hz.
- Rendered pitch (spectral): 440Hz (peaks at 440, 880, 1320). 0 cents error.
- Octave detection: plan-derived ratio (NOT audio pitch metering). Honest: sensorless.
- Near-miss nominal 460Hz: k=0 → nominal stands (correctly not "corrected").
- Sub-octave nominal 220Hz: k=+1 → 440Hz (correct).
- Polyphonic (dyad 220+330Hz): nvoice=2 → abstains, nominal stands (correct).
- Correct nominal 523.25Hz: k=0 → stands (correct).

## RT-CASCADE
- One-bit fault (XOR 64) at t=3s: 1 diff (fault sample), 0 strictly post-cut diffs.
- Sustained (XOR 64 at 10 region starts): 10 diffs, all exactly XOR 64, 0 propagation.
- 1,292-block sustained corruption (XOR 0xFF per block): 1,292 diffs, all local, 0 propagation.
- B's carried state is in `st`, not the mix. Output corruption cannot propagate.

## RT-EDGE (truncate at 15s)
- Pre-divergence (0–14.8s): 0 differing samples. No illegitimate diffs.
- Post-divergence diffs: legitimate (plan differences).
- Truncation step at 15.0s: B ~12,109 (16-bit units), PAR 10,303. Both have a step
  (fade ends); B's is ~17% larger. Minor edge-case artifact, not a hard discontinuity.

## Cross-region leakage
- All 10 regions standalone vs in-context: byte-identical in-window, zero outside.
- `LEAKAGE_OK` (10/10 PASS).

## Drift
- Bus max drift: 1 Q32 unit (quantization). Bed max drift: 1 Q32 unit.
- (Tiny-plan diagnostic; full-fixture driftcheck pending.)

## Adversarial plans
- Rail pins (99999999 Hz, 999999999 amp), negative dur, malformed lines: no crash,
  output bounded (peak 187k, finite, no NaN). Parser clamps rails, skips bad lines.
