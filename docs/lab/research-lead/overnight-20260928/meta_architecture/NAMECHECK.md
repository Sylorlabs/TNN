# NAMECHECK: META-ARCHITECTURE (MA1: multi-cell competitive means)

## Step 0: Toolchain guard (mandatory, recorded before any work)

- `export PATH="$HOME/safebin"` used for every shell command in this lane.
- `which python3` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which python` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which perl` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which ruby` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which node` returns NOTHING under the safebin-only PATH (verified 2026-10-03).
- `which znc` returns `/home/hatch/safebin/znc` (pinned Linux binary; verified 2026-10-03).
- `which git` returns `/home/hatch/safebin/git` (verified 2026-10-03).
- Safebin contents: coreutils, git, awk, sed, grep, cmp, diff, sha256sum,
  znc, ...; no python3/python/perl/ruby/node.
- All scientific computation in this lane is pure Zag (znc-compiled
  binaries). Shell is used only for: safebin setup, file staging,
  znc invocation, binary execution, hashing, git operations, diff/grep
  audits.
- Zero invocations of python3, python, or any other forbidden
  executable. No incidents to disclose.

## Step 1: Lane location and commit discipline

Lane repo: this directory
(`~/workspace/docs/lab/research-lead/overnight-20260928/meta_architecture/`),
fresh `git init -b main` 2026-10-03. Nothing is pushed to GitHub;
commits stay local with explicit pathspecs. Commit order: the first
commit contains ONLY PREREG.md (frozen, v1) and NAMECHECK.md (Step 0 +
this design record). The Zag source, binary, run logs, and REPORT.md
come in later commits, all strictly postdating the prereg commit.

## Design record (pre-prereg, no implementation run)

MA1 answers the parent task: design a learner-owned multi-cell
architecture that avoids the C426/C435 problem (single-cell mean
commits to the distractor block; ~624 episodes to wash it out).

Architecture: K=4 cells, each (sum, n, score). Per episode every cell
predicts its floor-mean (50 if empty); the active cell is the argmin
score (ties to lowest index); the estimator is LM2/MD's frozen etc_ep
with the active mean. After the supervised reveal: every cell's score
is updated by EMA (3/4 weight) of |prediction - value|; the winner
(argmin error) absorbs the value; a consecutive-failure tally on the
active cell triggers reallocation (3 straight errors > 20) of the
highest-score non-active non-winner cell, reseeded at the current
value. No block labels, change indicators, or episode indices reach the
learner; selection and reallocation run on failure patterns only.

Experiment: three conditions in one frozen binary. X: multi-cell,
Block D (MD's exact 12-episode distractor block) then Block R (660
episodes of tiled PRNG permutation of {76..84}, period 9) then Block B2
(60 episodes tiled {16..24}, period 9, shift back). Y: multi-cell,
Block R + B2 only (fresh). Z: single-cell (MD rule), D + R + B2 (C435
replication). N=1200, independent streams, shared parameters,
seeds 20261020/21/22/23.

Frozen predictions: R_X in [4, 64] via either the absorption path
(winner absorbs every Block-R episode; old mass at most n=2 dilutes
within 63 absorbs) or the reallocation path (clean reseed, within-1 in
<= 12); R_Y = 10 deterministically (9 consecutive absorbs = one full
period = mean exactly 80.0); R_Z in [625, 635] (replicates C435 ~624);
COST_XY in [100, 800] (vs 4690); reallocation predicted to fire at
Block-B2 episode 3 with R_XB2 <= 13.

Kill bar B5a: 1 <= R_X <= 99 (|active-mean - 80| <= 1; Y sits at 80 +/- 1
from k=10, so this is the draw-luck-free form of "within-1 of fresh";
R_XF reported alongside). Full bar list and verdict mapping in
PREREG.md Section 5. No bar may be weakened after the run.

Pre-prereg design-phase work (no frozen experiment executed): the
recovery bounds above were derived by hand from the frozen update rules
(no code run); the at-most-2-per-cell atypical distribution was verified
across all 6 permutation orders by case analysis recorded in PREREG.md
Section 4. No calibration Monte Carlo was run; the bounds are
mechanism-derived, not fitted.

## Build record

- 2026-10-03: `ma1.zag` written (642 lines) after prereg v1 + v1.1
  amendment. Learner: 4 cells (sum, n, score), argmin-score selection
  (ties: lowest index), frozen `etc_ep` byte-identical to lm2.zag,
  EMA(3/4) score update, winner-absorbs, consec tally on active errors
  > 20, reallocation at 3 (victim = highest score among non-active
  non-winner cells, ties: highest index; reseeded at current value).
  Harness: Block D = MD's exact 12-episode block; Block R = 660
  episodes tiled PRNG permutation of {76..84} (period 9); Block B2 =
  60 episodes tiled {16..24}; conditions X (732), Y (720), Z (732);
  N=1200; seeds 20261020/21/22/23. B7: case-insensitive grep for the
  frozen 29-word list returns empty (0 matches). Compiled with pinned
  safebin znc -> `ma1_bin`; one A0101 analyzer warning, the known
  false-positive class (max index fbase+e*1200+1199, in bounds).
- 2026-10-03: 3/3 runs byte-identical, sha256
  `6711c25c18d6463529c207aec5cbb247b0c7a3a89ccd09d1ee228628b670facb`
  (run1/2/3.txt). Results: RX=7 RY=2 RZ=624 RXF=3 RXB2=4
  COSTXY=1022 COSTXZ=-3936; TRIGX n=2 (E14, E675), TRIGY n=0; all
  bars PASS (B5a..B5g, DISTINCTD, PARID, XDISJ, MARG, GENFAIL).
  White-box: X cell 0 ends Block D at (180,9) [B5g]; Block-R trigger
  at k=2 reseeded the distractor cell itself (worst recent score);
  reseeded cell + cell 2 split Block-R absorbs 445/216; active mean in
  [81,82] for the rest of Block R (sustained, not transient). B2
  trigger at k=3, R_XB2=4; Z never re-recovers in B2. Honest misses:
  COSTXY=1022 above the predicted [100,800] range (unlucky k=2
  stream); R_Y=2 beat the deterministic bound of 10 by luck.
- Commit order self-check: prereg v1 (c3fb5a8) + v1.1 amendment
  (5147381) strictly before this implementation commit. PASS (B1).
