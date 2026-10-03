# PREREG: L2-METAREUSE (learner-selected reuse operator)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l2_adaptive_reuse/` only.
Worker: L2-ADAPTIVE-REUSE subagent (depth 2/2), 2026-10-03.
Parent mandate: push L2 adaptive reuse beyond the completed
matrix (SUBSTITUTE/TRUNCATE/EXTEND/SPECIALIZE, all PASS) and
the L2-COMBINE-XDOMAIN wave (PASS). This wave tests
L2-METAREUSE: the learner holds THREE reuse operators and
selects WHICH one to apply per query by trial verification.
The driver never assigns an operator to a query. Parent kill
bars K1-K8 govern.

## 1. What is being tested

Whether a learner holding (X) an arithmetic aggregation MAP
mA learned in an arithmetic episode (entry + 3 fold pairs,
7 hops), (Y) a planning ROUTE MAP mB0 learned in a planning
episode, and (D) a distractor ROUTE MAP mD, when faced with
THREE reuse queries on one world family, selects a DIFFERENT
reuse operator for each query by trial verification under one
fixed generic operator order, with no operator named by the
driver:

- Q_COMB (90,86,42,AGG,B): solvable only by COMBINE (mA +
  mB0, partner-head/AGG-tail binding b=2; the established
  cross-domain combination scenario).
- Q_SUB (200,43,11,AGG,A): solvable only by SUBSTITUTE
  (entry-relation substitution on mA: entry 18 -> 19, same
  fold structure, verified by execution).
- Q_TRUNC (100,42,32,AGG,A): solvable only by TRUNCATE
  (prefix truncation of mA to 2 fold pairs, verified by
  execution).

The operator enumeration order is fixed and generic:
[1=COMBINE, 2=SUBSTITUTE, 3=TRUNCATE]; the FIRST operator
whose full grounding executes to the query terminal with the
required value is committed. OP_MASK (driver-set
causal-control flag, one value per ARM, never per query,
never written by the learner) gates which operators may be
tried: bit0=COMBINE, bit1=SUBSTITUTE, bit2=TRUNCATE, tested
via (mask/n)%2 arithmetic, no bitwise ops.

The load-bearing discrimination: the SAME fixed order and
the SAME mask (7) yield DIFFERENT committed operators on
different queries (1, 2, 3). Position-in-order cannot explain
this (it predicts op 1 always commits); Q_SUB skipping op 1
and Q_TRUNC skipping ops 1-2 proves verification against
world facts decides. The ablation arms prove each operator is
necessary for its query: with op N masked out, query N fails
while the other two still pass.

Concrete scenario (all ids frozen). World facts (20):
  0:(40,5,30) 1:(30,6,41) 2:(41,5,31) 3:(31,6,42)
  4:(42,5,32) 5:(32,6,43)
  6:(43,2,11) 7:(100,18,40)
  8:(90,7,91) 9:(91,7,92) 10:(92,17,80) 11:(80,15,81)
  12:(81,16,82) 13:(82,15,83) 14:(83,16,84) 15:(84,15,85)
  16:(85,16,86) 17:(86,2,42)
  18:(200,19,40)   <- alternate entry into the fold chain
  19:(42,2,32)     <- VAL fact for the truncated terminal
MAPs (taught in this order):
  mD id0: dom=A(1), cap=ROUTE(2), rels [6], facts [1],
    start 30, end 41 (distractor, taught first).
  mA id1 (X): dom=A(1), cap=AGG(1), rels
    [18,5,6,5,6,5,6], facts [7,0,1,2,3,4,5], start 100,
    end 43. Descriptor (generic extraction): entry=18,
    r1=5, r2=6, nf=3, valrel=2.
  mB0 id2 (Y): dom=B(2), cap=ROUTE(2), rels [7,7], facts
    [8,9], start 90, end 92.

Queries (driver-issued as (start, terminal, value, cap,
dom) plus one arm-level OP_MASK; no MAP id, no operator,
no source pair, no binding, no segment information):
  QA:       (100,43,11, AGG,A) -> via mA (X works at home)
  QB:       (90,92,-1, ROUTE,B) -> via mB0 (Y works at home)
  Q_COMB:   (90,86,42, AGG,B)  -> op 1 COMBINE, Z id 3
  Q_SUB:    (200,43,11, AGG,A) -> op 2 SUBSTITUTE, Z id 4
  Q_TRUNC:  (100,42,32, AGG,A) -> op 3 TRUNCATE, Z id 5
  Q_COMB-B: (90,86,42, AGG,B)  -> re-asked; via Z id 3,
            no meta phase (persistence + reuse)
  Q_SUB-B:  (200,43,11, AGG,A) -> via Z id 4, no meta phase
  Q_TRUNC-B:(100,42,32, AGG,A) -> via Z id 5, no meta phase

Adapted structures (built by the learner):
  Z_comb id3: rels [7,7,17,15,16,15,16,15,16], facts
    [8,9,10,11,12,13,14,15,16], start 90, end 86, dom=B,
    cap=AGG, descriptor (0,0,0,0,2). t16: 3->1, 3->2.
  Z_sub id4: rels [19,5,6,5,6,5,6], facts
    [18,0,1,2,3,4,5], start 200, end 43, dom=A, cap=AGG,
    descriptor (19,5,6,3,2) (entry/fold/valrel all
    discovered at runtime). t16: 4->1.
  Z_trunc id5: rels [18,5,6,5,6], facts [7,0,1,2,3],
    start 100, end 42, dom=A, cap=AGG, descriptor
    (18,5,6,2,2). t16: 5->1.

## 2. Frozen learner machinery (disclosed)

Standalone pure-Zag learner (learner.zag, mr_ prefix, MR-
trace tags) + environment side (world.zag: 20 frozen facts)
+ experiment side (driver.zag: teaching, seven arms, in-Zag
bar evaluation). The frozen TNN core is not used. Unfrozen
only; no frozen source touched.

State: one u8 buffer. Offsets: 0 NF, 1 NM, 2 NE,
3 reserved, 4 NN, 5 unused, 6 STALE_MAP, 7 STALE_HOP,
8 STALE_FACT, 9 LAST_VIA, 10 unused, 11 IN_MR, 12
MR_ENTERED. Facts: 38 x 8 bytes at 16..319
[sub,rel,obj,live,0,0,0,0]. MAPs: 16 x 40 bytes at
320..959 [tag=20,live,start,end,rlen,flen,reason,pad,
rels x12 @+8, facts x12 @+20, dom @+32, cap @+33, d_entry
@+34, d_r1 @+35, d_r2 @+36, d_nf @+37, d_valrel @+38, pad
@+39]. Edges: 64 x 4 bytes at 960..1215
[from,to,type,pad]. Answer nodes: 8 x 4 bytes at
1216..1247 [via,0,0,0]. Stats: SEARCH i32 @1248, EXEC
i32 @1252, A_SEARCH i32 @1256, A_EXEC i32 @1260.
LAST_VAL i32 @1264, AGG_SRC i32 @1268, ROUTE_SRC i32
@1272, BINDING i32 @1276, BIND_DECIDED i32 @1280,
BIND_TRIES i32 @1284 (binding attempts made), PIPE_HIT
i32 @1288, LAST_TERM i32 @1292, MR_OP i32 @1296 (chosen
operator for current query, -1 none), MR_OP_TRIES i32
@1300 (operator attempts made), MR_OP_DECIDED i32 @1304
(set ONLY in a committing branch), OP_MASK i32 @1308
(driver-set causal-control flag, never written by the
learner). Scratch at 1312+.

Edge-type semantics (reused, zero new types):
- type 16: derived-from. Z_comb: 3->1 AND 3->2. Z_sub:
  4->1. Z_trunc: 5->1.
- type 14 (LINK14): answer-node -> delivering MAP on
  deliver.
- No other edge types may appear.

Generic operations (frozen, relation-agnostic,
MAP-agnostic, domain-agnostic; no capability literal
except comparison against the query's own cap; no
operator literal except the fixed 1/2/3 enumeration
order):
- f_teach, m_teach (with generic AGG descriptor
  extraction), map_create, map_retire, m_exec,
  chain_exec, e_add, e_count, e_has, e_has_to, ex_eoth:
  as in the sibling combine lane.
- ex_find_sub_skip / ex_find_subrel / ex_valof: counted
  scans (frozen counting rules, section 3).
- ex_foldwalk(st,u,k,vrel,ff): as in the combine lane.
- mr_agg_seg(st,ob,atp,s,k,vrel,final,t,v,tr,tf): as the
  combine lane's cb_agg_seg (entry scan, k-fold walk
  with runtime relation discovery; final==1 requires
  term==t AND VAL(term,vrel)==v). MR- trace tags.
- mr_route_seg(st,s,rsrc,hr,hf): strict walk over the
  partner source's stored relseq rels from s.
- mr_buildwin(...): concatenate head+tail rels/facts,
  MR-ZBUILD print, chain_exec verify (must reach t),
  MR-VERIFY, map_create promote, e_add type-16 edges to
  the given source(s) (src2<0 means single-source),
  MR-PROMOTE, ex_deliver.
- mr_combine(st,ob,atp,s,t,v,qdom,qcap,agg_src): the
  combine lane's cb_combine logic verbatim (partner
  collection: first distinct live non-query cap in id
  order; fixed (partner-source, binding) enumeration:
  b=1 AGG-head/partner-tail, b=2 partner-head/AGG-tail;
  first verifying combination wins). Sets AGG_SRC,
  ROUTE_SRC, BINDING, BIND_DECIDED (only in the
  verifying branch), BIND_TRIES. MR- trace tags.
- mr_substitute(st,ob,atp,s,t,v,qdom,qcap,agg_src):
  entry-relation substitution. Prints MR-SRC-SUB with
  the source descriptor. Collects entry candidates: all
  live facts with sub==s and rel != d_entry (fid order,
  every fid ticked). For each candidate (fid f, rel r,
  obj u): MR-SUB-CAND print; ex_foldwalk from u with
  k=d_nf and runtime (s1,s2) discovery; SHAPE-FAIL ends
  the candidate; on shape OK require term==t AND
  VAL(term,d_valrel)==v (VERIFY-OK/FAIL print); on
  VERIFY-OK build Z as rels=[r,s1,s2,...] (alternating
  discovered s1/s2) and facts=[f, ff...], then
  mr_buildwin with single-source provenance to agg_src
  and descriptor (r,s1,s2,d_nf,d_valrel). First
  verifying candidate wins; the enumeration stops.
- mr_truncate(st,ob,atp,s,t,v,qdom,qcap,agg_src):
  prefix truncation. Prints MR-SRC-TRUNC. For nf2 in
  {d_nf-1, ..., 1} descending: MR-TRUNC-TRY print;
  mr_agg_seg(s, k=nf2, final=1, t, v); on success build
  Z from the discovered segment rels/facts, then
  mr_buildwin with single-source provenance to agg_src
  and descriptor (re,s1,s2,nf2,d_valrel). First
  verifying nf2 wins; the enumeration stops.
- mr_adapt(st,ob,atp,s,t,v,qdom,qcap,agg_src,op_mask):
  fixed operator enumeration. For op in [1,2,3]: if the
  op's mask bit ((mask/n)%2, n=1,2,4) is 0, print
  MR-OP-SKIP and continue; else MR_OP_TRIES++,
...[truncated 12582 chars]
