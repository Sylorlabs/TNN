# CREW A — fork A-long: 600 s continuous render. Results 2026-09-24.

## Build
- `plans/theme_long600.txt`: 600 s theme (bed + motif recurrences at
  5.0–8.4 s and 590.0–593.4 s); `plans/long600.plan`: formed plan.
- `src/render_fn.zag`: chunked streaming renderer (each chunk < 2^25-byte
  slice cap), `par` and `nat` modes (nat = carried accumulators, no servo).
- Equivalence: `render_fn par` on the 30 s fixture == `render_a` exact.

## Identity & determinism
- Rendered 26,460,000 samples / 105,840,000-byte MIX (both reruns).
- Two `par` rerenders: **byte-identical** (`cmp` clean).
- SHA-256 of the two A 600 s files: (recorded equal in RUNLOG.md at render
  time; files deleted after — size prohibits retention/commit).

## Long-horizon behavior
- Motif windows @5 s vs @590 s: **byte-identical**, zero-lag normalized
  xcorr **1.0000000000**. No measurable drift over 585 s.
- Bed tuning (Hann-windowed Goertzel FFT, zero-padded): 20–30 s:
  **110.00018 Hz (+1.65 ppm)**; 560–570 s: **110.00018 Hz (+1.65 ppm)** —
  identical to 0.00001 Hz; no tuning drift.
- `nat` (carried-accumulator) comparison: early/late motif xcorr 0.999945,
  windows NOT byte-identical (one-time `inc`-truncation phase noise, bounded,
  non-growing — same structure the characterization measured at 300 s).

## Fork verdict: PASSES. PAR is scale-invariant by construction; A-long
## demonstrates byte-exact 600 s recurrence vs native's LSB-level drift.
## (Prereg minimum was 300 s; tested at 600 s.)
