# Re-clustering Draft: TNN-2 Freeze at 4/9

**Status: DRAFT - AWAITING RECONCILED EVALUATOR REPORT**

**Date:** 2026-10-01
**Worker:** Re-clustering Drafter
**Basis:** Prereg compliance audit `8959a7c14` (draft claims 5/9, table shows 4/9; correct score is 4/9)

**Do not quote a freeze score from this document.** The evaluator's reconciled committed report is the authoritative source. This draft assumes the audit's corrected 4/9 for the purpose of preparing the prereg-required re-clustering analysis.

---

## 1. The 5 TNN-1 Failure Clusters

From CORE-FREEZE-TNN1 Evaluation Report (`7bde57f52`), section "Notes for Root-Cause Clustering":

| # | Cluster | Worlds | Symptom |
|---|---------|--------|---------|
| 1 | Arithmetic/composition | FW3, W3 | 0/10 on both. Cannot construct multiplication from ISA basis. |
| 2 | Planning | FW7, W7 | 0/4 on both. Actions do not compose toward target. |
| 3 | Novel utterance | FW8, W8 | 0/5 novel on both, despite 4/4 retention. Recalls but does not generate novel forms. |
| 4 | Relational DAG | FW9, W9 | 5/30 and 9/30 (FW), 14/28 and 14/26 (W). Multi-hop relational inference fails. |
| 5 | Active inquiry | FW6, W6 | Degenerate constant-action mechanism. Single-element action alphabet cannot express contingent inquiry. |

TNN-1 FW passes: FW1, FW2, FW4, FW5 (associative recall, law change/revert, targeted update).
TNN-1 FW failures: FW3, FW6, FW7, FW8, FW9.

---

## 2. TNN-2 Draft Results (per audit-corrected reading)

From the untracked evaluator draft (`core_freeze_tnn2_eval/FREEZE_REPORT.md`), as corrected by audit `8959a7c14`:

| World | TNN-2 Draft | TNN-1 | Match |
|-------|-------------|-------|-------|
| FW1 | PASS (12/12) | PASS (10/12) | Yes |
| FW2 | PASS (8/8) | PASS (8/8) | Yes |
| FW3 | FAIL (0/10) | FAIL (0/10) | Yes |
| FW4 | PASS (12/12, 12/12, 12/12) | PASS (12/12, 12/12, 12/12) | Yes |
| FW5 | PASS (10/10, 3/3, 9/9) | PASS (10/10, 3/3, 9/9) | Yes |
| FW6 | FAIL (CHOICE 30, not contract CHOICE 0) | FAIL (degenerate, CHOICE 0) | Yes (both fail) |
| FW7 | FAIL (0/4) | FAIL (0/4) | Yes |
| FW8 | FAIL (0/5 novel, 4/4 retention) | FAIL (0/5 novel, 4/4 retention) | Yes |
| FW9 | FAIL (3/30, 7/30, 2/5) | FAIL (5/30, 9/30, 0/5) | Yes (both fail) |

**Corrected FW SCORE: 4/9** (FW1, FW2, FW4, FW5).

No regressions on previously passing worlds. No fixes on previously failing worlds.

---

## 3. Pass/Fail Pattern Comparison

**The 4 passes are identical.** TNN-2 passes exactly FW1, FW2, FW4, FW5, the same four worlds TNN-1 passed. The pass margins improved slightly on FW1 (12/12 vs 10/12) but the set is unchanged.

**The 5 failures are identical in kind.** TNN-2 fails exactly FW3, FW6, FW7, FW8, FW9, the same five worlds TNN-1 failed. The failure modes are the same:
- FW3: 0/10 (all -2), unchanged
- FW6: degenerate constant action (CHOICE 30 vs TNN-1's CHOICE 0; both fail the contingent-inquiry requirement)
- FW7: 0/4, unchanged
- FW8: 0/5 novel with 4/4 retention intact, unchanged
- FW9: low multi-hop scores, unchanged

**Conclusion:** TNN-2's three architectural changes did not move any of the five failure clusters. The pass/fail pattern is byte-identical at the world level.

---

## 4. What "Falsifies the Diagnosis" Means

The TNN-2 prereg (`ce1a7c5f8`, Section 5) states:

> "The three changes target specific clusters: Change 1 (runtime construction) targets FW3, FW8, FW9, half of FW7. Change 2 (miss-to-act inquiry) targets FW6 and half of FW7. Change 3 (generic revision) targets the revision ceiling; may not move FW scores directly but future-proofs Change 1."

> "A FW SCORE above 4/9 with no regressions on FW1/FW2/FW4/FW5 would confirm the architectural diagnosis. A score at or below 4/9, or regressions on previously passing worlds, would falsify the root-cause analysis and require re-clustering."

The diagnosis was: TNN-1's 4/9 is caused by three specific gaps (no runtime construction, no inquiry loop, no generic revision). TNN-2 fills these three gaps.

The prediction was: filling the three gaps will move the FW score above 4/9 by fixing the targeted clusters.

The result (per audit-corrected draft): FW score remains 4/9. Zero of the five targeted clusters moved. Zero regressions (the passing worlds still pass).

**Falsification means:** the three gaps, as implemented in TNN-2, were not the actual causal bottlenecks. Or equivalently: the "fixes" did not actually fill the gaps they were named for. The prereg's causal account, "TNN-1 fails because it lacks X, TNN-2 adds X, therefore TNN-2 will pass," is falsified for all three X.

This does not mean the original five symptom clusters were wrong. FW3 still fails on arithmetic, FW7 still fails on planning, etc. What is falsified is the specific architectural diagnosis that "adding runtime construction / inquiry loop / generic revision (as implemented) fixes these clusters."

**Re-clustering is required** because we need a new causal account: why did the three changes fail to move their targets?

---

## 5. Revised Clusters: Why the Three Changes Failed

The original five clusters describe symptoms (what capabilities are missing). The revised clusters describe causes (why TNN-2's fixes did not work). They are informed by the three independent red-team reports (construction `340e94e3e`, inquiry `4e329c772`, revision `687ba0219`), the synthesis (`42b4dfa91`), and the DOF map (`d2af26581`).

### Revised Cluster R1: Enumerated construction (explains FW3, FW8, FW9, half of FW7)

**What Change 1 was supposed to do:** Provide runtime construction of procedures/graphs from a 4-op ISA, enabling the learner to build multiplication (FW3), compose novel utterances (FW8), traverse relational DAGs (FW9), and chain actions (FW7).

**Why it failed:** The red-team construction report found three fixed assembler families (chain/count/sum) with researcher-fixed wiring patterns, fixed bounds, fixed trial order, and oracle-gated verification. The sum family is unreachable in production (gated on a type-8 node no cognition-path code can create). The DOF map found zero pure learner decisions in the cognition path. The "construction" is a finite template menu, not open construction.

**Shared architectural cause:** The researcher enumerates the solution space (three topologies); the learner selects indices and fills literals within it. This is L2 structural learning (fixed templates with variable content), not the open-ended construction FW3/FW8/FW9 require. FW3 needs the learner to invent multiplication; the template menu contains no path to it. FW8 needs novel composition; the menu has no composition operator beyond fixed chains. FW9 needs multi-hop traversal; the chains are bounded at depth 4 by researcher literal.

**Falsifiable prediction for a genuine fix:** A general construction substrate would show FW3 moving (learner-invented multiplication from ADD), FW8 novel moving (compositions not in the menu), and FW9 moving (unbounded traversal). None moved, confirming the menu bound.

### Revised Cluster R2: Non-contingent inquiry (explains FW6, half of FW7)

**What Change 2 was supposed to do:** Provide a miss-to-act inquiry loop where the learner detects uncertainty and emits a discriminating inquiry action, enabling FW6's contingent inquiry and FW7's goal-directed action selection.

**Why it failed:** The red-team inquiry report found the action is a constant (CHOICE 30 in TNN-2, CHOICE 0 in TNN-1). The guide is a fixed 2-node schema; the "question" is the input (s,r), never derived. There is no uncertainty-resolution path. The DOF map confirmed: the inquiry guide schema is researcher-fixed.

**Shared architectural cause:** The "inquiry loop" is a miss flag wired to a constant output. It detects (something missed) but does not inquire (no discriminating question, no information-seeking action, no use of the answer). FW6 requires the action to be contingent on epistemic state (different acts before vs. after diagnostics); a constant cannot express this. The change from CHOICE 0 to CHOICE 30 is a different constant, not contingency.

**Falsifiable prediction for a genuine fix:** A contingent-inquiry substrate would show CHOICE varying with internal uncertainty state across FW6's phases, and FW7 emitting non-zero action sequences. Neither occurred.

### Revised Cluster R3: Single-schema revision (explains the revision ceiling)

**What Change 3 was supposed to do:** Provide generic revision machinery that future-proofs construction by repairing promoted graphs after counterexamples.

**Why it did not move FW scores (as prereg predicted it might not):** The red-team revision report found one fixed "replace the DEP-tagged SET step under its guard" topology. It handles literal patches only. It cannot retarget guards (FW4/GW4 class), cannot do topological repair, and cannot touch sum graphs (no provenance). The prereg correctly anticipated this might not move FW scores directly.

**Shared architectural cause:** The "generic revision" is a single researcher-authored repair schema with learner-filled indices (which cell, which literal). It is L1 parameter filling on a fixed topology. Genuine revision would require the learner to select or construct repair operators based on the failure mode.

**Note:** R3 is not a falsification of Change 3's limited claim (the prereg said it "may not move FW scores directly"). It is included because the revision ceiling matters for the interaction between construction and revision: construction emits template instances, revision patches literals, and neither can change the other's grammar.

### The Meta-Cause (shared across R1, R2, R3)

All three revised clusters share one pattern, identified by the red-team synthesis (`42b4dfa91`):

> **Enumerated-schema / filled-slot:** the researcher chooses the meaningful form, topology, question, verifier, or repair family; the learner fills runtime-selected indices and literals.

TNN-2 is "fixed templates with variable content" (vs. TNN-1's "fixed templates with fixed content"). This is a real L2 advance, but it does not address any of the five symptom clusters, because all five require the learner to originate form, not just fill content:
- FW3 requires inventing multiplication (form), not selecting a template.
- FW6 requires deriving a discriminating question (form), not firing a constant.
- FW7 requires composing action sequences toward a goal (form), not emitting CHOICE 0/30.
- FW8 requires novel composition (form), not menu selection.
- FW9 requires unbounded traversal (form), not depth-4 chains.

**The diagnosis was falsified because the three "gaps" were mischaracterized.** The gap was not "no construction" but "no learner-originated form." TNN-2 added "construction" in the sense of runtime template instantiation, but the forms remained researcher-enumerated. The prereg's change targets named the right symptom clusters but the wrong causal level.

---

## 6. What Re-clustering Changes for TNN-3

The original five symptom clusters remain valid as descriptions of what TNN-2 cannot do. The revised cause clusters (R1, R2, R3 + meta-cause) replace the prereg's causal account.

**Implications:**

1. **Do not re-attempt "construction" as a larger menu.** The treadmill risk (adding SUB, DIV, or more templates) is now empirically grounded: Change 1 was already a menu, and it moved nothing. H1 widening must be genuinely open (learner-originated topology), not a bigger finite set.

2. **H2 (oracle verification) is now the binding constraint on H1.** The synthesis noted verification is answer-keyed (`expected` flows driver to trial). Even a genuinely open constructor would be "answer-fed" under oracle gating. The roadmap's order (H2 probes before H1 widening) is confirmed by the falsification.

3. **H3 (procedure ownership) is structural fact, not hypothesis.** The DOF map's "zero pure learner decisions" and the red teams' "indices and literals" converge: no TNN-2 policy is learner-revisable. H3-lite (moving decisions into learner state) is the minimal next step, but it changes locus of control, not capability scores.

4. **C0-D cannot be established by any FW score.** The C0-D analysis (`8bfb80fdd`) showed promoted graphs are causally inert at query time (shadowed by `ev_teach_in`). Even a hypothetical 9/9 would not demonstrate reuse. The GW battery and a reuse path are prerequisites.

5. **The five symptom clusters should be retained** as the benchmark for TNN-3, but the kill bars must test learner-originated form (per the kill-bar draft `76231baa8` and review `eb354e3a2`), not template instantiation.

---

## 7. Open Questions for the Reconciled Report

This draft is prepared in advance of the evaluator's reconciled committed report. When that report lands, verify:

1. Does the reconciled FW score remain 4/9? (Audit corrected the arithmetic; confirm.)
2. Is K-FZ2-4 (determinism) resolved? (Was PENDING in the draft.)
3. Are the W (supplementary) results consistent with the FW pattern? (TNN-1 had W 4/9 with the same world set passing.)
4. Do any FW worlds change status between draft and reconciled report?
5. Does the reconciled report include the prereg-required per-cluster analysis, and does it agree with or modify this re-clustering?

If the reconciled score differs from 4/9, this draft's falsification analysis must be revised accordingly.

---

**End of draft.**
