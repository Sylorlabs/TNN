# ADDENDUM M4b (P1-MECHANISM) -- committed ALONE, before implementing A1-A6

Lane `p1_mech/`, branch `lane/p1mech`. Parent: implementation v1 `323832ae9`
(C610-C618), whose certified run is
`e401ed88fb5e30091d28f5b682f1b201266b7425e813e262bfb676d7cb47ce7e`, 15511 B, 3/3.

**No number in this addendum has been observed.** Every item below is read out
of the frozen source (`c8_learn.zag`, `lt3_support.zag`) and is falsifiable as
stated. No kill bar is moved; one bar from `ERRATA_M4.md` is **corrected
because it was based on a misreading of the frozen memory map**, and the
correction makes the bar harder, not easier.

---

## A0. WHY THESE SIX ITEMS

The v1 run answered the crux (K-GEN1: **no substitution**), confirmed the reuse
measure is unrepresentable at the structure level (K-R1c `STRUCTREL=0`), and
located a cost crossing at `N=3`. It did **not** explain *why* the answer cannot
depend on experience, and its cost curve has an unexplained feature: the aged
learner is 4.2x cheaper than a cold learner on the full arena at `N=10` yet
**exactly at parity** at `N>=3`. That inversion is the most interesting
unexplained datum in the lane and A2 tests it directly. A1 is the only
remaining mechanism by which age could be *strictly worse*, and v1 did not
reach it.

---

## A1. `K-I6c` -- SATURATE THE FROZEN 8-SLOT BIND TABLE FOR REAL

**v1's arm was not saturated.** `SAT_bindfree=1`: 7 of 8 slots used, because the
stress set only mints **7** distinct need signatures. Reading
`lt_sig_need` (`lt3_support.zag:579`): `nf*7 + k1*13 + k2*29 + k3*61`, so
distinct signatures come from distinct `(nf, link-kind-count)` pairs.

**The trigger, derived from source and not yet observed.** `lt_query`'s
template-miss branch (`lt3_support.zag:929-953`) mints one canonical tag per new
need signature and, **only in that branch**, evicts one *frozen* bind slot when
the frozen table is full. Two consequences:

1. A need signature already in the 16-slot `LT` store whose **frozen** slot has
   since been evicted by *another* goal takes **no** eviction of its own
   (`lt_bs_find` hits, so the mint branch is skipped).
2. `learn_bindings` (`c8_learn.zag:531-533`) then runs
   `if(bi<0){ bi=bind_new(L,tag); }` with **no check of `bind_new`'s return**,
   against a table that is full, so `bind_new` returns `-1`, and
   `bind_fam(L,-1)` reads `get32(L,12744-32+4) = L[12716]`. The second loop of
   `learn_bindings` (`c8_learn.zag:558-560`) then finds no slot for that need tag
   and **returns 0**; `compose_iter` returns 0; `lt_query` sets that template's
   poison bit (`lt_tb(e)+8 = 2`, `lt3_support.zag:1027-1032`); and from then on
   `if(st==2){ return 0; }` (`lt3_support.zag:906-909`) makes **every later goal
   of that shape DECLINE at cost 0 forever**.

**Prediction K-I6c.** With **>= 9** distinct bindable need-shape signatures
presented to one lifetime in a chosen order, the frozen table overflows,
`bind_new` returns `-1` for at least one need, that shape is poisoned, and the
aged arm DECLINES goals that `FRESH_ARENA`, on the **identical arena** with zero
experience, ANSWERS correctly. **Same facts, lifetime strictly worse.** Which
shape loses is decided by LRU order, i.e. by history.

**Kill bars.** `SATB_newneg` (count of `bind_new` returns of `-1`, measured by
`L[13232]` trial growth with no matching bind-slot creation) `>= 1`;
`SATB_ageddeclines` **>** `SATB_freshdeclines` on the same goal sequence. Both
reported whichever way they fall. A `SATB_ageddeclines == SATB_freshdeclines`
result is an honest FAIL of the prediction and is reported as one.

## A2. `K-I6d` -- CORRECTION TO `ERRATA_M4.md` E4's `K-INV-ARITH`

**E4 was wrong about the memory.** The frozen arena header
(`c8_learn.zag:10-26`) puts the CNT region at `8496` with
`cnt_fidx[16][64]` at `8628`, so `cnt_fidx[63]` occupies `12660..12723`, and
`cnt_prov_parent / ep0 / ep1 / nfacts / rev` occupy `12724..12743`. The 28 bytes
below the bind table are therefore **legitimate frozen cells**, not slack:

* `L[12716] = cnt_fidx[63][14]`, an ordinary COUNT index cell;
* `L[12728..12743] = cnt ep0, ep1, nfacts, rev`, all written by every episode.

So v1's measured `oobdelta = 213` on the first COUNT-bearing query is **legal
COUNT-index traffic**, and the v1 shell note calling it a possible
out-of-bounds write is **retracted**. This is a prereg error caught by reading
the map; it is recorded rather than quietly fixed.

**Corrected bar K-I6d.** The `bind_fam(L,-1)` path is a **cross-structure
corruption** -- it would write a family id (`0`, `1` or `2`) into
`cnt_fidx[63][14]` -- and is a defect only if, in the same query, `bind_new`
returned `-1` **and** `L[12716]` took a value in `{0,1,2}` **and** no COUNT
operation ran in that query. M4 snapshots `L[12716]` alone (not the 28-byte
block) before and after every query in the A1 arm and reports the conjunction.
A conjunction of `0` means the branch is **never taken**: honest negative, and it
also means A1's poisoning must have another route, which the report will state.

## A3. `K-K4` -- PROBE AMORTISATION: is the cost win knowledge, or a fixed setup?

v1's sweep queries each `(N,D)` cell exactly once, with a shape the aged learner
has never seen, so it measures `setup + execute`. v1's `REUSE4` queries shapes
the aged learner has seen, and finds a 1.08x-1.42x win. Both are consistent with
**"age amortises a one-off per-shape construction"** and inconsistent with
**"age reduces search"**.

**New arm.** Fix the world (10 stages, 519 facts). Probe the **same** goal `P`
times in a row on the aged learner, and `P` times on a cold learner handed the
identical arena, `P in {1,2,3,5,8,13}`. Record per-probe query cost for both arms.

**Predictions, fixed now.**
* **K-K4a** fresh cost is **constant** in `P` (it rebuilds the template and plan
  every time, `lt3_support.zag:906`/`944`).
* **K-K4b** aged cost **decreases** with `P` and `APP-SEARCH = costLT/costFA`
  falls below `1` at `P=2` and reaches a floor by `P=5`.
* **K-K4c** aged cost at `P=1` is **greater than or equal to** fresh cost at
  `P=1` (the setup is paid, not saved).
* **K-K4d** if `APP-SEARCH < 1` is **sustained** for `P>=2` while correctness is
  identical at every `P`, that is a **positive cost-only result for age** and is
  reported as charter-25 "reduce search" satisfied *in the amortisation sense
  only*. K-K4c failing (i.e. aged cheaper already at `P=1`) would mean the win is
  not amortisation and is reported as such.

**Kill bar.** The full `P` table plus the `P` at which `APP-SEARCH` first falls
below `1`. No bar on the values.

## A4. `K-LOC7` `PINFO` -- THE DECISIVE LOCALISATION (added; no bar weakened)

`try_family` (`c8_learn.zag:483-520`) returns `1` on a **shape test alone**:
`nf==2` binds RETRIEVE with no reference to the arena; `nf==4+` binds VERIFY when
`nf==1+ns*3`; `nf==3` with `aggop==1` binds COUNT. **The family decision never
reads the arena.** So the executed procedure should be a total function of the
goal's shape, and no lifetime experience can change it. v1 measured the
*consequence* (`misbind=0`, `APP-MATCH=1.0`, `STRUCTREL=0`) but never the
procedure itself.

**`PINFO(g,L,LT)`** = the per-need family vector actually bound for `g`, read
back as `bind_fam(L, bind_find(L, tag_i))` with
`tag_i = get32(LT, lt_bb(lt_bs_find(LT, lt_sig_need(g,i)))+4)`, encoded as a
single i32 (`f0*10000 + f1*1000 + f2*100 + f3`, `-1` per missing need).

**Prediction K-LOC7.** `PINFO` is **identical** across five settings that differ
in arena content and, in the last two, in the ANSWER:
`(a)` the true arena, aged; `(b)` the true arena, cold (`FRESH_ARENA`);
`(c)` `true arena + 600 distractors`; `(d)` `true arena + the hole triple
(115,1501,2501)` -- **the answer changes from 15 to 16 subjects**; `(e)` the
`GACF` 3-stage join. If `PINFO` is identical in all five, then the *procedure*
carries no information about whether the facts are present, and the negative
result is fully explained: **age cannot select a better procedure because the
procedure is chosen before the arena is consulted and never revised.**
Setting `(d)` is load-bearing: it is the one place where the arena and the answer
both change, and if `PINFO` still does not move, no appeal to "the learner could
have known" survives.

**Kill bar.** `PINFO` reported for all five; equality asserted or refuted.

## A5. `K-R1a` IMPLEMENTATION + TWO OUTPUT CORRECTIONS

* `GCEQ-GOAL(a,b)`: v1 never emitted it. Implemented by canonicalising `a` and
  `b` exactly as `lt_query` does (goal tag and per-need tags replaced, all
  fields copied through) and comparing all 512 bytes. **Expected 0**, and
  `ERRATA_M4.md` E2's retraction of D2 is confirmed only if it is 0.
* `REUSE2`'s `GCEQSTRUCT_*` fields printed `t4-t3` where the bar means the
  equality indicator. Fixed to `1/0`. The bar itself (K-R1b) was already
  evaluated correctly by the shell from the raw template indices, so **no verdict
  changes**.
* `K-LOC5` and `K-LOC6` verdict lines are now emitted explicitly rather than left
  to the reader to infer from the `GEN`/`INV` sections.

## A6. `K-I4` `INV-REVISE` -- REVISION PRESSURE

The only inverse-attack arm in the prereg that was never implemented. Deliver
stages 0..4 as usual, then add a **second object** under relation `1401` for
subject `100` (so the relation stops being single-valued), then re-query `G4`.

**Predictions.** `K-I4a` `FRESH_ARENA` answers the revised world; `K-I4b` the
aged learner either agrees (revision is harmless) or returns the **stale**
single-object answer from its memoised `lt_fun_observe` belief
(`lt3_support.zag:728`), which would be a **negative-transfer** row for K-I.
Either way the comparison is on the identical arena and is recorded.

---

## ADJUDICATION UPDATE (the rest of `PREREG_M4.md` section 8 is verbatim)

* **NEGATIVE-CONFIRMED-SHARPENED** stands unless A4's `PINFO` prediction fails.
* **NEGATIVE-RENDERED-CONDITIONAL** is *additionally* triggered by A1 succeeding
  (`SATB_ageddeclines > SATB_freshdeclines`): age is then demonstrably worse on
  the same facts, with the cause localised to one poisoned shape-bit.
* A **cost-only positive** for age (A3's K-K4b/K-K4d) does **not** touch the
  correctness adjudication and is reported separately, exactly as in the prereg.
* **Nothing here clears L3.** `PINFO` measures a frozen substrate; `STUPID-MAJORITY`
  is a researcher-written baseline. A K-K4 win is a statement about amortising a
  template, not about learning.