# CORE-FREEZE-2 RESULTS

Lane `corefreeze2/`. Prereg `PREREG.md` committed ALONE at `f1264a3af`, before any
implementation file existed. No bar was moved after seeing a result.

## 0. FROZEN CORE: UNCHANGED, VERIFIED BEFORE AND AFTER EVERY RUN

```
750cb01d086f0f4eeb29d0a8481e36941a7551396e5c514429a0dffc7aa4b4e8  c8_learn.zag    1331
fc1f6e73c43ae8e4ea2b7af50f1606cc4b6c5353992bd5d4411cb4c9a3b73e61  c15_base.zag    174
4200e21fea5fa75d774f8f9785637d2305eccfa3d9b8486f27b7ac287b10b30d  hq_module.zag    326
```

Identical before and after. `cf2_base.zag` is `c15_base.zag` modulo exactly ONE
line (the `o_flush` body; `_zag_raw_syscall` is inert on this host, brief
4.0/4.1), verified by `diff`. Only DRIVER and WORLD code changed.

## 1. KILL BARS

| bar | result |
|---|---|
| K-A no world/goal/need literals in engine or oracle | **PASS** (grep) |
| K-B1 oracle names no frozen function | **PASS** (grep) |
| K-B2 oracle reads `L` zero times | **PASS** by construction |
| K-B4 oracle self-test | **PASS** (4/4 hand-derived checks) |
| K-D determinism | **PASS**: 3/3 byte-identical stdout (`d3b79961...`); 3 independent clean builds give 3 identical binary shas (`e5932200...`) AND 3 identical stdout shas |
| K-E stdout non-empty, `_zag_print` only | **PASS** (215 lines) |
| K-F all runs through `tnnwatch.sh reg cf2 900` | **PASS**, no orphans |
| K-G frozen hashes unchanged | **PASS** |

**Build-to-build IS byte-stable.** CORE-FREEZE-1's "plan order differed across
rebuilds" is a STALE BINARY, exactly as `lane/buildstab` said. Refuted here
directly.

## 2. THE ORDER-INDEPENDENT CORRECTNESS PREDICATE (as preregistered)

`CORRECT(arm,goal)` iff `rc_ok` AND, for every need index `n`, the SET of values
in the core's record for need `n` equals the SET the oracle computes for need
`n`. Records are keyed by NEED index via the plan (`plan[q]`), so the predicate
is invariant to the core's topological choice; sets are compared as sets, so it
is invariant to in-record order. Version correctness is scored separately and
never folded in.

**This is not cosmetic.** Measured plan orders differ from need order in 9 of
the 20 scored goals (e.g. `porder=1,0,2` and `porder=0,2,1,3`). A need-ordered
comparison would have failed goals that are correct.

## 3. PER-ARM CORRECTNESS (independent oracle, NOT agreement)

25 oracle-scored goals per arm. `Lnz` = nonzero 4-byte cells of the learner
arena.

| arm | learner state | episodes | CORRECT | cost | Lnz before 1st goal -> after |
|---|---|---|---|---|---|
| **EXP** | full | yes | **23/25** | 1200 | 66 -> 76 |
| **NOEP-COLD** | zero, never rebuilt | **none** | **25/25** | 1581 | **0 -> 10** |
| **NOEP-WARM-A** | ALPHA-episode image | none | 22/25 | 975 | 66 -> 76 |
| **NOEP-WARM-B** | end-of-EXP image | none | **9/25** | 78 | 257 -> 258 |
| DEV-NOEP | zero, stage 1 skipped | none | 1/1 | 15 | 0 -> 28 |
| DEV | stage 1 + stage 2 | yes | 1/1 | 25 | 29 -> 57 |
| DEV-ABL | stage 1, RET coverage zeroed | yes | 1/1 | 27 | 28 -> 56 |
| CURR-ABC / BCA / CAB / INT | see §7 | yes | **1/3 each** | 54/54/54/102 | |

**EXP's two failures are real wrong answers, not metric artefacts.** Both are
the stale-index probe (PB.stale, PB.stale2): the core answers `[]` where the
oracle says `{202,203,209}`.

**NOEP-COLD is 25/25. The arm with NO experience is more correct than the arm
with experience.** CORE-FREEZE-1 reported the two arms as byte-identical
(MR=27/27); under a correctness metric they are not, and the difference runs
against the learned arm.

## 4. IS A TRUE NOVICE ARM POSSIBLE? NO. PREREG N-1 CONFIRMED.

In NOEP-COLD the learner arena is all zeros before the first goal and has **10
nonzero cells after it**. `compose_iter` has only two paths: `plan_find<0` ->
`learn_bindings` (writes the binding table, increments `L[13232]`) -> `plan_new`
(writes a plan slot) -> execute; or `plan_find>=0` -> execute. **There is no
read-only path.** A true novice -- one that answers a goal with `L` byte-identical
before and after -- is IMPOSSIBLE through the frozen core's public interface.

This is reported as a finding about the core's interface, not papered over.
CORE-FREEZE-1's `BASE-NOEP` was not a novice arm and `FRESH_ARENA` is not
implementable as a no-experience arm at all (it rebuilds
`specialize_ret/vfy/cnt` FROM the arena by construction). NOEP-COLD is the
strongest honest approximation: zero episodes, zero `specialize_*`, zero
arena-derived learner state, `L` never carrying anything across cases.

## 5. THE `L` BASELINE AUDIT (PREREG section 5, adjudication fixed in advance)

The two values are two DIFFERENT ARMS, not two measurements of one arm:
`L`-inherited = NOEP-WARM, `L`-zeroed = NOEP-COLD. A no-experience arm that
begins with experience is not a no-experience arm, so the arm that answers the
mission's question is NOEP-COLD.

* **Correct value for the `L`-zeroed arm: MR-equivalent 25/25 CORRECT.** The
  `L`-inherited arm is NOEP-WARM-B at **9/25**, not 13/27 and not 27/27.
* The prereg expectation in CORE-FREEZE-1 that "zeroing `L`" would reveal
  agreement at 27/27 was WRONG in its sign: zeroing `L` does not produce
  agreement, it produces the *only arm with no wrong answers*.
* **PREREG DEVIATION D2, recorded not fixed:** CORE-FREEZE-1 chose which arm to
  call "the baseline" after observing that the choice flipped its headline.
  Independently, its reference arm was 6/14 correct, so neither value was
  licensed. Both are recomputed here under the section-2 predicate.

## 6. BATTERIES, ALL WITH ZERO FROZEN-SOURCE CHANGE

CF1, world ALPHA (relations 11..20): RET projection, fan-in VERIFY conjunction,
COUNT over a subject set, generic fallback on an uncovered relation,
multi-source fan-in into one COUNT, kind-1 scalar dataflow, honest decline
(rc=0), one-shot storage + immediate reuse. **7/7 correct in EXP.**

CF2, the same five shapes in **4 UNSEEN domains** -- BETA (9001..9005), GAMMA
(5001..5005, 6001..6003), DELTA (7001..7004), EPSILON (31..35). **4/4 correct
in EXP**, 4-need goals each, no ALPHA identifier reused except the need tags.

CF3, ONE frozen lifetime, `L` never reset: F1 typed rewriting (maximal reduct
set filtered by type AND grade) `[2,2,3;2,2,3;1,1]`, F2 causal blast radius
(union of one-hop consequences) `[1,1;1,3;1,1]`, F3 long lifetime through six
worlds with re-derivation. **Correct**, except that the PB probes inside F3 are
wrong (below).

Long-lifetime probe result: the ALPHA answer after the full six-world lifetime
is still `{101,102,103}` = oracle. **No lifetime degradation when the arena is
consistent.** The failures appear only when the arena changes under a
specialized index.

## 7. CURRICULUM UNDER THE CORRECTED METRIC: KILL BAR NOT MET, AND NOW INTERPRETABLE

| order | episodes | finals correct |
|---|---|---|
| ABC | A B C | 1/3 (only C) |
| BCA | B C A | 1/3 (only A) |
| CAB | C A B | 1/3 (only B) |
| INTERLEAVED A B A C B C | 6 blocks | 1/3 (only C) |

**No order reaches 3/3. F-3 FAILS.** But unlike CORE-FREEZE-1's uninterpretable
FAIL, the mechanism is named and oracle-verified: in every order exactly the
LAST-presented task is correct and the earlier ones answer `[]`. The failing
answers are `ans=[0;0]` against `orc=[2,8001,8002;2,8001,8002]` -- a WRONG answer
of the same shape as the EXP PB failures. `specialize_ret` stores FACT INDICES;
after task C is specialized, querying task A's arena reads C's indices. This is
the stale-index defect again, not catastrophic interference: the failure count
is order-INDEPENDENT (1/3 in all four orders).

## 8. WHAT LEARNER STATE ACTUALLY BUYS

* **COST: nothing, and sometimes worse.** EXP 1200 fact checks, NOEP-COLD 1581
  (1.32x). NOEP-WARM-B costs 78 because its indexes are stale and match almost
  nothing.
* **A version label.** 16 of 25 relations are covered; the rest fall back to
  the generic path.
* **TWO WRONG ANSWERS that the no-experience arm gets RIGHT** (EXP 23/25 vs
  NOEP-COLD 25/25).
* **A worse DEV ablation profile is not observable**: DEV, DEV-ABL and DEV-NOEP
  are all 1/1 correct, so stage-2 competence is again independent of stage-1
  state -- now measured against an oracle rather than against a transcript.
* **OSC-DEP: `how=1` (invented, 4 passes, lag 2) in EXP, NOEP-COLD and
  NOEP-WARM-A alike.** The oscillation response is produced with ZERO learner
  state, so CORE-FREEZE-1's Tier-A evidence does not survive: it is not a
  learned capability.
* **F-4 CONFIRMED: no one-shot generalisation.** `L[13232]` = 12 in both EXP and
  NOEP-COLD, i.e. exactly 3 family trials per new need tag, never fewer. One
  episode never reduces the family search space.
* One-shot STORAGE is real: `us` shows 23 `ret_spec` uses in EXP versus 0 in
  NOEP-COLD. One episode buys an index, i.e. a constant factor on a linear scan.

## 9. ACCOUNTING (charter 2/108): THE HONEST RATIO

| capability | source change | oracle verdict in EXP |
|---|---|---|
| CF1 RET / VERIFY-fanin / COUNT / fallback / multisrc / kind-1 / decline | **ZERO** | 7/7 correct |
| CF1 one-shot storage + reuse | **ZERO** | correct |
| CF2 BETA / GAMMA / DELTA / EPSILON | **ZERO** | 4/4 correct |
| CF3 F1 formal / F2 causal / F3 long lifetime | **ZERO** | correct (PB probes wrong) |
| oscillation response `how=1` | ZERO | **NOT ORACLE-SCORABLE** (iterative) |

**20 oracle-scored capabilities : 0 lines of cognition source changed.**
Plus 1 oscillation observation that is deliberately NOT counted, because the
oracle cannot define an iterative fixed-point query and because it fires with
no learner state.

**Disclosed driver code, all measurement plumbing, none of it a capability:**
D1 `dropall` (24 lines) -- releases the frozen core's own 4 plan slots between
world batteries; without it `plan_new` returns -1 and the core reads out of
bounds. D2 `reindex` (20 lines) -- the plan-order to need-index mapping that
makes the metric order-independent. D3 lesion cells (2 lines).

**Harsh reading, which is the correct one:** all 20 are instances of the SAME
three researcher-authored procedure families and three dataflow rules, on
researcher-authored goal records. That is TIER-B work: the researcher writes
the capability into the goal record every time. **TIER-A = 0.** The delta is
`20 : 0` only in the trivial sense that I touched no cognition source; the
honest statement is **zero new capabilities from learner state and zero from
new experience**, exactly as CORE-FREEZE-1 said, now measured correctly.

## 10. HARNESS DEFECTS FOUND (all mine, none in the frozen core)

1. **`vbuf` must be >= 88 bytes and `R` >= 116.** The frozen core writes
   `vbuf[16]`, `vbuf[20]` and `R[28]`. I first allocated 32 bytes each: a heap
   overflow that silently corrupted an unrelated table and produced a garbage
   fact value. CORE-FREEZE-1 used 32 for both and may have been affected.
2. **`ans[0]` is the count of INTS in the stream, not the count of records.**
   `ans_append` is called once per value, record length included. Isolated with
   a 30-line probe (`rc=2 ans0=4 ans4=3 ans8=101 ans12=102 ans16=103`). My
   first raw-record walker mis-read this; the metric addressed records by byte
   offset and was never wrong.
3. **`bld()`'s final table int was not reliably written.** `get32(SA,220)`
   returned `0xAAAAAAB0` (uninitialised heap) for the last row of a table built
   by `bld`. Not diagnosed. Worked around by reordering the segment record so
   no load-bearing field sits at the table tail. **UNEXPLAINED, FLAGGED.**
4. Goal rows and episode rows must be exactly self-delimiting: four VERIFY
   episode rows had 13 ints instead of 12 and silently shifted every later
   episode by one int.

## 11. BOUNDS FOUND IN THE FROZEN CORE

* **BOUND-6 (NEW, HARD).** `compose_iter` sizes `W=320`, `OUTS=640`,
  `dirty=16`, `SUBL=512` -- exactly **4 needs**. A 5-need goal reads and writes
  out of bounds. Found because a 5-need GAMMA goal silently returned `[]` for
  its last need while the oracle said `{2,3}`. All goals here are <= 4 needs.
* **BOUND-3 confirmed and it bites.** `ret_log_rel` caps at 16 relations
  (`retcov=16`). DELTA, EPSILON and the one-shot world's relations were never
  logged, so those goals ran the GENERIC path (`ver` 0/4/1). The specialized
  path was therefore exercised only on ALPHA/BETA/early-GAMMA.
* **BOUND-5 confirmed.** `plan_find` keys on goal tag only, 4 slots; `dropall`
  is required between batteries.
* **BOUND-4 (stale index) is the dominant correctness defect.** It is not an
  edge case: it produced 2 of EXP's 3 wrong answers and 8 of the 12 curriculum
  wrong answers.

## 12. VERDICT

**The frozen core is a competent, deterministic, domain-agnostic goal-record
INTERPRETER, and this is now measured against an independent oracle rather
than against another arm. It is not a learner of capability, and the evidence
is stronger than CORE-FREEZE-1's, because it no longer rests on agreement
between two arms that may both be wrong.**

* 20 novel world / namespace / task combinations executed with ZERO cognition
  source change and zero domain handlers. Real, verified generality of the
  *interpreter*.
* The no-experience arm is 25/25. The full-experience arm is 23/25 and its two
  failures are the experience-induced stale-index defect. **Learner state does
  not buy competence; it buys a linear-scan speedup, a version label, and two
  wrong answers.**
* A true novice arm is impossible through the public interface: the core writes
  learner state on the very first goal call.
* The oscillation response, CORE-FREEZE-1's only Tier-A evidence, fires
  identically with zero learner state.
* One-shot storage is real and is a constant factor on a linear scan.
  One-shot generalisation is absent: 3 family trials per new need tag, always.

**A stronger negative than "it does not learn": the specialized index is a
correctness liability.** `specialize_ret`/`vfy`/`cnt` persist FACT INDICES
across world changes, so any goal whose arena changed after specialization
returns a confidently wrong answer with `rc=2`.

## 13. BOUNDARIES

* One oracle, one author. The oracle is independent of learner state and of
  every arm, and its self-test is 4 hand-derived checks, but it is not a
  third-party implementation and its declared semantics were read off the
  frozen core's own generic procedures (`c15_base.zag` 79-174). A different
  reading of "VERIFY fan-in" would move some counts.
* The oscillation goal is OUT OF ORACLE SCOPE (it has a self-link, so need order
  is not a topological order) and is excluded from the competence denominator.
  It is reported as an observation only.
* `R`/`vbuf`/coverage saturation means the specialized code path was exercised
  on fewer worlds than the generic one.
* Curriculum tasks are 2-need goals in 4-fact worlds; the ordering effect is
  clean but the battery is small.
* Harness defect 3 is unexplained.

## 14. NEXT EXPERIMENT

1. **Make the stale index impossible, then re-run this battery unchanged.** A
   generation counter on the arena plus a coverage stamp in `L` would convert
   every failure in §7 and §8 into a version downgrade instead of a wrong
   answer. That is a cognition-source change and must be measured as its own
   wave; this lane exists to measure, not to fix.
2. **Attack the 4-need ceiling (BOUND-6).** Goals above 4 needs corrupt the
   heap silently. Either dimension the buffers from `g_nneeds(G)` or make
   `nneeds>4` a hard decline, and measure which.
3. **The one lever that produced a learner-state-dependent behaviour was the
   oscillation handler, and it turned out not to depend on learner state.** The
   next falsifiable target is the outcome record (`L[14500..]`): `outc_find`
   replays a stored response, and NOEP-WARM-B's `how=0` versus `how=1`
   elsewhere is the only place in this wave where the stored record changed the
   outcome. Construct an arena whose oscillation has a period that the
   researcher did not enumerate, and test whether the invented response
   transfers to an unseen goal shape.