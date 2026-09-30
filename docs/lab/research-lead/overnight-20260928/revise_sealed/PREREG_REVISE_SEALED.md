# PREREG: F3 REVISE Sealed Evaluation

Status: FROZEN. This prereg is committed alone, before any sealed
world file, build script, binary, or run exists. It strictly
precedes all sealed-evaluation work (K1).

Parent chain:
- Design: f3_revise/REVISE_DESIGN.md (commit ca157c743), verdict
  REVISE-DESIGN-COMPLETE.
- Builder prereg: f3_revise_impl/PREREG_REVISE_IMPL.md (commit
  c197e7cd8), frozen before implementation.
- Builder result: f3_revise_impl/RESULT_REVISE.md (commit
  7009d711c), verdict REVISE-PASS (bounded L2).
- Pipeline: this is step 3 (sealed evaluation) of the 11-step
  frontier pipeline for the REVISE mechanism.

## 1. Purpose and independence

The builder tested the frozen learner on two worlds it knew
during development (world_adv1.zag, world_tneg_a.zag) plus a
rename. A sealed evaluation re-tests the FROZEN, BYTE-IDENTICAL
learner on NEW worlds designed by an independent evaluator
after the builder's commit, which the builder never saw. The
learner is not modified, tuned, or rebuilt in any way for the
sealed worlds. If the learner fails on a sealed world, the
verdict is REVISE-SEALED-FAIL with diagnosis; the prereg is not
amended to rescue the mechanism.

Frozen learner artifacts (verified by sha256 before any run):
- f3_revise.zag:
  354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392
- f3_revise_abl.zag (condition-(b) ablation):
  4e3bdf0680f11778d9226ac127d20588b40a42295e85af2efaf3a1b77ea786b2
Both match commit 7009d711c byte-for-byte. Any mismatch voids
this evaluation before it starts.

## 2. Sealed world specifications (frozen)

Two new worlds, plus renamed variants. The builder never saw
these structures. Variable naming follows the disclosed
researcher convention X(0), Z(1), Y(2) [W(3) dummy where noted];
the learner resolves X/Z/Y by name (disclosed infrastructure).

### S-CONJ2 (world_sconj2.zag)

- Name string: "SQ3-beta-combine". (The learner cannot read it;
  M-REVISE1 holds. The string carries no answer hint.)
- Vars: X(0,ctrl), Z(1,ctrl), Y(2), W(3,dummy).
  w_nvars()=4, w_nctrl()=2, w_ctrl=[0,1], w_ctxvar()=-1.
- Sealed truth: Y(t) = X(t-3) AND Z(t-2). Pulsed writes, no
  persistence. Out-of-range reads are 0.
- Passive schedule: env SETs X at t=1,7; env SETs Z at t=2,8.
  Then Y=1 exactly at t=4,10:
  t=4: X(1)=1 and Z(2)=1. t=10: X(7)=1 and Z(8)=1.
  No other t satisfies X(t-3)=1 (t in {4,10} only).
- w_goal_setup: start from all-zero (no-op).
- w_goal_mode()=0 (final-state Y=1). w_plan_maxd()=8.
- main emits fixed string "SEALED DONE mask=" (no world name).
- Predicted behavior: discovery finds [X@3] and [Z@2];
  trial phase combines to [X@3 & Z@2]; attempt 1 achieves
  GOAL_REAL 1; D1 trigger does NOT fire (no GOAL_FAIL line).

### S-NEG2 (world_sneg2.zag)

- Name string: "SQ7-delta-causal".
- Vars: X(0,ctrl), Z(1,ctrl), Y(2).
  w_nvars()=3, w_nctrl()=2, w_ctrl=[0,1], w_ctxvar()=-1.
- Sealed truth: Y(t) = X(t-2) AND NOT Z(t-2). Pulsed writes,
  no persistence. Out-of-range reads are 0.
- Passive schedule: env SETs X at t=3,9. Z never pulsed.
  Then Y=1 exactly at t=5,11:
  t=5: X(3)=1 and Z(3)=0. t=11: X(9)=1 and Z(9)=0.
  No other t satisfies X(t-2)=1 (t in {5,11} only).
- w_goal_setup: Z=1 at t=0 (inhibitor present); X=0, Y=0.
- w_goal_mode()=0. w_plan_maxd()=8.
- main emits fixed string "SEALED DONE mask=" (no world name).
- Predicted behavior: discovery finds [X@2]; attempt 1 plans
  with [X@2], SETs X at t=0 while Z(0)=1, Y stays 0,
  GOAL_REAL 0; D1 fires (GOAL_FAIL_GROW_ATTEMPT); the grow
  search finds !Z@2 (false at refutation since Z(t_ref-2)=1;
  true on all true positives since Z never pulsed in
  passive); rule becomes [X@2 & !Z@2]; replan waits out the
  inhibitor; attempt 2 achieves GOAL_REAL 1.

### Renamed variants (F-RNAME)

- world_sneg2r.zag: byte-identical to world_sneg2.zag except
  the name string becomes "SQ7-delta-causal-R2".
- world_sconj2r.zag: byte-identical to world_sconj2.zag
  except the name string becomes "SQ3-beta-combine-R2".
- The world's main() emits no name, so every emitted line of
  a renamed run must be byte-identical to the original run.

## 3. Evaluation protocol (frozen)

1. Setup validation (not a falsifier): concatenate the frozen
   f3_revise.zag with the ORIGINAL worlds
   (f2_ablation/world_adv1.zag, f3_phase3/world_tneg_a.zag),
   build with znc, run 3x each, and confirm md5 match against
   the builder's committed raw outputs. This validates the
   evaluator's build/run pipeline reproduces the builder's
   environment. A mismatch here is a pipeline defect, not a
   learner defect; diagnose before proceeding.
2. Write the four sealed world files exactly per section 2.
   Verify the renamed pairs differ ONLY in the name string
   (diff).
3. Build: cat frozen learner + world > run file; znc compile;
   run 3x each; capture stdout/stderr. Configurations:
   sealed_c (S-CONJ2), sealed_cr (S-CONJ2 renamed),
   sealed_n (S-NEG2), sealed_nr (S-NEG2 renamed),
   sealed_abl_c (ablation + S-CONJ2),
   sealed_abl_n (ablation + S-NEG2).
4. Run all falsifiers (section 4) and harness checks
   (section 5) with shell tools only (grep, cmp, md5sum,
   sha256sum, diff). Zero Python at every stage.

## 4. Falsifiers (frozen criteria)

- F-RNAME: cmp sealed_c r1..r3 vs sealed_cr r1..r3, and
  sealed_n r1..r3 vs sealed_nr r1..r3. All pairs byte-identical
  required. Any divergence FIRES F-RNAME and kills the build.
- F-RABLN: on sealed_abl_c and sealed_abl_n (3 runs each), the
  ablated learner must NOT achieve (GOAL_REAL 1 AND the
  section-5 literal key for that world). If it does on either
  world, F-RABLN FIRES: condition (b) is decorative and the
  mechanism claim is void.
- F-RNAMEAUDIT: the token w_worldname occurs zero times in
  the frozen f3_revise.zag outside comment lines. Any code
  occurrence FIRES F-RNAMEAUDIT.
- F-RCOST: every sealed run reports F3P3 NEXPS <= 8 and
  COST_OK 1. Any violation FIRES F-RCOST.
- F-RDET: 3/3 byte-identical stdout per configuration and
  zero stderr bytes on all 18 runs. Any deviation FIRES F-RDET.

## 5. Harness answer checks (sealer's keys; live in the
## evaluator's check script, never in the learner)

- H-SCONJ2: sealed_c FINALRULE V=Y line contains both "X@3"
  and "Z@2"; output contains "GOAL_REAL 1 (attempt 1)"; output
  contains no "GOAL_FAIL_GROW_ATTEMPT".
- H-SNEG2: sealed_n FINALRULE V=Y line contains both "X@2"
  and "!Z@2"; output contains "GOAL_FAIL_GROW_ATTEMPT";
  output contains "GROW_OK (goal-fail)" with "+lit=!Z@2";
  output contains "GOAL_REAL 1 (attempt 2)".

## 6. Kill bars

- K1 (sealed prereg frozen first): PASS iff this commit
  strictly precedes every sealed world file, build script,
  binary, and run (verified by commit ancestry and timestamps).
- K2 (all falsifiers run): PASS iff F-RNAME, F-RABLN,
  F-RNAMEAUDIT, F-RCOST, F-RDET and both harness checks are
  executed with committed raw evidence.
- K3 (pure Zag, 3/3 identical): PASS iff every stage uses
  shell + znc + grep/cmp/md5sum/sha256sum/diff only (zero
  Python invocations), all 18 runs are 3/3 byte-identical
  per configuration with zero stderr, and no em/en dash
  bytes appear in any new file (shell byte check).

## 7. Verdict rule (frozen)

REVISE-SEALED-PASS iff: F-RNAME silent, F-RABLN silent,
F-RNAMEAUDIT silent, F-RCOST silent, F-RDET holds, H-SCONJ2
passes, H-SNEG2 passes. Otherwise REVISE-SEALED-FAIL with a
per-falsifier diagnosis. A FAIL caused by a malformed sealed
world (not a learner defect) is still recorded as FAIL with
the diagnosis stated; the prereg is not amended after runs.

## 8. Honest scope (frozen)

This evaluation tests the generic REVISE mechanism on unseen
world structure. It claims no L3, no T-NEG-class generality,
and does not revive the F3 Phase 3 BUILD-PASS. A PASS here
completes pipeline step 3 (sealed evaluation) only; steps
4-11 (independent reproduction, baseline, alt-explanation
attack, OOD, ablation, transfer/reuse, red team, governance
audit) remain.
