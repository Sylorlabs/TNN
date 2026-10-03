# RESULT_F3ATTACK: Alternative-explanation attack on F3 Phase 3

Date: 2026-09-30. Worker: F3 Alternative-Explanation Attacker.
Prereg: 1a53c4a87 (frozen before any attack artifact).
Target: F3 Phase 3 BUILD-PASS (41ed1ef9a).
Verdict: **F3-ATTACK-KILLS**.

## 1. Summary

H-NAME CONFIRMED. The T-NEG "negation learning via OP-GROW on goal
failure" (P-GROW-N, P-REPLAN-N) is gated on the learner detecting
the world's name string. When the sealed T-NEG world is run with
only its name changed ("TNEG-grow-negation" -> "XNEG-grow-negation",
one line, everything else byte-identical), the goal-failure GROW
does not fire, the negation is not learned, and the goal fails.
The "discovery" is a world-specific script, not a general causal
mechanism.

H-ABL REJECTED. The true-on-positives condition in F3_grow_search
is NOT decorative. An ablated learner (condition (b) removed) grows
wrong literals on both sealed worlds and fails. The causal search
does real work when it runs.

H-SCHED NOT RUN. Designed in the prereg but deferred: H-NAME was
decisive for the verdict per the frozen verdict rule, and H-SCHED
could only weaken, not kill or save.

## 2. H-NAME: confirmed (kills)

### Code basis (frozen learner f3_p3.zag)

- Lines 1237-1242: w_worldname() is read. First byte 65 ('A')
  sets is_conj_world=1. First byte 84 ('T') sets is_neg_world=1.
- Line 1295: `if(is_neg_world==1 && attempt==1)` gates the
  goal-failure OP-GROW. Comment: "For T-NEG, try OP-GROW on the Y
  rules using the goal execution ws as the refutation observation."
- Lines 1378-1379: verdict world_pass requires the name flag.

The prereg (97287f87c section 2) describes the goal-failure GROW
as a general mechanism and section 7 discloses it as "a simplified
precursor of Phase 7 REVISE." Neither section discloses
world-name gating.

### Empirical test

world_tneg_renamed.zag: copy of sealed world_tneg_a.zag with ONLY
line 24 changed (w_worldname "TNEG-grow-negation" ->
"XNEG-grow-negation"). Diff verified: exactly one line differs.
Sealed truth, passive schedule, goal setup, interface, and main()
are unchanged. Frozen unmodified f3_p3.zag. 3/3 byte-identical
runs (md5 ee9b5769ee94a31d4cacca3bf1f788d5), zero stderr.

OP-PROP and trials are IDENTICAL to the sealed run:
- PROP V=Y lit=X@1 ok=2 (exactly one candidate, as in sealed)
- TRIAL [SX,W,OY], RULE_CONFIRMED obs=1 (as in sealed)

Goal phase DIVERGES completely:
- Renamed: `F3P3 WORLD_IS_NEG 0`. No GOAL_FAIL_GROW_ATTEMPT line.
  No GROW_OK (goal-fail) line. `F3P3 GOAL_REAL 0 (attempt 1)`.
  No attempt 2. Verdict PHASE3-FAIL.
- Sealed (41ed1ef9a): GOAL_FAIL_GROW_ATTEMPT, GROW_OK (goal-fail)
  +lit=!Z@1, GOAL_REAL 0 (attempt 1), replan [SX,CZ,W],
  GOAL_REAL 1 (attempt 2). Verdict PHASE3-TESTED.

The only difference between the runs is the world name string.
The "negation discovery" appears if and only if the learner
recognizes the name. H-NAME confirmed.

### What this kills

The frozen Phase 3 K2 bar requires: "T-NEG tested per section 2;
negation literal learned via GROW on goal failure; replanned goal
achieved within cost bound." That bar is met in the sealed run only
because the learner detects the T-NEG name and runs the
negation-specific recovery path. The result does not demonstrate a
general mechanism that learns negation from goal failure. It
demonstrates a world-specific script.

F3 Phase 3 BUILD-PASS is therefore retracted to BUILD-FAIL as a
claim about general causal learning. The T-CONJ trial-driven
OP-GROW result stands (see H-ABL), but T-CONJ alone does not
satisfy the frozen K2 bar.

## 3. H-ABL: rejected (causal condition is necessary)

### Ablation

f3_p3_abl.zag: copy of frozen f3_p3.zag with F3_grow_search
condition (b) (true on all true positives) removed. When
false_at_ref==1, the first (c, pol, d) in search order is accepted
immediately. Diff verified: only lines 327-365 replaced (39 lines
-> 7 lines). Search order unchanged. All else identical.

### Results (sealed worlds, unmodified; 3/3 identical, zero stderr)

Ablated T-CONJ (world_adv1.zag):
- GROW_OK V=Y rule=1 +lit=X@1, then +lit=!X@1 (contradictory),
  V=Y rule=0 +lit=!X@2, V=Z rule=0 +lit=!X@1. Wrong literals.
- Verdict: PHASE3-FAIL. GOAL_REAL never 1.

Ablated T-NEG (world_tneg_a.zag):
- GOAL_REAL 0 (attempt 1). GROW_OK (goal-fail) +lit=!X@1
  (wrong; sealed run finds !Z@1). Verdict: PHASE3-FAIL.

The ablated learner grows garbage and fails both sealed worlds.
Condition (b) is necessary for correct learning. H-ABL rejected.
The OP-GROW causal search is a real mechanism, not decorative,
wherever it is allowed to run.

## 4. Net assessment

The attack separates two things the BUILD-PASS had fused:

1. Trial-driven OP-GROW (T-CONJ): generic, ungated, causally
   necessary (H-ABL rejected). SURVIVES as a real mechanism.
2. Goal-failure-driven OP-GROW (T-NEG): world-name-gated
   (H-NAME confirmed). The "negation learning" is a script, not
   a general mechanism. KILLED as evidence of general causal
   learning.

Phase 3 as specified (both T-CONJ and T-NEG via a general OP-GROW)
does not survive. The honest standing claim is narrower:
trial-driven OP-GROW is a real causal growth operator; the
goal-failure-driven extension was never general and must be
redesigned without world-identity gating (a proper Phase 7 REVISE
precursor) before any T-NEG-class claim is made again.

## 5. Kill bars

- K1: PASS. Prereg 1a53c4a87 committed alone before any attack
  artifact existed (world_tneg_renamed.zag, f3_p3_abl.zag,
  binaries, and logs all postdate it).
- K2: PASS. The ablation was implemented (f3_p3_abl.zag, diff
  verified) and tested on both sealed worlds (ablc: T-CONJ FAIL;
  abln: T-NEG FAIL with wrong literal).
- K3: PASS. Pure Zag at every stage (znc, sh, cp, sed, diff,
  grep, git, md5sum only). Zero Python. Zero em/en-dash bytes in
  authored files (shell byte check, not Python). 3/3 byte-identical
  per test, zero stderr bytes.

## 6. Files

All in docs/lab/research-lead/overnight-20260928/f3_attack/:
- PREREG_F3ATTACK.md (prereg, 1a53c4a87)
- RESULT_F3ATTACK.md (this file)
- world_tneg_renamed.zag (H-NAME world; one-line diff vs sealed)
- f3_p3_abl.zag (H-ABL learner; (b) block removed)
- run_name.zag, name_bin, name_r1..3.txt/.err, name_build.err
- run_ablc.zag, ablc_bin, ablc_r1..3.txt/.err, ablc_build.err
- run_abln.zag, abln_bin, abln_r1..3.txt/.err, abln_build.err

## 7. Governance notes

- No sealed file was modified. No frozen learner was modified
  (copies only, in f3_attack/).
- The contaminated paper was not touched.
- H-SCHED (world_conj2.zag) was designed in the prereg but not
  run; the frozen verdict rule made H-NAME decisive, and H-SCHED
  could neither kill nor save beyond that. Noted here, not hidden.
- Verdict: **F3-ATTACK-KILLS**. F3 Phase 3 BUILD-PASS is retracted
  to BUILD-FAIL on the T-NEG leg. Trial-driven OP-GROW survives
  as a real mechanism; the goal-failure extension needs redesign.
