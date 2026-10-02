# Architecture Compression Analysis: C181-C189
## Constitution Section 4 metrics for the 10-priority wave (2026-10-01)

### Step 0
Toolchain guard active (safebin, no python3/python). Governance only. Pure shell/git.

### Compression table

| Claim | Lines added | M/B/H/S | Researcher-owned structural | Learner-owned structural | Capability gained |
|---|---|---|---|---|---|
| C181 learner-verification | ~140 | 0/0/0/0 | 3: threshold value (3), decision structure, header fields | 2: reliability values, V4 accept/reject judgments | revision acceptance via learner reliability |
| C182 adaptive-threshold | ~80 | 0/0/0/0 | 1: update rule (+3/-1, T=2+E/3, clamps) | 2: threshold values (2 vs 5), write timing | adaptive evidence requirements |
| C183 provenance-learning | ~157 | 0/0/0/0 | 5: record layout, count rule, prefer-higher rule, tiebreak, schedules | 4: reliability values, disagreement winners, switch point (k=7), B recovery | source reliability from consequences |
| C184 mini-lifetime-integration | ~250 | 0/0/0/0 | integration glue (4 mechanisms composed) | 5: MAP graphs, rebind bindings, substrate records, PRO edges, source tags | integrated lifetime, transfer + withholding |
| C185 substrate-expansion | ~452 | 0/0/0/0 | 2: config bitmask per battery, abandonment permanence design | 3: consec_fail values, STRATEGY.successes, life.state | 5 behaviors from one substrate |
| C186 persistent-connections | ~90 | 0/0/0/0 | 1: link-priority (newest-first) | 1: all link endpoints and topology | persistent A-B-C chains, 11x retrieval |
| C187 utility-integration | ~697 | 0/0/0/0 | 4: update magnitudes, FOSSIL_AGE=200, PRED schema, battery designs | 4: U values, MAP promotions, eviction orders, prediction outcomes | Test 6 + predictive utility, wrong-but-frequent killed |
| C188 rebind-hardening | ~106 (+227 driver) | 0/0/0/0 | 1: 4 test drivers (no new mechanism code) | 1: A-phase MAP graphs (reused) | adversarial characterization (not a mechanism) |
| C189 protect-how | ~36 | 0/0/0/0 | 3: tier order, derived-marker semantics, tier membership | 0 | generative retention by eviction order |

M/B/H/S = modes / bridges / handlers / semantic cases added.

### Totals

- Cognition lines added (C181-C189): ~2008
- Modes/bridges/handlers/semantic cases: 0 across all 9 (One-System Rule holding)
- Distinct capabilities: 9 (8 mechanisms + 1 adversarial characterization)
- Lines per capability: ~223
- Researcher-owned structural decisions: ~20 (counted from reports)
- Learner-owned structural decisions: ~22 (values and structures)

### Learner-authority ratio

Counting listed structural decisions per report: learner-owned 22 vs researcher-owned 20, ratio ~1.1. But this flatters the picture. The researcher-owned items are MECHANISMS (update rules, tier orders, priority rules); the learner-owned items are mostly VALUES inside researcher-defined slots (reliability scores, threshold values, link endpoints). The central gap persists: learner fills slots and creates simple structures (A-B links, MAP graphs), but does not create new slots, fields, or mechanisms. C189 is the extreme: 3 researcher-owned, 0 learner-owned.

### Compression opportunities (ranked by information gain)

1. **Five parallel scoring systems should be one.** C181 uses PRED nodes (tag-31) for prediction reliability. C183 uses tag-61 records (correct/total) for source reliability. C185 uses tag-61 (consec_fail/successes) for consequence records. C187 uses the U field (+-1) for predictive utility. C182 uses error score E for threshold adaptation. All five are "experience -> score -> future decision." C185 already proved one store can drive 5 behaviors. The next compression experiment: merge prediction reliability, source reliability, utility, and error scores into the single consequence substrate. Predicted saving: ~400+ lines of parallel scoring machinery.

2. **Two protection mechanisms should be one.** a298709d5 (use-dependent PRO edges from live MAP topology; learner-adjacent) vs eb19a4f3c (3-tier eviction order; fully researcher-authored, 36 lines, 0 learner-owned). Both protect generative structure under pressure. Test whether PRO-edge protection subsumes tier-based eviction, or whether tier-based eviction can be made use-dependent. One should be deleted.

3. **Threshold adaptation (C182) and withholding (C185 B2a) both gate on accumulated evidence.** C182 adapts T via experienced noise; C185 withholds at consec_fail >= 3 and abandons at >= 6. A single evidence-sufficiency mechanism with learner-adaptive thresholds would remove one of the two gating paths.

4. **C184 integration is itself a compression result.** Four mechanisms (rebind, substrate, provenance, protection) compose in one learner with ~250 lines of glue and zero new architectural constructs. No interference. This is the pattern to repeat: integrate first, then look for shared machinery to delete.

5. **C188 added no mechanism (test drivers only).** Correctly excluded from compression targets; it is evidence, not architecture.

### What NOT to compress yet

- C186 persistent links (type-14): the only structural connection mechanism. Deleting it reverts to XEDGES=0.
- C181 learner verification: the only path replacing researcher expected. Still needed for withholding work (P1-deep gap).

### Verdict
GOVERNANCE-COMPRESSION-COMPLETE (partial: C181-C189 tabled; C190+ pending new-worker completion).

No em dashes used (verified).
