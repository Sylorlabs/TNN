# PREREG: F3 REVISE Simple-Baseline Comparison (Pipeline Step 5)

Status: FROZEN. This prereg is committed alone, before any baseline
implementation file, build script, binary, or run exists. It strictly
precedes all baseline-comparison work (K1).

Parent chain:
- Design: f3_revise/REVISE_DESIGN.md (ca157c743).
- Builder prereg: f3_revise_impl/PREREG_REVISE_IMPL.md (c197e7cd8).
- Builder result: f3_revise_impl/RESULT_REVISE.md (7009d711c),
  verdict REVISE-PASS (bounded L2).
- Sealed prereg: revise_sealed/PREREG_REVISE_SEALED.md (8cdf0992a).
- Sealed result: revise_sealed/RESULT_REVISE_SEALED.md (1df8addec),
  verdict REVISE-SEALED-PASS (bounded L2).
- Repro result: revise_repro/RESULT_REVISE_REPRO.md (7407dd4a7),
  verdict REVISE-REPRO-PASS (33/33 byte-identical).
- Pipeline: this is step 5 (simple-baseline comparison) of the 11-step
  frontier pipeline for the REVISE mechanism.

## 1. Purpose

Steps 1-4 established that the frozen REVISE learner achieves GOAL_REAL 1
on both sealed worlds (S-CONJ2: [X@3 & Z@2] on attempt 1; S-NEG2:
[X@2 & !Z@2] on attempt 2 after D1 revision). Step 5 asks whether that
performance is trivially matched by simple, researcher-authored
alternatives. If a dumb baseline matches REVISE on the sealed worlds,
the L2 claim is bounded further; if REVISE strictly beats simple
baselines, its discovery/trial/growth/revision machinery is doing
non-trivial work.

## 2. Worlds (frozen, reused)

The sealed world files from the sealed-evaluation commit (1df8addec),
verified by sha256 before any run:
- S-CONJ2: revise_sealed/world_sconj2.zag
  (sha256 8668e4a9933a99ee73a05661148fae7f33ad0d4bd95b73ba7607c994b04f682f).
  Truth: Y(t) = X(t-3) AND Z(t-2). Passive: X at t=1,7; Z at t=2,8;
  Y=1 at t=4,10. Goal: all-zero start, final-state Y=1.
- S-NEG2: revise_sealed/world_sneg2.zag.
  Truth: Y(t) = X(t-2) AND NOT Z(t-2). Passive: X alone at t=3,9;
  Y=1 at t=5,11. Goal setup: Z=1 at t=0 (inhibitor), X=0, Y=0.

The baselines must NOT read the sealed truth comments; they interact
with the worlds only through the w_ interface (w_reset, w_act, w_passive,
w_snapshot, w_goal_setup, w_goal_met, w_nvars, w_nctrl, w_ctrl, w_vname).
The w_vname convention (X=0, Z=1, Y=2) is disclosed infrastructure,
same as for the learner.

REVISE reference scores (frozen, from the sealed evaluation):
- S-CONJ2: GOAL_REAL 1, FINALRULE [X@3 & Z@2].
- S-NEG2: GOAL_REAL 1 (attempt 2), FINALRULE [X@2 & !Z@2].

## 3. Baselines (frozen specifications)

### B-REPLAY (rote memorization)

A pure memorization baseline: observe the passive schedule, find the
first Y=1 event, record the control actions in the preceding window,
replay them verbatim.

Exact algorithm:
1. Allocate ws (8+nvars*32 bytes), w_reset.
2. Passive observation: for t=0..12: call w_passive(ws); w_snapshot
   into rec[t] (nvars bytes); then w_act(ws,2,0) to advance, except
   do not advance past t=12.
   (Note: w_passive uses the world's clock; call it BEFORE advancing
   past each t, matching the world's own schedule semantics.)
3. Find first t* in 0..12 with rec[t*][Y]=1, where Y is the var with
   w_vname "Y". If none, emit B-REPLAY GOAL_REAL 0 and stop.
4. For dt in 1..4: for each control var c (w_ctrl list): if
   rec[t*-dt][c]=1, record action (SET c at replay-time t*-dt).
5. w_reset(ws); w_goal_setup(ws).
6. Replay: for t=0..t*: if t has a recorded SET for var v, w_act(ws,0,v);
   then if t<t*, w_act(ws,2,0) to advance.
7. w_snapshot(ws,fin); g=w_goal_met(fin); emit B-REPLAY GOAL_REAL g.

Predicted outcome (prediction only; verdict follows measured runs):
- S-CONJ2: PASS. First Y=1 at t*=4; replays SET X at t=1, SET Z at
  t=2; at t=4, X(1)=1 and Z(2)=1 so Y=1.
- S-NEG2: PASS. First Y=1 at t*=5; replays SET X at t=3; at t=5,
  X(3)=1 and Z(3)=0 (no persistence; Z was 1 only at t=0), so Y=1.
  The replay avoids the t=0 inhibitor by acting at t=3 as observed.

### B-SINGLETON (best single literal, no growth, no revision)

A greedy single-literal baseline: score every candidate literal by F1
against the passive observations, pick the best, plan once, execute
once. No conjunction formation, no trials, no goal-failure revision.

Exact algorithm:
1. Passive observation as in B-REPLAY steps 1-2, t=0..12.
2. Candidate literals: for each control var v in w_ctrl list, for delay
   k in 1..4, both polarities: (v,+,k) and (v,-,k). Literal (v,+,k)
   holds at t iff t-k>=0 and rec[t-k][v]=1. Literal (v,-,k) holds at t
   iff t-k>=0 and rec[t-k][v]=0. (t-k<0: literal does not hold.)
3. For each literal L: hits = #{t in 0..12: rec[t][Y]=1 and L holds at t};
   hold = #{t in 0..12: L holds at t}; yc = #{t: rec[t][Y]=1}.
   P = hits/hold (0 if hold=0); R = hits/yc (0 if yc=0);
   F1 = 2*P*R/(P+R) (0 if P+R=0). Integer arithmetic scaled by 1000.
4. Pick max F1. Tie-break order: higher P; smaller k; smaller var index;
   positive before negated.
5. w_reset(ws); w_goal_setup(ws).
6. If chosen literal is (v,+,k): w_act(ws,0,v) (SET v at t=0); then
   advance k times via w_act(ws,2,0). If (v,-,k): advance k times
   (no action can force a var to 0; the baseline just waits).
7. w_snapshot(ws,fin); g=w_goal_met(fin);
   emit B-SINGLETON GOAL_REAL g and the chosen literal.

Predicted outcome (prediction only):
- S-CONJ2: FAIL. X@3 and Z@2 tie at F1=1.0 (both perfect on passive);
  tie-break picks X@3 (smaller var index). Plan: SET X at t=0,
  advance 3; at t=3, X(0)=1 but Z(1)=0, so Y=0. GOAL_REAL 0.
- S-NEG2: FAIL. X@2 has F1=1.0 (perfect); !Z@2 has low precision
  (Z=0 almost everywhere). Picks X@2. Plan: SET X at t=0; at t=2,
  X(0)=1 but Z(0)=1 (goal-setup inhibitor), so Y=0. GOAL_REAL 0.

## 4. Protocol (frozen)

1. Verify sealed world bytes by sha256 against the hashes in section 2
   before any run. Mismatch voids the comparison.
2. Implement b_replay.zag and b_singleton.zag (each defines L_run();
   the world's main() calls it). No other files.
3. Build: cat baseline + world > run_baseline_<name>_<world>.zag;
   compile with the repo znc; run 3x each; capture stdout/stderr.
   Configurations: replay_c (B-REPLAY + S-CONJ2),
   replay_n (B-REPLAY + S-NEG2), single_c (B-SINGLETON + S-CONJ2),
   single_n (B-SINGLETON + S-NEG2).
4. Determinism: 3/3 byte-identical stdout per configuration, zero
   stderr bytes.
5. Score each configuration by its emitted GOAL_REAL line.

## 5. Comparison bars and verdict rule (frozen)

Let R_c, R_n be REVISE's frozen GOAL_REAL (1, 1).
Let P_c, P_n be B-REPLAY's measured GOAL_REAL.
Let S_c, S_n be B-SINGLETON's measured GOAL_REAL.

- CB1 (REVISE beats the greedy baseline): (R_c > S_c) or (R_n > S_n).
  That is, REVISE strictly outperforms B-SINGLETON on at least one
  sealed world.
- CB2 (no baseline beats REVISE): not ((P_c > R_c) or (P_n > R_n) or
  (S_c > R_c) or (S_n > R_n)). No baseline achieves GOAL_REAL 1 on a
  world where REVISE achieves 0.

Verdict:
- REVISE-BASELINE-PASS iff CB1 and CB2 both hold.
- REVISE-BASELINE-FAIL otherwise.

Honest-scope note (pre-registered): if B-REPLAY matches REVISE
(P_c=R_c=1 and P_n=R_n=1), the verdict can still be PASS via CB1, but
the result honestly bounds the claim: the sealed worlds are solvable by
rote replay of the passive schedule, so REVISE's demonstrated advantage
is specifically over greedy single-literal strategies (conjunction
formation and goal-failure revision), not over memorization. That bound
is part of the PASS verdict, not a rescue.

## 6. Kill bars

- K1 (prereg frozen before implementation): PASS iff this prereg's
  commit strictly precedes every baseline .zag file, build script,
  binary, and run (verified by git ancestry).
- K2 (baselines run): PASS iff all four configurations run 3x with
  committed raw logs and scored GOAL_REAL lines.
- K3 (pure Zag, 3/3 identical): PASS iff zero Python invocations at
  every stage (authoring, build, run, analysis, byte checks); 3/3
  byte-identical stdout per configuration; zero stderr bytes on runs.

## 7. Governance

- Baselines are researcher-authored simple algorithms; they are not
  claimed as learner mechanisms and carry no L2/L3 status.
- The sealed world files are reused byte-identical; the baselines do
  not modify them.
- The contaminated research paper is not touched.
- Commits are local, owned path only
  (docs/lab/research-lead/overnight-20260928/revise_baseline/),
  tight pathspecs.
