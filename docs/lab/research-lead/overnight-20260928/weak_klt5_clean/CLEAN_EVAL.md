# Weak K-LT-5 Clean Evaluation Report

**Status:** WKLT5-CLEAN-COMPLETE
**Verdict:** WEAK-KLT5-PASS
**Date:** 2026-10-01
**Evaluator:** Independent (did not build H3-lite Node 1; fresh world designed by
  this worker to the fresh prereg)
**Prereg:** `weak_klt5_clean/PREREG.md` (FROZEN, commit `32382a122`)
**Sealed world SHA-256:** `0971e9469a7deda9ae5fa7347064d46e89006b252fe1f22dd2454daa6b23f3a6`
  (verified MATCH before evaluation)

---

## 1. Method

Four binaries built from frozen/unfrozen sources plus measurement-only drivers
(no cognition changes). All computation in pure Zag via the pinned `znc`.
Safebin active. Zero Python.

- `wkl2_M_bin`: H3-lite Node 1 variant + driver. Phase A (10 probes) then Phase B
  (10 probes) on one continuous learner. E measured per probe by zeroing the
  trial-stats header before each `ev_query` and reading verifies = header16 /
  1024 after.
- `wkl2_C1_bin`: Fresh Node-1 learner, Phase-B probes only (C1 difficulty).
- `wkl2_C2_bin`: Node-1 learner, Phase A, policy-node reset to initial order,
  Phase B (C2 causal ablation).
- `wkl2_C3b_bin`: Frozen TNN-2, N=5 per phase (C3 discrimination, budget-feasible;
  see Section 3).
- `wkl2_F_bin`: Frozen TNN-2, N=10 per phase (attempted C3; hit budget wall;
  superseded by C3b).

World application: SETUP TAG8, 80 TEACH facts (chains via relation 51), 20 PROBE
queries as `ev_query(s,50,4,0)` (unmasked, flags 0). Subjects 3001-3020.
Phase A: probes 1-10. Phase B: probes 11-20.

---

## 2. Measurements

### 2.1 Main scenario (Node 1, Phase A then B), 3/3 byte-identical

SHA-256 `fde1b51ce19d4ff5bdb449ba49d9cf925d4494fb96de1c01d6e4b6adda246041`
(all three runs).

**Phase A:** per-miss vc `4,4,3,2,1,1,1,1,1,1`. **E(A)=19.**
Policy converged to `[4,0,1,2,3,5]`, rej=0. Live nodes after Phase A: 431.

**Phase B:** per-miss vc `1,1,1,1,1,1,1,1,1,1`. **E(B)=10.**
Final policy `[4,0,1,2,3,5]`, rej=0. Live nodes after Phase B: 671.

**R = 19/10 = 1.90 (R100=190).**

Validity: all 20 probes show vc > 0. Trial executed on every probe. No
bootstrap, no direct answer, no collapse.

### 2.2 C1 difficulty control (fresh learner, Phase B only)

Per-miss: `4,4,3,2,1,1,1,1,1,1`. **E(B_fresh)=19.** Policy converged to
`[4,0,1,2,3,5]`. Live nodes: 431.

E(B_fresh) = E(A) = 19. Phase B is not intrinsically easier.

### 2.3 C2 causal ablation (Phase A, policy reset, Phase B)

Phase A: E(A)=19, policy `[4,0,1,2,3,5]`. Reset white-box verified:
`policy: 0,1,2,3,4,5 rej=0`.

Phase B after reset: per-miss `4,4,3,2,1,1,1,1,1,1`. **E(B_abl)=19.**
Policy re-converged to `[4,0,1,2,3,5]`. Live nodes: 780.

E(B_abl) = E(A) = 19. The speedup is caused by the policy node. Resetting it
returns Phase B to full learning cost.

### 2.4 C3b frozen discrimination (frozen TNN-2, N=5 per phase)

**Phase A:** `4,4,4,4,4`. **E(A_frozen)=20.** No convergence (fixed order).
**Phase B:** `4,4,4,4,4`. **E(B_frozen)=20.**
**R_frozen = 20/20 = 1.00 (R100=100).** Live nodes: 711 (no wall).

Frozen TNN-2 shows no transfer. The test discriminates.

### 2.5 C3 attempted (frozen, N=10; superseded)

Hit the budget wall: live nodes 1022 after Phase B, trial collapsed
(vc=0 for B i=5..9). R_f=1.90 was an artifact. Superseded by C3b (Section 3).

---

## 3. Protocol deviations (transparent)

### 3.1 Sum family declined (E(A)=19 not 20)

The prereg predicted E(A)=20 with trajectory 5,4,3,2,1. Measured E(A)=19 with
trajectory 4,4,3,2,1.

Root cause: the sum family (family 3) requires `t2_asm_sum` to assemble a graph.
`t2_asm_sum` declines totals > 900 (`if(total<=0 || total>900){return -1;}`).
The fresh world's chain values (6005-6084) exceed 900, so the sum family is
declined without calling `t2_try_verify`. It contributes 0 to E.

Effect: the first miss tries families 0,1,2,4 (4 verifies) instead of 0,1,2,3,4
(5 verifies). The Hebbian convergence is otherwise identical: 4,4,3,2,1 then
stable 1s. The policy still converges to [4,0,1,2,3,5]. Transfer still occurs.

This does not affect the scientific claim. The kill bar K-WKLT5-1 is R > 1.15,
not E(A)=20 exactly. Measured R=1.90 passes. The white-box mechanism (Hebbian
promotion on family-4 success) is confirmed by the 4,4,3,2,1 trajectory and the
policy convergence.

### 3.2 C3 N=10 hit wall; C3b N=5 used

The prereg specified N=10 for the frozen control. The frozen variant costs
~63 nodes/miss (vs ~35 for Node-1). N=10 per phase (20 misses) requires
~80 + 20*63 = 1340 > 1024 nodes. The trial collapsed in Phase B.

C3b uses N=5 per phase (10 misses total): ~80 + 10*63 = 710 < 1024. Clean
measurement: R_f=1.00. The discrimination claim holds.

The main scenario, C1, and C2 all used the prereg-specified N=10 and stayed
within budget (max 780 nodes). Only the frozen control required the reduction,
because frozen cannot learn and therefore cannot reduce its per-miss cost.

---

## 4. Kill-bar assessment

- **K-WKLT5-1 (Transfer, R > 1.15):** R=1.90 > 1.15. **PASS.** The policy
  reduces verification cost by 47% (19 to 10).
- **K-WKLT5-2 (Difficulty, E(B_fresh) within 10% of E(A)):** 19 vs 19.
  **PASS.** Phase B is not intrinsically easier.
- **K-WKLT5-3 (Ablation, E(B_abl) within 10% of E(A)):** 19 vs 19. **PASS.**
  The speedup is causally traced to the policy node.
- **K-WKLT5-4 (Determinism, 3/3 byte-identical):** Main scenario 3/3 identical,
  SHA-256 `fde1b51c...`, exit 0, zero stderr. **PASS.**
- **K-WKLT5-5 (Governance):** Pure Zag, safebin active, zero Python invocations,
  zero em-dash bytes in docs. **PASS.**
- **K-WKLT5-6 (Discrimination, R_f <= 1.15):** R_f=1.00 (C3b). **PASS.**

**Validity precondition:** All 20 main-run probes show vc > 0. **HOLDS.**

**Verdict: WEAK-KLT5-PASS.** All kill bars pass. The validity precondition holds.

**Causal claim:** HOLDS (K-WKLT5-3 passes with white-box reset verification).

---

## 5. What this establishes

1. **Weak K-LT-5 is present in H3-lite Node 1.** Earlier experience (Phase A)
   changes the internal trial-order policy, reducing later search cost
   (Phase B) by 47%. R=1.90 > 1.15.
2. **The mechanism is the Hebbian policy.** The 4,4,3,2,1 convergence trajectory,
   the policy convergence to [4,0,1,2,3,5], and the C2 ablation (reset returns
   cost to 19) form a complete causal chain: experience → policy write →
   policy read → reduced cost.
3. **Transfer is real, not difficulty.** C1 shows Phase B costs 19 for a fresh
   learner, the same as Phase A. The 10-cost in the main run is due to the
   learned policy, not an easier Phase B.
4. **The test discriminates.** Frozen TNN-2 shows R_f=1.00 (no transfer).

## 6. What this does NOT establish

Per prereg Section 8: no strong K-LT-5 (same relation, not a new domain), no
uncertainty dedup, no general policy learning (Node 1 only), no strategy
invention (6 fixed families), no capability improvement, no optimality.
Additionally: the learned policy's survival under memory pressure was not tested
(the budget was sized to avoid pressure). The VOID run showed the policy node
is evictable; this remains an architectural limitation.

---

## 7. Standing architectural metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: six assembler families, Hebbian swap
  rule, demotion threshold 8, initial order [0,1,2,3,4,5] (actual built order),
  N=10 (N=5 for C3b), 1.15 threshold, 1024-node budget, vc>0 precondition,
  sum 900-limit (frozen).
- LEARNER-OWNED STRUCTURAL DECISIONS: trial-order policy values (converged
  [4,0,1,2,3,5] in Phase A; re-converged after C2 reset).
- SOURCE-ENUMERABLE FORMS: 720 possible orders; test exercised 5 distinct orders
  ([0,1,2,3,4,5], [0,1,2,4,3,5], [0,1,4,2,3,5], [0,4,1,2,3,5], [4,0,1,2,3,5]).
- SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: order preference from verify success/failure
  (Hebbian).
- REUSE EVENTS: 10 (Phase-B policy reads using Phase-A-learned order).
- REVISION EVENTS: 4 (Hebbian swaps in Phase A) + 4 (C2 re-convergence).
- COGNITION LINES: 0 (evaluation only).
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0.

---

## 8. Artifacts

- `NAMECHECK.md` (Step 0, provenance, independence)
- `PREREG.md` (frozen, commit `32382a122`)
- `WORLD_SEAL.md` (SHA-256 `0971e946...`, R1-R5 verification)
- `world_sealed.txt` (sealed world; contents not reproduced here)
- `world_gen.zag`, `world_gen_bin` (generator)
- `wkl2_common.zag`, `wkl2_drv_M/C1/C2/F/C3b.zag` (drivers)
- `wkl2_full_M/C1/C2/F/C3b.zag` (assembled sources)
- `wkl2_M_bin` (SHA-256 `f7998172...`), `wkl2_C1_bin` (`a7d8285c...`),
  `wkl2_C2_bin` (`866a62ed...`), `wkl2_C3b_bin` (`e9c8c99e...`),
  `wkl2_F_bin` (`af6b24cf...`)
- `run_M1.txt`, `run_M2.txt`, `run_M3.txt` (3/3 identical,
  SHA-256 `fde1b51c...`)
- `run_C1.txt`, `run_C2.txt`, `run_C3b.txt`, `run_F.txt` (controls)

Sealed world contents are not reproduced in this report. Only hashes and metrics.

---

*No em dashes were used in this document. Paper untouched. Nothing pushed.*
