# PREREG: MA3 -- Redundancy-aware victim choice

## 0. Standing

MA2 (C444) demonstrated dormant-cell protection: the victim veto plus
the decline rule kept every demonstrated-useful cell alive across
three shifts (RX=7, PROTDEST=0). Its honest boundaries state the open
problem this experiment answers: (1) K=4 covers at most 4 demonstrated
models, so a 5th distinct block with all cells protected would be
declined indefinitely; (2) the decline does not distinguish redundant
from unique knowledge (at MA2's T3, cells 2 and 3 both held 80-mass).
MA3 adds a learner-owned redundancy measure on top of MA2's
architecture (not a redesign: cell selection, scoring, absorption,
the trigger condition, and the protection predicate are unchanged)
and tests whether the architecture can distinguish redundant from
unique knowledge when forced past the K=4 limit.

Nothing in this prereg weakens any frozen bar. All thresholds below
are frozen before implementation.

## 1. Redundancy design (frozen learner mechanism)

New per-trigger computation, from revealed values only. For protected
cells i, j (i != j) with means mi, mj (integer cell means, empty
value 50 as in selection):

  dup(i,j) iff prot(i) AND prot(j) AND |mi - mj| <= RDDM

with frozen researcher-supplied constant RDDM = 10 (same status as
MA2's PACT=5, PERR=10). Cell i is REDUNDANT iff it is protected and
some protected j != i satisfies dup(i,j). The anchor j may be any
protected cell: a candidate, the active cell, or the winner. The
anchor must be protected because a fresh unprotected cell's mean is
a single revealed value, not demonstrated knowledge; treating it as
an anchor would destroy proven models for unproven ones.

Design rationale, frozen:

- Redundancy means demonstrated duplicated explanatory success: two
  cells that both repeatedly best-explained revealed values AND now
  agree on the value of the world. Pairwise mean distance is chosen
  over winner-episode co-tallies because it needs no new per-episode
  state: it is computable at trigger time from existing tallies,
  all derived from revealed values. Honest limitation, frozen: mean
  distance conflates genuinely distinct regimes whose means agree
  within RDDM. The frozen W5 below separates distinct regimes by
  >= 15 while redundant pairs sit at <= 5; adversarial close
  regimes are red-team future work, not claimed here.
- Victim rule (extends MA2's): candidates are the non-active,
  non-winner cells. (a) If any unprotected candidate exists, the
  victim is the highest score (ties: highest index), exactly MA2's
  rule: legitimate reallocation is never blocked. (b) Else, if any
  REDUNDANT candidate exists, the victim is the redundant candidate
  with the LOWEST wpart (ties: highest score, ties: highest
  index): when two cells demonstrably explain the same data, keep
  the stronger demonstration and reseed the weaker duplicate. (c)
  Else, the reseed is DECLINED, exactly MA2's rule: unique
  demonstrated knowledge is never destroyed.
- The mechanism degrades gracefully: each redundancy reseed
  sacrifices one layer of duplication; the survivor becomes unique
  and is then decline-protected. No unique protected cell is ever
  a victim under any path.

## 2. Experimental protocol (frozen harness)

X, Y, Z replicate MA2 exactly (same seeds 20261020..23, same
blocks D/R/B2; the new victim rule never fires on X/Y/Z because an
unprotected candidate always exists at their triggers, so their
trajectories are byte-identical to MA2's by construction). W is
replaced by W5, one frozen binary:

- W5: Block D (12 episodes, MA1's exact block D) then Block R
  (660 episodes, MA1's exact tiled {76..84} permutation, period 9)
  then Block B2 (60 episodes, tiled {16..24}, period 9) then Block
  B4 (60 episodes, NEW tiled {46..54} permutation, period 9) then
  Block B5 (60 episodes, NEW tiled {91..99} permutation, period 9).
  852 episodes total. Five distinct blocks.

The D/R/B2 tiles are drawn from the SEED_B stream in MA2's exact
order before the two new tiles, so W5's block values over episodes
0..731 are identical to MA2's W (and to X's); W5's cell-state
trajectory matches MA2's W through E731 by construction. New tiles
use the continuing PRNG stream (frozen, deterministic).

Frozen seeds: SEED_B = 20261020, SEED_X = 20261021,
SEED_Y = 20261022, SEED_Z = 20261023 (all MA1/MA2 values),
SEED_W5 = 20261025 (flips).

## 3. Frozen metrics

All MA2 metrics carried over (RX, RY, RZ, RXF, RXB2, RWB2,
COSTXY, COSTXZ, TRIGX, TRIGY, DECLX, DECLY, B5a..B5g, DISTINCTD,
PARID, XDISJ, MARG, GENFAIL, PROTDEST), with PROTDEST now meaning
reseeds whose victim was protected AND unique (a violation under
any path), plus:

- R_WB4: first Block-B4 episode k (1..60) with |mean_Wa - 50| <= 1
  (0 if never).
- R_WB5: first Block-B5 episode k (1..60) with |mean_Wa - 95| <= 1
  (0 if never).
- TRIGW: triggers in W5; DECLW: declines in W5.
- REDSEEDW: redundancy-path reseeds in W5 (victim protected and
  redundant).
- BADRED: in-binary white-box tripwire: redundancy-path reseeds
  where the victim failed the redundancy predicate at reseed time
  (must be 0).
- Per trigger evaluation: episode, victim index with path marker
  (U = unprotected path, R = redundancy path, D = declined,
  X = tripwire: protected-unique victim, must never occur), and
  the 4-cell protection bitmask.

## 4. Mechanism-derived predictions (frozen)

W5's trajectory matches MA2's W through E731, so T1/T2 are MA2's:

- T1 (X/W5 E14, mask F=1): unprotected path, victim = cell 3
  (unprotected spare). R_X in [1, 99].
- T2 (X/W5 E675, mask F=13): unprotected path, victim = cell 1.
  R_XB2 <= 30, R_WB2 <= 30.
- T3 (W5 E734, Block-B4 onset, values {46..54}): the active cell
  (cell 0, distractor, mean 21) errs 25..33 three straight;
  consec hits 3 at B4k=3. Winner = cell 2 (err 26). Candidates:
  cells 1 and 3, both protected. Cell 1 (mean ~17..20) is
  redundant via cell 0 (|17-21| <= 10); cell 3 (mean 81) is
  redundant via cell 2 (|81-76| <= 10). Victim = cell 1, the
  lower-wpart redundant cell (WP ~19 < ~437). REDSEEDW = 1.
  Cell 1 reseeds as the 50-model. Predicted R_WB4 <= 15.
- T4 (W5 E794, Block-B5 onset, values {91..99}): the active cell
  (cell 1, 50-model) errs 41..49 three straight; trigger at
  B5k=3. Winner = cell 3 (err ~14). Candidates: cells 0 and 2.
  Cell 2 (mean 76) is redundant via cell 3 (|76-81| <= 10);
  cell 0 (mean 21) is UNIQUE (nearest protected mean is 50,
  distance 29 > 10). Victim = cell 2, the only redundant
  candidate. This is the discriminating case: the rule picks the
  redundant 80-duplicate over the unique distractor cell.
  REDSEEDW = 2. Predicted R_WB5 <= 15.
- TRIGW n=4 (two U-path, two R-path); DECLW = 0; PROTDEST = 0;
  BADRED = 0. The decline path is preserved but not exercised in
  W5 (honest boundary).
- The T3 tie-break (cell 1 vs cell 3, both redundant) is decided
  by the frozen lowest-wpart rule; the kill bar below is on the
  redundancy property, not the identity.

## 5. Frozen verdict mapping

- B1 COMMIT-ORDER: PASS iff this prereg commit (PREREG.md +
  NAMECHECK.md Step 0 only) strictly predates every implementation
  commit.
- B2 TOOLCHAIN: PASS iff safebin-only PATH throughout, Step 0
  recorded, zero forbidden-executable invocations.
- B3 DETERMINISM: PASS iff 3/3 runs byte-identical (sha256 recorded).
- B4 NOVELTY: PASS iff (a) 12 Block-D values pairwise distinct,
  (b) every episode's flip vector differs across conditions
  (same-episode X/Y/Z pairwise, plus W5 vs X/Y/Z over shared
  ranges), (c) per-condition per-block ones-fraction within fixed
  bands, with W5's B4 block in [28800, 43200] and B5 block in
  [61200, 72000] of 72000 flips.
- B5a RECOVERY (PRIMARY, kill bar): PASS iff 1 <= R_X <= 99.
- B5b BASELINE-REPLICATION: PASS iff R_Z >= 500.
- B5c COST: PASS iff COST_XY < 4690.
- B5d SHIFT-BACK: PASS iff 1 <= R_XB2 <= 30.
- B5e APPARATUS: PASS iff max etc <= 1200 and genfail = 0.
- B5f STREAM-VALIDITY: PASS iff PARID = 1 (values identical across
  conditions per episode/block, including W5 vs X over 0..731) and
  XDISJ = 1.
- B5g MANIPULATION: PASS iff the in-binary white-box assertion
  holds that cell 0 of X and of W5 both end Block D with
  (sum = 180, n = 9).
- B6 NO-RESEARCHER-RULE: PASS iff the learner fns' only
  cross-episode inputs are revealed values and tallies derived
  from them (means, wpart, wpsm, prot, redun); no episode-index
  or block-conditioned logic in learner code (audit by
  diff/grep; harness gen() is the experimenter as in MA1/MA2).
- B7 OPAQUE-IDS: PASS iff episode labels are E0001.. and a
  case-insensitive grep for the frozen 29-word list in ma3.zag
  returns empty.
- B8 NO-UNIQUE-DESTRUCTION: PASS iff PROTDEST = 0, i.e. no reseed
  in any condition destroyed a protected cell with no protected
  duplicator.
- B9 REDUNDANT-VICTIM (CO-PRIMARY, kill bar): PASS iff
  REDSEEDW = 2 AND BADRED = 0, i.e. the redundancy path fired
  exactly on the two designed 5th/4th-block triggers and every
  redundancy-path victim satisfied the redundancy predicate
  in-binary.

Headline verdict: REDUNDANCY-AWARE VICTIM CHOICE DEMONSTRATED iff
B5a PASS and B9 PASS with B1, B2, B3, B5e, B5f, B6, B7, B8 all
PASS and B5b PASS. B5b FAIL invalidates the comparison (verdict
becomes UNDECIDED, not a pass). No bar may be weakened after the
run; a broken prereg is amended transparently and re-frozen, never
reinterpreted.

## 6. Honest boundaries (frozen)

- What is learned are cell means, same level as MA1/MA2
  (L1/L2-ish). Not strategy invention, not L3. RDDM=10 joins the
  researcher-supplied constants; redundancy status, victim
  choice, and decline are learner-driven from revealed values.
- Mean distance is a proxy for shared regime knowledge, not a
  proof of it. Distinct regimes closer than RDDM would be
  conflated; W5 keeps separations >= 15. The (~21, ~17)
  distractor/B2 pair counts as redundant by the measure: by value
  they are one regime, and the architecture receives no block
  labels.
- The decline path is preserved for the all-unique-protected
  case but is not exercised in W5 (DECLW = 0 predicted); a
  follow-up W condition should force a decline alongside
  redundancy to test path selection between them.
- One W5 scenario, one frozen seed quintuple; MA1/MA2's four
  seeds are reused for direct comparability (frozen before
  MA1/MA2's outcomes existed).

## 7. Artifacts planned

- `ma3.zag`: frozen implementation (B6/B7 audited).
- `ma3_bin`: frozen compiled binary.
- `run1.txt`, `run2.txt`, `run3.txt`: 3/3 byte-identical outputs.
- `REPORT.md`: results and frozen verdict.
- `NAMECHECK.md`: build record (this file's Step 0 + build record).
