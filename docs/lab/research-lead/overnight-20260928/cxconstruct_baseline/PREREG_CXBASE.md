# PREREG: H-CAUSALEXP-CONSTRUCT Simple-Baseline Comparison (cxconstruct_baseline)

Date: 2026-09-30.
Status: FROZEN. Committed before any implementation, build, or run.
Lane: causal frontier, step 5 of 11-step promotion pipeline for
H-CAUSALEXP-CONSTRUCT (BUILD-PASS 7/7 at 48f2adc15, REPRODUCED step 4).

## 1. Objective

Test whether the experiment-construction capability of
H-CAUSALEXP-CONSTRUCT is trivially matched by simple baselines, or
whether the hypothesis-driven disagreement criterion adds real value.

The learner under test: given a hypothesis pair (delay-rule sets as
data), composes sequences from 4 generic primitives (S,W,OY,OZ) by
iterative deepening (depths 1..5, base-4 lexicographic order), simulates
each candidate under both hypotheses, selects the FIRST sequence with
disagreeing predictions, executes it exactly ONCE against the sealed
true world, and eliminates mismatching hypotheses. Builder result:
World A -> [S,W,OY] (len 3); World B -> [S,W,W,OY] (len 4); 4/4 configs
converge with 1 real-world execution each.

Key question: is this trivially matched by simple search, or does the
disagreement criterion add real value?

## 2. Reimplementation (sanity anchor)

I reimplement the generic simulator and the learner's construction
algorithm from the frozen prereg description (not by copying the
builder's source bytes), parameterized by an explicit hypothesis-pair
input so novel worlds can be tested. The simulator semantics are:
state (X,Z,Y,t,tX,tZ,tY); S sets X:=1,tX:=t; W does t:=t+1 then two
rule-application passes; OY/OZ observe. A rule (src,dst,delay) fires
when src==1 and t-t_src >= delay.

Variables: X=0, Z=1, Y=2. Actions: S=0, W=1, OY=2, OZ=3.

## 3. Worlds

Replication worlds (from frozen builder prereg):
- World A: H0=[(X,Z,2),(Z,Y,0)], H1=[(X,Y,1)]. Configs: true=H0, true=H1.
- World B: H0=[(X,Z,3),(Z,Y,0)], H1=[(X,Y,2)]. Configs: true=H0, true=H1.

Novel worlds (designed now, before implementation; learner never sees
them during replication):
- World C: H0=[(X,Z,4),(Z,Y,0)], H1=[(X,Y,3)]. Hand analysis: lengths
  1-4 agree ([S,W,W,OY] gives t=2: H0 needs >=4 -> 0; H1 needs >=3 ->
  0). Length 5 [S,W,W,W,OY] gives t=3: H0 -> 0, H1 -> 1. DISAGREE.
  Expected: constructive learner finds a length-5 discriminator.
- World D: H0=[(X,Z,2)], H1=[(X,Z,3)]. Only Z varies; OY is useless.
  Hand analysis: no depth<=3 sequence discriminates (need t-tX==2 with
  an observe; depth 3 maxes at t=1 with X set, or t=2 without X).
  [S,W,W,OZ] (len 4): t=2, H0 Z=1, H1 Z=0. DISAGREE. Expected:
  constructive learner finds an OZ-based discriminator at length 4,
  proving it is not hardcoded to OY.

Worlds C and D test whether the construction machinery generalizes to
novel hypothesis pairs (different delays, different observed variable).

## 4. Baselines (exact procedures)

All baselines use the same generic simulator for prediction and the
same sealed world_step for real execution. A baseline "converges" on a
config iff after its real-world execution(s), exactly the true
hypothesis survives elimination (predicted outcome == real outcome).

B1 RANDOM+ELIMINATE (density test):
For each of the 4 replication configs, run 200 trials. Each trial:
seeded LCG generates a random length L in 1..5 and random actions;
resample until the sequence has at least one observe action. Execute it
once against the true world (1 real-world execution). Simulate under
both hypotheses; eliminate mismatches. Record: correct-converge
(only true survives) vs ambiguous (both survive). The true hypothesis
always matches reality, so incorrect-converge is impossible by
construction; the rate measures the density of discriminating
sequences. LCG: s = (s*1103515245+12345) mod 2^31, seed=12345, actions
from high bits mod 4, fresh subsequence per trial.

B2 SINGLE-PRIMITIVE EXHAUSTIVE (hand-proof check):
For each world (A,B,C,D), simulate each of the 4 single primitives
under both hypotheses. Confirm all pairs agree (no discrimination).
This computationally re-verifies the frozen K-CX1 hand proof and
extends it to the novel worlds.

B3 GREEDY SHORTEST-FIRST TRIAL-AND-ERROR:
For each replication config: for d=1..5, for each sequence in
lexicographic order with at least one observe action: EXECUTE it
against the real world (counting each as a real-world execution);
simulate under both hypotheses; if exactly one hypothesis survives,
stop and record the execution count. This is "shortest-first" without
the simulation pre-filter: it pays real-world cost for every
non-discriminating sequence. Compare execution count vs the learner's
exactly-1.

B4 MEMORIZATION LOOKUP (generalization test):
Build a lookup table from the replication results: key=(hypothesis
pair) -> sequence. Train on Worlds A and B: {(H0A,H1A)->[S,W,OY],
(H0B,H1B)->[S,W,W,OY]}. Test on Worlds C and D: look up the novel
hypothesis pair. A pure lookup has no entry -> emits NO-SEQUENCE
(fail). Report 0/2 generalization. Additionally verify that the
CONSTRUCTIVE learner (same code as replication) solves C and D,
proving the machinery generalizes where the table cannot.

## 5. Validity bars (numbered; all must pass for the comparison to be valid)

- P-CB1 (replication sanity): my reimplemented learner constructs
  [S,W,OY] for World A and [S,W,W,OY] for World B, and converges 4/4
  replication configs with exactly 1 real-world execution each. If
  this fails, my reimplementation is wrong and all baseline numbers
  are void.
- P-CB2 (B2 confirms): all 4 primitives agree under both hypotheses
  in all 4 worlds (A,B,C,D): 16/16 agree per world. Extends K-CX1.
- P-CB3 (B1 executed): 200 trials per replication config complete;
  report exact correct-converge counts (4 numbers).
- P-CB4 (B3 executed): greedy trial-and-error converges on all 4
  replication configs; report exact real-world execution counts
  (4 numbers).
- P-CB5 (B4 + generalization): lookup table has entries for A,B and
  misses on C,D (0/2); constructive learner converges on C (both
  true-hypothesis configs) and D (both configs): 4/4 novel configs.
- P-CB6 (determinism): 3 runs, byte-identical (cmp), exit 0.
- P-CB7 (purity): pure Zag (znc build; bash/grep/cmp/md5sum analysis
  only); zero Python invocations; zero em dash bytes in committed docs.

## 6. Verdict criteria (frozen)

Comparison dimensions: correctness (converge to true hypothesis),
efficiency (real-world executions), generalization (novel pairs).

Learner reference performance: 4/4 correct, 1 execution/config,
generalizes (P-CB5).

- BASELINE-WINS: any baseline achieves 4/4 replication correctness
  with <=1 real-world execution per config AND 4/4 novel-world
  generalization. (Would mean the capability is trivial.)
- BASELINE-MATCHES: a baseline matches 4/4 correctness but uses
  moderately more executions (2-3) or matches correctness+efficiency
  but fails generalization; i.e., competitive on one dimension only.
- BASELINE-LOSES: every baseline is strictly worse on at least one
  dimension with no compensating win: B1 converges at low rate
  (density < 25%), B2 at 0%, B3 needs >=4 executions per config,
  B4 generalizes 0/2 while the learner generalizes 4/4.

The verdict is read off the numbers against these frozen thresholds.
No post-hoc redefinition.

## 7. Honest limitations (frozen)

- Worlds are synthetic and tiny (3 binary variables, 2 hypotheses).
- B1's density depends on the chosen sequence distribution (uniform
  over lengths 1..5 with observe); a different distribution gives a
  different density. The comparison is against THIS natural
  distribution.
- B3 is deliberately naive (no simulation); it isolates the value of
  the simulation pre-filter, not the value of search order.
- B4 tests pure lookup; a nearest-neighbor variant might do better,
  but the frozen question is specifically about a learned
  (world->sequence) table.
- This is step 5 (baselines) of the promotion pipeline. Adversary,
  OOD, ablation, transfer, red team, governance remain.

## 8. Amendments

None. If needed, committed as a separate file before the result, with
the changed section quoted.
