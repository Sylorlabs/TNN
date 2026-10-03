# PREREG: BP-7 (d_self dynamics, bar meta-parameter sensitivity, per-belief bars)

Worker: BELIEF-PROVENANCE-7 subagent, 2026-10-03. Non-ledger
task (claim minting paused); nothing minted.
Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_7/`
Status: FROZEN. Committed before any implementation file
exists in this lane. All predicted numbers below are
hand-derived from the frozen forms: BP-4 R3-prime
(bp4_disconf_learn, FP4 PASS), the dormant bp2_bar_after
rule (BP-6 BA arm), and probe-measured block behaviors
(type-7/type-3 evidence edges from ev_observe, all
re-probed 2026-10-03). The 7 falsifiable predictions
(FP1-FP7) stay sealed; this lane tests the remaining
open dynamics suggested by BP-6: d_self dynamics,
bar-policy meta-parameter sensitivity, per-belief bars.

## 0. What is being tested

Three open-dynamics questions, each with discriminating
kill bars:

- DSELF (d_self dynamics): BP-4 FP4 showed d_self
  255->205 after 2 self-majority disconfirmations
  (source-selective; the frozen rule is
  bp4_disconf_learn: R3, then if b_self > b_ext:
  d_self = max(0, d_self-25); confirmations never move
  it). Here the trajectory is run long: 10 and 11
  disconfirmations (to the floor), then confirmations
  (the recovery question), the resulting eff() value,
  source-selectivity under an ext-majority belief, the
  strict-majority boundary (b_self == b_ext), and a
  mid-trajectory majority flip via R4 relicensing after
  killing self facts. Predicted: d_self reaches 5 at
  k=10 and floors at 0 at k=11 (no u8 wraparound);
  confirmations never recover it (stays 0); the
  discount has teeth on eff (30->7); the majority
  condition is evaluated live at each disconfirmation,
  not frozen at formation.
- META (bar-policy meta-parameter sensitivity): the
  frozen bp2_bar_after has meta-parameters INC=1 (false
  positive raise), DEC=1 (easy true positive lower),
  threshold 2x, MIN_BAR=10. Driver-side experimental
  parameterized rule bp7_bar_param(bar, confirmed, eff,
  inc, dec, thr_num, thr_den, minbar) (disclosed; NOT a
  belief-layer change, same status as BP-6's combiner
  variants) is swept over six settings on the same
  world-driven evidence stream as BP-6's BA arm
  (FP,TP,TP,TP,TP with eff_at_commit 100,80,90,100,
  110): frozen (1,1,2x), aggressive raise (3,1,2x),
  aggressive lower (1,3,2x), hair-trigger threshold
  (1,1,1.5x), zero raise (0,1,2x), zero lower (1,0,2x).
  Predicted final bars: 50/52/48/47/48/51. S3 and
  S5 share the final 48 (both end low by different
  routes: aggressive lowering vs never raising); they
  are discriminated at e1 (51 vs 50). Only the frozen
  setting is neutral over a balanced FP/TP cycle.
- PBAR (per-belief bars): one global bar punishes every
  belief for one belief's false positives.
  Driver-side experimental per-belief bar array plus
  bp7_select_pbar (candidate admitted iff eff >= its
  own bar; argmax; tie -> -3) is compared against the
  global bar on two questions. Help: after mA's false
  positives the global bar excludes the innocent mB
  (eff 50) while per-belief bars keep mB usable
  (isolation) and preserve the penalty where earned
  (teeth). Cost: a belief with a 40-TP lucky streak
  lowers its own bar to MIN_BAR=10 and is then
  selected at eff 15 where the population-informed
  global bar (53) refuses (overfit to local luck).
  Predicted: both the help and the cost are real and
  measured, a discriminating pair each way.

## 1. Researcher machinery (frozen, disclosed)

Belief layer: BP-6's bp6_learner.zag reused VERBATIM as
bp7_learner.zag (SHA-256
2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e,
re-verified after copy): record schema (8 u8), R1-R7,
eff(), bp2_bar_after. Constants: BASE=100, INC_HI=20,
INC_LO=10, DEC=20, BAR0=50, MIN_BAR=10.

R3-prime: BP-4's bp4_rules.zag reused VERBATIM
(SHA-256
7392299309082836bf376bb445492ef8d9fd75b3d857ad425b8ca74d7399e4d9,
re-verified): exactly one function,
bp4_disconf_learn (R3, then d_self -= 25 floored at 0
iff b_self > b_ext at call time). Frozen FP4 code,
not new machinery.

New learner machinery this lane: NONE. In particular:
- bp7_bar_param is driver-side experimental code in
  bp7_driver.zag, NOT a belief-layer change. The
  frozen bp2_bar_after is exactly bp7_bar_param with
  (inc=1, dec=1, thr=2x, minbar=10); the S1 arm
  replicates the BP-6 BA trajectory as a control.
- Per-belief bars (pb array) and bp7_select_pbar are
  driver-side experimental code, disclosed here. R7
  with a single global bar stays the frozen
  belief-layer rule regardless of the comparison
  outcome.
- The global bar in the PBAR arm is updated only on
  the selected belief's commitment outcomes (mA);
  per-belief bars update on each belief's own
  outcomes. This credit-assignment scope IS the
  architectural difference under test; disclosed.

Test-harness code (in bp7_driver.zag, not belief
machinery): bp7_absorb (BP-6 absorb renamed),
bp7_bar_param, bp7_select_pbar, bp7_kill_self_prov
(kill first live tag-1 type-1 provenance target with
field16 in {3,4,6}), world builders per arm,
in-driver bars, commitment bookkeeping.

Block behaviors (probe-measured, frozen block):
ev_observe matching writes one new type-7 self-edge
per call; contradicting writes one new type-3;
ev_teach/promote_graph/alloc_node deterministic.

## 2. Arm DSELF: d_self long trajectory (world WD)

tnn2_init. m: facts f1..f4 = ev_teach(901..904,91..94,
10..40), field16 tags 3,4,6 (self) and 2 (ext).
m=promote_graph(WD,-1,901,91,10,[f1..f4],4).
bp2_form(m,0): b_sup=100, b_conf=1, b_disc=0,
b_ext=1, b_self=3, d_self=255, formed=4.
eff(m)=100 throughout the discount arm (d moves but
ne=1,nself=3 fixed; eff uses d only).

Hand-derived (bp4_disconf_learn, k applications):
- k=1..10: sup=max(0,100-20k):
  80,60,40,20,0,0,0,0,0,0; disc=k; conf=0;
  d_self=255-25k: 230,205,180,155,130,105,80,55,30,5.
- k=11: d_self=max(0,5-25)=0. No u8 wraparound.
- Then 3x bp2_confirm(m,0): sup 0->10->20->30;
  conf=3; disc=0 (R2 zeroes disc); d_self stays 0:
  the frozen machinery has NO recovery path.
- eff(m) at the end: ne=1, nself=3, d=0, s=30:
  30*(1*255+0*3)/(255*4)=7650/1020=7 (i32
  truncation). Undiscounted (d=255) it would be 30:
  the one-way discount has teeth.

Source-selectivity and boundary (hand-derived):
- m2: facts tags 1,2,5 (ext), 3 (self); form(0):
  ext=3, self=1. 5x bp4_disconf_learn: sup
  80,60,40,20,0; disc=5; d_self stays 255 (1>3
  false) even as support is destroyed.
- m3: facts 2 ext (tags 1,2), 2 self (tags 3,4);
  form(0): ext=2, self=2. 2x bp4_disconf_learn: sup
  80,60; d_self stays 255 (strict > fails at tie).
- m4: facts 3 self (3,4,6), 1 ext (2); form(0):
  ext=1, self=3, formed=4, sup=100. Kill 2 self
  facts via bp7_kill_self_prov x2; bp2_relicense:
  live=2, formed=4: sup=100*2/4=50; recount:
  ext=1, self=1. 2x bp4_disconf_learn: sup 30,10;
  disc=2; d_self stays 255: the majority condition
  is evaluated live at each disconfirmation, not
  frozen at formation.

## 3. Arm META: meta-parameter sweep (world WM)

tnn2_init. fa1=ev_teach(701,71,10), fa2=ev_teach(702,
72,20), fa3=ev_teach(703,73,30), fa4=ev_teach(704,74,
40); tags 2/6/2/6. mA=promote_graph(WM,-1,701,71,10,
[fa1..fa4],4); bp2_form(mA,0): sup=100, ext=2,
self=2, d_self=255. mB=alloc_node bare B-COMP;
bp2_form(mB,1); 2x bp2_disconfirm -> sup=60.

Evidence script (world-driven, BP-6 BA shape):
- e1: sel=bp2_select({mA,mB},2,bar); eff_c=eff(mA)
  =100; ev_observe(WM,702,72,999) -> type-3 on fa2
  -> absorb -> R3(mA): sup 80; cf=1 (FP).
- e2: eff_c=80; ev_observe(WM,701,71,10) -> type-7
  on fa1 -> R2: sup 90; cf=0 (TP).
- e3: eff_c=90; ev_observe(WM,703,73,30) -> R2:
  sup 100; cf=0.
- e4: eff_c=100; ev_observe(WM,704,74,40) -> R2:
  sup 110; cf=0.
- e5: eff_c=110; ev_observe(WM,701,71,10) -> second
  type-7 on fa1 -> R2: sup 120; cf=0.
Selection is bar-independent here: mA eff
100..110 > mB eff 60 > every bar (max 53), no ties,
so all 30 selections must be mA.

Six settings (inc,dec,thr_num,thr_den), minbar=10,
bar0=50; update: bp7_bar_param(bar,cf,eff_c,...).
Hand-derived trajectories:
- S1 (1,1,2,1) frozen: 50->51->51->51->51->50.
  Final 50. Replicates BP-6 BA as control.
- S2 (3,1,2,1): 50->53->53->53->53->52 (e5:
  110>=106 -> 52). Final 52: raise step dominates,
  upward drift.
- S3 (1,3,2,1): 50->51->51->51->51->48 (e5:
  110>=102 -> 48). Final 48: lower step dominates,
  downward drift.
- S4 (1,1,3,2) 1.5x: e1: 51; e2: 80*2=160>=51*3
  =153 -> 50; e3: 90*2=180>=150 -> 49; e4:
  100*2=200>=147 -> 48; e5: 110*2=220>=144 -> 47.
  Final 47: hair-trigger threshold ratchets down
  every step.
- S5 (0,1,2,1): 50->50->50->49->48 (e4: 100>=2*50
  =100 -> 49; e5: 110>=2*49=98 -> 48). Final 48: FP
  never moves the bar; the raise is load-bearing. S3
  and S5 share the final 48; they are discriminated at
  e1 (51 vs 50: the FP raise step), promoted to
  explicit bars K-MT-S3E1/K-MT-S5E1 below.
- S6 (1,0,2,1): 50->51->51->51->51->51 (e5:
  110>=102 but dec=0 -> 51). Final 51: permanent
  ratchet, never recovers.

Unit checks (pure function):
- bp7_bar_param(50,1,100,1,1,2,1,10)==51.
- bp7_bar_param(51,0,80,1,1,3,2,10)==50.
- bp7_bar_param(10,0,25,1,1,2,1,10)==10.
- bp7_bar_param(50,1,100,0,1,2,1,10)==50.

Stability reading (reasoned, not a bar): only S1
is neutral over the balanced cycle (returns to
50); S2 drifts up, S3/S4 drift down, S5 ignores
FPs, S6 never recovers. The stable region is the
inc/dec-balanced band around the frozen setting.

## 4. Arm PBAR: per-belief bars (world WP)

tnn2_init. mA: ga1=ev_teach(801,81,10) tag 2,
ga2=ev_teach(802,82,20) tag 6, ga3=ev_teach(804,84,25)
tag 2; mA=promote_graph(WP,-1,801,81,10,
[ga1,ga2,ga3],3); bp2_form(mA,0): sup=100, ext=2,
self=1. (Three facts: the block writes at most one
type-3 per fact, probe-verified 2026-10-03 in
/tmp/bp7probe; each FP below contradicts a fresh
fact. A repeated contradict returns 1 and writes no
new edge, and a contradicted fact ignores later
matches.)
mB=alloc_node; bp2_form(mB,1); bp2_revise(mB) ->
sup=50 (bare B-COMP: eff=sup=50).
mX=alloc_node; bp2_form(mX,1); bp2_revise(mX) ->
sup=50.
mO: go1=ev_teach(805,85,30) tag 2;
mO=promote_graph(WP,-1,805,85,30,[go1],1);
bp2_form(mO,0): sup=100, ext=1, self=0.
gbar=50; pb[0..1023]=50.

Help script (world-driven FPs on mA, one fresh fact
per FP):
- FP1: contradict ga1 (ev_observe(WP,801,81,999))
  -> type-3 -> absorb -> R3(mA): sup 80.
  gbar=bp2_bar_after(50,1,100)=51.
  pb[mA]=bp7_bar_param(50,1,100,1,1,2,1,10)=51;
  pb[mB]=50 (mB never commits).
- FP2,FP3: contradict ga2 (ev_observe(WP,802,82,
  999)) then ga3 (ev_observe(WP,804,84,999)): sup
  60,40; gbar 52,53; pb[mA]=53. (eff(mA)=sup
  throughout: d_self=255, partition (2,1).)

Hand-derived comparisons:
- After FP1: bp2_select({mB},1,51)==-3 (50<51:
  the innocent is excluded by the global bar);
  bp7_select_pbar({mB},1,pb)==mB (50>=50: the
  per-belief penalty stays on mA). Isolation.
- After FP3: bp2_select({mA,mB},2,53)==-3 (40<53
  and 50<53: global bar abstains entirely);
  bp7_select_pbar({mA,mB},2,pb)==mB (mA 40<53
  excluded, mB 50>=50 admitted). Availability.
- mX own FP (direct bookkeeping):
  pb[mX]=bp7_bar_param(50,1,100,1,1,2,1,10)=51;
  bp7_select_pbar({mX},1,pb)==-3 (50<51): the
  per-belief bar still has teeth where earned.

Overfit script (mO lucky streak, world-driven):
- 40x: sel=bp7_select_pbar({mO},1,pb) (must be
  mO); ev_observe(WP,805,85,30) -> type-7 on go1
  -> absorb -> R2(mO,0); pb[mO]=bp7_bar_param(
  pb,0,eff_c,1,1,2,1,10) with eff_c=sup before
  the confirm. sup: 100+20k clamped: k=1:120...
  k=8:255; conf=41 (formation sets b_conf=1, plus
  40 R2s). pb: 50->49->...->10 (every step eff_c
  >= 2*pb: k=1: 100>=100; holds all the way down). The global bar does NOT move on
  mO's outcomes (credit-assignment scope under
  test; disclosed in Section 1).
- Then 12x direct bp2_disconfirm(mO) (driver-side,
  non-commitment evidence, BP-6 COMB-arm
  convention): sup 255->15; disc=12; pb[mO]=10.

Hand-derived: eff(mO)=15 (ne=1,nself=0 -> eff=
sup). bp7_select_pbar({mO},1,pb)==mO (15>=10:
selected on thin evidence); bp2_select({mO},1,
53)==-3 (15<53: the population-informed global
bar refuses). The per-belief bar overfits to the
local lucky streak: help and cost both measured.

## 5. Kill bars (frozen)

Preconditions:
- PC-DS-FORM: m: sup==100 && ext==1 && self==3
  && d_self==255; m2: ext==3 && self==1; m3:
  ext==2 && self==2; m4: ext==1 && self==3.
- PC-MT-FORM: mA: sup==100 && ext==2 && self==2;
  mB: sup==60.
- PC-PB-FORM: mA: sup==100 && ext==2 && self==1;
  mB: sup==50; mX: sup==50; mO: sup==100.

DSELF bars:
- K-DS-TRJ: after 10x: d_self[m]==5 &&
  b_sup[m]==0 && b_disc[m]==10 && b_conf[m]==0.
- K-DS-FLOOR: after 11th: d_self[m]==0.
- K-DS-NOREC: after 3x R2: d_self[m]==0 &&
  b_sup[m]==30 && b_conf[m]==3.
- K-DS-EFF: bp2_eff(bt,m)==7.
- K-DS-SEL: m2 after 5x: d_self[m2]==255 &&
  b_sup[m2]==0 && b_disc[m2]==5.
- K-DS-BOUND: m3 after 2x: d_self[m3]==255 &&
  b_sup[m3]==60.
- K-DS-FLIP: m4 after kills+relicense+2x:
  d_self[m4]==255 && b_sup[m4]==10 &&
  b_ext[m4]==1 && b_self[m4]==1.

META bars:
- K-MT-U1..U4: unit values above (51/50/10/50).
- K-MT-S1: final bar S1==50.
- K-MT-S2: final bar S2==52.
- K-MT-S3: final bar S3==48.
- K-MT-S4: final bar S4==47.
- K-MT-S5: final bar S5==48.
- K-MT-S6: final bar S6==51.
- K-MT-S3E1: bar S3 after e1==51.
- K-MT-S5E1: bar S5 after e1==50 (the FP raise
  step discriminates S3 from S5; both end at 48).
- K-MT-SEL: all 30 selections (5 events x 6
  settings) == mA.

PBAR bars:
- K-PB-ISO: after FP1: bp2_select({mB},1,51)
  ==-3 && bp7_select_pbar({mB},1,pb)==mB.
- K-PB-AVAIL: after FP3: bp2_select({mA,mB},2,
  53)==-3 && bp7_select_pbar({mA,mB},2,pb)==mB.
- K-PB-TEETH: pb[mX]==51 &&
  bp7_select_pbar({mX},1,pb)==-3.
- K-PB-STREAK: pb[mO]==10 && b_sup[mO]==255 &&
  b_conf[mO]==41 (formation sets b_conf=1).
- K-PB-OVERFIT: after 12x R3: b_sup[mO]==15 &&
  bp7_select_pbar({mO},1,pb)==mO &&
  bp2_select({mO},1,53)==-3.

Determinism and hygiene:
- K-DET: 3/3 runs byte-identical whole-output
  (SHA-256).
- K-HYG: pure Zag under safebin (`which python3` /
  `which python` empty at build and run); zero em/en
  dash bytes in lane files; 0 new edge types (1/3/7/14
  frozen-and-pre-existing; 7 is block-written
  evidence); 0 new node types (tags 1/3/20
  pre-existing); 0 modes, 0 bridges, 0 handlers;
  xf_block.zag SHA-256
  172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
  re-verified before and after the build;
  bp7_learner.zag byte-identical to bp6_learner.zag
  (SHA-256
  2de20f5a0ff87bc45140a161548b613b008e9c2adabf4da3fdda6d6d46040c5e);
  bp4_rules.zag reused verbatim (SHA-256
  7392299309082836bf376bb445492ef8d9fd75b3d857ad425b8ca74d7399e4d9);
  opaque identifiers.

Bar count: 3 PCs + 25 K bars + K-DET + K-HYG = 30.

## 5b. Amendments (2026-10-03, after the first
implementation run; transparent re-freeze)

The first run (23/26) exposed three prereg errors.
No implementation rule was changed to chase a bar;
each correction below re-derives the prediction from
the frozen rule or a measured block behavior. The
implementation was then fixed to match the corrected
world design, and the lane re-run from scratch.

- A1 (K-MT-S5 arithmetic slip): the prereg predicted
  S5 final 49 with trajectory 50->50->50->50->50
  ->49. Wrong: at e4 the bar is already 50 (the FP
  never raised it), so 100 >= 2*50 fires the lower
  one step earlier than written. Correct trajectory:
  50->50->50->49->48, final 48. The implementation
  (unit bars K-MT-U1..U4 all passing) was faithful
  to the frozen rule; the hand composition was not.
  Consequence: S3 and S5 share the final 48 (both
  end low by different routes). Discrimination is
  preserved by promoting the already-preregistered
  e1 values to explicit bars: K-MT-S3E1==51,
  K-MT-S5E1==50 (the inc step is what separates
  them).
- A2 (K-PB-STREAK conf slip): the prereg predicted
  b_conf==40 after 40 R2s. Wrong: bp2_form sets
  b_conf=1 at formation (same pattern as BP-6
  PC-COMB-FORM: 2 confirms -> conf 3). Correct:
  41.
- A3 (repeat-contradict block behavior): the prereg
  assumed each ev_observe contradict writes one new
  type-3. Probe-measured 2026-10-03 (/tmp/bp7probe,
  ephemeral): the first contradict on a fact returns
  0 and writes one type-3; a second contradict on
  the same fact returns 1 and writes nothing; a
  contradicted fact also ignores later matches
  (ret 0, no type-7). So the PBAR world as built
  could not deliver FP3 (repeat contradict on ga1:
  no R3, cf=0, gbar stuck at 52). World fix: mA
  now promotes 3 facts (tags 2,6,2; ext=2, self=1;
  PC-PB-FORM updated) and FP1/FP2/FP3 contradict
  ga1/ga2/ga3 once each; mO's fact renumbered to
  (805,85,30) to avoid key overlap. All downstream
  hand-derivations are unchanged (eff(mA)=sup still
  holds with partition (2,1)).

## 6. Falsifiers (what kills the claim)

- DSELF: any trajectory value != hand-derived
  (d_self wraparound at the floor kills the floor
  reading); confirmations move d_self (a recovery
  path exists in the frozen machinery, contradicting
  the one-way claim); m2/m3 discount (source
  selectivity broken); m4 discounts after the flip
  (majority not evaluated live).
- META: any setting final != hand-derived; S1 !=
  BP-6's BA trajectory (control replication fails);
  any selection != mA (outcome sequence not
  bar-independent).
- PBAR: global bar fails to exclude mB after FP1
  (no isolation gap); per-belief selection admits
  mA at FP3 (penalty leaks); mX admitted at pb 51
  (teeth missing); mO streak values differ; no
  divergence at eff 15 (no overfit gap).

## 7. Verdict rule

BP-7-PASS iff every PC bar and every K bar passes on
the frozen implementation, 3/3 byte-identical. A
single failed K bar fails its arm. This lane does not
re-open the 7 sealed predictions, does not change R7
or the bar rule, and adds no learner machinery. The
per-belief bars and parameterized rule are
experimental comparisons only.

## 8. Out of scope (not claimed)

Whether per-belief bars should replace the global
bar (measured help and cost, design judgment left to
the parent); which meta-parameter setting is
"correct" (sensitivity mapped, stability region
reasoned); a learner-owned d_self recovery rule
(tested absent, not implemented); multi-channel
absorption.
