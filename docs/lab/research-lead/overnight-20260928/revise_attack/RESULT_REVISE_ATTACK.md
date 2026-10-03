# RESULT: F3 REVISE Alternative-Explanation Attack (Pipeline Step 6)

Verdict: REVISE-ATTACK-SURVIVES.

Parent prereg: revise_attack/PREREG_REVISE_ATTACK.md (commit
12da75511), frozen alone before any attack world file, build
script, binary, or run existed. K1 holds by commit ancestry.
Parent chain: design ca157c743, builder prereg c197e7cd8, builder
result 7009d711c (REVISE-PASS), sealed prereg 8cdf0992a, sealed
result 1df8addec (REVISE-SEALED-PASS), repro 7407dd4a7
(REVISE-REPRO-PASS), baseline prereg 4786633c5 plus amendment
db585360a, baseline result c810d5f55 (REVISE-BASELINE-PASS).
Pipeline: this completes step 6 (alternative-explanation attack)
only.

## 1. What was attacked

Two alternative explanations for REVISE's success (prereg
section 2):

E1: "Rote replay explains everything." B-REPLAY tied REVISE (1,1
vs 1,1) on both sealed worlds; perhaps D1 revision does no work
that passive-schedule replay cannot do.

E2: "The world-calibrated REFUTE-DRILL secretly guides the
mechanism." If drill state leaks into mechanism decisions, the
sealed evidence is contaminated.

## 2. Attack 1: replay-discriminating world S-RK

### 2.1 Setup validation (prereg 3.5)

Frozen learner (sha256
354236fb3071729fc8921489163f1454bb04d673655f2cb3d1f3c88cb771d392,
verified before any run) concatenated with sealed world_sneg2.zag
(extracted via git show from 1df8addec): 3/3 runs byte-identical,
md5 85ebb436b4f7d6eac370466bc98a878c, matching the sealed
committed raw outputs exactly. Zero stderr bytes. Pipeline valid;
not VOID.

### 2.2 The attack world

revise_attack/world_srk.zag. Derived from sealed world_sneg2.zag
by changing ONLY the passive pulse times (X at t=0,6 instead of
t=3,9) and the name string ("SQ9-epsilon-replaykill"). Sealed
truth identical: Y(t) = X(t-2) AND NOT Z(t-2). Goal setup
identical: Z=1 inhibitor at t=0. Y=1 exactly at t=2,8. Verified by
diff: only the name string and the two passive-time lines differ.

### 2.3 B-REPLAY on S-RK (E1 setup)

b_replay.zag (commit c810d5f55, unmodified), 3/3 byte-identical
(md5 f32e61a365ff4ecd8232b79fd0e66a83), zero stderr bytes:

B-REPLAY GOAL_REAL 0 (3/3).

As predicted: first Y=1 at ts=2; the 4-step window records (at=0,
X); absolute-time replay SETs X at t=0; the check Y(2) = X(0) AND
NOT Z(0) lands on the goal-setup inhibitor Z(0)=1. The attack
discriminates; A1 is not VOID.

### 2.4 REVISE on S-RK (E1 test)

Frozen learner, 3/3 byte-identical (md5
85ebb436b4f7d6eac370466bc98a878c), zero stderr bytes. The full
trace:

- Discovery found [X@2]; trial phase did not refute it.
- Attempt 1: plan SET X at t=0; Y(2)=0 (inhibitor).
  F3P3 GOAL_REAL 0 (attempt 1).
- D1 fired: F3P3 GOAL_FAIL_GROW_ATTEMPT.
- Goal-fail growth: F3P3 GROW_OK (goal-fail) V=Y rule=0
  +lit=!Z@2. F3P3 REVISED_GROWN.
- Attempt 2: replanned around the inhibitor.
  F3P3 GOAL_REAL 1 (attempt 2).
- F3P3 NEXPS 3 COST_OK 1 GOAL_OK 1 NGROW 1.
- F3P3 FINALRULE V=Y rule=0 [X@2 & !Z@2].

Striking fact: the S-RK outputs are BYTE-IDENTICAL (md5
85ebb436b4f7d6eac370466bc98a878c) to the sealed S-NEG2 outputs.
The D1 mechanism is invariant to passive pulse phase: same
discovery, same failure, same grown literal, same replan. The
S-NEG2 success was not phase-lucky.

### 2.5 H-SRK (frozen harness)

- (a) B-REPLAY GOAL_REAL 0 on all 3 runs: PASS.
- (b) GOAL_REAL 1 (attempt 2), GOAL_FAIL_GROW_ATTEMPT present,
  GROW_OK +lit=!Z@2, on all 3 runs: PASS.
- (c) FINALRULE contains (X,+,2) and (Z,-,2) on all 3 runs: PASS.
- (d) 3/3 byte-identical per configuration; zero stderr: PASS.

H-SRK passes. E1 is KILLED: rote replay cannot explain REVISE's
success. D1 revision does work (goal-failure-triggered inhibitor
guard growth and replanning) that verbatim replay provably cannot
do on a minimal timing variant of a passed world. Attack 1
SURVIVES.

## 3. Attack 2: REFUTE-DRILL isolation (empirical)

### 3.1 Excision (prereg 4.1)

Copied frozen f3_revise.zag to revise_attack/f3_revise_nodrill.zag.
Excised ONLY the REFUTE-DRILL block (input lines 1096-1109 and
1111-1138), KEEPING line 1110 ("let drill_ok:i32=0;"). Verified by
diff: the only difference from the frozen learner is the removed
drill block (44 diff lines, all drill). SPLIT-DRILL intentionally
kept. Source-verified safety: drill-written buffers tsk, tsv,
onevar are never read after the drill; ws is w_reset before the
goal phase.

### 3.2 Runs

Drill-excised learner concatenated with sealed world_sconj2.zag
and world_sneg2.zag (git show from 1df8addec, sha256 verified).
3/3 byte-identical per world (md5 d65428cecec95ab93e73e2c928e30c5a
for S-CONJ2, 4e4423fed1642ffab2573d087c0ea1d3 for S-NEG2), zero
stderr bytes on all 6 runs.

### 3.3 Comparison (frozen rule, honestly reported)

Excluded lines containing "DRILL"; compared all remaining stdout
bytes against the sealed committed raw outputs:

- S-NEG2: BYTE-IDENTICAL (including the RESULT line, which reads
  REVISE-FAIL in both, since drill_ok=0 in both).
- S-CONJ2: identical EXCEPT two lines:
  - "F3P3 RESULT REVISE-PASS" vs "F3P3 RESULT REVISE-FAIL"
  - "SEALED DONE mask=0" vs "SEALED DONE mask=1"

Both S-CONJ2 differences are the MECHANICAL consequence of the
excision, not mechanism contamination: the verdict conjunction is
(goal_ok && drill_ok && split_ok && cost_ok && search_ok), and the
excised build forces drill_ok=0 (the drill did not run), so the
verdict line and the return mask flip. Every MECHANISM output line
(discovery, candidates, trials, refutations, growth, D1 trigger,
plans, GOAL_REAL per attempt, FINALRULE, NEXPS, COST_OK, GOAL_OK)
is byte-identical on both worlds.

Prereg imprecision noted transparently: section 4.2 stated the
RESULT line is included in the comparison and reasoned only about
S-NEG2 (where it matches). On S-CONJ2 the RESULT line must differ
by construction. This does not rescue a failed attack: no
mechanism line differs anywhere. The drill is empirically inert.

### 3.4 Attack 2 verdict

A2-ISOLATED on all mechanism outputs. E2 is KILLED: the
REFUTE-DRILL does not guide, leak into, or alter any mechanism
decision (discovery, trial, D1, growth, planning). The sealed
evaluator's source assertion is confirmed behaviorally. Attack 2
SURVIVES.

## 4. Kill bars

- K1 (prereg frozen before attack): PASS. Commit 12da75511
  contains only PREREG_REVISE_ATTACK.md and strictly precedes
  every attack world file, build script, binary, and run
  (verified by commit ancestry).
- K2 (attacks run): PASS. Setup validation, B-REPLAY on S-RK
  (3x), REVISE on S-RK (3x), drill-excised learner on S-CONJ2
  (3x) and S-NEG2 (3x): all executed with committed raw logs.
- K3 (pure Zag, 3/3 identical): PASS. Shell, znc, git, grep, diff,
  cmp, md5sum, sha256sum, wc, sed only; zero Python invocations at
  every stage (authoring, world files, excision, build, run,
  analysis, byte checks via shell-only check_no_dash.sh). Every
  reported configuration is 3/3 byte-identical with zero stderr
  bytes. No em/en dash bytes in any new file.

## 5. Combined verdict rule application (frozen)

Per PREREG_REVISE_ATTACK.md section 6:
REVISE-ATTACK-KILLS iff (Attack 1 KILLS) OR (Attack 2 KILLS).
Attack 1 SURVIVES (E1 killed). Attack 2 SURVIVES (E2 killed).
Neither attack is VOID. K1, K2, K3 all PASS.

Verdict: REVISE-ATTACK-SURVIVES.

## 6. Honest scope

This attack killed two specific alternative explanations:

E1 (rote replay explains everything): DEAD. On S-RK, B-REPLAY
scores 0 while REVISE scores 1 via the full D1 revision trace.
REVISE's demonstrated advantage is no longer bounded to "over
greedy strategies only": on S-RK it strictly outperforms rote
memorization. This strengthens the step-5 bound.

E2 (drill secretly guides the mechanism): DEAD. The drill is
empirically inert; all mechanism outputs are byte-identical with
it excised.

REVISE-ATTACK-SURVIVES keeps REVISE at bounded L2. It claims no
L3, no Criterion 0, and does not advance the pipeline past step 6.
Untested: OOD delays beyond the 1..4 literal inventory,
multi-inhibitor worlds, the 3-literal cap boundary, transfer/reuse
(step 9), and the independent red team (step 10). The contaminated
research paper was not touched.

## 7. Evidence index (all under revise_attack/)

- PREREG_REVISE_ATTACK.md (commit 12da75511, frozen alone first)
- ATTACK_BUILD.sh (build script)
- world_srk.zag (attack world S-RK; diff vs S-NEG2 shows only
  passive times and name string)
- f3_revise_frozen.zag (frozen learner, sha256-verified)
- b_replay_frozen.zag (frozen baseline)
- w_sneg2_ref.zag, w_sconj2_ref.zag (pristine sealed worlds via
  git show)
- f3_revise_nodrill.zag (drill-excised learner; diff shows only
  the removed REFUTE-DRILL block)
- run_valid_n.zag / bin_valid_n / raw_valid_n_r{1,2,3}.txt/.err
  (setup validation; md5 85ebb436b4f7d6eac370466bc98a878c)
- run_srk_replay.zag / bin_srk_replay /
  raw_srk_replay_r{1,2,3}.txt/.err (B-REPLAY GOAL_REAL 0)
- run_srk_revise.zag / bin_srk_revise /
  raw_srk_revise_r{1,2,3}.txt/.err (REVISE GOAL_REAL 1, md5
  85ebb436b4f7d6eac370466bc98a878c, byte-identical to S-NEG2)
- run_nodrill_c.zag / bin_nodrill_c /
  raw_nodrill_c_r{1,2,3}.txt/.err
- run_nodrill_n.zag / bin_nodrill_n /
  raw_nodrill_n_r{1,2,3}.txt/.err
- build_*.err (znc notices only; no errors)
- RESULT_REVISE_ATTACK.md (this file)
