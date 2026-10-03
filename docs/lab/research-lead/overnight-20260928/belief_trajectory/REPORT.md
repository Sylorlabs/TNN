# REPORT: Trajectory-Shaped Reliability Update (H-DECEPT-2)

Wave: 2026-10-02. Verdict: BELIEF-TRAJECTORY-COMPLETE. All kill bars
K1-K6 evaluated against the frozen PREREG.md (committed a3c9b2482
before implementation; prereg-order self check holds).

## What was tested

H-DECEPT-1 (results fa78c53f2) left one precise failure: the reliability
downgrade after defection is EXACTLY linear (952, then 909/869/833/800/
769), with the high-stakes betrayal after 20 correct rounds moving
rel(S) by exactly one instance. This wave tests the specified next: a
trajectory-shaped reliability update. The update is trajectory-weighted
instance counting, applied uniformly to every source on every
verification outcome:

- correct: correct += 1; total += 1; streak = c + 1
- wrong: p = floor(c * w / (c + w)); total += 1 + p; streak = 0

where c = consecutive correct outcomes immediately preceding the
outcome (new learner-owned per-source streak state) and w = claim
weight (the claim's stake). The penalty is parameter free: monotone in
streak and stake, zero on a zero streak, saturating at the claim's
stake w. No source identity checks, no phase checks, no betrayal
detection logic; it is general, not betrayal specific.

## Results

All in-binary checks passed (exit 0, "ALL PASS"). 3/3 runs byte
identical (sha256
03c019c55b4a65fb1227618f4982d27e116dcc1f72410364a4fa00dd051a6dd3).
Stdout byte verified with od -c spot check.

### D1 trajectory vs the frozen linear baseline (the bar to beat)

| checkpoint | observed rel(S) | linear null | below |
|---|---|---|---|
| exposure (streak 20, w=3, p=2) | 869 | 952 | yes |
| post +1 (streak 0, w=1, p=0) | 833 | 909 | yes |
| post +2 | 800 | 869 | yes |
| post +3 | 769 | 833 | yes |
| post +4 | 740 | 800 | yes |
| post +5 | 714 | 769 | yes |

Every checkpoint is strictly below its frozen baseline value, exactly
matching the preregistered mechanistic predictions (869; 833, 800,
769, 740, 714). The defection is no longer one instance among many:
the exposure costs 1 + 2 instances because a 20-streak, w=3 error is
high surprise. The penalty persists through the aftermath: the five
ordinary wrongs each cost exactly one instance (streak 0), but they
start from the penalized total of 23, so the trajectory stays below
the linear null at every point. The learner now distinguishes "one
error among many" from "a trust-building run exploited by a
high-stakes betrayal" in the source model. The belief stance itself is
unchanged from H-DECEPT-1 (11, 12, 22; s1 = 3000, s2 = 4000); the fix
lives entirely in the reliability update, as specified.

### R1 control (no over-penalize)

Exposure verification added: S verified CORRECT (w=3, streak 20):
rel(S) = 1000, unchanged, truth-teller holds. W1 and W2 verified WRONG
(w=1, streak 2 each): p = floor(2/3) = 0, rel = 666 = linear null
exactly, no over-penalize. Stance stays 12 (11, 12, 12; s1 = 3000,
s2 = 2000). The same uniform rule that punishes the D1 defector leaves
short-streak errors linear.

### C1 control (no overreaction to noise)

T: correct then wrong weak (streak 1 at the error): p = floor(1/2) = 0,
rel = 500 = linear null. U: wrong (streak 0) then correct weak:
rel = 500 = linear null. Ordinary single errors are treated as pure
noise, exactly as before.

## Hypothesis verdict (frozen rule from PREREG.md)

H-DECEPT-2 is SUPPORTED: (a) all six D1 checkpoints strictly below the
frozen baseline; (b) R1 holds with S at 1000 and W1/W2 at the linear
666; (c) C1 at the linear 500/500. The trajectory-shaped update
repairs the D1b failure without overreacting anywhere the controls
probe.

## Honesty and limits

The rule FORM is researcher-authored; only its inputs (streaks) are
learner-owned. This wave is mechanism evidence (L2 class), not L3
representational invention: nothing about the update was invented by
the learner. The worlds are the same scripted D1/R1 structures as
H-DECEPT-1, not fresh sealed adversarial worlds; a sealed re-test is
still owed before any generality claim. The penalty saturates at the
claim's stake, so a very long streak's single error is bounded; whether
that bound is the right shape for repeated betrayals (streak rebuild
then re-defect) is untested.

## Kill bars

K1 PASS: 3/3 byte identical (sha256 03c019c5...).
K2 PASS: D1 build rel 1000/1000/1000; stance 11, 12, 22; s1 = 3000;
    s2 = 4000.
K3 PASS: exposure rel == 869 (< 952); aftermath exactly 833, 800, 769,
    740, 714 (each < 909/869/833/800/769); stance stays 22; zero
    evictions.
K4 PASS: R1 stance 11, 12, 12; s1 = 3000; s2 = 2000; final st = 12;
    exposure rel(S) = 1000, rel(W1) = rel(W2) = 666.
K5 PASS: C1 rel(T) = 500, rel(U) = 500.
K6 PASS: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag
    (safebin PATH, no python3/python present at any point). Unfrozen
    variant only; frozen sources untouched; paper untouched; nothing
    pushed; explicit pathspecs on all git operations.

## Artifacts

- PREREG.md (frozen, committed a3c9b2482 before implementation)
- NAMECHECK.md (toolchain guard Step 0 recorded)
- belief_trajectory.zag (source, pure Zag)
- belief_trajectory_bin (binary, 67290 bytes)
- compile.log (znc warnings only, same analyzer class as H-DECEPT-1)
- run1.txt, run2.txt, run3.txt (byte identical outputs)

Architecture accounting: capability added 0 lines to the protected
core; new hardcoded semantic cases 0; modes/bridges/handlers 0;
learner-state structures created: 1 (per-source correct-streak cell,
learner-owned); researcher-authored machinery: the trajectory rule
form (counted honestly, not learner-invented).
