# PREREG -- CORE-FREEZE-2 (C5xx block)

Lane `corefreeze2/`. Committed ALONE, before any implementation file exists.
This prereg supersedes nothing; it re-runs the CORE-FREEZE-1 battery under a
correctness metric instead of an agreement metric, and it repairs three defects
the CORE-FREEZE-1 red team (7c82f5d2a) found in that lane's load-bearing claim.

Refs: charter 2/59/60/61/62/63/108/216. Brief sections 1, 2, 3, 4.0, 4.1, 7, 10.

## 0. FROZEN CORE. UNMODIFIABLE. HASHES VERIFIED BEFORE AND AFTER EVERY RUN.

```
750cb01d086f0f4eeb29d0a8481e36941a7551396e5c514429a0dffc7aa4b4e8  cogops_learnosc2/c8_learn.zag    1331
fc1f6e73c43ae8e4ea2b7af50f1606cc4b6c5353992bd5d4411cb4c9a3b73e61  cogops_rescueaware/c15_base.zag  174
4200e21fea5fa75d774f8f9785637d2305eccfa3d9b8486f27b7ac287b10b30d  hook_phase1/hq_module.zag        326
```

Only DRIVER and WORLD code may change. `cf2_base.zag` is `c15_base.zag` modulo
exactly one line (the `o_flush` body: `_zag_raw_syscall` is inert on this host,
brief 4.0/4.1). Verified by `diff`. Concatenation order:
`cf2_base, cf2_data, cf2_oracle, c8_learn, hq_module, cf2_engine`.

## 1. THE THREE DEFECTS BEING REPAIRED

**D1. MR=27/27 WAS ARM-AGREEMENT, NOT CORRECTNESS.** In CORE-FREEZE-1 the
reference arm `BARSEG s=0` scored MA=6/14 against researcher-transcribed
expected answers. Agreement between two arms licenses no inference when the
reference itself is mostly wrong. Fix: section 2.

**D2. MR WAS 13/27 UNTIL `L` WAS ZEROED.** The SIGN of the headline was set by
an unaudited baseline. Fix: section 5. Reported as a PREREG DEVIATION, not as a
correction of the previous lane.

**D3. THE "NO EXPERIENCE" ARM WAS NOT A NOVICE.** CORE-FREEZE-1's `BASE-NOEP`
ran `compose_iter` from a zeroed `L`; `compose_iter` calls `learn_bindings` and
`plan_new`, which WRITE learner state derived from the arena before answering.
It also reports `FRESH_ARENA`, which by construction rebuilds
`specialize_ret/vfy/cnt` FROM the arena and is therefore not an arm of "no
experience". Fix: section 4.

**D4. THE COMPETENCE METRIC WAS CONTAMINATED BY EMISSION ORDER.** Answer
records are emitted in PLAN order (`topo_g` takes the LAST zero-indegree need),
not need order, and per-record objects are emitted in FACT order. The previous
metric compared a need-ordered expectation against a plan-ordered emission and
then "reordered" with driver code that reads the plan table. Fix: section 3.

## 2. THE INDEPENDENT ORACLE (the load-bearing new artifact)

`cf2_oracle.zag` computes, for every goal, the correct answer **directly from the
world fact table**, under these DECLARED semantics, which are read off the
frozen core's own generic procedures (`c15_base.zag` lines 79-174) and are
restated here in full so the oracle can be audited without reading the core:

* **RET(rel, obj)** -> the SET of subjects `s` such that `(s, rel, obj)` is a
  fact of the world.
* **VERIFY(chain)** -> 1 if every step `(s, r, o)` of the chain is a world fact,
  else 0. When the chain is fanned in over a source need's subject set S, the
  answer is the SET `{ x in S : the chain with every `s==0` slot filled by x
  holds }`.
* **COUNT(rel, subs)** -> the number of DISTINCT objects `o` such that
  `(x, rel, o)` is a fact for some `x` in `subs`.

Constraints on the oracle, enforced by grep as kill bar K-B:

* K-B1: `cf2_oracle.zag` contains NO call to, and NO textual mention of, any
  frozen-core function name (`ret_gen`, `vfy_gen`, `cnt_gen`, `ret_spec`,
  `vfy_spec`, `cnt_spec`, `compose_iter`, `execute_plan_iter`, `learn_bindings`,
  `try_family`, `plan_new`, `plan_find`, `plan_drop`, `specialize_*`, `osc_*`,
  `ret_episode`, `vfy_episode`, `cnt_episode`, `fact_add`, `world_new`, and no
  `get32(L,...)` read).
* K-B2: the oracle reads the learner arena `L` ZERO times. Its only inputs are
  the world fact table and the goal record.
* K-B3: the oracle is never compared against another arm's output to decide what
  is correct. Correctness is defined only by `CORRECT(arm, goal)` in section 3.
* K-B4: the oracle's own answers are validated by a self-test that must run
  first: for each world, three hand-checkable queries embedded in the DATA file
  with their hand-derived answers, plus a mutual-consistency check that the
  oracle's RET answer for `(rel,obj)` equals the transpose of its COUNT answer
  over the resulting subject set. A failing self-test is a HARD FAIL of the whole
  wave; no core result is then citable.

## 3. THE ORDER-INDEPENDENT CORRECTNESS PREDICATE (PREREGISTERED HERE)

Let a goal have `nn` needs. The core returns `rc` and an answer vector that is a
concatenation, in PLAN order, of per-need records `[n_i, v_1..v_ni]`.

```
CORRECT(arm, goal)  iff  rc_ok(arm, goal)
                    AND  for every need index n in 0..nn-1:
                          SET(core_record_for_need_n) == SET(oracle_record_for_need_n)
```

* `core_record_for_need_n` is obtained by re-indexing the emitted records by
  PLAN position (the frozen core's `ans_append_rec` emits need
  `plan[13000+pi*56+8+q*12]` at record `q`), so the predicate is keyed on NEED
  index and is therefore **invariant to which topological order the core chose**.
* `SET(...)` is set equality on the value list: same length and every oracle
  value present in the core list. This is **invariant to the order of objects
  inside a record**. Distinctness violations are penalised: a record with a
  duplicate has length > oracle length and fails.
* `rc_ok(arm,goal)` is TRUE iff `rc != 0`, except for goals listed in the DATA
  file with `must_decline=1`, where `rc_ok` is TRUE iff `rc == 0`.
* `VER` correctness is scored SEPARATELY and never folded into competence:
  version correctness is exact equality of the per-need version vector against
  the DATA file, in NEED order, and is reported as its own denominator.

A goal is CORRECT or it is not. There is no partial credit and no
agreement-based fallback. If two arms agree and the oracle says otherwise, BOTH
arms are recorded INCORRECT. That is the expected shape of the headline if D1
was fatal.

## 4. ARMS. AND THE QUESTION "IS A TRUE NOVICE ARM POSSIBLE?"

The previous lane's `BASE-NOEP` is DISCARDED as a novice arm. The arms here:

* **EXP** (reference): `ret/vfy/cnt` episodes run, then `specialize_*`, then
  goals. Identical to CORE-FREEZE-1 `s=0`.
* **NOEP-COLD**: `L` zeroed. NO episodes. NO `specialize_*`. NO arena-derived
  learner state of any kind. Then goals. This is the honest "no experience" arm.
* **NOEP-WARM**: `L` zeroed, NO episodes run in THIS arm, but `L` is preloaded
  with the `L` byte-image produced by EXP. Purpose: separate "no experience in
  this lifetime" from "no learner state at all". This is the arm whose value
  moved 13/27 -> 27/27 in CORE-FREEZE-1; here it is preregistered in advance so
  its SIGN cannot be chosen after the fact.
* **NOEP-FRESHARENA**: PREREGISTERED AS INFEASIBLE, and expected to fail. It is
  included as a NEGATIVE CONTROL, not as an arm: implementing it requires calling
  `specialize_ret/vfy/cnt` against the arena, i.e. rebuilding learner state from
  the world, which is precisely the experience this arm claims to lack. It is
  therefore NOT IMPLEMENTED, and the report must say so.

**PREREGISTERED STRUCTURAL PREDICTION N-1.** A true novice arm, defined as
"answers at least one goal with the learner arena byte-identical before and
after", is **IMPOSSIBLE through the frozen core's public interface**.
`compose_iter` has exactly two paths: `plan_find<0` -> `learn_bindings` (writes
the binding table and increments `L[13232]` trials) -> `plan_new` (writes a plan
slot) -> execute; or `plan_find>=0` -> execute. There is no read-only path. If
this prediction is WRONG (i.e. some arm exists with `L` unchanged after a goal),
that is reported as a positive finding about the core's interface and I must say
so. I will measure `L`'s nonzero-cell count immediately before and immediately
after the first goal call in NOEP-COLD and print it.

## 5. THE `L` BASELINE AUDIT (D2), PREREGISTERED

CORE-FREEZE-1 reported MR=13/27 for the no-experience arm until `L` was zeroed,
then 27/27. Preregistered adjudication, fixed BEFORE any run:

1. The two values are the values of TWO DIFFERENT ARMS, not two measurements of
   one arm. `L`-inherited = NOEP-WARM. `L`-zeroed = NOEP-COLD.
2. **A no-experience arm that begins with experience is not a no-experience
   arm.** Therefore the arm that answers the mission's question -- "does
   competence come from learner state?" -- must be NOEP-COLD, and the correct
   value for the `L`-zeroed arm is the one CORE-FREEZE-1 ultimately reported.
3. CORE-FREEZE-1 nevertheless committed a prereg violation in effect: it chose
   which of the two arms to call "the baseline" after observing that the choice
   flipped the sign of its headline. This is recorded as **PREREG DEVIATION D2**,
   not fixed, and the previous lane's 27/27 headline is reported as
   **not independently licensed**, because its reference arm was only 6/14
   correct (D1).
4. Both values are recomputed here under the section-3 predicate and reported
   side by side. Neither is deleted.

## 6. BATTERIES

**CF1 -- 8 capabilities, world ALPHA (relations 11..15).**
C1 1-step RET projection; C2 fan-in VERIFY conjunction; C3 COUNT over a subject
set; C4 per-need version selection incl. generic fallback (ver 0); C5
multi-source fan-in into one COUNT (2 sources); C6 oscillation detected from
the learner's own trajectory with the response invented (how=1); C7 honest
decline on an unbindable need shape (rc=0); C8 one-shot storage + immediate
reuse (ver 2 after exactly one episode).

**CF2 -- the same five goal SHAPES in 4 UNSEEN domains** (BETA relations
9001..9005, GAMMA relations 5001..5003 and 6001..6003, DELTA relations
7001..7004, EPSILON relations 2001..2005). No goal tag, relation id, or need tag
from ALPHA is reused except the need tags 901/902/903 themselves, which are part
of the interface under test.

**CF3 -- formal + causal + long lifetime in ONE frozen lifetime, `L` never
reset.** F1 typed rewriting (a conjunction whose two steps must hold in
sequence over a fan-in set, i.e. formal reduction). F2 causal blast radius
(COUNT over the subject set reachable in one relation hop, i.e. the union of
distinct consequences). F3 long lifetime: EXP-style episodes in world 1, then a
goal in world 2, then a goal in world 3, then a re-derivation episode, then a
goal in world 1 again, all on ONE `L`, with the learner arena never zeroed and
the plan table never manually dropped.

**DEV ablation** (charter 61): DEV, DEV-ABL (early RET coverage count zeroed),
DEV-NOEP (stage 1 skipped entirely). Scored by the oracle, not by agreement.

**CURRICULUM ORDER** (charter 62): three two-need tasks T-A, T-B, T-C in worlds
never used elsewhere; orders ABC, BCA, CAB and INTERLEAVED (A B A C B C).
Kill bar: an order reaches 3/3 CORRECT final queries.

**ONE-SHOT / FEW-SHOT** (charter 63): 0, 1, 2 episodes; four repeats; and the
stale-index probe (does a re-presentation after arena change give the ORACLE's
answer or a stale one).

## 7. KILL BARS (frozen)

* **K-A** `cf2_engine.zag` and `cf2_oracle.zag` contain ZERO world relation ids,
  ZERO goal tags, ZERO need tags in any literal. (grep; both files)
* **K-B** oracle independence, section 2, K-B1..K-B4.
* **K-D** determinism: `tools/zbuild.sh <src> --rep 3` must report 3/3
  byte-identical stdout, PLUS 3 independent clean builds of the same source must
  yield 3 identical binary sha256 values AND 3 identical stdout sha256 values.
  (This directly tests the CORE-FREEZE-1 "plan order differs across rebuilds"
  observation, which `lane/buildstab` attributed to a stale binary.)
* **K-E** stdout non-empty. `status=EMPTY` from the watchdog is a FAIL, not a
  result. `_zag_print` is the only output path.
* **K-F** every run goes through `tnnwatch.sh reg cf2 900`. No orphans.
* **K-G** frozen core hashes unchanged, checked before and after each run.

## 8. ACCOUNTING RULE (charter 2/108), PREREGISTERED

Every capability is labelled with exactly one of:

* **Z** = obtained with ZERO cognition-source change. The driver called only
  `compose_iter` / `osc_handle` / `plan_drop` / the episode wrappers, all of
  which are frozen-core entry points selected by DATA (mode byte), never by
  goal identity.
* **D** = required driver code I added. **A capability labelled D DOES NOT COUNT
  toward the capability total and DOES NOT COUNT as zero-source-change.** D is
  disclosed with the line count.

Reported ratio is `(number of Z capabilities) : (lines of cognition source
changed in the frozen core)`, which is `N : 0` when the core is untouched, plus
the separate count of D capabilities. A driver line that exists only to make a
capability measurable (e.g. the order re-index) is not cognition and is listed
separately as instrumentation.

## 9. FALSIFIERS (fixed in advance)

* **F-1 (competence is not from learner state, CORRECTLY MEASURED).** EXP and
  NOEP-COLD have equal per-goal CORRECTNESS on every goal of CF1+CF2+CF3, AND
  EXP's absolute correctness is high. If EXP correctness is LOW, the correct
  conclusion is "the core is an interpreter that is frequently WRONG", which is a
  different and stronger negative. Both outcomes are reported.
* **F-2 (a true novice arm is impossible).** `L` changes across the first goal
  call of NOEP-COLD. If it does not, F-2 is refuted.
* **F-3 (curriculum independence).** At least one of the four orders reaches
  3/3 CORRECT. CORE-FREEZE-1's kill bar was 9/9 under a contaminated metric; this
  prereg resets the bar to 3/3 on a clean metric because its battery has three
  final queries, not nine. This is a NEW preregistered bar for a NEW metric, and
  the old result is reported next to it as uninterpretable, not as a pass.
* **F-4 (one-shot generalisation).** `learn_bindings` trial counter `L[13232]`
  grows by exactly 3 per NEW need tag and 0 per already-bound need tag. If it
  grows by 3 per goal regardless, one-shot generalisation is absent.

## 10. WHAT WOULD MAKE THIS WAVE A FAILED ZERO

Reporting "the core learns nothing" while EXP is itself mostly incorrect would
be a faked result in the opposite direction. If EXP correctness < 14/14 I must
say so in the headline, and the verdict must be "interpreter, and an unreliable
one at that". Equally, reporting agreement as competence is the CORE-FREEZE-1
error and is forbidden here.