# PREREG: L2 TRUNCATE-XDOMAIN (cross-domain truncate, learner-chosen cut point)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l2_truncate_xdomain/` only.
Worker: L2 Adaptive Reuse subagent (depth 2/2), 2026-10-02.
Parent mandate: test L2 TRUNCATE with cross-domain transfer: a
learned procedure from one domain is truncated (shortened) and
applied to a different domain where the full procedure would be
too long. Parent kill bars K1-K8 govern.

## 1. What is being tested

Whether a learner holding (X) an arithmetic aggregation MAP mA
learned in an arithmetic episode (entry + 4 fold pairs, 9 hops)
and (Y) a planning ROUTE MAP mB0 learned in a planning episode,
when asked for an aggregation in the planning domain whose
grounding chain is SHORTER than X (entry + 3 fold pairs, 7 hops),
(1) searches its MAP inventory by capability signature across
domains, examining and rejecting a distractor MAP, (2) attempts
the FULL X grounded in the target domain and records its failure
(the 4th fold has no grounding: the walk dead-ends), (3) runs a
generic longest-verifying-prefix enumeration over strict prefixes
of X (k = nf-1 down to 1), committing to the first prefix whose
target-domain grounding executes to the query terminal with the
required value, (4) promotes the truncated Z with derived-from
(type-16) provenance to X, and (5) answers later queries through
Z with no re-truncation. The cut point k=3 is chosen by the
learner's enumeration policy, never passed by the driver: the
driver issues Q2 as (start, terminal, value, cap, dom) with no
length, no MAP id, no relation.

Concrete scenario (all ids frozen):

Domain A (arithmetic aggregation), facts:
  0:(40,5,30) 1:(30,6,41) 2:(41,5,31) 3:(31,6,42)
  4:(42,5,32) 5:(32,6,43) 6:(43,5,33) 7:(33,6,44)
  8:(44,2,12) 9:(100,18,40)
  rel 5/6 = fold pair, rel 18 = entry, rel 2 = VAL.
  mA (id 1): dom=A(1), cap=AGG(1),
  relseq [18,5,6,5,6,5,6,5,6], facts [9,0,1,2,3,4,5,6,7],
  start 100, end 44.
  Descriptor (extracted generically at teach time, never
  hardcoded): entry=18, r1=5, r2=6, nf=4, valrel=2.

Domain B (planning), facts:
  10:(50,17,70) 11:(70,15,60) 12:(60,16,71) 13:(71,15,61)
  14:(61,16,72) 15:(72,15,62) 16:(62,16,73) 17:(73,2,75)
  18:(50,7,51) 19:(51,7,52)
  rel 15/16 = fold pair, rel 17 = entry, rel 2 = VAL,
  rel 7 = route.
  mB0 (id 2): dom=B(2), cap=ROUTE(2), relseq [7,7],
  facts [18,19], start 50, end 52.
  mD (id 0, distractor): dom=A(1), cap=ROUTE(2), relseq [6],
  facts [1], start 30, end 41. Taught FIRST so it sorts
  before mA; the capability search must examine and reject it.

Queries (driver-issued, no MAP id, no length ever passed):
  QA:  (100,44,12, cap=AGG, dom=A) -> via mA (X works at home)
  QB:  (50,52,-1, cap=ROUTE, dom=B) -> via mB0 (Y works at home)
  Q2:  (50,73,75, cap=AGG, dom=B)  -> pipeline fails (no B AGG
         MAP); TRUNCATE builds Z with learner-chosen k=3.
  Q2B: (50,73,75, cap=AGG, dom=B)  -> re-asked; must go via Z
         with no trunc phase (persistence + reuse).

Z (built by the learner, id 3): relseq [17,15,16,15,16,15,16],
facts [10,11,12,13,14,15,16], start 50, end 73, dom=B,
cap=AGG, descriptor (17,15,16,3,2). Walk: 50-17->70-15->60
-16->71-15->61-16->72-15->62-16->73. Terminal VAL 75.

## 2. Frozen learner machinery (disclosed)

Standalone pure-Zag learner (learner.zag, tx_ prefix, TX- trace
tags) + environment side (world.zag: 20-fact table) +
experiment side (driver.zag: teaching, four arms, in-Zag bar
evaluation). The frozen TNN core is not used. Unfrozen only; no
frozen source touched.

State: one u8 buffer. Offsets: 0 NF, 1 NM, 2 NE, 3 TRUNC_ON
(driver-set causal-control flag, never written by the learner),
4 NN, 5 unused, 6 STALE_MAP, 7 STALE_HOP, 8 STALE_FACT,
9 LAST_VIA, 10 unused, 11 IN_TRUNC, 12 TR_ENTERED,
13 SRC_ID (255=none).
Facts: 38 x 8 bytes at 16..319 [sub,rel,obj,live,0,0,0,0].
MAPs: 16 x 40 bytes at 320..959 [tag=20,live,start,end,rlen,
flen,reason,pad, rels x12 @+8, facts x12 @+20, dom @+32,
cap @+33, d_entry @+34, d_r1 @+35, d_r2 @+36, d_nf @+37,
d_valrel @+38, pad @+39]. (40-byte rows: the source X has a
9-rel relseq, which does not fit the sibling lane's 8-rel
rows; this lane's layout is its own.)
Edges: 64 x 4 bytes at 960..1215 [from,to,type,pad].
Answer nodes: 8 x 4 bytes at 1216..1247 [via,0,0,0].
Stats: SEARCH i32 @1248, EXEC i32 @1252, A_SEARCH i32 @1256,
A_EXEC i32 @1260. LAST_VAL i32 @1264, SRC_ID32 @1268,
LAST_TERM i32 @1272, TRUNC_K i32 @1276, FULL_OK i32 @1280,
TRUNC_DECIDED i32 @1284. Scratch at 1288+.

Edge-type semantics (reused, zero new types):
- type 16: derived-from. At Z promotion: 3->1 (X is the
  truncation source).
- type 14 (LINK14): answer-node -> delivering MAP on deliver.
- No other edge types may appear.

Generic operations (frozen, relation-agnostic, MAP-agnostic,
domain-agnostic):
- f_teach(sub,rel,obj): observe a world fact.
- m_teach(rs,rl,fs,fl,start,end,dom,cap): learn a MAP (facts
  must be live and rel-matching; rl,fl <= 12). If cap==AGG,
  extract the interface descriptor generically: d_entry=
  rels[0], d_r1=rels[1], d_r2=rels[2], require rels[1..] to
  alternate (r1,r2) with (rlen-1) even and >= 2, d_nf=
  (rlen-1)/2, d_valrel = rel of the first live fact (fid
  order) with sub==end. No rel literal anywhere in this
  procedure.
- m_exec / chain_exec: hop walk with licensing checks.
- tx_foldwalk(st,u,k,vrel,ff): from entry node u, walk k
  alternating folds. Fold 1 discovers (s1,s2) as rels of the
  first live facts with sub==u then sub==a0 (skipping
  vrel-annotated facts); folds 2..k require rel==s1 /
  rel==s2. Fills ff[0..2k) fact ids. Returns 0 on fail,
  else s1 + s2*256 + term*65536.
- tx_try_len(st,ob,atp,s,t,v,k,vrel,...): entry scan over
  fids ascending; for each live fact with sub==s, run
  tx_foldwalk with k folds; on shape success require
  term==t AND tx_valof(term,vrel)==v. First verifying
  grounding is committed (first-match precedent); the scan
  stops. Returns the pack or 0. Prints TX-ENTRY-CAND lines.
- tx_truncate(st,ob,atp,s,t,v,dom,smid,trunc_on):
  1. read descriptor (entry,r1,r2,nf,valrel) from sm; print
     TX-SRC. Set SRC_ID32=smid.
  2. k=nf (the FULL X): TX-TRY k=nf; tx_try_len. If it
     verifies: FULL_OK=1, build/promote/verify/deliver
     (a full copy; cannot happen in this world; caught by
     F-FULL-OK). If it fails: TX-FAIL k=nf, TX-FULL-FAIL,
     FULL_OK=0.
  3. if trunc_on==1: for k=nf-1 down to 1 (longest-first):
     TX-TRY k; tx_try_len; first verifying k wins: TX-OK
     k, TRUNC_K=k, TRUNC_DECIDED=1 (set ONLY in this
     branch), build Z (rels=[re,s1,s2,...], facts=
     [entry_fid, fold fids...], start=s, end=term),
     TX-ZBUILD, verify by chain_exec (must reach t),
     TX-VERIFY, promote Z via map_create, e_add(Z,sm,16),
     TX-PROMOTE, deliver through Z.
  4. if trunc_on==0 the enumeration is skipped: full-only
     attempt, then failure.
- tx_query(s,t,v,cap,dom,trunc_on): pipeline over live MAPs
  in id order from s; first terminal==t delivers (value read
  through the MAP's stored d_valrel; skipped when 0). Else
  trunc phase (IN_TRUNC=1, A_* reset, TR_ENTERED=1):
  TX-QUERY print; capsearch: first live MAP (id order)
  with cap==qcap (any domain), printing TX-SEARCH
  id/cap SKIP/MATCH (the distractor mD is examined and
  rejected here); then tx_truncate. No rebuild fallback:
  without a capability-matching learned structure the
  query fails with ans=-2.

## 3. Frozen cost-counting rules

- A_SEARCH += 1 per fact id examined in any learner scan
  loop (entry scan, fold first/rel-match scans, VALscans).
- A_SEARCH += 1 per MAP header examined in any learner MAP
  scan loop (capseearch).
- A_EXEC += 1 per m_exec/chain_exec call while
  IN_TRUNC==1.
- A_SEARCH/A_EXEC reset at trunc-phase entry; IN_TRUNC=0
  outside the trunc phase. Global SEARCH/EXEC count always
  (informational).

## 4. Frozen arms and hand-derived expectations

Phase 0 (all arms except FRESH): teach facts 0..19; m_teach
mD(0), mA(1), mB0(2). QA -> term 44 val 12 via 1. QB ->
term 52 val -1 via 2.

- ARM-FULL (trunc_on=1): Q2. Pipeline: mD/mA clean fail
  from 50, mB0 -> 52 != 73. Trunc phase:
  capsearch: id0 SKIP (cap 2), id1 MATCH (cap 1) (A=2);
  trace TX-SEARCH id=0 cap=2 SKIP / id=1 cap=1 MATCH.
  descriptor: entry=18 r1=5 r2=6 nf=4 valrel=2;
  trace TX-SRC id=1 entry=18 r1=5 r2=6 nf=4 valrel=2.
  k=4 (FULL X): entry scan fids 0..19 (A=20):
   fid 10 (50,17,70): foldwalk: f1 sub==70 skip rel 2:
     0..11=12 (s1=15); f2 sub==60: 0..12=13 (s2=16);
     fold2 (71,15): 0..13=14, (61,16): 0..14=15;
     fold3 (72,15): 0..15=16, (62,16): 0..16=17;
     fold4 (73,15): 0..19=20 FAIL (rel 2 at fid 17).
     (107) trace TX-ENTRY-CAND r=17 u=70 FAIL-SHAPE.
   fid 18 (50,7,51): f1 sub==51: 0..19=20 (s1=7);
     f2 sub==52: 0..19=20 FAIL. (40)
     trace TX-ENTRY-CAND r=7 u=51 FAIL-SHAPE.
   k=4 total 20+107+40=167. trace TX-FAIL k=4 /
   TX-FULL-FAIL. FULL_OK=0.
  k=3: TX-TRY k=3; entry scan fids 0..10 (A=11, stops at
   first verifying candidate):
   fid 10: foldwalk k=3: 12+13+14+15+16+17=87, term=73;
    trace TX-ENTRY-CAND r=17 u=70 SHAPE-OK term=73;
    VALscan (2,73): 0..17=18, v=75==75 VERIFY-OK. (116)
   trace TX-OK k=3. TRUNC_K=3, TRUNC_DECIDED=1.
  TX-ZBUILD rels=17,15,16,15,16,15,16
    facts=10,11,12,13,14,15,16.
  verify: chain_exec -> 73 (E=1); TX-VERIFY term=73 OK.
  promote Z id 3; t16 3->1; TX-PROMOTE z=3 t16=3->1;
  LINK14 ans42->3; deliver exec (E=2).
  Frozen: ANS term=73 val=75 via=3; A_SEARCH=285;
  A_EXEC=2; t16=1 {3->1}; e_has_to(3,14)=1; no edge type
  outside {14,16}; Z: id 3, rlen 7, rels
  [17,15,16,15,16,15,16], facts [10,11,12,13,14,15,16],
  start 50, end 73, dom 2, cap 1, live 1, descriptor
  (17,15,16,3,2); SRC_ID32=1; FULL_OK=0; TRUNC_K=3;
  TRUNC_DECIDED=1.
  A_SEARCH derivation: 2 + 167 + 116 = 285.
  A_EXEC: verify + deliver = 2.
  Q2B: pipeline mD/mA fail, mB0 -> 52, Z -> 73 val 75.
  Frozen: ANS term=73 val=75 via=3, TR_ENTERED=0,
  Z live=1.
- ARM-NOTRUNC (trunc_on=0): as FULL through the k=4
  attempt (A=2+167=169 informational); enumeration
  skipped; ans=-2. Frozen: ANS term=-2 val=-2 via=-1;
  t16=0; NM=3. (Proves the full-X-only operator cannot
  solve Q2: truncation is REQUIRED.)
- ARM-ABLATE-X (trunc_on=1, mA retired reason 3 pre-Q2):
  pipeline fails; capsearch id0/id1(retired)/id2 all SKIP
  (A=3 informational); no source; ans=-2. Frozen: ANS
  term=-2 val=-2 via=-1; t16=0; NM=3.
- ARM-FRESH (trunc_on=1, facts only, no MAPs): pipeline
  empty; capsearch empty; ans=-2. Frozen: ANS term=-2
  val=-2 via=-1; t16=0; NM=0.

## 5. Kill bars (frozen)

- K1 (X and Y exist before the truncation task, learned
  independently): in-Zag: qa_via==1 AND qb_via==2 AND
  q2_via==3 AND every rel of mA in {18,5,6} AND every rel
  of mB0 == 7 (disjoint relation sets: no shared
  vocabulary between source procedure and target-domain
  native MAP). Shell: output line number of `Q QA` <
  `Q QB` < `Q Q2`.
- K2 (full X fails on target; truncation REQUIRED):
  in-Zag: FULL_OK==0 AND na_val==-2 AND na_t16==0 (the
  full-X grounding fails AND the no-truncate control arm
  fails the same query). Shell (verbatim grep -F on
  run1): `TX-FULL-FAIL`.
- K3 (learner decides the truncation point, not the
  researcher): in-Zag: TRUNC_K==3 AND TRUNC_DECIDED==1
  (the flag is set only inside the learner's descending
  enumeration branch). Shell (verbatim): `TX-TRY k=4`,
  `TX-FAIL k=4`, `TX-TRY k=3`, `TX-OK k=3` all present in
  run1, in that order; and `grep -c` of `trunc_k\|TRUNC_K`
  in driver.zag == 0 (the driver never names a length;
  tx_query takes no length parameter, only the TRUNC_ON
  causal-control flag).
- K4 (truncated version succeeds where full fails):
  in-Zag: q2_via==3 AND q2_val==75 AND FULL_OK==0.
  Shell (verbatim): `TX-ZBUILD rels=17,15,16,15,16,15,16
  facts=10,11,12,13,14,15,16`, `ANS term=73 val=75 via=3`.
- K5 (determinism): 3/3 runs byte-identical (sha256 equal).
- K6 (no domain-pair template in source): 12 frozen grep
  patterns return 0 hits on learner.zag (section 6).
- K7 (ablation: no X fails): in-Zag: ax_val==-2 AND
  ax_t16==0 AND ax_nm==3 (with mA retired, the trunc
  phase finds no capability-matching source and the
  query fails; nothing is promoted).
- K8 (truncated form persists and is reused): in-Zag:
  q2b_via==3 AND q2b_val==75 AND q2b_adapt==0 AND Z
  live==1 (second query served from the persisted
  truncated structure, no re-truncation).

Verdict L2-TRUNCATE-XDOMAIN-PASS iff K1-K8 all PASS, no
falsifier fires, F-COUNT silent.

## 6. Frozen K6 grep audit spec (run on learner.zag)

Each pattern must return zero matches (grep -c == 0):
1. `5,6,5,6` (mA's fold relseq must not be in the learner)
2. `18,5,6,5,6` (mA's full relseq head must not be there)
3. `17,15,16,15,16,15,16` (Z's relseq must not be there)
4. `10,11,12,13,14,15,16` (Z's fact list must not be there)
5. `(50,17,70)` (B entry fact literal; world data stays out)
6. `(70,15,60)` (B chain fact literal)
7. `(73,2,75)` (B terminal VAL fact literal)
8. `73,75` (query target pair must not be there)
9. `_MODE` (zero modes)
10. `bridge` (case-insensitive; no bridge handlers)
11. `python` (case-insensitive; pure Zag)
12. `as *i32` (the pinned-znc miscompile pattern; u8 cells
    + get32/set32 only)

## 7. Frozen falsifiers

- F-NO-GROUND: FULL q2_via != 3.
- F-WRONG-Z: promoted Z header/rels/facts/(start,end)/
  (dom,cap)/descriptor != frozen section 4 values.
- F-FULL-OK: FULL_OK != 0 (the full X must fail on B).
- F-NOTRUNC-PASS: NOTRUNC ans != -2.
- F-ABLX-PASS: ABLATE-X ans != -2 OR t16 != 0.
- F-FRESH-PASS: FRESH ans != -2.
- F-Q2B-RE: Q2B TR_ENTERED != 0 or via != 3.
- F-T16-COUNT: FULL t16 != 1.
- F-NO-T16-SRC: e_has(3,1,16) != 1.
- F-EDGE-NEW: any edge with type outside {14,16}, any arm.
- F-COUNT: FULL A_SEARCH != 285 or A_EXEC != 2
  (implementation must match the frozen counting rules
  exactly; a pure arithmetic slip in this prereg's hand
  derivation may be transparently amended pre-verdict,
  an algorithmic counting change may not).
- F-AUDIT / F-NONDET / F-PYTHON: as in prior waves; any
  fires voids the build.

## 8. Determinism spec

No RNG. MAP-id order, fid-ascending scans, first-match
rules, longest-first prefix enumeration everywhere. Output
via one preallocated buffer and a single raw-syscall write
loop (the pinned-znc stdout workaround). 3/3 byte-identical
required.

## 9. Disclosed residual footprint and non-claims

- The cross-domain TRUNCATE operator, descriptor
  extraction, entry/fold search with runtime relation
  discovery, longest-verifying-prefix enumeration, and
  cost counters are researcher-supplied generic machinery,
  frozen here. None names a relation, MAP, domain, length,
  or domain pair. The L2 claim is narrow: a planning query
  with no native aggregation is served by a strict prefix
  of a learner-selected arithmetic aggregation structure,
  where the full structure provably fails to ground, the
  cut point is chosen by the learner's longest-first
  verification policy, and the truncated form is verified
  by execution, persists, and is reused.
- TRUNC_ON is a driver-set causal-control flag (the
  composition_l2 adapt_on precedent), never written by the
  learner. It enables the lesion comparison; it is not a
  runtime mode.
- One world family (arithmetic aggregation x plan-cost
  aggregation). No generality claim beyond the four arms.
  The world is builder-designed, not adversary-designed.
  Sealed-adversary generality is open future work.
- 0 modes, 0 bridges, 0 handlers, 0 new edge types, 0 new
  opcodes, 0 new semantic cases. Pure Zag, safebin
  toolchain, zero forbidden executables.
- No em/en dashes in loop documentation. Paper untouched.
  Nothing pushed. Commits local with explicit pathspec.
- Unfrozen only: no frozen source touched. The frozen TNN
  core is not used here; this is a standalone
  learner-mechanism experiment in the chain family.
