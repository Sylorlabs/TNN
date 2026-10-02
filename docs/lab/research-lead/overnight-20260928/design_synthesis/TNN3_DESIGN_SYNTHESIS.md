# TNN-3 Design Synthesis

**Status: DRAFT synthesis. Collects committed guidance; invents nothing.** This document ties together six committed inputs (floor, treadmill guard, SUF implications, bar priority, roadmap-with-bars, bug report) into one reading order. It creates no new bars, modifies none, proposes no mechanisms, fixes no bugs, and makes no banked decision. All source documents remain DRAFT-NOT-FROZEN; this synthesis governs nothing until a TNN-3 preregistration frozen by Micah references the sources it summarizes.

Inputs: SUF implications `b1835dec6`; treadmill guard `1646b9732`; floor spec `f383dd11c`; bar priority `20d810d4b`; roadmap with bars (swept into `bbe79ddf1`); revision bug report `8b58c4104`. Supporting: SUF property definition `64eec921f`, SUF check `8ef148a42`, re-clustering `ed2357141`, GW eval `881fbb3d4`, boundary map `8d763d766`.

The honest line this synthesis serves: TNN-2 is "fixed templates with variable content," a real L2 advance, but the envelope is unchanged in kind. The three targeted changes moved zero worlds. Ledger: 159 claims, zero new SURVIVES, L3 zero.

---

## 1. What TNN-3 must preserve: the floor (7 capabilities)

From the floor spec (`f383dd11c`). These are regression tests, not L3 bars. TNN-3 may add mechanisms, but all seven must pass at their transcribed thresholds before any new-capability claim is evaluated. Run the floor battery first, under the freeze protocol (fresh learner state, three deterministic runs, byte-identical transcripts).

**Freeze floor (from the 4/9 pass set, byte-identical TNN-1/TNN-2):**

- **F1. Associative recall (FW1, FW2).** Taught facts returned on exact query, with retention after intervening unrelated teaching. Thresholds: FW1 10/12 probes, 7/10 retention minimum (TNN-2: 12/12, 10/10); FW2 7/8 minimum (TNN-2: 8/8). Breaking: recall below TNN-1 bars or retention degradation.
- **F2. Law change and revert (FW4).** Contradicted regularity updates; revert restores the original; no stale answers. Threshold: 12/12 on all three probe groups (both generations). Breaking: stale answers or partial propagation. Note: covers only the fact-level path; GW8 showed MAP-level revert fails. That is a gap, not the floor.
- **F3. Targeted update without collateral damage (FW5).** Contradiction updates the intended key; neighbors intact. Thresholds: 10/10, 3/3, 9/9 (identical both generations). Breaking: update bleeds into neighboring keys.

**GW floor (from the three adversarial-battery positives, `881fbb3d4`):**

- **G1. Construction over learner-taught facts (GW3 phase 2).** Level-2 chain traverses the level-1 taught answer fact as a first-class edge; probes 300 correctly. 3/3 byte-identical runs. Breaking: level-2 probe misses, meaning construction can no longer consume learned state as edges. Boundary: phases 3-4 (revision with dependents, retirement) are gaps, not floor.
- **G2. Single-level value revision through the query path (GW7 probe 5).** One 100-to-200 contradiction probes 200, with no dependent MAPs at contradiction time. Breaking: stale 100 in the no-dependent configuration. TNN-3 must keep the no-dependent case while fixing the dependent case.
- **G3. Inquiry discrimination and re-fire (GW6 primary, GW7).** Taught key answers with `CHOICE 0`; untaught key misses (-2) with `CHOICE 30`; fresh-key ignorance re-fires `CHOICE 30`. Threshold: 7/7 primary probes, 3/3 identical runs. This is discrimination, not contingency: FW6's variable-act requirement remains failed and is not part of the floor.

**Explicitly NOT the floor:** FW3, FW7, FW8, FW9; FW6 contingent inquiry; GW6 retirement; GW8 rev2/revert; GW3 phases 3-4; GW4; GW5; the GW1 depth ceiling; the GW2 DAG-only bound. Preserving a failure mode is the treadmill.

**Breaking criteria (floor spec section 5):**
1. Any of F1-F3 drops below its transcribed freeze threshold.
2. Any of G1-G3 fails its transcribed GW probe sequence.
3. Any floor test stops being deterministic across three runs.
4. **Anti-gaming clause:** a previously passing floor test passes only with a researcher-supplied crutch not needed for TNN-2 (extra teaching, manual state resets, relaxed determinism). If TNN-3 needs more scaffolding than TNN-2 to pass the same seven tests, that is a regression in learner autonomy even if scores match.

---

## 2. What TNN-3 must avoid: the treadmill

From the treadmill guard (`1646b9732`).

**Definition.** The treadmill is the development pattern in which each frozen-core failure is met by adding researcher-authored machinery (new operators, wider menus, more templates, benchmark-specific handlers) that raises the score on the failing world without changing the property that caused the failure. Score goes up; envelope unchanged in kind. Canonical instance: TNN-2. TNN-1 froze at 4/9; the gap analysis identified three missing capabilities; TNN-2 implemented them; the reconciled result was byte-identical pass/fail at the world level with zero clusters moved. The diagnosis ("TNN-1 fails for lack of X; TNN-2 adds X") was falsified for all three X because the mechanisms satisfied capability names while violating the required property. Zero movement with zero regressions is the signature of orthogonality, not incompleteness.

Related failure modes that count as treadmill even with flat scores: **scaffolding inflation** (floor tests pass only with more researcher help; floor spec criterion 4); **failure-mode preservation** (constant act relabeled as "inquiry," acceptance-without-verification as "verification," the floor presented as the ceiling).

**Warning signs (any one is a warning; two or more is a strong presumption):**
1. The menu grows (more templates, operators, fixed families; a larger finite menu is still a finite menu).
2. Capability names satisfied, property absent (described as "construction" but template instantiation; "inquiry" but a constant act; "revision" but a literal patch).
3. World-specific fixes with no general mechanism named.
4. Scaffolding inflation.
5. H1 widening before H2 (a larger menu under the same oracle).
6. Preserved failure modes renamed.
7. Source-enumerable outputs (SUF operational test returns an empty list; treadmill by definition regardless of score).
8. Score up, property flat (freeze score improves but SUF still fails and no kill bar newly passes).

**The five guard checks.** Run on every proposed TNN-3 change before adoption. Failing check 1 or 2 rejects the change; failing 3, 4, or 5 returns it for redesign with the failure named.
1. **SUF check (primary).** List every structural decision the learner can make that the source cannot. Empty list: the mechanism cannot move any cluster. Treadmill by definition. No score movement overrides this.
2. **Anti-gaming check.** Run the seven floor tests with no more scaffolding than TNN-2 needed. Any crutch TNN-2 did not need is a learner-autonomy regression.
3. **Generality check.** Name every world the change should move and the shared architectural cause (re-clustering cause clusters R1/R2/R3 plus the C0-D shadow). A one-world fix must name its general mechanism or be rejected.
4. **Property check.** State the property added, mapped to the target cluster's SUF sub-property (FW3 history-parameterized generativity, FW6 epistemic-state-contingent discrimination with resolution transition, FW7 goal-conditioned composition, FW8 combinatorial novelty, FW9 learner-scaled search). Capability-only preregs are underdetermined and treadmill-risky.
5. **Menu check.** Count researcher-enumerated schema families before and after. A real advance moves schema decisions into learner state; it does not grow the menu.

The guard also documents per-capability treadmill forms for all seven floor capabilities (what scaffolding inflation and world-specific cheating look like for each, and which check catches them) and three ways to game the guard itself (SUF theater, vague property statements, floor-only optimization), named so they can be watched for.

---

## 3. What TNN-3 must achieve: SUF-PASS per mechanism

From the SUF property definition (`64eec921f`), the SUF check (`8ef148a42`), and the SUF implications (`b1835dec6`).

**The property.** Source-Underdetermined Form (SUF): the structural form of a mechanism's outputs cannot be enumerated from the source code alone; at least one structural decision in the production path is genuinely resolved by learner history. Formal: for source S, histories H, Forms(S,H) the producible structural schemas, SUF holds iff for every enumeration E taking only S, there exists a reachable H and a form f in Forms(S,H) not listed by E.

**Why it is the entrance gate.** The SUF check ran the 4-step operational test on frozen TNN-2: all three mechanisms SUF-FAIL with an empty (b) list (source-underdetermined structural decisions). Construction: 10 decisions, all class (a). Inquiry: 6 decisions, all (a); TNN-1's constant was 0, TNN-2's is 30, a different constant, not contingency. Revision: 6 decisions, all (a); 19 RESEARCHER decisions, zero MIXED. The DOF map's 5 MIXED decisions all map to class (a): value selection within source-fixed spaces. There are zero production write paths from learner state to any structural decision. Contrapositive as design law: cluster movement requires producing a form outside the source-enumerable set, so any fix keeping the (b) list empty cannot move any cluster. SUF is necessary, not sufficient: the sufficiency stack is SUF AND utility (world-pass bars) AND learner-internal verification (K-H2) AND revisability (K-H3) AND cognitive reuse (K-REUSE-1/2).

**The zero-to-one recipe (cross-cutting).** The minimal change is zero-to-one, not N-to-N+1: (1) select one source-fixed structural decision on the mechanism's production path (SUF check Step 1 tables: 10 for construction, 6 for inquiry, 6 for revision); (2) route it through learner state with an exercised write path (dead code does not count); (3) keep the value space non-source-enumerable (learner-composed via the frozen generic ISA, not a finite menu; a policy choosing among 3 source-listed orders is still (a)); (4) preregister the Step 4 negative control (the source-only enumeration E) before implementing; (5) respect sequencing (H2 before H1 widening; reuse path in parallel so new (b) entries are query-visible, not C0-D shadowed).

**Per-mechanism (b) candidates (cheapest first):**

- **Construction** (clusters FW3, FW7, FW8, FW9; bars K-T3-CON-1/2, K-T3-TOPO; future K-COMP-OP). (C-b) search bound from a learner-state resource node (FW9: replaces the 900 literal and depth-4 ceiling literal); (C-c) assembly phase order from an H3-lite policy node (Step 4 control decides whether the policy's value space is genuinely open). Cheapest pair. Genuine widening: (C-a) assembler wiring from learner-composed fragments via generic ISA ops (H1, H2-gated; FW8 combinatorial novelty, FW3 generativity); (C-d) acceptance criterion from learner state, not oracle `expected` (K-H2-3, H2-gated). Explicit non-moves: a fourth assembler family, k extended to 5, budget 900 raised to 1800. Future: (C-e) learner-originated operators (K-COMP-OP).
- **Inquiry** (cluster FW6; bars K-T3-INQ-1..4; future K-INQ-INFO). (I-a) act indexed by a learner-maintained uncertainty representation with a resolution transition (the FW6 sub-property; currently no resolution transition exists at all; any new constant is still (a)). Alternatives: (I-b) guide structure composed from learner history; (I-c) learner-owned stopping criterion (K-H2-3). Caveat: structural effect may need the banked protected-core structural-ops decision, which belongs to Micah and is not made here.
- **Revision** (R3 ceiling; bars K-T3-REV-1/2/3, K-TSEL-1/2, K-H3). (R-b) target selection from a learner-state policy (K-TSEL-1/2, the fourth H3-lite site; cheapest). Real widening: (R-a) repair proposal generated from learner state (roadmap step 3); (R-c) history-contingent post-repair sequence. Full (R-a) with novel repair topologies likely needs the banked structural-ops decision.

**Do-not-do list:** capability-shaped additions that keep (b) empty; widening before H2; mistaking the 5 MIXED DOF decisions for (b) entries (all map to (a)); treating H3-lite parameterization as SUF-PASS before the Step 4 control rules; preserving failure modes as floor.

---

## 4. The order to do it in: bar priority

From the bar priority (`20d810d4b`) and the roadmap with bars (in `bbe79ddf1`). 24 bars total, all DRAFT-NOT-FROZEN: 21 minimal TNN-3, 2 future-generation, 1 audit-grade.

**Phase 0 (process precondition, first).** K-T3-ADV (adversarial process): the fail-closed precondition for every sealed-world bar. Nothing sealed until the adversary protocol is in place.

**Phase 1 (diagnostics, runnable now against frozen TNN-2, all parallel).** K-H2-1, K-H2-2, K-H2-3, K-H2-4 (mutually independent checks on the same trap battery) plus K-STATE-RET as audit probe (diagnostic infrastructure, predicted TNN-2 FAIL). All five start immediately. Phase 1 is also the treadmill guard: H2 results must be recorded before Phase 4 begins.

**Phase 2 (two parallel build tracks, independent of each other).** Track A: K-REUSE-1, K-REUSE-2 (reuse path; the enabler for K-TSEL-1/2, K-T3-CON-2, K-T3-INQ-4). Track B: K-H3 (the minimal TNN-3 core; three policy nodes with parallel sub-tests; the prerequisite for every Phase 3 bar).

**Phase 3 (mechanism completion, requires Track B).** Three parallel groups: (K-T3-INQ-1, K-T3-INQ-3) on the revisable guide policy; (K-T3-REV-1/2/3) on the repair-proposal generator; (K-T3-INQ-2) on guide policy plus the inquiry resolution path.

**Phase 4 (H1 widening; requires Phase 1 results recorded AND Phase 2).** K-T3-CON-1 (open constructor; H2 gate applies); K-TSEL-1/2 (need Track A signals plus the H2 gate); K-T3-TOPO (audits diversity sets; rides with CON-1 and REV-1); K-T3-CON-2 and K-T3-INQ-4 (need Track A).

**Integration (PX, parallel with Phase 3 and Phase 4).** K-XMECH (cross-mechanism interference; include its worlds in the K-T3-ADV battery from the start).

**Critical path:** K-T3-ADV → K-H3 → Phase 3 mechanism bars → K-TSEL-1/2. The H2 probes and reuse path are off the critical path (parallel, with gate roles only).

**Future bars (explicit non-claims for minimal TNN-3):** K-COMP-OP triggers when a future generation claims learner-originated composition operators (preconditions: K-REUSE-1 and K-TSEL-1/2 pass first). K-INQ-INFO triggers when a future generation implements an informativeness criterion (preconditions: K-H3 passes and the Step 3 inquiry resolution path exists).

**Audit bar:** K-STATE-RET runs as a governance audit probe alongside every sealed evaluation battery, not as a generation-gating kill bar. No dependencies; establish the baseline against frozen TNN-2 now (predicted FAIL).

---

## 5. The bugs to avoid: revision corruption

From the bug report (`8b58c4104`), sourced from the boundary map (`8d763d766`, Surprise 1, probe pE E4). TNN-2 is frozen; the bug is part of the evaluated artifact. TNN-3 must avoid it.

**What happens.** A failed interior revision permanently corrupts the promoted graph. `t2_revise_graph` patches an interior SETREG; verification re-execution correctly fails (-999999); the REVERT path runs but is corrupt. The graph fails every future execution while `ev_query` keeps answering the stale value, because queries hit the promoted fact directly and never re-execute the graph. White-box state and answers diverge silently.

**Why.** Frame-allocation alias: the verifier's `t2_exec` allocates its execution frame via `alloc_node`, which returns the just-tombstoned stale node; `fr_set` overwrites its fields (f4=0, f8=0, f20=frame garbage). The revert restores only node type and live-flag, not f4/f8/f20. The corrupted SETREG fails the execute guard forever.

**Impact.** Irreversible (one-shot per fact lineage, per Surprise 2, so the damage can never be repaired through revision); silent (`standing` tracks DEP/CON edge balance, not correctness, and does not catch this); worse than no revision (an un-revised graph at least executed correctly to its stale answer); blocks multi-step belief correction in any TNN-3 design that revises graphs in place.

**Required fix (TNN-3 only).** Any of: (1) atomic revision (recommended): reserve the execution frame before tombstoning, or verify against a snapshot copy and swap only on success; (2) full field snapshot/restore: snapshot ALL node fields before patching and restore the full set on revert (type-plus-live-flag-only is the direct cause); (3) separate the free pools: revision-epoch tags on tombstoned nodes, respected by the allocator. Plus a regression test: contradict an interior fact, force failed verification, assert the graph re-executes to its pre-revision answer and a white-box field dump matches the pre-revision snapshot byte-for-byte.

**Compounding, not this bug:** Surprise 2 (one-shot revision: the second contradiction on the same (s,r) never reaches the graph because the first revision forked the fact lineage) is architectural, not a memory bug, but it means the corruption damage can never be repaired through the revision path. E5 (contradicting the promoted fact itself teaches a shadowing fact by recency without revising any graph) is silent divergence via a different route.

---

## 6. Reading order and open items

**Reading order for the full guidance:** (1) floor spec section 3 first (know what is NOT the floor, so failure modes are not preserved); (2) treadmill guard sections 1-2 (recognize the pattern TNN-2 instantiated); (3) SUF implications sections 1-2 (the formal reason zero worlds moved, and the zero-to-one recipe); (4) SUF implications section 3 (per-mechanism (b) candidates, cheapest first); (5) bar priority (the phase order, gates, and critical path); (6) roadmap with bars (roadmap phase to bar mapping, unchanged recommendations); (7) bug report (the one concrete bug that must not be reintroduced).

**Open items for preregistration (not decisions):** the exact Step 4 enumeration E per mechanism (frozen pre-implementation); whether H3-lite policies clear Step 4; the banked protected-core structural-ops decision (Micah only; Alternative C recommended, H3-lite only and defer; Alternatives A/B/C NOT DECIDED); K-STATE-RET placement; the six banked kill-bar open questions; the floor battery's placement as a regression precondition.

**What governs.** This synthesis invents nothing and freezes nothing. The five guard checks, the seven floor thresholds, the per-mechanism (b) candidates, the phase order, and the bug-avoidance requirements govern TNN-3 work only if a frozen preregistration reviewed by Micah references them. Until then, all remains DRAFT.
