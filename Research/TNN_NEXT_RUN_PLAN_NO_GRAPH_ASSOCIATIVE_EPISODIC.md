# TNN Next Run Plan — No-Graph Associative-Episodic Rebuild

**Status:** Proposed next execution generation; not yet executed.
**Parent:** verified R27 accepted brain, development step 60,423, zero newborn restarts, digest `562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04`.
**Implementation authority:** native Zag v2 only for promotable cognition.
**Primary architectural decision:** retire graph as the default cognitive/entity substrate. Keep graph variants only as frozen falsification controls and optional derived relation indexes.

---

## Executive thesis

The last factorial campaign changed the problem. The strongest finding was not that one graph variant won. It was that the associative-episodic identity family had a massive true-switch advantage while graph/persistence-heavy architectures frequently achieved high aggregate scores by refusing to change identity. That is unacceptable for a system intended to develop open-ended world models.

The next branch therefore makes a deliberate context switch:

> **Persistent identity is grounded first in episodic evidence, temporal hypotheses, prediction, and active observation—not in an authoritative entity graph.**

The graph hypothesis is not deleted from science. All graph families remain in matched control suites so this decision can be falsified. If a graph unexpectedly wins a hard matched confirmation, the result is retained and investigated. But the architecture no longer assumes that intelligence, identity, or memory must be encoded as nodes and edges.

The new primary entity substrate is an **Associative Episodic Identity Fabric (AEIF)**:

1. exact and compressed multi-view episodes are stored under TNN-controlled memory policy;
2. current observations retrieve compatible historical episodes;
3. several identity hypotheses can remain active without immediate commitment;
4. a predictive temporal process estimates what each hypothesis should generate next;
5. learned sensory-reliability calibration decides how much current evidence should override continuity;
6. active reinspection is used when the evidence does not discriminate enough;
7. identity can switch rapidly when reliable fresh evidence contradicts the old hypothesis;
8. long gaps and occlusion preserve uncertainty rather than turning persistence into certainty;
9. stabilized entities may optionally be indexed by a derived relation graph later, but the graph is not authoritative identity memory.

The other major correction is experimental: **training and architecture stay separate variables**. Every architecture result is evaluated under matched training, and every training result under frozen architecture. If a learned mechanism loses to random, the default interpretation is that its learning/credit formulation is bad until deeper learning formulations have been tested.

The project also tests **Innate System Fluency** as a protected core skill: TNN can be born knowing how to invoke its generic machinery—PAM/substrate creation, fibers, memory operations, traces, shadow tests, rollback, reinspection—without knowing which mechanism or answer is correct for any external problem.

---

# Phase 0 — Restore real native Zag authority

This must be solved first rather than carried indefinitely as `BLOCKED_ENV`.

The pinned Zag repository itself contains a trusted `znc` seed when checked out on a normal GitHub runner. Existing CI logs show the checkout executing `sha256sum znc`, rebuilding the compiler from Zag source, reaching byte-identical self-hosted stages, and emitting static native binaries. The next run should exploit that infrastructure directly instead of depending on the local sandbox's blocked DNS or text-only GitHub connector.

## 0.1 Obtain the compiler through an actual repository checkout

Preferred paths, in order:

1. run the TNN native build in a GitHub Actions runner that checks out `Sylorlabs/zag` at the pinned commit/branch and uses the repository `znc` seed;
2. upload the resulting verified compiler as a workflow artifact;
3. download/materialize that artifact into the TNN worktree and persist it under `/TNN/Research/toolchain/` if policy permits;
4. otherwise run all native TNN verification in the GitHub runner itself and return signed/hash-addressed result artifacts.

Do not substitute a different compiler version merely because it is easier to obtain.

## 0.2 Compiler verification

Require:

- repository/commit pin;
- seed SHA-256;
- bootstrap stage hashes;
- byte-identical self-host fixpoint where supported;
- static ELF status;
- no host C compiler fallback;
- compiler version/edition recorded;
- native smoke program compiled and executed;
- TNN source compiled twice to byte-identical binaries;
- checked/release parity if supported by the pinned compiler.

Persist the compiler provenance so later agents do not repeat this access problem.

---

# Phase 1 — Freeze the scientific protocol

Before using new architecture results to modify the branch, create four distinct evaluation generations:

- **development** — may change architecture/training;
- **validation** — may select among development candidates;
- **confirmation** — fresh seeds for replication;
- **sealed qualification** — unavailable to learner, Master, proposal learner, and architecture search.

Each generation gets independent hashes.

Final qualification is one-shot. If results cause another architecture revision, create a new qualification generation rather than reusing the old one.

Graph and no-graph conditions must see exactly matched experience streams within each comparison.

---

# Phase 2 — Build Innate System Fluency natively

The previous reference experiment supports the idea that birth-level knowledge of one's own generic operations dramatically reduces early developmental regret, while schema-only and Master-taught conditions can eventually catch up.

Implement this as a protected core interface in native Zag.

## 2.1 Innate operations

TNN may know from birth **how** to:

- allocate/start/stop a fiber;
- assign/revise a resource budget;
- create a non-core computational candidate;
- clone/mutate/delete a candidate;
- launch a shadow evaluation;
- compare candidate consequences;
- promote/demote/rollback a non-core mechanism;
- store exact, structured, working, short-term, long-term, cold, or discardable evidence;
- retrieve/reopen memories;
- query causal traces;
- request another sensory observation;
- ask Master/sibling for evidence;
- save/reload/checkpoint.

TNN does **not** know from birth:

- which architecture to build;
- which memory to retain;
- what an object/category/action means;
- what English words mean;
- how to solve the entity benchmark;
- what evaluator score is desired.

## 2.2 Four-way native comparison

Compare:

1. `INNATE_FLUENCY`;
2. `MASTER_TAUGHT_FLUENCY`;
3. `SCHEMA_ONLY_LEARN_EFFECTS`;
4. `DISCOVER_FROM_SCRATCH`.

Measure early and late:

- function invocation regret;
- useless-operation rate;
- correct architecture-search initiation;
- memory-policy quality;
- debugging/failure-attribution quality;
- rollback safety;
- transfer to new tasks/functions;
- rigidity from innate semantics.

If innate fluency gives a broad bootstrap advantage without limiting later self-discovery, promote it as a protected core skill.

---

# Phase 3 — Retire graph as primary state and construct AEIF

## 3.1 Authoritative state

The authoritative persistent identity state is **not** a graph node.

It is a distributed set of:

- exact episodic records;
- compressed episode summaries;
- retrieved candidate episode sets;
- current identity hypothesis population;
- temporal prediction state;
- evidence reliability state;
- provenance;
- uncertainty;
- action/consequence histories.

A graph may be constructed later as a derived relational index over stabilized events/entities. Deleting the graph cache must not destroy core identity or episodic memory.

## 3.2 Associative retrieval

Current raw/invariant evidence retrieves multiple prior episodes, not one nearest centroid.

The retrieval process should support:

- exact historical analogues;
- multiple views of the same entity;
- near-twins;
- partial observations;
- raw/structured/cold memory tiers;
- retrieval uncertainty;
- contradictory episodes.

Do not collapse all views into a single centroid because that destroys useful edge cases and can blur near-twins.

## 3.3 Multi-hypothesis temporal state

Maintain several live hypotheses:

- identity A continues;
- identity B/new entity replaced it;
- evidence insufficient/unknown.

Hypotheses have learned support, not hand-coded Bayesian constants.

The system may remain uncertain across frames rather than forcing a same/different decision immediately.

## 3.4 Predictive continuity

For each hypothesis, predict future sensory/action consequences.

If hypothesis A predicts the next observation poorly while a replacement hypothesis predicts it well, support can shift quickly.

This directly attacks the previous persistence-too-sticky problem without removing object permanence.

---

# Phase 4 — Solve sensory confidence calibration

The hard post-100 challenge isolated the current main identity problem: TNN can be confidently wrong under adversarial/high-confidence corruption.

The next architecture therefore needs **metacognitive sensory calibration**, not merely another identity threshold.

## 4.1 Learn reliability from developmental history

Inputs may include generic internal statistics such as:

- confidence margin;
- disagreement across sensory routes;
- temporal prediction error;
- cross-view agreement;
- active-reinspection consistency;
- history of similar confidence values being right/wrong;
- corruption-like internal signatures learned from consequences;
- cross-modal/action agreement.

No evaluator corruption labels or hidden answers enter learner state.

## 4.2 Confidence adversarial curriculum

Train specifically on situations where:

- high internal confidence is wrong;
- low confidence is actually correct;
- two sensory routes confidently disagree;
- a known entity changes appearance sharply;
- a near-twin appears after a gap;
- a true switch occurs during occlusion;
- an active reinspection reverses the first impression.

The objective is not merely calibration score. It is downstream identity and action performance.

## 4.3 Reinspection policy

TNN learns whether another observation is worth its cost.

Available actions may include:

- another view;
- wait for motion;
- inspect exact episodic memory;
- observe an action consequence;
- ask sibling;
- ask Master during development;
- abstain.

No fixed `if confidence < X then reinspect` rule should be canonical.

---

# Phase 5 — Full graph-retirement falsification tournament

Even though the development branch is no-graph-first, run **all graph variations anyway** as requested.

No architecture is removed because it “obviously should lose.”

## 5.1 Frozen graph controls

At minimum:

- static entity graph;
- temporal graph;
- multi-view graph;
- uncertainty graph;
- predictive graph;
- graph + active reinspection;
- graph + associative episodic memory;
- graph + particle hypotheses;
- graph + blackboard;
- graph + all no-graph helpers.

These controls answer whether the graph itself remains a bottleneck even when given the same helpers.

## 5.2 No-graph candidate families

Run at least:

- pure associative episodic;
- associative + temporal hypotheses;
- associative + predictive state;
- associative + reliability calibration;
- associative + active perception;
- associative + temporal + predictive;
- associative + temporal + reliability;
- associative + predictive + reliability;
- associative + temporal + predictive + reliability;
- full AEIF + active perception;
- slot/object-file without graph;
- particle/hypothesis population without graph;
- recurrent field without graph;
- blackboard/workspace without graph;
- executable/process identity model;
- substrate-foundry generated hybrids.

## 5.3 Matched comparison

Every variant receives the same:

- entities;
- exact exposure order;
- Master intervention budget;
- active-observation budget;
- memory resource envelope;
- training dose;
- corruption distribution;
- evaluation set.

Measure component and all-or-nothing episode success.

Key metrics:

- changed-view identity;
- near-twin true switches;
- switch under occlusion;
- severe occlusion continuity;
- long-gap replacement;
- ambiguous/unknown calibration;
- high-confidence corruption;
- active observation cost;
- exact memory usage;
- downstream naming;
- downstream affordance;
- sibling reference.

The graph-retirement claim is considered supported only if strong no-graph variants win the balanced capability frontier, not merely one metric.

---

# Phase 6 — Deep training-only campaign on frozen architectures

Take the top several graph and no-graph architectures from Phase 5 and **freeze them**.

Then vary only training.

## 6.1 Training modes

- random exposure;
- balanced exposure;
- maximum diversity;
- adaptive Master;
- contrastive/minimal pairs;
- counterexample-heavy;
- active self-selected curriculum;
- TNN-selected replay;
- sibling-assisted development;
- staged Master → diverse independent experience;
- mixed curriculum.

## 6.2 Dose curves

Use:

`1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, ...`

Continue until:

- near-perfect robust performance;
- a statistically credible plateau;
- interference;
- resource saturation;
- hidden-transfer ceiling.

Record causal traces at each dose.

This phase answers whether the remaining failures are truly architectural.

---

# Phase 7 — Finish learned memory v2/v3

The previous campaign ended while the improved memory learner was incomplete.

Do not promote the human heuristic that scored ~93.6%. It contains privileged hand-designed importance structure and is a teacher/control.

## 7.1 Long developmental query history

Give TNN a long life in which future queries reveal which retained details later mattered.

It must learn:

- probability of future exact-detail use;
- probability of semantic/event use;
- source/provenance future value;
- procedure/action future value;
- delayed regret from losing evidence;
- retrieval frequency;
- storage cost.

## 7.2 Compare learned policies

- learned linear future-use predictor;
- learned nonlinear/RF-style reference, then native equivalent;
- online contextual bandit;
- recurrent future-use estimator;
- architecture-foundry generated memory policy;
- exact-all;
- structured-all;
- LRU;
- random;
- privileged heuristic control.

## 7.3 Important principle

When storage is cheap, `EXACT_ALL` is allowed to win.

The learner should not forget for aesthetic reasons.

Selective memory should emerge only under actual resource pressure or utility tradeoffs.

---

# Phase 8 — Generalize PAM Foundry into a Substrate Foundry

PAM Foundry should no longer assume the output must be a graph.

The protected core exposes generic executable primitives, for example:

- associative banks;
- local fields;
- recurrent arrays;
- state tables;
- state machines;
- temporal accumulators;
- routing/gates;
- memory interfaces;
- executable small programs/processes;
- blackboard/workspace ports;
- graph structures as one optional primitive family.

TNN emits executable non-core structures directly.

## 8.1 Architecture-learning algorithms

The last campaign showed competent whole-structure learning can beat random search strongly, while simple per-module credit fails on synergistic/deceptive landscapes.

Canonical candidates:

- learned mutation;
- evolution;
- quality-diversity;
- learned surrogate;
- evolution + surrogate hybrid;
- retrieval of analogous prior architecture experiments;
- learned proposal model conditioned on failure telemetry;
- program induction.

Random remains the exploration control, not the final mechanism.

## 8.2 Architecture experiment memory

Every candidate stores:

- failure telemetry that triggered it;
- architecture representation;
- training curriculum;
- learning curve;
- hidden gain;
- regressions;
- compute/memory cost;
- ablation outcome;
- rollback/promotion result.

Later proposal learners train on this causal history.

---

# Phase 9 — Native AEIF + world model integration

After entity identity becomes robust, integrate all dependent capabilities around the same no-graph entity substrate.

## 9.1 Affordance/action consequence

Learn:

`episodic entity state + action + context -> predicted consequence`

No category→action lookup.

Test:

- same entity, new context;
- unseen action sequence;
- similar-looking different-affordance objects;
- different-looking same-affordance objects;
- delayed consequence;
- noisy sensory evidence;
- action consequence used to resolve identity.

## 9.2 Names/language

Spoken/byte names bind to the same episodic identity state.

Test:

- one-shot name;
- changed view;
- long delay;
- near-twin distractor;
- noisy speaker;
- another speaker;
- ambiguous reference;
- correction/renaming;
- save/reload;
- entity switch after old name association.

A name must not itself create false persistence.

---

# Phase 10 — Connected speech repair

The previous nominal no-VAD system reached ~99% but fell to ~71% on hard duration/noise/blending.

The next speech campaign should keep the VAD control and build a harder learned temporal representation.

Candidate mechanisms:

- multi-scale acoustic motifs;
- overlapping candidate segmentation;
- recurrent motif transitions;
- predictive acoustic state;
- active request/repetition when uncertain;
- speaker-invariant episodic acoustic memory;
- Substrate-Foundry generated acoustic specialists.

Training progression:

1. clean isolated speech;
2. connected TTS;
3. duration variation;
4. blending/coarticulation;
5. multiple speakers;
6. real human connected speech;
7. background noise;
8. overlapping/ambiguous speech;
9. delayed grounded reference.

Do not call speech solved from controlled TTS alone.

---

# Phase 11 — Master curriculum and withdrawal

The last dose curves showed strong adaptive teaching helps early and can lose its advantage later.

Use a competence-dependent policy:

- heavy diagnostic Master early;
- targeted minimal contrasts/counterexamples;
- teach-back;
- delayed tests;
- then increased independent/diverse experience;
- Master withdrawn completely for qualification.

Compare matched controls throughout.

The Master may also teach **system fluency** but may not install task answers into mutable cognition.

---

# Phase 12 — Independent sibling teaching on AEIF

The previous per-target sibling result was ~98%, but it was not integrated with the repaired entity substrate.

Rebuild sibling teaching using independent brains and the AEIF identity representation.

The sender may communicate:

- description;
- contrast;
- demonstration;
- action consequence;
- question suggestion.

The receiver:

- retains testimony provisionally;
- tracks source lineage;
- asks a discriminating question;
- verifies locally;
- consolidates only after sufficient evidence.

Test:

- unseen sender wording;
- similar distractors;
- incorrect repeated claim from one lineage;
- independent corroboration;
- long delay;
- changed view;
- noisy speech;
- save/reload.

---

# Phase 13 — Full causal-debugging gate

For every final error, reconstruct the exact causal path.

Required trace chain:

`raw sensor -> protected core evidence -> non-core substrate -> episodic retrieval -> hypothesis population -> reliability estimate -> temporal prediction -> memory access -> active observation -> world/language/social binding -> decision -> outcome -> diagnosis -> revision`

The failure classifier must distinguish at least:

- undertraining;
- bad curriculum/teacher;
- memory retention;
- memory retrieval;
- sensory representation loss;
- sensory calibration failure;
- routing failure;
- hypothesis arbitration failure;
- excessive persistence;
- excessive switching;
- architecture capacity;
- interference;
- resource saturation;
- source/provenance conflict.

Every architecture revision must be traceable to measured evidence.

---

# Phase 14 — Continuous-life integrated qualification

One continuing brain, no newborn resets.

Example scenario:

1. experience several unfamiliar entities from raw video/audio;
2. TNN decides what exact/structured evidence to store;
3. associative episodic identity develops;
4. Master teaches one arbitrary spoken name;
5. TNN observes actions/consequences;
6. long unrelated experience and memory pressure occur;
7. target disappears;
8. a near-twin replacement appears during degraded evidence;
9. TNN maintains uncertainty rather than blindly persisting;
10. TNN selects a discriminating observation;
11. target or replacement is resolved correctly;
12. name/reference is resolved;
13. appropriate affordance is predicted/selected;
14. independent sibling learns the entity;
15. sibling asks a discriminating question;
16. false echo-lineage testimony is introduced;
17. provenance prevents false consensus;
18. Master is withdrawn;
19. brain is serialized;
20. fresh process reloads;
21. target returns under a harder unseen corruption;
22. identity, name, affordance, memory, source history, and architecture state survive;
23. old R25–R27 regression suites rerun.

Report both component scores and all-or-nothing scenario success.

---

# Phase 15 — Qualification statistics and post-near-perfect attacks

Use at minimum:

- 5 development seeds;
- 5 validation/architecture-selection seeds;
- 10 independent confirmation seeds;
- 10 sealed qualification seeds when compute permits.

Report numerators/denominators, not only percentages.

Status language:

- `PARTIAL` — major residual failures;
- `STRONG` — broad but material gaps;
- `ROBUST_NEAR_SOLVED` — near-perfect on a large hostile sealed battery with a narrow characterized failure boundary;
- `SOLVED_BOUNDED` — 100% on sealed bounded qualification **and** survives harder post-100 challenge.

A robust 99%+ result is acceptable and should not be sabotaged by chasing cosmetic 100%.

But any nominal 100% automatically triggers harder tests.

---

# Phase 16 — Native promotion and regression

No new mechanism becomes canonical until it is native Zag v2 and passes:

- compiler provenance gate;
- source determinism;
- save/reload determinism;
- no-newborn continuity;
- hidden confirmation;
- R25–R27 retained regressions;
- no evaluator leakage;
- hardcoding ledger;
- memory-policy ledger;
- architecture creation/deletion ledger;
- teacher withdrawal;
- causal trace integrity.

Graph retirement itself is an architecture promotion and therefore needs regression testing. If a derived graph cache is removed entirely, verify that source/provenance/relation capabilities remain intact through non-graph structures or a non-authoritative relation index.

---

# Phase 17 — Release

Every verified release contains:

- native Zag source;
- compiler/version/hash provenance;
- parent R27 digest and zero-restart proof;
- accepted state/policy;
- raw factorial results;
- graph-control results;
- training dose curves;
- memory v2/v3 results;
- system-fluency results;
- Substrate-Foundry history;
- causal traces/failure atlas;
- authorship ledger;
- hardcoding ledger;
- negative/rollback results;
- qualification hashes;
- verifier;
- deterministic smoke tests;
- ZIP + tar.gz;
- independent extraction and tree/hash parity.

Upload the final release and updated project context to `/TNN/Research`.

---

# Exact execution order

1. Obtain a real repository checkout/networked runner and persist verified `znc` provenance.
2. Native-compile the current shadow Zag branch and repair any source incompatibilities.
3. Freeze new evaluation generations.
4. Implement/verify Innate System Fluency natively.
5. Implement AEIF as the primary no-graph entity substrate.
6. Implement learned sensory-confidence calibration.
7. Implement active evidence seeking.
8. Run the complete graph-control/no-graph factorial with identical training.
9. Freeze top graph/no-graph variants; run full training-only curves.
10. Complete learned-memory v2/v3 developmental-history experiment.
11. Generalize PAM Foundry to substrate-agnostic Foundry.
12. Train architecture proposal/mutation learners from causal architecture history.
13. Verify learned architecture search beats/meaningfully competes with random across deceptive/synergistic tasks; if not, debug the learner rather than declaring randomness superior.
14. Integrate entity-action-effect affordance learning.
15. Rebind names/language to AEIF identity.
16. Repair connected raw speech and progress to real human audio.
17. Run competence-dependent Master teaching and full withdrawal.
18. Rebuild sibling teaching on independent AEIF brains.
19. Run long memory-pressure/delayed-relevance development.
20. Run continuous-life integrated qualification.
21. Run harder post-99/post-100 challenges.
22. Run every retained historical regression.
23. Promote only native mechanisms supported by the complete evidence.
24. Package and clean-room verify dual archives.
25. Persist release + project-local decision history.

---

# Primary hypotheses to falsify

**H1:** Graph authority caused part of the entity-switch bottleneck; a no-graph associative-episodic primary substrate improves balanced identity capability.

**H2:** Associative episodic identity can gain robust occlusion/object permanence through temporal hypotheses, prediction, reliability calibration, and active perception without sacrificing rapid true switching.

**H3:** Innate system fluency substantially accelerates early development without constraining late architectural autonomy.

**H4:** Learned whole-structure architecture search can systematically outperform random search when credit is assigned at the correct compositional granularity.

**H5:** TNN-controlled learned memory can eventually approach or beat privileged fixed heuristics once it has sufficient delayed future-use developmental history.

**H6:** A heterogeneous intelligence substrate—episodic memory, hypothesis state, prediction, local fields/workspaces/programs, and optional derived graphs—outperforms a single universal graph representation.

All six hypotheses may fail. The experiment design must retain results even if they contradict the architectural direction above.

---

# Decision boundary

This plan intentionally accepts a large architecture replacement. The goal is not continuity of implementation style; it is continuity of the **developing learner and its accumulated knowledge**.

The graph can be scrapped as the primary substrate without restarting the brain if learned evidence is migrated into episodic/non-graph representations with verified behavioral and memory continuity.

That is the next branch's central engineering/scientific challenge.
