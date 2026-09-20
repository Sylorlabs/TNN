# TRIAL_RESULTS.md — Wave-3 Hypothesis-Driven Exploration

**Verdict: NEGATIVE.** The HDE mechanism (as amended A1+A2+A3) does not meet
its preregistered acceptance gate. It is killed as a promoted mechanism.
The explicit-hypothesis ledger and deterministic rerun discipline are
retained as infrastructure; the mechanism itself is not.

This is a preregistered negative, reported as first-class evidence.

## Final head-to-head (native Zag, deterministic, no RNG in either learner's core logic*)

*The baseline uses a seeded LCG only as the random-exploration adversary,
as preregistered. The HDE core contains no RNG, no seeded RNG, no random
tie-break: `grep -rniE "rng|random" impl/hyp_core/learner_core.zag` exits 1.

### Training positives (the preregistered primary measure)

| Curriculum | HDE train | Baseline train | Δ | HDE tests | Base explores |
|---|---:|---:|---:|---:|---:|
| std (40A+40B) | 76/80 | 68/80 | **+8** | 6 | 11 |
| single (16A+16B) | 28/32 | 26/32 | +2 | 6 | 5 |
| flap (16A+[4]×6) | 26/40 | 30/40 | −4 | 12 | 5 |
| walk (16A+16B+8A+8B) | 42/48 | 40/48 | +2 | 8 | 5 |
| storm (16A+[2]×12) | 19/40 | 25/40 | −6 | 20 | 5 |
| **Total** | **191/240** | **189/240** | **+2** | **52** | **31** |

### Test/explore quality (were the "educated guesses" educated?)

| | HDE | Baseline |
|---|---|---|
| Positive tests / explores | 19/52 = **36.5%** | 3/31 = 9.7% |
| Stable-regime explores that were pure waste | — | 0/16 positive on std (every ε-flip plays the known-wrong arm) |

The core's tests are ~3.8× more likely to be right than the baseline's
flips. In stable regimes the baseline's random exploration is 100% wasted
negatives; the core's tests are confirmatory probes. This rate difference
is the mechanism's clearest positive signal — but it does not buy
efficiency where it was preregistered to matter (see F2).

### Frozen endpoint capability (learn=0, detection only)

| Curriculum | HDE evalA | HDE evalB | HDE returnA | Base evalA | Base evalB | Base returnA |
|---|---|---:|---:|---:|---:|---:|
| std | 16/16 | 16/16 | 15/16 | 16/16 | 16/16 | 15/16 |
| single | 15/16 | 15/16 | 15/16 | 15/16 | 15/16 | 15/16 |
| flap | 16/16 | **0/16** | 16/16 | 16/16 | 15/16 | 15/16 |
| walk | 15/16 | 15/16 | 15/16 | 15/16 | 15/16 | 15/16 |
| storm | 16/16 | **0/16** | 16/16 | 16/16 | 15/16 | 15/16 |

Hypothesis confirmations (F5): std 2, single 2, flap 7, walk 2, storm 3 —
nonzero in every curriculum; the machinery was engaged, not inert.

## Preregistered criterion accounting

- **F1** (core total train positives > baseline total): 191 > 189 → **PASS**,
  but the +2/240 margin is negligible and not statistically significant.
- **F2** (core uses fewer explores than baseline on flap and storm):
  flap 12 > 5, storm 20 > 5 → **FAIL**. Under rapid switching the core
  test-storms; the baseline's 5 flips beat the core's 20 tests.
- **F3** (no RNG/randomness in the HDE core): grep clean → **PASS**.
- **F4** (bit-identical reruns): std/single/flap/walk/storm all identical
  across reruns → **PASS**.
- **F5** (confirmations in every curriculum): yes → **PASS**.

Acceptance gate: F1–F5 all pass AND core beats baseline on std and walk
AND explore-success(core) > explore-success(baseline). **F2 fails, so the
gate fails → REJECT.**

(std 76>68 ✓, walk 42>40 ✓, explore-success 36.5% > 9.7% ✓ — the gate
fails on F2 alone.)

## What the mechanism actually does

**Where it wins (std, walk, single):** stable regimes let confirmation
thresholds do their job. The core detects the B-regime surprise in one
episode, partitions (H_RECRUIT) or switches to confirmed knowledge
(H_SWITCH), confirms the new claim in 3 tests, and exploits. Its tests
are confirmatory, so exploration spend is low (6–8) and mostly positive.

**Where it loses (flap, storm):** 4-episode and 2-episode segments are
shorter than the confirmation pipeline. Two failure modes, both observed
in claim-state dumps:
1. **Partition pollution:** the recruited context is seeded with the probe
   arm; when the regime flips back before the challenger confirms, the
   seeded arm gets confirmed for the *wrong* regime (flap: c1 recruited
   for B ended CONFIRMED on obj0/A). The partition becomes a duplicate
   instead of a complement.
2. **Sticky partition-failure block:** after a failed recruit, `x_st==5`
   blocks re-partitioning until "a confirmed claim lifts the block" — but
   under 2-episode alternation nothing ever confirms (storm: hyp_conf
   stayed 1 for all 12 segments), so the core grinds arm-level tests
   forever (20 explores, 5 positive).
3. The baseline's reflexive switch-on-negative is near-optimal for
   2-episode segments (≈1/2 per segment); no hypothesis machinery can
   beat a reflex when the world changes faster than evidence accumulates.

**Endpoints:** the A3 attribution fix repaired frozen detection on
std/single/walk (15–16/16 everywhere). flap/storm evalB remain 0/16 —
legitimate, not a bug: no clean B-knowledge exists to switch to (see
pollution above). The frozen detector correctly reports "nothing confirmed
to switch to" by scoring 0; the failure is in learning, not detection.

## Chronology (what was preregistered vs repaired)

1. **Prereg** written before any run. **A1** (Micah's no-randomness/scaling
   law) folded in before trials.
2. **A2** (smoke-test refinements: preservation-before-revision,
   inconclusive-test escalation) recorded before the full trial.
3. Full A1+A2 trial: all curricula exit 0, deterministic. Training looked
   plausible; endpoints exposed 0/16 frozen failures on single/walk.
4. **A3** (attribution rule + stale-x fix + spent-count fix + storm 12th
   segment): diagnosed from claim-state dumps, implemented, full trial
   re-run from scratch. All numbers above are A1+A2+A3.
5. The A1+A2 endpoint failures are developmental observations, not trial
   outcomes. Do not present the full run as "prereg unchanged" — it used
   A1+A2+A3, with A3 motivated by observed evidence.

## Defects found (all fixed before the reported runs)

- **Spurious refutation** (mechanism defect): regime-change negatives
  refuted confirmed claims before surprise attribution; fixed by the A3
  attribution rule (count → attribute → transition).
- **Stale cross-context state** (implementation bug): one-shot hypothesis
  stuck in TESTING during frozen mode; now resolves whenever its test
  executes.
- **Spent double-count** (implementation bug, introduced during the A3
  refactor): test spend counted at derive and at count; now counted once.
- **Storm protocol**: ran 11 segments vs preregistered 12; added `tA7`,
  both arms re-run.

## Confounds and limitations (disclosed)

- All curricula begin in regime A and deterministic lowest-index
  initialization picks object 0 (correct in A): frozen base is 16/16 for
  the core vs 8/16 for the baseline. Training totals exclude base, but the
  ordering favors the core's initial acquisition.
- n=240 training episodes total; the +2 F1 margin is noise.
- The `updates` counter counts learning outcomes routed to claims
  (single-count since A3); x-test episodes with no matching claim are not
  counted. It is not "episodes learned".
- Operating envelope: the mechanism needs segments longer than its
  confirmation pipeline (≥ ~8 episodes). Below that, reflexive switching
  dominates. This is a measured boundary, not a tuning target.

## Recommendation

**Kill HDE v1 as a promoted mechanism.** Retain the explicit-hypothesis
ledger (named claims, support/refute/ARCHIVED states, deterministic
reruns) as infrastructure — it is what made this negative *diagnosable*,
which is its own vindication as a research tool. A v2 would need
pollution-resistant partitioning, graded/faster confirmation for volatile
regimes, and a rapid-alternation detector — and must be separately
preregistered with counterbalanced (A-first and B-first) curricula. No
further work on v1 is authorized by this report.

## Evidence

- Raw native logs: `evidence/hde_{std,single,flap,walk,storm}.log`,
  `evidence/base_{std,single,flap,walk,storm}.log`
- Determinism reruns: `evidence/hde_{std,single,flap,walk}_r2.log`,
  `evidence/base_{std,storm}_r2.log` (all diff-identical)
- Binaries: `impl/hyp_core/trial_hde`, `impl/baseline/trial_baseline`
  (compiled with `znc_linux_x86_64_abed8aa1`; recompile from source to
  verify)
- Static checks: F3 grep (exit 1 = clean), F4 diffs (identical)
