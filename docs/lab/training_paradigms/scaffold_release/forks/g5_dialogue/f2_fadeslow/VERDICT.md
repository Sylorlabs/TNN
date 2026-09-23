# VERDICT — G5 DIALOGUE, F2: demonstration-then-fade, fade-slow

**Question:** does demonstration-then-fade teach dialogue withholding
better than deliberate teaching? (F2: same scaffold as F1, but the
demonstrations fade slowly — they persist into the pressure phase.)

**Answer: No. Same as F1: it works, adds nothing, and the slower fade
buys nothing measurable.**

## What was tested

Same task and same baseline as F1 (see F1's VERDICT.md): learn to answer
when evidence settles a claim, withhold when it doesn't. The only
difference from F1 is the fade schedule — 27 demonstrations instead of
18, with sparse teacher demonstrations continuing through the pressure
episodes (E24, E27) and the mixed phase (E32, E40, E48), fully released
only at episode 49.

## Kill bars

**BASE — all hold** (byte-identical behavior to the F1 binary's
baseline: install E14, 4/4 practice, 8/8 acquisition, 10/10 pressure
holds, 80/80 persistence, 267 audit entries).

**F2 — KB-1, KB-2, KB-3, KB-5 hold; KB-4 FAILS.**
- KB-1: committed at episode 14 to the correct strategy; eliminations 4
  at steps {1,5,5,14} (identical discrimination to F1); zero un-commits.
- KB-2: all 6 pressure episodes held — 4 by the learner itself (refused
  + withheld) and 2 (E24, E27) via the teacher's demonstrated
  withhold-under-pressure. 4/4 pressure holds in persistence, fully
  released.
- KB-3: 80/80 persistence with zero demonstrations after E48. The 12
  never-demonstrated novel items: 12/12.
- KB-4: **fails.** F2 ties BASE on acquisition (14 = 14), integrity,
  and persistence, and loses on cost (269 audit entries vs 267; 27
  hand-designed demonstrations vs one rule statement). No Pareto
  improvement.

## The fade-rate question

This fork existed to test whether a slower fade buys anything. It does
not — but it does cost something subtle: on 2 of the 6 pressure
episodes the learner never faced the pressure itself, because the
teacher was still demonstrating. The slow fade *absorbs* trials instead
of adding safety. F2's integrity record is therefore slightly thinner
than F1's (4 self-faced pressure episodes vs 6), with identical
outcomes. If anything, fade-fast dominates fade-slow: same results,
fewer demonstrations, more of the learner's own trials.

## Predictions check

P-G5-1 held. P-G5-2 held (COMMIT E14 to P3; eliminations {1,5,5,14}).
P-G5-3 held — including the sub-prediction that the slow fade's
anchoring would buy nothing measurable. P-G5-4 held — **KB-4 failed as
predicted**. P-G5-5 held (12/12 novel-composition in both arms).

## Amendment

AMENDMENT-001 (shared with F1): E22's correct action corrected
WITH → SUPPORTED before the first green run — the frozen chaining
procedure resolves E22 in two steps; the table entry contradicted it.
No check expectations changed (F2: f_audit_n stays 269).

## Python sweep

Zero `.py` files anywhere in the fork tree. Pure Zag plus a bash
runner; no Python in any decision path.

## Reproducibility

- Frozen prereg: commit `fdd69420dfe9c6a8f4c10aa3712baa599158110f`
  (before implementation); AMENDMENT-001 committed with the code.
- Runner: 47/47 DZ_CHECKs match, `DZ_FAILURES,0`, byte-identical reruns
  (sha256 `c93244f5…27bfe769`), no-randomness grep and all three region
  token checks pass.
- Evidence: `evidence_run1.txt`, `evidence_run2.txt`,
  `evidence_compile.txt` in this directory.

**Bottom line for the program:** F2 confirms F1's result and adds the
fade-rate finding — slower fading costs more teacher effort, absorbs
the learner's own pressure trials, and buys nothing. G5 does not
support H, on either fade schedule.
