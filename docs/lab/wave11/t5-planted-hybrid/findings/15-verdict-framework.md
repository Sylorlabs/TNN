# Track 5 capstone — the verdict framework (slice 15)

## 1. Slice
Track 5 (planted-only vs learned-only vs hybrid), slice 15: the preregistered verdict
framework — metric weights, decision tree, track-level kill criteria, and the per-arm
recommendation format. Written BEFORE the other Track 5 slices' results are in; it is the
prereg, not the verdict. Changing any weight or branch after results requires Micah's
re-approval (program law 4).

## 2. Falsifiable claim
This framework classifies every possible Track 5 outcome — any combination of the five
metrics below across the three arms — into exactly one verdict per arm (GO / DEAD /
NEEDS-DECISION) with no added rules and no re-weighting. If a real result forces a new
branch, a new metric, or a weight change, the framework's completeness claim is killed.

## 3. Design
Arms, fixed per slices 02/03/14: A = planted-only (learn-gate, Zharovia domain, 240
facts, 12 deliberately false); B = learned-only (identical domain spec, learns from
scratch); C = hybrid (provenance-tagged lifecycle, kb_unplant, slice 14).

**Metric set and weights (sum = 100). Integrity is ALSO a gate (see tree step 1):**
- Mastery 30% — clean held-out recall (A ≥85% required for the comparison to be valid,
  slice 03-K(c)). Weight justification: useless knowledge is useless, but all three arms
  are engineered for recall, so mastery is baseline, not the discriminator.
- Revisability 25% — contradiction-suite score (12 false plants + 20 probes) AND the
  ex-planted truth-tracking metric (slice 14-K(2)). Justification: self-repair is the
  entire reason B and C exist; the two biggest falsification bars in the track sit here.
- Integrity 25% — refusal invariance, hallucination rate on unknown probes (≤5%, slice
  03-K(b)), provenance K1–K3 (slice 07), byte-identical reruns. Justification: program
  laws 2, 5, 8 — but note it is under-weighted deliberately because integrity is a GATE
  first (a failing arm is disqualified, not scored); the 25% only ranks survivors.
- Retention 10% — scores at 10x/100x episode legs, no degradation (testing standard).
- Cost 10% — trainer interventions per 100 episodes (escalations, ratifications), compute
  per episode. Justification: Micah's autonomy default — trainer-as-backup, not primary —
  so cost breaks ties, never overrides mastery or revisability.

**Decision tree (evaluated in order; first match binds):**
1. Integrity gate: any arm failing an integrity kill clause (03-K(b), 07-K1–K3, refusal
   break, non-identical rerun) is DEAD regardless of other metrics. Weights never trade
   integrity for recall.
2. Hybrid-special: if C's score vector is statistically indistinguishable from A's on all
   five metrics, C is DEAD (planted with machinery — Occam). If C matches B on
   revisability within ±5pp at equal-or-lower cost, B is DEAD for the hybrid's scenario
   (redundant arm, no-free-lunch says keep the winner).
3. If hybrid wins mastery but fails integrity → integrity gate (step 1): DEAD. No
   appeal; integrity is 0% of the constitution's negotiability (RC1).
4. If learned-only wins mastery + revisability but costs ≥10x arm A's cost →
   NEEDS-DECISION with the scenario-fit table (step 6), not an automatic GO: the
   verdict routes to Micah with cost scenarios priced.
5. If no arm dominates (no arm is best on both mastery and revisability among
   survivors) → scenario-fit table (below); each arm gets GO-in-scenario /
   NEEDS-DECISION, never a blanket GO.
6. Scenario-fit table (preregistered, the "no single winner" outcome):
   - Closed, audited domain + trainer available → A: GO (lookup-table honesty is a
     feature); C: GO if escalation rate < 1/100 eps; B: NEEDS-DECISION (why learn
     what is known?).
   - Open/changing domain, world evidence available → B or C: GO on revisability
     leader; A: DEAD (brittleness claim, slice 03).
   - Adversarial/sensor-spoof risk → whichever arm held refusals under spoof:
     GO; the others NEEDS-DECISION (accepted program hole — report as-is).
   - Cost-capped deployment (no trainer in the loop) → highest mastery-per-cost
     survivor: GO; arms needing per-episode ratification: DEAD for that scenario.

**Track-level binding kill criteria (what kills planted knowledge as a program
direction entirely):**
- K-T1: A scores ≥75% on the contradiction suite (slice 03-K(a)) — planted-only
  self-repaired, so the "planted" concept collapses; the arm's identity is dead.
- K-T2: across ALL arms, provenance K2 fails (deliberation outcomes differ with
  provenance stripped) — planted status exercises hidden evidential privilege no
  arm can bound; planting is uncontrollable, kill the direction.
- K-T3: B reaches mastery parity with A (within 5pp) while beating A on
  revisability by ≥20pp AND C adds nothing over B (step 2) — planting buys nothing
  anywhere: kill planted knowledge as a direction, keep the arms as controls.
- K-T4: A fails clean recall <85% (slice 03-K(c)) AND B fails to reach 70% —
  the domain harness is malformed; the TRACK is voided, not any arm (rerun, don't
  conclude).

**Recommendation format for Micah (per arm):**
`ARM <A/B/C>: <GO | DEAD | NEEDS-DECISION> — <one-line verdict>. Evidence: mastery
<x%>, revisability <x%>, integrity <pass/fail + clause>, retention <x% @ scale>,
cost <trainer-eps + compute>. Binding note: <which tree step / kill clause fired>.
If NEEDS-DECISION: the exact question for Micah + scenario-fit rows.`

## 4. Kill bar
The framework itself dies (completeness claim) if: (a) any real Track 5 result
requires adding a metric, branch, or re-weighting to classify; (b) two arms tie on
the weighted composite AND the scenario-fit table cannot break the tie on any
preregistered scenario; (c) an integrity-failing arm cannot be disqualified without
invoking an unlisted rule. Separately, Micah may reject the weights before the run;
after his sign-off they are frozen (law 4).

## 5. Honesty notes
Weakest: the weights are judgment, not measurement — 30/25/25/10/10 encodes my read
of Micah's values (autonomy, integrity-first, honest failure), and a different
principal would weight differently; the prereg's protection is freezing, not
objectivity. The integrity-as-gate-then-25% design double-counts by construction —
deliberate, but if a survivor's integrity edge is what decides the composite, the
report must say so explicitly. Cost at 10% will look too low to anyone who has to
run the trainer console; if Micah disagrees pre-run, the number changes before
sign-off, not after. NOT claiming this framework picks "the true best arm" — it
picks the verdict Micah's stated values imply, with every trade-off named. The
scenario-fit table is where no-free-lunch lives; a blanket GO for any arm out of
step 5/6 is a framework violation.

## 6. Next build step
Get Micah's sign-off on the five weights and the four track kill clauses BEFORE any
Track 5 trial runs; then hand the frozen scorecard + decision tree to the trial
builders as the scoring contract, and archive the signed version alongside the
prereg so any post-result edit is detectable.
