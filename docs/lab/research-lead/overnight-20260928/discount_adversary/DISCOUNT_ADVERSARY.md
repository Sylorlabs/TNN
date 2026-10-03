# Discount Adversary: Majority-Wrong World Design

**Status:** DESIGN ONLY. No implementation. No variant built. No experiments run.
**Verdict:** DISCOUNT-ADVERSARY-COMPLETE.
**Date:** 2026-10-01.

## 0. Purpose

The discount specification (`62fa77192`, Section 6.2) flags W3 (minority
discount on bootstrap failure) as the highest-risk component:

> "W3 assumes the majority is more likely correct. In adversarial or
> low-redundancy worlds, the majority can be wrong (five self-generated
> 42s vs one genuine 99, as demonstrated). W3 then punishes truth. This
> is inherent to any source-blind heuristic and cannot be fixed within
> discount; it requires source provenance."

The specification's recommended next step 3 (`62fa77192`, Section 8)
calls for this design:

> "Adversarial W3. Construct a world where the majority is wrong and W3
> punishes truth. Measure the damage. This bounds the heuristic's risk."

This document designs that world. It does not build it, run it, or
claim results. It specifies the setup, the predicted mechanism
behavior, the harm metrics, and the validity conditions for a future
implementation.

## 1. The adversarial scenario

### 1.1 Core inversion

The contradiction-break probe (`510b6cb42`) established that a single
genuine 99 breaks a self-generated 42-loop, and discount (`0daaa2ed4`)
recovers by excluding the 99. In that scenario, the 42s were
self-generated (epistemically suspect) and the 99 was genuine (the only
true evidence). Discount preserved the loop and excluded the truth.

This design inverts the evaluation: what if the scenario is not
"fragile loop vs genuine contradiction" but "wrong loop vs genuine
correction"? The mechanism cannot distinguish these cases (source-blind,
Section 5.1 of the spec). The adversarial world makes the majority
wrong and the minority right, then measures how much damage W3 does.

### 1.2 World narrative

Relation r=50. The true value for a class of subjects is 99 (unknown to
the learner; "truth" here means the value that genuine observations
consistently report, not a metaphysical claim).

Phase 1 establishes a wrong bootstrap loop on 42 (self-generated,
incorrect). Phase 2 introduces genuine 99 observations (correct but
minority). W3 discounts the 99s. Phase 3 measures the resulting
epistemic state: a system that has actively suppressed true evidence
and now infers wrong answers with no internal signal of error.

## 2. Detailed design

### 2.1 Phase 1: Establish the wrong loop

**Setup:** Use the confirmed bootstrap loop procedure from `ee7815de8`.

1. Teach 3 genuine observations that happen to agree on 42 for
   subjects 1001, 1002, 1003 on relation 50. (In this world, these are
   the misleading seeds; perhaps they were miscalibrated sensors, or a
   transient regime that has since changed. The learner cannot know.)
2. Query 4 fresh subjects (2001-2004, r=50, masked, expected=-2).
   Bootstrap fires, teaches self-generated 42-facts.
3. Verify: queries return 42. The recency window holds self-generated
   42s. The loop is established and wrong (true value is 99, but no
   99-evidence exists yet).

**End state:** 5+ self-generated 42-facts in the window. The learner
"believes" 42. This belief is false but internally consistent.

### 2.2 Phase 2: Introduce genuine correction (minority)

**Setup:** The world now provides genuine observations of the true
value 99.

1. Via `ev_teach` (or `ev_observe` on existing subjects), introduce
   ONE genuine 99-fact for the same relation: e.g.,
   `ev_teach(3001, 50, 99)`.
2. Query fresh subjects. The bootstrap evidence scan now sees
   [99, 42, 42, 42, 42, 42] (or similar, depending on recency).
3. The unanimity gate fires (not unanimous). W3 applies: strict
   majority exists (five 42s vs one 99). The 99-fact gets
   `discount += 1`.
4. Repeat queries. Each non-unanimous bootstrap increments the 99's
   discount. After T+1 queries (T=2, so 3 queries), the 99 is excluded
   by R1.
5. The loop resumes inferring 42. The genuine correction has been
   suppressed.

**Predicted mechanism behavior (from spec Section 3.2, inverted):**

| Query | Result | 99 discount | Note |
|-------|--------|-------------|------|
| b0 | -2 | 0 -> 1 | W3 fires, 5x42 vs 1x99 |
| b1 | -2 | 1 -> 2 | 99 still eligible |
| b2 | -2 | 2 -> 3 | 99 still eligible |
| b3 | 42 | 3 (excluded) | R1 excludes 99; 42s unanimous |
| b4+ | 42 | 3 | Wrong loop resumes, truth suppressed |

This is the exact replay from the discount spec, but now the 42s are
wrong and the 99 is right. The mechanism behaves identically; only the
epistemic labels have flipped. This is the source-blindness made
measurable.

### 2.3 Phase 3: Measure the damage

After Phase 2, the system is in a damaged epistemic state. Measure:

**M1. Persistence of wrong inference.** Query 10 fresh subjects.
Count how many return 42 (wrong) vs -2 (withheld) vs 99 (correct).
Predicted: all 42. The system is confidently wrong with no internal
hesitation.

**M2. Truth exclusion depth.** Inspect the 99-fact's discount value.
Predicted: 3 (or higher if more queries ran). The truth is not merely
outvoted; it is structurally excluded from the evidence pool.

**M3. Rehabilitation cost.** Now introduce 5 more genuine 99
observations (via `ev_teach`). Each new 99-fact starts at discount 0.
Query fresh subjects. The window now contains multiple 99s and
multiple 42s. Does W3 now discount the 42s (they are the minority if
99s outnumber them), or does the recency ordering keep 42s in the
majority? Measure how many genuine observations are required to flip
the loop to 99. This quantifies the "epistemic immune response":
the system's resistance to correction after W3 has committed to the
wrong majority.

**M4. Self-generated amplification.** Count the total number of
self-generated 42-facts created during Phases 2-3. Each bootstrap
success teaches a new 42-fact via `ev_teach_in`. The wrong loop is
not static; it actively expands, creating more majority members that
future W3 applications will protect. Measure the growth rate.

**M5. W2 rehabilitation check.** If any 99-facts were introduced via
`ev_observe` (not `ev_teach`), check whether W2 (confirmation
decrement) ever fired to rehabilitate them. In the pure-teach
adversarial setup, W2 never fires (teach performs no contradiction
check). Document this as a design limitation of the adversarial
world, not a mechanism finding.

### 2.4 Phase 4: The mirror control (optional, recommended)

Run the identical procedure but with the epistemic labels swapped:
establish a correct 99-loop via genuine seeds, then introduce a single
wrong 42 (e.g., a miscalibrated sensor reading). W3 should discount
the 42 and preserve the 99-loop.

This control verifies that the mechanism behaves symmetrically (as
source-blindness predicts). If the mechanism behaves differently in
the mirror case, that asymmetry is itself a finding (it would suggest
some source sensitivity the spec did not predict).

The control is recommended but not required for the core adversarial
result. The core result is M1-M4 in the majority-wrong world.

## 3. Expected results and interpretation

### 3.1 Predicted outcome

The mechanism will behave exactly as specified: W3 will discount the
minority 99-facts, R1 will exclude them, and the wrong 42-loop will
resume. M1 will show persistent wrong inference. M2 will show
structural truth exclusion. M3 will quantify rehabilitation cost
(predicted: high, because each new 99 must survive T+1 W3 applications
before it can join the majority, while the 42-majority keeps growing
via self-generation). M4 will show loop amplification.

### 3.2 What this proves

1. **W3 is source-blind (confirmed empirically).** The mechanism
   cannot distinguish "minority is noise" from "minority is truth."
   This is not a bug; it is the specified behavior. The adversarial
   world makes the cost visible.
2. **Discount can entrench error.** Beyond merely failing to correct,
   W3 actively suppresses correction by discounting the corrective
   evidence. The system is worse off than if it had no discount
   (in the no-discount baseline, the 99 would permanently break the
   loop via the unanimity gate; with discount, the loop routes
   around the correction).
3. **The fragility fix has an epistemic price.** The spec (Section
   5.1) states this plainly: "discount trades epistemic purity for
   robustness." The adversarial world quantifies the price.

### 3.3 What this does not prove

1. **It does not show discount is net harmful.** The baseline
   (no discount) has permanent paralysis from one contradiction.
   The adversarial world shows discount has a failure mode, not
   that the failure mode is worse than the baseline failure mode.
   A full evaluation needs both the fragility scenario and the
   adversarial scenario, with a judgment about which failure is
   more costly in the target deployment.
2. **It does not show the majority is usually wrong.** The
   adversarial world is constructed to make the majority wrong.
   In natural environments, the majority heuristic may be well
   calibrated. The design bounds the worst case, not the typical
   case.
3. **It does not invalidate W3.** The spec includes W3 because
   teach-path contradictions have no other discount write path.
   The adversarial result is a known limitation to be documented,
   not a refutation of the mechanism's purpose.

## 4. Validity conditions

For a future implementation of this design to be valid:

1. **Unfrozen variant only.** The discount implementation (`0daaa2ed4`)
   is unfrozen. The adversarial test must run on an unfrozen variant,
   never on frozen TNN-2.
2. **3/3 byte-identical runs.** All measurements (M1-M5) must be
   replicated 3 times with byte-identical transcripts.
3. **No threshold tuning.** T must remain at the spec value (T=2).
   Running the adversarial world at different T values is permitted
   for sensitivity analysis but the primary result must use the
   fixed T.
4. **Baseline comparison.** The adversarial world should also be run
   on the no-discount variant (frozen behavior) to show the
   counterfactual: without discount, the single 99 permanently breaks
   the loop (no wrong inference, but no inference at all). This frames
   the trade precisely.
5. **Source labels are researcher knowledge.** The "genuine" vs
   "self-generated" labels are known to the experimenter, not the
   learner. The design must not leak these labels into the learner
   state (e.g., via different teach paths that the learner could
   distinguish). All facts must enter through the same production
   paths the learner normally uses.

## 5. Relationship to other work

- **Contradiction break (`510b6cb42`).** The adversarial world is the
  epistemic inverse of the contradiction-break probe. Same mechanics,
  flipped truth labels.
- **Discount spec (`62fa77192`), Section 6.2.** This design is the
  concrete realization of the flagged adversarial test.
- **Discount impl (`0daaa2ed4`).** The validated minimal subset
  (D1+D2+W3+R1) is the target. W1/W2 are not required for the core
  adversarial result (teach-path introduction bypasses observe).
- **Source provenance (C6).** The adversarial world demonstrates why
  C6 (source tags from first write) is the actual fix. With source
  tags, W3 could prefer genuine minority over self-generated
  majority. Without them, it cannot.
- **Weak K-LT-5.** Unrelated. The adversarial world tests epistemic
  robustness, not trial-order learning.

## 6. Standing metrics (for this design)

This is a design document; no implementation exists, so behavioral
counts are zero.

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 in this document
  (design only). A future implementation would add: adversarial
  world setup, phase definitions, metric definitions (M1-M5).
  Estimated: 5.
- LEARNER-OWNED STRUCTURAL DECISIONS: 0.
- SOURCE-ENUMERABLE FORMS: 0.
- SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: 0.
- REUSE EVENTS: 0. REVISION EVENTS: 0.
- COGNITION LINES: 0 added (design only).
- MODES: 0. BRIDGES: 0. HANDLERS: 0. SEMANTIC CASES: 0.

## 7. Recommended implementation order (for coordinator, not this task)

1. Build the adversarial world driver on the existing discount
   variant (`0daaa2ed4`).
2. Run Phases 1-3, collect M1-M5, 3/3 byte-identical.
3. Run the no-discount baseline for counterfactual framing.
4. Run the mirror control (Phase 4) if resources permit.
5. Report: does the predicted W3-truth-punishment occur? What is
   the measured rehabilitation cost (M3)?

None of the above is authorized by this task. This task ends at
design.

**Verdict: DISCOUNT-ADVERSARY-COMPLETE.**
