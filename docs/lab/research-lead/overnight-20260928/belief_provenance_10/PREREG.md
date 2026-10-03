# PREREG: BP-10 (belief revision under contradiction)

Worker: BELIEF-PROVENANCE-10 subagent, 2026-10-03. Non-ledger
task (claim minting paused); nothing minted.
Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_10/`
Status: FROZEN. Committed before any implementation file
exists in this lane. All predicted numbers below are
hand-derived from the frozen forms (BP-2 R1-R7, bp9_absorb
renamed) plus block behaviors probe-measured 2026-10-03 in
/tmp/bp10work (ephemeral; four probe binaries, pure Zag under
safebin). This lane tests task option 2 from the BP-9
suggested nexts: belief revision under contradiction. It does
not presuppose the pending governance decisions (#16
eviction-sync, #17 per-belief bars, #18 d_self recovery):
all worlds use current frozen semantics only.

## 0. What is being tested

The frozen belief layer has four things that could be
called "revision": R2/R3 in-place support adjustment,
the R5 operator bp2_revise (halves support, increments
b_rev, zeroes conf/disc), retirement (bp2_retire, kind-3
self-edge with reason, support zeroed), and retire+reform
(retire then bp2_form). Source audit shows bp2_revise has
ZERO callers in the frozen learner, the frozen block, and
the BP-9 driver: the R5 operator exists but no revision
rule invokes it. This lane measures, against frozen
predictions: (a) what contradictory evidence does to a
belief's record (genuine vs forged); (b) whether the belief
can recover and whether the record distinguishes genuine
from forged contradiction through a full
contradict-recover cycle; (c) whether a revision operation
distinct from retire+create exists anywhere the learner
can reach; (d) what the provenance record retains vs
erases about a revision history.

Threat model (same as BP-9): an adversary with the same
write access as the world harness (link_edge for arbitrary
edges). Adversary actions are driver-side test code, NOT
new learner machinery. Four arms: CON (contradiction
events), REC (recovery: genuine vs forged), REV (revision
operation vs retire+create), AMB (revision-history
erasure).

## 1. Researcher machinery (frozen, disclosed)

Belief layer: BP-9's bp9_learner.zag reused VERBATIM as
bp10_learner.zag (SHA-256 to be re-verified after copy;
expected
2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e):
record schema (8 u8), R1-R7, eff(), bp2_bar_after.
Constants: BASE=100, INC_HI=20, INC_LO=10, DEC=20,
BAR0=50, MIN_BAR=10.

New learner machinery this lane: NONE. In particular
bp10_absorb is the BP-9 absorb renamed (identical body:
n7>0 -> one R2 indep=0; n3>0 -> one R3; out carries
n7/n3); it is driver-side test-harness code, NOT a
belief-layer change. The forgery actions (link_edge
writes of type-7/type-3 edges) are adversary actions in
the driver, NOT belief-layer changes. Direct driver calls
to frozen learner functions (bp2_disconfirm,
bp2_confirm, bp2_revise, bp2_retire, bp2_form) are test
actions, disclosed per bar; they invoke frozen operators
and add no rules. R2/R3/R5/R6/R7, eff(), bp2_retire,
bp2_relicense stay frozen.

Test-harness code (in bp10_driver.zag, not belief
machinery): bp10_absorb, bp10_ck, bp10_bar,
bp10_selfcnt, world builders per arm, in-driver bars.

Block behaviors (probe-measured 2026-10-03,
/tmp/bp10work; frozen block SHA-256
172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a):
- P-BP10a: a genuine observation after a contradict on
  the same (s,r) is routed by activate-by-bid to the
  NEWEST fact node; the ORIGINAL fact node sees no new
  type-7 and no new type-3 (probe2: f1 n7/n3 unchanged;
  the observation took the contradict path on the new
  node, ret 0). The original fact is frozen: genuine
  same-fact recovery through the block is impossible.
- P-BP10b: contradict is one-shot per value; repeating
  with the same new value matches on the newest node
  (ret 1); the original fact is untouched (probe2).
- P-BP10c: promote_graph with 2 facts writes 2 type-1
  licensing edges; a genuine match on the second (fresh)
  fact lands on the ev_teach'd node (probe4-A: ret 1,
  f3b n7 0->1). Genuine recovery via a fresh licensed
  fact works end to end.
- P-BP10d: fresh ev_teach fact has n7=0, n3=0.
- P-BP10e: ev_observe match ret 1 (+1 type-7);
  contradict ret 0 (+1 type-3).
- P-BP10f: with a promote_graph belief licensing the
  fact, one genuine contradict writes EXACTLY ONE
  type-3 on the original fact node; revise_on_contradict
  surgery no-ops here (MAP field28 unchanged at 10,
  licensing edge intact, probe3).
- P-BP10g: bid(W,n) subtracts evcount(type-3). Two
  FORGED type-3s on f5 drop its bid to -2; a subsequent
  genuine match (ret 1) is routed to the internal
  promote_graph node (bid 0), NOT to f5 (probe4-B:
  f5 n7 stays 0). The block's routing is provenance
  blind: forged type-3s burn the fact's bid exactly
  like genuine ones.

Source facts (read from frozen code, not probed):
- S1: bp2_revise is defined at bp9_learner.zag line 84
  and has zero callers in the frozen learner, the
  frozen block, and the BP-9 driver (grep-verified).
- S2: bp2_confirm and bp2_disconfirm do not check
  kind-3 retirement edges or hasb: retirement gates
  nothing in the evidence path.
- S3: bp2_retire does not clear hasb; bp2_form sets
  hasb=1 and resets all 8 fields.

## 2. World construction and event sequences

CON world (fresh tnn2_init):
- fA1=ev_teach(901,91,10), field16=2;
  mA1=promote_graph(-1,901,91,10,[fA1],1).
- fA2=ev_teach(902,92,20), field16=2;
  mA2=promote_graph(-1,902,92,20,[fA2],1).
- fA3=ev_teach(903,93,30), field16=2;
  mA3=promote_graph(-1,903,93,30,[fA3],1).
- fA4=ev_teach(904,94,40), field16=2;
  mA4=promote_graph(-1,904,94,40,[fA4],1).
- bp2_form on all four, iscomp=0.

Event E1 (mA1, genuine contradict): ev_observe(901,91,999);
bp10_absorb(mA1,fA1,0,0).
Event E2 (mA2, forged contradict): link_edge(fA2,3,fA2,0);
bp10_absorb(mA2,fA2,0,0).
Event E3 (mA3, contradiction to zero): 5x {link_edge
(fA3,3,fA3,0); bp10_absorb(mA3,fA3,0,i)} with i=0..4
as the p3 watermark.
Event E4 (mA4, contradict saturation): 3x link_edge
(fA4,3,fA4,0); bp10_absorb(mA4,fA4,0,0) once.

REC world (fresh tnn2_init):
- fB1=ev_teach(911,91,10), field16=2;
  mB1=promote_graph(-1,911,91,10,[fB1],1).
- fB2=ev_teach(912,92,20), field16=2;
  mB2=promote_graph(-1,912,92,20,[fB2],1).
- fB3a=ev_teach(913,93,30), field16=2;
  fB3b=ev_teach(914,94,40), field16=2;
  mB3=promote_graph(-1,913,93,30,[fB3a,fB3b],2).
- fB4a=ev_teach(915,95,50), field16=2;
  fB4b=ev_teach(916,96,60), field16=2;
  mB4=promote_graph(-1,915,95,50,[fB4a,fB4b],2).
- fB5=ev_teach(917,97,70), field16=2;
  mB5=promote_graph(-1,917,97,70,[fB5],1).
- bp2_form on all five, iscomp=0.

Event R1 (mB1, genuine recovery blocked): ev_observe
(911,91,999); bp10_absorb(mB1,fB1,0,0); then
r1=ev_observe(911,91,10) [genuine match attempt];
bp10_absorb(mB1,fB1,0,1).
Event R2 (mB2, forged recovery on burned fact):
ev_observe(912,92,999); bp10_absorb(mB2,fB2,0,0);
then link_edge(fB2,7,fB2,0) [forged match];
bp10_absorb(mB2,fB2,0,1).
Event R3 (mB3, genuine contradict, genuine recovery on
fresh fact): ev_observe(913,93,999);
bp10_absorb(mB3,fB3a,0,0); then ev_observe(914,94,40);
bp10_absorb(mB3,fB3b,0,0).
Event R4 (mB4, forged contradict, genuine recovery on
fresh fact): link_edge(fB4a,3,fB4a,0);
bp10_absorb(mB4,fB4a,0,0); then ev_observe(916,96,60);
bp10_absorb(mB4,fB4b,0,0).
Event R5 (mB5, forged contradicts burn the bid): 2x
link_edge(fB5,3,fB5,0); bp10_absorb(mB5,fB5,0,0);
then r5=ev_observe(917,97,70) [genuine match attempt];
bp10_absorb(mB5,fB5,0,2).

REV world (fresh tnn2_init):
- fC1=ev_teach(921,91,10), field16=2;
  mC1=promote_graph(-1,921,91,10,[fC1],1).
- fC2=ev_teach(922,92,20), field16=2;
  mC2=promote_graph(-1,922,92,20,[fC2],1).
- fC3=ev_teach(923,93,30), field16=2;
  mC3=promote_graph(-1,923,93,30,[fC3],1).
- fC4a=ev_teach(924,94,40), field16=2;
  fC4b=ev_teach(925,95,50), field16=2;
  mC4=promote_graph(-1,924,94,40,[fC4a,fC4b],2).
- bp2_form on all four, iscomp=0.

Event V1 (mC1, R5 operator): ev_observe(921,91,999);
bp10_absorb(mC1,fC1,0,0); then driver calls
bp2_revise(bt,mC1) [disclosed test action invoking the
frozen operator; no rule is added].
Event V2 (mC2, retire+reform): ev_observe(922,92,999);
bp10_absorb(mC2,fC2,0,0); then bp2_retire(W,mC2,2);
then bp2_form(W,bt,hb,mC2,0).
Event V3 (mC3, full evidence cycle, no revise call):
ev_observe(923,93,30); bp10_absorb(mC3,fC3,0,0); then
ev_observe(923,93,999); bp10_absorb(mC3,fC3,1,0);
then bp2_retire(W,bt,mC3,2); then
bp2_form(W,bt,hb,mC3,0).
Event V4 (mC4, retired belief keeps learning):
ev_observe(924,94,999); bp10_absorb(mC4,fC4a,0,0);
then bp2_retire(W,bt,mC4,2); then
ev_observe(925,95,50); bp10_absorb(mC4,fC4b,0,0).

AMB world (fresh tnn2_init):
- zD1=alloc_node; zD2=alloc_node;
  bp2_form(zD1,1); bp2_form(zD2,1) [iscomp=1].
Event D1 (zD1): bp2_disconfirm, bp2_confirm,
bp2_disconfirm, bp2_confirm [direct frozen layer ops].
Event D2 (zD2): bp2_confirm, bp2_disconfirm,
bp2_disconfirm, bp2_confirm [direct frozen layer ops].

## 3. Kill bars (hand-derived)

Preconditions:
- PC-CON-FORM: mA1..mA4 have sup==100, conf==1,
  disc==0, rev==0, ext==1, self==0, formed==1,
  hasb==1.
- PC-REC-FORM: mB1,mB2,mB5 have sup==100, conf==1,
  ext==1, formed==1; mB3,mB4 have sup==100, conf==1,
  ext==2, formed==2; all hasb==1.
- PC-REV-FORM: mC1,mC2,mC3 have sup==100, conf==1,
  ext==1, formed==1; mC4 has ext==2, formed==2; all
  hasb==1.
- PC-AMB-FORM: zD1,zD2 have sup==100, conf==1,
  hasb==1.

CON bars:
- K-CON-GENUINE: after E1, absorb out n3==1,
  sup[mA1]==80, disc[mA1]==1, conf[mA1]==0.
  Derivation: one genuine type-3 (P-BP10e/f) -> one
  R3: 100-20=80, disc 0+1=1, conf zeroed.
- K-CON-FORGEIDENT: after E2, absorb out n3==1,
  sup[mA2]==80, disc[mA2]==1, conf[mA2]==0, and the
  (sup,conf,disc,rev) record equals mA1's.
  Derivation: one forged type-3 -> one R3, same
  arithmetic. The record cannot distinguish forged
  from genuine contradiction.
- K-CON-NORETIRE: after E3, sup[mA3]==0,
  disc[mA3]==5, conf[mA3]==0, hasb[mA3]==1,
  bp2_has_k3(mA3)==0. Derivation: five R3s,
  100-5*20=0 (floor), disc counts to 5; no rule
  maps contradiction to retirement (retire is only
  called by R4/R6 or explicitly). Contradiction,
  even to zero support, never retires the belief.
- K-CON-SAT: after E4, absorb out n3==3,
  sup[mA4]==80, disc[mA4]==1, conf[mA4]==0.
  Derivation: three forged type-3s, one absorb ->
  per-channel single application, ONE R3 (the
  contradict-side twin of BP-8 K-MCH-SAT). The
  record hides the true forged multiplicity.

REC bars:
- K-REC-GENBLOCKED: after R1's match attempt, absorb
  out n7==0 and n3==0, sup[mB1]==80, disc[mB1]==1,
  conf[mB1]==0. Derivation: P-BP10a, the block
  routes the post-contradict observation to the
  newest node; fB1 sees no new edges; no rule fires;
  the record is unchanged. Genuine same-fact recovery
  through the block is impossible.
- K-REC-FORGED: after R2's forged match, absorb out
  n7==1, sup[mB2]==90, conf[mB2]==1, disc[mB2]==0.
  Derivation: the forged type-7 bypasses block
  routing (direct edge write); absorb counts it;
  one R2 indep=0: 80+10=90, conf 1, disc zeroed.
  On a burned fact the ONLY same-fact recovery path
  is forged; the layer applies R2 without question.
- K-REC-IDENT-C: after the contradict step of R3/R4,
  sup[mB3]==80 and sup[mB4]==80, disc==1 both,
  conf==0 both. Derivation: one R3 each, genuine
  (P-BP10f) and forged alike.
- K-REC-IDENT-R: after the recovery step of R3/R4,
  sup[mB3]==90 and sup[mB4]==90, conf==1 both,
  disc==0 both. Derivation: one genuine R2 each on
  the fresh fact (P-BP10c). Through a full
  contradict-recover cycle the records are identical:
  the learner cannot distinguish genuine from forged
  contradiction, even in recovery.
- K-REC-FORGEBURN: after R5's match attempt,
  r5==1, absorb out n7==0 and n3==0, sup[mB5]==80,
  disc[mB5]==1. Derivation: P-BP10g, the two forged
  type-3s drop fB5's bid to -2; the block routes the
  genuine match (ret 1) to the internal node; fB5's
  absorb sees nothing. Forged type-3s burn the
  fact's routing exactly like genuine ones: the
  BLOCK is provenance-blind too.

REV bars:
- K-REV-OP: after V1, sup[mC1]==40, rev[mC1]==1,
  conf[mC1]==0, disc[mC1]==0, bp2_has_k3(mC1)==0,
  hasb[mC1]==1. Derivation: bp2_revise halves
  support (80/2=40), increments b_rev, zeroes
  conf/disc, writes no reason edge. The operator
  works as specified.
- K-RETREFORM: after V2, sup[mC2]==100,
  conf[mC2]==1, disc[mC2]==0, rev[mC2]==0,
  bp2_has_k3r(mC2,2)==1. Derivation: retire zeroes
  sup and writes the reason-2 self-edge; reform
  resets all fields (S3). The retire record persists
  across reform.
- K-REV-DISTINCT: sup[mC1]==40 and rev[mC1]==1 and
  bp2_has_k3(mC1)==0 and sup[mC2]==100 and
  rev[mC2]==0 and bp2_has_k3r(mC2,2)==1.
  Derivation: conjunction of the two measured end
  states. The record CAN distinguish a revision
  from retire+reform (halved support + rev counter
  + no reason edge vs reset support + reason edge):
  if a revision rule existed, its trace would be
  visible. It is not.
- K-REV-UNREACH: after V3, rev[mC3]==0.
  Derivation: S1, bp2_revise has zero callers in the
  frozen code; the exercised evidence paths (R1
  form, R2, R3, retire, reform) never invoke it.
  The revision operator is dead machinery: no
  revision rule exists in the frozen layer.
- K-RET-NOGATE: after V4, sup[mC4]==10,
  conf[mC4]==1, disc[mC4]==0,
  bp2_has_k3r(mC4,2)==1. Derivation: S2,
  bp2_confirm checks no retirement state; the
  genuine match on the fresh fact applies R2 to
  the retired belief (0+10=10, conf 1). Retirement
  does not gate evidence absorption: a retired
  belief keeps revising while its retire record
  persists.

AMB bars:
- K-REV-AMBIG: sup[zD1]==80 and sup[zD2]==80,
  conf[zD1]==1 and conf[zD2]==1, disc==0 both,
  rev==0 both. Derivation: D1: 100->80->90->70->80,
  conf 1->0->1->0->1, disc ends 0; D2:
  100->110->90->70->80, conf 1->2->0->0->1, disc
  ends 0. R2 zeroes disc, R3 zeroes conf, so only
  the trailing run and the net support change
  survive. Two different contradiction timings give
  the identical record: the provenance record
  erases WHEN the contradiction happened.

In-driver total: 4 PC + 15 kill = 19.

## 4. Determinism and hygiene bars

- K-DET: 3/3 runs of bp10_bin byte-identical
  (SHA-256 recorded in REPORT.md after the runs).
- K-HYG: pure Zag under safebin (`which python3` /
  `which python` empty at build and run); zero
  em/en dash bytes in all authored lane files and
  run outputs; 0 new edge types (1/3/7/14 all
  pre-existing in the block; kind-3 self-edges
  pre-exist via bp2_retire); 0 new node types
  (tags 1/3/20 pre-existing); 0 modes, 0 bridges,
  0 handlers, 0 semantic cases; frozen block
  SHA-256 unchanged
  (172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a);
  bp10_learner.zag byte-identical to bp9_learner.zag
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
