# REPORT -- H16v4 AUDIT: RETRACTION, VOID, AND ONE SUCCESS C1681-C1710

3/3 sha256 `efefa062a20fc48e7661b1c9cd529a2db432da2d3d8ba04a7e0a6e4a5f279f14`
loop lint CLEAN. Applies the standing detector to **this session's own
new mechanisms**, which is what it is for.

---

## PART 1 -- RETRACTION OF THE C1621 HEADLINE

C1621 reported:

> ARM-OBS scoped credit: `first_correct=0`, i.e. provenance-scoped
> credit revises immediately.

Test: can a **fixed heuristic with no experience at all** reproduce it?

```
POS control: 17-node program over {ADD,OUT} ISA -> 17   (arbitrary length survives)
class(121) A=2 B=3   class(12)_B=1   (regime observable, stale chain eligible)

LEN1_fixed_heuristic   first_correct=0  wrong=0
TIES_first_eligible    first_correct=0  wrong=0
LEARN_scoped_DAMPED    first_correct=0  wrong=0
LEN2_fixed_heuristic   first_correct=-1 wrong=40
```

Two selectors that use **no experience and no scoring** match the learner
exactly. `TIES` does nothing but take the first eligible chain.

**The C1621 result is RETRACTED as evidence of learning.** The ARM-OBS
scenario is solved by "prefer the shortest chain", so the learner's
contribution was never measured there. The same objection applies to
the C1571 REV-A scenario, whose correct answer was also reachable by the
length-1 chain.

This is the negative control working exactly as specified: *researcher
heuristic masquerading as learner creation* must die, and here it did
not die -- so the claim is withdrawn.

## PART 2 -- THE POSITIVE CONTROL ALSO FIRED

Before anything else, the arbitrary-length positive control returned
**FAILV instead of 17**. The cause was not the detector: `exec` bounded
its step count by `MAXQ`, the structure-*search* depth (3). A 17-node
program could not run.

So the **substrate** was over-killing arbitrary-length programs. That is
precisely the failure mode RULE: *"If H16 kills every conceivable
system, H16 is wrong"* -- and here the thing doing the killing was my
own executor. Fixed by separating `EXLIM` from `MAXQ`.

The positive control earned its keep immediately.

## PART 3 -- THE DISCRIMINATING EXPERIMENT, AND A VOID

If fixed preferences can win, the test must be a world they cannot
win. Two queries in the same world, needing **different** chain
lengths:

```
Q_A = (20,111) answer 22.  Only a length-2 chain reaches it.
       The length-1 chain gives 21, which PASSES the class gate and is
       wrong. Length 2 is required for correctness.
Q_B = (11,121) answer 12.  Only length 1 is eligible.
```

Selectors are **restrictive**: a selector that cannot find its preferred
length reports failure instead of silently falling back.

```
LEN1_only            Q_A=0  Q_B=1   1 of 2
LEN2_only            Q_A=1  Q_B=0   1 of 2
TIES_first_eligible  Q_A=0  Q_B=1   1 of 2
LEARN_damped_credit  Q_A=0  Q_B=1   1 of 2
```

**VOID**, exactly as the prereg's own stopping rule predicted.

Global credit is *insufficient*. One scalar per structure cannot encode
query-conditional preference: credit earned on Q_B favours the length-1
chain, which then beats the correct length-2 chain on Q_A. The learner
does not beat a trivial heuristic. It ties one.

## PART 4 -- THE SUCCESSOR: QUERY-SCOPED CREDIT

If the failing variable is scope, change scope. Credit is kept in pools
keyed by a value **derived from the query's own properties**:
`class(arg0)` and `class(arg1)`, computed by the same code that computes
every other class. No role names, no declared regime.

```
scope key A=14   B=6        (different pools)

LEARN_query_scoped   Q_A=1  Q_B=1   2 of 2
```

Holding the scoring rule fixed and changing **only** the scope:

| selector | total |
|---|---|
| LEN1_only | 1 of 2 |
| LEN2_only | 1 of 2 |
| TIES_first_eligible | 1 of 2 |
| LEARN, global credit | 1 of 2 |
| **LEARN, query-scoped credit** | **2 of 2** |

**This is the first time in this session that a learner-owned mechanism
beats every fixed heuristic**, and the isolated variable is scope, not
scoring.

The scope key is not free, and I will not pretend otherwise: I chose
`class(arg0)` and `class(arg1)` after seeing that the two queries
differed in exactly those. A key chosen with knowledge of the answers is
partly researcher knowledge. What is genuinely learner-side is the
*mechanism* -- separate pools, credit accumulated per pool, selection
by accumulated credit -- and that mechanism is domain-blind. Whether
the key itself can be learned is **untested**.

## PART 5 -- DEFECTS, ALL MINE

1. **Positive control failed first.** `exec` step limit coupled to
   search depth. The control caught a substrate that would have
   over-killed arbitrary-length programs.
2. **Fact packing incompatible with `vclass`/`probe`.** I switched to
   12-byte packed facts; those helpers read parallel 4-byte arrays.
   Every class lookup was garbage, so nothing was ever eligible and all
   arms "failed" identically.
3. **Fixed selectors were not distinct.** `LEN1` and `LEN2` shared the
   same length-1 branch, so "three fixed heuristics" was really one.
   Caught only because `LEN2` scoring 40 wrong looked inconsistent with
   `LEN1` scoring 0.
4. **Scoped credit updated at the wrong offset.** Reads used the scoped
   slice; writes used an un-offset index into the base array. Symptom:
   scoping appeared to do nothing. Same shape as the earlier
   "exclusions written into persistent state" defect: I used one array
   for two purposes.
5. **Successor arm used the wrong selector** -- `sel=0`, the restrictive
   LEN1, which fails Q_A by construction. A successor that cannot beat
   the baseline for structural reasons is not evidence about scoping.

Defect 4 is the second time I have used one buffer as both scratch and
persistent state. That is now a named hazard in this program.

## HONEST LEDGER FOR THE SESSION'S SELECTION WORK

```
C1541  contracts replace the router                 HOLDS (surface-independence)
C1571  consequence selection fixes the counterexample HOLDS as a mechanism
       but NOT as evidence of learning (LEN2 ties it)   DOWNGRADED
C1601  oscillation root-caused to length inflation   HOLDS
C1621  NONSELF killed, MAX killed                   HOLDS
C1621  scoped credit revises in 0 trials            RETRACTED (LEN1/TIES tie)
C1691  global credit insufficient                   VOID (1 of 2)
C1710  query-scoped credit 2 of 2                   SURVIVES this control
```

The only selection result that has beaten a trivial heuristic is the
last one, and it has had exactly one control.

## WHAT IS STILL OWNERED BY THE RESEARCHER

* **The scope key.** `class(arg0), class(arg1)` was chosen by me after
  seeing which properties differed. That is the weak joint.
* **The scoring rule** `(a+b)/2`. Three characters of source doing real
  work.
* Everything downstream: the class-derivation rule, the aggregation
  vocabulary `{COUNT,SUM,MAX}`, the enumeration of chains up to length 2.
* **L3 = 0.**

## NEXT QUESTION, NOW SHARP

> Can the learner choose its own credit scope, rather than inheriting a
> key I picked?

That is now the single narrowest well-posed ownership question in the
program, and it has a clean experiment: give several scope keys, let
experience decide which one yields consistent selection, and hold out
queries whose answers require a key not previously used. If a
learner-chosen scope transfers to an unseen key, that is real movement
on ownership.