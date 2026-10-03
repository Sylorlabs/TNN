# REPORT: L2-METAREUSE (learner-selected reuse operator)

Worker: L2-ADAPTIVE-REUSE subagent (depth 2/2), 2026-10-03.
Prereg: `l2_adaptive_reuse/PREREG.md`, frozen alone at commit
4f043b49f before any implementation existed. One transparent
pre-verdict amendment: PREREG_AMENDMENT1.md (Q_COMB A_SEARCH
280->260, pure hand-derivation arithmetic correction: the
b=1 partner-tail is attempted only when the AGG-head
succeeds; the frozen counting rules and code are untouched;
commit d57f14216).

## Verdict

**L2-METAREUSE-PASS.** All eight kill bars PASS, no falsifier
fired, 3/3 byte-identical.

## What was built

A standalone pure-Zag learner (`learner.zag`, 966 lines,
mr_ prefix, MR- trace tags) plus environment side
(`world.zag`: frozen 20-fact table) plus experiment side
(`driver.zag`: teaching, seven arms, in-Zag bar evaluation),
assembled as `cat learner.zag world.zag driver.zag >
mr_full.zag` (1585 lines) and compiled with the pinned znc
to `mr_bin` (build exit 0, 59 warnings: A0102
ignored-return-value class and two benign E0101/E0102
constant-fold notes in driver arithmetic, same classes as
the sibling lanes). No forbidden executables. 0 modes, 0
bridges, 0 handlers, 0 new edge types, 0 new opcodes, 0
semantic cases, 0 domain-pair templates.

The learner holds three reuse operators and selects which
one to apply per query by trial verification under a fixed
generic order [1=COMBINE, 2=SUBSTITUTE, 3=TRUNCATE]; the
first operator whose full grounding executes to the query
terminal with the required value is committed. OP_MASK
(driver-set causal-control flag, one value per ARM, never
per query, never written by the learner) gates which
operators may be tried.

Scenario: X = arithmetic aggregation MAP mA (entry + 3
fold pairs) learned in domain A; Y = planning ROUTE MAP
mB0 learned in domain B; distractor mD (ROUTE, taught
first). Three reuse queries, each solvable by exactly one
operator:
- Q_COMB (90,86,42,AGG,B): op 1 COMBINE. Neither mA
  (no rel-18 fact from 90) nor mB0 (reaches 92, not 86)
  grounds it. The (partner-source, binding) enumeration
  tries (mD,b=1) FAIL, (mD,b=2) FAIL, (mB0,b=1) FAIL
  (AGG-head fails shape from 90, so no tail is attempted),
  then (mB0,b=2) VERIFY-OK: partner-head rel-[7,7] walk
  reaches 92, AGG-tail (entry 17, folds 15/16 discovered
  at runtime) reaches 86 with VAL 42. Z_comb built as
  head+tail, verified by execution, promoted with dual
  type-16 provenance (3->1, 3->2), delivered via=3.
- Q_SUB (200,43,11,AGG,A): op 1 fails all four
  (partner,binding) attempts; op 2 SUBSTITUTE collects
  entry candidates (live facts with sub==200 and rel !=
  18): fid 18 (200,19,40). Foldwalk from 40 with k=3
  discovers (5,6) and reaches 43, VAL(43)=11. Z_sub =
  rels [19,5,6,5,6,5,6], facts [18,0,1,2,3,4,5], verified
  by execution, promoted with type-16 provenance
  (4->1), delivered via=4.
- Q_TRUNC (100,42,32,AGG,A): ops 1-2 fail (no entry
  candidate from 100 with rel != 18); op 3 TRUNCATE
  tries nf=2 first: entry (100,18,40), 2-fold walk
  reaches 42, VAL(42)=32 via the world VAL fact.
  Z_trunc = rels [18,5,6,5,6], facts [7,0,1,2,3],
  verified by execution, promoted with type-16
  provenance (5->1), delivered via=5.
Re-asks Q_COMB-B/Q_SUB-B/Q_TRUNC-B go through the
pipeline via Z ids 3/4/5 with no meta phase
(MR_ENTERED=0): the adapted structures persist and are
reused.

## Kill-bar results (in-Zag BARS + shell checks on mr_run1.txt)

- K1 (X and Y exist before reuse, learned independently):
  in-Zag qa_via=1, qb_via=2, disj=1 (mA rels in
  {18,5,6}, mB0 rels all 7). Shell: `Q QA` (line 2) <
  `Q QB` (line 4) < `Q QCOMB` (line 6). PASS.
- K2 (no single structure solves the reuse queries;
  reuse REQUIRED): in-Zag qc_phit=0, qs_phit=0,
  qt_phit=0, NOREUSE arm all three vals=-2, t16=0.
  Shell: verbatim `MR-PIPELINE-FAIL` (18 occurrences:
  3 reuse queries x 6 arms). PASS.
- K3 (learner decides WHICH operator per query, not the
  researcher): in-Zag qc_op=1, qs_op=2, qt_op=3,
  tries 1/2/3, decided=1 each, qc_asrc=1, qc_rsrc=2,
  qc_bind=2, qc_btr=4, qc_bdec=1. Shell verbatim, in
  order: `MR-OP-TRY 1` ... `MR-BIND b=2 OK` ...
  `MR-OP-OK 1` (QCOMB); `MR-OP-TRY 1`,
  4x `MR-BIND b=n FAIL`, `MR-OP-FAIL 1`,
  `MR-OP-TRY 2`, `MR-SUB-CAND r=19 u=40 SHAPE-OK
  term=43 VERIFY-OK`, `MR-OP-OK 2` (QSUB);
  `MR-OP-TRY 1`, `MR-OP-FAIL 1`, `MR-OP-TRY 2`,
  `MR-OP-FAIL 2`, `MR-OP-TRY 3`,
  `MR-TRUNC-TRY nf=2`, `MR-OP-OK 3` (QTRUNC).
  `grep -c` of MR-OP-TRY/MR-OP-OK/MR-SUB-CAND/
  MR-TRUNC-TRY/MR-BIND in driver.zag = 0: the driver
  never names an operator or a trace tag; ex_query
  takes only the arm-level OP_MASK. The same fixed
  order and the same mask (7) yield different
  operators on different queries, so position-in-order
  cannot explain the choice; Q_SUB skipping op 1 and
  Q_TRUNC skipping ops 1-2 proves verification
  decides. PASS.
- K4 (adapted structures succeed where sources alone
  fail): in-Zag qc_via=3, qc_val=42, qs_via=4,
  qs_val=11, qt_via=5, qt_val=32, zc=zs=zt=1 (exact
  header/rels/facts/descriptor match). Shell
  verbatim: `MR-ZBUILD
  rels=7,7,17,15,16,15,16,15,16
  facts=8,9,10,11,12,13,14,15,16`,
  `MR-ZBUILD rels=19,5,6,5,6,5,6
  facts=18,0,1,2,3,4,5`,
  `MR-ZBUILD rels=18,5,6,5,6 facts=7,0,1,2,3`,
  `ANS term=86 val=42 via=3`,
  `ANS term=43 val=11 via=4`,
  `ANS term=42 val=32 via=5`. PASS.
- K5 (each operator necessary for its query):
  ABLATE-COMBINE (mask 6): QCOMB ans=-2 (op 1
  skipped; substitute candidate (90,7,91) fails shape;
  truncate nf=2 fails shape, nf=1 reaches 80 not 86),
  QSUB val=11, QTRUNC val=32, t16=2.
  ABLATE-SUBST (mask 5): QSUB ans=-2 (truncate nf=2
  reaches 42 not 43, nf=1 reaches 41), QCOMB val=42,
  QTRUNC val=32, t16=3. ABLATE-TRUNC (mask 3): QTRUNC
  ans=-2, QCOMB val=42, QSUB val=11, t16=3. In-Zag
  k5=1. PASS.
- K6 (determinism): 3/3 runs byte-identical, sha256
  5fb7423cce26c3a34ceb52f201591e2349ea7c62ae56f0865dc8c0e3f0bbe6d8
  x3. PASS.
- K7 (no world/answer literals in the learner): 12/12
  frozen grep patterns return 0 hits on learner.zag
  (fixed-string). PASS.
- K8 (provenance): in-Zag t16F=4, e_has(3,1,16)=1,
  e_has(3,2,16)=1, e_has(4,1,16)=1, e_has(5,1,16)=1.
  Each adapted Z carries derived-from provenance to
  its source(s). PASS.

Falsifiers: 0 fired. F-COUNT silent (FULL A_SEARCH
260/214/203, A_EXEC 2/2/2, exactly the amended hand
derivation: QCOMB 2+3+50+20+50+135=260; QSUB
2+4+160+20+21+7=214; QTRUNC 2+5+138+20+38=203).
Ablate-arm informational counts match independent
hand derivations (143/217/165).

## Numbers

- FULL: QCOMB op=1 tries=1 as=260 ae=2 via=3 val=42;
  QSUB op=2 tries=2 as=214 ae=2 via=4 val=11; QTRUNC
  op=3 tries=3 as=203 ae=2 via=5 val=32; re-asks via
  3/4/5, MR_ENTERED=0; t16=4 {3->1,3->2,4->1,5->1};
  LINK14 to 3,4,5; NM=6; distractor mD live=1; no
  edge type outside {14,16} in any arm.
- ABLATE-COMBINE: QCOMB -2 (as=143), QSUB 11 (op 2),
  QTRUNC 32 (op 3), t16=2.
- ABLATE-SUBST: QCOMB 42 (op 1), QSUB -2 (as=217),
  QTRUNC 32 (op 3), t16=3.
- ABLATE-TRUNC: QCOMB 42 (op 1), QSUB 11 (op 2),
  QTRUNC -2 (as=165), t16=3.
- NOREUSE: all -2, t16=0, NM=3. FRESH: all -2,
  t16=0, NM=0.

## Disclosures and non-claims

- The three operators, descriptor extraction,
  entry/fold search with runtime relation discovery,
  strict partner-segment walk, first-verifying-
  operator enumeration, and cost counters are
  researcher-supplied generic machinery, frozen in
  the prereg. None names a relation, MAP, domain,
  query, operator-to-query assignment, source pair,
  or binding. The fixed operator order [COMBINE,
  SUBSTITUTE, TRUNCATE] is generic policy; which
  operator verifies is decided at runtime by
  execution, as the ablation arms demonstrate (same
  order and mask structure, different outcomes per
  query).
- The SUBSTITUTE operator here is entry-relation
  substitution (one facet of the matrix lane's
  interface adaptation); the TRUNCATE operator tries
  strict prefixes at the query start. Both are
  narrower than the full matrix operators; the L2
  claim is the OPERATOR SELECTION, not the
  operators' generality.
- This is L2 (learner-driven structural adaptation
  with operator choice), not L3: the operator menu
  is researcher-supplied. Meta-selection does not
  invent operators.
- OP_MASK is a driver-set causal-control flag (the
  COMBINE_ON precedent), never written by the
  learner; it enables the lesion comparison and is
  set per ARM, never per query.
- One world family. No generality claim beyond the
  seven arms; the world is builder-designed, not
  adversary-designed. Sealed-adversary generality is
  open future work.
- 0 modes, 0 bridges, 0 handlers, 0 new edge types,
  0 new opcodes, 0 new semantic cases. Pure Zag,
  safebin toolchain, zero forbidden executables.
- No em/en dashes in loop documentation. Paper
  untouched. Commits local with explicit pathspecs.
  Nothing pushed.
- Unfrozen only: no frozen source touched. The
  frozen TNN core is not used here; this is a
  standalone learner-mechanism experiment.
- This wave does not integrate anything into the
  protected core or any continuing learner.

## Files

- `learner.zag`, `world.zag`, `driver.zag`,
  `mr_full.zag` (concatenated build input),
  `mr_bin` (pinned-znc binary), `mr_compile.txt`,
  `mr_run1.txt`, `mr_run2.txt`, `mr_run3.txt`
- `NAMECHECK.md` (Step 0 toolchain guard),
  `PREREG.md` (frozen, committed alone at 4f043b49f
  before implementation), `PREREG_AMENDMENT1.md`
  (pre-verdict arithmetic correction, commit
  d57f14216)
