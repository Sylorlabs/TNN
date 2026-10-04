# PREREG M4 (P1-MECHANISM) -- attacking the mechanism behind "Smarter with age: NO"

Claims **C600-C6xx**. Lane `p1_mech/`. Branch `lane/p1mech`.
Committed **ALONE, pre-implementation**, no M4 number observed.
Attacks **C500-R1 / FA1 / C585-C596 (LT3 FREEZE-ARENA-2)**.

Baseline anchor already reproduced on this branch, pre-implementation:
`cat frozen_prefix.zag lt3_*.zag > lt3.zag`; stdout sha256
`555792382303bb090403ce7152f77eba9388c1e9d088b3e7b64757d7ce76e4c9`, 20363 B,
identical to the certified `lane/p1freeze` value. Kills bar **K1**.

---

## 0. WHAT IS BEING ATTACKED, PRECISELY

LT3's preregistered adjudication cell (a) `LIFETIME` correct / (b) `FRESH_ARENA`
correct is **both yes**, and the prereg fixed that as **NEGATIVE for "smarter
with age"**. That adjudication is not disputed here. What is attacked is the
**LOCALIZATION** in `REPORT_LT3.md` section 5, and the **two supporting
measurements** in section 3.3 and section 3.5.

LT3's own stated next experiment (section 9) is: stop enlarging the world,
attack the mechanism, and test (i) whether a learned rule can substitute for
absent triples, (ii) a goal-shape-sensitive reuse measure.

### 0.1 THREE DEFECTS FOUND IN THE PRIOR RESULT BY DIRECT INSPECTION

Recorded now, before any M4 implementation, because each changes what M4 must
measure. All three are re-verified mechanically by kill bars **K2** below.

* **D1. "8 goal shapes vs the frozen 4-slot PLAN table" is not true of LT3.**
  `LT3_world.zag` builds all eight ordinary goals with the SAME
  `lt3_goal4` four-need chain; they differ only in which stage each need's
  `(relation, object)` comes from. `lt_sig_goal` hashes `nf` and link kinds
  only, so all of them collapse onto **one** template. Certified output:
  `plans=1` (one `plan_new` success in the whole lifetime) and `pld=8` at the
  end, where `pld` is the **plan-LOAD** counter `L[13228]`, not a drop
  counter. The LT3 report reads it as "plans 1->10 and plan drops 0,1,...,8".
  Plan-table capacity was therefore never pressured. `Q9` is void, not "half".
* **D2. The internal representation of a join goal is byte-identical to that of
  a stage-local goal.** `lt_query` rewrites `GC` by replacing the goal tag with
  a canonical tag and each need tag with a canonical tag; **every field value
  of every need is copied through unchanged** (`lt_copy(GC,G,512)` then
  `set32(GC,need_off(GC,i), ...)` on tags only). `lt_sig_need` hashes
  `nf*7 + k1*13 + k2*29 + k3*61`. Hence two goals of the same shape have the
  same template, the same canonical goal bytes, and the same canonical tag, and
  `plan_find` is keyed on that canonical tag. A consequence that M4 measures
  directly (K2b, `GCEQ`): **the learner cannot represent which stages a goal
  needs**, so charter-25 "recognise applicability" is not merely unmeasured, it
  is unrepresentable at this layer.
* **D3. The cost multiple in LT3 section 3.3 is not a like-for-like
  comparison.** The `1.11x` is `query cost of LIFETIME` over `query cost of
  FRESH_ARENA`. `FRESH_ARENA` is charged **zero** for the 1068 episodes that
  `LIFETIME` paid for: certified `costep` is **762480** (LIVE) / **570846**
  (FROZEN) against `costq` 75764 / 42720. On total cost the aged learner is
  **~15x worse**, not 1.11x better. M4 measures both accountings
  (K-K1/K-K2) and reports the sign flip.

None of D1-D3 changes the adjudication cell. All three change what the
negative result *means*.

---

## 1. HYPOTHESIS UNDER TEST

**H-MECH.** The limitation behind "smarter with age: NO" is **(c) the absence
of any generalisation/substitution mechanism**, together with the
shape-only internalisation of D2 -- and **not** (a) the flat append-only
arena, **not** (b) `try_family`'s arity-only family decision, and **not** (d)
the goal-tag-keyed PLAN table.

**H-MECH predicts:**
* the learner is wrong on any goal whose answer requires a triple that is not
  in the arena, **even when a rule derivable from the same triples determines
  that triple's value** (K-GEN1);
* a non-learning, arena-only majority induction recovers the same answer
  (K-GEN2), and is falsifiable on a world with identical arena contents and a
  different declared answer (K-GEN3);
* arena re-organisation and arena duplication change nothing (K-LOC1, K-LOC2);
* the frozen family decision is never wrong (K-LOC3);
* plan capacity is never reached (K-LOC4).

**H-MECH is REFUTED** if the learner answers the hole goal correctly (K-GEN1
fails) -- that is, if a rule learned from related triples substitutes for an
absent triple. **The negative result is OVERTURNED** in that case and this
would be the single largest available result in the program. M4 is committed to
reporting that outcome if it occurs.

---

## 2. WORLD W4 (harness side; no literal below is visible to the learner)

Subject band **100..115** (16), shared across all stages -- required so a
fan-in join is expressible. Relation band per stage `s` is
`1001+100s .. 1010+100s`; object band per stage `s` is `2001+100s ..
2010+100s`. Bands are disjoint across stages, so per-stage attribution is
unambiguous and value-collision cannot arise (LT3's LK2 confound removed at
source).

Witness set of relation index `k` in an ordinary stage:

```
k : 0    1    2    3    4..9
w : 16   12   8    4    2
```

so 16+12+8+4+6*2 = **52 facts per stage**, 10 stages, **520 triples**.

### 2.1 THE HOLE

Stage **5** is the hole stage. Its index-0 relation `1501` (object `2501`) is
witnessed by subjects **100..114** only. The triple `(115,1501,2501)` is
**never delivered by any episode and never written to the arena**. Stage 5 has
**51** facts. The index-0 witness-size table is therefore `{16,16,16,16,16,15,
16,16,16,16}` over the ten stages: supported nine times, violated once.

### 2.2 W4F -- THE FALSIFICATION WORLD FOR THE STUPID BASELINE

**Identical arena contents and identical declared answers for every goal
except the hole goal.** The hole goal's declared answer is **15** subjects
(`100..114`) instead of 16. W4 and W4F differ ONLY in whether the absent triple
exists in the world. Nothing observable by the learner differs. This minimal
pair is what makes the induction test non-vacuous: any procedure that gets
W4 right and W4F wrong is doing real induction, not reading the answer.

### 2.3 GOALS

All ordinary goals use `lt3_goal4`'s exact four-need chain (RETRIEVE, two
kind-2 fan-ins, one kind-3 COUNT), which is the frozen executor's grammar:

| id | shape | needs | load-bearing stages |
|---|---|---|---|
| `G0` | 4-need | all from stage 0 | 0 |
| `G4` | 4-need | all from stage 4 | 4 |
| `G5` | **4-need** | all from stage 5 (the hole stage) | 5 |
| `GACF` | 4-need | s0, s2, s5 | 0,2,5 |
| `GSWAP` | 4-need | s5, s2, s0 (**need order permuted**) | 0,2,5 |
| `G14` | **3-need** | s1, s2, s3 | 1,2,3 |
| `G2NF` | **5-need** | s0..s4 | 0,1,2,3,4 |
| `GX` | 3-need, unbindable (`nf=5` on need 1) | -- | must DECLINE |

**Six genuinely distinct goal shapes** (`4-need`, `3-need`, `5-need`,
`unbindable`) against a frozen 4-slot PLAN table -- this is the plan-capacity
pressure LT3 did not have (D1). `GSWAP` is the applicability probe: same needs
as `GACF`, different order.

Declared answers are hand-derived from section 2 and cross-checked against the
memory-free oracle (**K3**), except where divergence is preregistered
(**K-GEN4**).

---

## 3. THE CRUX: CAN A LEARNED RULE SUBSTITUTE FOR AN ABSENT TRIPLE?

### K-GEN1 (the crux kill bar)
`LIFETIME` on `G5` in W4 with the hole present: **`ok` must be 0.**
`ok=1` means the learner substituted a rule for the absent triple and the
central negative is OVERTURNED.

### K-GEN1b (the age control at the hole)
`FRESH_ARENA` (zero experience, identical arena) on `G5`: **`ok` must equal
`LIFETIME`'s `ok`.** Any difference means age changes the hole outcome in either
direction and must be reported as the boundary of the negative result.

### K-GEN2 (the stupid baseline -- induction must recover it)
`STUPID-MAJORITY` on `G5` in W4: **must produce 16 subjects `100..115`** and
score `ok=1`. The procedure is arena-only, memory-free, episode-free, ~25
lines: for the query relation's index `k`, take the witness-set size that
`k` has at the largest number of *other* stages, and return the witness set of
any relation at another stage having that size. It reads no world definition,
no declared answer, and no learner memory.

### K-GEN3 (the stupid baseline must be falsifiable)
`STUPID-MAJORITY` on `G5` in W4F (identical arena, declared answer 15):
**must score `ok=0`.** If it scores 1 it is an oracle in disguise and the whole
section is void; that outcome is reported as a KILL BAR FAILURE and no
generalisation claim may be made.

### K-GEN4 (no generic procedure recovers it)
The memory-free oracle on `G5` in W4 must return the **15**-subject answer,
i.e. `orc == 0` against the declared 16. Preregistered divergence: this is the
measurement showing the information is reachable by induction and by nothing in
the frozen executor.

### K-GEN5 (the test is not vacuous on intact data)
`STUPID-MAJORITY` and `LIFETIME` on `G4` (intact stage): both `ok=1`.

---

## 4. THE REUSE MEASURE (charter 25 made testable)

`xw`/`rr` fire on ANY reuse. Three new quantities, all learner-side except
where stated:

* **`APP-STAGES(g)`** (harness, ground truth) = number of distinct stages whose
  relation ids appear in `g`'s need fields. `G0`=1, `GACF`=3, `GSWAP`=3.
* **`APP-MATCH(g)`** = fraction of `g`'s needs whose frozen bound family is
  field-consistent with `g` (arity per `try_family`, aggregate-op per
  `fam 2`, and the need's relation id inside the band the learner has actually
  observed for that family). Charter 25 "recognise applicability".
* **`APP-SEARCH(g)`** = `cost(LIFETIME,g) / cost(FRESH_ARENA,g)`. Charter 25
  "reduce search". `< 1` is a reduction.
* **`GCEQ(a,b)`** = 1 iff the learner's canonical goal bytes for `a` and `b`
  are identical field-for-field after tag canonicalisation. **This is the
  decisive measure.**

### K-R1 `GCEQ(G4, GACF) == 1` and `GCEQ(GACF, GSWAP) == 1`
i.e. the learner's executable representation does not distinguish a 3-stage
join from a stage-local goal, nor the join from its own permutation. **If
`GCEQ == 1` the learner provably cannot be selecting prior stages because the
goal requires them**, and charter 25 is refuted at the representation level,
not merely unmeasured. If `GCEQ == 0`, the representation does carry stage
information and section 4's localisation of D2 is wrong and must be corrected.

### K-R2 `APP-MATCH == 1` at every ordinary goal
If a bound family is ever field-INconsistent the applicability claim is false
at the family level.

### K-R3 `APP-SEARCH < 1` at the join `GACF`
Charter 25 requires reuse to reduce search. Recorded either way.

### K-R4 the naive measure cannot discriminate
`xw` must be identical (1) at a purely stage-local goal and at the 3-stage join
goal. If they differ, the naive measure does discriminate and the prior report's
Q10 verdict is wrong.

### K-R5 the stupid reuse baseline is non-discriminating
`APP-STUPID(g)` = 1 iff the template table is non-empty. Must be 1 at a
reprobe goal that needs nothing new. Demonstrates that "did anything exist to
reuse" is the null measure, and that any reuse claim needs `GCEQ`/`APP-STAGES`
to be interpreted.

---

## 5. COST AND DEFERRAL

* **K-K1** Report `costq` **and** `costep` for the aged learner and `costq`
  for `FRESH_ARENA`, plus the totals `TOT-LT = costep + costq` and
  `TOT-FA = costq`. **K-K1 is killed if `TOT-LT / TOT-FA >= 1` is not
  reported.** No bar is placed on the sign; the sign is the finding (D3).
* **K-K2 decay curve.** Fix the goal (`GACF`), sweep prior-stage count
  `N in {0,1,2,3,5,8,10}` and distractor count `D in {0,52,208,600}`.
  Record `APP-SEARCH` at each point. **Kill bar: the curve is reported in full
  and the crossing point (if any) where `APP-SEARCH >= 1` is located.** The
  preregistered expectation is monotone decay through 1; any regime with
  `APP-SEARCH < 1` sustained is a positive cost finding for age and is reported
  as such.
* **K-K3 deferral.** Aging would be a *deferral* win if the aged learner pays
  less total work than a learner handed the same arena cold. Test: compare
  `TOT-LT` against `TOT-FA` on the same arena. Also report `costep(s)/s` at each
  stage `s`; a rising ratio is eager (non-deferred) work.

---

## 6. THE INVERSE ATTACK (can the lifetime BEAT a same-facts fresh learner?)

Every row compares `LIFETIME` against `FRESH_ARENA` on the **identical arena**,
zero episodes vs all episodes. Preregistered: **I expect zero configurations
where `LIFETIME` beats `FRESH_ARENA` on correctness, and I expect at least one
where it LOSES.**

* **K-I1 `INV-POISON` (predicted LOSS -- age makes it worse).**
  Deliver stages 0..4. Query `G5`'s shape while stage 5's facts are absent:
  `compose_iter` returns 0, and `lt_query` sets the template's poison bit
  (`lt_tb(e)+8 = 2`). Deliver stage 5's 51 facts. Query `G5` again.
  **Prediction: `LIFETIME` `code=0` (DECLINE, cost 0) while `FRESH_ARENA`
  `ok=1` on the identical arena.** If measured, the negative result is
  *conditional*: age is never better and is sometimes worse, with the cause
  localised to a single monotone bit per goal shape.
* **K-I2 `INV-POISON-CLEAR`.** Clear **only** the poison bits (`lt_tb(e)+8`)
  on the same state and re-query. **Prediction: `ok=1`.** Confirms the bit and
  not the rest of the template is responsible.
* **K-I3 `INV-DEPTH`.** A 4-stage join (`GACF`) plus a 5-need goal `G2NF`
  (5 load-bearing stages) -- harder and longer than anything in LT3.
* **K-I4 `INV-REVISE`.** A stage that adds a second object under a relation the
  learner has marked functional (`lt_fun_observe`), then re-queries the old
  goal. Tests whether memoised arity/functionality beliefs help or hurt.
* **K-I5 `INV-CAP`.** Arena driven to its 1200-triple capacity so later facts
  are **dropped** (`lt3_add` refuses). Tests whether the aged learner's
  specialized index returns a stale answer where a cold learner recomputes.
* **Kill bar K-I**: at least one row with
  `LIFETIME ok < FRESH_ARENA ok` on the identical arena **or** an explicit
  statement that none was found across K-I1..K-I5.

---

## 7. ROOT-CAUSE LOCALISATION (charter 55: categorise, do not patch)

Nothing below is patched. Each row is a measurement that kills one candidate.

| bar | candidate | measurement | falsifies the candidate if |
|---|---|---|---|
| **K-LOC1** | (a) flat append-only arena | `LOC-REPACK`: identical fact set sorted by relation | answers **identical** to the unsorted arena |
| **K-LOC2** | (a) also: interference/duplication | `LOC-DUP3`: every fact duplicated x3 | answers **identical** |
| **K-LOC3** | (b) shape-only family decision | count needs whose bound family is field-inconsistent | count **== 0** |
| **K-LOC4** | (d) PLAN keyed by goal tag | enumerate the plan table: slots used, identity (canonical shape tag vs harness tag), `plan_new` refusals, over **6 distinct shapes** | `plan_new` refusals **== 0** and no goal loses its plan |
| **K-LOC5** | (c) no generalisation | K-GEN1 + K-GEN2 + K-GEN3 | K-GEN1=0 and K-GEN2=1 |
| **K-LOC6** | (e) NEW: shape-keyed sticky poison | K-I1 + K-I2 | K-I1 loses and K-I2 recovers |

---

## 8. KILL BARS, FROZEN

| id | bar |
|---|---|
| K1 | LT3 baseline reproduces sha `555792382303bb090403ce7152f77eba9388c1e9d088b3e7b64757d7ce76e4c9` |
| K2 | **D1 verified**: `plan_new` successes == 1 and plan loads == 8 in the LT3 replica |
| K2b | **D2 verified**: `GCEQ(G4,GACF) == 1` **or** D2 retracted in the report |
| K2c | **D3 verified**: LT3 replica `costep` (FROZEN) > `costq` (FRESH_ARENA) |
| K3 | oracle == declared for every non-hole goal, every row, W4 and W4F |
| K4 | `G0`, `G4`, `GACF`, `G14`, `G2NF` all correct under `LIFETIME` |
| K5 | `GX` DECLINES under `LIFETIME` and under `FRESH_ARENA` |
| K6 | determinism: **3/3 byte-identical stdout** |
| K7 | stdout **non-empty** (byte count > 0); no `_zag_raw_syscall` output path |
| K8 | every run behind `tnnwatch.sh reg <name> 900 ./m4`; timeout == FAIL |
| K9 | pure-Zag: no forbidden interpreter; compilation and run via `znc`/`zbuild.sh` |
| K10 | namecheck: the two learner entry points reach no goal builder, declared answer, oracle, or hole/rule code |
| K11 | hole integrity: `frz_lk1(arena, stage5) == 51` and the arena never contains `(115,1501,2501)` at any checkpoint |
| K-GEN1..5 | section 3 |
| K-R1..R5 | section 4 |
| K-K1..K3 | section 5 |
| K-I1..K5, K-I | section 6 |
| K-LOC1..K6 | section 7 |

**Adjudication fixed in advance.**

* **OVERTURN** iff `LIFETIME ok(G5, W4) == 1` (K-GEN1 fails) with
  `FRESH_ARENA ok == 0` (K-GEN1b). Then a learned rule substitutes for an
  absent triple and "smarter with age: NO" is **false as stated for the
  lifetime arm**.
* **NEGATIVE-CONFIRMED-SHARPENED** iff K-GEN1 holds (`ok == 0`) and K-GEN2/K-GEN3
  hold (a non-learning induction recovers the same answer from the same
  triples, and is falsifiable). Then the negative result stands and its cause
  is **(c)+(D2)**, not (a), (b) or (d).
* **NEGATIVE-WEAKENED** iff `LIFETIME ok(G5) == 0` and
  `STUPID-MAJORITY` also fails on W4 (K-GEN2 fails). Then the absent triple's
  value is **not** derivable from the same triples, the task is ill-posed, and
  the negative result is untested by this section.
* **NEGATIVE-RENDERED-CONDITIONAL** iff K-I1 loses. Age is never better and is
  demonstrably worse, with the cause localised to one bit.
* Any K-K2 regime with `APP-SEARCH < 1` is reported as a **partial positive on
  cost only** and does not touch the correctness adjudication.

---

## 9. DETERMINISM AND LIMITS PREREGISTERED

* 3/3 byte-identical stdout (K6). No randomness anywhere; every "choice" is a
  deterministic first/last-match rule.
* Wall clock limit **900 s** per run, fixed now, never extended (K8).
* **Nothing here clears L3.** RETRIEVE/VERIFY/COUNT are researcher-frozen
  templates (C397). The goal shapes are researcher-authored. `STUPID-MAJORITY`
  is a researcher-written baseline, not a learner, and is explicitly **not**
  evidence that TNN can generalise. A positive K-GEN1 would be evidence about
  the *frozen COGOPS substrate*, and even then only about substitution for a
  missing triple of a hand-built regular family.
* W4 has 10 stages, 520 triples, no noise, no drift, no perception, one
  lifetime, no revision except K-I4, and the hole is a single triple.
* If the machine is too loaded to finish in 900 s, that is recorded as
  FAIL/TIMEOUT, not retried longer.

## 10. SCOPE NOTE

M4 does not modify the frozen prefix (sha pinned, K1) and does not touch
`frz_episode` / `lt_query`. All new code is harness-side plus two purely
additive evaluator-side measures (`GCEQ`, `APP-MATCH`), none of which is
reachable from a learner entry point (K10).