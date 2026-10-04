# PREREG: LT3 -- the harder third lifetime (FREEZE-ARENA-2)

Branch `lane/p1freeze`. Lane `p1_freeze_arena/`. Claims **C581-C596**.

Mandated by `PREREG.md` section 12, committed pre-implementation at `22a015c1e`,
and by `REPORT.md` section 9 ("NEXT EXPERIMENT"). This document is the
**measurement contract** for that continuation. It is committed ALONE, before any
LT3 code is committed and before any LT3 number is observed.

---

## 0. What LT3 is for

FA1 (`REPORT.md`) produced a negative result and, more usefully, a *localization*:

> Correctness is a function of **arena contents**, not of age. The decisive row
> was `FRESH_ARENA` -- **zero** experience, **full** arena -- answering the
> 2-stage join goal correctly, at 5.8x the lifetime's cost. Age bought cost.

FA1 also exposed a weakness in its own world, stated in `REPORT.md` section 9:

> `ABL-NOFACT-A` broke the composed goal F but `ABL-NOFACT-C` did **not**. The
> goal was *declared* to need A+C; only A's facts were load-bearing. **The world
> did not in fact force a composition.**

So the FA1 composition claim was weaker than advertised, and LT3 exists to
build the world that FA1's world failed to be, then re-run the same question at
higher difficulty. Two possibilities, both valuable:

* the 3-stage join **is** load-bearing on all three stages, and we learn whether
  a genuine fan-in changes anything;
* the 3-stage join **still** answers correctly for a zero-experience learner
  handed the arena, which confirms the architectural verdict at higher
  difficulty rather than overturning it.

LT3 must be able to return either. It is not permitted to be built so that only
one answer is possible.

## 1. THE QUESTION

Identical to FA1 section 1, restated:

> With facts reachable **only** through episodes, does a learner's accumulated
> **age** make it answer a composed goal **more correctly** than a fresh learner
> given the identical arena-construction rule and zero episodes -- or does the
> answer depend only on which facts are present?

## 2. Design: two arms, ONE difference

Unchanged from FA1 section 2. The arms differ only in whether `frz_fill`
preloads stage `s`'s facts into the arena at stage entry.

| arm | arena at stage entry | during stage |
|---|---|---|
| **LIVE** (`frz=0`) | stage `s`'s facts **prefilled** (C500-R1's schedule) | one append per episode |
| **FROZEN** (`frz=1`) | **empty of stage `s`** | one append per episode, and nothing else, ever |

The third arm required by the mission -- *the same lifetime WITHOUT the freeze* --
is the **LIVE** arm. It is retained, not dropped: FA1 showed the correctness gap
appears identically in both arms, which is exactly why the verdict is negative.

## 3. The world (pinned by hash; changes are detectable)

Ten stages **A-J**. sha256 of the committed world file is asserted by `run.sh`.

* **10 relation ids per stage**, **16 subjects per stage** (4 subjects per
  `(relation, object)` pair, so every declared answer is closed-form).
* **600 distractor facts at E** (not FA1's 200).
* **Eight distinct goal shapes** against the frozen **4-slot PLAN table**
  (`PREREG.md` section 12 asked for six; eight is a superset, so the
  saturation condition is strictly harder. Recorded, not moved.)
* **`GACF` (goal 5): a genuine THREE-STAGE join, `A + C + F`** -- three needs
  drawn from three different stages, so no single prior stage can satisfy it.
* **A SECOND revision at stage I**, contradicting stage A's functional-arity
  rule as well as stage B's, so **two** arity violations must be detectable.
* **Stage J requires the structure first assembled at I** (`GIJ`, goal 8).

**ID bands are disjoint by construction.** Every stage owns a private subject
band, object band and relation band. FA1's bands overlapped (ERRATA2 E7), which
made the LK2 value-equality test uninterpretable; LT3 removes the confound at the
source instead of masking it after the fact.

Stage-fact totals: A 40, B 40, C 40, D 40, E 600, F 40, G 40, H 40, I 40, J 40
= **960 triples**.

## 4. Frozen core, unchanged

`frozen_prefix.zag` = `c15_base.zag` + `c8_learn.zag` + `hq_module.zag`,
sha256 `043b62b427e97f0e5f59f8d0de9ec2b8cfa506ecf4b271d971cdfee07c1b177c`.
The 1331-line `c8_learn.zag` prefix is carried byte-for-byte. **No
recompilation of the core, no edits inside it.** Exactly one `fn main(` per
translation unit.

## 5. No labels, no feedback, no reset

As FA1 section 5. The learner is reached only through `frz_episode(...)` and
`lt_query(...)`; neither takes a stage selector or a correctness signal. Every
literal -- world, goals, declared answers, stage ids, names -- lives on the
harness side. Verified mechanically, not asserted (K23).

## 6. THE LEAK CONTROLS -- primary artifact, unchanged

All seven are the FA1 implementations, unmodified, so FA1 and LT3 are comparable.

| id | question | required outcome |
|---|---|---|
| **LK1** | how many of stage `s`'s triples are in the arena at stage entry | FROZEN **0**; LIVE `nf` |
| **LK2** | how many of stage `s`'s triples are already in learner memory at stage entry | FROZEN **0** |
| **LK2C** | dump `offset=value(sig)` for colliding cells | disambiguates any non-zero LK2 |
| **LK3** | deliver **every** episode with the arena's write path deleted, then query | `nfe_ok == 0` |
| **LK4** | arena fact count == episode count at all 10 checkpoints | `eq == 1` |
| **LK5** | LIVE arena == FROZEN arena, element-wise, at all 10 checkpoints | `eq == 1`, `firstdiff == -1` |
| **LK7** | at each stage midpoint: partial arena count, suffix memory | `arena == floor(n/2)`, memory `0` |

**LK3 is the positive control that makes a silently-failing freeze detectable.**
A freeze that fails open reproduces FA1/C500-R1 for the wrong reason; a freeze
that fails *closed* produces a lifetime that looks bad for a trivial reason.
LK3 separates those. If LK3 passes and the freeze verdict still comes out
negative, the negative result is real.

## 7. Arms, baselines, ablations at the `GACF` join

| row | state | arena | what it isolates |
|---|---|---|---|
| `LIFETIME` | full | full | the aged learner |
| `FRESH0` | zero | **empty** | can age help where facts are absent? |
| `FRESH_ARENA` | zero | **full** | **is the answer just a lookup?** |
| `FRESH_F` | zero | stage F only | is one stage enough? |
| `RECENCY16` | zero | last 16 facts | is recency enough? |
| `ABL-NOSTRUCT` | lifetime snapshot, templates+bindings wiped | full | data vs **structure** |
| `ABL-SNAPSTALE` | lifetime snapshot, refresh off | full | snapshot staleness (C500-R1) |
| `ABL-SNAPCTRL` | lifetime snapshot, refresh on | full | the control for the above |
| `ABL-NOFACT-A` | lifetime snapshot | full **minus A's 40** | is A load-bearing? |
| `ABL-NOFACT-C` | lifetime snapshot | full **minus C's 40** | is C load-bearing? |
| `ABL-NOFACT-F` | lifetime snapshot | full **minus F's 40** | is F load-bearing? |
| `*-_COV` variants | as above, coverage arrays also cleared | | separates fact removal from index removal |

**The `FRESH_ARENA` row is the load-bearing measurement of this whole
continuation.** FA1 showed it is the row that decides the verdict.

## 8. Measurements, all required

Per stage, per arm: examples-to-criterion (**TTC**), positives delivered, facts,
arena count, `memL`/`memLT` occupancy, `costep`, `costq`, revision events,
retention/verify/count coverage, plans built, plan loads, plan drops, trials,
declines, templates built/held, bind hits/misses, cross-stage reuse (`xw`),
reused-template fires (`rr`), functional-arity violations (`fviol`), query
count, goal `ok`, answer vector.

Plus: positive transfer (`D-reprobe-GA`, `E-reprobe-GA`, `I-reprobe-GA`),
negative transfer / interference (`H` decline under invention pressure, plan
drops, `fviol`), forgetting, and cost for every ablation row.

**Spontaneous reuse (charter 25)** is measured, not asserted: `xw` and `rr` must
be read at the `GACF` goal *specifically*, not just cumulatively. FA1's reuse
counters were flat at F -- the one goal the world was built for -- and that is
the specific finding LT3 must re-test at its own join goal.

## 9. Preregistered predictions (all falsifiable, none movable)

| | prediction |
|---|---|
| **Q1** | LIVE reproduces the FA1 pattern: TTC `0` at every stage. |
| **Q2** | FROZEN TTC `>0` at every stage-local stage. If any is `0` the freeze failed at that stage and that stage's result is void. |
| **Q3** | FROZEN `FRESH0` answers `GACF` **incorrectly**. Load-bearing. |
| **Q4** | FROZEN `LIFETIME` answers `GACF` **correctly**, identically to LIVE, because LK5 gives arena equality. |
| **Q5** | Therefore a strict `LIFETIME > FRESH0` correctness gap exists at `GACF` in **both** arms. If it appears only in FROZEN, the freeze produced it; if in both, it is not about the freeze. |
| **Q6** | **`ABL-NOFACT-A`, `ABL-NOFACT-C` and `ABL-NOFACT-F` each make `GACF` wrong.** All three branches are preregistered. If any leaves `GACF` correct, the join is **not** load-bearing on that stage and **no reuse or composition claim may be made from this run**; that is reported as the finding. This is the correction FA1 section 9 demanded. |
| **Q7** | `FRESH_ARENA` answers `GACF` **correctly** at a large multiple of `LIFETIME`'s cost. This is the predicted-negative row. If `FRESH_ARENA` is *wrong*, the architecture is not a fact-store lookup and the negative result needs re-deriving from scratch. |
| **Q8** | `ABL-NOSTRUCT` breaks or degrades `GACF` -- but this is **not** decisive on its own, because NOSTRUCT is a hybrid state (episode-derived `L` + wiped `LT`). The clean discriminator is the `FRESH_ARENA` vs `LIFETIME` cost ratio at equal correctness. Both are reported. |
| **Q9** | Plan-table saturation: with 8 goal shapes against a 4-slot table, `pld` (plan drops) is `>0` at some stage in at least one arm, and saturation costs at least one goal its plan. |
| **Q10** | At the `GACF` goal the reuse counters `xw`/`rr` are **flat** relative to the preceding stage, i.e. the learner still does not spontaneously decide that A and C apply to `GACF`. FA1 observed exactly this at F. |
| **Q11** | The second revision at I raises `fviol` at **two** distinct arity rules (A's and B's) before I's goal, unprompted. If `fviol` is 0 at I, the learner is blind to the second contradiction too, which is interference with age and is reported as such. |
| **Q12** | FROZEN costs **more** in aggregate than LIVE. |

## 10. Kill bars

| bar | requirement |
|---|---|
| **K20** | determinism: 3/3 **byte-identical** stdout for the LT3 binary, asserted by hash |
| **K21** | NON-EMPTY stdout, byte count > 0, asserted in the build script |
| **K22** | oracle == declared for every goal in both arms (`orc` == number of goals) |
| **K23** | namecheck: no stage id/name, goal tag, declared answer or oracle call in the learner-side files; `frz_episode` and `lt_query` are the only entry points |
| **K24** | LK1 == 0 at all 10 FROZEN stage entries |
| **K25** | LK2 == 0 at all 10 FROZEN stage entries (collision-excluded control reported alongside) |
| **K26** | LK3 `nfe_ok == 0` |
| **K27** | LK4 `eq == 1` at all 10 checkpoints, both arms |
| **K28** | LK5 `eq == 1` and `firstdiff == -1` at all 10 checkpoints |
| **K29** | LK7: `arena == floor(n/2)` at all 10 midpoints, suffix memory `0` |
| **K30** | frozen prefix sha256 `043b62b427e9...`, exactly one `fn main(` |
| **K31** | world file sha256 matches section 3's pin |
| **K32** | FA1 anchor still reproduces its certified sha256 `1d2a2688...` on this host -- LT3 must not have perturbed FA1 |

If **K24, K25, K26, K27, K28 or K29** fail, the freeze is declared **BROKEN**,
no FROZEN verdict is issued, and the failing checkpoint is reported. If **K20,
K21 or K22** fail, no verdict is issued at all.

## 11. Adjudication rule, fixed in advance

The mechanical verdict is the conjunction of K20-K32. The **scientific** verdict
is stated in words from the measured table, never selected from a label list.

The scientific question is answered by this pair, both required:

> **(a)** Does FROZEN-`LIFETIME` answer `GACF` correctly while FROZEN-`FRESH0`
> answers it incorrectly? (the age gap)
> **(b)** Does FROZEN-`FRESH_ARENA` -- zero experience, full arena -- also answer
> `GACF` correctly? (is the answer a lookup?)

The decision table, fixed now:

| | (b) yes | (b) no |
|---|---|---|
| **(a) yes** | age improves correctness over an empty arena, but **not** over the same facts. Verdict: **NEGATIVE for "smarter with age"** -- the gain is data, not age. This is FA1's result confirmed at higher difficulty. | age improves correctness **and** the zero-experience learner with the same facts cannot match it. Verdict: **POSITIVE**. This would overturn C500-R1 and FA1 and is the only cell that does. |
| **(a) no** | verdict: **NEGATIVE**, and a stronger one -- age does not even beat an empty arena. | verdict: **INCONCLUSIVE**; the procedures cannot answer at all and no intelligence claim is licensed. |

Q6 gates everything: if any of A, C, F is not load-bearing, the world did not
force a 3-stage join, the `(a)` cell is not testing composition, and the report
must say so before any verdict is read off the table.

## 12. Boundaries preregistered as expected

* **Nothing here clears L3.** RETRIEVE/VERIFY/COUNT are researcher-frozen
  templates (C397). Every learner-created object remains enumerable from source.
  A positive result in the one positive cell of section 11 would still be L2.
* The `LIFETIME > FRESH0` gap, whenever it appears, is the weak claim "the
  learner retains and can use what it has seen". It is **not** evidence of
  increased intelligence.
* One lifetime, one finite triple store (960 facts, capacity 1200), no
  perception, no noise, no drift, every episode and every goal researcher-
  authored.
* One host, one compiler build (`znc 2026.07.0-dev`, macos-arm64).
* The compiler is **not** blamed for anything. No defect is attributed to it
  without a memory-free oracle, and none is anticipated.

## 13. Honesty note on ordering

The world file, helpers, freeze layer and driver skeleton for LT3 were drafted
in an earlier session of this lane **before** this prereg was committed, and
were left untracked. To keep the prereg meaningful rather than decorative:

* their sha256 are pinned in section 3 / `run.sh` (K31), so any later edit is
  detectable after the fact;
* **no LT3 number had been observed** when this prereg was written;
* this prereg is committed **ALONE**, with an explicit pathspec, containing no
  LT3 implementation file;
* the predictions in section 9 were fixed before the driver was completed, and
  in particular before the `ABL-NOFACT-{A,C,F}` rows were known to work.