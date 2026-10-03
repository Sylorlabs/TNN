# REPORT: Forgiveness Clock for Belief Source Reliability (Belief Forgiveness Worker)

Verdict: BELIEF-FORGIVENESS-COMPLETE. Frozen prereg 48ed4891e with
AMENDMENT 1 (d8669aae0) governed every check below; all kill bars K1-K5
hold. 3/3 runs byte identical
(sha256 2cb2d82f1bf187f834841b011dee6572ab8991f2604e13c5040ba2a19332e2b9).
Binary stdout byte verified (od -c spot check) before trusting it.

## What was built

One learner owned addition to the BELIEF-MISINFO machinery: a signed
streak counter per source (consecutive same outcome calibration
length), plus the streak gated wrong retirement rule in ev_calibrate.
On a correct outcome at streak >= 2 with historical wrongs present,
one historical wrong is retired (total decrements by 1; the new correct
still increments correct). Wrong outcomes only add to the record,
exactly as the old fraction rule. No tunable parameter exists: the
rule form is researcher scaffold (same category as the independence
discount halving); every value it operates on is learner state; the
recovery rate is fully determined by the source's own record.

## Findings

### Recovery: yes, gradual, proportional (M3)

World M3 (continues M2 state: 4 historical wrongs, streak -1). After S
became fully reliable, rel(S) traced 851, 888, 925, 962, 1000 at
+1..+5 clean rounds, and stayed 1000 at +20. The wrongs counter drained
visibly in learner state: 4, 3, 2, 1, 0. Full recovery required exactly
wrongs+1 = 5 consecutive clean rounds. Not instant (+1 gives 851, not
1000). Proportional: a single isolated wrong costs 2 clean rounds
(M5), 4 wrongs cost 5. The parent experiment's fraction rule reached
only 913 after 20 clean rounds; the forgiveness rule reaches 1000 in 5.

### M1/M2 rationality preserved (K2)

Every BELIEF-MISINFO prediction P1-P8 holds exactly on the new
machinery: M1 copy/exposure/contradiction/fragility (correction in 2,
reassertion reopens uncertainty), M1b correction count 3, M2 degrade
952/909/913/875/880/846 with W1 control at 1000, downstream discount
1692. The forgiveness rule is inert in all these worlds (no correct
streak >= 2 coexists with historical wrongs there), so correction and
downgrade behavior are untouched. nevicted == 0 throughout.

### Vulnerability: the laundering channel (M4, M4b, M5)

M4: a strategic liar telling truth 2/3 of the time (R,R,W repeating)
saw rel(S) climb 666, 800, 857, 888 across 12 rounds, with wrongs
oscillating 0/1 as each lie is retired by the following truth pair.
In the limit rel approaches 1000 while the source keeps lying on every
third claim. Under the old fraction rule the same source converges to
666. The forgiveness rule therefore creates a genuine rehabilitation
channel priced at 2 truthful claims per lie.

M4b: an alternating liar (R,W) gets no forgiveness at all (500, 500,
500; 3 wrongs unforgiven), because the streak never reaches 2. The
channel requires sustained truth between lies, but 2 per lie suffices.

M5: forgiveness is not immunity. After full recovery (record (42,42),
note the record keeps growing past recovery), one relapse dropped
rel(S) 1000 -> 976 immediately, and repair cost 2 clean rounds
(977, then 1000). A reformed source that relapses pays at once.

Honest accounting of the cost: retired wrongs are destroyed
information. A fully forgiven source is indistinguishable in learner
state from a never degraded source. Any wrong retiring forgiveness
rule has this property; the experiment measures its price (a 2:1 truth
ratio buys full credibility) rather than hiding it. Mitigations not
implemented: capping retired wrongs, pacing forgiveness by long run
accuracy, or retiring only wrongs older than the streak. Each would
introduce a researcher set parameter, which is why none was adopted
here; they are open follow ups.

## Kill bar results

K1: 3/3 byte identical. HOLD.
K2: P4 exact (all M1/M1b/M2 predictions from BELIEF-MISINFO unchanged).
HOLD.
K3: P5 exact (M3 recovery 851/888/925/962/1000 at +1..+5, 1000 at +20;
nevicted == 0; +1 is 851, not 1000). HOLD.
K4: P6/P7/P8 hold (P8 as transparently amended: 976/977/1000; the
amendment corrected the author's post M3 state model from (27,27) to
(42,42) before the implementation was updated, and was recommitted
first). Laundering trajectory, alternating control, and relapse cost
all exact. HOLD.
K5: pure Zag, safebin PATH, no forbidden executables, prereg committed
before implementation, amendment recommitted before the corrected
checks, 0 modes/bridges/handlers, frozen source untouched, paper
untouched, nothing pushed, explicit pathspecs. HOLD.

Rationality (evidence relative): M3 recovery to 1000 is rational 1/1
(20 consecutive correct verifications with zero wrongs remaining is
strong evidence of reform). M4's climbing reliability is rational 1/1
given the retirement rule and is the documented vulnerability, not a
scoring failure. M5's immediate relapse drop is rational 1/1.

## Architecture accounting

Cognition lines added: the forgiveness mechanism is about 15 lines
(streak cell per source row, streak update and retirement branch in
ev_calibrate, two small accessor helpers) plus world scripts
M3 checkpoints, M4, M4b, M5. New hardcoded semantic cases: 0. Modes:
0. Bridges: 0. Handlers: 0. Capability source delta: reliability now
recovers; correction and downgrade behavior unchanged.

## Deliverables in belief_forgiveness/

PREREG.md (frozen, committed first; AMENDMENT 1 recommitted before the
corrected implementation), NAMECHECK.md, REPORT.md (this file),
belief_forgiveness.zag (source), belief_forgiveness_bin (binary),
compile.log, run1.txt, run2.txt, run3.txt.

## Follow-ups specified (not decided here)

1. Parameter free mitigations for the laundering channel: test whether
a variant resists 2:1 laundering without adding a researcher set knob.
2. Interaction of forgiveness with the exposure step: currently a liar's
recorded false evidence is never retro edited (parent finding); whether
retired wrongs should also discount that source's past recorded
evidence weight is open.
