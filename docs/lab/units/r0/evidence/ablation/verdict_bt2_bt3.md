# Verdict sheet — B-T2 / B-T3 (crew B-ABLDOSE, R0)

Date: 2026-09-21. Prereg FROZEN (Micah signed 2026-09-21), §2 R0.1 batteries 2–3.
Manifest: `docs/lab/units/r0/evidence/ablation/MANIFEST_BT2_BT3.md` — frozen and
committed BEFORE any evidence run (commits `d8eaefa5`, `10a64cf8`, `30fa2f19`;
amendments document the leg-1 promotion scope and the M8 mode-4 clarification).
Binaries: `b_t2.zag` / `b_t3.zag` (pure Zag, zero RNG in AI decision paths),
built with `znc_linux_x86_64_abed8aa1`, seed 20260921 (environment inputs only).
1x only per R-9.

## B-T2 causal ablation (200 hard-grounding occurrences, label-3 per R-1)

| leg | params | raw (/1000) | chunk (/1000) | dual (/1000) | dual−raw (/1000) | ratio (/1000) | ledger |
|---|---|---|---|---|---|---|---|
| 0 | recovered | 950 | 550 | 950 | 0 | 1417 | 2048 |
| 1 | re-derived | 950 | 250 | 950 | 0 | 1195 | 1008 |

- Leg 0: 24/24 vocabulary spans promote; chunk recall succeeds exactly on the
  22 consistent vocabulary spans (110/200); rare (seen=2<5) and novel (unseen)
  spans have no chunks (80/200); 10 inconsistent-span occurrences excluded
  from label-3 by b=0. Ordering chunk < dual = raw holds.
- Leg 1 (stricter re-derived gate: seen≥6, purity≥0.40): 12/24 spans
  promote (88 total promotions); chunk=250/1000.
  The structural ordering chunk < dual = raw survives the tighter inventory —
  the ablation conclusion is robust to the re-derived parameters.
- Near-twin set (192 trials): reference-only, no bar. Leg 0: raw 609, chunk
  468, dual 468 (/1000). Leg 1: 609 / 609 / 609.

## B-T3 dose curve (dual hard-grounding score, /1000)

| leg | 250 | 500 | 1000 | 2000 | 4000 | 8000 | non-decreasing | max drop (/1000) |
|---|---|---|---|---|---|---|---|---|
| 0 | 950 | 950 | 950 | 950 | 950 | 950 | 1 | 0 |
| 1 | 950 | 950 | 950 | 950 | 950 | 950 | 1 | 0 |

Dual score is flat at 950/1000 from the lowest dose in both legs: the 24-span
vocabulary is fully learned by dose 250 and additional dose only grows the
compression ratio (leg 0: 1234→1898 /1000 across doses) and saturates the
ledger (2048 entries from dose 500).

## M8 adversarial-allocation battery

Every config/leg: perturbations 0–4 + repeated perturbation-0 run; stdout and
stderr byte-identical across all six runs; expected-value readback probe and
golden mini-run passed in every invocation. (Mode 4 = free-list reversal +
mid-run churn; modes 0–3 pre-run only.)

| config | leg | byte-identical 6/6 |
|---|---|---|
| B-T2 | 0 | YES |
| B-T2 | 1 | YES |
| B-T3 | 0 | YES |
| B-T3 | 1 | YES |

## Bar mapping

- R-1 (label 2*a+b): hard-grounding battery implements label-3 = recall
  success AND cross-occurrence consistency (b=0 for the 10 inconsistent-span
  occurrences). Reported per route.
- R-3 (causal ablation): descriptive bar (chunk < raw, chunk < dual) —
  **PASS** in both legs. Formal numeric ε and minimum compression ratio are
  **PENDING-MICAH-AMENDMENT** (proposed: |dual−raw| ≤ 25/1000, ratio ≥ 1.2).
  Measured: dual−raw = 0/1000 (leg 0), 0/1000 (leg 1);
  ratio = 1417/1000 (leg 0), 1195/1000 (leg 1).
  Note: leg 1's ratio (1.195) sits just below the proposed 1.2 minimum — the
  tighter re-derived inventory compresses less. The formal bar needs Micah's
  numeric decision precisely because the legs disagree here.
- R-4 (dose curve): descriptive bar (flat / non-decreasing) — **PASS** in both
  legs (max adjacent drop 0/1000 leg 0, 0/1000 leg 1).
  Formal degradation tolerance **PENDING-MICAH-AMENDMENT** (proposed ≤ 25/1000).
- R-7/R-8: both legs run (argv-selected, one binary per config). R-9: 1x only.
- Scorecard follows `METRICS.md` (flags-as-strings). Known conflict: the
  harness `ARM_INTERFACE.md` disagrees on flag encoding; this battery follows
  METRICS.md and records the disagreement (no silent deviation).

## Honest limitations

- The ledger saturates at 2048 entries (leg 0 B-T2; B-T3 from dose 500): the
  frozen harness stops appending silently at capacity. Trust-update entries
  past saturation are dropped, not applied — disclosed, not hidden.
- Compression ratio measures the dual indexing layer only (chunk payload +
  4-byte index references + literal bytes vs source); raw evidence remains
  externally available and is not deleted.
- The twin probe is reference-only; the battery makes no discrimination claim.
- Development/debug runs (fixed-filler calibration, 0x7F probe-filler
  diagnosis) are NOT evidence; only the post-freeze M8 matrix counts.

## Recommended follow-ups (for parent / Micah)

1. Micah to set the R-3 numeric ε and minimum compression ratio, and the R-4
   degradation tolerance (proposals above).
2. R-9: 10x replication once 1x bars pass — needs the 10x harness schedule.
3. Consider a leg-1 variant with re-derived parameters that promote 24/24
   (e.g. larger inventory) to separate "stricter gate" from "different
   derivation" effects.
