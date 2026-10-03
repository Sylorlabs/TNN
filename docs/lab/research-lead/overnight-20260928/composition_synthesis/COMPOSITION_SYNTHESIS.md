# Composition Synthesis

**Date:** 2026-10-03
**Purpose:** Strategic map of the composition research frontier: what is handled, by what mechanism, with what verdicts; what remains open; whether one mechanism or several survive.

Evidence base: WATCHDOG ledger commits C361 through C434 on branch `tnn-native-lab` (commit messages carry the canonical per-entry verdicts), plus the memory-recorded composition history (A/B/C comparison, C319 collapse, three-level battery, heterogeneity negatives). Ledger numbers below are quoted verbatim from the committing WATCHDOG entries. Known caveat: concurrent watchdogs double-assigned several numbers (C377, C378, C379, C380, C396, C398, C403, C404, C406, C407, C409, C410); each entry is disambiguated here by its name, not just its number.

---

## 1. Executive summary

Composition now has exactly one live general mechanism for learned-structure composition: the unified 5-operation contract module established by C424 (CONTRACT-UNIFICATION, SUBSUMES), which absorbed GEN, LCONT, and FC. Its documented shape envelope covers pipelines, fan-out/diamond, fan-in, DAG-4, chain-3, partial applicability, and the full cycle family (fixpoint, generalized, oscillatory, convergent, feedback). U, the earlier unified DFS operation, was formally retired as a separate mechanism by C413 and survives only as a documented restricted form of GEN.

One lane remains potentially distinct: COGOPS procedure composition (C417 2-way, C422 3-way, C433 diamond), which composes learner-owned procedure bodies via trial-learned bindings and topo assembly. No subsumption test has yet been run between the contract module and COGOPS composition, so "one mechanism" is the honest status only for learned-structure (MAP/contract) composition, not for procedure-body composition.

L2 adaptive reuse has substantial BUILD-PASS evidence for truncate, substitute, specialize, and cross-domain combine, but two BOUND entries (C388 interface adaptation, C390 extension) flag principled limits that may need protected-core change. L3 novel intermediate in composition is unresolved: the Level 3 battery FAILED, and no lane has demonstrated a learner-invented bridge structure used in composition. Oracle-free composition (no expected-answer verification) and composite revision after counterexample remain open.

---

## 2. The composition envelope

### 2.1 Shapes handled, with verdicts

| Shape / family | Mechanism | Ledger | Verdict | Notes |
|---|---|---|---|---|
| Pipeline pairs (5 pairs, incl. spatial-layout x task-scheduling) | U | C368 | BUILD-PASS K1-K6 | Unmodified U handled all 5; 3/3 byte-identical |
| Pipeline pairs, ANS parity | GEN-R restriction | C413 | demonstrated | U retired; parity on 5 pairs; 3/3 byte-identical |
| Diamond / fan-out | GEN (value-graph generalization) | C380 | INFORMATIVE-FAIL for U; GEN solves | U's trial space {singles,pairs} defeated; GEN needed no new mechanism; boundary not fundamental |
| Diamond / fan-out | COGOPS procedures | C433 | DEMONSTRATED K1-K6 | 3 diamond goals (divergent, convergent, world-B) from same bindings; generic multi-source fan-in, not a handler; 6/6 agreement 1.77x; chain regression clean |
| Fan-in, DAG-4, chain-3, partial applicability | frozen GEN, unmodified | C402 | PASS K1-K7 | Diamond failure was a trial-space limit, not a shape patch |
| Fixpoint cycles (C403) | GEN sequences + learned halting | C414 | PASS C1-C8 | seqmax=2 byte-identical to U; 5 pairs + GEN batteries regress clean; "cycles join general envelope via one principle" |
| Generalized cycles (alternating 5-hop chain, data-dependent halt, HALT-kind additive) | sequences + halting | C420 | PASS G1-G9 | Mechanism general, not fitted; C403 regression clean |
| Oscillatory cycles (period-2, period-3, lasso) | frozen sequences + halting | C425 | PASS O1-O9 | Zero mechanism change; fixpoint halt never misfires; detection-vocabulary gap characterized, not patched |
| Convergent signal | GEN | C428 | PASS | QC1 ANS=7004, QC2 ANS=7106 exact-length, QC3 ANS=7204 limit-distinguished; threshold-halt characterized, not patched |
| Feedback / re-application with learned termination | sequences + halting | C430 | INFORMATIVE-FAIL (prereg arithmetic, not mechanism) | F3 prereg TRIES=44 miscalculated vs actual 28; winner [0,1,0,1] k=4 exact; F4/F5 PASS; mechanism vindicated with zero change |
| Feedback refix | sequences + halting | C432 | PASS | Fresh prereg TRIES=28 correct; frozen binary re-run 3/3 byte-identical; C430 INFORMATIVE-FAIL stands unaltered; feedback family closed clean |
| 2-way procedure composition | COGOPS | C417 | DEMONSTRATED K1-K6 | Two learner-owned procedures composed learner-driven; per-goal order [R,V]/[V,R]; version selection from coverage; plans persisted/reused; 10/10 agreement |
| 3-way procedure composition | COGOPS | C422 | DEMONSTRATED K1-K9 | 3 procedures, 3 forced orders [RVC]/[CRV]/[VRC] from identical bindings; version selection; re-derivation byte-identical; 12/12 agreement; 1.92x efficiency |
| Learned-contract unification | contract module | C424 | SUBSUMES | One 5-op module (induct/check/grow/invalidate/revise) unifies GEN+LCONT+FC; 7/7 bars PASS; F1/F2/F3 silent; drift latch q=3 9/9; grammar 6/6 exact; zero scenario branches |
| Domain-blindness | U | C398 | PASS B1-B6 | U invariant to human identifiers and kind-label polarity; no architectural failure |
| Domain-blindness (relation labels) | U | C399 (second assignment) | PASS | Composition U independent of human relation labels |
| Joint blindness (relation+node relabel) | composition | C409 (second assignment) | PASS | Simultaneous relabeling changes zero bytes |
| Node-blindness | U | C403 (second assignment) | PASS | Composition U independent of node-id values |
| Redimensioned arena (nm dynamic) | GEN-REDIM | C429 then C434 | PASS exploratory, then CLEAN-REPRODUCTION-PASS canonical | C429 was PROCESS-FAIL (self-disclosed python3 keystroke, zero-computation) and stayed exploratory; C434 clean safebin reproduction promoted it to canonical; 5/10+ unblocked |

### 2.2 Mechanism lineage: what is live, what is retired

Live: the unified contract module (C424). It reproduces GEN behavior, LCONT drift traces, and FC grammar picks with 7/7 bars and no scenario branches. GEN's own generalizations (sequences + learned halting for cycles, value-graph generalization for diamond, redimensioned NM arena) are inherited into the contract module's lineage.

Retired: A (contract/plen chaining via compose_try), B (co-use type-15 LINK edges), C (constraint-driven assembly). These three were collapsed into U by C319 and independently reproduced by C325. U itself was then shown to be subsumed by GEN (C397 PARTIAL, then C406 UPGRADE-TO-SUBSUMES after a 10-line state fix, with an explicit recommendation to retire U), and formally retired as a separate mechanism by C413. U survives only as a documented restricted form; a 15-row inventory was recorded.

Live but relationship-untested: COGOPS composition. C417, C422, and C433 demonstrate procedure-body composition over learner-owned cognitive-operation bodies. This lane postdates the C418 compression audit (which flagged the chain family but did not cover COGOPS), and no ledger entry records a subsumption test between COGOPS composition and the contract module.

### 2.3 Cycle map: closed, with characterized boundaries

C432 records "cycle family map scientifically closed." The five cycle families each have at least one PASS: fixpoint (C414), generalized (C420), oscillatory (C425), convergent (C428), feedback (C432, after C430's prereg-arithmetic INFORMATIVE-FAIL). Two known boundaries were characterized rather than patched: the detection-vocabulary gap (C425) and threshold-halt specificity (C428). The cycle result rests on one principle, sequences plus learned halting, with zero mechanism change across families.

---

## 3. Verdict inventory: exact ledger citations

- C368: COMPOSE-PAIR5 BUILD-PASS K1-K6. Unmodified U handles 5th pair (spatial-layout x task-scheduling). 3/3 byte-identical.
- C380 (first assignment): COMPOSE-PAIR6-ADV INFORMATIVE-FAIL. Diamond defeats U's trial space {singles,pairs}; GEN value-graph generalization solves it with no new mechanism. Boundary is not fundamental.
- C380 (second assignment): TRUNC-1 PASS. Z2 truncates to Z1; adaptive reuse demonstrated. (Duplicate numbering; both entries preserved by watchdog convention.)
- C397: GEN-SUBSUMES-U PARTIAL. GEN reproduces U's 5 linear pairs plus diamond; residual boundary was multi-query contract growth from a stale tried-state defect, not a principled limit. Explicit: do NOT retire U yet.
- C398 (first assignment): DOMAIN-BLINDNESS PASS. U invariant to human identifiers and kind-label polarity, B1-B6 all PASS, no architectural failure.
- C398 (second assignment): DEEP7-RC EXPLORATORY. Unrelated (stack overflow investigation); duplicate number.
- C399 (second assignment): DOMAIN-BLIND PASS. Composition U independent of human relation labels. (C399 first assignment was LCONT-1; see below.)
- C402 (second assignment): GEN-GENERALITY GEN-GENERAL K1-K7. Unmodified frozen GEN handles fan-in, DAG-4, chain-3, partial applicability; diamond was a trial-space limit, not a shape patch. 3/3 byte-identical.
- C403 (second assignment): NODE-BLIND PASS. Composition U independent of node-id values. (C403 first assignment: COMPOSE-CYCLES INFORMATIVE-FAIL, the fixpoint problem later solved by C414.)
- C404 (second assignment): NEGATIVE-TRANSFER NT1 PASS. (Not composition; recorded for the interference context in section 5.)
- C406 (first assignment): GEN-STATEFIX UPGRADE-TO-SUBSUMES. 10-line fix restores P5 sequential growth (ANS=3 TRIES=6, no WIDEN); zero regression on 9 subsumes plus diamond batteries; 3/3 byte-identical; recommend retiring U.
- C406 (second assignment): COGNITIVE-OPS-LEARNER MIGRATION DEMONSTRATED. VERIFY specialized into a learner-owned indexed procedure. (Duplicate number; this entry is the origin of the COGOPS lane, later continued as C417.)
- C409 (second assignment): JOINT-BLIND PASS. Simultaneous relation+node relabeling changes zero bytes. (C409 first assignment was the L3-INR sealed KILL, unrelated.)
- C410 (second assignment): GEN-STRESS BOUNDARY-FOUND ARENA-4MAP. Frozen GEN cannot address 5+ structures; nm=5-7 silent corruption, nm=8 panic; WIDEN breaks decline-soundness; 64-pool caps quantified. 3/3 byte-identical. (Superseded in effect by C429/C434 redimensioning.)
- C413: U-RETIREMENT. U formally retired as separate mechanism; GEN-R restriction proves ANS parity on 5 pairs; trial-space leg load-bearing, not admission; 15-row inventory; U as documented restricted form. 3/3 byte-identical.
- C414: GEN-CYCLES PASS C1-C8. Sequences + learned halting solves the C403 fixpoint (ANS=1005 TRIES=23); seqmax=2 byte-identical to U; 5 pairs + GEN batteries regress clean; cycles join the general envelope via one principle. 3/3 byte-identical.
- C417: COGOPS-COMPOSE COMPOSITION DEMONSTRATED K1-K6. Two learner-owned procedures composed learner-driven; per-goal order [R,V]/[V,R]; version selection from coverage; plans persisted/reused; 10/10 agreement; 3/3 byte-identical.
- C418: COMPRESSION-AUDIT. 13 mechanisms surveyed; top candidate unified learned-contracts GEN+LCONT+FC with a prereg-ready CONTRACT-UNIFICATION test; honest non-compressions listed (LM/NT/INQ/DCE/BP); SEM to retire; chain family flagged.
- C420: CYCLES-GENERALIZE PASS G1-G9. Sequences+halting general, not fitted: alternating 5-hop chain ANS=3006; data-dependent halt operative ANS=4002; HALT-kind signal additive ANS=5002; C403 regression clean. 3/3 byte-identical.
- C422: COGOPS-3WAY THREE-WAY COMPOSITION DEMONSTRATED K1-K9. 3 learner-owned procedures; 3 forced orders [RVC]/[CRV]/[VRC] from identical bindings; version selection; re-derivation byte-identical; 12/12 agreement; 1.92x efficiency; 3/3 byte-identical.
- C424: CONTRACT-UNIFICATION SUBSUMES. One 5-op module (induct/check/grow/invalidate/revise) unifies GEN+LCONT+FC; 7 bars PASS; F1/F2/F3 silent; drift latch q=3 9/9; grammar 6/6 exact; zero scenario branches; 3/3 byte-identical.
- C425: CYCLES-OSCILLATORY PASS O1-O9. Frozen sequences+halting handles period-2 (ANS=6001), lasso (ANS=6003), period-3 (ANS=6001) with zero mechanism change; fixpoint halt never misfires; detection gap characterized, not patched. 3/3 byte-identical.
- C428: CYCLES-CONVERGENT PASS. Convergent-signal family closed: QC1 ANS=7004, QC2 ANS=7106 exact-length, QC3 ANS=7204 limit-distinguished; exact-length matching; halt is exact-equality-specific; threshold-halt characterized. 3/3 byte-identical.
- C429: GEN-REDIM PASS exploratory C1-C11. Dynamic NM-parameterized arena; S1 ANS=2, S2 ANS=219, S4 clean decline; nm<=4 batteries byte-identical to frozen. PROCESS-FAIL from a self-disclosed python3 keystroke (zero-computation), so EXPLORATORY pending clean reproduction.
- C430: CYCLES-FEEDBACK INFORMATIVE-FAIL. F3 prereg TRIES=44 was arithmetic miscalculation vs actual 28; winner [0,1,0,1] k=4 exact; F4 QF2 ANS=8001, F5 QF3 ANS=8102 PASS; mechanism vindicated with zero change; cycle map closed. 3/3 byte-identical. The INFORMATIVE-FAIL is a prereg defect, not a mechanism failure, and stands unaltered.
- C432: CYCLES-FEEDBACK-REFIX PASS. Fresh prereg corrects TRIES=28; frozen binary re-run 3/3 byte-identical; digest matches C430; C430 INFORMATIVE-FAIL stands unaltered; feedback family closed clean.
- C433: COGOPS-DIAMOND DIAMOND COMPOSITION DEMONSTRATED K1-K6. 3 diamond goals (divergent, convergent, world-B) from the same bindings; generic multi-source fan-in, not a handler; chain regression clean; 6/6 agreement 1.77x; 3/3 byte-identical.
- C434: GEN-REDIM-CLEAN CLEAN-REPRODUCTION-PASS. Untainted worker re-ran build.sh from frozen prereg plus committed sources; C1-C11 all PASS; all digests match REPORT.md; C429 PROMOTED from EXPLORATORY to canonical; 5/10+ unblocked.

Adjacent ledger context used in this synthesis: C366 L2-EXTEND-XDOMAIN BUILD-PASS, C367 L2-SPECIALIZE-XDOMAIN BUILD-PASS, C377 (second assignment) L2-IFACE-XDOMAIN BUILD-PASS, C378 (second assignment) L2-COMBINE-XDOMAIN BUILD-PASS, C382 XDTRUNC-1 PASS, C384 XXHIER-TRANSFER PASS, C387 SUBST-1 PASS, C388 ADAPT-1 BOUND, C390 EXTEND-1 BOUND, C392 SPEC-1 PASS, C399 (first assignment) LCONT-1 BUILD-PASS, C426 META-DISTRACTOR interference demonstrated.

---

## 4. The gaps: what is NOT yet covered

Honest accounting. None of the following have a ledgered composition PASS.

1. **COGOPS vs contract-module subsumption.** The single open architectural question inside composition. No experiment has tested whether the unified contract module can reproduce C417/C422/C433 (per-goal ordering, version selection from coverage, trial-learned bindings, topo assembly over procedure bodies), or whether procedure-body composition genuinely needs distinct machinery. The C418 compression audit predates the COGOPS results, so the audit's "chain family flagged" conclusion does not cover this lane.

2. **L3 novel intermediate in composition.** The three-level battery (commits `4c15fe32d`/`f72e501f1`) found Level 3 FAIL: the composer only composes existing MAPs and cannot create a missing bridge structure. HIER-INVENT is BOUND at C395 (no single-shot invention, L2-only). L3-INR was sealed-KILLED and reclassified L2+ (C409 first assignment). Nothing in composition has demonstrated a learner-invented intermediate structure that then participates in composition.

3. **Composite revision after counterexample.** The original composition criteria (Micah, 2026-10-02) require revision and reuse of composites. No ledger entry demonstrates a composite revised by the learner after contradictory evidence and then reused in revised form. The C424 contract module has a `revise` operation for contracts, but its application to composed structures is untested.

4. **Oracle-free composition.** The strong sealed composition battery (`a9fa821f3`/`bda6cb426`) still supplied the target output for verification; that was recorded as an honest bound. IVWC-EXPAND (C379 second assignment) demonstrated multi-step internal verification via world consequences but honestly falsified its own preregistered safety proof (bump-drift). End-to-end composition where the learner proposes, verifies, and adopts a composite with no expected answer supplied is open.

5. **L2 extension and interface-adaptation bounds.** Mixed evidence that must be resolved honestly:
   - EXTEND: L2-EXTEND-XDOMAIN (C366) BUILD-PASS with learner-chosen k=4, yet EXTEND-1 (C390) is BOUND: frozen executor is flat, cannot build on Z2, protected-core change stated as needed.
   - ADAPT: L2-IFACE-XDOMAIN (C377 second assignment) BUILD-PASS with a learner-derived zero-rel adapter, yet ADAPT-1 (C388) is BOUND: no interface-adaptation operator, coarse type discipline only.
   Truncate, substitute, specialize, and cross-domain combine have clean BUILD-PASS evidence (C380 second assignment, C382, C387, C392, C367, C378 second assignment, C374, C384). The two BOUND entries may mark genuine principled limits or under-explored operator space; they have not been reconciled experimentally.

6. **Domain-blindness under the current mechanism.** C398/C399/C409/C403 blind tests were run against U-era composition. The unified contract module (C424) and COGOPS composition have not been re-verified under identifier relabeling. The overnight architectural clarification makes this a standing requirement: dependence on human domain identity is architectural failure, so the blind battery must follow each mechanism change.

7. **Composite scaling.** GEN-STRESS (C410 second assignment) found the 5+ structure wall; GEN-REDIM (C429/C434) unblocked 5/10+ in the arena. But composition at scale in the MAP-count dimension, and composite interaction cost as structure count grows, remain unmeasured. The 5000-MAP operand-encoding fix is canonical elsewhere; composition has no equivalent scaling demonstration.

8. **Cycle x composition interaction.** Cycles are handled inside GEN via re-application with learned halting, and feedback composition is closed (C432). Not tested: composition of components that are themselves cyclical (feedback loops inside composite legs), and COGOPS procedures with cyclical bodies composed over diamond or chain shapes.

9. **Composite interference and negative transfer.** C426 demonstrated distractor interference (Option C, ADV_R=-680, ~76/ep slower). Stored composites have not been tested for mutual interference, retention under unrelated learning, or revision contagion across composites. This is the lifetime dimension of composition and is untouched.

10. **Multi-input/multi-output and arity-general composition.** Fan-in is demonstrated (C402, C433), but arity-general contracts (structures with multiple typed inputs and outputs composed through several legs at once) and partial applicability beyond the endpoint check (C396 second assignment: "tax not failure") have thin coverage.

---

## 5. Prioritized next frontiers

Ordered by architectural information gain, per Micah's standing rule.

**P0. Subsumption test: contract module vs COGOPS composition.** Design a preregistered battery in which the unified contract module must reproduce C417/C422/C433 behaviors (per-goal ordering, version selection, trial-learned bindings, diamond over procedure bodies), or document exactly which capability resists subsumption and why. This is the experiment that decides "one mechanism or two." It is the highest-value composition experiment available.

**P1. Composite revision.** Freeze a composite, introduce contradictory evidence on one leg, and test whether the learner revises the composite (not just a single contract), re-verifies, and reuses the revised form. Required by the original composition criteria; currently at zero ledgered evidence.

**P2. Oracle-free composition.** Compose to a sealed goal with no expected answer supplied at any stage; learner proposes, evaluates via world consequence or internal verification, and adopts or rejects. Extends the IVWC direction with an unfalsified verification story.

**P3. Reconcile the L2 BOUND entries.** Run preregistered adversarial tests on C388 (interface adaptation) and C390 (extension): either demonstrate learner-owned operators that dissolve the bounds, or confirm they are genuine principled limits requiring protected-core change (which would be a governance decision for Micah, not a worker decision).

**P4. Composite scaling.** 5/10+ structure composition now that GEN-REDIM is canonical (C434); measure interaction cost and correctness as structure count and MAP count grow. Connect to the canonical 5000-MAP operand-encoding fix.

**P5. Domain-blindness re-verification.** Re-run the C398/C399/C409 battery against the contract module and COGOPS composition. Standing requirement after every mechanism change.

**P6. L3 bridge invention in composition.** The main AGI-architecture target: a sealed battery where the goal is unreachable from existing structures and the learner must invent the missing intermediate, then compose with it. Level 3 battery FAIL is the baseline to beat; C395 BOUND is the bound to break.

**P7. Cyclical components and feedback-rich composites.** Compose structures with internal feedback loops; test halting and termination behavior of composites whose legs are cyclical.

**P8. Composite lifetime behavior.** Interference between stored composites, retention under unrelated learning, revision contagion. The C426 interference map (A=TRANSFER, B=UNDECIDED, C=INTERFERENCE) is the starting vocabulary.

---

## 6. Assessment: one mechanism or several?

For **learned-structure composition** (MAPs, contracts, value graphs): one mechanism. The evidence is a clean reduction chain: A/B/C collapsed into U (C319, reproduced C325); U subsumed by GEN (C397 partial, C406 upgrade with explicit retirement recommendation); U retired as a separate mechanism (C413); GEN+LCONT+FC unified into the 5-op contract module (C424, SUBSUMES, zero scenario branches). GEN's generalizations (diamond C380, fan-in/DAG-4/chain-3/partial C402, cycles C414/C420/C425/C428/C430/C432, redimensioning C429/C434) all landed without new mechanisms, modes, bridges, or handlers. This is the strongest architectural-compression result in the composition program, and it satisfies Micah's directive that the diamond failure trigger general hypotheses rather than a diamond handler.

For **procedure-body composition** (COGOPS): unresolved. C417/C422/C433 are genuine composition demonstrations over learner-owned procedure bodies with per-goal ordering and version selection, and they postdate every subsumption analysis on record. Nothing in the ledger shows the contract module reproducing these behaviors, and nothing shows they are impossible for it either. The honest position is that composition currently has one proven general mechanism plus one candidate second mechanism awaiting the P0 subsumption test.

For **L2 adaptive reuse**: the operators are demonstrated but scattered across lanes (truncate C380/C382/C392, substitute C387, specialize C367/C392, combine C378, extend C366, interface-adapt C377) with two principled-limit BOUND entries (C388, C390) unresolved. Whether these collapse into one adaptive-reuse operation is the L2 analogue of the P0 question and has not been run.

For **L3 invention**: no mechanism exists yet. This is not a composition-specific failure; it is the standing frontier.

Net: composition is closer to one mechanism than at any prior point, with exactly one well-defined experiment (P0) standing between the current state and a justified "one general composition mechanism" claim for the full envelope.

---

## 7. Caveats and ledger hygiene

- Duplicate ledger numbers from concurrent watchdogs are listed with both assignments in section 3. Any downstream citation should use name plus number.
- C429 was PROCESS-FAIL (python3 keystroke, zero-computation) and EXPLORATORY until C434's clean reproduction promoted it to canonical. Citations of GEN-REDIM before C434 should carry the exploratory label.
- C430's INFORMATIVE-FAIL is a prereg arithmetic defect (TRIES=44 vs 28), not a mechanism failure; the mechanism was vindicated with zero change, and C432's refix closed the family cleanly.
- The C410 GEN-STRESS boundary (5+ structures, silent corruption at nm=5-7, panic at nm=8) is superseded in effect by C429/C434 but remains the honest record of the frozen pre-redimensioning build.
- Canonical GEN base (DEFECT-AUDIT C447, recommendations 1-2): the frozen pre-redimensioning GEN base is superseded for all work registering more than 4 MAPs; GEN-REDIM (C434) is the canonical GEN base. Citation rule: 6/8-structure GEN composition behavior must be cited from GEN-REDIM (C434: S1 ANS=2 TRIES=29, S2 ANS=219 TRIES=43, S4 ANS=-2 TRIES=48 clean decline), never from the GEN-STRESS K2/K3/K5 corrupted runs. The corrupted outputs remain valuable only as the defect's empirical signature.
- Red-team status: U's collapse was independently reproduced (C325); the contract module and COGOPS lanes carry 3/3 byte-identical determinism but no ledgered independent red-team attack yet. The P0 subsumption battery should include an adversarial arm.
- Note for the parent: the task brief described COGOPS diamond as "in progress" and C429 as "exploratory." Both advanced during this window: C433 demonstrated COGOPS diamond (K1-K6), and C434 promoted C429 to canonical. This synthesis reflects the updated ledger.
