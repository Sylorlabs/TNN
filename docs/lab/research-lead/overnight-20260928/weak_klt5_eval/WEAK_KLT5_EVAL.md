# Weak K-LT-5 Evaluation Report

**Status:** WEAK-KLT5-EVAL-COMPLETE  
**Verdict:** WEAK-KLT5-VOID  
**Date:** 2026-10-01  
**Evaluator:** Independent (did not build H3-lite Node 1, did not design the sealed world)  
**Prereg:** `docs/lab/research-lead/overnight-20260928/weak_klt5/WEAK_KLT5_PREREG.md` (FROZEN, unmodified)  
**Sealed world SHA-256:** `20ed8d698e168661b54b6c510b994a33f02c615edaee6509efb15d9998f4fa90` (verified MATCH before running)

---

## 1. Method

The evaluator built two instrumented binaries from the frozen sources, appending a measurement-only driver (no cognition changes):

- `wkl_M_bin`: H3-lite Node 1 variant (unfrozen build `45c55ed83` lineage) + driver. Runs Phase A (20 probes) then Phase B (20 probes) on one continuous learner. E(X) measured per probe by zeroing the trial-stats header before each `ev_query` and reading `verifies = header16 / 1024` after (the header is write-only instrumentation; reading it changes no behavior).
- `wkl_F_bin`: frozen TNN-2 base (verbatim) + driver. Same 40 probes. C3 discrimination control.
- `wkl_C1_bin`: fresh Node-1 learner, Phase-B probes only. C1 difficulty control.
- `wkl_C2_bin`: Node-1 learner, Phase A, policy-node reset to initial order, Phase B. C2 causal ablation.

World application: SETUP TAG8 (allocate tag-8 node, enabling the sum family), 160 TEACH facts, 40 PROBE queries as `ev_query(s,50,4,0)` (unmasked, flags 0). The world file was translated mechanically line-by-line into the driver; the evaluator independently verified R2 (40 distinct subjects 1001-1040), R3 (all relation 50), R4 (zero TEACH with relation 50), R5 (expected 4, flags 0).

All computation in pure Zag via the pinned `znc`. Safebin active. Zero Python. 3/3 byte-identical runs for the main scenario.

---

## 2. Measurements

### 2.1 Main scenario (Node 1, Phase A then B), 3/3 identical

SHA-256 `27b6bcbe2e00f3777f782e79f8d50c527828db3fc33e40bc0cd454a18563388e` (all three runs).

**Phase A:** per-miss verify counts `5,4,3,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1`. **E(A)=30.** Policy converged to `[4,0,1,2,3,5]`, rej=0. Live nodes after Phase A: 853. This matches the prereg prediction (E(A)=30) EXACTLY, including the Hebbian convergence trajectory.

**Phase B:** per-miss verify counts `1,1,1,1,1,1,5,0,0,0,0,0,0,0,0,0,0,0,0,0`. **E(B)=11.** Final policy `[0,1,2,3,4,5]`, rej=8. Live nodes: 1022 (budget exhausted).

**R = 30/11 = 2.72 (R100=272).**

### 2.2 C1 difficulty control (fresh learner, Phase B probes only)

Per-miss: `5,4,3,2,1,1,...,1`. **E(B_fresh)=30.** Policy converged to `[4,0,1,2,3,5]`. Completed in under 2 seconds; no budget pressure (861 nodes max).

### 2.3 C3 frozen control (frozen TNN-2, Phase A then B)

**Phase A:** `5,5,5,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0`. **E(A_frozen)=30.**  
**Phase B:** `0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0`. **E(B_frozen)=4.**  
**R_frozen = 30/4 = 7.50 (R100=750).**

### 2.4 C2 causal ablation (Phase A, policy reset, Phase B)

Phase A reproduced E(C2A)=30 with convergence to `[4,0,1,2,3,5]`. The reset was white-box verified (`policy: 0,1,2,3,4,5 rej=0`). Phase B per-miss: `6,0,0,0,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0`. **E(B_abl)=12.** Final policy `[0,1,2,3,4,5]`, rej=7.

Note: the first post-reset miss cost 6 verifies (not 5), indicating accumulated Phase-A state adds a trial candidate versus a fresh workspace. 18 of 20 post-reset misses were answered by bootstrap with zero trial verifies.

---

## 3. Diagnosis: the budget wall (white-box, source-grounded)

The prereg estimated ~14 nodes per miss (~560 for 40 probes), predicting no memory pressure. Measured node consumption:

- Frozen base: ~165 nodes per successful trial+promote. Budget (1024) exhausted during the 6th probe (996 live before probe 7; 1022 at probe 7).
- Node-1 variant: ~35 nodes per miss in Phase A (853 after 20). Budget exhausted during Phase B probe 7.

A dedicated diagnostic binary confirmed the causal chain at the moment of collapse (frozen base, probe 7): live nodes = 1022, live FACT nodes with the probe subject = 0 (the background chain facts had been evicted), verify calls = 0, answer = 4.

Mechanism, traced in source:
1. `evict_node` selects the lowest-bid unprotected node. Background chain facts (old, low bid) and the policy node (tag 40, low bid, no type-9 protection edge) are prime victims.
2. With chain facts gone, `t2_gather`/`t2_gather_sum`/`t2_rels` find nothing; the trial makes zero `t2_try_verify` calls and returns -2.
3. `ev_query` falls through to `bootstrap_miss`, which finds unanimous prior `(r=50,o=4)` shadow facts and returns 4, teaching a direct `(s,50,4)` fact.
4. The policy node, when evicted, is recreated by `h3n1_get_policy` with the INITIAL order `[0,1,2,3,4,5]` (source lines 602-612), causing re-convergence (the `vc=5` at B i=6).

Consequences for the E measure:
- 13 of 20 Phase-B misses in the main scenario were answered by bootstrap unanimity with ZERO trial verify calls, not by the learned policy.
- The frozen control's E(A_frozen)=30 and E(B_frozen)=4 are likewise artifacts of trial collapse, not of trial cost.
- R_frozen=7.50 does not indicate a world flaw; it indicates protocol infeasibility.

---

## 4. Kill-bar assessment

- **K-WKLT5-1 (Transfer Present, R > 1.15):** Measured R=2.72 > 1.15, but the prereg's white-box requirements (Section 6) require Phase-B transcripts to show family 4 attempted first on every miss and state that a trace contradicting the claimed mechanism fails the bar. 13 of 20 Phase-B misses show zero attempts (bootstrap, not policy). The cost reduction is not caused by the trial-order policy. **FAIL** (mechanism contradicted; the numeric ratio is an artifact).
- **K-WKLT5-2 (Difficulty, E(B_fresh) within 10% of E(A)):** 30 vs 30. **PASS.** Phase B is not intrinsically easier.
- **K-WKLT5-3 (Causal ablation, E(B_abl) within 10% of E(A)):** E(B_abl)=12 vs E(A)=30. Not within 10%. **FAIL.** The ablation is confounded by the same wall: 18 of 20 post-reset misses never ran a trial (bootstrap answered), so E(B_abl) does not measure the reset policy's cost. The one clean post-reset trial (C2B i=0) cost 6 verifies, not 5, showing other retained state affects trial cost.
- **K-WKLT5-4 (Determinism, 3/3 byte-identical):** Main scenario 3/3 identical, exit 0, zero stderr. **PASS.**
- **K-WKLT5-5 (Governance):** Pure Zag, safebin active, zero Python invocations, zero em-dash bytes in docs. **PASS.**
- **K-WKLT5-6 (Discrimination, R_frozen <= 1.15):** R_frozen=7.50. **FAIL.**

**Verdict rule application:** K-WKLT5-6 fails → **WEAK-KLT5-VOID** (test invalid as designed).

The VOID is not because the sealed world is flawed (R1-R5 all verified; the count-family bias is real and the policy demonstrably exploits it). It is because the frozen protocol's resource assumption was wrong by an order of magnitude, so neither arm completes the specified N=20 phases with a valid E measure.

---

## 5. What the test DID establish (mechanism level)

Although the protocol-level verdict is VOID, the white-box traces establish three mechanism-level facts about H3-lite Node 1:

1. **The Hebbian policy learns exactly as predicted.** Phase A shows the 5,4,3,2,1 convergence with E(A)=30, matching the prereg's quantitative prediction to the integer. The write path (promotion on success at slot>0) fires visibly in the trajectory.
2. **Transfer occurs before the wall.** Phase B misses 1-6 run at 1 verify each (policy `[4,0,1,2,3,5]` read on the production dispatch path). The decision takes different values after different experience histories (K-H3 element 6, mechanism half).
3. **Learned state does not survive memory pressure.** The policy node is evictable and unprotected; eviction resets it to the researcher's initial order. This is a genuine architectural limitation of the implementation, not a test artifact: learner-owned state is more fragile than the frozen fixed order under the same budget.

---

## 6. Standing architectural metrics (prereg Section 7)

- RESEARCHER-OWNED STRUCTURAL DECISIONS: six assembler families, Hebbian swap rule, demotion threshold 8, initial order [0,1,2,3,4,5] (actual built order; prereg text said [2,1,0,3,4,5]), N=20, 1.15 threshold, 1024-node budget.
- LEARNER-OWNED STRUCTURAL DECISIONS: trial-order policy values during the run (converged [4,0,1,2,3,5] in Phase A; reset by eviction in Phase B).
- SOURCE-ENUMERABLE FORMS: 720 possible orders; test exercised 5 distinct orders.
- SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: order preference from verify success/failure (Hebbian).
- REUSE EVENTS: 6 (Phase-B misses 1-6 reading the converged order before the wall).
- REVISION EVENTS: 4 (Hebbian promotions in Phase A) + 1 re-convergence promotion at B i=6.
- COGNITION LINES: 0 (evaluation only).
- MODES: 0, BRIDGES: 0, HANDLERS: 0, SEMANTIC CASES: 0.

---

## 7. Implications and recommendations

1. **The weak K-LT-5 question is not answered.** A re-test needs a feasible protocol: either N scaled to the measured node budget (pilot first), or a node budget sized from measured per-miss cost, with the prereg amended transparently and re-frozen. The evaluator recommends the amendment route, not a reinterpretation of this VOID run.
2. **Node-1 needs eviction protection for the policy node** (or a utility-based protection scheme) before any lifetime claim. The current implementation loses learned policy state under pressure that the frozen baseline does not suffer (its order is in code, not in evictable state). This asymmetry is the precise architectural gap.
3. **Per-miss node cost (~165 frozen, ~35 Node-1 variant) must be measured and budgeted** in all future lifetime protocols. The prereg's ~14/miss estimate was the root cause of this VOID.
4. **Bootstrap unanimity as a fallback** answered 13/20 Phase-B probes correctly. This is the P-INV mechanism working as designed, but it contaminates E as a trial-cost measure whenever the trial cannot run. Future E-based tests must assert trial execution per miss (vc>0) as a validity precondition.

## 8. Artifacts

- `NAMECHECK.md` (Step 0, hash verification, independence)
- `WEAK_KLT5_EVAL.md` (this report)
- `wkl_driver_node1.zag`, `wkl_driver_frozen.zag`, `wkl_drv_M/C1/C2.zag` (eval drivers)
- `wkl_M_bin`, `wkl_C1_bin`, `wkl_C2_bin`, `wkl_F_bin`, `wkl_diag_bin` (compiled evaluators)
- `M_run1.txt`, `M_run2.txt`, `M_run3.txt` (3/3 identical, SHA-256 `27b6bcbe...`)
- `C1_run1.txt`, `C2_run1.txt`, `F_run1.txt` (controls)
- `teach.inc`, `probes.inc` (mechanical translation of the sealed world)
- `wld_data` derivation: `awk` translation of `world_sealed.txt` (verified 160/40/1 lines)

Sealed world contents are not reproduced in this report. Only hashes and metrics.

---

*No em dashes were used in this document. Paper untouched. Nothing pushed.*
