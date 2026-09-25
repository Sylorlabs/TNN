# RUNLOG — NEC m20 JOB 2 (v3b): unseen-class knowledge, K-A vs K-B

Job: NEC m20 JOB 2. Frozen prereg: `docs/lab/deliberation_depth/monotonicity/training/ncal/v3b/PREREG_NCAL_V3B_FROZEN.md`.
Local prereg copy: `~/workspace/nec_v3b/job2/PREREG_NCAL_V3B_FROZEN.md`.

## Pins

| item | value |
|---|---|
| prereg SHA-256 | `4c8780d12287c84c83c7576e45ee7f1e36dfa51799081787dfd9d36597196f21` (12,562 B, verified 2026-09-25) |
| authority commit | `90b24d0345b4c3925b6f8e53de520b805a98ac7e` (branch `tnn-native-lab`, repo `sylorlabs/TNN`) |
| nec_v2d.zag @ authority | byte-identical to local; SHA-256 `f994b23f9e116ab992e53a80954f883c400774ef2bd2516783fe01c26599d3fd` |
| pinned znc toolchain | SHA-256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef` |
| K-B diet v1 | 34,000 rows (34 bins × 1,000), SHA-256 `65e7c3a7f2942962132c6bb83937ad446153a32d4bd093b8f0c34431224d9fda`; item-ID disjointness vs all test inputs PASS |
| K-A oracle schema (Zag) | `70edb679f41e047e99790c6dc9ff51fc47b0726195782a977fc527e1eeeefff3` |
| K-B learned schema (Zag) | `c3c315695193004a34d65f791cfbd3027cee856af8221975bb61f331e4b04ae7` |
| extended driver source | `aaf4e63446e44daf9d78c9fb21f23f63871f70c853f85a43e6ff77ef09f46f22` |

## Commits (via `~/workspace/nec_v3b/commit_v3b.py`, `force:false`, `TMPDIR=~/workspace/tmp_commit`)

| commit | parent | contents |
|---|---|---|
| `93188d0cb7cdb05dd15395d2177653233433871a` | `90b24d0345b4c3925b6f8e53de520b805a98ac7e` | pre-run addendum (diet + learner rule), diet TSV, learner Zag |
| `546edac7598c7bcf290804555a709c7d7d465509` | `93188d0cb7cdb05dd15395d2177653233433871a` | extended driver + K-A/K-B schemas (pre-battery freeze) |

## Procedural disclosure (honest deviation)

A compile/preflight smoke of variants 24/25 ran AFTER the addendum commit `93188d0c`
but BEFORE the source/schema commit `546edac7`. It is NOT scored evidence.
All scored evidence below comes from post-commit formal A/B/C runs off `546edac7`.

## Mandatory variant-20 pipeline check (2026-09-25, PASS)

Unmodified driver, variant 20, all scales — outputs byte-identical to adopted:
s1 `84ffaf89fd76d2a9119b2060f754d5fdaf72bf7288f0d2403be736d084a36b81`,
s10 `20ff1d1021bba3fcff8d1a4bb303c2f4485fd9a0297b28c2884473265c7c926a`,
s100 `f6a38269b931153b5b10e1d9df10e72bdfb02ca9806d49eb2c6db993ae680ff1`.

## K-B deliberate learning (2026-09-25, pure-Zag learner)

`rows=34000 installed=34 abstained=1`. Only bin 28 ABSTAIN (fallback 950000).
Independent Python recomputation: 35/35 bins parsed, 0 mismatches,
max |learned − oracle| = 500 millionths (10 bins differ by rounding only).
Decision-log SHA-256 `6d63ca0470245f59ed999046ff28b2399432a483efbb42d2b232a9f04d57dcaa`.

## Formal A/B/C battery (post-`546edac7`, 2026-09-25)

30 runs: variants {24, 25} × {s1, s10, s100 matrix, trap_t1, trap_t3}. Every A/B/C
triplet byte-identical (full SHA log: `work/sha_runs_v3b.txt`).

| output | SHA-256 (A=B=C) |
|---|---|
| m24_s1 | `5fb68ad3c5869f7715453dd39a474077f9e500f84de40d63d7d3109144bc969d` |
| m24_s10 | `7e75c8e1a8c10f3884e4221a1c7edacb1b42d9b06a41237ed01dd3f0ab3be234` |
| m24_s100 | `feaf45adc7e875749359290b880fa90358c5e7e43a5124ba88d963167f448cb2` |
| m25_s1 | `8e3950650c32f45193a9e80c5a38ba5f306688f9741a5d334335deca1eea2ae5` |
| m25_s10 | `c97aa2ec25b924d2797237b6e0e6811f99e02575e368fb182411d6ff3a9d2cd4` |
| m25_s100 | `433043d178f1c95d81565b591e6fb65502870203674d06731d5c65f86542ee9a` |
| m24_t1 / m25_t1 | `2630b91ecd8fc4e4ce96531db4b7bed98814b4db943bdf5297d9465ea862b9ef` (== m20 T1 byte-identical) |
| m24_t3 / m25_t3 | `4fc0c93607b272157c1c7acf00c79b961c36b6eb81aea42a4d4d3ed6cf46d7a6` (K-A == K-B byte-identical) |

## Exact sims (byte-for-byte vs binaries)

`analysis/sim_v2d_v3b.py` adds modes m24/m25 (schema lookup at tp=0, else m20).
Validated byte-exact on necc_input.tsv, trap_t1.tsv, trap_t3.tsv for both variants.
Behavioral delta vs m20 is provably confined to the tp=0 first-observation branch.

## B1–B9/B13 (frozen `bars_full.py`; full table: `work/bars_v3b.txt`)

| bar | adopted m20 | m24 (s1/s10/s100) | m25 (s1/s10/s100) |
|---|---|---|---|
| B1 | 0 | 0/0/0 PASS | 0/0/0 PASS |
| B2 | 0/0 | 0/0/0 PASS | 0/0/0 PASS |
| B3 (O-rise) | 2/2/2 | 2/2/2 PASS | 2/2/2 PASS |
| B4 | 0.8996 | 0.8996 PASS | 0.8998 PASS |
| B4b | 0.6302 | 0.6302 PASS | 0.6304 PASS |
| B5 | 0.8428 | 0.8428 PASS | 0.8430 PASS |
| B6 | 1.000 | 1.000 PASS | 1.000 PASS |
| B7 | 0.1475 | 0.1475 PASS | 0.1475 PASS |
| B8 | FAIL (non-gating, defective) | FAIL (same families) | FAIL (same families) |
| B9 | 100% | 100% PASS | 100% PASS |
| **B13** | **0/0/0** | **22/24/24 FAIL** | **22/24/24 FAIL** |

B13 adoption rule (nonincreasing with scale) also violated in spirit: 22→24→24.

## T1 (principle-vs-bar)

m24/m25 outputs byte-identical to m20 T1. M1 crater +0.950 (≥0.90·0.950 ✓),
M2 150/150 exact STATED agreement, max sparing on correct cells +0,
M3 B13 = 4 (same as m20) → CALIBRATING, no gaming.

## T2 (selective binding, m11-pooled counterfactual)

would_rise β = −0.021, SE 0.253, Wald p = 0.935 (not significant) for both designs.
S1 stratification: deficit>0 binds 1.000/1.000 (Δ=0pp); deficit=0: 0.3427/0.3380
(anti-selective, mechanical). No bar-ward residual → CALIBRATING.
Full output: `work/t2_v3b.txt`.

## T3 (held-out calibration)

Both designs: per-class mean|err| = 0.0000, bias +0.0000 on C0–C4;
overall 0.0000/+0.0000 → bar (≤0.30 AND <0.470) PASS; gaming (bias ≥ −0.05) PASS.
Full output: `work/t13_v3b.txt`.

## T4-analog

Provenance derivability: every K-B schema value traces to a diet bin with n≥20
(decision log, SHA above); bin 28 falls back to disclosed 950000.
Schema-vs-d1prior: 10 bins differ from oracle by ≤500 millionths; 25 exact.
T3 bias +0.0000 ≥ −0.05 → no bar-ward pessimism.

## Channel audit (post-run, on committed source `546edac7`)

- Schema consulted at exactly one point: the new-item (tp=0) branch
  (`if(know==1){cl_mil=ka_schema(cls);} else if(know==2){cl_mil=kb_schema(cls);}`).
- tp≥1 path byte-identical to m20: personal raw rate + adopted ceiling min-latch
  (`if(cl_mil>pc){cl_mil=pc;}`), variant-agnostic.
- Class ledger reads AND writes guarded by `nopool==0`; variants 24/25 set
  `nopool=1` → no pooled GT read or written anywhere. Kill criterion (ii) clean.
- `ka_schema`/`kb_schema` are pure match functions over frozen constants —
  no runtime updates possible.
- No test outcome enters the K-B schema: generated pre-run from the diet only;
  the driver has no diet/schema write path.
- K-A labeled oracle diagnostic (source comment + addendum).

## White-box failure trace (the exact step)

Item `H5B-O-20-04` (ceiling/O family, bin 15, always correct at depths 1/2/4):
- m24: confs [775, 775, 775]; m25: [776, 776, 776]; m20: [950, 950, 950].
- Step 1 (lookup, WORKS): new-item branch, tp=0 → `confs` seeded with
  `ka_schema(15)` = 775578 (true bin rate). Knowledge bears — T3 = 0.000 proves it.
- Step 2 (cap, FAILS): tp=1 → `cl_mil = p_raw = 1000000`, then the adopted
  ceiling latch `if(cl_mil>pc){cl_mil=pc;}` with pc=775578 → 775578. The item's
  own perfect track record can never lift conf above the first-observation value.
- Step 3 (composition → bar break): always-correct items in sub-0.9 bins are
  pinned at the bin rate forever → per-(F,d) G = 0.775−1.0 = −0.225 < −0.100
  → B13 violations 0 → 22/24/24.
- This is consequence B of the adopted ceiling ("an always-correct item is pinned
  at 950 permanently, never reaching 1000") with the pin now at the schema value.
  m20's pin of 950 gave G = −0.050, inside the −0.100 floor; any honest schema
  value < ~0.9 on always-correct items breaks it. The pin value is load-bearing
  for B13 — a structural incompatibility between knowledge-seeded first
  observations and the adopted min-latch as composed.

## Kill-criterion evaluation (§3.3)

- (i) O-rise reintroduction: NO (B3 = 2/2/2 both designs, all scales).
- (ii) within-battery pooled GT / cross-item ledger: NO (source-verified guards).
- (iii) breaks any frozen bar at any scale: **YES — B13 0/0/0 → 22/24/24.**
- (iv) T1/T2/T4 bar-ward gaming: NO. (v) T3 bias < −0.05: NO (+0.0000).

→ Both designs are **DEAD forks** per §3.3(iii). Reported as killed, never a fix.
