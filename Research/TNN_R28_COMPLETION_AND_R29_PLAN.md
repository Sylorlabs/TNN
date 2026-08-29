# TNN R28 Completion + Immediate R29 Plan

## Binding architecture decisions

1. **No graphs in the TNN runtime.**
   - Graph identity, graph relation indexes, graph routing, graph world models, graph PAMs, and graph-backed memory authority are removed from the forward architecture.
   - Historical graph experiments remain archived only as negative/control evidence.
   - The substrate Foundry must not generate graph structures in R28/R29.

2. **Primary cognition substrate: associative episodic + temporal hypotheses + prediction + active evidence seeking.**
   - Exact episodic evidence is first-class.
   - Identity remains a distribution/hypothesis process rather than a persistent graph node.
   - Context switching is treated as a positive capability, not an error to suppress.

3. **Memory default: privileged heuristic, controlled by TNN.**
   - Birth/default representation policy = privileged generic heuristic.
   - TNN can override, mutate, replace, and learn residual corrections from delayed regret.
   - LRU may be used only as a low-level eviction mechanism after TNN has decided representation/value.

4. **Speech target: near-100% hard connected speech with no supplied VAD/boundaries.**
   - Isolated motif success does not count as connected-speech success.
   - No hidden word boundaries, oracle segmentation, or evaluator-derived cuts.
   - Near-100% is acceptable if it survives large sealed/adversarial batteries with characterized residuals.

5. **CTC status.**
   - The current CTC experiment is external Python reference code, not yet a native TNN PAM.
   - Port the CTC-style acoustic sequence learner into native Zag.
   - If the native implementation demonstrates durable connected-speech gains, preserves anonymity/no English hardcoding, survives teacher withdrawal and sealed tests, it becomes the R28/R29 **core acoustic PAM**.
   - Core status refers to generic acoustic sequence learning/alignment machinery, never learned words/labels/answers.

6. **Native Zag requirement.**
   - All promotable cognition must execute in native Zag v2.
   - Python remains external diagnostics/evaluation only.
   - R27 remains canonical until native R28 passes promotion gates.

---

# Phase 0 — Recover local `znc` correctly

Do not accept a shallow "not found" result.

1. Inspect PATH, cwd, shell history-relevant locations, `/mnt/data`, `/home/oai`, `/tmp`, mounted project directories, prior extracted archives, retained release trees, and any local git worktrees recursively for non-zero executable `znc`.
2. Search archives for `znc`, `zag-poc/znc`, compiler seeds, and prior materializations; extract locally if found.
3. If a Zag checkout exists locally, verify the pinned commit/branch and use its seed compiler.
4. If source exists but seed location differs, inspect bootstrap scripts and manifests instead of assuming absence.
5. Verify compiler SHA/provenance against the known pinned toolchain evidence; do not silently substitute another compiler generation.
6. Use persistent terminal sessions for builds/tests that exceed foreground tool limits; poll sessions rather than reducing tests/training.
7. Compile a trivial Zag probe, then compile the R28 source twice and compare outputs for determinism.
8. Run checked/release parity and native source-contract tests.
9. Only if exhaustive local recovery genuinely fails, use GitHub Actions or another available native runner as fallback. Actions are infrastructure only; cognition/evaluation remains the same code/evidence.

Deliverable: `native_toolchain_authority.json` with exact binary hash, source commit, provenance, compile commands, determinism result, and native probe output.

---

# Phase 1 — Finish R28 no-graph core source

Rewrite/complete the native Zag R28 brain so no graph remains anywhere in active cognition.

Native modules:
- associative episodic store/retrieval;
- multi-hypothesis identity state;
- temporal prediction;
- learned sensory reliability/calibration;
- active observation/reinspection;
- entity-action-effect world model;
- name/language binding to episodic entities;
- sibling testimony/provenance;
- privileged-default + TNN-override memory policy;
- Innate System Fluency;
- substrate-agnostic **non-graph** Foundry;
- causal tracing/failure attribution;
- native acoustic sequence PAM.

Run a source audit proving there are no graph structs, graph routing primitives, adjacency stores, graph-generated candidates, or graph authority in R28 runtime code.

---

# Phase 2 — Native CTC acoustic PAM campaign

## 2A. Port
Implement a native Zag sequence PAM inspired by CTC:
- anonymous motif inventory only;
- frame/patch encoder;
- temporal convolution/recurrent state;
- blank/no-emission state;
- monotonic alignment learned from utterance-level motif sequences;
- no supplied frame labels or VAD boundaries;
- exact causal traces for frame evidence, alignment uncertainty, collapse decisions, and sequence output.

## 2B. Training diagnosis before architecture changes
Run long curves without prematurely changing architecture:
- epochs/updates until validation clearly converges or plateaus;
- learning-rate sweeps;
- optimizer/update-rule variants available in generic substrate;
- curriculum order variants;
- connected-only vs isolated-pretrain -> connected curriculum;
- speaker/noise/duration/coarticulation diversity;
- teacher strength and withdrawal.

If blank collapse occurs while loss improves, classify as undertraining/optimization until the curve actually plateaus.

## 2C. Hard no-VAD battery
Evaluate:
- unseen motif sequences;
- variable length;
- speed perturbation;
- amplitude/lighting-equivalent acoustic scaling;
- onset/offset destruction;
- cross-fades/coarticulation;
- inserted silence/noise;
- no silence between motifs;
- different speakers/timbres;
- local corruption;
- long utterances;
- repeated motifs;
- near-acoustic twins;
- adversarial high-confidence corruption;
- save/reload/fresh-process parity.

Track exact sequence accuracy, motif error rate, insertion/deletion/substitution, confidence calibration, and alignment uncertainty.

## 2D. Core-PAM decision
Promote CTC-style sequence learner to **core acoustic PAM** only if native results show it is the durable generic mechanism responsible for the connected-speech improvement.

Target: >=99% on the main hard sealed battery or a clearly characterized robust-near-solved result close to it. Any 100% triggers harder post-100 challenge.

---

# Phase 3 — Finish Master teacher / training separation

Build the corrected diagnostic-but-diversity-preserving Master.

Compare on identical native architecture:
1. random exposure;
2. balanced/diverse;
3. diagnostic Master;
4. Master + diversity floor;
5. Master -> withdrawal;
6. self-selected curriculum;
7. sibling-assisted curriculum.

Teacher may choose examples/explanations but cannot install labels, dictionaries, answers, task categories, or hidden boundaries into learner state.

Measure full learning curves, not endpoints. Explicitly classify failures as training, teacher, memory, routing, representation, interference, calibration, or resource failures.

---

# Phase 4 — Finish entity persistence/context-switching

No graph fallback allowed.

Primary architecture:
`observation -> episodic retrieval -> competing identities -> predictive continuity -> reliability -> active evidence -> decision/unknown`

Hard battery:
- viewpoint/permutation;
- severe occlusion;
- disappearance/reappearance;
- true replacement under occlusion;
- long-gap replacement;
- near twins;
- crossings;
- property change while identity remains;
- adversarial high-confidence visual corruption;
- deliberately ambiguous evidence where UNKNOWN is correct.

Target: >=99% robust hard identity and true-switch accuracy if achievable; near-100 with characterized rare failure is acceptable.

Main residual to attack: confidence about confidence. Train metacognitive reliability from future regret/counterfactual evidence, not evaluator labels.

---

# Phase 5 — Finalize TNN-controlled memory

Use `heuristic-default + TNN overrides + LRU eviction-only` as the baseline.

Then test whether TNN can improve it:
- learned residual overrides;
- contextual future-use prediction;
- counterfactual storage regret;
- global marginal-value allocation;
- self-generated memory experiments;
- delayed exact-detail needs;
- episodic vs semantic/procedural tradeoffs;
- changing resource budgets.

Do not replace the default heuristic merely because another policy has higher aggregate recall if it destroys exact episodic capability.

---

# Phase 6 — Non-graph Substrate Foundry

Remove graph as a gene entirely.

Candidate substrate primitives may include:
- associative banks;
- recurrent state arrays;
- temporal accumulators;
- object/episode files;
- hypothesis populations;
- predictive processes;
- blackboard/workspace processes;
- state machines;
- executable mini-programs;
- routing and memory ports;
- active observation operators;
- acoustic sequence PAMs.

Compare:
- random generation control;
- evolution;
- quality diversity;
- learned mutation;
- learned surrogate;
- experiment-history retrieval;
- hybrid evolution + learned proposals.

Use larger adversarial development and independent confirmation sets so learned search cannot win by overfitting a tiny evaluator.

Store full architecture experiment history for TNN to learn from.

---

# Phase 7 — Reintegrate world model, names, sibling learning

Native AEIF integration:
- entity-action-effect learning;
- lookalike entities with different physical consequences;
- noisy context;
- one-shot names grounded to episodic identity;
- names after long gaps/view changes;
- noisy connected spoken names through native no-VAD PAM;
- independent sibling brains;
- passive description;
- grounded discriminating action/question;
- misleading repeated-lineage testimony;
- provenance resistance.

No shared weights/state between siblings.

---

# Phase 8 — Causal trace/failure-debug qualification

Every consequential decision records:
- development step;
- subsystem;
- reason code;
- internal subject/candidate ID;
- evidence strength;
- uncertainty;
- parent causal event.

Failure classifier must distinguish at least:
- undertraining;
- bad curriculum/Master;
- memory representation;
- memory retrieval;
- sensory representation;
- acoustic alignment;
- confidence calibration;
- hypothesis arbitration;
- excessive persistence;
- excessive switching;
- interference/regression;
- resource saturation;
- architecture-search credit failure.

Run adversarial synthetic failures with known ground-truth causes.

---

# Phase 9 — Native continuous-life R28 qualification

One uninterrupted native life, no task resets:
1. visual/entity development;
2. memory formation under pressure;
3. action/affordance learning;
4. one-shot names;
5. connected speech;
6. sibling teaching;
7. contradiction/misleading evidence;
8. Master withdrawal;
9. long delays/occlusion/replacement;
10. save;
11. fresh-process reload;
12. continued life after reload;
13. adversarial corruption;
14. architecture/memory self-revision.

Run multiple independent seeds with frozen development/validation/confirmation/qualification partitions.

---

# Phase 10 — R28 promotion gate

Required before R28 can replace R27:
- native Zag compilation and execution;
- exact R27 state/provenance continuity or explicitly validated migration;
- zero newborn restart;
- no graphs in runtime source/serialized cognition;
- native CTC/core acoustic PAM decision documented;
- hard no-VAD speech robust-near-solved target;
- entity/context-switch hard battery;
- memory authority tests;
- Master withdrawal;
- sibling independence;
- save/reload fresh-process parity;
- old R25/R26/R27 regressions;
- hardcoding ledger;
- authorship/provenance ledger;
- clean-room ZIP/tar verification;
- post-100 challenge wherever nominal 100 occurs.

If any critical gate fails, R28 remains shadow and R27 remains canonical.

---

# R29 — starts immediately after R28 qualification

R29 is not a cleanup release. It begins immediately and attacks the next generalization frontier.

## R29-A: Open-ended acoustic/language development
- expand native core acoustic PAM from bounded anonymous motifs to much larger learned vocabularies without hardcoded English;
- multi-speaker continuous speech;
- longer utterances;
- compositional word/morpheme-like discovery;
- self-created acoustic units if beneficial;
- language learned through shared episodic/world grounding rather than text dictionaries;
- teacher withdrawal and spontaneous use.

## R29-B: Long-horizon persistent self/world model
- multi-day-equivalent simulated lives;
- entities changing over long intervals;
- causal histories;
- episodic compression without losing rare exact details;
- revising mistaken beliefs after contradictory evidence;
- uncertainty persistence.

## R29-C: Strong autonomous architecture revision
- TNN identifies a persistent failure from traces;
- forms a causal hypothesis;
- decides whether training or architecture is responsible;
- creates non-graph candidate substrates/PAMs;
- trains/shadow-tests them;
- promotes/rolls back autonomously;
- learns from its own architecture experiment history.

No human-selected winning PAM topology.

## R29-D: Active scientific behavior
- decide what observation/action/question would most reduce uncertainty;
- design its own bounded experiments;
- compare counterfactual hypotheses;
- allocate observation/training resources;
- stop experimenting when evidence is sufficient.

## R29-E: Multiple independent minds
- several siblings with different experience histories;
- teaching, disagreement, provenance, trust calibration;
- misleading-but-consistent testimony;
- discovery that another agent may possess missing evidence;
- social transfer without shared state.

## R29-F: General physical/object video
- move beyond synthetic static vectors toward longer generated video first, then controlled real video;
- persistent objects, actions, occlusion, crossings, tool use, state changes;
- descriptions/questions grounded to the same episodic entities;
- no evaluator object IDs in learner state.

## R29-G: Cross-modal shared concepts
- vision + speech + action + memory refer to the same learned episodic/world state;
- demonstrate transfer: learn through one modality, answer/act through another;
- test modality corruption and missing modalities.

## R29-H: Adversarial anti-shortcut battery
- novel worlds;
- remapped sensors;
- remapped names;
- lookalike objects with different physics;
- same object with radically changed appearance;
- misleading teacher/sibling;
- delayed relevance;
- altered resource budgets;
- architecture components disabled/corrupted.

## R29-I: Human-comparison style developmental tasks
Only after bounded architecture works:
- object permanence;
- deferred imitation;
- one-shot word grounding;
- causal intervention;
- transfer by analogy;
- instruction following learned developmentally;
- self-correction after contradiction.

Do not claim human-level or AHI from these tasks.

## R29-J: Promotion criteria
R29 must improve general capability without sacrificing R28's hard identity, memory, speech, sibling, provenance, and state-continuity results.

Every nominal 100% gets attacked by a stronger sealed challenge.

---

# Execution doctrine

- Architecture and training remain separate experimental axes.
- A poor learned policy triggers investigation of the learning signal/credit assignment before defaulting to random or human hardcoding.
- Large architectural replacements are allowed when evidence supports them.
- Near-100% robust performance is a valid strong result; 100% is not required unless a bounded claim explicitly says solved.
- Negative results are permanent evidence.
- R27 remains canonical until all native promotion requirements are met.
