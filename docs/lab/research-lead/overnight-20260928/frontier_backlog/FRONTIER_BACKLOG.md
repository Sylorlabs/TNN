# Frontier Backlog

Date: 2026-10-01. Maintainer: frontier backlog worker. Status: LIVING DOCUMENT.

Micah's directive: maintain at least 15 substantive research questions. When a worker finishes, replace it with the highest-information non-duplicative task. This document holds 18.

## Ranking rationale

Ranked by expected information gain for the north star: one frozen general architecture that creates, evaluates, revises and reuses cognitive structures its programmers did not supply, operating as a continuous adaptive learner (frozen researcher code + continuously changing learner state).

## Status summary

- ACTIONABLE NOW: 15 (Q1, Q2, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q13, Q15, Q16, Q17, Q18)
- BLOCKED: 3 (Q3 on H2 results; Q12 on Micah's H3-lite freeze go; Q14 probe design actionable now, full measurement needs Q1)

---

## Q1. Lifetime evaluation protocol: concrete design

**Question:** Design the concrete lifetime stream protocol Micah mandated: WORLD A, learn, WORLD B, retain/reuse/connect, WORLD C, revise, WORLD D, discover new representation, return to WORLD A-like problem, exploit everything learned since. Specify the world sequence, no-reset mechanics, task-label-free operation, and all eight lifetime metrics: forward transfer, backward transfer, spontaneous cross-domain connections, reduced examples-to-criterion over time, reuse of old executable structures, revision without destroying useful prior structure, memory under long interference, whether learning itself improves.

**Why it matters:** Micah designated the lifetime stream the PRIMARY long-term AGI evaluation. Without a concrete executable protocol, the lifetime direction cannot run. This unblocks an entire evaluation paradigm and gives every other lifetime question (Q7, Q11, Q14, Q17) its test harness.

**Confirm:** A frozen protocol document with world specs, metric definitions, and pure-Zag scoring code that a worker can execute end to end with no researcher task labels and no state resets.

**Falsify (as a design):** If the protocol cannot be executed without researcher-supplied task labels or mid-stream resets, it violates Micah's constraints and must be redesigned, not patched.

**Dependencies:** None. Design only.

**Status:** ACTIONABLE NOW.

---

## Q2. Cross-domain structure transfer without hardcoded mappings

**Question:** The reuse experiment (commit ea8fc0ac1) confirmed the value-trace limitation: graphs bake literals into structure, so a MAP built for one subject fails on a different subject and rebuilds instead of invoking. Design and test (unfrozen variant, white-box verified) a mechanism by which a structure learned in context A is recognized as applicable in context B, adapted or invoked there, requiring fewer experiences than a fresh learner. No hardcoded cross-domain mappings.

**Why it matters:** This is the core architectural blocker for C0-D and for the lifetime vision. Micah named it a major target explicitly: learn structure in context A, recognize applicability in context B, adapt/invoke it, require fewer experiences than a fresh learner.

**Confirm:** Sealed test: structure learned in A is invoked (white-box: same MAP node executes, not a rebuild) in B; measured examples-to-criterion in B is lower than a fresh-learner control; no domain hint supplied.

**Falsify:** If every variant still rebuilds per-subject graphs under adversarial inspection, the value-trace limitation is architectural and needs a representation change (role/addressing abstraction), not a lookup change. That negative result is itself high-information: it scopes Q13 and Q18.

**Dependencies:** None. Builds on reuse_experiment infrastructure.

**Status:** ACTIONABLE NOW.

---

## Q3. H2 results: interpretation and next diagnostic

**Question:** H2 (K-H2-1 through K-H2-4) is frozen and the evaluator is authorized; predicted outcome is FAIL on all four bars. When results land: what exactly do they falsify about learner-internal accept/reject/withhold criteria? Produce the conditional next-diagnostic plan: for each outcome pattern (e.g., K-H2-3a passes but 3b fails means a criterion value exists but is not causal), specify the follow-up experiment. No outcome may be interpreted more broadly than its bar warrants.

**Why it matters:** H2 gates H1 widening. Misreading its results (overclaiming a pass, or under-reading a partial) wastes the next cycle. The predicted FAIL needs a pre-committed interpretation so the failure is information, not disappointment.

**Confirm:** A decision tree mapping each of the 16 outcome patterns to a named next experiment, recorded before results land if possible.

**Falsify:** Not applicable (interpretation task). The failure mode to avoid is post-hoc reinterpretation of bars.

**Dependencies:** H2 evaluator results.

**Status:** BLOCKED on H2 evaluator completion. The pre-commitment half (outcome-pattern tree) is ACTIONABLE NOW.

---

## Q4. Learner-owned retention policy under long interference

**Question:** The transfer analysis (commit 475c57e23) showed the memory pathology: beyond the 1024-node budget, graph cells are evicted, MAPs survive as inert fossils, promoted facts are evicted, learned answers are catastrophically forgotten, and rejected trial candidates accumulate as unreclaimed garbage. Design and test (unfrozen variant) a general learner-owned retention policy: what survives, what compresses, what retires, with the decision made from learner state, not researcher cache policy. No task-specific storage logic (Micah's explicit constraint: the store/eviction failure must not become another cache-policy treadmill).

**Why it matters:** The lifetime vision requires memory that survives long interference. Key question from Micah: what general learner-owned memory representation/policy lets one frozen learner preserve newly useful knowledge, dependencies, hypotheses and structures without task-specific storage logic?

**Confirm:** Under a long interference stream, retention of useful structures beats a recency-eviction baseline on revisit probes; white-box shows retention decisions reading learner-state utility fields through a production write path (theater rule applies).

**Falsify:** If no learner-state-driven policy beats simple recency-eviction, retention may need an architectural change (different memory substrate), not a policy change.

**Dependencies:** None.

**Status:** ACTIONABLE NOW.

---

## Q5. Copy-and-commit revision: corruption fix verification

**Question:** Micah approved copy-and-commit plus MAP retargeting as a correctness architecture experiment: candidate repairs built in fresh cells, verified, then atomically committed; no in-place mutation or revert. Implement on an unfrozen variant and verify: (a) the allocator-alias corruption on failed interior revision (commit 8b58c4104) no longer occurs; (b) FW4 stays 12/12 with no extra scaffolding; (c) the four regression tests from the revision advice (commit 5a009ff87) pass: failed interior revision is a byte-identical no-op; second contradiction revises the same MAP; total repair failure supersedes the MAP and falls back to facts; FW4 remains 12/12.

**Why it matters:** A lifetime learner that revises beliefs must not corrupt its own memory when a revision fails. Revision safety is prerequisite infrastructure for everything downstream. Micah was explicit: this makes revision safe; it does not by itself count as progress toward SUF.

**Confirm:** All four regression tests pass, FW4 12/12, white-box shows a failed revision leaves the graph byte-identical.

**Falsify:** If copy-and-commit breaks FW4 or introduces a new corruption mode, the design needs revision before it can serve as the substrate for Q18.

**Dependencies:** None.

**Status:** ACTIONABLE NOW.

---

## Q6. SUF operationalization: what does a SUF decision concretely look like?

**Question:** Micah set Source-Underdetermined Form as the entrance criterion for future construction work: at least one causal structural decision in the production path must be resolved by learner history, such that the produced form cannot be completely enumerated from source alone. SUF is necessary, not sufficient. Construct the minimal concrete demonstration: name a specific decision point in a production path, show the specific learner-history dependence, and give the non-enumerability argument. Then test whether TNN-2 or an unfrozen variant can exhibit it, and submit the example to red-team review.

**Why it matters:** SUF gates all future invention work. If no one can exhibit what a SUF decision concretely looks like, the gate is decorative and every future claim will be arguable. Making it concrete also gives the SUF check (commit 8ef148a42, currently SUF-FAIL on all three mechanisms) a positive target.

**Confirm:** A worked example (decision point, history dependence, non-enumerability argument) that survives independent red-team review, plus an empirical demonstration on an unfrozen variant.

**Falsify:** If the candidate "SUF" example collapses to a source-enumerable parameterization under adversarial inspection (e.g., the history only selects among researcher-enumerated options), it was not SUF. Record the collapse mode; it sharpens the criterion.

**Dependencies:** None. Analysis plus minimal experiment.

**Status:** ACTIONABLE NOW.

---

## Q7. Learning-to-learn: does examples-to-criterion decrease over a lifetime?

**Question:** Run a sequential multi-world stream through one learner (no process reset, no learner-state reset, unfrozen variant) and measure examples-to-criterion on each successive new world. Does it decrease? Isolate the cause: attribute any decrease to reuse of specific structures (white-box) versus mere parameter warm-start. Fresh-learner control on each world is required.

**Why it matters:** Micah's lifetime metric: whether learning itself improves. This is the most direct test of the "continuously changing learner state" half of the scientific ideal, and the sharpest discriminator between a learner that accumulates and one that merely persists.

**Confirm:** Statistically robust decrease in examples-to-criterion versus fresh-learner controls, with white-box attribution to identified reused structures (not just warm weights).

**Falsify:** Flat or increasing examples-to-criterion across the stream falsifies learning-to-learn for the current architecture and redirects effort to Q2/Q4/Q13.

**Dependencies:** Lifetime protocol (Q1) for the full stream; an ad-hoc stream suffices to start.

**Status:** ACTIONABLE NOW (ad-hoc stream). Full version uses Q1 when it lands.

---

## Q8. Spontaneous cross-domain connection: the detection mechanism

**Question:** Micah wants cross-domain connection as a FEATURE, not contamination: a structure learned for arithmetic recognized as useful for planning, a causal abstraction reused in language. What mechanism would even detect such an opportunity? Design the minimal detector: what is compared between a current problem and stored structures, what triggers retrieval of a structure from a different domain, what verifies applicability before commitment. Test on an unfrozen variant with two genuinely different domains and no researcher hint.

**Why it matters:** Without a detection mechanism, cross-domain reuse cannot happen spontaneously; it would need researcher hints, which violates the north star. This is the perception half of Q2's action half.

**Confirm:** Sealed test where the learner retrieves and applies a cross-domain structure with no domain hint; white-box trace shows the retrieval decision and the applicability check firing.

**Falsify:** If retrieval only works with researcher-supplied similarity hints or domain tags, the mechanism is not spontaneous and the result is negative evidence about current representational generality.

**Dependencies:** None.

**Status:** ACTIONABLE NOW.

---

## Q9. Inquiry: derived questions from hypothesis structures

**Question:** The inquiry generalization analysis (C159, commit dedfad368) diagnosed the constant-action root cause (a prereg spec gap: the bars tested chain structure, not question content) and sketched a derived-question design within the frozen ISA: persist trial candidates as hypothesis structures linked to the uncertainty node; derive one guide per discriminating sub-query; score competing guides by informativeness in ev_act's existing max-scan; on later learning, resolve uncertainties and supersede guides via the existing type-3 self-edge convention. Implement on an unfrozen variant and test whether guides become discriminating (contentful, hypothesis-splitting questions) rather than constant actions.

**Why it matters:** Inquiry is one of the three red-teamed mechanisms (4e329c772 ATTACK-SUCCESS). The root cause is diagnosed and a concrete fix direction exists. This is the highest-information inquiry experiment available.

**Confirm:** Guides vary with hypothesis content; sealed inquiry scenarios (5+ per the accepted Q1 recommendation) show above-baseline discrimination; white-box shows guides derived from persisted hypotheses.

**Falsify:** If guides remain constant-action despite persisted hypotheses, the sketch is insufficient and inquiry needs architectural work, not procedure work.

**Dependencies:** None.

**Status:** ACTIONABLE NOW.

---

## Q10. White-box structure census after a long run

**Question:** Micah: use the white box to find things. Run frozen TNN-2 through a long mixed stream, then systematically catalog what learner state actually contains: MAP nodes, FACT nodes, fossil MAPs, unreclaimed garbage, policy-relevant fields. For each structure: was it ever executed, how often, when last? What fraction of learner state is write-only (created, never read in production)? Produce the first census of a TNN learner's internal world.

**Why it matters:** We reason about learner state abstractly; a concrete census grounds the retention (Q4), reuse (Q2), revision (Q5/Q18), and forgetting (Q11) questions in what is actually there. The write-only fraction directly measures theater versus participation.

**Confirm:** A complete census document with counts, execution frequencies, recency, and the write-only fraction, reproducible from committed scripts.

**Falsify:** Not applicable (survey). Surprise is the product: any large write-only fraction is itself a finding.

**Dependencies:** None.

**Status:** ACTIONABLE NOW.

---

## Q11. Useful forgetting: learner-owned retirement policy

**Question:** When should a structure be retired? Design a learner-owned retirement criterion (not researcher TTL): structures that have not contributed to successful cognition over an experience window are compressed or retired, freeing budget. The hard case, from Micah: a previously useless memory becoming important because of a new connection. Test that retirement handles dormancy correctly (compress, do not delete, or keep a re-derivable trace) and does not destroy structures that later prove useful.

**Why it matters:** A lifetime learner without forgetting drowns in garbage (observed: unreclaimed rejected trial candidates). But naive forgetting destroys the dormant-then-useful case that makes long lifetimes valuable. Forgetting must be useful and dormancy-aware.

**Confirm:** Retirement frees measurable budget, does not increase errors on revisit probes, and a seeded dormant-then-useful structure survives retirement in recoverable form.

**Falsify:** If every retirement policy either leaks (no space freed) or destroys needed knowledge, the criterion class is wrong and retirement needs architectural support (e.g., a compression substrate).

**Dependencies:** Related to Q4 (retention); proceed in parallel, merge findings.

**Status:** ACTIONABLE NOW.

---

## Q12. H3-lite: freeze, implement, evaluate

**Question:** The H3-lite preregistration draft (commit dab50dd68) is DRAFT-NOT-FROZEN, scoped honestly per Micah: it moves researcher-fixed decision points into learner-state policy nodes (3 nodes: construction trial order, inquiry guide defaults, revision topology dispatch) and does not establish learner-authored procedures, SUF, or L3. Once Micah gives the explicit freeze go: freeze the preregistration, implement the 3 policy nodes on an unfrozen variant (Alternative C boundary: no structural opcodes, no ISA change), run the K-H3 six-element write-path audits on sealed worlds, and report whether moving decision criteria into learner-writable state produces causal improvement.

**Why it matters:** This is Micah's Alternative C diagnostic: the key test of whether learner-writable criteria matter, before any protected-core expansion. A clean negative result banks Alternative B with evidence; a positive result revises the research program.

**Confirm:** K-H3 evaluated per the frozen bar; every claimed learner-owned decision shows its production write path firing on transcripts, or theater is declared.

**Falsify:** If the policy nodes do not change behavior versus frozen TNN-2 on sealed worlds, H3-lite is negative evidence for the criteria-in-learner-state hypothesis. Record it as such; do not reinterpret.

**Dependencies:** Micah's explicit freeze go for H3-lite preregistration.

**Status:** BLOCKED on Micah (freeze go). Implementation prep (variant scaffolding, audit harness) is ACTIONABLE NOW.

---

## Q13. Composition: the plan constructor

**Question:** The design synthesis names the plan constructor as the missing piece: procedures and causal rules converging on one executable graph type, composition as one execution problem. Design the minimal plan constructor: given a goal and a set of existing MAPs/procedures, compose them into one executable plan graph. Specify its inputs, its output form, how a composed plan is verified before execution, and what happens when composition fails. Prototype on an unfrozen variant.

**Why it matters:** Without composition, TNN has fragments, not cognition. Every mechanism builds structures; nothing assembles them toward a goal. This is the architectural hole the synthesis identified, and the lifetime vision (exploit everything learned since) presupposes it.

**Confirm:** Design plus unfrozen-variant prototype that composes two learned structures into a working plan on a sealed test, with a verification step that rejects bad compositions.

**Falsify:** If composition requires researcher-authored glue per task, it is not a general constructor; record the glue as the missing mechanism.

**Dependencies:** None. Design plus prototype.

**Status:** ACTIONABLE NOW.

---

## Q14. Backward transfer: does later learning improve earlier capabilities?

**Question:** Design the backward-transfer probe for the lifetime stream: after the learner masters WORLD C, revisit a WORLD A-like problem. Is performance better than the original A run? Better than a learner that only ever saw A? And the interference control: does C damage A, and if so, which structures were harmed (white-box)?

**Why it matters:** Micah's lifetime metric: backward transfer (new knowledge improving old capabilities) is strong evidence of integrated rather than siloed learning. Forward transfer gets the attention; backward transfer is the harder and more informative test.

**Confirm:** A-like revisit outperforms the original A run with white-box attribution to specific C-learned structures; interference bounded and characterized.

**Falsify:** If C only interferes with A and no backward transfer appears anywhere across several domain pairs, learning is siloed and the integration question (Q8/Q13) becomes the priority.

**Dependencies:** Lifetime protocol (Q1) for the full stream; probe design is independent.

**Status:** Probe design ACTIONABLE NOW; full measurement uses Q1 when it lands.

---

## Q15. Architectural compression audit

**Question:** Count across TNN-2 per Micah's standing metric: researcher-owned structural decisions, learner-owned structural decisions, source-enumerable forms, SUF decisions, learner-internal criteria, reuse events, revision events, cognition lines, modes, bridges, handlers, semantic cases. Propose the minimal mechanism set under the One-System Rule. Flag every MODE smell (CAUSAL_MODE, REVISION_MODE, LANGUAGE_MODE, MEMORY_MODE, PROCEDURE_MODE), every bridge, every task-specific handler; identify any boundary with three custom bridges as an ARCHITECTURE REVIEW trigger.

**Why it matters:** Micah scores ARCHITECTURAL COMPRESSION explicitly and the One-System Rule needs enforcement teeth. The audit also establishes the baseline counts that every future mechanism report must be measured against.

**Confirm:** A complete count table plus a concrete deletion/merge proposal that preserves the 4/9 freeze score and the floor (6 capabilities, 7 tests).

**Falsify:** Not applicable (audit). If no deletions preserve 4/9, that is itself evidence about which mechanisms carry the score, and it constrains Q13's design space.

**Dependencies:** None.

**Status:** ACTIONABLE NOW.

---

## Q16. TNN-vs-serious-LLM arena: design

**Question:** Design the fair competitive arena Micah specified: a capable non-crippled LLM baseline, 15 measured capabilities chosen where GPT-3-class systems are awkward (persistent one-shot learning, long-lived corrections, learner-owned memory, traceable beliefs, conflicting hypotheses, active inquiry, invention, structural adaptation, continuing life, plus six more), honest resource charging (compute, memory, energy per task), and capability curves rather than superiority declarations.

**Why it matters:** The mandate requires demonstrating capability/cost advantages against serious baselines, never a deliberately crippled LLM. The arena must be designed (and its honesty properties argued) before it can be run.

**Confirm:** A frozen arena spec: capability list with operational definitions, named baseline, resource accounting method, scoring code, and a pre-committed interpretation policy (curves, not declarations).

**Falsify:** Not applicable (design). If honest charging later shows TNN losing everywhere, that is a result to report, not a design failure.

**Dependencies:** None for design. Running needs baseline access and is a separate future question.

**Status:** ACTIONABLE NOW (design).

---

## Q17. Node-budget scaling: retention versus capacity law

**Question:** The transfer analysis used the 1024-node budget. Vary the budget (256, 512, 1024, 2048, 4096) on an unfrozen variant under an identical interference stream and measure: retention of useful structures on revisit probes, reuse event frequency, onset of catastrophic forgetting. Is there a scaling law? Does more capacity help, or does the eviction/fossil/garbage pathology scale with it?

**Why it matters:** This cheaply discriminates two hypotheses: if the pathology scales with capacity, the fix is architectural (Q4), not more memory. If 4096 nodes eliminate forgetting, capacity was the binding constraint. Do not spend a year on Q4 if the answer is capacity.

**Confirm:** A measured curve across the five budgets with the pathology characterized at each point.

**Falsify:** If 4096 nodes eliminate forgetting and fossils, the memory problem was capacity all along (unlikely given the fossil mechanism, but it must be checked, not assumed).

**Dependencies:** None.

**Status:** ACTIONABLE NOW.

---

## Q18. Contradiction that demands new structure (beyond MAP retargeting)

**Question:** Copy-and-commit plus MAP retargeting (Q5) handles contradictions resolvable within existing structure. What about contradictions that require inventing new structure: a new node type, a new relation, a new hypothesis object the current ontology lacks? Design the minimal structural-invention-under-contradiction experiment: can the learner create what it does not have when the contradiction proves the current ontology insufficient? Execute on the Q5 substrate once it exists; design now in parallel.

**Why it matters:** Lifetime revision will encounter ontology-breaking evidence. Retargeting is not invention. This probes the L3 frontier directly: representational invention under pressure, with a white-box creation trace. It is also the natural sequel to Q5: safe revision first, inventive revision second.

**Confirm:** Sealed test where the only resolution requires a structure type absent from the pre-contradiction state; white-box shows the creation trace and the triggering contradiction.

**Falsify:** If the learner only ever retargets or fails (the expected current outcome), structural invention under contradiction is absent. That maps the boundary honestly and scopes future work; it does not authorize adding researcher-authored structure types (the treadmill).

**Dependencies:** Q5 substrate for execution; design independent.

**Status:** Design ACTIONABLE NOW; execution follows Q5.

---

## Worker assignment notes

- Highest information gain per unit work right now: Q1 (unblocks the lifetime paradigm), Q2 (the core transfer blocker), Q6 (makes the SUF gate concrete).
- Cheapest discriminating experiments: Q17 (budget scaling), Q10 (census), Q15 (audit).
- Do not assign Q12 implementation until Micah's freeze go; prep work is fine.
- Q3's pre-commitment tree can be built before H2 results land.
- Every experimental question uses unfrozen variants; frozen TNN-2 (`tnn2.zag`, `tnn2_bin`, build `f4de7ff46`) is never modified.
- Every mechanism report must include Micah's 12-field standing metric.
