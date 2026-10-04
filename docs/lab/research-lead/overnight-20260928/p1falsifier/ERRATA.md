# ERRATA to PREREG (p1falsifier) — issued BEFORE any implementation, BEFORE any result

Three clarifications. None moves a bar, none relaxes a bar, and none is issued
after a result. They remove ambiguities that would have made a bar
unevaluable or would have let a bar be reported in either direction.

## E1 — PREREG 5, bar K7: the K grid is re-specified

The prereg wrote bar K7 as "exists `K in {4,6,8,9,10,12}` distinct bindable
need-shape signatures with `aged_declines > cold_declines`". On reading the
frozen signature function `lt_sig_need` (`sup.zag:579`,
`sig = nf*7 + k1*13 + k2*29 + k3*61`) the number of distinct bindable
need-shape signatures reachable with a 4-need DAG is a **property of the goal
sequence I construct**, not a knob I can dial to an arbitrary K: needs with the
same `(nf, k1, k2, k3)` share one canonical tag and therefore one BIND entry.
So the exact set `{4,6,8,9,10,12}` is not necessarily hit, and the bar as
written would be **unevaluable**, i.e. it could pass or fail by accident of my
goal construction.

**K7 is re-specified, stricter in what it demands and evaluable by
construction:**

> **K7.** There exists a sequence length `m` in `{1,2,3,4,5,6,7,8}` such that
> `aged_declines(m) > cold_declines(m)` on the identical arena, where
> `declines(m)` is the number of the sequence's goals the arm answers
> `code=0`. The **cumulative count of distinct bindable need-shape signatures**
> at that `m` is **measured and printed**, and the transition point is
> **bisected** to the exact `m*` at which the aged arm first declines a goal
> the cold arm answers correctly (`m*` = min such `m`). `m*` and the
> corresponding distinct-signature count are the reported boundary.

Rationale for the change: a boundary stated as an exact count is strictly more
informative than "some K in a set", and a bar that is always evaluable cannot
be passed by accident.

## E2 — PREREG 5, bar K12: made direction-neutral

K12 as written made "2 distinct plans" the bar and "C501 refuted" the failure,
which prejudges the direction of the only interesting outcome. `lt_query`
(`sup.zag:969-985`) sets the goal tag to a **canonical** `cg = 6000+counter`
on a template miss and then keys the plan on `g_tag(GC)`, so two goals with
identical structure but different declared tags may well **share** one plan —
which would refute "PLAN keyed by goal tag alone" in the *stronger* direction
(shape-keyed, hence maximal cross-goal reuse and maximal negative-transfer
surface).

**K12 is re-specified as a pure measurement with both readings preregistered:**

> **K12.** Two goals identical in every need field and link, differing only in
> the declared goal tag, are queried in sequence on one state. Record
> `plans_built` delta and `templates_created` delta.
> * `plans_built = 1` -> the plan is keyed by **canonical shape tag**; C501 as
>   stated ("keyed by goal tag alone") is **REFUTED**, and the reuse surface is
>   shape-wide.
> * `plans_built = 2` -> the plan is keyed by the **declared** tag; C501 stands.

No bar is moved; the bar becomes a two-way readout.

## E3 — PREREG 4: OFC is a mechanism diagnostic, not the competence criterion

The prereg's section 4 is titled "the competence metric" and defines `OFC`.
Reading the frozen `exec_step_iter` (`frz.zag:1085-1161`) shows a consequence
I must fix **before** running rather than interpret afterwards: on a goal whose
arena is empty, `ret_gen` returns 0, so every expected set `E(i)` is empty, so
`W(i)=1` for every need and `OFC = nn` — while `EXACT = 0`, because the answer
does not match the declared answer. **`OFC` measures faithful execution of the
declared procedure over the store, not success.** A metric that scores a
confidently wrong empty-arena answer as perfect cannot be the competence
criterion, and reporting it as one would be the same class of error as
corefreeze's arm-agreement metric.

**Reclassification, preregistered:**

* **The competence criterion is `EXACT` alone** — the binary, order-free
  equality of the answer vector with the declared answer. `EXACT` was already
  in the prereg and is unchanged and unweakened.
* **`OFC-W`/`OFC-N`/`OFC` are reclassified as ORDER-FREE EXECUTION-FIDELITY
  DIAGNOSTICS.** Their job is the one the contaminated prior metric could not
  do: say, without reference to emission order or plan order, *which* needs the
  learner computed correctly **with respect to the store as it currently
  stands**. A row with `OFC = nn` and `EXACT = 0` is reported as
  **FAITHFUL-BUT-WRONG**, and that combination is a result, not a pass.
* Bars `V0`-`V3` are unchanged. `V3` (`OFC = nn` on `AGED_FULL`) remains the
  bar that OFC recognises a *correct* answer.

This makes the metric suite **stricter**, not looser: it adds a distinction
(faithful vs correct) that the prereg's single-number framing would have hidden.

## E4 — PREREG 8, candidate (c): the scope of DERIV is restated

The prereg said a memory-free induction "recovers `GGAP`'s declared answer from
the full arena". That is the wrong description and would have been an
overclaim. What is actually true, and what will be measured:

* `DERIV-PREDICT` computes `GGAP`'s declared answer from (i) evidence, read off
  the arena, that the world obeys the nested-witness-prefix regularity
  `w(0..9) = 16,12,8,4,2,2,2,2,2,2`, together with (ii) **that regularity as a
  researcher-stated constant** in the harness. It is a *predictor*, not an
  inference procedure.
* `DERIV-FALSIFY` runs the same predictor on a world in which one relation's
  witness count violates the regularity and requires the predictor to return a
  **different** value from the evaluator's independent computation, so the
  predictor is shown to be falsifiable rather than a tautology.

So the claim DERIV supports is: *the declared answer is entailed by arena
evidence of regularity plus a researcher-stated regularity, and the frozen
learner performs no such inference.* It does **not** show the regularity is
learnable, and the report must say so.

## E5 — PREREG 6: `AGED_STL` is added to the expected-cost ordering

No change to any bar. Recording explicitly, before the run, that
`AGED_STL`'s cost is **not predicted**: with a stale index the fact-checks
count depends on how many stale bucket entries the deleted triples leave
behind, and the frozen code has no staleness guard. Any `AGED_STL` cost number
is reported as measured with no expectation attached.