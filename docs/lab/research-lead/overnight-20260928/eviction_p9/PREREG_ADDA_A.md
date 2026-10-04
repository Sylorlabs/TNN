# PREREG ADDENDUM A -- MISSION ITEM 2: DEDICATED ROOT-CAUSE OF THE 20k Q1 HANG

Added 2026-10-04 by SCALING-EVICT, lane `lane/eviction`. Frozen BEFORE the
counters were committed, and BEFORE any 20k run completed under them.
Sections 1-10 of `PREREG.md` are UNCHANGED. No bar in that file is moved.

## A0. THE OBSERVATION TO BE EXPLAINED

Inherited (C534 / P8 lane): at 20000 MAPs the build completed and Q0 was
correct, but Q1 never returned (INCOMPLETE after 5m53s). At 10000 MAPs the same
9-phase battery finished in 1.48s with 417,172 visits. So the blow-up is
localized to the 10000 -> 20000 transition and to the SECOND query.

Three structural candidates were identified BY READING THE CODE, not by
profiling, and each is a superlinear scan that is NOT in the retrieval path:

* `comb_present(W)` — unconditional loop `n = 2 .. NN-1` looking for the single
  tag-8 comb node. O(NN) per call, ~262,144 probes, and it is called from the
  contradiction path (`contradict_map`), i.e. once per candidate relation
  whenever a fact is contradicted.
* `t2_gather_sum(W,s,...)` — unconditional loop `x = 2 .. NN-1` over node ids
  to collect s's facts, O(NN) per call, called once per trial.
* `t2_chain(W,s,r,...)` — the candidate/path enumeration behind
  `t2_trial`; its branching factor grows with live nodes, so its cost grows
  with the LIVE NODE COUNT, not with the query.

These are exactly the shape of the residue described as "superlinear residue in
the `mp_run`/`t2_trial` fallback at ~20k".

## A1. INSTRUMENTATION (dedicated counters, preregistered)

Counters added, each incremented ONLY at the site named:

| key | name | site |
|---|---|---|
| 75 | `comb_present_probes` | loop iterations in `comb_present` |
| 76 | `gsum_probes` | loop iterations in `t2_gather_sum` |
| 77 | `subset_mask_iters` | inner `mask` loop iterations in `t2_trial` |
| 78 | `subset_assemblies` | `t2_asm_sum` calls from the subset loop |
| 79 | `asm_chain_calls2` | reserved |
| 80 | `asm_sum_cells` | cells summed per `t2_asm_sum` call |
| 81 | `trial_calls` | entries to `t2_trial` |
| 82 | `chain_branch_iters` | `while(p<np...)` iterations in `t2_chain` |
| 83 | `t2rels_calls` | `t2_rels` calls from the fallback branch |
| 84 | `evict_nontag20` | evictions of nodes whose tag != 20 (PROCEDURE) |
| 85 | `evict_total` | total evictions |
| 86 | `evict_foundational` | evictions of nodes with subject in [1000,1006) |
| 87 | `evict_junk` | evictions of nodes with subject in [20000,60000) |

`evict_total` is an identity check on 84+85+86+87 and MUST hold; a violation
means a node in the test world's subject space was not classified by any of the
three ranges, and is reported as such rather than silently dropped.

## A2. PREDICTION, FROZEN

**Prediction A2a (the hypothesis under test).** The 20k Q1 stall is caused by
`comb_present` and/or `t2_gather_sum`, i.e. by O(NN) full-arena scans on the
contradiction and trial paths, NOT by the retrieval indices (which are already
sublinear, C529-C534) and NOT by eviction cost.

Falsifiable signature: in a run that COMPLETES, `comb_present_probes +
gsum_probes` divided by MAP count grows by more than 4x going 5000 -> 10000
-> 20000 while `trial_calls`, `chain_branch_iters` and the P8 retrieval
counters stay within a small constant factor. If instead `trial_calls` or
`chain_branch_iters` is the dominant and superlinear term, A2a is FALSIFIED and
the trial chain is the cause.

**Prediction A2b.** If A2a holds, replacing those two scans with the existing
learner-maintained subject index (`sbkt`, the 4098-bucket FACT subject index
already built and used by the retrieval path in C529) makes `t2_trial` and
`contradict_map` sublinear WITHOUT changing any answer in the regime where
eviction never fires. K0b's prediction (the hang is an allocation artifact)
is a COMPETING explanation and is tested in the same run: `TOT` is already the
CORRECTED `WSZ()+P9X()` allocation (45221344 bytes, vs the inherited
7556800), so if 20k still stalls with the corrected allocation, K0b is
FALSIFIED and the corruption explanation is dead.

## A3. KILL BARS AND HONEST LIMITS

* **K0b is FALSIFIED, not confirmed**, if 20000 MAPs still fails to reach the
  Q1 answer under the corrected 45,221,344-byte allocation. K0b must then be
  recorded as falsified and the cause must be the scan residue above.
* If the 20000 MAP run does not complete inside the preregistered 900s
  watchdog limit, that is recorded as **TIMEOUT, INCOMPLETE** — a FAIL for the
  20k level, not a pass and not a reason to extend the limit.
* If NO counter is shown to be superlinear, the honest result is
  **INCONCLUSIVE / NOT ROOT-CAUSED**, and the 20k ceiling stands unexplained.
  A plausible story is not a root cause.
* Counters that overflow the i32 profiler range at 20000 MAPs are reported as
  saturated; they are not silently reported as exact.

## A4. FIX BAR FOR THE SCAN REPLACEMENT (only if A2a is confirmed)

`comb_present` and `t2_gather_sum` are replaced by lookups on the existing
learner-maintained structures. Kill bar: answers byte-identical to canonical at
1000/5000/10000 MAPs (`scan=5/6`, `ans=6205/6405` from C529), `comb_present_probes`
and `gsum_probes` reduced to O(1)-per-call bucket-walk counts, and 3/3
byte-identical stdout on every reported run. Correctness beats speed: an
answer difference is a hard FAIL, not a trade.