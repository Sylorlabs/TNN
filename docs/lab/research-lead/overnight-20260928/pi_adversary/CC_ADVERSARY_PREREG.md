# Preregistration: Content-Conditional Adversary Attacks (CC-A1..CC-A6)

**Date:** 2026-09-29 07:50 PDT
**Adversary:** Content-Conditional Adversary (independent subagent)
**Branch:** tnn-native-lab
**Status:** FROZEN (committed before any attack execution)
**Target:** H-CC claim (commit dd95a64b3), implementation proc_cond.zag (commit dd95a64b3), prereg dd5f2f77e

## Stance

Assume H-CC is false. The researcher's claim is "H-CC SURVIVES" with 4/4 kill
bars passing. My job is to find the boundaries where it breaks and determine
whether the claim is overstated.

The researcher honestly disclosed scope limitations (position-0 predicates,
size-3 branches, single predicate, batch learning). My attacks test whether
these limitations are fatal to the generality of the claim, and whether the
training-data cleaning (CC-A6) was load-bearing.

## Attack Battery (frozen)

### CC-A1: Predicate position generality

**Question:** The predicate EQ0(v) checks only input position 0. Is the
"content-conditional" genuinely general, or just "position-0-conditional"?

**Test:** Training where the discriminating feature is at position 1:
- ("aXb"->"aaa"): broadcast-first, seq [0,0,0], n=3, input[1]='X'
- ("aYb"->"bbb"): broadcast-last, seq [2,2,2], n=3, input[1]='Y'
- ("cXd"->"ccc"): broadcast-first, seq [0,0,0], n=3, input[1]='X'
- ("cYe"->"eee"): broadcast-last, seq [2,2,2], n=3, input[1]='Y'

True rule: IF input[1]=='X' THEN C0 ELSE SUB(N,C1).

**Predicted outcome:** NO CONDITIONAL FOUND (FAIL to learn). The mechanism
extracts candidate v from position 0 only. Position-0 values here are
'a','a','c','c' — no value discriminates the [0,0,0] vs [2,2,2] seqs.
For v='a': inputs "aXb" and "aYb" both satisfy predicate, requiring then-branch
to fit both [0,0,0] and [2,2,2] — impossible for a base program.
Same for v='c'. Hence no conditional fits.

**Kill condition:** If NO PROGRAM FOUND, CC-A1 PASSES as an attack (mechanism
boundary confirmed: position-0 only). If a program IS found, CC-A1 FAILS as
an attack (mechanism more general than claimed) and I must explain how.

### CC-A2: Value extraction scaling

**Question:** Candidate values v are "distinct bytes at position 0." What
happens with many distinct values? Does search explode beyond K-CC1's 100k?

**Test (analytical + empirical):** Construct training with V distinct
position-0 bytes, all requiring the same conditional structure.
- V=50: total = 1055 + 50*55*55 = 1055 + 151,250 = 152,305.
- 152,305 > 100,000 → K-CC1 (tractability) FAILS.

**Predicted outcome:** The mechanism's tractability guarantee breaks at
V >= 33 (33*3025 = 99,825 + 1055 = 100,880 > 100k). The 100k bar was
validated only for V=3. The claim "remains tractable" does not generalize.

**Kill condition:** CC-A2 PASSES as an attack if I demonstrate (by
construction/counting, and a small Zag program that enumerates the count)
that V=50 yields >100k programs. This does not invalidate the V=3 result,
but it bounds the tractability claim: tractable only for small V.

Additionally: check source for any cap on ncand. If uncapped, a 256-value
worst case gives 1055 + 256*3025 = 775,455 programs.

### CC-A3: Branch size limit

**Question:** Branches limited to size <= 3 (55 programs). What if correct
branches need size 5?

**Test:** Training where THEN branch needs reverse (n-1-k, size 5):
- ("xab"->"bax"): reverse, seq [2,1,0], n=3, input[0]='x'
- ("xcd"->"dcx"): reverse, seq [2,1,0], n=3, input[0]='x'
- ("abc"->"ccc"): broadcast-last, seq [2,2,2], n=3, input[0]='a'
- ("def"->"fff"): broadcast-last, seq [2,2,2], n=3, input[0]='d'

True rule: IF input[0]=='x' THEN (n-1-k) ELSE (n-1).
The then-branch (n-1-k) is a size-5 program (base index 50). Branch
enumeration only includes size <= 3.

**Predicted outcome:** NO CONDITIONAL FOUND. No size<=3 program fits the
[2,1,0] seqs (reverse needs size 5). Phase 2 exhausts all 9075 conditionals
without success.

**Kill condition:** CC-A3 PASSES as an attack if NO PROGRAM FOUND. This
confirms the branch-size limit is a hard boundary, not a principled one:
any conditional task needing a complex branch fails.

### CC-A4: Two-phase gating masks needed conditionals

**Question:** Phase 2 runs "only if Phase 1 fails." Can Phase 1 spuriously
succeed on training data that actually needs a conditional, preventing
Phase 2 from ever running?

**Test:** Training where a base program fits all training seqs, but the
true rule is conditional and hidden cases expose it:
- ("abc"->"cba"): reverse, seq [2,1,0], input[0]='a'
- ("xab"->"bax"): reverse, seq [2,1,0], input[0]='x'

Base program n-1-k fits both. Phase 1 SUCCEEDS. Phase 2 never runs.
Mechanism returns n-1-k.

Hidden test: ("xcd"->"xxx"). True rule (unknown to mechanism): IF
input[0]=='x' THEN broadcast-first ELSE reverse. Mechanism predicts "dcx"
via n-1-k. Correct is "xxx". WRONG.

**Predicted outcome:** Mechanism returns base program n-1-k (Phase 1
success). On the hidden case it predicts incorrectly. This demonstrates
that two-phase gating is not just "hallucination prevention" — it is also
"conditional blindness": the mechanism cannot discover that training data
was insufficient.

**Kill condition:** CC-A4 PASSES as an attack if (a) mechanism returns a
base program for the training set, AND (b) that program is wrong on the
hidden case where the true rule is conditional. This shows the gating
creates a generalization blind spot.

Note: This does not contradict K-CC4 (no hallucination on the researcher's
tests). It shows K-CC4's test design was insufficient: their "pure" cases
were genuinely pure. Mine shows what happens when training data is
misleadingly pure.

### CC-A5: Predicate generality (equality only)

**Question:** EQ0(v) checks equality. Can the mechanism learn inequality,
greater-than, or any other predicate?

**Test (source inspection + empirical):** Training where rule is
"IF input[0] > 'm' (109) THEN broadcast-first ELSE broadcast-last":
- ("zab"->"zzz"): broadcast-first, seq [0,0,0], input[0]='z' (122 > 109)
- ("yab"->"yyy"): broadcast-first, seq [0,0,0], input[0]='y' (121 > 109)
- ("aab"->"bbb"): broadcast-last, seq [2,2,2], input[0]='a' (97 < 109)
- ("cab"->"bbb"): broadcast-last, seq [2,2,2], input[0]='c' (99 < 109)

No single EQ0(v) predicate separates {'z','y'} from {'a','c'} for the
required branches. For v='z': then must fit [0,0,0] (from "zab"), else
must fit [0,0,0] (from "yab"), [2,2,2], [2,2,2] — else-branch impossible.

**Predicted outcome:** NO CONDITIONAL FOUND. The predicate language
{equality to one byte} cannot express threshold/range conditions.

**Kill condition:** CC-A5 PASSES as an attack if NO PROGRAM FOUND,
documenting the predicate boundary: equality-only, no inequality,
no ranges, no compound predicates. The "content-conditional" is really
"single-byte-equality-at-position-0 conditional."

### CC-A6: Training data cleaning legitimacy

**Question:** The researcher admits: "I cleaned the H-REVISE training data...
replaced ('xy'->'yy') with ('def'->'fff') to ensure a fair test." The
original ("xy"->"yy") starts with 'x' but requires broadcast-last, making
the predicate non-discriminating. Was this legitimate cleaning or
deck-stacking?

**Test:** Run the ORIGINAL uncleaned training data through the UNMODIFIED
mechanism:
- ("abc"->"ccc"): broadcast-last, seq [2,2,2], input[0]='a'
- ("xy"->"yy"): broadcast-last, seq [1,1], n=2, input[0]='x'
- ("defg"->"gggg"): broadcast-last, seq [3,3,3,3], n=4, input[0]='d'
- ("xab"->"xxx"): broadcast-first, seq [0,0,0], n=3, input[0]='x'

With v='x': then-branch must fit seq [1,1] (from "xy") AND [0,0,0] (from
"xab"). No base program fits both ([1,1] needs n-1 with n=2; [0,0,0]
needs C0). So v='x' yields no conditional. Other v values ('a','d')
also fail to discriminate. 

**Predicted outcome:** NO CONDITIONAL FOUND on original data. The mechanism
cannot handle the researcher's own motivating example as originally stated.

**Kill condition:** CC-A6 PASSES as an attack if NO PROGRAM FOUND on the
original data. This does NOT invalidate the cleaned-data result, but it
proves the cleaning was LOAD-BEARING: the mechanism only works when the
human pre-arranges training data so the predicate discriminates. The
researcher's "fair test" framing is misleading — the original H-REVISE
counterexample ("xab" vs "xy") is precisely the hard case, and the
mechanism fails it. A fair characterization: "works when the discriminating
feature is pre-isolated by the researcher."

If instead a program IS found on original data, CC-A6 FAILS as an attack
and I will document how the mechanism handled the non-discriminating case.

## What Does NOT Count as a Kill

- Showing the mechanism fails on tasks outside its stated scope does not
  invalidate H-CC's 4/4 kill bars. The researcher disclosed limitations.
- A successful attack NARROWS the claim; it does not necessarily KILL it.
- H-CC is KILLED only if: (a) one of K-CC1..K-CC4 is shown to be false
  on the researcher's own test data (reproduction failure), OR (b) the
  training-data cleaning is shown to invalidate K-CC2's interpretation
  (the "finds conditional" bar was passed on stacked data).

## Commit Order

1. This prereg (FROZEN) — before any attack code is written or run.
2. Attack implementation (pure Zag + shell).
3. Attack results + verdict.

## Pure Zag Compliance

All attack test programs in Zag. Shell only for build/run/diff.
No Python anywhere.
