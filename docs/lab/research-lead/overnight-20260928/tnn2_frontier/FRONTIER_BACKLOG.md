# TNN-2 Next-Frontier Research Backlog

Scout: TNN-2 Next-Frontier Scout. Date: 2026-10-01 (overnight).
Context: TNN-2 is frozen (src `a29972ca8183`, bin `6044f91f8fe3`, 1591 lines) with three new mechanisms: (A) runtime executable-graph construction via the t2_trial propose/execute/verify/promote loop over the frozen 4-op ISA; (B) miss to uncertainty to guide to POLICY_ROOT to ACT inquiry; (C) counterexample-driven executable-graph revision (`revise_on_contradict`). Build verdict is BUILD-PASS, not SURVIVES.

North star (Micah): "Can one frozen general architecture create, execute, revise and reuse cognitive structure its programmers did not supply, and thereby become capable in genuinely new worlds without source-code changes?"

Ranking principle: information gain first. A question ranks high if its answer would redirect the research program (kill a mechanism, force an architecture review, or unlock a frontier), and if it is experimentally discriminable under the frozen-ISA, pure-Zag, preregistered-kill-bar regime. No question below proposes a per-world patch, a new opcode, a new mode/bridge/handler, or benchmark-specific machinery. A negative answer to any question is a finding, not a request for a fix.

The 17 questions are grouped: Q1-Q5 test whether TNN-2's three mechanisms are genuine or theater (highest information gain); Q6-Q9 test generality and fair evaluation; Q10-Q13 test architecture convergence and developmental integration; Q14-Q17 test compression, learner authority, and hygiene.

---

## Q1. Is the revision operator genuinely general, or is it a "replace the bad MAP step" procedure wearing general clothes?

**The question.** `revise_on_contradict` is described as: find licensing MAPs, tombstone the stale SETREG step, insert a corrected step, rewire the GUARD. The build report's single revision test (`t_t2_revise`) demonstrates exactly one repair topology. What part of the repair topology was actually chosen by the learner, and can the SAME operator derive structurally different repairs: a loop-bound change, a branch retarget, a multi-step insertion, a topology reshaping, a repair that removes rather than adds?

**Why it matters.** Frontier: procedure invention (revision half), L3 criterion C0. Mechanism C is the load-bearing half of mechanism A: construction without general revision just moves the FW3 failure into the continuing learner, as the root-cause analysis states. If revision is one researcher-authored repair shape, TNN-2 has a repair procedure, not a revision capability. This is the question Micah's overnight brief singles out for the most aggressive review.

**What positive/negative establishes.** Positive: the same operator, with no new code, derives at least three structurally distinct repair topologies on sealed counterexamples, and white-box traces show the learner choosing the topology (which step to tombstone, what to insert, how to rewire) rather than executing a fixed script. That is evidence that revision is learner-driven and general. Negative: only the demonstrated MAP-step swap works; other counterexample shapes either fail or silently reduce to the same swap. That means mechanism C is a researcher-authored repair procedure and must be redesigned toward learner-chosen repair topology, not patched with more repair shapes.

**Experimental discrimination.** Yes. Design sealed counterexample batteries after the freeze, each requiring a different repair topology for a promoted graph (branch retarget vs step swap vs loop-bound change vs insertion vs deletion), authored by an adversary who sees the public architecture claim but not the builder fixtures. Preregister: success requires the learner's trace to show topology choice (e.g., which edge was rewired and why the alternatives were rejected), not just a correct final answer. A correct answer with a fixed repair script is a FAIL on the process criterion.

---

## Q2. Is the trial loop open construction, or search over a finite researcher-authored family?

**The question.** `t2_trial` searches in a fixed order: chains k=2..4, then sums, then counts, then single hops, with BFS depth 1-4, unrolled INC cells, and a frozen composition preference. Is this genuine open construction of executable structure, or a larger finite menu than TNN-1's three templates? Can it build anything outside its four search phases: nested loops, two-branch graphs, chains longer than 4 hops, CALL-composed subroutines, structures whose depth or shape appears in no builder test?

**Why it matters.** Frontier: procedure invention, L3 criterion C0-B (open structural form). This is the C0-B test for mechanism A. A constructor capped at a researcher-enumerated family is L2 structural learning at best, no matter how large the family. The MUL Rung B result (primitive basis to learner-built ADD to learner-built MUL via CALL) suggests hierarchy is possible; the question is whether the integrated trial loop preserved that openness or froze it into phases.

**What positive/negative establishes.** Positive: on sealed worlds requiring non-isomorphic structures (e.g., a traversal with a nested inner loop, a 6-hop chain, a program that calls a previously promoted graph as a subroutine), the learner assembles novel graphs with genuine rejections recorded, and no complete successful graph existed in source. That is C0-B evidence for construction. Negative: capability ends exactly at the phase boundaries (works at depth 4, fails at depth 5; works for sums, fails for a structure needing a branch the phases never emit). That means the trial loop is a bigger menu, and the frontier is proposal machinery that is itself learner-driven rather than a frozen search order.

**Experimental discrimination.** Yes. Sealed worlds requiring structures outside each phase boundary, one boundary at a time, plus one world requiring a shape in no phase. Measure not just pass/fail but the trial trace: count of genuine rejections before the winner (the build already instruments tried/rejected counts in header field 16), and whether the winning graph's topology was reachable by the search phases at all. A win by a graph the phases could not emit is the strongest positive.

---

## Q3. Can the learner hold multiple competing structures under ambiguity and revise through successive counterexamples, including reverting?

**The question.** The MUL Rung B 0/4 result and the root-cause analysis both point at revision as a lifecycle, not an event. Can TNN-2: (a) maintain two or more candidate graphs for the same miss when evidence is ambiguous, rather than collapsing to one; (b) revise a promoted graph twice in a row as new counterexamples arrive; (c) revert to an earlier graph regime when the environment reverts (the FW4 law-change/revert pattern, but for procedures instead of facts)?

**Why it matters.** Frontier: procedure invention, causal invention, Level E (correction/revision) of the pattern-matching program, and the innovation standard's revise-retire requirement. Real environments change their regularities; a learner that can revise once but not twice, or that cannot keep a superseded-but-possibly-returning structure, is doing one-shot repair. This is also the direct descendant of the MUL Rung B 0/4 wall, now inside the continuing learner where it belongs.

**What positive/negative establishes.** Positive: the learner keeps competing candidates with standing-like differentiation, applies successive topological revisions, and reverts to a prior graph when evidence reverts, all visible in learner state. That is a genuine executable-structure lifecycle and Level E evidence. Negative: the first revision destroys the alternative (tombstoning as deletion rather than supersession), the second counterexample fails, or revert requires relearning from scratch. That locates the missing piece: a versioned or hypothesis-structured executable memory, which is a general architectural gap, not a per-world fix.

**Experimental discrimination.** Yes. A sealed sequence: teach regularity R1, promote graph G1; introduce ambiguous evidence consistent with R1 and R2 (measure whether two candidates coexist in state); disambiguate to R2 (measure revision to G2 and whether G1's structure is preserved or destroyed); revert the environment to R1 (measure whether G1 is reactivated vs rebuilt). Each transition is a separate preregistered bar. White-box state inspection distinguishes reactivation from relearning.

---

## Q4. Can a promoted executable graph transfer across changed surface representation and be reused cross-domain?

**The question.** Promoted graphs carry provenance edges to specific licensing facts. Is a promoted graph a brittle license bound to its training facts, or a reusable cognitive structure? If the same regularity appears with new symbols, new key ranges, or a different domain encoding, does the learner reuse the graph (zero-shot or few-shot), or does it rebuild from scratch through the full trial loop?

**Why it matters.** Frontier: transfer/reuse (pipeline step 9), L3 criterion C0-D (cognitive reuse: the invented structure must improve transfer, prediction, procedure learning, or sample efficiency), and the innovation standard's transfer requirement. C0-D is conjunctive with the other three; construction and revision without reuse is clever search, not cognition. This is also the fairest test that the graph is a structure and not a memorized answer with extra steps.

**What positive/negative establishes.** Positive: a graph promoted in domain A accelerates learning or directly solves an isomorphic task in domain B with changed surface form, with the reuse visible as graph invocation (CALL or equivalent) rather than re-derivation. That is C0-D evidence and justifies calling the graphs cognitive structure. Negative: every new surface requires full re-trial with no speedup, or reuse attempts produce wrong answers because the graph is overfit to its licensing facts. That means provenance binding is too tight and the frontier is a general abstraction/separation mechanism between graph structure and its licensing evidence, which must be learner-driven to count.

**Experimental discrimination.** Yes. Teach to promotion criterion in domain A; then present an isomorphic regularity in domain B with disjoint symbols/keys and no additional training on the underlying operation; measure trials-to-criterion in B vs a naive control learner with no graph from A, plus a surface-scrambled control. Preregister the speedup or zero-shot bar. Inspect whether B's solution path references A's graph node.

---

## Q5. Can the learner invent a reusable abstraction with runtime-defined semantics, or is the representational ceiling the four frozen ops?

**The question.** The 4-op ISA (MOVE/BRANCHEQ/INC/DEC) has researcher-defined semantics; the learner arranges cells but never defines what a cell means. Can the learner recruit a new useful primitive: a composite (e.g., a repeatedly used multi-cell pattern) that becomes a named, reusable unit with semantics residing in learner-created state, where source holds only the generic construction machinery? This is the representational-invention frontier, the hardest L3 test.

**Why it matters.** Frontier: representation invention, L3 criterion C0-A (runtime-defined semantics: the new cognitive object's semantics must reside in learner-created persistent state; a dedicated pre-written semantic case kills the claim). Micah's highest-priority frontier is the generic executable representation substrate with learner-authored representation semantics. Everything TNN-2 does is arrangement of given semantics; C0-A asks whether meaning itself can be learner-authored. A positive answer here is the single highest-value discovery in the program.

**What positive/negative establishes.** Positive: in a sealed world where a composite pattern recurs across tasks, the learner creates a persistent abstraction node, reuses it in new graphs, and ablation of the abstraction node (not the graphs) destroys the advantage while ablation of any single graph does not. The abstraction's semantics exist only as learner state plus the generic executor. That is C0-A evidence and genuine L3 territory. Negative: the learner never compresses recurring patterns into reusable units, or any "abstraction" is traceable to a researcher-authored template. That confirms the representational ceiling and points the next generation at the invention mechanism itself, which is a different research problem than better search.

**Experimental discrimination.** Yes but hard. Requires sealed worlds designed after the freeze where a non-obvious composite recurs, with the composite not isomorphic to multiplication or any builder-fixture pattern. Bars: (1) the abstraction appears in persistent learner state after experience, not before; (2) white-box trace explains its creation from recurring substructure; (3) reuse across at least two new tasks; (4) ablation of the abstraction destroys the advantage; (5) no source semantic case covers it. All five are individually checkable in pure Zag with state dumps.

---

## Q6. Does the trial loop's search cost scale tractably, and how does it compare against serious baselines on sample and compute?

**The question.** The trial loop is search: BFS paths, phase-ordered candidate assembly, execute-and-verify with genuine rejections. What is its cost scaling law as required structure depth/complexity grows? And on identical construction tasks, how do its sample efficiency (observations to criterion) and compute (candidate executions) compare against serious baselines: exhaustive search over the same 4-op space, a memorization control, and a capable non-crippled LLM baseline given the same observations?

**Why it matters.** Frontier: fair evaluation (the TNN-vs-LLM arena requirements: capable baseline, measured capabilities, honest resource charging, capability curves). The mandate demands capability/cost advantages against serious baselines, not benchmark wins. If the trial loop's cost explodes combinatorially past depth 5, TNN-2's construction is a demo-scale phenomenon and the frontier is proposal efficiency, not more search. If it is sample-efficient relative to baselines, that is a real, quotable advantage.

**What positive/negative establishes.** Positive: sub-exponential cost scaling to the depths tested, and better sample efficiency than the baselines at equal or lower compute. That supports the north star's cost-advantage clause. Negative: combinatorial blowup, or a simple exhaustive search matches it, or the LLM baseline learns the same regularities from fewer observations. A negative on the baseline comparison does not kill the architecture, but it reframes the claim: TNN-2's advantage must then be found in revision, persistence, or integration rather than raw construction efficiency, and the next experiments should measure those instead.

**Experimental discrimination.** Yes. Instrument the trial loop's tried/rejected counts (already in header field 16) across parametric task families of increasing structural depth; fit the scaling curve. Run the three baselines on the same task families with preregistered metrics (observations to criterion, candidate executions, wall-clock on comparable hardware). The arena rules require the LLM baseline be capable and non-crippled; document its prompting and charge its pretraining honestly as context, not as a trick.

---

## Q7. Can constructed graphs drive multi-step action sequences with environmental feedback and replanning?

**The question.** TNN-2 converged query-path construction (mechanism A) and act-path inquiry (mechanism B) partway: FW7 needs both a constructed action sequence and a live act channel. Can the learner construct an executable graph whose steps are actions, emit them through ev_act/POLICY_ROOT, observe the resulting state transitions, and replan (revise the action graph) when the environment deviates? Or does the architecture still split into query-graphs that answer and act-guides that select?

**Why it matters.** Frontier: developmental integration, planning, procedure/action convergence. Micah's doctrine is that procedure and plan converge on one executable graph type. If constructed graphs cannot act and act-guides cannot be constructed by the trial loop, the convergence is aspirational and the architecture still has two output systems. Planning is also the capability most directly tied to the north star's "become capable in genuinely new worlds."

**What positive/negative establishes.** Positive: a sealed planning world where the learner builds an action graph, executes it stepwise through the act channel, hits a blocked transition, revises the graph (mechanism C on an action graph), and reaches the goal. Query construction, inquiry, action, and revision all operating on the same graph type is the strongest integration evidence available. Negative: action graphs cannot be emitted, or feedback cannot trigger revision of an action graph, or planning works only for action sequences the trial loop's query phases happen to emit. That identifies the exact missing link (graph-to-action emission, or feedback-to-revision routing) as the next architectural target.

**Experimental discrimination.** Yes. Sealed grid/transition worlds with: a goal requiring a multi-step novel route (not a memorized transition chain), a mid-execution blockage requiring replan, and a distractor goal testing that the plan is goal-conditioned. Preregister bars on route novelty, replan success, and graph-type unity (the replanned structure must be the same 4-op graph type, inspected in state).

---

## Q8. Under memory pressure, does a learner-owned retention policy protect useful executable structures?

**The question.** This is Micah's standing memory question in its TNN-2 form: "What general learner-owned memory representation/policy would let one frozen learner preserve newly useful knowledge, dependencies, hypotheses and structures without task-specific storage logic?" As the continuing learner accumulates promoted graphs, uncertainty nodes, guides, and facts under bounded state, which structures survive? Is there a general, learner-owned retention policy (usefulness, dependency tracking via the existing ET_DEP provenance edges, recency, verification history), or does pressure cause arbitrary loss, starting with the most valuable graphs?

**Why it matters.** Frontier: memory, developmental integration, interference. A continuing learner that cannot manage its own memory under pressure is not a continuing learner; it is a long episode. The provenance edges (ET_DEP from cells to licensing facts) are a candidate substrate for dependency-aware retention, but nothing in TNN-2 uses them for retention decisions. This question also subsumes the "store/eviction must not become a cache-policy treadmill" ruling: the answer must be a general policy, not a tuned cache.

**What positive/negative establishes.** Positive: under engineered memory pressure, the learner preferentially retains graphs with live dependents, recent verification success, and cross-task reuse, while shedding stale facts and superseded graphs; retention correlates with a learner-computed usefulness signal, not insertion order. That is evidence for a general learner-owned memory policy. Negative: pressure evicts arbitrarily (e.g., oldest-first destroys the foundation graphs everything depends on, or newest-first destroys yesterday's learning), or retention requires a researcher-written priority scheme. That forces the memory-policy question into the next generation as a first-class architectural problem.

**Experimental discrimination.** Yes. Long-horizon runs: teach a sequence of construction tasks with dependencies (later graphs CALL earlier ones), then impose state bounds and continue teaching; measure retention of dependency-critical graphs vs disposable facts, and post-pressure retest scores on old tasks. Compare against trivial policies (FIFO, LIFO, random) as controls. The policy, if any, must be read off learner state and learner operations, not researcher code paths.

---

## Q9. Does inquiry select genuinely discriminating questions, and can it resist locally attractive but uninformative probes?

**The question.** Mechanism B creates an uncertainty node and a guide for the miss subject, and ev_act selects the inquiry act. But which question does the learner ask? In the current design the guide is built with choice 30 (the inquiry act) for the miss subject. Under ambiguous or misleading evidence, does the learner derive a discriminating need (ask the question whose answer would most reduce uncertainty over candidate structures), or does it emit a fixed probe? When the locally attractive question is uninformative or actively misleading, does it still ask it?

**Why it matters.** Frontier: active inquiry, Level D (self-directed evidence: the learner must act to obtain missing information). Level D is the program's explicit inquiry frontier, and the overnight brief demands inquiry be attacked with ambiguous and misleading evidence. An inquiry system that cannot choose what to ask is a notification system, not active inquiry. This also tests the full causal chain the brief requires: miss to uncertainty to discriminating need to guide to POLICY_ROOT to ACT to evidence updating later behavior.

**What positive/negative establishes.** Positive: on sealed worlds where candidate structures disagree on specific probes, the learner's inquiry act targets the disagreed-upon probe (visible as the guide's role/payload tracking the discriminating dimension), avoids the attractive-but-uninformative probe, and later trial-loop proposals reflect the returned evidence. That is genuine active inquiry. Negative: the guide always probes the miss subject identically regardless of which evidence would discriminate, or misleading evidence derails construction permanently. That reduces mechanism B to miss-notification and puts discriminating-question selection on the frontier.

**Experimental discrimination.** Yes. Adversary-designed worlds with: two candidate structures consistent with current evidence but disagreeing on probe P1 while agreeing on the attractive probe P2; and a world where the obvious probe returns misleading evidence (true in the probe context, false in general). Bars: probe choice distribution across runs, post-inquiry construction success, and recovery from misleading evidence. The adversary must not know the builder fixtures, only the public claim.

---

## Q10. Do causal rules and procedures actually share one executable graph type, or does causal cognition still run on separate machinery?

**The question.** Micah's doctrine: procedure and causal rule converge on the same executable graph type with different evidence/lifecycle edges. TNN-2 unified query plans and the 4-op ISA, but causal machinery (trial-based P-DEP from CAM-1, edge-derived standing) predates TNN-2 and was integrated under a separate lane. Can a causal regularity (intervention X leads to outcome Y under conditions) be learned as a 4-op executable graph through the same t2_trial machinery, with causal evidence carried on lifecycle edges rather than in a separate causal engine? Or does causal learning still require its own representation?

**Why it matters.** Frontier: causal invention, architecture convergence, the One-System Rule. If causal rules need separate machinery, the architecture is accumulating subsystems (the exact failure mode the One-System Rule forbids), and the "same graph type" doctrine is unmet. If they converge, one mechanism covers prediction, procedure, and causal intervention, which is the kind of unification the north star rewards.

**What positive/negative establishes.** Positive: intervention-outcome regularities are acquired as executable graphs via the trial loop, with causal semantics (intervention vs observation, confounding control) represented as edge types and verification regimes on the same graph type. That is doctrine-satisfying unification. Negative: causal tasks require the separate P-DEP path and cannot be expressed as constructed graphs, or the attempt produces graphs that predict but cannot guide intervention. That triggers the architecture-review question Micah posed: "Why can the existing general architecture not learn this behavior?" with causal intervention as the exhibit.

**Experimental discrimination.** Yes. Sealed causal worlds: regularities learnable from observation alone vs ones requiring the learner to choose interventions (Level D for causality); confounded regularities where observation-only graphs fail but intervention-conditioned graphs succeed. Bars: acquisition through the trial loop (not the legacy causal path), intervention success rate, and graph-type inspection confirming the same 4-op representation.

---

## Q11. Can the learner detect systematic constructor failure and widen its own search, or is the search order frozen researcher bias?

**The question.** The trial loop's search order (chains, then sums, then counts, then single hops; BFS depth 1-4; frozen composition preference) is researcher-authored. The rejection counts are instrumented but nothing reads them. When the constructor fails repeatedly on a world family, can the learner adjust its own search (deepen BFS, reorder phases, relax the composition preference), or does it fail identically forever? This is learner authority over mechanism A itself.

**Why it matters.** Frontier: learner authority, procedure invention, meta-cognition. A constructor the learner cannot steer is a researcher tool the learner happens to run. The north star asks for structure "its programmers did not supply"; the search strategy is currently 100 percent supplied. Even a small amount of learner-driven search control (e.g., promoting a phase that recently succeeded) would be evidence that the learner owns the construction process rather than renting it.

**What positive/negative establishes.** Positive: across a family of worlds, the learner's search behavior adapts based on its own rejection/verification history (e.g., phase reorder after repeated phase-1 failures, deepening after near-misses), measurably reducing trials-to-solution on later worlds of the family. That is learner-owned construction strategy. Negative: search behavior is identical on world 50 as on world 1, with adaptation (if any) traceable to researcher-written heuristics. That keeps search strategy on the researcher side of the ledger and defines the next mechanism precisely: a learner-writable search policy over the frozen ISA.

**Experimental discrimination.** Yes. Families of sealed worlds sharing a structural signature that the default search order handles poorly (e.g., all solutions are counts, which the default order tries third). Measure trials-to-solution across the family sequence; a learner-owned policy shows a decreasing curve, a frozen policy shows a flat one. Control: shuffle the family order to rule out task-easiness confounds. The adaptation signal must be in learner state, not in code.

---

## Q12. Do honest simple baselines match the trial loop, and what exactly is the trial loop's irreducible contribution?

**The question.** Pipeline step 5 (simple-baseline comparison) and step 6 (alternative-explanation attack) are still open for TNN-2. Does exhaustive search over the 4-op ISA up to the same depth bound, or a memorization-plus-nearest-neighbor control, achieve the same construction tasks with comparable observations and compute? Is the trial loop's contribution the search, the verification regime, the promotion/lifecycle machinery, or the integration into the continuing learner?

**Why it matters.** Frontier: fair evaluation, alternative-explanation attack, honest capability accounting. Every mechanism must survive the "simpler explanation" attack before any strong claim. If exhaustive search matches the trial loop, then TNN-2's construction is brute force with good PR, and the real research question becomes proposal efficiency (Q6/Q11), not construction per se. If the trial loop wins, decomposing where it wins tells the next generation what to keep during compression (Q14).

**What positive/negative establishes.** Positive (for TNN-2): the trial loop beats exhaustive search on trials-to-solution and beats memorization controls on novel-structure generalization, with the gap attributable to specific components (e.g., the phased proposal order, the masked/unmasked verification regime). That decomposes the mechanism into keepable parts. Negative: a baseline matches it. That is not a kill of the program, but it demotes mechanism A from "construction breakthrough" to "adequate search," redirecting effort to revision (Q1), reuse (Q4), and invention (Q5) as the differentiators.

**Experimental discrimination.** Yes. Implement the baselines in pure Zag against the same frozen ISA and the same task families: exhaustive bounded search, memorization control, nearest-neighbor over taught facts. Preregister the metrics (observations to criterion, candidate executions, novel-structure generalization rate). The baselines must be genuinely attempted, not strawmen; document their tuning.

---

## Q13. Does learning new executable structures interfere with old ones: retention, corruption, or peaceful coexistence?

**The question.** In a continuing learner with no reset, the learner will promote dozens of graphs. Do they coexist? Specifically: does promoting graph G2 corrupt, displace, or degrade G1 (shared cells, overwritten literals, provenance-edge confusion)? Does revising G1 break G2 that CALLs it? After a long heterogeneous sequence, do early capabilities survive (the developmental-integration requirement: one learner experiencing many things with no process reset)?

**Why it matters.** Frontier: developmental integration, interference, memory. This is the dark twin of Q8 (which asks about retention under pressure): Q13 asks about corruption without pressure. The continuing-learner requirement is explicit in Micah's program: one persistent learner, no task labels, no recompilation. If each new construction risks breaking old ones, the architecture has a structural-isolation gap, and scaling to a real continuing learner is blocked regardless of how good construction is.

**What positive/negative establishes.** Positive: sequential construction tasks show no retrograde degradation; revision of a called graph either preserves callers' behavior or propagates correctly; interference metrics stay flat across long sequences. That is genuine developmental-integration evidence. Negative: measurable interference (e.g., retest scores on old tasks decay as new graphs are promoted, or revising a subroutine silently breaks its callers). That identifies structural isolation (namespaces, copy-on-write, dependency-aware revision propagation) as a required general mechanism, and it must be learner-managed to satisfy the One-System Rule.

**Experimental discrimination.** Yes. Sequences of unrelated construction tasks with periodic retests of all prior tasks; targeted experiments where a revised graph is CALLed by another promoted graph (does the caller see the revision, the old behavior, or corruption?). Metrics: retest accuracy curves, caller-consistency checks, state-diff analysis attributing any degradation to specific shared structure.

---

## Q14. Which researcher-authored machinery can be deleted while preserving the new capability?

**The question.** TNN-2 is 1591 lines, up 263 from the TNN-1 base, and the 1200-line ceiling remains a failed axis. The overnight brief orders a separate compression investigation after evidence collection: which machinery is load-bearing? Candidates: the P-INV bootstrap vs the trial loop (is the bootstrap redundant now?), the frozen phase order vs a simpler uniform search, the masked/unmasked dual verification regime, the composition-preference preservation, the literal 902-node convention, the guide-building code vs a more general candidate-emission path.

**Why it matters.** Frontier: architecture compression, beautiful architecture. Micah's scoring dimensions include ARCHITECTURAL COMPRESSION and LEARNER AUTHORITY alongside capability. A mechanism that survives only as 263 lines of researcher-authored scaffolding is less evidence of learner capability than the same behavior from a smaller core. Compression is also the forcing function for generality: deleting a component and watching capability survive proves the component was not the source of intelligence.

**What positive/negative establishes.** Positive: large deletions (whole components, not lines) with capability preserved on both the regression battery and fresh sealed worlds. Each surviving deletion is evidence about where the capability actually lives, and it directly serves the target (capability up, researcher machinery down). Negative: every deletion degrades fresh-world capability, meaning the 263 lines are all load-bearing researcher intelligence. That is an honest, quotable result too: it says the current capability/source-delta ratio is poor and the next generation must find a smaller sufficient core, not add to this one.

**Experimental discrimination.** Yes. Systematic ablation: remove or stub each candidate component, rerun the frozen regression battery plus a held-out fresh-world set, and record the capability delta per deleted line/function/template. Track the full accounting ledger the brief requires (cognition lines, functions, fixed semantic cases, modes, bridges, handlers, fixed candidate templates, learner-created structures, fresh-world capability, transfer, revision, interference). Ablation must be preregistered per component with a predicted outcome to prevent post-hoc storytelling.

---

## Q15. Can the learner define its own verification criteria, or is the verifier a researcher-written oracle?

**The question.** The trial loop verifies by researcher-written rules: unmasked output must equal expected, masked queries take the first non-sentinel. The verifier is an oracle the learner cannot question or modify. Can the learner ever determine for itself what counts as success: inferring the success criterion from sparse feedback, from environmental consequences of its actions, or from the structure of the inquiry that motivated the construction? Or is learner cognition permanently bounded by researcher-specified correctness?

**Why it matters.** Frontier: learner authority, representation invention, the deepest form of the "structure programmers did not supply" clause. If the verifier is fixed, then every constructed graph is a solution to a researcher-posed problem, and C0-B (open structural form) is bounded by C0-researcher (closed success criteria). Genuine open-ended learning needs learner-driven success criteria; otherwise the architecture is a powerful solver of given problems, not an inventor of its own.

**What positive/negative establishes.** Positive: sealed worlds where the success criterion is not stated but must be inferred (e.g., the environment rewards a consequence the learner must discover, or the criterion shifts and the learner tracks it), and the learner constructs graphs satisfying the inferred criterion, with the criterion itself visible in learner state. That extends learner authority from structure to purpose. Negative: the learner can only optimize researcher-given criteria, and inferred-criterion worlds fail uniformly. That draws the current boundary of learner authority precisely and makes verifier-generalization a named next frontier rather than a vague aspiration.

**Experimental discrimination.** Yes but hard. Design sealed worlds with latent success criteria discoverable only through action consequences (e.g., an action graph succeeds iff a downstream state persists, where persistence is observable but unstated). Bars: the learner's verification behavior must differ across worlds with different latent criteria (proving the criterion is inferred, not fixed), and the inferred criterion must be inspectable in learner state. Control worlds with stated criteria must still pass.

---

## Q16. Can the learner perform representational expansion for a genuinely new abstraction P that arithmetic never anticipated?

**The question.** The innovation standard's representational-expansion requirements (detect/create/use/persist/reuse/transfer/revise-retire P, with the researcher forbidden from adding P) have so far been exercised near arithmetic (ADD, MUL, counts, chains). Can the learner do it for a domain whose useful abstraction is not anticipated by arithmetic examples: e.g., a parity-like invariant, a temporal ordering pattern, a containment hierarchy, or a synthetic relational role? The post-freeze battery explicitly demands "a domain whose useful abstraction was not anticipated by arithmetic examples."

**Why it matters.** Frontier: representation invention, L3 C0-C (multiple unforeseen forms: at least one evaluation family designed by an independent adversary after freeze). TNN-2 was designed after observing TNN-1's failures, so FW1-FW9 success cannot establish generality (the brief says this explicitly). C0-C is the antidote: sealed, adversary-designed, post-freeze families requiring materially different representations. This question is the program-level version of that requirement.

**What positive/negative establishes.** Positive: the learner detects, creates, uses, persists, reuses, transfers, and revises-or-retires a genuinely novel abstraction P in an adversary-designed domain, meeting all seven representational-expansion requirements with no researcher-added P. That is the strongest generality evidence the program can produce short of full L3. Negative: the learner succeeds only when P is arithmetic-shaped and fails on non-arithmetic abstractions, revealing that the "general" constructor is actually an arithmetic-structure constructor. That would be the most important negative result of the cycle: it would show TNN-2's generality is domain-shaped, and the next generation must find the actual general substrate.

**Experimental discrimination.** Yes. This is precisely what the post-freeze adversarial battery is for. Require the adversary to author at least one domain whose natural abstraction is non-arithmetic and non-isomorphic to any builder fixture, seeing only the public architecture claim. Preregister the seven expansion requirements as separate bars. Score representation generality separately from task success.

---

## Q17. Should the two documented EXECUTE deviations be closed, and does learner-visible execution budget change anything?

**The question.** The CORE-FREEZE-TNN1 cycle recorded two deviations in the approved EXECUTE placement: the execution budget is a code literal rather than learner-visible state, and the specified INC/DEC kind guard is absent. The root-cause analysis deliberately deprioritized them as hygiene, not capability fixes. Now that the executor runs learner-built graphs in the cognition path (not just tests), does closing them matter: would a learner-visible budget enable the learner to reason about or adapt its own computation cost, and does the missing kind guard create a soundness hole the trial loop could exploit or trip on?

**Why it matters.** Frontier: architecture hygiene, learner authority over computation, the cost-awareness half of the capability/cost mandate. This is the lowest-information question in the backlog, included for completeness because the deviations are on the books and the executor's promotion to the cognition path changed their significance. A learner that cannot see its own compute budget cannot learn cost-aware strategies, which the north star's cost clause may eventually require.

**What positive/negative establishes.** Positive: making the budget learner-visible enables measurable cost-adaptive behavior (e.g., the learner prefers cheaper graphs when both verify, or aborts unpromising trials early based on budget state). That would promote a hygiene item to a capability lever. Negative: no behavioral change, confirming the deprioritization was correct and the deviations can stay closed-or-open as pure engineering. Either way the item leaves the books.

**Experimental discrimination.** Yes. Expose the budget as learner state in an experimental (non-frozen) branch, keeping the frozen TNN-2 untouched; test whether trial-loop behavior or graph selection changes on cost-differentiated task pairs. The kind guard can be tested by adversarial graph shapes that would violate it. Small, bounded, reversible experiments only.

---

## Cross-cutting notes for whoever works this backlog

1. Order of attack by expected information per unit effort: Q1, Q2, Q12 form one natural red-team cluster (are the mechanisms real?); Q4, Q5, Q16 form the L3 cluster (C0-D, C0-A, C0-C); Q6 is the fair-evaluation cluster; Q3, Q7, Q8, Q13 form the continuing-learner cluster; Q10, Q11, Q15 probe learner authority and convergence; Q14 is the compression program; Q17 is hygiene.
2. Every experimental question above needs its own preregistration with frozen kill bars before world exposure, per the standing governance. The post-freeze adversarial battery already authorized covers Q1, Q2, Q5, Q9, Q10, Q16; the remaining questions need their own adversaries or experimental designs.
3. Negative answers are findings. A negative on Q2 or Q16 is more valuable than a positive on Q17. Do not convert negatives into patch requests; cluster them by shared architectural cause per the standing rule.
4. The 11-step promotion pipeline applies to any mechanism that emerges from this backlog. Nothing here is SURVIVES; nothing here is even BUILD-PASS. These are questions, not claims.
5. Lineage: this backlog derives from the TNN-2 build report (commit `f4de7ff46`), the CORE-FREEZE-TNN1 root-cause analysis (commit `ed38121d4`), the CORE-FREEZE-TNN2 preregistration (commit `ce1a7c5f8`), Micah's L3 criteria (C0-A/B/C/D), the L0-L3 taxonomy, the innovation-testing standard, the Levels A-E program, and the overnight north-star brief. It proposes no opcodes, no modes, no bridges, no handlers, and no per-world patches.
