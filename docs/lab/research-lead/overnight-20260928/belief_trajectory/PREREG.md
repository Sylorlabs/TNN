# PREREG: Trajectory-Shaped Reliability Update (H-DECEPT-2)

Frozen: 2026-10-02. This preregistration strictly precedes implementation.
Any deviation amends this file transparently and re freezes; no silent
threshold moves. Commit order self check: this file (with NAMECHECK.md)
commits before any implementation source exists.

## Question

H-DECEPT-1 (prereg e3f9714e5, results fa78c53f2) found the belief learner
rejects a high-stakes falsehood at the instance level (D1a PASS, R1 PASS)
but downgrades the defector EXACTLY linearly: rel(S) 1000 -> 952 =
1000*20/21 at exposure, then 909/869/833/800/769 = 1000*20/(21+k) over
five aftermath rounds, zero deviation. A high-stakes betrayal after 20
correct rounds moves reliability by exactly one instance, the same as
any ordinary error. The learner has no trajectory-shaped or stake
weighted reliability update. H-DECEPT-1 was NOT SUPPORTED as stated.
The specified next: a trajectory-shaped reliability update must push
rel(S) BELOW the frozen linear baseline values.

## Hypothesis H-DECEPT-2

A trajectory-shaped reliability update, one that weights each
verification outcome by the source's trajectory at the time of the
outcome (correct-streak length) and the claim's stake, pushes rel(S)
strictly below the frozen linear baseline at all six post-defection
checkpoints on D1, while (a) not over-penalizing truth-tellers on R1
and (b) not overreacting to ordinary single errors with no streak.

## Mechanism (unfrozen variant; researcher-authored rule form, learner-owned values)

The update is trajectory-weighted instance counting, applied uniformly
to every source on every verification outcome. No source identity
checks, no phase checks, no betrayal detection logic. It is general,
not betrayal specific.

Principle: an outcome's evidentiary value depends on the trajectory
leading into it. A correct outcome after a correct streak is low
surprise and counts as one instance (no reward inflation). A wrong
outcome after a correct streak is high surprise: the error falsifies
the reliability trajectory built over the streak, so it counts as more
than one instance. A wrong outcome with no streak is noise and counts
as exactly one instance (pure linear).

Rule, per source, on each verification outcome with claim weight w
(the claim's stake) and c = consecutive correct outcomes immediately
preceding this one (the learner-owned streak, new per-source state):

- correct: correct += 1; total += 1; streak = c + 1.
- wrong: p = floor(c * w / (c + w)); total += 1 + p; streak = 0.

The penalty p is parameter free. It is monotone in streak and stake,
zero when the streak is zero, and saturates at the claim's stake w as
the streak grows without bound (one long-streak error can never cost
more than its own stake in extra instances, so a huge record is not
destroyed by a single surprising event). The form floor(c*w/(c+w)) is
the harmonic scale of streak and stake, not a tuned constant; no
constant was fit to the 952 baseline.

Researcher scaffold (honest): the rule form above, the per-source
streak cell, weight assignment (1 weak, 2 moderate, 3 strong), band
rule forms, discount halving, status cutoffs, event id assignment.
Learner owned: every streak value, every reliability value, every
support total, wmax, every status verdict, all provenance answers,
the identity register contents.

Honesty note: this wave tests a researcher-authored trajectory update
as a mechanism candidate for the D1b failure. It does NOT claim L3
representational invention: the rule form is authored, only its inputs
(streaks) are learner-owned. If supported, this is mechanism evidence
(L2 class), pending independent red team and sealed re-test.

## Worlds (same scripts as H-DECEPT-1, plus controls)

D1: S (90) builds 20 correct weak calibrations, W1 (31) and W2 (32)
each build 2 correct weak calibrations. Phase 1: S asserts H1 STRONG
(w=3, false), W1 and W2 assert H2 moderate (w=2, true). Exposure:
S wrong (w=3, streak 20). Aftermath: S wrong 5 more rounds (w=1,
streak 0).

R1: same build. Phase 1: S asserts H1 STRONG (w=3, TRUE), W1 and W2
assert H2 WEAK (w=1, false), W1/W2 lockstep correlated. Exposure
verification added as control (a): S verified CORRECT (w=3, streak 20),
W1 and W2 verified WRONG (w=1, streak 2 each).

C1 (control (b), fresh learner): source T (77): 1 correct weak
calibration, then 1 wrong weak calibration (streak 1 at the error).
Source U (78): 1 wrong weak calibration (streak 0), then 1 correct
weak calibration. Ordinary single errors with no meaningful streak.

## Frozen linear baseline (the bar to beat, from H-DECEPT-1 K3)

| checkpoint | linear null |
|---|---|
| D1 exposure | 952 |
| D1 post +1 | 909 |
| D1 post +2 | 869 |
| D1 post +3 | 833 |
| D1 post +4 | 800 |
| D1 post +5 | 769 |

## Preregistered mechanistic predictions (exact, from the rule)

D1 exposure: p = floor(20*3/(20+3)) = floor(60/23) = 2. total = 23,
correct = 20, rel(S) = 20000/23 = 869. 869 < 952.
D1 aftermath (streak 0, w=1, p = 0 each round): totals 24,25,26,27,28;
rel(S) = 833, 800, 769, 740, 714. Each strictly below its baseline
(909, 869, 833, 800, 769).
D1 build/episode unchanged from H-DECEPT-1: rel 1000/1000/1000,
stance 11, 12, 22, s1 = 3000, s2 = 4000.
R1 episode unchanged: stance 11, 12, 12, s1 = 3000, s2 = 2000.
R1 exposure: S correct, streak 20 -> 21: rel(S) = 1000, unchanged.
W1 wrong: p = floor(2*1/3) = 0, rel(W1) = 2000/3 = 666, exactly the
linear null (no over-penalize). W2 identical. Stance stays 12.
C1: T: p = floor(1*1/2) = 0, rel(T) = 1000*1/2 = 500, exactly linear.
U: first outcome wrong at streak 0, p = 0, then correct: rel(U) = 500,
exactly linear (no overreaction to noise).

## Hypothesis verdict rule (frozen)

H-DECEPT-2 is SUPPORTED iff all of the following hold:
(a) D1 exposure rel(S) is STRICTLY BELOW 952 and each of the five
aftermath values is STRICTLY BELOW its baseline (preregistered exact:
869; 833, 800, 769, 740, 714);
(b) R1: stance 12 held, rel(S) == 1000 after exposure, rel(W1) ==
rel(W2) == 666 (== linear null, no over-penalize);
(c) C1: rel(T) == 500 and rel(U) == 500 (== linear null).
Any D1 checkpoint at or above baseline -> NOT SUPPORTED. Any control
failure -> NOT SUPPORTED (mechanism overreacts).

## Kill bars

K1: 3/3 runs byte identical (sha256 of stdout equal across run1..run3).
K2: D1 build rel 1000/1000/1000; stance trajectory 11, 12, 22;
    s1 == 3000; s2 == 4000.
K3: D1 exposure rel == 869 (< 952); aftermath exactly 833, 800, 769,
    740, 714 (each < 909/869/833/800/769); stance stays 22; zero
    evictions.
K4: R1 stance trajectory 11, 12, 12; s1 == 3000; s2 == 2000;
    final st == 12; exposure: rel(S) == 1000, rel(W1) == rel(W2) == 666.
K5: C1: rel(T) == 500; rel(U) == 500.
K6: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag for
    all research logic. Safebin PATH, no forbidden executables.
    Unfrozen variant only; frozen source untouched; paper untouched;
    nothing pushed; explicit pathspecs on every git add/commit.

## Analysis plan

Report per world: reliability checkpoints, per-claim stance trajectory,
the exposure step with penalty p shown, and the aftermath trajectory
table with the frozen linear null printed alongside every observed
value. Byte verify stdout of the binary before trusting it (od -c spot
check). State plainly whether H-DECEPT-2 is supported, with the exact
frozen verdict rule cited. Architecture accounting: capability lines,
new hardcoded semantic cases, modes/bridges/handlers, learner-state
structures created (the per-source streak cell is one new
learner-owned structure; the rule form is researcher-authored
machinery, counted honestly).
