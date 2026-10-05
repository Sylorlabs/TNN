# REPORT -- PHASE 10: BR-4 NUMERIC MAP LOSSINESS C1651-C1680

Attack on the second bridge class from the audit. 3/3 sha256
`cd0f3d1bb561f750585957ee29eb8ca960fe546ded02d6b1be26ba07f7a32c5a`
bars lint CLEAN, loop lint CLEAN.

## THE AUDITED DEFECT

From `BRIDGE_MAP.md`:

```
t2_asm_count(v, plen, f)  ->  plen-1 INC cells
t2_asm_sum(vals, n)       ->  total INC cells, total = SUM(vals)
```

Both emit **the same shape**: a chain of INC cells whose length *is*
the number. `promote_graph` persists relation, subject, graph root,
promo index, answer, and DEP edges -- but **not which aggregation
produced the length**.

So a learned numeric MAP is lossy. It records the answer, not the
operation that generalises to a new input. `xio_stage_exec` therefore
substitutes the one aggregator that exists:

```
xio_core.zag:95-99
  let len:i32=t2_chain(W,x,rel,vv2,ff2);
  let root2:i32=t2_asm_count(W,vv2,len,ff2);
```

Documented consequence: `sum(103)=15` reported as `count(103)=2`.

## DESIGN

Three aggregations, so a **generic executor is distinguishable from a
hardcoded fix**. If the treatment merely hardcoded SUM, COUNT and MAX
would break.

```
subject 103, relation 71 -> objects 6, 9     COUNT=2  SUM=15  MAX=9
subject 103, relation 72 -> objects 301..303 COUNT=3
subject 103, relation 73 -> objects 3, 8     COUNT=2  SUM=11  MAX=8
```

All three MAPs have the identical graph shape (an INC chain). They
differ **only** in the recorded aggregation -- which is exactly the
information the audit said was missing.

## RESULTS

```
BASE (no provenance, count bridge)
  SUM   want 15  got 2      <- the audited bug, reproduced
  COUNT want 3   got 3      <- right by coincidence
  MAX   want 8   got 2      <- wrong
  1 of 3

TREAT (MAP retains its own aggregation)
  SUM   want 15  got 15
  COUNT want 3   got 3
  MAX   want 8   got 8
  3 of 3

FO (provenance erased)   SUM -> FAILV     facts alone do not restore it
no-facts subject 999     -> FAILV         graceful
```

## FINDINGS

**1. BR-4 is a representation defect, and representation is learner
state.** One generic executor -- read the relation and the aggregation
out of the MAP record, gather, build, run -- handles all three
aggregations. The count bridge handled one of three, and that one only
by luck.

This is the second bridge class with a measured generic replacement,
and the two are different in kind:

```
BR-1  wrong because applicability was owned by source  -> fix by deriving it
BR-4  wrong because the information was ABSENT         -> fix by retaining it
```

**2. Facts alone are insufficient.** With provenance erased the SUM arm
returns FAILV rather than silently reverting to COUNT. The failure is
loud, which is the desirable property: a lossy record cannot quietly
answer a different question.

**3. Declared resource limit.** An INC chain is one node per unit of
value, so a large sum exhausts the node store and returns FAILV. That
is a real limitation of representing the number as chain *length*, and
it is inherited from the audited design rather than introduced here.
Recording `906` by chain length is absurd; the honest fix is a
different numeric representation, which is future work and is exactly
the kind of thing that should become a learner decision rather than a
frozen choice.

## THREE DEFECTS, ALL MINE

1. **Execution step limit coupled to search depth.** `exec` bounded
   steps by `MAXQ`, which is the structure-*search* depth (3). An INC
   chain of 16 nodes never reached its `OUT` and returned FAILV. Symptom
   was indistinguishable from a wrong aggregation. Fixed by separating
   `EXLIM` from `MAXQ`.
2. **Frame slot pre-loaded with the subject.** I passed `subj` as both
   frame inputs, so the counter started at 103 and every answer was off
   by 103 (`105`, `106`). Symptom looked like an aggregation bug.
3. **Aggregation read from a fixed slot** rather than from the MAP
   record, so only the first MAP was correct. Symptom: `COUNT` failed
   and `MAX` returned the SUM `11`. This is the most interesting one,
   because the fix *is* the treatment -- reading the mode from the
   record is precisely what makes the executor generic.

Defect 3 is a good example of a bug and a hypothesis having the same
shape. It was fixed by making the code express the claim.

## WHAT THIS DOES NOT ESTABLISH

* The treatment was tested on **three** aggregations in **one** world.
  `{COUNT, SUM, MAX}` is a finite vocabulary, and a finite vocabulary of
  aggregation labels is close to the menu pattern H16v3 exists to kill.
  Whether a MAP can retain a *general* aggregation descriptor rather
  than a label from a list is **untested** and is the obvious next
  question for this bridge.
* No transfer test, no ablation of the gather step, no adversary.
* **L3 = 0.**

## STANDING

```
BR-1  replacement MEASURED (C1541)
BR-2  blocked on selection
BR-3  deletable with BR-1/BR-2
BR-4  replacement MEASURED (this lane): retain the aggregation in the MAP
BR-5  keep, already the right shape
```

Two of four D-class bridges now have measured generic replacements,
and they needed *different* fixes -- one derived, one retained. That
distinction is worth carrying into the deletion queue: "delete the
bridge" is not one kind of work.