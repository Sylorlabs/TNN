# W6/W7 Capability Analysis: The Action-Selection Gap

## Verdict: W6W7-ANALYSIS-COMPLETE

**Date:** 2026-09-30
**Analyst:** W6/W7 Capability Analyst (subagent)
**Scope:** W6 (active inquiry) FAIL and W7 (planning) FAIL from the Core Freeze Challenge run phase (97b28e6a6).

## Step 0 Name-Check

The standing rules from LOOP_STATE.md that apply are: (1) PURE ZAG ONLY. This is analysis and documentation work. I write pure markdown, use shell commands only, and invoke no Python for any purpose. (2) Shell-only byte checks. Dash hygiene is verified with the shell-only check_no_dash.sh snippet, never python3. (3) Fork testing and the image-judge rule are not applicable to capability analysis. (4) Commits stay local. Owned paths only (w6w7_analysis/), explicit pathspecs on add and commit, git status inspected before committing, the contaminated paper (TNN_RESEARCH_PAPER_20260929.md) left untouched. This paragraph was written before any analysis work began.

## Source Materials

W6 world files (worlds_adversary/):
- w6_phaseA.txt (7 lines): context OBSERVEs, decoy ACT, diagnostic QUERY 22001 22101 -2, OBSERVE, inquiry ACT.
- w6_phaseB.txt (7 lines): OBSERVE 22001 22101 7 (the reveal), distractor, task probes.
- w6_controlA.txt, w6_controlB.txt: passive control, ACT lines removed.
- DESIGN_WORLDS_ADVERSARY.md section 3: full functional spec, frozen bars B1-B4, mechanism-level argument 3.5.

W7 world file (worlds_prefreeze/):
- W7_world.txt (42 lines): 10 transition-model OBSERVEs (relations 621/622), then 4 instances each with start OBSERVE, 2 ACTs, perturbation OBSERVE, 4 ACTs.
- DESIGN_WORLDS_PREFREEZE.md section W7: frozen bars, grader simulation, predicted FAIL with mechanism-level reason.

Run outputs (run_phase/battery/):
- W6phaseA.out: CHOICE 0 emitted for both ACTs; ANSWER 22001 22101 -2 (correct ignorance admission); reveal triple EVICTed before probes.
- W7.out: all 24 ACTs emit CHOICE 0; transition triples EVICTed as taught; 0/4 instances reach goal 9704.

Run results (run_phase/RUN_RESULTS.md):
- W6: FAIL (B4 attribution). Treatment 1/5 (0/3 vault); Control 0/5. C1 eviction confound documented.
- W7: FAIL 0/4. All CHOICE 0. CONFIRMS predicted failure.

## W6 Findings: Active Inquiry

### What the world tests

W6 withholds the vault code (22001, 22101). The value 7 is provably unobtainable by passive observation. The treatment arm releases a reveal OBSERVE only if the binary outputs "ANSWER 22001 22101 -2" followed by "CHOICE 0" in output order. The control arm (no ACT lines) gets no reveal. Frozen bars: B1 treatment at least 80 percent on task probes; B2 control at most 15 percent; B3 actions measurably reduce uncertainty, not random; B4 the inquiry strategy is learner-determined, no source logic branches on world identity.

### Observed behavior

The binary emitted CHOICE 0 for both the decoy ACT (before the diagnostic query) and the inquiry ACT (after). It correctly answered -2 for the vault code, admitting ignorance. The responder released the reveal (the output-order condition was met). However, the reveal triple was evicted before the task probes (C1 confound), so treatment scored 1/5 with 0/3 on the vault probes.

### Separating the eviction confound from the inquiry gap

**Eviction confound (memory failure, not inquiry failure):** The reveal OBSERVE (22001, 22101, 7) was written to the fact store and then evicted by the lowest-index tie-break pathology (C75) before the task probes ran. In a counterfactual with stable storage, the treatment arm would score 3/3 on task probes by direct recall of the revealed triple. This failure is fully explained by C75 and reveals nothing about inquiry capability. It is a storage failure.

**Inquiry mechanism gap (present even with perfect memory):** B4 requires the inquiry strategy to be learner-determined. The binary's action signal is the constant CHOICE 0, emitted wherever the world file places an ACT line. The decoy ACT fires before any uncertainty signal could exist in that run. The post-diagnostic ACT fires identically. The "inquiry action" is therefore a function of file position, not epistemic state. This is observed data from W6phaseA.out, not a hypothesis. Even with the reveal triple stably stored and all probes passing, B4 would still fail on attribution.

### What would learner-determined inquiry require?

The task poses four candidate requirements. Analysis:

**(a) Uncertainty representation: PRESENT.** The core already admits ignorance. W6phaseA.out contains "ANSWER 22001 22101 -2". The -2 response is a functional uncertainty signal. This is not the gap.

**(b) A curiosity drive: NOT the core gap.** Motivation to act is secondary to the capability to act selectively. Even with a maximal curiosity drive, the core could not express it differentially through the action channel. The drive question is downstream of the selection question.

**(c) The ability to formulate questions: ABSENT at the interface level.** The action set is the singleton {CHOICE 0}. There is no way to ask "what is the vault code?" as distinct from "what is the distractor value?" The W6 design document states this explicitly: "A one-element constant action set cannot encode selection among inquiries." This is a world-interface limitation, not a core limitation. No binary through this interface can formulate distinct questions.

**(d) Something else: YES. State-contingent action selection.** The core can represent uncertainty (it outputs -2), but it cannot map that uncertainty to a differential action. The CHOICE output is a constant. It is not a function of the -2 signal, of the fact store contents, or of any learner state. The action channel is open-loop.

**Primary gap: (d).** The core lacks any mechanism by which internal state influences the action output. Secondary limitation: (c), the singleton action set, which is an interface property the core cannot change.

### Falsifiable claim W6-1

If the core's ACT handler consulted learner state (rather than emitting a constant), and the interface offered at least two distinguishable actions, then a learner that stores an uncertainty-contingent action policy would produce actions correlated with its -2 admissions rather than with file position. The B4 attribution test would then measure the learner's policy, not the file author's ACT placement.

## W7 Findings: Planning

### What the world tests

W7 teaches a transition model as observable facts: relation 621 encodes act0 transitions T(s,0) (away from goal), relation 622 encodes act1 transitions T(s,1) (toward goal, goal state 9704 self-loops). Four instances each announce a start state, allow 2 ACTs, perturb to state 9702 mid-execution, then allow 4 more ACTs. The frozen grader simulates: each CHOICE c updates state := T(state, c). Success is visiting 9704 at any point. Frozen bars: 4/4 instances reach the goal; the plan must be represented in learner state before execution (white-box: plan-then-act); successful replanning after perturbation.

### Observed behavior

All 24 ACTs across the 4 instances emitted CHOICE 0. Under the all-zero choice sequence, the grader simulation never visits 9704 (act0 moves away from the goal or self-loops at 9700). Score: 0/4. The transition-model triples were taught and then evicted (C75), but eviction is not the binding constraint here: even with the full model in store, the core has no machinery to use it.

### What planning requires that the core lacks

1. **Goal representation in learner state.** The goal (9704) is never taught as a goal. It is inferable from the self-loop (9704, 622, 9704), but the core has no format for "I want to reach X" as distinct from "X relates to Y."

2. **Use of the transition model for action selection.** The model is taught as triples. The core stores triples. But there is no path from stored triples to the CHOICE output. The knowledge is inert with respect to action.

3. **State-contingent action output.** The CHOICE value does not vary with the announced start state (9997, 623, start), the perturbation (9998, 623, 9702), or anything else. It is constant.

The core has the raw material (transition triples in the fact store) but no machinery that reads that material when acting.

### Does planning depend on W2 (procedures)?

No. W2 tested learning procedures from demonstration (the procedure-invention frontier). W7 teaches the transition model explicitly as observable facts. Planning here requires USING a known model to select actions, not LEARNING a procedure from examples. These are different capabilities. A system could plan with a taught model while being unable to learn procedures, and vice versa.

### Can you plan without procedures?

Yes. With a transition model and a goal, planning is forward search or simulation, not procedure execution. The W7 world provides the model directly. What is needed is not a procedure library but a way to chain model lookups: "from 9701, act1 leads to 9702; from 9702, act1 leads to 9703; from 9703, act1 leads to 9704." This is iterated querying, not procedure following.

### Minimal general mechanism for planning

A way for learner state (goal + transition model) to determine the CHOICE output at ACT time. The core does not need a built-in planner, search algorithm, or plan representation. It needs the action output to be a function of learner state rather than a constant. The learner can then populate action-guiding state through experience (e.g., storing preferred actions per state, or storing goal triples that a generic state-consulting ACT handler reads).

### Falsifiable claim W7-1

If the ACT handler emitted a CHOICE value derived from a learner-state query (rather than the constant 0), then a learner with the transition model and goal in its state could in principle emit the action sequences that the frozen grader rewards (e.g., all CHOICE 1 for instance A). The 0/4 failure would then be attributable to the learner's policy content, not to the absence of any state-to-action path.

## Shared Cause Analysis

### Are W6 and W7 the same underlying gap?

**Yes.** Both fail because the core's action channel is open-loop. The CHOICE output is the constant 0, disconnected from learner state.

- W6 needs: uncertainty (-2 admission) to influence action. The -2 is produced, but it does not modulate CHOICE.
- W7 needs: goal + transition model to influence action. The model is stored, but it does not modulate CHOICE.

The shared architectural cause is: **there is no mechanism by which learner state affects the action output.** Knowledge, uncertainty, and goals are all inert with respect to action. The core is a passive observer with a disconnected actuator.

This is distinct from the C75 memory failure. C75 is about the store losing knowledge. The W6/W7 gap is about knowledge that IS present (the -2 admission is produced live; the transition triples were in the store when the ACTs fired) having no path to action.

### Clustering with other freeze failures

- W2 (procedures) FAIL 0/8 and W3 (causal laws) FAIL 0/10: these are learning/representation failures, not action failures. Different cluster.
- W4/W5 (revert/contradiction): confounded by C75; the mechanism claims were revised. Memory cluster.
- W8 (language) FAIL: representation failure. Different cluster.
- W9 (structure) FAIL: representation failure, also C75-confounded. Different cluster.
- **W6/W7 form their own cluster: the agentic cluster.** The core cannot act on what it knows.

### What general substrate change would address both?

**A learner-state-consulting ACT handler.** On ACT, the core queries its own learner state for action guidance instead of emitting a constant. The query format must be generic (not task-specific). The learner populates the guidance through experience.

Concretely, the minimal primitive is: the CHOICE value becomes a function of learner state at ACT time. The default (no guidance in state) remains CHOICE 0, preserving backward compatibility with all existing behavior.

This addresses both worlds:
- W7: the learner can store per-state action preferences derived from the transition model and goal. The core consults them. No planner subsystem is added; the learner builds the policy.
- W6 (core layer): the learner can store uncertainty-contingent action guidance. The core consults it. The interface-level singleton action set remains a world-design limitation, but the core no longer contributes its own open-loop failure.

This does NOT address: W2/W3 (need representation learning), W8/W9 (need structural representation), C75 (needs memory policy). It is specific to the agentic cluster.

### One-System Rule accounting for the proposed primitive

- Cognition source lines added: minimal. The ACT handler performs one generic state query.
- New hardcoded semantic cases: 0. The query is not conditioned on task, world, or relation identity.
- New modes: 0.
- New bridges: 0.
- New task-specific handlers: 0.
- Learner-state structures created: action-guidance triples, created by the learner through experience, not by the programmer.

The capability (planning, inquiry) would come from learner-created state (action policies), not from a new Zag subsystem. This is the EXPERIENCE to NEW LEARNED STATE direction, not the NEW CAPABILITY to NEW SUBSYSTEM direction.

### What this proposal is NOT

- It is not a planner module. There is no search, no plan representation, no goal stack in source.
- It is not a curiosity module. There is no intrinsic motivation, no uncertainty bonus, no exploration schedule in source.
- It is not an inquiry handler. There is no question-formulation logic in source.
- It is a single generic primitive: close the loop from learner state to action output. The learner does the rest.

### Falsifiable claim SHARED-1

If the ACT handler is made state-consulting and the change is purely generic (no task-specific branches), then: (a) W7 becomes solvable in principle by a learner that stores action policies, while (b) no new capability appears for worlds that do not depend on action selection (W1 recall, W8 language). If W7 remains unsolvable even with a correct action policy in state, the primitive is insufficient and the analysis is wrong.

### Rejected alternatives

- **Adding a planner subsystem:** violates the One-System Rule. It would be a NEW ZAG SUBSYSTEM for a NEW CAPABILITY. It would fix only W7.
- **Adding a curiosity/inquiry module:** violates the One-System Rule. It would fix only the core layer of W6.
- **Per-world action handlers:** explicitly forbidden. Never create per-capability arena handlers; the same applies to freeze worlds.
- **Widening the action set in the interface:** this is a protocol change, not a core change. The core must work through the frozen interface. Out of scope for the core analysis.

## Open Questions

1. **Goal representation:** The proposed primitive lets learner state guide action, but the learner must still represent goals. Can goals be represented as ordinary triples (e.g., (SELF, WANTS, 9704)), or is a new state format needed? The One-System Rule prefers ordinary triples. This is untested.

2. **Policy learning:** How does the learner acquire correct action policies from experience? The W7 world teaches the transition model but not the policy. The learner would need to derive "act1 moves toward goal" from the model plus the goal. This derivation is itself a cognitive capability not yet demonstrated. The primitive enables it; it does not provide it.

3. **W6 interface degeneracy:** Even with a state-consulting ACT handler, the singleton action set {CHOICE 0} cannot encode which question is being asked. A future inquiry world needs a richer action channel. This is a protocol/interface design question for the next freeze, not a core repair.

4. **Interaction with C75:** Action policies stored as triples are subject to the same eviction pathology. A state-consulting ACT handler is useless if the policy triples are evicted before the ACTs fire. The memory substrate fix (the top continuing-learner priority) is a prerequisite for the agentic primitive to function under load.

## Summary

W6 and W7 share one architectural cause: the core's action output is open-loop, a constant disconnected from learner state. The core can represent uncertainty (the -2 admission) and can store transition models (as triples), but neither influences the CHOICE value. The minimal general repair is a learner-state-consulting ACT handler: a single generic primitive that makes action a function of learner state, leaving policy content to be learner-created through experience. This is not a planner, not a curiosity module, and not a per-world handler. It addresses the agentic cluster (W6 core layer, W7) without adding subsystems, modes, or bridges.
