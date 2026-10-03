# REPORT: BP-2 (provenance-death + propagation)

Worker: BELIEF-PROVENANCE-2 subagent, 2026-10-03. Non-ledger
task (claim minting paused); nothing minted.
Branch: tnn-native-lab, local only, never pushed.
Lane: docs/lab/research-lead/overnight-20260928/belief_provenance_2/
Verdict: **BP-2-PASS** (all 7 preconditions, all 11 kill bars,
K-DET 3/3 byte-identical, K-HYG clean). Method: frozen prereg
(committed as 5912fb0eb before any implementation), belief
layer (R1-R7) in pure Zag over the verbatim patched
XHIER-COUNTMAP-FIX block, two sealed arms replaying the
frozen world, in-driver bars.

## 0. What was built

`bp2_learner.zag` implements the DESIGN.md belief layer: a
learner-owned u8 table of records
`(b_sup, b_conf, b_disc, b_rev, b_ext, b_self, d_self,
formed)` per node id, with R1 formation, R2 confirmation,
R3 disconfirmation, R4 relicense (literal 3.2 formula),
R5 revision, R6 propagation (min over live type-14 targets),
R7 selection (argmax eff, -3 abstain), eff(), retirement
via kind-3 self-edge with reason in field12, and the
liveness-gating baseline lg() for the kill criterion. R3/R5
and the bar-adjustment rule are implemented but untriggered
in these arms (disclosed in the prereg); B-FACT/B-META are
not formed.

`bp2_full.zag` = `xf_block.zag` (patched block, verbatim,
SHA-256 172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
re-verified before and after the build) + `bp2_learner.zag`
+ `bp2_driver.zag`. One `main`. Pinned znc, build exit 0;
the 199 A0102 warnings are the benign ignored-return-value
pattern pervasive in the frozen block itself.

`bp2_driver.zag` replays the frozen XHIER-COUNTMAP-FIX
phases on two fresh workspaces and runs the arms:
- W2 (FP2): candidates {MAP_Z2}; tombstone MAP_V3's 4
  licensing facts one at a time (R4+R6+R7+lg+xhier_exec per
  step), then 3 persistence selections.
- W3 (FP3): rival composite MAP_Z3 built in Phase C
  (before the MAP_Y tombstone, preserving the XF
  no-allocation-after-tombstone invariant); one R2
  independent confirmation on MAP_Z2 (models the K1
  verified execution); tombstone exactly one of MAP_V3's
  facts; measure the flip.

Replay fidelity: MAP_Y=84, MAP_V2=194, MAP_V3=274,
navx=27, MAP_Z1=290 exactly as in the XF REPORT;
MAP_Z2=299 here vs 311 there (allocator-order detail;
all structural PCs pass, and the K1-divergence shape
holds: singleton rel 85, MAP_Z2's own rel 87, EXEC=4).

## 1. Kill-bar results

Preconditions (replay matches the frozen world): PC-W2.0,
PC-W2.1, PC-W2.2, PC-W3.0, PC-W3.1, PC-W3.2, PC-W3.3 all
PASS (singleton==MAP_V2; MAP_V3 prov rel 87 with 4 live
type-1 targets; MAP_Z2's own count MAP==MAP_V3; MAP_Z3 is
MAP_Z with (field8,field4)=(11,93) and type-14 targets
{navx, MAP_V2}).

FP2 (provenance-death), all PASS:
- K-FP2-G1: t1: live=3, b_sup[V3]=75, b_sup[Z2]=75,
  R7=Z2, lg=Z2, EXEC=4. Graded weakening, still selected.
- K-FP2-G2: t2: live=2, b_sup=37/37, R7=-3, lg=Z2,
  EXEC=4. Belief abstains below bar while the binary
  layer still executes.
- K-FP2-G3: t3: live=1, b_sup=9/9, R7=-3, lg=Z2,
  EXEC=4.
- K-FP2-D1: t4: live=0, b_sup=0/0, kind-3 self-edge with
  field12=2 on MAP_V3 AND on MAP_Z2; no kind-3 edge on
  either before t4.
- K-FP2-D2: three post-death R7 queries: -3, -3, -3.
  MAP_Z2 never selected at/after t4 although its node
  stays live.
- K-FP2-D3 (kill criterion): at t4 lg=MAP_Z2 (node live)
  vs R7=-3: DISAGREE. Belief is right: the XF K3a
  control leg showed liveness-gating silently computing
  3 from this destroyed provenance.
- K-FP2-C1: binary contrast. Per-step EXEC column:
  4,4,4,-2 (fence trips only at t4, per query, with
  XHIER-EXEC-NOREL). Per-step R7 column: Z2,Z2,-3,-3,-3
  (weakens from t1, refuses from t2, retires persistently
  at t4; xhier_exec is never reached again).

FP3 (propagation), all PASS:
- K-FP3-S1: setup: b_sup[Z2]=120, b_sup[Z3]=100,
  R7=Z2, lg=Z2 (agreement baseline).
- K-FP3-F1: after exactly one tombstone: live=3,
  b_sup[V3]=75, b_sup[Z2]=75, b_sup[Z3]=100, R7=Z3,
  lg=Z2. The flip occurs at the R4-predicted point
  (first tombstone), not before or later.
- K-FP3-F2: MAP_Z2's edge census identical before/after
  (5/5); no kind-3 edge on MAP_Z2; exactly one fact
  tombstoned. Nothing of A was touched but its
  provenance.
- K-FP3-F3 (kill criterion): lg=Z2 vs R7=Z3: DISAGREE.
  Belief is right: Z2's licensing is degraded (1 of 4
  facts destroyed) while Z3 is fully licensed.

K-DET: 3/3 runs byte-identical, SHA-256
9318027e43ecdabf4eb4ce11e87f27bcb475b50324c3ae8c544a63f1096c65a8.
K-HYG: pure Zag under safebin (`which python3` empty at
build and run); zero em/en dash bytes; 0 new edge types
(1/14/3 only), 0 new node types, 0 modes, 0 bridges,
0 handlers; xf_block.zag hash unchanged; opaque ids.
BP2-SUMMARY 18/18.

## 2. What this means

FP2 is confirmed as preregistered: the R4 compounding
reading (75, 37, 9) held exactly, so the literal 3.2
formula is now measured, not just reasoned. A composite
whose licensing facts all die retires persistently with
kind-3 reason-2 edges on both the count MAP and the
composite, and R7 never selects it again. The binary
fence (per-query -2) stays correct as a backstop, but the
belief layer changes behavior strictly earlier and more
informatively: graded weakening from the first death,
refusal below bar while the binary layer would still
execute (t2/t3: belief -3 vs EXEC 4), persistent
retirement at death.

FP3 is confirmed as preregistered: weakening traveled
the type-14 provenance path with no write to the
composite itself, and selection flipped to the healthy
rival at the predicted point. This is behavior the
current architecture cannot express: today only
existence gates change selection.

Kill criterion: both arms show R7 disagreeing with
liveness-gating where belief is right (W2 t2-t4,
W3 s1). The belief layer is load-bearing, not
decorative. It may ship as learner-state machinery
subject to the usual red-team/replication pipeline.

## 3. One-system accounting

New learner machinery: the belief table, R1-R7, eff(),
lg() baseline, all generic over claim-bearing nodes.
0 new edge types (1/14/3 reused), 0 new node types,
0 modes, 0 bridges, 0 handlers, 0 semantic cases.
Beliefs are learner-state records, not a subsystem.

## 4. What was tested vs what was reasoned

Tested (frozen, this lane, PASS): the FP2 graded
sequence and persistent retirement with kind-3
reason-2 edges; the FP3 propagation flip at the
predicted point with no touch to the composite; the
R7-vs-liveness-gating disagreements; determinism;
hygiene.

Reasoned: that the t2/t3 refusal (37/9 < 50) is the
*desirable* operating point rather than merely the
preregistered one (threshold placement is a design
choice, sensitivity analysis is future work); that
compounding R4 is preferable to re-baselining R4
(the prereg froze the literal formula; the
alternative remains untested); the binary-fence
backstop argument.

## 5. Open questions (not claimed)

FP1/FP4/FP5/FP6/FP7, R3/R5 dynamics, bar-adjustment
trajectories, d_self learning, B-FACT/B-META records,
multi-hop and cyclic propagation fixpoints, min vs
product/weighted combiners, eviction interaction,
constant sensitivity. The FP6 domain-blindness
permutation test is the natural next seal for the
domain-blindness claim (Section 7 of DESIGN.md).

## 6. Notes for the parent

- No ledger entry: non-ledger task, nothing minted.
- No push: commits local on tnn-native-lab only,
  explicit pathspecs. This report is committed with the
  lane's implementation artifacts.
- DESIGN.md is untouched; this lane tests it and does
  not reinterpret it. BP-1's REPORT.md is untouched.
- Suggested next step if approved: BP-3 with FP6
  (domain-blindness permutation) and FP7 (abstention)
  as the remaining cheap sealed arms, since the
  machinery and the frozen world are now in place.
- Style: no em/en dashes in this file (hyphens only),
  opaque identifiers throughout.
