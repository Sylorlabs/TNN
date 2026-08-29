# TNN User Research Preferences

**Status:** Living project constraint file  
**Last updated:** 2026-08-20  
**Scope:** TNN research design, implementation, evaluation, promotion, rollback, and reporting.

This file records the user's explicit preferences separately from experimental findings. Future agents should update it when the user states a new preference, correction, boundary, or priority. New entries should preserve the original intent, mark whether the preference is explicit or inferred, and note any experimental evidence that supports or conflicts with it.

## Confirmed preferences

### 1. Minimize hardcoding

**Preference:** Avoid hardcoding whenever a learnable mechanism is feasible. Hardcoding is acceptable for genuinely core infrastructure, immutable safety/verification boundaries, or when strong controlled evidence shows that a hardcoded mechanism is currently necessary and superior.

**Operational consequence:**

- Do not hardcode English grammar, dictionaries, category names, social concepts, object identities, target answers, or task-specific solution rules into mutable TNN cognition.
- Treat hardcoded prostheses as controls, not learner capability.
- Before promoting a hardcoded runtime mechanism, compare it against serious learned candidates using hidden tests, delayed tests, transfer tests, and regression tests.
- Prefer generic substrate mechanisms over named task modules.
- Record every remaining hardcoded component and why it remains.

**Source:** Explicit user instruction on 2026-08-20: prefer no hardcoding when possible; hardcoding should remain only when core/necessary or when real in-depth results justify it.

### 2. Hardcoded teachers are an acceptable special case

**Preference:** A hardcoded Master TNN may be highly capable because it is a teacher working with the base TNN, not a hidden implementation of the learner's final cognition.

**Operational consequence:**

- The Master may know mature English, evaluator identities, curriculum structure, and pedagogy.
- The Master should diagnose the learner's exact confusion, choose grounded examples and minimal contrasts, vary wording/context, request teach-back, test delayed transfer, and withdraw as competence rises.
- Master knowledge must not be copied directly into mutable TNN as dictionaries, named concept modules, target labels, or answer tables.
- Teacher dependence must be measured after withdrawal.
- Direct grounded evidence and the immutable root verifier remain more authoritative than the Master.

**Evidence already established:** Adaptive/grounded Master teaching repeatedly outperformed symbolic yes/no and weaker teaching. R27's stronger Master bridge improved general-to-specific abstraction from 66.67% to 94.44% without a new named social-language module. Earlier work also found a trained TNN teacher could outperform the hardcoded Master on a bounded teaching task.

### 3. Training-first diagnosis

**Preference:** When a result is weak, first determine whether the failure is caused by insufficient data, poor lesson quality, missing contrasts, bad curriculum ordering, inadequate rehearsal, or a weak teacher. Change architecture only when the learning curve or error structure shows that training is no longer the main bottleneck.

**Required diagnosis sequence:**

1. Establish a fixed-architecture baseline.
2. Run quantity/dose curves.
3. Improve teaching quality and targeted contrasts.
4. Test changed contexts, delay, noise, and counterexamples.
5. Classify the residual failure.
6. Try architecture only for a measured plateau, representation mismatch, interference, missing cognitive operation, or resource-allocation failure.
7. Shadow-test and roll back on regression.

### 4. Strong, in-depth experiments rather than weak demonstrations

**Preference:** Use serious tests that can disconfirm the intended claim. Do not promote mechanisms from tiny, favorable, single-seed, or circular evaluations.

**Minimum evidence expectations where feasible:**

- multiple independent seeds;
- development/selection data separated from hidden evaluation;
- meaningful baselines and negative controls;
- hard near-neighbor and counterexample cases;
- delayed retention and teacher withdrawal;
- clean, noisy, changed-context, and interference conditions;
- regression protection for accepted historical capabilities;
- exact provenance and authorship separation;
- preserved failed candidates and negative results;
- fresh-process save/reload verification;
- independent archive extraction and verifier reruns.

### 5. Do not mistake evaluator help for learned cognition

**Preference:** External labels may be used for scoring and a teacher may use them to choose lessons, but evaluator truth must not silently enter mutable learner state.

**Operational consequence:** Report separately:

- what TNN observed, learned, proposed, selected, and retained;
- what the hardcoded Master knew and taught;
- what the researcher/assistant mechanically implemented;
- what the external verifier used only for scoring and promotion.

### 6. Siblings should be real independent learners

**Preference:** Siblings should question, teach, debate, share sourced evidence, and potentially work as a development team while retaining independent identities and histories.

**Operational consequence:**

- Do not merge sibling weights and call that social learning.
- Repeated copies from one origin remain one evidence lineage.
- Sibling information stays provisional until locally verified.
- Questions should target uncertainty or discriminate hypotheses, not request arbitrary extra data.
- Report absolute performance as well as relative gains.

### 7. Protect accepted state and core mechanisms

**Preference:** Continue the same developmental brain; do not restart merely to make an experiment easier. Core PAMs, exact archive, provenance, rollback, and immutable root verification remain protected unless unusually strong evidence justifies replacement.

**Operational consequence:** New mechanisms begin as shadow/non-core candidates. The only canonical checkpoint is changed after promotion gates pass.

### 8. Capability first; compute is secondary but must be accounted for

**Preference:** Do not reject a real capability gain only because it costs more, but do not promote expensive machinery that ties or regresses a simpler mechanism.

### 9. Report claim boundaries plainly

**Preference:** Controlled or generated results must not be renamed as unrestricted camera vision, natural adult speech, teenager/adult English, human superiority, open-ended recursive self-improvement, AHI, or production readiness.

### 10. Preserve terminology and explain acronyms

**Preference:** Use consistent project terminology and expand acronyms when introduced.

## Current decision hierarchy

When deciding whether to promote a mechanism, use this order:

1. hidden capability and transfer;
2. regression safety;
3. teacher-withdrawal and delayed retention;
4. provenance/evaluator-leak audit;
5. robustness under noise and counterexamples;
6. state continuity and deterministic reload;
7. compute/memory cost;
8. conceptual elegance.

A cleaner or more biologically appealing mechanism does not replace a working one unless the evidence supports it.

## Hardcoding ledger rule

Every checkpoint should include a table with:

- hardcoded component;
- location;
- purpose;
- whether it enters mutable cognition;
- learned alternatives tested;
- evidence for retaining it;
- removal/retest trigger.

## Preference update log

| Date | Status | Preference/change | Source |
|---|---|---|---|
| 2026-08-20 | CONFIRMED | Prefer no hardcoding where possible; retain it only for core necessities or after rigorous results justify it. | Direct user message |
| 2026-08-20 | CONFIRMED | Hardcoded Master teachers are acceptable because strong teacher-to-base-TNN training has worked best so far. | Direct user message plus retained R22-R27 evidence |
| 2026-08-20 | CONFIRMED | Use real, in-depth tests rather than weak tests. | Direct user message |
| 2026-08-20 | CONFIRMED | Maintain this living preference file as the conversation continues. | Direct user message |

## Update protocol for future agents

After an explicit user preference message:

1. add or revise the relevant confirmed preference;
2. append one dated row to the update log;
3. distinguish preference from experimental fact;
4. note contradictions rather than silently replacing history;
5. copy the updated file into the next verified release and persistent `/TNN/Research/` library.

## 2026-08-20 update — Native Zag v2, autonomous PAM creation, capability-scale architecture

### 11. Pure Zag v2 implementation path

**Preference:** New TNN architecture and experiments should be implemented natively in Zag v2. Python must not become the implementation path for TNN cognition, PAMs, learning, or self-revision. Python may be used only as external analysis/evaluation glue when absolutely necessary, and such use must never be counted as TNN capability.

**Operational consequence:**
- New PAM lifecycle, sensory learning, architecture-revision machinery, and integrated TNN execution belong in native Zag v2.
- Any result produced only by a Python research surrogate is diagnostic evidence, not a promotable TNN mechanism.
- Native strict compilation, checked-mode parity, deterministic state continuity, and fresh-process verification are required for promotion.

### 12. TNN-created non-core PAMs must be autonomous

**Preference:** Once TNN proposes a non-core PAM, the human/researcher should not have to mechanically implement that PAM. Human implementation is acceptable only for protected core substrate that TNN cannot access.

**Operational consequence:**
- Replace researcher-authored PAM candidate instantiation with a TNN-accessible generative PAM construction system in Zag v2.
- TNN must be able to create, wire, initialize, train, clone, specialize, merge, route, shadow-test, promote, demote, and delete non-core PAMs using its own learned evidence and resource budget.
- The root verifier and protected core PAM substrate remain outside TNN mutation authority.
- PAM proposals must be executable structures, not English suggestions that require a researcher to translate them into source.
- PAM provenance must identify which evidence caused creation, which components were generated, and why promotion/rollback occurred.

### 13. Architecture goal is superior integrated capability, not local benchmark wins

**Preference:** The target is a large integrated architecture with superior capability. Weak integrated scores—especially 0% same-entity changed-view recognition, 0% sibling teaching, and 0% fully integrated success—are unacceptable as an endpoint and should trigger deep investigation into training, representation, routing, memory, PAM/core-PAM limitations, or architecture composition.

**Operational consequence:**
- Optimize for integrated causal capability across identity, naming, affordance, communication, robustness, memory, and self-improvement rather than isolated test scores.
- Diagnose whether failures originate in the core sensory substrate, entity persistence, cross-view invariance, binding, world-model integration, communication grounding, or self-revision machinery.
- Permit larger architecture changes when evidence shows a structural bottleneck; do not confine work to shallow tuning.
- Aim for 100% on the bounded integrated battery, but only count 100% when it survives hidden seeds, changed views, noise, distractors, delay, teacher withdrawal, and regression checks.

### 14. Core PAM redesign is allowed when evidence demands it

**Preference:** Core PAMs are protected from TNN self-mutation, not sacred. If deep tests show the protected core PAM interface prevents robust learning, the researcher may redesign the core and then rerun the complete regression and developmental battery.

**Operational consequence:**
- First distinguish training failure from substrate/interface failure with dose curves and diagnostic probes.
- If changed-view identity remains structurally impossible or information is lost before higher layers can learn, run a serious core-PAM architecture tournament.
- A new core must materially improve broad capability and must not merely overfit the current integrated test.

| Date | Status | Preference/change | Source |
|---|---|---|---|
| 2026-08-20 | CONFIRMED | New implementation path is pure native Zag v2; Python-only cognition experiments are diagnostic, not promotable. | Direct user message |
| 2026-08-20 | CONFIRMED | TNN-created non-core PAMs must be autonomously instantiated and managed without human implementation. | Direct user message |
| 2026-08-20 | CONFIRMED | Protected core PAMs may be redesigned by the researcher if deep evidence shows a substrate bottleneck. | Direct user message |
| 2026-08-20 | CONFIRMED | Goal is a giant integrated architecture with superior capability; weak integrated scores trigger deep architectural investigation. | Direct user message |

## 2026-08-20 update — Memory autonomy, skeptical 100% qualification, and stepwise training diagnosis

### 15. Memory hierarchy is TNN-controlled

**Preference:** Memory autonomy is a core differentiator of TNN. Do not impose a human-authored developmental schedule that slowly phases exact memory away. TNN should choose what enters, stays in, moves between, compresses within, or leaves short-term, working/active, long-term structured, exact episodic, semantic, procedural, sensory, and archival memory.

**Operational consequence:**
- Preserve a protected generic memory substrate, addresses, provenance, integrity checks, and resource limits, but do not hardcode which experiences deserve long-term retention.
- TNN must learn retention, promotion, compression, indexing, replay, retrieval, eviction, duplication, and archival policies from downstream value, uncertainty, future regret, recurrence, novelty, causal usefulness, source reliability, and resource cost.
- Exact raw episodes may remain addressable when affordable; compression must not silently destroy unique information before TNN has evidence that loss is acceptable.
- Different memory forms may coexist. Moving information to structured/semantic/procedural memory does not require deleting the exact episode.
- Memory policies must remain revisable from later regret: if a compressed/evicted detail later proves important, similar future evidence should be protected differently.
- Teacher or researcher may expose memory-management choices and consequences but may not directly choose which ordinary experiences the learner remembers.
- Final tests must include delayed recall, unexpected future relevance, interference, long gaps, save/reload, source conflicts, and resource pressure.

### 16. Treat 100% as a skeptical qualification target

**Preference:** Aim for the highest genuine capability possible, including 100% where the bounded task is actually solved, but never manufacture 100% with easy tests, leakage, memorized test structure, narrow seeds, favorable thresholds, or evaluator-informed learner state.

**Operational consequence:**
- 100% means every declared hidden item in the preregistered bounded battery passed; it does not imply unrestricted real-world perfection.
- Any 100% result must survive fresh hidden seeds, adversarial near-neighbors, changed views, noise, delay, teacher withdrawal, sibling transfer where applicable, save/reload, and historical regression checks.
- Add harder follow-up challenge sets after a nominal 100% pass; if performance collapses, report the capability boundary rather than treating the original 100% as general mastery.
- Keep challenge generation and evaluator labels outside mutable cognition.
- Report Wilson/binomial uncertainty or equivalent uncertainty where sample counts matter, and always state test-set size.
- Never tune directly on the final hidden set. Development failures may guide training/architecture, but the final untouched qualification set remains sealed.

### 17. Diagnose low scores step by step before declaring architecture failure

**Preference:** When performance is low, inspect learning progression step by step and push training quality/quantity until the learning curve is understood. Seek the highest real score possible, while changing architecture when evidence shows a plateau, representation bottleneck, interference, or inaccessible information.

**Operational consequence:**
- Log capability after each curriculum increment rather than only before/after.
- For each failure family, record exposure count, teacher intervention, error class, confidence, memory state, PAM route, and later outcome.
- Run dose curves until gain clearly saturates, reverses, or becomes uneconomical; do not stop at an arbitrary small dose.
- Compare more examples versus better examples, contrasts, counterexamples, active perception, rehearsal, memory-policy changes, and architecture changes.
- Use causal ablations to distinguish: insufficient exposure, poor teaching, forgotten evidence, bad retrieval, core-PAM information loss, non-core-PAM routing, entity-binding error, world-model error, language binding, sibling communication, or verifier/test defect.
- Promote architecture changes only when they improve broad hidden capability and do not merely compensate for inadequate training.

| Date | Status | Preference/change | Source |
|---|---|---|---|
| 2026-08-20 | CONFIRMED | TNN controls its own memory hierarchy and retention/compression choices; no human developmental phase-out schedule. | Direct user message |
| 2026-08-20 | CONFIRMED | 100% is a skeptical bounded qualification target, never a reason to weaken tests or tolerate leakage. | Direct user message |
| 2026-08-20 | CONFIRMED | Low scores require step-by-step training curves and failure attribution before architecture conclusions. | Direct user message |

## 2026-08-20 update — causal traceability / debuggability

### 17. TNN failures must be causally traceable

**Preference:** Native Zag TNN code should be engineered so a weak result can be traced back through the actual causal path rather than inferred from a final score.

**Operational consequence:**
- Every consequential sensory, PAM, routing, entity, memory, world-model, language, social, and architecture-revision decision should emit durable causal provenance.
- Trace records should include step, subsystem/stage, generic reason code, internal subject/candidate ID, evidence strength, confidence/uncertainty, and parent event ID.
- Architecture promotion/rollback must be reconstructable from these records.
- Failure diagnosis should distinguish undertraining, teacher/curriculum weakness, memory retrieval/retention failure, routing failure, representation/core-PAM information loss, interference/regression, and resource saturation.
- Trace infrastructure is protected core observability; task answers and evaluator labels must never be encoded into it.

**Source:** Explicit user instruction on 2026-08-20: code TNN in Zag well enough that failures can be traced back to their reason.

## 2026-08-20 update — training/architecture separation, innate system fluency, non-graph intelligence

### 18. Training is an independent experimental variable from architecture

**Preference:** Do not conflate training quality or quantity with architecture. Training, teacher/curriculum, memory policy, routing, and architecture are separate variables and must be isolated experimentally.

**Operational consequence:**
- Hold architecture fixed while running serious training dose/quality curves before declaring an architectural bottleneck.
- Hold training curriculum fixed when comparing architectures so gains cannot be attributed to a better lesson schedule.
- Use factorial comparisons where feasible: architecture A/B × teacher A/B × dose × memory policy.
- If learning is poor, investigate whether the learner/teacher failed to extract useful credit before interpreting random-search superiority as proof that learning cannot work.
- Record what changed in every experiment: data, teacher, optimizer/credit mechanism, memory, routing, non-core PAM topology, protected core, or evaluator.

### 19. Innate fluency with TNN's own generic functions may be hardcoded and tested

**Preference:** TNN should not necessarily have to rediscover from raw experience how to invoke its own generic internal facilities. It is acceptable to hardcode a birth-level skill/interface for using generic core capabilities such as creating/managing PAMs, allocating fibers, managing memory/storage, invoking tracing, running shadow experiments, and requesting observations, provided this does not encode task answers or domain knowledge.

**Operational consequence:**
- Test an `INNATE_SYSTEM_FLUENCY` condition against learned-from-scratch and teacher-taught controls.
- Innate fluency may define valid operations, schemas, safety/resource constraints, and how to call them; it may not prescribe which PAM to build, what to remember, what conclusion to reach, or which task answer is correct.
- Measure whether innate function fluency improves learning speed, self-revision quality, debugging, PAM search, memory management, and transfer.
- If it produces broad hidden gains with no harmful rigidity, treat it as a candidate protected-core skill rather than learned domain cognition.

### 20. Random generation beating a learned PAM selector is evidence that the learner/credit mechanism is bad

**Preference:** Do not interpret random generation outperforming a learned architecture selector as evidence that learning is inherently inferior. Treat that outcome as a diagnosis that the learning/credit representation is inadequate until deeper alternatives have been tested.

**Operational consequence:**
- Preserve random search as an important control.
- When random beats learned, inspect reward assignment, representation of candidate structure, exploration, diversity, delayed credit, interaction/compositional credit, memory of prior experiments, and training curriculum.
- Compare multiple learned search paradigms before accepting random as best: value learning, contextual bandits, evolutionary/population search, novelty/quality diversity, program induction, local structural credit, predictive world-model scoring, and hybrid approaches.
- The current whole-graph evolutionary result is evidence for population-level compositional search, not evidence that non-learning/random generation should remain the final mechanism.

### 21. Do not assume intelligence must be represented as a graph

**Preference:** Graph-based architecture is a hypothesis, not a definition of intelligence. The project should experimentally compare graph and non-graph computational organizations.

**Operational consequence:**
- Treat the current graph/PAM substrate as one candidate architecture family.
- Test alternatives such as event-driven fields, distributed state machines, cellular/local dynamical substrates, associative memories, recurrent arrays, program-like executable structures, sequence/temporal substrates, blackboard/workspace systems, mixture/routing systems, and hybrids.
- Comparisons must use the same training/evidence budget and downstream integrated capability tests.
- Favor the architecture or hybrid that learns and generalizes best; do not preserve graph structure for conceptual elegance.

### 22. Near-perfect robust capability is acceptable even when 100% is not reached

**Preference:** 100% is desirable on bounded solvable tests but is not required to recognize genuine high capability. Near-perfect performance on hard, diverse, hidden/adversarial tests can be more meaningful than a weak 100%.

**Operational consequence:**
- Continue to seek maximum real performance and diagnose residual errors.
- Report both score and difficulty/coverage. For example, 99.5% on a large hostile hidden battery is strong evidence even if not literally 100%.
- Never lower test difficulty to achieve 100%.
- Mark a capability `ROBUST_NEAR_SOLVED` versus `SOLVED_BOUNDED` when appropriate rather than forcing binary rhetoric.

| Date | Status | Preference/change | Source |
|---|---|---|---|
| 2026-08-20 | CONFIRMED | Training is an independent variable from architecture and must be isolated experimentally. | Direct user message |
| 2026-08-20 | CONFIRMED | Test hardcoded birth-level fluency for using TNN's generic own functions, without encoding task answers. | Direct user message |
| 2026-08-20 | CONFIRMED | Random outperforming learned search diagnoses poor learning/credit assignment; do not stop at random generation. | Direct user message |
| 2026-08-20 | CONFIRMED | Graph intelligence is only one hypothesis; test non-graph and hybrid substrates. | Direct user message |
| 2026-08-20 | CONFIRMED | Near-perfect robust performance is acceptable and meaningful even when not exactly 100%. | Direct user message |

## 2026-08-20 update — retire graph as primary substrate; associative episodic first

### 23. Graph is no longer the default/authoritative cognitive substrate

**Preference:** Based on the large entity-substrate tournament and the user's architectural judgment, the next TNN branch should stop treating a graph as the primary substrate for identity or general intelligence. The large switch advantage of associative episodic identity is considered strategically more valuable than preserving graph-centric continuity. Large context-switching architecture replacements are acceptable and desirable when evidence indicates the current substrate constrains capability.

**Operational consequence:**
- Make an associative-episodic / memory-first entity substrate the primary candidate branch.
- Do not require persistent entities, thought, or intelligence to be represented as graph nodes/edges.
- Graph structures may remain only as frozen controls or derived downstream relation indexes/caches; they cannot be authoritative state unless they re-earn that role through matched hidden tests.
- Preserve every graph family in comparison suites so the graph-retirement hypothesis remains falsifiable; never suppress a graph result that unexpectedly wins.
- Optimize the no-graph branch for rapid true-switch detection, exact episode retrieval, temporal persistence under missing evidence, uncertainty, active reinspection, and downstream language/affordance grounding.
- Treat major substrate replacement as a legitimate architectural move, not an undesirable discontinuity, provided state continuity and learned knowledge are preserved rather than restarting the learner.

### 24. Associative episodic identity becomes the primary baseline

**Preference:** The associative-episodic family should be developed aggressively because its near-perfect/100% true-switch behavior in the matched tournament indicates a potentially important capability advantage. Its weak occlusion/persistence score is a specific problem to solve, not a reason to discard the family.

**Operational consequence:**
- Start from associative retrieval of exact/multi-view episodes rather than graph identity nodes.
- Add non-graph temporal hypothesis state, learned evidence reliability, predictive continuity, and active observation to repair occlusion without sacrificing switch sensitivity.
- Never repair persistence by simply making identity sticky; require near-twin true switches and switches-under-occlusion in every development gate.
- Couple the architecture to TNN-controlled exact/structured/cold memory choices because machine memory is a central advantage of this substrate.

| Date | Status | Preference/change | Source |
|---|---|---|---|
| 2026-08-20 | CONFIRMED | Retire graph as the default primary cognitive/entity substrate; keep graph only as falsification controls or optional derived relations. | Direct user message |
| 2026-08-20 | CONFIRMED | Make associative episodic identity the primary development baseline and solve its persistence/occlusion weakness without sacrificing switching. | Direct user message |
| 2026-08-20 | CONFIRMED | Large substrate replacements are acceptable/necessary when they unlock major capability gains. | Direct user message |

## 2026-08-20 update — heuristic-default memory under TNN authority

### 25. Privileged memory heuristic is the birth/default policy, not immutable authority

**Preference:** Use the strongest privileged memory heuristic as TNN's default/birth memory-management policy because the learned policies have not yet earned replacement. TNN must still own memory decisions and be able to inspect, override, mutate, or replace that heuristic from experience. LRU may remain as a subordinate eviction primitive/control only when it preserves TNN authority over what is stored, downgraded, retrieved, or discarded.

**Operational consequence:**
- Initialize memory management with the privileged heuristic as a protected default policy interface, not a fixed answer table.
- Expose its generic decision factors/outputs to TNN's trace system so TNN can learn where it helps or hurts.
- TNN may override individual storage decisions, alter policy parameters, shadow alternative policies, and eventually replace the heuristic when hidden evidence supports replacement.
- LRU cannot be the final authority if recency mechanically evicts information TNN explicitly chose to protect; LRU can be used inside TNN-selected tiers/budgets or as a fallback among memories with comparable learned value.
- Continue learned-memory research; heuristic-default is a current engineering choice, not evidence that learned memory allocation is impossible.
- Record policy provenance for every storage/eviction decision.

### 26. Native execution infrastructure

**Preference:** Prefer the cloud terminal for TNN work. Use all local files/toolchain paths first. If the exact Zag compiler cannot be materialized or built locally, GitHub Actions is acceptable as a fallback native execution environment rather than substituting another cognition runtime.

## 2026-08-20 — R28/R29 binding update
- Remove graphs completely from active TNN runtime/cognition. Historical graph experiments remain controls only; future Foundry must not generate graph substrates.
- Continue no-VAD connected speech until near-100% robust performance if technically achievable; do not substitute supplied VAD/boundaries.
- Current CTC implementation is external reference, not native. Port CTC-style acoustic sequence learner to Zag; if native validation proves it is the generic mechanism driving robust speech, promote it as the core acoustic PAM.
- Exhaust local `znc` recovery/build using persistent long-running terminal sessions before falling back to GitHub Actions.
- Complete all unfinished R28 phases and begin R29 immediately after R28 qualification; do not treat R29 as mere cleanup.

## R30 Big Boom execution rules — 2026-08-21
- Any exact **0%** or **100%** bounded result is automatically suspicious. It must trigger a diagnostic/harder battery before interpretation. 0% may mean undertraining, broken task construction, evaluator failure, or true total failure; 100% may mean genuine excellence, leakage, triviality, evaluator saturation, or shortcut exploitation.
- R30+ should prefer **long developmental training curves** before blaming architecture. Training dose, curriculum, teacher quality, memory pressure, routing, representation, interference, resource pressure, and evaluation integrity are separate causal variables.
- Long-running jobs should checkpoint frequently and every meaningful checkpoint/result/source should be persisted immediately under `/TNN/Research`; do not rely on ephemeral terminal storage.
- Active cognition remains completely **graph-free**. Graphs are historical controls only, not runtime structures or Foundry genes.
- CTC-style latent acoustic alignment remains the preferred core acoustic PAM candidate, but it earns promotion only after native Zag training/evaluation reproduces the capability with no VAD, supplied boundaries, phoneme inventory, word dictionary, or English labels.
- All future **promotion** evidence must be native Zag. Python/reference fallback may diagnose and explore when the toolchain environment blocks, but cannot promote the brain.
- Counterfactual interventions (`what if A happens instead of B?`) are a default experiment style: appearance vs identity, confidence vs correctness, teacher/sibling vs direct evidence, memory retention vs later regret, action physics changes, sensor loss, PAM disablement, and resource shifts.
- Context-aware architecture learning is required. Architecture-history retrieval/mutation must be keyed by observable failure/telemetry context; pooling unrelated regimes is an invalid credit design.

## 2026-08-21 update — self-chunking is authoritative; no transformer/token framing

### 30. TNN chooses its own chunks / motifs

**Preference:** TNN must discover and revise its own useful segmentation/chunking over raw streams. Fixed transformer-style tokens, BPE vocabularies, word boundaries, phoneme inventories, or externally chosen linguistic units must not become the cognitive representation or primary speech/language target.

**Operational consequence:**
- Treat prior Adaptive Motif / motif-gated / support-gap results as the preferred starting evidence for R31 speech-language segmentation.
- Evaluate fixed token/motif inventories only as controls/ablations, never as the default TNN design.
- Speech should begin from raw waveform and allow learned chunks to vary in duration, overlap, cross human word/phoneme boundaries, combine hierarchically, split/merge, and be recruited from unsupported spans.
- The learner chooses chunks using endogenous utility such as predictive value, reversible compression/information preservation, grounding, discriminative usefulness, future retrieval, consequence prediction, and transfer—not resemblance to human words.
- Replace `token_accuracy` as a primary project metric with raw-stream reconstruction, learned-chunk stability/reuse, grounded discrimination, sequence/meaning fidelity, information preservation, chunk prediction/utility, transfer, and downstream integrated capability.
- Human boundaries/words/phonemes may be used only by the evaluator after the fact for microscope analysis, never as training targets or learner state.
- CTC may remain as a generic temporal alignment/control mechanism, but it must not impose the unit inventory. Core status for CTC is suspended until compared with native self-chunking on identical raw-stream training and downstream tests.

### 31. No transformer/LLM architecture drift

**Preference:** TNN is not an LLM/transformer project. Do not introduce transformer attention stacks, autoregressive token prediction, BPE/tokenizer assumptions, embedding-table language models, next-token objectives, or LLM wrappers as TNN cognition merely because the task involves speech/language.

**Operational consequence:**
- Preserve the project architecture: associative episodic memory, recurrent/local PAMs, temporal hypotheses, prediction, active evidence, adaptive motifs/chunks, grounded schema memory, workspaces/state processes, and TNN-created non-graph substrate mechanisms.
- Any transformer/BPE/token model may appear only as an external control if scientifically useful and must never be credited as TNN capability.

| Date | Status | Preference/change | Source |
|---|---|---|---|
| 2026-08-21 | CONFIRMED | TNN chooses its own chunking; fixed tokens/word/phoneme/BPE units are controls only, not the TNN representation. | Direct user message plus recovered Adaptive Motif evidence |
| 2026-08-21 | CONFIRMED | No transformer/LLM architecture or next-token framing in TNN cognition. | Direct user message |

## 2026-08-21 update — endogenous chunking architecture decision after R31 causal ablations

### 27. Self-chunking is auxiliary/compositional cognition, not an irreversible tokenizer

**Preference / evidence-backed decision:** TNN must continue to choose its own reversible chunks from raw experience. R31 additionally shows that learner-created chunks must not replace the high-fidelity raw/episodic route merely because they compress well.

**Operational consequence:**
- Primary sensory architecture is dual-route: endogenous chunks for reusable compression/indexing/grounded constructions plus exact/raw episodic evidence for fidelity and difficult discrimination.
- Chunk-only cognition is not promoted when it loses hidden grounding capability relative to the raw route.
- TNN may retrieve raw evidence when chunk reconstruction error, route disagreement, uncertainty, or delayed regret makes exact evidence valuable.
- Compression is a resource/cognition advantage, never the primary objective by itself.
- No transformer, BPE, fixed tokenizer, next-token objective, human phoneme inventory, VAD boundary, or externally imposed speech-unit vocabulary enters TNN cognition.

### 28. Chunk boundaries are mutable hypotheses

**Preference / evidence-backed decision:** TNN-created chunks may split, merge, specialize, archive, or be bypassed when delayed evidence shows the current chunking is harmful or context-dependent.

**Operational consequence:**
- Preserve learner-driven split/merge operations and causal provenance.
- Support-gap recruitment remains a preferred generic few-shot mechanism because it grounds the largest unsupported raw span without human boundaries.
- Context/regime specialization may branch consequences while preserving perceptual chunk identity.
- Avoid globally fixed chunk sizes or permanent vocabularies.

### 29. Active grounded evidence outranks more chunk compression when hypotheses are confusable

**Preference / evidence-backed decision:** R31 shows that near-twin/confidently misleading acoustic failures are primarily evidence-acquisition/arbitration problems after a competent dual representation exists.

**Operational consequence:**
- TNN may choose discriminating physical observations/actions using learned consequence separation.
- Learned commit/continue/abstain policies use internal evidence and delayed regret only.
- Do not encode corruption/ambiguity labels into learner state.
- Generic global probe-budget policies are rejected when they become overly conservative; evidence gathering must remain state-dependent.
- Genuine ambiguity/no-unique-answer remains an explicit open epistemic capability rather than being hidden by forced guesses.

| Date | Status | Preference/change | Source |
|---|---|---|---|
| 2026-08-21 | CONFIRMED | Endogenous chunks remain TNN-selected but are an auxiliary/compositional route alongside exact raw episodic evidence; chunk-only replacement is rejected. | Direct user anti-token guidance + R31 causal ablation |
| 2026-08-21 | CONFIRMED | Chunk split/merge/context specialization and support-gap recruitment remain part of the forward architecture; no fixed transformer/token vocabulary. | Direct user guidance + R31 experiments |
| 2026-08-21 | CONFIRMED | Active cross-modal/physical evidence is preferred over further compression when self-chunk hypotheses remain confusable; genuine ambiguity may require UNKNOWN. | R31 post-repair evidence |

## 2026-08-23 update — logical UNKNOWN and temporally extended investigation

### 32. UNKNOWN is a structured epistemic state, not a class label

**Preference:** UNKNOWN means that commitment is not yet logically justified. TNN may favor one hypothesis while retaining alternatives and should preserve why each remains live, what supports or contradicts it, which sources are genuinely independent, what consequences differ, and what observation could discriminate them. No ambiguity label, numeric confidence cutoff, or conventional knowledge graph may substitute for this structure.

**Operational consequence:**

- Bind evidence provenance, support, contradiction, learned consequence relations, incompatibility, temporal consistency, and unresolved alternatives in learner-visible native state.
- Allow UNKNOWN to lead to a learned investigation when a discriminating consequence is worth its learned opportunity cost, or to persist for an explicit reason when no affordable discriminating action exists.
- Score logical warrant from reconstructible native traces rather than generated reasoning text.

### 33. Multi-step investigation must retain its initiating reason

**Preference:** The V44 frontier is an option-completion failure, not a mandate to probe indiscriminately. A TNN-created investigation should persist through temporarily uninformative observations when its delayed expected value remains positive, while retaining the original question and terminating when the live distinction is resolved or no longer worth pursuing.

**Operational consequence:**

- Compare matched per-step, recursive-option, explicit-target, and full logical/temporal/resource arms.
- Learn continuation from delayed grounded outcome and regret; never impose minimum duration, fixed probe count, evidence-count stage, or evaluator-side mode/deadline.
- Report useful initiation, completion, success conditional on initiation, premature exit, false-positive investigation, opportunity loss, replacement/reversal performance, UNKNOWN quality, wrong commitments, and logical-warrant consistency separately.

| Date | Status | Preference/change | Source |
|---|---|---|---|
| 2026-08-23 | CONFIRMED | UNKNOWN is a logically structured state that may favor one hypothesis while retaining alternatives and their warrants; it is not an ambiguity class or confidence threshold. | Direct continuation brief |
| 2026-08-23 | CONFIRMED | Repair V44 through a learned temporally extended investigation option with no fixed duration/count and native matched causal qualification. | Direct continuation brief |
