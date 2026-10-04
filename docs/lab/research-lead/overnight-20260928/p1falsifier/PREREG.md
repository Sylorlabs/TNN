# PREREG — P1-FALSIFIER (C660-C699)

**Lane** `p1falsifier`, branch `lane/p1falsifier`. Preregistered BEFORE any
implementation; no result observed at the time of writing. Frozen kill bars.
If a design flaw is found the affected test is marked **VOID** in
`ERRATA.md` and re-preregistered; a miss is never reinterpreted as a pass.

## 0. WHY THIS LANE EXISTS

Two claims were to settle charter 24/238 (does TNN become *more intelligent*
with age, or merely larger/slower/more cluttered?) and both were invalidated by
`lane/redteaw4` (C632-C647) for the **same** reason:

* **Claim A** (`lane/p1freeze` 222907a39 / 93817f97f, C585-C596) rested on
  `FRESH_ARENA` (zero learner state, full arena) answering a goal correctly
  while `LIFETIME` also answered. Red team: `lt_query`
  (`sup.zag:880`) opens with `lt_fresh` (`:899`), `lt_fresh` (`:765`)
  rebuilds `specialize_ret/vfy/cnt` **FROM THE ARENA** and **writes** learner
  state, and `lt3_main.zag:273` sets `T2[68]=1` to switch it on for that arm.
  `FRESH_ARENA` is therefore LIFETIME's exact code path with a different
  trigger: the row could not fail. The 62x->5.8x cost series moved at constant
  416 facts / 8 stages, so it is not a size sweep and the extrapolation to zero
  is withdrawn.
* **Claim B** (`lane/corefreeze` 2ceaa1748 / 82bfa0ae1) rested on
  `BASE-NOEP` reproducing `BASE-FULL` on 27/27 goals (MR). Red team: MR is
  **arm-agreement, not correctness**; MR was **13/27 until `L` was zeroed**, so
  the sign was set by an unaudited baseline; `BASE-NOEP` has a **pre-loaded
  arena**, so it *is* `FRESH_ARENA`; and the competence metric is admitted
  contaminated (records emit in PLAN order, `topo_g` takes the last
  zero-indegree need) with several prereg values wrong.

**The starting point, adopted verbatim:** *"Both A and B need the same falsifier:
a goal whose facts are NOT ALL PRESENT. Neither lane can produce it, and that is
the finding."*

## 1. WHAT IS FROZEN AND WHAT IS NEW

Frozen, copied **byte-identical** from `lane/p1mech` commit `2162252f2`
(`docs/lab/research-lead/overnight-20260928/p1_mech/`), sha256 recorded in
`run.sh` output and asserted by `run.sh`:

| file | role |
|---|---|
| `frz.zag` | the frozen COGOPS prefix (1831 lines) — learner + world primitives |
| `sup.zag` | LT3 lifetime support: template store, bind store, `lt_fresh`, `lt_query`, eviction |
| `wld.zag` | LT3 world W-LT3: 10 stages A-J, 1068 triples, goal grammar, declared answers |
| `life.zag` | FREEZE-ARENA episode layer: `frz_episode`, the only arena writer |
| `hlp.zag` | harness formatting helpers |

Not one byte of those five files is edited. Everything new is in
`fx_main.zag`. **The learner is reached only through `frz_episode` and
`lt_query`.** No file of any other lane is touched.

## 2. THE CRUX: A GOAL WHOSE FACTS ARE NOT ALL PRESENT, FIRST-CLASS

A goal is a goal record: a tag, `nn` needs with `nf` fields each, and links.
The *information* a need needs is exactly its `(relation, object)` pair: for a
`nf=2` RETRIEVE need it is the pair `(f0,f1)`; for a `nf=4` kind-2 fan-in VERIFY
need it is `(f2,f3)`; for a `nf=3` kind-3 COUNT need it is `f0`.

**SPEC** is a separately declared table `sp_rel(i)`, `sp_obj(i)` written in
`fx_main.zag` by hand, one line per goal, *not* read out of the goal record.
**CONTAINED(i)** is measured by scanning the arena for triples with
`(r,o) = (sp_rel(i), sp_obj(i))`. **GAP(i) = 1 iff CONTAINED(i) == 0.**

A goal is a **SPEC-GAP goal** iff `sum_i GAP(i) >= 1`. This is a property of
the *specification* versus the *store*, computed before any query is run, and it
is printed for every goal whether or not it is queried. It is not inferred from
a wrong answer.

**SPECMISMATCH** (bar `V0`): the declared SPEC must equal the `(r,o)` pairs
implied by the goal record, need by need. Must be 0 over all goals. If it is
non-zero the SPEC table is wrong and every gap number is void.

### 2.1 THE SPEC-GAP GOAL

`GGAP` = `lt3_goal4(7500, 1001,2001, 1202,2202, 1403,2403, 1404)`
(the `GACF` three-stage join A+C+F of `wld.zag`), with **the GAP arena** defined
as the full W-LT3 arena minus **every triple whose relation is 1403** (the
`k=2` relation of stage F: 8 triples, subjects 100..107).

`GGAP`'s SPEC requires 4 `(r,o)` pairs: (1001,2001) present 16, (1202,2202)
present 12, **(1403,2403) present 0**, (1404,2404) present 2. So GAP = 1 of 4,
and the absent pair sits in the middle of the chain: need 2 fans in from need 1
and need 3 counts over need 2's output.

**DECLARED ANSWER** for `GGAP` is the no-gap answer, hand-derived and
independently cross-checked by the evaluator (`V2`): `[16, 100..115][12,
100..111][8, 100..107][1, 1]`. It is declared, not fitted: it is what the goal
specifies, and the arena does not contain it.

**The crux claim under test (H0):** *a learner that has experienced the fact
cannot answer a goal that requires it, from a store that does not contain it.*
**H1 (the inverse):** *there is a configuration in which experience does help
correctness.*

## 3. ELIMINATING THE `FRESH_ARENA` CONTAMINATION

`FRESH_ARENA` is **not used as a competence contrast anywhere in this lane.**
The 2x2 factorial below replaces it. Everything is run on the **identical GAP
arena**; the four cells differ only in (i) whether the learner has experience
and (ii) whether the index-rebuild flag `LT[68]` is on.

| cell | learner state | `LT[68]` | role |
|---|---|---|---|
| `AGED_REB` | 1068 episodes, then the state snapshot | 1 | experienced, rebuild permitted |
| `AGED_STL` | same snapshot | 0 | experienced, no rebuild |
| `COLD_REB` | **all zero** | 1 | **DECLARED CONTAMINATED** — same code path as `AGED_REB`, reported only as a same-data control, never as a competence contrast |
| `COLD_STL` | **all zero** | 0 | the honest fresh learner |

`AGED_STL` is the only configuration in the whole program in which the frozen
`ret_spec/vfy_spec/cnt_spec` indices can address fact indices belonging to
triples that are **no longer in the arena** — i.e. the only configuration in
which learner memory could conceivably supply a value the store has lost. It is
new to this lane and it is the strongest available test of H1.

### 3.1 NOVICE ARMS CARRY NO PRE-LOADED ARENA AS EXPERIENCE

Rule 3 of the mission: a novice must genuinely have no experience.
* `NOVICE_EMPTY` (arm `A1`): `L` all zero, `LT` all zero, **arena genuinely
  empty (0 triples)**, `LT[68]=0`. Nothing pre-loaded at all.
* `COLD_STL` / `COLD_REB`: `L` and `LT` are **all zero before the query**. They
  are *handed the GAP arena*, which is **data the aged arm is also handed
  identically** — handing the same data to both arms is what makes experience
  the only difference. It is not a substitute for experience: bar `K4`
  requires `prewrites=0` and `rebuilds=0` for every novice cell, so no index is
  reconstructed from that data before the novice answers.

### 3.2 INSTRUMENTATION — every arm reports its reads and writes

Per arm, printed: `arena` (triples), `reads` (`R[84]`, fact-checks during the
query), `trials` (`R[4]`), `miss` (`R[28]`, need-shape cache misses),
`builds` (`R[72]`), `passes` (`R[44]`), `cost` (`R[84]`), `rebuilds`
(`LT[4]`, the `lt_fresh` counter), `prewrites` (non-zero learner cells in
`L`+`LT` **before** the query), `postwrites` (after), `poison` (`LT[40]`),
`bindex` (`LT[88]`, the BIND-exhaustion counter), `declineDelta` (`R[80]`).

**Bar `K4` (contamination kill).** Every novice cell must have
`prewrites=0`; `COLD_STL` and `NOVICE_EMPTY` must additionally have
`rebuilds=0`. A novice cell with `rebuilds>0` or `prewrites>0` is reported
`CONTAMINATED` and the competence contrast is **VOID**.

**Bar `K5`.** `AGED_REB` and `AGED_STL` must both have `postwrites>0`
(`prewrites>0` at the snapshot) and `reads>0`. An aged arm with `postwrites=0`
means the lifetime did not happen and the arm is VOID.

## 4. THE COMPETENCE METRIC (PREREGISTERED, ORDER-FREE)

The prior metric was contaminated: answer records are appended in **plan order**
(`execute_plan_iter`, `frozen_prefix.zag:1209-1213`) and `topo_g` takes the last
zero-indegree need, so any "needs satisfied before the answer" measure is a
function of plan order. Three replacements, none of which reads emission order:

* **EXACT** = 1 iff `ANS` equals `DECL` element-wise. Binary, order-free.
* **OFC-W (witness-satisfied need fraction).** For each need index `i` **in
  ascending need index** (a property of the goal record, not of execution),
  `W(i)=1` iff the answer record for need `i` equals what the declared procedure
  over the arena `A` returns:
  - `nf=2`: returned set `==` `{s : (s, sp_rel(i), sp_obj(i)) in A}`;
  - `nf=4` fan-in: returned set `==` `{s in previous need's returned set : (s,
    sp_rel(i), sp_obj(i)) in A}`;
  - `nf=3` COUNT: returned value `==` number of distinct arena objects `o` with
    `(s, sp_rel(i), o) in A` over the previous need's returned set.
  `OFC-W = (#i with W(i)=1)/nn`.
* **OFC-N (no fabrication).** 1 iff every value in `ANS` is a value the arena
  contains for the corresponding declared `(r,o)` (0 unbacked values).
* **OFC = OFC-W * OFC-N** (integer numerator `W` count times `N`, over `nn`).

Inputs are exactly `{A, G, ANS, i}`; no plan, no pass counter, no emission
position. `OFC` is therefore **not a function of emission order by
construction**, and bars `V1`/`V3` test that empirically too.

## 5. FROZEN KILL BARS

| id | bar | fail means |
|---|---|---|
| **V0** | `SPECMISMATCH = 0` over all 9 goals | SPEC table wrong; all gap numbers VOID |
| **V1** | `EXACT` and `OFC` identical on 3 deterministic permutations of the GAP arena (`AGED_REB`) | metric or answer is order-sensitive; OFC VOID as a metric |
| **V2** | declared answer == evaluator's independent computation, on all 9 goals over the full arena | `DECL` is wrong; `EXACT` VOID |
| **V3** | `OFC = nn` on `AGED_FULL` (the correct answer) | metric cannot recognise a correct answer; OFC VOID |
| **K1** | **CRUX / H0 falsifier.** `AGED_REB` `EXACT=0` on `GGAP` | H0 **REFUTED**: experience supplied the absent fact |
| **K1b** | all four 2x2 cells `EXACT=0` on `GGAP`, and `FAMV` identical across them | the gap is not first-class or family choice consults the arena |
| **K2** | `AGED_FULL` `EXACT=1` | test is vacuous (the goal is unanswerable anyway) |
| **K3** | `AGED_GAP+1` : adding exactly **one** of the 8 absent triples gives `EXACT=0` **and** an answer vector different from `AGED_GAP`'s | the goal does not actually depend on the absent relation; `GGAP` is not a valid spec-gap goal |
| **K4** | every novice cell `prewrites=0`; `COLD_STL`/`NOVICE_EMPTY` `rebuilds=0` | contamination not eliminated; competence contrast VOID |
| **K5** | both aged cells `prewrites>0` and `reads>0` | the lifetime did not happen; arm VOID |
| **K6** | `reads>0` on every cell whose arena is non-empty | instrumentation is not measuring |
| **K7** | **NT-A.** exists `K in {4,6,8,9,10,12}` with `aged_declines > cold_declines` on the identical arena | negative transfer not reproduced |
| **K8** | **NT-B.** at least one shape declines `EXACT=0` aged while a cold learner answers `EXACT=1` **on the identical arena and identical facts** | age-induced negative transfer not reproduced |
| **K9** | **NT-ORD.** the SET of shapes lost differs between two acquisition orders of the same goal multiset | losses are not chosen by history (LRU); p1mech's mechanism claim refuted |
| **K10** | **NT-PERM.** a shape lost at step K still declines when re-probed twice at the end | the loss is not permanent |
| **K11** | **FAMV** (per-need bound family vector) identical in `AGED_REB`, `AGED_STL`, `COLD_STL` | `try_family` DOES consult the arena; cause (b)/(e) refuted |
| **K12** | **PLAN.** two goals with identical structure but different tags build 2 distinct plans | plan is NOT keyed by tag alone; C501 refuted |
| **K13** | **POIS.** clearing the aged state's poison bits and re-querying a lost shape changes its outcome | the permanent decline is not the sticky poison bit |

A bar that fails is reported as FAIL. **No bar is moved after the fact.**

## 6. PREREGISTERED EXPECTATIONS (stated so they cannot be adopted after the fact)

* `H0`: all four 2x2 cells `EXACT=0` on `GGAP`. Expected, not required.
* `AGED_STL` (stale index into deleted triples) is expected to produce either
  the same wrong answer as `AGED_REB` or a *different* wrong answer. If it
  produces `EXACT=1`, `H1` is **confirmed** and this is the single most
  important cell in the lane.
* Cost ordering expected `AGED_REB` < `COLD_REB` on fact-checks (the index win)
  with `AGED_REB` > `COLD_STL` (the rebuild cost). If `AGED_REB` is not cheaper
  than `COLD_REB` the "index win" story is dead and that is reported.
* Negative transfer expected to appear between 8 and 10 distinct bindable
  need-shape signatures (p1mech's boundary was unbisected; `K` grid above
  brackets it).
* Expected answer to "any configuration where age helps correctness": **none**,
  with the single candidate being `AGED_STL`.

## 7. EXAMPLES-TO-CRITERION

`TTC-RESTORE`: starting from the aged snapshot and the GAP arena, restore the 8
triples of relation 1403 **one at a time**, querying `GGAP` after each
restoration, from a copy so the sequence is deterministic. `TTC-RESTORE` = the
number restored at which `EXACT` first becomes 1, or -1. Measured for `AGED_REB`
and for `COLD_STL` on the identical arena. Reported with the number of search
attempts (`trials`, `miss`, `builds`) and cost at each step.

`TTC-AGE`: the same measure with the aged state **replaced by a zero state**
(`COLD_STL` is that arm). Reported as the paired row.

## 8. LOCALISATION — DISCRIMINATING EXPERIMENT PER CANDIDATE CAUSE

| candidate | discriminating measurement in this lane | reading |
|---|---|---|
| (a) flat append-only arena | `V1`: 3 deterministic permutations (reverse, stride-7 rotate, sort-by-relation) of the GAP arena; `EXACT`/`OFC` invariance | if invariant, flatness/order is not the cause of the negative |
| (b) `try_family` binds on shape alone | `FAMV` = per-need bound family vector, compared across the 2x2 and against an **empty-arena** query of the same goal | if identical with and without any arena content, family choice is arena-blind |
| (c) no generalisation / substitution mechanism | `K1` + `DERIV`: a memory-free 30-line induction recovers `GGAP`'s declared answer from the **full** arena using the world's nested-prefix regularity, and returns a **different** answer on a world where that regularity is broken | derivable, not performed |
| (d) PLAN keyed by goal tag alone (C501) | `K12` | key is the canonical tag, so structurally identical goals do not share a plan |
| (e) core is a goal-record interpreter | `K11` + `PINFO`-style invariance of `FAMV` across all 2x2 cells including one where the answer changes | instruction selection is a total function of shape |
| (f) poison + bounded BIND table | `K13` + `K8`/`K9`/`K10` | discriminate sticky poison from BIND-slot loss |

## 9. EXECUTION

* Pure Zag for all computation. `. /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh`,
  `tnn_pure_zag_report` must print `VERDICT: PURE-ZAG-CLEAN`.
* `tools/zbuild.sh ./fx.zag` for every compile (it removes a stale binary first).
* **Every run** through `tools/tnnwatch.sh reg p1falsifier 900 ./fx`. Watchdog
  limit 900 s, **frozen, never extended**. Timeout = FAIL.
* **3/3 byte-identical** stdout required (`--rep 3` plus an explicit sha triple
  from three watchdog runs).
* `_zag_print`-based single-buffer flush (brief 4.0/4.1: `_zag_raw_syscall` is
  inert on this host). Output asserted non-empty.
* No binary is ever left unattended; `tnnwatch status` checked after every run.
* No file outside `p1falsifier/` is modified.

## 10. VERDICT RULE (frozen)

* `H0 REFUTED` iff `K1` passes (aged answers the spec-gap goal correctly).
* `H1 CONFIRMED` iff any arm answers `GGAP` `EXACT=1` while `COLD_STL` on the
  identical arena does not.
* Otherwise: `H0 CONFIRMED-NEGATIVE`, scoped to
  {goals over an append-only value-indexed triple store, goal shapes drawn from
  the frozen RETRIEVE/VERIFY/COUNT template set, worlds with <= 1200 triples,
  goal width <= 4 needs}. The verdict is **NOT** "architectural" unless a
  localisation bar shows the cause is in the frozen core rather than in the
  chosen world or template set.