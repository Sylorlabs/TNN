# PREREG: BP-11 (cross-belief interaction beyond shared-fact scoping)

Worker: BELIEF-PROVENANCE-11 subagent, 2026-10-03. Non-ledger
task (claim minting paused); nothing minted.
Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_11/`
Status: FROZEN. Committed before any implementation file
exists in this lane. All predicted numbers below are
hand-derived from the frozen forms (BP-2 R1-R7, bp10_absorb
renamed) plus block behaviors read from the frozen source
(activate/bid/ev_observe/ev_teach/promote_graph, bid
arithmetic counted by hand from the driver's own edge
writes) and probe-measured in BP-10 (/tmp/bp10work:
P-BP10a post-contradict observation routed away from the
original fact; P-BP10e match ret 1 / contradict ret 0;
P-BP10f revise_on_contradict no-ops on promote_graph MAPs;
P-BP10g bid subtracts evcount(type-3), forged type-3s burn
routing like genuine ones). This lane tests task option 3
from the BP-10 suggested nexts: cross-belief interaction
beyond the shared-fact scoping measured in BP-9
(K-FORGE-SHARED: evidence non-rivalrous across beliefs
sharing a fact; K-FORGE-BLAST: forged edge blast radius 2
from one shared fact). It does not presuppose the pending
governance decisions (#16 eviction-sync, #17 per-belief
bars, #18 d_self recovery): all worlds use current frozen
semantics only, no eviction pressure anywhere, one fixed
bar in selection calls, no d_self manipulation.

## 0. What is being tested

Hypothesis H-BP11: cross-belief interaction in the frozen
belief layer plus the frozen block is exactly scoped to
three channels: (1) shared-fact evidence edges (BP-9
SHARED/BLAST); (2) type-14 structural edges via R6
propagation (bp2_propagate); (3) shared-(s,r) bid routing
at the block (activate-by-bid). Beliefs with disjoint
facts, no type-14 path between them, and disjoint (s,r)
do not interact: one belief's R2/R3/retire/propagate/absorb
never moves another belief's record or eff. R7 selection
couples outcomes at the call site only, never records.

Three arms, fresh world each (PROP/ROUTE share nothing;
NULL is separate):

- PROP: R6 coupling between beliefs that share no fact
  and no (s,r). Composite z1 with driver-written type-14
  edges to m1, m2 (disjoint facts, disjoint (s,r)); m3 a
  third belief with no type-14 path to z1. Tests that the
  coupling exists (P1), is asymmetric target->composite
  (P2), is scoped to the type-14 adjacency (P3), is fixed
  in direction by edge direction (P4), and tracks the min
  live target in both directions (P5).
- ROUTE: block bid-routing theft between beliefs that
  share an (s,r) but share no fact node. mA over
  fA=(921,91,10), mB over fB=(921,91,20): distinct fact
  nodes, same (s,r) namespace. fB's bid is inflated with
  forged type-7s (adversary action, same threat model as
  BP-9/BP-10). A genuine observation matching mA's fact
  is routed by activate-by-bid to fB, where it becomes a
  contradict against mB. Control world without mB shows
  the observation reaches mA; a disjoint-(s,r) belief mC
  in the same world shows the theft is (s,r)-scoped.
- NULL: boundary bars for beliefs with disjoint facts,
  no type-14 path, disjoint (s,r): one's forged
  contradicts do not leak into another's absorb (N1);
  one's retirement gates nothing for another (N2);
  one's provenance death does not touch another's
  licensing counts (N3); selection couples outcomes, not
  records (N4).

Threat model (same as BP-9/BP-10): an adversary with the
same write access as the world harness (link_edge for
arbitrary edges). Adversary actions are driver-side test
code, NOT new learner machinery. Direct driver calls to
frozen learner functions (bp2_disconfirm, bp2_confirm,
bp2_retire, bp2_form, bp2_propagate, bp2_kill_one_prov,
bp2_relicense, bp2_select, bp2_eff, bp2_lic_live) are
disclosed test actions invoking frozen operators; they
add no rules. The driver-written type-14 edges in PROP
are test setup for the frozen R6 rule, exactly as in
BP-9 CHAIN.

## 1. Researcher machinery (frozen, disclosed)

Belief layer: BP-10's bp10_learner.zag reused VERBATIM as
bp11_learner.zag (SHA-256 to be re-verified after copy;
expected
2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e):
record schema (8 u8), R1-R7, eff(), bp2_bar_after.
Constants: BASE=100, INC_HI=20, INC_LO=10, DEC=20,
BAR0=50, MIN_BAR=10.

New learner machinery this lane: NONE. In particular
bp11_absorb is the BP-10 absorb renamed (identical body:
n7>0 -> one R2 indep=0; n3>0 -> one R3; out carries
n7/n3); it is driver-side test-harness code, NOT a
belief-layer change. The forgery actions (link_edge
writes of type-7/type-3 edges) are adversary actions in
the driver, NOT belief-layer changes. The type-14 edges
in PROP are driver-written test setup for the frozen R6
rule, NOT belief-layer changes.

Test-harness code (in bp11_driver.zag, not belief
machinery): bp11_absorb, bp11_ck, bp11_bar,
bp11_selfcnt, bp11_liclive (thin wrapper over frozen
bp2_lic_live), world builders per arm, in-driver bars.

Block behaviors (frozen source, hand-derived bid counts;
BP-10 probe citations where the behavior was measured):
- B-BP11a: activate(W,s,r) scans live non-superseded
  tag-1 nodes with field20==s and field24==r and picks
  the strictly highest bid(W,n); ties keep the lowest
  node id (strict > in the scan). bid(W,n) =
  evcount(1)+evcount(2)+evcount(6)+evcount(7)
  -evcount(3) over edges with to==n, plus type-10
  inbound neighbor terms (none in these worlds).
- B-BP11b: a promote_graph MAP contributes exactly one
  type-1 edge to its fact's bid (the licensing edge,
  from==MAP, to==fact). The MAP's own self-edges
  (type 2/6/13) do not touch the fact's bid. The
  promote_graph-internal ev_teach_in node has bid 0
  (no inbound edges).
- B-BP11c: forged type-7 self-edges add +1 each to the
  fact's bid and do NOT supersede the fact
  (is_superseded needs a type-3 self-edge). So a fact
  with k forged type-7s and one licensing type-1 has
  bid 1+k and stays a live activation candidate.
- B-BP11d: ev_observe on the contradict path writes
  exactly one type-3 self-edge on the ACTIVATED node
  (P-BP10e/f), runs revise_on_contradict (no-op here:
  no tag-101 cells, P-BP10f), allocates a tag-3 history
  node, and ev_teach_in's a new (s,r,o) node (bid 0).
  Returns 0. On the match path it writes one type-7
  self-edge on the activated node and returns 1
  (P-BP10e). ref_prot only refreshes type-9 clocks.
- B-BP11e: bp2_propagate(z) reads edges from==z with
  type==14, takes the min support over targets that are
  live (ng 36==1) and have hasb==1, writes it to
  bt[z*8], and returns the min (255 when no recorded
  target). Targets' records are not written.
- B-BP11f: bp2_select over candidates computes each
  eff independently (pure function of that belief's own
  8 fields), returns -3 on an exact tie at the top or
  when max eff < bar. The comparison is the only
  cross-candidate coupling in the call.

Source facts (read from frozen code, not probed):
- S1: bp2_confirm/bp2_disconfirm write only the
  target belief's 8 fields; bp11_absorb counts only
  self-edges on the named fact (bp11_selfcnt filters
  from==fid and to==fid). No cross-fact reads exist in
  the absorb path.
- S2: bp2_retire writes a kind-3 self-edge and zeroes
  the target's support only; bp2_kill_one_prov and
  bp2_relicense walk only the named belief's type-1
  edges.

## 2. World construction and event sequences

PROP world (fresh tnn2_init):
- f1=ev_teach(931,91,10), field16=2;
  m1=promote_graph(-1,931,91,10,[f1],1).
- f2=ev_teach(932,92,20), field16=2;
  m2=promote_graph(-1,932,92,20,[f2],1).
- f3=ev_teach(933,93,30), field16=2;
  m3=promote_graph(-1,933,93,30,[f3],1).
- z1=alloc_node; bp2_form(z1,1) [iscomp=1].
- link_edge(z1,14,m1,0); link_edge(z1,14,m2,0)
  [driver-written test setup for frozen R6].
- bp2_form on m1/m2/m3, iscomp=0.
No two beliefs share a fact; all three (s,r) differ;
m3 has no type-14 path to or from z1.

Event P1 (couple): 3x bp2_disconfirm(m2);
rp1=bp2_propagate(z1).
Event P2 (asymmetry): no new actions; read m1/m2
records after P1.
Event P3 (scope): 2x bp2_confirm(m3,1);
rp2=bp2_propagate(z1).
Event P4 (direction): rp3=bp2_propagate(m1).
Event P5 (track): 3x bp2_confirm(m2,1);
rp4=bp2_propagate(z1).

ROUTE world (fresh tnn2_init):
- fA=ev_teach(921,91,10), field16=2;
  mA=promote_graph(-1,921,91,10,[fA],1).
- fB=ev_teach(921,91,20), field16=2;
  mB=promote_graph(-1,921,91,20,[fB],1).
- fC=ev_teach(941,91,10), field16=2;
  mC=promote_graph(-1,941,91,10,[fC],1).
- bp2_form on all three, iscomp=0.
mA and mB share the (s,r) namespace (921,91) but no
fact node; mC is disjoint on (941,91).

Event R1 (theft): 3x link_edge(fB,7,fB,0) [forged
matches, adversary action]; bp11_absorb(mB,fB,0,0);
then rc=ev_observe(921,91,10) [genuine observation
matching mA's fact value]; bp11_absorb(mA,fA,0,0);
bp11_absorb(mB,fB,3,0).
Event R2 (control, separate fresh world WR2):
fA2=ev_teach(921,91,10), field16=2;
mA2=promote_graph(-1,921,91,10,[fA2],1);
bp2_form(mA2,0); rc2=ev_observe(921,91,10);
bp11_absorb(mA2,fA2,0,0).
Event R3 (bound, back in the ROUTE world after R1):
rc3=ev_observe(941,91,10); bp11_absorb(mC,fC,0,0).

NULL world (fresh tnn2_init):
- fD=ev_teach(951,91,10), field16=2;
  mD=promote_graph(-1,951,91,10,[fD],1).
- fE=ev_teach(952,92,20), field16=2;
  mE=promote_graph(-1,952,92,20,[fE],1).
- fF=ev_teach(961,91,10), field16=2;
  mF=promote_graph(-1,961,91,10,[fF],1).
- fG=ev_teach(962,92,20), field16=2;
  mG=promote_graph(-1,962,92,20,[fG],1).
- bp2_form on all four, iscomp=0.
All (s,r) disjoint; no shared facts; no type-14 edges.

Event N1 (absorb isolation): 3x link_edge(fE,3,fE,0)
[forged contradicts on mE's fact]; 1x
link_edge(fD,7,fD,0) [forged match on mD's fact];
bp11_absorb(mD,fD,0,0); bp11_absorb(mE,fE,0,0).
Event N2 (retire gates nothing): bp2_retire(mE,2);
rcD=ev_observe(951,91,10) [genuine match on mD's
fact]; bp11_absorb(mD,fD,1,0);
sel1=bp2_select([mD,mE],50).
Event N3 (provenance death is per-belief):
kf=bp2_kill_one_prov(mE); lvD=bp11_liclive(mD);
bp2_relicense(mE).
Event N4 (selection couples outcomes only):
selA=bp2_select([mF,mG],50);
bp2_confirm(mG,1); selB=bp2_select([mF,mG],50).

## 3. Kill bars (hand-derived)

Preconditions:
- PC-PROP-FORM: sup==100 for z1,m1,m2,m3; m1/m2/m3
  have conf==1, ext==1, formed==1; hasb==1 for all
  four.
- PC-ROUTE-FORM: mA/mB/mC have sup==100, conf==1,
  ext==1, formed==1, hasb==1.
- PC-NULL-FORM: mD/mE/mF/mG have sup==100, conf==1,
  ext==1, formed==1, hasb==1.

PROP bars (R6 without shared facts):
- K-PROP-COUPLE: after P1, rp1==40 and sup[z1]==40,
  conf[z1]==1, disc[z1]==0, rev[z1]==0,
  bp2_has_k3(z1)==0. Derivation: 3x R3 on m2:
  100-3*20=40, disc 3, conf 0; propagate takes
  min(100,40)=40 over the two type-14 targets and
  writes only z1's support. A belief's support moves
  another belief's record with no shared fact.
- K-PROP-ASYM: after P1, sup[m1]==100, conf[m1]==1,
  disc[m1]==0, rev[m1]==0, and sup[m2]==40,
  conf[m2]==0, disc[m2]==3, rev[m2]==0. Derivation:
  B-BP11e, propagate writes the composite only; the
  targets' records are untouched. The coupling is
  asymmetric: target->composite, never back.
- K-PROP-SCOPE: after P3, rp2==40 and sup[z1]==40
  and sup[m3]==140 and conf[m3]==3. Derivation: 2x
  R2 indep=1 on m3: 100+2*20=140, conf 3; m3 is not
  a type-14 target of z1, so re-propagation still
  reads min(100,40)=40; m3's own record keeps its
  140. The propagation blast radius is exactly the
  type-14 adjacency.
- K-PROP-NOBACK: after P4, rp3==255 and
  sup[m1]==100, conf[m1]==1, disc[m1]==0,
  rev[m1]==0. Derivation: B-BP11e, m1 has no
  type-14 out-edges, so propagate returns 255 and
  writes nothing. The z1->m1 edge couples z1 to m1,
  never m1 to z1: direction is fixed by edge
  direction.
- K-PROP-TRACK: after P5, rp4==100 and
  sup[z1]==100 and sup[m2]==100, conf[m2]==3,
  disc[m2]==0. Derivation: 3x R2 indep=1 on m2:
  40+3*20=100, conf 3, disc zeroed by R2;
  propagate reads min(100,100)=100. The composite
  tracks the min live target in both directions.

ROUTE bars (bid routing without shared facts):
- K-ROUTE-THEFT: after R1, rc==0,
  absorb(mA,fA) out n7==0 and n3==0, sup[mA]==100,
  conf[mA]==1, disc[mA]==0,
  bp11_selfcnt(fA,7)==0, bp11_selfcnt(fA,3)==0,
  absorb(mB,fB) out n7==0 and n3==1, sup[mB]==90,
  conf[mB]==0, disc[mB]==1. Derivation: B-BP11a/c,
  bid(fB)=1+3=4 beats bid(fA)=1 (licensing type-1)
  and the bid-0 internal nodes, so the genuine
  observation matching mA's fact value activates
  fB; field28 20 != 10 takes the contradict path
  (B-BP11d, P-BP10e): one type-3 on fB, ret 0,
  revise_on_contradict no-ops (P-BP10f). fA sees
  zero new edges, so mA's absorb fires no rule and
  mA's record is unchanged; mB's absorb sees the
  one new type-3: one R3, 110-20=90, disc 1, conf
  zeroed. mB's bid dominance converts mA's
  confirming evidence into mB's disconfirmation,
  with no shared fact between the beliefs.
- K-ROUTE-CONTROL: after R2, rc2==1,
  absorb(mA2,fA2) out n7==1, sup[mA2]==110,
  conf[mA2]==2, disc[mA2]==0. Derivation: without
  mB, activate sees fA2 (bid 1, the licensing
  type-1) vs the bid-0 internal node; fA2 wins,
  field28 10==10 takes the match path (P-BP10e):
  one type-7, ret 1; one R2 indep=0: 100+10=110,
  conf 2. The theft requires mB's bid dominance.
- K-ROUTE-BOUND: after R3, rc3==1, sup[mC]==110,
  conf[mC]==2, sup[mA]==100, sup[mB]==90.
  Derivation: (941,91) candidates are fC (bid 1)
  and its bid-0 internal node only; fC wins, match
  path, one R2 on mC. mA and mB are untouched by
  the (941,91) observation. The routing channel is
  (s,r)-scoped: bid dominance over (921,91) does
  not leak into (941,91).

NULL bars (no fourth channel):
- K-NULL-CONFIRM: after N1, absorb(mD,fD) out
  n7==1, sup[mD]==110, conf[mD]==2, and
  absorb(mE,fE) out n3==3, sup[mE]==80,
  disc[mE]==1, conf[mE]==0. Derivation: S1, each
  absorb counts only self-edges on its own fact:
  one R2 indep=0 on mD (100+10=110, conf 2),
  per-channel single R3 on mE (100-20=80, disc 1,
  conf 0) despite n3==3. mE's three forged
  contradicts do not leak into mD's counts.
- K-NULL-RETIRE: after N2, rcD==1, sup[mD]==120,
  conf[mD]==3, bp2_has_k3r(mE,2)==1, sup[mE]==0,
  sel1==mD. Derivation: S2, retire touches only
  mE; the genuine match on (951,91) activates fD
  (bid 2: licensing type-1 + forged type-7) and
  writes one type-7; mD's absorb with p7=1 sees
  n7==1: one R2, 110+10=120, conf 3. Retirement
  of mE gates nothing for mD; selection over
  [mD,mE] with bar 50 picks mD on eff (120 vs 0).
- K-NULL-PROVKILL: after N3, kf==fE, lvD==1,
  b_ext[mD]==1, sup[mD]==120,
  bp2_has_k3r(mE,2)==1. Derivation: S2,
  bp2_kill_one_prov walks only mE's type-1 edges
  and kills fE; mD's live licensing count is still
  1 and its table fields (b_ext 1, sup 120) are
  untouched; relicense retires mE on reason 2
  (formed 1, live 0). Provenance death is
  per-belief.
- K-NULL-SELECT: after N4, selA==-3, selB==mG,
  sup[mF]==100, conf[mF]==1, bp2_eff(mF)==100.
  Derivation: B-BP11f, eff is a pure function of
  each belief's own fields: 100/100 ties at the
  top -> -3; after one R2 indep=1 on mG
  (100+20=120, conf 2), mG wins outright while
  mF's record and eff are unchanged. Selection
  couples outcomes at the call site; records stay
  independent.

In-driver total: 3 PC + 12 kill = 15.

## 4. Determinism and hygiene bars

- K-DET: 3/3 runs of bp11_bin byte-identical
  (SHA-256 recorded in REPORT.md after the runs).
- K-HYG: pure Zag under safebin (`which python3` /
  `which python` empty at build and run); zero
  em/en dash bytes in all authored lane files and
  run outputs; 0 new edge types (1/3/7/14 all
  pre-existing; kind-3 self-edges pre-exist via
  bp2_retire); 0 new node types (tags 1/3/20
  pre-existing); 0 modes, 0 bridges, 0 handlers,
  0 semantic cases; frozen block SHA-256 unchanged
  (172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a);
  bp11_learner.zag byte-identical to bp10_learner.zag
  (SHA-256
  2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e);
  opaque identifiers throughout.
- F-VOID: void on sight if any Python/C/JS/Rust
  interpreter or compiler beyond the pinned znc is
  invoked. (Not a kill bar: a tripwire.)

## 5. Amendment log

5a. Pre-implementation: none. This prereg is
frozen as committed.

5b. Post-run amendments: (to be filled only if a
run exposes a prereg error; any change records the
re-derivation here and no frozen rule is changed
to chase a bar.)
