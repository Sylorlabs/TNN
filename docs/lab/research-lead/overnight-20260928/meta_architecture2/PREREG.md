# PREREG: MA2 -- Dormant-cell protection for the multi-cell architecture

## 0. Standing

MA1 (C440) demonstrated multi-cell recovery: 7 episodes vs the
single-cell baseline's 624, via failure-pattern selection and
reallocation, with no human-supplied change labels. Its honest boundary
states the open problem this experiment answers: the naive victim rule
(highest recent score among non-active non-winner cells) destroyed the
distractor cell at the Block-R trigger and the 80-cell at the Block-B2
trigger; the architecture survived only because a second cell held
redundant mass each time. MA2 adds a learner-owned dormant-cell
protection mechanism on top of MA1's architecture (not a redesign: cell
selection, scoring, absorption, and the trigger condition are
unchanged) and tests whether useful dormant cells can be protected
without blocking legitimate reallocation.

Nothing in this prereg weakens any frozen bar. All thresholds below are
frozen before implementation.

## 1. Protection design (frozen learner mechanism)

MA1's cell state was (sum, n, score). MA2 adds two tallies per cell,
updated ONLY from revealed episode values:

- wpart[i]: episodes on which cell i was the winner (argmin
  prediction error, ties to lowest index).
- wpsm[i]: sum of cell i's prediction error over those winner
  episodes.

A cell is PROTECTED iff wpart[i] >= PACT and wpsm[i]/wpart[i] <= PERR,
with frozen researcher-supplied constants PACT = 5, PERR = 10 (same
status as MA1's K=4, FAIL=20, TRIG=3). On reseed, wpart/wpsm reset to
0 with the rest of the cell state; protection must be re-earned.

Design rationale, frozen:

- Protection measures demonstrated explanatory success: the cell
  repeatedly best-explained revealed values with low error. A
  single-observation spare (wpart = 1) can never be protected; a
  regime model (wpart in the dozens to hundreds, mean win-error in
  the low single digits) always is. The margins are wide, not tuned:
  at the Block-R trigger the distractor cell has wpart = 9 with mean
  win-error ~= 2, while the atypical spares have wpart <= 3.
- The criterion is deliberately NOT recency-weighted. A recency
  requirement would unprotect exactly the dormant cells this
  mechanism exists to save: during a 660-episode block the dormant
  regime cell's last win is hundreds of episodes old, yet its
  knowledge is precisely what the next shift needs. "Recent
  activity" here means a standing record of activity, not a fresh
  timestamp.
- Winner-episodes (not active-episodes) are the unit because winning
  means the cell explained the data; being active while failing is
  evidence against the cell, not for it.

Victim rule (replaces MA1's naive rule): at a trigger, the victim is
the highest-score cell (ties to highest index, as in MA1) among cells
that are neither the active cell nor the current winner AND are not
protected.

Decline rule (pressure valve, new): if no unprotected candidate
exists among the non-active non-winner cells, the reseed is
DECLINED: no cell state changes, consec resets to 0, and the decline
is logged. Rationale: when every candidate cell is a demonstrated
regime model, destroying one to reseed is never legitimate
reallocation; the inventory already covers the data, and score
selection will move the active cell to the best-explaining dormant
cell within a few episodes. Reallocation is therefore never blocked
when a useless cell exists, and never destroys demonstrated
knowledge when none exists. A decline is counted (DECL) and its
prot-flag bitmask logged, same white-box treatment as a reseed.

## 2. Experimental protocol (frozen harness)

Four conditions, one frozen binary. X, Y, Z are MA1's conditions
unchanged (X: D+R+B2 multi-cell; Y: R+B2 multi-cell fresh; Z: D+R+B2
single-cell MD rule). New:

- W: multi-cell learner, Block D (12 episodes, MA1's exact block D)
  then Block R (660 episodes, MA1's exact tiled {76..84} permutation,
  period 9) then Block B2 (60 episodes, tiled {16..24}, period 9)
  then Block R3 (60 episodes, the same {76..84} tile as Block R: the
  80 regime returns). 852 episodes total. Three shifts: 20->80,
  80->20, 20->80.

Block values for W episodes 0..731 are generated from the same
permutations as X (shared SEED_B); W's R3 reuses the Block-R tile.
Cell updates depend only on revealed values, so X and W have
identical cell-state trajectories through episode 731 by
construction; their flip streams differ (independent seeds).

Frozen seeds (B/X/Y/Z identical to MA1, frozen before MA1's outcomes;
W new and frozen here):
SEED_B = 20261020 (parameters), SEED_X = 20261021, SEED_Y = 20261022,
SEED_Z = 20261023, SEED_W = 20261024.

## 3. Frozen metrics

All MA1 metrics unchanged (RX, RY, RZ, RXF, RXB2, COSTXY, COSTXZ,
TRIGX, TRIGY, B5a..B5g, DISTINCTD, PARID, XDISJ, MARG, GENFAIL), plus:

- R_WB2: first Block-B2 episode of W with |mean_Wa - 20| <= 1
  (0 if never).
- R_W: first Block-R3 episode k of W (k = 1..60) with
  |mean_Wa(k) - 80| <= 1 (0 if never).
- TRIGW: reallocation reseeds in W; DECLX/DECLY/DECLW: declines per
  condition.
- PROTDEST: reseeds whose victim was protected at reseed time
  (in-binary white-box tally).
- Per trigger evaluation: episode, victim index (or decline marker),
  victim protected-flag, and the 4-cell protection bitmask
  (white-box log).

## 4. Mechanism-derived predictions (frozen)

X and W share MA1's seeds and pre-trigger rules, so X's trajectory is
byte-identical to MA1's through E14, and W's cell trajectory matches
X's through E731.

- T1 (X E14, W E14): consec hits 3 exactly as in MA1. Winner is
  cell 2; candidates are cell 0 (protected: wpart = 9, mean
  win-error ~= 2) and cell 3 (unprotected, wpart = 1). Victim =
  cell 3, the atypical spare. The distractor cell survives its first
  trigger untouched. Predicted R_X in [4, 64] (MA1's mechanism
  bound; the reallocation path, as in MA1).
- T2 (X E675, W E675): the active 80-cell fails 3 straight at
  B2k = 3. The winner is cell 0 (the dormant distractor cell,
  err <= 4; it also absorbs, re-earning mass). Candidates: cell 1
  (unprotected, wpart = 1, never wins Block R) and cell 2. Victim =
  an unprotected cell (predicted cell 1, the higher score; either
  satisfies every bar). Both protected 80-cells survive. No decline
  in X (DECLX = 0). Predicted R_XB2 <= 13, R_WB2 <= 13.
- T3 (W E735): the active 20-cell fails 3 straight at R3k = 3.
  Winner = the 80-cell reseeded at T1 (err <= 4), spared by rule.
  Two sub-cases, both honest and both consistent with every bar:
  (A) cell 2 accumulated >= 5 Block-R wins with mean win-error
  <= 10 and is protected: then every candidate is protected, the
  reseed is DECLINED (DECLW >= 1), and score selection moves the
  active cell to a dormant 80-cell within a few episodes
  (dormant reuse, zero destruction); (B) cell 2 stayed below the
  protection bar: it is the sole unprotected candidate and is
  reseeded (TRIGW = 3), exactly the legitimate-reallocation path.
  Predicted R_W <= 15 in both cases; PROTDEST = 0 in both cases.
- White-box end states: W's final snapshot shows four cells
  holding block mass (two ~= 20, two ~= 80); no protected cell is
  ever reseeded in any condition; the distractor cell is never a
  victim in X or W.
- Y: no triggers (dynamics identical to MA1 until a first trigger;
  MA1 had none), TRIGY = 0, DECLY = 0. Z: single-cell rule
  unchanged, RZ in [625, 635] (C435 replication guard).
- COSTXY < 4690 (bar only; the point value diverges from MA1's 1022
  because the T1 victim differs, so no tight range is claimed).

## 5. Frozen verdict mapping

- B1 COMMIT-ORDER: PASS iff this prereg commit (PREREG.md +
  NAMECHECK.md Step 0 only) strictly predates every implementation
  commit.
- B2 TOOLCHAIN: PASS iff safebin-only PATH throughout, Step 0
  recorded, zero forbidden-executable invocations.
- B3 DETERMINISM: PASS iff 3/3 runs byte-identical (sha256 recorded).
- B4 NOVELTY: PASS iff (a) 12 Block-D parameters pairwise distinct,
  (b) every episode's flip vector differs across conditions
  (same-episode X/Y/Z pairwise, plus W vs X/Y/Z over their shared
  episode ranges), (c) per-condition per-block ones-fraction within
  the MA1 v1.1 calibrated intervals, with W's R3 block in
  [0.70, 0.90] ([50400, 64800] of 72000 flips).
- B5a RECOVERY (PRIMARY, kill bar): PASS iff 1 <= R_X <= 99.
- B5b BASELINE-REPLICATION: PASS iff R_Z >= 500.
- B5c COST: PASS iff COST_XY < 4690.
- B5d SHIFT-BACK: PASS iff 1 <= R_XB2 <= 30.
- B5e APPARATUS: PASS iff max etc <= 1200 and genfail = 0.
- B5f STREAM-VALIDITY: PASS iff PARID = 1 (parameters identical
  across conditions per episode/block, including W over 0..731) and
  XDISJ = 1.
- B5g MANIPULATION: PASS iff the in-binary white-box assertion holds
  that cell 0 of X and of W both end Block D with (sum = 180, n = 9).
- B6 NO-RESEARCHER-RULE: PASS iff the learner fns' only
  cross-episode inputs are revealed values and tallies derived from
  them (wpart/wpsm included); no episode-index or block-conditioned
  logic in learner code (audit by diff/grep; harness gen() is the
  experimenter as in MA1).
- B7 OPAQUE-IDS: PASS iff episode labels are E0001.. and a
  case-insensitive grep for the frozen 29-word list (coin, bias,
  heads, tails, shrink, prior, learn, meta, cluster, outlier,
  typical, atypical, general, poisson, rate, lambda, gauss, count,
  event, slot, family, distractor, shift, phase, regime, original,
  interference, recover) in ma2.zag returns empty.
- B8 PROTECTION (CO-PRIMARY, kill bar): PASS iff PROTDEST = 0, i.e.
  no reseed in any condition destroyed a cell that met the
  protection criterion at reseed time.

Headline verdict: DORMANT-CELL PROTECTION DEMONSTRATED iff B5a PASS
and B8 PASS with B1, B2, B3, B5e, B5f, B6, B7 all PASS and B5b PASS.
B5b FAIL invalidates the comparison (verdict becomes UNDECIDED, not
a pass). No bar may be weakened after the run; a broken prereg is
amended transparently and re-frozen, never reinterpreted.

## 6. Honest boundaries (frozen)

- What is learned are cell means, same level as MA1 (L1/L2-ish).
  Not strategy invention, not L3. The mechanism constants (K=4,
  FAIL=20, TRIG=3, EMA 3/4, W=20, empty value 50, PACT=5, PERR=10)
  are researcher-supplied; selection, protection status, victim
  choice, and decline are learner-driven from failure patterns and
  revealed values.
- Truth-reveal per episode is supervised; within-episode learning
  has zero feedback.
- Protection is a veto plus a decline, not a capacity increase:
  K=4 covers at most 4 demonstrated block models. A fifth distinct
  block with all cells protected would be declined indefinitely;
  redundancy-aware victim choice (preferring a protected cell whose
  knowledge duplicates another's) is identified future work, not
  claimed here.
- The decline path (T3 case A) is predicted but stream-dependent;
  both sub-cases satisfy every bar and are reported as observed.
- One W scenario, one frozen seed quintuple, fixed before
  implementation; no seed selected on outcomes. MA1's four seeds
  are reused for direct comparability (they were frozen before
  MA1's outcomes existed).

## 7. Artifacts planned

- `ma2.zag`: frozen implementation (B6/B7 audited).
- `ma2_bin`: frozen compiled binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical outputs.
- `REPORT.md`: results and frozen verdict.
- `NAMECHECK.md`: build record (this file's Step 0 + build record).
