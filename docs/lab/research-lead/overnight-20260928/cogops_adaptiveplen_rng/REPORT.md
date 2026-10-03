# REPORT: Matched-RNG follow-up to COGOPS-ADAPTIVEPLEN K4 FAIL

**Verdict: INCOMPLETE (negative result).** MR1 FAIL, MR2 FAIL;
MR3 PASS, MR4 PASS; MR5 partial (binary RNG-match 8/8 PASS;
the `cur==100` prereg expectation was erroneous -- see MR5 note).

Prereg `d8bf929f9` strictly precedes implementation. 3/3
byte-identical, sha256
`70bd0f42decf914bd380ebbc8e7c55e0dbf25168a4f0f41774f786d086f2c1c0`.

## Question

COGOPS-ADAPTIVEPLEN reported INCOMPLETE on an informative K4 FAIL:
adaptive revise cost 284 trials plus one failed 368-trial attempt
(best=0, no adopt) vs fixed-3's 188. Hypothesized mechanism: the
adaptive ramp leaves revise-search under-pressured (plen still 1
during revise vs 3 fixed), retaining longer variants and diluting
the single-slot etype fix (imm 5->6). Preregistered confound: arms
shared RNG seeds at arm start but diverged in RNG consumption before
revise, mixing treatment with RNG path.

This lane ran the preregistered matched-RNG discrimination:
8 RNG pairs; within each pair, a revise search at fixed plen=1 (P1,
the adaptive arm's exact revise-phase state: pmode 3, cell 2370=1)
vs fixed plen=3 (P3, PARSIMONY-exact), from the same seed body, the
same learner state, and binary-verified identical RNG stream states
at revise start. The ONLY difference between arms is the plen
coefficient in the composite fitness.

## Result: the K4 gap does NOT replicate -- stronger, the plen
treatment is behaviorally inert

| pair | P1 trials | P3 trials | P1 best/ad | P3 best/ad | P1 firstpass | P3 firstpass | P1 meanlen | P3 meanlen |
| 0 | 152 | 152 | 871/1 | 871/1 | 1 | 1 | 8.86 | 8.86 |
| 1 | 164 | 164 | 914/1 | 914/1 | 2 | 2 | 6.31 | 6.31 |
| 2 | 368 | 368 | 0/0 | 0/0 | 31 | 31 | 6.05 | 6.05 |
| 3 | 368 | 368 | 0/0 | 0/0 | 31 | 31 | 5.59 | 5.59 |
| 4 | 368 | 368 | 0/0 | 0/0 | 31 | 31 | 7.89 | 7.89 |
| 5 | 140 | 140 | 1000/1 | 1000/1 | 0 | 0 | 6.28 | 6.28 |
| 6 | 332 | 332 | 1000/1 | 1000/1 | 16 | 16 | 10.69 | 10.69 |
| 7 | 320 | 320 | 1000/1 | 1000/1 | 15 | 15 | 6.83 | 6.83 |

(cost = trials if adopted else 369; firstpass 31 = no passer in
30 gens; meanlen = mean over generations of mean member length.)

Not only are the trial counts identical: the per-generation GEN
trajectories (sumlen, bestraw, fixcount) are byte-identical between
P1 and P3 in all 8 pairs (verified by direct diff of the GEN
sequences: 11-30 generations each, all identical). The plen=1 vs
plen=3 treatment produced not a single divergent selection event
across 8 pairs x up to 30 generations x 12 offspring x tournament
selection.

## Mechanism analysis: why the treatment cannot bite

Exhaustive audit of every code path where plen affects behavior
(grep over plen_of / cell 2370): within this driver, plen is read
ONLY by the composite fitness `fit = raw - plen*nin` in pop_fit
(tournament, best-passer, final-best) and off_beats_pop (offspring
displacement). plen_adapt is a provable no-op at plen=1 (returns
when cell 2370 != 0); the post-adopt plen updates in
try_create/try_revise are not called by this driver; all other
2370 reads are reporting/init.

Selection depends only on the ORDERING induced by fit. Two facts
make the plen=1 vs plen=3 orderings coincide here:

1. Within equal raw replay, shorter always wins under BOTH plen
   values (the penalty is monotonic in length either way).
2. Replay scores are quantized into coarse tiers (per-snapshot
   scores in {0,100,150,400,1000}); in these runs, raw differences
   between compared members always dominated the length penalty
   (max plen-3 swing 3x15=45 over the 16-instruction cap), so no
   cross-tier comparison ever flipped between plen=1 and plen=3.

A flip is arithmetically possible in principle (averaged replays
can differ by <45), but empirically zero flips occurred in
8 pairs. The hypothesized mechanism -- weaker plen-1 pressure
retaining longer variants and diluting the fix -- cannot operate
through the selection path as implemented: the pressure
coefficient changes no selection decision.

## What, then, explains the original 284-vs-188 gap?

By elimination, the original gap came from pre-revise divergence,
not revise-phase pressure:

1. Divergent RNG stream states at revise start (the preregistered
   confound): different draw sequences drive different search
   paths. Note pairs 2/3/4 here reproduce the original's failed
   368-trial attempt (best=0, budget exhausted) as a property of
   the pair's RNG path -- affecting both arms identically.
2. Divergent accumulated learner state: A-FULL's policy, IMMC
   etype bias, snapshot ring, and graft sources were shaped under
   the plen 0->1 create history; F-FULL's under constant plen=3.
   Different mutation sampling at revise start changes revise
   cost through the OPERATORS, not through selection pressure.

Both are history/RNG effects, not a revise-phase pressure effect.
The K4 FAIL's hypothesized mechanism is disconfirmed; the K4 FAIL
itself is attributed to RNG-path/history artifact.

## Kill bars

- MR1 REPLICATE: P1 cost > P3 cost in 0/8 pairs (needed >=6/8);
  mean cost ratio 1.00 (needed >=1.25). **0**.
- MR2 MECHANISM: (a) meanlen P1>P3 in 0/8 (needed >=6/8);
  (b) firstpass P1>P3 in 0/8 (needed >=6/8). **0**.
- MR3 DETERMINISM: 3/3 byte-identical (sha256 above). **1**.
- MR4 GUARDS: build.sh guards (no python, no `as *i32`, no
  _MODE, opcodes exactly 1..8, no `while.*!(`, single main). **1**.
- MR5 SETUP-SANITY: binary RNG-match self-check 8/8 pairs **1**;
  seed-body cur replay == 100 in 16/16 runs: **0 as literally
  preregistered** (actual: cur = 142/142/200/175/100/100/100/100
  across pairs, matched within every pair). NOTE (transparent):
  the prereg expectation was erroneous -- cur necessarily varies
  with the pair-specific snapshot ring (different env seeds give
  different world instances). The substantive invariant holds
  16/16: the seed body is unfixed everywhere (cur in [100,200],
  all far below any passing score) and matched within each pair,
  so the adopt bar (best > cur+150) is apples-to-apples. This is
  reported as a prereg-expectation error, not a pass; it does not
  touch the verdict-driving bars. No rerun: forcing cur==100
  would mean fixing one snapshot ring across pairs, reducing
  generality for zero inferential gain.

OVERALL per the frozen mapping (MR1 FAIL): the K4 gap does not
replicate under matched RNG -> **INCOMPLETE (negative result)**.

## SUF analysis (honest)

L2, not L3 -- same split as the parent lane; this lane adds no new
learning claim, only a causal discrimination. Researcher-owned:
everything in ap.zag plus the matched-RNG driver design, pair
seeds, and the fixed-plen proxy. What is genuinely new: a
mechanism-level disconfirmation -- the adaptive ramp's revise lag
is not caused by revise-phase selection pressure. What is NOT
claimed: this does not test the full adaptive 0->1->2 trajectory
(plen HISTORY effects on policy/IMMC remain untested as a causal
factor), and the inertness result is scoped to this revise setup
(quantized replay, 16-instruction cap); a finer-grained replay
could let the coefficient bite.

Standing results of COGOPS-ADAPTIVEPLEN are unaffected: the
learner-owned PLEN discovery 0->1->2 and the safety property
(byte-identical minimal 6-instruction body, replay 1000) stand as
reported. Only the K4 mechanism hypothesis is retired.

## Follow-ups

- Causal test of plen HISTORY (not plen value): matched-RNG
  revise where the two arms differ ONLY in pre-revise plen
  history (policy/IMMC shaped under plen 0->1 vs constant 3),
  then revise both at the same plen with the same RNG state.
  Discriminates operator-shaping effects from pure RNG luck in
  the original gap.
- Make pressure bite: finer replay granularity or a larger
  length cap so the plen coefficient can actually flip
  selections; test whether adaptive plen then helps or hurts
  revise, and whether the ramp speed matters.
- The no-adopt phenomenon (pairs 2/3/4: 30 gens, best=0) as a
  search-luck object: what predicts budget exhaustion, and does
  any learner-owned signal anticipate it (stall-triggered
  pressure, proposed in the parent lane's follow-ups)?
