# REPORT: Sealed adversarial re-test of the antifarm reliability rule (BELIEF-SEALED)

Wave: 2026-10-02. Verdict: BELIEF-SEALED-COMPLETE. All kill bars
K1-K4 evaluated against the frozen PREREG.md (committed 99c1977cc
before any sealed-world implementation source existed; prereg-order
self check holds; no amendments).

## What was tested

The H-DECEPT-4 antifarm rule (commit 035e9593c,
BELIEF-ANTIFARM-COMPLETE): per-source betrayal count b scales the
wrong-outcome penalty as p = base * (1 + b), with forgiveness of one
b per 100 consecutive honest outcomes. All of its evidence worlds were
scripted D1/R1-family structures, and its REPORT.md recorded the owed
item: a sealed re-test before any generality claim. This wave is that
re-test. Four worlds were designed AFTER reading the frozen rule, to
stress its load-bearing claims: the priced patient-farmer regime,
per-source escalation under collusion, the forgiveness question
(grudge vs reform), and the betrayal detector's separation of
adversarial from noisy error processes.

Freeze method: the sealed source reuses belief_antifarm.zag lines
22..248 (fn z_alloc through fn ev_calibrate) byte-identical,
verified by cmp (empty diff). Only the header and scenario layer are
new. The binary asserts the frozen PREREG rule predictions, so its
ALL PASS certifies the rule executed with zero implementation drift;
the SURVIVE/KILL/BOUND verdicts below are then scored against the
frozen rationality bars, which the binary does not assert.

## Results

All in-binary checks passed (exit 0, "ALL PASS", zero FAIL lines).
3/3 runs byte identical (sha256
acbf0ae30122a92a278743cc050be0763bafa03679cdcdc26dc70e0bfd49a59e).
Stdout byte verified with od -c spot check: clean ASCII, ends with
"ALL PASS\n".

### World A: slow-burn deceiver. SURVIVE.

Mostly truthful, rare high-stake lies, full reform between lies.
Confirmed in-binary: A1 (500 honest, lie w=8): b=0 before, base=7,
p=7, rel=984. A2 (300 honest): b=0 before, p=7, rel=980. A3:
p=7, rel=978. No escalation leaks across full-reform intervals.
Streak comparison: fresh 20-streak lie costs p=5 (rel 769); fresh
500-streak lie costs p=7 (rel 984): longer trust extended, larger
base, as the trajectory formula intends. The sustained reliability
of the slow-burn deceiver sits at 978-984, inside the patient-farmer
price the H-DECEPT-4 report documented and accepted (rel 925 at the
100-honest rate). The rule behaves exactly as its designers priced
it. No finding.

### World B: colluding pair. SURVIVE per-source, BOUND on aggregate.

B1 joint lies (both sources lie together at w=8, three cycles):
confirmed in-binary, both sources identical: penalties 5, 10, 15;
b = 1, 2, 3; exposure rels 769, 701, 645; rebuild rels 869, 779.
Per-source escalation matches the solo D4 trajectory exactly:
colluders caught together are punished exactly as solo betrayers.
B2 alternating reform-launder (each source lies once per 200 rounds,
fully reforming between its own lies): confirmed in-binary, all four
lies at p=7, b=0 before each second lie, per-source rel=925. Each
source is indistinguishable from a genuinely reformed source, so the
per-source stances are rational given per-source evidence.

BOUND: the pair sustains one lie per 100 rounds at rel 925 per
source, twice the solo farmer rate; with N colluders the aggregate
deception rate scales as N/100 rounds while every member holds high
trust. The rule has no cross-source state by design, and no
per-source rule could distinguish the launderers from the reformed,
so this is a documented scope limit, not a per-source irrationality.
The antifarm guarantee is per-source only; a collusion-level farm is
outside the claimed envelope.

### World C: reformed deceiver. SURVIVE.

Two early betrayals (b=2), then honest runs. Confirmed in-binary:
after 200 honest, b=0, rel=933, c=200; the test lie at w=8 costs
p=7, exactly equal to the fresh 200-streak reference (p=7, rel=961):
reform equality holds, full reform returns first-timer standing, no
grudge. Partial reform (100 honest after b=2): b=1, test lie costs
p=14 = 2x first-timer: the rule holds a proportional grudge after
partial reform, exactly per its linear-milestone forgiveness form.
The rule forgives appropriately and does not exile.

### World D: noisy-but-honest. KILL.

Frequent low-stake errors, never a lie: 40 cycles of [5 correct w=1,
1 wrong w=1]. The rule's own base prices every noise event at p=0
(floor(5*1/6)=0). Confirmed in-binary: after 40 noise cycles b=40
(the rationality bar required 0); rel=833, which rationally tracks
the empirical 200/240 rate. After 20 further honest rounds
(rel=846, b still 40), one rare high-stake error at w=8, c=20 costs
p=205 = 41x the first-timer price of 5, collapsing rel from 846 to
472, with b=41. The 200-honest tail moves b only 41 -> 39.

The kill: the rule's counter and its own penalty judge contradict
each other. Each noise event was judged harmless (p=0) at the time,
yet each incremented the deceit counter by a full betrayal. The
forgiveness mechanism is unreachable for any source whose honest
error rate exceeds 1/100: this source would need 4100 consecutive
honest outcomes to clear b=41, but its noise process emits an error
every 6th outcome, so the grudge is effectively permanent. Two
claimed principles die here: (a) "a betrayal is evidence that the
source's error process is adversarial rather than noisy": 40
zero-penalty noise events are counted as 40 betrayals, so the
detector does not separate the two; (b) "reform is possible; exile
is not permanent": true only for near-perfect sources, false for any
persistently noisy honest source. Note the inversion the rule
produces: one high-stake lie followed by 100 honest rounds is fully
forgiven (world C), while forty harmless honest mistakes are never
forgiven (world D). Per the frozen verdict rule, world D is KILL.
Per the task brief, this finding is reported, not fixed.

Fairness of the world (frozen in prereg): the noise wrongs occur at
c=5 > 0, meeting the rule's letter of "betrayal"; the world is fair
because the sealed brief requires the noisy source to not accumulate
b, the rule's own severity judge prices each event at zero, the
H-DECEPT-4 report claims adversarial/noisy separation, and control
C0 shows the designers' intent that non-betrayals not poison
history.

## Kill bars

K1 PASS: 3/3 byte identical (sha256 acbf0ae3...), exit 0, ALL PASS,
zero FAIL lines. The binary asserted the frozen rule predictions,
not the rationality bars.
K2 PASS: rule layer (fn z_alloc through fn ev_calibrate) of
belief_sealed.zag is byte-identical to belief_antifarm.zag lines
22..248 at commit 035e9593c (cmp empty).
K3 PASS: per-world verdicts scored against the frozen bars: A
SURVIVE (predictions held: p=7,7,7; rels 984,980,978; p500=7 >
p20=5); B SURVIVE per-source with aggregate BOUND (B1 penalties
5,10,15 identical across colluders; B2 all lies p=7, rel 925 per
source; pair rate 2x solo); C SURVIVE (b=0 after 200 honest;
p(R test)==p(F)==7; partial p=14); D KILL (b=40 after noise vs bar
0; test p=205 vs bar 5; tail b 41->39 vs reachable forgiveness).
K4 PASS: 0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Pure
Zag (safebin PATH, no python3/python at any point). Unfrozen variant
only; frozen belief_deception, belief_trajectory, belief_repeated,
belief_antifarm sources untouched; paper untouched; nothing pushed;
explicit pathspecs on all git operations.

## Honesty and limits

The sealed worlds confirm the rule executes exactly as specified and
that its documented behaviors (patient-farmer price, per-source
escalation, full reform) are real, not artifacts. They also confirm
two undocumented behaviors the designers did not price: the
noise-grudge kill (world D) and the collusion-rate bound (world B2).
The D kill is a claim kill, not an implementation bug: the binary
proves the behavior is the frozen rule's. The natural repair
direction (count a betrayal only when base > 0, or make forgiveness
proportional rather than milestone-gated) is noted here and NOT
implemented, per the red-team brief. rel(S) itself remains a
rational stance throughout (it tracks correct/total in every world,
including D at 833); the irrationality is confined to the betrayal
counter b and the forgiveness gate. No generality claim for the
antifarm rule survives world D unqualified: the rule is antifarm
against periodic betrayers and colluders at the per-source level,
and unfit as stated for noisy-but-honest sources.

## Artifacts

- PREREG.md (frozen, committed 99c1977cc before implementation; no
  amendments; prereg-order self check holds)
- NAMECHECK.md (toolchain guard Step 0 recorded)
- belief_sealed.zag (source, pure Zag; rule layer byte-identical to
  H-DECEPT-4)
- belief_sealed_bin (binary)
- compile.log (znc warnings only: 7x E0101, same analyzer class as
  H-DECEPT-4)
- run1.txt, run2.txt, run3.txt (byte identical outputs)

Architecture accounting: capability added 0 lines to the protected
core; new hardcoded semantic cases 0; modes/bridges/handlers 0;
learner-state structures created 0 (H-DECEPT-4 betrayal cell reused
unchanged); researcher-authored machinery: the four sealed worlds
(scenario code only, counted honestly, not learner-invented).

## Verdict

BELIEF-SEALED-COMPLETE, with per-world scores: A SURVIVE, B SURVIVE
with aggregate BOUND, C SURVIVE, D KILL. The owed sealed re-test is
discharged. The antifarm rule's generality claim does not survive
unqualified: it holds against periodic betrayers and per-source
collusion, and it fails for noisy-but-honest sources, whose
zero-penalty errors accumulate an undischargable betrayal count.
