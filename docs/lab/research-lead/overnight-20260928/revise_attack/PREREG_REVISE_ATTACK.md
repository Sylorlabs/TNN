# PREREG: F3 REVISE Alternative-Explanation Attack (Pipeline Step 6)

Status: FROZEN. This prereg is committed alone, before any attack
world file, attack build script, attack binary, or attack run
exists. It strictly precedes all step-6 work (K1).

Parent chain:
- Design: f3_revise/REVISE_DESIGN.md (commit ca157c743).
- Builder prereg: f3_revise_impl/PREREG_REVISE_IMPL.md (c197e7cd8).
- Builder result: f3_revise_impl/RESULT_REVISE.md (7009d711c),
  verdict REVISE-PASS (bounded L2).
- Sealed prereg: revise_sealed/PREREG_REVISE_SEALED.md (8cdf0992a).
- Sealed result: revise_sealed/RESULT_REVISE_SEALED.md (1df8addec),
  verdict REVISE-SEALED-PASS (bounded L2).
- Repro: 7407dd4a7 (REVISE-REPRO-PASS).
- Baseline prereg: revise_baseline/PREREG_REVISE_BASELINE.md
  (4786633c5) plus Amendment 1 (db585360a).
- Baseline result: revise_baseline/RESULT_REVISE_BASELINE.md
  (c810d5f55), verdict REVISE-BASELINE-PASS (bounded L2).
- Pipeline: this is step 6 (alternative-explanation attack) of the
  11-step frontier pipeline for the REVISE mechanism.

## 0. Standing rules name-check (read from LOOP_STATE.md before work)

1. PURE ZAG ONLY. No Python anywhere: not glue, not analysis, not
   verifiers, not harnesses. This attack uses only hand-authored Zag,
   znc, shell, and coreutils (grep, diff, cmp, md5sum, sha256sum).
   Zero python3 invocation at every stage (authoring, world files,
   build, run, analysis, byte checks).
2. Image judge: not applicable; no image work.
3. Fork testing: noted; single-lane attack on tnn-native-lab.
4. Pure-Zag red line scope: fixture provisioning counts as loop work.
   Sealed world files are extracted via git plumbing (git show) only.
5. Shell-only byte checks: all new docs checked with
   docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh.

## 1. Claim under attack

Bounded L2 claim (from steps 1-5): REVISE implements GENERIC
goal-failure revision. When an attempt fails to reach the goal
(GOAL_REAL 0), the D1 trigger fires, the learner refutes via the
unchanged generic F3_grow_search using the post-failure world state
as refutation evidence (D2), grows a literal gated by condition
(a)+(b) (D3), replans (D4), and retries (ATTEMPT_MAX=3). Demonstrated
on T-CONJ, T-NEG, S-CONJ2, S-NEG2. Condition (b) is causally
necessary (ablation). Beats greedy singleton (CB1). Ties rote replay
(CB2 bound: advantage is over greedy strategies, not memorization).

## 2. Alternative explanations under attack

E1: "Rote replay explains everything." B-REPLAY tied REVISE (1,1 vs
1,1) on both sealed worlds. The sealed worlds are solvable by
verbatim replay of the passive schedule. Perhaps REVISE's D1
revision does no work that passive-schedule replay cannot do, and
the S-NEG2 revision trace is a lucky path, not a generic mechanism.

E2: "The world-calibrated REFUTE-DRILL secretly guides the
mechanism." The sealed evaluation (section 4 of
RESULT_REVISE_SEALED.md) diagnosed the drill as a blemish in the
self-test, asserting via source inspection that it runs on a scratch
copy and cannot alter any mechanism decision. If that assertion is
wrong and drill state leaks into discovery, trials, D1, growth, or
planning, the sealed evidence is contaminated.

## 3. Attack 1: replay-discriminating world S-RK

### 3.1 World specification (frozen; implementation is mechanical)

File: revise_attack/world_srk.zag. Derived from sealed
world_sneg2.zag (commit 1df8addec) by changing ONLY the passive
pulse times and the name string. All physics, goal setup, and
conventions are otherwise byte-identical in structure.

- Name string: "SQ9-epsilon-replaykill". (The learner cannot read
  it; F-RNAME holds by construction. The string carries no answer
  hint.)
- Vars: X(0,ctrl), Z(1,ctrl), Y(2).
  w_nvars()=3, w_nctrl()=2, w_ctrl=[0,1], w_ctxvar()=-1.
- Sealed truth: Y(t) = X(t-2) AND NOT Z(t-2). Pulsed writes, no
  persistence. Out-of-range reads are 0. IDENTICAL to S-NEG2.
- Passive schedule: env SETs X at t=0,6. Z never pulsed.
  Then Y=1 exactly at t=2,8.
  t=2: X(0)=1 and Z(0)=0. t=8: X(6)=1 and Z(6)=0.
  No other t satisfies X(t-2)=1.
- w_goal_setup: Z=1 at t=0 (inhibitor present); X=0, Y=0.
  IDENTICAL to S-NEG2.
- w_goal_mode()=0 (final-state Y=1). w_plan_maxd()=8.
- main emits fixed string "SEALED DONE mask=" (no world name).

This world is a MINIMAL timing variant of S-NEG2: same truth, same
goal setup, same inhibitor, same discovery correlation (X-pulse to
Y-event lag is exactly 2). The ONLY difference is the passive pulse
phase (t=0,6 vs t=3,9). If the D1 mechanism is generic, passive
phase cannot matter: the learner never sees phase, only
(pulse, event) correlations.

### 3.2 Predicted B-REPLAY behavior (frozen)

b_replay.zag (commit c810d5f55, unmodified): first Y=1 at ts=2.
Window dt=1..4 covers t=1,0. rec shows X=1 at t=0. Records
(at=0, X). Replay from goal setup: SET X at t=0, advance to t=2.
Y(2) = X(0) AND NOT Z(0) = 1 AND NOT 1 = 0. w_goal_met = 0.
Predicted: B-REPLAY GOAL_REAL 0 (3/3).

Rationale: replay uses ABSOLUTE passive times. The passive X pulse
at t=0 coincides with the goal-setup inhibitor at t=0, so the
replayed check lands on the inhibitor. On S-NEG2 the passive pulse
was at t=3, so the replayed check at t=5 read Z(3)=0 and replay
succeeded by luck of phase.

### 3.3 Predicted REVISE behavior (frozen)

Frozen learner f3_revise.zag (commit 7009d711c, sha256
354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392,
verified before any run; any mismatch voids the attack):

- Discovery: passive trace shows Y=1 exactly at t=2,8 with X=1 at
  t=0,6. Discovers [X@2] (same correlation as S-NEG2).
- Trial phase: [X@2] is never refuted in passive (every X(t-2)=1
  coincides with Y=1; Z never pulsed). No pre-attempt growth.
- Attempt 1: plan under [X@2] SETs X at t=0 (earliest). Post-plan
  check: Y(2) = X(0) AND NOT Z(0) = 0 (inhibitor Z(0)=1 from goal
  setup). GOAL_REAL 0. D1 fires: F3P3 GOAL_FAIL_GROW_ATTEMPT.
- Goal-fail growth: F3_grow_search on rule [X@2], t_ref=t_goal.
  Candidate scan in (var, polarity, delay) order:
  - (X,-,d): (a) needs X(t_ref-d)=1; (b) needs !X@d true on all
    passive true positives (t=2,8: X(0)=1 blocks d=2; other d
    fail (b) on timing). Rejected by evidence gate (b).
  - (X,+,d): (a)/(b) fail on passive timing (same as S-NEG2).
  - (Z,-,1): (a) needs Z(t_ref-1)=1; Z pulsed nowhere, setup Z=1
    only at t=0; t_ref>=2 so Z(t_ref-1)=0. Rejected.
  - (Z,-,2): (a) Z(t_ref-2)=Z(0)=1, so the negated literal is
    false at ref. (b) Z=0 on all passive true positives
    (Z never pulsed: Z(0)=0, Z(6)=0 in passive). ACCEPTED.
  GROW_OK (goal-fail) V=Y rule=0 +lit=!Z@2. REVISED_GROWN.
- Attempt 2: replan under [X@2 & !Z@2]; waits out the inhibitor
  (SET X at t>=1); check reads Z=0 at the delayed time.
  Y=1. GOAL_REAL 1.
- FINALRULE V=Y rule=0 [X@2 & !Z@2]. NEXPS within bound (<=8).

### 3.4 Harness H-SRK (frozen)

H-SRK passes iff ALL of:
- (a) B-REPLAY on S-RK: "B-REPLAY GOAL_REAL 0" on all 3 runs.
- (b) REVISE on S-RK: "F3P3 GOAL_REAL 1" appears (attempt 2) on
  all 3 runs; "F3P3 GOAL_FAIL_GROW_ATTEMPT" present on all 3 runs;
  "F3P3 GROW_OK (goal-fail)" with "+lit=!Z@2" on all 3 runs.
- (c) FINALRULE contains (X,+,2) and (Z,-,2) on all 3 runs.
- (d) 3/3 byte-identical stdout per configuration; zero stderr
  bytes on all runs.

Note: the learner's self-reported "F3P3 RESULT" line is NOT part of
H-SRK. The REFUTE-DRILL's world-calibrated expectation misfires on
any world where [X@2] is the true 1-literal rule (diagnosed in
RESULT_REVISE_SEALED.md section 4); the harness judges mechanism
outputs (GOAL_REAL, growth trace, FINALRULE), not the drill-gated
verdict line. This follows the sealed evaluator's precedent
(H-SCONJ2/H-SNEG2).

### 3.5 Attack 1 verdict rule (frozen)

Setup validation (not a falsifier): concatenate the frozen learner
with sealed world_sneg2.zag, build, run 3x, confirm md5
85ebb436b4f7d6eac370466bc98a878c against the sealed committed raw
outputs. If this fails, the attack pipeline is broken: verdict is
VOID, fix the pipeline, do not proceed.

- If setup validation fails: A1-VOID (pipeline). No verdict.
- Else if B-REPLAY GOAL_REAL is not 0: A1-VOID (design). The
  attack world does not discriminate; E1 is not tested. Do not
  kill, do not claim.
- Else (replay 0): E1 is under test.
  - If H-SRK passes: E1 is KILLED. Rote replay cannot explain
    REVISE's success; D1 revision does work replay cannot do on a
    timing variant of a passed world. Attack 1 SURVIVES.
  - If H-SRK fails (REVISE GOAL_REAL 0, or wrong growth, or
    non-determinism): REVISE fails on a minimal timing variant of
    S-NEG2 (same truth, same setup, same correlation). The
    "generic mechanism" qualifier is falsified; success on S-NEG2
    was phase-lucky. Attack 1 KILLS.

## 4. Attack 2: REFUTE-DRILL isolation (empirical)

### 4.1 Procedure (frozen)

1. Copy frozen f3_revise.zag (7009d711c) to
   revise_attack/f3_revise_nodrill.zag.
2. Excise ONLY the REFUTE-DRILL block (lines 1096-1138 of the
   frozen file: from "// ---- REFUTE-DRILL" through the
   DRILL_RESULT emits), KEEPING line 1110
   ("let drill_ok:i32=0;"). No other byte changes. Verify by diff
   that the only difference from the frozen learner is the removed
   drill block.
   Safety (source-verified before freezing): drill-written buffers
   tsk, tsv, onevar are never read after line 1140 (grep-verified);
   ws is w_reset before the goal phase; SPLIT-DRILL uses disjoint
   buffers (srule, strace, split_*). The excision cannot alter
   mechanism state by construction.
3. Build f3_revise_nodrill.zag concatenated with sealed
   world_sconj2.zag and world_sneg2.zag (extracted via git show
   from 1df8addec; sha256 verified before any run).
4. Run 3x each. Compare against the sealed committed raw outputs
   (md5 84ab277e7535c740c5210c2065a8cef6 for S-CONJ2,
   85ebb436b4f7d6eac370466bc98a878c for S-NEG2).

### 4.2 Comparison rule (frozen)

Exclude lines containing "DRILL" (the excised self-test's own
emits, expected absent) and compare all remaining stdout bytes.
The RESULT line is INCLUDED in the comparison: on S-NEG2 the
original already reports REVISE-FAIL (drill_ok=0), and the excised
build keeps drill_ok=0, so the RESULT lines must also match.

A2-ISOLATED iff: for both worlds, all 3 runs of the excised build
are byte-identical to the sealed committed raw outputs after
removing DRILL-containing lines, with zero stderr bytes.

### 4.3 Attack 2 verdict rule (frozen)

- If A2-ISOLATED: E2 is KILLED. The drill is empirically inert;
  the sealed evaluator's source assertion is confirmed
  behaviorally. Attack 2 SURVIVES.
- If NOT A2-ISOLATED (any mechanism line differs): drill state
  leaks into mechanism decisions; the sealed evidence is built on
  a contaminated artifact. Attack 2 KILLS.

## 5. Kill bars

- K1 (prereg frozen before attack): PASS iff this prereg's commit
  strictly precedes every attack world file, build script, binary,
  and run. Verified by commit ancestry.
- K2 (attacks run): PASS iff Attack 1 (setup validation, B-REPLAY
  on S-RK, REVISE on S-RK, 3x each) and Attack 2 (excised build on
  both sealed worlds, 3x each) all execute with committed raw logs.
- K3 (pure Zag, 3/3 identical): PASS iff zero Python invocations at
  every stage and every reported configuration is 3/3
  byte-identical with zero stderr bytes.

## 6. Combined verdict rule (frozen)

- REVISE-ATTACK-KILLS iff (Attack 1 KILLS) OR (Attack 2 KILLS).
- REVISE-ATTACK-SURVIVES iff (Attack 1 SURVIVES) AND (Attack 2
  SURVIVES), with K1/K2/K3 all PASS.
- If Attack 1 is VOID (pipeline or design), the combined verdict
  is REVISE-ATTACK-INCONCLUSIVE with the void reason recorded; do
  not claim SURVIVES on a voided attack. (Attack 2 still reports.)

KILLS here kills the bounded-L2 genericity claim as stated; it does
not revive or alter any prior verdict, and no bar is moved after
results.

## 7. Honest scope

This attack tests two specific alternative explanations (E1, E2).
It does not test OOD delays beyond the 1..4 literal inventory, does
not test multi-inhibitor worlds, and does not test the 3-literal
cap boundary; those belong to pipeline step 7 (OOD). A SURVIVES
verdict keeps REVISE at bounded L2; it claims no L3, no Criterion 0,
and does not advance the pipeline past step 6. The contaminated
research paper is not touched by this attack.
