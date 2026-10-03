# REPORT: Adaptive (Learner-Owned) PLEN

**Verdict: INCOMPLETE** (K4 FAIL; K1-K3, K5-K12 all PASS).
Prereg `c06ee6d01` strictly precedes implementation. 3/3
byte-identical, sha256
`3205ebcc78b78bc515efbf57e3cb73881369ec9d93cde051f079d5f90c6d966e`.

## Question

COGOPS-PARSIMONY showed parsimony pressure works (P-FULL discovers
the exact minimal 6-instruction form at ~2.3x/2.8x trial cost) but
left PLEN=3 as a researcher-owned hand-derived constant. This lane
makes PLEN learner-owned: it lives in learner cell 2370, starts at
0 (no pressure), and moves only from experienced consequences.
Preregistered questions: (1) can the learner discover an
appropriate PLEN from 0? (2) does adaptive PLEN keep the safety
property (never trade working for shorter-broken)? (3) how does
adaptive compare to fixed PLEN=3 on trials, final length, and
revisability?

## What was built

`ap.zag` (pp.zag plus the adaptive mechanism; pure Zag, pinned
znc, safebin): the hardcoded 3 in `pop_fit`/`off_beats_pop`
becomes `plen_of(S)` (3 for pmode!=3, learner cell 2370 for the
new pmode 3 = A-FULL arm). Three researcher-authored update
triggers move the learner-owned value (floor 0, cap 6, steps
of 1); the rule is fixed, the VALUE and trajectory are the
learner's:

- why=avail (per-generation, at most 0->1, provably): plen==0
  and a shorter working body (raw>=850) exists that composite
  selection ignores -> plen=1.
- why=compress (post-adopt): compression just proved shortening
  is free (strict deletions > 0) -> plen+1.
- why=regress (post-adopt): adopted raw replay regressed vs the
  previous adoption -> plen-1 (skipped when regressed: safety
  first).
- Inversion diagnostic (reporting only, no plen change): counts
  composite comparisons where the winner has strictly lower raw
  replay than the loser (tournament, elitism, displacement).

Adopt bars stay on RAW replay (>=850); compression
keep-criterion stays raw non-decrease. Three arms, one binary,
identical per-arm RNG seeds: arm 0 = A-FULL (adaptive),
arm 1 = F-FULL (fixed 3, in-binary PARSIMONY replication),
arm 2 = NP (LB1-exact).

## Results

**Q1: YES -- the learner discovered PLEN=2 from a 0 default,
entirely from experienced evidence.** Trajectory (the only two
PLEN-ADJ lines in 3 identical runs):
```
PLEN-ADJ plen=1 why=compress   (after create: 11->6 proved free)
PLEN-ADJ plen=2 why=compress   (after revise: 10->6 proved free)
```
The why=avail trigger never fired (no generation ever held
coexisting passers of different lengths at plen 0); why=regress
never fired (adoptions: 1000 then 1000). plen_inv_tot=0 (at
plen<=1 inversions are rare/impossible; most selection ran at
plen 0 where composite==raw). Honest note: the discovery was
driven by post-hoc compression evidence, not in-loop selection
adaptation -- the per-generation trigger's precondition never
materialized, a design weakness (see follow-ups).

**Q2: YES -- safety held.** A-FULL's final body is byte-identical
to F-FULL's (and to PARSIMONY's hand-optimal form):
```
SET R0,6 / MATCH R7,R0->R1 / SET R4,1 / READF R1,R4->R5 /
SET R6,2 / YIELD R6,R5
```
final replay 1000, 6 instructions (K12). No adopted body in
A-FULL ever traded raw replay for length (adopt bars on raw;
compression raw-non-decrease); the inversion diagnostic recorded
0 harmful events.

**Q3: MIXED -- same outcome as fixed-3, but slower revision
(K4 FAIL, the informative result).**

| arm | create | revise | final | compress | plen |
| A-FULL (adaptive) | 212 | 284 (+368 failed attempt, no adopt) | 6 instr / 1000 | 9 strict | 0->2 |
| F-FULL (fixed 3) | 212 | 188 | 6 instr / 1000 | 7 strict | 3 (constant) |
| NP (none) | 92 | 68 | 11 instr / 1000 | 0 | 0 |

- Create: identical trial cost (212 = 92 + 10 refinement gens).
  At plen 0 the adaptive create adopted 11 instr (like NP);
  selection pressure contributed nothing (avail never fired);
  compression did all the shortening (11->6 vs P-FULL's 9->6).
- Revise: A-FULL needed TWO attempts: ep 474 ran the full
  30-generation budget (368 trials) with best=0 (no passer
  found, no adopt), ep 499 adopted in 284 trials (10->6).
  F-FULL adopted first attempt in 188. K4
  (revise_trials < create_trials within-arm) fails: 284 > 212
  (true revise-phase cost 652 vs 188).
- Mechanism (honest, with confound stated): the adaptive ramp
  leaves the revise search under-pressured -- plen is still 1
  during revise-search (it becomes 2 only after
  revise-compression), vs 3 for fixed. Weaker pressure retains
  longer variants, diluting the targeted single-slot etype fix
  (imm 5->6) across more slots; the first attempt exhausted the
  budget without sampling it. CONFOUND (preregistered arms share
  seeds but diverge in RNG consumption, so arm differences mix
  treatment with RNG path): the second attempt at the same
  plen=1 succeeded in 284, so the first-attempt failure may be
  partly RNG-path artifact; the 284-vs-188 gap is the cleaner
  comparison and is still 1.5x. A matched-RNG follow-up is
  needed to discriminate (see follow-ups).

## Kill bars

- K1 PARSEFFECT (A-FULL 48B <= 64B, < NP 88B): 1.
- K2 SUCCESS-PRESERVED (19/19+23/23; 19/19+22/23; 19/19+23/23): 1.
- K3 REPLICATION (NP 92/88B; F-FULL 212/188/48B, create_best
  1000 -- experimental lines byte-identical to PARSIMONY
  P-FULL): 1.
- K4 REVISE-PARSIMONY (A-FULL revise 284 < create 212): **0**.
  Informative FAIL (see Q3).
- K5 VS-RESEARCHER (1000/100/1000): 1.
- K6 OPEN-FORM (enum 0, trials>=20, all arms): 1.
- K7 DETERMINISM: 1 (sha256 match x3).
- K8 NO-MODES: 1 (build.sh guards).
- K9 COMPRESS-CAUSAL (9 strict dels, A-FULL): 1.
- K10 RETIRE (op3 retired all arms, slot5 not): 1.
- K11 PLEN-ADAPTED (end 2 in [1,6], adj 2 >= 1): 1.
- K12 PLEN-SAFE (final 1000, 48B): 1.

## SUF analysis (honest)

L2, not L3. Researcher-owned: ISA, interpreter, trial/replay
machinery, graded shaping, etype-frequency bias, eight generic
operators, triggers, adopt bars, budgets, composite-fitness form,
compression operator + keep-criterion, refinement length, AND the
PLEN adaptation rule itself (the three triggers, floor/cap/step,
initial 0). The learner did not invent parsimony or the
thermostat. Learner-owned: every body byte, policy contents,
selection survivors, kept deletions, revision/retirement
decisions, AND NOW the PLEN value at every instant -- 0->1->2,
each step caused by its own experienced evidence (free shortening
proved twice by compression). What is genuinely new vs
PARSIMONY: the coefficient is no longer a researcher constant.
What is NOT new: in-loop adaptation (the per-generation trigger
never fired); the learner's "discovery" was post-hoc.

## Follow-ups

- Matched-RNG revise comparison: rerun the revise search at
  fixed plen=1 vs plen=3 from the same seed body and RNG state
  to discriminate systematic pressure effect from RNG-path
  artifact in the 284-vs-188 gap and the failed first attempt.
- Stall-triggered pressure: raise plen when the search stalls
  (no passer for N generations) instead of only post-adopt;
  test whether in-loop adaptation fixes the K4 revise lag.
- Widen the why=avail precondition (it never fired): trigger on
  length variance among near-passers, not just coexisting
  passers, and measure whether selection-time adaptation engages.
- Second law change (6->7): does plen keep ratcheting, and does
  the revise lag compound?
