# PREREG: BP-4 (FP1 graded flip point, FP4 learned source discount, FP5 independence discount)

Worker: BELIEF-PROVENANCE-4 subagent, 2026-10-03. Non-ledger.
Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_4/`
Status: FROZEN. Committed before any implementation file
exists in this lane. All predicted numbers below are
hand-derived from DESIGN.md Sections 3.1-3.2 and the
BP-2/BP-3 measured R1-R7 behavior (BP-2-PASS 18/18,
BP-3-PASS 31/31).

## 0. What is being tested

The three remaining open falsifiable predictions from
DESIGN.md Section 10, as sealed arms on the frozen belief
machinery. Together with FP2/FP3 (BP-2) and FP6/FP7 (BP-3),
this completes all 7.

- FP1 (graded flip point, DESIGN.md Section 8): two
  candidate MAPs; the leader has 4 licensing facts.
  Tombstone the leader's facts one at a time. Predicted:
  b_sup drops by the exact R4 fraction at each step and R7
  flips to the rival at the predicted step. The open
  question is the shape: is the flip gradual or sudden?
  Predicted shape: graded (strictly decreasing) support
  with a SUDDEN single-step selection flip at the crossing
  point.
- FP4 (learned source discount, DESIGN.md Sections 3.1, 6,
  8): d_self starts at 255 (no discount) and moves only
  through experienced disconfirmation of self-sourced
  beliefs. Two arms: T experiences a self-amplification
  failure (C170 shape: a self-inferred majority is wrong);
  C does not. Both then choose between an external-sourced
  and a self-sourced belief with equal b_sup. Predicted: T
  selects the external belief (d_self < 255); C shows no
  systematic discount (d_self = 255, tie abstention).
- FP5 (independence discount, DESIGN.md Sections 3.2, 8):
  six confirmations from one licensing set vs six from
  disjoint sets. Predicted: b_sup differs by exactly the
  INC_HI/INC_LO ratio accumulated over six R2 applications;
  the independently-confirmed belief is selected. The
  C211 Probe-R failure mode (repetition without
  independence going falsely confident) is the falsifier.

## 1. Researcher machinery (frozen constants, disclosed)

The belief layer is BP-3's `bp3_learner.zag` reused VERBATIM
(no redesign): record schema (8 u8 fields per node id:
b_sup, b_conf, b_disc, b_rev, b_ext, b_self, d_self,
formed), R1-R7, eff(), b_retire, bp2_lgsel baseline,
bp2_kill_one_prov, bp2_census. Constants: BASE=100,
INC_HI=20, INC_LO=10, DEC=20, BAR0=50, MIN_BAR=10. The R4
compounding reading is frozen as in BP-2/BP-3: successive
calls scale the CURRENT b_sup.

New learner machinery this lane (exactly one function, in
`bp4_rules.zag`, disclosed here as the FP4 mechanism):

R3-prime (d_self learning rule). DESIGN.md 3.1 specifies
d_self "starts at 255 (no discount); learned downward
only through experience" but leaves the update form to the
implementation. Frozen form for this lane:
`bp4_disconf_learn(bt, mid)` =
  1. apply R3 (bp2_disconfirm): b_sup = max(0, b_sup-DEC);
     b_disc++; b_conf = 0.
  2. if b_self[mid] > b_ext[mid] (self-majority licensing):
     d_self[mid] = max(0, d_self[mid] - 25).
  3. R2 confirmations never change d_self.
The step of 25 and the self-majority condition are
researcher-chosen disclosed machinery; what is LEARNED
(the FP4 claim) is whether d_self moves at all and in
which arms. Falsifier per DESIGN.md: arm T shows no
discount (d_self stuck at 255), or arm C also discounts
(researcher bias leak: d_self moving without experience).

Test-harness code (in `bp4_driver.zag`, not belief
machinery):
- `bp4_build(W,out)`: the BP-3 world replay verbatim
  (pm=0, no mz3): ev_teach chains, four ev_query_xs5
  calls, xs5_compose, promote_graph MAP_Z2 with type-14
  edges to navx and mv3. Expected node ids (deterministic
  allocator, same build path as BP-3): navx=27, mv2=194,
  mv3=274 (BP-3 K-FP6-IDX measured). out: 0=my 4=mv2
  8=mv3 12=navx 20=mz2.
- `bp4_set_prov_tag(W,mid,tag)`: for each live tag-1
  type-1 provenance target f of mid, ns(W,f,16,tag).
  Disclosed researcher scripting of the P6 source
  partition: tag 2 = TAUGHT (EXTERNAL), tag 6 =
  DERIVED-FROM-STRUCTURE (SELF). The block never reads
  node field16 of tag-1 facts (field16 reads in
  xf_block.zag are tag-102 branch targets and the
  workspace head), so tagging is side-effect-free on the
  world. The source partition itself is not what FP4
  tests; FP4 tests the d_self learning dynamics given
  the partition.
- `bp4_ck`/`bp4_bar`: tally helpers (same as BP-3).
- Helpers copied from BP-3's driver with bp4_ prefix:
  bp4_other_countmap, bp4_max_countmap, bp4_only_mapz,
  bp4_prov_rel, bp4_bufcopy, bp4_bufeq_ref.

Disclosure: the "self-amplification failure" is modeled
as two disconfirmation experiences on the self-sourced
belief (the C170 shape: a self-inferred majority is
wrong), followed by two independent confirmations that
restore b_sup to exactly 100 so the choice is at equal
b_sup, per DESIGN.md FP4 ("equal b_sup"). The evidence
is researcher-scripted; what is tested is the learner
state trajectory (d_self) and the selection outcome.
Disclosure: the FP5 indep flag is driver-supplied (the
driver models whether the licensing sets are disjoint,
per DESIGN.md R2's indep parameter); the mechanism under
test is the differential INC_HI/INC_LO weighting.
Disclosure: FP1/FP4/FP5 treat the R7 candidate set as the
operational conflict set (as FP7 did); R7 does not check
(field8,field4) identity.

## 2. Arm FP1: graded flip point (workspace WF1)

Build (bp4_build). No source tagging (facts stay
field16=0, neither ext nor self; eff = b_sup). Form mv3
(leader, 4 licensing facts) and mv2 (rival). Leader gets
2 independent confirmations: b_sup = 100+40 = 140
(b_conf=3). Rival stays at 100 (b_conf=1). bar=50.
Candidates cands = {mv3, mv2}.

Hand-derived step values (R4 compounding on formed=4):
- s0 (pre): live=4, b_sup[mv3]=140. R7: 140>100, no tie,
  140>=50 -> mv3. lg: mv3.
- s1: kill 1 fact + R4: b_sup = 140*3/4 = 105, live=3.
  R7: 105>100 -> mv3. lg: mv3.
- s2: kill 1 fact + R4: b_sup = 105*2/4 = 52 (210/4
  truncates), live=2. R7: 52<100 -> mv2. THE FLIP. lg:
  mv3 (node still live; existence says use-it).
- s3: kill 1 fact + R4: b_sup = 52*1/4 = 13, live=1.
  R7: mv2. lg: mv3.
- s4: kill 1 fact + R4: live=0 -> b_retire(mv3,2),
  b_sup=0, kind-3 reason-2 self-edge on mv3. R7: mv2
  (eff[mv3]=0<50). lg: mv3.

Predicted shape: support declines gradually and strictly
(140 > 105 > 52 > 13 > 0); selection flips suddenly in a
single step at s2, the step where eff crosses the rival.
The flip is a crossing event, not a bar event (52 >= 50
at the flip step).

## 3. Arm FP4: learned source discount (workspaces WT, WC)

Build each world (bp4_build). Tag: mv2's licensing facts
-> 2 (TAUGHT, EXTERNAL); mv3's facts -> 6
(DERIVED-FROM-STRUCTURE, SELF). Form mv2 (M_EXT) and mv3
(M_SELF). Both: b_sup=100, d_self=255.

Arm WT (treatment: self-amplification failure experience):
- 2x bp4_disconf_learn(bt,mv3): b_sup 100->80->60;
  b_disc=2; b_conf=0; d_self 255->230->205
  (b_self=4 > b_ext=0, self-majority, so the discount
  moves).
- 2x bp2_confirm(bt,mv3,1): b_sup 80->100 (b_conf=2,
  b_disc=0). d_self unchanged at 205 (R2 never moves it).
- Hand-derived at choice: b_sup[mv2]=100, b_sup[mv3]=100
  (equal, as DESIGN.md requires); eff[mv2] =
  100*(4*255+255*0)/(255*4) = 100; eff[mv3] =
  100*(0*255+205*4)/(255*4) = 82000/1020 = 80 (integer
  division: 1020*80=81600, remainder 400).
- R7({mv2,mv3},50): 100 vs 80, no tie -> mv2 (M_EXT).

Arm WC (control: no experience):
- Nothing applied. d_self[mv3]=255; eff both = 100.
- R7({mv2,mv3},50): exact tie at 100 -> -3 (no
  systematic discount).

Post-choice control leg (on WT, after WT bars measured):
- 2x bp4_disconf_learn(bt,mv2): b_sup 100->80->60;
  b_disc=2; d_self[mv2] stays 255 (b_self=0 > b_ext=4 is
  false: external-majority disconfirmation does not move
  the self discount).

## 4. Arm FP5: independence discount (workspace WI)

Build (bp4_build). No source tagging. Form mv2 (M_A) and
mv3 (M_B). bar=50.
- M_A: 6x bp2_confirm(bt,mv2,0) (same licensing set):
  b_sup = 100+6*10 = 160; b_conf = 7.
- M_B: 6x bp2_confirm(bt,mv3,1) (disjoint licensing
  sets): b_sup = 100+6*20 = 220; b_conf = 7.
- Hand-derived: b_sup[mv2]=160, b_sup[mv3]=220;
  220-160 = 60 = 6*(INC_HI-INC_LO).
- R7({mv2,mv3},50): 220>160 -> mv3 (M_B).

## 5. Kill bars (frozen)

Preconditions (all must pass):
- PC-F1-BUILD: xs5_find_countmap(WF1)==mv2;
  bp4_prov_rel(WF1,mv3)==87 with 4 live type-1 facts.
- PC-F1-IDX: navx==27, mv2==194, mv3==274.
- PC-F1-SUP0: after the 2 leader confirmations,
  b_sup[mv3]==140 and b_sup[mv2]==100.
- PC-F4-T-BUILD / PC-F4-C-BUILD: same shape as
  PC-F1-BUILD on WT/WC.
- PC-F4-T-TAG / PC-F4-C-TAG: after tagging,
  lic_live(mv2) has self==0 and ext==live (live>=1);
  lic_live(mv3) has live==4, ext==0, self==4.
- PC-F5-BUILD: same shape as PC-F1-BUILD on WI.

FP1 bars:
- K-FP1-SEQ: b_sup[mv3] at s0..s4 == (140,105,52,13,0).
- K-FP1-FLIP: R7 at s0..s4 == (mv3,mv3,mv2,mv2,mv2);
  the flip occurs exactly at s2 (second tombstone).
- K-FP1-RETIRE: at s4, bp2_has_k3r(WF1,mv3,2)==1 and
  b_sup[mv3]==0.
- K-FP1-KILLCRIT: at s4, bp2_lgsel({mv3,mv2})==mv3 while
  R7==mv2: existence says use-it, belief says refuse.
  (Belief is right per the sealed XHIER-COUNTMAP-FIX K3a
  finding: a structure whose entire provenance died was
  still used to compute a silent wrong-relation answer
  under the control build; the belief refusal is that
  fence as persistent state.)
- K-FP1-SHAPE: 140>105>52>13>0 strictly decreasing
  (graded weakening); the R7 selection flips in exactly
  one step (sudden), at the crossing point, not at a bar
  boundary (52>=50 at the flip step).

FP4 bars:
- K-FP4-T-D: d_self[mv3]==205 after the failure
  experience (255-2*25).
- K-FP4-T-SUP: b_sup[mv2]==100 and b_sup[mv3]==100 at
  choice (equal b_sup).
- K-FP4-T-EFF: eff[mv2]==100 and eff[mv3]==80.
- K-FP4-T-SEL: R7({mv2,mv3},50)==mv2 (selects the
  external-sourced belief).
- K-FP4-C-D: d_self[mv3]==255 (no experience, no
  discount).
- K-FP4-C-SEL: R7({mv2,mv3},50)==-3 (exact tie: no
  systematic discount).
- K-FP4-EXT-INERT: post-choice, 2x disconfirmation of
  mv2 leaves d_self[mv2]==255 and b_sup[mv2]==60.

FP5 bars:
- K-FP5-SUP: b_sup[mv2]==160 and b_sup[mv3]==220.
- K-FP5-DIFF: (b_sup[mv3]-b_sup[mv2])==60.
- K-FP5-SEL: R7({mv2,mv3},50)==mv3.
- K-FP5-CONF: b_conf[mv2]==7 and b_conf[mv3]==7 (same
  confirmation count; only independence differs).

Determinism and hygiene:
- K-DET: 3/3 runs byte-identical whole-output (SHA-256).
- K-HYG: pure Zag under safebin (`which python3` empty at
  build and run); zero em/en dash bytes in lane files; 0
  new edge types (only 1/14/3), 0 new node types, 0 modes,
  0 bridges, 0 handlers; xf_block.zag SHA-256
  172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
  re-verified before and after the build; bp4_learner.zag
  byte-identical to bp3_learner.zag (SHA-256
  2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e);
  opaque identifiers.

Bar count: 8 PCs + 16 K bars + K-DET + K-HYG = 26.

## 6. Falsifiers (what kills the claim)

- FP1: any b_sup[mv3] step value != hand-derived; flip at
  a step other than s2; no flip while eff stays above the
  rival; retirement without the kind-3 reason-2 edge;
  liveness-gating and R7 agreeing at s4 (the belief layer
  would be decorative there).
- FP4: d_self[mv3]==255 in WT after the failure
  experience (the discount is not learned); d_self moved
  in WC (researcher bias leak: discount without
  experience); WT selects mv3 (learned discount with no
  behavioral effect); external-majority disconfirmation
  moves d_self (the rule is not source-selective).
- FP5: b_sup[mv2]==b_sup[mv3] (the C211 Probe-R failure
  mode: repetition without independence falsely
  confident); mv2 selected (independence counts for
  nothing).

## 7. Verdict rule

BP-4-PASS iff every PC bar and every K bar passes on the
frozen implementation, 3/3 byte-identical. FP1-PASS,
FP4-PASS, FP5-PASS reported per prediction family. A
single failed K bar fails its arm. This lane completes
the belief layer's 7 falsifiable predictions: FP1, FP4,
FP5 here; FP2/FP3 (BP-2); FP6/FP7 (BP-3).

## 8. Out of scope (not claimed)

Whether the d_self step of 25 or the self-majority
condition is the right form (sensitivity analysis is
future work; the lane tests that learning happens at
all, is experience-gated, and is source-selective).
Bar-adjustment trajectories (bar stays at BAR0; the
disconfirmations here are experiences, not fed back as
commitment outcomes). B-FACT/B-META records,
multi-hop/cyclic propagation, combiner alternatives,
eviction interaction, constant sensitivity. The Seq-style
evidence in FP4/FP5 is researcher-scripted ground truth
for the mechanism comparison, disclosed as such; what is
sealed is the learner-state trajectory and the selection
outcome under the frozen rules.
