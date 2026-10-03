# Next Frontier Scout: Ranking the Unexplored

Date: 2026-09-30. Worker: Next Frontier Scout.
Verdict label target: FRONTIER-SCOUT-COMPLETE.
Status: scout only. No implementation proposed or written.

## Current wave status (what is already covered)

Before ranking the unexplored, the covered ground:

- CLA-2/CAM-1/ACT implementation: builders paused pending Micah's ruling on integration amendments A1-A12 and EXECUTE placement amendments A-C. The protected-core boundary is now frozen: SMALL, FROZEN, domain-neutral ISA (ALLOC, READ, WRITE, LINK, COPY, COMPARE/EQ, ADD, BRANCH, APPLY/EXECUTE, registers). No regularity detectors in core. Finite-difference is OUT of CAM-1; trial/compositional discovery is the route.
- Composition prereg: scout complete (`composition_scout/`, commit `cd7a3dd28`). Execution vocabulary suffices; the plan constructor is the gap. Prereg spec with P1-P5/F1-F5 exists.
- MUL-from-ADD: scouting in progress (`mul_scout/`). Micah flagged this as potentially "very interesting L3-ish evidence."
- C1 Zag driver rerun: in progress. The 63/63 vs 27/63 comparison awaits canonical status.
- FW1-FW9: sealed, awaiting implementation completion for D7 evaluation.
- H-EXP2 v2: sustained active experiment construction preregistered (commit `cc87d6f09`), implementation follows.
- DEVINT1/DEVINT2: developmental integration demonstrated on the OLD substrate (separate rule stores, twin stores), BUILD-PASS. Adversary found no kill.

## Candidate frontiers

### (a) Developmental integration on CLA-2

What is known: DEVINT1 ran 11 stages (concepts, segments, rules, contradiction, inquiry, rollback, eviction) in one persistent process. DEVINT2 added delayed reuse, interference, correction, memory pressure. Both passed on the old architecture with separate stores.

What is unknown: whether the consolidated CLA-2 workspace preserves all of this. The old demos used separate rule stores and twin-store comparisons. CLA-2 dissolves those into one workspace with edge-type conventions. Consolidation is only a win if capability is preserved while mechanism count drops. Nothing has tested the full developmental sequence on the new substrate.

Why it matters: this is Micah's standing requirement in its strongest form, "one continuing learner should eventually experience new vocabulary, concept learning, procedure invention, conflicting evidence, active inquiry, causal learning, memory pressure, unrelated interference, corrections, and delayed reuse, with no process reset, no task label supplied to cognition, and no recompilation per task." It is also the direct empirical test of the One-System Rule: fewer mechanisms, same or better capability. If the developmental sequence breaks on CLA-2, the consolidation lost something load-bearing and we need to know exactly what.

### (b) Active inquiry from learner-authored uncertainty

What is known: H-EXP2 v2 (preregistered) tests sustained experiment construction: the learner prunes 16 hypotheses, scores 1654 probes by predicted-outcome distinctness, executes the top probe. This is researcher-specified probe scoring over a researcher-enumerated hypothesis family.

What is unknown: whether inquiry can be driven by the learner's own uncertainty structures. The W6 B4 ruling set the bar: FAIL unless the learner itself chose the information-seeking act from its own uncertainty. The learner-state ACT prereg provides UNCERTAINTY conventions and a POLICY_ROOT mechanism, but nothing has tested whether learner-authored uncertainty actually drives action selection. The gap between H-EXP2 v2 (researcher scoring rule) and genuine self-directed inquiry (learner uncertainty to ACT) is unexplored.

### (c) Linguistic relation as executable structure

What is known: unified structures section 1e specifies the workspace form, symbol nodes with INSTANCE-OF and REFINES edges, BIND cells attaching symbols to roles, COMPOSE cells assembling novel combinations. EXECUTE runs the mapping on QUERY or TEACH.

What is unknown: everything empirical. No linguistic structure has been built or executed in any workspace. The W8 vocabulary results (frozen core 0/4 recall) show the old substrate could not hold vocabulary; CLA-2 P4 predicts 4/4 on fresh worlds. But word-to-meaning mapping as an executable graph, compositional utterance assembly, and novel combination from familiar cells are all untested.

### (d) Transfer across changed surface representations on the new architecture

What is known: the old contlearn2 transfer test (D9-D10) showed schema FORM applying to novel values. The C1 baseline showed the contestant far above memorization. Transfer as a phenomenon is established on old substrates.

What is unknown: whether CLA-2 preserves transfer. The mechanism changed (evidence edges instead of schema slots), so the old transfer results do not carry over automatically. This is confirmatory rather than discriminating: it checks for regression, not new capability.

### (e) MUL-from-ADD construction as L3-ish evidence

Status: already scouting (`mul_scout/`). Not ranked here except to note its position: it is the first empirical test of the frozen ISA boundary. If the learner constructs MUL from INC/DEC/ADD and persists it as a reusable cognitive object, that validates the boundary and produces the program's first L3-flavored result. The scout is in flight; no duplication needed.

## Ranking by information gain

**1. Developmental integration on CLA-2 (DEVINT-CLA2).** Highest information gain. It is the single experiment that most discriminates the architecture program's central bet. Every other frontier tests one capability on the new substrate; this one tests whether the substrate is a general continuing learner at all. A pass validates the entire consolidation direction. A fail localizes exactly which developmental demand the unified workspace cannot meet, which is itself high-value (it tells us what the separate stores were actually buying). No other candidate has this win-big/lose-informative symmetry.

**2. Learner-driven inquiry (UNCERTAINTY to ACT).** High information gain. It tests whether the ACT mechanism plus uncertainty conventions produce behavior the researcher did not script. H-EXP2 v2 will show the learner can execute a researcher-designed inquiry loop; this frontier asks whether the learner can originate one. This is the difference between L2 (executing an inquiry procedure) and L3-ish (constructing the inquiry from experienced uncertainty). It is also the direct answer to the W6 B4 ruling.

**3. Linguistic relations as executable structures.** Medium-high information gain. Language is the least explored modality in the new architecture, and the unified-structures claim ("same substrate for procedures, causal rules, plans, linguistic relations") is currently pure spec. An implementation would test the strongest version of the consolidation thesis. Ranked below inquiry because the W8 vocabulary work and CLA-2 P4 already cover the retention half; what remains is the executable-mapping half, which is narrower.

**4. Transfer on the new architecture.** Medium information gain. Necessary regression coverage, but confirmatory. It should be run as a standard battery against every new substrate generation, not as a standalone frontier.

## Top candidate specification: DEVINT-CLA2

**Question.** Does the CLA-2 unified workspace support the full developmental sequence, vocabulary learning, concept formation, rule induction, contradiction handling, correction and rollback, active inquiry, eviction under memory pressure, interference between domains, and delayed reuse, in one persistent process with no reset, no task labels supplied to cognition, and no recompilation?

**Experiment.** Port the DEVINT1/DEVINT2 stage structure to the CLA-2 implementation once builders resume post-ruling. Same 11-stage skeleton (S1 raw episodes, S2 segmentation, S3 concept inventory, S4 relation counting, S5 rule activation, S6 treatment/control criterion, S7 contradiction events, S8 inquiry emission, S9 demotion/rollback, S10 eviction under pressure, S11 delayed reuse and interference). Every check that previously read separate stores now reads the one workspace: concepts as GROUP nodes, rules as executable graphs with SUPPORTS edges, contradictions as CONTRADICTS edges with superseded history, inquiry as UNCERTAINTY structures driving ACT, eviction via the three-step retention routine. Twin-store comparisons are replaced by workspace self-consistency checks (the old twin was a control for implementation bugs; the new control is byte-identical determinism across 3 runs plus stage-by-stage comparison against the DEVINT1/2 baselines).

**Prereg shape.** Frozen stage definitions with exact checks (B1 persistence: one compilation, one process, STATE-CONT after every stage with non-decreasing structure counts; B2 stage function: per-stage exact numbers as in DEVINT1; B3 blindness: no stage labels, task IDs, or mode flags reach cognition; B4 interference: alternating conflicting domains with clean selection and recovery; B5 delayed reuse: structures from early stages reused late without reteaching). Determinism: 3/3 byte-identical. Kill bars: any stage check fails, any task label leaks to cognition, any reset or recompilation between stages, or capability below the DEVINT1/2 baseline on any shared check. The prereg must state which DEVINT1/2 checks are shared (regression) and which are new (workspace-native), so a pass cannot hide a regression behind new checks.

**Dependencies.** Requires CLA-2 implementation complete (blocked on Micah's A1-A12 and A-C rulings). Requires the C1 Zag-driver pattern for clean reruns. Should run after the composition prereg implementation, since S8 inquiry and multi-fact queries benefit from plan execution.

**What a fail would teach.** If specific stages fail, the failure localizes the consolidation cost: e.g., S7 contradiction handling fails implies CONTRADICTS edges do not carry the revision semantics the old rollback had; S10 eviction fails implies the three-step retention routine prices structures differently than the old policies. Each such localization is a precise, falsifiable claim about what the unified workspace cannot express, which is the most valuable possible input to the next architecture iteration.

## Queue recommendation

1. DEVINT-CLA2 prereg (this scout's output; author after CLA-2 implementation lands).
2. UNCERTAINTY-to-ACT inquiry frontier (prereg after H-EXP2 v2 results).
3. Linguistic executable structures (prereg after vocabulary retention P4 is confirmed).
4. Transfer battery as standard per-generation regression (not a standalone frontier).

## Verdict

**FRONTIER-SCOUT-COMPLETE.** Four candidates surveyed, ranked by information gain. Top candidate DEVINT-CLA2 fully specified: question, experiment, prereg shape, dependencies, and what failure would teach. Zero source lines; zero modes, bridges, handlers, or semantic cases; analysis only.

## Process failure disclosure

During the pre-commit dash check, this worker executed `python3 -c "pass"` as part of a shell command line (a stray fragment left in the command before the actual grep-based check). Python 3 exists at `/usr/bin/python3`, so the interpreter did run. No research logic depended on it: the em-dash verification was done by shell grep (`grep -c` for the UTF-8 byte sequence, returning 0 in both files), the report content was authored as markdown, and the `pass` invocation produced no output and influenced nothing. Per the exact purity rule any Python invocation is a process failure, and disclosure does not cure it. This wave is therefore PROCESS-FAIL per the standing worker-startup guard. The scout content above is unaffected as analysis, but its canonical standing is for the parent to judge; if the result matters it must be cleanly re-frozen.
