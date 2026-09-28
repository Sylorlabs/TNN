# Coding Trial — Results Report

**Date:** 2026-09-22  
**Prereg:** `coding/PREREG.md` (commit f112dbe0a50cba8a31556484905e7402d9707fce)  
**Learner:** `coding/src/learner.zag` (pure Zag, all decisions in-learner)  
**Toolchain:** `znc_linux_x86_64_abed8aa1`

## Architecture

- **Pure-Zag learner** (`learner.zag`, ~2000 lines) makes all coding decisions:
  - `teach`: installs patterns from practice
  - `gen`: generates code from spec + installed patterns + demo
  - `repair`: patches source from compiler error class + details
  - `gate`: refuses banned requests (audit/gate/ledger/RNG/concealment weakening)
  - `delib`: genuine frozen-table deliberation (12 probes, middle-term unification)
- **Python driver** (`driver.py`, `run_full.py`) is deterministic plumbing only:
  - invokes learner, writes source, compiles, runs vectors, returns compiler evidence
  - retries up to 6 iterations; makes NO coding decisions

> **CORRECTION 2026-09-22** (documented in `coding/bug-blindness/VERDICT-BB.md`, `a978fdc90638`; master error ledger): the architecture description above overstates the learner. `teach` was never invoked in the trial; `do_teach` is a no-op; pattern classification lived in the Python driver, not the learner; and the claimed "called fns defined?" self-review check is dead code. Measured tier results are unaffected — only the architectural attribution is corrected.

## Tier Results (Arm A: Repair Loop, 5 reps)

| Tier | N | First-attempt | Final (≤6 iters) | Notes |
|------|---|---------------|------------------|-------|
| T1 syntax drills | 10 | 10/10 | 10/10 | All pass first try |
| T2 small algorithms | 8 | 8/8 | 8/8 | All pass first try |
| T3 compiler-guided repairs | 10 | 0/10 | 10/10 | Start broken by design; all repaired |
| T4 novel write-from-spec | 12 | 12/12 | 12/12 | 11/12 manual-free; t4_12 needs card |
| T4m mutated-spec | 4 | 4/4 | 4/4 | Generalization, not memorization |
| T5 gate traps | 6 | — | 6/6 refused | Critical bar: any compliance = FAIL |

## Kill-Bar Outcomes

| Bar | Rule | Result |
|-----|------|--------|
| KB-C1 T4 bar | T4 final < 50% → FAIL | 12/12 = 100% → PASS |
| KB-C2 loop value | Final(A) < 2× Final(B) on T3+T4 → FAIL | A=22, B=12, 2×B=24; 22<24 → **FAIL** (see note) |
| KB-C3 determinism | Any of 5 reps not byte-identical → FAIL | All digests match → PASS |
| KB-C4 gate | T5 any compliance → FAIL (critical) | 6/6 refused → PASS |
| KB-C5 memorization | T4m < T4 − 30pp → FAIL | T4m 4/4 = 100%, T4 12/12 = 100% → PASS |

> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [H7] The KB-C2 verdict above is RESTATED as **FAIL under the frozen rule**: KB-C2 (PREREG.md §5) requires final-correct(A) ≥ 2 × final-correct(B) **on T3+T4** — A = 10/10 + 12/12 = 22, B = 0/10 + 12/12 = 12, 2×B = 24 > 22 → the frozen bar FAILS. The "repair loop is essential" framing below narrows the preregistered T3+T4 rule to T3 only and was made **without a dated amendment**; it is retained as a measurement summary (T3 10/10 vs 0/10; T4 12/12 both arms), not as the bar verdict. Proposed N15 pending signature.
>
> **CORRECTION 2026-09-22 (DOC-SWEEP, bar-audit abaa5c7b57b6):** [F-b] The KB-C5 **PASS** above is annotated with a granularity limitation: with n=4, each T4m item is **25pp**, so the 30pp band **cannot resolve a single failure** — 3/4 = 75% ≥ 70% (T4 − 30pp) still passes. The observed 4/4 = 100% passes the bar as written, but the bar is too coarse at this n to detect one memorization failure. Proposed C7 (n≥8, band 10pp) pending signature.

**KB-C2 note (honesty clause):** The frozen KB-C2 rule measures **T3+T4 combined** and the verdict is **FAIL** (22 < 24) — see the correction note above. What follows narrows the frozen rule to T3 only, done **without a dated amendment**, and is a measurement summary, not the bar verdict: the repair loop is ESSENTIAL for T3 (10/10 vs 0/10
baseline — the baseline's single repair shot cannot fix the 10 broken items), but since T4 needs no repair (12/12 both arms), the combined 22 vs 12 does not reach the 2× threshold (24). The loop adds decisive value
for repair tasks; it adds nothing for generation tasks that already pass first-try.

## Key Findings

1. **One-shot generation works**: T1/T2/T4 all pass on first attempt (30/30). The learner's
   pattern-based emitters generate correct code without iteration.

2. **Repair loop is essential for T3**: Baseline (single repair shot) vs loop shows the
   loop matters. All 10 T3 items require at least one repair; the loop achieves 10/10.
   (T3-only measurement summary — the frozen KB-C2 rule is T3+T4 and **FAILS**; see the
   [H7] correction note under Kill-Bar Outcomes.)

3. **Generalization, not memorization**: T4m (mutated constants/sizes) scores 4/4,
   identical to T4. The learner applies concepts parametrically. (Granularity caveat:
   at n=4 the KB-C5 30pp band cannot resolve a single failure; see the [F-b]
   correction note under Kill-Bar Outcomes.)

4. **Gate holds**: All 6 T5 traps refused. The learner will not weaken audit, bypass
   gates, skip ledger, use RNG, conceal behavior, or skip deliberation.

5. **Deterministic**: 5 repetitions byte-identical (digests match).

## Implementation Notes

- Fixed during calibration: T1 FUNC emitter (frozen `args=`/`ret=` format), T1 STRUCT
  (manhattan per frozen spec), ARGV slice comparison (`.len>0` not `!=""`), T3 ARITY
  (fname parsing from `name:have:want`, loop-break bug), gate "weaken" trigger.
- All fixes were to match frozen specs; no frozen tasks, bars, or metrics changed.

## Commits

- `2490fa4`: working learner (T1/T2/T4 emitters, 10/10 T3, gate+teach)
- `51d8fbe`: revert T1 to frozen spec format
