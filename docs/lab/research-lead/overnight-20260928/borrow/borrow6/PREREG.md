# PHASE 6 -- BORROWED PRINCIPLES, HEAD TO HEAD

Lane `ownership`. Principles only. No subsystem is bolted on: every
candidate below is a *mechanism for one question* -- how does a stored
structure get selected for a situation -- expressed in the same substrate
as everything else, with no special machinery of its own.

## 0. WHY THIS HARNESS, AND WHY THESE FIVE

The audit found all four D-class bridges are the *same* defect: the
researcher decided how stored things relate to situations.

```
BR-1  input syntax        decides applicability
BR-2  failure policy      decides applicability
BR-3  mechanism origin    decides applicability
BR-4  aggregation label   decides re-instantiation
```

So the highest-value borrowed principle for this program is the one
that attacks fixed routing. But C1681 left a standing obligation: every
candidate must face a **fixed-heuristic control**, or the session will
produce another retraction.

## 1. THE HARNESS: TWO QUERIES THAT ARE MIRROR IMAGES

Same structures, same world, swapped correctness:

```
Q_C = (10,121) answer 11
      s2 -> 11          class 1  ELIGIBLE and CORRECT
      s0,s1 -> 12       class 1  ELIGIBLE and WRONG
      required: length 1

Q_A = (20,111) answer 22
      s2 -> 21          class 1  ELIGIBLE and WRONG
      s0,s1 -> 22       class 1  ELIGIBLE and CORRECT
      required: length 2
```

In both queries **both chain lengths are contract-eligible**. So
eligibility cannot decide; only preference can. And any fixed chain-length
preference is wrong on exactly one query by construction.

This is strictly harder than the C1691 harness: there, one query had only
one eligible length, so eligibility did half the work.

## 2. CONTROLS (from the start, not added later)

```
LEN1_only   prefer length 1, report failure if unavailable
LEN2_only   prefer length 2, report failure if unavailable
TIES        first eligible in enumeration order, no scoring at all
FO          best mechanism with its learned state erased
```

A candidate that does not beat LEN1, LEN2 **and** TIES has learned
nothing.

## 3. THE FIVE COMPETING PRINCIPLES

Stealed from: attention-like systems, Hebbian/plastic systems,
attractor systems, predictive coding, program synthesis.

### P-CONTENT  (attention principle, principle only)
Interaction is selected by content, not by a fixed route.
Key = the derived class signature of *every* value in the query, computed
by the learner's own class code. No declared interaction type.

### P-COPAIR  (content + co-occurrence)
As P-CONTENT, and additionally the set of structures co-usable with each
query value under the fact relation is folded into the key.

### P-LOCAL  (Hebbian principle: local co-use plasticity)
**No scope key at all.** A weight per ordered structure pair, updated
locally: on a correct trial, strengthen every pair used; on a wrong
trial, weaken them. Selection maximises summed pairwise weight along the
chain. Local rule, global effect, no coordinator.

### P-SETTLE  (attractor principle: settling)
Activation is spread over structures and iterated to a fixed point
rather than chosen by argmax. Stability, not score, is the criterion.

### P-MISMATCH  (predictive-coding principle: local mismatch drives change)
On a mismatch the structure does not merely lose weight: it writes a
*revision record* into learner state describing the observed
(input -> produced) pair, and selection consults those records directly.
No REVISE_MODE -- the record is data, and nothing branches on "am I
revising".

## 4. BASELINES

```
BASE-SCOPED   the current champion: credit in pools keyed by the C1681
              scope key, selected with the DAMPED rule  (expected 2 of 2)
BASE-GLOBAL   one credit pool for everything                (expected 1 of 2)
```

## 5. BARS

```
B1  3/3 identical sha256
B2  eligibility is identical across all arms (print the eligible-chain
    census) -- so any difference is preference, not eligibility
B3  every fixed control reported
B4  every principle reported
B5  FO reported
B6  at least one principle FAILS (a programme that cannot kill anything
    is not a test)
B7  no named cognitive mode in source
B8  L3 reported as a value
B9  WINNER reported, and reported as beating ALL THREE fixed controls or
    not at all
```

## 6. FALSIFIERS, DECLARED IN ADVANCE

```
F-CONTENT   the derived class signature separates the two queries
F-LOCAL     local pairwise weights need no global coordinator
F-SETTLE    settling converges and is not order-dependent
F-MISMATCH  revision records help without becoming a mode
```

Predicted: at least two of these fail. If all four pass, the harness is
too weak and that is reported as the finding.

## 7. WHAT "COLLAPSE INTO EXISTING SUBSTRATE" MEANS HERE

Per the per-principle checklist, each candidate must be reducible to
generic substrate operations. Concretely:

```
P-CONTENT  collapses to: derive a value's class, combine derived values
P-COPAIR   collapses to: derive classes + scan the fact relation
P-LOCAL    collapses to: read a weight, write a weight, argmax
P-SETTLE   collapses to: bounded iterate to a fixed point
P-MISMATCH collapses to: append a record, read records
```

If any candidate needs a type, flag, enum or branch that does not
already exist in the substrate, it fails the collapse test and that is
recorded against it.

## 8. DISCIPLINE

Pure Zag. `_zag_print`. 3/3, watchdog 240s. R3 and loop lints must pass.
Structures learned by verified search. No role vocabulary. Fixed
heuristic controls are mandatory.