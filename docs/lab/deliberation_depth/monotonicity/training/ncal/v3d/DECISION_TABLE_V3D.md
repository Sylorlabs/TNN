# DECISION TABLE — NEC v3d: m20 (v20) vs Design S (v26)

- **Prereg:** `PREREG_NCAL_V3D_H2H_FROZEN.md` (committed `695997f5`
  before measurement) + Amendment A1 (`4df783f9`, FIX1 applies now).
- **Runlog:** `RUNLOG_V3D.md`. **No aggregate score is computed** (prereg
  §7); each dimension's margin stays visible. Winner per dimension is
  marked, but adoption is a judgment over the three dimensions, stated
  in `VERDICT_V3D.md`.
- **Blowout rule** (prereg §7): a dimension is a blowout iff margin ≥10×
  or binary catch/miss asymmetry with zero overlap. None fires (closest:
  T3 at 1.24× on mean|err|).

## SPEED

| metric | v20 | v26 | margin | winner |
|---|---|---|---|---|
| wall/item s1 (median of 3) | 219.6 µs | 245.7 µs | 1.12× | — (noise) |
| wall/item s10 (median of 3) | 159.6 µs | 190.6 µs | 1.19× | — (noise) |
| wall/item s100 (median of 3) | 194.8 µs | 806.5 µs | 4.14× | — (POLLUTED, discard) |
| interleaved s10 (5 alternating pairs, drift-cancelling) | 12.61 s med | 9.66 s med | **0.77×** | — (noise) |
| deliberation steps/item (S2) | 1 (constant) | ≤4 levels; 1000/1000 L1 observed | <1% bound | — |
| tail (S3) | machine-noise | machine-noise | — | — |

**SPEED: TIE within measurement noise.** Sequential medians say v26
12–19% slower; interleaved medians say v26 23% faster — the contradiction
proves machine noise (shared 2-core VM, load 5–14), not mechanism. The
mechanistic bound (<1% for ≤312 integer comparisons on first obs only)
is the reliable number. No blowout.

## COST

| metric | v20 | v26 | margin | winner |
|---|---|---|---|---|
| ledger B/item (C1) | 88 | 88 | 1.00× | TIE |
| schema static (C2) | 0 B | 20,520 B data-equiv | — | **v20** |
| RSS Δ resident (C2) | — | +126 KB @s1, ~0 @s10+ | — | **v20** (small) |
| output B/row (C3) | 42.01 | 42.70 | 1.016× | **v20** (formatting) |
| 1M×100 wall (C5) | 0.85 h | 1.01 h | — | TIE (noise) |
| 1M×100 ledger (C5) | 0.088 GB | 0.088 GB | 1.00× | TIE |
| 1M×100 output (C5) | 4.00 GB | 4.07 GB | 1.017× | **v20** (formatting) |

**COST: v20, by a small margin.** The differences are all small and
honest: a fixed ~20.5 KB schema (+~126 KB resident code pages at small
scale) and +1.6–2% audit bytes from wider conf printing. Nothing scales
against S — the schema is fixed cost, the ledger is identical. No blowout.

## CATCHES

| metric | v20 | v26 | margin | winner |
|---|---|---|---|---|
| matrix B3 / B13 | 2 / 0 | 0 / 0 | — | v26 (reported; bars at floor per ruling) |
| RT-A..F binary catches (17 batteries) | = | = | 0 asymmetric rows | TIE |
| RT-A..F mean\|err\| | baseline | lower on 16/17 | −1% to −17% | **v26** |
| T1 (M1/M2/M3) | +0.950 ✓ / 150/150 / 4 | +0.802 ✓ / 150/150 / 4 | — | TIE |
| T3 overall \|err\|/bias | 0.4700/+0.4500 FAIL | **0.3812**/+0.3020 PASS | 1.24× | **v26** |
| RT-F (pre-FIX1) | miss (30 rows) | miss (30 rows) | — | TIE (both; FIX1→both catch) |

**CATCHES: v26.** No blowout (no binary asymmetry; best margin T3 at
1.24×). But the direction is uniform: identical binary catches with
better calibration everywhere (16/17 red-team batteries), T1 tie, T3 win
by honest mechanism (L3 backoff 0.802 trace-verified vs 0.95 constant).

## Dimension summary

| dimension | result | blowout? |
|---|---|---|
| SPEED | TIE (noise; mechanistic bound <1%) | no |
| COST | v20 by small fixed margin | no |
| CATCHES | v26 (calibration everywhere, T3 by mechanism) | no |

Micah's ~11:20 ruling stands: bars don't discriminate; these three
dimensions decide. The adoption judgment is in `VERDICT_V3D.md`.
