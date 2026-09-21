# M2 — Death Certificate

## Arm
M2 — Compositional counter IDs (Track A, family IDENT)

## Date
2026-09-21

## Binding kill criterion (frozen)
"Single-byte leaf edit invalidates > 25% of cached compositions in the
recall benchmark, OR ID recomputation > 10% of recall latency on the 10x run."

## Cause of death
**K2: ID recomputation > 10% of recall latency.**

## Evidence
- 1x K2 benchmark (r1 prose, 84,731 leaves, 63,547 compositions):
  - T_recall (leaf + composed): 124.1s
    - leaf_recall: 0.95s
    - composed_recall: 123.1s (includes per-recall SHA-256 verify)
  - T_recompute (standalone parent-ID SHA-256 + map lookup): 32.1s
  - Ratio: 32.1 / 124.1 = 25.8% — exceeds 10% kill bar.
  - Verdict: KILLED.

- The 10x run (847,310 leaves, ~635k compositions) is in progress to
  confirm the binding verdict. The 1x result (25.8%) already exceeds the
  bar by 2.5x; scale will not improve the ratio (both numerator and
  denominator scale linearly with composition count).

## Mechanism
Counter IDs composed canonically (sorted ascending) for multi-span units;
max composition depth frozen at 2. Parent ID = SHA-256 of canonical
encoding. Verification recomputes SHA-256 on every recall.

## Why it died
The SHA-256 verification cost dominates recall latency. Each composed
recall recomputes the parent ID (SHA-256 of 10B or 66B encoding) to
verify cache integrity. At 63k compositions, this costs 32s standalone,
25.8% of total recall time. The security/integrity benefit does not
justify the latency cost under the frozen kill bar.

## K1 (for the record)
PASS: Single-byte leaf edit invalidated 2/63,547 compositions (0.003%),
well under the 25% kill bar. The tree structure localizes invalidation.

## 1x battery (for the record)
All applicable legs PASS except m7-1x (re-run pending after accidental
process kill during investigation; not binding for K2 verdict).

## Disposition
**KILLED.** Do not promote. The compositional ID mechanism is
disqualified by its own binding kill criterion.

## Evidence preserved
- Source: `units/arms/M2/cl/arm.zag`
- Battery logs: `/home/hatch/workspace/m2scratch/battery_1x/`
- K2 logs: `/home/hatch/workspace/m2scratch/k2_10x*.log`
- Binary: `/home/hatch/workspace/m2scratch/m2_bin` (not committed)
