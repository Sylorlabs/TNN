# PREREG: META-ARCHITECTURE (MA1) -- Multi-cell competitive means with
# failure-pattern selection and reallocation

## v1.1 amendment (2026-10-03, before any implementation commit)

MARG interval calibration fix. v1.0 specified B4(c)/B5f with
"per-condition ones-fraction within [0.30, 0.95] per block". This
interval is provably miscalibrated, by pure analysis, no outcome data
needed: Block D's episode values are 9x{16..24} (sum 180) plus
{40,47,54} (sum 141), i.e. mean 321/12 = 26.75 by construction, so
E[ones-rate] on Block D is 0.2675 < 0.30 necessarily (sd ~= 53/14400;
P(rate >= 0.30) ~= 0). The interval cannot contain Block D's true rate;
it was a prereg bug, not a finding.

Frozen replacement (analytic, from the disclosed block means; wide
sanity-only bounds at roughly +/-20 sd, catching degenerate streams,
not tuning to outcomes):

- Block D (mean 26.75): ones-rate in [0.20, 0.35].
  X-D / Z-D (14400 flips): [2880, 5040].
- Block R (mean exactly 80): ones-rate in [0.70, 0.90].
  X-R / Y-R / Z-R (792000 flips): [554400, 712800].
- Block B2 (mean exactly 20): ones-rate in [0.12, 0.28].
  X-B2 / Y-B2 / Z-B2 (72000 flips): [8640, 20160].

No kill bar is changed or weakened (B5a untouched); the bar's intent
(stream sanity) is unchanged; only the provably-wrong constants are
corrected. Implementation (ma1.zag) is amended to match before the
frozen runs; the pre-amendment test binary is discarded and rebuilt.

## 0. Standing

This is Micah's priority #8 (lifetime/meta-learning). It follows the
completed meta-learning map:

- C405 (LM1): NO net meta-learning (split: B5b DECREASE PASS, outliers
  killed advantage)
- C411 (LM2): META-LEARNING DEMONSTRATED on cluster episodes
- C415 (MG): TRANSFER DEMONSTRATED across location
- C419 (FB): UNDECIDED across family
- C426 (MD): INTERFERENCE DEMONSTRATED under shift (single-cell mean
  commits to the distractor block, ADV_R = -680)
- C435 (MR): RECOVERY DEMONSTRATED, transient, ~624 episodes to within-1
  of fresh, COST_TF = 4690

The C426/C435 problem: one accumulating mean is a single-regime
commitment. After a 12-episode distractor block it needs ~624 further
episodes to wash the history out. MA1 tests a learner-owned multi-cell
architecture that (1) detects the change from failure patterns alone (no
human-supplied block labels reach the learner), (2) keeps several
candidate means and selects among them per episode, (3) re-allocates a
cell when the in-use mean fails persistently.

Nothing in this prereg weakens any frozen bar. All thresholds below are
frozen before implementation.

## 1. Architecture (frozen learner mechanism)

Four cells (K=4). Each cell holds (sum, n, score), all integers, all
updated ONLY from revealed episode values. Researcher-supplied
mechanism constants (frozen here, not learned): K=4, estimator inertia
W=20 (same as LM2/MD), empty-cell value 50, FAIL=20, TRIG=3, score
smoothing 3/4.

Per episode, with hidden integer value v*:

1. Predict: every cell predicts mean_i = floor(sum_i / n_i), or 50 if
   n_i = 0.
2. Select: active cell a = argmin score_i (ties go to the lowest index).
   The estimator uses mean_a exactly as LM2/MD used m:
   est_n = (20*mean_a + 100*h) / (20+n), criterion |est_n - v*| < 5,
   smallest n in 1..1200, else 1201 (etc_ep byte-identical to lm2.zag).
3. Reveal v* (supervised, same as LM2/MD). For every cell:
   err_i = |mean_i - v*|; score_i = floor((3*score_i + err_i) / 4).
   Scores are the failure-pattern record: recent prediction error per
   cell, no block labels anywhere.
4. Absorb: winner w = argmin err_i (ties to lowest index) takes the
   observation: sum_w += v*, n_w += 1. Cells therefore specialize by
   competitive absorption; diversity emerges from the dynamics, not from
   researcher-assigned roles.
5. Failure streak: if err_a > FAIL (20) then consec += 1 else consec = 0.
   consec counts consecutive episodes where the IN-USE mean failed badly.
6. Reallocate (the change detector's structural response): if
   consec >= TRIG (3), the cell with the highest score among cells that
   are neither the active cell nor the current winner is reset to
   (sum = v*, n = 1, score = 0); consec = 0. Rationale, all
   learner-owned: three straight large errors on the deployed mean is
   evidence the cell inventory misses the current data; the least
   recently useful cell is recycled; the cell that best explains the
   latest evidence (the winner) is spared.

No cell ever sees a block label, a change indicator, or the episode
index. Selection (step 2) and reallocation (step 6) are driven purely by
the failure patterns in steps 3 and 5.

## 2. Experimental protocol (frozen harness)

Three conditions, one frozen binary:

- X: multi-cell learner, Block D then Block R then Block B2.
- Y: multi-cell learner, Block R then Block B2 only (fresh; naive at R).
- Z: single-cell learner (MD treatment rule: mean = floor(mean of ALL
  past revealed values)), Block D then Block R then Block B2. This is
  the C435 replication baseline.

Block D (episodes 1..12, X and Z only): EXACTLY MD's block D: 9 values =
PRNG permutation of {16..24}, 3 values = permutation of {40,47,54} at
idx 3, 7, 11. X and Z share parameters (PARID); Y skips D.

Block R (660 episodes; X episodes 13..672, Y episodes 1..660,
Z episodes 13..672): pure group values, tiled PRNG permutation of
{76..84} with period 9: value_k = perm9[(k-1) mod 9]. Any 9 consecutive
values are exactly one full permutation (sum 720, mean 80.0). The pure
tiling (no {40,47,54} mixed in) matches C435's implied design: it is what
makes "within-1 of 80" well-defined, and it is disclosed here, not
hidden.

Block B2 (60 episodes; shift back): tiled PRNG permutation of {16..24},
period 9 (sum 180, mean 20.0 per 9).

N = 1200 flips per episode per condition; outcome = 1 iff draw < v.
Independent streams per condition. Shared parameters across conditions.

Frozen seeds (disjoint from LM2 20261004/05/06, MG 20261007/08/09,
FB 20261010/11/12, MD 20261013/14/15):
SEED_B = 20261020 (parameters), SEED_X = 20261021, SEED_Y = 20261022,
SEED_Z = 20261023.

## 3. Frozen metrics

- mean_Xa(k): X's ACTIVE cell floor-mean entering Block-R episode k
  (k = 1..660). mean_Ya(k), mean_Z(k) analogously (Z: floor running
  mean over all its past reveals).
- R_X = first k with |mean_Xa(k) - 80| <= 1; 0 if never. R_Y, R_Z
  analogously.
- R_XF = first k with |mean_Xa(k) - mean_Ya(k)| <= 1 (within-1 of
  fresh, reported).
- COST_XY = sum over Block R of (EX_k - EY_k); COST_XZ analogously.
- TRIGX, TRIGY = reallocation counts in Blocks R+B2.
- R_XB2 = first Block-B2 episode with |mean_Xa - 20| <= 1; 0 if never.

## 4. Predicted recovery curve (mechanism-derived, frozen)

Block D end state is DETERMINISTIC for X: cell 0 absorbs all 9
{16..24} values (it wins every one: ties at episode 1 go to index 0,
then its error <= 8 beats every other cell's >= 16), so
cell0 = (sum 180, n 9, mean 20). The 3 atypical values are absorbed by
cells 1..3, at most 2 on any one cell (verified across all 6 permutation
orders: a twice-holding cell always loses the third atypical to an
empty cell, whose |50 - v*| <= 10 beats the holder's >= 11). Z enters
Block R with (sum 321, n 12, mean 26), exactly MD's treatment.

Block R, condition X. Episode k=1: active = cell 0 (lowest score from
Block D), mean 20, err ~= 60 > 20, consec = 1. The winner is a cell
1..3 (its err <= 44 < 60); it absorbs v* ~= 80. From here two
disjoint paths, BOTH fast:

- Path 1 (absorption): the k=1 winner keeps winning every episode (its
  mean only moves toward 80 while others are frozen), absorbing
  consecutive values. Its old mass is at most (n_old <= 2,
  |sum_old - 80*n_old| <= 59). After j = 9q absorbs,
  |mean - 80| = |sum_old - 80*n_old| / (n_old + 9q) <= 59/(2+9q) <= 1
  at q = 7, i.e. j = 63. So R_X <= 64 on this path, typically 10..28
  (n_old = 0 gives exact 80.0 at j = 9; n_old = 1 gives <= 27).
- Path 2 (reallocation): if the active cell errs > 20 three episodes
  running, a clean cell is seeded at v* ~= 80 with n = 1 and score 0,
  becomes active at once, then absorbs every episode: 9 consecutive
  absorbs give sum exactly 720 + seed, mean within 0.5 of 80 at once
  and exact-80-class within 9 episodes. So R_X <= 12 on this path.

Predicted: R_X in [4, 64], typical 10..28. Either path satisfies the
kill bar with large margin. Which path the frozen run takes is reported,
not selected.

Condition Y (fresh): all cells start (0, 0, 0); cell 0 wins k=1
(tie -> index 0), absorbs v*_1, then wins every episode; 9 consecutive
absorbs = one full period = 720, mean exactly 80.0 entering k=10.
Predicted R_Y = 10 deterministically.

Condition Z (single-cell): mean_Z(k) = floor((321 + S_j)/(12+j)),
j = k-1, S_j = tiled sums. |mean - 80| <= 1 needs
(321 + 720q)/(12 + 9q) >= 79, i.e. 9q >= 627, q = 70, j = 630:
mean = floor(50721/642) = 79. Predicted R_Z in [625, 635],
replicating C435's ~624.

Predicted etc shape: EX_1 ~= 220 (mean 20 vs v* ~= 80); EX_2..3 fall to
~30..90 as the active cell switches to the absorbing cell; EX_k <= 10
from about k = 5. COST_XY predicted in [100, 800], far below C435's
4690.

Block B2 (shift back to ~20), condition X: active 80-cell errs ~= 60
three running -> consec hits 3 at B2 episode 3 -> reallocation fires
(predicted), victim = highest-score cell among non-active non-winner
(a stale spare; the winner, cell 0 with err ~= 0, is spared by rule).
The reseeded cell (mean = v* ~= 20, n = 1, score 0) goes active at
B2k = 4 and absorbs every B2 episode; 9 absorbs give exact 20.0 at
B2k = 13. Predicted R_XB2 <= 13. Z will not re-recover inside B2
(its mean needs ~600 more episodes); reported as the contrast.

## 5. Frozen verdict mapping

- B1 COMMIT-ORDER: PASS iff this prereg commit (PREREG.md + NAMECHECK.md
  Step 0 only) strictly predates every implementation commit.
- B2 TOOLCHAIN: PASS iff safebin-only PATH throughout, Step 0 recorded,
  zero forbidden-executable invocations.
- B3 DETERMINISM: PASS iff 3/3 runs byte-identical (sha256 recorded).
- B4 NOVELTY: PASS iff (a) 12 Block-D parameters pairwise distinct,
  (b) every episode's flip vector differs across conditions
  (same-episode X/Y/Z pairwise), (c) per-condition per-block
  ones-fraction within the v1.1 calibrated intervals (D: [0.20,0.35],
  R: [0.70,0.90], B2: [0.12,0.28]). (Block-R/B2 tiling is disclosed
  design, not a novelty violation.)
- B5a RECOVERY (PRIMARY, kill bar): PASS iff 1 <= R_X <= 99.
  (R_X is |active-mean - 80| <= 1; Y sits at 80 +/- 1 from k = 10, so
  this is the draw-luck-free form of "within-1 of fresh"; R_XF is
  reported alongside.)
- B5b BASELINE-REPLICATION: PASS iff R_Z >= 500 (the single-cell
  baseline reproduces C435-scale slowness in this run; predicted
  ~631).
- B5c COST: PASS iff COST_XY < 4690 (beats C435's transient cost).
- B5d SHIFT-BACK: PASS iff 1 <= R_XB2 <= 30 (predicted <= 13).
- B5e APPARATUS: PASS iff max etc <= 1200 and genfail = 0.
- B5f STREAM-VALIDITY: PASS iff PARID = 1 (parameters identical across
  conditions per episode/block) and XDISJ = 1.
- B5g MANIPULATION: PASS iff the in-binary white-box assertion holds
  that X's cell 0 ends Block D with (sum = 180, n = 9), i.e. the
  distractor block was genuinely captured as a dedicated cell with mean
  exactly 20 (the multi-cell analogue of MD's B5d2 manipulation
  check).
- B6 NO-RESEARCHER-RULE: PASS iff the learner fns' only cross-episode
  inputs are revealed values and scores derived from them; no
  episode-index or block-conditioned logic in learner code (audit by
  diff/grep; harness gen() is the experimenter as in LM2/MD).
- B7 OPAQUE-IDS: PASS iff episode labels are E0001.. and a
  case-insensitive grep for the frozen 29-word list (coin, bias, heads,
  tails, shrink, prior, learn, meta, cluster, outlier, typical,
  atypical, general, poisson, rate, lambda, gauss, count, event, slot,
  family, distractor, shift, phase, regime, original, interference,
  recover) in ma1.zag returns empty.

Headline verdict: MULTI-CELL RECOVERY DEMONSTRATED iff B5a PASS with
B1, B2, B3, B5e, B5f, B6, B7 all PASS. B5b FAIL invalidates the
comparison (verdict becomes UNDECIDED, not a pass). No bar may be
weakened after the run; a broken prereg is amended transparently and
re-frozen, never reinterpreted.

## 6. Honest boundaries (frozen)

- The learned quantities are cell means (empirical-Bayes base values),
  same level as LM2/MD (L1/L2-ish). Not strategy invention, not L3.
  The mechanism (K=4, FAIL=20, TRIG=3, EMA 3/4, W=20, empty value 50)
  is researcher-supplied; the selection among cells and the
  reallocation are learner-driven from failure patterns.
- Truth-reveal per episode is supervised; within-episode learning has
  zero feedback.
- One shift scenario (20 -> 80 -> 20), one frozen seed quadruple, fixed
  before implementation; no seed selected on outcomes.
- The reallocation victim rule is naive (highest recent score); Block
  B2 will show whether it harms dormant-cell reuse. Reported as-is.
- K=4 covers at most 3 historical groups plus the current one; more
  groups than cells is untested.

## 7. Artifacts planned

- `ma1.zag`: frozen implementation (B6/B7 audited).
- `ma1_bin`: frozen compiled binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical outputs.
- `REPORT.md`: results and frozen verdict.
- `NAMECHECK.md`: build record (this file's Step 0 + build record).
