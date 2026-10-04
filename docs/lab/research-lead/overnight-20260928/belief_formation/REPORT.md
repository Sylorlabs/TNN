# REPORT: Rational Belief Formation from Evidence (Priority 9)

## Question

Can TNN form rational beliefs from available evidence: adopt a hypothesis
provisionally on weak evidence, become uncertain on contrary evidence, and
revise on strong independent evidence, with confidence tracked, provenance
answerable, and old evidence retained? Rationality is scored relative to the
evidence available at the time, never against omniscience.

## Mechanism

All state lives in one learner owned state block (296 i32 cells). No new
modes, bridges, handlers, or semantic cases.

Belief score: each hypothesis accumulates support in milli units.
An observation of hypothesis h with event strength w in {1 weak, 2 moderate,
3 strong} from source s contributes `w * rel(s) * disc / 1000`, where:

- `rel(s)` is source reliability per mille, LEARNED from verification
  outcomes only. Every source starts neutral at 1000 and stays neutral until
  at least 2 verifications are observed. There is no researcher written
  ranking of sources anywhere in the code.
- `disc` is the independence discount: the k-th claim by the same source for
  the same hypothesis within one evidence episode contributes half the
  previous one (1000, 500, 250, ...). Repetition is not independence.

Status derivation from the signed score B = s1 - s2 and two bands:

- U (uncertainty band) = largest single contribution ever observed.
- T (certainty bar) = 2 * U. Certainty requires support that no single
  observation could have supplied on its own.
- Both hypotheses supported and |B| <= U: UNCERTAIN.
- |B| >= T: CONFIDENT in the leader. Otherwise PROVISIONAL in the leader.
  One sided evidence can only ever be PROVISIONAL, never UNCERTAIN.

Honest scaffold split. Researcher scaffold: the table layout, the band rules
U = wmax and T = 2U, the halving discount, the status cutoffs. Learner owned:
every reliability value, every support total, wmax itself, every status
verdict, and every provenance answer. The band *values* come from experience;
only the band *rule form* is scaffold.

## World script (fixed, deterministic, no randomness)

Calibration (reliability learning, 4 verifiable facts):
- Sa claims H1 weak, truth H1: correct. Sa claims H2 weak, truth H1: wrong.
  Sa track record 1/2, rel 500.
- Sb claims H2 weak then H2 moderate, truth H2 both: correct. Sb 2/2, rel 1000.

Phase 1: Sa reports H1 weak twice. Only H1 evidence exists.
Phase 2: Sb reports H2 moderate once (credible contrary evidence); Sa doubles
down with three H1 moderate claims.
Phase 3: three fresh sources Sc, Sd, Se each report H2 strong once
(independent: three distinct sources, first claim each, no discount).
Then the world reveals truth H2 and reliabilities update from the outcome.

## Results (3/3 byte identical, sha256 9eca77362447e781484e48add05eaad52fa616fa9f366956e53d94e680118e4b)

```
MAIN P1: leader=1 status=PROVISIONAL s1=750 s2=0 conf=750 U=2000 T=4000
MAIN P2: leader=1 status=UNCERTAIN s1=2500 s2=2000 conf=500 U=2000 T=4000
MAIN P3: leader=2 status=CONFIDENT s1=2500 s2=11000 conf=-8500 U=3000 T=6000
```

Phase 1: two weak reports from a 1/2 track record source give support 750,
far below the certainty bar 4000. The learner adopts H1 PROVISIONALLY, not
certainly. Rational: it is the only evidence available, and its weakness is
reflected in the status.

Phase 2: credible contrary evidence (Sb moderate, rel 1000, contrib 2000)
meets Sa's discounted repetition (1000 + 500 + 250 = 1750 on top of 750).
Support stands 2500 vs 2000, |B| = 500 inside the uncertainty band 2000.
The learner becomes UNCERTAIN. It does not stubbornly hold H1 (status moved
off provisional) and does not flip to H2 (margin far too small). Rational:
the evidence is genuinely conflicting.

Phase 3: three independent strong reports add 9000 to H2. |B| = 8500 against
a certainty bar of 6000. The learner revises to CONFIDENT H2. Rational: the
new evidence is strong, independent, and one sided.

## Rationality scores (relative to evidence at time)

- Phase 1: 1/1. Provisional H1 is the rational response to weak one sided
  evidence. Certainty would be overconfidence; no belief would ignore data.
- Phase 2: 1/1. Uncertainty is the rational response to conflicting
  evidence. Stubborn H1 or instant H2 flip would both misread the margin.
- Phase 3: 1/1. Confident H2 is the rational response to strong
  independent evidence outweighing everything prior.
- Total: 3/3.

## Measurements

Belief state per phase: printed above (leader, status, supports, confidence,
bands). Uncertainty representation: the learner tracks confidence |B|,
conflict (both hypotheses supported), and the bands U/T at all times; the
phase 2 line shows all of them jointly determining UNCERTAIN.

Evidence provenance: `belief_why` lists every contributing record.
After phase 3, why-H2 returns exactly the 4 H2 records
(seq 7 phase 2 Sb moderate; seqs 11, 12, 13 phase 3 Sc/Sd/Se strong) and
why-H1 returns the 5 H1 records (seqs 5, 6, 8, 9, 10). The learner can say
why it believes H2 and why it ever believed H1.

Revision speed: first contrary evidence at seq 7, confident revision at
seq 13. Contrary pieces to confident revision: 4 (1 moderate credible +
3 strong independent). A provisional H2 lean appears after 3 contrary
pieces. The learner neither flips on first contact nor waits forever.

Old evidence availability: all 13 records (4 calibration + 2 + 4 + 3) are
retained after phase 3 and verification. Nothing is deleted or overwritten;
the superseded H1 belief remains fully explainable.

No hardcoded authority hierarchy: at init every source reads rel 1000
(asserted in binary for a fresh source). Sa's rel 500 and Sb's rel 1000
exist only because calibration verifications put them there. After the
final verification Sa falls to 142 (1/7) from its wrong H1 claims while
Sb stays 1000 (3/3).

## Ablations (both in binary, both pass)

ABL-REL (reliability learning disabled, all rel fixed 1000): phase 2 goes
PROVISIONAL H1 (leader 1, conf 3000, s1 5000 vs s2 2000), stubbornly holding
H1 on the discredited source's loud repetition despite credible contrary
evidence. It still revises to CONFIDENT H2 in phase 3. Conclusion:
reliability learning is causal for the rational phase 2 outcome; it changes
when and how the learner moves, not just the endpoint.

Probe R (repetition attack: one neutral source repeats a weak H1 claim
6 times): with the independence discount the learner stays PROVISIONAL
(conf 1968 < T 2000); with the discount ablated it goes CONFIDENT
(conf 6000 >= T 2000) on a single source repeating itself. Conclusion: the
discount is load bearing against manufactured confidence; repetition is
treated as repetition, not as six independent witnesses.

## Architecture accounting

- Cognition lines added: 406 (belief.zag, self contained).
- New modes: 0. New bridges: 0. New handlers: 0. New semantic cases: 0.
- Learner state structures created: one evidence table (32 records),
  one source reliability table (8 sources), one episode discount table.
- Net capability: 3 phase rational belief formation + provenance queries +
  retention + 2 causal ablations, at ~223 lines per capability, in line
  with the C181-C189 ledger.

## Limitations (honest)

- Event strength (weak/moderate/strong) is assigned by the world script at
  observation time. It is an observation property, not a source hierarchy,
  but the world, not the learner, decides an event is strong. Strength
  induction from raw observations is future work.
- The band rule forms (U = wmax, T = 2U) are researcher scaffold; only the
  values are learner derived. A fully learner owned decisiveness rule
  (e.g. from the learner's own error frontier) is not yet implemented.
- Single binary question; belief interaction across multiple questions,
  and belief revision under memory pressure, not tested.
- Not yet merged into the tag-61 consequence substrate. Merge path: evidence
  records map to substrate rows (kt=new, ka=hypothesis, kb=seq; fields carry
  weight, source, phase, contribution), reliability reuses the kt=3 source
  reliability rows from C194, and belief status becomes a 7th substrate
  behavior. No new subsystem needed.

## Verdict

BELIEF-FORMATION-COMPLETE. Rationality 3/3 phases relative to evidence at
time. Both ablations pass, proving reliability learning and the
independence discount are each causal for rational outcomes. Deterministic
3/3 byte identical. Pure Zag, safebin, unfrozen only, paper untouched,
nothing pushed.
