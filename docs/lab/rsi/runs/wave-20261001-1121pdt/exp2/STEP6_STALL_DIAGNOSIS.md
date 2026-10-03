# H-EXP2 v2 step 6: B=2 stall diagnosis (wave-20261001-1121pdt)

## Status

DIAGNOSIS, not a verdict. No frozen prereg exists for the step-6
alternative-explanation attack, so nothing is adopted or killed here.
The evidence analyzed is the 08:21 wave's committed sweep
(docs/lab/rsi/runs/wave-20261001-0821pdt/exp2/sweep_out/sweep.tsv and
rounds logs): the FROZEN expseq_bin (wave-20261001-0221pdt, the H-EXP2
v2 BUILD-PASS binary) run against 16 adversary-authored laws (all
(A,B) pairs, A,B in 0..3). Result: 12/16 IDENTIFIED; the four B=2 laws
((0,2),(1,2),(2,2),(3,2)) all STALLED at round 6.

## Diagnosis: law-family identifiability property, NOT a baseline artifact

The stall is proven to be a property of the law family under the fixed
6-action interface. Proof by behavioral equivalence, checked against
both the hypothesis model (altexp.zag hyp_step) and the true world
(expworld.zag, lines 82-87, identical dynamics):

1. The state is (t,p,l) with t in {0,1,2}, p in {0,1}, l in {0,1}.
2. Action 2 (pressurize) sets p:=1 UNLESS blocked, where blocked iff
   (t==A or A==3) AND (l==B or B==3).
3. Under B=2: l is always 0 or 1, so l==B is never true, and B==3 is
   false; hence the block condition is never true and action 2 always
   sets p:=1, for EVERY hypothesis with B=2 and for the true law.
4. Actions 0,1,3,4,5 never reference A or B in either implementation.

Therefore hypotheses (0,2),(1,2),(2,2),(3,2) are behaviorally identical
under every action, hence under every probe of any length. The
parameter A is unidentifiable when B=2. No probe enumeration of any
length cap could discriminate the four survivors; the length-4 cap
(1554 candidates) is irrelevant to the stall.

The mechanism's behavior was correct in the only sense available: by
round 6 it had eliminated every B!=2 hypothesis (identifying the
identifiable part, B=2) and stopped when no probe could reduce the
survivor set further, rather than oscillating forever or
misidentifying. STALLED is the honest terminal state for a
behaviorally-equivalent survivor class.

## Consequence for the step-6 attack design

Any future step-6 prereg must state its identifiability assumptions up
front: behaviorally-equivalent hypothesis classes (like the B=2
A-quadruple) cannot count as attack failures, because no mechanism,
however guided, can distinguish them through the fixed action
interface. The honest attack metric is identification of the
identifiable structure (here: B=2), which the frozen mechanism
achieved 4/4. A prereg that scores STALLED-on-B=2 as a kill would be
measuring the world's unidentifiability, not the mechanism's weakness.

## Interim alt-baseline evidence (08:21 wave, recorded, no verdict)

The 08:21 lane also ran dumb baselines (altexp.zag) against the sealed
v2 worlds W-A and W-B (no frozen prereg; evidence only):

- first (first probe in enumeration order scoring >= 2; keeps the
  informativeness test, drops argmax maximization): IDENTIFIED W-A at
  round 5 and W-B at round 6.
- enum (round-robin, zero scoring): BUDGET-EXHAUSTED on both.
- rnd (deterministic LCG, no scoring): BUDGET-EXHAUSTED on W-A,
  IDENTIFIED W-B at round 11 (lucky draw).
- fixed (trivial open-loop script): BUDGET-EXHAUSTED on both.

Reading (not a verdict): the informativeness filter (score >= 2) plus
the shared pruning machinery suffices to identify both sealed worlds;
the argmax maximization is not load-bearing for W-A/W-B (expseq used
4 and 5 rounds; "first" used 5 and 6). Pure round-robin and the
trivial script fail. This weakens any claim that v2's guided
maximization is the active ingredient, and strengthens the case that
the pruning machinery plus any splitting probe does the work. The
frozen step-6 prereg (queued) should make this comparison its central
question with the identifiability caveat above.

## Queued

Freeze a step-6 alternative-explanation prereg (with the
identifiability assumption stated and the first-vs-argmax comparison
as the central question) before any adoption verdict.
