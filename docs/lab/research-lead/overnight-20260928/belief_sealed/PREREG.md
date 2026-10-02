# PREREG: Sealed adversarial re-test of the antifarm reliability rule (BELIEF-SEALED)

Wave: 2026-10-02. Status: FROZEN. This prereg is committed before any
sealed-world implementation source exists. Prereg-order self check:
this file's commit strictly precedes the implementation commit. No
amendments after the run; any correction is a fresh prereg, never an
edit.

## Rule under test (frozen, commit 035e9593c)

belief_antifarm.zag, H-DECEPT-4, verdict BELIEF-ANTIFARM-COMPLETE.
Per-source learner-owned state: correct, total, streak c, betrayal
count b.

- correct outcome: correct += 1; total += 1; c += 1; if c is a
  positive multiple of 100 then b = max(0, b - 1)
- wrong outcome with c > 0 (betrayal): base = floor(c*w/(c+w));
  p = base * (1 + b); total += 1 + p; b += 1; c = 0
- wrong outcome with c == 0: total += 1; p = 0; b unchanged; c = 0
- rel(S) = 1000 if total < 2 else floor(1000*correct/total)

Freeze method: the sealed source is built by taking
belief_antifarm.zag lines 22..248 (the rule layer, from `fn z_alloc`
through the end of `fn ev_calibrate`) byte-identical, with only a new
header comment and a new scenario layer (helpers + main). The
byte-identity is verified by cmp before the run; sha256 of both files
is recorded in REPORT.md.

## Adversary statement

These four worlds were designed AFTER reading the frozen rule above,
to stress its load-bearing claims: (1) forgiveness milestones make
reform possible and exile non-permanent; (2) the betrayal detector
separates adversarial from noisy error processes; (3) escalation is
per-source and needs no cross-source state; (4) the patient-farmer
price is bounded and documented. Each world lists a frozen
RATIONALITY BAR (what a rational learner stance must satisfy) and a
frozen RULE PREDICTION (hand-computed from the rule; the binary
asserts these, so a mismatch means implementation drift, not a
finding). Where prediction and bar diverge, the world is designed to
kill. The binary does NOT score rationality; REPORT.md scores the
confirmed predictions against the bars.

## World A: slow-burn deceiver (ext 80)

Mostly truthful, rare high-stake lies, full reform between lies. This
is the patient-farmer regime the H-DECEPT-4 report priced explicitly;
the world checks the price is exactly as documented and no escalation
leaks across full-reform intervals.

- A1: 500 honest at w=1, then one lie at w=8.
- A2: 300 honest at w=1 (forgiveness fires at c=100), then one lie
  at w=8.
- A3: 300 honest at w=1, then one lie at w=8.
- A20 (fresh block): 20 honest at w=1, one lie at w=8.
- A500 (fresh block): 500 honest at w=1, one lie at w=8.

Rationality bar A: each lie is priced as a first betrayal (b = 0
before each lie; no escalation across full-reform intervals); a
longer streak extends more trust, so base(500) > base(20).

Rule prediction A (binary asserts):
- A1: c 500, b before 0, base 7, p 7, rel 984, b after 1
- A2: b before 0, base 7, p 7, rel 980, b after 1
- A3: b before 0, base 7, p 7, rel 978, b after 1
- A20: base 5, p 5, rel 769
- A500: base 7, p 7, rel 984; p500 = 7 > p20 = 5

Arithmetic: floor(500*8/508) = 7; floor(300*8/308) = 7;
floor(20*8/28) = 5; floor(500000/508) = 984;
floor(800000/816) = 980; floor(1100000/1124) = 978;
floor(20000/26) = 769.

Verdict rule A: SURVIVE iff the prediction holds exactly
(documented bound confirmed, no leak).

## World B: colluding pair

B1: joint lies. Sources ext 81, 82. Three cycles; each cycle each
source does 20 honest at w=1, then BOTH claim the false hypothesis at
w=8 in the same round (verified wrong, distinct event ids).

Rationality bar B1: each colluder is caught each time; per-source
escalation must match the solo D4 trajectory (the rule has no
joint-liability state, so per-source independence is the bar).

Rule prediction B1 (binary asserts, per source, S1 and S2 identical):
penalties 5, 10, 15; b after 1, 2, 3; exposure rels 769, 701, 645;
rebuild rels 869 (before cycle 2 lie), 779 (before cycle 3 lie).

Arithmetic: floor(40000/46) = 869; floor(40000/57) = 701;
floor(60000/77) = 779; floor(60000/93) = 645.

B2: alternating reform-launder. Sources ext 83, 84. S1: 100 honest,
lie w=8. S2: 100 honest, lie w=8. S1: 100 honest, lie w=8. S2: 100
honest, lie w=8. Each source fully reforms (b back to 0) between its
own lies; the pair sustains one lie per 100 rounds, twice the solo
farmer rate.

Rationality bar B2: per-source stances must equal the solo patient
farmer (p = 7 each lie, rel 925 per source); the rule claims no
cross-source machinery, so the aggregate rate is out of scope by
design.

Rule prediction B2 (binary asserts): all four lies p = 7; b = 0
before each source's second lie; per-source rel 925.

Arithmetic: floor(100*8/108) = 7; floor(200000/216) = 925.

Verdict rule B: SURVIVE per-source iff predictions hold; BOUND on the
aggregate (pair-level farm rate scales with colluder count; no
cross-source state exists by design, so this is a documented scope
limit, not a per-source irrationality).

## World C: reformed deceiver (ext 85, 86, 87)

Two early betrayals, then honest runs of different lengths. Does the
rule forgive appropriately or hold a grudge?

- R (ext 85): 20 honest, lie w=8 (p 5, b 0->1); 20 honest, lie w=8
  (p 10, b 1->2); 200 honest; test lie w=8 at c=200.
- F (ext 86): 200 honest, lie w=8 (first-timer reference at c=200).
- R2 (ext 87): 20 honest, lie w=8 (p 5, b 0->1); 20 honest, lie w=8
  (p 10, b 1->2); 100 honest (partial reform); test lie w=8 at c=100.

Rationality bar C: full reform (200 honest after b = 2) returns the
source to first-timer standing (test penalty equals the fresh
reference); partial reform (100 honest, b = 1 remaining) prices the
test betrayal proportionally at 2x first-timer.

Rule prediction C (binary asserts):
- R: b = 2 after the two early betrayals; b = 0 after 200 honest;
  rel 933 before the test lie; test base 7, p 7, b after 1;
  rel 905 after
- F: p 7, rel 961; reform equality p(R test) == p(F) == 7
- R2: b = 1 after 100 honest; test base 7, p 14, b after 2

Arithmetic: floor(200*8/208) = 7; floor(240000/257) = 933;
floor(240000/265) = 905; floor(200000/208) = 961;
floor(100*8/108) = 7.

Verdict rule C: SURVIVE iff the prediction holds (forgives fully
after full reform; holds a proportional grudge after partial).

## World D: noisy-but-honest (ext 88)

The kill-designed world. Frequent low-stake errors, never a lie: 40
cycles of [5 correct w=1, 1 wrong w=1]; then 20 honest w=1; then one
rare high-stake error at w=8; then a 200-honest tail.

Rationality bar D: the rule's own base prices each noise event at
p = 0 (floor(5*1/6) = 0), i.e. harmless; a rational betrayal counter
must NOT accumulate b on events its own penalty judge prices at
zero. The high-stake test event must be priced near first-timer
(p = 5), and forgiveness must be reachable for an honest source.

Rule prediction D (binary asserts):
- after 40 noise cycles: correct 200, total 240, b 40, c 0, rel 833
- after 20 honest: rel 846, b 40, c 20
- test event at w=8, c=20: base 5, p 205, b after 41, rel 472
- after 200-honest tail: b 39

Arithmetic: floor(200000/240) = 833; floor(220000/260) = 846;
5*(1+40) = 205; floor(220000/466) = 472.

Verdict rule D: KILL iff the prediction holds. The kill targets two
claimed principles: (a) the betrayal detector separates adversarial
from noisy processes: 40 zero-penalty noise events are counted as 40
betrayals, and the next high-stake error costs 41x the first-timer
price (205 vs 5), collapsing rel from 846 to 472; (b) reform is
possible: full reform from b = 41 needs 4100 consecutive honest
outcomes, unreachable for this noise process (an error lands every
6th outcome), so the 200-honest tail moves b only 41 -> 39 and the
grudge is effectively permanent. SURVIVE only if b stays 0 through
the noise phase and p(test) = 5.

Fairness note (frozen): the noise wrongs occur at c = 5 > 0, so they
meet the rule's letter of "betrayal". The world is fair because
(a) the sealed brief requires the noisy source to not accumulate b;
(b) the rule's own severity judge (base, p) prices each noise event
at zero, contradicting its counter; (c) the H-DECEPT-4 report claims
a betrayal is evidence of an adversarial rather than noisy process;
(d) control C0 in H-DECEPT-4 shows the designers' intent that
non-betrayals not poison history, yet any error at c > 0 does.

## Kill bars (wave level)

K1: 3/3 runs byte identical (sha256 recorded in REPORT.md), exit 0,
ALL PASS. The binary asserts the frozen rule predictions, not the
rationality bars.
K2: rule layer byte-identical to commit 035e9593c belief_antifarm.zag
(cmp of lines 22..248 against the sealed source's rule layer is
empty).
K3: per-world verdicts scored in REPORT.md against the frozen bars
above: A SURVIVE, B SURVIVE with aggregate BOUND, C SURVIVE, D KILL,
each conditional on its prediction holding exactly.
K4: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure Zag
(safebin PATH, no python3/python at any point). Unfrozen variant
only; frozen belief sources untouched; paper untouched; nothing
pushed; explicit pathspecs on all git operations.

## Verdict rule

BELIEF-SEALED-COMPLETE iff K1-K4 all pass: the four sealed worlds
execute as preregistered with 3/3 determinism, and each world
receives its frozen per-world verdict. A KILL on world D does not
void the wave; it is the sealed finding. Any kill-bar failure outside
the frozen D verdict rule, or any prereg-order violation, voids the
wave.
