# RESULTS_MORG — Memory Self-Organization Experiment (crew 2)

Date: 2026-09-24. Frozen prereg: `docs/lab/memory_org/PREREG_MORG_FROZEN.md`
(frozen commit `0994ad5174a7977b7c2bc270822120750fa0f290`, repo `sylorlabs/TNN`,
branch `tnn-native-lab`).
Toolchain (pinned): `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`.
Arm contract §2, battery order B1–B8 — no deviations.
Mechanisms: pure Zag, zero RNG, no hardcoded query answers; retrieval genuinely
navigates (hierarchical type→domain→code→keywords) and scores (deterministic
exact-token overlap).

## Determinism

Three full battery reruns (each: rebuild + B1–B8 on all 3 arms, real fixture:
240 base items, 40 holdout astronomy items, 48 queries [16 calib / 32 test],
12 holdout queries). SHA-256 over every required output file
(`retrieval.txt`, `retrieval_holdout.txt`, `retrieval_holdout_old.txt`,
`scheme.txt`, `scheme_t0.txt`, `scheme_t1.txt`, `verify_report.txt`,
`ops.txt`, `summary.txt`) per arm per run:

**3x RERUN: ALL BYTE-IDENTICAL** (27 files × 3 runs, zero mismatches).

Result layout matches the official scorer contract:
`results/SELF/run<R>/`, `results/IMPOSED/run<R>/`, `results/FLAT/run<R>/`
(uppercase, as `scorer.py` requires).

## B1 — retrieval macro F1 (32 test queries, top-20)

| arm     | PURE   | SUBJ   | AMBIG  | overall |
|---------|--------|--------|--------|---------|
| SELF    | 0.6104 | 1.0000 | 0.5125 | 0.6833  |
| IMPOSED | 0.8333 | 0.6667 | 0.1250 | 0.6146  |
| FLAT    | 0.4750 | 0.6667 | 0.8313 | 0.6120  |

SELF: 32/32 queries retrieved, all ids from ingested corpus. Per-query lines in
`results/SELF/run1/retrieval.txt` (`qid|id1,id2,...`).

## B2 — interference (8 PURE test queries, top-10)

| arm     | frac wrong type | frac wrong domain |
|---------|-----------------|-------------------|
| SELF    | 0.0000          | 0.4250            |
| IMPOSED | 0.0000          | 0.0000            |
| FLAT    | 0.1375          | 0.4875            |

SELF's wrong-domain leakage (0.4250) comes from its S6 (flat) domains
(physics/history/music): global keyword scoring lets cross-domain items into
the top-10. IMPOSED's hierarchical navigation has zero leakage. No arm
retrieves a wrong-typed item for SELF/IMPOSED (0.0000).

## B3 — revision locality (all arms: PASS)

10 items revised (CD11 CD13 CD15 CD01 CD03 CD05 CD21 CD23 CD25 CD31); every
other item byte-identical before/after (`verify_report.txt`: 10/10 per-item
PASS lines + `B3: PASS - revised 10 items, all other items byte-identical`).

## B4 — separability / portable chunks (all arms: PASS)

- `deletecat CODE`: store hash after deleting all CODE items ==
  hash of fresh ingest without CODE
  (`49f5793429f1758200b646768100e6a1c7cadd99b103094eb0d6199cbeb7a19a` both).
- `exportcat FACT` → import into fresh store: hash ==
  hash of FACT-only fresh ingest
  (`1c37785b6e53984c6cd01e0119e3ee122db219d7dc32f7e3106cf9890239def9` both).
- `verify_report.txt`: `B4: PASS - deletecat CODE hash matches fresh ingest;
  FACT export/import round-trips` on all three arms.

## B5 — reorganization cost

- SELF (choose+refile on 240 items, counters reset at choose start):
  `reads=480 writes=240 moves=240`, `B5: PASS`.
- IMPOSED / FLAT: fixed schemes, no reorg (`reads=0 writes=240 moves=0`
  ingest-only; `B5: PASS - no reorg (fixed scheme)`).

## B6 — drift (holdout ingest → re-choose)

| arm     | scheme t0 | scheme t1 | changed | F1 old | F1 new | delta   | outcome |
|---------|-----------|-----------|---------|--------|--------|---------|---------|
| SELF    | 6 domains | 7 domains (+astronomy:S6) | y | 0.0000 | 0.7583 | +0.7583 | helped |
| IMPOSED | fixed     | fixed     | n/a     | 0.0000 | 0.5278 | +0.5278 | helped |
| FLAT    | fixed     | fixed     | n/a     | 0.0000 | 0.5083 | +0.5083 | helped |

SELF t0: `{coding:S1, cooking:S3, gardening:S3, history:S6, music:S6,
physics:S6}`.
SELF t1: `{astronomy:S6, coding:S1, cooking:S3, gardening:S3, history:S6,
music:S6, physics:S6}` — existing 6 domain choices unchanged; only the new
astronomy domain added (S6, disclosed degenerate rationale: n=0 calib queries,
all schemes tie at 0.0, frozen tie-break picks fewest levels).
Old-scheme holdout retrieval (`retrieval_holdout_old.txt`, t0 scheme on
base+holdout store) F1 = 0.0000: without an astronomy domain the t0 scheme
cannot reach holdout items at all — the drift was load-bearing, and the
re-choose fixed it.

## B7 — holdout F1 (12 astronomy queries, top-20, under t1 scheme)

| arm     | PURE   | SUBJ   | AMBIG  | overall |
|---------|--------|--------|--------|---------|
| SELF    | 0.6917 | 0.9167 | 0.6667 | 0.7583  |
| IMPOSED | 0.9167 | 0.3333 | 0.3333 | 0.5278  |
| FLAT    | 0.5250 | 0.3333 | 0.6667 | 0.5083  |

## B8 — SELF scheme report (per-domain choose, 16 calib queries)

Calibration set = contract split (Q01..Q08, Q25..Q28, Q37..Q40), verified
against `queries.txt`. Per-domain means use the domain's PURE calib queries
only (SUBJ/AMBIG calib queries are domain-less by design — cross-domain
goldens — and cannot be assigned to one domain; the n's below disclose this).

| domain    | chosen | S1  | S2  | S3  | S4  | S5  | S6  | rationale (abridged) |
|-----------|--------|-----|-----|-----|-----|-----|-----|----------------------|
| coding    | S1     | 1.0 | 1.0 | 0.8333 | 1.0 | 1.0 | 0.8333 | S1 wins argmax (n=2); ties S1,S2,S4,S5 at 1.0; fewest-levels→lowest-index |
| cooking   | S3     | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.6667 | S3 wins argmax (n=1); ties S1–S5 at 1.0; fewest levels |
| gardening | S3     | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.6667 | S3 wins argmax (n=1); ties S1–S5 at 1.0; fewest levels |
| history   | S6     | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | S6 wins argmax (n=1); all tie at 1.0; fewest levels |
| music     | S6     | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | S6 wins argmax (n=1); all tie at 1.0; fewest levels |
| physics   | S6     | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | S6 wins argmax (n=2); all tie at 1.0; fewest levels |

Global (all 16 calib, informational): S1 = 0.9438 (S2/S4/S5 tie), S3 = 0.9229,
S6 = 0.8813 → S1 wins. Note the tension: globally S1 beats S6, but per-domain
calibration on PURE-only queries ties them at 1.0, so the frozen
fewest-levels tie-break selects S6 for 3/6 domains. The tie-break's simplicity
bias is doing real work here — and on the PURE test set it costs SELF
(PURE 0.6104 vs IMPOSED 0.8333).

Full per-domain blocks with 12-decimal scores and one-line rationales:
`results/SELF/run1/scheme.txt` (63 lines; also `scheme_t0.txt`,
`scheme_t1.txt` with the astronomy block).

## Kill bars (official `scorer.py`)

- **KB-1 non-inferiority: PASS** — SELF 0.6833 >= IMPOSED 0.6146 − 0.02
  (delta +0.0688).
- **KB-2 separability: PASS** — B4 PASS on all three arms.
- **KB-3 revision locality: PASS** — B3 zero collateral on all three arms.
- **KB-4 consciousness: PASS** — scorer re-derived all 6 per-domain choices
  from recorded scores under the frozen tie-break (fewer levels, then lowest
  scheme index; levels S1=3 S2=3 S3=2 S4=3 S5=3 S6=1): 6/6 MATCH.
- **KB-5 superiority probe (REPORTED, not a kill):**
  SELF−IMPOSED: PURE −0.2229 (SELF loses ≥0.03), SUBJ +0.3333 (SELF wins),
  AMBIG +0.3875 (SELF wins), overall +0.0688.

Cross-arm deltas: SELF−IMPOSED +0.0688, SELF−FLAT +0.0714,
IMPOSED−FLAT +0.0026.

## Sol's failure modes (checked against B2/B6/B7)

1. **Self-reinforcing misorganization** — NOT OBSERVED as a loop. B6 drift
   helped (+0.7583); re-choose kept all 6 existing domain choices and only
   added astronomy. One-shot simplicity bias (above) is real but did not
   reinforce across the drift event.
2. **Popularity bias** — OBSERVED in SELF/FLAT, absent in IMPOSED. B2
   wrong-domain leakage: SELF 0.4250, FLAT 0.4875, IMPOSED 0.0000. Flat
   global scoring lets high-keyword-overlap cross-domain items displace
   in-domain items in the top-10; hierarchical navigation suppresses it.
3. **Misleading cross-domain links** — OBSERVED as a precision/recall
   trade-off across arms (B1 AMBIG vs PURE gap): IMPOSED AMBIG 0.1250 vs
   PURE 0.8333 (hierarchy misleadingly constrains ambiguous queries);
   FLAT AMBIG 0.8313 vs PURE 0.4750 (flat captures cross-domain links,
   at the cost of PURE leakage); SELF sits between (AMBIG 0.5125,
   PURE 0.6104) because it mixes hierarchical (S1/S3) and flat (S6)
   domains per its own calibration.

## Implementation notes

- Sources: `arms/lib.zag` (shared arenas, accessors, SHA-256, store ops),
  `arms/arm_self.zag`, `arms/arm_imposed.zag`, `arms/arm_flat.zag`;
  `arms/build.sh`, `arms/run_battery.sh`, `arms/summarize.py`,
  `arms/mini/` (6-item smoke fixture).
- ID-sorted canonical record storage; explicit `[]u8` arenas + little-endian
  accessors (no typed-array aliasing); hierarchical navigation for organized
  schemes; deterministic exact-token scoring for FLAT; integer mean-F1
  accumulation (1e9 scale, 12-decimal printing resolves the integer quantum
  for nq ≤ 16, so printed order/ties match the integer argmax exactly);
  frozen tie-break; SHA-256 verification via native substrate.
- **Defect found and fixed during verification (2026-09-24):** the calib
  mean-F1 accumulator divided by the query count twice
  (`den = nsq*(r+g)` instead of `den = (r+g)`), so recorded scores printed
  as mean_F1/nq. Integer argmax — and therefore all choices, all retrieval,
  and KB-4 — was unaffected (nq is a common factor per scope), but the
  recorded scores misrepresented the true means. Fixed, rebuilt, full
  3-run battery re-executed: still ALL BYTE-IDENTICAL, all KBs still PASS,
  scores now true means (e.g. per-domain calib F1s are 1.0 across tied
  schemes; global S1 = 0.9438 > S6 = 0.8813).
- Zero RNG anywhere in arm decision paths (no random tie-breaks, no
  stochastic policies); determinism is structural, verified by the 3x
  byte-identical reruns above.

## Files

- Arm sources + scripts: `arms/` (this directory)
- Results: `results/{SELF,IMPOSED,FLAT}/run{1,2,3}/`
- Official scorer output: `SCORES.md`
- Battery log: `~/workspace/morg/battery2.log`
