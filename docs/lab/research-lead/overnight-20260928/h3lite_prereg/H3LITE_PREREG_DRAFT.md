# H3-Lite Preregistration: DRAFT-NOT-FROZEN

Date drafted: 2026-10-01.
Status: **DRAFT-NOT-FROZEN.** This draft has not been reviewed or frozen. It must not govern any implementation or evaluation until Micah gives an explicit separate freeze go. The preregistration's first freeze commit must strictly precede any implementation.

Design source: `tnn2_h3lite/H3LITE_DESIGN.md` (commit `22197da2c`), read-only.
Boundary: protected-core Alternative C (commit `092566072`), chosen by Micah 2026-10-01.
Ruling: Micah 2026-10-01, H3-lite section.

---

## 1. Diagnostic purpose

H3-lite tests one causal question before the protected core is expanded:

**Does moving researcher-fixed structural decision criteria into learner-writable state produce meaningful causal improvement in revisability, before paying for structural graph-mutation opcodes?**

The three TNN-2 mechanisms (runtime executable-graph construction, learner-originated uncertainty to guide to action, counterexample-driven revision) each contain decision points that are currently source literals or straight-line researcher code. H3-lite parameterizes exactly those decision points as reads from learner-state policy nodes, and adds one production write path per node from experience. The procedures stay researcher-authored Zag code. The locus of control moves; the envelope of forms does not.

If H3-lite delivers policy revisability but procedures remain unrevisable in ways that block further progress, the banked structural question (Alternative B: ALLOC, field WRITE, LINK, KILL in learner-executable ISA) returns with more evidence. If H3-lite shows no causal improvement from learner-writable criteria, that is informative against the "criteria ownership is the disease" hypothesis and the program must look elsewhere.

---

## 2. Alternative C boundary (frozen for this experiment)

- Structural graph-mutation opcodes are **DEFERRED**, not decided. No ALLOC, field WRITE, LINK, KILL, or tombstoning operations are added to the learner-executable ISA in this experiment.
- The protected core ISA remains exactly as ruled: the small frozen domain-neutral basis. No benchmark-driven growth.
- Alternative A (permanent prohibition of structural mutation) is **rejected** by Micah. Alternative D (second graph type) remains **rejected** under the One-System Rule. Alternative B remains **banked behind evidence**: it may be revisited only if H3-lite results demonstrate that decision-level revisability is insufficient and procedure-level learner authorship is the blocking factor.
- All policy-node writes in this experiment use field writes and edge link/kill operations that the frozen TNN-2 source already performs. No new opcode, mode, bridge, or handler is introduced. This is verified by the architecture accounting in section 8.

---

## 3. The three policy nodes

All three use the proposed tag 40 (T_POLICY, unused in frozen TNN-2 source). Bootstrap for all three is copy-then-revise: on first use the node is created with the researcher's current defaults copied in. The learner revises a copy; it does not invent the initial policy.

### Node 1: Trial search order policy (construction)

**Decision moved to learner state:** the order in which `t2_trial` attempts assembler families (currently source literals: chains k=4,3,2, then sum, then count, then single hop).

**Learner-state fields (tag 40, subtype field 4 = 1):**
- Fields 8, 12, 16, 20, 24, 28: six order slots holding family ids in preference order (0 = chain k=2, 1 = chain k=3, 2 = chain k=4, 3 = sum, 4 = count, 5 = single hop). Initialized to 2,1,0,3,4,5 (researcher's current literal order).
- Field 32: first-choice rejection count (saturating). Per-family attempt counts reuse the existing header field 16 trial stats.

**Production read path:** the `t2_trial` loop nest becomes a dispatch loop over the six order slots. Per-family assembly code (`t2_asm_chain`, `t2_asm_sum`, `t2_asm_count`, single-hop) is unchanged; only invocation order is policy-driven.

**Production write path:** in `t2_try_verify`, on verification success for family F at position p > 0, swap F one step earlier (Hebbian promotion). On trial exhausting all families without success, increment field 32; when field 32 exceeds 8 (researcher-chosen threshold, documented), demote the first-choice family one step and reset field 32.

**Triggering experience:** verification success or failure outcomes of trial families during ordinary world interaction.

**Discrimination test:** sealed world where chains-before-counts systematically picks the wrong family first (all answers are counts, chains always fail verification). H3-lite prediction: order flips to counts-first within the demotion threshold. Frozen TNN-2 prediction: order never changes.

### Node 2: Guide template policy (inquiry)

**Decision moved to learner state:** the default action and content written into every guide node by `miss_inquire` (currently literals: action 30, content -999).

**Learner-state fields (tag 40, subtype field 4 = 2):**
- Field 20: default action (initialized to 30).
- Field 24: default content (initialized to -999).
- Field 28: resolution count.
- Field 32: miss count.
- History: ET_REF edges to the three most recent resolved uncertainty nodes (fixed three-slot bound, researcher-chosen).

**Production read path:** `miss_inquire` guide creation reads action/content from the template policy fields instead of literals.

**Production write path:** new `resolve_uncertainty`, called from `ev_observe`: when an observation matches an open uncertainty (s,r), supersede the uncertainty and its guide via the existing type-3 self-edge convention, increment field 28, record the resolving action in history. If the most recent three resolutions all followed action A where A differs from the current default, set field 20 = A (majority-of-three rule, researcher-authored heuristic operating on learner-state history).

**Triggering experience:** observations that resolve open uncertainties during ordinary world interaction.

**Discrimination test:** two-phase sealed test. Phase 1: misses on relation R1 with resolutions; phase 2: misses on relation R2 where the world reveals answers only after a different action. H3-lite prediction: template default shifts if phase-1 resolutions consistently followed a non-30 action. Frozen TNN-2 prediction: action is 30 forever. (Test design is adversary work; the frozen worlds may not supply differential action feedback.)

**Known limit (stated, not hidden):** this makes guide content revisable; it does not make guides discriminating. The informativeness criterion is not implemented. A revisable constant action is still a constant action until experience changes it.

### Node 3: Repair dispatcher policy (revision)

**Decision moved to learner state:** which repair topology `t2_revise_graph` attempts (currently straight-line literal-patch code only).

**Learner-state fields (tag 40, subtype field 4 = 3):**
- Field 20: preferred topology id 0-5 (initialized to 5, literal-patch, the current behavior).
- Fields 24, 28, 32: packed success counters for topologies 0-5 (two 16-bit halves per field, saturating at 65535).

**The six researcher-enumerated topologies (H1 unaddressed; the family is fixed):**
- 0: guard-predicate edit. 1: branch rerouting. 2: multi-step coordinated repair. 3: step-count/type conversion. 4: step deletion without insertion. 5: literal-patch (current behavior, default and fallback).

**Production read path:** the body of `t2_revise_graph` becomes a dispatch on field 20. Each topology is researcher-written and preserves the verify-by-reexecution / revert-on-failure contract. On preferred-topology failure, the dispatcher tries remaining topologies in descending success-count order before returning failure.

**Production write path:** on verification success for topology T, increment T's counter. If T differs from the current preference and T's counter exceeds the preference's counter by margin 2 (researcher heuristic), set field 20 = T. On total failure (all tried, all reverted): no counter changes.

**Triggering experience:** contradiction events and their repair verify/revert outcomes during ordinary world interaction.

**Discrimination test:** sealed graphs where literal-patch systematically fails but another topology succeeds (e.g., guard-predicate faults). H3-lite prediction: preference shifts from 5 to the succeeding topology after the margin is exceeded. Frozen TNN-2 prediction: literal-patch attempted every time, failing every time.

---

## 4. K-H3 write-path audit (kill bar, DRAFT-NOT-FROZEN)

K-H3 is adopted from the design draft with Micah's 6-element audit. For **every** structural decision the mechanism makes that is not determined by its immediate input, the frozen preregistration must list all six:

1. **The structural decision** (e.g., "trial search order", "guide default action", "repair topology selection").
2. **The learner-state node and fields storing the decision** (tag, subtype, field numbers).
3. **The production (non-test) code path that reads those fields** (the existing decision point being parameterized).
4. **The production (non-test) code path that writes to those fields** (the new update).
5. **The experience event triggering the write** (must be an ordinary production event, not a test scaffold).
6. **A sealed test demonstrating the decision taking different values after different experience histories** (the decision change must be an outcome of experience, not an input).

A structural decision is any choice among alternatives not dictated by the current input: search orders, default parameters, topology selections, ranking criteria. Pure functions of the input are not structural decisions.

**Failure conditions (any one fails K-H3):**
- (a) A structural decision is implemented as a source literal, loop bound, or straight-line code with no learner-state read. (This is the frozen TNN-2 condition for all three mechanisms.)
- (b) A structural decision is read from learner state but no production code path writes to it. Read-only policy is revisability theater.
- (c) A production write path exists but is unreachable in the sealed evaluation (e.g., gated behind a test-only flag). Write-path theater.
- (d) The demonstration test uses researcher-supplied experience histories that directly encode the expected decision (e.g., teaching the policy node the answer). Histories must be ordinary world interactions; the decision change must be an outcome, not an input.

**Theater rule (Micah): a value stored in learner state with no exercised production write path is theater.** Conditions (b) and (c) exist to enforce this. The audit must show each write path firing on the sealed test transcripts, not merely existing in source.

---

## 5. Explicit non-claims

This experiment does NOT establish, and the preregistration forbids claiming:

1. **Learner-authored procedures.** The procedures (trial loop, guide creation, revision dispatch, all six repair topologies, all assembler families) remain researcher-authored Zag code. Only decision criteria move into learner state. C0-A still fails at the procedure level after H3-lite.
2. **Source-Underdetermined Form (SUF).** H3-lite does not establish SUF by itself. The policy value spaces (six order slots over six fixed families; one default action; six fixed topologies) are enumerable from source. Learner history selects among researcher-enumerated alternatives; it does not create new structural forms.
3. **L3 (representational invention).** Passing K-H3 establishes that mechanism policies are revisable by experience. That is a precondition for procedure-level learning claims, not L3. C0-A/B/C/D are evaluated separately and are not met by this experiment.
4. **Capability improvement on frozen batteries.** No FW1-FW9 score improvement is predicted. H3-lite changes the locus of control; frozen scores measure the researcher-enumerated envelope, which is unchanged in kind.
5. **Inquiry discrimination.** The guide template becomes revisable; guides do not become discriminating. The informativeness criterion is out of scope.
6. **H1 (open construction).** The repair family and assembler family remain researcher-enumerated and fixed. The learner selects among given alternatives; it cannot invent a new family.

---

## 6. Experimental protocol

**Target:** a TNN-3-line build implementing the three policy nodes on the frozen TNN-2 base, built only after this preregistration is frozen (freeze commit strictly precedes implementation).

**Sealed evaluation:** the three discrimination tests in section 3, run against sealed worlds designed by an independent adversary after the freeze. The adversary designs worlds where the researcher's default decision is systematically wrong and a different enumerated alternative is systematically right. Minimum: one sealed world per policy node.

**Predictions (frozen before evaluation):**
- H3-lite build: each policy node's decision value changes across the sealed runs in the direction of the world's feedback (order flips, default action shifts, topology preference moves), with the write paths firing on transcript.
- Control (frozen TNN-2 binary): no decision value changes; source literals hold.

**Determinism:** three byte-identical runs per sealed world, as per the freeze-evaluation convention.

**Kill-bar evaluation order:** K-H3 first (all six elements per node, all four failure conditions checked). If K-H3 fails for any node, that node's claim is dead; the experiment does not proceed to capability interpretation for that node.

**White-box requirement:** per Micah, TNN stays a white-box architecture. Every claimed write-path firing must be traceable in the transcript and node state. If a decision value changed but the write path cannot be shown firing, the change is unexplained and the node fails condition (c).

---

## 7. Standing architectural metric (reporting requirements)

Every H3-lite mechanism report must include these fields, per Micah's standing metric. Benchmark scores must not substitute for them.

- RESEARCHER-OWNED STRUCTURAL DECISIONS: count and list (the three procedures, the six families, the six topologies, all thresholds/margins/bounds, the copy-then-revise bootstrap).
- LEARNER-OWNED STRUCTURAL DECISIONS: count and list (the three policy values while the experiment runs; each must pass the K-H3 audit or be struck).
- SOURCE-ENUMERABLE FORMS: the full enumeration (6! orders, action value space, 6 topologies) stated explicitly.
- SUF DECISIONS: none claimed by this experiment (must read zero; any nonzero claim fails the non-claims).
- LEARNER-INTERNAL CRITERIA: which criteria moved (order preference, default action, topology preference) and the experience that set each.
- REUSE EVENTS: count of policy-node reads serving later decisions (distinguished from first-use initialization reads).
- REVISION EVENTS: count of policy-node writes from experience (each tied to its triggering event).
- COGNITION LINES: lines of mechanism source added/changed vs frozen TNN-2.
- MODES: must be zero new.
- BRIDGES: must be zero new.
- HANDLERS: must be zero new benchmark-specific handlers.
- SEMANTIC CASES: must be zero new.

---

## 8. What freezing this preregistration requires

1. Micah's explicit freeze go (this draft's "APPROVE preregistration" is not a freeze authorization).
2. Adversary named and sealed worlds specified (one per policy node minimum), with authorship after the freeze commit.
3. The six-element K-H3 listing completed per node with exact field numbers and code paths (sections 3 and 4 above are the template; the frozen version fills any remaining implementation-detail gaps after the design is finalized).
4. Discrimination predictions quantified (e.g., demotion threshold crossings, margin values) rather than directional only, where the design permits.
5. Freeze commit strictly precedes any implementation commit. No H3-lite source changes exist yet; this draft authorizes none.

---

## 9. Relation to parallel tracks

- **H2 (masked probes):** independent and approved. H2 asks whether the learner accepts/rejects/withholds structures on a learner-internal criterion; H3-lite asks whether decision criteria in learner state are revisable by experience. Neither depends on the other. H2 MUST precede any H1 widening; H3-lite does not widen H1.
- **Reuse path:** HIGH PRIORITY in parallel. The C0-D shadow fix (MAP-first execution, no shadow memoization) is structural and independent of policy revisability. A promoted procedure executing on later cognition is a separate claim from a policy value changing.
- **Revision substrate (copy-and-commit + MAP retargeting):** approved as a correctness experiment. It makes revision safe; H3-lite's repair dispatcher makes topology selection revisable. The two compose (dispatcher selects topology; copy-and-commit executes the repair safely) but neither implies the other.
- **Full TNN-3:** waits for H2, H3-lite, and reuse evidence. This preregistration is scoped to the H3-lite diagnostic only.

---

*End of draft. DRAFT-NOT-FROZEN. No implementation authorized. No scores claimed. Paper untouched.*
