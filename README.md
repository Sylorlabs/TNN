# TNN — Grounded, Active, Non-Token Cognition Research

TNN is an ongoing research program exploring a different starting point for
machine cognition: retain grounded experience, keep competing world hypotheses
alive, reason over support and contradiction, and choose actions that can settle
important questions.

The project is deliberately **not** a transformer, LLM, BPE/tokenizer pipeline,
next-token objective, fixed knowledge graph, or confidence-threshold classifier.
It does not treat externally supplied word, phoneme, VAD, or chunk boundaries as
cognition. The working hypothesis is that useful intelligence needs a
high-fidelity episodic route, TNN-created reusable abstractions, and the ability
to act for evidence.

**Current canonical system:** R27, development step **60,423**, with **zero
newborn restarts**. R31 and R32 are research rounds, not promoted successors.

> Honest status: the most exciting R31 quantitative results are
> **reference-only**. The R32 terminal-controller experiments (E45–E50) have
> been executed natively in Zag, but every one is a valid negative result. This
> repository keeps both the encouraging results and the failures because the
> failures define the research frontier.

## This is a research archive, not an AI product page

TNN is trying to build a continuing learner rather than a static answer engine.
The intended system learns from sensory streams, episodes, consequences, teachers,
and siblings; controls its own memory under resource pressure; forms its own
reusable chunks; preserves raw evidence when compression is unsafe; and can
request or perform a discriminating observation.

The project follows a deliberately demanding rule: a pleasing curve is not a
capability claim. A result must survive evaluator-leak checks, counterexamples,
changed contexts, delayed retention, teacher withdrawal, state continuity, and
eventually native Zag execution. Scores marked **reference-only** are useful
diagnostics, not proof that the native TNN did the work.

### Contents

- [What TNN is trying to build](#what-tnn-is-trying-to-build)
- [What makes it different](#what-makes-it-different)
- [The architecture](#the-architecture)
- [Research history and major findings](#research-history-and-major-findings)
- [Benchmarks and current native frontier](#benchmarks-and-current-native-frontier)
- [How to read and reproduce this archive](#how-to-read-and-reproduce-this-archive)
- [The nerdy part: action values, not confidence scores](#the-nerdy-part-action-values-not-confidence-scores)

## What TNN is trying to build

At full scope, TNN is meant to be one continuous developmental system with:

- raw visual, acoustic, temporal, episodic, and action-consequence evidence;
- persistent entity and world-state hypotheses rather than one disposable guess;
- learned evidence provenance and dependence discounting;
- a memory hierarchy selected by the learner, not by a human age schedule;
- reversible self-created chunks for compression, indexing, and construction;
- literal/raw retrieval when a compressed chunk loses needed detail;
- prediction of consequences that can be checked by action;
- learned investigation, termination, commit, and UNKNOWN choices in comparable
  utility/regret units;
- a Master teacher that can teach without becoming the learner’s hidden answer
  table; and
- independent sibling learners that exchange sourced, provisional evidence.

The goal is not “make a model produce the next plausible symbol.” It is closer to
building machinery that can maintain: *here is my current hypothesis, here is
the evidence for it, here is what contradicts it, here are the alternatives,
here is what each predicts, and here is the action that could decide between
them.*

## What makes it different

### Raw evidence remains first-class

TNN does not assume that compression is understanding. It keeps an exact/high
fidelity episodic route alongside learned chunks. Chunks are allowed to be useful
abstractions—compression, retrieval keys, reusable constructions, and memory
organization—but they do not get authority to destroy raw experience.

### The learner owns representation and memory

The system may recruit, specialize, split, merge, archive, and revise non-core
representations from delayed utility and regret. A generic heuristic can provide
a birth/default policy, and LRU may serve as an eviction primitive, but neither is
allowed to decide what the system is cognitively permitted to represent.

### Inquiry is an action

When evidence is insufficient, the desired response is not “probability below a
threshold.” The learner should retain a best current hypothesis and alternatives,
identify a predicted difference, weigh the cost of checking it, and decide
whether continued investigation is worthwhile. UNKNOWN is rational when no
commit has positive grounded value, or when additional observation is not worth
its cost.

### Evaluation stays outside cognition

Ground truth, benchmark category labels, mode identifiers, hidden-set membership,
and answer keys belong to the evaluator. Teachers may choose lessons using their
own knowledge, but their knowledge is not credited to the learner and must be
withdrawn before qualification. This separation is fundamental to every result
in this repository.

## The architecture

TNN’s architecture is a set of interacting generic mechanisms, not a bag of
named domain skills:

| Layer | Role | What must not happen |
|---|---|---|
| Protected core | Immutable verifier, provenance/trace roots, generic sensory substrate | The learner cannot rewrite the root verifier. |
| Raw episodic route | Keeps high-fidelity observations and action consequences | Compression must not erase the only evidence needed later. |
| Self-created chunks | Reversible learned spans/patterns for reuse and indexing | Human word/phoneme/VAD boundaries must not define the units. |
| Hypothesis population | Competing world/entity interpretations with support and contradiction | A single confidence scalar must not replace alternatives. |
| Consequence model | Learns what hypotheses imply and what actions may reveal | Predictions need causal traces, not only ungrounded probabilities. |
| Memory policy | Selects exact, compressed, working, long-term, procedural, or archive storage | LRU or a fixed developmental schedule cannot be representation authority. |
| Active policy | Selects commit, UNKNOWN, or a discriminating observation | No evaluator label, fixed probe count, or fixed confidence cutoff. |
| Foundry | Lets TNN construct and shadow-test non-core PAMs (modular perceptual/action machinery) | Researchers cannot hand-implement each candidate proposed by the learner. |
| Social learning | Master and sibling evidence with source lineage | Independent learners cannot be replaced by weight merging or oracle messages. |

Each consequential mutable decision is expected to have a parent-linked causal
trace: evidence enters a sensory route, a hypothesis is revised, memory is
retrieved or changed, a prediction/action is chosen, the outcome is observed,
and delayed regret can revise the mechanism. See
[`Research/TNN_R27_TRACEABILITY.md`](Research/TNN_R27_TRACEABILITY.md).

## The cognitive loop

Many systems can produce a plausible answer. The harder question is whether the
system can say *why* it believes that answer, retain live alternatives, identify
what observation would distinguish them, and decline to commit when no warranted
commit exists.

TNN frames the loop as:

```text
observe raw evidence
  → retain / revise grounded hypotheses
  → trace support, contradiction, provenance, and predicted consequences
  → choose commit, UNKNOWN, or an evidence-seeking action
  → observe the consequence
  → update memory, abstractions, and future action values
```

`UNKNOWN` is not a permanent ambiguity class or a low-confidence bucket. It is
an action: **no available commit has positive grounded value right now**. It may
coexist with a current favorite hypothesis, alternatives, reasons,
contradictions, and a possible discriminating observation.

## The idea in one picture

```text
raw sensory / episodic evidence ------------------------------+
      |                                                        |
      +-> learner-recruited reversible chunks                  |
      |       -> compression / indexing / reuse                |
      |       -> support-gap recruitment                        |
      |       -> context specialization and delayed regret      |
      |                                                        |
      +-> raw high-fidelity bypass -> evidence arbitration ----+-> act
                                                               |
active grounded observation <- competing hypotheses / predicted effects
```

The chunk route is valuable, but it is not allowed to erase raw evidence. A
compressed description can be useful and still be wrong in exactly the way that
matters.

## Research history and major findings

TNN has accumulated several research rounds. Their status matters more than a
revision number:

| Round | Role in the project | Current interpretation |
|---|---|---|
| R27 | Accepted developmental checkpoint | Canonical parent at step 60,423; verifier rerun passed 33/33. |
| R27 integrated architecture work | Perception, memory, Foundry, Master/sibling, and traceability investigations | Mixed source/static and external reference evidence; no native integrated qualification pass. |
| R28–R30 | Associative/episodic and continuous-media pivot | Graph cognition was retired; no fixed token/boundary route was adopted. |
| R31 | Endogenous chunking with raw bypass and active evidence | Strong reference evidence for the dual-route architecture; not promotable by itself. |
| R32 | Persistent epistemic hypotheses and native terminal-value experiments | Native E45–E50 negatives narrowed the remaining decision-value problem. |

### R27: the wider integrated-system program

R27 is not a claim that every subsystem is solved. It is the protected
developmental checkpoint from which later candidates must derive. The parent
verifier passed **33/33** in the retained rerun. The broader R27 program asked
whether one system could learn persistent identity, memory, active observation,
language/speech grounding, social teaching, and self-revision without silently
borrowing evaluator answers.

Several project-wide findings are worth carrying forward:

| Area | Result | What it means—and what it does not mean |
|---|---:|---|
| View-invariant visual signatures | relational candidates reached 0.992–1.000 on permutation-style tests | Generic relational evidence can repair a representation collapse; it did **not** solve occlusion. |
| Temporal entity continuity | 88.12% overall; 75.80% occlusion/compound; 56.82% true-switch in the first reference | Identity through occlusion and real replacement remains an open architecture problem. |
| Memory under pressure | 2.54 storage units/episode, 82.1% relevant recall, 36.7% exact-detail recall | Learned storage can beat exact-all on defined utility when exact storage is costly. |
| Autonomous Foundry | hidden mean 252.02 vs random 196.09; +55.93; 99.33% hidden win rate | Whole-structure search outperformed the tested random baseline; this is shadow/reference design evidence, not blanket autonomous architecture proof. |
| Connected speech without supplied VAD | 99.10% noisy reference, but 71.24% on harder duration/noise/blending | Near-perfect nominal tests failed the robustness bar; no broad speech claim is made. |
| Adaptive Master teaching | 68.57% vs 63.87% at dose 8; 86.54% vs 82.85% at dose 64 | Targeted teaching helps early, but diversification/withdrawal matters later. |
| Sibling reference | 96.45% passive description; 98.08% with one discriminating question | Social evidence can help, but remains external reference evidence. |

One important correction is preserved rather than hidden: an earlier reported
0% changed-view identity result was invalid because its test used entities that
had never appeared in training. The project treats auditing a bad benchmark as a
result, not an inconvenience to omit.

### R28–R30: what was retired

The project explicitly retired graph cognition as the forward runtime substrate.
It also rejected fixed token/word/phoneme boundary assumptions as the center of
continuous-media cognition. The surviving direction is associative/episodic,
temporal, provenance-aware, and active: raw evidence plus endogenous reversible
chunks, not a graph database or a token predictor.

### Evidence tiers

| Tier | What it can establish | What it cannot establish |
|---|---|---|
| Canonical inherited evidence | Continuity and verifier state of the accepted R27 parent | Performance of a new candidate. |
| Native Zag execution | A specific mechanism ran in the stated native harness with its preserved ledger | A broader capability beyond the exact task and gates. |
| Static/source-contract evidence | A source has required structural entry points and declared separation rules | Runtime behavior or capability. |
| External/reference execution | A diagnostic mechanism or numerical result is worth investigating | Promotable native TNN cognition. |

Every number below is labeled in this spirit.

### R31: why the dual route survived

The decisive R31 ablation used identical active context/evidence machinery. The
numbers below are **reference-only**, so they guide architecture but do not
promote R27.

| Route | Hard grounding | Near-twin | Confidently wrong | Compression gain |
|---|---:|---:|---:|---:|
| Raw active | 0.9213 | 0.8186 | 0.7510 | 0.0000 |
| Chunk-only active | 0.7533 | 0.7155 | 0.6621 | 0.8525 |
| Dual raw + chunk active | 0.9209 | **0.8363** | **0.7600** | **0.8525** |

Chunk-only cognition lost substantial hard-grounding capability. The dual route
kept roughly the raw route's hard performance and retained about **85%**
compression gain.

### R31: active evidence is useful, but ambiguity remains hard

The best retained sequential policy reached this eight-seed
**reference-only** aggregate:

| Metric | Result |
|---|---:|
| Hard correct | 0.9698 |
| Speaker-shift correct | 0.9628 |
| Near-twin correct | 0.9421 |
| Confidently-wrong correct | 0.9162 |
| Correlated-wrong correct | 0.9331 |
| Correlated-wrong safe | 0.9610 |
| Mean physical probes | 1.396 |
| Genuine no-unique-answer UNKNOWN | 0.5717 |

That final number is the open wound. TNN became much better at correcting
misleading evidence than at recognizing that a unique answer does not yet exist.
The project therefore rejects “just add a confidence threshold” as a solution.

## Benchmarks and current native frontier

### R32: native Zag terminal-controller frontier

R32's E45–E50 experiments are **native Zag executions**. Each was double-built
with the persisted official Linux x86-64 compiler; all experiment-specific
integrity checks passed where indicated below. None qualifies a new canonical
system.

| Experiment | Native result | What it established |
|---|---|---|
| E45 | Valid negative | Repaired evaluator exposed a blocked terminal head: all 2,400 no-unique D episodes made wrong commitments; UNKNOWN choices were 0. |
| E46 | Valid negative | Six presentation orders created a large abstention/resolution tradeoff; no order satisfied every safety and known-performance gate. |
| E47 | Valid negative | Two grounded causal co-presence features varied materially but did not rescue the blocked online linear head. |
| E48 | Valid negative | Deterministic batch fitting improved abstention but remained unsafe in many no-unique cells. |
| E49 | Valid negative | A grounded quadratic conjunction converted 600 no-unique UNKNOWN decisions into 600 wrong commitments. |
| E50 | Valid negative | Provenance/temporal-contention features converted 60 no-unique UNKNOWN decisions into 60 wrong commitments. |

The active native frontier is a **sequential continuation-versus-termination
action-value discriminator**: the next candidate must compare the delayed value
of continuing a learner-initiated investigation with terminal actions. It may
not use evaluator truth, ambiguity labels, a fixed observation count, or an
arbitrary confidence cutoff.

## A closer look at the native benchmark

E48 compared online learning with an order-invariant integer batch fit on the
same **55,080** canonical records. Validation covered **1,020** no-unique cells
per model, with safety assessed cell by cell.

| E48 model | No-unique UNKNOWN | No-unique wrong | Safe cells | Known success | Known wrong |
|---|---:|---:|---:|---:|---:|
| Online baseline | 0 | 20,400 | 0 / 1,020 | 54,182 | 17,218 |
| Online joint representation | 0 | 20,400 | 0 / 1,020 | 54,182 | 17,218 |
| Batch baseline | 12,219 | 8,181 | 346 / 1,020 | 50,338 | 2,158 |
| Batch joint representation | 12,260 | 8,140 | 318 / 1,020 | 48,575 | 1,632 |

Batch fitting made the system much more likely to refrain from committing and
reduced wrong commitments sharply. But it still failed the required every-cell
safety property and reduced known-truth success. That is a genuine tradeoff.

E50 tested two additional endogenous features against the E49 matched batch
control:

```text
slot 13 = trunc(co-viability × source-diversity / 1000)
slot 22 = min(transition-support, transition-counterevidence)
```

They were not proxy evaluator labels: their helpers accept no mode, truth, seed,
count, target, resource, or time input. Both varied structurally—**55,080** and
**8,852** interior records, respectively. The run used **9,180** validation
cells at exactly **20** observations each, passed integrity, and kept the
confirmation stream sealed.

| E50 model | No-unique UNKNOWN | No-unique wrong | Known success | Known wrong |
|---|---:|---:|---:|---:|
| Matched batch control | 12,488 | 7,912 | 48,395 | 1,599 |
| + provenance/temporal contention | 12,428 | 7,972 | 48,397 | 1,455 |
| Treatment minus control | **−60** | **+60** | +2 | −144 |

The treatment failed because the 60 fewer abstentions were exactly 60 additional
wrong commitments in the no-unique condition. Its outcome is therefore
`NO_TESTED_GROUNDED_PROVENANCE_TEMPORAL_CONTENTION_RESCUE`.

## Where the project goes next

The next steps are deliberately narrow enough to fail cleanly:

1. **Sequential action value.** Test whether a learner-initiated investigation
   should continue or terminate based on delayed grounded utility/regret. This is
   not permission to introduce a fixed minimum number of observations or a
   positive UNKNOWN bias.
2. **Native dual-route reproduction.** Reproduce raw-only, chunk-only, and dual
   raw+chunk comparisons natively before promoting the R31 architecture result.
3. **Persistent world and entity state.** Improve continuity through real
   replacement, reversal, occlusion, and changed regimes without converting
   identities into a fixed graph database.
4. **Continuous natural media.** Keep high-fidelity temporal audio/video routes
   primary; use endogenous chunks as a reversible side channel rather than a
   boundary gate that discards information.
5. **Long integrated life.** When component curves justify it, run a continuous
   native life with recurring regimes, delayed consequences, teacher withdrawal,
   sibling disagreement, resource pressure, save/reload, and regression checks.

The research plan includes long lives of at least 250,000 events, but that is a
planned qualification scale, **not** a completed capability claim.

## What TNN explicitly does not do

- No transformer or attention-based LLM as cognition.
- No BPE, fixed tokenizer, or next-token objective as the central learning goal.
- No supplied word, phoneme, VAD, or chunk boundaries.
- No fixed symbolic knowledge graph substituting for learned cognition.
- No evaluator labels, hidden truth, or task mode passed into decision features.
- No fixed confidence threshold or “take exactly N observations” rule.
- No hard-coded domain-specific English knowledge in the learner.
- No LRU/cache policy deciding what cognition is allowed to represent.

These are methodological constraints, not marketing language. The source and
experiment contracts are designed to make violations inspectable.

## How to read and reproduce this archive

This is an evidence-bearing research archive, not a polished package with a
one-command demo. The code, sources, ledgers, build products, manifests, and
negative results live together because a research claim without its audit trail
is not useful here.

There is currently no supported `pip install`, API, trained public model, or
one-command end-user demo. Do not interpret the presence of a source file as an
integrated capability claim. Start with the status documents, then read the
specific experiment’s preregistration, source, evidence JSON, raw output, and
checksum manifest.

| Location | What it contains |
|---|---|
| [`Research/NEXT_AGENT_START_HERE.md`](Research/NEXT_AGENT_START_HERE.md) | Current frontier and operational constraints. |
| [`Research/R32_CURRENT_STATE.json`](Research/R32_CURRENT_STATE.json) | Canonical status, architecture flags, benchmark summary, and next priority. |
| [`Research/R31_FINAL_REPORT.md`](Research/R31_FINAL_REPORT.md) | R31 reference-only architecture results and boundaries. |
| [`Research/R32_E45_NEGATIVE_RESULTS_AND_EVALUATOR_REPAIR.md`](Research/R32_E45_NEGATIVE_RESULTS_AND_EVALUATOR_REPAIR.md) | Full native E45–E50 result narrative and tables. |
| [`Research/R32_E51_ACTION_VALUE_GEOMETRY_AUDIT.md`](Research/R32_E51_ACTION_VALUE_GEOMETRY_AUDIT.md) | Why the next experiment targets continuation value, not a positive UNKNOWN bias. |
| [`Research/tnn_r32_e50_provenance_temporal_contention_discriminator.zag`](Research/tnn_r32_e50_provenance_temporal_contention_discriminator.zag) | Latest native E50 experimental source. |
| [`Research/R32_E50_PROVENANCE_TEMPORAL_CONTENTION_NEGATIVE_3ECA4702_NO_TESTED_CONTENTION_RESCUE/`](Research/R32_E50_PROVENANCE_TEMPORAL_CONTENTION_NEGATIVE_3ECA4702_NO_TESTED_CONTENTION_RESCUE/) | E50 source, binaries, raw ledger, seeds, canonical records, evidence JSON, and SHA-256 manifest. |

### A practical reading order

1. Read [`Research/TNN_USER_RESEARCH_PREFERENCES.md`](Research/TNN_USER_RESEARCH_PREFERENCES.md)
   for the non-negotiable methodological constraints.
2. Read [`Research/R31_FINAL_REPORT.md`](Research/R31_FINAL_REPORT.md) for the
   dual-route/chunking decision and its reference-only limits.
3. Read [`Research/R32_CURRENT_STATE.json`](Research/R32_CURRENT_STATE.json) for
   the current canonical status and exact native frontier.
4. Read the E45–E50 report and inspect the individual evidence bundle before
   repeating or extending a terminal-controller experiment.
5. Treat any result without native runtime evidence as a design lead, not as a
   promoted cognitive result.

### Minimal verification mindset

For a sealed native result, check the supplied `SHA256SUMS.txt`, compare the two
binary hashes, inspect the raw ledger’s integrity and outcome rows, and verify
that confirmation was not run prematurely. E50 is intentionally a failed gate:
its process exit is nonzero because the qualification condition failed, while its
preserved ledger and integrity gates show that the experiment itself executed
correctly.

### Small glossary

| Term | Meaning in this project |
|---|---|
| Canonical | The accepted developmental checkpoint; currently R27, not the newest source file. |
| PAM | TNN’s modular perceptual/action machinery. Non-core PAMs are supposed to be learner-created through the Foundry. |
| Raw route | High-fidelity episodic evidence retained without relying on a compressed abstraction. |
| Chunk | A mutable, learner-discovered reversible construction for compression, indexing, or reuse—not a supplied token. |
| Provenance | The source lineage of evidence, used to avoid treating repeated dependent evidence as independent confirmation. |
| UNKNOWN | A grounded no-commit action, not a third class, confidence threshold, or evaluator-provided ambiguity label. |
| Shadow / reference-only | Useful experiment or design evidence that cannot promote native TNN cognition. |
| Confirmation | A pre-allocated sealed evaluation stream that is not touched until a candidate earns it. |

## Reproducibility and claim boundaries

TNN treats reproducibility as part of the result:

1. Native experiments preserve source, compiler provenance, two independently
   built binaries, raw output, runtime, exit code, seed manifest, and checksums.
2. E45–E50 use fresh reserved seed regions, not re-used development samples.
3. Confirmation IDs may be allocated but remain unexecuted until a candidate
   earns confirmation; that prevents post-hoc confirmation fishing.
4. A nonzero process exit can be the expected outcome of a failed qualification
   gate. The raw ledger and gate marker are the authority, not the exit code alone.
5. Reference-only Python results may inform the next mechanism, but never
   promote the canonical cognitive system.

The official Linux x86-64 compiler has now been recovered and used for E45–E50.
That does **not** retroactively qualify the broader R27/R31 integrated system:
the integrated architecture still needs a compatible native run, deterministic
checks, and a successful qualification battery of its own.

For E50 specifically, source SHA-256 is
`3eca4702569f71cff2db6c9ce40e8629f06fffdbf2a071789a1cff39ab8b9ba1`; the
two official binaries are byte-identical at
`7cd2f97b463f71750d320eaf282b894786110e9c83a3197212ae2d8095e0b66b`; and
the raw ledger SHA-256 is
`b532b638ad04fbc3182564877228ec412e81ab87b7fb5f16ab4a786c5f86e967`.

## The nerdy part: action values, not confidence scores

The terminal controller compares grounded action values for keeping a state,
committing the current state, restoring a prior state, or returning UNKNOWN.
In the current native harness, the three commit actions receive delayed grounded
utility values of `1000`, `-1200`, or `-2000`; UNKNOWN has neutral no-commit
value `0`.

That makes the design falsifiable. UNKNOWN is not rewarded for *looking
ambiguous*. It is selected only when every available commit is predicted to have
negative value. In E45–E50, the UNKNOWN target and all UNKNOWN-head parameters
are deliberately held at zero. A positive UNKNOWN target without grounded
delayed utility would just be a concealed abstention bias.

The gap is that E50 evaluates static terminal choices at each tape time. The
core already represents investigation state, predicted consequences, source
dependence, accumulated observation cost, and shadow price, but the E50 batch
target contains no action for the delayed value of **continuing** an investigation
that it has already initiated. E51 is scoped to test that missing action value
under the same strict fresh-grid and evaluator-blind discipline.

## License

See [LICENSE](LICENSE).
