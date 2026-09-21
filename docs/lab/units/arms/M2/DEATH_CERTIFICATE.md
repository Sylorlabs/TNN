# M2 — Death Certificate

## Arm
M2 — Compositional counter IDs (Track A, family IDENT)

## Date
2026-09-21

## Binding kill criterion (frozen)
"Single-byte leaf edit invalidates > 25% of cached compositions in the
recall benchmark, OR ID recomputation > 10% of recall latency on the 10x run."

## Cause of death
**K2: ID recomputation > 10% of recall latency on the official 10x run.**

## Evidence
- 1x K2 benchmark (r1 prose, 84,731 leaves, 63,547 compositions):
  - T_recall (leaf + composed): 124.1s
    - leaf_recall: 0.95s
    - composed_recall: 123.1s (includes per-recall SHA-256 verify)
  - T_recompute (standalone parent-ID SHA-256 + map lookup): 32.1s
  - Ratio: 32.1 / 124.1 = 25.8% — exceeds 10% kill bar.

- Official 10x K2 (`m2-k2-10x`; r1 prose ingested 10x: 847,310 leaves,
  635,470 compositions), double runs A/B:
  - Run A: leaf_recall 5.98s, composed_recall 1239.60s,
    id_recompute 359.73s; T_recall 1245.57s;
    ratio 28.8% — **KILLED**
  - Run B: leaf_recall 6.21s, composed_recall 904.86s,
    id_recompute 244.80s; T_recall 911.07s;
    ratio 26.8% — **KILLED**
  - stdout verdict line `M2K2,prose.bin,KILLED` byte-identical
    across both runs.
  - Both runs exceed the 10% kill bar on the binding measurement.

## Mechanism
Counter IDs composed canonically (sorted ascending) for multi-span units;
max composition depth frozen at 2. Parent ID = SHA-256 of canonical
encoding. Verification recomputes SHA-256 on every recall.

## Why it died
The SHA-256 verification cost dominates recall latency. Each composed
recall recomputes the parent ID (SHA-256 of the canonical encoding) to
verify cache integrity. At 10x scale (635k compositions), standalone ID
recomputation is 26.8–28.8% of total recall time. The
integrity benefit does not justify the latency cost under the frozen
kill bar. Scale did not improve the ratio: both numerator and
denominator scale linearly with composition count, as predicted.

## K1 (for the record)
PASS: Single-byte leaf edit invalidated 2/63,547 compositions (0.003%),
well under the 25% kill bar. The tree structure localizes invalidation.

## 1x battery (for the record)
All applicable legs PASS except m7-1x (re-run pending after accidental
process kill during investigation; not binding for K2 verdict).

## Disposition
**KILLED.** Do not promote. The compositional ID mechanism is
disqualified by its own binding kill criterion, confirmed on the
official 10x run.

## Evidence preserved
- Source: `docs/lab/units/arms/M2/cl/arm.zag`
  (moved from `units/arms/M2/cl/arm.zag`, 2026-09-21 finalization)
- Battery logs: `/home/hatch/workspace/m2scratch/battery_1x/`
- K2 10x logs (double runs): `~/workspace/tnn-lab/units/arms/M2/k2_10x/`
- Binary (measurement): `/home/hatch/workspace/m2scratch/m2_bin`
  sha256 `44601bc5dc51c37f49d89fe0f0fe40a55feb27cef411afc3917dc2bc676e5273`
  (not committed)
