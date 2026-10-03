# Mechanism-Level Architectural Compression Audit

**Date:** 2026-10-03. **Worker:** COMPRESSION-AUDIT (mechanism survey).
**Scope:** ANALYSIS ONLY. No source edits, no builds, no binaries run, no prereg (per task). Read-only survey of committed lane REPORT.md files and the canonical claim ledger.
**Relationship to the 2026-10-01 audit:** that audit (`COMPRESSION_AUDIT.md` in this lane) was code-level: it inventoried functions in frozen TNN-2 source and ranked 8 code candidates (trial-loop iterator, FACT/MAP duality, teach flags, pick-max, assembler params, and others). This audit is mechanism-level: it inventories learned-capability mechanisms across lanes, post-C413, and asks which mechanisms subsume which. The two audits are complementary; nothing here supersedes the code candidates.

## 0. Grounding notes

- U retirement (C413) is parent-provided governance context. The canonical claim ledger surveyed ends at C409; no C410+ entries were located in the files searched, so C413's ledger text was not independently verified. The evidence chain that was verified: GEN-SUBSUMES-U (ledger C397, verdict PARTIAL with a characterized residual boundary: multi-query arena reuse failed on stale tried-state) followed by GEN-STATEFIX (verdict UPGRADE-TO-SUBSUMES: the specified tried-state reset closed the boundary, P5 now ANS=3 with no widening, U documented as the restriction of GEN: single-round linear pool, predicted handshake, stateless trial enumeration).
- BP-1's REPORT says "to be ledgered C397", which collides with GEN-SUBSUMES-U's C397. Cited here by verdict (BP-1-PASS), not by claim number.
- All scenario numbers below are copied from committed REPORT.md files; nothing was re-run.

## 1. Mechanism inventory

| ID | Mechanism | Job | Source lanes / claims | Status |
|---|---|---|---|---|
| GEN | General composition | Compose learned structures via kind-contract admission over a value pool: rounds of trial execution, observed-kind checking (replaced U's predicted pair handshake), failure-triggered widening (WIDEN=1), success-recording with contract growth (e.g. X.out {2} to {1,2} via provenance closure), end-to-end verification. One rule covers fan-in, DAG-4, 3-chains, partial applicability. | C380 frozen value-graph extension of U (`d6_gen.zag`); gen_generality (GEN-GENERAL); gen_subsumes_u (C397 PARTIAL); gen_statefix (UPGRADE-TO-SUBSUMES) | SURVIVES. U retired (C413). |
| LCONT | Learned contracts | Hold typed contracts the learner commits to and acts on; detect staleness from verification failures (3 consecutive failures latch CONTRACT_REVISE_REQ); revise from post-change data only (generic first fit over [REV_PTR, XN)); retract stale ledger bits (U6: per-bit disconfirmation counters, retire at 2 consecutive disconfirmations). Tested distinction: a contract is a promise acted on with a verifier comparing commitment vs consequence; a mask is a passive input filter. | contract_drift_detect (CONTRACT-DRIFT-DETECT-COMPLETE); contract_revision (CONTRACT-REVISION-COMPLETE); compose_ledger U1-U6 (C341/C345/C352/C355) | LIVE |
| BP | Belief provenance / adjudication | Adjudicate between two conflicting grounded structures using learner-learned evidential weights: meta-table rows of (winner corr, loser corr) written after resolved conflict episodes, each row carrying type-16 provenance edges to both structures. Open-ended query (no target to verify against). Regime-sensitive: STANDARD commits via=20 val=202, REVERSED commits via=21 val=204, NOMETA declines (-3). | belief_provenance (BP-1-PASS) | LIVE |
| FC | Formal constraints | Learner builds constraint CONTENT from experience (grammar judgments to clause registry via minimal-cardinality search); the registry constrains generation/composition. Split verdict: content CAN be learner-built and is task-adequate (Arm L 6/6 picks identical to faithful Arm R), but the channel wiring (ABI plus the composer's reg_check call) remains researcher machinery; the learned content is a shortcut (fidelity_L 448/468), not the grammar. | formal_constraints (FORMAL-CONSTRAINTS-COMPLETE, split); background C264 | LIVE |
| NT | Negative transfer / retention | Retain useful structures under interference and memory pressure; control negative transfer. 3-tier eviction order (derived answers, then other, then generative last) preserves 8/8 generative cells under 1000 interference teaches; interference boundary mapped (NULL/PARTIAL/FULL overlap retention 100/100/34). | l2_interference (C314 PASS); l2_interference_d3 (L2-INTERFERENCE-D3-BOUND); PROTECT-HOW (C189); failure_retention (analysis); belief_forgiveness / belief_nogrudge | LIVE |
| LM | Lifetime meta-learning | Learn the learning dynamics: learner-owned adaptive update magnitude (STEP init 100, bounds [25,400], agree→x2 / disagree→/2 from experienced sign-volatility history LSIGN); invented revision procedures ([loo3, med] adopted from 7 candidates on the learner's own self-check, converging on the researcher hand-specified REVISE). Honest bound: the meta-mapping form remains fixed scaffold; the learned/scaffold boundary moved one level deeper, not eliminated. | belief_mprov, belief_mprov2, belief_mprov3 (MP-3-PASS, C408); hcontlife5-invent (C346 INVENTION-PASS) | LIVE |
| COGOPS | Cognitive operations | Cognitive procedures as learner-owned structures: selection, composition, and retirement of ops from learner state; body learning via REPAIR (blind single-SET-imm search on replay consequences), DIVERGE (context specialization into empty slots), INLINE (splice of high-composition pairs with JNZ retargeting); migration of researcher-supplied procedures into learner-owned indexed structures with context-sensitive selection and fallback. | cogops_structures; cogops_bodies (COGOPS-BODIES-COMPLETE); cogops_compose (PREREG only, in progress); cogop_invention; C406 COGNITIVE-OPS-LEARNER (MIGRATION DEMONSTRATED) | LIVE |
| INQ | Inquiry / uncertainty | Act under uncertainty: UNCERTAINTY node creation on true miss, POLICY_ROOT guides, ev_act action selection, P-INV statistical bootstrap shortcut. | tnn2_build (2026-10-01 audit sec E); belief lanes | LIVE |
| REV | Revision | Repair stale executable graphs: provenance-guided surgical revision (find stale SET cell, tombstone, insert corrected cell, rewire, re-execute, revert on verification failure). Copy-and-commit approved as the replacement for the in-place revert path. | tnn2_build (2026-10-01 audit sec F); C346 background | LIVE |
| DCE | Delayed consequence | Temporal credit assignment: commit to a composite, attribute the delayed consequence to the correct cause (attr (1,3)), demote/retire on evidence (relB 120 to 60); tamper-evident records (LS_RCK checksum, quarantine on mismatch). | C306, C309, C321 (DCE-V2, red teams) | LIVE |
| SEM | Semantic subsystem | Bounded L2+ subsystem: experimental baseline, negative/control reference, possibly a useful low-level component. Explicitly not L3, not general semantic understanding, not representational invention. On the record as retireable. | Governance 2026-09-29 | BOUNDED, RETIREABLE |
| CHAIN | Chain-family composition (A/B/C) plus L2 adapt operators | Mechanism A: compose_try contract/plen chaining ("unified composition contract fallback"). Mechanism B: type-15 co-use LINK edges on episode success. Mechanism C: cc_relseq constraint-driven assembly from MAP relation sequences. L2 adapt operators: EXTEND, TRUNCATE-TAIL, SPECIALIZE, SUBSTITUTE, INTERFACE-ADAPT (operation matrix complete, C302). Still live in 2026-10-03 lanes (l2_interference_d3 uses compose_try mechanism-A pair scan verbatim). | C295, C297, C298, C302, C310, C313, C314; l2_interference_d3 | LIVE |
| ISA | Protected core | 4-op ISA (MOVE/BEQ/INC/DEC) plus EXECUTE(root, frame). Frozen machinery, not intelligence. | Governance 2026-09-30 | FROZEN, not a candidate |

## 2. Pairwise subsumption analysis

Verdict key: SUBSUME = one mechanism could replace the other's job (compression candidate). OVERLAP = shared sub-job, partial. DISTINCT = genuinely different jobs (triggers, artifacts, or outputs differ). Pairs are judged on capability overlap, not surface similarity.

### 2a. Core seven, all pairs

| Pair | Verdict | Reasoning |
|---|---|---|
| GEN x LCONT | SUBSUME (candidate 1) | Both maintain learned applicability descriptions of structures, revised by experienced failure. GEN: kind-set masks, success-recording growth, observed-kind checking, failure-triggered widening, U6 disconfirmation-counter retraction. LCONT: commitment contracts, 3-failure drift latch, post-change refit, U6 bit retirement. Same artifact class (consumes/produces/constraints/confidence), same revision trigger (failure). Residual question: admission filter (GEN) vs acted-on promise with verifier (LCONT); the test in section 4 decides whether that distinction is load-bearing. |
| GEN x FC | SUBSUME (candidate 1) | FC's clause registry is learned constraint content consulted during composition; GEN's admission is learned kind constraints consulted during composition. FC adds content induction from judgments (minimal-cardinality search), which GEN's growth-by-success-recording does not currently do. The unified mechanism would need FC's induction plus GEN's checking. |
| LCONT x FC | SUBSUME (candidate 1) | Both are learned constraint/contract content revised by experience: LCONT's (C_SLOT, C_THRESH) promise vs FC's clause sets. Different induction sources (verification failures vs grammar judgments) feeding the same artifact class. Fold into candidate 1. |
| GEN x COGOPS | SUBSUME (candidate 2) | GEN composes structures by kind-contracts over a value pool; cogops_compose composes cognitive operations. Cognitive ops are structures; if they carry kind-contracts, GEN's rounds apply unchanged (GEN is already domain-blind: opaque integer identifiers only). Scope limit: only the composition part. REPAIR/DIVERGE/INLINE are body invention, not composition, and stay distinct. |
| GEN x BP | DISTINCT | GEN admits structures by contract and verifies by trial; BP adjudicates already-grounded conflicting structures by learned evidential weights with no verification target. Admission vs conflict resolution: different triggers (query vs conflict episode), different outputs (trial plan vs commitment). |
| GEN x NT | DISTINCT | Composition vs retention under pressure. Nothing in GEN decides what survives memory pressure or interference; nothing in NT assembles structures. |
| GEN x LM | DISTINCT | Composition vs learning dynamics. MP-3's STEP adaptation has no counterpart in GEN; GEN's trial rounds have no counterpart in LM. |
| LCONT x BP | DISTINCT | LCONT revises a contract on verification failure; BP commits to one of two conflicting structures on learned evidential weights. Both consume failure evidence, but outputs differ (revised promise vs chosen structure). Merging would blur the contract/adjudication line the BP-1 design deliberately holds (open-ended query, no target). |
| LCONT x NT | DISTINCT | Contract revision vs retention under pressure. Different triggers (verification failure vs memory pressure/interference), different outputs (new contract vs eviction order). |
| LCONT x LM | DISTINCT | Contract content vs update dynamics. No overlap. |
| LCONT x COGOPS | DISTINCT | Contract lifecycle vs cognitive-procedure ownership. No overlap. |
| BP x FC | DISTINCT | Conflict adjudication vs constraint induction. No overlap. |
| BP x NT | DISTINCT (examined closely) | Tempting because both rank structures, but the jobs differ: BP decides which structure to trust now (decision, triggered by conflict episodes, output is a commitment); NT decides what survives pressure (retention, triggered by interference/memory pressure, output is an eviction/retention order). Collapsing decision into retention would lose the regime-sensitivity BP-1 demonstrated (STANDARD vs REVERSED opposite commitments under identical structure profiles). |
| BP x LM | DISTINCT | Adjudication weights are learned from conflict episodes; LM's STEP is learned from update-sign volatility. Both are "learned meta-state" but about different objects (evidence weights vs update magnitude). Superficial similarity only. |
| BP x COGOPS | DISTINCT | No overlap. |
| FC x NT | DISTINCT | No overlap. |
| FC x LM | DISTINCT | No overlap. |
| FC x COGOPS | DISTINCT | No overlap. |
| NT x LM | DISTINCT | Retention policy vs learning dynamics. Different objects, different triggers. |
| NT x COGOPS | DISTINCT | No overlap. |
| LM x COGOPS | DISTINCT | LM learns how updates should behave (STEP, revision-procedure invention as an instance); COGOPS owns cognitive procedures as structures. H-CONTLIFE-5-INVENT sits near the boundary (invented revision procedure), but MP's update-magnitude job has no COGOPS counterpart. Not a compression candidate. |

### 2b. Extended pairs (other live mechanisms)

| Pair | Verdict | Reasoning |
|---|---|---|
| REV x LCONT | SUBSUME (candidate 3) | Both are failure-driven revision with provenance: detect staleness via failed verification, localize via provenance, repair, re-verify, revert/retire on failure. REV operates on executable graphs (surgical SET replacement); LCONT operates on contracts (exception list, post-change refit). If contracts attach to structures (the direction GEN's contract growth already points), one revision operator parameterized by revision target could serve both. Substrates differ today, so this is a design unification, testable. |
| REV x GEN | DISTINCT | Repair vs composition. GEN has no repair path; REV has no trial search. |
| DCE x BP | DISTINCT (examined closely) | Both update structure reliability from evidence with provenance, but the problems differ: DCE does temporal causal attribution (which composite caused this delayed consequence, under confounding and decoys); BP does conflict adjudication (which of two grounded structures to trust, no target). DCE's record/checksum integrity machinery is tamper-evidence, not adjudication. Merging would conflate credit assignment with conflict resolution. |
| INQ x GEN | DISTINCT (examined) | GEN's WIDEN=1 expands the trial space on failure; INQ creates UNCERTAINTY nodes and selects inquiry actions via POLICY_ROOT/ev_act. Trial-space expansion is not inquiry: widening never produces an action, and inquiry never assembles structures. Different outputs. |
| GEN x CHAIN | EXAMINED, boundary flagged (not ranked) | The largest unresolved surface. GEN sequences structures by kind-contracts over a value pool; the chain family chains MAP graphs (compose_try), records co-use (type-15), assembles from relation sequences (cc_relseq), and mutates structures (8 L2 adapt operators). Overlap: both answer queries by combining learned structures. Genuine difference: GEN as frozen does reuse and growth, not structural mutation; the adapt operators (truncate a MAP, substitute a segment, adapt an interface) change structures rather than sequence them. A subsumption claim would need GEN's trial rounds to generate adapted variants as candidates, which is an extension of GEN, not a replacement of the adapt operators. Per the parent's framing GEN holds the composition slot and the adapt operators hold the L2-reuse slot; forcing a merger now would be premature while L2 adaptive reuse is Micah's top priority and actively researched. Recommended as the follow-up probe after candidate 1 (see section 5). |
| SEM x anything | RETIRE, not subsume | SEM is already on the record as a bounded L2+ subsystem and retireable. The compression move is formal retirement through the supersession process, not absorption into another mechanism. |

### 2c. What does not compress (honest list)

LM (update dynamics: nothing else adapts learning magnitude from experienced volatility), NT (retention under pressure: nothing else decides survival under interference), INQ (inquiry under uncertainty: nothing else produces inquiry actions), DCE (temporal attribution: nothing else assigns delayed consequences to composites under confounding), BP (conflict adjudication: nothing else resolves structure conflicts by learned evidential weights without a verification target), ISA (frozen protected machinery by governance). These are distinct jobs with distinct triggers, artifacts, and outputs. Compressing any of them into the candidates above would be superficial similarity, not capability overlap.

## 3. Top 3 compression candidates, ranked

### Candidate 1: One learned-contract mechanism (GEN contract core + LCONT + FC)

**What unifies:** GEN's kind-set machinery (admission checking, success-recording growth, observed-kind checking, failure-triggered widening, U6 disconfirmation-counter retraction), LCONT's lifecycle (commit to a typed contract, 3-consecutive-failure drift latch, post-change-window refit, value-keyed exception revision), and FC's content induction (judgments to clause registry via minimal-separation search). All three maintain the same artifact: a learned applicability description of a structure (consumes, produces, constraints, confidence), inducted from experience, consulted during composition, revised by failure. This is also the exact shape of Micah's 2026-10-03 clarification (structures described by learned properties: consumes, produces, constraints, consequences, confidence/evidence, state changes, cost, provenance, learned applicability).

**What it replaces:** three separate contract-related machineries (GEN's masks, LCONT's drift/revision loop, FC's registry) with one: induct, check, grow, invalidate, revise.

**Risk:** medium. The admission-filter vs acted-on-promise distinction (GEN vs LCONT) may be load-bearing; FC's induction bias (researcher-chosen minimal cardinality) may not be expressible as experience-driven growth. Section 4's test is designed to characterize exactly these boundaries rather than assume them away.

**Why ranked first:** strongest capability overlap in the inventory, directly serves the learned-contracts priority, and both source scenarios are frozen with exact expected outputs, so the subsumption test is fully designable now.

### Candidate 2: One composer for domain and cognitive structures (GEN + COGOPS composition)

**What unifies:** GEN's value-pool rounds (admit by kind-contract, trial-execute, verify, widen on failure) applied to cognitive operations as well as domain structures. cogops_structures already showed selection/composition/retirement of ops can be learner-owned; GEN is domain-blind (opaque integer identifiers only), so nothing in its rule cares whether a structure is a domain procedure or a cognitive op, provided kind-contracts exist.

**What it replaces:** a separate cognitive-op composer with GEN's composer. REPAIR/DIVERGE/INLINE stay as the distinct body-invention layer (invention, not composition).

**Risk:** medium-high. cogops_compose is PREREG-only (no frozen scenarios yet), so the test cannot be fully specified until its scenarios land. There is also a real question whether cognitive ops admit kind-contracts of the same form (their "inputs/outputs" are interpreter states, not values).

**Why ranked second:** principled and high-value (one composition operation for the whole architecture, matching the "ONE general composition operation" direction), but blocked on cogops_compose producing frozen scenarios first.

### Candidate 3: One failure-driven revision operator (REV + LCONT revision)

**What unifies:** the shared revision process: staleness detected via failed verification, localized via provenance, repaired, re-verified, reverted or retired on failure. REV does this on executable graphs (surgical SET replacement); LCONT does it on contracts (post-change refit, exception list). One operator parameterized by revision target (contract vs graph) could serve both, especially as GEN's contract growth already attaches contracts to structures.

**What it replaces:** two separate revision paths with one provenance-guided revise-and-reverify loop.

**Risk:** medium. The substrates genuinely differ today (kind-sets vs executable graphs), so this is a design unification requiring the contract/graph attachment to be real, not just asserted. The 2026-10-01 code audit's Rank 2 (one knowledge node with optional executable) is the structural precondition; without it, the unification is cosmetic.

**Why ranked third:** real process overlap, but the test needs the structural precondition first, and LCONT's revision is already covered by candidate 1's test (contract revision is part of the contract lifecycle), so candidate 3 is partly downstream of candidate 1.

## 4. Subsumption test design for candidate 1: CONTRACT-UNIFICATION

Design only. No implementation. Intended to be prereg-ready as written.

### 4.1 Question

Can one learned-contract mechanism reproduce LCONT's drift-detection and revision verdicts AND FC's constrained-generation verdicts, with no separate contract machinery? The mechanism: a contract is (consumes, produces, constraint-clauses, confidence); operations are induct (from judgments, FC-style), check (admission, GEN-style), grow (success-recording, GEN-style), invalidate (disconfirmation counters, retire at 2 consecutive, U6-style), revise (post-change refit triggered by 3 consecutive verification failures, LCONT-style).

### 4.2 Frozen sources (read-only, byte-verified against committed lanes)

- S1: contract_drift_detect lane: `cd_full.zag`, REPORT.md. Contract CONTRACT_TY=7 (C_SLOT, C_THRESH); world change moves the outcome law from slot 2 to slot 4 with the surface stream unchanged. Frozen trace: Arm A phase 1 8/8 correct req=0; phase-2 queries 1..3 mismatch (1/0, 0/1, 0/1), req latches at q=3; revision yields slot=4, revcount=1, fiterr=0, olderr=2; phase-2 remainder 9/9; phase 3 (fresh world) 8/8 req=0. Arm C (revision disabled): phase 2 3/12, req latched and held.
- S2: formal_constraints lane: REPORT.md. Six trials; frozen Arm R picks: (19,87), (17,119), (19,87), (85,85), (19,87), (19,87). Frozen Arm L (learner-built content) matches all six picks exactly; fidelity_L 448/468 (the 20 predicted shortcut disagreements).

### 4.3 Build (one unified contract module, pure Zag, pinned znc)

A single contract module used identically by both arms below. No per-scenario branches (shell-audited: the scenario identifier never appears in the module). Opaque integer identifiers only. 0 new modes, bridges, handlers, semantic cases, opcodes, or edge types beyond what the frozen sources already use.

### 4.4 Arms and frozen predictions

- **Arm D (drift):** the unified contract on S1's world-change scenario. Frozen predictions: req latches at exactly q=3 (3 consecutive verification failures); revised contract is slot=4 with revcount=1, fiterr=0, olderr=2; phase-2 remainder 9/9; fresh-world phase 3 8/8 req=0. A revision-disabled control reproduces Arm C's 3/12 with req held.
- **Arm G (grammar):** the unified contract's induct plus check on S2's six trials. Frozen prediction: all six picks exactly (19,87), (17,119), (19,87), (85,85), (19,87), (19,87), matching frozen Arm R.
- **Arm N (ablation):** unified contract with induct and revise disabled. Frozen predictions: req never latches on S1 (drift undetected, phase-2 stays at control level); picks diverge from Arm R on at least one of the six S2 trials. Proves the unified machinery (not the harness) does the work.

### 4.5 Kill bars

- K1: Arm D reproduces the frozen drift trace exactly (req at q=3, revised slot=4, 9/9 remainder).
- K2: Arm G reproduces the 6/6 frozen picks exactly.
- K3: 3/3 byte-identical runs per arm; stderr empty.
- K4: mechanism hygiene: 0 new modes/bridges/handlers/semantic cases/opcodes/edge types; opaque identifiers only; one contract module serves both arms (diff-verified: no scenario branches).
- K5: Arm N fails as predicted (drift undetected; at least one pick diverges).
- K6: toolchain guard: safebin PATH, `which python3` and `which python` return nothing, pure Zag, pinned znc, shell only for build/run/verify.
- K7: zero em/en dash bytes in lane docs.

### 4.6 Falsification criteria (what kills or bounds the subsumption claim)

- F1: if LCONT's commitment-vs-consequence verifier cannot be expressed as contract checking without changing Arm D's verdicts, the boundary is characterized: admission contracts (GEN) and commitment contracts (LCONT) are distinct jobs. Verdict: SUBSUMPTION FAILS; LCONT survives as the commitment-contract mechanism.
- F2: if FC's content induction requires the researcher-chosen minimal-cardinality bias in a form the unified mechanism cannot supply from experience, the boundary is characterized: induction bias is separate machinery. Verdict: PARTIAL (unified checking and revision, separate induction).
- F3: if either arm needs per-scenario branches inside the unified module, the unification is fake. Verdict: FAIL.
- A PARTIAL or FAIL here is informative, not a defect: it maps exactly where the contract jobs diverge.

### 4.7 Honest bounds (not claimed by this test)

- The direction of absorption is open: the test establishes that ONE mechanism suffices, not whether GEN's core absorbs LCONT/FC or a fresh unified module replaces all three. Governance decides the landing shape.
- U6's ledger status (Micah's call per C352) is unchanged by this test; the test only uses the disconfirmation-counter pattern as the unified retraction path.
- Out of scope: the chain family (A/B/C), the L2 adapt operators, BP, DCE, NT, LM, INQ, and COGOPS body invention. None are exercised or affected.

## 5. Strategic recommendation: where the next compression effort goes

1. **First: run the CONTRACT-UNIFICATION test (section 4).** Highest information gain per unit effort: both source scenarios are frozen with exact expected outputs, the overlap is the strongest in the inventory, and the result directly serves the learned-contracts priority and the 2026-10-03 "structures described by learned properties" clarification. Either outcome is useful: full subsumption removes two machineries; a characterized boundary (F1/F2) tells us exactly which contract jobs are distinct.
2. **Second: the GEN-vs-COGOPS-composition probe,** once cogops_compose lands frozen scenarios. Do not run it now: the scenarios do not exist yet, and a premature test would manufacture its own target.
3. **Third: the revision-unification probe** (candidate 3), downstream of candidate 1: if contracts unify, the revision operator unification becomes a natural corollary; if F1 fires (commitment contracts stay separate), candidate 3's scope narrows to graph-side revision only.
4. **Do not compress:** LM, NT, INQ, DCE, BP (section 2c). Each is a distinct job with distinct triggers and outputs; merging any of them would be superficial similarity, the exact failure mode this audit was asked to avoid.
5. **Retire SEM formally** through the supersession process. It is already "retireable" on the governance record; retirement is a decision, not an experiment.
6. **Flag for governance (not decided here):** the chain family (A/B/C plus the 8 L2 adapt operators) is the largest unresolved compositional surface, and it is still live in 2026-10-03 lanes. GEN's frozen form sequences structures; it does not mutate them. Recommend a dedicated GEN-vs-chain-family subsumption probe as the follow-up after contract unification, framed as: can the L2 adapt operators be expressed as candidate generators inside GEN's trial rounds, or is structural mutation a genuinely separate job from compositional sequencing? Do not force this merger while L2 adaptive reuse is the top research priority; the probe should be adversarial, not promotional.

## 6. Method note

Read-only survey. Sources: committed REPORT.md files in the lanes named in section 1, the canonical claim ledger (C1-C409 surveyed; entries cited by number where present), the 2026-10-01 code-level compression audit in this lane, and standing governance records (MEMORY.md, alignment synthesis). No binaries built, no worlds executed, no sealed evaluator assets opened. Pairwise judgments follow capability overlap (shared artifacts, triggers, and outputs), not surface similarity. Where the evidence did not support a merger, the pair is marked DISTINCT with the reason, per the task's honesty requirement.
