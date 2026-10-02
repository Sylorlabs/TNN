# PREREG: Betrayal-History-Aware Reliability Update (H-DECEPT-4)

Wave: 2026-10-02. Status: FROZEN. This prereg is committed before any
implementation source exists. Prereg-order self check: this file's
commit strictly precedes the implementation commit.

## Hypothesis

H-DECEPT-4: a betrayal-history-aware reliability update converges to
distrust under periodic betrayal, while preserving the H-DECEPT-2/3
controls (first betrayals punished exactly as before, truth-teller
unaffected, no-streak errors stay linear null, reform possible).

## The rule (frozen form)

Per-source learner-owned state: correct, total, streak c, betrayal
count b. The betrayal count b is a sufficient statistic of the
source's deceit history: it counts prior wrong outcomes that occurred
while trust was extended (c > 0). The penalty for a wrong outcome
scales multiplicatively with (1 + b): the first betrayal is punished
at the H-DECEPT-2/3 trajectory rate, the second at twice that, the
third at three times, and so on. This is a smooth general function of
history, not a hardcoded strike threshold: there is no ban, no mode,
no special case on the count.

Update on a verified outcome for source S with claim weight w:

- correct: correct += 1; total += 1; c += 1; if c is a positive
  multiple of 100 (c - (c/100)*100 == 0) then b = max(0, b - 1).
  Forgiveness is slow: one betrayal forgiven per 100 consecutive
  honest outcomes. Reform is possible; exile is not permanent.
- wrong with c > 0 (betrayal): base = floor(c*w/(c+w));
  p = base * (1 + b); total += 1 + p; b += 1; c = 0.
- wrong with c == 0 (no-streak error): total += 1; p = 0;
  b unchanged; c = 0. Linear null, and a no-streak error does not
  poison the betrayal history.
- rel(S) = 1000 if total < 2 else floor(1000*correct/total).

Principle: a betrayal is evidence that the source's error process is
adversarial rather than noisy. The marginal cost of the k-th betrayal
is 1 + base*(k), strictly increasing in k, so farming gets strictly
more expensive with repetition while a single betrayal followed by
honest behavior is fully forgiven.

## Frozen bar to beat

H-DECEPT-3 (commit 8be4b18d4) established: the memoryless update
converges to the fixed point rel* = 769 under the (20, 8) betray/rebuild
cycle, with repeat betrayals punished exactly as first betrayals.
This wave beats that bar iff the D4 exposures go BELOW 769 and keep
falling across the five betrayals, the escalation inequalities hold,
and the long-run limit is distrust (0), not a positive fixed point.

## Scenario D4 (mirrors H-DECEPT-3 D3 exactly)

Source S (ext 90). Five phases; each phase = 20 correct w=1 claims,
then one wrong claim at betrayal weight bw = 3, 5, 8, 8, 8.

Frozen expected values (hand computed, checked twice):

| phase | bw | rebuild rel | streak | base | prior b | p | marginal 1+p | exposure rel | b after |
|---|---|---|---|---|---|---|---|---|---|
| A | 3 | 1000 | 20 | 2 | 0 | 2 | 3 | 869 | 1 |
| B | 5 | 930 | 20 | 4 | 1 | 8 | 9 | 769 | 2 |
| C | 8 | 833 | 20 | 5 | 2 | 15 | 16 | 681 | 3 |
| D | 8 | 740 | 20 | 5 | 3 | 20 | 21 | 620 | 4 |
| E | 8 | 671 | 20 | 5 | 4 | 25 | 26 | 571 | 5 |

Arithmetic notes: base = floor(20*3/23) = 2; floor(20*5/25) = 4;
floor(20*8/28) = 5. Exposures: floor(20000/23) = 869;
floor(40000/52) = 769; floor(60000/88) = 681; floor(80000/129) = 620;
floor(100000/175) = 571. Rebuilds: floor(40000/43) = 930;
floor(60000/72) = 833; floor(80000/108) = 740;
floor(100000/149) = 671.

Escalation table (verdict deliverable): penalties 2, 8, 15, 20, 25;
marginal costs 3, 9, 16, 21, 26, strictly increasing. The second
betrayal costs 9 instances vs 3 for the first.

Long-run analytic (frozen): after n pure (20, 8) cycles,
correct = 20n, total = 20n + n + 5n(n+1)/2, so
rel(n) = 20000n / (21n + 2.5n(n+1)), which tends to 0 as n grows.
At n = 5: floor(100000/180) = 555. There is no positive fixed point:
the escalating penalty adds a quadratic term to the denominator, so
any fixed-period periodic betrayer converges to distrust.

## Controls (frozen expected values)

Q (ext 91): fresh source, 20-streak, ONE betrayal at w=5, b=0.
p = 4, rel = 800. Identical to H-DECEPT-3: a first betrayal is
punished exactly as before.

V (ext 92): fresh source, 20-streak, ONE betrayal at w=8, b=0.
p = 5, rel = 769. Identical to H-DECEPT-3.

Escalation inequalities (the H-DECEPT-3 no-escalation equalities must
now FAIL in the intended direction): p(S betrayal 2) = 8 > p(Q) = 4;
p(S betrayal 3) = 15 > p(V) = 5.

(a) Reform W (ext 93): 20 corrects, betray at w=8 (p = 5, b 0->1),
then 100 honest rounds. At c = 100 the forgiveness triggers: b = 0.
rel(W) = floor(120000/126) = 952. Second betrayal at w=8, c=100:
base = floor(800/108) = 7, p = 7*(1+0) = 7.
Fresh X (ext 94): 100 corrects, one betrayal at w=8: base = 7, p = 7.
Reform equality: p(W second) == p(X) == 7. W is treated exactly as a
first-time betrayer at its streak: reform, not permanent exile.

(b) R1 (ext 95): 120 corrects, no wrongs. rel = 1000, b = 0.
Truth-teller unaffected.

(c) C0 (ext 96): one wrong at c=0: p = 0, b stays 0, rel = 1000
(total < 2). Then 20 corrects and a betrayal at w=8: p = 5*(1+0) = 5,
rel = floor(20000/27) = 740. A no-streak error stays linear null and
does not inflate a later betrayal penalty.

Patient-farmer probe P (ext 97), informational: 100 corrects, betray
at w=8 (base 7, p = 7, b 0->1), 100 corrects (forgiveness: b -> 0),
betray at w=8 (base 7, p = 7). Expected: p1 = 7, p2 = 7,
rel = floor(200000/216) = 925. A farmer patient enough to fully
reform between betrayals sustains the same reliability as under the
old rule: that is the documented price of allowing reform, and it
costs 5x the honest rounds per betrayal of the H-DECEPT-3 farmer.

## Kill bars

K1: 3/3 runs byte identical (sha256 recorded in REPORT.md).
K2: after each rebuild streak(S) == 20; rel(S) exactly
    1000, 930, 833, 740, 671.
K3: betrayal exposures exactly 869, 769, 681, 620, 571; penalties
    exactly 2, 8, 15, 20, 25; b after each betrayal exactly 1..5.
K4: escalation: p(S#2) = 8 > p(Q) = 4; p(S#3) = 15 > p(V) = 5;
    marginal costs strictly increasing 3 < 9 < 16 < 21 < 26;
    exposures 3, 4, 5 below 769 and strictly falling
    (681 > 620 > 571).
K5: controls: Q p == 4, rel == 800; V p == 5, rel == 769;
    (a) b(W) == 0, rel(W) == 952, p(W2) == 7, p(X) == 7,
    p(W2) == p(X); (b) rel(R1) == 1000, b(R1) == 0;
    (c) first wrong p == 0, b == 0, later betrayal p == 5.
K6: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag
    (safebin PATH, no python3/python at any point). Unfrozen variant
    only: frozen belief_deception, belief_trajectory, belief_repeated
    sources untouched; paper untouched; nothing pushed to GitHub;
    explicit pathspecs on every git operation.

## Verdict rule

BELIEF-ANTIFARM-COMPLETE iff K1-K6 all pass: rel(S) goes below 769
and keeps falling under the H-DECEPT-3 farming strategy, the second
betrayal costs strictly more than the first, all controls hold, and
the escalation table above is confirmed in-binary. Any kill bar
failure, or any prereg-order violation, voids the wave.
