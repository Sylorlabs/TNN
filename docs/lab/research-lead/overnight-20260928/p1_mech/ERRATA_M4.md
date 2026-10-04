# ERRATA M4 (P1-MECHANISM) -- committed ALONE, pre-implementation

Lane `p1_mech/`, branch `lane/p1mech`. Parent: prereg `9bc11edf0` (C600-C605).
No M4 number has been observed. Every change below is a **mechanism
correction made by reading the frozen source**, not a bar move, and each is
recorded with the code evidence that forced it. No kill bar is weakened; two
are strengthened and one new pair is added.

---

## E1. K-I1's TRIGGER IS WRONG. The predicted LOSS is unchanged in sign; the route is different.

**Prereg said:** "deliver stages 0..4, query `G5`'s shape while stage 5's facts
are absent; `compose_iter` returns 0; the poison bit is set; `LIFETIME` then
DECLINES while `FRESH_ARENA` answers."

**Why that cannot happen.** `execute_plan_iter` is declared `void`
(`cogops_learnosc2/c8_learn.zag:994`). `compose_iter`
(`cogops_learnosc2/c8_learn.zag:1045`) therefore returns 0 on exactly one
path: `learn_bindings(...) == 0`. **A missing fact never causes a decline.**
Evidence from the certified LT3 output already in the repository:
`J3 FRESH0 arm ok cost code 0 0 0 1 0 0` -- zero experience, empty arena,
`code=1` (answered), cost 0, `ok=0`. An empty world is answered, not
declined.

`lt_query` sets the poison bit only on `r == 0`
(`lt3_support.zag:1027-1032`), so the bit is set **only when a goal's shape is
unbindable**, which is a permanent property of the shape. Poisoning an
unbindable shape is therefore harmless, and K-I1 as written will **not
trigger**.

**Correction.** K-I1 is retained and is expected to report "did not trigger",
i.e. an honest FAIL of the preregistered route. The predicted LOSS is moved to
a new bar:

### K-I6 (new) -- BIND-TABLE SATURATION IS THE REAL NEGATIVE-TRANSFER VECTOR
`learn_bindings` (`c8_learn.zag:527-568`) inserts one frozen bind slot per
**distinct need-shape signature**, and the frozen table has **8** slots
(`bind_find`/`bind_new`, `c8_learn.zag:458-475`). `lt_query`'s template-miss
branch mints a canonical tag per need shape and stores it in the additive
16-slot `LT` bind store, but the tag is inserted into the **frozen 8-slot**
table only via `learn_bindings`. `lt_query` pre-evicts **at most one** frozen
bind slot per new need shape
(`lt3_support.zag:944-953`), so with more than 8 distinct need shapes in one
lifetime the frozen table saturates.

**Prediction (K-I6).** With >= 9 distinct need-shape signatures presented to
one lifetime: `learn_bindings` fails for some goal, `compose_iter` returns 0,
`lt_query` sets that shape's poison bit, and from then on **every** goal of
that shape declines at cost 0 regardless of arena contents -- while
`FRESH_ARENA`, holding the identical arena and zero experience, answers
correctly. **Same facts, lifetime strictly worse.** K-I6 also requires the
pair K-I2-style: clearing **only** the poison bits must restore correctness.

**Kill bar K-I6b (new, strengthened).** `learn_bindings` does **not** check
`bind_new`'s return value (`c8_learn.zag:532-533`:
`if(bi<0){ bi=bind_new(L,tag); }`, then `bind_fam(L,bi)` reads
`get32(L,12744+(bi)*32+4)` with `bi == -1`, i.e. **`L[12716]`**, 28 bytes
*below* the bind table). M4 must **count** how many queries take this branch
(`bi == -1` reaching `bind_fam`) and report it. If the count is > 0 the frozen
learner performs a **read and a write at a negative table index** on a
saturated bind table. That is a memory-safety defect in the frozen core,
distinct from every hypothesis (a)-(e), and must be reported as such rather
than attributed to age or to the arena.

---

## E2. D2 IS WRONG AS WRITTEN. Split into two measures; the conclusion is STRONGER.

**Prereg said:** "the learner's canonical goal bytes for a join and a
stage-local goal of the same shape are identical" (`K-R1`).

**Why that is false.** `lt_query` does `lt_copy(GC,G,512)` and then overwrites
**only the tags** (`lt3_support.zag:900,929-937,978-982`):
`set32(GC,0,...)` and `set32(GC,need_off(GC,i),...)`. Every *field* of every
need -- including the relation and object ids -- is copied through unchanged.
So the canonical goal record **does** carry the goal's relation ids, and
`GCEQ(G4,GACF) == 0` will be measured. **D2 is retracted as stated.**

**What survives, and it is a stronger claim.** The *executable structure* the
learner reuses does not carry them:

* `lt_sig_goal` / `lt_sig_need` hash `nf` and link kinds only
  (`lt3_support.zag:579-606`). All goals of one shape share one template.
* The template record stores `sig`, canonical tag, per-need canonical tags,
  hit counters and `lt_relsig` -- a **hash** of the relation content, never the
  ids (`lt3_support.zag:636-654`).
* The bind store stores `need-signature -> canonical tag` (`lt3_support.zag:660-677`).
* The frozen PLAN stores `(need index, need tag, family)` only
  (`c8_learn.zag:578-601`), and `plan_find` is keyed on the **canonical** tag
  `c8_learn.zag:570-577`, so plan identity follows shape, not the harness goal
  tag (adversary defect C501 is therefore **not** the operative defect here).

So two goals that require **different stages** are executed through the **same
structure**, and that structure contains no relation id anywhere.

### K-R1 is replaced by three bars
* **K-R1a `GCEQ-GOAL(a,b)`** = 1 iff the canonical goal bytes are identical.
  Expected **0**. Recorded, and D2 is retracted in the report.
* **K-R1b `GCEQ-STRUCT(a,b)`** = 1 iff the two goals resolve to the *same*
  template index, the same canonical tag and the same per-need canonical tag
  vector, and the same plan index. Expected **1** for
  `(G4,GACF)` and `(GACF,GSWAP)`.
* **K-R1c `STRUCTREL` (new)** = the number of cells in the template store, the
  `LT` bind store, the frozen bind table and the frozen plan table that hold a
  value in the world's relation-id range `[1001,1910]`. Expected **0**. If
  `STRUCTREL == 0` then applicability-to-a-specific-stage is not merely
  unmeasured, it is **unrepresentable in the learner's executable structure**,
  and charter 25's "recognise applicability" is refuted at the representation
  level rather than at the counter level. This is the decisive version of
  D2 and it is strictly stronger than what the prereg claimed.

---

## E3. D1's CORRECTION IS REFINED: LT3 has 2 goal shapes, and M4 measures 6.

Certified LT3 output on this branch reproduces
`555792382303bb090403ce7152f77eba9388c1e9d088b3e7b64757d7ce76e4c9`. In it
`STAGE ... plans pld ...` reads `plans=1` for every stage and `pld=8` at the
last, where `plans` is `L[13224]` (`plan_new` successes) and `pld` is
`R[76] = L[13228]` deltas, which `compose_iter:1071` increments on a **plan
load**. So: **one plan for the whole lifetime, zero evictions, zero drops.**
LT3's report reads `plans 1->10` and `pld 0,1,...,8` as growth and drops; both
are misreads, and its `Q9` "saturation is real" is void.

The reason is that all eight ordinary LT3 goals are the *same* four-need chain,
so they are **one** shape, plus the unbindable decline goal = **2** shapes
against a 4-slot table.

M4 therefore specifies **6 measured shapes** against the same 4-slot table,
listed in `PREREG_M4.md` section 2.3 plus `G3F` (a four-need chain ending in a
fan-in rather than a count): 4-need, 3-need fan-in, 5-need, 2-need, 4-need
ending in fan-in, and unbindable. K-LOC4 is unchanged and now has real
pressure to detect.

---

## E4. ADDITIONAL PREDICTIONS ADDED (no bar moved)

* **K-GEN6 (new).** `STUPID-MAJORITY`'s family/index identification must be
  derived from the arena alone (contiguity of relation blocks), never from the
  world definition. M4 emits the identified `rbase` and `k` for every
  `STUPID-MAJORITY` call so the derivation is auditable, and the function
  signature takes **only** `(A, r)` -- no world, no stage, no declared answer.
* **K-INV-ARITH (new).** Because `bind_off(-1) = 12716` and the bind table
  starts at `12744`, a saturated-table write lands 28 bytes below the table.
  M4 records `L[12716..12743]` before and after every query in the K-I6 arm
  and reports whether it changed. Unchanged => the branch is taken but benign;
  changed => an out-of-bounds write (report as a frozen-core defect).

## E5. WHAT IS NOT CHANGED

Adjudication section 8 verbatim. K1, K3-K11, K-GEN1-K-GEN5, K-R2-K-R5,
K-K1-K-K3, K-I2-K-I5, K-I, K-LOC1-K-LOC5 unchanged. The OVERTURN condition is
still exactly `LIFETIME ok(G5, W4) == 1` with `FRESH_ARENA ok == 0`. K-GEN2 and
K-GEN3 (the stupid baseline and its falsification world) are untouched: they
remain the load-bearing pair, and a K-GEN3 failure still voids section 3.