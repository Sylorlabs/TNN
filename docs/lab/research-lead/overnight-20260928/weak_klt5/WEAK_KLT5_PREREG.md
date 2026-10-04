# Weak K-LT-5 Preregistration: FROZEN

Date drafted: 2026-10-01.
Date frozen: 2026-10-01.
Status: **FROZEN.** This preregistration is frozen before any H3-lite implementation exists. It governs the weak K-LT-5 test for H3-lite Node 1 (trial-order policy). The freeze commit strictly precedes any implementation or evaluation.

Design sources (read-only):
- H3-lite frozen prereg `dab50dd68` (Node 1 specification)
- L2L analysis `106ee6698` (operational definition, weak/strong calibration)
- Lifetime protocol v2 `dd745851e` (K-LT-5w bar, D5 banked decision)
- L2L2 prereg (reference minimal-unit structure)

---

## 1. Purpose

This test measures whether H3-lite Node 1 (revisable trial-order policy) exhibits learning-to-learn in the weak sense: experience with task A measurably reduces the cost of learning task B, where both tasks share the same relation and the same structural bias.

This is the diagnostic readout for H3-lite's policy-revisability claim. It does not test strong K-LT-5 (cross-relation transfer), uncertainty dedup, or strategy invention. Those are explicitly out of scope (see section 8).

---

## 2. Definitions

### 2.1 Weak K-LT-5

**Weak K-LT-5** is present when:

1. A learner experiences N misses in a biased world (Phase A), where one assembler family F* is systematically correct and all families tried before F* in the initial order systematically fail verification.
2. The same learner then experiences N misses on the same relation with the same bias (Phase B).
3. The total trial cost E(B) is strictly less than E(A), with ratio R = E(A)/E(B) > 1.15.
4. A difficulty control shows Phase B is not intrinsically easier (fresh learner on Phase B alone costs E(A)).
5. A causal ablation shows the cost reduction is caused by the trial-order policy state (resetting the policy returns Phase B to E(A) cost).

"Same relation, biased world" means: all misses use the same relation r (with distinct subjects to avoid trivial caching), and the world is constructed so that family F* (count, family id 4) verifies successfully while families 0,1,2,3 (chains k=2,3,4 and sum) fail verification on every probe.

### 2.2 E-ratio

**E(X)** = total number of `t2_try_verify` invocations across all N misses in Phase X.

This counts every assembler family attempted, including failures. It is the direct measure of trial cost. It is observable in transcripts by counting `t2_try_verify` calls per miss.

**R** = E(A) / E(B).

- R > 1.15: **PASS** (weak K-LT-5 present)
- R <= 1.15: **FAIL** (weak K-LT-5 absent)

The 1.15 threshold is adopted from the lifetime protocol v2 K-LT-5w bar.

### 2.3 Why E-ratio, not examples-to-criterion

The L2L analysis defines E() as "examples to criterion." In this test, the criterion is fixed (N misses resolved), and E measures the total trial cost to reach it. This is equivalent: fewer trial attempts per miss means faster learning. The E-ratio captures the policy's effect directly.

---

## 3. Test Design

### 3.1 Phases

**Phase A (policy learning):** N = 20 misses.
- Each miss i uses subject s_i (i = 1..20), all with the same relation r.
- For each miss, the correct answer requires family 4 (count).
- Families 0,1,2,3 fail verification. Family 4 succeeds.
- The trial-order policy starts at the researcher's default: [2,1,0,3,4,5].
- Measure E(A) = total `t2_try_verify` calls across all 20 misses.
- White-box: record the policy node order fields after each miss.

**Phase B (transfer):** N = 20 misses.
- Each miss j uses subject s_{20+j} (j = 1..20), same relation r.
- Same bias: family 4 correct, families 0,1,2,3 fail.
- The trial-order policy starts from the state learned in Phase A (not reset).
- Measure E(B) = total `t2_try_verify` calls across all 20 misses.
- White-box: record the policy node order fields after each miss.

**No process reset, no learner-state reset, no recompilation between phases.** The learner is continuous across A and B. This is the lifetime requirement.

### 3.2 Sealed World Requirements

The sealed world (designed by an independent adversary after this freeze) must satisfy:

1. **R1 (bias):** For every probe in both phases, assembler family 4 (count) produces a graph that verifies successfully against the expected answer, while families 0 (chain k=2), 1 (chain k=3), 2 (chain k=4), and 3 (sum) produce graphs that fail verification. Family 5 (single hop) is never reached in the predicted trajectories but should also fail if reached, for cleanliness.

2. **R2 (distinct subjects):** All 40 subjects (s_1 through s_40) are distinct. No (s,r) key repeats across the 40 misses. This prevents trivial caching and ensures each miss is a genuine trial.

3. **R3 (same relation):** All 40 misses use the same relation r. This is the "same relation" in "same relation, biased world." It ensures we are not testing cross-relation generalization (that is strong K-LT-5, out of scope).

4. **R4 (no direct answers):** The teach stream must contain no direct (s,r) fact that would let `activate()` answer without trial. Every probe must be TRIAL-EXPECTED (per the H2 void lesson in lifetime v2). If more than 2 of 40 probes are answered by direct lookup, the world is VOID.

5. **R5 (verifiability):** The expected answer for each probe must be unambiguous and the count assembler must produce exactly that answer. No ambiguous probes.

The adversary is responsible for concrete world construction satisfying R1-R5. This prereg specifies functional requirements, not implementation details.

### 3.3 Predicted Trajectories

**H3-lite Node 1 (with Hebbian promotion):**

Initial order: [2,1,0,3,4,5] (positions 0-5). Family 4 at position 4.

Phase A:
- Miss 1: tries families at positions 0,1,2,3,4 (5 attempts). Family 4 succeeds at position 4. Hebbian swap: family 4 moves to position 3. Order: [2,1,0,4,3,5].
- Miss 2: 4 attempts. Family 4 at position 3, swap to position 2. Order: [2,1,4,0,3,5].
- Miss 3: 3 attempts. Family 4 at position 2, swap to position 1. Order: [2,4,1,0,3,5].
- Miss 4: 2 attempts. Family 4 at position 1, swap to position 0. Order: [4,2,1,0,3,5].
- Misses 5-20: 1 attempt each (family 4 at position 0, succeeds immediately, no swap since p=0).

E(A) = 5 + 4 + 3 + 2 + (16 * 1) = 30.

Phase B:
- Policy starts as [4,2,1,0,3,5] (from end of Phase A).
- Misses 1-20: 1 attempt each.

E(B) = 20.

R = 30 / 20 = **1.50**.

**Prediction: R = 1.50 > 1.15, PASS.**

**Frozen TNN-2 (control):**

Order fixed at [2,1,0,3,4,5]. Never changes.

Phase A: 20 misses * 5 attempts = 100.
Phase B: 20 misses * 5 attempts = 100.

R = 100 / 100 = **1.00**.

**Prediction: R = 1.00 <= 1.15, FAIL (as expected for frozen TNN-2).**

### 3.4 Why N=20

N=20 is chosen because:
- It allows full policy convergence (4 misses) with 16 post-convergence misses in Phase A, giving a stable E(A).
- It gives R=1.50, comfortably above the 1.15 threshold (not a knife-edge).
- Larger N would dilute R toward 1.0 (convergence cost amortized). Smaller N would make R noisier.
- 40 total misses * ~14 nodes/miss = ~560 nodes, well under the 1024 budget. No eviction confound.

---

## 4. Controls

### 4.1 C1: Difficulty Control (fresh learner)

**Procedure:** A fresh H3-lite learner (policy node at initial default order [2,1,0,3,4,5], no prior experience) runs Phase B alone (20 misses, same subjects s_21..s_40, same relation r, same bias).

**Measure:** E(B_fresh).

**Prediction:** E(B_fresh) = E(A) = 30.

**Kill condition:** If E(B_fresh) < E(A) by more than 10%, Phase B is intrinsically easier and the test is VOID. The transfer claim requires B to be equally difficult.

**Rationale:** Rules out "B is just easier." This is P2 from L2L2.

### 4.2 C2: Causal Ablation (policy reset)

**Procedure:** After Phase A completes on the main learner, reset the trial-order policy node (tag 40, subtype 1) to initial values: order fields [2,1,0,3,4,5], field 32 (rejection count) = 0. All other learner state is preserved. Then run Phase B (20 misses).

**Measure:** E(B_ablated).

**Prediction:** E(B_ablated) = E(A) = 30.

**Kill condition:** If E(B_ablated) < E(A) by more than 10%, the speedup is not caused by the policy node (some other retained state is responsible), and the causal claim FAILS.

**Rationale:** Proves the cost reduction is causally traced to the policy state, not to other retained state (e.g., cached facts, MAPs). This is P3 from L2L2.

**Note:** The ablation must reset ONLY the policy node, not the entire learner state. If other state (e.g., taught facts) affects trial cost, the ablation isolates the policy's contribution.

### 4.3 C3: Frozen TNN-2 Control

**Procedure:** Frozen TNN-2 binary (no H3-lite) runs Phase A then Phase B (40 misses total, same world).

**Measure:** E(A_frozen), E(B_frozen), R_frozen.

**Prediction:** E(A_frozen) = E(B_frozen) = 100. R_frozen = 1.00.

**Rationale:** Confirms the test discriminates. If frozen TNN-2 shows R > 1.15, the world is flawed (some non-policy mechanism is causing speedup) and the test is VOID.

---

## 5. Kill Bars and Verdict Rules

### 5.1 K-WKLT5-1: Transfer Present

**Bar:** R = E(A)/E(B) > 1.15.

**Pass:** Weak K-LT-5 is present. The trial-order policy exhibits learning-to-learn.
**Fail:** Weak K-LT-5 is absent. The policy does not produce measurable transfer.

### 5.2 K-WKLT5-2: Difficulty Control

**Bar:** E(B_fresh) within 10% of E(A).

**Pass:** Phase B is not intrinsically easier. Transfer claim is valid.
**Fail (VOID):** Phase B is easier. The test is invalid; R is uninterpretable.

### 5.3 K-WKLT5-3: Causal Ablation

**Bar:** E(B_ablated) within 10% of E(A).

**Pass:** The speedup is caused by the policy node. Causal claim holds.
**Fail:** The speedup is caused by other state. The policy is not the mechanism.

### 5.4 K-WKLT5-4: Determinism

**Bar:** 3/3 runs byte-identical, exit 0, zero stderr.

**Pass:** Result is deterministic.
**Fail:** Result is non-deterministic; investigate before claiming.

### 5.5 K-WKLT5-5: Governance

**Bar:** Pure Zag, zero Python at every stage, zero em-dash bytes in docs, safebin active.

**Pass:** Governance holds.
**Fail:** Process violation; result is PROCESS-FAIL.

### 5.6 K-WKLT5-6: Discrimination

**Bar:** R_frozen <= 1.15 (frozen TNN-2 does not pass).

**Pass:** The test discriminates H3-lite from frozen.
**Fail (VOID):** The test does not discriminate; world or measure is flawed.

### Verdict Rule

**WEAK-KLT5-PASS** iff K-WKLT5-1 through K-WKLT5-6 all pass.

**WEAK-KLT5-FAIL** if K-WKLT5-1 fails (no transfer) but K-WKLT5-2 through K-WKLT5-6 pass (test is valid but H3-lite does not exhibit weak K-LT-5).

**WEAK-KLT5-VOID** if any of K-WKLT5-2, K-WKLT5-4, K-WKLT5-5, or K-WKLT5-6 fails (test invalid).

---

## 6. White-Box Requirements

Every claimed result must be traceable in white-box state and transcripts:

1. **Policy node existence:** Tag 40, subtype field 4 = 1 node must exist after first miss. Field values (order slots 8,12,16,20,24,28) must be readable.

2. **Write path firing:** The Hebbian swap in `t2_try_verify` must be visible on transcript for misses 1-4 of Phase A. Each swap must show: family F at position p > 0 succeeded, F swapped with position p-1.

3. **Read path use:** The dispatch loop in `t2_trial` must read the order slots. Phase B transcripts must show family 4 attempted first on every miss.

4. **E() measurement:** `t2_try_verify` invocation count per miss must be extractable from transcripts. The E(A)=30, E(B)=20 predictions must match exactly (deterministic).

5. **Ablation verification:** After C2 reset, the policy node fields must read [2,1,0,3,4,5]. Post-ablation Phase B transcripts must show 5 attempts per miss.

If any white-box trace is missing or contradicts the claimed mechanism, the result is unexplained and the corresponding kill bar fails.

---

## 7. Standing Architectural Metric (Reporting Requirements)

Every weak K-LT-5 report must include:

- RESEARCHER-OWNED STRUCTURAL DECISIONS: The six assembler families, the Hebbian swap rule, the demotion threshold (8), the initial order [2,1,0,3,4,5], the N=20 choice, the 1.15 threshold.
- LEARNER-OWNED STRUCTURAL DECISIONS: The trial-order policy values during the run (must pass K-H3 audit or be struck).
- SOURCE-ENUMERABLE FORMS: 720 possible orders (6!); the test exercises at most 5 distinct orders.
- SUF DECISIONS: 0 (policy selection, not form invention).
- LEARNER-INTERNAL CRITERIA: Order preference from verify success/failure.
- REUSE EVENTS: Count of policy reads in Phase B that used the Phase-A-learned order.
- REVISION EVENTS: Count of Hebbian swaps in Phase A (predicted: 4).
- COGNITION LINES: 0 (test only; H3-lite implementation lines counted separately).
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0.

---

## 8. Explicit Non-Claims

This test does NOT establish, and the preregistration forbids claiming:

1. **Strong K-LT-5.** This test uses the same relation in both phases. It does not test cross-relation transfer or conditional policies. Strong K-LT-5 requires a different test.

2. **Uncertainty dedup.** The test uses distinct subjects to avoid (s,r) repeats. It does not measure or claim cheaper repeated ignorance. The dedup gap (L2L analysis Rank 1) is unaddressed.

3. **General policy learning.** Only Node 1 (trial order) is exercised. Nodes 2 (guide template) and 3 (repair topology) are not tested here. Their write paths are not expected to fire (no guide resolutions, no contradictions in this world).

4. **Strategy invention.** The learner selects among 6 fixed families. It does not invent a 7th family or a new trial strategy. SUF is not claimed.

5. **Capability improvement.** No FW1-FW9 score change is predicted or claimed. This is a diagnostic of policy revisability, not a capability benchmark.

6. **Optimality.** R=1.50 is the predicted ratio for N=20 with the Hebbian swap rule. A different N, a different swap rule, or a different world bias would give a different R. The test measures whether transfer exists (R>1.15), not whether the policy is optimal.

---

## 9. Relation to H3-lite K-H3 Audit

This test serves as the **sealed demonstration** for H3-lite Node 1 under K-H3 element 6: "a sealed test demonstrating the decision taking different values after different experience histories."

Specifically:
- K-H3(1): The structural decision is trial search order.
- K-H3(2): Tag 40, subtype 1, fields 8,12,16,20,24,28.
- K-H3(3): Production read path is the dispatch loop in `t2_trial`.
- K-H3(4): Production write path is the Hebbian swap in `t2_try_verify`.
- K-H3(5): Triggering experience is verification success/failure during ordinary misses.
- K-H3(6): This test. Phase A history (counts-biased) leads to order [4,2,1,0,3,5]. A different history (e.g., chains-biased) would lead to a different order. The decision change is an outcome of experience, not an input.

If this test passes with white-box traces showing the write path firing, Node 1 passes K-H3(6). If the policy changes but the write path cannot be shown firing, Node 1 fails K-H3 condition (c).

---

## 10. Freeze Record

1. This preregistration is frozen on 2026-10-01 before any H3-lite implementation exists.
2. The sealed world will be designed by an independent adversary after this freeze, satisfying R1-R5 in section 3.2.
3. Predictions are quantified (E(A)=30, E(B)=20, R=1.50) not directional only.
4. Freeze commit strictly precedes any implementation or evaluation commit.
5. If H3-lite implementation reveals that Node 1 as built differs materially from the frozen prereg `dab50dd68` specification, this test prereg must be amended transparently and re-frozen before evaluation.

---

*End of frozen preregistration. FROZEN 2026-10-01. Evaluation may begin only after H3-lite implementation exists and the sealed world is designed. No scores claimed. Paper untouched.*
