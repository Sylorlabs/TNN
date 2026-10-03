# PREREG: BP-3 (domain-blindness + abstention)

Worker: BELIEF-PROVENANCE-3 subagent, 2026-10-03. Non-ledger.
Lane: `docs/lab/research-lead/overnight-20260928/belief_provenance_3/`
Status: FROZEN. Committed before any implementation file
exists in this lane. All predicted numbers below are
hand-derived from DESIGN.md Sections 3.1-3.2 and the BP-2
measured R4/R6/R7 behavior (BP-2-PASS, 18/18).

## 0. What is being tested

The BELIEF-PROVENANCE DESIGN.md specifies two remaining
falsifiable predictions not yet sealed (BP-2 tested FP2/FP3;
BP-1 tested evidential adjudication). This lane implements
them as sealed arms on the frozen belief machinery, plus the
task's "does abstention help" question.

- FP6 (domain-blindness, DESIGN.md Section 7): opaque
  permutation of all relation and entity ids, world
  otherwise identical. Predicted: belief tables and the
  full selection trace byte-identical. Falsifier: any byte
  difference.
- FP7 (abstention, DESIGN.md Section 8): no candidate above
  bar. Predicted: R7 returns -3, no commitment, no
  belief-state side effects (the BP-1 K-4 result at the
  belief layer). Falsifier: commitment without support.
- Help question: does abstention avoid wrong answers, or
  just avoid answering? Tested by a preregistered evidence
  sequence: a weakly-supported leader is disconfirmed after
  the abstention decision (Seq D), and a parallel world
  confirms it instead (Seq C). Predicted: the abstention
  policy never endorses the disconfirmed claim, while a
  forced-pick policy and a lower bar do; the abstention
  policy does endorse when later evidence makes the claim
  endorsable.

Comparison targets: plain liveness-gating (existence implies
endorsement) and a forced argmax policy (always pick the
best available belief, ignoring bar and tie).

## 1. Researcher machinery (frozen constants, disclosed)

The belief layer is BP-2's `bp2_learner.zag` reused VERBATIM
(no redesign): record schema, R1-R7, eff(), b_retire,
bp2_lgsel baseline, bp2_kill_one_prov, bp2_census.
Constants: BASE=100, INC_HI=20, INC_LO=10, DEC=20, BAR0=50,
MIN_BAR=10. The R4 compounding reading is frozen as in
BP-2: successive calls scale the CURRENT b_sup, giving
100 -> 75 -> 37 -> 9 -> retire for formed=4.

New in this lane (driver/test-harness only, not belief
machinery):
- `bp3_perm(x, pm)`: opaque relabeling bijection. pm=0:
  identity. pm=1: x+100000 (order-preserving offset).
  pm=2: 1000000-x (order-reversing reflection). All three
  are exact bijections on the id set; permuted ids never
  collide with node ids (0..1023) or structural constants.
- `bp3_build(W,out,pm,mkz3)`: the BP-2 world replay with
  every entity/relation literal passed through bp3_perm.
  Structural parameters are NOT permuted: ev_query counts
  (3,4), xs5_compose expected (2, a chain-length count),
  promote_graph ans (4, the structural count xhier_exec
  returns), flags, modes, node ids. The nav query expected
  IS permuted: ev_query_xs5(11,91,14) expects the nav
  terminal entity value 14 (XF PREREG line 158: "-> 14"),
  so the permuted call expects bp3_perm(14,pm).
- `bp3_force(bt,hasb,cands,nc)`: forced argmax over eff,
  ignoring the bar and the tie rule (the "always guess"
  baseline policy). Test-harness only.
- `bp3_bufeq(a,b,n)`: byte equality over n bytes.

B-META note: DESIGN.md FP7 predicts "no B-META row
written". B-META records are not implemented in this belief
layer (disclosed in BP-2: "B-FACT/B-META are not formed"),
so that clause is vacuous here; "no commitment" is tested
as: belief table byte-unchanged by R7 queries, no kind-3
edges written, bar untouched.

Bar-adjustment note: as in BP-2, R7 selections are measured
and never fed back as commitment outcomes, so bar stays at
the researcher constant BAR0=50 in all arms except the
explicit bar=30 counterfactual (K-FP7-B3), which is a
researcher-set contrast, disclosed as such.

## 2. Arm FP6: domain-blindness (workspaces W6a/W6b/W6c)

W2-style world (single composite candidate MAP_Z2), built
three times: pm=0 (identity), pm=1 (offset), pm=2
(reflection). Beliefs formed on navx, MAP_V3, MAP_Z2
(B-COMP). Then the BP-2 FP2 measurement sequence on each
arm: t0 (pre), t1..t4 (tombstone one MAP_V3 licensing fact
per step; R4+R6 per step), plus 3 persistence R7 queries.

Hand-derived per-step values (identical for all three
arms; the pm=0 arm reproduces BP-2 exactly):
- t0: live=4, b_sup[V3]=100, b_sup[Z2]=100, R7=MAP_Z2,
  lg=MAP_Z2.
- t1: live=3, b_sup[V3]=100*3/4=75, b_sup[Z2]=75,
  R7=MAP_Z2 (75>=50), lg=MAP_Z2.
- t2: live=2, b_sup[V3]=75*2/4=37 (150/4 truncates),
  b_sup[Z2]=37, R7=-3 (37<50), lg=MAP_Z2.
- t3: live=1, b_sup[V3]=37*1/4=9, b_sup[Z2]=9, R7=-3,
  lg=MAP_Z2.
- t4: live=0, b_retire(V3,2), b_retire(Z2,2) via R6
  min=0; b_sup=0/0; kind-3 reason-2 self-edges on both;
  R7=-3, lg=MAP_Z2.
- persistence: R7 = -3, -3, -3.

Predicted: node ids (navx, mv2, mv3, mz2) identical across
arms; the 8192-byte belief tables byte-identical across
arms at t0,t1,t2,t3,t4; the 1024-byte hasb vectors
byte-identical; the per-step belief trace
(live, b_sup[V3], b_sup[Z2], R7, lg) identical across
arms. xhier_exec values are recorded but informational
(the binary layer is outside FP6's scope, which covers the
belief layer: tables + selection trace).

## 3. Arm FP7a: core abstention (workspace W7a)

W3-style world (pm=0, rival composites MAP_Z2 from MAP_V3
and MAP_Z3 from MAP_V2), NO R2 confirmation. Beliefs formed
on navx, MAP_V3, MAP_V2, MAP_Z2 (B-COMP), MAP_Z3 (B-COMP);
R6 propagate (no-op at 100).

Degrade: tombstone 2 of MAP_V3's facts, then 2 of MAP_V2's
facts. Per MAP: R4 100 -> 100*3/4=75 -> 75*2/4=37.
R6: b_sup[Z2]=min(100,37)=37; b_sup[Z3]=min(100,37)=37.

Hand-derived predictions:
- K-FP7-A1: b_sup[V3]=37, b_sup[V2]=37, b_sup[Z2]=37,
  b_sup[Z3]=37 (all < BAR0=50).
- K-FP7-A2: R7({Z2,Z3},50) = -3 (exact tie at 37; also
  37<50).
- K-FP7-A3: R7({Z2},50) = -3; R7({Z3},50) = -3.
- K-FP7-A4: full 8192-byte belief table byte-identical
  before and after the A2/A3 queries; no kind-3 edge on
  MAP_Z2 or MAP_Z3.
- K-FP7-A5: R7({},50) = -3 (empty candidate set);
  R7({Z2,999},50) = -3 (999 has no belief record; the
  recordless candidate is skipped, Z2 alone is below bar).

## 4. Arm FP7b: does abstention help (workspaces W7b, W7c)

Setup (both worlds, W3-style pm=0): degrade MAP_V3 by 2
facts (100->75->37; R6 Z2=37), degrade MAP_V2 by 3 facts
(100->75->37->9; R6 Z3=9).

Hand-derived setup predictions (both worlds):
b_sup[Z2]=37, b_sup[Z3]=9; R7({Z2,Z3},50) = -3 (max eff
37 < 50, no tie); bp3_force({Z2,Z3}) = MAP_Z2 (37>9).

Seq D (world W7b; models the world revealing the weak
leader's claim as wrong and the rival's as right; this
evidence sequence is researcher-scripted ground truth for
the policy comparison, disclosed):
- bp2_disconfirm(bt,Z2): b_sup = 37-20 = 17; b_disc=1.
- bp2_confirm(bt,Z3,1): b_sup = 9+20 = 29; b_conf=2.
- K-FP7-B2: b_sup[Z2]=17, b_sup[Z3]=29;
  R7({Z2,Z3},50) = -3 (29<50). The abstention policy never
  endorsed Z2 at any point.
- K-FP7-B3 (bar counterfactual): R7({Z2,Z3},30) BEFORE
  the Seq D evidence = MAP_Z2 (37>=30, 37>9, no tie).
  The less-cautious bar commits to the claim the evidence
  then disconfirms; the BAR0 bar abstains. (Post-evidence
  R7(...,30) = -3 since 29<30; informational.)

Seq C (world W7c; the evidence goes the other way):
- Pre-evidence: same setup; R7({Z2,Z3},50) = -3
  (K-FP7-B0 also asserts b_sup[Z2]=37, b_sup[Z3]=9,
  verifying the W7c build).
- bp2_confirm(bt,Z2,1): b_sup = 37+20 = 57.
- bp2_disconfirm(bt,Z3): b_sup = 9-20 -> 0 (floor).
- K-FP7-B4: b_sup[Z2]=57, b_sup[Z3]=0;
  R7({Z2,Z3},50) = MAP_Z2 (57>=50, no tie). The
  abstention policy DOES commit once the evidence makes
  the claim endorsable: abstention is not "never answer".

## 5. Kill bars (frozen)

Preconditions (world builds; all must pass):
- PC6-0A/0B/0C (pm=0): singleton==mv2; prov_rel==87 with 4
  live type-1 facts on mv3; mz2 is MAP_Z with agg==mv3.
- PC6-1A/1B/1C (pm=1): same, with prov_rel==bp3_perm(87,1).
- PC6-2A/2B/2C (pm=2): same, with prov_rel==bp3_perm(87,2).
- PC7a-0/1/2/3 (W7a): singleton==mv2; mv3 prov 4 live;
  mz2 agg==mv3; mz3 is MAP_Z, (field8,field4)==(11,93),
  agg==mv2, nav==navx.
- PC7b-0/1/2/3 (W7b): same as PC7a on W7b.

FP6 bars:
- K-FP6-VAL: pm=0 arm per-step (live, b_sup[V3],
  b_sup[Z2], R7, lg) equals the Section 2 hand-derived
  values at t0..t4; persistence -3,-3,-3.
- K-FP6-IDX: node ids navx, mv2, mv3, mz2 identical
  across pm=0/1/2.
- K-FP6-TAB: bt (8192 B) and hasb (1024 B) byte-identical
  across pm=0/1/2 at each of t0,t1,t2,t3,t4.
- K-FP6-TRC: per-step belief trace (live, b_sup[V3],
  b_sup[Z2], R7, lg) identical across pm=0/1/2.

FP7 bars:
- K-FP7-A1..A5: Section 3 predictions.
- K-FP7-B0: W7c setup (b_sup 37/9, R7(50)=-3).
- K-FP7-B1: W7b setup (b_sup 37/9, R7(50)=-3,
  forced=MAP_Z2).
- K-FP7-B2: W7b Seq D post (b_sup 17/29, R7(50)=-3).
- K-FP7-B3: W7b bar=30 pre-evidence picks MAP_Z2.
- K-FP7-B4: W7c Seq C post (b_sup 57/0, R7(50)=MAP_Z2).

Determinism and hygiene:
- K-DET: 3/3 runs byte-identical whole-output (SHA-256).
- K-HYG: pure Zag under safebin (`which python3` empty at
  build and run); zero em/en dash bytes in lane files; 0
  new edge types (only 1/14/3), 0 new node types, 0 modes,
  0 bridges, 0 handlers; xf_block.zag SHA-256
  172a2e7dbbaa4e60d662331965887327350068e0c13f25e438260ad08313c12a
  re-verified before and after the build; opaque
  identifiers; bp2_learner.zag reused verbatim (hash
  recorded).

## 6. Falsifiers (what kills the claim)

- FP6: any byte difference in bt/hasb across permutations;
  any node-id difference; any trace difference; any
  permuted-arm PC failure (the world must build
  identically or the comparison is void, and the bars
  fail as written).
- FP7: any R7 commitment (result != -3) where -3 is
  predicted; any belief-table mutation by an R7 query; any
  kind-3 edge written by abstention; forced-pick not equal
  to the weak leader pre-evidence; bar=30 not picking the
  leader (the contrast is mismeasured).
- Help question: if R7(50) endorses Z2 pre-evidence in
  Seq D, abstention did not avoid the wrong answer; if
  R7(50) still abstains post-evidence in Seq C, abstention
  is just never-answering.

## 7. Verdict rule

BP-3-PASS iff every PC bar and every K bar passes on the
frozen implementation, 3/3 byte-identical. FP6-PASS and
FP7-PASS are reported per prediction family. A single
failed K bar fails its arm. This lane completes the belief
layer's falsifiable predictions (FP1/FP4/FP5 remain open
per DESIGN.md Section 10).

## 8. Out of scope (not claimed)

FP1/FP4/FP5, R3/R5 dynamics beyond the scripted Seq C/D
evidence, bar-adjustment trajectories (bar stays at BAR0
except the disclosed counterfactual), d_self learning,
B-FACT/B-META records, multi-hop/cyclic propagation,
combiner alternatives, eviction interaction, constant
sensitivity. The Seq C/D evidence is researcher-scripted
ground truth for the policy comparison, not emergent
world behavior; the honest help-answer carries this
disclosure.
