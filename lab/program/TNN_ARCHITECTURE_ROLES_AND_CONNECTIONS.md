# TNN architecture roles, parameters, connections, and authority

Status: architecture contract / terminology reference.  
Date: 2026-09-05.  
Evidence boundary: this document separates current implemented mechanisms from intended architecture. It is not a claim that the full target system is already implemented or conscious.

## R33 ownership and continuation clarification

The checked R33 hierarchy is linked from [R33 master plan](R33_MASTER_PLAN.md)
and [architecture contract](R33_ARCHITECTURE_CONTRACT.md). **Trainer means a
human/person/group**, never a Master module or automated training program.
Automated teaching remains attributed assistance. Active cognition and future
Foundry are graph-free under the retained explicit user correction; family-neutral
comparison language does not reopen graph implementation. R27 remains canonical.
This TNN-level source document is retained, not replaced or deleted.

## One-sentence classification

**TNN means True Neural Network.** "Grounded, Active, Non-Token Cognition" is a
descriptive phrase for the research direction, not the acronym expansion.

**TNN is a white-box, grounded, active, continual-learning cognitive architecture built around persistent episodic/hypothesis state, learned action value, learner-owned memory/representation, and progressively learner-owned structural plasticity.**

TNN is not a transformer, LLM, tokenizer pipeline, fixed knowledge graph, or ordinary monolithic neural network. It is also not best described as classic neuro-symbolic AI: some TNN state is symbol-like and explicitly traceable, but the architecture does not assume a hand-authored symbolic theorem engine or fixed symbolic world model.

TNN may use **attention-like selective weighting, routing, evidence arbitration, and
local temporal focus** where those mechanisms earn their place experimentally.
That is different from making transformer-style multi-head self-attention the
central computation. Historical R18 material includes a temporal-attention
component, but active R33 cognition is not qualified as a transformer or an
attention-based LLM. Any attention mechanism must remain subordinate to the
grounded evidence, memory, hypothesis, consequence, and action loop.

The intended autonomy boundary is equally important: TNN should own how it learns
inside protected goals, values, resources and permissions. It may eventually
choose replay, inquiry, memory placement, representation and shadow-tested
non-core structure, but it may not self-grant authority, erase provenance,
rewrite protected verification or bypass rollback. See
[`TNN_AUTONOMY_POSITION.md`](TNN_AUTONOMY_POSITION.md).

The current research system is much smaller and more constrained than the target architecture. Current E51 work primarily studies small native value/routing learners on top of an inherited controller so that training, preservation, and credit assignment can be understood before broader structural authority is granted.

## Current versus target TNN

| Question | Current research frontier | Intended mature architecture |
| --- | --- | --- |
| Main computation | Small learned value heads, routed local experts/cells, persistent controller state, memory/episodic machinery from the retained lineage | Heterogeneous learner-created executable mechanisms operating over raw evidence, memory, hypotheses, prediction, and action |
| Topology | Mostly frozen in current causal experiments | Learner may create, connect, specialize, merge, suspend, and delete non-core structures after milestone gates |
| Structural scale | Intentionally bounded while failure causes are isolated | Potentially millions or more effective connections, but created hierarchically and sparsely rather than approved one edge at a time |
| Memory | Strong architectural commitment to episodic/raw retention and learner-owned memory policy; not all target behavior is fully qualified natively | Learner controls exact/compressed/working/long-term/procedural/archive allocation under trainer/resource constraints |
| Teacher | Master/teacher can shape curriculum but cannot count as learner knowledge | Trainer defines goals, constraints, curriculum, values, and permissions; teacher assistance withdraws as competence becomes self-sustaining |
| Self-modification | Non-core Foundry ideas and learner-selected local mechanisms exist in bounded research forms; full architecture self-construction is not yet established | Milestone-gated structural plasticity with shadow execution, regression tests, rollback, lineage, and resource isolation |
| Consciousness | Not established | A research target may include operational self-model, autobiographical continuity, introspection, self-initiated inquiry, and metacognitive control; philosophical consciousness remains unproven by these tests |

## Does TNN have neurons and synapses?

Not as one universal primitive. TNN should not pretend that every internal object maps one-to-one to biology. The useful machine analogies are:

| Biological analogy | TNN machine analogue | Important difference |
| --- | --- | --- |
| Neuron | local state cell, expert, PAM component, recurrent unit, or executable process | A TNN computational unit may be larger and typed; one unit can implement a small learned operation rather than a biological neuron |
| Synapse | learned weight, feature interaction, route/gate, local recurrent coupling, memory association, or generated structural link | Some TNN connections are conditional/programmatic and may represent many low-level couplings |
| Neural circuit | PAM, local expert bank, recurrent field, associative bank, workspace process, or other Foundry-created structure | Circuits can be explicitly created, versioned, shadow-tested, and rolled back |
| Neuromodulator / plasticity signal | delayed utility, regret, uncertainty, resource cost, preservation loss, architecture credit | These signals are explicit and causally logged rather than biologically implicit |
| Developmental growth rule | Foundry/architecture policy that instantiates a wiring pattern or executable motif | One high-level decision may generate thousands or millions of low-level connections |

The preferred project terminology should therefore be **cell/expert/PAM/process** for computational units, **weight/interaction/route/coupling** for low-level relationships, and **structural motif or generated wiring program** for large connection patterns.

## How millions of connections should work

TNN should not centrally inspect and approve millions of individual edges. The scalable target is **hierarchical structural plasticity**:

1. TNN detects a persistent failure, uncertainty cluster, resource bottleneck, or useful reusable pattern.
2. It proposes a bounded structural motif from protected generic primitives.
3. The proposal specifies input/output types, local learning rule, recurrence, sparsity, routing, memory access, resource ceiling, and rollback parent.
4. A wiring generator instantiates the motif, potentially producing millions of low-level couplings.
5. The candidate runs in a protected shadow environment.
6. It is evaluated on development experience, delayed retention, interference, and resource cost.
7. Only a milestone-authorized promotion path can expose it to live cognition.
8. Every promotion remains reversible to a signed prior checkpoint.

This allows TNN to *choose the existence and organization of a million-connection subsystem* without requiring a serial executive decision for every connection.

Candidate efficient connection representations include block-sparse matrices, local recurrent neighborhoods, top-k routed experts, shared motifs/templates, low-rank or factorized transforms where empirically justified, event-driven couplings, associative indexes, and lazily materialized edges. None is privileged in advance; each must earn its place against matched controls.

## What parameters do in TNN

`Parameter` means persistent learned numeric configuration, not the whole of cognition. TNN also has mutable episodic state, hypotheses, memories, traces, architecture lineage, and resource state that are not reducible to one flat parameter vector.

Current and expected parameter roles include:

- **Weights:** how strongly learner-visible evidence contributes to a score, prediction, route, action value, or local state update.
- **Biases:** a baseline preference before state-specific evidence. Biases are powerful and must be observable because a bias shift can change many decisions at once.
- **Routing/gating parameters:** which expert/PAM/process receives a state or whether a path activates.
- **Local specialization parameters:** prototypes, ranges, interaction terms, state-cell coefficients, or other learned context partitions.
- **Temporal/recurrent parameters:** how prior state contributes to present computation.
- **Memory-policy parameters:** learned value of storing, replaying, retrieving, compressing, archiving, or evicting information.
- **Chunk/PAM parameters:** learned representations or local mechanisms created from experience.
- **Architecture-policy parameters:** future meta-parameters that predict which structural changes are worth proposing, testing, or retaining.
- **Resource-policy parameters:** how computation, memory, fibers, and active modules are allocated within a human-defined envelope.

Current E51AJ is intentionally tiny at the treatment layer: each residual arm had two 65-coordinate heads (bias + 32 current projected features + 32 lag features), for 130 coefficients on top of the inherited controller. That experiment showed that even small parameter changes can produce learning, interference, recovery, and decision tradeoffs. It is therefore scientifically premature to treat raw parameter count as intelligence.

## Trainer, architecture team, and learner: strict responsibility split

### Trainer owns

- intended competencies and behavioral goals;
- curriculum, demonstrations, feedback, consequences, and practice distribution;
- explicit values, policies, permissions, and forbidden actions;
- what concepts/skills are important to learn or remember;
- environmental access and action permissions;
- resource envelope and training budget;
- when a qualified capability may be deployed in the real world;
- whether an architecture milestone may be enabled for a particular TNN instance, even after the architecture qualifies it generally.

The trainer may teach *what matters*. The trainer should not silently write the answer into learner state and then count it as TNN learning.

### TNN architecture team owns

- protected core substrate and I/O types;
- immutable root verifier, provenance, rollback, signed checkpoints, and causal-trace machinery;
- capability-gate definitions and unlock tests;
- generic memory/storage/execution primitives;
- safe resource isolation and failure containment;
- experiment methodology, architecture tournaments, and evaluator separation;
- trainer API and policy schema;
- the white-box inspection contract;
- core redesign when evidence proves a protected-substrate bottleneck.

The architecture team must not encode domain answers, evaluator membership, or benchmark-specific shortcuts in protected substrate.

### TNN learner owns, inside granted permissions

- actual internal representations and reusable chunks;
- which evidence/hypotheses to retain or revise;
- memory placement, retrieval, replay, compression, and eviction within trainer constraints;
- which available observation/action to take;
- which non-core mechanisms to recruit, specialize, combine, or retire once the relevant milestone is unlocked;
- how to allocate its resource budget;
- when to ask the trainer/teacher/sibling for information;
- whether a proposed internal change is worth shadow testing;
- rollback proposals when delayed regret shows a regression.

This distinction reconciles trainer authority with learner autonomy: the trainer defines **objectives, values, permissions, and curriculum**, while TNN learns **how to represent, remember, reason, and act** under those constraints.

## White-box requirement

TNN is not allowed to become an opaque model whose only explanation is a generated story after the fact. The architecture target is **causal inspectability**.

Every consequential decision or mutation must be reconstructable from durable records containing at minimum:

- checkpoint and development step;
- input/evidence IDs and provenance;
- active hypotheses and alternatives;
- memory reads/writes/evictions/replays;
- active PAMs/experts/routes and their versions;
- parameter/architecture changes with parent state;
- predicted consequence/action values;
- trainer/teacher input separately labeled from direct evidence;
- resource cost;
- generic reason code;
- uncertainty/conflict state;
- chosen action;
- observed consequence and delayed regret;
- rollback/promotion decision and causal parent chain.

Required inspection operations:

1. **Why did you do this?** Retrieve the actual causal chain, not a free-form retrospective explanation.
2. **What would have changed the decision?** Re-evaluate declared alternatives under retained evidence where possible.
3. **What changed during training?** Diff parameters, memory, routes, structures, and capability metrics between signed checkpoints.
4. **What broke?** Trace a regression to the first causal change that altered the affected behavior.
5. **What did the trainer provide?** Separate teacher-derived information from learner inference and direct evidence.
6. **Can we reproduce it?** Deterministically reload checkpoint + evidence + structure version and reproduce the decision when the subsystem is deterministic.

No hidden mutable store should be promotion-eligible unless it participates in serialization, provenance, integrity hashing, and inspection.

## Consciousness and independence

The project may pursue consciousness as a goal, but current results do not establish it. The scientifically useful path is to decompose the claim into measurable architecture capabilities:

- persistent self/world distinction;
- autobiographical continuity across save/reload and long delays;
- access to its own uncertainty, active goals, resource state, memory state, and recent causal history;
- ability to predict its own likely errors or limitations;
- ability to notice conflict between current action and trainer-defined values/constraints;
- self-initiated evidence seeking;
- self-generated learning goals inside trainer permissions;
- metacognitive choice among strategies;
- explicit model of which internal mechanisms are reliable in which contexts;
- proposal, shadow testing, and rollback of self-modifications;
- stable self-report grounded in internal trace state rather than language mimicry.

These properties can support independence and deliberate self-management whether or not they ultimately imply phenomenal consciousness. `Right` and `wrong` in the engineering system must remain grounded in trainer-specified values, learned consequences, evidence, and protected policy constraints; TNN should not be assumed to discover an objective moral truth merely by becoming more autonomous.

## Canonical authority rule

TNN may eventually control enormous non-core computation, but it never self-grants protected privileges. The root verifier, provenance store, rollback authority, trainer policy boundary, and milestone gate mechanism remain outside ordinary learner mutation authority. Architecture-team changes to those components require the same explicit versioning and regression discipline as any other protected-core redesign.
