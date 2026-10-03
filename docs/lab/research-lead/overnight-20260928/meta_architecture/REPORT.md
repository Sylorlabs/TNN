# REPORT: META-ARCHITECTURE (MA1) -- Multi-cell competitive means

## Frozen verdict: MULTI-CELL RECOVERY DEMONSTRATED

Per the frozen verdict mapping, B5a (primary, kill bar) PASSED (R_X = 7,
within 1..99) with B1, B2, B3, B5e, B5f, B6, B7 all PASS and B5b
(replication guard) PASS, so the preregistered headline verdict is
MULTI-CELL RECOVERY DEMONSTRATED: the learner-owned multi-cell
architecture recovers from the C426 distractor shift in 7 episodes
against the single-cell baseline's 624, with no human-supplied change
labels. Nothing was weakened or reinterpreted. One transparent
pre-implementation amendment (v1.1, MARG interval calibration, analytic)
is disclosed below.

## What was built (pure Zag, safebin-only)

- `ma1.zag` (642 lines): three conditions in one frozen binary.
  X: 4-cell learner, Block D (12 episodes, MD's exact distractor block)
  then Block R (660 episodes, tiled PRNG permutation of {76..84},
  period 9) then Block B2 (60 episodes, tiled {16..24}, shift back).
  Y: 4-cell learner, Block R + B2 only (fresh). Z: single-cell learner
  (MD treatment rule: floor mean of all past reveals), D + R + B2
  (C435 replication). N=1200 flips/episode/condition, independent
  streams (SEED_X=20261021, SEED_Y=20261022, SEED_Z=20261023), shared
  parameters (SEED_B=20261020). Estimator `etc_ep` byte-identical to
  lm2.zag; W=20, criterion |est_n - v*| < 5.
- Cell mechanism (frozen, PREREG.md Section 1): per episode every cell
  predicts its floor-mean (50 if empty); active cell = argmin score
  (ties: lowest index); after the supervised reveal every score updates
  by EMA(3/4) of |prediction - value|; the winner (argmin error) absorbs
  the value; consec tallies consecutive active errors > 20; at 3 the
  highest-score cell among non-active non-winner cells is reseeded at
  the current value (sum=value, n=1, score=0). No block labels, change
  indicators, or episode indices reach the cells; the e==11/671/731
  hooks only copy state to snapshot areas (write-only observation, no
  feedback into cell state).
- Commit order honored: prereg v1 (c3fb5a8, PREREG.md + NAMECHECK.md
  Step 0 only) and v1.1 amendment (5147381, MARG interval calibration
  fix, analytic justification, no bar weakened), both strictly before
  any implementation file. This commit adds implementation + report.
- Toolchain: PATH="$HOME/safebin" throughout; python3/python/perl/ruby/
  node all unresolvable; zero forbidden invocations. One znc analyzer
  warning (A0101 on `etc_ep`, the known false-positive class from
  LM2/MG/FB/MD; max index is fbase+e*1200+1199, in bounds).
- Determinism: 3/3 runs byte-identical,
  sha256 `6711c25c18d6463529c207aec5cbb247b0c7a3a89ccd09d1ee228628b670facb`.

## Results (frozen binary output, 3/3 identical)

```
RX=7 RY=2 RZ=624 RXF=3 RXB2=4 COSTXY=1022 COSTXZ=-3936
B5A=1 B5B=1 B5C=1 B5D=1 B5E=1 B5F=1 B5G=1
DISTINCTD=1 PARID=1 XDISJ=1 MARG=1 GENFAIL=0
TRIGX n=2 E14 E675
TRIGY n=0
SNAPXD S0=180 N0=9 C0=10 S1=40 N1=1 C1=15 S2=54 N2=1 C2=22 S3=47 N3=1 C3=19
SNAPXR S0=36248 N0=445 C0=1 S1=40 N1=1 C1=39 S2=16689 N2=217 C2=3 S3=47 N3=1 C3=26
SNAPXB S0=597 N0=33 C0=1 S1=661 N1=29 C1=2 S2=16689 N2=217 C2=55 S3=47 N3=1 C3=26
SNAPYR S0=52800 N0=660 C0=1 (cells 1..3 empty)
SNAPYB S0=52800 N0=660 C0=59 S1=1199 N1=60 C1=1 (cells 2..3 empty)
```

Block-R head (X): E0013 P=81 EX=268 MXA=20; E0014 P=83 EX=312 MXA=40;
E0015 P=76 EX=1 MXA=83; E0016..E0018 MXA=83, EX<=3; E0019 P=84 EX=1
MXA=81 (first |mean-80|<=1: R_X=7). After k=7 the active mean stays in
[81,82] for the remaining 653 Block-R episodes (1 episode at 82):
the recovery is sustained, not transient.

Block-B2 head (X): E0673 P=16 EX=177 MXA=81; E0674 P=24 EX=133 MXA=81;
E0675 P=19 EX=381 MXA=76; E0676 P=22 EX=1 MXA=19 (R_XB2=4). Z in B2:
MZ stuck at 78..79, EZ in the hundreds: no re-recovery.

Bar scorecard:
- B1 COMMIT-ORDER: PASS (v1 + v1.1 strictly predate implementation).
- B2 TOOLCHAIN: PASS (safebin-only, Step 0 recorded, zero incidents).
- B3 DETERMINISM: PASS (3/3 identical, digest above).
- B4 NOVELTY: PASS (12 Block-D parameters distinct; all same-episode
  cross-condition flip vectors differ; per-block ones-fractions inside
  the v1.1 calibrated intervals).
- B5a RECOVERY (PRIMARY, kill bar): PASS (1 <= 7 <= 99).
- B5b BASELINE-REPLICATION: PASS (RZ=624 >= 500; replicates C435's
  ~624 exactly).
- B5c COST: PASS (1022 < 4690).
- B5d SHIFT-BACK: PASS (1 <= 4 <= 30).
- B5e APPARATUS: PASS (max etc <= 1200, genfail 0).
- B5f STREAM-VALIDITY: PASS (PARID=1, XDISJ=1, MARG=1).
- B5g MANIPULATION: PASS (in-binary white-box: X cell 0 ends Block D
  at (sum=180, n=9), the distractor block genuinely captured as a
  dedicated cell with mean exactly 20).
- B6 NO-RESEARCHER-RULE: PASS (learner decisions use only revealed
  values and scores derived from them; the episode-index-conditioned
  hooks are write-only snapshots/flags with no feedback into cell
  state; audited in source).
- B7 OPAQUE-IDS: PASS (labels E0001..; case-insensitive grep for the
  frozen 29-word list returns empty).

## Reading of the result

The mechanism took the reallocation path, earlier than the typical
prediction. Block D ended with an atypical value (P=47, active error
27 > 20, consec=1). Block-R k=1: active cell 0 (mean 20) errs 61,
consec=2; the winner (cell 2, mean 54) absorbs v*=81. k=2: score
selection moves the active cell to cell 1 (mean 40), which errs 43,
consec=3 -> REALLOCATION FIRES at E14. Victim: cell 0 itself, the
distractor cell, which had the worst recent score (32) among the
non-active non-winner cells. It is reseeded at v*=83 (sum=83, n=1,
score=0) and goes active at once (MXA=83 at E0015, EX=1). From there
the reseeded cell 0 and cell 2 competitively absorb Block-R values
(445 vs 216 absorbs); the active mean reaches within-1 of 80 at k=7
and never leaves [81,82] again. Total: 7 episodes vs the single-cell
baseline's 624, measured in the same run on the same streams.

Three facts make this a mechanism demonstration rather than a lucky
draw. First, the single-cell baseline Z, running the MD rule on the
identical episode sequence, recovered at RZ=624, reproducing C435's
number exactly: the shift really is the hard C426/C435 shift, and the
7-vs-624 gap is the architecture, not the scenario. Second, the
white-box snapshots show the predicted cell specialization emerging
from the dynamics with no researcher-assigned roles: after Block D,
cell 0 = (180,9) is the distractor mean and cells 1..3 hold the three
atypical values; after Block R, two cells hold ~80-mass (means 81 and
77); after Block B2, cells 0..1 hold ~20-mass while cell 2 still
dormant-holds the 80-mass (16689, 217). Third, the shift-back: at
B2k=3 the failure streak fires again (E675), reseeding the worst
stale cell, and X is within-1 of 20 by B2k=4 while Z never re-recovers
inside B2. The dormant 80-cell survives both reallocations untouched:
multiple priors are genuinely maintained across two shifts, and the
fresh condition Y (R_Y=2, pure absorption, no trigger) shows the
selection half of the mechanism working alone.

Prediction misses, reported honestly: COSTXY=1022 landed above the
preregistered [100,800] range (Block-R k=2's active cell was the
mean-40 spare on an unlucky stream, EX=312); the bar (< 4690) still
passes at 4.6x margin. R_Y=2 beat the deterministic guarantee of 10
(the first Block-R value fell in [79,81]); the guarantee was a bound,
not a point prediction. The B2 trigger victim was cell 0 (the 80-cell,
highest score), not "a stale spare" as the prereg's parenthetical
guessed; the rule itself behaved exactly as specified.

## The v1.1 amendment (disclosed)

v1.0's MARG interval [0.30,0.95] was provably miscalibrated: Block D's
values average 26.75 by construction, so E[ones-rate]=0.2675 < 0.30
necessarily. v1.1 replaced it with analytic per-block intervals from
the disclosed block means (D: [0.20,0.35], R: [0.70,0.90],
B2: [0.12,0.28]), wide sanity-only bounds. No kill bar was changed or
weakened; the amendment was committed (5147381) before any
implementation file, and the pre-amendment test binary was discarded
and rebuilt.

## Honest boundaries

- What is learned are cell means (empirical-Bayes base values), same
  level as LM2/MD (L1/L2-ish). Not strategy invention, not L3. The
  mechanism constants (K=4, FAIL=20, TRIG=3, EMA 3/4, W=20, empty
  value 50) are researcher-supplied; cell selection and reallocation
  are learner-driven from failure patterns.
- The truth-reveal per episode is supervised; within-episode learning
  has zero feedback.
- One shift scenario (20 -> 80 -> 20), one frozen seed quadruple, fixed
  before implementation; no seed selected on outcomes.
- The victim rule (highest recent score) destroyed the distractor cell
  at the Block-R trigger and the 80-cell at the B2 trigger; the
  architecture survived this naivety because a second cell held
  redundant mass each time. A less redundant history could be hurt by
  the naive victim choice; protecting dormant cells with low long-run
  error is identified future work, not claimed here.
- K=4 covers at most a few groups; more groups than cells is untested.
- COSTXY=1022 vs the predicted [100,800]: the cost-range prediction
  was missed (unlucky k=2 stream); the bar still passes comfortably.

## Artifacts in this commit

- `ma1.zag`: frozen implementation (B6/B7 audited).
- `ma1_bin`: frozen compiled binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical outputs
  (sha256 `6711c25c18d6463529c207aec5cbb247b0c7a3a89ccd09d1ee228628b670facb`).
- `REPORT.md`: this file.
- `NAMECHECK.md`: build record updated.
