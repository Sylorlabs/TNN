# PREREG: L2-INVERT-VALUE (value-mapping inversion completes op 4 INVERT)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l2_invert_value/` only.
Worker: L2-INVERT-VALUE subagent (depth 2/2), 2026-10-03.
Parent mandate: L2-METAREUSE-EXTEND achieved
L2-METAREUSE-EXTEND-PASS (K1-K8) with six operators, but
disclosed honestly: "INVERT here is relation-sequence
reversal (value-mapping inversion not attempted)". This
lane completes the INVERT operator: INVERT must also invert
the VALUE MAPPING, not just the relation sequence. This is
a non-ledger task.

## 1. What is being tested

What "value-mapping inversion" means for a MAP. A MAP
implements a key->value mapping: key --forward relation
sequence--> terminal --value relation--> value. The
value-mapping inverse implements value->key: value
--value relation (reversed)--> terminal --forward rels
walked backward--> key. If the MAP maps A->B, the inverse
maps B->A.

Concretely for the taught MAP mA (id 1): forward rels
[18,5,6,5,6,5,6], facts [7,0,1,2,3,4,5], start 100, end
43, value relation 2 with fact 6 = (43,2,11). mA's value
mapping is 100->11. The value-mapping inverse is 11->100:
reverse value lookup (which terminal carries value 11?
fact 6 says 43) then backward chain walk
43->32->42->31->41->30->40->100 against world facts.

The load-bearing question the parent task asks: "Can the
learner do it? (or is it just structural?)" The learner
must perform a genuine reverse lookup (the terminal
carrying the value is DISCOVERED by scanning facts, never
given) and a genuine backward traversal (each hop inverts
a world fact obj->sub, verified step by step). It is not
just reversing an array: the structural form (Form A)
cannot solve the new query, and the value-mapping form
(Form B) cannot solve the old structural query. Each form
is necessary for its query; neither subsumes the other.

New query (driver-issued as (start,terminal,value,cap,dom)
plus one arm-level OP_MASK; no MAP id, no operator, no
source, no binding):
  Q_INVVAL: (11,100,11, AGG,A) -> op 4 INVERT Form B,
    Z id 10. The query presents the VALUE 11 (as start and
    as value) and asks for the KEY 100. Ops 1-3 fail (no
    fact with sub==11, so no entry scan, no candidate, no
    segment grounds). Op 4 Form A fails (reversed rels
    [6,5,6,5,6,5,18] walked forward from 11: no rel-6 hop
    from 11). Op 4 Form B: reverse value lookup finds
    fact 6 (43,2,11), t*=43 which EQUALS mA's stored
    terminal 43, backward walk 43->32->42->31->41->30->
    40->100 reaches t=100. The value v=11 is consumed by
    the reverse lookup itself (that IS the reverse
    lookup); no separate valof check is needed or
    performed.

Form order inside op 4: Form B (value-mapping inversion)
is tried FIRST; Form A (structural relation-sequence
reversal, the parent lane's form, unchanged) is the
fallback when Form B fails. Rationale frozen here: Form
B completes INVERT per the parent task, so it takes
precedence; structural reversal remains for queries that
do not ground a reverse value chain. Visible
discrimination in the FULL trace: Q_INV shows
MR-INVVAL-FAIL then MR-INV-OK (value 60's terminal 127
is not mA's terminal 43, so value-inversion fails;
structural inversion succeeds); Q_INVVAL shows
MR-INVVAL-OK with Form A never attempted.

The fixed operator enumeration order [1..6] and OP_MASK
semantics are unchanged from the parent lane. The
inverse MAP is ordinary learner-created structure: one
new per-MAP direction flag (see section 2), no new modes,
bridges, handlers, edge types, opcodes, or semantic
cases.

Concrete scenario (all ids frozen; world facts 0..43
identical to the parent lane; NO new world facts):
Queries (FULL arm order): QA (100,43,11,AGG,A),
QB (90,92,-1,ROUTE,B), Q_COMB (90,86,42,AGG,B) -> op 1,
Z 4; Q_SUB (200,43,11,AGG,A) -> op 2, Z 5;
Q_TRUNC (100,42,32,AGG,A) -> op 3, Z 6;
Q_INV (120,127,60,AGG,A) -> op 4 Form A, Z 7;
Q_ABS (150,166,77,AGG,A) -> op 5, Z 8;
Q_CONC (210,234,91,AGG,A) -> op 6, Z 9;
Q_INVVAL (11,100,11,AGG,A) -> op 4 Form B, Z 10.
Re-asks: Q_COMB-B, Q_SUB-B, Q_TRUNC-B, Q_INV-B, Q_ABS-B,
Q_CONC-B, Q_INVVAL-B -> via Z ids 4/5/6/7/8/9/10, no
meta phase (persistence + reuse; the inverse Z reuses via
backward pipeline execution).

Adapted structure built by the learner (FULL arm):
  Z_invval id 10: walk-order rels
    [2,6,5,6,5,6,5,18] (value hop first, then mA's
    forward rels in reverse order), walk-order facts
    [6,5,4,3,2,1,0,7] (value fact 6 = (43,2,11), then
    the backward-traversed chain facts), start 11, end
    100, dom=A(1), cap=AGG(1), dir=1 (inverse/backward),
    descriptor (de=2, dr1=6, dr2=5, dnf=3, dvr=2): the
    inverse walk's entry relation (the value relation),
    first backward fold pair, fold count, value
    relation. t16: 10->1 (single-source provenance to
    mA). LINK14 on deliver.

## 2. Frozen learner machinery (disclosed)

Standalone pure-Zag learner (learner.zag) + environment
side (world.zag: 44 frozen facts, UNCHANGED from the
parent lane) + experiment side (driver.zag: teaching,
nine arms, in-Zag bar evaluation). The frozen TNN core
is not used. Unfrozen only; no frozen source touched.
This lane EXTENDS the parent harness: ops 1,2,3,5,6,
mr_combine, mr_substitute, mr_truncate, mr_abstract,
mr_concretize, mr_buildwin, mr_adapt enumeration,
ex_query, and all mechanical helpers are inherited
unchanged apart from the items below.

State: one u8 buffer, parent lane layout. One change:
MAP row byte +39 (previously pad, always 0) is now the
direction flag `dir`: 0 = forward (all existing MAPs),
1 = inverse/backward (Z_invval). m_teach and
map_create set it (0 for taught/forward); map_create
takes a new trailing `dir` argument (existing six call
sites pass 0).

New / changed operations (all generic,
relation-agnostic, MAP-agnostic, domain-agnostic; no
capability literal except comparison against the
query's own cap; no operator literal except the fixed
1..6 enumeration order; no world/answer literals):
- ex_find_objrel(st,o,r): counted scan, first live fact
  with obj==o AND rel==r; returns fid or -1. Cost
  (first matching fid)+1 ticks, or 44 on no match
  (mirrors ex_find_subrel).
- chain_exec_bwd(st,fs,rs,n,start): backward execution
  over stored fact/rel arrays: each hop requires live
  fact, obj==cur, rel==rs[k], then cur=sub. One
  ex_exec call (same counting as chain_exec).
- m_exec: if MAP dir==1, each hop checks obj==cur AND
  rel==stored rel, then cur=sub (backward); else the
  existing forward check. No tick change.
- mr_invert_val(st,ob,atp,s,t,v,qdom,qcap,agg_src):
  operator 4 Form B. Prints MR-SRC-INV (kept in
  mr_invert before the forms). Reads the source's
  forward rels (rlen rl), d_valrel dvr, stored end
  aend. Reverse value lookup: scan all 44 fids (every
  fid ticked, cost 44), first live fact with
  rel==dvr AND obj==v gives value-fact tfv and
  terminal tstar; prints MR-INVVAL-LOOKUP with tstar
  and srcend=aend. If none, or tstar!=aend (the value
  does not belong to THIS source's value mapping),
  prints MR-INVVAL-FAIL and returns -2. Else backward
  walk from tstar along the source's forward rels in
  reverse order (one ex_find_objrel per hop,
  collecting fids into hf[1..], hr[0]=dvr/hf[0]=tfv
  as the value hop); any missing hop prints
  MR-INVVAL-FAIL and returns -2. On reaching cur:
  require cur==t (else MR-INVVAL-VERIFY-FAIL, -2);
  the value v was consumed by the reverse lookup. On
  success prints MR-INVVAL-WALK with the recovered
  key and MR-INVVAL-OK, then mr_buildwin_inv.
- mr_buildwin_inv(st,ob,atp,s,t,v,qdom,qcap,src1,hr,
  hf,zl,de,dr1,dr2,dnf,dvr): mirrors mr_buildwin but
  verifies with chain_exec_bwd over the walk-order
  arrays, creates the MAP with dir=1 via map_create,
  single-source t16 edge to src1, ex_deliver. Same
  MR-ZBUILD / MR-VERIFY / MR-PROMOTE trace tags.
  ae=2 on the committing path (chain_exec_bwd verify
  + deliver m_exec), 0 otherwise.
- mr_invert: unchanged Form A (structural reversal +
  strict forward walk, MR-INV-REV / MR-INV-FAIL /
  MR-INV-VERIFY-FAIL / MR-INV-OK) now runs ONLY if
  Form B fails (ans<0). mr_adapt op-4 slot unchanged
  (mask bit 8 gates both forms together: they are one
  operator).
- ex_query pipeline: after m_exec(st,mid,s)==t, if the
  MAP's dir==1, vv = obj of the MAP's stored fact[0]
  (the value fact: the inverse mapping's value at its
  terminal is the looked-up value, read from learner
  state + world, never from the query); else the
  existing ex_valof logic. No other pipeline change.

What the driver never does: name an operator, a form,
a trace tag, a MAP id, a source, a binding, or a
segment. Queries are (start,terminal,value,cap,dom)
plus one arm-level OP_MASK.

## 3. Frozen counting rules

Parent lane rules unchanged, plus:
- ex_find_objrel(o,r) costs (first matching fid)+1
  ticks, or 44 ticks when no live fact matches.
- The reverse value lookup costs 44 ticks (every fid
  ticked, fid order, first match wins).
- chain_exec_bwd costs one ex_exec (as chain_exec).
- mr_buildwin_inv verify + deliver contribute ae=2 on
  the committing path; a failed Form B contributes
  ae=0.

## 4. Kill bars (parent K1-K8 numbering, adapted)

Arms (nine): FULL mask 63; ABLATE-COMBINE mask 62;
ABLATE-SUBST mask 61; ABLATE-TRUNC mask 59; ABLATE-INV
mask 55 (op 4 OUT: both forms); ABLATE-ABS mask 47;
ABLATE-CONC mask 31; NOREUSE mask 0; FRESH mask 63,
facts only (no MAPs). Every arm issues QA, QB, then
the seven reuse queries in fixed order
(Q_COMB, Q_SUB, Q_TRUNC, Q_INV, Q_ABS, Q_CONC,
Q_INVVAL); FULL additionally re-asks all seven.

- K1 (X and Y exist before reuse, learned
  independently): in-Zag qa_via=1, qb_via=2, disj=1.
  Shell: `Q QA` before `Q QB` before `Q QCOMB`.
- K2 (no single structure solves the reuse queries;
  reuse REQUIRED): in-Zag all seven phit=0 in FULL
  (qc/qs/qt/qv/qe/qn/qvv_phit), NOREUSE arm all seven
  vals=-2, t16=0. Shell: verbatim `MR-PIPELINE-FAIL`
  for each of the seven reuse queries in FULL and
  NOREUSE.
- K3 (learner decides WHICH operator per query, not
  the researcher): in-Zag qc_op=1, qs_op=2, qt_op=3,
  qv_op=4, qe_op=5, qn_op=6, qvv_op=4; tries
  1/2/3/4/5/6/4; decided=1 each; qc_asrc=1,
  qvv_asrc=1 (AGG source is mA for all). Shell
  verbatim, in order per query: `MR-OP-TRY N` ...
  `MR-OP-OK N`; Q_INVVAL shows `MR-OP-TRY 1`,
  `MR-OP-FAIL 1`, `MR-OP-TRY 2`, `MR-OP-FAIL 2`,
  `MR-OP-TRY 3`, `MR-OP-FAIL 3`, `MR-OP-TRY 4`,
  `MR-INVVAL-OK`, `MR-OP-OK 4` with NO `MR-INV-REV`
  after (Form A never attempted); Q_INV shows
  `MR-INVVAL-FAIL` before `MR-INV-REV`/
  `MR-INV-OK` (Form B tried first and failed).
  `grep -c` of MR-OP-TRY/MR-OP-OK/MR-SUB-CAND/
  MR-TRUNC-TRY/MR-ABS-CAND/MR-CONC-CAND/MR-INV-REV/
  MR-INVVAL-LOOKUP/MR-INVVAL-OK/MR-BIND in driver.zag
  = 0: the driver never names an operator, a form, or
  a trace tag; ex_query takes only the arm-level
  OP_MASK.
- K4 (adapted structures succeed where sources alone
  fail): in-Zag qc_via=4, qc_val=42; qs_via=5,
  qs_val=11; qt_via=6, qt_val=32; qv_via=7, qv_val=60;
  qe_via=8, qe_val=77; qn_via=9, qn_val=91;
  qvv_via=10, qvv_val=11; zc=zs=zt=zi=za=zn=zv=1
  (exact header/rels/facts/descriptor/dir match per
  section 1; zv checks rlen=8, start=11, end=100,
  dir=1, rels [2,6,5,6,5,6,5,18], facts
  [6,5,4,3,2,1,0,7], descriptor (2,6,5,3,2)).
  Shell verbatim `ANS term=... val=... via=...` for
  all seven, plus the seven `MR-ZBUILD` lines.
- K5 (each operator necessary for its query; op 4 as
  ONE operator covers both its queries): six
  ablation arms. In-Zag: ABLATE-COMBINE: qC=-2,
  others 11/32/60/77/91/11, t16=6. ABLATE-SUBST:
  qS=-2, others 42/32/60/77/91/11, t16=7.
  ABLATE-TRUNC: qT=-2, others 42/11/60/77/91/11,
  t16=7. ABLATE-INV: qV=-2 AND qVV=-2, others
  42/11/32/77/91, t16=6. ABLATE-ABS: qE=-2, others
  42/11/32/60/91/11, t16=7. ABLATE-CONC: qN=-2,
  others 42/11/32/60/77/11, t16=7. (Z ids shift down
  by one in each ablation arm after the missing Z;
  t16 counts: FULL has 8 edges
  {4->1,4->2,5->1,6->1,7->1,8->1,9->3,10->1}.)
- K6 (determinism): 3/3 runs byte-identical
  (sha256 x3).
- K7 (no world/answer literals in the learner): frozen
  two-part audit on learner.zag. (a) Token allowlist:
  strip `//` comments and `"..."` string literals, extract
  every numeric token via `grep -P -o
  '(?<![0-9a-zA-Z_.])-?[0-9]+'`; the resulting set must
  equal exactly the frozen allowlist
  {-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,14,16,20,24,32,33,
  34,35,36,37,38,39,40,44,45,48,64,255,256,368,1008,
  1264,1328,1332,1336,1340,1344,1348,1352,1356,1360,
  1364,1368,1372,1376,1380,1384,1388,65536}
  (structural: sentinels, state offsets, MAP field
  offsets, edge types, map tag, capacities, strides,
  pack bases, stat offsets; verified complete on the
  parent lane's learner.zag). In particular none of
  120,127,150,166,210,234,240,60,77,91,43,100,90,86,
  42,200,18,19,17,15 may appear at all. (b) New-id spot
  check: the Q_INVVAL triple 11/43/100 must not occur
  outside the allowlisted structural context `st[11]`
  (IN_MR flag): `grep -P -c
  '(?<![0-9a-zA-Z_\[])11(?![0-9])'` hits only the two
  pre-existing `st[11]` uses, and `43`/`100` return 0
  hits under the part-(a) token rule.
- K8 (provenance): in-Zag t16F=8, e_has(4,1,16)=1,
  e_has(4,2,16)=1, e_has(5,1,16)=1, e_has(6,1,16)=1,
  e_has(7,1,16)=1, e_has(8,1,16)=1, e_has(9,3,16)=1,
  e_has(10,1,16)=1. Each adapted Z carries
  derived-from provenance to its source(s).

Falsifiers (in-Zag, any one fires => verdict FAIL):
F-EDGE-NEW (any arm with an edge type outside
{14,16}); F-COUNT (any FULL-arm as/ae deviating from
section 5); F-NO-GROUND-* (any reuse query via != its
section-1 Z id, incl. F-NO-GROUND-INVVAL qvv_via!=10);
F-WRONG-Z* (any d_check_* != 1, incl. F-WRONG-ZV);
F-PIPE-HIT-* (any reuse query phit != 0, incl.
F-PIPE-HIT-INVVAL); F-NOREUSE-*/F-FRESH-* (any reuse
val != -2, incl. the INVVAL variants); F-ABLATE*
(ablated query val != -2, or a surviving query val
wrong, or t16 wrong; ABLATE-INV additionally bars
av_qvv_val != -2); F-RE-*-ENTERED/VIA/VAL (any re-ask
with MR_ENTERED != 0, wrong via, or wrong val, incl.
F-RE-INVVAL-*: qvvb_en!=0, qvvb_via!=10,
qvvb_val!=11); F-OP-* (committed op != query index,
incl. F-OP-INVVAL qvv_op!=4); F-TRIES-* (tries !=
query index, incl. F-TRIES-INVVAL qvv_tries!=4);
F-T16-COUNT (t16F != 8); F-NO-T16-* (incl.
F-NO-T16-101); F-NO-LINK14-* (incl. F-NO-LINK14-10);
F-SRC-A (qc_asrc != 1); F-SRC-AVV (qvv_asrc != 1);
F-DISTR-SURVIVES (mD not live at FULL end).

## 5. Hand-derived counts (N=44 facts; F-COUNT bars the FULL-arm values)

Notation: find(s,r)=F means ex_find_subrel(s,r) costs F
ticks (first matching fid +1, or 44 on no match);
objfind(o,r)=F is the same for ex_find_objrel. All
seven FULL-arm queries end ae=2 (buildwin
verify+deliver).

QCOMB/QSUB/QTRUNC: op 4 never runs (earlier operator
commits); unchanged from the parent lane: 333, 335,
324.

QINV (120,127,60), nm=7: as=1186, ae=2.
  Parent 1142 = 2 (agg) + 7 (partner) + 548 (op-1) +
  208 (op-2) + 181 (op-3) + 196 (op-4 Form A). New
  op-4 = Form B first: reverse value lookup 44 ticks
  (finds fact 27 = (127,2,60), t*=127 != mA end 43
  -> MR-INVVAL-FAIL, no walk), then Form A 196.
  op-4 total = 44+196 = 240. as = 1142-196+240 =
  1186.

QABS (150,166,77), nm=8: as=1286, ae=2.
  Parent 1242 = 2+8+624 (op-1) + 44 (op-2) + 245
  (op-3) + 44 (op-4) + 275 (op-5). New op-4 = Form B
  44 (lookup finds fact 35 = (166,2,77), t*=166 !=
  43 -> FAIL) + Form A 44 (find(150,6) miss) = 88.
  as = 1242-44+88 = 1286.

QCONC (210,234,91), nm=9: as=1146, ae=2.
  Parent 1102 = 2+9+250 (op-1) + 250 (op-2) + 162
  (op-3) + 44 (op-4) + 88 (op-5) + 297 (op-6). New
  op-4 = Form B 44 (lookup finds fact 42 =
  (234,2,91), t*=234 != 43 -> FAIL) + Form A 44
  (find(210,6) miss) = 88. as = 1102-44+88 = 1146.

QINVVAL (11,100,11), nm=10: as=393, ae=2.
  2 (agg: id0 SKIP, id1 MATCH)
  + 10 (partner collection over 10 MAPs)
  + 176 (op-1: rsrcs mD, mB0; per rsrc b=1
  mr_agg_seg entry 44 miss + b=2 mr_route_seg 44
  miss = 88; x2 = 176)
  + 44 (op-2: candidate collection 44, no sub==11)
  + 88 (op-3: nf2=2 entry 44 miss, nf2=1 entry 44
  miss)
  + 73 (op-4 Form B: reverse value lookup 44, finds
  fact 6 = (43,2,11), t*=43 == mA end 43; backward
  walk objfind(43,6)=6, objfind(32,5)=5,
  objfind(42,6)=4, objfind(31,5)=3, objfind(41,6)=2,
  objfind(30,5)=1, objfind(40,18)=8 -> 6+5+4+3+2+1+8
  = 29; cur=100==t; MR-INVVAL-OK; Form A never
  attempted)
  = 2+10+176+44+88+73 = 393.

Ablation-arm informational counts (ablated query only;
not kill-barred, reported for transparency):
- ABLATE-COMBINE QCOMB as=460: parent 416 = 2+109
  (op2) + 104 (op3) + 44 (op4) + 44 (op5) + 113
  (op6). New op-4 = Form B 44 (lookup v=42 -> fact
  17 = (86,2,42), t*=86 != 43 -> FAIL) + Form A 44
  (find(90,6) miss) = 88. as = 416-44+88 = 460.
- ABLATE-SUBST QSUB as=533: parent 460 = 2+5+256
  (op1) + 51 (op3) + 44 (op4) + 44 (op5) + 58 (op6).
  New op-4 = Form B 73 (lookup v=11 -> t*=43 == 43;
  walk 29 reaches key 100 != t=43 ->
  MR-INVVAL-VERIFY-FAIL) + Form A 44 (find(200,6)
  miss) = 117. as = 460-44+117 = 533. Note: Form B
  walks correctly but the query terminal does not
  match: the value 11 inverts to key 100, not to
  43.
- ABLATE-TRUNC QTRUNC as=585: parent 541 = 2+6+234
  (op1) + 88 (op2) + 44 (op4) + 65 (op5) + 102
  (op6). New op-4 = Form B 44 (lookup v=32 -> fact
  19 = (42,2,32), t*=42 != 43 -> FAIL) + Form A 44
  (find(100,6) miss) = 88. as = 541-44+88 = 585.
- ABLATE-INV QINV as=1132: op 4 skipped; ops
  1,2,3,5,6 unchanged from parent. as=1132.
- ABLATE-INV QINVVAL as=411: op 4 skipped; nm=9:
  2 (agg) + 9 (partner) + 176 (op-1: same 44/44 per
  rsrc as FULL) + 44 (op-2) + 88 (op-3) + 44 (op-5:
  no sub==11 && rel==18 candidate) + 48 (op-6:
  pattern search 4 + candidates 44, no sub==11) =
  411.
- ABLATE-ABS QABS as=1185: parent 1141 = 2+8+624
  (op1) + 44 (op2) + 245 (op3) + 44 (op4) + 174
  (op6). New op-4 = 44 (Form B: t*=166 != 43) + 44
  (Form A: find(150,6) miss) = 88. as =
  1141-44+88 = 1185.
- ABLATE-CONC QCONC as=849: parent 805 = 2+9+250
  (op1) + 250 (op2) + 162 (op3) + 44 (op4) + 88
  (op5). New op-4 = 44 (Form B: t*=234 != 43) + 44
  (Form A: find(210,6) miss) = 88. as =
  805-44+88 = 849.

F-COUNT bars (in-Zag falsifiers): QC-AS=333, QC-AE=2;
QS-AS=335, QS-AE=2; QT-AS=324, QT-AE=2; QV-AS=1186,
QV-AE=2; QE-AS=1286, QE-AE=2; QN-AS=1146, QN-AE=2;
QVV-AS=393, QVV-AE=2.
