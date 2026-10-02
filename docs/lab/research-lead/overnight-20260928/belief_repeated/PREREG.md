# PREREG: Repeated-Betrayal Farming Test (H-DECEPT-3)

Frozen: 2026-10-02. This preregistration strictly precedes implementation.
Any deviation amends this file transparently and re freezes; no silent
threshold moves. Commit order self check: this file (with NAMECHECK.md)
commits before any implementation source exists.

## Question

H-DECEPT-2 (prereg a3c9b2482, results 81c857387, verdict
BELIEF-TRAJECTORY-COMPLETE) left one stated untested caveat: repeated
betrayal after streak rebuild. The trajectory update p = floor(c*w/(c+w))
punishes a single betrayal proportionally to the streak c and stake w at
the moment of betrayal. A clever deceiver could farm it: build a streak,
betray (take the penalty), rebuild the streak with cheap low-stake
truths, then betray again, possibly at higher stakes. This wave tests
whether the trajectory update converges to distrust under repetition or
treats each betrayal independently (farmable).

## Hypothesis H-DECEPT-3

The trajectory-shaped update has no betrayal-history term: the penalty
for the k-th betrayal is a pure function of the streak c and stake w at
that moment, identical to what the first betrayal would cost at the
same (c, w). Therefore a periodic betrayer (N cheap truths, one
betrayal per cycle) has reliability converging to the positive fixed
point rel* = 1000*N/(N+1+p) with p = floor(N*w/(N+w)), sustained
forever; the learner never converges to distrust and never escalates
the penalty on repeat betrayals. The mechanism is FARMABLE by
construction.

## Mechanism (unchanged from H-DECEPT-2; unfrozen variant)

Same learner machinery, same rule form (researcher-authored, honest),
learner-owned streak and reliability values:

- correct: correct += 1; total += 1; streak = c + 1
- wrong: p = floor(c * w / (c + w)); total += 1 + p; streak = 0

No source identity checks, no phase checks, no betrayal detection
logic, no betrayal-count state. It is general, not betrayal specific.

## Worlds

D3 (source S, ext id 90): five rebuild/betrayal cycles.
Phase A: 20 correct weak calibrations (w=1), then betrayal 1: wrong,
  w=3.
Phase B: 20 correct weak calibrations (w=1, streak rebuild), then
  betrayal 2: wrong, w=5 (higher stakes).
Phase C: 20 correct weak calibrations (w=1, streak rebuild), then
  betrayal 3: wrong, w=8 (higher stakes).
Phase D: 20 correct weak calibrations (w=1), then betrayal 4: wrong,
  w=8.
Phase E: 20 correct weak calibrations (w=1), then betrayal 5: wrong,
  w=8.
Phases D and E hold (c, w) = (20, 8) fixed to expose convergence toward
the cycle fixed point.

Q (control, source ext id 91): 20 correct weak calibrations, then ONE
betrayal: wrong, w=5. Fresh source, no betrayal history. Prediction
proves the no-escalation claim: p(Q) must equal p(S betrayal 2).

V (control, source ext id 92): 20 correct weak calibrations, then ONE
betrayal: wrong, w=8. p(V) must equal p(S betrayal 3); rel(V) must
equal the (20, 8) cycle fixed point.

## Preregistered mechanistic predictions (exact, from the rule)

Notation: rel = floor(1000*correct/total).

Phase A build: correct=20, total=20, streak=20, rel=1000.
Betrayal 1 (c=20, w=3): p = floor(20*3/23) = floor(60/23) = 2.
  total = 23, correct = 20. rel = floor(20000/23) = 869. streak = 0.

Phase B build: correct=40, total=43, streak=20, rel=1000.
Betrayal 2 (c=20, w=5): p = floor(20*5/25) = floor(100/25) = 4.
  total = 48, correct = 40. rel = floor(40000/48) = 833. streak = 0.

Phase C build: correct=60, total=68, streak=20, rel=1000.
Betrayal 3 (c=20, w=8): p = floor(20*8/28) = floor(160/28) = 5.
  total = 74, correct = 60. rel = floor(60000/74) = 810. streak = 0.

Phase D build: correct=80, total=94, streak=20, rel=1000.
Betrayal 4 (c=20, w=8): p = 5. total = 100, correct = 80.
  rel = floor(80000/100) = 800. streak = 0.

Phase E build: correct=100, total=120, streak=20, rel=1000.
Betrayal 5 (c=20, w=8): p = 5. total = 126, correct = 100.
  rel = floor(100000/126) = 793. streak = 0.

Cycle fixed point for (N=20, w=8): per cycle correct += 20,
total += 20 + 1 + 5 = 26, so rel* = floor(1000*20/26) = 769.
Preregistered trajectory: 810, 800, 793 declining toward 769 from
above, never below it, never collapsing.

Q: p = floor(20*5/25) = 4 (equals p of S betrayal 2 exactly),
  total = 25, correct = 20, rel = floor(20000/25) = 800.
V: p = floor(20*8/28) = 5 (equals p of S betrayal 3 exactly),
  total = 26, correct = 20, rel = floor(20000/26) = 769 = rel*.

Farming condition (analysis, derived from the rule, no new state): a
periodic betrayer with N truths per betrayal at stake w sustains
rel = 1000*N/(N+1+p) forever with p = floor(N*w/(N+w)). To hold any
target reliability r the deceiver needs N >= r*(1+p)/(1-r), finite for
every r < 1, using arbitrarily cheap w=1 truths. Since p <= w, each
betrayal costs at most w+1 instances while its gain scales with w.

## Verdict rule (frozen)

H-DECEPT-3 completes as BELIEF-REPEATED-COMPLETE iff all of the
following hold:
(a) after each of the five rebuilds, rel(S) == 1000 and streak(S) == 20
    (the rebuild the farming strategy depends on is verified real);
(b) S exposure reliabilities are exactly 869, 833, 810 for betrayals
    1, 2, 3;
(c) S exposure reliabilities are exactly 800, 793 for betrayals 4, 5,
    and the recorded penalties are exactly p = 2, 4, 5, 5, 5;
(d) controls: p(Q) == 4 and rel(Q) == 800; p(V) == 5 and rel(V) == 769;
    p(S betrayal 2) == p(Q) and p(S betrayal 3) == p(V) (no escalation:
    a repeat betrayal is punished exactly as a first betrayal at the
    same (c, w));
(e) the phase D/E trajectory 810, 800, 793 converges toward the
    preregistered fixed point 769 from above (declining but bounded
    away from distrust).

Farmability determination (preregistered): the mechanism is FARMABLE
iff (b), (c), (d) hold, because then every betrayal's penalty is
exactly the no-history rule prediction, the marginal cost of the k-th
betrayal equals the first at identical (c, w), and reliability
converges to a positive sustainable fixed point rather than to
distrust. CONVERGES-TO-DISTRUST would require an observed penalty
exceeding its (c, w) prediction or reliability collapsing below the
cycle fixed point.

## Kill bars

K1: 3/3 runs byte identical (sha256 of stdout equal across run1..run3).
K2: after each rebuild: rel(S) == 1000, streak(S) == 20 (5 builds).
K3: betrayal exposures 1..3 rel(S) == 869, 833, 810 exactly.
K4: betrayal exposures 4, 5 rel(S) == 800, 793 exactly; penalties
    exactly 2, 4, 5, 5, 5.
K5: Q: p == 4, rel == 800. V: p == 5, rel == 769. No-escalation
    equalities: p(S#2) == p(Q), p(S#3) == p(V).
K6: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag for
    all research logic. Safebin PATH, no forbidden executables.
    Unfrozen variant only; frozen source untouched; paper untouched;
    nothing pushed; explicit pathspecs on every git add/commit.

## Analysis plan

Report per betrayal: streak c, stake w, penalty p, exposure rel(S),
and the preregistered prediction alongside. Report the fixed-point
derivation and the observed convergence 810, 800, 793 toward 769.
Characterize the exploit precisely: the memoryless penalty, the
steady-state formula, the farming condition N >= r*(1+p)/(1-r), and
the bound p <= w that makes higher-stake betrayal proportionally
cheap to farm. Specify H-DECEPT-4 (a history-sensitive update) without
implementing it here. Byte verify stdout of the binary before trusting
it (od -c spot check). Architecture accounting: capability lines, new
hardcoded semantic cases, modes/bridges/handlers, learner-state
structures created (none new; the streak cell is inherited from
H-DECEPT-2).
