# PAM REBUILD — Hypotheses (verbatim, attributed)

Elicited 2026-09-22. Sol via gpt-5.6-sol (UnoRouter); Grok via grok-4.6 (grok-4.7 delisted, verified 2026-09-22). First Sol call returned empty choices:null; retry succeeded.

---

## SOL HYPOTHESES (verbatim)

## H1 — Witnessed Event Lattice

**(a) Architecture.**  
H1 replaces continuous feature streams and categorical labels with a deterministic temporal lattice of witnessed events. Audio and vision encoders detect bounded changes, relations, and continuities, then emit event objects linked into a local causal timeline. Each event is supported by multiple fixed-resolution witnesses from the same input: onset/offset evidence, persistence, spatial or spectral location, and an exact source span. The lattice is modality-neutral: `agent`, `action`, `object`, `relation`, and `change` are shared types, while modality-specific witnesses remain attached. The original audio waveform or image frames remain available as native evidence; the lattice is an index into perception, not a synthesized replacement.

**(b) Percept.**  
A percept is a deterministic ordered set of event records:

```text
Event {
  id: stable hash of source span and content,
  time_span: [start, end],
  entity_slots: typed anonymous IDs,
  predicate: typed change or relation,
  attributes: quantized intervals, not point estimates,
  witnesses: fixed-size references to source audio/video regions,
  support: integer witness score,
  contradiction: integer contradiction score,
  alternatives: at most K mutually exclusive event records
}
```

Granularity is event-scale: onsets, sustained states, transitions, spatial relations, and repetitions. It does not expose sample or pixel values and does not collapse directly to labels such as “laugh.”

**(c) Memory contract.**  
Every event carries a machine-checkable warrant, not merely a confidence score.

1. Memory first checks whether the event's source witnesses are still addressable and whether its support exceeds a fixed modality-specific threshold.
2. It searches for contradictory witnesses and for incompatible existing memories.
3. If support is insufficient or contradiction is nonzero, the event cannot install a permanent memory. It may enter a bounded provisional buffer marked `WITHHOLD`.
4. If support passes but the event conflicts with an existing memory, deliberation receives both the event and the conflict edge. The decision procedure must either request a deterministic re-check of the source span or choose the action that is robust under both interpretations.
5. Installation requires temporal persistence or independent corroboration: two non-overlapping source spans, or two modalities, must produce the same normalized event structure. The installed memory stores the event plus its witness references and contradiction tests.
6. At future use, memory retrieves the event only if the current percept satisfies the stored invariant. A partial match can influence deliberation but cannot trigger an irreversible action by itself.

Thus a confident but unsupported “laugh” becomes a provisional event, while a repeatedly witnessed acoustic transition can change both installation and downstream action selection.

**(d) Efficiency.**  
The target is no more than 35% of raw-value compute and 10% of raw-value percept memory per second of input. The saving comes from processing only detected change windows and storing quantized event intervals plus source references, rather than retaining every sample or pixel-derived activation. Static regions generate no new event records. Fixed-size witnesses bound memory use even for long recordings.

**(e) Beauty.**  
One object, the witnessed event, serves simultaneously as perception, temporal indexing, uncertainty representation, memory evidence, conflict detection, and retrieval key. The same structure explains what happened, where to verify it, and why the system is or is not entitled to remember it.

**(f) Kill bar.**  
On a preregistered adversarial audio-visual benchmark containing at least 10,000 percepts and at least 30% deliberately misleading high-confidence inputs, H1 dies if any of these conditions holds:

- permanent false-install rate exceeds **5%**;
- correct-install recall is below **85%**;
- decision accuracy is not at least **10 percentage points higher** than the frozen Approach A baseline under the same memory budget;
- median percept compute exceeds **35%** of Approach A;
- native audio replay fails a human double-blind field-recording equivalence test at **90% agreement**, or visual reconstruction/imagery is judged realistic by fewer than **80%** of raters.

---

## H2 — Executable Percept Programs

**(a) Architecture.**  
H2 represents perception as a small deterministic program that can be executed against the current sensory evidence. Instead of asserting “there is a dog” or emitting a feature vector, the PAM emits a typed relational program such as “find a persistent compact source; verify four repeated impacts; test whether the source moves left-to-right; reject the hypothesis if the predicted timing pattern is absent.” The program contains observations, tests, and expected consequences. Memory therefore receives a procedure for checking a percept, not just the percept's conclusion. Programs are modality-independent at the operator level and use modality-specific witnesses only inside primitive tests.

**(b) Percept.**  
A percept is a canonical, bounded program:

```text
PerceptProgram {
  subject_slots: typed variables,
  observations: primitive witness bindings,
  relations: temporal/spatial/acoustic constraints,
  tests: ordered deterministic predicates,
  predicted_consequences: bounded list of expected future/current evidence,
  result: PASS | FAIL | UNRESOLVED,
  source_refs: exact evidence spans,
  cost: fixed instruction count
}
```

The granularity is relational and testable: trajectories, repetitions, co-occurrence, occlusion, rhythm, persistence, and change. A program may produce `UNRESOLVED`; it is not forced to produce a label.

**(c) Memory contract.**  
Memory stores and uses percept programs as executable warrants.

1. On arrival, memory canonicalizes the program and executes each test against the referenced evidence.
2. A `FAIL` result is discarded for installation and can be used as negative evidence against a currently retrieved memory.
3. An `UNRESOLVED` result is withheld from permanent memory and is passed to deliberation only as a hypothesis with its unresolved predicates explicitly listed.
4. A `PASS` result may be installed only when the program has at least one successful prediction outside the original source span, such as a later continuation, a second occurrence, or a cross-modal consequence.
5. During a real decision, memory executes stored programs against the current percept. A program that passes can authorize retrieval; one that fails suppresses retrieval; conflicting programs force deliberation to choose an action that remains valid across the surviving programs.
6. Installation is reversible until the program has passed its required external prediction count. This prevents a high-confidence wrong conclusion from becoming durable merely because its initial evidence looked persuasive.

The percept changes downstream behavior by enabling memory to reject, retrieve, or defer a memory based on explicit tests rather than scalar confidence.

**(d) Efficiency.**  
The target is 20% of raw-value compute for repeated scenes and 40% in the worst case, with no more than 15% of raw-value memory. The mechanism is program reuse: a stored test is run on sparse witness bindings and cached intermediate relations. Stable background content is represented by a short program and references, not repeatedly encoded. Compute can increase on ambiguous inputs, but the fixed instruction budget prevents unbounded search.

**(e) Beauty.**  
The single idea is that every percept is a claim together with its own experiment. The same executable object labels an occurrence, explains uncertainty, verifies memory, supplies negative evidence, and guides deliberation. No separate confidence model, memory validator, and contradiction subsystem are needed.

**(f) Kill bar.**  
Using a preregistered suite of 5,000 normal and 5,000 adversarial trials, H2 dies if:

- false permanent installations exceed **3%**;
- fewer than **90%** of wrong high-confidence percepts reach `FAIL` or `UNRESOLVED` before installation;
- decision accuracy under adversarial percepts is below **95% of the best human reference performance**;
- 95th-percentile compute exceeds **40%** of Approach A;
- program replay changes any byte in a byte-identical rerun;
- native audio or realistic visual-output human acceptance falls below **90%**.

---

## H3 — Counterfactual Predictive State

**(a) Architecture.**  
H3 makes the PAM a deterministic predictive-state estimator. It does not primarily describe what is present; it describes the smallest state needed to predict how the sensory scene will change under fixed observation windows and permitted interventions. Audio and vision are converted into typed state transitions with predicted next observations, persistence limits, and counterfactual branches. A percept is accepted only when its predicted continuation agrees with subsequent evidence. The original sensory stream is retained for direct native playback or visual grounding; prediction is used for verification and memory, not for fabricating sensory output.

**(b) Percept.**  
A percept is a bounded predictive state transition:

```text
StateTransition {
  state_signature: canonical typed relational state,
  transition: before -> after,
  invariants: predicates expected to remain true,
  predictions: ordered time-window -> expected perceptual relation,
  branch_set: up to K alternative transitions,
  observed_evidence: source spans,
  prediction_status: UNTESTED | CONFIRMED | BROKEN
}
```

Granularity is change-and-prediction scale: “a periodic source will recur within 420–480 ms,” “the occluded object will reappear on the right,” or “the red region will remain attached to the moving object.” It is neither raw sensory data nor a static semantic label.

**(c) Memory contract.**  
Memory treats each transition as a conditional model with an explicit falsification path.

1. `UNTESTED` transitions are eligible only for provisional retrieval and cannot install a durable memory.
2. Deliberation compares candidate actions by simulating each stored transition over the fixed prediction horizon.
3. When the next sensory window arrives, memory scores each prediction as confirmed, broken, or unresolved using exact deterministic tolerances.
4. A broken prediction downgrades or quarantines the associated memory and contributes negative evidence against future retrieval.
5. A confirmed transition can be installed only after two prediction confirmations from disjoint episodes, or one confirmation plus cross-modal confirmation.
6. If two memories predict incompatible futures, both remain available to deliberation; the chosen action must be evaluated against each surviving branch. The system may withhold action when no branch dominates the fixed decision margin.

This directly changes install, retrieval, and action: unsupported percepts cannot become durable, broken memories are actively retired, and decisions account for predictive consequences rather than belief confidence alone.

**(d) Efficiency.**  
The target is 30% of raw-value compute and 8% of raw-value memory for persistent scenes, with a 60% ceiling on ambiguous scenes. Savings come from state persistence and transition encoding: unchanged structure is carried forward by a state signature, while only deltas and prediction windows are recomputed. Memory stores compact transitions and bounded branches instead of complete sensory histories.

**(e) Beauty.**  
One mechanism, prediction failure, performs perception quality control, memory revision, uncertainty management, and action evaluation. A percept earns authority by surviving time. The architecture turns the unavoidable passage of sensory time into the memory gate itself.

**(f) Kill bar.**  
On a preregistered 20-minute-per-scene streaming evaluation with at least 40% adversarial percept injections, H3 dies if:

- false permanent installation exceeds **4%**;
- fewer than **90%** of injected false percepts are quarantined or withdrawn within the declared prediction horizon;
- confirmed percept recall falls below **80%**;
- action regret is not at least **25% lower** than Approach A under the same compute budget;
- byte-identical replay fails in any tested run;
- audio is judged non-native by more than **10%** of human listeners, or visual output is judged non-realistic by more than **20%** of human raters.


---

## GROK-4.6 HYPOTHESES (verbatim)

Elicited 2026-09-22 via grok-4.6 (UnoRouter). Note: first two attempts failed (120s client timeout; HTTP 524 gateway timeout on long response). Third attempt used a compact prompt with max_tokens 2500 and succeeded. Hypotheses are terse but complete on all six required parts.

G1
(a) Symmetry Group Percept (SGP). Extracts minimal symmetry group generators and fixed points from input via fixed kernels for direct integration into one unified memory module. Encodes the anchoring elements as a single bitstring to enforce global consistency across the brain.
(b) PERCEPT: 512-bit bitstring (256 generators as integer codes, 256 fixed-point coords quantized to 16-bit).
(c) MEMORY CONTRACT: Installs anchor state only if generators match canonical form within 1% variance; else withhold. Changes: enforces symmetry consistency for install/withhold; retrieves by projecting onto group alignment.
(d) EFFICIENCY: 512 bits vs raw millions; saving via group reductions collapsing equivalents, O(log d) compute.
(e) BEAUTY: One idea: group theory distillation of essence, elegant across all modalities.
(f) KILL BAR: False-install rate >5% under adversarial inputs or retrieval accuracy <80%.
G2
(a) Predictive Residual Percept (PRP). Generates forward prediction from current invariants and outputs residual vector as percept to unified memory. Creates contract requiring predictive consistency for state handling.
(b) PERCEPT: 256-element vector of 8-bit signed residuals in invariant space.
(c) MEMORY CONTRACT: Installs if norm < epsilon and predicted hash matches; else withhold. Changes: install requires match, affects retrieve by biasing memory search with prediction.
(d) EFFICIENCY: O(N) compute vs O(N^2) raw; saving by invariant reuse for prediction, 256 bytes compressed.
(e) BEAUTY: Prediction as bridge from perception to memory, elegant unified extension to action.
(f) KILL BAR: False-install rate >8% or integration success <85%.
G3
(a) Relational Signature Percept (RSP). Abstracts input to minimal relation graph and computes cryptographic hash as percept for single-brain memory. Ensures relational template matching for integration.
(b) PERCEPT: 256-bit hash of canonicalized graph adjacency + 32-bit metadata (node/edge density).
(c) MEMORY CONTRACT: Installs only on exact signature match (collision <2^-128); else withhold. Changes: enforces global relational consistency for install/withhold; retrieves via signature lookup then graph expansion.
(d) EFFICIENCY: Constant 288 bits vs raw variable; saving via hashing eliminating redundancy, O(N log N) optimized compute.
(e) BEAUTY: One idea: relational abstraction as universal primitive, elegant wide reach in cognition.
(f) KILL BAR: False-install rate >1% under attack or retrieval accuracy <90%.
