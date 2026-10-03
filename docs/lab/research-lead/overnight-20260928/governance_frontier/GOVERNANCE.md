# Governance Report: 2026-10-01 Frontier Wave

**Worker:** Governance/Frontier Worker
**Date:** 2026-10-01
**Scope:** Ledger C169-C180, prereg compliance, SUF tracking (Micah Q10), frontier gaps (Micah 15 questions)

---

## 1. Prereg Compliance Audit

**Rule:** Prereg commit must strictly precede implementation commit. Failures cannot be adopted that wave.

### COMPLIANT (frozen prereg before implementation)

| Experiment | Prereg | Implementation | Order | Status |
|------------|--------|----------------|-------|--------|
| Node2-v2 K-H3 | `4b05c8011` (18:24:03) | `0988839a2` (18:25:24) | Prereg 81s before | **COMPLIANT** |
| Weak K-LT-5 clean | `32382a122` (17:41:51) | `84855c1e1` (17:42:19) then `4e6fb77ef` (17:45:33) | Prereg before seal before eval | **COMPLIANT** |
| Node2-v2 ablation | `4b05c8011` (18:24:03) | `ab1bee9a6` (18:57:50) | Under original frozen prereg scope | **COMPLIANT** |

**Note on Node2-v2:** Draft prereg `21115becf` (17:17:10) predates the frozen `4b05c8011` (18:24:03). The frozen prereg is the governing document; it strictly precedes implementation. The draft is preserved as a design artifact, not a governing prereg. No violation.

### DESIGN-BEFORE-BUILD (not a formal frozen prereg)

| Experiment | Design | Build | Note |
|------------|--------|-------|------|
| Mini-lifetime | `0bab6db08` (17:16:48) | `4339119e9` (18:24:40) | Design doc, not a kill-bar prereg. Build followed design. |

### EXPLORATORY (no prereg; BUILD-PASS status only, not preregistered claims)

The following produced valuable results but had no frozen prereg. Per governance rules, these are **EXPLORATORY / BUILD-PASS**, not preregistered SURVIVES. They may earn promotion through future preregistered replication.

| Experiment | Commit | Time | Result |
|------------|--------|------|--------|
| Dedup | `296fd79cb` | 17:24:31 | DYN-1 BENT (201 nodes) |
| Substrate consolidation | `1ed3f5a6b` | 17:33:09 | EMERGES (decline from substrate) |
| Provenance | `8c352e5bf` | 17:44:40 | FIXES (10/10 to 0/10) |
| Rebinding | `91585087c` | 17:45:38 | PASS (7 vs 11) |
| Decline adversary | `c7f4df907` | 17:48:26 | SURVIVES with 3 NEEDS-FIX |
| Retention | `5dc1004fc` | 18:02:52 | MIXED |
| Structural protection | `a298709d5` | 18:12:40 | SAVES-HOW |
| Dedup-decline integration | `4f45993c3` | 19:08:03 | REDUNDANT |

**Utility design** (`cd6a8a74a`, 17:35:50) is design-only; no implementation yet. No prereg required for a design document.

### Violations

**Zero violations.** All preregistered experiments show correct commit order. Exploratory work is honestly labeled as such and does not claim preregistered status.

---

## 2. SUF Tracking: Researcher-Owned vs Learner-Owned (Micah Q10)

**Question:** For each mechanism, what structural choice did learner history make that source code did not enumerate? Is the learner column growing?

### SUF Table

| Mechanism | RESEARCHER-OWNED structural decisions | LEARNER-OWNED structural decisions | SUF | Modes/Bridges/Handlers/Semantic |
|-----------|--------------------------------------|-----------------------------------|-----|-------------------------------|
| **Node2-v2** (`0988839a2`) | 6: field layout (8/12/16 history, 20 default), 3-threshold, history bound, bootstrap, action channel (`ev_observe_aw`), reset-on-update | 1: default action = 45 (set by world experience, not enumerated) | 0 | 0/0/0/0 |
| **Rebinding** (`91585087c`) | 1 mechanism (~70 lines): shape walk, plen filter, positional re-instantiation, retrieve-before-trial ordering, splice point in `ev_query` | 2: two A-phase MAP graphs (created by trial + promote_graph from experience); plen values read back are learner-created topology | 2 (MAP scan order by node id, B-path BFS order) | 0/0/0/0 |
| **Dedup** (`296fd79cb`) | 1: dedup gate + identity rule (tag-30/field4=-4/(s,r) match) at `miss_inquire` | 0 | 1 (source-enumerable) | 0/0/0/0 |
| **Provenance** (`8c352e5bf`) | 9: field 16, 6 tag values, external/self partition, unanimity rule, W3-external rule, 5 write-path edits | 0 (tag values researcher-defined; learner does not choose them) | 0 | 0/0/0/0 |
| **Substrate** (`1ed3f5a6b`) | 3: substrate record format, N=3 threshold (carried over), tag-61 storage tag | 0 (consec_fail values are learner state, but the decline criterion is researcher-authored) | 0 | 0/0/0/0 |
| **Structural protection** (`a298709d5`) | 1: protect-on-reference policy (no per-cell researcher choices) | Protection edges written on use; protected cell set derived from learner-built graph topology (not enumerated in source) | 0 | 0/0/0/0 |
| **Weak K-LT-5** (`4e6fb77ef`) | 9: six assembler families, Hebbian swap rule, demotion threshold 8, initial order [0,1,2,3,4,5], N=10, 1.15 threshold, 1024-node budget, vc>0 precondition, sum 900-limit | 1: trial-order policy values (converged [4,0,1,2,3,5] in Phase A; re-converged after C2 reset) | 0 | 0/0/0/0 |
| **Utility** (`cd6a8a74a`, design) | Magnitudes, thresholds, priority order honestly labeled as researcher scaffolding with stated retirement condition | 0 (design only; values would accumulate from experience stream) | N/A | 0/0/0/0 |

### Is the learner column growing?

**Yes, slowly, and in a specific pattern.**

Learner-owned counts by mechanism:
- Dedup: 0
- Provenance: 0
- Substrate: 0
- Node2-v2: 1 (policy value 45)
- Weak K-LT-5: 1 (policy order [4,0,1,2,3,5])
- Rebinding: 2 (two MAP graphs)
- Structural protection: learner-derived (protection edges + cell set from topology)
- Utility: 0 (design stage)

**Pattern:** The learner owns **values and structures** (policy=45, MAP graphs, protection edges, policy orderings), not **mechanisms**. Every mechanism (the rebind procedure, the provenance partition, the dedup gate, the substrate format, the protection policy) remains researcher-authored.

**What would genuine growth look like (per Micah Q10):**
- Not: parameter learned inside a fixed schema (policy=45 is a value in a researcher-defined field)
- But: schema/form created by the learner (a new policy structure, a new evidence type, a new retrieval index the source did not enumerate)

**Current status:** We are at "parameter learned inside fixed schema" for most mechanisms. Rebinding and structural protection show the most learner contribution (graph topologies the source did not enumerate). The gap between "learner fills a slot" and "learner creates the slot" remains the central challenge.

**Trajectory:** The One-System Rule is holding (zero new modes/bridges/handlers/semantic cases across all 8 mechanisms). Cognition lines per mechanism are bounded (15-110). The researcher-supplied cognitive structure per capability is not growing, which is the desired direction, but the learner-owned column needs to grow faster.

---

## 3. Frontier Gaps: Micah's 15 Questions

### Active coverage

| Question | Topic | Active worker | Status |
|----------|-------|---------------|--------|
| Q1 | Node2-v2 generalization (threshold, multiple policies, competing, revision, cross-policy) | Node2-v2 ablation (done); generalization pending | **PARTIAL** |
| Q2 | Rebinding frontier (A-F) | Rebinding adversary (running) | **ACTIVE** |
| Q7 | Substrate integration (one mechanism, many effects) | Substrate consolidator (done, EMERGES); dedup-decline integration (done, REDUNDANT) | **ACTIVE** |

### Gaps (no active worker)

| Question | Topic | Priority | Recommended next experiment |
|----------|-------|----------|----------------------------|
| Q3 | Spontaneous connections (no explicit reuse instruction) | **HIGH** | Lifetime stream: learn A, 100s of unrelated events, encounter B, test if A retrieved without instruction |
| Q4 | Learned compression (functional equivalence, not byte-exact) | **HIGH** | Beyond dedup: can TNN discover renamed-entity / same-causal-role / same-procedure-different-constants equivalence? No hardcoded classes. |
| Q5 | Learner-derived utility (consequences teach value) | **HIGH** | Use researcher-authored utility as baseline; test if downstream consequences (search saved, prediction enabled, deletion caused failure) can alter retention without per-case +2 rules |
| Q8 | Learner-owned success criteria (predict before outcome) | **HIGH** | Can TNN generate predictions BEFORE seeing outcomes and use prediction error to judge structure usefulness? (Stronger than match-to-expected-answer) |
| Q9 | Generic revision (all learned objects revisable) | **MEDIUM** | For each mechanism (policy, procedure, retrieval preference, abstraction): what happens when it becomes wrong? No mechanism-specific reversal code. |
| Q11 | Meta-learning (improve how it learns) | **MEDIUM** | A/B/C experience → D learned with fewer examples; ablation of prior learning removes speedup. Test search ordering, evidence requirements, memory strategy improvement. |
| Q12 | Continuous lifetime connections (overlaps Q3) | **MEDIUM** | Long streams, old info becomes useful later, track spontaneous cross-domain edges. No task labels. |
| Q13 | Scale (architectural alternatives) | **HIGH** | Implement and measure: stable structural references, structure-level allocation, sublinear retrieval, local indexing. Measure until failure. Do not merely enlarge arrays. |
| Q14 | Architecture metric (intelligence up, researcher structure down) | **ONGOING** | This report contributes the SUF table. Needs continuous tracking per generation. |

### Replacement priority (when workers complete)

Per Micah's allocation (2 transfer, 2 consequence/meta, 2 memory/scale, 1 verification, 1 lifetime, 1 integration, 1 governance):

1. **Next transfer worker:** Q3 (spontaneous connections) or Q2E (topology transfer: chain to branched)
2. **Next consequence worker:** Q1-deep (Node2-v2 generalization: context-dependent policies, noisy evidence, policy revision) or Q11 (meta-learning)
3. **Next memory worker:** Q13 (scale: sublinear retrieval prototype) or Q4 (learned compression)
4. **Next verification worker:** Q8 (learner-owned success criteria: prediction-before-outcome)
5. **Next lifetime worker:** Q3/Q12 (spontaneous connections in long streams)
6. **Next integration worker:** Q9 (generic revision) or Q5 (learner-derived utility)

---

## 4. Ledger Entries Added (C169-C180)

- **C169:** WEAK-KLT5-PASS (clean sealed test, R=1.90, all kill bars, prereg-compliant)
- **C170:** PROVENANCE FIXES (source-aware bootstrap, 10/10 to 0/10, exploratory)
- **C171:** NODE2V2 K-H3 PASS + ABLATION (reachable policy update, 4/4 links necessary, prereg-compliant)
- **C172:** REBINDING PASS (chain family, 7 vs 11, exploratory)
- **C173:** DEDUP BENT (201 nodes, 37% reduction, exploratory)
- **C174:** SUBSTRATE CONSOLIDATION EMERGES (decline from shared substrate, exploratory)
- **C175:** UTILITY-DESIGN (learner-owned MAP utility, design only)
- **C176:** STRUCTURAL PROTECTION SAVES-HOW (PRO edges save executable how, exploratory)
- **C177:** MINI-LIFETIME RUN (Build B reuse-path, A/B comparison, design-before-build)
- **C178:** RETENTION MIXED (substrate retention preserves answerability, exploratory)
- **C179:** DECLINE-ADV SURVIVES (3 NEEDS-FIX items, exploratory)
- **C180:** DEDUP-DECLINE INTEGRATION REDUNDANT (byte-identical to dedup-only, exploratory)

See CLAIM_LEDGER.md for full entries.

---

## 5. Verdict

**GOVERNANCE-COMPLETE.**

- Ledger updated: C169-C180 appended with commit hashes, measurements, and status labels.
- Prereg compliance: 3/3 preregistered experiments compliant. 8 exploratory results honestly labeled. Zero violations.
- SUF tracking: Learner column growing slowly (values/structures, not mechanisms). One-System Rule holding (0 modes/bridges/handlers across all mechanisms).
- Frontier gaps: 9 of 15 questions lack active workers. Prioritized replacement list provided.

**Constraints honored:** No experiment files modified. Pure documentation. Zero em/en dashes (verified). Paper untouched. Nothing pushed. Explicit pathspecs on commit.

---

*No em dashes were used in this document.*
