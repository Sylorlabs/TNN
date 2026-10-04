# HYPPOP_RESULT.md -- Competing Hypothesis Population Scale Test

Date: 2026-09-30 UTC. Builder: Hypothesis Population Worker.
Verdict: **POP-TESTED** (K1-K4 all pass as preregistered).

## Commits (local, tnn-native-lab, owned path only)

- Prereg: `a0ca3fd62` -- `hyp_pop/PREREG_HYPPOP.md`, committed alone before
  any implementation.
- Implementation + results: this commit -- `hyp_pop/hyppop.zag` (637 lines),
  `HYPOP_RAW_1/2/3.txt`, `HYPOP_ERR_1/2/3.txt`, this report.
- Order verified: `git merge-base --is-ancestor a0ca3fd62 HEAD` must hold
  (checked before pushing this report upstream to the coordinator).
- Binary `hyppop_bin` left untracked (not committed), consistent with
  prior waves.

## What was built

`hyppop.zag` (pure Zag): a synthetic world of 10 binary variables with
6 true conjunctive causal laws (4 noise variables), 200 episodes x
20 timesteps, one concept shift at episode 100 (dst 2 gets a new law).
A population of exactly 2200 competing hypotheses (400 singles +
1800 conjunctions "s1 AND s2 at t predicts dst at t+delay") is
maintained with per-episode incremental evidence updates (for/against/
fired counters), per-destination top-8 contests after episodes 50, 100,
150, 200 that prune losers, and five query types (top-8, best-per-dst,
evidence trails, score<0 prune, shift-recovery ranks).

`emit_sql` mode regenerates the identical world as `world.sql`
(2200 hypothesis INSERTs + 40000 state INSERTs) so the SQLite baseline
runs on byte-identical data.

## Kill bars

- **K1 (population scale): PASS.** Engine counter verifies exactly 2200
  hypotheses (400 singles + 1800 conjunctions). `HYPOTHESES 2200` in all
  3 runs.
- **K2 (update efficiency): PASS.** Full feed completes: 200 episodes,
  205,179 hypothesis-updates applied. Measured: feed 802/1021/892 ms
  (3 runs), queries 11-14 ms, peak RSS 244-248 kB. Episodes/sec ~222.
  Updates/sec ~228k.
- **K3 (baseline comparison): PASS.** SQLite implements the identical
  feed (per-episode UPDATEs, same incremental discipline), identical
  contests (per-dst top-8, same tie-break), and Q1-Q5 equivalents on
  identical data. **Every baseline output matches the Zag output
  exactly** (Q1 top-8 ids/scores, Q2 per-dst best, Q3 trails, Q4 pruned
  count 0, alive 80, all 5 shift ranks = 1). Measured comparison below.
- **K4 (purity/governance): PASS.** Pure Zag only: no .py files, no
  python3 invocation at any stage (world gen, build, runs, baseline
  data gen all in Zag; baseline driver is bash+sqlite3). Zero em/en-dash
  bytes in docs (byte-checked). Prereg strictly precedes implementation.
  3/3 runs byte-identical stdout
  (md5 `63d6c066834adbe564f43e03c0660b52`).

## Baseline comparison (honest, both directions)

| Dimension | Zag engine | SQLite baseline |
|---|---|---|
| Feed (200 ep x 2200 hyp) | 0.80-1.02 s | 3.8-5.0 s wall |
| Queries Q1-Q5 | 11-14 ms | included in wall |
| Peak RSS | 244-248 kB | ~6.1 MB |
| Result equality | -- | exact match on all outputs |
| Hand-written code | 637 lines Zag | ~15 lines SQL (templates) |
| Data | generated in-process | 1.6 MB world.sql |

Where Zag wins (measured): ~5x faster incremental feed, ~25x smaller
resident footprint, zero IPC/parse overhead, single static binary
(72 kB). Where SQL wins (observed): the feed logic is ~15 lines of
declarative SQL versus 637 lines of Zag; the query formulations
(window functions) are far more concise; SQLite brings persistence,
ACID, and ad-hoc queryability the Zag engine lacks. A differently
structured SQL formulation (set-based per-episode rather than
correlated UPDATEs) might narrow the speed gap; the comparison is
apples-to-apples on the same incremental algorithm, not a claim about
optimal SQL.

Fair headline: for in-process incremental maintenance of a few
thousand competing hypotheses, a purpose-built flat-array engine beats
SQLite on speed and footprint while SQLite wins decisively on code
concision and database properties. This is a bounded engineering
result, not an architectural advantage unique to TNN.

## Dynamics findings (information gain)

1. **Tautology dominance.** Delay-0 self-singles ("v at t predicts v
   at t") are unfalsifiable: they fire exactly when correct. They win
   every per-destination contest on raw score and occupy all 10 Q2
   slots. This is not a bug in the engine; it is a property of
   raw-count scoring in hypothesis populations.
2. **Precision-vs-frequency.** True conjunctive laws tracked with
   perfect precision (e.g. id 1335: f=23, a=0) were pruned by contests
   because rare-but-exact hypotheses lose to frequent tautologies on
   raw score. Implication for TNN causal contests: evidence-count
   ranking without a complexity or tautology guard selects for
   unfalsifiable hypotheses. This connects to the Q4 design note on
   MDL/compression scoring.
3. **Q5 confound.** Shift-recovery ranks measured 1,1,1,1,1 -- the
   shifted hypothesis ranks first by default in a heavily pruned
   population, not through demonstrated re-ranking. The rank metric as
   designed is uninformative under these dynamics; reported honestly,
   not hidden.
4. **World warts (disclosed).** Delay-0 laws may draw a source equal to
   the destination, which reads a stale buffer cell (deterministic but
   semantically murky; the shift triple has this property). A latent
   non-termination exists in law generation for dst 0 with delay 0
   under other seeds (range-1 resample loop); the frozen seed never
   triggers it.

## Honest scope

The hypothesis FORM (conjunctions) is researcher-designed; the test
measures population maintenance, update efficiency, and contest
dynamics, not representational invention. The concept-shift recovery
did not demonstrate learning beyond re-ranking dynamics. No SURVIVES
claim is made; promotion steps are for the parent to schedule.

## Files

- `PREREG_HYPPOP.md` (frozen)
- `hyppop.zag` (implementation)
- `HYPOP_RAW_1.txt`, `HYPOP_RAW_2.txt`, `HYPOP_RAW_3.txt` (stdout)
- `HYPOP_ERR_1.txt`, `HYPOP_ERR_2.txt`, `HYPOP_ERR_3.txt` (metrics)
- Baseline artifacts (reproducible): `/tmp/hyppop_world.sql`,
  `/tmp/baseline_run.sql` (via `/tmp/gen_baseline.sh`),
  `/tmp/sqlite_out.txt`; driver `/tmp/run_baseline.sh`

**Builder label: POP-TESTED** (K1-K4 pass; comparison honest both ways)
