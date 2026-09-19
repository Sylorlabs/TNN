# R32 E51 — Proposed Longitudinal Research Track

Date: 2026-09-04 Pacific.
Status: research design only; no experiments executed, preregistered, or dispatched by this document.
Scope: this document only. It assigns no experiment identifiers, stages, or world ranges and leaves the parallel short-context diagnostic untouched.

## 1. Authority and evidence boundaries

- R27 remains canonical; Baseline V1 and the E51AH source, thresholds, evidence, and negative closure remain immutable.
- E51AH is an integrity-valid development negative: local replay lost 121 of 12,622 union successes while rescuing 159; net +38 did not pass its zero-loss gate. Validation and confirmation remain sealed.
- This proposal neither resumes nor retunes AH and does not authorize access to its sealed populations. New work requires separate preregistration and fresh, nonoverlapping populations.
- Frozen mature-controller hashes are not retention evidence when a learned residual can override those controllers. Evaluate the actual deployed policy, including arbitration and abstention.
- The charter, AH result, arc report, and generality scorecard listed below govern interpretation. Historical experiment rows are not checkpoints of one continuing learner.

## 2. Questions and distinct claim levels

Ask whether further experience produces acquisition, interference, durable preservation, recovery, or transfer, and which intervention changes those trajectories.
Family S uses one task and the same generator, with A–D denoting explicitly specified curricula or environment regimes; its conclusions are repeated learning and within-family retention only.
Family T requires preregistered, meaningfully distinct tasks with different rules, objectives, or input–outcome relationships and comparable interfaces; different seeds or names do not create new tasks.
Do not merge the two families into a generality score. Even a successful four-task cycle is bounded multitask evidence, not lifelong competence or cross-domain intelligence.
More iterations count as longitudinal evidence only when the same learning lineage continues and earlier competencies are retested after intervening experience.
Record active compute, cumulative exposure, switch count, and elapsed time separately; elapsed time alone does not establish retention under learning.

## 3. Two research lanes

**Diagnostic lane:** preregister the entire exploratory curve, arm set, seeds, exposure schedule, metrics, anchors, and stopping rules before any curve is observed.
A weak model may complete that bounded schedule despite early negative checkpoints, failure to acquire a task, or incomplete recovery. Report those observations without selecting a favorable prefix.
Diagnostic probes are research-visible development evidence, never promotion holdouts. No in-run dose, objective, sampler, threshold, or checkpoint-selection changes may depend on them.
**Qualification lane:** a separately frozen candidate and full schedule must meet preregistered capability-specific development gates before fresh sealed validation and confirmation can open.
Use independent seeds/worlds and predetermined terminal and retention assessments; commit the assessment list before exposure and prohibit adaptive feedback into training.
Qualification needs all required preservation, integrity, replication, and generalization gates. Partial recovery, positive net change, or a favorable final checkpoint cannot erase earlier required-gate failures.
The diagnostic lane cannot retrospectively relax AH gates, unlock AH holdouts, update Baseline V1, or confer promotion.

## 4. Exposure ladder and checkpoints — proposed defaults

Let one block U equal 1,024 newly experienced training episodes, distinct from replay presentations, optimizer updates, and evaluation episodes.
Train A once, then repeat [B, C, D, A]; adjacent cycles share the returning A rather than adding an extra A block: A→B→C→D→A→B→C→D→A…
Checkpoint at zero exposure and every 256 new episodes, including every block boundary. Each panel evaluates 256 frozen probes for each of A–D, giving 1,024 probe episodes.
The same lineage supplies all selected tier prefixes; choose its highest tier before execution. The following are ceilings/design defaults, not measured runtime forecasts.

| Tier | Returns to A | New training episodes | Checkpoint panels | Probe episodes | Native wall-time cap per lineage |
| --- | ---: | ---: | ---: | ---: | --- |
| Acquisition | 0 | 1,024 | 5 | 5,120 | 30 minutes |
| Short cycle | 1 | 5,120 | 21 | 21,504 | 1 hour |
| Repeated cycle | 4 | 17,408 | 69 | 70,656 | 3 hours |
| Extended cycle | 16 | 66,560 | 261 | 267,264 | 8 hours |

The first panel is pretraining; endpoint panels also serve as pre-switch evaluations, without duplicate exposure. Every return block supplies four recovery checkpoints.
Use three predetermined paired seeds for a comparative diagnostic; a one-seed feasibility pilot is explicitly non-replicated and cannot choose a favorable seed for the main comparison.
Select the feasible tier from an independent bounded pilot before freezing a comparative run; do not extend or shorten that run after inspecting its learning curve.
Optional 24-hour/seven-day serialized-state holds test persistence across elapsed time or restart, separately from interference; do not count idle time as learning longevity.

## 5. Continuous state and exposure accounting

Within an arm, carry forward all declared trainable parameters, optimizer state, recurrent state, and writable memory across blocks; pin any intentional episode-boundary resets.
Never reinitialize between A–D or splice the best checkpoints together. A reset-from-parent comparator is a separate lineage and cannot be labeled continual learning.
Save parent/child checkpoint hashes, parameter deltas, optimizer counters, memory hashes, and the exact consumed training-stream position at every checkpoint.
An unchanged parameter hash with extra iterations is not evidence of continued parameter learning; report attempted updates, actual changes, and any state-only adaptation separately.
Keep separate counters for new environment episodes, unique examples, current-task repeats, past-task replay, record-update presentations, native operations, and evaluator-only probes.
Pin intervention onset, withdrawal, and persistence independently of task switches. Report both new-task exposure and intervention exposure at each checkpoint.
Do not silently reset accumulated optimizer or memory state when changing an environment; any reset must be an explicit preregistered intervention.

## 6. Comparators and causal ablations

| Comparator | What is held fixed / question answered |
| --- | --- |
| Frozen static policy | Zero further learning from the identical starting parent; evaluate on every panel to detect evaluator or persistence drift. |
| Continued-dose A | Train only A for the switching arm's full exposure horizon and matched update budget; distinguish interference from ordinary continued learning or overtraining. |
| Stationary mixed-task stream | Share the initial A block, then shuffle each 4U packet containing equal A–D counts; match examples/work and compare at complete-cycle endpoints. |
| Task-only from the matched parent | Train j without prior other-task experience; supplies the untrained and target-dose-matched transfer baselines defined below. |
| No replay | Retain parameters but never present prior-task examples; identifies interference without rehearsal. |
| Replay | Use only legitimately observed training experience, with fixed buffer, insertion/sampling policy, replay ratio, and replay age accounting. |
| Memory disabled | Disable declared nonparametric/recurrent memory while retaining trainable parameter continuity; distinguish persistent weights from memory-assisted performance. |
| Context destroyed | Destroy only permitted history by a preregistered reset or within-split shuffle; match length, capacity, marginal inputs, and work without introducing task IDs. |

The core switching comparison needs frozen-static and continued-dose controls; transfer claims additionally need task-only baselines, and ordering claims need matched mixture endpoints.
A replay attribution needs a no-replay control: replace replay updates with repeats of the same available current-task examples, keeping new interactions and total record presentations fixed.
Record-count matching alone is not compute matching: include retrieval, history processing, and native update operations. Report changed per-task allocation and separate data-matched results when work differs.
For memory claims, add capacity-matched current-state and context-destroyed controls; distinguish training-time disabling from evaluation-only lesions of the same frozen checkpoint.
Match model capacity, targets, observation/action interfaces, seeds, update counts, and native operation budgets wherever the contrast permits; padding time with idle work is not compute matching.
Not every ablation or mechanism belongs in one run. Select the smallest preregistered comparison that identifies the chosen hypothesis; omitted controls limit the corresponding claims.

## 7. Frozen probe protocol and retention matrix

Freeze probe manifests, worlds, seeds, evaluator version, and stratum membership before training; enforce disjointness from all training and replay stores.
At each checkpoint evaluate a clone with parameters/optimizer frozen and training/replay writes disabled. Permit only preregistered inference-state transitions, isolated per probe and discarded afterward.
Clone evaluation must not advance the training RNG or alter the continuing lineage; give each probe a fixed evaluation RNG stream so paired pointwise losses remain interpretable.
Primary probes start from the same declared episode-local context policy; any warm persistent-memory evaluation is a separately labeled panel with its state source fixed beforehand.
Keep truth, UNKNOWN labels, ambiguity, task/mode/resource/world identities, and split membership evaluator-only. A–D are scheduler labels, not learner input tokens.
Ordinary observations, actions, and grounded outcomes may train the learner; probe outcomes and evaluator-only candidate unions may not become training targets or replay records.
Let R[k,j] be the actual deployed-policy success rate on task/regime j's identical frozen probe set at checkpoint k. Rows are checkpoints; columns are A, B, C, D, plus fixed prior-competency probes where required.
Store each pointwise success vector as well as the rate, counts, no-warrant/ambiguity strata, native work, task exposures, and phase. Extra prior-competency panels require explicit additional budgets.
Report deployable online decisions and resource-feasible reachability separately; never substitute evaluator-selected feasible actions for actual policy behavior or count an oracle as successful by construction.
Repeated probes measure trajectories on that fixed suite, not independent replications. They are consumed development evidence; fresh qualification suites remain separately sealed.
Keep fixed first-block and per-cycle pre-departure anchors; never choose the best earlier checkpoint after seeing outcomes.
Separately preregister a task-acquisition criterion and set acquisition anchor a_j to its first qualifying scheduled checkpoint, including a later block if initial acquisition fails.
Until that event occurs, show curves and pointwise changes but mark acquired-competency retention/recovery unestablished. A later acquisition does not revise the original first-block anchor.

## 8. Losses, gains, and recovery

For task j and fixed anchor a, let s[a,i] and s[k,i] denote success on the same probe i. Report first-block, criterion-based acquisition, and per-cycle anchors separately.
Pointwise losses L[k,j] = Σ_i s[a,i](1−s[k,i]); rescues G[k,j] = Σ_i (1−s[a,i])s[k,i]; net change = G[k,j]−L[k,j].
Retained-success fraction = Σ_i s[a,i]s[k,i] / Σ_i s[a,i]; an empty anchor-success set is undefined, not 100% retention.
Include cumulative ever-lost anchor successes, worst checkpoint loss, final loss, and loss by task/stratum. A restored final average cannot conceal temporary or concentrated forgetting.
Measure retention immediately before reentry into A; measure recovery only after new A experience begins. Prespecify the same distinction for any other revisited task.
If no pre-reentry loss occurred, record retained/recovery not needed and zero reacquisition dose; do not invent a recovery event.
Default exact-recovery time is the first scheduled return checkpoint with zero losses against the fixed pre-departure success set, sustained at the next scheduled checkpoint within that return block.
Report the detection interval, confirming checkpoint, new-task episodes, updates, and native time; a final-block-only recovery cannot be called sustained without its scheduled confirmation.
No recovery within the preregistered horizon is right-censored, not assigned an invented recovery time. A task never meeting its acquisition criterion has no established acquired-competency recovery time.
Prespecified relaxed diagnostic tolerances may be secondary curves only; they cannot replace exact-preservation qualification gates or repair AH's failed gate retrospectively.

## 9. Forward and backward transfer

Define U_j(d) using a task-only clone with the same inherited frozen components, new trainable initialization, capacity, interface, seed pairing, and j-specific training/replay presentations at dose d.
U_j(0) is matched target-task-untrained performance: disclose inherited competence explicitly; it does not mean a fully blank model when the parent already contains trained controllers.
For task j's first introduction, zero-shot forward transfer FWT0_j = R[before j,j]−U_j(0); exclude j from all preceding replay and other training when making this claim.
At matched first-introduction target dose d, learning-curve forward transfer FWT_j(d) = R[prior tasks then j at d,j]−U_j(d); report the curve and acquisition-threshold crossing, including failures.
This matches target exposure, not total historical compute. Add a task-only control spending the same total useful native-work budget before claiming computational efficiency.
For an already learned j with acquisition anchor a_j, raw backward transfer BWT_j(k) = R[k,j]−R[a_j,j]; evaluate before relearning j to distinguish transfer from recovery.
Also report baseline-adjusted BWT_j(k) = [R[k,j]−U_j(d_j(k))]−[R[a_j,j]−U_j(d_j(a_j))], matching any additional j rehearsal in the task-only trajectory.
With no extra j exposure the matched baseline term cancels; with replay, positive raw BWT alone cannot establish beneficial transfer from other tasks rather than direct practice.
Report each task and paired-seed differences before any mean; mark transfer from an unacquired task, contaminated target, or unmatched baseline as unestablished.
Transfer within Family S remains within-generator adaptation. Structural or cross-task transfer requires the independently defined Family T tasks and fresh-world qualification.

## 10. Interventions and changing environments

Preregister intervention-on, intervention-off, fixed withdrawal/reintroduction, or acquisition-only exposure schedules; choose contrasts for one causal question rather than automatically crossing every factor.
Hold intervention assignment and switch timing independent of probe performance. Any adaptive schedule needs a separately frozen rule using learner-visible information only.
Candidate environmental changes include input noise, delayed consequences, resource limits, observation transforms, and changed transition/outcome rules; distinguish nuisance shifts from genuinely new tasks.
Begin with fixed-length blocks and observable experience only; later candidates may test gradual drift or unannounced switches without privileged boundary labels.
Track distribution severity, task difficulty, buffer content, replay age, and cumulative intervention dose so a changed exposure mix is not mistaken for a better mechanism.
Replay can sustain A through direct practice; no-replay retention and controlled withdrawal identify a different claim. Report both only when those conditions were actually tested.

## 11. Native resource envelope and integrity stops

Promotable learning and evaluation execute in native Zag v2; analysis may summarize ledgers but cannot replace native cognition. Freeze compiler/source/binary identities and require deterministic double builds.
Proposed limits: at most two CPU workers per lineage, 2 GiB peak resident memory, 8 GiB checkpoint/evidence storage, and 1,024 training-record update presentations per new episode, replay included.
The tier table caps training and primary probe exposure plus total native training/evaluation wall time; pin batch size, sweeps, operation accounting, hardware, and any extra panels before execution.
Set a separate 30-minute build/preflight cap and a 512 CPU-core-hour campaign ceiling covering every arm, seed, baseline, and pilot; preregister an itemized schedule that fits all limits.
These are proposed ceilings, not execution authorization or promises of feasibility. Reduce the selected tier before preregistration if necessary; do not omit causal controls to manufacture a longer run.
Stop immediately for leakage, split overlap, identity/build mismatch, nonfinite state, checkpoint corruption, undeclared reset, probe mutation of training state, or missing integrity evidence.
An integrity-failed instance is invalid, not a valid treatment negative; preserve its trace and exclude downstream checkpoints from scientific claims.
Otherwise continue the complete preregistered exploratory horizon despite weak scores. Completing all prescribed exposure and probe panels is completion, regardless of scientific outcome.
Never exceed the exposure, update, wall-time, memory, storage, or campaign caps; a cap preventing completion of the prescribed schedule yields administrative censoring, not a completed negative or positive.
No unbounded retries or automatic budget extensions. A resumable interruption must restore the exact full checkpoint/stream state under a preregistered policy and the original cumulative caps.

## 12. Branching candidates and decision records

Candidate branches remain quantity/dose, curriculum, contrastive or trajectory-preservation objectives, sampling coverage, optimization, short context, memory/replay, representation, uncertainty, and routing geometry.
Later branches may consider prediction, composition, learner-created mechanisms, or structural plasticity only with evidence justifying escalation; this inventory does not claim any branch was tested.
For each chosen branch, record at least two competing explanations, the cheapest distinguishing contrast, expected directional outcomes, and what positive or negative results would leave unresolved.
Persist the full retention matrix, pointwise losses/rescues, baseline trajectories, exposure ledger, checkpoint lineage, compute costs, and all negative/censored/invalid outcomes in any future result package.
Label every future conclusion by task family, tested horizon, intervention, control coverage, native verification, and lane; document recovery without relabeling it uninterrupted retention or promotion.

## Source documents read

- [Program charter](R32_E51_PROGRAM_CHARTER.md).
- [E51AH authoritative result](R32_E51AH_RESULT.md).
- [E51AC–E51AH arc report](R32_E51AC_AH_ARC_REPORT.md).
- [Generality scorecard](R32_E51_GENERALITY_SCORECARD.md), the repository's named scorecard file.
