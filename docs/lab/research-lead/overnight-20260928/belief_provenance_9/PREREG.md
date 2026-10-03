# PREREG: BP-9 (provenance chain integrity under adversarial corruption)

Worker: BELIEF-PROVENANCE-9 subagent, 2026-10-03. Non-ledger
task (claim minting paused); nothing minted.
Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_9/`
Status: FROZEN. Committed before any implementation file
exists in this lane. All predicted numbers below are
hand-derived from the frozen forms (BP-2 R1-R7, bp8_absorb
renamed) plus block behaviors probe-measured 2026-10-03 in
/tmp/bp9probe (ephemeral; one probe binary, pure Zag under
safebin). The 7 falsifiable predictions (FP1-FP7) stay
sealed; this lane tests provenance chain integrity, the
first of the three options in the task brief. It does not
presuppose the pending governance decisions (#16
eviction-sync, #17 per-belief bars, #18 d_self recovery):
all worlds use current frozen semantics only.

## 0. What is being tested

The belief layer's provenance record has three parts: the
learner-owned table bt[] (b_sup/b_conf/b_disc/b_rev/
b_ext/b_self/d_self/formed per belief), the reason edges
(kind-3 self-edges on MAP nodes, field12 = reason code,
written by bp2_retire), and the evidence edges (type-7
match and type-3 contradict self-edges on fact nodes,
written by the block's ev_observe). Absorption
(bp8_absorb) derives record updates from edge counts
since caller-held watermarks; it never verifies how an
edge was written.

Threat model: an adversary with the same write access
as the world harness (link_edge for arbitrary edges,
direct bt[] writes). The adversary is driver-side test
code, NOT new learner machinery. Two arms:

- FORGE (direct edge forgery vs the evidence record):
  the adversary writes type-7 / type-3 self-edges with
  link_edge, bypassing ev_observe, then the frozen
  absorb runs. Predicted: (a) a forged type-7 absorbs
  to sup 110/conf 2, record-identical to a genuine
  single match, so the record cannot distinguish
  forged from block-mediated evidence; (b) a forged
  type-3 absorbs to sup 80/disc 1/conf 0,
  record-identical to a genuine contradict from
  formation; (c) a forged type-7 written on an
  already-contradicted fact IS absorbed (n7==1),
  bypassing the block's one-shot protection that
  drops genuine post-contradict matches (BP-7 probe,
  BP-8 K-MCH-ORD): the resulting 90/1/0 record is
  unreachable by any genuine ev_observe path; (d)
  three forged type-7s saturate to ONE R2 (sup 110,
  conf 2, n7==3): the per-channel single-application
  rule caps per-absorb forgery impact, the same
  saturation genuine multiplicity gets (BP-8
  K-MCH-SAT); (e) re-running absorb with stale
  watermarks re-applies the forged edges (sup 120,
  conf 3): no replay protection exists, watermarks
  are caller-held; (f) two beliefs licensing one
  shared fact each independently count the same
  genuine type-7 (sup 110 both): evidence is
  non-rivalrous, no cross-belief watermark
  consumption; (g) one forged type-7 on the shared
  fact corrupts BOTH beliefs (sup 120 both): blast
  radius 2 from a single forged edge.

- CHAIN (record completeness and tamper-evidence):
  (a) R6 propagation changes a composite's support
  with no reason edge and no counter movement, so
  the composite's record cannot attribute the change
  to its source; (b) a forged kind-3 self-edge with
  a novel reason code (9) is queryable exactly like
  a genuine retire record, and coexists with a later
  genuine reason-2 retire: the reason record is
  ambiguous and the layer has no resolution
  mechanism; (c) direct bt[] tampering (resurrecting
  a retired belief's support to 100) is followed by
  the layer without question: eff returns 100 and
  R7 selects the retired belief while its genuine
  reason-2 retirement edge is still present; (d)
  after fact death the table's licensing counts go
  stale (b_ext stays 1, live licensing 0) until an
  explicit bp2_relicense, which still retires
  reason-2 when triggered: the dormant R4 detection
  from BP-6 works, measured without presupposing
  the #16 design decision.

## 1. Researcher machinery (frozen, disclosed)

Belief layer: BP-8's bp8_learner.zag reused VERBATIM
as bp9_learner.zag (SHA-256
2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e,
re-verified after copy): record schema (8 u8),
R1-R7, eff(), bp2_bar_after. Constants: BASE=100,
INC_HI=20, INC_LO=10, DEC=20, BAR0=50, MIN_BAR=10.

New learner machinery this lane: NONE. In
particular bp9_absorb is the BP-8 absorb renamed
(identical body: n7>0 -> one R2 indep=0; n3>0 ->
one R3; out carries n7/n3); it is driver-side
test-harness code, NOT a belief-layer change. The
forgery actions (link_edge writes of type-7/type-3/
kind-3 edges, direct bt[] writes) are adversary
actions in the driver, NOT belief-layer changes.
R2/R3/R5/R6/R7, eff(), bp2_retire, bp2_relicense
stay frozen.

Test-harness code (in bp9_driver.zag, not belief
machinery): bp9_absorb, bp9_ck, bp9_bar,
bp9_selfcnt, bp9_allsup, bp9_liclive (thin wrapper
reading bp2_lic_live's out[0]), world builders per
arm, in-driver bars.

Block behaviors (probe-measured 2026-10-03,
/tmp/bp9probe; frozen block SHA-256
172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a):
- P1a: two promote_graph calls on one shared fact
  return distinct MAP ids (mP=3, mQ=5), each with
  exactly one type-1 licensing edge to the fact.
- P1b: ev_observe match on the shared fact: ret 1,
  +1 type-7 self-edge.
- P1c: a link_edge type-7 self-edge on a fact is
  counted by the self-edge census (n7 1->2).
- P1d: a link_edge kind-3 self-edge with field12=9
  on a MAP is found by the reason-code query.
- Prior frozen facts reused: genuine contradict is
  one-shot (first ret 0 + one type-3; repeats add
  nothing); a genuine match after a contradict on
  the same fact is dropped by the block (n7==0,
  BP-7 probe, BP-8 K-MCH-ORD); per-channel absorb
  saturation (n7=2 -> one R2, BP-8 K-MCH-SAT);
  bp2_form sets conf=1; R2 zeroes disc; R3 zeroes
  conf; bp2_retire writes kind-3 self-edge and
  zeroes sup without checking existing k3 edges;
  eff() with ext+self==0 returns support directly.

Disclosure: reason code 9 is a novel field12 VALUE
used only as the forgery marker in K-CHAIN-
FORGEREASON / K-CHAIN-DOUBLEK3. It is not a new
edge type (kind 3 pre-exists), not a new node
type, not a mode/bridge/handler, not a semantic
case: no layer code branches on it.

## 2. World construction and event sequences

FORGE world (fresh tnn2_init):
- fA=ev_teach(701,71,10), field16=2; mA=
  promote_graph(-1,701,71,10,[fA],1).
- fB=ev_teach(702,72,20), field16=2; mB=
  promote_graph(-1,702,72,20,[fB],1).
- fC=ev_teach(703,73,30), field16=2; mC=
  promote_graph(-1,703,73,30,[fC],1).
- fD=ev_teach(704,74,40), field16=2; mD=
  promote_graph(-1,704,74,40,[fD],1).
- fS=ev_teach(705,75,50), field16=2; mP=
  promote_graph(-1,705,75,50,[fS],1); mQ=
  promote_graph(-1,705,75,50,[fS],1).
- bp2_form on all six, iscomp=0.

Event F1 (mA): link_edge(fA,7,fA,0); then
bp9_absorb(mA,fA,p7=0,p3=0).
Event F2 (mB): link_edge(fB,3,fB,0); then
bp9_absorb(mB,fB,0,0).
Event F3 (mC): ev_observe(703,73,999) [genuine
contradict]; bp9_absorb(mC,fC,0,0); then
link_edge(fC,7,fC,0) [forged match on the
contradicted fact]; bp9_absorb(mC,fC,0,1).
Event F4 (mD): 3x link_edge(fD,7,fD,0);
bp9_absorb(mD,fD,0,0).
Event F5 (mD replay): bp9_absorb(mD,fD,0,0)
again with the same stale watermarks.
Event F6 (mP/mQ): ev_observe(705,75,50) [genuine
match on the shared fact]; bp9_absorb(mP,fS,0,0);
bp9_absorb(mQ,fS,0,0).
Event F7 (mP/mQ): link_edge(fS,7,fS,0) [one forged
type-7 on the shared fact]; bp9_absorb(mP,fS,1,0);
bp9_absorb(mQ,fS,1,0).

CHAIN world (fresh tnn2_init):
- z1=alloc_node; z2=alloc_node;
  bp2_form(z1,1); bp2_form(z2,1) [iscomp=1:
  sup 100, conf 1, ext 0, self 0, formed 0].
- link_edge(z1,14,z2,0).
- fE=ev_teach(706,76,60), field16=2; mE=
  promote_graph(-1,706,76,60,[fE],1);
  bp2_form(mE,0).

Event C1: 3x bp2_disconfirm(z2); bp2_propagate(z1).
Event C2: 2x bp2_confirm(z2,1); bp2_propagate(z1).
Event C3: link_edge(z2,3,z2,9); then
bp2_retire(z2,2).
Event C4: bp2_retire(z1,2); then bt[z1*8]=100
[direct table tamper]; bp2_eff(z1);
bp2_select over [z1] with bar 50.
Event C5: bp2_kill_one_prov(mE) [kills fE];
bp2_lic_live(mE) read; then bp2_relicense(mE).

## 3. Kill bars (hand-derived)

Preconditions:
- PC-FORGE-FORM: all six of mA,mB,mC,mD,mP,mQ
  have sup==100 and conf==1; mA..mD have ext==1,
  self==0, formed==1; mP,mQ have ext==1, self==0,
  formed==1.
- PC-CHAIN-FORM: sup[z1]==100, sup[z2]==100,
  sup[mE]==100, ext[mE]==1, formed[mE]==1.

FORGE bars:
- K-FORGE-MATCH: after F1, n7==1, sup[mA]==110,
  conf[mA]==2. Derivation: one new type-7 -> one
  R2 indep=0: 100+10=110, conf 1+1=2. This is the
  exact record a genuine single match produces
  (BP-8 genuine-match nets): the forged edge is
  undetectable from the record.
- K-FORGE-DISC: after F2, n3==1, sup[mB]==80,
  disc[mB]==1, conf[mB]==0. Derivation: one new
  type-3 -> one R3: 100-20=80, disc 0+1=1, conf
  zeroed. Record-identical to a genuine
  block-mediated contradict from formation.
- K-FORGE-ORD: after F3, second absorb reports
  n7==1, sup[mC]==90, conf[mC]==1, disc[mC]==0.
  Derivation: genuine contradict absorbs first
  (R3: 80/0/1); the forged type-7 is then counted
  (n7=1, the block's drop rule is bypassed) and
  applies R2 (80+10=90, conf 1, disc zeroed).
  Contrast: the genuine path (BP-8 K-MCH-ORD) gives
  n7==0, 80/0/1. The 90/1/0 record is unreachable
  by genuine ev_observe paths (match-then-
  contradict gives 90/0/1; contradict-then-match
  is dropped): the forged edge is the unique
  producer of this record state among the tested
  shapes.
- K-FORGE-SAT: after F4, n7==3, sup[mD]==110,
  conf[mD]==2. Derivation: three new type-7s ->
  per-channel single application, ONE R2 indep=0
  (100+10=110, conf 2, the BP-8 K-MCH-SAT
  saturation). The record hides the true forged
  multiplicity; per-absorb forgery impact is
  capped at one R2 exactly as with genuine edges.
- K-FORGE-REPLAY: after F5, sup[mD]==120,
  conf[mD]==3. Derivation: stale watermarks
  (p7=0) recount the same 3 type-7s -> second R2
  (110+10=120, conf 3). No replay protection:
  integrity of the record depends on caller-held
  watermarks. (Disclosed: bp9_absorb is
  driver-side harness code, not belief-layer
  machinery; the finding maps where replay
  protection does NOT live.)
- K-FORGE-SHARED: after F6, sup[mP]==110 and
  sup[mQ]==110. Derivation: each absorb sees the
  one genuine type-7 with fresh watermarks ->
  one R2 each. Evidence is non-rivalrous: no
  cross-belief watermark consumption.
- K-FORGE-BLAST: after F7, sup[mP]==120 and
  sup[mQ]==120. Derivation: the single forged
  type-7 is counted by both absorbs (n7=2-1=1
  each) -> one R2 each (110+10=120, conf 3 each).
  One forged edge corrupts two beliefs' records:
  measured blast radius 2.

CHAIN bars:
- K-CHAIN-WEAK: after C1, sup[z1]==40,
  disc[z1]==0, conf[z1]==1, rev[z1]==0,
  bp2_has_k3(z1)==0. Derivation: 3x R3 on z2
  (100-60=40, disc 3, conf 0); propagate reads
  the type-14 target z2 (live, hasb=1), min=40,
  writes b_sup[z1]=40, ret 40. Propagation
  touches no counter and writes no reason edge
  on z1. z1's record (sup 40, conf 1 from
  formation, disc 0, no reason edge) cannot
  attribute the 40 to z2's disconfirmations:
  the provenance chain loses the link at the
  propagation step.
- K-CHAIN-RAISE: after C2, sup[z1]==80,
  conf[z1]==1, disc[z1]==0. Derivation: 2x R2
  indep=1 on z2 (40+20+20=80, conf 2, disc
  zeroed); propagate writes b_sup[z1]=80, ret 80.
  z1's support rose 40->80 with no confirm
  recorded on z1: the snap-up is likewise
  invisible to the record.
- K-CHAIN-FORGEREASON: after the forged
  link_edge(z2,3,z2,9), bp2_has_k3r(z2,9)==1.
  The forged reason code is queryable exactly
  like a genuine retire record; the layer
  performs no verification of reason edges.
- K-CHAIN-DOUBLEK3: after bp2_retire(z2,2),
  bp2_has_k3r(z2,2)==1 and bp2_has_k3r(z2,9)==1
  and sup[z2]==0. Derivation: retire writes the
  reason-2 self-edge and zeroes sup without
  checking for existing k3 edges, so the forged
  reason-9 record coexists with the genuine
  reason-2 record. The provenance record is now
  ambiguous (two retirements, one forged) and
  the layer has no mechanism to resolve which
  is genuine.
- K-CHAIN-TAMPER: after bt[z1*8]=100,
  bp2_eff(z1)==100. Derivation: b_ext=b_self=0
  (iscomp form), so eff returns support directly;
  nothing cross-checks the table against the
  edge record. The tampered value is accepted
  without question.
- K-CHAIN-RESURRECT: bp2_select over [z1] with
  bar 50 returns z1, while bp2_has_k3r(z1,2)==1.
  Derivation: hasb[z1]==1 (retire does not clear
  it), eff=100 >= 50, no tie -> z1. The layer
  selects a genuinely retired belief on
  corrupted state while its reason-2 retirement
  edge is still present: the edge record and the
  table contradict each other and the layer
  follows the table.
- K-CHAIN-STALE: after bp2_kill_one_prov(mE),
  b_ext[mE]==1 and live licensing==0.
  Derivation: killing fE clears its tag/liveness;
  bp2_lic_live counts 0 live targets, but the
  table's b_ext is untouched until an explicit
  relicense. The licensing counts in the record
  are stale after fact death.
- K-CHAIN-R4: after bp2_relicense(mE),
  sup[mE]==0 and bp2_has_k3r(mE,2)==1.
  Derivation: formed=1>0, live=0 -> retire
  reason 2 (provenance-death), sup zeroed. The
  dormant R4 detection measured in BP-6 still
  fires when triggered; this bar uses current
  frozen semantics only and presupposes no
  #16 outcome.

In-driver total: 2 PC + 7 FORGE + 8 CHAIN = 17.

## 4. Determinism and hygiene bars

- K-DET: 3/3 runs of bp9_bin byte-identical
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
  (172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a); bp9_learner.zag
  byte-identical to bp8_learner.zag (SHA-256
  2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e); opaque identifiers
  throughout.

## 5. Amendment log

5a. Pre-implementation: none. This prereg is
frozen as committed.

5b. Post-run amendments: (to be filled only if a
run exposes a prereg error; any change records the
re-derivation here and no frozen rule is changed
to chase a bar.)
