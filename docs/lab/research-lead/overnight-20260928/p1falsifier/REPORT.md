# REPORT — P1-FALSIFIER (C675-C699)

Lane `p1falsifier`, branch `lane/p1falsifier`. Prereg `27e82988c`, errata
`b29c2fbad`. Certified artefact `fx_run1.txt`, **10951 B**, sha256
`c3d002969585d26698ab96c829af95bbb1ba69285823b093e490cb32b210bd60`, **3/3
byte-identical** over three `tnnwatch reg p1falsifier 900 ./fx` runs, rc=0,
never extended. `tnn_pure_zag_report` = `PURE-ZAG-CLEAN`. Five frozen inputs
byte-identical to `lane/p1mech @2162252f2` (`frz 043b62b4 / sup 86857712 /
wld 0ecaf57d / life 2d955707 / hlp 1e6ea807`), asserted by `run.sh`. The learner
is reached only through `frz_episode` and `lt_query`. No other lane's file was
touched.

## 0. WHAT THE MISSION ASKED AND WHAT IS HERE

The red team's conclusion was *"both A and B need the same falsifier: a goal
whose facts are NOT ALL PRESENT. Neither lane can produce it, and that is the
finding."* **I produced one.** So the finding is no longer that neither lane can
produce it; it is what happens when you do.

## 1. THE GOAL WHOSE FACTS ARE NOT ALL PRESENT — HOW

Not a hole the learner answers wrongly. A first-class specification-versus-store
gap, computed and printed **before any query runs**:

* **SPEC** is a hand-written table in `fx_main.zag` (`fx_rel_of`/`fx_obj_of`)
  stating, per need, the `(relation, object)` pair the goal **requires**. It is
  not read out of the goal record.
* **CONTAINED(i)** is a scan of the arena for triples with that pair.
* **GAP(i) = 1 iff CONTAINED(i) == 0**; a goal is a SPEC-GAP goal iff any GAP.

Printed for all nine goals (`S1 SPEC` rows). Seven well-formed goals:
`contained=4 gap=0`. The eighth, `GGAP` = `GACF` (A+C+F) on the GAP arena, is
`contained=3 gap=1 gapneed=2` — **the whole `k=2` relation of stage F (8
triples, subjects 100..107) is deleted**, so the missing pair `(1403,2403)` sits
in the *middle* of the chain: need 2 fans in from need 1 and need 3 counts over
need 2's output. `gap_contained_1403 = 0`, full arena `= 8`.

* **V0 PASSES**: declared SPEC == goal-record-implied pairs,
  `V0specmismatch_wellformed7 = 0`.
* **V2 PASSES**: `V2all = 1` — the memory-free oracle agrees with the
  hand-derived declaration on all nine goals (where the declaration is
  `DECLINE`, the oracle declining counts as agreement).
* The declared answer for `GGAP` is the **no-gap** answer, records `16,12,8,1`.
  It is what the goal specifies; the arena does not contain it.

This is strictly harder than `lane/p1mech`'s hole goal, which deleted a single
triple: here an entire relation is gone and the correct answer requires knowing
that relation's witness count, which is a property of the relation, not of any
surviving fact.

## 2. FRESH_ARENA CONTAMINATION — ELIMINATED

`FRESH_ARENA` is used **nowhere as a contrast**. `lt_query` (`sup.zag:899`) ->
`lt_fresh` (`:765`) rebuilding `specialize_ret/vfy/cnt` from the arena and
writing learner state is replaced by a **2x2 on the identical GAP arena**, so
the two things redteaw4 confounded — experience and the rebuild trigger — are
separated:

| arm | learner state before query | `LT[68]` | `EXACT` | `famv` | reads | preW | rebuilds |
|---|---|---|---|---|---|---|---|
| `AGED_REB` | 1068 episodes | 1 | **0** | 0112 | 32876 | 523 | 1 |
| `AGED_STL` | 1068 episodes | 0 | **0** | 0112 | 3180 | 522 | 0 |
| `COLD_REB_CONTAM` | **all zero** | 1 | 0 | 0112 | 33920 | 1 | 1 |
| `COLD_STL` | **all zero** | 0 | **0** | 0112 | 33920 | **0** | **0** |
| `NOVICE_EMPTY` | **all zero**, arena **0 triples** | 0 | 0 | 0112 | 0 | 0 | 0 |
| `AGED_FULL` | 1068 episodes, FULL arena | 1 | **1** | 0112 | 41668 | 523 | 1 |
| `AGED_GAP1` | + **one** restored triple | 1 | 0 | 0112 | 33968 | 523 | 1 |

* **K4 PASSES.** Every novice arm has `preW=0` learner cells before its query;
  the two rebuild-off arms report `rebuilds=0`. The `preW=1` on
  `COLD_REB_CONTAM` is the arm's own `LT[68]` switch cell and nothing else.
  `NOVICE_EMPTY` has **nothing pre-loaded at all**: zero state, zero triples,
  zero fact-checks.
* **K5 PASSES**: both aged arms `preW>0` and `reads>0`. **K6 PASSES**:
  `reads>0` on every non-empty arena.
* **K2 PASSES**: `AGED_FULL EXACT=1` — the goal is answerable, so the negative
  is not vacuity.
* **K3 PASSES**: restoring exactly **one** of the 8 absent triples moves the
  answer vector (`ansn` 33 -> 34) and leaves `EXACT=0`. The goal genuinely
  depends on the absent relation.

**`AGED_STL` is new to the program** and is the only configuration in which the
frozen `ret_spec/vfy_spec/cnt_spec` indices can address fact slots belonging to
triples the arena no longer owns — i.e. the only configuration in which learner
memory could conceivably supply a value the store has lost. It does not supply
it. It does something worse: it answers a **different wrong vector**
(`ansn` 33 -> **5**, `ora=0`, so the answer does not even match a memory-free
evaluator running over the same arena) at **1/10th the cost** (3180 vs 32876
fact-checks). The frozen core has no staleness guard. Cheap, and silently wrong.

## 3. THE COMPETENCE METRIC

The prior metric was contaminated because answer records are appended in **plan
order** (`frz.zag:1209-1213`) and `topo_g` (`frz.zag:978`) takes the last
zero-indegree need. Replaced, preregistered, and **falsified by its own bars**:

* **`EXACT`** — the competence criterion: binary equality of the answer vector
  with the declared answer. Zero ordering dependence. (ERRATA E3: this alone is
  the competence criterion, for the reason below.)
* **`OFC-W`** — witness-satisfied needs, evaluated in **ascending need index**
  (a property of the goal record, not of execution), each need's expected
  record recomputed from `A` and the declared SPEC with set semantics.
* **`OFC-N`** — unbacked values. Inputs are exactly `{A, G, i, ANS}`: no plan,
  no pass counter, no emission position, so **OFC is not a function of emission
  order by construction**.
* **V1 PASSES**: `EXACT` and `OFC-W` are identical on three deterministic
  permutations of the GAP arena (reverse, stride-7, sort-by-relation).
* **V3 PASSES**: `OFC-W = nn` on `AGED_FULL`.

**ERRATA E3 was correct and is the metric's most useful output.** On
`NOVICE_EMPTY` (empty arena) `OFC-W = 4/4` while `EXACT = 0`: the learner
computes the arena-determined answer perfectly and that answer is wrong. A
metric that scores a confidently wrong empty-arena answer as perfect cannot be
the competence criterion — that would have repeated corefreeze's arm-agreement
error under a new key. Every row is therefore labelled **FAITHFUL-BUT-WRONG**
when `OFC-W = nn` and `EXACT = 0`, and `NOVICE_EMPTY` is the proof that the
distinction is real and needed: it answers `code=1` with **zero fact-checks** and
`ansn=5`. **There is no abstention.**

## 4. THE DECISIVE COMPARISON

**`TTC-RESTORE = 8` for the aged arm and 8 for the cold arm.** Restoring the 8
triples of relation 1403 one at a time, `EXACT` is 0 at every step 0..7 and 1
only at 8. Cost ratio `cold/aged` is **1.032x flat** across the whole curve
(33920/32876 at n=0, 42720/41668 at n=8). Search attempts are identical
(`trials=9`, `miss=0`, `builds=1`, `passes=2`) in every arm.

| quantity | `AGED_REB` | `COLD_STL` | ratio |
|---|---|---|---|
| EXACT on `GGAP` | 0 | 0 | — |
| examples-to-criterion | 8 | 8 | 1.00 |
| fact-checks (n=0) | 32876 | 33920 | **1.032x** |
| family trials | 9 | 9 | 1.00 |
| need-shape cache misses | 0 | 0 | — |
| passes | 2 | 2 | — |

Age buys **3.2%** on query cost, **0%** on examples, **0%** on search attempts,
and **0%** on correctness. Against 1068 episodes of setup that is never repaid.
`AGED_REB` is cheaper than `COLD_REB` (32876 vs 33920) — the index win is real
and is 1.03x, not the 1.11x-62x previously reported. `AGED_REB` is *not*
cheaper than `COLD_STL`... it is, but only because both rebuild nothing useful;
the honest statement is that the index win and the rebuild cost cancel to
within 3%.

## 5. THE INVERSE TEST — `K7`/`K8` **FAIL**, `K9`/`K13` PASS

Six goals with ten distinct bindable need-shape signatures, three acquisition
orders, six sequence lengths, **three arms** (`AGED`, `COLD_STL`,
`COLD_REB_CONTAM` — the contaminated arm run here specifically to test whether a
rebuild-on fresh arm is what made `p1mech`'s fresh row look competent).

**`K8lost = 0` in all 18 cells and `mstar = -1`.** The aged arm and *both* cold
arms return **identical `code` and identical `EXACT` on all six shapes, in every
order, at every length** (verified per goal in `S8 PERGOAL`).

| order | m | distinct sigs | aged wrong | COLD_STL wrong | COLD_REB wrong | declined set (all three arms) |
|---|---|---|---|---|---|---|
| fwd | 1 | 4 | 0 | 0 | 0 | — |
| fwd | 2 | 7 | 0 | 0 | 0 | — |
| fwd | 3 | **9** | 1 | 1 | 1 | `{3}` |
| fwd | 6 | 10 | 4 | 4 | 4 | `{3,5,6}` |
| rev | 6 | 10 | 3 | 3 | 3 | `{1,2}` |
| alt | 6 | 10 | 0 | 0 | 0 | `{4,5}` (both declared-DECLINE) |

What is real, precisely characterised:

1. **The boundary is the frozen 8-slot BIND table, not age.** Losses begin
   exactly when cumulative distinct need-shape signatures cross 8: at 4 and 7
   signatures nothing is lost; at 9 one goal is lost; at 10 up to four. Every
   arm crosses at the same point.
2. **The victims are chosen by ORDER — K9 PASSES** — `{3,5,6}` forward,
   `{1,2}` reversed, `{4,5}` alternating. LRU by presentation order is
   confirmed as the selection rule.
3. **But it is not age-induced.** A learner with zero experience, handed the
   identical arena and the identical goals, loses the *same shapes*. So
   `lane/p1mech`'s K-I6c — "four shapes decline forever while same-facts fresh
   answers correctly", presented as the programme's most important robustness
   finding — **is DOWNGRADED**: the fresh arm in that experiment cannot have
   been cleaner than `COLD_STL`, which loses identically. The most likely
   mechanism for their asymmetry is the one `redteaw4` identified for Claim A:
   a rebuild-on fresh arm. My `COLD_REB_CONTAM` cell shows the rebuild flag
   changes nothing here (identical to `COLD_STL` in all 18 cells), so if their
   fresh row was rebuild-on, the asymmetry must come from goal construction
   rather than from the trigger; either way the effect is not reproduced here.
4. **K10 PASSES (permanence)**: on re-probe twice at the end, every lost shape
   is lost again, identically.
5. **K13 PASSES**: clearing only the poison bits on the aged state recovers
   **2** of the losses (`poisonbits_cleared=3 recovered=2`). The remainder
   decline in the template-mint path before any template exists (`bindex` = the
   BIND-exhaustion counter), so **the permanent decline has two distinct
   mechanisms: sticky shape-keyed poison, and pre-template BIND exhaustion.**
6. `aged_bindex` reaches 2 and `aged_poison` 3 at the worst cell; both arms
   identical.

**No configuration was found anywhere in this lane where age helps
correctness.** The single candidate — `AGED_STL`, the stale index — returns a
wrong answer that does not even match a memory-free evaluator over the same
arena.

## 6. LOCALISED CAUSE — a discriminating measurement per candidate

| candidate | measurement | verdict |
|---|---|---|
| **(a) flat append-only arena** | V1: three deterministic permutations of the GAP arena; `EXACT` and `OFC-W` invariant, 1060 triples each | **EXCLUDED as the cause of the negative** |
| **(b) `try_family` binds on shape alone** | `famv = 0112` (RETRIEVE, VERIFY, COUNT) in **all seven arms**, including the empty arena and including one where the answer changes; BIND table contents identical (`5000:0 5001:1 5002:2`) in all seven | **CONFIRMED as the mechanism; it is arena-blind** |
| **(c) no generalisation / substitution** | K1 + `DERIV`: `regular_full=1`; the researcher-stated nested-prefix regularity predicts `16,12,8,1`, which is exactly `declared_recn`; on a regularity-violating world (`wcount_1402=20`) the evaluator returns `16,16,8,1` against the stated `12` | **CONFIRMED.** The answer is entailed by regularity evidence plus a stated regularity, and the learner performs no such inference. Per ERRATA E4, this does **not** show the regularity is learnable |
| **(d) PLAN keyed by goal tag (C501)** | K12 PASSES and **REFUTES C501 as stated**: a goal identical in every need field and link but with declared tag 7600 instead of 7500 builds **0** new plans and **loads** the existing one (`plansbuilt_A=1 plansbuilt_B=0`, `loads=1`, `trials=0`, cost 38464 vs 41668). `sup.zag:969` keys the plan on the **canonical shape** tag | **REFUTED as stated.** Reuse is shape-wide, which is maximal reuse and therefore the *maximum* negative-transfer surface |
| **(e) core as a goal-record interpreter** | K11 PASSES: `famv` invariant across a 2x2, a stale-index cell and an empty arena, one of which changes the answer | **CONFIRMED** — instruction selection is a total function of the goal's shape, not of the store |
| **(f) poison + bounded BIND table** | K13 + the order table above | **CONFIRMED as a capacity limit, and the limit is age-INDEPENDENT** |

The whole negative result reduces to one sentence, now measured rather than
argued: **experience cannot make the learner smarter here because experience
cannot change which procedure runs (`famv` invariant over seven arms), and every
value the procedure returns is read out of the store at query time — `ret_spec`,
`vfy_spec` and `cnt_spec` are value lookups through a relation index, not
learned content.**

## 7. BOUNDARIES

* One world: W-LT3, 10 stages, 1068 triples, no noise, no drift, one lifetime,
  one gap, one restoration curve. The gap is one relation of one stage.
* Goal width <= 4 needs (the frozen plan record is 56 B = 8 + 4*12).
* `GGAP`'s declared answer is the no-gap answer by declaration. It is
  cross-checked against the memory-free oracle (V2) but it is still a
  *declaration*; a world where the no-gap answer is itself the wrong
  specification would not be caught by anything here.
* For 3 of the 6 NT goals the memory-free oracle itself declines, so their
  declared answer is `DECLINE` and `EXACT` for them measures
  `lt_oracle`'s `apply_kind1` against `execute_plan_iter`'s `apply_kind1_g`
  rather than competence. This affects all three arms identically and so does
  not affect any aged-vs-cold comparison, but it does mean `EXACT` on those
  shapes is not a sound criterion in isolation.
* **`wld.zag:185-194` declares goal 7 with `nn=4` but writes only THREE need
  records**, so need 3 is read out of the link area. Goal 7 is **VOID** for V0
  (its mismatch is 2, entirely from this defect). Reported, not patched:
  `wld.zag` is a frozen file.
* `AGED_STL` is a **stale-index** condition, produced by disabling the
  freshness flag. It is not reachable through the ordinary episode path, which
  grows the arena and so keeps the flag satisfied. It is reported because it is
  the only configuration in which learner memory could have supplied a deleted
  value, and because a caller who disables freshness gets silent corruption at
  1/10 the cost.
* 3 NT goals whose answers are degenerate (fan-in over a count, kind-1 field
  substitution) were exercised on one instance each.
* Cost is `R[84]`, the learner's own fact-check counter, not wall clock.
* 900 s watchdog limit, never extended; runs take ~4 s. 3/3 byte-identical.
* **S11** (added mid-run, disclosed): two of my own call sites initially
  disagreed on the NT sequence. The cause was an index slip of mine, not the
  compiler — but because it could have been a heap-dependence defect that would
  invalidate every comparison here, I added a call-history-independence probe:
  the same sequence from the same pristine state under four heap perturbations
  (4/8/12/16 KB) gives identical `codes=110100` and `exacts=110000` every time.

## 8. VERDICT

**`H0 CONFIRMED-NEGATIVE. H1 NOT CONFIRMED. `K7`/`K8` FAIL. "Architectural"
is still not licensed.**

1. The crux experiment both prior lanes could not build **has now been built
   and run**. On a goal whose specification requires four `(relation, object)`
   pairs and whose store contains three, a learner with 1068 episodes of
   experience answers `EXACT=0`, exactly as a learner with zero state does, at
   a 3.2% cost difference and an identical 8-example criterion.
2. The contamination that invalidated Claim A is eliminated by construction:
   the rebuild trigger is a separate factor of the design, every novice arm is
   shown to hold zero learner state before its query, and `FRESH_ARENA` appears
   once, labelled contaminated, and is never a contrast.
3. The competence metric is order-free by construction and is shown to be
   necessary: on an empty arena `OFC-W = nn` while `EXACT = 0`. The prior
   metrics failed in opposite directions — one measured arm agreement, this one
   would have measured faithful execution — and both would have flattered the
   learner.
4. **The scope of the negative, stated exactly:** goals over an append-only,
   value-indexed triple store; goal shapes drawn from the researcher-frozen
   RETRIEVE/VERIFY/COUNT template set; worlds up to 1200 triples; goal width up
   to 4 needs; one lifetime; one relation removed. Within that scope the answer
   to charter 24 is: **no configuration was found where age improves
   correctness, and the cause is localised to (b)+(c)+(e) — procedure selection
   is a total function of the goal's shape, so experience cannot change which
   procedure runs, and every value that procedure returns is read from the store
   at query time.**
5. **Was the earlier "architectural" verdict overclaimed? Yes, and this lane
   makes the overclaim precise rather than merely rhetorical.** The word was not
   supported by Claim A's `FRESH_ARENA` row, which could not fail. It is still
   not supported here, because the localisation bars land on
   (b)+(c)+(e) — *shape-keyed procedure selection in a frozen template set over
   an append-only value-indexed store* — and every one of those three is a
   **choice the researchers made and can change**: the template set is
   researcher-frozen (brief §9, C397), the goal shapes are researcher-authored,
   and the store is a value index by construction. The honest word is
   **conditional**, not architectural. What *is* now architectural, and is
   demonstrated rather than asserted, is narrower and harder: **the learner's
   entire state is rebuildable from the store at a 3.2% constant factor in
   fact-checks, so state cannot carry information the store does not have; and
   the same is true of its failures — the 8-slot BIND table's losses are
   reproduced exactly by a learner with no experience at all.**
6. **`lane/p1mech`'s most important robustness claim is downgraded.** Age-induced
   negative transfer, characterised there as four shapes declining forever while
   a same-facts fresh learner answered correctly, does not reproduce: the aged
   and cold arms are identical in all 18 cells. What reproduces is *capacity*
   loss with *order-chosen* victims, which is arguably the more alarming finding
   because it means **a TNN instance's reachable goal set is decided by the order
   in which goal shapes happened to arrive, and no amount of experience helps.**

## 9. NEXT EXPERIMENT

1. **Attack (b)+(c) jointly with a substrate change, not a patch** — the single
   experiment that can turn the negative positive without changing the world.
   Give the frozen core a *second* family decision rule permitted to read the
   store (e.g. "bind VERIFY only if the relation has >= 2 witnessed objects"),
   preregistered, and re-run K1. If the crux flips, the cause is (b)+(c); if
   not, (c) alone. This is `p1mech`'s §9 item 3, which I endorse and did not
   attempt here because it modifies the frozen core and must be its own lane.
2. **Make the gap first-class in the goal language itself.** `GGAP`'s gap was
   constructed by deleting triples. A goal record that carries an explicit
   *sufficient-condition* clause, and a learner that must either satisfy it or
   abstain, would make the specification/store gap the executor's problem rather
   than the harness's — and would give the no-abstention finding (`ansn=5` at
   `reads=0`) something to fail against.
3. **Bisect the BIND boundary properly.** My grid moves distinct-signature count
   4, 7, 9, 10. The transition is between 7 and 9; a generator that adds one
   signature at a time (7, 8, 9) would locate it exactly and test whether the
   sticky-poison share or the BIND-exhaustion share dominates at the boundary.
4. **Test whether order-selected loss is order-*stable*.** Present the same
   multiset in 6 orders, record the lost set for each, and ask whether the lost
   set is a function of order alone. If it is, then "which knowledge a lifetime
   can still reach" is determined by arrival order and nothing else — a sharper
   statement than either prior lane's version, and directly actionable.
5. **Cost at scale.** Every cost number here is one world of 1068 triples and a
   1.03x ratio. The red team correctly withdrew p1freeze's 62x->5.8x series for
   not being a size sweep; an actual sweep in fact count and relation count,
   with the join load-bearing count held fixed, is still missing from the
   programme and is cheap to run on this harness.