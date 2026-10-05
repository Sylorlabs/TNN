# REPORT -- SELF-ORGANIZING ROLES FROM USE C1861-C1890

Lane `ownership`. Phase 9. 3/3 sha256
`4eb8e817f9c138d81b5424f4bd555f3a8c651952cd71c8a20422005d522c14e8`
loop lint CLEAN.

## WHAT WAS ATTEMPTED

No role names anywhere in the program. Structures obtain functional
role from **use**: each structure accumulates the situations in which it
actually succeeded, and recruitment is by overlap of those
situation-features.

Features are structural only:
```
class(arg0)   class(arg1)   arg0_in_goal   arg1_in_goal
```

Three decision rules on identical candidate sets:

```
TYPE      derived class of the arguments only     (the C1681 approach)
FREQ      most frequently successful structure     (a heuristic)
AFFINITY  best overlap of learned success-features (the claim)
```

## RESULTS

```
learned from the training queries:
  s0 successes=2  recorded_situations=2
  s1 successes=2  recorded_situations=2
  s2 successes=4  recorded_situations=4

correct by rule (Q1 Q2 Q3 train, Q4 HELD OUT):
  TYPE       0 0 0 0    total 0 of 4
  FREQ       1 1 1 1    total 4 of 4
  AFFINITY   0 1 0 0    total 1 of 4

affinity_beats_freq = 0
affinity_beats_type = 1
repurposes_heldout_query = 0
```

## FINDING 1: THE LEARNED AFFINITY IS WORSE THAN COUNTING

`FREQ` gets **4 of 4**, including the held-out query. `AFFINITY` gets
**1 of 4**. The use-derived mechanism I built is beaten by simply
counting successes.

That is now the **fourth** independent case in this program of the same
shape:

```
C1681  selection   a fixed heuristic ties the learner
C1800  generation  a fixed heuristic beats the learner
C1850  procedure   a fixed heuristic beats the learner
C1860  affinity    a fixed heuristic beats the learner
```

Four different learner mechanisms -- contracts, generated shapes,
induced procedures, learned affinities -- and four times the simple
heuristic matched or won. That is a much stronger empirical regularity
than any single negative, and it is the most important thing in this
report.

The honest reading: **counting is a very strong baseline for
applicability, and every mechanism I have built to be smarter than
counting has been worse than counting.**

## FINDING 2: THE WORLD COLLAPSED TO A SINGLE GENERALIST

The repurposing bar was unmeasurable, and the reason is a world-design
defect on my part.

The diagnostic dump shows `s2` (a one-op increment) solves everything,
including the held-out query, by **composing with itself**:

```
chain(2,-1) -> 11    (Q1, length 1)
Q2  s2(11) -> 12
Q3  s2(20) -> 21, s2(21) -> 22
Q4  s2(20) -> 21, s2(21) -> 22
```

So there is exactly one workhorse and therefore **no role difference to
repurpose**. A test of repurposing needs at least two structures that are
genuinely irreplaceable in different contexts; I did not build one, so
`repurposes_heldout_query=0` measures nothing.

This is the third time in this program I have built a world that could
not measure its own bar (the class-2 unreachable answer, the label-bounded
alphabet, and now a universal structure). It is becoming a pattern
worth naming:

> **A harness that admits a universal solution cannot test selection at
> all.** Selection only exists where competence is distributed.

## FINDING 3: TYPE MATCHING IS THE WEAKEST, CONFIRMING KILL-6

`TYPE` scores 0 of 4, the worst of the three. KILL-6 (C1721) showed type
signatures collide on situations demanding opposite actions, and this is
the same result from a different direction: type information is
available, always applicable, and never discriminative.

## FOUR DEFECTS, ALL MINE

1. **`has()` scanned only 8 bits** while labels reach 22 (bit 21). Every
   goal above label 8 silently reported "not a member", so nothing ever
   matched and all three rules scored 0. Symptom: a uniform, suspicious
   zero across every arm.
2. **Compared a produced value against a goal mask.** `11 != bitof(11)
   = 1024`. Goals are sets, chain results are values; I compared them
   as integers.
3. **The learning loop only tried `(a,-1)` and `(a,a)`**, so the
   `(s0,s1)` chain that Q3 needs was never attempted.
4. **The `aff` buffer was undersized** (`z_alloc(32*8)` = 256 bytes) for
   indices up to `(2*8+7)*24+12 = 564`.

Defects 1 and 2 are the same failure mode as the earlier episodes:
**a harness where nothing matches looks like a negative result.** Both
were caught only by dumping the intermediate values rather than reading
the bars. That is now the fourth time. The practice is:

> If every arm scores identically zero, suspect the harness before
> believing the result.

## WHAT BECAME LEARNER-OWNED

Nothing. Affinity is a mechanism I built and it lost to counting.

What the lane *does* establish, negatively and usefully:

```
use-derived roles       NOT better than counting success
type-derived roles      worse (confirms KILL-6 from a new direction)
a generalist structure  defeats any role-separation test
```

## STANDING

```
roles from use beat frequency            NO
roles from use beat type                 YES
repurposing demonstrated                 NO  (bar unmeasurable; world collapsed)
L3 = 0
```

## WHAT THIS ADDS TO THE PICTURE

Combined with the four-lanes pattern above, the program's central
empirical claim is now:

> **Across four different attempts to make selection learner-owned --
> contracts, generated shapes, induced procedures, learned affinities --
> the learner's contribution has been confined to reusing stored
> knowledge cheaply, never to choosing better than a count.**

And the three harness collapses (unreachable answer, label-bounded
alphabet, universal structure) say something equally important:

> **Most of my "learner loses to the heuristic" results come from worlds
> where a competent procedure exists and the learner is asked to
> replicate it, not to exceed it.** The next experiment has to be built
> where no competent procedure is *available* to be replicated.

That is a much sharper brief than "learn the finder", and it is the
concrete recommendation the consolidated report carries forward.