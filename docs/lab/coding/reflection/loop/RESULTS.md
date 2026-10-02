# Fast-Loop Harness — Measurement Results

**Date:** 2026-09-22 · **Battery:** 18 items (10 repair seeds, 4 gen tasks,
1 format repair, 1 logic regen, 2 unfixable-by-design) · **Learner:**
`learner.zag` → `work/learner` · **Toolchain:** `znc_linux_x86_64_abed8aa1`
(`--no-analyze --no-zagd`)

## The lead's question, answered first

**Does speed compound into QUALITY, or just into faster wrong answers?**

**It compounds into quality — and the loop converges instead of thrashing.**
Iterations used are flat across budgets once the budget covers what the task
needs (1 for first-try items, 2 for repair items); raising the budget from 3
to 12 adds **zero** iterations and **zero** passes because the loop stops
itself — by passing, or by the learner's own `halt-*` decision. Speed does
not produce faster wrong answers here: on tasks outside the learner's
knowledge the loop halts in 1 iteration (0.0–0.7s) instead of burning the
budget. The honest boundary: the loop fixes mechanical defects (syntax, name,
arity, type, duplicate, formatting) and logic defects *reducible to
regeneration from spec*; novel logic it cannot re-derive halts, it does not
improve with more iterations.

## Budget sweep: converge, not thrash

| budget | pass | iters | iter/hour | defect rate | first-try rate |
|---|---|---|---|---|---|
| 1 | 4/18 (22%) | 18 | 11,085 | 77.8% | 22.2% |
| 3 | 16/18 (89%) | 30 | 5,983 | 46.7% | 22.2% |
| 6 | 16/18 (89%) | 30 | 5,893 | 46.7% | 22.2% |
| 12 | 16/18 (89%) | 30 | 5,053 | 46.7% | 22.2% |

- Budget 1 → only the 4 first-try gen items pass. Budget 3 → all 12
  fixable items pass. Budgets 6 and 12 change **nothing**: identical
  iteration counts, identical outcomes. The 2 remaining items halt by design
  (`halt-genfail`: spec beyond the learner's concepts; `halt-no-patch`:
  undefined variable, no applicable patch).
- **Convergence table** (iterations used per item — flat = converge):

| item | b1 | b3 | b6 | b12 | outcome |
|---|---|---|---|---|---|
| G1–G4 (gen, first-try) | 1 | 1 | 1 | 1 | pass |
| R01–R10 (repair seeds) | 1 | 2 | 2 | 2 | pass |
| F1 (format) | 1 | 2 | 2 | 2 | pass |
| H1 (logic regen) | 1 | 2 | 2 | 2 | pass |
| X1 (ungenable spec) | 1 | 1 | 1 | 1 | halt-genfail |
| X2 (unfixable error) | 1 | 1 | 1 | 1 | halt-no-patch |

No item ever used more iterations at a higher budget. **Thrash count: 0**
(no `halt-thrash`, no `halt-cycle`, no `stall-guard-halt` fired in any run).

## Headline metrics

| metric | value | notes |
|---|---|---|
| iterations/hour | ~5,000–11,000 | mix- and load-dependent (see below) |
| time to first working build (median) | 0.89s | min 0.42s, max 3.07s (passed items, budget 6) |
| defect rate per iteration | 46.7% | failing iters / total iters at budget ≥3 |
| first-attempt pass rate | 22.2% | 4/18 (the gen items; repair seeds start broken by design) |
| repair success | 12/12 | 10 T3 seeds + format + logic-regen, all ≤2 iters |
| determinism | 3/3 identical | sha256 `71d39ae2…6bb` across 3 full runs |

## Where the time goes (per-iteration phase medians, budget 6)

| phase | median | n | notes |
|---|---|---|---|
| znc compile, broken source | 19.5ms | 11 | fails fast at the check phase — no codegen |
| znc compile, good source | 825ms | 16 | full native codegen dominates the loop |
| test-vector run | 2.5ms | 18 | byte-compare harness |
| learner `diagnose` invoke | 5.5ms | 14 | the deliberation itself |
| learner `gen`/`gate` invoke | ~2–30ms | — | process spawn dominates |

**The deliberation is <1% of iteration cost; successful compilation is ~95%.**
The lead's bet is half-right in an interesting way: generation speed compounds
because *verification* (test run, 2.5ms) and *diagnosis* (5.5ms) are nearly
free — but the loop's wall clock is set by znc codegen on passing builds
(~0.8s), not by thinking. Faster wrong answers are cheap (19.5ms to fail);
verified right answers cost one codegen. The iter/hour spread (5k–11k)
reflects the failed-vs-successful compile mix plus system load, not loop
overhead.

## Diagnosis quality (budget 6, 14 diagnose calls)

| class | n | strategies fired |
|---|---|---|
| TYPE | 3 | patch-type-delbadassign, patch-type-retword, patch-type-argunquote |
| NAME | 3 | patch-unknownfn ×2, halt-no-patch ×1 |
| ARITY | 2 | patch-arity ×2 |
| SYNTAX | 2 | patch-brace ×2 |
| DUPFN | 1 | patch-dupfn |
| OUTPUT_FORMAT | 1 | patch-add-newline |
| LOGIC_VALUE | 1 | regen-from-spec (delta −88, not off-by-one/sign → re-derive) |
| GEN_FAILURE | 1 | halt-genfail |

All 10 T3-equivalent repairs classified correctly with the repair the prior
trial proved; every trace shows the rejected hypotheses too
(e.g. `NAME+0:named-is-defined-conflict` on ARITY items — the NAME hypothesis
was scored and refuted by the source cross-check, not skipped).

## Determinism proof

3 full battery runs at budget 6 → canonical-log sha256 identical all 3 runs:
`71d39ae2af35a444dbaf12752ddce713dbcf67d1367d8b77411eecff216c16bb`.
(Canonical form drops wall-clock timings; one driver-side normalization was
needed and is documented: znc echoes the run-specific source directory in
diagnostics, folded to the basename before logging/hand-off.)

## Honest limits

- The loop repairs what its patch set + regeneration cover. A logic defect
  whose spec is not generable halts; more budget does not help it.
- `LOGIC_OTHER` (non-integer behavioral diffs) and `RUNTIME` (panics) always
  halt — no strategy exists yet. These are the task crews' frontier, not the
  harness's.
- Battery is small (18 items) and the repair seeds are single-defect by
  construction. Multi-defect and cross-file repairs are unmeasured.
- First-attempt pass rate (22%) is dominated by seeds that start broken by
  design; on pure generation tasks it is 4/4.
