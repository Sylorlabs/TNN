# Governance Report: Wave 2 (Micah's 10 Priorities)

**Date:** 2026-10-01
**Worker:** Governance/Frontier Worker (Wave 2)
**Status:** GOVERNANCE-COMPLETE
**Ledger:** C181-C188 appended (8 new claims)

## 1. New Claims Summary (C181-C188)

All 8 workers from Micah's 10 priorities completed with verdicts.
All commits verified via git log. All exploratory (no frozen prereg).

| ID | Priority | Commit | Verdict |
|----|----------|--------|---------|
| C181 | P1 learner-verification | d52666a8b | LEARNER-VERIFICATION-COMPLETE |
| C182 | P8 adaptive-threshold | b6135c531 | ADAPTIVE-THRESHOLD-COMPLETE |
| C183 | P4 provenance-learning | 96fa237b1 | PROVENANCE-LEARNING-COMPLETE |
| C184 | P9 mini-lifetime-integration | 1963e994d | MINI-LIFETIME-INTEGRATION-COMPLETE |
| C185 | P5 substrate-expansion | 02a338dbf | SUBSTRATE-EXPANSION-COMPLETE |
| C186 | P2 persistent-connections | 105e9ee8b | PERSISTENT-CONNECTIONS-COMPLETE |
| C187 | P6 utility-integration | ff0d91691 | UTILITY-INTEGRATION-COMPLETE |
| C188 | P3 rebind-hardening | 0509fd116 | REBIND-HARDENING-COMPLETE |

**Pending:** Protect-how retry (P7) has REPORT.md with PROTECT-HOW-COMPLETE
verdict but has not committed yet. Will be C189 when committed.

## 2. SUF Tracking Update (Micah Q10)

### New mechanisms (C181-C188)

| Mechanism | Researcher-Owned | Learner-Owned | Pattern |
|-----------|------------------|---------------|---------|
| Learner-verification (C181) | Reliability scoring rule | Reliability VALUES, accept/reject decisions | Values in researcher framework |
| Adaptive-threshold (C182) | Threshold update rule | Threshold VALUE from experience | Value in researcher field |
| Provenance-learning (C183) | Reliability update rule | Source reliability VALUES, A->B switch | Values, policy switch |
| Mini-lifetime-integration (C184) | 3-arm design, metrics | Accumulated structures, policies | Integration test |
| Substrate-expansion (C185) | 5 behavior read rules | Consequence RECORDS drive all 5 | Records learner-written |
| Persistent-connections (C186) | Connection creation rule | A-B RELATION structure, reuse | Structure not enumerated |
| Utility-integration (C187) | Predictive utility rule | Utility VALUES from prediction | Values from learner criterion |
| Rebind-hardening (C188) | 4 world designs | (adversarial, no new mechanism) | Hardening only |

### Updated aggregate (C169-C188)

**Finding:** The learner-owned column is growing in two dimensions:
1. **Values:** reliability scores, threshold values, source reliability,
   utility values (C181, C182, C183, C187)
2. **Structures:** A-B relations, MAP graphs, protection edges (C186,
   plus prior C172, C176)

**Persistent gap:** Learner fills slots and creates simple structures,
but does not yet create new slots, new fields, or new mechanisms.
The "learner creates slot" vs "learner fills slot" gap remains central.

**One-System Rule:** Holding across all new mechanisms. Zero new modes,
bridges, handlers, or semantic cases in C181-C188.

## 3. Frontier Gaps vs Micah's 10 Priorities

All 10 priorities now have completed workers:

1. **P1 Learner-owned verification:** C181 COMPLETE. Reliability replaces
   expected for revision acceptance. Next: test candidate acceptance,
   rejection, withholding using learner-owned evidence (beyond revision).
2. **P2 Persistent connections:** C186 COMPLETE. A-B relations created.
   Next: test whether C exploits A-B faster, ablation loss, spontaneous
   formation in longer lifetimes.
3. **P3 Rebinding adversary:** C188 COMPLETE. 4 hardening worlds GRACEFUL.
   Next: 100 MAP scale, adaptation (not just exact reuse), misleading
   structurally similar MAPs that verify.
4. **P4 Provenance learning:** C183 COMPLETE. A->B switch from experience.
   Next: multi-source reliability, recovery when B improves again,
   no hardcoded rank in larger source sets.
5. **P5 Substrate expansion:** C185 COMPLETE. 5 behaviors, per-behavior
   ablations. Next: independent replication, test if substrate can drive
   revision strategy (6th behavior).
6. **P6 Utility integration:** C187 COMPLETE. Test 6 run, wrong-but-frequent
   attacked. Next: connect to downstream consequences (does high-utility
   structure actually help later learning?).
7. **P7 Protect the how:** PENDING COMMIT. Report complete, awaiting git
   commit. Next: measure reconstruction cost vs storage, downstream
   capability after forgetting answers.
8. **P8 Adaptive threshold:** C182 COMPLETE. Threshold from experience.
   Next: test if learner can distinguish noisy vs stable vs changing
   environments and adjust evidence requirements accordingly.
9. **P9 Mini-lifetime:** C184 COMPLETE. 3-arm comparison done. Next:
   longer lifetimes, more mechanisms integrated, measure
   examples-to-criterion improvement over lifetime.
10. **P10 Allocation:** MAINTAINED. Wave completed 8/8 workers plus
    protect-how retry. Replacement priority BUILD->RUN->ABLATE->
    ADVERSARY->INTEGRATE->ANALYZE followed.

## 4. Prereg Compliance

**New claims C181-C188:** All exploratory (no frozen prereg). Honestly
labeled BUILD-PASS, not preregistered claims. Zero prereg violations.

**Cumulative:** C169, C171 remain the only SURVIVES (preregistered).
All others are BUILD-PASS or EXPLORATORY. This is correct per Micah's
standard: preregistration required for SURVIVES.

## 5. Constraints Honored

Governance only. No experiment files modified. Pure shell/git operations.
Zero em/en dashes in docs (verified). Paper untouched. Nothing pushed.
All commits verified via git log before ledger entry.

## 6. Recommendation for Next Wave

Per Micah's north star: "TNN should not merely remember previous
experience. It should use consequences to change how it judges, connect
old and new structures, reuse those connections spontaneously, preserve
generative knowledge, and become cheaper and better at learning as its
lifetime grows."

Highest information-gain next steps:
1. **P1-deep:** Learner-owned verification for withholding (not just
   revision). Can reliability scores drive WITHHOLD decisions?
2. **P2-deep:** Persistent connections in 1000+ event lifetime. Do A-B
   relations form spontaneously? Do they compound?
3. **P5-deep:** Substrate driving revision strategy. 6th behavior from
   same store would strengthen One-System claim.
4. **Integration:** Combine C181 (verification) + C183 (provenance-learning)
   + C185 (substrate): can learner-owned reliability drive substrate
   writes that then drive verification?

Replacement priority remains: BUILD -> RUN -> ABLATE -> ADVERSARY ->
INTEGRATE -> ANALYZE. Do not stop.
