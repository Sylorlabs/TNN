# PREREG: L2 SUBSTITUTE-XDOMAIN (cross-domain substitute with interface adaptation)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l2_substitute_xdomain/` only.
Worker: L2 Adaptive Reuse subagent (depth 2/2), 2026-10-02.
Parent mandate: L2 ADAPTIVE REUSE is top priority; the L2 operation
matrix (extend, truncate, specialize, substitute, interface-adapt)
is complete at L1/within-domain. This lane pushes SUBSTITUTE across
domains with PARTIAL INTERFACE MISMATCH: the source structure comes
from arithmetic (SUM) and is substituted into a planning procedure
where arity, parameter (relation) names, and value ranges all
differ. The learner must ADAPT the interface, not copy.

Predecessor: `l2_substitute/` (verdict L2-SUBSTITUTE-COMPLETE) did
within-domain substitution of a dead middle segment, triggered by a
fact kill. Its stated open future work was exactly this lane:
"Cross-domain substitution and substitution with interface
adaptation (endpoints not exactly matching) are open future work."
The trigger here is different on purpose: no fact dies; the
planning domain simply LACKS an aggregation capability, and the
learner must reach across domains to borrow and adapt one.

## 1. What is being tested

Whether a learner holding (X) an arithmetic SUM MAP mA learned in
an arithmetic episode and (Y) a planning ROUTE MAP mB0 learned in a
planning episode, when asked for the TOTAL COST of a plan (a
capability no B-domain MAP has), (1) searches its own MAP inventory
by capability signature across domains, examining and rejecting a
distractor MAP, (2) selects mA by first-match in MAP-id order,
(3) derives mA's interface descriptor (entry hop + alternating
fold-pair + fold count + value-relation, all discovered at teach
time, never hardcoded), (4) searches B facts for a fold-chain
matching the descriptor shape under a runtime-derived relation
remap, (5) enforces B's pair interface (each addend must be
COST-linked from a plan step enumerated via mB0; addend values
read from B facts through the discovered value-relation),
rejecting a decoy chain that matches structurally but violates the
pair interface, (6) verifies the built Z by real execution to the
query target with terminal value check, (7) promotes Z with
adapted-from provenance to BOTH source structures, and (8) answers
later queries through Z. The substitution choice and every
interface mapping come from learner state, never from a
researcher-selected structure per problem. One generic operator;
no relation named, no MAP named, no domain pair named.

Concrete scenario (all ids frozen):

Domain A (arithmetic SUM), facts:
  0:(40,5,30) 1:(30,6,41) 2:(41,5,31) 3:(31,6,42) 4:(42,5,32)
  5:(32,6,43) 6:(30,2,3) 7:(31,2,4) 8:(32,2,5) 9:(43,2,12)
  10:(100,18,40)
  rel 5/6 = add-fold pair, rel 18 = list->initial-total entry,
  rel 2 = VAL. Addend values 3,4,5 (single-digit range).
  mA (id 1): dom=A(1), cap=AGG(1), relseq [18,5,6,5,6,5,6],
  facts [10,0,1,2,3,4,5], start 100, end 43.
  Descriptor (extracted generically at teach): entry=18, r1=5,
  r2=6, nf=3, valrel=2.

Domain B (planning), facts:
  11:(50,7,51) 12:(51,7,52)             [NEXTB plan chain]
  13:(50,8,60) 14:(51,8,61) 15:(52,8,62) [COST step->cost]
  16:(60,2,20) 17:(61,2,30) 18:(62,2,25) [VAL of costs]
  19:(50,17,64) 20:(50,17,70)            [entries: plan->chains]
  21:(70,15,60) 22:(60,16,71) 23:(71,15,61) 24:(61,16,72)
  25:(72,15,62) 26:(62,16,73)            [U add-chain]
  27:(73,2,75)                           [VAL of total]
  28:(64,15,74) 29:(74,16,65) 30:(65,15,75) 31:(75,16,66)
  32:(66,15,76) 33:(76,16,67)            [decoy add-chain]
  34:(74,2,1) 35:(75,2,2) 36:(76,2,3) 37:(67,2,6)
  Cost values 20,30,25 (two-digit range, disjoint from A's).
  mB0 (id 2): dom=B(2), cap=ROUTE(2), relseq [7,7],
  facts [11,12], start 50, end 52.
  mD (id 0, distractor): dom=A(1), cap=ROUTE(2), relseq [6],
  facts [1], start 30, end 41. Taught FIRST so it sorts before
  mA; the capability search must examine and reject it.

Interface mismatches (all load-bearing, none hardcoded):
  (a) parameter names: A fold rels (5,6) vs B fold rels (15,16);
      A entry rel 18 vs B entry rel 17.
  (b) arity: A's addends are bare VAL nodes; B's addends arrive
      through a (step, COST, cost) pair interface. The adapter
      discovers cost_rel=8 at runtime and requires every addend
      to be COST-linked from a plan step, with one uniform link
      rel across addends.
  (c) value ranges: A addends 3,4,5 vs B addends 20,30,25. The
      adapter reads B values through the discovered valrel and
      never consults A's range.

Queries (driver-issued, no MAP id ever passed):
  QA:  (100,43,12, cap=AGG, dom=A)  -> via mA (A-sum works)
  QB:  (50,52,-1, cap=ROUTE, dom=B) -> via mB0 (B-route works)
  Q2:  (50,73,75, cap=AGG, dom=B)   -> pipeline fails (no B AGG
         MAP); ADAPT builds Z.
  Q2B: (50,73,75, cap=AGG, dom=B)   -> re-asked; must go via Z
         with no adapt phase (persistence + reuse).

Z (built by the learner, id 3): relseq [17,15,16,15,16,15,16],
facts [20,21,22,23,24,25,26], start 50, end 73, dom=B, cap=AGG,
descriptor (17,15,16,3,valrel 2). Walk: 50-17->70-15->60-16->
71-15->61-16->72-15->62-16->73. Terminal VAL 75.

## 2. Frozen learner machinery (disclosed)

Standalone pure-Zag learner (learner.zag) + environment side
(world.zag: fact table + COST kill) + experiment side
(driver.zag: teaching, five arms, in-Zag bar evaluation).
The frozen TNN core is not used. Unfrozen only; no frozen
source touched.

State: one u8 buffer. Offsets: 0 NF, 1 NM, 2 NE, 3 ADAPT_ON
(driver-set causal-control flag, composition_l2 adapt_on
precedent, never written by the learner), 4 NN (answer nodes),
5 unused, 6 STALE_MAP, 7 STALE_HOP, 8 STALE_FACT, 9 LAST_VIA,
10 LAST_VAL, 11 IN_ADAPT, 12 ADAPT_ENTERED, 13 SRC_ID.
Facts: 38 x 8 bytes at 16..319 [sub,rel,obj,live,0,0,0,0].
MAPs: 16 x 32 bytes at 320..831 [tag=20,live,start,end,rlen,
flen,reason,pad, rels x8 @+8, facts x8 @+16, dom @+24, cap @+25,
d_entry @+26, d_r1 @+27, d_r2 @+28, d_nf @+29, d_valrel @+30,
pad @+31]. Edges: 64 x 4 bytes at 832..1087 [from,to,type,pad].
Answer nodes: 8 x 4 bytes at 1088..1119 [via,val,0,0].
Stats: SEARCH i32 @1120, EXEC i32 @1124, A_SEARCH i32 @1128,
A_EXEC i32 @1132. Scratch at 1136+.

Edge-type semantics (reused, zero new types):
- type 16: adapted-from. At Z promotion: 3->1 (structural
  source mA) and 3->2 (interface/step source mB0).
- type 15: co-use. On Q2 episode success: 1->2, 2->1
  (mechanism B convention: co-use written by episode success
  between distinct sources).
- type 14 (LINK14): answer-node -> delivering MAP on deliver.
- No other edge types may appear (F-EDGE-NEW).

Generic operations (frozen, relation-agnostic, MAP-agnostic,
domain-agnostic):
- f_teach(sub,rel,obj): observe a world fact.
- m_teach(rs,rl,fs,fl,start,end,dom,cap): learn a MAP (facts
  must be live and rel-matching). If cap==AGG, extract the
  interface descriptor generically: d_entry=rels[0],
  d_r1=rels[1], d_r2=rels[2], require rels[1..] to alternate
  (r1,r2) with (rlen-1) even and >= 2, d_nf=(rlen-1)/2,
  d_valrel = rel of the first live fact (fid order) with
  sub==end. No rel literal anywhere in this procedure.
- m_exec / chain_exec: hop walk with licensing checks
  (predecessor semantics).
- xa_collect(st,mid,start,buf): walk a MAP recording visited
  nodes (used for plan steps). Counts A_EXEC+=1 in adapt.
- xa_query(s,t,v,cap,dom,adapt_on): pipeline over live MAPs in
  id order from s; first terminal==t delivers. Else adapt
  phase (IN_ADAPT=1, A_* reset, ADAPT_ENTERED=1):
  1. steps: first live MAP (id order) with dom==qdom and
     start==s; xa_collect -> stepset. None -> stepset={s}
     (fallback, traced).
  2. capsearch: first live MAP (id order) with cap==qcap.
     None -> rebuild_fallback. (mD is examined and rejected
     here in FULL: SKIP then MATCH, traced.)
  3. adapter (source sm found):
     a. read descriptor (entry,r1,r2,nf,valrel) from sm.
     b. entry scan: fids ascending; for each LIVE fact
        (re,s,u): fold-walk: fold1 discovers (s1,s2) as rels
        of first live facts with sub==u then sub==a; folds
        2..nf require rel==s1 / rel==s2 (skipping
        non-matching fids). Fail -> next entry.
     c. arity check (skipped iff adapt_on==0): for each
        addend a (pair-middle nodes): VALscan (valrel,a,v)
        must hit (record v); LINKscan: first live fact
        (r,st,a) with st in stepset must hit; all addends'
        link rels must be equal (uniform interface; recorded
        as cost_rel). Fail -> next entry (continue scan).
     d. build Z: rels=[re,s1,s2,...], facts=[entry_fid,
        fold fids...], start=s, end=terminal. Record remap
        r1->s1, r2->s2, entry->re (traced).
     e. verify: chain_exec Z from s; terminal==t AND VALscan
        (valrel,terminal)==v required. Fail -> adapt fails
        (first accepted grounding is committed; no
        backtracking on verify failure: the
        composition_l2/l2_substitute first-match precedent).
     f. promote Z (id 3), t16 3->sm and 3->stepsMAP,
        deliver through Z, t15 between distinct sources.
  4. rebuild_fallback (generic, disclosed): BFS over live
     facts from s, L=1..7, fid-ascending extension order.
     For each walk with terminal==t: AGG shape check
     ([entry,(r1,r2)xk] on its relseq, k>=1), addend VALscans,
     arity LINKscans vs stepset; first full pass promotes a
     NATIVE MAP (no t16) and delivers. The honest blind
     from-scratch baseline: no learned structure guides it.

## 3. Frozen cost-counting rules

- A_SEARCH += 1 per fact id examined in any learner scan loop
  (entry scan, fold first/rel-match scans, VALscans,
  LINKscans, rebuild extension scans).
- A_SEARCH += 1 per MAP header examined in any learner MAP
  scan loop (steps-MAP search, capsearch).
- A_EXEC += 1 per m_exec/chain_exec/xa_collect call while
  IN_ADAPT==1.
- A_SEARCH/A_EXEC reset at adapt-phase entry; IN_ADAPT=0
  outside adapt. Global SEARCH/EXEC count always
  (informational).

## 4. Frozen arms and hand-derived expectations

Phase 0 (all arms except FRESH): teach facts 0..37; m_teach
mD(0), mA(1), mB0(2). QA -> term 43 val 12 via 1. QB ->
term 52 val -1 via 2.

- ARM-FULL (adapt_on=1): Q2. Pipeline: mD/mA clean fail from
  50, mB0 -> 52 != 73. Adapt:
  steps-MAP search: id0 skip, id1 skip, id2 match (A=3);
  xa_collect mB0 -> {50,51,52} (E=1); trace XA-STEPS 50,51,52.
  capsearch: id0 SKIP (cap 2), id1 MATCH (cap 1) (A=2);
  trace XA-SEARCH id=0 cap=2 SKIP / id=1 cap=1 MATCH.
  descriptor: entry=18 r1=5 r2=6 nf=3 valrel=2;
  trace XA-SRC id=1 entry=18 r1=5 r2=6 nf=3 valrel=2.
  entry scan fids 0..20 (A=21):
   (7,51): fold1 s1scan 0..12=13 (r7), s2scan 0..15=16 (r8);
     fold2 r1scan sub==62 rel==7: 0..37=38 FAIL. (67)
     trace XA-ENTRY-CAND r=7 u=51 FAIL-SHAPE.
   (8,60): s1scan 0..16=17 (r2), s2scan sub==20: 0..37=38
     FAIL. (55) trace XA-ENTRY-CAND r=8 u=60 FAIL-SHAPE.
   (17,64): fold1 0..28=29 (r15), 0..29=30 (r16); fold2
     0..30=31, 0..31=32; fold3 0..32=33, 0..33=34 (189);
     arity: addend74 VALscan 0..34=35 (v=1), LINKscan
     0..37=38 FAIL -> reject (73). trace XA-ENTRY-CAND r=17
     u=64 SHAPE-OK add=74,75,76; XA-ARITY u=64
     addvals=1,2,3 LINK-FAIL.
   (17,70): fold1 0..21=22 (r15), 0..16=17 (r16); fold2
     0..23=24, 0..17=18; fold3 0..25=26, 0..26=27 (fid 18
     rel 2 skipped) (134); arity: add60 VAL 0..16=17
     (v=20) LINK 0..13=14 (r8); add61 VAL 0..17=18 (v=30)
     LINK 0..14=15 (r8); add62 VAL 0..18=19 (v=25) LINK
     0..15=16 (r8); cost_rel=8 uniform (99).
     trace XA-ENTRY-CAND r=17 u=70 SHAPE-OK add=60,61,62;
     XA-REMAP 5->15 6->16; XA-ENTRY 18->17;
     XA-ARITY u=70 addvals=20,30,25 cost_rel=8 OK.
  ZBUILD rels=17,15,16,15,16,15,16
    facts=20,21,22,23,24,25,26.
  verify: chain_exec -> 73 (E=2); VALscan (2,73): 0..27=28
    (v=75). trace XA-VERIFY term=73 val=75 OK.
  promote Z id 3; t16 3->1, 3->2; t15 1->2, 2->1;
  LINK14 ans42->3; deliver exec (E=3).
  Frozen: ANS term=73 val=75 via=3; A_SEARCH=671;
  A_EXEC=3; t16=2 {3->1,3->2}; t15=2 {1->2,2->1};
  e_has_to(3,14)=1; no edge type outside {14,15,16};
  Z: id 3, rels [17,15,16,15,16,15,16], facts
  [20,21,22,23,24,25,26], start 50, end 73, dom 2, cap 1,
  live 1; SRC_ID=1.
  A_SEARCH derivation: 3+2+21+67+55+(189+73)+(134+99)+28
  = 671. A_EXEC: collect + verify + deliver = 3.
  Q2B: pipeline mD/mA fail, mB0 -> 52, Z -> 73.
  Frozen: ANS term=73 val=75 via=3, ADAPT_ENTERED=0,
  Z live=1.
- ARM-NOADAPT (adapt_on=0): as FULL until arity: decoy
  (17,64) accepted with arity SKIPPED (VALs 1,2,3 read:
  35+36+37=108); Z' built rels [17,15,16,15,16,15,16]
  facts [19,28,29,30,31,32,33] start 50 end 67; verify:
  chain_exec -> 67 != 73 FAIL (no backtrack: first-match
  precedent). Frozen: ANS term=-2 val=-2 via=-1; t16=0;
  NM=3. (A_SEARCH=444, A_EXEC=2 informational.)
- ARM-ABLATE-X (adapt_on=1, mA retired reason 3 pre-Q2):
  capsearch finds no live AGG MAP (A=3); rebuild BFS
  L=1..7 (A~1786+99): L4/L6 terminal-73 walks fail shape;
  L7 walk [20,21,22,23,24,25,26] passes shape+VAL+arity
  (steps via mB0); promotes NATIVE MAP id 3 (no t16);
  delivers. Frozen: ANS term=73 val=75 via=3; t16=0;
  e_has(3,1,16)=0; NM=4. (A_SEARCH~1891, A_EXEC=3
  informational: blind rebuild costs ~2.8x the guided
  adapt and yields no adapted-from provenance.)
- ARM-ABLATE-Y (adapt_on=1, COST facts 13,14,15 killed
  pre-Q2): adapt as FULL but arity fails everywhere
  (decoy LINK-FAIL; U-chain addend 60 LINKscan 38, fail);
  entry scan exhausts (38). Frozen: ANS term=-2 val=-2
  via=-1; t16=0; NM=3. (A_SEARCH=561 informational.)
- ARM-FRESH (adapt_on=1, no MAPs taught): steps fallback
  {50} (trace XA-STEPS FALLBACK 50); capsearch none;
  rebuild BFS: L7 Z-walk passes shape+VAL but arity fails
  (addend 61 not linked from 50); no walk passes.
  Frozen: ANS term=-2 val=-2 via=-1; t16=0; NM=0.
  (A_SEARCH~1892 informational.)

## 5. Kill bars (frozen)

- K1 (X and Y exist before Z, learned independently):
  in-Zag: qa_via==1 AND qb_via==2 AND q2_via==3 AND every
  rel of mA in {18,5,6} AND every rel of mB0 == 7 (disjoint
  relation sets: no shared vocabulary). Shell: output line
  number of `Q QA` < `Q QB` < `Q Q2`.
- K2 (Z causally depends on both; ablation breaks Z):
  ABLATE-X: t16==0 AND via==3 AND ans==75 AND
  e_has(3,1,16)==0 (the adapted Z, defined by its
  adapted-from provenance, cannot exist without mA; only
  a native lookalike rebuilds). ABLATE-Y: ans==-2 AND
  t16==0 AND NM==3 (without B's pair interface no
  grounding exists).
- K3 (interface adaptation actually occurs, not exact
  copy): in-Zag: NOADAPT ans==-2 AND t16==0 AND NM==3.
  Shell (verbatim grep -F on run1): `XA-REMAP 5->15 6->16`,
  `XA-ENTRY 18->17`, `XA-ARITY u=70 addvals=20,30,25
  cost_rel=8 OK`, `XA-ZBUILD rels=17,15,16,15,16,15,16
  facts=20,21,22,23,24,25,26`, `ANS term=73 val=75 via=3`.
  The remap, entry remap, discovered cost_rel, B-range
  addvals, and B-fact-grounded ZBUILD prove runtime
  interface derivation; the exact-copy path (NOADAPT)
  grounds the decoy and fails verification.
- K4 (fresh learner fails): FRESH ans==-2 AND t16==0 AND
  NM==0. A learner with no prior structures cannot reach
  the answer: blind BFS finds the walk shape but cannot
  satisfy the pair interface without mB0's steps.
- K5 (determinism): 3/3 runs byte-identical (sha256 equal).
- K6 (no domain-pair template in source): 10 frozen grep
  patterns return 0 hits on learner.zag (section 6).
- K7 (substitute is learner-triggered, not
  researcher-selected): in-Zag: FULL SRC_ID==1 AND mD
  (id 0) live==1 at Q2 (the distractor survives unchosen).
  Shell (verbatim): `XA-SEARCH id=0 cap=2 SKIP` and
  `XA-SEARCH id=1 cap=1 MATCH` both present in run1.
  The driver issues Q2 as (50,73,75,AGG,B) with no MAP id;
  selection is first capability match in MAP-id order
  over learner state.
- K8 (Z persists and is reused): Q2B ans==75 AND via==3
  AND ADAPT_ENTERED==0 AND Z live==1 (second query served
  from the persisted adapted structure, no re-adaptation).

Verdict L2-SUBSTITUTE-XDOMAIN-PASS iff K1-K8 all PASS,
no falsifier fires, F-COUNT silent.

## 6. Frozen K6 grep audit spec (run on learner.zag)

Each pattern must return zero matches (grep -c == 0):
1. `5,6,5,6` (mA's fold relseq must not be in the learner)
2. `17,15,16,15,16,15,16` (Z's relseq must not be in learner)
3. `20,21,22,23,24,25,26` (Z's fact list must not be there)
4. `(50,17,70)` (B entry fact literal; world data stays out)
5. `(70,15,60)` (B chain fact literal)
6. `(64,15,74)` (decoy fact literal)
7. `_MODE` (zero modes)
8. `bridge` (case-insensitive; no bridge handlers)
9. `python` (case-insensitive; pure Zag)
10. `as *i32` (the pinned-znc miscompile pattern; u8 cells
    + get32/set32 only)

## 7. Frozen falsifiers

- F-NO-GROUND: FULL adapt finds no grounding.
- F-WRONG-Z: promoted Z relseq/facts/(start,end) != frozen.
- F-CTRL-PASS: NOADAPT ans != -2.
- F-ABLX-ADAPT: ABLATE-X t16 != 0.
- F-ABLY-PASS: ABLATE-Y ans != -2.
- F-FRESH-PASS: FRESH ans != -2.
- F-Q2B-RE: Q2B ADAPT_ENTERED != 0 or via != 3.
- F-EDGE-NEW: any edge with type outside {14,15,16}.
- F-COUNT: FULL A_SEARCH != 671 or A_EXEC != 3
  (implementation must match the frozen counting rules
  exactly; a pure arithmetic slip in this prereg's hand
  derivation may be transparently amended pre-verdict,
  an algorithmic counting change may not).
- F-AUDIT / F-NONDET / F-PYTHON: as in prior waves; any
  fires voids the build.

## 8. Determinism spec

No RNG. MAP-id order, fid-ascending scans, first-match
rules, BFS L=1..7 in extension order everywhere. Output via
one preallocated buffer and a single raw-syscall write loop
(the pinned-znc stdout workaround). 3/3 byte-identical
required.

## 9. Disclosed residual footprint and non-claims

- The cross-domain SUBSTITUTE-ADAPT operator, descriptor
  extraction, entry/fold search, arity check, rebuild BFS,
  edge-type conventions, and cost counters are
  researcher-supplied generic machinery, frozen here. None
  names a relation, MAP, domain, or domain pair. The L2
  claim is narrow: a planning query with no native
  aggregation is served by a learner-selected arithmetic
  SUM structure whose interface (relation names, entry,
  addend arity, value source) is derived at runtime from
  learner state and B facts, verified by execution, with
  adapted-from provenance to both source structures, while
  the no-adaptation control provably fails on the decoy.
- ADAPT_ON is a driver-set causal-control flag (the
  composition_l2 adapt_on precedent), never written by the
  learner. It enables the lesion comparison; it is not a
  runtime mode.
- One world family (arithmetic SUM x plan-cost
  aggregation). No generality claim beyond the five arms.
  The world (fact table, decoy, COST kill) is
  builder-designed, not adversary-designed. Sealed-
  adversary generality is open future work.
- 0 modes, 0 bridges, 0 handlers, 0 new edge types, 0 new
  opcodes, 0 new semantic cases. Pure Zag, safebin
  toolchain, zero forbidden executables.
- No em/en dashes in loop documentation. Paper untouched.
  Nothing pushed. Commits local with explicit pathspec.
- Unfrozen only: no frozen source touched. The frozen TNN
  core is not used here; this is a standalone
  learner-mechanism experiment in the chain family.
