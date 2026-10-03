# TNN Capability Master Plan — 2026-09-18

## 1\. Mission

The goal is to turn TNN into a **general learning system** whose intelligence is increasingly earned from experience.

The highest research priority is:

> **hypothesis formation → reasoning → experiment → abstraction → invention**

Prediction remains useful, but it is one instrument inside this loop. It is not the definition of intelligence and it is not the single organizing objective.

TNN eventually needs breadth comparable to a general-purpose AI system:

| Capability | Target |
| --- | --- |
| Hypothesis formation | Generate competing explanations without being given answer candidates |
| Logic | Deduce consequences and detect contradictions |
| Causal reasoning | Distinguish correlation from intervention-sensitive causes |
| Counterfactual reasoning | Reason about states that did not occur |
| Abstraction | Discover reusable structure across superficially different problems |
| Analogy | Transfer structure between domains |
| Invention | Produce verifiably novel hypotheses, algorithms, experiments or procedures |
| Planning | Construct and revise multi-step plans |
| Memory | Decide what, how precisely, and how long to remember |
| Continual learning | Add competence without routinely destroying old competence |
| Language | Understand and generate broad natural language using the same knowledge system |
| Coding/tools | Learn procedures, manipulate computers and solve real engineering problems |
| Vision/audio | Learn useful concepts from raw sensory experience |
| Self-model | Learn which internal strategies work and when |
| Curiosity | Select experiences that are likely to produce useful learning |
| Meta-learning | Improve how it learns and eventually propose architectural improvements |
| Transparency | Make persistent connections, memories, hypotheses and learning changes inspectable |
| Scale | Grow to millions of learner-owned connections without requiring dense LLM-style compute |

Historical R25/R26/R27 continuity remains a required foundation track. It does **not** count as new intelligence merely because old outputs are reproduced.

* * *

# 2\. Three different things must never be conflated

## A. Architecture

Architecture is machinery supplied by the researchers.

Examples:

- memory containers
- sparse connection storage
- hypothesis workspace
- generic search
- arithmetic
- integrity checking
- update interfaces
- evidence provenance
- replay
- resource accounting
- evaluator interfaces

Architecture answers:

> **What is TNN capable of learning or representing?**

## B. Training

Training consists of experiences that modify learner-owned state.

Examples:

- examples
- books
- speech
- videos
- causal worlds
- puzzles
- experiments
- consequences of actions
- demonstrations
- code
- scientific problems

Training answers:

> **What does TNN actually discover from experience?**

## C. Evaluation

Evaluation is information TNN did not have while architecture or learned state was being selected.

Evaluation answers:

> **Did the resulting system genuinely generalize?**

This separation becomes mechanically enforced.

Every experiment records independently:

```
ARCHITECTURE HASH
INITIAL LEARNED-STATE HASH
TRAINING-DATA MANIFEST
TRAINING CONFIGURATION
FINAL LEARNED-STATE HASH
EVALUATION MANIFEST
RESULT
TRACE / PROVENANCE
```

Architecture source cannot silently change during a training run.

A TNN-generated architecture proposal is initially just another output artifact. It does not automatically become part of the running system.

* * *

# 3\. How architecture research proceeds

We should not keep adding architecture whenever training performs badly.

The default research cycle becomes:

```
freeze architecture
       ↓
train harder
       ↓
test fresh worlds
       ↓
inspect exact failure traces
       ↓
more optimization / more experience?
       │
       ├── yes → train more
       │
       └── no
             ↓
is required information representable?
             │
             ├── yes → learning/objective problem
             │
             └── no  → architecture problem
                         ↓
                  smallest justified change
                         ↓
                  repeat from freeze
```

This implements the user's requirement that **training should help discover which architecture is needed**.

Architecture changes require evidence that the previous mechanism has reached a meaningful capability limit. This follows the useful lesson from the existing R32 work: several apparent architectural failures turned out to be objective, ranking, representation or training problems rather than proof that an entirely new topology was necessary.

* * *

# 4\. The intelligence core

The main new research target is a persistent hypothesis-and-reasoning loop.

## Internal cycle

```
EXPERIENCE
    │
    ▼
RETRIEVE RELEVANT MEMORY
    │
    ▼
GENERATE MULTIPLE HYPOTHESES
    │
    ▼
CHECK LOGICAL / EMPIRICAL CONSISTENCY
    │
    ├──────────────┐
    ▼              ▼
DEDUCE          SIMULATE
CONSEQUENCES    CONSEQUENCES
    │              │
    └──────┬───────┘
           ▼
FIND DISCRIMINATING TEST
           │
           ▼
OBSERVE / EXPERIMENT / ACT
           │
           ▼
UPDATE HYPOTHESES
           │
           ▼
ABSTRACT REUSABLE PRINCIPLE
           │
           ▼
PLAN / EXPLAIN / INVENT
```

World prediction occupies one branch of this process.

A hypothesis can also succeed because it:

- satisfies logical constraints
- proves a statement
- explains observations parsimoniously
- survives intervention
- rules out alternatives
- compresses multiple facts into a reusable rule
- transfers to a different domain
- produces a verified program

Human-like cognition research similarly emphasizes causal models, compositionality and learning-to-learn rather than pattern recognition alone.

## Hypothesis representation

Each live hypothesis should carry at minimum:

```
stable ID
representation/program
creation step
generator/provenance
supporting evidence refs
contradicting evidence refs
dependent assumptions
deduced consequences
empirical predictions
known falsifiers
tests that could discriminate it
confidence/support state
novelty fingerprint
complexity/resource cost
status
```

No task-specific answer strings belong in this substrate.

* * *

# 5\. Hypothesis generation must be diverse

A major failure mode would be producing one obvious guess and repeatedly reinforcing it.

TNN should maintain multiple competing explanations.

Candidate generation should eventually combine:

- composition of previously learned concepts
- analogical transfer
- perturbation of existing explanations
- causal structure changes
- program synthesis
- reusable learned subroutines
- counterexample-driven revision
- stochastic exploration
- learned proposal distributions

GFlowNets are useful research inspiration because they explicitly target **diverse high-quality candidate generation**, rather than only finding a single argmax solution. DreamCoder is relevant because it learns reusable abstractions while solving program-induction problems. Neither architecture should simply be copied into TNN.

* * *

# 6\. Invention becomes a first-class research track

“Invention” needs an operational definition so we cannot fool ourselves.

## Invention ladder

| Level | Evidence |
| --- | --- |
| I0 | Reproduces known answer |
| I1 | Recombines known components into an unseen arrangement |
| I2 | Forms an unseen hypothesis that correctly explains held-out evidence |
| I3 | Discovers a new reusable rule/program absent from its direct training examples |
| I4 | Chooses an informative experiment that distinguishes competing hypotheses |
| I5 | Produces a verifiable solution better than its training references/baselines |
| I6 | Transfers a discovered principle into a substantially different problem family |
| I7 | Repeatedly performs I3–I6 across domains without researcher-written task-specific reasoning code |

No “TNN invents” claim before at least I3.

Strong general invention evidence requires I5/I6 across multiple domains.

## Initial invention battery

### Scientific-law discovery

Give TNN observations from hidden systems.

It must:

1. propose explanatory laws;
2. identify uncertain variables;
3. request experiments;
4. predict intervention results;
5. revise hypotheses;
6. express the final rule;
7. transfer the rule structure to a new system.

### Algorithm discovery

Use small but exact domains where every proposal can be verified.

Examples:

- sorting networks
- arithmetic programs
- graph algorithms
- compression transforms
- search heuristics
- scheduling
- tiny matrix algorithms

Known research demonstrates that automatic search can genuinely discover algorithms outside previous human solutions when hard verification is available.

### Program induction

Give only input/output examples.

Require a program that:

- explains demonstrations;
- works on hidden inputs;
- stays compact;
- can later become a reusable abstraction.

DreamCoder provides a useful precedent for learning reusable libraries rather than solving every problem from scratch.

### Formal reasoning

Add theorem environments where the verifier decides correctness.

AlphaGeometry is useful here: neural guidance plus symbolic deduction solved 25 of 30 olympiad-level geometry problems in its test set, while producing checkable proofs.

### Abstract concept induction

Use:

- ARC-style problems
- ConceptARC
- Bongard problems
- later Bongard-OpenWorld

ARC was explicitly designed around adaptation to novel tasks rather than accumulated task skill, and ARC-AGI-2 pushes this further. ConceptARC tests whether apparent ARC performance actually corresponds to abstraction and generalization.

* * *

# 7\. Prediction is a tool, not the core objective

TNN should still learn predictive models.

They are useful for:

- action consequences
- physical dynamics
- social consequences
- temporal continuity
- planning
- detecting surprise
- testing causal models

World-model research provides strong evidence that learned predictive models can support difficult planning and control. MuZero plans with a learned model without knowing environment dynamics, and DreamerV3 uses a learned world model across more than 150 diverse control tasks.

But TNN does **not** reduce all cognition to next-observation prediction.

Its reasoning workspace must also support:

```
proof
constraint satisfaction
causal inference
analogy
hypothesis competition
program execution
counterexample search
abstraction
experiment design
memory retrieval
planning
```

* * *

# 8\. Memory becomes learner-controlled

The old idea of “a memory system” is insufficient.

TNN needs to choose **what representation and fidelity a memory deserves**.

## Memory actions available to the learner

```
KEEP_IN_WORKING_MEMORY
STORE_EXACT
STORE_EPISODE
STORE_FEATURES
STORE_SUMMARY
STORE_RULE
LINK_TO_EXISTING
PIN
REHEARSE
CONSOLIDATE
COMPRESS
FORGET
```

These are generic actions.

The policy selecting them is learned.

## Four interacting memory forms

### Working memory

Short-lived state relevant to the current reasoning process.

### Episodic memory

Specific experiences with source and time.

### Semantic memory

General knowledge abstracted across experiences.

### Procedural memory

How to perform skills.

Complementary-learning-system research provides a useful biological/computational precedent for combining fast episodic storage with slower structured learning and replay.

## Exact video-memory requirement

A specific qualification test should directly implement the user's example.

Give TNN a long video under constrained memory.

Later ask:

- what happened at `t=08:42`?
- what color was object X?
- when did object Y first appear?
- show the exact interval where event Z occurred;
- what happened immediately before it?
- did the system preserve the exact clip or only a summary?

TNN chooses whether to retain:

```
exact bytes
exact frame interval
keyframes
visual features
event representation
semantic summary
nothing
```

Memory quality is then judged against fixed policies:

- exact-all
- FIFO
- LRU
- random
- researcher heuristic
- learned TNN policy

The learned policy gets credit only for outperforming those controls across **multiple task families**, not one hand-shaped memory test.

Neural Episodic Control, memory-augmented networks and the DNC show that rapid experience storage and learned read/write memory can materially change learning behavior.

* * *

# 9\. TNN must own its connections

A million connections should not mean a million static researcher-written graph edges.

Each persistent learned connection needs:

```
connection ID
source node
destination node
connection class
weight/state
creation step
evidence that caused creation
update history
last activation
utility/reliability history
protection state
deletion step if removed
```

## Learner-controlled topology

Candidate mechanisms to tournament:

1. static sparse topology;
2. learned gating of fixed edges;
3. prune-and-regrow sparse topology;
4. correlation-driven creation;
5. prediction-error-driven creation;
6. causal/hypothesis-support-driven creation;
7. mixed policy learned from connection utility.

Dynamic sparse training methods such as SET and RigL demonstrate that topology can change during learning while remaining sparse, making them useful engineering references.

TNN should not assume their exact rules are optimal.

The tournament determines what survives.

## Scale ladder

Run identical capability suites at approximately:

```
50,000 persistent connections
250,000
1,000,000
5,000,000
```

Stretch target:

```
10,000,000
```

At every scale record:

- capability score
- learning speed
- retention
- transfer
- active edges per decision
- bytes per persistent edge
- peak RSS
- decisions/sec
- updates/sec
- connection creation/deletion rates
- retrieval latency
- trace-storage overhead

The goal is to determine whether intelligence actually improves with scale.

A larger graph gets no credit merely for being larger.

* * *

# 10\. TNN must remain inspectable

I would reject an architecture where “traceability” means asking the model afterward why it acted.

That explanation can itself hallucinate.

## Persistent connection provenance

Every persistent edge and memory has a reconstructable history.

## Exact evaluation traces

For qualification episodes capture:

```
sensory evidence
memory reads
connections activated
hypotheses generated
hypotheses removed
score/support changes
inferences
counterfactuals
experiments selected
plans generated
actions
consequences
learning updates
new connections
deleted connections
```

## Causal replay

An explanation becomes credible only if we can intervene:

```
remove memory X
disable connection Y
remove evidence Z
freeze learning
scramble reward
rerun
```

and observe the predicted behavioral change.

This follows the spirit of causal interpretability methods that intervene on internal representations instead of relying only on descriptive explanations.

## Trace scaling

Logging every activation forever at millions of connections will become wasteful.

Therefore:

- persistent connection lifecycle provenance is always retained;
- qualification mode retains exact active-path traces;
- development mode can use compressed traces;
- any promoted result must be reproducible under exact-trace mode.

This gives us inspectability without making logging the dominant computation.

* * *

# 11\. Hardcoding firewall

A result can be `100%` and receive **zero intelligence credit**.

## Evidence ladder

| Class | Meaning |
| --- | --- |
| C0 | Hash/file/serialization works |
| C1 | Infrastructure transports information correctly |
| C2 | Historical behavior reconstructed |
| C3 | Learns a bounded task |
| C4 | Generalizes to fresh instances/worlds after freeze |
| C5 | Transfers to a structurally different task |
| C6 | Same learned mechanism succeeds across different domains |
| C7 | Sustained open-ended learning without task-specific rewrites |

Examples:

```
100% sensory-byte reconstruction = C1
16/16 historical generator reproduction = C2
perfect learned task performance = C3 unless held-out transfer exists
```

The dashboard must always display the **class beside the number**.

## Mandatory falsifiers

Every major learned capability receives:

- blank-brain baseline;
- update-disabled control;
- reward-scramble control where applicable;
- label/identifier permutation;
- structural permutation;
- fresh-world evaluation generated after freeze;
- whole-source-family holdout;
- novel composition;
- intervention test;
- information-denial ablation;
- source audit for answer strings/task names/evaluator state;
- memorization/near-duplicate scan;
- cross-domain transfer.

If a “reasoning” system gets 100% with learning disabled, that result triggers an investigation rather than celebration.

* * *

# 12\. Fresh evaluation is the main anti-cheating mechanism

Public benchmarks alone are insufficient.

TNN will eventually have seen many of them.

For core claims, build **generators of benchmark families**.

The generator itself is evaluator-side.

After the architecture and learned state are frozen:

```
freeze TNN
     ↓
sample secret seed
     ↓
generate new world/problem family
     ↓
evaluate once
```

The task generator must be unavailable to TNN during inference except through legitimate observations.

This makes it much harder for a result to come from memorization.

* * *

# 13\. Training data needs deliberate source diversity

No single text corpus should become “the world.”

Every training artifact gets:

```
source family
source ID
license
content hash
retrieval date
domain
modality
author/repository where available
training/dev/eval designation
dedup fingerprint
```

## Initial source families

### Encyclopedic knowledge

Wikipedia/Wikimedia material under its applicable free-content licensing.

### Books

Eligible Project Gutenberg texts after stripping Gutenberg-specific wrapper material and respecting the work's copyright status. Bulk acquisition uses their recommended mirrors rather than scraping the main website.

### Textbooks

Open educational materials such as OpenStax, **with per-book license tracking**. Current OpenStax materials include noncommercial/share-alike licensing as well as some books under CC BY, so ingestion cannot assume one license globally.

### Human problem solving

Stack Exchange's Creative Commons data dump, with attribution/license lineage preserved.

### Scientific material

arXiv and peer-reviewed papers are excellent researcher sources.

For **training ingestion**, use only papers whose individual reuse license is compatible with the experiment and record that license. Do not assume every arXiv PDF has the same reuse permission.

### Code

Only repositories with an admitted compatible license.

Hold out entire repositories and project families for evaluation.

### Speech

Mozilla Common Voice provides many CC0 speech datasets. LibriSpeech provides roughly 1,000 hours under CC BY 4.0.

### Generated experience

Locally generated:

- causal worlds
- logic problems
- algorithm tasks
- synthetic language games
- physical simulations
- puzzles
- experiments
- hidden-rule systems

Generated data is especially useful because evaluation instances can be created **after freeze**.

## Diversity guardrail

Initial training default:

```
no single source family >25% of a mixed training tranche
at least 4 independent families per major training phase
fresh/generated experiences included continuously
whole families withheld for transfer evaluation
```

The `25%` value is a research guardrail, not intelligence architecture.

Test 15%, 25% and 40% caps rather than assuming 25% is optimal.

Later the training sampler may itself become learner-directed according to learning progress, subject to minimum diversity protections.

* * *

# 14\. Reasoning curriculum

Training proceeds from capabilities, not memorized benchmark answers.

## Stage R1 — competing hypotheses

TNN sees evidence compatible with several explanations.

Goal:

- keep alternatives alive;
- gather more evidence;
- revise support.

## Stage R2 — falsification

Some hypotheses have identical predictions on observed data but differ under an intervention.

TNN must choose the differentiating experiment.

## Stage R3 — causal induction

Randomize confounders and correlation structure.

The correct latent cause must survive.

## Stage R4 — compositional reasoning

Train concepts individually.

Evaluate unseen combinations.

## Stage R5 — abstraction

Multiple tasks contain the same latent relation with different surface representations.

TNN should discover the reusable relation.

## Stage R6 — analogy

Transfer that abstraction into a different domain.

## Stage R7 — theorem/proof reasoning

Formal verifier gives exact correctness.

## Stage R8 — invention

No target solution is supplied.

The system searches for something that satisfies externally verifiable constraints.

* * *

# 15\. Memory curriculum

Memory progresses through:

```
remember exact event
        ↓
retrieve relevant event
        ↓
choose what to remember
        ↓
choose fidelity
        ↓
compress multiple memories
        ↓
retain source provenance
        ↓
infer general rule
        ↓
identify conflicting memories
        ↓
re-evaluate stale knowledge
        ↓
intentionally forget low-value information
```

Memory policies should be trained across unrelated worlds so they cannot simply learn:

> “video timestamp questions mean save every video frame.”

The same controller should face:

- video
- text
- navigation
- social observations
- scientific experiments
- procedures
- code execution traces

* * *

# 16\. Continual learning

The target is:

```
learn A
learn B
learn C
discover rule D
return to A
still know A
and ideally know A better because of B/C/D
```

This measures:

- stability
- plasticity
- positive forward transfer
- backward transfer
- interference
- consolidation

Experience replay and progress/compress research provide useful controls, not mandatory TNN designs.

Every serious continual-learning experiment measures a full pre/post skill matrix instead of only the newest task.

* * *

# 17\. Curiosity

Prediction error alone is a bad curiosity objective.

Unpredictable noise can remain permanently surprising.

Research on intrinsic motivation suggests using **learning progress** rather than raw error, and Pathak-style work shows curiosity can support exploration from self-supervised predictive error.

TNN's curiosity system should ultimately estimate:

```
expected information gain
+
expected model improvement
+
expected skill gain
+
novelty
+
relevance to unresolved hypotheses
-
resource cost
```

The weights should increasingly be learned.

A white wall and pure random noise should both become boring for different reasons.

* * *

# 18\. Self-model

TNN needs to learn facts about **its own competence**.

Examples:

```
strategy A is good for formal proof
strategy B is cheap but unreliable here
visual reinspection usually resolves this ambiguity
memory retrieval is more useful than another experiment
my current hypothesis model is poorly calibrated in this domain
```

Internal strategy IDs remain generic.

The researcher does not encode:

```
IF geometry THEN strategy_3
```

The system learns strategy/context relationships from outcomes.

* * *

# 19\. Language

Language should attach to the same concepts, memories and hypotheses used elsewhere.

Avoid building a powerful standalone text engine with a weak “TNN brain” beside it.

Target flow:

```
utterance
   ↓
grounded internal structures
   ↓
memory / hypothesis / reasoning
   ↓
response intention
   ↓
language generation
```

Development sequence:

1. token/phoneme structure;
2. grounded names;
3. relations;
4. compositional instructions;
5. temporal references;
6. memory references;
7. explanations;
8. dialogue;
9. technical language;
10. broad reading;
11. argument/reasoning;
12. coding/tool instructions.

Current hard connected-speech evidence remains a major weakness and should stay visible rather than being hidden behind easier speech scores.

* * *

# 20\. Coding and tool use

This is a major missing capability and should become a formal track.

TNN eventually receives generic tools:

```
READ_FILE
WRITE_FILE
SEARCH
RUN
TEST
BROWSE
CALCULATE
INSPECT
```

The reasoning system determines sequences.

Training should begin with tiny deterministic repositories and progress to real permissively licensed repositories.

Eventually evaluate with repository-level tasks inspired by SWE-bench rather than only isolated code completion. SWE-bench was designed around real multi-file software issues requiring repository understanding and executable verification.

Public benchmark solutions must not enter training if we later claim benchmark performance.

* * *

# 21\. Perception

Vision is necessary, but it is not the research program's organizing principle.

## Vision progression

```
raw pixel integrity
→ learned visual features
→ persistent entities
→ viewpoint invariance
→ motion
→ occlusion/object permanence
→ scene relations
→ affordances
→ cross-modal grounding
→ active perception
```

Object-centric approaches such as MONet and relational architectures provide useful research ideas for representing entities and relations.

JEPA research is useful as evidence that useful representations can be learned through latent-space self-supervision instead of reconstructing every pixel. I-JEPA demonstrated semantic image representations using prediction in representation space, and V-JEPA-family work extends the idea to video.

TNN should test these objectives without assuming transformer encoders are required.

* * *

# 22\. Hearing

Progression:

```
raw waveform
→ local acoustic motifs
→ temporal grouping
→ speaker/source identity
→ word-like units
→ phrase structure
→ grounded meaning
→ connected natural speech
```

Training must mix:

- speakers
- microphones
- noise
- speaking rate
- accents
- read speech
- spontaneous speech

Speaker/source families must be held out in evaluation.

* * *

# 23\. Architecture primitives: what may remain hardcoded

Some hardcoding is inevitable.

The correct question is whether it encodes **answers** or merely supplies **general computational machinery**.

## Appropriate fixed substrate

Likely acceptable:

- bytes and numeric types
- memory allocation
- bounds checking
- cryptographic hashing
- deterministic RNG
- generic sparse arrays/maps
- arithmetic primitives
- generic comparison
- generic search mechanics
- checkpoint format
- transactional writes
- provenance
- permission boundaries
- resource accounting
- process isolation
- observation/action APIs

## Prefer learned

- object categories
- words and meanings
- connection topology
- source reliability
- memory policy
- attention targets
- hypothesis priors
- abstractions
- causal relations
- strategies
- subgoals
- skills
- reasoning heuristics
- exploration policy
- concept importance
- compression policy
- which memories deserve exact retention

## Tournament rather than decide philosophically

Interesting uncertain priors should be tested both ways:

- temporal continuity
- object permanence
- causal locality
- compositional operators
- recursion
- hierarchy
- uncertainty representation
- compression bias

If a generic prior dramatically improves transfer across many unrelated domains, it may deserve to become “startup software.”

Lake et al.'s human-learning analysis is useful precisely because it treats such priors as an empirical architecture question rather than assuming blank-slate learning.

* * *

# 24\. Architecture self-revision is earned gradually

TNN should eventually help redesign itself.

It should not begin with permission to rewrite arbitrary substrate code.

Authority ladder:

```
A0  inspect own traces
A1  estimate own failure modes
A2  propose training changes
A3  propose memory-policy/topology changes
A4  execute bounded learner-state/topology changes
A5  propose new reasoning modules or learning rules
A6  build candidate architecture in isolated sandbox
A7  run regression/transfer battery
A8  candidate can be considered for human-approved promotion
```

This produces developmental self-improvement without turning the research process into uncontrolled self-corruption.

* * *

# 25\. Scaling strategy

Intelligence is the priority.

Efficiency remains architectural.

## Report a Pareto curve

For every major candidate plot:

```
capability
vs
training experience
vs
CPU time
vs
RAM
vs
connection count
```

Do not choose the cheapest system automatically.

Do not choose the largest system automatically.

Prefer a candidate when additional compute creates real new capability.

## Sparse by default, dense when evidence supports it

No ideological ban on GPUs or dense modules.

If a dense or GPU component materially expands intelligence and cannot be replaced effectively, use it and measure the tradeoff.

The research question is empirical.

* * *

# 26\. Benchmark portfolio

No single benchmark becomes “the intelligence score.”

## Core reasoning

- ARC-AGI-2
- ConceptARC
- generated ARC-like worlds
- causal intervention worlds
- logic
- counterfactuals
- analogy
- relational reasoning

## Formal reasoning

- miniF2F-style proof tasks
- generated theorem families
- geometry deduction

## Invention

- symbolic law discovery
- algorithm search
- program synthesis
- scientific experiment design
- open-ended challenge generation

## Memory

- exact episodic recall
- video timestamp recall
- long-delay retrieval
- conflicting evidence
- consolidation
- rare-event memory
- selective forgetting

## Language

- comprehension
- reference resolution
- long-context memory
- grounded dialogue
- explanation
- scientific reading
- novel composition

## Coding

- generated repositories
- hidden unit tests
- later SWE-bench-style real repositories

## Perception

- Bongard-LOGO
- Bongard-OpenWorld
- unseen camera/speaker
- occlusion
- cross-modal conflicts

Bongard-OpenWorld is useful because its real-image few-shot concepts remain materially harder for machines than humans in the published benchmark.

* * *

# 27\. Claim policy

The research dashboard should stop saying things like:

> vision 100%

Instead:

```
SENSORY_TRANSPORT
C1
8/8 exact packet reconstruction

HARD_CONNECTED_SPEECH
C3
22.08%

WORLD_EFFECT_LEARNING
C3/C4 depending exact held-out protocol
95.23% clean
88.92% noisy

GENERAL INVENTION
NOT EARNED
```

This prevents infrastructure successes from visually masquerading as intelligence.

* * *

# 28\. Minimum promotion gates

A capability can be called **learned** when:

- update-disabled control fails materially;
- learning produces improvement;
- labels/task IDs are not embedded in architecture;
- source audit is clean.

It can be called **generalized** when:

- architecture and state were frozen;
- evaluation instances were unseen;
- performance survives identifier permutations;
- performance survives meaningful structural variation.

It can be called **transferred** when:

- the same learned mechanism improves a different task family;
- no task-specific rewrite is introduced.

It can be called **inventive** when:

- output was not present in direct training examples;
- there is a hard external correctness test;
- novelty is checked against the admitted corpus/baselines;
- the result survives independent re-verification.

It can be called **general invention** only after independent successes in multiple domains.

* * *

# 29\. Source contamination controls

Before training:

- exact deduplication;
- near-duplicate detection;
- repository/book/paper source IDs;
- benchmark-name scan;
- known solution scan.

Evaluation:

- whole-source holdouts;
- generator holdouts;
- author/repository holdouts;
- post-freeze generated tasks;
- secret seeds.

For invention:

- search training data for the candidate;
- compare against known baselines;
- test semantic near-duplicates;
- require external correctness;
- preserve discovery trace.

* * *

# 30\. The first large work packet

A single long work packet should **not pretend to finish general intelligence**.

Its job is to establish the architecture and falsification machinery from which the wider program can proceed.

## 0:00–0:45 — Baseline and custody

- snapshot current TNN state;
- record canonical hashes;
- inventory current reasoning/memory/perception modules;
- classify existing evidence C0–C7;
- preserve historical negative evidence.

## 0:45–1:45 — Architecture/training separation

Implement/enforce:

- immutable architecture identity per run;
- separate mutable learned-state package;
- training manifest;
- evaluation manifest;
- trace identity;
- fresh-evaluation seed custody.

## 1:45–3:30 — Hypothesis and reasoning substrate

Build the first integrated:

```
hypothesis store
evidence links
support/contradiction update
multiple-candidate generation
counterexample search
discriminating-experiment selection
abstraction output
```

Test on fresh hidden-rule and causal worlds.

## 3:30–5:00 — Learner-owned memory

Build/tournament:

- exact vs summarized storage actions;
- replay;
- consolidation;
- forgetting;
- video/time-indexed episodic storage;
- fixed-policy controls.

Run a first bounded exact-video recall experiment.

## 5:00–6:15 — Dynamic connection fabric

Exercise:

```
50k
250k
1M
```

learner-owned persistent edges.

Collect real scaling data.

Add 5M only if the 1M implementation is behaving sanely.

## 6:15–7:15 — Diverse training-source pipeline

Create local manifests for several source families.

Implement:

- provenance
- licensing metadata
- dedup
- source-family caps
- source-held-out splits

No giant indiscriminate download.

## 7:15–8:15 — Language/code reasoning mini-battery

Test the reasoning substrate on:

- logic expressed in language;
- source-grounded explanation;
- tiny code synthesis;
- hidden executable tests;
- novel composition.

## 8:15–9:30 — First invention battery

Run at least three distinct families:

1. symbolic law discovery;
2. algorithm/program discovery;
3. causal experiment design.

Require external verifiers.

## 9:30–10:00 — adversarial closeout

For each apparent success:

- disable learning;
- scramble labels/rewards;
- inspect source;
- generate fresh tasks;
- ablate key memories/connections;
- rerun from clean state;
- document failures as prominently as successes.

The output of this packet is a **research platform and first integrated reasoning evidence**, not a claim that all missing capabilities have been filled.

* * *

# 31\. Longer program order

After the first integrated packet:

```
P0  reasoning + hypothesis + invention
P0  autonomous memory
P0  continual learning / transfer
P0  interpretability / hardcoding firewall

P1  broad language
P1  coding / computer tools
P1  dynamic connection scaling

P2  vision
P2  natural connected speech
P2  cross-modal grounding

PARALLEL FOUNDATION
R25/R26/R27 native continuity closure
```

Vision remains important without becoming the organizing principle.

* * *

# 32\. Research sources driving the plan

The plan deliberately draws from different research traditions rather than one school.

### Human-like learning and abstraction

Lake, Ullman, Tenenbaum and Gershman argue for causal models, intuitive structure, compositionality and learning-to-learn.

ARC frames intelligence around skill-acquisition efficiency rather than raw task skill; ARC-AGI-2 continues that line for modern reasoning systems.

### Causal reasoning

Causal representation learning specifically targets discovering high-level causal variables from lower-level observations and links causality to transfer/generalization.

### Invention and discovery

AlphaTensor, AlphaDev, FunSearch and AlphaEvolve show several different generate/search/evaluate routes to verifiable discovery.

### Program induction and reusable abstraction

DreamCoder learns libraries of abstractions jointly with search.

### Diverse hypothesis generation

GFlowNets provide methods for learning distributions over diverse high-value composite candidates.

### Formal reasoning

AlphaGeometry demonstrates the value of combining learned proposal machinery with exact symbolic deduction.

### World models and planning

MuZero and DreamerV3 provide strong evidence for learned models as planning tools, without implying that prediction must be the entire cognitive architecture.

### Memory

DNC, Neural Episodic Control, memory-augmented meta-learning and complementary-learning-systems research provide different mechanisms for rapid episodic storage, learned read/write behavior and consolidation.

### Continual learning

CLEAR/experience replay and Progress & Compress provide useful stability/plasticity controls.

### Curiosity

Oudeyer/Kaplan's learning-progress framing and Pathak et al.'s curiosity work provide two useful but distinct exploration objectives.

### Sparse changing topology

SET and RigL establish that learned systems can alter sparse connectivity during training instead of requiring permanently dense topology.

### Perception

I-JEPA/V-JEPA show that meaningful visual/video representations can be learned through self-supervised latent prediction, while Bongard benchmarks directly stress concept induction and generalization.

### Interpretability

Network Dissection, causal model editing, sparse feature decomposition and circuit tracing provide useful methodologies, while TNN should aim for even stronger **native provenance by construction**.

* * *

# 33\. Final research rule

Every new TNN result must answer four questions:

> **What did TNN learn?**

> **What did we give it?**

> **What genuinely new situation did it handle?**

> **What experiment would make us admit that the apparent intelligence was fake?**

If those four answers are not clear, the capability is not ready to count.

The objective is not a beautiful dashboard.

The objective is a system whose increasingly broad competence survives attempts to prove that we accidentally built the answer into it.

The main design decision I would lock now is the **hypothesis/invention loop as the cognitive center**, with prediction, perception, language and tools feeding into it. That is consistent with the user's priority and gives us a concrete way to test whether TNN is doing more than pattern completion.
