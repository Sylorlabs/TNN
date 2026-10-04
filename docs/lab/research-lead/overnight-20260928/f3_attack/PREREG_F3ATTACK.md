# PREREG_F3ATTACK: Alternative-explanation attack on F3 Phase 3 BUILD-PASS

Date: 2026-09-30. Worker: F3 Alternative-Explanation Attacker.
Target: F3 Phase 3 BUILD-PASS (41ed1ef9a). Learner: f3_p3.zag (frozen).
Prereg: 97287f87c. Amendment: c35da8aa0. T-NEG result: 41ed1ef9a.
Status: PREREGISTRATION. No attack implementation exists yet.
Pipeline step 6 (alternative-explanation attack). Pure Zag. No Python.

## 1. The claim under attack

F3 Phase 3 claims BUILD-PASS via the OP-GROW mechanism:
- T-CONJ: trial-driven GROW forms the conjunction {(X,+,2),(Z,+,1)}.
- T-NEG: goal-failure-driven GROW forms {(X,+,1),(Z,-,1)}; replan
  clears Z; GOAL_REAL=1.

The prereg (section 2) describes the T-NEG goal-failure GROW as a
general mechanism: "The goal failure is treated as a refutation of
the planned rule: OP-GROW searches for L false at failure and true
on all correct firings." Section 7 discloses it as "a simplified
precursor of Phase 7 REVISE."

## 2. Code-grounded alternative hypotheses

### H-NAME (world-identity gating; primary)

Inspection of the frozen learner f3_p3.zag shows:

- Lines 1237-1242: the learner reads w_worldname(). If the first
  byte is 65 ('A', "ADV1-conjunctive") it sets is_conj_world=1.
  If the first byte is 84 ('T', "TNEG-grow-negation") it sets
  is_neg_world=1.
- Line 1295: the goal-failure GROW path executes ONLY under
  `if(is_neg_world==1 && attempt==1)`. The comment reads "For T-NEG,
  try OP-GROW on the Y rules using the goal execution ws as the
  refutation observation."
- Lines 1378-1379: the verdict world_pass requires the matching
  world-name flag.

The prereg does NOT disclose that the goal-failure GROW is gated on
detecting the world's name string. A "simplified precursor of
REVISE" would be "on goal failure, try OP-GROW" (general). What is
implemented is "on goal failure, IF the world name starts with 'T',
try OP-GROW" (world-specific).

Alternative explanation: the T-NEG "negation learning" (P-GROW-N,
P-REPLAN-N) is not produced by a general causal mechanism. It is
produced by a world-specific recovery script that runs only because
the learner recognizes the world's name. The learner does not
"discover" negation; it knows it is in the negation world and runs
the negation script.

Test: world_tneg_renamed.zag. Byte-identical to the sealed
world_tneg_a.zag EXCEPT w_worldname returns "XNEG-grow-negation"
(first byte 'X'=88, not 'T'=84). Sealed truth, passive schedule,
goal setup, interface, and main() block are unchanged. Run the
FROZEN unmodified f3_p3.zag on it.

- Prediction under H-NAME: is_neg_world=0. No
  "F3P3 GOAL_FAIL_GROW_ATTEMPT" line. No "F3P3 GROW_OK (goal-fail)"
  line. GOAL_REAL=0 on attempt 1. No attempt 2. The negation is not
  learned. The "discovery" disappears when the name changes.
- Prediction under the general-mechanism claim: the learner treats
  goal failure as refutation regardless of world name; GROW fires;
  (Z,-,1) is learned; replan clears Z; GOAL_REAL=1 on attempt 2.

Kill contribution: H-NAME confirmed KILLS the Phase 3 BUILD-PASS,
because T-NEG's "negation via OP-GROW" is then explained by
world-name gating, not by a general causal learning mechanism.
T-CONJ alone cannot carry Phase 3 (the frozen K2 bar requires
T-NEG: "negation literal learned via GROW on goal failure").

### H-ABL (decorative causal condition; ablation)

F3_grow_search (lines 307-380) has two conditions:
(a) L false at refutation time t_ref.
(b) L true on all true positives in the passive trace (with at
least one true positive).

Condition (b) is the causal part: it ensures L is consistent with
all observed correct firings. Without (b), the search degrades to
"first literal false at refutation," which is not causal learning.

Alternative explanation: condition (b) is decorative. The sealed
results can be produced by condition (a) alone, because the search
order (c, pol, d) happens to hit the right literal first.

Test: f3_p3_abl.zag. Copy of the frozen f3_p3.zag with F3_grow_search
modified to DROP condition (b): when false_at_ref==1, immediately
write out (c, pol, d) and return 1, skipping the true-positive
scan. Search order unchanged. Run on the SEALED worlds
(world_adv1.zag for T-CONJ, world_tneg_a.zag for T-NEG), unmodified.

- Prediction under H-ABL: the ablated learner still achieves
  GOAL_REAL=1 on both sealed worlds (the simpler rule suffices;
  the causal condition does no work).
- Prediction under the mechanism claim: the ablated learner fails
  at least one sealed world (grows a wrong literal, or fails to
  converge, or exceeds cost).

Kill contribution: H-ABL confirmed KILLS the OP-GROW mechanism
claim, because the advertised causal search is then unnecessary;
a non-causal heuristic explains the sealed results.

### H-SCHED (schedule fitting; sensitivity)

Both sealed worlds use fixed simple passive schedules designed by
the researcher. T-CONJ: X at t=2,8; Z at t=3,9. T-NEG: X at t=2,6.
The prereg predictions are specific to these schedules.

Alternative explanation: OP-GROW is fitted to the specific passive
schedules, not a general causal learner. A different schedule with
the same causal truth defeats it.

Test: world_conj2.zag. Same sealed truth Y(t)=X(t-2) AND Z(t-1),
same w_* interface shape (4 vars, X/Z ctrl, Y target, W dummy),
but a different passive schedule: X pulsed at t=1,5; Z pulsed at
t=2,6; hence Y=1 at t=3,7. The relative causal delays are preserved;
only the absolute times change. Run the FROZEN unmodified f3_p3.zag
on it. The world name starts with 'A' ("ADV1-conjunctive-2") so the
verdict path is the T-CONJ one.

- Prediction under H-SCHED: the learner fails (GOAL_REAL=0, or the
  converged rule set lacks the conjunction, or cost exceeded).
- Prediction under the general-mechanism claim: the learner
  succeeds (GOAL_REAL=1; conjunction learned; cost within bound).

Kill contribution: H-SCHED confirmed WEAKENS but does not alone
KILL; a schedule failure indicates limited generality, not a
void mechanism. It contributes to a kill only combined with H-NAME
or H-ABL.

## 3. Overall verdict rule

- F3-ATTACK-KILLS if H-NAME is confirmed (world-name gating
  explains T-NEG).
- F3-ATTACK-KILLS if H-ABL is confirmed (causal condition
  decorative).
- F3-ATTACK-KILLS if H-NAME and H-SCHED are both confirmed
  (mechanism is world-specific AND schedule-fitted).
- F3-ATTACK-SURVIVES otherwise (H-NAME fails and H-ABL fails).

A SURVIVES verdict means the attack did not find a simpler
explanation; it does not promote F3 past BUILD-PASS. Pipeline
steps 7-11 remain.

## 4. Frozen test procedures

### H-NAME

  A=docs/lab/research-lead/overnight-20260928/f3_attack
  P=docs/lab/research-lead/overnight-20260928/f3_phase3
  ZNC=/home/hatch/workspace/tnn-forkbattery-1121pdt/local-tnn-native-lab/znc
  # world_tneg_renamed.zag: copy of $P/world_tneg_a.zag with ONLY
  # w_worldname changed: "TNEG-grow-negation" -> "XNEG-grow-negation".
  # Verified by diff: exactly one line differs.
  cat $P/f3_p3.zag $A/world_tneg_renamed.zag > $A/run_name.zag
  $ZNC $A/run_name.zag -o $A/name_bin
  $A/name_bin > $A/name_r1.txt 2> $A/name_r1.err   (x3, byte-identical)
  # Judge: grep for GOAL_FAIL_GROW_ATTEMPT, GROW_OK (goal-fail),
  # GOAL_REAL values per attempt.

H-NAME confirmed iff: no GOAL_FAIL_GROW_ATTEMPT line appears AND
GOAL_REAL=0 on attempt 1 AND no attempt 2 occurs. (The verdict line
will read PHASE3-FAIL because world_pass requires the name flag;
the verdict is not the test. The mechanism lines are the test.)

### H-ABL

  # f3_p3_abl.zag: copy of $P/f3_p3.zag with condition (b) removed
  # from F3_grow_search. Diff shows only the (b) block deleted.
  cat $A/f3_p3_abl.zag $P/../f2_ablation/world_adv1.zag > $A/run_ablc.zag
  $ZNC $A/run_ablc.zag -o $A/ablc_bin
  $A/ablc_bin > $A/ablc_r1.txt 2> $A/ablc_r1.err   (x3)
  cat $A/f3_p3_abl.zag $P/world_tneg_a.zag > $A/run_abln.zag
  $ZNC $A/run_abln.zag -o $A/abln_bin
  $A/abln_bin > $A/abln_r1.txt 2> $A/abln_r1.err   (x3)
  # Judge: GOAL_REAL per world; GROW_OK lines; converged rules.

H-ABL confirmed iff: ablated learner achieves GOAL_REAL=1 on BOTH
sealed worlds within the cost bound (NEXPS<=8). (If it fails either,
the causal condition does work and H-ABL is rejected.)

### H-SCHED

  # world_conj2.zag: new world, truth Y=X(t-2) AND Z(t-1), schedule
  # X at t=1,5; Z at t=2,6; Y at t=3,7. Name "ADV1-conjunctive-2".
  cat $P/f3_p3.zag $A/world_conj2.zag > $A/run_sched.zag
  $ZNC $A/run_sched.zag -o $A/sched_bin
  $A/sched_bin > $A/sched_r1.txt 2> $A/sched_r1.err   (x3)
  # Judge: GOAL_REAL; HAS_CONJ; converged Y rule set.

H-SCHED confirmed iff: GOAL_REAL=0 OR the converged Y rule set
lacks {(X,+,2),(Z,+,1)}.

## 5. Kill bars

- K1: this prereg is committed alone before any attack artifact
  exists. No world, learner copy, binary, or log may be created
  before the prereg commit.
- K2: the ablation (H-ABL) is implemented and tested on both
  sealed worlds. An attack without the ablation does not satisfy
  K2.
- K3: pure Zag at every stage (znc, sh, cp, diff, grep, git,
  md5sum only). Zero Python. Zero em/en-dash bytes in authored
  files and logs (verified with shell byte checks, not Python).
  3/3 byte-identical runs per test.

## 6. Honest scope

This attack does not modify the sealed worlds or the frozen
learner. All attack artifacts live in f3_attack/. The renamed world
changes only the name string; the ablated learner changes only the
(b) block; the rescheduled world is a new file with a new name.

H-NAME uses code inspection as the hypothesis source and an
empirical run as the test. Code inspection alone does not confirm;
the run must show the mechanism lines absent.

If F3-ATTACK-SURVIVES, F3 Phase 3 remains BUILD-PASS and proceeds
to pipeline step 7 (OOD). If F3-ATTACK-KILLS, the BUILD-PASS is
retracted to BUILD-FAIL with the killing hypothesis named, and the
mechanism returns to design.

No L3 claim is touched by this attack (none was made).
