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

## Why this project exists

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

## Results at a glance

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

## Repository guide

This is an evidence-bearing research archive, not a polished package with a
one-command demo. Start here:

| Location | What it contains |
|---|---|
| [`Research/NEXT_AGENT_START_HERE.md`](Research/NEXT_AGENT_START_HERE.md) | Current frontier and operational constraints. |
| [`Research/R32_CURRENT_STATE.json`](Research/R32_CURRENT_STATE.json) | Canonical status, architecture flags, benchmark summary, and next priority. |
| [`Research/R31_FINAL_REPORT.md`](Research/R31_FINAL_REPORT.md) | R31 reference-only architecture results and boundaries. |
| [`Research/R32_E45_NEGATIVE_RESULTS_AND_EVALUATOR_REPAIR.md`](Research/R32_E45_NEGATIVE_RESULTS_AND_EVALUATOR_REPAIR.md) | Full native E45–E50 result narrative and tables. |
| [`Research/R32_E51_ACTION_VALUE_GEOMETRY_AUDIT.md`](Research/R32_E51_ACTION_VALUE_GEOMETRY_AUDIT.md) | Why the next experiment targets continuation value, not a positive UNKNOWN bias. |
| [`Research/tnn_r32_e50_provenance_temporal_contention_discriminator.zag`](Research/tnn_r32_e50_provenance_temporal_contention_discriminator.zag) | Latest native E50 experimental source. |
| [`Research/R32_E50_PROVENANCE_TEMPORAL_CONTENTION_NEGATIVE_3ECA4702_NO_TESTED_CONTENTION_RESCUE/`](Research/R32_E50_PROVENANCE_TEMPORAL_CONTENTION_NEGATIVE_3ECA4702_NO_TESTED_CONTENTION_RESCUE/) | E50 source, binaries, raw ledger, seeds, canonical records, evidence JSON, and SHA-256 manifest. |

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
