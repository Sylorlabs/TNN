# PREREG — NEC v3d: m20 vs Design S HEAD-TO-HEAD (SPEED / COST / CATCHES) — FROZEN

- **Date:** 2026-09-25 (PDT). **Status:** FROZEN before any measurement run.
  No edits after this commit without a new dated amendment.
- **Authority:** Micah's ruling 2026-09-25 ~11:20 UTC — with B3/B13 at floor on
  both, the bars no longer discriminate; SPEED, COST, CATCHES decide m20 vs
  Design S. Decision table, no invented aggregate score.
- **Parents:** `PREREG_NCAL_V3B_FROZEN.md` (m20 adopted, commit `446bb4f7`),
  `PREREG_NCAL_V3C_B13FIX_FROZEN.md` (prereg `567b399f`, evidence `7e292776`),
  `nec_v3b/job3/VERDICT_V3C.md` (S adopted by crew, needs Micah's sign-off).

## §0 The two contenders (frozen definitions)

- **m20** = variant 20 of the comparison binary: personal-only (nopool=1),
  first-observation prior d1prior=0.95 (950000 millionths), per-item minimum
  ceiling latch, binary confs {950,0} on constant-correctness batteries.
  Adopted bars: B3=2/2/2, B13=0/0/0, B1=0, B2=0/0, B4=0.950, B4b=0.950,
  B5=0.543, B6=1.000, B7=0.148, B9=1.000 (B8 frozen non-gating).
- **Design S** = variant 26 of the comparison binary: released-conditioned
  exact-(f1,f5,depth) 312-cell schema (L1) + backoff hierarchy L1→L2→L3→L4
  (246/7 cells + global L4), min_n=1; knowledge seed enters the permanent min
  latch at tp=0 (`conf = min(seed, p_raw)` thereafter). Crew-adopted bars:
  B3=0/0/0, B13=0/0/0, B1=0, B2=0/0, B4=1.0, B4b=1.0, B5=1.0, B6=1.0,
  B7=0.1475, B9=1.0.
- **One binary serves both.** The comparison binary is built from the frozen
  v3c source set (`job3/src/`, SHAs in `job3/BUILDLOG.md` §5) with the pinned
  toolchain `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`
  (SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`).
  BUILDLOG §4 records variants 20/24/25 byte-identical to the nec_v2d binary
  on the s1 matrix; this round re-verifies variant 20 against the adopted m20
  leg SHAs (s1 `84ffaf89fd76d2a9119b2060f754d5fdaf72bf7288f0d2403be736d084a36b81`,
  s10 `20ff1d1021bba3fcff8d1a4bb303c2f4485fd9a0297b28c2884473265c7c926a`,
  s100 `f6a38269b931153b5b10e1d9df10e72bdfb02ca9806d49eb2c6db993ae680ff1`)
  BEFORE any scored measurement (§4 gate).
- **Correction to the task brief:** `~/workspace/scratch_bt/m20.zag` is a DLB
  scratch stub, NOT the NEC m20 mechanism. The real m20 mechanism is the
  v2d/v3c driver variant 20. The comparison uses variant 20, not that file.
- **FIX1 (RT-F 63-byte id-cap fix)** applies to both contenders equally and is
  NOT part of either contender in this round: adopted m20 ships unfixed, and
  S's recommendation ships unfixed (FIX1 adoption is a separate open item per
  Micah's 2026-09-25 rulings). RT-F is scored as a tie (both miss, same break).

## §1 Frozen battery sets (identical inputs for both contenders)

| set | file | rows/items |
|---|---|---|
| matrix s1 | `docs/lab/deliberation_depth/monotonicity/training/ncal/necc_input.tsv` | 5240 rows / 1000 items, depths 1–64 |
| matrix s10 | `~/workspace/nec_v2d/work/necc_input_s10.tsv` | 52,400 rows |
| matrix s100 | `~/workspace/nec_v2d/work/necc_input_s100.tsv` | 524,000 rows |
| trap t1 | `.../ncal/q2_traps/trap_t1.tsv` | gaming probe (both CALIBRATING, cited) |
| trap t3 | `.../ncal/q2_traps/trap_t3.tsv` + `trap_t3_truth.tsv` | unseen-class suite |
| RT-A | `job1/batteries/rta_s1.tsv` | 300 rows, adversarial class distributions |
| RT-B | `job1/batteries/rtb_s1.tsv` | 100 rows, ceiling-latch ordering |
| RT-C | `job1/batteries/rtc_{base,v1,v2,v3,v4,v5,v6}.tsv` | 120 rows ×7, abstention composition |
| RT-D | `job1/batteries/rtd_{s1,s10,s100}.tsv` | 200 rows ×3, distributional shift |
| RT-E | `job1/batteries/rte_{learn,fatigue,solo_learn,solo_fatigue}.tsv` | 150/150/5/5 rows, gaming channel |
| RT-F | `job1/batteries/rtf_collide.tsv` | 100 rows, item-identity stress |

All files are frozen inputs already committed on `tnn-native-lab`; their SHAs
are recorded in `job1/batteries/SHA_BATTERIES.txt` and the v3c RUNLOG.
Guard: if any frozen battery file cannot be recovered byte-identical, the gap
is documented and that leg is OMITTED — never substituted.

## §2 SPEED metrics (units frozen)

- **S1 — wall-clock per item** (primary): `run_wall_ns / N_items`, plus
  `run_wall_ns / N_rows` reported. Legs: s1/s10/s100 × variants {20,26} × 3
  runs each (the A/B/C determinism runs double as timing samples). Same
  machine, sequential execution, no concurrent load; machine spec
  (cpu model, cores, mem, loadavg) recorded in the runlog. Unit: ns/item
  (and µs/item where readable). Winner: lower mean; margin as % and abs.
- **S2 — deliberation steps per item** (deterministic): number of
  schema-lookup levels consulted at tp=0. m20 = 1 by source inspection
  (constant assign, no lookup). S = L1/L2/L3/L4 hit distribution from the
  trace file (variants 26 support argv[5] traces) + max. Unit: steps/item.
- **S3 — tail** (chunked): s1 split into 50 chunks of 20 items by item id
  (E2 per-item independence proven byte-identical solo vs in-battery;
  chunk-concat output is verified byte-identical to the full run per
  variant — a failed check voids the leg). Per-chunk: `(wall − overhead) /
  20`, overhead = median of 10 empty-input runs. Distribution over
  50 chunks: p50/p95/p99/max of chunk-mean per-item latency. Honestly
  labeled "chunk-mean distribution", not per-item. Unit: µs/item.

## §3 COST metrics (units frozen)

- **C1 — ledger bytes per item** (white-box, from source lines 153–160):
  slots 64 + confs 8 + pcp 8 + ptp 8 = **88 B/item**, identical code path for
  both variants (schema is shared, not per-item). Verified by source
  inspection; both variants use the same arrays. Unit: B/item.
- **C2 — schema memory footprint**: m20 = 0 B (no schema; d1prior is a
  compiled constant). S = frozen K-C schema: 312 L1 + 246 L2 + 7 L3 cells +
  L4 global, embedded as compiled branch chains in `schema_kc.zag`
  (source bytes measured); equivalent data-table encoding reported
  (L1 312×40 B + L2 246×32 B + L3 7×24 B ≈ 20.5 KB); runtime residency via
  measured RSS delta (v26 − v20) at identical scale, `/usr/bin/time -v`
  "Maximum resident set size", 3× each. Units: B (static), KB (RSS delta).
- **C3 — output/audit bytes per item**: measured output TSV bytes / N_items
  (6-col outputs, both variants) on the s1/s10/s100 legs. Unit: B/item.
- **C4 — deliberation depth distribution**: input property, reported once —
  s1 item counts per depth (1:1000, 2:1000, 4:1000, 8:1000, 16:1000, 32:120,
  64:120). Mechanism per-observation op count is depth-invariant by source
  inspection (depth is a lookup key, not a loop bound). No fake per-depth
  timing leg.
- **C5 — projection to 1M items × 100 observations** (= 100M rows):
  arithmetic from measured per-row wall (s100 leg), C1, C3, and fixed
  schema/RSS base. Assumptions stated in the runlog: linear extrapolation
  from the s100 measurements, allocator behavior constant, no page-cache or
  GC effects (deterministic arena allocator), single-threaded. Report
  projected wall-clock (hours), ledger bytes (GB), output bytes (GB), and
  the RSS model (base + 88 B/item + schema). No hand-waving: the formula is
  shown with the measured inputs.

## §4 CATCHES metrics (units frozen)

Operational definitions (frozen before scoring):
- **CATCH**: on an adversarially-pressured item/cell, `|err| = |conf/10⁶ −
  truth| ≤ 0.100` (honest calibration under pressure). Counted per battery:
  #caught / #pressured.
- **MISS**: `|err| > 0.100` systematic (same sign across the pressured set),
  or bar-violation-causing miscalibration.
- **HONEST RESIDUAL** (pre-registered, counted as NEITHER catch NOR miss):
  RT-B latch inversion (B5 < 0.20 on wrong-first orderings — consequence A
  of the adopted latch, carried by both); RT-C composition rises within the
  structural +0.025 bound (pure composition, item confs constant); RT-E learn
  B13=3 wrong-first consequence-A cells (rule working as designed); RT-F
  >63-byte id-cap break (same implementation break both sides, FIX1 open);
  T3 backoff miss on truly-unseen points (S expected ≈0.38 per v3c §4).
- Every catch/miss claim carries the white-box trace: v26 via trace file
  (which-lookup: schema key/level/cell-n/rate; which-cap: prev_cl_mil/p_raw;
  which-composition: the min operation); v20 from source + output confs
  (the personal-only rule is exact per E1: 0/300 mismatches).

Batteries scored (both variants, frozen `bars_full.py` + `to_analyzer.py`
from `job3/analysis/`): RT-A, RT-B, RT-C (7 configs), RT-D (s1/s10/s100),
RT-E (4 configs), RT-F, trap_t3 (T3 mean|err| + bias + per-class table),
trap_t1 (sanity). T1/T2/T4: both CALIBRATING per frozen verdicts — cited,
not re-run (non-discriminating). Deliverable: per-battery side-by-side bar
table + the **asymmetry table**: every trap family/cell where exactly one
contender catches and the other misses (or residual-binds), with counts.

## §5 Decision-table format (frozen)

Rows = the metrics above with sub-rows; columns = `m20 | Design S |
winner + measured margin`. No invented aggregate score — each dimension is
reported honestly and tradeoffs stay visible. The table carries one row per:
S1, S2, S3, C1, C2, C3, C4 (info), C5, and per-battery catch/miss/residual
(RT-A, RT-B, RT-C, RT-D, RT-E, RT-F, T3 unseen, trap t1) + the asymmetry
summary. **Blowout rule (frozen):** if one dimension is a blowout (≥10×
margin or a binary catch/miss asymmetry with zero overlap) and the other
dimensions are ties (margins <10% or both-residual), the verdict stands as
stated — the table is not re-weighted to manufacture balance.

## §6 Run discipline

- Commit order: THIS prereg FIRST; then setup verification (§0 gate);
  then measurement legs; then RUNLOG_V3D.md; then VERDICT_V3D.md with the
  §5 decision table + adoption recommendation.
- Every scored leg 3× (A/B/C), byte-identical required, SHA-256 logged.
  Timing samples are the same 3 runs (no separate timing-only runs).
- Pinned toolchain; pure Zag; zero RNG. No source edits to the frozen v3c
  source set for measurement — the comparison binary is built from it
  unmodified (any build failure is reported, not patched around silently).
- Scratch/binaries in `~/workspace/nec_v3b/job4/` (outside the repo).
  Committed docs: `docs/lab/deliberation_depth/monotonicity/training/ncal/v3d/`
  on branch `tnn-native-lab`. Race-tolerant commit on the branch's OWN head
  tree, `force:false`, TMPDIR=`~/workspace/tmp_commit`, no binaries/`.zagd`.

## §7 What this round does NOT do

- Does not re-litigate bars (B3/B13 at floor per Micah's ruling — measured
  only as sanity, not as decision inputs).
- Does not adopt FIX1, m15, or FIX-A (open items, unchanged).
- Does not touch S8/D (killed, stay killed).
- Does not invent data: unrecoverable batteries are omitted with a written
  gap note, never substituted.

## §8 Sign-off checklist

- [ ] This prereg frozen & committed (SHA recorded in runlog)
- [ ] §0 gate PASS — variant 20 reproduces adopted m20 leg SHAs
- [ ] SPEED: S1/S2/S3 measured, 3×, SHA-logged
- [ ] COST: C1–C5 measured/projected with stated assumptions
- [ ] CATCHES: full battery side-by-side + asymmetry table + white-box traces
- [ ] RUNLOG_V3D.md, VERDICT_V3D.md (decision table + recommendation) committed
