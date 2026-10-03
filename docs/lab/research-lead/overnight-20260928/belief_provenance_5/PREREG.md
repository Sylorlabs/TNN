# PREREG: BP-5 (belief-layer open dynamics)

Worker: BELIEF-PROVENANCE-5 subagent, 2026-10-03. Non-ledger
task (claim minting paused); nothing minted.
Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_5/`
Status: FROZEN. Committed before any implementation file
exists in this lane. All predicted numbers below are
hand-derived from the frozen R1-R7 forms (BP-4 REPORT.md,
DESIGN.md 3.1-3.2) and the probe-measured block behaviors
(type-7/type-3 evidence edges from ev_observe, t2_revise_graph
success/failure shapes). The 7 falsifiable predictions
(FP1-FP7) are sealed; this lane tests the open dynamics from
the BP-4 suggested-next list.

## 0. What is being tested

Four open-dynamics questions, each with discriminating kill
bars:

- E-R3 (R3 beyond scripted): R3 was triggered by the driver
  calling bp2_disconfirm directly. Here the evidence is
  emergent: the frozen block's ev_observe writes type-7
  (confirm) or type-3 (contradict) self-edges on facts from
  world data, and the harness applies R2/R3 iff the block
  wrote the edge. The driver never chooses confirm vs
  disconfirm; the observed value does.
- E-R5 (R5 beyond scripted): R5 was triggered by the driver
  calling bp2_revise directly. Here the harness applies R5
  iff the block's own t2_revise_graph changed the MAP's
  field28 (detected structurally, pre/post compare). A
  control observation with no contradiction must not revise.
- B-FACT: fact beliefs (DESIGN.md 2: claim "(s,r,v) holds"
  for a tag-1 fact node) were never formed. Formation,
  emergent evidence, R7 selection, eff() partition
  branches, and I1 record-destruction on tombstone.
- B-META: meta-beliefs (DESIGN.md 2, P5/P8: meta-row claim
  "profile X beat profile Y") were never formed.
  Formation on type-16 meta-rows, revision from policy
  outcomes, R7 selection over meta-rows.
- MH (multi-hop propagation): R6 weakening across 2 and 3
  type-14 hops. Discriminator: a single R6 application does
  not cascade; each hop needs its own application.
- CY (cyclic propagation): the DESIGN.md 10 open question.
  A 2-cycle under R6: fixpoint, oscillation, or prevented?
  Predicted: monotone convergence to the min (fixpoint),
  no oscillation, cycles not prevented; R6 snaps a node to
  its targets' min (can raise); 0 absorbs with retirement.

## 1. Researcher machinery (frozen, disclosed)

Belief layer: BP-4's bp4_learner.zag reused VERBATIM as
bp5_learner.zag (SHA-256
2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e):
record schema (8 u8: b_sup b_conf b_disc b_rev b_ext b_self
d_self formed), R1-R7, eff(), b_retire, bp2_lic_live,
bp2_kill_one_prov, bp2_lgsel. Constants: BASE=100,
INC_HI=20, INC_LO=10, DEC=20, BAR0=50, MIN_BAR=10.

New learner machinery this lane (exactly three functions,
in bp5_rules.zag, disclosed here):

- bp5_form_fact(W,bt,hasb,fid): B-FACT R1. The fact's own
  P6 field16 tag sets the source partition (same ext/self
  sets as bp2_lic_live: ext={1,2,5}, self={3,4,6}).
  b_sup=100, b_conf=1, b_disc=0, b_rev=0, d_self=255,
  formed=0 (a fact has no type-1 licensing of its own, so
  R4 is a no-op; its provenance-death is tombstone, I1).
- bp5_form_meta(W,bt,hasb,mr): B-META R1. No type-1
  licensing (b_ext=b_self=0, formed=0); support moves only
  via R2/R3 on policy outcomes. b_sup=100, b_conf=1,
  d_self=255.
- bp5_fact_tombstone(W,bt,hasb,fid): I1 enforcement.
  Tombstones the fact (ns 0/36 pattern) and destroys its
  belief record (hasb=0, 8 bytes zeroed). Slot recycling
  gives the next occupant a fresh R1, never an
  inheritance.

Test-harness code (in bp5_driver.zag, not belief
machinery):

- bp5_build: the BP-4 world replay verbatim (pm=0).
  Expected ids: mv2=194, mv3=274 (BP-4 PC-F1-IDX).
- bp5_tag(W,mid,tag): field16 tagging of live tag-1
  type-1 targets (BP-4 bp4_set_prov_tag, renamed).
- bp5_selfcnt(W,n,t): count of type-t self-edges on n.
- bp5_t16cnt(W,mr): count of outgoing type-16 edges.
- bp5_absorb_fact(W,bt,mid,fid,p7,p3,out): emergent
  evidence absorption. Counts NEW type-7/type-3
  self-edges on fid since (p7,p3); each new type-7
  applies bp2_confirm(bt,mid,0) [same-set: the edge is
  on the belief's own licensing fact]; each new type-3
  applies bp2_disconfirm(bt,mid). The rule fires iff
  the block wrote the edge.
- Meta-update mapping (driver logic, disclosed): for a
  meta-row mr with type-16 edges to winner w and loser
  l (driver-known roles; edges written winner-first per
  the BP-1 meta_add convention): w confirmed ->
  bp2_confirm(mr,0); w disconfirmed ->
  bp2_disconfirm(mr); l confirmed -> bp2_disconfirm(mr);
  l disconfirmed -> bp2_confirm(mr).
- R5 emergent trigger (driver logic, disclosed):
  pre28=ng(W,mb,28); after ev_observe, if
  ng(W,mb,28)!=pre28 the block revised the MAP ->
  bp2_revise(bt,mb). Otherwise no R5.

Emergent evidence facts (probe-measured on the frozen
block, pre-prereg):

- ev_observe(W,s,r,o) with o == fact field28: returns 1,
  writes exactly one type-7 self-edge on the activated
  fact, teaches nothing, revises nothing.
- ev_observe(W,s,r,o) with o != fact field28: returns 0,
  writes exactly one type-3 self-edge on the activated
  fact, calls revise_on_contradict, teaches a new fact
  and a history node.
- On a chain-graph MAP (t_t2_revise shape):
  ev_observe contradicting a licensing fact makes
  t2_revise_graph succeed: MAP field28 201->999.
  On a count-graph MAP or a rootless promoted MAP the
  revise is attempted and reverted: field28 unchanged.
- activate(W,s,r) picks the max-bid fact; ev_teach-logged
  facts outrank ev_teach_in facts, so observations on
  driver-taught (s,r) hit the driver's fact
  deterministically.

## 2. Arm E-R3: emergent disconfirmation (world WA)

Teach (701,71,10)->fa1 [id 2], (702,72,20)->fa2 [id 3].
Tag fa1=2 (EXT), fa2=6 (SELF). Promote
ma=promote_graph(WA,-1,701,71,10,[fa1,fa2],2) [id 4,
field28=10]. Form ma (B-STRUCT): b_sup=100, b_conf=1,
b_ext=1, b_self=1.

Confirm leg: p7=bp5_selfcnt(fa1,7)=0.
ev_observe(WA,701,71,10) -> ret 1 (probe-measured).
n7 = new type-7 = 1 -> bp2_confirm(bt,ma,0).
Hand-derived: b_sup=100+10=110, b_conf=2, b_disc=0.

Disconfirm leg: p3=bp5_selfcnt(fa2,3)=0.
ev_observe(WA,702,72,999) -> ret 0 (probe-measured).
n3 = new type-3 = 1 -> bp2_disconfirm(bt,ma).
Hand-derived: b_sup=110-20=90, b_disc=1, b_conf=0.
The revise is attempted and reverted (rootless MAP):
field28 stays 10 -> R5 must NOT fire (b_rev=0).

## 3. Arm E-R5: emergent revision (world WB)

The t_t2_revise shape: ev_teach(WB,101,11,102),
ev_teach(WB,102,12,201), ev_query(WB,101,40,201)->201.
mb = the tag-20 MAP with field4==40. pre28=201.
Form mb (B-STRUCT): b_sup=100, b_conf=1, b_rev=0.

Control: ev_observe(WB,102,12,201) -> ret 1
(probe-measured). field28 unchanged (201) -> the
emergent trigger is absent -> bp2_revise NOT applied.
Hand-derived: b_sup=100, b_rev=0.

Treatment: ev_observe(WB,102,12,999) -> ret 0
(probe-measured). t2_revise_graph succeeds:
field28 201->999 -> bp2_revise(bt,mb).
Hand-derived: b_sup=100/2=50, b_rev=1, b_conf=0,
b_disc=0. (This arm's harness absorbs only the
revision signal, disclosed; edge absorption is the
E-R3 arm's channel.)

## 4. Arm B-FACT: fact beliefs (world WC)

fc1=ev_teach(WC,703,73,30), field16=2.
fc2=ev_teach(WC,704,74,40), field16=6.
fc3=ev_teach(WC,705,75,50), untagged.
bp5_form_fact on each.
Hand-derived: b_sup=100, b_conf=1 all; (b_ext,b_self):
fc1=(1,0), fc2=(0,1), fc3=(0,0).

Evidence (emergent): ev_observe(WC,703,73,30)->ret 1,
one new type-7 on fc1 -> bp2_confirm(fc1,0):
b_sup=110, b_conf=2. ev_observe(WC,704,74,999)->ret 0,
one new type-3 on fc2 -> bp2_disconfirm(fc2):
b_sup=80, b_disc=1, b_conf=0.

Selection: R7({fc1,fc2,fc3},50): eff 110/80/100 ->
fc1. eff() branches: fc3 (no partition) eff=b_sup=100;
fc1 eff=110*(1*255+255*0)/(255*1)=110.

I1: bp5_fact_tombstone(fc2): hasb=0, node dead.
R7({fc2,fc3},50)=fc3 (fc2 has no record, skipped).
fc4=ev_teach(WC,706,76,60); bp5_form_fact(fc4):
b_sup=100, b_disc=0, b_conf=1 (fresh, no inheritance
from fc2's record even if the slot is recycled).

## 5. Arm B-META: meta-beliefs (world WD)

fA=ev_teach(WD,711,71,100), field16=2.
fB=ev_teach(WD,712,72,200), field16=6.
mA=promote_graph(WD,-1,711,71,100,[fA],1).
mB=promote_graph(WD,-1,712,72,200,[fB],1).
Form mA (b_ext=1), mB (b_self=1): b_sup=100.
mr1=alloc_node (tag 3): type-16 -> mA, type-16 -> mB
(mr1: mA winner, mB loser; "ext-profile beats
self-profile"). mr2=alloc_node (tag 3): type-16 -> mB,
type-16 -> mA (reversed claim). bp5_form_meta on both:
b_sup=100, b_conf=1, b_ext=b_self=0.

Event: ev_observe(WD,711,71,100)->ret 1, one new
type-7 on fA (mA's licensing fact) ->
bp2_confirm(mA,0): b_sup[mA]=110. Meta-update:
mr1 winner confirmed -> bp2_confirm(mr1,0):
b_sup=110, b_conf=2. mr2 loser confirmed ->
bp2_disconfirm(mr2): b_sup=80, b_disc=1, b_conf=0.

Selection: R7({mr1,mr2},50): 110 vs 80 -> mr1. The
evidential policy is revisable state that participates
in selection.

## 6. Arm MH: multi-hop propagation (world WE)

bp5_build replay. mv2=194, mv3=274. Form both
(B-STRUCT): b_sup=100. Weaken mv3: 2x bp2_disconfirm
-> b_sup=60 (100->80->60). z1..z4=alloc_node, form
B-COMP: b_sup=100. link_edge type-14: z1->mv3,
z2->z1, z3->z2, z4->mv2, z4->mv3.

Hand-derived (R6 = min over live recorded targets):
- bp2_propagate(z1): min(60)=60. z2,z3 untouched.
- bp2_propagate(z2): min(b_sup[z1]=60)=60. z3=100.
- bp2_propagate(z3): min(60)=60.
- bp2_propagate(z4): min(100,60)=60.

## 7. Arm CY: cyclic propagation (world WF)

Minimal world (tnn2_init only). zA,zB=alloc_node [2,3],
form B-COMP: b_sup=100. link_edge type-14 zA->zB and
zB->zA (2-cycle).

Hand-derived:
- bp2_disconfirm(zB): zB=80.
- bp2_propagate(zA): min(80)=80. (80,80).
- bp2_disconfirm(zB): zB=60.
- bp2_propagate(zB): min(b_sup[zA]=80)=80. R6 snaps
  to the targets' min; it can RAISE the node.
  (80,80).
- bp2_propagate(zA), bp2_propagate(zB): (80,80).
  Re-application is idempotent: fixpoint, no
  oscillation.
- 4x bp2_disconfirm(zB): zB=0 (80->60->40->20->0).
- bp2_propagate(zA): min(0)=0 -> b_retire(zA,2):
  kind-3 reason-2 self-edge on zA.
- bp2_propagate(zB): min(b_sup[zA]=0)=0.

Predicted answer to the open question: fixpoint
(monotone convergence to the cycle min), not
oscillation, not prevented; 0 absorbs the whole
strongly-connected component with retirement.

## 8. Kill bars (frozen)

Preconditions:
- PC-E-R3-FORM: b_sup[ma]==100 && b_ext[ma]==1 &&
  b_self[ma]==1.
- PC-E-R5-FORM: b_sup[mb]==100 && ng(WB,mb,28)==201.
- PC-MH-BUILD: xs5_find_countmap(WE)==194 (mv2).
- PC-CY-FORM: b_sup[zA]==100 && b_sup[zB]==100.

E-R3 bars:
- K-E-R3-C7: new type-7 on fa1 == 1 (the block wrote
  the confirmation evidence).
- K-E-R3-CSUP: b_sup[ma]==110 && b_conf[ma]==2.
- K-E-R3-D3: new type-3 on fa2 == 1 (the block wrote
  the disconfirmation evidence).
- K-E-R3-DSUP: b_sup[ma]==90 && b_disc[ma]==1 &&
  b_conf[ma]==0.
- K-E-R3-NOR5: ng(WA,ma,28)==10 && b_rev[ma]==0
  (failed revise -> R5 correctly absent).

E-R5 bars:
- K-E-R5-CTL: after the matching observe,
  ng(WB,mb,28)==201 && b_rev[mb]==0 && b_sup[mb]==100
  (no contradiction -> no revision -> no R5).
- K-E-R5-REV: after the contradicting observe,
  ng(WB,mb,28)==999 (the block revised the MAP).
- K-E-R5-TRAJ: b_sup[mb]==50 && b_rev[mb]==1 &&
  b_conf[mb]==0 && b_disc[mb]==0.

B-FACT bars:
- K-BF-FORM: b_sup 100/100/100; (ext,self)
  (1,0)/(0,1)/(0,0); b_conf 1/1/1.
- K-BF-EV: new t7 on fc1 == 1 && new t3 on fc2 == 1
  && b_sup[fc1]==110 && b_sup[fc2]==80 &&
  b_disc[fc2]==1 && b_conf[fc1]==2.
- K-BF-SEL: R7({fc1,fc2,fc3},50)==fc1.
- K-BF-EFF: eff[fc3]==100 && eff[fc1]==110.
- K-BF-I1DIE: hasb[fc2]==0 && ng(WC,fc2,36)==0.
- K-BF-I1SEL: R7({fc2,fc3},50)==fc3.
- K-BF-I1FRESH: b_sup[fc4]==100 && b_disc[fc4]==0
  && b_conf[fc4]==1.

B-META bars:
- K-BM-FORM: b_sup[mr1]==100 && b_sup[mr2]==100 &&
  bp5_t16cnt(mr1)==2 && bp5_t16cnt(mr2)==2.
- K-BM-EV: new t7 on fA == 1 && b_sup[mA]==110 &&
  b_sup[mr1]==110 && b_conf[mr1]==2 &&
  b_sup[mr2]==80 && b_disc[mr2]==1.
- K-BM-SEL: R7({mr1,mr2},50)==mr1.

MH bars:
- K-MH-1HOP: after R6(z1): b_sup[z1]==60 &&
  b_sup[z2]==100 && b_sup[z3]==100 (no cascade).
- K-MH-2HOP: after R6(z2): b_sup[z2]==60 &&
  b_sup[z3]==100.
- K-MH-3HOP: after R6(z3): b_sup[z3]==60.
- K-MH-MIN: after R6(z4): b_sup[z4]==60.

CY bars:
- K-CY-C1: after R6(zA): b_sup[zA]==80 &&
  b_sup[zB]==80.
- K-CY-C2: after R3(zB)+R6(zB): b_sup[zB]==80
  (R6 snaps to target min, can raise).
- K-CY-C3: after R6(zA)+R6(zB): (80,80)
  (fixpoint, idempotent, no oscillation).
- K-CY-C4: after 4xR3(zB)+R6(zA): b_sup[zA]==0 &&
  bp2_has_k3r(WF,zA,2)==1 (0-absorption retires).
- K-CY-C5: after R6(zB): b_sup[zB]==0.

Determinism and hygiene:
- K-DET: 3/3 runs byte-identical whole-output
  (SHA-256).
- K-HYG: pure Zag under safebin (`which python3` /
  `which python` empty at build and run); zero em/en
  dash bytes in lane files; 0 new edge types (1/3/14
  frozen; 16 pre-exists in the block per DESIGN.md P5,
  used here for meta-rows); 0 new node types (tag
  1/3/20 all pre-existing); 0 modes, 0 bridges,
  0 handlers; xf_block.zag SHA-256
  172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
  re-verified before and after the build;
  bp5_learner.zag byte-identical to bp4_learner.zag
  (SHA-256
  2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e);
  opaque identifiers.

Bar count: 4 PCs + 27 K bars + K-DET + K-HYG = 33.

## 9. Falsifiers (what kills the claim)

- E-R3: block writes no type-7/type-3 (evidence not
  emergent); b_sup trajectory != hand-derived; R5
  fires without a field28 change.
- E-R5: control observe revises (b_rev moves without
  contradiction); treatment observe leaves field28 at
  201; b_sup != 50 after a real revision.
- B-FACT: partition != (1,0)/(0,1)/(0,0); fact
  beliefs not selectable; tombstone leaves hasb=1;
  recycled slot inherits old b_disc.
- B-META: one observation moves both meta-rows the
  same direction; R7 does not follow the revised
  policy.
- MH: a single R6 cascades (z2 or z3 move without
  their own R6); 3-hop value != 60.
- CY: oscillation (re-application changes values);
  R6 cannot raise (C2 shows 60); no retirement on
  0-absorption.

## 10. Verdict rule

BP-5-PASS iff every PC bar and every K bar passes on
the frozen implementation, 3/3 byte-identical. A
single failed K bar fails its arm. This lane does not
re-open the 7 sealed predictions.

## 11. Out of scope (not claimed)

Whether the emergent absorb mapping (indep=0 for
same-fact evidence) is the right form; combiner
alternatives (min is frozen); bar-adjustment
trajectories; eviction interaction; d_self dynamics
on fact/meta beliefs; per-belief bars. The R5 arm
absorbs only the revision signal by disclosed design;
full multi-channel absorption is future work.
