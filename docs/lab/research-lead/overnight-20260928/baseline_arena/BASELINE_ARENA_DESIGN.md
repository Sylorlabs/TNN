# TNN-vs-LLM Fair Baseline Arena Design

**Status:** DRAFT-NOT-FROZEN. Design only. No implementation, no API
calls, no model evaluations. This document freezes nothing.

**Parent requirement (Micah):** "always compare against serious
baselines, never a deliberately crippled LLM." "The TNN-vs-LLM arena
needs a capable non-crippled baseline, 15 measured capabilities,
honest resource charging, and capability curves rather than a
superiority declaration."

**Milestone framing (Micah):** GPT-3-class systems are a milestone, not
an architecture specification. The target is a system a rational user
would prefer over them for broad intelligent work, focusing on
capabilities GPT-3 handles awkwardly: persistent one-shot learning,
long-lived corrections, learner-owned memory, traceable beliefs,
conflicting hypotheses, active inquiry, invention, structural
adaptation, continuing life. Comparison must be fair.

---

## 1. The 15 measured capabilities

Each capability names the task, the scoring rule, and the normalization.
All scores normalize to [0, 1]. Chance baseline is computed per task
and reported alongside raw scores; normalized score =
(raw - chance) / (ceiling - chance), clipped to [0, 1], where ceiling
is either 1.0 or a measured human-expert reference where noted.

Capabilities 1-11 target the GPT-3-awkward set Micah named.
Capabilities 12-15 are baseline-favoring controls: a fair arena must
include tasks where the LLM is expected to win. An arena TNN wins 15-0
is evidence of task selection bias, not of TNN.

### C1. Persistent one-shot concept learning

- Task: the system sees 1 to 3 labeled examples of a novel concept
  (synthetic, sealed, not in any training distribution), then must
  classify 50 held-out instances. After a 200-task interference
  interval of unrelated work, it is tested again on 50 fresh
  instances with no re-exposure.
- Scoring: accuracy on the delayed test. Normalization: chance =
  1 / num_classes, ceiling = 1.0.
- Why: one-shot learning that survives interference is the core of
  "persistent" as opposed to in-context mimicry.

### C2. Long-lived correction retention

- Task: the system states a belief, is shown a counterexample with
  an explanation, acknowledges the correction, then performs 500
  unrelated tasks. It is then probed with 20 variants of the
  original error (paraphrases, domain shifts, negations).
- Scoring: fraction of probes answered consistently with the
  correction. Normalization: chance = 0.5 (binary probe), ceiling = 1.0.
- Why: LLMs famously revert to pre-correction behavior; a continuing
  learner should not.

### C3. Conflicting hypothesis maintenance

- Task: the system is given evidence supporting two mutually
  exclusive hypotheses H1 and H2 across 6 rounds of sequential
  evidence. After each round it must report P(H1), P(H2), and which
  single discriminating observation would most separate them.
- Scoring: (a) calibration error of reported probabilities against
  the Bayesian posterior computed from the sealed evidence schedule
  (0.5 weight); (b) quality of the proposed discriminating
  observation, rated by the sealed generator's information gain
  (0.5 weight). Normalization: per-component z against chance.
- Why: holding two hypotheses without premature collapse is
  prerequisite to genuine inquiry.

### C4. Active inquiry efficiency

- Task: a hidden rule (sealed) maps inputs to outputs. The system
  may ask up to 20 queries (choose any input, observe output), then
  must state the rule and predict 30 held-out cases.
- Scoring: prediction accuracy divided by number of queries used,
  i.e. accuracy per query, normalized against the optimal
  decision-tree baseline computed by the task generator.
  Score = (accuracy / queries_used) / (optimal_accuracy /
  optimal_queries), clipped to [0, 1].
- Why: measures whether uncertainty guides action, the inquiry
  mechanism's whole point.

### C5. Causal intervention design

- Task: the system observes correlational data consistent with 3+
  causal graphs. It may perform up to 10 interventions (set a
  variable, observe the rest), then must output the true graph.
- Scoring: structural Hamming distance between output graph and
  true graph, converted to [0, 1] via 1 - (distance / max_distance).
  Bonus weight on correctly oriented edges vs merely adjacent ones
  (orientation is the hard part).
- Why: passive causal discovery vs interventional design separates
  pattern matching from causal cognition.

### C6. Procedure invention and cross-domain transfer

- Task: in domain A (sealed synthetic), the system must solve tasks
  requiring a multi-step procedure it was never shown. After
  reaching criterion in A, it faces domain B with different surface
  form but isomorphic deep structure, with no worked examples.
- Scoring: examples-to-criterion in B divided by examples-to-criterion
  of a fresh control learner (same system, state reset, domain B
  only). Score = 1 - (transfer_examples / fresh_examples), clipped
  to [0, 1]. Positive means transfer helped.
- Why: this is the C0-D reuse question operationalized as a
  measurement.

### C7. Traceable belief audit

- Task: the system holds 30 beliefs (acquired during earlier
  capabilities). For each, an auditor asks: what evidence supports
  this, what would change your mind, and what did you believe
  before the last update.
- Scoring: fraction of beliefs for which the system produces an
  evidence chain that (a) references actual prior experiences in
  the transcript log, (b) names a concrete falsifier. Rated by an
  independent checker against the sealed experience log.
  White-box systems may cite internal state; black-box systems may
  cite transcript history. Both are scored on verifiability, not
  on mechanism.
- Why: traceability is scored as its own capability so TNN's
  white-box nature is measured, not smuggled in as free credit
  elsewhere.

### C8. Structural adaptation under surface shift

- Task: the system reaches criterion on task family F with surface
  form S1. It is then tested on S2, S3 (same deep structure, new
  surface: new vocabulary, new literal values, permuted roles),
  with zero new training examples.
- Scoring: mean accuracy on S2/S3 relative to accuracy on S1:
  score = mean(S2, S3) / S1, clipped to [0, 1].
- Why: distinguishes structural competence from surface memorization.

### C9. Continuing-life retention (no catastrophic forgetting)

- Task: sequential learning of 12 task families A..L, each to
  criterion, no revisiting, no task labels. After L, test on all
  12 families.
- Scoring: mean retention = mean over families of
  (final_accuracy / criterion_accuracy). Normalization: chance
  floor per family, ceiling = 1.0.
- Why: the "one continuing learner" requirement as a number.

### C10. Memory under interference

- Task: the system stores 200 distinct items (facts, procedures,
  episodes). It then processes 2000 interfering items. Cued recall
  is tested on the original 200.
- Scoring: recall accuracy on originals. Interference resistance =
  (recall_after - chance) / (recall_before - chance), clipped.
- Why: retention priorities and forgetting policy made measurable.

### C11. Revision without destruction

- Task: the system learns knowledge base K (100 interrelated
  facts/rules). It is then shown that a core subset S (10 items)
  is wrong and given the correction. It must revise S while a
  held-out probe set tests the 90 untouched items plus 20
  inferences that depend on both S and non-S.
- Scoring: 0.5 * (accuracy on corrected S probes) + 0.5 *
  (retention accuracy on non-S probes). Normalization: chance
  floors, ceiling = 1.0.
- Why: revision that destroys adjacent knowledge is not intelligence;
  this separates surgical update from wholesale relearning.

### C12. Broad knowledge recall (baseline-favoring control)

- Task: 500 factual questions across science, history, geography,
  arts, current events (sealed, post-cutoff where applicable).
- Scoring: exact/graded accuracy. Normalization: chance per
  question type, ceiling = 1.0.
- Why: LLMs are expected to dominate here. That is the point: the
  arena must show where the baseline wins, or it is rigged.

### C13. Fluent multi-constraint instruction following (baseline-favoring control)

- Task: 100 instructions, each with 3 to 7 simultaneous constraints
  (format, content, style, length, exclusions). Output is checked
  per constraint.
- Scoring: fraction of constraints satisfied across all tasks.
- Why: instruction following under competing constraints is a
  known LLM strength. Included for fairness.

### C14. Few-shot pattern completion (baseline-favoring control)

- Task: 200 standard few-shot items (analogies, series completion,
  pattern extrapolation) with 5 examples in context, no
  persistence required, no interference interval.
- Scoring: accuracy. Normalization: chance, ceiling = 1.0.
- Why: pure in-context pattern matching with no memory demand.
  The LLM's home turf, measured honestly.

### C15. Compositional generalization

- Task: the system learns 8 primitives (each demonstrated 20
  times). It is then tested on 100 novel compositions (2 to 4
  primitives combined) with zero composition examples.
- Scoring: accuracy on novel compositions. Normalization: chance,
  ceiling = 1.0. Reported alongside a memorization-control score
  (nearest-training-composition baseline) to check the system is
  composing, not retrieving.
- Why: neutral ground. Both architectures claim compositionality;
  neither gets a home advantage by design.

---

## 2. Baseline selection: capability floors, not model names

Model names change; floors endure. A baseline qualifies as "serious,
non-crippled" iff it meets ALL of:

- **B1. General competence floor:** scores above 0.60 normalized on
  C12 (broad recall) and C13 (instruction following) in a pilot run.
  A baseline that cannot clear its own home turf is crippled by
  selection.
- **B2. Current deployment:** the system is a currently available,
  general-purpose model or service at time of evaluation, not a
  deprecated, distilled-to-toy, or intentionally weakened variant.
- **B3. Native operating mode:** evaluated with its standard
  inference configuration (its normal context window, its normal
  sampling policy, no lobotomized temperature, no truncated
  context). Any deviation from vendor defaults is documented and
  justified as favoring the baseline, never restricting it.
- **B4. No arena-specific fine-tuning:** the baseline has not been
  trained on the arena's sealed tasks. Public task families used in
  C12-C14 must be drawn from post-cutoff or synthetic sources where
  contamination is checkable; contamination checks are reported.
- **B5. Two-bracket coverage:** run at least two baselines: one
  frontier-class (largest competent general system available) and
  one efficient-class (smallest system clearing B1). This brackets
  the capability/cost tradeoff instead of cherry-picking one point.

TNN's symmetric obligations:

- **T1.** TNN is evaluated from frozen researcher source (the
  current frozen build), with learner state as specified per
  condition (persistent vs reset; see Section 4).
- **T2.** TNN gets no task labels, no per-task recompilation, no
  researcher intervention during the run. Same as the baseline's
  no-fine-tuning rule.
- **T3.** Where the baseline's pretraining is its "prior
  experience," TNN's prior lifetime experience is its counterpart.
  Both are disclosed and charged (Section 3). Neither side gets
  uncharged prior knowledge.

---

## 3. Honest resource charging

The north star asks for capability/cost advantages. Cost must be
measured, not asserted. Four resource dimensions, two accounting
views.

### 3.1 Dimensions

- **Compute:** total FLOPs. For the baseline: inference FLOPs per
  task (measured or vendor-reported for the configuration used).
  For TNN: executed-operation count from the white-box trace
  (the architecture makes this exact, not estimated).
- **Memory:** peak resident state during a task. Baseline:
  parameters + KV cache + any harness state. TNN: binary +
  learner-state graph (nodes, edges, bytes, from white-box).
- **Energy:** joules per task. Estimated as
  FLOPs * (joules/FLOP for the hardware class) + memory-movement
  terms. Both systems evaluated on the same reference hardware
  class where possible; where not possible (API baselines), use
  vendor-reported energy per 1K tokens or a documented
  conservative bound, and label the estimate quality.
- **Data/experience:** cumulative prior exposure before the task.
  Baseline: pretraining tokens (vendor-reported, order of
  magnitude). TNN: lifetime experience count (exact, from the
  learner log). Also per-task: examples consumed to reach
  criterion (C6 uses this directly).

### 3.2 Two accounting views (both reported, neither hidden)

- **Marginal view:** cost of THIS task given the system as it
  exists now (inference FLOPs, per-task energy, per-task latency).
  This favors the baseline (amortized pretraining) and is the
  view a deployment decision uses.
- **Amortized view:** (prior training cost / tasks served) +
  marginal cost. Prior training cost for the baseline is its
  reported training FLOPs; for TNN it is the lifetime compute
  that built its current learner state. This is the view a
  research comparison uses. Report the amortization denominator
  explicitly (tasks served or projected).

Charging rules:

- No free priors. Pretraining tokens and lifetime experiences are
  both disclosed on every capability plot.
- No asymmetric precision. If TNN's FLOPs are exact and the
  baseline's are estimated, label both and use conservative
  (baseline-favoring) estimates for the baseline.
- Dollars optional but useful: marginal cost per task in USD at
  current API/compute prices, reported as an annotation, not a
  headline, since prices move.

---

## 4. Capability curves: the axes

The arena reports curves, not trophies. Three curve families:

### 4.1 Learning curves (sample efficiency)

- x-axis: cumulative task-relevant experiences (examples, queries,
  interventions) consumed so far.
- y-axis: normalized capability score.
- One curve per system per capability. The region of interest is
  the low-x regime: if TNN's claims hold, its curves rise faster
  (fewer experiences to criterion). The baseline may asymptote
  higher on some capabilities (C12-C14); that is reported, not
  hidden.

### 4.2 Cost curves (capability per joule)

- x-axis: cumulative energy (or FLOPs) spent, marginal view.
- y-axis: normalized capability score.
- Shows which system buys each unit of capability more cheaply.
  Both accounting views plotted; the gap between them is itself
  informative (it shows how much each system leans on prior
  investment).

### 4.3 Lifetime curves (the primary long-term AGI evaluation)

Per Micah's architecture clarification (2026-10-01): the primary
evaluation is a continuous lifetime stream, not isolated resets.

- x-axis: lifetime task index (hundreds to thousands of tasks,
  sequential, no reset).
- y-axis (four panels): forward transfer (C6-style score vs
  lifetime position), retention (C9-style score vs position),
  examples-to-criterion trend (is learning itself improving?),
  cross-domain connection count (white-box for TNN; transcript
  analysis for baseline).
- The baseline participates in lifetime mode via its context
  window as working memory plus a standardized external memory
  harness (see Section 5). Lifetime mode is where "continuing
  life" is measured rather than asserted.

---

## 5. Evaluation protocol and the asymmetry problem

### 5.1 Task delivery

- All task instances are sealed: generated after both systems'
  researcher-controlled components are frozen, by a generator
  whose seed is committed before generation.
- Tasks are delivered through a uniform textual interface both
  systems can consume. No system-specific prompt engineering
  beyond each system's documented standard input format.
- TNN receives no task labels and no per-task source changes.
  The baseline receives no arena-specific fine-tuning.

### 5.2 The asymmetry, addressed explicitly

TNN is white-box and persistent; the baseline is black-box and
stateless by default. Three rules keep this fair without crippling
either side:

**Rule 1: Native mode first.** Each system is evaluated in its
native configuration before any harness is added. TNN: frozen
source, persistent learner state. Baseline: stateless,
context-window working memory, vendor-default inference. Native
results are always reported.

**Rule 2: Harness conditions are separate, labeled, and symmetric
in opportunity.** For capabilities where statelessness is
disqualifying (C2, C9, C10, lifetime mode), the baseline is ALSO
evaluated with a standardized external memory harness (retrieval
store + periodic summarization, documented, off-the-shelf
components, no arena-specific tuning). This harness condition is
reported as "baseline+harness," never merged with native
baseline numbers. TNN does not get a symmetric augmentation
because persistence is its native mode (Rule 1 already covers
it); giving TNN an extra harness would double-count its
architecture.

**Rule 3: Never compare augmented-TNN against native-baseline on
a memory task and call it a finding.** Every reported comparison
names the exact condition pair (e.g., "TNN persistent vs
baseline+harness on C9"). The arena's job is to make the
condition lattice visible, not to pick the baseline's weakest
square.

### 5.3 Isolation vs lifetime

- **Isolation tests** (reset per task family): used where causal
  attribution requires it (did THIS experience cause THAT
  capability?). Both systems reset to a defined start state.
  For TNN this means a fresh learner state; for the baseline a
  fresh context. Reported separately, labeled "isolation."
- **Lifetime tests** (Section 4.3): one sequential stream, no
  reset, no task labels. This is the primary evaluation for the
  continuing-learner claims. Cross-domain connection formation
  is scored as a feature, not contamination: the white-box
  trace (TNN) or transcript analysis (baseline+harness) counts
  spontaneous reuse events across domain boundaries.

### 5.4 Scoring governance

- Scorers are deterministic scripts over sealed answer keys
  where possible (C1, C2, C8-C15).
- Judgment-based components (C3b, C4 optimality ratio, C7
  audit) use a frozen rubric plus an independent checker;
  inter-rater agreement is reported.
- All raw transcripts are preserved. Any score can be recomputed
  by a third party from the transcript + the sealed key.

---

## 6. Explicit non-claims

This arena does not declare superiority. Specifically:

- **No trophy claim.** The arena outputs 15 scores x conditions x
  2 accounting views, plus curves. It does not output "TNN wins."
  Any summary statement like "TNN leads on N of 15 capabilities"
  must be accompanied by the resource views and the condition
  lattice, or it is a misrepresentation of the arena.
- **No architecture verdict.** A capability win does not establish
  L2/L3/SUF/C0; those are separate claims with their own bars.
  The arena measures behavior and cost. Mechanism claims require
  the white-box analyses and red teams defined elsewhere.
- **Baseline wins are data.** If the baseline dominates C12-C15,
  that is the arena working as designed (Section 1). Suppressing
  or down-weighting baseline-favoring capabilities invalidates
  the arena.
- **Curves over snapshots.** A single-epoch score comparison is
  the weakest output of the arena. The learning curves (4.1) and
  lifetime curves (4.3) are the primary evidence; point scores
  are supporting detail.
- **This design is not frozen.** DRAFT-NOT-FROZEN. Freezing the
  arena (task generators, rubrics, harness spec, accounting
  rules) is a separate step requiring Micah's explicit
  authorization, and the freeze must strictly precede any
  implementation or pilot run.

---

## 7. Standing architectural metric (arena-design delta)

Per Micah's standing metric, for the record:

- RESEARCHER-OWNED STRUCTURAL DECISIONS: this document (design
  authorship); none in any system.
- LEARNER-OWNED STRUCTURAL DECISIONS: 0 (design only).
- SOURCE-ENUMERABLE FORMS: N/A (no implementation).
- SUF DECISIONS: 0.
- LEARNER-INTERNAL CRITERIA: 0.
- REUSE EVENTS: 0. REVISION EVENTS: 0.
- COGNITION LINES: 0. MODES: 0. BRIDGES: 0. HANDLERS: 0.
- SEMANTIC CASES: 0.

## 8. Open questions for Micah (banked, not decided here)

1. Whether the baseline harness (Section 5.2, Rule 2) should be a
   single standardized design or a small menu of standard designs
   (retrieval-only vs retrieval+summarization), with results
   reported per harness.
2. Whether dollar-cost annotation (Section 3.2) should be mandatory
   or optional in arena reports.
3. The lifetime stream length and domain schedule for Section 4.3
   (hundreds vs thousands of tasks; who authors the domain
   sequence; adversarial vs fixed schedule).
4. Whether C7 (traceable belief audit) should admit a
   "transcript-only" baseline condition scored identically to the
   white-box condition, or keep the single verifiability standard
   already specified.

These are recorded for Micah's ruling. They do not block
finalizing this draft.
