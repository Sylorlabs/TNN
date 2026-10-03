# PREREG: L2 SPECIALIZE-XDOMAIN (learner-decided specialization of a general procedure, cross-domain)

Status: PREREG-FROZEN. No implementation exists at this commit.
Scope: `docs/lab/research-lead/overnight-20260928/l2_specialize_xdomain/` only.
Worker: L2 Adaptive Reuse subagent (depth 2/2), 2026-10-02.
Parent mandate: L2 ADAPTIVE REUSE is top priority. The L2 operation matrix
(extend, truncate, specialize, substitute, interface-adapt) is complete at
L1/within-domain, and L2-SUBSTITUTE-XDOMAIN just passed cross-domain.
This lane pushes SPECIALIZE across domains: a GENERAL parametric procedure
(a variable-arity AGG fold learned in arithmetic) is NARROWED for a planning
target (total plan cost), and the learner itself decides WHICH parameters to
fix, by trial-and-verification over candidates derived from its own
target-domain MAP inventory. The researcher specifies only the generic
specialize operator; no parameter value is researcher-specified.

Predecessor: `l2_substitute_xdomain/` (verdict L2-SUBSTITUTE-XDOMAIN-PASS)
built the cross-domain adapter idiom reused here (capability search,
entry/fold discovery, pair-interface arity check, execution verification,
type-16 provenance). The operation under test here is different:
SUBSTITUTE borrows a structure to fill a missing capability; SPECIALIZE
takes an EXISTING general procedure and compiles a cheaper
target-specific variant of it. The trigger here: the planning domain has
no AGG MAP, and the general arithmetic AGG procedure CAN serve the target
but only via expensive per-query re-derivation; the learner specializes it
once and reuses the cheap variant.

## 1. What is being tested

Whether a learner holding (X) a GENERAL parametric AGG MAP mG learned in
an arithmetic episode (fold-count recorded as a parameter, not fixed) and
(Y) planning ROUTE MAPs mD2/mB0 learned in planning episodes, when asked
for the TOTAL COST of a plan (cap=AGG, dom=B), (1) runs the general
procedure cross-domain via per-query re-derivation (expensive), (2) in the
specialize arm instead DERIVES specialization candidates from its own
target-domain MAP inventory (hypothesized fold-count = plan step count per
live B MAP: mD2 -> 2, mB0 -> 3, in MAP-id order), (3) TRIALS each candidate
with the cross-domain adapter (entry/fold discovery, fold walk, terminal +
VAL + pair-interface arity checks), observing nf=2 fail verification on
every entry grounding while nf=3 verifies on entry (50,17,70), (4) FIXES
the discovered parameters (nf=3, entry rel 17, fold rels 15,16) into a new
specialized MAP mS with adapted-from provenance to BOTH mG (structural
source) and mB0 (target-interface source), and (5) answers later B AGG
queries through mS at strictly lower per-query search cost than the
general procedure, on the same query with different values (not overfitted
to one grounding) while refusing a query outside its fixed arity (genuine
narrowing, no spurious fire).

Concrete scenario (all ids frozen):

Domain A (arithmetic SUM), facts:
  0:(40,5,30) 1:(30,6,41) 2:(41,5,31) 3:(31,6,42) 4:(42,5,32)
  5:(32,6,43) 6:(30,2,3) 7:(31,2,4) 8:(32,2,5) 9:(43,2,12)
  10:(100,18,40)
  rel 5/6 = add-fold pair, rel 18 = list->initial-total entry,
  rel 2 = VAL. Addend values 3,4,5.
  mG (id 1): GENERAL AGG MAP: dom=A(1), cap=AGG(1),
  relseq [18,5,6,5,6,5,6], facts [10,0,1,2,3,4,5], start 100,
  end 43. Descriptor (extracted generically at teach):
  entry=18, r1=5, r2=6, nf=3 (observed), valrel=2, param=1
  (fold-count is a PARAMETER, not fixed).

Domain B (planning), facts:
  11:(54,7,55) 12:(55,7,56)                 [mD2 2-hop route]
  13:(50,7,51) 14:(51,7,52) 15:(52,7,53)     [mB0 3-hop route]
  16:(50,8,60) 17:(51,8,61) 18:(52,8,62)     [COST step->cost]
  19:(60,2,20) 20:(61,2,30) 21:(62,2,25)     [VAL of costs]
  22:(50,17,64) 23:(50,17,70)                [entries]
  24:(64,15,74) 25:(74,16,65) 26:(65,15,75) 27:(75,16,66)
  28:(66,15,76) 29:(76,16,67)                [decoy add-chain]
  30:(74,2,1) 31:(75,2,2) 32:(76,2,3) 33:(67,2,6)
  34:(70,15,60) 35:(60,16,71) 36:(71,15,61) 37:(61,16,72)
  38:(72,15,62) 39:(62,16,73)                [U add-chain]
  40:(73,2,75)                               [VAL of total]
  41:(50,17,80)                              [entry, chain 2]
  42:(80,15,90) 43:(90,16,91) 44:(91,15,92) 45:(92,16,93)
  46:(93,15,94) 47:(94,16,95)                [chain 2]
  48:(95,2,36)                               [VAL of total 2]
  49:(50,8,90) 50:(51,8,92) 51:(52,8,94)     [COST links 2]
  52:(90,2,11) 53:(92,2,12) 54:(94,2,13)     [VALs 2]
  mD2 (id 0): dom=B(2), cap=ROUTE(2), relseq [7,7],
  facts [11,12], start 54, end 56. Taught FIRST; contributes
  the nf=2 specialization candidate the learner must reject.
  mB0 (id 2): dom=B(2), cap=ROUTE(2), relseq [7,7,7],
  facts [13,14,15], start 50, end 53. Contributes nf=3 and
  the plan stepset for the pair interface.

Queries (driver-issued, no MAP id ever passed):
  QA:  (100,43,12, cap=AGG, dom=A) -> via mG home replay
  QB:  (50,53,-1, cap=ROUTE, dom=B) -> via mB0
  Q2:  (50,73,75, cap=AGG, dom=B)  -> FULL: specialize arm
         promotes mS; GEN: general procedure answers;
         ABLATE-X: fails
  Q2B: (50,73,75, cap=AGG, dom=B)  -> FULL: via mS, no
         re-specialize; GEN: general re-derives
  Q2C: (50,95,36, cap=AGG, dom=B)  -> FULL only: via mS on
         different values (not overfitted to one grounding)
  Q2D: (50,72,-1, cap=AGG, dom=B)  -> FULL only: mS must NOT
         fire (fixed arity 3 cannot reach 72; genuine
         narrowing, no spurious accept)

mS (built by the learner, id 3): relseq [17,15,16,15,16,15,16],
facts [23,34,35,36,37,38,39], start 50, end 73, dom=B, cap=AGG,
descriptor (17,15,16,nf=3,valrel=2,param=0). Execution re-grounds
per query from the FIXED descriptor: entry-rel-17 candidates in
fid order, exactly-3-fold walk with fixed rels (15,16), terminal
+ VAL + pair-interface arity checks (addend VAL hit, COST-link
from plan stepset, uniform link rel).

## 2. Frozen learner machinery (disclosed)

Standalone pure-Zag learner (xs_learner.zag) + world side
(xs_world.zag: fact table + MAP teaching per arm) + experiment side
(xs_driver.zag: three arms, in-Zag bar evaluation, main).
The frozen TNN core is not used. Unfrozen only; no frozen source touched.

State: one u8 buffer. Header: 0 NF, 1 NM, 2 NE, 3 SPEC_ON
(driver-set causal-control flag, never written by the learner),
4 LAST_VIA, 5 LAST_TERM, 6 IN_SPEC, 7 SPEC_ENTERED,
8 SRC_ID (255=none), 9 SPEC_NF (255=none), 10 TRIAL2F,
11 TRIAL3OK. Facts: 64 x 8 bytes at 16..527
[sub,rel,obj,live,0,0,0,0]. MAPs: 16 x 32 bytes at 528..1039
[tag=20,live,start,end,rlen,flen,reason,pad, rels x8 @+8,
facts x8 @+16, dom @+24, cap @+25, d_entry @+26, d_r1 @+27,
d_r2 @+28, d_nf @+29, d_valrel @+30, d_param @+31].
Edges: 64 x 4 bytes at 1040..1295 [from,to,type,pad].
S_SEARCH i32 @1296, S_EXEC i32 @1300, LAST_VAL i32 @1304.
Scratch: stepset 8 x i32 @1408, addends 8 x i32 @1472,
candidates 8 x i32 @1504, walk-fids 8 x i32 @1536.

Edge-type semantics:
- type 16: specialized-from. At mS promotion: 3->1 (structural
  source mG) and 3->2 (target-interface source mB0).
- type 14 (LINK14): answer-node -> delivering MAP on deliver
  (recorded as edge ans->MAP; informational).
- No other edge types may appear (F-EDGE-NEW).

Scan primitives (all fid-ascending over live facts, S+=1 per fid
examined; MAP loops S+=1 per header examined):
- scan1(sub,rel): first live fid with sub==sub, rel==rel.
- scan_nv(sub,valrel): first live fid with sub==sub, rel!=valrel
  (fold-relation discovery).
- scan_val(node,valrel): first live fid with rel==valrel,
  sub==node -> obj (VAL read).
- scan_link(node,stepset): first live fid with obj==node and
  sub in stepset -> (rel,sub) (pair-interface link).
- xa_collect(mid): walk MAP rels from MAP start via scan1;
  record visited nodes in stepset; S_EXEC+=1.

Generic operations (frozen, relation-agnostic, MAP-agnostic,
domain-agnostic):
- f_teach(sub,rel,obj): observe a world fact. No S ticks.
- m_teach(rs,rl,fs,fl,start,end,dom,cap): learn a MAP. If
  cap==AGG, extract the interface descriptor generically:
  d_entry=rels[0], d_r1=rels[1], d_r2=rels[2], require
  rels[1..] to alternate (r1,r2) with (rlen-1) even and >= 2,
  d_nf=(rlen-1)/2, d_valrel = rel of the first live fact
  (fid order) with sub==end, d_param=1 (AGG fold-count is
  parametric by construction; no rel literal anywhere).
- home_exec(mid,s,t,v): replay of a parametric MAP in its home
  domain: walk d_entry then d_nf folds of (d_r1,d_r2) via
  scan1; terminal==t and (v<0 or scan_val(t)==v) required.
  S_EXEC+=1.
- chain_exec(mid,s,t,v): plain relseq walk via scan1 (for
  ROUTE MAPs in the pipeline); terminal==t and VAL check.
  S_EXEC+=1.
- adapter_trial(sm,s,t,v,L,stepset): ONE candidate grounding
  of source sm at fold-count L. Entry loop over fids 0..NF-1
  (S+=1 per fid; candidates are live facts with sub==s, any
  rel); per candidate: scan_nv(u)->(s1,a); scan_nv(a)->(s2,b);
  walk folds 2..L via scan1 (addends=[a,c1_2,..,c1_L],
  walk-fids recorded); terminal==t required, then VAL check
  (v>=0), then arity: per addend scan_val must hit,
  scan_link must hit, all link rels equal (uniform pair
  interface). First full pass ACCEPTs and returns
  (re,s1,s2,linkrel,entry_fid); else FAIL. No S_EXEC ticks
  (pure search).
- xs_specialize(s,t,v): IN_SPEC=1, SPEC_ENTERED=1.
  1. stepsMAP: first live MAP (id order) with dom==qdom and
     start==s; xa_collect -> stepset. None -> fail.
  2. capsearch: first live MAP (id order) with cap==qcap and
     d_param==1 -> sm (the GENERAL procedure). None -> fail
     (trace XS-SPECIALIZE-FAIL reason=no-source). SRC_ID=sm.
  3. candidates: live MAPs of dom==qdom, id order:
     c=|xa_collect|-1 (hypothesized fold-count = plan step
     count); distinct values in id order -> cand list.
     Trace XS-CANDIDATES.
  4. for L in cand: trace XS-TRIAL; r=adapter_trial(sm,s,t,v,
     L,stepset); L==2&&r==FAIL sets TRIAL2F=1;
     L==3&&r!=FAIL sets TRIAL3OK=1. On first ACCEPT:
     SPEC_NF=L; promote mS (next id): rels=[re,s1,s2,...]
     (L pairs), facts=[entry_fid,walk-fids...], start=s,
     end=t, dom=qdom, cap=qcap, d=(re,s1,s2,L,valrel,0);
     t16 mS->sm and mS->stepsMAP; trace XS-SPEC-NF,
     XS-SPEC-RELS, XS-SPEC-COSTREL, XS-SPEC-PROMOTE;
     deliver via spec_exec; return.
  5. no candidate accepts -> ANS -2 (fail).
- spec_exec(mid,s,t,v): execute a specialized (param=0) MAP:
  re-collect stepset from stepsMAP (first live qdom MAP with
  start==s); entry loop over live facts with sub==s AND
  rel==d_entry (fid order); per candidate walk exactly d_nf
  folds of (d_r1,d_r2); terminal==t, VAL check (v>=0),
  arity (addend VAL hit + scan_link hit + uniform link rel).
  First pass delivers. S_EXEC+=1 on entry.
- xs_general(s,t,v): the general procedure WITHOUT
  specialization (per-query re-derivation): steps 1-3 as in
  xs_specialize, then for L in cand: adapter_trial; first
  ACCEPT delivers via sm (no promotion, no provenance).
  Trace XS-GENERAL-ACCEPT.
- xs_query(s,t,v,cap,dom): reset S/E; pipeline over live MAPs
  in id order: if start==s and dom==qdom: exec (param==0 ->
  spec_exec; cap==AGG and dom==MAP.dom -> home_exec; else
  chain_exec); first terminal==t (and VAL if v>=0) delivers
  (LAST_VIA=mid). Else if SPEC_ON==1: xs_specialize; else:
  xs_general. LAST_TERM/LAST_VAL/LAST_VIA recorded; -2/-2/-1
  on failure.

## 3. Frozen cost-counting rules

- S_SEARCH += 1 per fact id examined in any learner scan loop
  (entry loops, scan1, scan_nv, scan_val, scan_link, collect
  hop scans).
- S_SEARCH += 1 per MAP header examined in any learner MAP
  scan loop (pipeline, stepsMAP search, capsearch, candidate
  derivation).
- S_EXEC += 1 per xa_collect call, per pipeline MAP-exec call
  (home_exec/chain_exec), per spec_exec entry.
- adapter_trial costs search only (no EXEC ticks).
- Teaching (f_teach/m_teach) costs nothing.
- S/E reset at each xs_query entry; driver prints per-query
  S/E/ANS.

## 4. Frozen arms and hand-derived expectations

All arms: teach facts 0..54; m_teach mD2(0), mG(1), mB0(2).
QA -> (43,12) via 1. QB -> (53,-1) via 2. Scan-cost atoms
(fact ids examined, all facts live; NF=55):
scan1: (100,18)=11 (40,5)=1 (30,6)=2 (41,5)=3 (31,6)=4
(42,5)=5 (32,6)=6 (50,7)=14 (51,7)=15 (52,7)=16 (54,7)=12
(55,7)=13 (70,15)=35 (60,16)=36 (71,15)=37 (61,16)=38
(72,15)=39 (62,16)=40 (80,15)=43 (90,16)=44 (91,15)=45
(92,16)=46 (93,15)=47 (94,16)=48 (64,15)=25 (74,16)=26
(65,15)=27 (75,16)=28 (66,15)=29 (76,16)=30; MISS=55.
scan_nv(sub): 51->15(s1=7) 52->16(s2=7) 60->36(s1=16)
71->37(s2=15) 64->25(s1=15) 74->55 FAIL 70->35(s1=15)
61->38(s2=16) 80->43(s1=15) 90->44(s1=16) 91->45(s2=15)
92->46(s2=16).
scan_val: 43->10(v12) 60->20 61->21 62->22 71->55 FAIL
72->55 FAIL 73->41(v75) 90->53 92->54 94->55 95->49(v36).
scan_link (stepset {50,51,52,53}): 60->17(r8) 61->18(r8)
62->19(r8) 90->50(r8) 92->51(r8) 94->52(r8) 74->55 FAIL
71->55 FAIL.
collect(mB0)=14+15+16=45 steps {50,51,52,53}; collect(mD2)=
12+13=25 steps {54,55,56}.

- ARM-FULL (SPEC_ON=1): QA: pipeline headers 2 + home_exec
  (11+1+2+3+4+5+6) + VAL 10 = 44, E=1, ANS 43,12 via 1.
  QB: headers 3 + chain_exec 45 = 48, E=1, ANS 53,-1 via 2.
  Q2: pipeline headers 3 + mB0 exec 45 = 48 (53!=73).
  specialize: stepsMAP headers 3; collect mB0 45 (E);
  capsearch headers 2 (id0 skip, id1 match, SRC_ID=1);
  candidates: headers 3 + collect mD2 25 (E) + collect mB0
  45 (E) -> [2,3], trace XS-CANDIDATES 2,3.
  Trial nf=2 (entry loop 55 fids): (50,7,51): 15+16+55=86
  FAIL-WALK; (50,8,60): 36+37+38+39=150 FAIL-TERM(62);
  (50,17,64): 25+55=80 FAIL-DISC2; (50,17,70):
  35+36+37+38=146 FAIL-TERM(72); (50,17,80):
  43+44+45+46=178 FAIL-TERM(93); (50,8,90):
  44+45+46+47=182 FAIL-TERM(94). Trial = 877,
  trace XS-TRIAL nf=2 FAIL, TRIAL2F=1.
  Trial nf=3 (entry loop 24 fids, accept at 23):
  (50,7,51): 86 FAIL-WALK; (50,8,60):
  36+37+38+39+40+55=245 FAIL-WALK; (50,17,64): 80
  FAIL-DISC2; (50,17,70): walk 35+36+37+38+39+40=225,
  term 73 OK, VAL 41 (75 OK), arity
  20+17+21+18+22+19=117 (addvals 20,30,25, linkrel 8
  uniform) -> ACCEPT. Trial = 24+86+245+80+383 = 818,
  trace XS-TRIAL nf=3, XS-ACCEPT re=17 s1=15 s2=16 lr=8,
  TRIAL3OK=1.
  Promote mS id 3: rels [17,15,16,15,16,15,16], facts
  [23,34,35,36,37,38,39], start 50, end 73, dom 2, cap 1,
  d=(17,15,16,3,2,0); t16 3->1, 3->2 (NE=2);
  trace XS-SPEC-NF 3, XS-SPEC-RELS 17,15,16,
  XS-SPEC-COSTREL 8, XS-SPEC-PROMOTE id=3.
  Delivery spec_exec: stepsMAP headers 3 + collect 45 (E)
  + entry loop 24 + (50,17,64) walk
  25+26+27+28+29+30=165 -> 67!=73 + (50,17,70) walk 225
  + VAL 41 + arity 117 = 383 -> ACCEPT. = 620 (E+1).
  Q2 frozen: S=48+3+45+2+3+25+45+877+818+620=2486, E=6,
  ANS term=73 val=75 via=3, SPEC_NF=3, NM=4.
  Q2B: pipeline headers 4 (id0,1 skip; id2 mB0 exec 45 ->
  53!=73; id3 mS) + spec_exec 620 = 669, E=3,
  ANS 73,75 via 3, SPEC_ENTERED=0.
  Q2C: pipeline headers 4 + mB0 exec 45 + spec_exec:
  stepsMAP 3 + collect 45 + entry loop 42 + (50,17,64)
  walk 165 -> 67!=95 + (50,17,70) walk 225 -> 73!=95 +
  (50,17,80) walk 43+44+45+46+47+48=273 -> 95 OK +
  VAL 49 (36 OK) + arity (53+50+54+51+55+52)=315
  (addvals 11,12,13, linkrel 8 uniform) = 1117.
  S=4+45+1117=1166, E=3, ANS 95,36 via 3.
  Q2D: pipeline headers 4 + mB0 exec 45 + spec_exec:
  3+45 + entry loop 55 + walks 165+225+273 (67/73/95,
  none 72) = 766, no accept. S=4+45+766=815, E=3,
  ANS -2,-2 via -1.
- ARM-GENERAL (SPEC_ON=0): QA 44/1, QB 48/1 (as FULL).
  Q2: pipeline 48 (as FULL) + general: stepsMAP 3 +
  collect 45 (E) + capsearch 2 + candidates 3+25+45 (E,E)
  + trial nf=2 877 FAIL + trial nf=3 818 ACCEPT (same
  atoms as FULL) -> deliver via sm, NO promotion.
  S=48+3+45+2+3+25+45+877+818=1866, E=5,
  ANS 73,75 via 1, NM=3, t16=0,
  trace XS-GENERAL-ACCEPT nf=3.
  Q2B: pipeline headers 3 + mB0 exec 45 + general 1818
  = 1866, E=4, ANS 73,75 via 1 (general re-derives every
  query; no memory of the fix).
- ARM-ABLATE-X (SPEC_ON=1, mG live=0 pre-Q2): QA 44/1,
  QB 48/1 (as FULL). Q2: pipeline headers 3 (id1 dead
  skip) + mB0 exec 45 = 48; specialize: stepsMAP headers
  3 + collect 45 (E); capsearch headers 3 (id0 cap!=1,
  id1 dead, id2 cap!=1) -> none ->
  trace XS-SPECIALIZE-FAIL reason=no-source, ANS -2,-2
  via -1. S=48+3+45+3=99, E=2, NM=3, t16=0.

One-time investment vs amortization (informational):
FULL total after Q2B = 2486+669 = 3155; GEN total after
Q2B = 1866+1866 = 3732. Breakeven at the 2nd query:
specialization pays off immediately on reuse.

## 5. Kill bars (frozen)

- K1 (general X exists before specialization): in-Zag (FULL):
  qa_via==1 AND qb_via==2 AND q2_via==3. Shell: output line
  number of `Q QA` < `Q QB` < `Q Q2` in run1.
- K2 (general X suboptimal on target; specialization REQUIRED
  for best performance): in-Zag: gen_q2b_term==73 AND
  gen_q2b_val==75 (general answers correctly) AND
  gen_q2b_s > full_q2b_s (at strictly higher search cost).
  Frozen: 1866 > 669.
- K3 (learner decides specialization; which parameters to fix
  not researcher-specified): in-Zag (FULL): spec_nf==3 AND
  trial2f==1 AND trial3ok==1 (the learner tried nf=2 from its
  own inventory, watched it fail verification, and fixed
  nf=3 on verification success). Shell (verbatim grep -F on
  run1): `XS-CANDIDATES 2,3`, `XS-TRIAL nf=2 FAIL`,
  `XS-SPEC-NF 3`, `XS-SPEC-RELS 17,15,16`. The candidates
  {2,3} are derived from the learner's target-domain MAP
  inventory (step counts of mD2, mB0); the choice is by
  verification trial, never a researcher-supplied value.
- K4 (specialized outperforms general on target): in-Zag:
  full_q2b_term==73 AND full_q2b_s < gen_q2b_s.
  Frozen: 669 < 1866 (2.79x).
- K5 (specialized retains correctness, not overfitted to
  breakage): in-Zag (FULL): q2b_via==3 AND q2b_term==73 AND
  q2b_val==75 AND q2c_via==3 AND q2c_term==95 AND
  q2c_val==36 (different values served: values not baked in)
  AND q2d_via==-1 (fixed arity 3 does not spuriously fire on
  the 2-fold-shaped query: genuine narrowing).
- K6 (determinism): 3/3 runs byte-identical (sha256 equal).
- K7 (no domain-pair template): 8 frozen grep patterns return
  0 hits on xs_learner.zag (section 6).
- K8 (ablation: no X fails): in-Zag (ABLATE-X): q2_term==-2
  AND q2_via==-1 AND nm==3 AND t16==0 (no mS promoted, no
  provenance). Without the general procedure there is
  nothing to specialize; blind from-scratch rebuild is a
  different lane's claim and is not attempted here.

Verdict L2-SPECIALIZE-XDOMAIN-PASS iff K1-K8 all PASS, no
falsifier fires, F-COUNT silent.

## 6. Frozen K7 grep audit spec (run on xs_learner.zag)

Each pattern must return zero matches (grep -c == 0):
1. `50,17,70` (B entry fact literal; world data stays out)
2. `70,15,60` (B chain fact literal)
3. `17,15,16,15,16,15,16` (mS's relseq must not be in the learner)
4. `23,34,35,36,37,38,39` (mS's fact list must not be there)
5. `_MODE` (zero modes)
6. `bridge` (case-insensitive; no bridge handlers)
7. `python` (case-insensitive; pure Zag)
8. `as *i32` (the pinned-znc miscompile pattern; u8 cells
   + get32/set32 only)

## 7. Frozen falsifiers

- F-NO-SPEC: FULL Q2 via != 3 or SPEC_NF != 3.
- F-TRIAL: TRIAL2F != 1 or TRIAL3OK != 1 (the learner did not
  genuinely decide between candidates).
- F-GEN-WRONG: GEN Q2 or Q2B term != 73 or val != 75.
- F-Q2B: FULL Q2B via != 3 or term/val != 73/75.
- F-Q2C: FULL Q2C via != 3 or term/val != 95/36.
- F-Q2D: FULL Q2D via != -1 (spurious fire).
- F-ABLX: ABLATE-X Q2 ans != -2 or NM != 3 or t16 != 0.
- F-EDGE-NEW: any edge with type outside {14,16}.
- F-COUNT: any frozen per-query S or E != frozen value
  (a pure arithmetic slip in this prereg's hand derivation
  may be transparently amended pre-verdict; an algorithmic
  counting change may not).
- F-AUDIT / F-NONDET / F-PYTHON: as in prior waves; any
  fires voids the build.

## 8. Determinism spec

No RNG. MAP-id order, fid-ascending scans, first-match rules,
candidate order [2,3] from MAP-id order everywhere. Output via
one preallocated buffer and a single raw-syscall write loop
(the pinned-znc stdout workaround). 3/3 byte-identical required.

## 9. Disclosed residual footprint and non-claims

- The SPECIALIZE operator, candidate-derivation rule
  (hypothesized fold-count = plan step count per live
  target-domain MAP), the cross-domain adapter (entry/fold
  discovery, fold walk, terminal + VAL + pair-interface arity
  checks), descriptor extraction, edge-type conventions, and
  cost counters are researcher-supplied generic machinery,
  frozen here. None names a relation, MAP, domain, domain
  pair, or parameter value. The L2 claim is narrow: the
  learner derives specialization candidates {2,3} from its
  own inventory, trials each with execution verification,
  fixes the verified parameters (nf=3, entry 17, folds
  15/16) into a new persistent MAP with specialized-from
  provenance, and reuses it at 2.79x lower per-query search
  cost than the unspecialized general procedure, while the
  general procedure remains correct (K2 is about cost, not
  correctness) and the ablation without X fails outright.
- SPEC_ON is a driver-set causal-control flag (the
  composition_l2 adapt_on precedent), never written by the
  learner. It enables the lesion comparison; it is not a
  runtime mode.
- One world family (arithmetic SUM x plan-cost aggregation).
  No generality claim beyond the three arms. The world (fact
  table, decoy chain, chain 2, mD2 distractor) is
  builder-designed, not adversary-designed. Sealed-adversary
  generality is open future work.
- 0 modes, 0 bridges, 0 handlers, 0 new edge types, 0 new
  opcodes, 0 new semantic cases. Pure Zag, safebin toolchain,
  zero forbidden executables.
- No em/en dashes in loop documentation. Paper untouched.
  Nothing pushed. Commits local with explicit pathspec.
- Unfrozen only: no frozen source touched. The frozen TNN
  core is not used here; this is a standalone
  learner-mechanism experiment in the chain family.
