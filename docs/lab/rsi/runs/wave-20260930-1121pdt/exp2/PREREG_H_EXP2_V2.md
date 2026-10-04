# PREREG H-EXP2 v2: sustained active experiment construction

Wave: wave-20260930-1121pdt. Worker: EXP2. Date: 2026-09-30.
Provenance: NEW (this wave). Inherits the H-EXP2 v1 result (overnight
20260928, one-shot discriminating-experiment selection, bounded) only as
motivation: v1 selected a single experiment from a pre-ambiguous state and
left the execution step out of scope. This v2 closes the loop and hardens
the goal: the learner must choose informative experiments over a SEQUENCE,
executing each against a continuing hidden world, pruning its hypothesis
set from observed trajectories, and identifying the world's causal law
within a probe budget. DDES t*=0 is being repaired in parallel; this
mechanism is self-contained and does not depend on it.

## Goal (harder sustained)

A learner faces a continuing hidden world with unknown causal law L*.
State is (t,p,l) with t in 0..2, p in 0..1, l in 0..1. Actions 0..5:
0 heat (t:=min(t+1,2)), 1 cool (t:=max(t-1,0)), 2 pressurize, 3
depressurize (p:=max(p-1,0)), 4 lamp_on (l:=1), 5 lamp_off (l:=0).
The effect of action 2 is law-governed: pressurize sets p:=1 UNLESS
blocked, where blocked iff (t==A or A vacuous) AND (l==B or B vacuous).
The learner knows the FAMILY (all 16 (A,B) pairs with A,B in {0,1,2,
vacuous}) but not which pair is true. All other action dynamics are
shared and known.

Per round the learner MUST: (1) prune the 16 hypotheses against every
observed trajectory in its history; (2) stop with IDENTIFIED (A,B) iff
exactly one hypothesis survives; (3) otherwise enumerate all action
sequences of length 1..4 (1654 probes) executable from the CURRENT world
state (the world persists across rounds; there is no free choice of start
state); (4) score each probe by the number of DISTINCT predicted outcome
trajectories across the surviving hypotheses (a probe scoring 0 or 1 is
uninformative and never chosen); (5) execute the top probe (score DESC,
length ASC, lexicographic ASC by action ids) against the hidden world;
(6) append the observed trajectory to history and continue. The true
world is a SEPARATE binary (expworld) and the SOLE reader of the sealed
law file; the learner binary (expseq) never receives the law path. A
shell loop only pipes files between the two binaries (orchestration).

This is sustained, not one-shot: probe choice at round k depends on the
pruned hypothesis set and the evolved world state from rounds 1..k-1.
Setup actions are required (e.g. reaching t==2 with p==0 needs heat,
heat, depressurize before a pressurize test can discriminate), so a
single probe cannot identify the law.

## Frozen sealed worlds (committed with this prereg; law contents frozen)

Law file format: `LAW <A> <B>` then `INIT <t> <p> <l>`, where 3 means
vacuous. Files: prereg/law_WA.txt, prereg/law_WB.txt.

- W-A: LAW 2 3 (pressurize blocked iff t==2). INIT 0 0 0.
- W-B: LAW 2 1 (pressurize blocked iff t==2 AND l==1). INIT 0 0 0.
  W-B requires the learner to set up the lamp itself (no free start
  state), so identification provably needs a multi-round sequence.

## Frozen kill bars (ALL must pass; bars never move after this commit)

- K-X1 (W-A sustained identification): the loop emits IDENTIFIED 2 3
  within 6 executed probes; the emitted pair equals the sealed law file;
  no BUDGET-EXHAUSTED, no STALLED, no INCONSISTENT.
- K-X2 (W-B sustained identification): the loop emits IDENTIFIED 2 1
  within 10 executed probes; same failure exclusions as K-X1.
- K-X3 (sustained, not one-shot): on W-B, IDENTIFIED occurs at round
  >= 3, and the per-round trace shows the surviving hypothesis count
  strictly decreasing in at least 2 distinct rounds.
- K-X4 (determinism): two full loop runs per world are byte-identical
  (cmp on the concatenated round logs).
- K-X5 (no leak): expseq.zag contains no reference to any law file name
  or path and never opens one; only expworld opens the law file.
  Verified by grep over both sources; matches recorded in evidence.
- K-X6 (every probe informative): every executed probe in both sealed
  runs has trace score >= 2 against the then-surviving hypothesis set
  (no wasted probe; the choice is load-bearing each round).

## Cost budget

Max 6 probes on W-A, max 10 probes on W-B; each probe at most 4 actions.
Exact probe counts and total actions are reported. Exceeding the probe
budget is FAIL (BUDGET-EXHAUSTED).

## What counts as FAIL

BUDGET-EXHAUSTED, STALLED (no probe scores > 1 while > 1 hypothesis
survives), INCONSISTENT (history refutes all 16 hypotheses), IDENTIFIED
with the wrong (A,B), any probe executed that was not the algorithm's
top pick, any nondeterminism (K-X4), any leak (K-X5).

## Predicted honest boundaries (declared before implementation)

Authored: the 16-hypothesis family, the shared action dynamics, the
length<=4 probe bound, the distinct-trajectory scoring rule, the
tie-break order, the budgets. NOT authored: the per-round probe choice
(it is a function of pruned hypotheses and evolved state), the number
of rounds, the identification outcome. Honest classification target on
PASS: bounded L2 active experiment construction (Level D, sustained);
explicitly NOT L3 and NOT invention in the Criterion 0 sense: the
hypothesis family is researcher-enumerated (fails C0-B open form), no
new representation is created, semantics are not learner-defined
(C0-A not met). Criterion 0 is therefore not triggered; no L3 claim is
made. Builders report BUILD-PASS/BUILD-FAIL only.

## Implementation plan (pure Zag, zero randomness)

- expseq.zag: argv = history file, state file. Rebuilds the 16
  hypotheses, replays history to prune, prints per-round trace
  (survivor count, top probe, its score), then either IDENTIFIED A B
  or PROBE n a0 ... .
- expworld.zag: argv = law file, state file, probe file. Applies the
  true law step by step, prints OUT with the trajectory states.
- Shell loop (orchestration only): invoke expseq, check for
  IDENTIFIED, else write probe file, invoke expworld, append history
  line, update state file, next round. No decision logic in shell.
