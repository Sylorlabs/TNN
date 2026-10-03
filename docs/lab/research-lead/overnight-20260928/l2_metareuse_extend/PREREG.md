# PREREG: L2-METAREUSE-EXTEND (INVERT / ABSTRACT / CONCRETIZE)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l2_metareuse_extend/` only.
Worker: L2-METAREUSE-EXTEND subagent (depth 2/2), 2026-10-03.
Parent mandate: extend the L2-METAREUSE meta-reuse harness
(L2-METAREUSE-PASS, K1-K8, operators 1=COMBINE,
2=SUBSTITUTE, 3=TRUNCATE) with three new reuse operators:
4=INVERT (reverse a structure), 5=ABSTRACT (extract a
pattern from examples), 6=CONCRETIZE (instantiate a pattern
with specific values). New op ids + mask bits in the
existing harness. New queries, each solvable by exactly one
of the new operators. The learner selects by trial
verification under the same fixed order [1..6]; verification
decides. This extends L2 adaptive reuse to the full
frontier named in the parent task. Parent kill bars K1-K8
govern, adapted to six operators. Non-ledger task.

## 1. What is being tested

Whether the learner, holding (X) the arithmetic
aggregation MAP mA, (Y) the planning ROUTE MAP mB0, (D) the
distractor ROUTE MAP mD, and (P) a taught 2-fold AGG
pattern MAP mP with a hole entry (d_entry=0), when faced
with SIX reuse queries on one world family, selects a
DIFFERENT reuse operator for each query by trial
verification under one fixed generic operator order, with
no operator named by the driver:

- Q_COMB (90,86,42,AGG,B): op 1 COMBINE (as in the parent lane).
- Q_SUB (200,43,11,AGG,A): op 2 SUBSTITUTE (as in the parent lane).
- Q_TRUNC (100,42,32,AGG,A): op 3 TRUNCATE (as in the parent lane).
- Q_INV (120,127,60,AGG,A): op 4 INVERT. The source mA's
  stored relation sequence [18,5,6,5,6,5,6] is reversed to
  [6,5,6,5,6,5,18] and walked strictly forward from the
  query start; the world holds a forward chain matching
  the reversed pattern. Ops 1-3 fail (COMBINE: AGG-head
  SHAPE-FAIL / partner-head dead; SUBSTITUTE: the one
  entry candidate SHAPE-FAILs on the 3rd fold pair;
  TRUNCATE: prefix walks miss the terminal).
- Q_ABS (150,166,77,AGG,A): op 5 ABSTRACT. The pattern
  (entry rel 18, 3 fold pairs, value rel 2) is extracted
  from the source descriptor; the query start's entry uses
  the SAME entry relation (rel==d_entry, so SUBSTITUTE's
  rel!=d_entry filter excludes it and TRUNCATE's fixed
  fold relations miss); the fold relations (8,9) are
  discovered at runtime from the query's own chain.
- Q_CONC (210,234,91,AGG,A): op 6 CONCRETIZE. The pattern
  MAP mP (2 folds, value rel 2, hole entry) is found by a
  generic pattern-source search; the query start offers
  two concrete entry bindings (a dead-end first, then the
  live one with a fresh entry rel 38); the fold relations
  (11,12) are discovered at runtime and must DIFFER from
  the source structure's (5,6) (else it is not a new
  instantiation); the first verifying instantiation wins.

The operator enumeration order is fixed and generic:
[1=COMBINE, 2=SUBSTITUTE, 3=TRUNCATE, 4=INVERT,
5=ABSTRACT, 6=CONCRETIZE]; the FIRST operator whose full
grounding executes to the query terminal with the required
value is committed. OP_MASK (driver-set causal-control
flag, one value per ARM, never per query, never written by
the learner) gates which operators may be tried:
bit0=COMBINE, bit1=SUBSTITUTE, bit2=TRUNCATE, bit3=INVERT,
bit4=ABSTRACT, bit5=CONCRETIZE, tested via (mask/n)%2 with
n=1,2,4,8,16,32, no bitwise ops.

The load-bearing discrimination: the SAME fixed order and
the SAME mask (63) yield SIX different committed operators
on six queries (1,2,3,4,5,6). Position-in-order cannot
explain this (it predicts op 1 always commits); each
query skipping all earlier ops proves verification
against world facts decides. The six ablation arms prove
each operator is necessary for its query: with op N
masked out, query N fails while the other five still pass.

Concrete scenario (all ids frozen). World facts (44):
  0:(40,5,30) 1:(30,6,41) 2:(41,5,31) 3:(31,6,42)
  4:(42,5,32) 5:(32,6,43)
  6:(43,2,11) 7:(100,18,40)
  8:(90,7,91) 9:(91,7,92) 10:(92,17,80) 11:(80,15,81)
  12:(81,16,82) 13:(82,15,83) 14:(83,16,84) 15:(84,15,85)
  16:(85,16,86) 17:(86,2,42)
  18:(200,19,40) 19:(42,2,32)
  20:(120,6,121) 21:(121,5,122) 22:(122,6,123)
  23:(123,5,124) 24:(124,6,125) 25:(125,5,126)
  26:(126,18,127) 27:(127,2,60)
  28:(150,18,160) 29:(160,8,161) 30:(161,9,162)
  31:(162,8,163) 32:(163,9,164) 33:(164,8,165)
  34:(165,9,166) 35:(166,2,77)
  36:(210,18,220) 37:(210,38,230) 38:(230,11,231)
  39:(231,12,232) 40:(232,11,233) 41:(233,12,234)
  42:(234,2,91) 43:(240,0,42)
Fids 0-19 are identical to the parent lane. All node, rel,
fact ids < 256 (u8 cells).
MAPs (taught in this order):
  mD id0: dom=A(1), cap=ROUTE(2), rels [6], facts [1],
    start 30, end 41 (distractor, taught first).
  mA id1 (X): dom=A(1), cap=AGG(1), rels
    [18,5,6,5,6,5,6], facts [7,0,1,2,3,4,5], start 100,
    end 43. Descriptor: entry=18, r1=5, r2=6, nf=3,
    valrel=2.
  mB0 id2 (Y): dom=B(2), cap=ROUTE(2), rels [7,7], facts
    [8,9], start 90, end 92.
  mP id3 (P): dom=A(1), cap=AGG(1), rels [0,5,6,5,6],
    facts [43,4,5], start 240, end 43. Descriptor:
    entry=0 (hole: no query start uses rel 0 as a live
    entry except mP's own example), r1=5, r2=6, nf=2,
    valrel=2 (first live fact with sub==43 is fid 6,
    rel 2).

Queries (driver-issued as (start, terminal, value, cap,
dom) plus one arm-level OP_MASK; no MAP id, no operator,
no source pair, no binding, no segment information):
  QA:       (100,43,11, AGG,A) -> via mA (X works at home)
  QB:       (90,92,-1, ROUTE,B) -> via mB0 (Y works at home)
  Q_COMB:   (90,86,42, AGG,B)  -> op 1 COMBINE, Z id 4
  Q_SUB:    (200,43,11, AGG,A) -> op 2 SUBSTITUTE, Z id 5
  Q_TRUNC:  (100,42,32, AGG,A) -> op 3 TRUNCATE, Z id 6
  Q_INV:    (120,127,60, AGG,A) -> op 4 INVERT, Z id 7
  Q_ABS:    (150,166,77, AGG,A) -> op 5 ABSTRACT, Z id 8
  Q_CONC:   (210,234,91, AGG,A) -> op 6 CONCRETIZE, Z id 9
  re-asks:  Q_COMB-B, Q_SUB-B, Q_TRUNC-B, Q_INV-B,
            Q_ABS-B, Q_CONC-B -> via Z ids 4/5/6/7/8/9,
            no meta phase (persistence + reuse)

Adapted structures (built by the learner, FULL arm):
  Z_comb id4: rels [7,7,17,15,16,15,16,15,16], facts
    [8,9,10,11,12,13,14,15,16], start 90, end 86, dom=B,
    cap=AGG, descriptor (0,0,0,0,2). t16: 4->1, 4->2.
  Z_sub id5: rels [19,5,6,5,6,5,6], facts
    [18,0,1,2,3,4,5], start 200, end 43, dom=A, cap=AGG,
    descriptor (19,5,6,3,2). t16: 5->1.
  Z_trunc id6: rels [18,5,6,5,6], facts [7,0,1,2,3],
    start 100, end 42, dom=A, cap=AGG, descriptor
    (18,5,6,2,2). t16: 6->1.
  Z_inv id7: rels [6,5,6,5,6,5,18], facts
    [20,21,22,23,24,25,26], start 120, end 127, dom=A,
    cap=AGG, descriptor (6,5,6,3,2) (reversed entry 6,
    reversed folds (5,6) x3). t16: 7->1.
  Z_abs id8: rels [18,8,9,8,9,8,9], facts
    [28,29,30,31,32,33,34], start 150, end 166, dom=A,
    cap=AGG, descriptor (18,8,9,3,2) (extracted pattern
    entry 18 + runtime-discovered folds (8,9) x3).
    t16: 8->1.
  Z_conc id9: rels [38,11,12,11,12], facts
    [37,38,39,40,41], start 210, end 234, dom=A,
    cap=AGG, descriptor (38,11,12,2,2) (concretized
    entry 38 + concretized folds (11,12) x2). t16: 9->3.

## 2. Frozen learner machinery (disclosed)

Standalone pure-Zag learner (learner.zag, mx_ prefix kept
as mr_ for harness continuity, MR- trace tags) +
environment side (world.zag: 44 frozen facts) +
experiment side (driver.zag: teaching, nine arms, in-Zag
bar evaluation). The frozen TNN core is not used. Unfrozen
only; no frozen source touched. This lane EXTENDS the
parent harness: ops 1-3, mr_combine, mr_substitute,
mr_truncate, mr_buildwin, ex_query pipeline, and all
mechanical helpers are inherited unchanged apart from the
mechanical state-layout shift below.

State: one u8 buffer. Layout (44-fact capacity; the parent
lane's 38-fact layout is shifted mechanically: every MAP
base 320->368, edge base 960->1008, answer base
1216->1264, every stat offset +80; the fact base stays
16). Offsets: 0 NF, 1 NM, 2 NE, 3 reserved, 4 NN,
5 unused, 6 STALE_MAP, 7 STALE_HOP, 8 STALE_FACT,
9 LAST_VIA, 10 unused, 11 IN_MR, 12 MR_ENTERED. Facts:
44 x 8 bytes at 16..367 [sub,rel,obj,live,0,0,0,0].
MAPs: 16 x 40 bytes at 368..1007 [tag=20,live,start,end,
rlen,flen,reason,pad, rels x12 @+8, facts x12 @+20,
dom @+32, cap @+33, d_entry @+34, d_r1 @+35, d_r2 @+36,
d_nf @+37, d_valrel @+38, pad @+39]. Edges: 64 x 4 bytes
at 1008..1263 [from,to,type,pad]. Answer nodes: 16 x 4
bytes at 1264..1327 [via,0,0,0] (16 slots: the FULL arm
issues 14 answers). Stats: SEARCH i32 @1328, EXEC i32
@1332, A_SEARCH i32 @1336, A_EXEC i32 @1340, LAST_VAL i32
@1344, AGG_SRC i32 @1348, ROUTE_SRC i32 @1352,
BINDING i32 @1360, BIND_DECIDED i32 @1364,
BIND_TRIES i32 @1368 (binding attempts made),
PIPE_HIT i32 @1372, LAST_TERM i32 @1376, MR_OP i32 @1380
(chosen operator for current query, -1 none),
MR_OP_TRIES i32 @1384 (operator attempts made),
MR_OP_DECIDED i32 @1388 (set ONLY in a committing
branch), OP_MASK i32 @1392 (driver-set causal-control
flag, never written by the learner). Scratch at 1396+.

Edge-type semantics (reused, zero new types):
- type 16: derived-from. Z_comb: 4->1 AND 4->2. Z_sub:
  5->1. Z_trunc: 6->1. Z_inv: 7->1. Z_abs: 8->1.
  Z_conc: 9->3.
- type 14 (LINK14): answer-node -> delivering MAP on
  deliver.
- No other edge types may appear.

Generic operations (frozen, relation-agnostic,
MAP-agnostic, domain-agnostic; no capability literal
except comparison against the query's own cap; no
operator literal except the fixed 1..6 enumeration
order):
- f_teach (capacity 44), m_teach (with generic AGG
  descriptor extraction), map_create, map_retire,
  m_exec, chain_exec, e_add, e_count, e_has, e_has_to,
  ex_eoth: as in the parent lane, layout-shifted.
- ex_find_sub_skip / ex_find_subrel / ex_valof: counted
  scans (frozen counting rules, section 3).
- ex_foldwalk(st,u,k,vrel,ff): as in the parent lane.
- mr_agg_seg, mr_route_seg, mr_buildwin: as in the
  parent lane (MR- trace tags).
- mr_combine, mr_substitute, mr_truncate: as in the
  parent lane, unchanged logic.
- mr_invert(st,ob,atp,s,t,v,qdom,qcap,agg_src):
  operator 4. Prints MR-SRC-INV with the source id.
  Reads the source's stored rels (rlen rl) and reverses
  them into irev (irev[k]=rels[rl-1-k]); prints
  MR-INV-REV with the reversed rels. Strict forward walk
  from s over irev (one ex_find_subrel per hop,
  collecting fids; any missing hop prints MR-INV-FAIL
  and returns -2). On reaching cur: require cur==t
  (else MR-INV-VERIFY-FAIL, -2) and VAL(cur,dvr)==v
  via ex_valof (else VERIFY-FAIL, -2); on success print
  MR-INV-OK and mr_buildwin with single-source
  provenance to agg_src and descriptor
  (irev[0],irev[1],irev[2],(rl-1)/2,dvr).
- mr_abstract(st,ob,atp,s,t,v,qdom,qcap,agg_src):
  operator 5. Prints MR-SRC-ABS with the source
  descriptor, then MR-PATTERN with the extracted
  pattern (d_entry, d_nf, d_valrel: the interface and
  skeleton, concrete fold relations dropped). Collects
  entry candidates: all live facts with sub==s AND
  rel==d_entry (fid order, every fid ticked; the
  interface must MATCH, no adaptation). For each
  candidate (fid f, obj u): MR-ABS-CAND print;
  ex_foldwalk from u with k=d_nf and runtime (s1,s2)
  discovery; SHAPE-FAIL ends the candidate; on shape OK
  require term==t AND VAL(term,d_valrel)==v
  (VERIFY-OK/FAIL print); on VERIFY-OK build Z as
  rels=[d_entry,s1,s2,...] and facts=[f,ff...], then
  mr_buildwin with single-source provenance to agg_src
  and descriptor (d_entry,s1,s2,d_nf,d_valrel). First
  verifying candidate wins; the enumeration stops.
- mr_concretize(st,ob,atp,s,t,v,qdom,qcap,agg_src):
  operator 6. Pattern-source search: first live MAP in
  id order with cap==qcap AND d_entry==0 (the hole
  entry marks a pattern MAP; one ex_tickm per MAP
  scanned); none prints MR-NO-PATTERN and returns -2,
  else MR-PATTERN-SRC with the pattern id, nf, valrel.
  Collects entry candidates: ALL live facts with
  sub==s (any rel: the hole is concretized by whatever
  the query offers), fid order, every fid ticked. For
  each candidate (fid f, rel r, obj u): MR-CONC-CAND
  print; ex_foldwalk from u with k=p_nf (the
  pattern's nf) and runtime (s1,s2) discovery;
  SHAPE-FAIL ends the candidate; on shape OK require
  (s1,s2)!=(d_r1,d_r2) of agg_src (the concretized
  folds must be NOVEL values, else MR-CONC-OLD and the
  candidate is skipped: reusing the source's exact
  folds is not an instantiation); then require
  term==t AND VAL(term,p_valrel)==v (VERIFY-OK/FAIL);
  on VERIFY-OK build Z as rels=[r,s1,s2,...] and
  facts=[f,ff...], then mr_buildwin with
  single-source provenance to the PATTERN source and
  descriptor (r,s1,s2,p_nf,p_valrel). First verifying
  candidate wins; the enumeration stops.
- mr_adapt(st,ob,atp,s,t,v,qdom,qcap,agg_src,op_mask):
  fixed operator enumeration over [1..6]. For op in
  1..6: if the op's mask bit ((mask/n)%2, n=1,2,4,8,
  16,32) is 0, print MR-OP-SKIP N and continue; else
  MR_OP_TRIES++, print MR-OP-TRY N, run the
  operator; on ans>=0 set MR_OP=N, MR_OP_DECIDED=1
  (ONLY in the committing branch), print MR-OP-OK N
  and stop; else print MR-OP-FAIL N and continue.
- ex_query: as in the parent lane (pipeline over all
  live MAPs; on total failure the meta phase with
  AGG-source search = first live MAP with cap==qcap,
  then mr_adapt). Takes only the arm-level OP_MASK.

## 3. Frozen counting rules

- ex_tick / ex_tickm: +1 to A_SEARCH (and SEARCH) per
  call, i.e. one tick per fact scanned in
  ex_find_sub_skip, ex_find_subrel, mr_agg_seg entry
  scan, mr_substitute / mr_abstract / mr_concretize
  candidate collection; one tick per MAP scanned in
  mr_combine partner collection, ex_query AGG-source
  search, mr_concretize pattern-source search.
- ex_exec: +1 to EXEC, and +1 to A_EXEC iff IN_MR==1.
  Called once per m_exec and once per chain_exec.
- A_SEARCH / A_EXEC are zeroed at meta-phase entry, so
  they count the meta phase only. A query solved in the
  pipeline reports as=0, ae=0.
- ex_find_subrel(s,r) / ex_find_sub_skip(s,skip) cost
  (first matching fid)+1 ticks, or N=44 ticks when no
  live fact matches.
- mr_agg_seg entry scan costs (first fid with sub==s)+1
  ticks (any rel).
- Candidate collections cost N=44 ticks (every fid
  ticked, fid order).
- ex_foldwalk(u,k,vrel,ff) costs the sum of its
  ex_find_sub_skip / ex_find_subrel calls, stopping at
  the first failure (returns 0).
- mr_buildwin verify (chain_exec) + ex_deliver
  (m_exec) contribute ae=2 on every committing path;
  a failed operator contributes ae=0.

## 4. Kill bars (parent K1-K8 numbering, adapted)

Arms (nine): FULL mask 63; ABLATE-COMBINE mask 62 (op 1
out); ABLATE-SUBST mask 61 (op 2 out); ABLATE-TRUNC mask
59 (op 3 out); ABLATE-INV mask 55 (op 4 out);
ABLATE-ABS mask 47 (op 5 out); ABLATE-CONC mask 31
(op 6 out); NOREUSE mask 0; FRESH mask 63, facts only
(no MAPs). Every arm issues QA, QB, then the six reuse
queries in fixed order; FULL additionally re-asks all
six (Q_COMB-B ... Q_CONC-B) after.

- K1 (X and Y exist before reuse, learned
  independently): in-Zag qa_via=1, qb_via=2, disj=1 (mA
  rels in {18,5,6}, mB0 rels all 7). Shell: `Q QA`
  before `Q QB` before `Q QCOMB`.
- K2 (no single structure solves the reuse queries;
  reuse REQUIRED): in-Zag all six phit=0 in FULL,
  NOREUSE arm all six vals=-2, t16=0. Shell: verbatim
  `MR-PIPELINE-FAIL` for each of the six reuse queries
  in FULL and NOREUSE.
- K3 (learner decides WHICH operator per query, not the
  researcher): in-Zag qi_op: qc_op=1, qs_op=2, qt_op=3,
  qv_op=4, qe_op=5, qn_op=6; tries 1/2/3/4/5/6;
  decided=1 each; qc_asrc=1 (AGG source is mA for all).
  Shell verbatim, in order per query: `MR-OP-TRY N`
  ... `MR-OP-OK N` with N=1..6, and the earlier ops
  failing (e.g. QINV shows `MR-OP-TRY 1`,
  `MR-OP-FAIL 1`, `MR-OP-TRY 2`, `MR-OP-FAIL 2`,
  `MR-OP-TRY 3`, `MR-OP-FAIL 3`, `MR-OP-TRY 4`,
  `MR-INV-OK`, `MR-OP-OK 4`). `grep -c` of
  MR-OP-TRY/MR-OP-OK/MR-SUB-CAND/MR-TRUNC-TRY/
  MR-ABS-CAND/MR-CONC-CAND/MR-INV-REV/MR-BIND in
  driver.zag = 0: the driver never names an operator
  or a trace tag; ex_query takes only the arm-level
  OP_MASK. The same fixed order and the same mask
  (63) yield different operators on different queries,
  so position-in-order cannot explain the choice.
- K4 (adapted structures succeed where sources alone
  fail): in-Zag qc_via=4, qc_val=42; qs_via=5,
  qs_val=11; qt_via=6, qt_val=32; qv_via=7,
  qv_val=60; qe_via=8, qe_val=77; qn_via=9,
  qn_val=91; zc=zs=zt=zi=za=zn=1 (exact
  header/rels/facts/descriptor match per section 1).
  Shell verbatim `ANS term=... val=... via=...` for
  all six, plus the six `MR-ZBUILD` lines.
- K5 (each operator necessary for its query): six
  ablation arms. In-Zag: ABLATE-COMBINE: qC=-2, others
  11/32/60/77/91, t16=5. ABLATE-SUBST: qS=-2, others
  42/32/60/77/91, t16=6. ABLATE-TRUNC: qT=-2, others
  42/11/60/77/91, t16=6. ABLATE-INV: qV=-2, others
  42/11/32/77/91, t16=6. ABLATE-ABS: qE=-2, others
  42/11/32/60/91, t16=6. ABLATE-CONC: qN=-2, others
  42/11/32/60/77, t16=6. (Z ids shift down by one in
  each ablation arm after the missing Z; t16 counts:
  the ablated Z's edges are absent.)
- K6 (determinism): 3/3 runs byte-identical
  (sha256 x3).
- K7 (no world/answer literals in the learner):
  frozen grep patterns return 0 hits on learner.zag
  (fixed-string): the new node/rel/value ids
  120, 127, 150, 166, 210, 234, 240, 38, 60, 77, 91,
  plus the parent lane's 90, 86, 42, 200, 43, 11,
  100, 32, 18, 19, 5, 6, 7, 17, 15, 16, 2. (Legitimate
  small structural literals such as op ids 1..6, edge
  types 14/16, map tag 20, and state offsets are not
  world/answer literals; the audit uses patterns that
  cannot collide with them.)
- K8 (provenance): in-Zag t16F=7, e_has(4,1,16)=1,
  e_has(4,2,16)=1, e_has(5,1,16)=1, e_has(6,1,16)=1,
  e_has(7,1,16)=1, e_has(8,1,16)=1, e_has(9,3,16)=1.
  Each adapted Z carries derived-from provenance to
  its source(s); Z_conc points at the pattern MAP mP.

Falsifiers (in-Zag, any one fires => verdict FAIL):
F-EDGE-NEW (any arm with an edge type outside
{14,16}); F-COUNT (any FULL-arm as/ae deviating from
section 5); F-NO-GROUND-* (any reuse query via != its
section-1 Z id); F-WRONG-Z* (any d_check_* != 1);
F-PIPE-HIT-* (any reuse query phit != 0); F-NOREUSE-*
/F-FRESH-* (any reuse val != -2); F-ABLATE* (ablated
query val != -2, or a surviving query val wrong, or
t16 wrong); F-RE-*-ENTERED/VIA/VAL (any re-ask with
MR_ENTERED != 0, wrong via, or wrong val);
F-OP-* (committed op != query index); F-TRIES-*
(tries != query index); F-T16-COUNT; F-NO-T16-*;
F-NO-LINK14-*; F-SRC-A (qc_asrc != 1); F-DISTR-SURVIVES
(mD not live at FULL end).

## 5. Hand-derived counts (N=44 facts; F-COUNT bars the FULL-arm values)

Notation: find(s,r)=F means ex_find_subrel(s,r) costs
F ticks (first matching fid +1, or 44 on no match).
Foldwalk costs are sums of their find calls. All six
FULL-arm queries end ae=2 (buildwin chain_exec verify +
deliver m_exec).

QCOMB (90,86,42), nm=4: as=333, ae=2.
  2 (agg search: id0 SKIP, id1 MATCH)
+ 4 (partner collection: id0 PCAP, id1 SKIP, id2 PCAP,
  id3 SKIP)
+ 74 (mD,b=1: entry fid8=9 + foldwalk(91,3)=10+11+44=65,
  head SHAPE-FAIL, no tail)
+ 44 (mD,b=2: find(90,6) no match)
+ 74 (mB0,b=1: as mD,b=1)
+ 19 (mB0,b=2 head: find(90,7)=9, find(91,7)=10)
+ 116 (mB0,b=2 tail: entry fid10=11 +
  foldwalk(80,3)=12+13+14+15+16+17=87, term=86 +
  valof(86,2)=find(86,2)=18, vv=42 VERIFY-OK)
= 2+4+74+44+74+19+116 = 333.

QSUB (200,43,11), nm=5: as=335, ae=2.
  2 (agg) + 5 (partner)
+ 84 (mD,b=1: entry fid18=19 + foldwalk(40,3)=1+2+3+4+5+6
  =21 SHAPE-OK term=43 + tail find(43,6)=44 FAIL)
+ 44 (mD,b=2: find(200,6) no match)
+ 84 (mB0,b=1) + 44 (mB0,b=2: find(200,7) no match)
  = 256 op-1
+ 72 (op-2: candidates 44, cand fid18 foldwalk(40,3)=21
  SHAPE-OK term=43, valof(43,2)=find(43,2)=7, vv=11
  VERIFY-OK)
= 2+5+256+72 = 335.

QTRUNC (100,42,32), nm=6: as=368, ae=2.
  2 (agg) + 6 (partner)
+ 73 (mD,b=1: entry fid7=8 + foldwalk(40,3)=21 SHAPE-OK
  term=43 + tail find(43,6)=44 FAIL)
+ 44 (mD,b=2) + 73 (mB0,b=1) + 44 (mB0,b=2) = 234 op-1
+ 88 (op-2: candidates 44; cand fid20 (100,2,50):
  foldwalk(50,3): f1 no match=44 SHAPE-FAIL)
+ 38 (op-3: nf2=2: entry fid7=8 + foldwalk(40,2)=1+2+3+4
  =10 term=42 + valof(42,2)=find(42,2)=20, vv=32
  VERIFY-OK; nf2=1 not attempted, first verifying
  nf2 wins)
= 2+6+234+88+38 = 368.

QINV (120,127,60), nm=7: as=1142, ae=2.
  2 (agg) + 7 (partner)
+ 185 (mD,b=1: entry fid20=21 + foldwalk(121,3)=
  22+23+24+25+26+44=164 SHAPE-FAIL on g2=find(126,6)
  no match; head fails)
+ 134 (mD,b=2: head find(120,6)=21 -> 121; tail
  agg_seg(121,3,final=1): entry fid21=22 +
  foldwalk(122,3)=23+24+44=91 SHAPE-FAIL on
  g1=find(124,5); b=2 FAIL)
+ 185 (mB0,b=1) + 44 (mB0,b=2: find(120,7) no match)
  = 548 op-1
+ 208 (op-2: candidates 44; cand fid20 foldwalk(121,3)
  =164 SHAPE-FAIL)
+ 181 (op-3: nf2=2: entry 21 + foldwalk(121,2)=
  22+23+24+25=94 term=125 VERIFY-FAIL =115; nf2=1:
  entry 21 + foldwalk(121,1)=22+23=45 term=123
  VERIFY-FAIL =66)
+ 196 (op-4 INVERT: reversed rels [6,5,6,5,6,5,18]
  strict walk find(120,6)=21, find(121,5)=22,
  find(122,6)=23, find(123,5)=24, find(124,6)=25,
  find(125,5)=26, find(126,18)=27 =168, cur=127==t;
  valof(127,2)=find(127,2)=28, vv=60 VERIFY-OK)
= 2+7+548+208+181+196 = 1142.

QABS (150,166,77), nm=8: as=1242, ae=2.
  2 (agg) + 8 (partner)
+ 268 (mD,b=1: entry fid28=29 + foldwalk(160,3)=
  30+31+32+33+34+35=195 SHAPE-OK term=166 + tail
  find(166,6)=44 FAIL)
+ 44 (mD,b=2: find(150,6) no match)
+ 268 (mB0,b=1) + 44 (mB0,b=2) = 624 op-1
+ 44 (op-2: candidates 44, no rel!=18 entry from 150)
+ 245 (op-3: nf2=2: entry 29 + foldwalk(160,2)=
  30+31+32+33=126 term=164 VERIFY-FAIL =155; nf2=1:
  entry 29 + 30+31=61 term=162 VERIFY-FAIL =90)
+ 44 (op-4: find(150,6) no match)
+ 275 (op-5 ABSTRACT: candidates 44; cand fid28
  (150,18,160): foldwalk(160,3)=195 SHAPE-OK term=166;
  valof(166,2)=find(166,2)=36, vv=77 VERIFY-OK)
= 2+8+624+44+245+44+275 = 1242.

QCONC (210,234,91), nm=9: as=1102, ae=2.
  2 (agg) + 9 (partner)
+ 81 (mD,b=1: entry fid36=37 + foldwalk(220,3):
  f1=find(220,2) no match=44 SHAPE-FAIL; head fails)
+ 44 (mD,b=2) + 81 (mB0,b=1) + 44 (mB0,b=2) = 250 op-1
+ 250 (op-2: candidates 44; cand fid37 (210,38,230):
  foldwalk(230,3)=39+40+41+42+44=206 SHAPE-FAIL on
  g1=find(234,11))
+ 162 (op-3: nf2=2: entry 37 + foldwalk(220,2)=44
  SHAPE-FAIL =81; nf2=1: =81)
+ 44 (op-4: find(210,6) no match)
+ 88 (op-5: candidates 44; cand fid36 (210,18,220):
  foldwalk(220,3)=44 SHAPE-FAIL)
+ 297 (op-6 CONCRETIZE: pattern search 4 ticks
  (id0 SKIP, id1 de!=0 SKIP, id2 SKIP, id3 MATCH);
  candidates 44; cand fid36: foldwalk(220,2)=44
  SHAPE-FAIL; cand fid37: foldwalk(230,2)=
  39+40+41+42=162 SHAPE-OK term=234, folds (11,12)
  != (5,6) novel OK; valof(234,2)=find(234,2)=43,
  vv=91 VERIFY-OK)
= 2+9+250+250+162+44+88+297 = 1102.

Ablation-arm informational counts (ablated query only;
not kill-barred, reported for transparency):
- ABLATE-COMBINE QCOMB as=416:
  2 + 109 (op2: 44+65) + 104 (op3: 74+30) + 44 (op4)
  + 44 (op5) + 113 (op6: 4+44+65).
- ABLATE-SUBST QSUB as=460:
  2+5+256 (op1) + 51 (op3: 29+22) + 44 (op4) + 44 (op5)
  + 58 (op6: 4+44+10, folds (5,6) not novel).
- ABLATE-TRUNC QTRUNC as=541:
  2+6+234 (op1) + 88 (op2) + 44 (op4) + 65 (op5:
  44+21, term 43!=42) + 102 (op6: 4+44+10+44, first
  cand folds not novel, second SHAPE-FAIL).
- ABLATE-INV QINV as=1132:
  2+7+548 (op1) + 208 (op2) + 181 (op3) + 44 (op5)
  + 142 (op6: 4+44+94, folds (5,6) not novel).
- ABLATE-ABS QABS as=1141:
  2+8+624 (op1) + 44 (op2) + 245 (op3) + 44 (op4)
  + 174 (op6: 4+44+126, folds (8,9) novel but term
  164!=166).
- ABLATE-CONC QCONC as=805:
  2+9+250 (op1) + 250 (op2) + 162 (op3) + 44 (op4)
  + 88 (op5).

F-COUNT bars (in-Zag falsifiers): QC-AS=333, QC-AE=2;
QS-AS=335, QS-AE=2; QT-AS=368, QT-AE=2; QV-AS=1142,
QV-AE=2; QE-AS=1242, QE-AE=2; QN-AS=1102, QN-AE=2.
