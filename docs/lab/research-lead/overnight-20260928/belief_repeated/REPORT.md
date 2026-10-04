# REPORT: Repeated-Betrayal Farming Test (H-DECEPT-3)

Wave: 2026-10-02. Verdict: BELIEF-REPEATED-COMPLETE. All kill bars
K1-K6 evaluated against the frozen PREREG.md (committed d063f8e40
before implementation; amendment A1 committed 3213a03a5 before any
re-run; prereg-order self check holds).

## What was tested

H-DECEPT-2 (results 81c857387, BELIEF-TRAJECTORY-COMPLETE) left one
stated untested caveat: repeated betrayal after streak rebuild. The
trajectory update p = floor(c*w/(c+w)) punishes a betrayal from the
streak c and stake w at that moment only. A clever deceiver could farm
it: build streak, betray, rebuild with cheap truths, betray again at
higher stakes. This wave runs that exact strategy: S builds a
20-streak and betrays at w=3, rebuilds the 20-streak with w=1 truths
and betrays at w=5, rebuilds and betrays at w=8, then two more
rebuild/betray cycles at w=8 to expose the long-run behavior. Fresh
single-betrayal controls Q (w=5) and V (w=8) prove whether a repeat
betrayal is punished differently from a first betrayal at identical
(c, w).

## Results

All in-binary checks passed (exit 0, "ALL PASS"). 3/3 runs byte
identical (sha256
d43648dc64b923560f4a42900e138e4390571ec9981368daebe4a97e0542da38).
Stdout byte verified with od -c spot check.

### D3: five betrayals, escalating then fixed stakes

| event | c | w | p | exposure rel(S) | prereg | match |
|---|---|---|---|---|---|---|
| betrayal 1 | 20 | 3 | 2 | 869 | 869 | yes |
| betrayal 2 | 20 | 5 | 4 | 833 | 833 | yes |
| betrayal 3 | 20 | 8 | 5 | 810 | 810 | yes |
| betrayal 4 | 20 | 8 | 5 | 800 | 800 | yes |
| betrayal 5 | 20 | 8 | 5 | 793 | 793 | yes |

Rebuilds verified real each time: streak(S) == 20 after all five
rebuilds, with rel(S) exactly 1000, 930, 882, 851, 833 (the A1
corrected values; reliability does not return to 1000 because the
penalty persists in the denominator, exactly as the rule specifies).

### No-escalation controls

Q (fresh source, one betrayal at w=5): p = 4, rel = 800.
V (fresh source, one betrayal at w=8): p = 5, rel = 769.
In-binary equalities: p(S betrayal 2) == p(Q) == 4;
p(S betrayal 3) == p(V) == 5. A repeat betrayal is punished EXACTLY as
a first betrayal at identical (c, w). The rule has no betrayal-history
term and recognizes no pattern.

### Fixed point, not distrust

The (20, 8) cycle adds 20 correct and 1+5 instances per cycle, so the
steady state is rel* = floor(1000*20/26) = 769. Observed exposures at
w=8: 810, 800, 793, declining toward 769 from above, bounded away from
distrust. V's single betrayal lands exactly on 769, the fixed point.

## Farmability analysis (the exploit, characterized precisely)

1. Memoryless penalty. p = floor(c*w/(c+w)) is a pure function of the
   streak and stake at the moment of betrayal. Betrayal count appears
   nowhere. Proven in-binary by the no-escalation equalities.
2. Positive sustainable fixed point. A periodic betrayer doing N cheap
   truths per betrayal at stake w converges to
   rel* = 1000*N/(N+1+p) with p = floor(N*w/(N+w)), which is positive
   for every finite N and w. The learner never converges to distrust;
   it converges to sustained usable trust in a known periodic
   betrayer.
3. Farming condition. To hold any target reliability r the deceiver
   needs N >= r*(1+p)/(1-r) cheap truths per cycle, finite for every
   r < 1. Example: sustain rel 900 while betraying at w=8 (p=5)
   needs 54 w=1 truths per cycle, repeatable forever.
4. Cost bounded by stake. Since cw/(c+w) < w, p <= w-1, so one
   betrayal costs at most w instances (1 + p <= w) while its gain
   scales with the stake w. At c=20 the w=8 betrayal costs 6 instances
   for stake 8 (0.75 per unit stake): higher-stake betrayals are
   proportionally cheaper to farm than low-stake ones at moderate
   streaks.
5. The rebuild the strategy needs is always available: 20 cheap truths
   restore streak 20 exactly, resetting the penalty basis for the next
   betrayal.

Conclusion: the trajectory update does NOT converge to distrust under
repeated betrayal. It is farmable indefinitely, by construction, and
the farming gets no harder with repetition.

## Hypothesis verdict (frozen rule from PREREG.md as amended by A1)

H-DECEPT-3 completes as BELIEF-REPEATED-COMPLETE with the mechanism
determined FARMABLE: (a) all five rebuilds show streak 20 with rel
exactly 1000/930/882/851/833; (b) exposures exactly 869/833/810;
(c) exposures exactly 800/793 with penalties exactly 2/4/5/5/5;
(d) Q p=4 rel=800, V p=5 rel=769, and the no-escalation equalities
hold; (e) the w=8 trajectory 810/800/793 converges toward the
preregistered fixed point 769 from above. Every betrayal's penalty is
exactly the no-history rule prediction, so the marginal cost of the
k-th betrayal equals the first at identical (c, w), and reliability
converges to a positive sustainable fixed point rather than to
distrust.

## H-DECEPT-4 specification (not implemented here)

Question: does a history-sensitive reliability update converge to
distrust under periodic betrayal while preserving the H-DECEPT-2
controls (R1 truth-teller not over-penalized, C1 single errors stay
linear)? Candidate direction: a learner-owned betrayal-history term,
for example a per-source count of prior high-surprise wrongs (or an
EWMA of betrayal rate) that scales the penalty upward on repetition,
so the marginal cost of the k-th betrayal exceeds the first. The wave
must preregister: the exact history state, the scaling form, the
no-escalation controls it must still pass (Q/V style equalities must
now FAIL in the intended direction, with the escalation quantified),
the fixed-point analysis showing convergence below usability for a
periodic betrayer, and proof that an isolated betrayal followed by
honest behavior still recovers (no permanent distrust from one
error). Design is left to that wave's preregistration.

## Honesty and limits

The rule FORM is researcher-authored; only its inputs (streaks) are
learner-owned. This wave is mechanism evidence (L2 class), not L3
representational invention. The worlds are scripted D3/Q/V structures,
not fresh sealed adversarial worlds; a sealed re-test is still owed
before any generality claim. The fixed-point and farming-condition
results are analytic consequences of the rule, confirmed in-binary;
they are not learner discoveries.

## Kill bars

K1 PASS: 3/3 byte identical (sha256 d43648dc...).
K2 PASS: after each rebuild streak(S) == 20; rel(S) exactly 1000, 930,
    882, 851, 833 (A1 corrected).
K3 PASS: betrayal exposures 1..3 rel(S) == 869, 833, 810 exactly.
K4 PASS: betrayal exposures 4, 5 rel(S) == 800, 793 exactly;
    penalties exactly 2, 4, 5, 5, 5.
K5 PASS: Q p == 4, rel == 800; V p == 5, rel == 769; p(S#2) == p(Q),
    p(S#3) == p(V) (no escalation, in-binary).
K6 PASS: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag
    (safebin PATH, no python3/python present at any point). Unfrozen
    variant only; frozen sources untouched; paper untouched; nothing
    pushed; explicit pathspecs on all git operations.

## Artifacts

- PREREG.md (frozen, committed d063f8e40 before implementation;
  amendment A1 committed 3213a03a5 before any re-run)
- NAMECHECK.md (toolchain guard Step 0 recorded)
- belief_repeated.zag (source, pure Zag)
- belief_repeated_bin (binary, 46352 bytes)
- compile.log (znc warnings only, same analyzer class as H-DECEPT-2)
- run1.txt, run2.txt, run3.txt (byte identical outputs)

Architecture accounting: capability added 0 lines to the protected
core; new hardcoded semantic cases 0; modes/bridges/handlers 0;
learner-state structures created: 0 new (the per-source streak cell is
inherited from H-DECEPT-2; this wave adds one header scratch cell,
cell 14 last_penalty, for the no-escalation cross check, which is test
instrumentation, not learner state); researcher-authored machinery: the
trajectory rule form (unchanged, counted honestly, not
learner-invented).
