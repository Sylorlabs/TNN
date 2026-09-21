# VERDICT.md — B-16 (Fixed-size chunks, S=16), Track A, round r1 1x

**Date:** 2026-09-20 (PDT). **Crew:** ARM CREW B-16. **Prereg:** `b0b9140c0eda`.

## 1. Verdict: B-16 SURVIVES at 1x — not retired, family not killed

- **1x bars:** M1/M2/M3/M4/M6/M8 all pass. M5 cost bars FAIL (3.626 B/B source,
  64.189 entries/KB) — same diagnostic FAILs the reference validator carries
  (1.719 / 16.189). M7 N/A (no ID layer, per §9 classification).
- **Retirement rule** ("a size retires when another B size strictly dominates
  it on M1/M2/M3 both corpora"): **not triggered.** B-64 ties B-16 exactly on
  M1 (100/100 both corpora), M2 (ETC 1 all tiers), and M3 (100.0/100.0/CLEAR
  all subfields). A tie is not strict dominance. No evidence either way from
  other B sizes except B-8 (below).
- **Family kill rule** ("any smart arm beats the best B size by ≥2x on M3 at
  equal-or-better M1"): **no qualifying evidence in front of this crew** — no
  smart-arm 1x rows were available at verdict time. Note: the best B size
  holds M3 at its ceiling (100.0), so a ≥2x beat is arithmetically unreachable
  while any B size sits at 100% — the kill bar as written can only fire after
  a B size first drops below 50% on M3. Flagged for the coordinator, not
  re-interpreted.
- **B-8 observation (for the coordinator):** B-8's self-reported 1x row
  (`units/arms/B-8/run/battery_r1/scorecard_r1_1x.json`) shows M3 fresh_recall
  67.6 and `FROZEN-UNDER-PRESSURE` with M1/M2 tied at ceiling — i.e. B-64
  strictly dominates B-8 on M1/M2/M3, which meets B-8's binding retirement
  condition. Retirement action belongs to the coordinator / B-8 crew; B-16
  takes no position on whether B-8's row reflects a real mechanism signal or a
  build defect.

## 2. Complete 1x row (metrics-v1)

| Metric | prose | code | notes |
|---|---|---|---|
| M1 recall / boundary | 100.0 / 100.0 | 100.0 / 100.0 | units 338,921 / 594,709 |
| M1 ID probe | — | — | N/A (no ID layer) |
| M2 T1 ETC | 1 | 1 | final 100.0/100.0 |
| M2 T2 ETC | 1 | 1 | final 100.0/100.0 |
| M2 T3 ETC | 1 (synthetic) | — | final 100.0/100.0 |
| M3 survival / fresh recall | 100.0 / 100.0 | — | freeze CLEAR, mgmt 8,050, weaken 50/50 |
| M4 rev boundary / content | 100.0 / 100.0 | 100.0 / 100.0 | kill_rate 0, 1 episode |
| M5 mem/src byte | 3.626 (FAIL ≤1.5) | — | prose leg |
| M5 audit/KB | 64.189 (FAIL ≤10) | — | 339,921 ledger entries |
| M6 tax p2c / c2p | 0.0 / 0.0 | — | validity gate PASS; memorizer drop 54.8 / −54.8 (≥15pt ✓) |
| M7 | — | — | N/A (no ID layer); re-read bytes 80,000 |
| M8 | — | — | M8GATE PASS |
| M9 shape | fast-then-flat, takeoff 1 | fast-then-flat, takeoff 1 | informational |

Full JSON: `scorecard_r1_1x.json` (this directory).

## 3. 10x status

**Not attempted.** The frozen r1 harness defines only 1x legs: no `corpora/r10`
exists and no arm — including the b64 validator — has a 10x row. Per C15 this
is "not attempted (10x undefined in the frozen r1 harness)", not
"ATTEMPTED — FAILED". Forward caveat for the coordinator: this binary's M8
ledger is capped at 2,097,152 entries while a 10x M8 leg would need ~9.5M;
a 10x attempt requires a shard-count bump and re-validation.

## 4. Determinism (K-DET)

- 18/18 battery legs: rc1=rc2=0, stdout byte-identical across reruns.
- M8: 5 perturbations × 2 reruns, all rc=0; `store_hashes.txt`,
  `store_chain.txt`, `ledger_chain.txt`, `alloc_trace.txt` byte-identical
  across all 10 runs (hashes in `logs/m8_artifact_hashes.txt`).
- M8 ledger: 945,680 entries, ledger.bin = 60,523,520 B = 945,680 × 64 —
  complete, zero truncation. **No K-DET disqualification.**

## 5. What the numbers say about the mechanism

- B-16 ≡ B-64 on every scored behavioral cell (M1–M4, M6, M8). Finer
  granularity bought nothing and cost nothing on the scored bars — consistent
  with the design's "does boundary placement matter, or just existence?"
  framing: at these bars, existence alone suffices.
- M5 prices the granularity: 3.626 B/B source vs B-64's 1.719 (~2.1×) and
  64.2 vs 16.2 entries/KB (~4×, exactly the chunk-count ratio — the audit
  cost is per-unit, the memory cost amortizes sublinearly). Both FAIL their
  bars, as does the validator; M5 is not in B-16's retirement criterion.
- M3 fresh units are 16B chunks here (B16-A1): the schedule's unit counts and
  pressure structure are identical to the validator's; only the byte range
  differs. If the coordinator rules M3 fresh units must be 64B spans for all
  B sizes, this arm re-runs with a 4-chunk-per-unit M3 path (mechanical).

## 6. Ambiguities & caveats

- B16-A1 (M3 16B fresh units), B16-A2/A3 (sharded ledger, per-array M8
  hashing — forced by the znc 2^25 limit), B16-A4 (non-ID-layer
  classification), B16-A5 (degenerate M9): see `AMBIGUITIES-B16.md`.
- `store_chain.txt`/`ledger_chain.txt` use the documented order-preserving
  chunked constructions (ARM_SPEC.md §5); M8 self-comparison (C13) is
  unaffected.
- B-8's row is cited from the B-8 crew's own run directory, not
  coordinator-certified.
- The family-kill ≥2x-on-M3 bar is unreachable while any B size holds M3 at
  100% — coordinator may wish to clarify whether "2x" is meant against a
  non-ceiling baseline (e.g. churn or cost), but this crew applies the prereg
  literally and does not amend it.

## 7. Commits

(appended after `commit_to_branch.py` runs; sources + docs + evidence only —
no corpora, binaries, `.zagd`, or transient battery work)
