# REPORT: Betrayal-History-Aware Reliability Update (H-DECEPT-4)

Wave: 2026-10-02. Verdict: BELIEF-ANTIFARM-COMPLETE. All kill bars
K1-K6 evaluated against the frozen PREREG.md (committed e443c5bd9
before any implementation source existed; prereg-order self check
holds; no amendments).

## What was tested

H-DECEPT-3 (commit 8be4b18d4, BELIEF-REPEATED-COMPLETE) proved the
H-DECEPT-2 trajectory update p = floor(c*w/(c+w)) is FARMABLE:
repeat betrayal is punished exactly as the first, and rel(S)
converges to the fixed point 769, not distrust. This wave implements
the H-DECEPT-4 specification: a per-source betrayal count b
(learner-owned) that scales the penalty multiplicatively,
p = base * (1 + b), with slow symmetric forgiveness (one unit of b
per 100 consecutive honest outcomes). The rule is general, not a
strike threshold: no ban, no mode, no special case on the count.

## Results

All in-binary checks passed (exit 0, "ALL PASS"). 3/3 runs byte
identical (sha256
4a6e18b39f561b6652c4ad7de3040288ed7bc40f0c5b4bb3e7a45d9a255327ae).
Stdout byte verified with od -c spot check.

### D4: five betrayals under the H-DECEPT-3 farming strategy

| betrayal | prior b | c | w | base | p = base*(1+b) | marginal 1+p | exposure rel(S) | prereg | match |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | 20 | 3 | 2 | 2 | 3 | 869 | 869 | yes |
| 2 | 1 | 20 | 5 | 4 | 8 | 9 | 769 | 769 | yes |
| 3 | 2 | 20 | 8 | 5 | 15 | 16 | 681 | 681 | yes |
| 4 | 3 | 20 | 8 | 5 | 20 | 21 | 620 | 620 | yes |
| 5 | 4 | 20 | 8 | 5 | 25 | 26 | 571 | 571 | yes |

Escalation table: penalties 2, 8, 15, 20, 25; marginal costs
3, 9, 16, 21, 26, strictly increasing. The second betrayal costs 9
instances vs 3 for the first: escalation inequality holds.

Rebuilds verified real each time: streak(S) == 20 after all five
rebuilds, rel(S) exactly 1000, 930, 833, 740, 671, and b exactly
0, 1, 2, 3, 4 before the five betrayals.

### The 769 bar is beaten

H-DECEPT-3 exposures: 869, 833, 810, 800, 793, converging to the
fixed point 769 from above. H-DECEPT-4 exposures: 869, 769, 681,
620, 571: below 769 from the third betrayal on and strictly
falling. Long-run analytic (frozen in prereg): after n pure (20, 8)
cycles rel(n) = 20000n / (21n + 2.5n(n+1)), which tends to 0. There
is no positive fixed point: the escalating penalty contributes a
quadratic term to the denominator, so any fixed-period periodic
betrayer converges to distrust.

### Escalation controls: the old equalities break in the right direction

Q (fresh source, one betrayal at w=5): p = 4, rel = 800, identical
to H-DECEPT-3. V (fresh source, one betrayal at w=8): p = 5,
rel = 769, identical to H-DECEPT-3. A first betrayal is punished
exactly as before: the history term only affects repeats.
In-binary inequalities: p(S betrayal 2) = 8 > p(Q) = 4;
p(S betrayal 3) = 15 > p(V) = 5. Repeat betrayal now costs strictly
more than a first betrayal at identical (c, w).

### Critical controls

(a) Reform W: one betrayal at w=8 (p = 5, b 0->1), then 100 honest
rounds. Forgiveness triggers at c = 100: b = 0, rel = 952.
Second betrayal at w=8, c=100: p = 7. Fresh X (100-streak, one
betrayal at w=8): p = 7. Reform equality p(W2) == p(X) == 7 holds:
W is treated exactly as a first-time betrayer at its streak.
Reform is possible; exile is not permanent.

(b) R1 truth-teller (120 corrects): rel = 1000, b = 0. Unaffected.

(c) C0 single no-streak error: p = 0, b stays 0, rel = 1000
(linear null, history not poisoned). A later 20-streak betrayal at
w=8 costs p = 5, rel = 740: the no-streak error did not inflate it.

### Patient-farmer probe (informational)

P: 100 honest rounds, betray at w=8 (p = 7), 100 honest rounds
(full forgiveness, b -> 0), betray at w=8 (p = 7). rel = 925,
both penalties 7, no escalation across a full reform interval.
A farmer patient enough to fully reform between betrayals sustains
the same reliability as under the old rule: that is the documented
price of allowing reform, and it costs 5x the honest rounds per
betrayal of the H-DECEPT-3 farmer (100 vs 20). Fast farming, the
attack H-DECEPT-3 characterized, now converges to distrust.

## Hypothesis verdict (frozen rule from PREREG.md)

H-DECEPT-4 completes as BELIEF-ANTIFARM-COMPLETE: (a) all five
rebuilds show streak 20 with rel exactly 1000/930/833/740/671;
(b) exposures exactly 869/769/681/620/571 with penalties exactly
2/8/15/20/25 and b exactly 0..4 before / 1..5 after; (c) the
escalation inequalities hold in-binary (8 > 4, 15 > 5) with
strictly increasing marginal costs 3 < 9 < 16 < 21 < 26;
(d) exposures 3, 4, 5 are below the frozen 769 bar and strictly
falling, with the long-run limit at distrust; (e) all three
critical controls hold, including the reform equality
p(W2) == p(X) == 7. The farming strategy H-DECEPT-3 characterized
no longer sustains usable trust: repetition makes each betrayal
strictly more expensive, and reliability converges to distrust
rather than to a positive fixed point.

## Honesty and limits

The rule FORM is researcher-authored; only its inputs (streaks,
betrayal counts) are learner-owned. This wave is mechanism evidence
(L2 class), not L3 representational invention. The worlds are
scripted D4/Q/V/W/X/R1/C0/P structures, not fresh sealed
adversarial worlds; a sealed re-test is still owed before any
generality claim. The fixed-point and long-run results are analytic
consequences of the rule, confirmed in-binary; they are not learner
discoveries. Known limitation, measured in-binary: full reform
between betrayals (100 honest rounds per betrayal) resets the
history term, so a maximally patient periodic betrayer sustains
rel 925, equal to the old rule at that honesty rate. Forgiveness
is the price of reform; the rate (1 unit per 100 honest rounds) is
the tunable parameter trading reform speed against farming cost.

## Kill bars

K1 PASS: 3/3 byte identical (sha256 4a6e18b3...).
K2 PASS: after each rebuild streak(S) == 20; rel(S) exactly 1000,
    930, 833, 740, 671.
K3 PASS: betrayal exposures exactly 869, 769, 681, 620, 571;
    penalties exactly 2, 8, 15, 20, 25; b before exactly 0..4,
    after exactly 1..5.
K4 PASS: p(S#2) = 8 > p(Q) = 4; p(S#3) = 15 > p(V) = 5; marginal
    costs strictly increasing 3 < 9 < 16 < 21 < 26; exposures 3-5
    below 769 and strictly falling (681 > 620 > 571).
K5 PASS: Q p == 4, rel == 800; V p == 5, rel == 769;
    (a) b(W) == 0, rel(W) == 952, p(W2) == 7, p(X) == 7,
    p(W2) == p(X); (b) rel(R1) == 1000, b(R1) == 0;
    (c) no-streak wrong p == 0, b == 0, later betrayal p == 5.
K6 PASS: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases.
    Pure Zag (safebin PATH, no python3/python present at any point).
    Unfrozen variant only; frozen sources untouched; paper
    untouched; nothing pushed; explicit pathspecs on all git
    operations.

## Artifacts

- PREREG.md (frozen, committed e443c5bd9 before implementation;
  no amendments; prereg-order self check holds)
- NAMECHECK.md (toolchain guard Step 0 recorded)
- belief_antifarm.zag (source, pure Zag)
- belief_antifarm_bin (binary, 71650 bytes)
- compile.log (znc warnings only, same analyzer class as H-DECEPT-3)
- run1.txt, run2.txt, run3.txt (byte identical outputs)

Architecture accounting: capability added 0 lines to the protected
core; new hardcoded semantic cases 0; modes/bridges/handlers 0;
learner-state structures created: 1 (per-source betrayal count
cell; source row widened 4 -> 5 cells); researcher-authored
machinery: the betrayal-history rule form (new, counted honestly,
not learner-invented).
