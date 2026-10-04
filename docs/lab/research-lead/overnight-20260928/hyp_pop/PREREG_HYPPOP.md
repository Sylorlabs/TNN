# PREREG_HYPPOP.md -- Competing Hypothesis Population Scale Test (C2)

Frozen: 2026-09-30. Committed alone before any implementation, world
generation, or measurement. Any implementation commit must strictly follow
this commit.

## 1. Claim under test

TNN can maintain and update thousands of learned competing models
efficiently: a population of 2200 competing causal hypotheses, updated
incrementally by an evidence feed, with periodic contests that prune
losers, plus exact evidence accounting per hypothesis.

This is a MACHINE-NATIVE claim (scale/precision), NOT an L3
representational-invention claim. The hypothesis FORM (conjunctions of
up to 2 source variables predicting a destination variable after a
delay) is researcher-designed. What is tested is maintenance,
incremental update efficiency, contest dynamics, and honest comparison
against a conventional baseline (SQLite) doing the same logical work.

## 2. Synthetic world (deterministic from sealed seed)

Generated entirely inside the Zag program from a fixed seed constant
(sealed at implementation; recorded in the result report):

- 10 binary variables V0..V9.
- True law: for each dst variable, either (a) a conjunction of 2 source
  variables at time t predicts dst at t+delay (delay 0..3), or (b) no
  relation (noise: dst flips randomly with p=0.5).
- 6 of 10 dst variables have true conjunctive laws; 4 are noise.
- 200 episodes, 20 timesteps each, binary states.
- Concept shift: after episode 100, the true law for ONE dst variable
  changes to a different (src1, src2, delay) triple.

## 3. Contestant: hypothesis population engine (pure Zag)

Hypothesis population (exact count verified by the engine's counter):

- Singles: (src, dst, delay): 10*10*4 = 400.
- Conjunctions: (src1 < src2, dst, delay): C(10,2)*10*4 = 1800.
- Total: 2200 hypotheses. Each stores: for_count, against_count,
  fired_count, status (alive/dead).

Feed (incremental, one episode at a time, no future peeking):

- For each episode, for each ALIVE hypothesis: for each timestep t
  where the hypothesis fires (conditions met), check prediction at
  t+delay; for_count += 1 on correct, against_count += 1 on wrong.
- Updates are applied per episode; nothing is recomputed from scratch.

Contests (mirroring TNN causal contests):

- After episodes 50, 100, 150, 200: for each dst variable, among ALIVE
  hypotheses predicting that dst, keep the top 8 by score
  (for_count - against_count); mark the rest dead (pruned).
- Pruned hypotheses stop receiving updates.

Queries (measured):

- Q1: top-8 alive hypotheses by score (global).
- Q2: best alive predictor for a given dst (argmax score).
- Q3: evidence trail for a hypothesis id (for/against/fired).
- Q4: prune all alive hypotheses with score < 0; report pruned count.
- Q5: recovery trace: rank of the true NEW law for the shifted dst at
  episodes 100, 125, 150, 175, 200 (does the population re-rank after
  the concept shift?).

Metrics recorded per run: hypotheses maintained, hypothesis-updates
applied (fired checks), episodes/sec, per-query latency (ms, via
clock_gettime), peak RSS (kB, /proc/self/status), state bytes.

## 4. Baseline (same world, same feed, same queries)

B-sql: SQLite implementation of the same logical work:

- tables: hypothesis(id, s1, s2, dst, delay, is_conj, f, a, fired,
  alive), episode(ep, t, v0..v9).
- Feed: per-episode UPDATE of f/a/fired via joins (same per-episode
  incremental discipline; no full recompute).
- Contests: per-dst top-8 keep via window functions.
- Queries: Q1-Q5 equivalents in SQL.
- Timing: wall-clock for feed + contests + queries, measured with
  sqlite3 .timer / shell time. Same hardware.

The world data for the baseline is emitted by the Zag program itself
(world.sql: hypothesis and episode INSERTs), guaranteeing identical
data. SQL is the tool; the baseline is not a TNN mechanism.

## 5. Kill bars (numbered; ALL must pass for POP-TESTED)

- K1 (population scale): hypotheses maintained = 2200 exactly
  (400 singles + 1800 conjunctions), verified by engine counter.
- K2 (update efficiency): full feed (200 episodes x 20 steps) completes;
  episodes/sec, hypothesis-updates/sec, per-query latency (ms), peak
  RSS (kB) all measured and recorded.
- K3 (baseline comparison): B-sql implements feed + contests + Q1-Q5 on
  identical data; wall-clock comparison reported for both directions
  (Zag vs SQLite); code size (Zag lines vs SQL lines) reported. No
  claim of superiority is made unless measured.
- K4 (purity/governance): pure Zag only (no .py files, no python3
  invocation at any stage); no em-dash bytes in docs; prereg commit
  strictly precedes implementation; 3/3 full runs byte-identical.

## 6. Honest scope and anti-spoof notes

- The hypothesis FORM is authored; the test measures population
  maintenance, not invention. The concept-shift recovery (Q5) measures
  re-ranking dynamics, not structural invention.
- SQLite is expected to be competitive or faster on pure bookkeeping;
  the honest question is WHERE (if anywhere) the Zag in-process engine
  differs: startup/latency profile, flat resource footprint,
  integration with learner-created state. Name the measured
  differences; do not claim unmeasured advantages.
- The 6 true laws are a small fraction of 2200 hypotheses; most
  hypotheses are distractors. This is the point: the population must
  carry dead weight efficiently.

## 7. Verdict rule

POP-TESTED iff K1..K4 all pass as numbered above. Any single failure
-> POP-FAIL with the failing bar named. Builder reports POP-TESTED or
POP-FAIL only; no SURVIVES claim (promotion pipeline steps are for the
parent to schedule).
