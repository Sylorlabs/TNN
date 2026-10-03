# PREREG: BP-6 (belief-layer open dynamics, continued)

Worker: BELIEF-PROVENANCE-6 subagent, 2026-10-03. Non-ledger
task (claim minting paused); nothing minted.
Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_6/`
Status: FROZEN. Committed before any implementation file
exists in this lane. All predicted numbers below are
hand-derived from the frozen R1-R7 forms (BP-4 REPORT.md,
DESIGN.md 3.1-3.2), the dormant bp2_bar_after rule in the
belief layer, and the probe-measured block behaviors
(type-7/type-3 evidence edges from ev_observe,
evict_node/rec_evict shapes, all re-probed 2026-10-03 in
/tmp/bp6probe). The 7 falsifiable predictions (FP1-FP7)
stay sealed; this lane tests the remaining BP-5 open
dynamics: bar-adjustment trajectories, combiner
alternatives, eviction interaction, larger/nested cycles.

## 0. What is being tested

Four open-dynamics questions, each with discriminating kill
bars:

- BA (bar-adjustment trajectories): the R7 selection bar is
  fixed in every lane so far. The belief layer already
  contains bp2_bar_after (implemented in BP-2, never
  triggered: confirmed commitment disconfirmed -> bar+1;
  confirmed commitment with eff>=2*bar -> bar-1 floored at
  MIN_BAR=10; else unchanged). Here R7 selections are fed
  back as learner commitments: select at the current bar,
  absorb the emergent world outcome (type-7/type-3 edges
  via the block, BP-5 convention, indep=0), then apply
  bp2_bar_after. Predicted trajectory: false positive
  raises the bar (50->51), near-bar true positive leaves it
  (51), far-above-bar true positive lowers it (51->50),
  floor holds at 10, and the raised bar excludes a
  marginal candidate it previously admitted.
- COMB (combiner alternatives): R6 uses the min combiner
  (frozen). Driver-side experimental variants max, avg,
  and evidence-weighted avg (weights w=conf+disc+1 from
  learner state, disclosed) are compared on one fixed
  structure with targets at sup 120 and 60. Predicted:
  min->60, max->120, avg->90, wavg->94 (hand-derived
  integer arithmetic). The discriminating criterion is
  no-invention: a combiner must not assign the composite
  support exceeding a component's support without new
  evidence (R2/R3 are the only evidence-driven support
  moves). Predicted: min is the unique combiner
  satisfying no-invention; max/avg/wavg all violate it;
  and the combiner flips R7 selection on the same
  structure.
- EV (eviction interaction): what happens to a belief when
  the block evicts its node? The block's own evict_node is
  called with every other live node protected by the
  block-native type-9 protection edge, so the victim is
  deterministic. Competing hypotheses: H-persist (record
  untouched) vs H-tombstone (record destroyed, I1-style).
  Predicted: H-persist holds (hasb=1, sup unchanged); R7
  still selects the dead MAP (stale selection, the gap);
  the liveness-gating baseline correctly skips it
  (discriminating pair); bp2_relicense on the evicted MAP
  retires it with reason 2 (the layer owns dormant
  detection machinery, nothing triggers it).
- CY5/NST (larger/nested cycles): BP-5 characterized the
  2-cycle. Here a 5-cycle and nested cycles (triangle with
  a 2-cycle nested on one node). Predicted: per-hop R6
  converges monotonically to the cycle min (no cascade on
  single application, fixpoint under re-application, no
  oscillation); R6 snap-up generalizes to the 5-cycle; the
  nested component converges to the shared min; 0 absorbs
  the nested component with reason-2 retirement.

## 1. Researcher machinery (frozen, disclosed)

Belief layer: BP-5's bp5_learner.zag reused VERBATIM as
bp6_learner.zag (SHA-256
2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e,
re-verified after copy): record schema (8 u8), R1-R7,
eff(), b_retire, bp2_lic_live, bp2_kill_one_prov,
bp2_lgsel, bp2_bar_after. Constants: BASE=100, INC_HI=20,
INC_LO=10, DEC=20, BAR0=50, MIN_BAR=10.

New learner machinery this lane: NONE. All four arms run
on the frozen belief layer. In particular:
- bp2_bar_after is existing (dormant) belief-layer code,
  now triggered in a closed loop; not new machinery.
- Combiner variants (bp6_cmax, bp6_cavg, bp6_cwavg) are
  driver-side experimental code in bp6_driver.zag, NOT
  belief-layer changes. They mirror bp2_propagate's
  traversal exactly (live type-14 targets holding
  records) and differ only in the aggregation. R6 (min)
  remains the frozen belief-layer rule regardless of the
  comparison outcome.
- Eviction uses the block's own evict_node; the type-9
  protection edges used for deterministic victim
  targeting are block-native (protection), pre-existing
  edge type, disclosed here.

Test-harness code (in bp6_driver.zag, not belief
machinery):

- bp6_absorb(W,bt,mid,fid,p7,p3,out): the BP-5 absorb
  verbatim in behavior (new type-7 -> bp2_confirm
  indep=0; new type-3 -> bp2_disconfirm), renamed.
  out[0]=new7, out[4]=new3.
- bp6_cmax/bp6_cavg/bp6_cwavg: max / integer-mean /
  evidence-weighted-mean (w=b_conf+b_disc+1) variants,
  same traversal and retire-on-0 shape as bp2_propagate.
- World builders per arm (below), in-driver bars,
  commitment bookkeeping (driver i32s: bar, eff_at_commit,
  confirmed flag derived from the absorb out: n3>0 -> 1
  else 0).

Emergent evidence facts (probe-measured on the frozen
block, pre-prereg, /tmp/bp6probe):

- ev_observe matching (o == fact field28): ret 1, exactly
  one new type-7 self-edge on the activated fact, teaches
  nothing. A second matching observe on the same fact
  writes a second type-7 (t7cnt 2/2).
- ev_observe contradicting: ret 0, exactly one new
  type-3 self-edge, revise attempted and reverted on the
  rootless promoted shape (field28 unchanged).
- Mixed sequence verified: contradict on fact k2 then
  matching observe on fact k1 of the same MAP gives
  t3-on-k2 == 1 and t7-on-k1 == 1 independently.
- evict_node with all live nodes except the target
  protected by type-9 edges (field12=100): returns the
  target id; target ng(36)==0; all incident edges killed
  (eg(e,0)==-1); rec_evict pushes a live tag-3 tombstone
  onto the hg(12) chain (probe: h 10, tag 3, live 1).
- bp2_bar_after(50,1,100)==51 (probe-verified).

## 2. Arm BA: bar-adjustment trajectories (world WBA)

tnn2_init. fa1=ev_teach(701,71,10), fa2=ev_teach(702,72,20),
fa3=ev_teach(703,73,30), fa4=ev_teach(704,74,40); field16
tags 2/6/2/6. mA=promote_graph(WBA,-1,701,71,10,
[fa1,fa2,fa3,fa4],4). mB=alloc_node (bare B-COMP).
bp2_form(mA,0): b_sup=100, b_ext=2, b_self=2, formed=4.
bp2_form(mB,1); 2x bp2_disconfirm(mB) -> 60.
eff(mA)==b_sup throughout (partition (2,2), d_self=255:
eff = s*(2*255+255*2)/(255*4) = s).

Unit checks (pure function):
- K-BA-U1: bp2_bar_after(50,1,100)==51 (false positive
  raises).
- K-BA-U2: bp2_bar_after(51,0,80)==51 (near-bar true
  positive: unchanged).
- K-BA-U3: bp2_bar_after(51,0,110)==50 (far-above-bar true
  positive: lowers).
- K-BA-U4: bp2_bar_after(10,0,25)==10 (floor at MIN_BAR).
- K-BA-U5: bp2_bar_after(10,1,5)==11 (raise works at
  floor).

T1 (false positive): R7({mA,mB},50): 100 vs 60 -> mA.
eff_at_commit=100. ev_observe(WBA,702,72,999) -> ret 0,
one new type-3 on fa2 -> absorb -> R3(mA): sup 80,
disc=1, conf=0. confirmed=1. bar=bp2_bar_after(50,1,100)
=51. Hand-derived: bar 51, sup 80.
T2 (near-bar true positive): R7({mA,mB},51): 80 vs 60
-> mA. eff_at_commit=80. ev_observe(WBA,701,71,10) ->
ret 1, one new type-7 on fa1 -> absorb -> R2(mA,0):
sup 90, conf=1. confirmed=0, 80 < 2*51=102 -> bar 51.
Boosts: ev_observe(WBA,703,73,30) -> R2: sup 100;
ev_observe(WBA,704,74,40) -> R2: sup 110.
T3 (far-above-bar true positive): R7({mA,mB},51): 110
vs 60 -> mA. eff_at_commit=110. ev_observe(WBA,701,71,10)
-> R2: sup 120. confirmed=0, 110 >= 102 -> bar 50.
EXCL: mC=alloc_node, bp2_form(mC,1), bp2_revise(mC) ->
sup 50. R7({mC},51)==-3 (raised bar excludes); R7({mC},
50)==mC (old bar admitted).

## 3. Arm COMB: combiner alternatives (world WBC)

tnn2_init. t1,t2,w=alloc_node x3. bp2_form(t1,1),
bp2_form(t2,1), bp2_form(w,1).
2x bp2_confirm(t1,0): sup 120, conf 3, disc 0.
2x bp2_disconfirm(t2): sup 60, disc 2, conf 0.
2x bp2_disconfirm(w) then 1x bp2_confirm(w,0): sup 70.
z=alloc_node; type-14 edges z->t1, z->t2.
Hand-derived (targets 120/60):
- V-min: bp2_form(z,1); bp2_propagate(z) -> 60.
- V-max: bp2_form(z,1); bp6_cmax(z) -> 120.
- V-avg: bp2_form(z,1); bp6_cavg(z) -> (120+60)/2=90.
- V-wavg: bp2_form(z,1); bp6_cwavg(z): weights
  w1=3+0+1=4, w2=0+2+1=3; (120*4+60*3)/7=660/7=94
  (Zag i32 truncation).
No-invention check (result <= min target sup 60):
min 60 ok; max 120 violates; avg 90 violates; wavg 94
violates.
Selection right after each variant, R7({z,w},50):
min: 60 vs 70 -> w; max: 120 vs 70 -> z; avg: 90 vs 70
-> z; wavg: 94 vs 70 -> z. The combiner flips selection
on the same structure.

## 4. Arm EV: eviction interaction (world WG)

tnn2_init. fa1=ev_teach(701,71,10), fa2=ev_teach(702,72,20),
tags 2/6; m1=promote_graph(WG,-1,701,71,10,[fa1,fa2],2).
fb1=ev_teach(801,81,15), fb2=ev_teach(802,82,25), tags
2/6; m2=promote_graph(WG,-1,801,81,15,[fb1,fb2],2).
bp2_form(m1,0), bp2_form(m2,0); bp2_disconfirm(m2) -> 80.
Protect: for all live n != m1: link_edge(WG,m2,9,n,100).
h0=hg(WG,12). ev1=evict_node(WG) (the block's own
evictor, exactly one call).
Hand-derived: ev1==m1; ng(m1,36)==0; ng(m2,36)==1;
tombstone h1=hg(WG,12): h1!=h0, ng(h1,0)==3,
ng(h1,36)==1; belief record persists: hasb[m1]==1,
b_sup[m1]==100; R7({m1,m2},50)==m1 (stale: R7 has no
liveness gate); bp2_lgsel({m1,m2})==m2 (baseline skips
the dead node); then bp2_relicense(WG,bt,m1): type-1
licensing edges died with the node, live=0, formed=2 ->
bp2_retire reason 2: b_sup[m1]==0,
bp2_has_k3r(WG,m1,2)==1.

## 5. Arm CY5: 5-cycle (world WE)

tnn2_init. z1..z5=alloc_node, bp2_form(.,1) each:
sup 100. type-14: z1->z2, z2->z3, z3->z4, z4->z5,
z5->z1.
3x bp2_disconfirm(z3) -> 40.
R6(z2): targets {z3:40} -> 40; z1,z5,z4 stay 100 (no
cascade).
R6(z1) -> 40; R6(z5) -> 40; R6(z4) -> 40; R6(z3):
targets {z4:40} -> 40. All 40.
Re-apply R6 to z1..z5: all stay 40 (fixpoint,
idempotent).
Snap-up: 2x bp2_confirm(z5,1) -> 80; R6(z4): targets
{z5:80} -> 80.

## 6. Arm NST: nested cycles (world WN)

tnn2_init. zA,zB,zC,zD=alloc_node, bp2_form(.,1):
sup 100. type-14: zA->zB, zB->zC, zC->zA (triangle),
zB->zD, zD->zB (2-cycle nested on zB).
2x bp2_disconfirm(zD) -> 60.
R6(zB): targets {zC:100, zD:60} -> 60; zA,zC stay 100.
R6(zA) -> 60; R6(zC) -> 60; R6(zD) -> 60. All 60.
3x bp2_disconfirm(zD) -> 0.
R6(zB): min(60,0)=0 -> retire reason 2.
R6(zA) -> 0; R6(zC) -> 0; R6(zD) -> 0 (retired node zB
stays a live recorded target with sup 0, BP-5 C5
shape). All retired with reason-2 edges.

## 7. Kill bars (frozen)

Preconditions:
- PC-BA-FORM: b_sup[mA]==100 && b_ext[mA]==2 &&
  b_self[mA]==2 && b_sup[mB]==60.
- PC-COMB-FORM: b_sup[t1]==120 && b_conf[t1]==3 &&
  b_sup[t2]==60 && b_disc[t2]==2 && b_sup[w]==70.
- PC-EV-FORM: b_sup[m1]==100 && b_ext[m1]==1 &&
  b_self[m1]==1 && b_sup[m2]==80.
- PC-CY5-FORM: b_sup[z1..z5]==100 (all five).
- PC-NST-FORM: b_sup[zA]==100 && b_sup[zB]==100 &&
  b_sup[zC]==100 && b_sup[zD]==100.

BA bars:
- K-BA-U1..U5: unit values above (51/51/50/10/11).
- K-BA-T1: T1 selection==mA && bar==51 &&
  b_sup[mA]==80 && b_disc[mA]==1.
- K-BA-T2: T2 selection==mA && bar==51 &&
  b_sup[mA]==90.
- K-BA-T3: T3 selection==mA && bar==50 &&
  b_sup[mA]==120.
- K-BA-EXCL: R7({mC},51)==-3 && R7({mC},50)==mC.

COMB bars:
- K-COMB-MIN: V-min b_sup[z]==60.
- K-COMB-MAX: V-max b_sup[z]==120.
- K-COMB-AVG: V-avg b_sup[z]==90.
- K-COMB-WAVG: V-wavg b_sup[z]==94.
- K-COMB-NOINV: min result <= 60 (holds) &&
  max/avg/wavg results > 60 (each violates).
- K-COMB-SELDISC: sel_min==w && sel_max==z &&
  sel_avg==z && sel_wavg==z.

EV bars:
- K-EV-VICTIM: ev1==m1 && ng(WG,m1,36)==0 &&
  ng(WG,m2,36)==1.
- K-EV-TOMB: h1!=h0 && ng(WG,h1,0)==3 &&
  ng(WG,h1,36)==1.
- K-EV-PERSIST: hasb[m1]==1 && b_sup[m1]==100
  (H-persist holds; H-tombstone fails).
- K-EV-STALE: R7({m1,m2},50)==m1 (stale selection).
- K-EV-LGSEL: bp2_lgsel({m1,m2})==m2 (baseline skips
  dead node; discriminating pair with STALE).
- K-EV-R4: after bp2_relicense: b_sup[m1]==0 &&
  bp2_has_k3r(WG,m1,2)==1 (dormant detection path).

CY5 bars:
- K-CY5-WEAK: b_sup[z3]==40.
- K-CY5-1HOP: after R6(z2): b_sup[z2]==40 &&
  b_sup[z1]==100 && b_sup[z5]==100 && b_sup[z4]==100.
- K-CY5-FULL: after R6(z1),R6(z5),R6(z4),R6(z3): all
  five == 40.
- K-CY5-FIX: re-apply R6 to all five: all still 40.
- K-CY5-RAISE: after 2xR2(z5)+R6(z4): b_sup[z4]==80.

NST bars:
- K-NST-1HOP: after R6(zB): b_sup[zB]==60 &&
  b_sup[zA]==100 && b_sup[zC]==100.
- K-NST-CONV: after R6(zA),R6(zC),R6(zD): all == 60.
- K-NST-Z0B: after 3xR3(zD)+R6(zB): b_sup[zB]==0 &&
  bp2_has_k3r(WN,zB,2)==1.
- K-NST-ZALL: after R6(zA),R6(zC),R6(zD): b_sup 0/0/0
  && reason-2 edges on zA and zD.

Determinism and hygiene:
- K-DET: 3/3 runs byte-identical whole-output
  (SHA-256).
- K-HYG: pure Zag under safebin (`which python3` /
  `which python` empty at build and run); zero em/en
  dash bytes in lane files; 0 new edge types (1/3/7/9/
  14 frozen-and-pre-existing; 9 is block-native
  protection, 7 is block-written evidence, 16 unused
  this lane); 0 new node types (tags 1/3/20
  pre-existing); 0 modes, 0 bridges, 0 handlers;
  xf_block.zag SHA-256
  172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
  re-verified before and after the build;
  bp6_learner.zag byte-identical to bp5_learner.zag
  (SHA-256
  2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e);
  opaque identifiers.

Bar count: 5 PCs + 30 K bars + K-DET + K-HYG = 37.

## 8. Falsifiers (what kills the claim)

- BA: bar trajectory != hand-derived (any branch of
  bp2_bar_after misfires); R7 selection does not follow
  the moving bar; raised bar fails to exclude mC.
- COMB: any variant value != hand-derived; min violates
  no-invention (would overturn the "min is the
  conservative combiner" reading); selection does not
  flip with the combiner.
- EV: victim != m1 (protection targeting broken);
  H-tombstone holds instead of H-persist (record
  destroyed); R7 skips the dead MAP (no stale gap);
  R4 fails to retire (dormant path broken).
- CY5/NST: single R6 cascades; re-application changes
  values (oscillation); 5-cycle converges somewhere
  other than the min; nested 0 does not absorb.

## 9. Verdict rule

BP-6-PASS iff every PC bar and every K bar passes on
the frozen implementation, 3/3 byte-identical. A
single failed K bar fails its arm. This lane does not
re-open the 7 sealed predictions, does not change R6,
and adds no learner machinery.

## 10. Out of scope (not claimed)

Whether min should be replaced by another combiner in
the belief layer (comparison only; min stays frozen);
the disjunctive (OR-composite) reading of max, which
the layer cannot represent; a learner-owned
eviction-sync rule (measured only; persist-vs-tombstone
as a design choice is reasoned, not implemented);
d_self dynamics; per-belief bars; multi-channel
absorption.
