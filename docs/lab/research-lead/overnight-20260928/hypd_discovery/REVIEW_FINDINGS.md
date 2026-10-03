# Hypothesis D Search Review: Findings

Review of the T3 parity miss in Hypothesis D v2 (MAP-Elites program discovery).
Prereg: `2c4c58e80` (REVIEW_PLAN.md). Implementation: `review.zag` (this directory).
Result: **HYPD-REVIEW-COMPLETE**. T3 miss status: **EXPLAINED**.

All analyses are pure Zag, deterministic 3/3 byte-identical
(md5 `745f81951d3c8f6fd1abceb3a8dbef5f` across REVIEW_RAW_1/2/3.txt).

## R0. Fidelity audit (review spec vs implementation)

The review spec (section 4 of `18be93c3e`) describes D as: archive indexed by
behavioral descriptor (discretized output vector on train episodes); candidates
by single-op mutate (append/replace/delete, deterministic order); retain iff
niche empty or exact-match score beats niche elite; fixed eval budget; per-niche
retention, no global top-K.

Committed implementation (`2500fd02b:hyp_d_v2.zag`) matches on every point:
- Niche = `(length_bucket, score_norm, behavior_hash)` where `length_bucket =
  min(len,12)`, `score_norm = (score*16)/n`, `behavior_hash` = rolling trit
  hash mod 256 over train outputs in episode order (trit 2 if o>0, 1 if o==0,
  else 0). Verified: my independent Zag recomputation of Q3's niche equals the
  logged value (13249 = 13249).
- Mutation: per-niche cyclic counter over M = nt + (nt+1)*pl templates
  (nt=31 full-VM); mi<31 append template mi; next 31*pl replace; rest delete.
  Template map verified: t 0..18 PUSH(t-9); 19 IN0; 20 IN1; 21 ADD; 22 SUB;
  23 MUL; 24 DIV; 25 MOD; 26 NEG; 27 DUP; 28 DROP; 29 SWAP; 30 OVER.
- Retention: `if niche empty -> insert; else if score > elite score -> replace`.
  Note: same niche implies same output vector implies same score, so the
  replace branch is effectively dead; retention is insert-on-empty-niche.
- Budget: 1,000,000 evals per task. T3 ran the full budget (EVALS 1000000).
- No global ranking. Round-robin parent selection over occupied niches.

One implementation detail not in the spec but load-bearing for the findings:
carried programs from the previous task are re-evaluated on the new train set
and inserted SILENTLY (no I-lines; first logged I-line is eval=24971 while
carried evals are 1..3901). CARRY_IN=3901, CARRY_DROPPED_INVALID=0 on T3.

## R1. Theory check: the 8-op solution is real

P8 = `[IN0,IN1,ADD,PUSH 2,MOD,PUSH 1,SWAP,SUB]`, scored by an independent
straight-line full-VM evaluator in `review.zag` on the frozen T3 episodes:
- Train (25 episodes, a,b in 0..4): **25/25**.
- Held-out (39 episodes, a,b in 0..7 excluding the 0..4 square): **39/39**.

The review's predicted solution is correct. The miss is a search failure,
not a theory failure.

Chain program scores (train): P5 `[IN0,IN1,ADD,PUSH 2,MOD]` 0/25;
P6 (+PUSH 1) 13/25; P7 (+SWAP) 0/25; PA `[IN0,IN1,ADD,PUSH 2]` 0/25;
Q3 `[IN1,IN0,ADD]` 0/25; Q4 `[IN1,IN0,ADD,PUSH 2]` 0/25.
Niches: P5 21925, P6 28322, P7 30629, PA 17570, Q3 13249, Q4 17570, P8 38990.

## R2. Broken link: the chain never completed

Insertion presence in the committed T3 log (12,863 I-lines):
- P5, P6, P7, P8, PA, Q4: **0 insertions each**.
- `[IN0 IN1 ADD]` (len 3): 0. `[IN0 IN1]` (len 2): 0.
- Deepest correct prefix ever inserted: Q3 = `[IN1,IN0,ADD]` (len 3, score 0),
  inserted once at eval=79426, niche 13249.

The search reached the IN1/IN0/ADD region (best program
`[PUSH:9 IN1 IN0 SUB MOD]`, 20/25) but never assembled the PUSH:2/MOD prefix
chain. Chain A (via `[IN0 IN1]`) never started. Chain B (via `[IN1]`, which WAS
in the archive from eval 28786) progressed to Q3 then stalled permanently.

## R3. Niche audit: never generated vs blocked

For each chain niche, max score among T3 insertions at that niche:
- 21925 (P5): empty. Never generated.
- 28322 (P6): empty. Never generated.
- 17570 (PA/Q4): empty in I-lines. Never generated via main loop (see R5).
- 38990 (P8): empty. Never generated.
- 30629 (P7): occupied by `[PUSH:-4 IN1 IN0 PUSH:-3 DIV ADD ADD]` (score 1,
  eval 678549). P7 scores 0 < 1: blocked even if generated.

So the break is at GENERATION (not eviction), except P7 which is doubly blocked.

## R4. Dilution arithmetic: deep serial chains are infeasible

To complete the solution via append chains, specific (parent niche, counter
value) alignments must fire in sequence. Template indices needed:
ADD=21, PUSH:2=11, MOD=25, PUSH:1=10, SWAP=29, SUB=22, IN0=19.

- Chain A (6 links via `[IN0 IN1]`): needs selections 22,12,26,11,30,23 = 124
  niche-selections.
- Chain B (7 links via `[IN1]`): needs 20,22,12,26,11,30,23 = 144.

Each niche-selection costs one round-robin period (~occn evals; occn grows
3901 -> 11930):
- Optimistic (occn frozen at 3901, parents instant): A=483,724, B=561,744 evals.
- Realistic (avg occn ~8000-9500): A=992,000, B=1,368,000 evals vs 1M budget.

Chain B's realistic cost EXCEEDS the entire budget. The median niche gets ~125
selections per run but its mutation cycle is M=191 (len 5), so each niche
covers only ~65% of its single-mutation neighborhood once. D can climb local
gradients but cannot reliably execute 6-7 deep serial mutation plans.

## R5. Carried niche blocking: the hard wall (key finding)

T2's final archive (carried into T3 silently) contains 11 constant-2 programs:
`[PUSH:-9 x k, PUSH:2]` for len k+1 = 2..12. On T3's episodes these output
constant 2. Their T3 niches (computed in `review.zag`):

- len 4: niche **17570** = Q4's niche exactly (blocked=1 verified).
- len 2: 8866; len 3: 13218 (same pattern).

Consequences:
1. Q4 = `[IN1,IN0,ADD,PUSH:2]` (the required continuation of Q3) maps to niche
   17570, which is PERMANENTLY occupied by carried
   `[PUSH:-9 PUSH:-9 PUSH:-9 PUSH:2]`. Same output vector -> same score (0) ->
   the strictly-greater retention rule can never displace it. **Q4 is
   unreachable for the entire run, regardless of eval budget.**
2. This explains the run-wide empirical anomaly: ZERO programs ending in
   PUSH:1/PUSH:2 at any length 4..10 on T3 (vs hundreds ending in ADD), while
   T2 (whose carried set lacked these blockers) had 11. The stepping-stone
   niches the solution chain needs were pre-poisoned by the previous task's
   junk.
3. Chain B therefore did not just "get unlucky": it hit a structural wall.
   Q3 was inserted at eval 79426 with 920,574 evals remaining, but its
   continuation was impossible from that moment.

## Synthesis: why D missed T3 parity

Three compounding mechanism failures, all verified:
1. **Dilution** (R4): round-robin over ~4k-12k niches with per-niche cyclic
   counters cannot execute the 6-7 deep serial mutation chain within 1M evals.
2. **Carried niche poisoning** (R5): the cross-task carry-over silently
   occupies the exact niches needed as stepping stones (constant-output
   niches), and strict-improvement retention makes the blockade permanent.
   The solution is not just unlikely but unreachable via the natural chains.
3. **No recovery**: the search climbed a different gradient to 20/25
   (`[PUSH:9 IN1 IN0 SUB MOD]`) but no single-mutation neighborhood of the
   archive contains a path to P8.

Falsification checks: D-F1 did not fire (T0 solved, control valid). F-TRICK
silent on T3 (no jumps in full-VM programs by construction). F-SMUG clean
(PVM_TRAPS 0). The miss is owned by D's search mechanism, not by controls.

## D vs the other hypotheses

A and C are FALSIFIED (commits `21d838921`, `aae06bac6`). B is under
construction by a parallel worker; no verdict yet. D is the only surviving
discovery hypothesis with a complete v2 run, and this review shows its T3
failure is structural (dilution + carried poisoning), not noise. Any future
D-variant must address at minimum: (a) serial-chain selection budget under
round-robin, and (b) carried-program niche poisoning of stepping stones.

## Kill bars

- K1 (plan before analysis): REVIEW_PLAN.md frozen as `2c4c58e80` before
  `review.zag` was written. PASS.
- K2 (all analyses run; controls re-verified): R0,R1,R2,R3,R4,R5 run;
  D-F1/F-TRICK/F-SMUG re-verified from committed logs. PASS.
- K3 (pure Zag; deterministic 3/3; no em dashes): `review.zag` is pure Zag
  (no Python anywhere); 3/3 byte-identical runs; this document uses the
  shell dash check. PASS.

## Recommended next step

Freeze a D-v3 prereg whose kill bars explicitly test the two mechanism
fixes: (1) a selection policy that concentrates budget on promising niches
instead of uniform round-robin (attacking R4 dilution), and (2) a carry-over
rule that does not let previous-task programs permanently block new niches
(e.g., carried programs compete on the new task's score rather than holding
niches by occupancy; attacking R5 poisoning). The prereg should predict T3
SOLVE only if both fixes are in place, with the R5 blockade (niche 17570) as
an explicit falsification check.
