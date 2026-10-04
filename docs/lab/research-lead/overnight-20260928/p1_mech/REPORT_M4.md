# REPORT M4 (P1-MECHANISM) -- the mechanism behind "Smarter with age: NO"

Claims **C634-C651** (implementation + certification). Prereg `9bc11edf0`
(C600-C605), errata `405be89a0` (C606-C609), addendum `a28192a1b` (C619-C630),
erratum `2162252f2` (C631-C633). Lane `p1_mech/`, branch `lane/p1mech`.

**Attacks** `C500-R1` / `FA1` / `C585-C596` (LT3 FREEZE-ARENA-2) and, in
parallel, `lane/corefreeze`'s BASE-NOEP result.

**Certified artefact.** `m4` stdout **27366 B**, sha256
`d4f5866e018eca6dd6c28d5f00f0de8d7142fbe87c1f350d00437c648fcb043e`,
**3/3 byte-identical**, 3-4 s per run behind `tnnwatch 900`.
`run_m4.sh` evaluates **86 kill bars mechanically, 86 PASS, 0 FAIL**, and exits
non-zero on any failure. Frozen prefix sha
`043b62b427e97f0e5f59f8d0de9ec2b8cfa506ecf4b271d971cdfee07c1b177c`; LT3 anchor
`555792382303bb090403ce7152f77eba9388c1e9d088b3e7b64757d7ce76e4c9` reproduced.

World W4: 10 stages, 520 triples, subject band 100-115, disjoint relation and
object bands per stage. Stage 5's index-0 relation is witnessed by subjects
100-114 only: **the triple (115,1501,2501) is never delivered and never written**
(K11: hole flag 0 at all 10 stage entries, 519 episodes, 51 stage-5 facts).

---

## 1. THE CRUX: can a learned rule substitute for an absent triple? **NO.**

| bar | result |
|---|---|
| **K-GEN1** `LIFETIME` on the hole goal | `ok=0`, `code=1` -- it **ANSWERED**, with the 15-subject vector the arena supports |
| **K-GEN1b** `FRESH_ARENA`, same arena | `ok=0` -- **identical**. Age changes nothing at the hole |
| **K-GEN2** arena-only `STUPID-MAJORITY` | recovers the declared **16-subject** answer exactly, `okW4=1` |
| **K-GEN3** same procedure, identical arena, W4F answer | `okW4F=0` -- **falsifiable** |
| **K-GEN4** memory-free oracle | `match=0` -- no generic frozen procedure recovers it |
| **K-GEN5** intact stage `G4` | aged 1, cold 1, oracle 1 -- the test is not vacuous |
| **K-GEN6** | `rbase`/`k` derived from arena contiguity alone; signature takes only `(A, r)` |

The value **is** derivable by a 25-line, memory-free, episode-free induction over
the same triples (K-GEN2), that induction **is** falsifiable (K-GEN3), and the
frozen executor **does not perform it** (K-GEN1/K-GEN4). This is the sharpest
form the negative can take: not "the information is missing" (LT3 proved it is
present) but "the information is reachable by induction and by nothing in the
learner".

`FRESH0` (zero experience, **empty** arena) returns `code=1` -- the frozen learner
**answers even with no facts at all**. There is no abstention.

**The negative result is not overturned.** No configuration anywhere in this lane
produced a correct answer by substitution.

## 2. THE REUSE MEASURE, CORRECTED (charter 25)

| quantity | stage-local `G4` | 3-stage join `GACF` | permutation `GSWAP` |
|---|---|---|---|
| `APP-STAGES` (ground truth) | 1 | 3 | 3 |
| naive `xw` | 1 | 1 | 1 |
| `GCEQ-GOAL` (canonical goal bytes) | **0** vs `GACF` | **0** vs `GSWAP` | -- |
| `GCEQ-STRUCT` (template/tag vector/plan) | **1** | **1** | **1** |
| `APP-MATCH` (field-consistency) | 4004 = 4/4 | 4004 = 4/4 | 4004 = 4/4 |
| `APP-SEARCH` (`costFA/costLT`) | 1.08 | 1.42 | -- |
| `APP-STUPID` ("did anything exist") | 1 | 1 | 1 |

* **Q10's verdict is confirmed**: the naive reuse signal is **1 everywhere** and
  cannot distinguish real transfer from reflexive reuse. Any reuse claim built on
  it is uninterpretable.
* **`ERRATA_M4c` D2 is retracted, and the replacement is stronger.** The goal
  *record* does carry the relations (`GCEQ-GOAL = 0`; `relsig` differs at all
  three: 212645 / 314899 / 76708, which is exactly why `xw` fires everywhere).
* **The executable structure carries none of it.** One shape signature (223318)
  and one template index serve the stage-local goal, the 3-stage join and the
  join's own permutation. **`STRUCTREL = 0`**: not one cell of the template
  store, the `LT` bind store, the frozen bind table or the frozen plan table
  holds a value in the world's relation-id range. `STRUCTREL_X = 0` excludes a
  hash coincidence. **Applicability-to-a-specific-stage is not unmeasured; it is
  unrepresentable in the structure the learner executes.**
* **`APP-MATCH = 4/4` is the problem, not the solution.** The learner recognises
  applicability *perfectly and vacuously*: its notion of "applicable" is a
  function of the goal's **shape**, so it matches everything of that shape and
  nothing distinguishes a 3-stage join from a stage-local goal. Charter 25's
  "recognise applicability" is **satisfied in form and empty in content**.

## 3. THE INVERSE ATTACK -- one configuration where age IS worse (K-I6c)

**NEGATIVE TRANSFER FOUND.** Ten distinct bindable need-shape signatures
(55 distinct need signatures over 16 goals x 4 passes = 64 queries) against the
**frozen 8-slot BIND table**:

```
SATaged_declines = 7      SATfresh_declines = 3      SAT_worse = 4
```

Four goal shapes **DECLINE at cost 0** in the aged arm and **ANSWER correctly in
the cold arm on the identical arena** (44-element vector). Mechanism, read out
directly rather than argued: `PINFO` digit **91** -- "canonical tag present, its
fROZEN bind slot gone" -- appears on **28 of 64** aged queries. `lt_query`
evicts a frozen bind slot **only in the template-miss mint branch**
(`lt3_support.zag:929-953`), so a need signature already resident in the 16-slot
`LT` store whose frozen slot another goal's mint evicted **never re-acquires
one**; `learn_bindings` then returns 0, `compose_iter` returns 0, and the
template's poison bit is set, after which `if(st==2){ return 0; }`
(`lt3_support.zag:906-909`) makes **every later goal of that shape decline
forever**. Which shape loses is decided by LRU order, i.e. **by history**.

**The negative result is therefore CONDITIONAL, not absolute.** Age is never
better and is *demonstrably worse* once a lifetime presents more distinct
need-shape signatures than the frozen bind table can hold.

Arms that found nothing (reported as NULLs, not passes):
* **K-I1** the preregistered poison route **did not trigger** (`poison=0`,
  `code=1`) -- exactly as `ERRATA E1` predicted: a missing fact is *answered*,
  never declined. 8 answered-wrong rows are all goals whose facts have not
  arrived.
* **K-I4 revision**: after the absent triple is added, aged `ok=1` == cold
  `ok=1`. No stale specialised index -- `lt_fresh` re-specialises on arena-size
  change.
* **K-I5 capacity** (arena driven to 1200): aged 1, cold 1. No stale answer.
* **K-I3 (5-stage join) is not a valid row**: the frozen plan record is
  56 B = `8 + 4*12`, so a goal of 5+ needs cannot be represented. Measured
  (**K-LOC8**): the 4 bytes immediately past plan slot 0 go **0 -> 4** across a
  five-need query, unchanged by the four-need control. A **real memory-safety
  defect in the frozen core**, reported not patched; it happens not to change
  that answer (the five-need goal is `ok=1`).

**No configuration was found where the lifetime BEATS a same-facts fresh learner
on correctness** -- across 24 sweep points, the crux, 13 amortisation probes and
6 `PINFO` settings, `okLT == okFA` everywhere.

## 4. COST AND DEFERRAL

**D3 confirmed, and the sign flips.** `costep=134940`, `costq=71455`,
`TOT-LT = 206395` against a cold learner's **query** cost of `20760`:
**age costs 9.94x**, not the 1.11x advantage LT3 reported. The LT3 replica makes
the accounting error explicit: episode cost alone (570846) is **13.4x** the
`FRESH_ARENA` query cost (42720).

**Where age *is* cheaper, and exactly why (K-K4).** Cold cost is **exactly
constant** at 20760 across 13 probes; the aged learner's **first** probe is also
20760 (**K-K4c: the setup is paid, not saved**), falls to 19203 at probe 2
(`APP-SEARCH = 0.925`) and is then **flat for probes 2-13** -- **it does not
compound**. Correctness is identical 13/13 in both arms: **the cost win is
cost-only**.

**The sweep's parity at N>=3 is an amortisation artifact, not an inversion.**
The sweep probes each shape exactly once, i.e. never past probe 1. Probed once:

| prior stages N | 1 | 2 | 3 | 5 | 8 | 10 |
|---|---|---|---|---|---|---|
| `costFA/costLT` at D=0 | 4.22 | 6.41 | **1.00** | **1.00** | **1.00** | **1.00** |
| at D=600 | 11.37 | 11.50 | **1.00** | **1.00** | **1.00** | **1.00** |

Age's advantage **grows with irrelevant facts** (4.22x -> 11.37x at N=1) and
**vanishes exactly** once the arena exceeds what the fixed specialised index
holds (16 relations; N=3 already means 30). For N>=3 the aged and cold costs are
**equal to the unit**, so specialisation contributes literally nothing. Age's
total advantage is therefore the sum of (i) an index that saturates above ~16
relations and (ii) a one-off per-shape template saving of 1.08x -- never enough to
pay back the episodes.

## 5. ROOT CAUSE, LOCALISED

**K-LOC7 `PINFO` -- the decisive measurement.** `PINFO`, the per-need family
vector actually bound, is **2010100 in all five settings**: aged; cold; +600
distractors; **hole-filled**; and the 3-stage join. The load-bearing control:
**adding the single absent triple moves the answer 40 -> 41 elements and
`ok 0 -> 1`, while `PINFO` does not move at all.**

> `try_family` (`c8_learn.zag:483-520`) returns 1 on a **shape test alone**:
> `nf==2` binds RETRIEVE with no reference to the arena; `nf==4+` binds VERIFY
> when `nf==1+3*ns`; `nf==3` with `aggop==1` binds COUNT. The procedure is chosen
> **before the arena is consulted and is never revised**.

That is the whole negative result in one sentence: **experience cannot make the
learner smarter because experience cannot change which procedure runs.**

| candidate | verdict | discriminating measurement |
|---|---|---|
| (a) flat append-only arena | **EXCLUDED** | `LOC-REPACK`: 155 facts re-sorted, **identical answer**; `LOC1b`: the hole decision is unchanged by arena order |
| (a') interference | not a test of (a) | `LOC-DUP3` changes the answer because `ret_gen` (`c15_base.zag:83-105`) appends per **matching fact** with no de-duplication -- multiplicity-sensitivity, not flatness |
| (b) `try_family` shape-only | **EXCLUDED as a defect; IDENTIFIED as the mechanism** | `misbind=0`, `APP-MATCH=4/4`, and `PINFO` well-formed and *invariant* everywhere |
| (d) PLAN keyed by goal tag (C501) | **EXCLUDED** | plan identity is the **canonical shape tag** (`c8_learn.zag:570-577`); 3 of 4 slots used across **6** shapes, 4 evictions, **no goal lost its plan** |
| (c) no generalisation | **CONFIRMED as the limitation** | K-GEN1 + K-GEN2 + K-GEN3: derivable by induction, not performed by the learner |
| (e) core as goal-record **interpreter** | **CONFIRMED and sharpened** | `PINFO` invariance across five settings including one where the answer changes |
| **NEW (f)** shape-keyed sticky poison + 8-slot BIND table | **CONFIRMED as the only negative-transfer vector** | K-I6c + K-I6d: 4 shapes aged-decline / cold-answer; `PINFO` digit 91 on 28/64 queries |

corefreeze's independent verdict -- *a competent, deterministic, domain-agnostic
goal-record interpreter, not a learner of capability* -- is reproduced exactly,
and M4 supplies the mechanism corefreeze could not measure: the interpreter's
**instruction selection is a total function of the goal's shape**.

## 6. CORRECTIONS TO THIS LANE'S OWN PRIOR WORK

* **ERRATA E4's `K-INV-ARITH` is RETRACTED.** The 28 bytes below the frozen bind
  table are **not** slack: `L[12716] = cnt_fidx[63][14]` and `L[12728..12743] =
  cnt ep0/ep1/nfacts/rev` (`c8_learn.zag:10-26`). The `oobdelta=213` reported by
  implementation v1 is **legal COUNT-index traffic**. The corrected, harder bar
  (bind_new == -1 **and** `L[12716] in {0,1,2}` **and** no COUNT op) is measured
  per query across all 64 saturation queries: **`L[12716]` never moves, end=0.
  The `bind_fam(L,-1)` branch is never taken**, and the poisoning route is
  `bind_find` returning -1 in `learn_bindings`' second loop.
* **ERRATA M4c**: two `m4_decl` cases were wrong. `m4_decl(8)`'s `[1,1]` reading
  misread the frozen code -- `apply_kind1` handles **kind-1** (scalar copy) links;
  the kind-2 fan-in is in `compose_iter` (`c8_learn.zag:703-722`), which walks
  **every** element of the source list and appends **every** passing subject. The
  independent memory-free oracle and the learner agree with each other against
  the declaration (`ANSV ANS_G3F_AGED n=44` == `ANSV OR_G3F n=44` !=
  `DECL_G3F n=41`), and the `oracle=1` field was certifying a wrong answer.
  After correction K4 G3F and K4 G2NF are `ok=1` and **K3 holds on every row
  whose facts are present**.
* **D1 and D3 from the prereg stand, verified**: LT3 used **one** plan for the
  whole lifetime (its "plans 1->10 / drops 0..8" is a misread of the plan-LOAD
  counter), and its cost multiple is not like-for-like.
* **Harness defects in `run_m4.sh`**: four of this lane's own checkers indexed
  past the label words and passed for the wrong reason; fixed before any verdict
  was issued. A PASS from the script is only meaningful after the fix.
* **The v1 run never completed certification.** `K4 G3F ok=0` was present in v1
  too and is explained by the declaration error above, not by a code change.

## 7. BOUNDARIES

* Nothing here clears L3. RETRIEVE/VERIFY/COUNT are researcher-frozen templates
  (C397); the goal shapes are researcher-authored; `STUPID-MAJORITY` is a
  researcher-written baseline, **not** evidence that TNN can generalise.
* W4 has 10 stages, 520 triples, no noise, no drift, one lifetime, one hole, one
  revision. The hole is a **single triple** in a hand-built regular family.
* Goal width is capped at **4 needs** by the frozen plan record (K-LOC8).
* The negative transfer is bounded by the **8-slot frozen bind table**; a
  lifetime presenting <= 8 distinct bindable need-shape signatures does not
  trigger it, and the boundary was not bisected.
* The 4-need-fan-in and 5-need shapes were only exercised on one instance each.
* Wall clock 900 s/run, never extended; 3-4 s used. 3/3 byte-identical.
* `PINFO` reads the learner's own structures and is evaluator-side; it is not
  reachable from `frz_episode` or `lt_query` (K10, unchanged).

## 8. VERDICT

**NEGATIVE-CONFIRMED-SHARPENED, and NEGATIVE-RENDERED-CONDITIONAL.**

1. The central negative **survives**: no learned rule substitutes for an absent
   triple, in any configuration tested. The cause is localised to (c) the absence
   of any generalisation mechanism, mechanised by (e): the frozen core is a
   goal-record interpreter whose **procedure selection is a total function of the
   goal's shape** (`PINFO = 2010100` in all five settings, including one where
   the answer changes). Experience cannot make it smarter because experience
   cannot change which procedure runs.
2. The negative is **conditional**: age is *demonstrably worse* once a lifetime
   presents more distinct need-shape signatures than the frozen 8-slot bind
   table can hold -- four shapes decline forever while a same-facts fresh learner
   answers correctly. This is the only configuration found where the two differ
   on correctness, and it makes the central result a statement about a
   **fixed-capacity, shape-keyed** structure rather than a law.
3. **Cost-only positive**, sharply bounded: age's query cost is 4.22x-11.5x lower
   while the arena holds <= 16 relations, exactly **1.00** above that, and a
   constant **1.08x** from the second probe of a shape onward. It never compounds
   and never repays the 9.94x episode cost.

## 9. NEXT EXPERIMENT

1. **Bisect the K-I6c boundary**: sweep distinct bindable need-shape signatures
   over `{4,6,7,8,9,10,12,16}` and locate the exact count at which the aged arm
   first declines a goal the cold arm answers. Predicted transition at 9 (the
   frozen table's 8 slots plus the one LT-store-resident signature that cannot
   re-acquire a slot). This converts "conditional" into a stated boundary.
2. **Order-dependence**: run the 16-goal saturation sequence under `k!`-class
   permutations and measure how many *distinct* shapes are lost. If the lost set
   is a function of LRU order, then **which knowledge a lifetime loses is decided
   by the order it was acquired in** -- a sharper statement of the architectural
   limit than "it cannot generalise".
3. **Attack (c) directly with a substrate change, not a patch**: give the frozen
   core a *second* family decision rule that is allowed to read the arena (e.g.
   "bind VERIFY only if the relation has >= 2 witnessed objects") and re-run K-GEN1.
   If the crux flips, the limitation is (b)+(c) jointly; if not, it is (c) alone.
   This is the single experiment that distinguishes the two, and it is the only
   route to an OVERTURN that does not change the world.
4. **Cost**: re-run the sweep with `P` probes per cell instead of 1, so the
   reported curve is the amortised curve. The current N/D grid measures only
   probe 1 and therefore reports parity where amortised measurement reports 1.08x.