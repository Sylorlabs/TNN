# REPORT: L2-METAREUSE-EXTEND (INVERT / ABSTRACT / CONCRETIZE)

Worker: L2-METAREUSE-EXTEND subagent (depth 2/2), 2026-10-03.
Prereg: `l2_metareuse_extend/PREREG.md`, frozen alone at
commit 89b3bbaf9 before any implementation existed. One
transparent pre-verdict amendment: PREREG_AMENDMENT1.md
(QT-AS 368->324: hallucinated (100,2,50) fact removed
from the derivation; QV-AS 1142->1193: foldwalk
(s1,s2) discovery-order correction in QINV op-1 b=2;
plus mechanical driver stat-offset fixes; no counting-
rule or learner-code change).

## Verdict

**L2-METAREUSE-EXTEND-PASS.** All eight kill bars PASS, no
falsifier fired, 3/3 byte-identical.

## What was built

The parent L2-METAREUSE harness extended with three new
reuse operators, assembled as `cat learner.zag world.zag
driver.zag > mx_full.zag` (2455 lines) and compiled with
the pinned znc to `mx_bin` (build exit 0; only A0102
ignored-return-value warnings, same class as the parent
lane). No forbidden executables. 0 modes, 0 bridges,
0 handlers, 0 new edge types, 0 new opcodes, 0 semantic
cases, 0 domain-pair templates.

The learner now holds SIX reuse operators and selects
which one to apply per query by trial verification under
the fixed generic order [1=COMBINE, 2=SUBSTITUTE,
3=TRUNCATE, 4=INVERT, 5=ABSTRACT, 6=CONCRETIZE]; the
first operator whose full grounding executes to the query
terminal with the required value is committed. OP_MASK
gates operators via mask bits 1/2/4/8/16/32
((mask/n)%2, no bitwise ops).

New machinery (all generic, relation-agnostic):
- mr_invert: reverses the source MAP's stored relation
  sequence and walks it strictly forward (one
  ex_find_subrel per hop), requiring terminal and
  value match; builds Z with the reversed rels.
- mr_abstract: extracts the pattern (entry rel, fold
  count, value rel) from the source descriptor; entry
  candidates must MATCH the interface (rel==d_entry);
  fold relations discovered at runtime.
- mr_concretize: finds the pattern MAP by generic
  descriptor search (first live MAP with cap==qcap and
  d_entry==0, the hole entry); tries every entry
  binding the query start offers; fold relations
  discovered at runtime must be NOVEL against the
  source structure's folds (else MR-CONC-OLD skip).
- State layout shifted mechanically for 44 facts
  (16..367), 16 MAPs (368..1007), 64 edges
  (1008..1263), 16 answer nodes (1264..1327); every
  stat offset +80. The shift was verified by grep
  (zero old literals remain) and by the F-COUNT bars.

World: 44 facts (parent's 20 plus INVERT region
20-27, ABSTRACT region 28-35, CONCRETIZE region 36-42,
pattern entry 43). MAPs: mD=0, mA=1, mB0=2, mP=3 (the
taught 2-fold pattern with hole entry 0).

Six reuse queries, each solved by exactly one operator:
- Q_COMB (90,86,42,AGG,B): op 1, Z id 4 (as parent).
- Q_SUB (200,43,11,AGG,A): op 2, Z id 5 (as parent).
- Q_TRUNC (100,42,32,AGG,A): op 3, Z id 6 (as parent).
- Q_INV (120,127,60,AGG,A): op 4 INVERT. Ops 1-3 fail
  (COMBINE b=1 SHAPE-FAIL / b=2 tail SHAPE-FAIL;
  SUBSTITUTE candidate SHAPE-FAIL on the 3rd fold
  pair; TRUNCATE prefixes miss terminal 127). INVERT
  reverses mA's [18,5,6,5,6,5,6] to
  [6,5,6,5,6,5,18], strict-walks 120->127, VAL=60.
  Z_inv rels [6,5,6,5,6,5,18], facts
  [20,21,22,23,24,25,26], descriptor (6,5,6,3,2).
- Q_ABS (150,166,77,AGG,A): op 5 ABSTRACT. Ops 1-4
  fail (SUBSTITUTE: no rel!=18 entry; TRUNCATE:
  prefixes reach 164/162 not 166; INVERT: no rel-6
  hop from 150). ABSTRACT extracts pattern
  (entry=18, nf=3, valrel=2), matches entry
  (150,18,160), discovers folds (8,9) at runtime,
  reaches 166, VAL=77. Z_abs rels [18,8,9,8,9,8,9],
  facts [28,29,30,31,32,33,34], descriptor
  (18,8,9,3,2).
- Q_CONC (210,234,91,AGG,A): op 6 CONCRETIZE. Ops 1-5
  fail (SUBSTITUTE: 3-fold walk SHAPE-FAILs;
  TRUNCATE: first entry is a dead end; INVERT: no
  rel-6 hop; ABSTRACT: the rel==18 entry is a dead
  end). CONCRETIZE finds pattern mP (id 3),
  tries (210,18,220) SHAPE-FAIL then (210,38,230):
  discovers folds (11,12) != (5,6), reaches 234,
  VAL=91. Z_conc rels [38,11,12,11,12], facts
  [37,38,39,40,41], descriptor (38,11,12,2,2).
Re-asks go through the pipeline via Z ids 4-9 with no
meta phase (MR_ENTERED=0): all six adapted structures
persist and are reused.

## Kill-bar results (in-Zag BARS + shell checks on mx_run1.txt)

- K1: qa_via=1, qb_via=2, disj=1. `Q QA` < `Q QB` <
  `Q QCOMB`. PASS.
- K2: all six phit=0 in FULL; NOREUSE arm all six
  vals=-2, t16=0. 54 `MR-PIPELINE-FAIL` lines.
  PASS.
- K3: qc_op=1, qs_op=2, qt_op=3, qv_op=4, qe_op=5,
  qn_op=6; tries 1/2/3/4/5/6; decided=1 each;
  qc_asrc=1. Shell verbatim per query, e.g. QINV:
  `MR-OP-TRY 1` `MR-OP-FAIL 1` ... `MR-OP-TRY 4`
  `MR-INV-OK` `MR-OP-OK 4`. `grep -c` of
  MR-OP-TRY/MR-OP-OK/MR-SUB-CAND/MR-TRUNC-TRY/
  MR-ABS-CAND/MR-CONC-CAND/MR-INV-REV/MR-BIND in
  driver.zag = 0: the driver never names an operator.
  Same fixed order and same mask (63) yield six
  different operators, so verification decides. PASS.
- K4: vias 4/5/6/7/8/9, vals 42/11/32/60/77/91,
  zc=zs=zt=zi=za=zn=1 (exact match). Six `MR-ZBUILD`
  lines and six `ANS` lines verbatim per section 1.
  PASS.
- K5: six ablation arms. ABLATE-COMBINE (62): QCOMB
  -2, others 11/32/60/77/91, t16=5. ABLATE-SUBST
  (61): QSUB -2, others 42/32/60/77/91, t16=6.
  ABLATE-TRUNC (59): QTRUNC -2, others 42/11/60/77/
  91, t16=6. ABLATE-INV (55): QINV -2, others
  42/11/32/77/91, t16=6. ABLATE-ABS (47): QABS -2,
  others 42/11/32/60/91, t16=6. ABLATE-CONC (31):
  QCONC -2, others 42/11/32/60/77, t16=6. PASS.
- K6: 3/3 byte-identical, sha256
  f981bf081530ebcf2bd32f44f2474703556154c94fa523819c9c1080be5e8e38
  x3. PASS.
- K7: frozen grep patterns return 0 standalone hits
  on learner.zag (multi-digit node ids 120/127/150/
  166/210/234/240 all 0; rel 38 and values 60/77/91
  appear only inside structural offsets like
  st[o+38] and st[..,1360], never as world
  literals). PASS.
- K8: t16F=7; e_has(4,1,16), (4,2,16), (5,1,16),
  (6,1,16), (7,1,16), (8,1,16), (9,3,16) all 1.
  PASS.

Falsifiers: 0 fired. F-COUNT silent (FULL as/ae:
333/2, 335/2, 324/2, 1193/2, 1242/2, 1102/2, exactly
the amended hand derivation). Ablate-arm
informational counts: 416/460/453/1183/1141/805,
each reconciled against the frozen algorithm (the
453 and 1183 incorporate the two amendment
corrections).

## Numbers

- FULL: QCOMB op=1 tries=1 as=333 ae=2 via=4 val=42;
  QSUB op=2 tries=2 as=335 ae=2 via=5 val=11;
  QTRUNC op=3 tries=3 as=324 ae=2 via=6 val=32;
  QINV op=4 tries=4 as=1193 ae=2 via=7 val=60;
  QABS op=5 tries=5 as=1242 ae=2 via=8 val=77;
  QCONC op=6 tries=6 as=1102 ae=2 via=9 val=91;
  re-asks via 4/5/6/7/8/9, MR_ENTERED=0; t16=7
  {4->1,4->2,5->1,6->1,7->1,8->1,9->3};
  LINK14 to 4..9; NM=10; distractor mD live=1; no
  edge type outside {14,16} in any arm.
- NOREUSE: all six -2, t16=0, NM=4. FRESH: all six
  -2, t16=0, NM=0.

## Disclosures and non-claims

- The six operators, descriptor extraction,
  entry/fold search with runtime relation discovery,
  strict reversed-relseq walk, pattern extraction
  with interface-match filter, pattern-MAP search
  with novel-folds check, first-verifying-operator
  enumeration, and cost counters are
  researcher-supplied generic machinery, frozen in
  the prereg. None names a relation, MAP, domain,
  query, operator-to-query assignment, source pair,
  or binding. The fixed operator order [1..6] is
  generic policy; which operator verifies is decided
  at runtime by execution, as the ablation arms
  demonstrate.
- INVERT here is relation-sequence reversal applied
  forward (the learned structure's rels reversed,
  then walked strictly). Inverting a value mapping
  (reverse lookup) was named in the parent task but
  not attempted this wave; the harness is extensible
  to it.
- ABSTRACT extracts the pattern (interface rel +
  fold skeleton) from a single source descriptor and
  the query's own chain as the second example; the
  multi-source common-structure form is future work.
- This is L2 (learner-driven structural adaptation
  with operator choice), not L3: the operator menu
  is researcher-supplied. Meta-selection does not
  invent operators.
- OP_MASK is a driver-set causal-control flag (the
  COMBINE_ON precedent), never written by the
  learner; it enables the lesion comparison and is
  set per ARM, never per query.
- One world family. No generality claim beyond the
  nine arms; the world is builder-designed, not
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
- The parent lane's PREREG.md file on disk is
  physically truncated mid-sentence (committed
  truncated at 4f043b49f); this lane's PREREG.md was
  verified byte-whole before freezing, and
  PREREG_AMENDMENT1.md records the two hand-
  derivation corrections transparently pre-verdict.

## Files

- `learner.zag`, `world.zag`, `driver.zag`,
  `mx_full.zag` (concatenated build input),
  `mx_bin` (pinned-znc binary), `mx_compile.txt`,
  `mx_run1.txt`, `mx_run2.txt`, `mx_run3.txt`
- `NAMECHECK.md` (Step 0 toolchain guard),
  `PREREG.md` (frozen, committed alone at 89b3bbaf9
  before implementation), `PREREG_AMENDMENT1.md`
  (pre-verdict arithmetic corrections)
