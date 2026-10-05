# REPORT -- LEARNED TRANSFORMATIONS C1811-C1850

Prereg `xform8/PREREG.md`. 3/3 sha256
`e9761b1195c47bd42ca91c7fb443c0e35da32d10592668458f33eaaf5c49ebf9`
loop lint CLEAN.

## THE LEARNED OBJECT

A **procedure**, not a prior. Three keys, three values:

```
key = size relation between current state and goal
      -1  current smaller      0  same size      +1  current larger
value = the edit kind that most often reduced distance at that key
```

Induced by counting signed distance changes over the learner's own
random exploration. Length-agnostic, label-agnostic, and stored in
learner state.

## THE INDUCED TABLE (printed, so it can be read directly)

```
key -1 (current smaller): DEL   gains DEL=2   INS=-8   MOV=2
key  0 (same size):      DEL   gains DEL=13  INS=-23  MOV=-2
key +1 (current larger): DEL   gains DEL=31  INS=-5   MOV=-2
```

Coherent, and correct for this world: most instances need deletions
before insertions, and `DEL` dominates once size reduction is the right
move.

## RESULTS

```
                          ORIGINAL            SHIFTED (labels 5..8, cap 3)
C  researcher heuristic   8 proposals  0 fail  8 proposals  0 fail
T  learner procedure     47 proposals  4 fail 79 proposals  4 fail
T-ERASED                 47 proposals  4 fail
T-IRRELEVANT             47 proposals  4 fail
T-MISLEADING             28 proposals  4 fail
T-FACTS                  47 proposals  4 fail
R  random                93 proposals  4 fail
```

Bars: `B3 learner_solves_all=0`, `B4 T_matches_C=0`,
`B5 T_transfers=0`, `B6..B8` all `0`, `B9=1`.

## THE FINDING: A PROCEDURE OVER KIND IS NOT A PROCEDURE

`T` induces *which kind* of edit to make and then takes the first legal
label. `C` scans all edits and takes the one that reduces distance.

Worked example, `{1,2} -> {4}` at capacity 2:

```
T:  DEL, lowest legal label -> {2}
    DEL again, lowest legal -> {}
    DEL with nothing left   -> dead end, FAIL

C:  DEL 1 -> {2}   (distance 3 -> 2)
    DEL 2 -> {}    (distance 2 -> 1)
    INS 4 -> {4}   (distance 1 -> 0)   SOLVED in 2 proposals
```

The induced procedure answers *"what kind of change"* and is
transferable in principle. It does not answer *"which instance to
change"*, and that second question is where all the work is. The
researcher's advantage is not the kind, it is the **argument**.

> **Inducing a procedure over a primitive's kind is insufficient. The
> argument selection is the researcher-owned part, and it is exactly the
> part the induction did not reach.**

That is a sharper statement of the boundary than anything earlier in
the program. It is not "the learner cannot learn search"; it is "the
learner learned half a search procedure, and the half it learned was
the easy half."

## THREE OF THE FIVE CONTROLS ARE DEGENERATE

`T-ERASED`, `T-IRRELEVANT` and `T-FACTS` all score **exactly** `47 / 4`
-- identical to `T`. The reason is an artefact of my own design: an
all-zero table makes `argmax` return the first kind, which is `DEL`,
which is also the induced answer. So "erased" is not an ablation at all.

`T-MISLEADING` (`INS/DEL/DEL`) does differ, and it is *cheaper* (28 vs
47) while failing the same four instances -- because `INS` is a no-op on
a full state, so the walk terminates sooner having done less.

Recorded because it means bars `B6` and `B7` did not test what they
claimed to test. The honest statement is that **the controls could not
discriminate, because the arm under test never succeeded.**

## TWO DEFECTS I INTRODUCED AND FIXED

1. **Sign inversion in the induction.** I stored
   `delta = dist_after - dist_before`, so a *good* edit has a negative
   delta, and then took the `argmax`. The table was exactly backwards:
   `DEL` correctly scored `-28` at key `+1` and was discarded in favour
   of `INS` at `+3`. Symptom: the induced table recommended `INS` at all
   three keys, including "current larger", which is obviously wrong.
   Fixed by storing improvement (`-delta`). Caught because the printed
   table was obviously wrong on inspection -- **printing the learned
   object, not just its score, is what found this.**
2. **The transfer test was unmeasurable.** The primitive alphabet spanned
   labels `1..4` only, so the shifted family used labels `5..8` and was
   unreachable *for every arm including the researcher*. `B5` was
   measuring nothing. Fixed by widening `NL` to 8, after which `C`
   correctly solves the shifted family in 8 proposals.

Defect 2 is the same error class as the earlier "expected answer was
class-2 and therefore unreachable": **an arm that could not measure
anything, reported as though it had.**

## FALSIFIERS

| | prediction | outcome |
|---|---|---|
| `F-PROC` | a learned procedure transfers where a learned prior did not | **not tested** -- T never solved an instance, so transfer of a *working* procedure was never exercised |
| `F-INDUCE` | the table is recoverable from experience, not facts | **untestable** -- all three table sources (induced, erased, facts) produced identical behaviour |
| `F-AGNOSTIC` | the table holds no label or capacity knowledge | **survives, weakly** -- the table is 3 integers over kind names, so it trivially cannot |
| `F-CONTROL` | a hand-written rule would do the same | **CONFIRMED, and this is the result** -- `C` does the same job in 8 proposals where `T` needs 47 and fails |

`F-CONTROL` firing is not a failure of the test. It is the finding.

## STANDING

```
learned a search procedure                          NO
learned a procedure over edit kind                  YES  (3 keys, induced)
transferred that procedure to a new family          NO  (arm never succeeded)
beat a researcher heuristic                         NO   47/4 fail vs 8/0 fail
argument selection learned                          NO   <- the identified gap
L3 = 0
```

## WHAT THIS ADDS

Three lanes now agree, and PHASE 8 names the mechanism:

```
C1681  selection   a fixed heuristic ties the learner
C1800  generation  a fixed heuristic beats the learner (prior over shapes)
C1850  procedure   a fixed heuristic beats the learner (procedure over kind)
```

In every case the learner's contribution is confined to *cost of
transfer* (reusing stored knowledge instead of re-deriving it), never to
capability. And PHASE 8 localises why in a way the others did not: the
learner can induce **what kind of change** to make, and cannot induce
**which instance to change it on**.

## THE NEXT EXPERIMENT, SPECIFICALLY

Not "learn a better procedure" -- that is what was just tried. Instead,
extend the induced table's key to include a facts-derived property of
the *candidate argument*:

```
key = (size relation) x (is the candidate label present in the goal?)
```

That property is computable from the fact table, so it is learnable
rather than given, and it is precisely the information `C` uses when it
scans edits. If inducing that second key closes the gap, the missing
piece was argument selection and nothing deeper. If it does not, the
remaining ownership gap is the *scan-and-compare* itself, which would be
a much more significant finding: the researcher's advantage would then
be the ability to evaluate a whole neighbourhood, not any particular
heuristic.

Either outcome is informative, and the experiment is cheap.