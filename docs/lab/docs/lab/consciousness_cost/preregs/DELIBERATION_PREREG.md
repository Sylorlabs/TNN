# Preregistration — SEAM 1: deliberation-depth cost (consciousness bill)

**Frozen:** 2026-09-23 22:54 PDT (2026-09-24T05:54:00Z). **Do not edit after
runs start.** Amendments, if needed, go in a new dated file; they never
rewrite this one.

**Question.** RESULTS_H5 measured deliberation cost in *rounds*. Rounds are
not a compute bill. This prereg converts rounds → measured wall-clock and
rounds → instrumented native op counts, and asks the trained-vs-untrained
question: does a calibrated stopping policy buy accuracy per unit compute,
or only less compute per unit accuracy?

**Prior result (input, not re-derived here).** `deliberation_depth/
results_v2/RESULTS_H5.md`: trap accuracy 0.000 / 0.331 / 0.961 / 1.000 /
1.000 at fixed depths 1/2/4/8/16; adaptive matches deep-16 accuracy
(1.000 everywhere, 877/877) with 54%/34%/12% fewer rounds on
admit/revoke/cost; trap mean 3.81 rounds; cap-16 never hit.

## 1. Arms (three, on the SAME batteries)

All arms run the frozen H5 batteries (`deliberation_depth/items_v2/`:
admit 248, revoke 113, logic 264, trap 127, cost 125; 877 items total),
through one instrumented harness binary built from a byte-copy of
`deliberation_depth/harness_v2/` plus additive instrumentation (§3). No
item, config value, or mechanism constant from the frozen sweep is
changed; the only source edits are: new file `dlb_time.zag`, an `ops`
counter field threaded through `DSt`, new stopping modes in
`dlb_delib.zag`/`dlb_cfg.zag`, per-item wall-clock timing in the driver,
and a fifth output file `metrics.jsonl`.

| Arm | Config | Mechanism |
|---|---|---|
| S1a FIXED-DEEP / ADAPTIVE TRAINED (exists) | `d1,d2,d4,d8,deep16,adaptive` (frozen `configs_v2/`, verbatim) | the frozen deliberation loop; fixed round counts or the calibrated §6 adaptive rule (ε=20 thousandths, k=3, cap 16) |
| S1b AUTOPILOT (new) | `auto.cfg` | **no deliberation loop.** One batch pass: all evidence (up to `evidence_cap`) applied to all hypotheses at once, no alive-set freezing, no ELIMINATE, no TEST; verdict = argmax (ties → lowest index); confidence = clamp(margin,0,1000). The "just answer" arm: single forward pass over the full context. `rounds_used` recorded as 1. Ledger: BEGIN, one EVIDENCE step (`batch ne=N`), ROUND, VERDICT. |
| S1c DELIBERATIVE-UNTRAINED (new) | `untut.cfg` (primary), `tocap.cfg` (secondary) | the full deliberation loop with an **uncalibrated** stopping policy. `untut`: stop iff `rounds ≥ 1` and `confidence ≥ 500` (thousandths) — a naive round-number threshold, no gain analysis, no stability, no calibration. Cap 16. `tocap`: no stopping intelligence at all — always run to the 16-round cap (natural termination still applies). |

Config values shared by the new configs are the frozen sweep values
(`elim_margin=900`, `refute_threshold=600`, `evidence_cap=64`,
`adaptive_max_rounds=16`); the new modes ignore keys they do not use,
exactly as `adaptive` ignores `conf_threshold`/`stability_window`.

## 2. What "trained" means here

"Trained" = the calibrated stopping policy from frozen DEPTH_DEF §6
(ε/k chosen by design and validated by the H5 sweep). "Untrained" = a
policy a builder would write with no calibration work: a naive
confidence threshold, or no stopping rule at all. No learning happens
during the runs in any arm; the contrast is calibrated vs uncalibrated
stopping, which is the honest form of the trained/untrained question for
this mechanism.

## 3. Instrumentation (frozen definitions)

**Wall-clock.** New `dlb_time.zag`: `time_ns()` calls
`clock_gettime(CLOCK_MONOTONIC)` via `_zag_raw_syscall(228, 1, ptr, 0,0,0,0)`
and returns nanoseconds (i64; -1 on error). The driver records `t0` before
and `t1` after each item's decision procedure. Per-item wall time includes
the decision mechanism **plus** the audit-ledger emission (SHA256 chain):
that is deliberate — the bill includes the audit cost of being conscious.
Ledger bytes/item are reported as the audit-memory footprint.

**Op counts (deterministic).** One *op* = one execution of an innermost
primitive of the decision mechanism, counted in a per-item `ops:i64`
counter on `DSt` (reset to 0 per item; threaded through `*DSt`, no
globals):
- one alive-check in the alive-count scan;
- one hypothesis scanned in a leader/runner-up recompute;
- one evidence weight application (one support link or one attack link);
- one hypothesis compared in the ELIMINATE scan;
- one (evidence, attack-link) pair examined in the TEST refutation scan;
- one absolute-gain computed in the §6 adaptive check;
- autopilot: one weight application, or one hypothesis in the final scan.

Ledger/JSON/SHA256 work is **excluded** from ops (audit overhead, reported
separately via wall-clock and ledger bytes). Ops are deterministic: they
must be byte-identical across runs (gate G2).

**Memory footprint.** Deterministic by construction; reported as computed
constants from the allocation sizes: per-item arenas (item 17,536 B +
state arenas, hist sized by config cap) and fixed process buffers (item
buffer 4 MiB, results buffer 4 MiB, ledger buffer 8 MiB), plus measured
mean ledger bytes/item per config.

**Metrics output.** Fifth output `metrics.jsonl`, one object per item:
`{"id","wall_ns","ops","rounds","ev","correct"}`. It is NOT part of the
byte-identical determinism cmp (wall_ns varies run to run — that variance
is itself reported). `ops`/`rounds`/`ev`/`correct` must be identical
across runs.

## 4. Run matrix and gates

9 configs × 5 batteries × 3 runs = 135 cells. Every cell: rebuild from
source once per run (or reuse one verified binary per run — binary
rebuild byte-identity checked per run), run, `cmp` results+ledger across
the 3 runs.

- **G1 (determinism):** `results.jsonl` and `ledger.jsonl` byte-identical
  across all 3 runs in every cell.
- **G2 (op determinism):** `ops`, `rounds`, `ev`, `correct` fields of
  `metrics.jsonl` identical across the 3 runs in every cell.
- **G3 (accuracy re-derivation):** an independent Python checker recomputes
  accuracy per config per battery from `results.jsonl` vs the frozen
  ground truths; must reproduce the H5 numbers for the six retrained
  configs (d1/d2/d4/d8/deep16/adaptive) within exact equality — the
  instrumented rebuild must not change any decision.
- **G4 (timing sanity):** no `wall_ns` ≤ 0; per-item wall times reported
  as mean/min/max per config (VM noise is expected and reported, not
  hidden).

## 5. Analysis (preregistered)

Per config per battery: accuracy, mean wall-clock ms/item (= mean
wall_ns / 1e6), mean ops/item, mean rounds/item, mean evidence/item,
mean ledger bytes/item. Derived: accuracy per 1k ops, accuracy per ms,
ops/round. The headline comparisons:

1. **rounds → ms**: the measured exchange rate (mean ms/round per
   battery) — the bill's core conversion.
2. **rounds → ops**: mean ops/round per battery — how much native work a
   "round" actually is.
3. **trained vs untrained**: adaptive (S1a) vs untut/tocap (S1c) on
   accuracy-per-ms and accuracy-per-1k-ops. Verdict rule: if untut
   matches adaptive accuracy at lower ms, the finding is "the calibrated
   rule buys nothing on these batteries" (and §8 limitations of RESULTS_H5
   apply: only the trap battery discriminates); if adaptive wins on
   accuracy-per-compute, training buys accuracy per unit compute; if
   untut wins on ms at equal accuracy, training buys less compute per
   unit accuracy.
4. **autopilot**: where S1b wins/loses vs S1a/S1c, with mechanism — the
   report must name the mechanism (e.g. "batch pass consumes all evidence
   at once; sequential rationing is what creates the depth effect").

## 6. Falsifiers / stop rules

- If G1 or G2 fails in any cell: stop, root-cause the nondeterminism,
  record, do not report timing numbers from that cell.
- If G3 fails (instrumented rebuild changes any verdict vs RESULTS_H5):
  stop — the instrumentation is not additive; fix and re-freeze.
- If any `wall_ns` ≤ 0: the clock path is broken; stop and fix.

## 7. Outputs

Raw: `docs/lab/consciousness_cost/deliberation/RAW_RESULTS.md` +
per-cell logs under `docs/lab/consciousness_cost/deliberation/logs/`.
Binaries and `.zagd` files are never written under `docs/`; build
scratch lives in `tnn-lab/consciousness_cost/`. Nothing is committed by
this crew (parent commits).
