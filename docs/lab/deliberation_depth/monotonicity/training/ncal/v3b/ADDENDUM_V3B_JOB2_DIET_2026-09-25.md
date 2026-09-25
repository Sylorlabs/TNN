# ADDENDUM (dated pre-run) — NCAL v3b JOB 2: K-A / K-B frozen specs, K-B diet, learning rule

- **Date:** 2026-09-25 (PDT). **Status:** FROZEN before any learning or battery run.
- **Parent:** `PREREG_NCAL_V3B_FROZEN.md` (frozen `90b24d0345b4c3925b6f8e53de520b805a98ac7e`, SHA-256
  `4c8780d12287c84c83c7576e45ee7f1e36dfa51799081787dfd9d36597196f21` — verified by crew before running).
- **Purpose:** freeze the two knowledge-design specs (§3.2), the K-B training diet, the K-B learning rule,
  and the channel-audit pre-declaration, BEFORE the learner runs and before any battery run.

## §1 K-A — oracle schema (variant 24, DIAGNOSTIC, never adopted)

Schema = true empirical per-class-bin rates, in millionths, frozen constants in committed source
(`src/schema_ka.zag`, function `ka_schema(cls)`). Consulted ONLY at first observation (tp=0),
replacing the d1prior constant at exactly one step: in `nec_run`'s new-item branch,
`cl_mil = ka_schema(cls)` instead of `cl_mil = d1prior`. Personal ledger + ceiling at tp≥1 unchanged
(adopted mechanism untouched). Class ledger never read or written (`nopool=1`, same as m20) —
structurally no pooled GT.

Derivation (disclosed oracle; values frozen, never computed from the test battery at runtime):

| cls | rate (millionths) | derivation |
|-----|-------------------|------------|
| 0 | 0 | matrix `necc_input.tsv` released 0/31 |
| 1 | 0 | matrix released 0/102 |
| 2 | 0 | matrix released 0/24 |
| 3 | 1000000 | `trap_t3_truth.tsv` C0 1.00 |
| 4 | 750000 | `trap_t3_truth.tsv` C1 0.75 |
| 5 | 515152 | matrix released 17/33 |
| 6 | 0 | matrix released 0/31 |
| 7 | 0 | matrix released 0/74 |
| 8 | 1000000 | matrix released 1/1 |
| 9 | 500000 | `trap_t3_truth.tsv` C2 0.50 |
| 10 | 673469 | matrix released 33/49 |
| 11 | 1000000 | matrix released 2/2 |
| 12 | 62500 | matrix released 1/16 |
| 13 | 250000 | `trap_t3_truth.tsv` C3 0.25 |
| 14 | 0 | matrix all-cell 0/10 (zero released cells; released rate undefined) |
| 15 | 775578 | matrix released 235/303 |
| 16 | 652174 | matrix released 75/115 |
| 17 | 659091 | matrix released 58/88 |
| 18 | 666667 | matrix released 20/30 |
| 19 | 1000000 | matrix released 1340/1340 |
| 20 | 1000000 | matrix released 55/55 |
| 21 | 1000000 | matrix released 8/8 |
| 22 | 1000000 | matrix released 4/4 |
| 23 | 0 | `trap_t3_truth.tsv` C4 0.00 |
| 24 | 1000000 | matrix released 20/20 |
| 25 | 1000000 | matrix released 92/92 |
| 26 | 1000000 | matrix released 10/10 |
| 27 | 1000000 | matrix released 4/4 |
| 28 | 950000 | NO EVIDENCE anywhere (no matrix, no trap cell): disclosed d1prior retained |
| 29 | 1000000 | matrix released 20/20 |
| 30 | 1000000 | matrix released 235/235 |
| 31 | 997290 | matrix released 368/369 |
| 32 | 996226 | matrix released 264/265 |
| 33 | 1000000 | matrix released 158/158 |
| 34 | 996964 | matrix released 985/988 |

Released-cell rates are used because the schema is consulted only for released cells at tp=0;
P(correct | released, bin) is the calibration target. The scale batteries (s10/s100) are deterministic
replications of `necc_input.tsv`, so these are the scale batteries' generative truth as well.

## §2 K-B — TNN-learned schema (variant 25, adoption-eligible)

### §2.1 Training diet (frozen, disclosed): `kb_diet_v1.tsv`

- Columns: `id \t f1 \t f5 \t correct \t prov` (5 cols).
- 34 bins (every bin EXCEPT 28, which has no evidence anywhere), 1000 items per bin, 34,000 rows.
- Item IDs: `KBDIET-{cls:02d}-{i:04d}` for i in 0..999 — a prefix disjoint by construction from every
  test ID; disjointness verified programmatically against `necc_input.tsv`, `necc_input_s10.tsv`,
  `necc_input_s100.tsv`, `trap_t1.tsv`, `trap_t3.tsv` (any overlap voids the run).
- Features: f1 = mb·150+75 where mb = cls//5; f5 = cb·250+125 where cb = cls%5. (Binning rule
  mb=min(f1//150,6), cb=min(f5//250,4) round-trips by construction; verified by the generator.)
- Correctness: for bin with K-A oracle rate R (millionths), K = round(R·1000/10⁶) correct items;
  item i correct ⟺ (i·K) mod 1000 < K. Deterministic (zero RNG), exactly K correct per bin,
  evenly interleaved. This teaches P(correct | observed item, bin) at the disclosed true rates.
- Provenance per row: `kb-diet-v1:bin{cls:02d}:i{i:04d}:rate{R}`.
- Bin 28 is deliberately ABSENT: no evidence exists for it anywhere; the learner must abstain there
  (see §2.2), exercising the deliberate-abstain path.

### §2.2 Learning rule (frozen; implemented in `src/learn_schema.zag`, pure Zag, zero RNG)

The learner is TNN's deliberate learning machinery in miniature, following the synonym-learner pattern
(evidence → relations with provenance → frozen store):

1. **Evidence intake (gated):** read each diet row; REJECT (hard fail, nonzero exit) any row whose
   provenance does not begin with `kb-diet-v1:` or whose columns are malformed. The learner never
   installs from unprovenanced evidence.
2. **Accumulation:** per-bin (correct, total) counts in the learner's own store. This is the
   learner's private evidence ledger — NOT the NEC driver's class ledger, and it is never consulted
   or updated during any battery run.
3. **Deliberate install/abstain decision per bin (the deliberation step):**
   - if total ≥ 20 (disclosed sufficiency threshold): **INSTALL** rate = (correct·10⁶ + total/2)/total
     (round-half-up, integer arithmetic), logged as `INSTALL` with bin, rate, n, correct, prov prefix.
   - else: **ABSTAIN** — no belief installed; schema entry = disclosed d1prior 950000 fallback,
     logged as `ABSTAIN` with the reason `insufficient-evidence`.
   The decision log (`kb_decisions.tsv`) is the deliberation record: every installed belief carries
   its provenance; every abstention carries its reason.
4. **Frozen store:** emits `src/schema_kb.zag` (`fn kb_schema(cls)`) — the table is frozen data from
   this point on; the NEC driver imports it and never recomputes it. The learner's evidence ledger
   is discarded after emission (frozen store only).

### §2.3 Auditability (frozen)

- The diet SHA-256 is recorded in RUNLOG_V3B.md; the decision log + diet + learner source fully
  determine `schema_kb.zag` — verified programmatically (independent Python recomputation of the
  table from diet+decisions, byte-compared against the committed table).
- Expected learned values: bin rate = K·1000 millionths where K = round(R·1000/10⁶), i.e. within
  500 of the K-A oracle R; bin 28 = 950000 via ABSTAIN.

## §3 Channel audit pre-declaration (frozen; verified post-run against source)

- Schema consulted ONLY at tp=0 (first observation of an item), indexed by class bin computed from
  the already-read f1/f5 inputs. Never consulted at tp≥1; never updated within a battery.
- K-A values derivable from `trap_t3_truth.tsv` + `necc_input.tsv` released rates only (§1 table).
- K-B values derivable from `kb_diet_v1.tsv` + `learn_schema.zag` only (§2). No test-battery outcome
  flows into either schema: the schemas are frozen before the first battery run.
- No within-battery cross-item GT pooling: variants 24/25 run with `nopool=1`; the class ledger is
  neither read nor written (source-verified, same guards as m20). The K-B learner's evidence ledger
  exists only during the pre-run learning step and is not present at battery runtime.
- Personal ledger (per-item cp/tp from the item's own past correctness) + ceiling min-latch at
  tp≥1: unchanged adopted mechanism. T1's trap bin is cls 28 → 950000 under BOTH schemas
  (K-A default, K-B abstain fallback) — T1 behavior is predicted identical to m20; any deviation
  would be a mechanism finding, not a knowledge effect.

## §4 Run plan (frozen)

1. Pipeline check §4: variant 20 reproduces adopted v2d legs byte-identically (s1/s10/s100). — DONE pre-addendum, PASS.
2. Commit this addendum + `kb_diet_v1.tsv` + `gen_kb_diet.py` + `src/learn_schema.zag` (pre-run freeze).
3. Run learner → `src/schema_kb.zag` + `kb_decisions.tsv`; verify vs §2.3; generate `src/schema_ka.zag`
   from §1 (byte-verified against this table); commit driver extension + schema tables (pre-battery freeze).
4. Battery: variants 24/25 × (s1/s10/s100 matrix + trap_t1 + trap_t3), A/B/C byte-identical, SHA logs.
5. Score: full bars B1–B9/B13 at s1/s10/s100 (bars_full.py on converted legs); T1/T3 (t13, extended with
   m24/m25 STATED rules); T2 (t2, extended); T4-analog (schema provenance audit + T3 bias check);
   channel audit (post-run source verification); white-box trace of the exact step where knowledge bears.
6. Verdict ladder per §3.4. Adoption is Micah's call.
