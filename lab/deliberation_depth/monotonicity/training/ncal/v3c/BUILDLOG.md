# BUILDLOG — NEC v3c Phase 1 (implementation, no scored runs)

- **Date:** 2026-09-25 (PDT). **Crew:** Phase-1 implementation.
- **Frozen inputs:** `PREREG_NCAL_V3C_B13FIX_FROZEN.md` (§3), `AMENDMENT_A1_V3C.md`
  (superseded for D), `AMENDMENT_A2_V3C.md` (Design D = v3b K-A + no latch — implemented).
- **Toolchain (pinned):** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
  All indexed tables in `[]u8` arenas with LE accessors (no `as []i32/u32/u16` anywhere).

## 1. Diet — `kb_diet_v3c.tsv`

- Script: `mk_diet_v3c.py` (deterministic, zero RNG), kept in job3/.
- Source: `~/workspace/nec_v3b/job2/work/necc_input.tsv` (7 cols id,fam,depth,f1,f5,rel,corr),
  kept rows with rel=1, emitted 6 cols `id f1 f5 depth correct prov`,
  prov=`kb-diet-v3c:matrix:<id>`.
- **Rows: 4467. SHA-256: `fc85209484424eb1efca20c49cb301960315cce5e2bbc4f29a02409b4d7889fe`**

## 2. Learner — `src/learn_schema_v3c.zag`

- Pure Zag, zero RNG. Reads the diet, gate-rejects unprovenanced rows (hard fail),
  accumulates (correct,total) per reference class in its private store:
  L1 exact (f1,f5,depth) → 312 cells; L2 (f1,f5) → 246 cells;
  L3 (depth) → 7 cells; L4 global → n=4467, rate 896575.
- Emits `src/schema_kc.zag` (kc_l1/kc_l2/kc_l3 + `kc_lookup` with the §3.1
  L1→L2→L3→L4 backoff, round-half-up integer millionths) and `kc_decisions.tsv`
  (every L1/L2/L3/L4 cell: key, correct, total, rate_mil, prov).
- Learner run: `rows=4467 L1cells=312 L2cells=246 L3cells=7 L4rate=896575`, exit 0.
- **Independent verification (PASS):** a separate Python recomputation from the diet
  reproduced every table cell (key, total, rate) and the full decision log —
  312/246/7 cells + L4, zero mismatches; emitted tables are sorted by key.

## 3. Driver — `src/nec_v3c.zag` (fork of `nec_v2d.zag`)

- New variants: **26** Design S (K-C, min_n=1, m20 latch), **27** Design S8 (K-C,
  min_n=8, m20 latch), **28** Design D per A2 (v3b `ka_schema` 35-bin at tp=0,
  tp≥1 `conf = p_raw` with NO latch).
- New-item branch: 26/27 use `kc_lookup(f1v, f5v, dep_int, min_n, ...)`; `cl_mil = rate`.
  28 uses `ka_schema(cls)`. `nopool=1` for 26/27/28 (no ledger reads/writes).
- Trace: optional argv[5] (26–28 only). tp=0: `L0 id f1 f5 depth level celln rate`
  (for 28, level=0 denotes the K-A oracle schema and celln=the 35-bin cls);
  tp≥1: `L1 id depth prev_cl_mil p_raw new_cl_mil` (28: prev=`-`).
- Output unchanged: 6 cols (id, fam, depth, release, correct, conf_thousandths).
- **Regression: variants 20/24/25 byte-identical to the nec_v2d binary on the s1 matrix.**

## 4. Smoke tests (s1 matrix `necc_input.tsv`, NO scored battery — Phase 2)

- **Variant 26:** exit 0; 6-col output (5240 rows, 0 malformed); A/B runs byte-identical
  (sha256 `534889b3…c3`); trace rows for `H5B-O-06-00`:
  `L0 H5B-O-06-00 300 142 1 1 2 1000000` — level=1, rate=1000000 as expected
  (all 1000 L0 lookups hit L1 with min_n=1).
- **Variant 27:** exit 0; backoff works: 690 L1 / 15 L2 / 295 L3 lookups with min_n=8.
- **Variant 28:** exit 0; `L0 H5B-O-06-00 300 142 1 0 10 673469` (level=0 K-A,
  cls=10 → ka_schema(10)=673469 ✓); L1 rows carry `-` for prev_cl_mil ✓.
- **Bar smoke-check** (frozen `bars_full.py` on legs converted from input+driver output):
  - Variant 26 (S): **B3 gviol=0, B13=0** (all G curves +0.000). Prereg predicted
    B3=2/2/2 (redteam artifacts, same as m20); observed 0 — a prediction MISS in the
    better direction. Control: m20 (variant 20) through the same pipeline gives
    B3 gviol=2 with the redteam rises, so the pipeline is faithful. B13=0 matches
    prediction. Kill criterion is B3>2 → not triggered. Mechanism hypothesis for the
    miss: the K-C exact-cell seeds sit at/above the personal rates on the redteam
    items, so the latch never manufactures the m20 rise pattern. Flagged for Phase 2.
  - Variant 28 (D): **B3 gviol=6, B13=3** — EXACTLY the A2 pre-registered prediction.
    G curves: D −0.085→0.000, O −0.369→0.000, admit −0.025→0.000,
    cost −0.208→0.000, logic −0.052→0.000, revoke −0.141→0.000 (all d1→d2 rises);
    B13 cells: revoke/d1, cost/d1, O/d1 (278 cells).

## 5. File SHAs (deliverables)

| file | sha256 |
|---|---|
| kb_diet_v3c.tsv | fc85209484424eb1efca20c49cb301960315cce5e2bbc4f29a02409b4d7889fe |
| mk_diet_v3c.py | 3e32468e9ef52b4d82040cd91c63315de502ce456ea51c73d66c54a0abd2e267 |
| kc_decisions.tsv | 18f6dce8261549cd109696b41bf552b12f23bf27bff30f4596c2f0db04ce83a7 |
| src/learn_schema_v3c.zag | 6c2ee5e2cf87a307b2b7b78e00791bece24b64a5aa6d95f5e261432c6ffd8754 |
| src/schema_kc.zag | b6aa3327ff72df5e75029cb3d66058dcdb53ebd5f1d58da9d941539a1dfdf8ab |
| src/nec_v3c.zag | c3fed78f7ff29f2683ed42807bb7c00acd6d8850cf26546a016192203ac7c95e |
| src/dlb_util.zag | 40ecdcec16de68d9f7d6df9c993970786e9f1cc908f00ea99c48512c599b3e93 |
| src/R33_NATIVE_SHA256_V2.zag | 9824f6db66a943917dbc7cd5e6862ab0967b7ea83161cfc357bb7d17ca683bcf |
| src/R33_NATIVE_IO_V1.zag | e6379ddb0b05d95b5ba2e8454ef8cc6bc74d054cfa44175c379296641e9f61d8 |
| src/schema_ka.zag (v3b, copied) | 70edb679f41e047e99790c6dc9ff51fc47b0726195782a977fc527e1eeeefff3 |
| src/schema_kb.zag (v3b, copied) | c3c315695193004a34d65f791cfbd3027cee856af8221975bb61f331e4b04ae7 |

## 6. Notes / blockers

- **No blockers.** The independent Python recomputation matched the Zag-emitted
  schema cell-for-cell (would-have-been blocker per brief: none).
- No binaries, `.zagd` files, or `.zag-cache` are committed (build artifacts lived
  in /tmp). A `.zag-cache/` dir exists in job3/src from the toolchain — excluded
  from the commit tree (builds were run with cwd in src/; the cache dir is NOT
  copied to the commit tree).
- Phase 2 (not done here): scored matrix s1/s10/s100 ×3, T1–T4 probes, red-team,
  channel audit, RUNLOG + VERDICT.
