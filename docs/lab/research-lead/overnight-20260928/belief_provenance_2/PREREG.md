# PREREG: BP-2 (provenance-death + propagation)

Worker: BELIEF-PROVENANCE-2 subagent, 2026-10-03. Non-ledger.
Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_2/`
Status: FROZEN. Committed before any implementation file
exists in this lane. All predicted numbers below are
hand-derived from DESIGN.md Sections 3.1-3.2.

## 0. What is being tested

The BELIEF-PROVENANCE DESIGN.md (committed as `eabbb1994`)
specifies belief records
`(b_sup, b_conf, b_disc, b_rev, b_ext, b_self, d_self)` with
seven generic update rules R1-R7. This lane implements that
layer in pure Zag and tests two falsifiable predictions as
sealed arms, each replaying the frozen XHIER-COUNTMAP-FIX
world (verdict XHIER-COUNTMAP-FIX-PASS), plus the design's
kill criterion for the belief layer itself.

- FP2 (provenance-death): a composite whose licensing facts
  are all tombstoned retires persistently with a kind-3
  reason-2 edge (not just a per-query binary fence).
- FP3 (propagation): tombstoning a licensing fact propagates
  weakening along type-14 edges to dependent composites and
  flips R7 selection to a rival.
- Kill criterion (DESIGN.md Section 8): if R7 selections
  always agree with plain liveness-gating, the belief layer
  is decorative and must not ship. Vindication needs a sealed
  world where existence says use-it, belief says refuse, and
  belief is right. The K3a replay is the candidate world.

Comparison target: XHIER-COUNTMAP-FIX's binary fences
(per-query -2: XHIER-EXEC-NOAGG / XHIER-EXEC-NOREL) versus
the belief layer's graded weakening plus persistent
retirement.

## 1. Researcher machinery (frozen constants, disclosed)

Record: 8 u8 fields per node id
`[b_sup, b_conf, b_disc, b_rev, b_ext, b_self, d_self, formed]`.
`formed` = live type-1 licensing count at R1 (needed by R4;
DESIGN.md names the first seven fields, `formed` is the
stated "count at R1" the R4 formula references).

Constants: BASE=100, INC_HI=20, INC_LO=10, DEC=20, BAR0=50,
MIN_BAR=10. (INC_LO, DEC, MIN_BAR are implemented but not
triggered in these arms; listed for completeness.)

R1: b_sup=BASE; b_conf=1; b_disc=0; b_rev=0; b_ext/b_self from
the P6 partition of live type-1 targets (field16: 1/2/5
EXTERNAL, 3/4/6 SELF, else neither); d_self=255;
formed=live count. B-COMP records (no type-1 licensing of
their own) form with b_ext=b_self=formed=0; their support is
maintained by R6.

R2: b_sup += INC_HI (indep) or INC_LO, saturate 255;
b_conf++, b_disc=0.

R3: implemented, not triggered in these arms.

R4: recompute live type-1 targets; live=count, formed=count
at R1; b_sup = b_sup * live / formed (integer truncation);
refresh b_ext/b_self; if live=0 then b_retire(reason=2).
READING (frozen for this prereg): the formula is applied to
the CURRENT b_sup each call, so successive calls compound:
with formed=4, b_sup goes 100 -> 100*3/4=75 -> 75*2/4=37
(150/4 truncates) -> 37*1/4=9 -> live=0 retires. DESIGN.md
S1's "scales 4/4 -> 3/4 -> ... -> 0/4" is read as the
live-fraction sequence, not the support sequence. If the
runs show 50/25 instead, this reading is falsified and the
bars below fail as written; that outcome is recorded, not
patched around.

R5: implemented, not triggered in these arms.

R6: b_sup[z] = min over live type-14 targets with belief
records of b_sup; if the min is 0, b_retire(z, reason=2).

R7: among live candidates with records, argmax eff; exact
tie at top or max eff < bar returns -3 (abstain). eff =
b_sup * (b_ext*255 + d_self*b_self) / (255*(b_ext+b_self));
eff = b_sup when b_ext+b_self=0. bar=BAR0=50 for all arms:
no commitment-outcome events occur (R7 selections are
measured, never fed back as confirm/disconfirm), so the
bar-adjustment rule is implemented but never triggered;
this is disclosed, not hidden.

b_retire(mid, reason): writes kind-3 self-edge on mid with
field12=reason (consistent with the frozen block's
contradict_map/is_superseded kind-3 self-edge convention,
reason carried in the clk slot per P10); sets b_sup=0. The
record persists (retired, not deleted); the node stays live.

Liveness-gate baseline lg(cands): first live candidate node
id, or -1. This is the "plain liveness-gating" of the kill
criterion: existence implies endorsement.

P6 note: in the frozen block, ev_teach/write_node never set
field16, and alloc_node zeroes it, so all licensing facts
are field16=0 (UNKNOWN, in neither partition). The
partition rule is implemented exactly as designed; in this
world it yields b_ext=b_self=0, hence eff=b_sup. d_self
stays 255 (FP4 is out of scope).

Domain-blindness: every rule references only node liveness,
edge types (1/14/3), integer counts, field8/field4 equality
for conflict sets, and the field16 partition. No relation
is interpreted; no domain label is read.

## 2. World replay (per arm, fresh workspace)

Each arm replays the frozen XHIER-COUNTMAP-FIX phases on a
fresh workspace W (z_alloc(110656), tnn2_init):

- Phase A: ev_teach nav (11,81,12),(12,81,13),(13,81,14);
  ev_query_xs5(11,91,14,0) forms nav MAP;
  ev_teach (50,82,51),(51,82,52),(52,82,53);
  ev_query_xs5(50,92,3,0) forms MAP_Y (rel 82); 30
  distractors.
- Phase B: ev_teach (110,85,111..113,85,114);
  ev_query_xs5(110,117,4,0) forms MAP_V2 (rel 85).
- Phase B2: ev_teach (120,87,121..123,87,124);
  ev_query_xs5(120,118,4,0) forms MAP_V3 (rel 87).
- Phase R: ev_teach (14,82,40),(40,82,41);
  xs5_compose(11,94,2) forms MAP_Z1 (nav + MAP_Y).
- Phase C: ev_teach 87-chain at 14 (60..63) and 85-chain at
  14 (30..32); MAP_Z2 = promote_graph(-1,11,93,4,empty,0) +
  LINK14 navx + LINK14 MAP_V3. FP3 arm also builds MAP_Z3 =
  promote_graph(-1,11,93,4,empty,0) + LINK14 navx + LINK14
  MAP_V2 here, BEFORE the tombstone (preserves the XF
  no-allocation-after-tombstone invariant).
- Phase T: tombstone MAP_Y (ns 0/36 pattern), no restore.
  Singleton becomes MAP_V2 (rel 85); MAP_Z2's own live
  count MAP stays MAP_V3 (rel 87).

Expected replay ids (from the XF REPORT): MAP_Y=84,
navx=27, MAP_V2=194, MAP_V3=274, MAP_Z1=290, MAP_Z2=311.
Belief records are formed AFTER the replay, for: nav MAP,
MAP_V3, MAP_V2 (FP3 also MAP_Z3's components), MAP_Z2
(B-COMP), MAP_Z3 (B-COMP, FP3 only).

## 3. Arm FP2: provenance-death (workspace W2)

Candidates for R7: {MAP_Z2} only. Beliefs formed at BASE.

- t0 (pre): b_sup V3=100 (4/4 live), Z2=100, nav=100.
- t1: tombstone ONE of MAP_V3's 4 type-1 facts. R4:
  live=3, b_sup[V3]=100*3/4=75. R6: b_sup[Z2]=min(100,75)
  =75.
- t2: tombstone a second fact. R4: live=2,
  b_sup[V3]=75*2/4=37. R6: b_sup[Z2]=37.
- t3: tombstone a third fact. R4: live=1,
  b_sup[V3]=37*1/4=9. R6: b_sup[Z2]=9.
- t4: tombstone the fourth fact. R4: live=0 ->
  b_retire(MAP_V3,2): kind-3 self-edge reason 2 on MAP_V3,
  b_sup=0. R6: b_sup[Z2]=min(100,0)=0 ->
  b_retire(MAP_Z2,2): kind-3 self-edge reason 2 on MAP_Z2,
  b_sup=0.
- Persistence: three further R7({Z2}) queries.

Binary-layer measurements at each step: xhier_exec(W2,Z2,11).

## 4. Arm FP3: propagation (workspace W3)

Candidates for R7: {MAP_Z2 (A), MAP_Z3 (B)}, both
(field8,field4)=(11,93). Setup: all beliefs at BASE, then
b_confirm(Z2, indep=1) modeling the K1 verified execution
of MAP_Z2 (the composite under test in the frozen world):
b_sup[Z2]=100+20=120. R6 at setup is a no-op
(min(100,100)=100 for both).

- s0: R7({Z2,Z3}): eff 120 vs 100 -> Z2. lg -> Z2 (lower
  id first).
- s1: tombstone exactly ONE of MAP_V3's 4 type-1 facts.
  R4: live=3, b_sup[V3]=100*3/4=75. R6(Z2)=min(100,75)=75;
  R6(Z3)=min(100,100)=100. R7: 75 vs 100 -> Z3. lg -> Z2.

No edge of MAP_Z2 itself is written in s1; the only write
is the fact tombstone (ns 0/36 on the fact node).

## 5. Kill bars (frozen)

Preconditions (world replay; all must pass):
- PC-W2.0: post-tombstone singleton == MAP_V2 id.
- PC-W2.1: MAP_V3 prov rel == 87; MAP_V3 has 4 live tag-1
  type-1 targets at belief formation.
- PC-W2.2: MAP_Z2 is MAP_Z; its type-14 count MAP ==
  MAP_V3 id.
- PC-W3.0..W3.2: same as W2 on W3.
- PC-W3.3: MAP_Z3 is MAP_Z; (field8,field4)==(11,93); its
  live type-14 targets are exactly {navx, MAP_V2}.

FP2 bars:
- K-FP2-G1 (graded t1): live=3; b_sup[V3]=75;
  b_sup[Z2]=75; R7({Z2})=MAP_Z2; lg=MAP_Z2;
  xhier_exec=4.
- K-FP2-G2 (graded t2): live=2; b_sup[V3]=37;
  b_sup[Z2]=37; R7=-3; lg=MAP_Z2; xhier_exec=4.
- K-FP2-G3 (graded t3): live=1; b_sup[V3]=9;
  b_sup[Z2]=9; R7=-3; lg=MAP_Z2; xhier_exec=4.
- K-FP2-D1 (death): live=0; b_sup[V3]=0; b_sup[Z2]=0;
  kind-3 self-edge with field12=2 exists on MAP_V3 AND on
  MAP_Z2; no kind-3 edge existed on either before t4.
- K-FP2-D2 (persistent): three consecutive R7({Z2})
  queries all return -3; MAP_Z2 is never selected at or
  after t4 although its node stays live.
- K-FP2-D3 (kill criterion): at t4, lg({Z2})=MAP_Z2
  (node live) while R7=-3: DISAGREE. Belief is right
  because the XF K3a control leg showed liveness-gating
  silently computing 3 from this destroyed provenance.
- K-FP2-C1 (binary contrast): at t4,
  xhier_exec(W2,MAP_Z2,11)=-2 with XHIER-EXEC-NOREL in the
  trace. Contrast table: binary layer per step
  (4,4,4,-2-fence) vs belief R7 per step
  (Z2,Z2,-3,-3,-3): graded weakening from t1, persistent
  retirement at t4, no per-query fence needed.

FP3 bars:
- K-FP3-S1 (setup): b_sup[Z2]=120; b_sup[Z3]=100;
  R7({Z2,Z3})=MAP_Z2; lg=MAP_Z2.
- K-FP3-F1 (flip): after exactly one tombstone: live=3;
  b_sup[V3]=75; b_sup[Z2]=75; b_sup[Z3]=100;
  R7({Z2,Z3})=MAP_Z3; lg=MAP_Z2. The flip occurs at the
  R4-predicted point (first tombstone), not before or
  later.
- K-FP3-F2 (no touch): MAP_Z2's edge census (edges with
  from==MAP_Z2) identical before/after s1; no kind-3 edge
  on MAP_Z2; exactly one fact tombstoned.
- K-FP3-F3 (kill criterion): lg=MAP_Z2 vs R7=MAP_Z3:
  DISAGREE. Belief is right: Z2's licensing is degraded
  (1 of 4 facts destroyed) while Z3 is fully licensed; the
  XF K1 leg showed selection must track the composite's
  own provenance.

Determinism and hygiene:
- K-DET: 3/3 runs byte-identical whole-output (SHA-256).
- K-HYG: pure Zag under safebin (`which python3` empty at
  build and run); zero em/en dash bytes in lane files; 0
  new edge types (only 1/14/3), 0 new node types, 0 modes,
  0 bridges, 0 handlers; xf_block.zag (the patched
  XHIER-COUNTMAP-FIX block) SHA-256
  172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
  re-verified before and after the build; opaque identifiers.

## 6. Falsifiers (what kills the claim)

- FP2: any selection of MAP_Z2 at or after t4; retirement
  without the kind-3 reason-2 edge on both structures;
  graded values differing from (75,37,9) (falsifies the
  R4 reading as preregistered); R7==lg at t4.
- FP3: no flip; flip at a non-R6-predicted point; any
  edge of MAP_Z2 written in s1 besides the tombstone;
  lg==R7 throughout the arm.
- Design kill criterion: if every measured R7 selection in
  both arms agrees with lg, the belief layer is decorative:
  verdict BP-2-FAIL (decorative), must not ship.

## 7. Verdict rule

BP-2-PASS iff every PC bar and every K bar passes on the
frozen implementation, 3/3 byte-identical. A single failed
K bar fails its arm; a failed kill-criterion bar
(K-FP2-D3/K-FP3-F3 showing agreement) fails the design.

## 8. Out of scope (not claimed)

FP1/FP4/FP5/FP6/FP7, R3/R5 dynamics, bar adjustment
trajectories, d_self learning, B-FACT/B-META records,
multi-hop/cyclic propagation fixpoints, combiner
alternatives to min, eviction interaction. The R4
compounding reading is a frozen prereg choice, not a
design amendment.
