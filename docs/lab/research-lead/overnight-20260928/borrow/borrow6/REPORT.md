# REPORT -- PHASE 6 BORROWED PRINCIPLES HEAD TO HEAD C1721-C1750

Prereg `borrow6/PREREG.md`. 3/3 sha256
`7129e4bf89448642b396e7267ae062a48d6f95a9bd2800c2454130253c0aa93e`
loop lint CLEAN.

## HARNESS

Two **mirror-image** queries in one world, correctness swapped:

```
Q_C = (10,121) answer 11
      s2 -> 11        class 1   ELIGIBLE and CORRECT
      s0,s1 -> 12     class 1   ELIGIBLE and WRONG      required: length 1

Q_A = (20,111) answer 22
      s2 -> 21        class 1   ELIGIBLE and WRONG
      s0,s1 -> 22     class 1   ELIGIBLE and CORRECT    required: length 2
```

Eligible-chain census, printed and identical in every arm:

```
Q0  eligible = 12, 11, 12   count 3
Q1  eligible = 22, 21, 22   count 3
```

So eligibility cannot decide anything. Only preference can, and any
fixed chain-length preference is wrong on exactly one query.

This is strictly harder than the C1691 harness, where one query had only
one eligible length.

## RESULTS

| mechanism | principle stolen | Q_C | Q_A | total |
|---|---|---|---|---|
| `LEN1_only` | control | 1 | 0 | 1 of 2 |
| `LEN2_only` | control | 0 | 1 | 1 of 2 |
| `TIES` | control | 0 | 1 | 1 of 2 |
| `BASE_scoped_damped` | C1681 champion | 0 | 0 | **0 of 2** |
| `P_LOCAL_hebbian` | Hebbian / plastic | 1 | 0 | 1 of 2 |
| `P_SETTLE_attractor` | attractor / settling | 0 | 1 | 1 of 2 |
| `P_MISMATCH_records` | predictive coding | 0 | 1 | 1 of 2 |
| `BASE_global_damped` | unscoped credit | 0 | 1 | 1 of 2 |
| `VALUE_SCOPED` | -- | 1 | 1 | **2 of 2** |

```
best fixed control  = 1 of 2
best principle      = 1 of 2
B9 principle_beats_all_fixed = 0
```

## FINDINGS

### 1. No borrowed principle beat a trivial control. All three failed.

Local co-use plasticity, attractor settling and mismatch-driven records
each scored **1 of 2** -- identical to `LEN1`, `LEN2` and `TIES`. Not one
of them produced a single correct answer that a fixed preference would
have missed. B6 is satisfied: the programme killed things.

### 2. The collapse test PASSED for all three, and that is not a compliment.

Per the per-principle checklist each candidate had to reduce to existing
substrate operations:

```
P_LOCAL     read a weight, write a weight, argmax
P_SETTLE    bounded iterate to a fixed point
P_MISMATCH  append a record, read records
```

None needed a new type, flag, enum or branch. So the principles cost
nothing in machinery -- **and bought nothing in capability.** A mechanism
that collapses trivially into substrate and does not help is not an
architectural result; it is a null with extra steps.

This is the useful shape of the negative: the ideas are not too heavy,
they are simply not the missing ingredient.

### 3. F-CONTENT IS FALSIFIED, AND IT UNDERCUTS MY OWN C1541 CLAIM

```
DERIVED SIGNATURE keys differ = 0
```

Both queries hash to signature key **14**: `class(10)=3` and
`class(20)=3`, with `class(121)=class(111)=2`. The two queries require
**opposite** answers and have **identical** type signatures.

So signature-keyed scoping scores **0 of 2** -- worse than unscoped
credit. And the reason generalises:

> **Type signatures are information-theoretically insufficient for
> routing.** Two situations can demand opposite actions while having the
> same type. No amount of contract learning fixes that, because the
> information needed to distinguish them is not in the types.

This narrows a claim I made earlier. C1541 showed that replacing a
surface router with derived contracts and probes works *when the
signatures separate the situations*. I stated it as a general
replacement for BR-1. That was too strong. The correct statement is:

```
contracts replace syntax-based routing  ->  TRUE
contracts replace routing in general     ->  FALSE
```

### 4. The only thing that works is memorisation

`VALUE_SCOPED` keys credit on the **raw query value**. It scores 2 of 2.
It is a lookup table indexed by input. It generalises to nothing it has
not already seen, and on an unseen value it has no opinion.

Which completes the argument into a real architectural constraint:

```
routing from TYPES        ->  insufficient, signatures collide
routing from VALUES       ->  sufficient, but it is memorisation
```

**This is the structural reason BR-1, BR-2 and BR-3 exist and cannot
simply be deleted.** A signature-based router cannot do the job, so the
researcher reaches for something value-specific: `route_line` reaches
for punctuation, `VALUE_SCOPED` reaches for the input. Both are
value-keyed. The bridge is not laziness; it is what happens when the
available abstraction is too coarse and something has to give.

That reframes the retirement queue. Deleting BR-1 without a *general*
substitute for type-based routing does not remove a bridge, it removes
the only thing making the bridge necessary and leaves the capability
unimplemented.

## WHAT BECAME MORE LEARNER-OWNED

Nothing from the three principles. They are recorded as falsified.

## WHAT BECAME MORE RESEARCHER-UNDERSTOOD

A great deal. The constraint above is the most useful thing this lane
produced, because it converts "delete the bridges" from a cleanup task
into a design requirement:

> The substrate needs an abstraction coarser than a type and finer than
> a raw value -- something that groups situations by *what they demand*,
> learned from experience, so that a new situation can be placed without
> having been seen.

`class(v)` is too coarse. `v` is too fine. The borrow programme should
look for principles that produce that middle granularity. Content
addressing is the obvious candidate and it did not work here, because
"content" was instantiated as the class signature. A content address over
*the full derived situation* rather than its type is untested.

## DEFECTS

One, and it is the interesting kind:

**I chose two mirror-image queries without checking that their derived
signatures differ.** The prereg's F-CONTENT was going to be tested, and
in fairness it was -- it failed. But `BASE_scoped_damped` scoring 0 of 2
is a *consequence of the collision*, not independent evidence against
scoping. Had I checked the signature separation first, that arm would
have been uninformative rather than negative.

Reported because it is the same error class as the earlier "expected
answer was class-2 and therefore unreachable" defect: **an arm that was
never going to measure anything, reported as if it had.**

## STANDING

```
C1681  query-scoped credit 2 of 2        HOLDS, but only where signatures separate
C1721  F-CONTENT falsified               signatures collide on mirror queries
C1721  3 borrowed principles falsified   all tie trivial controls
C1721  collapse test passes, utility fails  null with extra steps
C1721  VALUE_SCOPED 2 of 2               works, and is memorisation
L3 = 0
```

## NEXT FRONTIER, REVISED BY THIS LANE

The previous next-step was "can the learner choose its own credit scope".
This lane shows that is **not enough**, because scope choice cannot rescue
an abstraction that is too coarse. The revised question:

> Can the learner induce a grouping of situations coarser than raw values
> and finer than types, from experience alone -- so a situation it has
> never seen can still be placed correctly?

That is harder, it is the real remaining gap, and three borrowed
principles have now been shown not to answer it.