# Weak K-LT-5 Clean Preregistration: FROZEN

Date drafted: 2026-10-01.
Date frozen: 2026-10-01.
Status: **FROZEN.** This preregistration supersedes `weak_klt5/WEAK_KLT5_PREREG.md`
for the clean re-test. It is frozen before the fresh sealed world is built and
before any evaluation binary runs.

## 0. What changed from the VOID run

1. **Order discrepancy resolved.** The VOID prereg specified initial order
   [2,1,0,3,4,5]; the built H3-lite Node 1 uses [0,1,2,3,4,5] (the actual frozen
   source order). This prereg specifies the ACTUAL built order [0,1,2,3,4,5].
   Family 4 (count) is at position 4 in both orders, so the predicted
   convergence trajectory is unchanged.
2. **N scaled to measured budget.** The VOID run measured ~35 nodes/miss for the
   Node-1 variant (vs ~14 estimated). N=20 per phase exhausted the 1024-node
   budget and collapsed the trial. This prereg uses N=10 per phase:
   background ~80 nodes + 20 misses x ~35 = ~780 < 1024.
3. **Trial-execution validity precondition (NEW).** Every probe must execute the
   trial (vc > 0). Any probe with vc = 0 (bootstrap or direct answer) invalidates
   the run as VOID. This is the lesson of the VOID run's Section 7.4.
4. **Fresh sealed world.** A new world is built to this prereg's R1-R5, sealed
   by SHA-256 before evaluation. The VOID world's contents are not reused.

## 1. Purpose

Measure whether H3-lite Node 1 exhibits weak K-LT-5: earlier experience changes
the internal trial-order policy and reduces later search/verification cost on
the same relation with the same structural bias.

Weak K-LT-5 definition (Micah 2026-10-01): earlier experience changes an
internal learning/search policy and reduces later search/verification cost.
This test does NOT claim strong K-LT-5 (genuinely new domain).

## 2. Hypothesis

H1: After N=10 misses in a count-biased world (Phase A), the Node-1 policy
converges to [4,0,1,2,3,5], and Phase B (N=10 misses, same relation, same bias)
costs strictly less trial verification than Phase A, with R = E(A)/E(B) > 1.15.

H0: The policy does not produce transfer; R <= 1.15.

## 3. Method

### 3.1 Learner and phases

- Learner: H3-lite Node 1 variant (unfrozen build, `45c55ed83` lineage). Frozen
  TNN-2 cognition unchanged except the Node-1 policy dispatch (already built and
  white-box verified in `h3lite_node1/`).
- Phase A: N=10 misses, subjects s_1..s_10, relation r=50, expected answer 4,
  flags 0 (unmasked; dc=0, di=0 so all families eligible).
- Phase B: N=10 misses, subjects s_11..s_20, same relation r=50, expected 4,
  flags 0. No process reset, no learner-state reset, no recompilation between
  phases. Policy state carries over from Phase A.
- E(X) = total `t2_try_verify` invocations across Phase X (read from the
  trial-stats header: verifies = header16 / 1024, zeroed before each probe).
- R = E(A) / E(B).

### 3.2 Predicted trajectories (actual order [0,1,2,3,4,5])

Initial policy: [0,1,2,3,4,5]. Family 4 (count) at slot 4.

Phase A:
- Miss 1: tries slots 0-4 (families 0,1,2,3,4): 5 verifies. Family 4 succeeds.
  Hebbian swap slots 3,4. Order: [0,1,2,4,3,5].
- Miss 2: 4 verifies. Swap slots 2,3. Order: [0,1,4,2,3,5].
- Miss 3: 3 verifies. Swap slots 1,2. Order: [0,4,1,2,3,5].
- Miss 4: 2 verifies. Swap slots 0,1. Order: [4,0,1,2,3,5].
- Misses 5-10: 1 verify each (family 4 at slot 0, no swap).

E(A) = 5+4+3+2+1+1+1+1+1+1 = 20.

Phase B (policy starts [4,0,1,2,3,5]):
- Misses 1-10: 1 verify each.

E(B) = 10.

R = 20/10 = **2.00**.

Prediction: R = 2.00 > 1.15. PASS if all kill bars hold.

### 3.3 Sealed world requirements (R1-R5)

R1 (bias): For every probe, family 4 (count) verifies successfully (count = 4 =
expected), while families 0,1,2 (chains k=2,3,4), 3 (sum), and 5 (single hop)
fail verification.

R2 (distinct subjects): All 20 subjects distinct. No (s,r) key repeats.

R3 (same relation): All 20 misses use relation r=50.

R4 (no direct answers): The teach stream contains no (s,50,*) fact for any probe
subject. Every probe must reach the trial. If any probe is answered by
`activate()` direct lookup, the run is VOID.

R5 (verifiability): Expected answer 4 is unambiguous; the count assembler
produces exactly 4 on every probe.

World construction: each subject s gets background chain facts
(s,51,c1),(c1,51,c2),(c2,51,c3),(c3,51,c4) with chain-node ids chosen so no
chain value equals 4 (ensuring R1 for families 0,1,2,3,5). The count family
follows relation 51 from s, finds a 5-node chain, assembles 4 increments,
and verifies 4 = expected.

### 3.4 Budget validation

Measured Node-1 cost: ~35 nodes/miss (VOID run, Phase A).
Budget: 80 background + 20 x 35 = ~780 < 1024.
A pilot run must confirm live nodes stay below 1000 after Phase B. If the pilot
exceeds 1000, N is reduced and this prereg is amended transparently and
re-frozen before the sealed evaluation.

## 4. Controls

C1 (difficulty): Fresh Node-1 learner runs Phase B subjects only.
Prediction: E(B_fresh) = 20 = E(A). Kill: |E(B_fresh) - E(A)| / E(A) > 10%
implies Phase B intrinsically easier; test VOID.

C2 (causal ablation): After Phase A on the main learner, reset ONLY the policy
node (tag 40, subtype 1) to [0,1,2,3,4,5], rej=0. White-box verify the reset.
Then run Phase B. Prediction: E(B_abl) = 20 = E(A). Kill: |E(B_abl) - E(A)| /
E(A) > 10% implies speedup not caused by policy; causal claim FAILS.

C3 (frozen discrimination): Frozen TNN-2 (verbatim) runs Phase A then B.
Prediction: E(A_f)=E(B_f)=50, R_f=1.00. Kill: R_f > 1.15 implies the world or
measure does not discriminate; test VOID.

## 5. Kill bars and verdict

K-WKLT5-1 (transfer): R > 1.15. PASS/FAIL.
K-WKLT5-2 (difficulty): E(B_fresh) within 10% of E(A). Else VOID.
K-WKLT5-3 (ablation): E(B_abl) within 10% of E(A). Else causal FAIL.
K-WKLT5-4 (determinism): 3/3 byte-identical runs, exit 0, zero stderr. Else FAIL.
K-WKLT5-5 (governance): Pure Zag, safebin, zero Python, zero em-dash bytes.
Else PROCESS-FAIL.
K-WKLT5-6 (discrimination): R_f <= 1.15. Else VOID.

**Validity precondition (NEW, from VOID lesson):** Every one of the 20 main-run
probes must show vc > 0 (trial executed). Any probe with vc = 0 means the trial
did not run (bootstrap, direct answer, or collapse); the run is VOID and no
verdict is issued.

Verdict:
- WEAK-KLT5-PASS iff K-1..K-6 pass and validity precondition holds.
- WEAK-KLT5-FAIL iff K-1 fails but K-2..K-6 pass and precondition holds.
- WEAK-KLT5-VOID iff precondition fails or K-2/K-4/K-5/K-6 fails.
- Causal claim holds iff K-3 passes.

## 6. White-box requirements

1. Policy node (tag 40, subtype 1) exists after first miss; order slots
   readable at fields 8,12,16,20,24,28.
2. Hebbian swaps visible in Phase A transcript for misses 1-4 (5,4,3,2
   trajectory with promotion each miss).
3. Phase B transcript shows family 4 attempted first on every miss (vc=1 each).
4. E(A)=20 and E(B)=10 match predictions exactly (deterministic).
5. C2 reset white-box verified ([0,1,2,3,4,5], rej=0) before Phase B rerun.

## 7. Standing architectural metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: six assembler families, Hebbian swap
  rule, demotion threshold 8, initial order [0,1,2,3,4,5] (actual built order),
  N=10, 1.15 threshold, 1024-node budget, vc>0 precondition.
- LEARNER-OWNED STRUCTURAL DECISIONS: trial-order policy values during the run
  (predicted convergence [4,0,1,2,3,5]).
- SOURCE-ENUMERABLE FORMS: 720 possible orders; test exercises at most 5.
- SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: order preference from verify success/failure.
- REUSE EVENTS: policy reads in Phase B using Phase-A-learned order
  (predicted: 10).
- REVISION EVENTS: Hebbian swaps in Phase A (predicted: 4).
- COGNITION LINES: 0 (evaluation only).
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0.

## 8. Non-claims

Same as VOID prereg Section 8: no strong K-LT-5, no uncertainty dedup, no
general policy learning (Node 1 only), no strategy invention, no capability
improvement, no optimality. Additionally: this test does not claim the learned
policy survives memory pressure (the VOID run showed it does not); the budget
is sized so pressure does not occur during the test.

## 9. Freeze record

1. Frozen 2026-10-01 before fresh world construction and before evaluation.
2. Fresh sealed world built after this freeze to R1-R5; SHA-256 recorded before
   any evaluation binary runs.
3. Predictions quantified (E(A)=20, E(B)=10, R=2.00).
4. If the budget pilot exceeds 1000 live nodes, N is reduced via transparent
   amendment and re-freeze before sealed evaluation.
