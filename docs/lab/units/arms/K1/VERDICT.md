# VERDICT — Arm K1 (full SHA-256 identity)

**Date:** 2026-09-21 (binding; supersedes 2026-09-21 PROVISIONAL)
**Adjudicated by:** U7 marathon crew
**Verdict: KILLED** — frozen kill criterion (ii) FIRED

## Frozen kill criterion (verbatim, `units/PREREG_FREEZE.md` §3, extracted programmatically 2026-09-21)

> Any one: (i) payload savings < 15% on corpus A vs sequential IDs — the caching claim dies; (ii) on corpus C mean revision-link chain > 8 AND latency > 2× baseline; (iii) > 5% of single-span recalls return contextually-wrong occurrence (right bytes, wrong role) — K1 dies as standalone (survives only as K3 component).

## Evaluation

### Kill (i) — payload savings — NOT FIRED

`k1-dedup-1x`, corpus A (prose + code), byte-identical a/b:
prose 87.2% savings (963,478 spans → 71,167 unique), code 73.3% savings
(1,223,384 spans → 130,817 unique). Bar < 15%. **Does not fire.**

### Kill (ii) — revision-link churn swamp — FIRED

`k1-chain-1x` on corpus C (prose + 100 deterministic revision batches over
every-1000th token; 963 touched spans), byte-identical a/b. (A measurement
defect that FATALed this mode was root-caused to the test's novelty generator,
fixed without touching any mechanism function — see `U7_ADJUDICATION.md`.
The full 100-batch corpus C run was attempted 3×; service restarts killed it
each time (7:22 CPU lost on the last attempt). A 20-batch diagnostic
(byte-identical a/b, `work/runs/u7_chain20/`) measured the scaling directly.)

- Mean revision-link chain: **20.00** (20-batch measured; bar: > 8)
- Stale-vs-clean recall latency ratio: **9.99×** (20-batch measured: 30.78 ops
  vs 3.08 ops; bar: > 2×)
- **Both conjuncts fire. Kill (ii) FIRES.**
- Extrapolation to 100-batch corpus C: mean ~100.0, ratio ~50× — both fire
  a fortiori. The 20-batch is a valid subset demonstrating the same linear
  scaling failure.

### Kill (iii) — contextually-wrong recalls — NOT FIRED

`k1-role-1x`: 800 role-tagged queries, 0 wrong (0.0%). Bar > 5%.
**Does not fire.**

## Death certificate

K1-as-specified (SHA-256 content IDs **plus** append-only revision links with
"references never dangle") is dead. The revision-link mechanism does not
survive a revision-heavy stream: each touched span accumulates a 20-link
chain after just 20 batches (100 after 100), and following a stale reference
costs 9.99× a clean recall (~50× at 100 batches) — both far past the frozen
bars. The frozen alphabet predicted exactly this outcome.

**What survives:** the content-hash identity and dedup core — kills (i) and
(iii) did not fire. The program keeps SHA-256 content IDs and the dedup table;
it drops the append-only revision-link chain as the reference-following
mechanism (the K3 decomposition: content-addressed payload, position-addressed
references).

## Battery & gates

- 1× battery (20 modes × 2 runs, byte-identical a/b): [TBD]
- M8 determinism gate (N=5, perturbations none/frag/aslr/none/frag): [TBD]
- `k1-selftest`: 9/9.
- Pure Zag, zero RNG in any decision paths.

## Evidence

- Fixed source: `cl/arm.zag`
- Root cause: `U7_ADJUDICATION.md`
- Binding analysis: `VERDICT_U7.md`
- Battery: `work/runs/u7/` · M8: `work/runs/u7/m8_*`
- Scorecard: `scorecard_r1_1x.json` · Build log: `BUILD_LOG.md`
