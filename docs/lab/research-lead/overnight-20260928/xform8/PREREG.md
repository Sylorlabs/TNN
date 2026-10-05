# PREREG -- LEARNED TRANSFORMATIONS C1811-C1850

Lane `ownership`. Phase 8. Builds directly on the PHASE 7 finding.

## 0. WHY THIS SHAPE, GIVEN WHAT C1800 SHOWED

C1800 killed *learned generation by prior over proposals*: the learner
harvested kind-shapes of length 3-4 from training and could not propose
the 2-edit answers the test instances needed. The knowledge transferred
perfectly between disjoint distributions.

That is a failure of **priors**, not of learning. A prior is a fixed
enumeration shape. What C1800 did not test is whether the learner can
acquire a **procedure** -- a length-agnostic rule that decides the next
step -- which is a different object entirely.

C1800 also showed the researcher heuristic solves every instance in two
steps. So the bar is unambiguous and hard:

> Can the learner induce, from experience alone, a search procedure that
> matches a hand-written one on novel instances?

Not "beats" -- matching a 2-step optimal heuristic while never having
been told the rule is already a strong result. Beating it is not
expected and is not required.

## 1. THE LEARNED OBJECT

A **procedure**, stored as an executable table in learner state:

```
key   = size relation between current state and goal
        -1  current smaller than goal
         0  same size
        +1  current larger than goal
value = which edit kind most often reduced distance at that key
```

Three keys, three values. It is:

* **length-agnostic** -- it says nothing about how many edits remain;
* **label-agnostic** -- it says nothing about which labels;
* **induced** -- it comes from counted outcomes of the learner's own
  exploration, not from the researcher's heuristic.

This is the smallest object that is a procedure rather than a prior.
If this fails, prior-vs-procedure is not the distinction that matters.

## 2. INDUCTION (the learner's only input is its own search outcomes)

For each TRAIN instance the learner explores with random edits and
records, for each tried edit, `(size_relation, kind, distance_change)`.
It then sums `distance_change` per `(key, kind)` and keeps the argmax.

No heuristic, no goal-reading, no distance-function supplied. The
distance function is a plain symmetric difference and is the *scorer*,
exactly as a reward would be.

## 3. TRANSFER (the bar that matters most)

Held-out family, never seen, **no source change**:

```
labels shifted by 4  ->  the learner has only ever seen labels 1..4
capacity raised 2 -> 3
```

If the induced procedure is length- and label-agnostic it transfers
untouched. If it smuggled in label or capacity knowledge it fails.

## 4. ARMS

```
C   researcher heuristic      hand-written 1-step-lookahead greedy
T   learner procedure         the induced table, labels enumerated within
T-ERASED     table removed, fall back to random order
T-IRRELEVANT table induced from instances with unrelated goals
T-MISLEADING table induced from perturbed goals
T-FACTS      table induced from the fact table alone (goal membership),
             with no search outcomes at all
R   random proposals
A   exhaustive researcher finder
```

## 5. METRIC

Proposals evaluated per instance, **and** instances failed, reported
together. C1800 recorded that proposals alone are misleading when
success rates differ; both numbers are therefore mandatory here.

## 6. BARS

```
B1  3/3 identical sha256
B2  A solves every instance, original and shifted (world is solvable)
B3  T solves every instance
B4  T matches or beats C on proposals
B5  T solves all SHIFTED instances with no source change  <- decisive
B6  T beats T-ERASED
B7  T beats T-IRRELEVANT
B8  T beats T-MISLEADING
B9  T-FACTS is worse than T   (the table needs search outcomes, not facts)
B10 the induced table is printed, so it can be read directly
B11 no named cognitive mode in source
B12 L3 reported as a value
```

`B5` is decisive. `B4` is deliberately "matches or beats": the
hand-written heuristic is near-optimal here, so demanding that a learner
beat it would be demanding the impossible.

## 7. FALSIFIERS, DECLARED IN ADVANCE

```
F-PROC   a learned procedure transfers where a learned prior did not
F-INDUCE the table is recoverable from experience and not from facts
F-AGNOSTIC the table contains no label or capacity knowledge
F-CONTROL C is not doing hidden work; a hand-written rule would do the same
```

Predicted: `F-PROC` and `F-AGNOSTIC` survive. At least one of
`F-INDUCE`, `F-CONTROL` fails. If everything passes, the test is too
weak and that is reported.

## 8. DISCIPLINE

Pure Zag. `_zag_print`. 3/3, watchdog 300s. R3 and loop lints must pass.
The table is learner state, not source. No role vocabulary. Both the
proposal count and the failure count are reported for every arm.