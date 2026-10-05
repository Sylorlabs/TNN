# PREREG -- FINDER OWNERSHIP C1761-C1800

Lane `ownership`. Attacks the standing boundary directly:

```
researcher defines candidate space / finder  ->  learner chooses instance
```

Goal: move from **learned ranking of researcher proposals** to
**learned generation of useful proposals**.

## 1. WORLD: capacity-constrained graph transformation

States are sets of integer labels drawn from `1..6`. An instance is
`(start, goal, capacity)`. The goal is exact set equality.

Generic primitives (finite, allowed, not domain knowledge):

```
INS(x)   valid if x absent and |S| < capacity
DEL(x)   valid if x present
MOV(x,y) valid if x present, y absent, |S| <= capacity
```

Why this is not a tiny finite menu:

* solutions have **varying length** (2 to 4 edits) across instances,
  so there is no fixed list of complete forms to enumerate;
* the same edit kind means different things in different instances;
* **greedy fails**: to reach `{3}` from `{1,2}` at capacity 2, adding
  `3` first is *illegal*, so the first move must be a deletion that
  looks like it makes things worse under a naive distance heuristic;
* the labels themselves are instance-specific, so a form cannot be
  memorised, only its *shape*.

## 2. INSTANCES

```
TRAIN  (6 instances, used for all learning)
  t0 start{1,2}      goal{3}      cap 2
  t1 start{1,2,3}    goal{4,5}    cap 3
  t2 start{2,3}      goal{1}      cap 2
  t3 start{1,3}      goal{2,4}    cap 2
  t4 start{4,5}      goal{6}      cap 2
  t5 start{1,2,3}    goal{5,6}    cap 2

TEST   (4 unseen instances, all measurement happens here)
  e0 start{1,2}      goal{4}      cap 2
  e1 start{2,3}      goal{5,6}    cap 2
  e2 start{1,3}      goal{2}      cap 2
  e3 start{1,2}      goal{3,4}    cap 2
```

## 3. ARMS

```
A  exhaustive researcher finder    enumerate sequences up to length 4
B  random generic proposals       uniform random sequences, same alphabet
C  researcher heuristic            1-step-lookahead greedy, no learning
D  learned proposal STATE         same candidate set as B, ordered by a
                                   learned prior instead of randomly
E  facts-only reconstruction      rebuild D's prior from the FACT TABLE
                                   alone, with no search history
F  learned transformation GEN     whole sequences proposed as units, whose
                                   edit-KIND shape is learned from past
                                   successes; labels instantiated generically
G  fresh learner                  F with an empty prior
H  misleading prior learner       F given prior shapes harvested from
                                   instances whose goals were perturbed, so
                                   the shapes are wrong for TEST
```

`D` and `F` are the contrast the phase exists for:

> `D` = learned ranking of researcher proposals.
> `F` = learned generation of useful proposals.

## 4. METRIC

**Proposals evaluated before first success**, summed over the 4 TEST
instances. A proposal is one candidate sequence handed to the verifier.
An arm that never succeeds scores `LIMIT` per instance.

Success is checked by the verifier only. No arm sees the goal before
proposing.

## 5. BARS

```
B1  3/3 identical sha256
B2  exhaustive finder A finds every TEST instance (world is solvable)
B3  greedy C is WORSE than A (the detour is real, not an artefact)
B4  F beats C on proposals      <- the phase's decisive bar
B5  F beats D                   <- generation beats ranking
B6  G (fresh) worse than F      <- the prior is load-bearing
B7  H (misleading) worse than F <- the prior is not arbitrary
B8  E (facts-only) worse than F <- F is not reconstructible from facts
B9  all arms reported, including failures, with no arm omitted
B10 no named cognitive mode in source
B11 L3 reported as a value
```

`B4` is the decisive bar. `F` beating only `C` would show learning;
`F` failing to beat `C` would mean a researcher heuristic suffices and the
learner adds nothing -- the C1681 retraction pattern, tested in advance.

## 6. FALSIFIERS, DECLARED IN ADVANCE

```
F-FINDER   learned generation beats a researcher heuristic
F-CAP      capacity-constrained edits defeat naive greedy
F-SHAPE    the useful knowledge is the edit-kind SHAPE, not the labels
F-PRIOR    the learned prior is load-bearing and not reproducible from facts
```

Predicted: `F-SHAPE` and `F-CAP` survive. At least one of `F-FINDER`,
`F-PRIOR` fails. If everything passes the arm is not a test.

## 7. DISCIPLINE

Pure Zag. `_zag_print`. 3/3, watchdog 240s. R3 and loop lints must pass.
Primitives are finite and generic. No role vocabulary. Fixed controls are
present from the start, not added later. Expected answers are used only by
the scorer, never by a proposer.