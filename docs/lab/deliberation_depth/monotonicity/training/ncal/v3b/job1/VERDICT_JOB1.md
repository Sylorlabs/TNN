# VERDICT — JOB 1 red-team of adopted m20 (2026-09-25)

**Authority:** `PREREG_NCAL_V3B_FROZEN.md` §2 (SHA
`4c8780d12287c84c83c7576e45ee7f1e36dfa51799081787dfd9d36597196f21`).
**Pre-run freeze:** `ADDENDUM_V3B_JOB1_PRERUN_2026-09-25.md` (committed
`5475c9fd` BEFORE any attack run). All attacks A/B/C byte-identical,
SHA-logged. Toolchain pinned (`498abcb5…`).

## Adopted baseline (re-scored, pipeline PASS)

Variant 20 reproduces adopted m20 legs byte-identically at s1/s10/s100.
Bars: B1=0, B2=0/0, B3=2/2/2, B4=0.950, B4b=0.950, B5=0.543, B6=1.000,
B7=0.148, B9=1.000, B13=0/0/0. (B8 fails but is frozen non-gating.)

## Per-attack results

### RT-A — adversarial class distributions: NO MECHANISM BREAK

B1=55, B2=55/0, B3=4 (vs 2), B4=0.811, B4b=0.600 (≥0.50 ✓),
B5=0.324 (≥0.20 ✓), B13=2 (vs 0).
White-box: every B3 rise and both B13 cells are the authorized-state
lag on batteries with correctness flips. rta_mid `[C,W,C,W,C]`
alternates: at d2 all 20 items wrong but conf 950 (past=[C]) →
G=+0.950, rise +1.000; at d4 all correct but conf 500 (past=[C,W],
honest 50/50) → G=−0.500. The confs honestly track past empirical
rates; the G swings are maximal when correctness alternates. rta_low
rises (+0.025 d1→d2, +0.208 d4→d8) are C→W flips the conf cannot
reflect. **Classification: battery-design (adversarial correctness
flips) + frozen authorized-state rule. Not a mechanism defect.**
The frozen matrix's constant-correctness items (B1=0) deliberately
avoid this confound.

### RT-B — ceiling-latch ordering: V2 HOLDS, B5 INVERTS (honest residual)

m20: B1=25, B2=25/0, B3=2, B4=0.614, B4b=0.614, **B5=−0.101 (< 0.20)**,
B13=1. m11 control: B1=25, B2=8/0, B3=1, B13=1.
- **V2=0 in all four orders.** The ordering attack on the ceiling latch
  FAILS — conf never rises, exactly as designed.
- **V1=25 (m20), V1=8 (m11).** Trips occur ONLY at 1→0 correctness
  flips, via the frozen authorized-state rule (conf uses past cells'
  GT only; at the flip cell it cannot reflect the flip). m11 trips too
  → not m20-specific. m20 trips more because its personal-only conf
  lacks m11's pooled drag-down (the adopted design, not a defect).
  **Not a mechanism break.**
- **B5=−0.101: BREAK by the letter (a).** Wrong-first `[W,W,C,C,C]`
  items: correct cells (d4,d8,d16) conf 0 (ceiling latch), wrong cells
  d1=950/d2=0. Wrong-cell mean conf (0.715) exceeds correct-cell mean
  (0.614) — separation inverts. |err|=0.75 on wf correct cells at d16
  while the item's own ledger says p_raw=0.75 (the latch discards its
  own knowledge). Systematic, worse than disclosed limits.
  **Classification: mechanism (consequence A — adopted in-class).
  Honest residual: no principled in-class fix exists (the latch IS the
  adopted mechanism; removing it defeats the design).**

### RT-C — abstention composition: NO BREAK, bound established

Binary confirms sim (0 mismatches, 840 cells). Base: flat G=−0.025,
no rises. Single correct-abstention: +0.0011. Three: +0.0036.
Bound probe (all 12 correct abstain): +0.0250. **All rises are pure
composition** (item confs/correctness constant; only the released
fraction changes). Within the frozen neighborhood, rises are
+0.001–+0.004 (SMALLER than the disclosed +0.008); the structural max
is +0.025 and requires emptying the correct side. **Honest residual
(selection/composition). No miscalibration.**

### RT-D — distributional shift at scale: NO SCALE GROWTH

s1/s10/s100: B3=4/4/4, B13=2/2/2 (**nonincreasing ✓**), B4b min 0.600
stable, B5 0.509/0.499/0.494. The B13=2 is the RT-A alternating effect
(stable, not growing). Overweighting low-rate and rate-1.0 classes at
scale does not worsen any bar. **No break.**

### RT-E — gaming channel: NO CHANNEL FOUND

- **E1 (exact-rule):** 0 mismatches / 150 cells (learn), 0 / 150
  (fatigue) — the binary follows the stated personal-only rule exactly.
- **E2 (independence):** attacked-item trajectory solo vs in-battery
  **byte-identical** — the personal ledger provably carries zero
  cross-item (hence zero bar) information.
- **E3 (rise-selectivity):** V2=0 on both; conf never exceeds the
  stated rule.
The learn battery's B13=3 (G=−0.35 at d4/d8/d16: items correct but
conf 0) is consequence A (wrong-first pinning), not a channel — the
mechanism does exactly what it says. **No break. Honest residual.**

### RT-F — item-identity stress: CONFIRMED BREAK (mechanism) → FIXED

m20 bars: B1=0, B2=0/0, B3=0, B4=0.950, B5=0.380, B13=0 — **the bars
do not catch it.** White-box: 72-char ids NEVER match their slot.
`nec_cmp_id` caps the compare loop at 63 bytes and returns 0 whenever
`id.len > 63`; every observation is treated as a first observation →
conf 950 on all 25 cells of always-wrong items (|err|=0.95/cell,
systematic, 20 wrong cells). Short-id controls: correct 950,0,0,0,0.
**Classification: mechanism (implementation) break — lookup
correctness, not a design choice. Worse than disclosed limits.
Principled in-class fix exists → NEEDS-WORK fix round (see
ADDENDUM_V3B_JOB1_FIX1_PRERUN_2026-09-25.md).**

## What held

- V2=0 universally (all attacks, all orders) — the anti-theater
  property is structural.
- The stated personal-only rule is exact (E1: 0/300 mismatches) and
  per-item independent (E2: byte-identical solo vs in-battery).
- B13 nonincreasing under scale shift (2/2/2).
- Composition rises bounded (+0.025 max, +0.001–0.004 in-neighborhood).
- No bar-information channel exists (the ledger has no bar inputs).

## What broke

1. **RT-F (mechanism/implementation):** >63-char ids never match →
   systematic |err|=0.95. **FIXED** (fix1: full-id compare via ibuf
   offsets; frozen matrix byte-identical s1/s10/s100; RT-F long ids
   now 950,0,0,0,0).
2. **RT-B B5 inversion (mechanism/consequence A):** wrong-first
   ordering inverts separation (B5=−0.101), |err|=0.75 systematic.
   **Honest residual** — no in-class fix (the latch is the design).
3. **RT-A B3/B13, RT-B V1 (battery-design/frozen-rule):** correctness
   flips maximize authorized-state lag. Not mechanism defects.

## Fix vs residual

- **RT-F:** principled in-class fix implemented and validated (fix1).
  Recommended for adoption (replaces the 63-byte cap with full-id
  lookup; zero behavior change on ids ≤63, proven byte-identical).
- **RT-B B5 / consequence A:** honest residual. Any "fix" that lets
  conf rise is a different mechanism, out of class.
- **RT-C composition:** honest residual (bounded, pure composition).
- **RT-E learn B13:** honest residual (the rule working as designed
  on 0→1 patterns).
