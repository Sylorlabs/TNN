# RESULT: F3 REVISE Simple-Baseline Comparison (Pipeline Step 5)

Verdict: REVISE-BASELINE-PASS.

Parent prereg: revise_baseline/PREREG_REVISE_BASELINE.md (4786633c5)
plus Amendment 1 (db585360a), both frozen before any baseline
implementation file, build script, binary, or run existed. K1 holds by
commit ancestry (amendment db585360a strictly precedes the implementation
commit; no build or run occurred under the original prereg).

Parent chain: design ca157c743, builder prereg c197e7cd8, builder result
7009d711c (REVISE-PASS), sealed prereg 8cdf0992a, sealed result 1df8addec
(REVISE-SEALED-PASS), repro 7407dd4a7 (REVISE-REPRO-PASS).
Pipeline: this completes step 5 (simple-baseline comparison) only.

## 1. What was compared

Two researcher-authored simple baselines, implemented in pure Zag, run
against the sealed worlds (byte-identical files from 1df8addec):

- B-REPLAY (b_replay.zag): rote memorization. Observes the passive
  schedule, finds the first Y=1 event, replays the control actions in
  the preceding 4-step window verbatim.
- B-SINGLETON (b_singleton.zag): greedy best literal. Scores all 32
  candidate literals (control var x delay 1..4 x polarity) by F1 on
  passive observations, picks the best per the frozen tie-break, plans
  once, executes once. No conjunctions, no trials, no revision.

REVISE reference (frozen, from sealed evaluation):
- S-CONJ2: GOAL_REAL 1, FINALRULE [X@3 & Z@2].
- S-NEG2: GOAL_REAL 1 (attempt 2), FINALRULE [X@2 & !Z@2].

## 2. Runs (pure Zag: shell + znc only; zero Python)

Sealed world bytes verified by sha256 before any run (both OK against
Amendment 1 hashes). Four configurations, 3/3 byte-identical stdout per
configuration, zero stderr bytes on all 12 runs:

- replay_c (B-REPLAY + S-CONJ2): B-REPLAY GOAL_REAL 1 (3/3).
  md5 3becf8222a7a0137bbe4de2fc64b8730 (3/3 identical).
- replay_n (B-REPLAY + S-NEG2): B-REPLAY GOAL_REAL 1 (3/3).
  md5 3becf8222a7a0137bbe4de2fc64b8730 (3/3 identical).
- single_c (B-SINGLETON + S-CONJ2): B-SINGLETON GOAL_REAL 0,
  lit=Z@2 (3/3). md5 870843506bd28ecd7fe22d013533298e (3/3).
  Note: the frozen tie-break picked Z@2 over X@3 (both F1=1.0, Z@2
  has smaller delay k=2 vs k=3); the prereg's predicted literal
  (X@3) was wrong but the predicted outcome (FAIL) was correct. Plan SET Z at t=0 gives Y(2)=0 since X was
  never set.
- single_n (B-SINGLETON + S-NEG2): B-SINGLETON GOAL_REAL 0,
  lit=X@2 (3/3). Plan SET X at t=0; the goal-setup inhibitor Z=1
  at t=0 blocks Y(2)=0. No revision, so it stays failed.

## 3. Comparison bars (frozen)

R = REVISE (1, 1). P = B-REPLAY (1, 1). S = B-SINGLETON (0, 0).

- CB1 (REVISE beats the greedy baseline): R_c=1 > S_c=0. HOLDS.
  REVISE strictly outperforms B-SINGLETON on S-CONJ2 (and S-NEG2).
- CB2 (no baseline beats REVISE): no configuration has GOAL_REAL 1
  where REVISE has 0. HOLDS. B-REPLAY ties REVISE; B-SINGLETON is
  strictly worse.

Verdict: REVISE-BASELINE-PASS (CB1 and CB2 both hold).

## 4. Honest scope (pre-registered bound)

B-REPLAY matches REVISE on both sealed worlds (1,1 vs 1,1). The sealed
worlds are solvable by rote replay of the passive schedule: the
demonstrations contain the answer pattern. This honestly bounds the
step-5 claim: REVISE's demonstrated advantage is specifically over
greedy single-literal strategies - it forms conjunctions via
trial+growth (S-CONJ2) and revises on goal failure by growing inhibitor
guards (S-NEG2) - not over memorization. The PASS verdict stands via
CB1, with this bound recorded, not hidden.

This is a bounded-L2 infrastructure verdict. No L3 claim, no Criterion 0,
no revival of the retracted F3 Phase 3 BUILD-PASS. Pipeline steps 6-11
(alternative-explanation attack, OOD, ablation, transfer/reuse,
independent red team, governance audit) remain open.

## 5. Kill bars

- K1 (prereg frozen before implementation): PASS. Amendment db585360a
  strictly precedes the implementation commit (verified by
  git merge-base --is-ancestor). No build or run occurred before the
  amendment.
- K2 (baselines run): PASS. All four configurations ran 3x with
  committed raw logs and scored GOAL_REAL lines.
- K3 (pure Zag, 3/3 identical): PASS. Shell, git, znc, coreutils only;
  zero Python invocations at every stage (authoring, build, run,
  analysis, byte checks via shell-only check_no_dash.sh). 3/3
  byte-identical per configuration; zero stderr bytes.

## 6. Governance notes

- Amendment 1 disclosed a hash-recording error in the original prereg
  (wrong sha256 copied for world_sconj2.zag); corrected transparently
  before any implementation, build, or run. The world files were never
  in question (they are the sealed-evaluation files from 1df8addec).
- The contaminated research paper was not touched.
- One prediction in the prereg was wrong (B-SINGLETON picked Z@2, not
  X@3, on S-CONJ2); the outcome prediction (FAIL) was correct and the
  verdict rule depends only on measured GOAL_REAL, not on which
  literal was picked. Recorded here, not hidden.
