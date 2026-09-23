# DO NOT REPEAT — the complete negative record

*Source of truth for experiment-design agents. Every entry: what was tried,
why it failed, what to do instead. All pointers are paths in sylorlabs/TNN
(branch `tnn-native-lab`, post-reorg layout). Treated as law: do not rerun a
listed failure without a preregistered mechanism that addresses the named
cause.*

---

## 1. E45–E50: six consecutive valid native negatives on safe terminal control

**What was tried.** Six native experiments on the terminal controller's
no-unique safety gate (every-cell must abstain, never wrongly commit):
- **E45** — baseline native terminal control.
- **E46** — order schedules over commit/abstain decisions.
- **E47** — two grounded co-presence features (epoch two-hypothesis
  co-viability; option support/contradiction co-mass) added to the terminal
  controller.
- **E48** — batch fitting.
- **E49** — quadratic conjunctions of the E47 statistics.
- **E50** — provenance/contention conjunctions.

**Why it failed.** In E45 the controller made wrong commitments on *every*
no-unique episode; E46–E50 each failed the every-cell no-unique gate in their
own way (no schedule passes all gates; `NO_TESTED_REPRESENTATION_RESCUE`;
more UNKNOWN with less known success). The mechanism is documented in
`docs/hypotheses/H-05-inquiry-as-action.md`: **the UNKNOWN target was grounded
zero on every training record, so its head stayed exactly zero, and abstention
required every commit value to go negative — which the tested linear value
geometries never achieved.** The features in E47 varied substantially on
training data yet every joint-model no-unique decision still committed wrongly
under the blocked online linear head. The repo's bounded reading: these
features are insufficient *under the tested linear value geometry and training
dynamics*, not refuted in general.

**Do instead.** The proposed post-E50 mechanism is a grounded **nonzero**
UNKNOWN value geometry (delayed investigation/termination action value).
Any rerun must change the target geometry, not just add features to the same
zero-UNKNOWN setup. E45–E50 sources: `docs/generations/R32/runs/` (E45–E50
dirs), `docs/hypotheses/H-04-competing-hypotheses.md`,
`docs/hypotheses/H-05-inquiry-as-action.md`.

---

## 2. E51AH / E51AI / E51AJ: preservation replay fails retention gates

**What was tried.** Replay-based preservation of an accepted capability
lineage (E51 series), culminating in E51AJ: 1.1M probe rows, 3 replicas,
independently verified (21 analysis + 11 verifier tests).

**Why it failed.**
- **E51AH** failed the frozen zero-loss development gate: global replay
  **lost 236 union successes, rescued 6**; local lost 121, rescued 159;
  stages 109/110 stayed sealed.
- **E51AI** was mixed: anchor losses 22→9, but real history gained known
  cases while *losing* no-unique preservation.
- **E51AJ** lowered ever-lost and worst-loss in every replica yet **failed
  the all-three-replica endpoint retention rule** (final anchor losses
  1/14, 9/11, 17/6) and **failed the no-final-behavioral-tradeoff rule**
  (known reachability decreased in every replica). The A-only arm showed
  continued fitting lost shared-anchor successes in all replicas *including
  its own cohort* — damage without any cohort alternation.

**The law.** `docs/hypotheses/H-08-continuing-brain.md`: **cumulative
disruption ≠ endpoint recovery; aggregate gains never cancel pointwise or
cohort-specific damage.** Never report aggregate-only retention numbers;
always report endpoint retention per replica and per cohort.

**Do instead.** The preregistered-but-unlaunched E51AJ follow-up
discriminator: a training-only preservation constraint vs. an action-ranking
objective, to separate objective-mismatch from support/optimization causes of
retention failure. Sources: `docs/generations/R32/runs/R32_E51AH_NATIVE`,
`R32_E51AI_NATIVE`, `R32_E51AJ_NATIVE`, `R32_E51AJ_ANALYSIS`,
`docs/hypotheses/H-08-continuing-brain.md`.

---

## 3. The abstention/resolution tradeoff (unsolved, recurring)

**What was tried.** R31 evidence policies, E46 order schedules, E48 batch
fitting, E51AJ replay — every mechanism that increases safe abstention
degrades resolution, and vice versa.

**Why it persists.** Nothing tested breaks it. Related rejections:
- Global probe-budget and generic RF stopping policies: **rejected** as
  over-conservative (~0.68 hard correct vs 0.9698 for the learned sequential
  policy) — `docs/hypotheses/H-05-inquiry-as-action.md`.
- R31's best shadow policy abstained on only ~57% of deliberately
  no-unique-answer cases — genuine ambiguity over time
  (temporarily-difficult-but-resolvable vs. genuinely-no-unique-referent)
  remains the highest-value unsolved capability.

**Do instead.** Do not propose another abstention knob without a mechanism
aimed at the tradeoff itself (the nonzero-UNKNOWN geometry in §1 is the
current candidate). Sources: `docs/hypotheses/H-05-inquiry-as-action.md`,
`docs/hypotheses/MATRIX.md`.

---

## 4. Evaluator leakage — the default suspect (E45's broken evaluator)

**What was tried (and invalidated).** E45's first two native runs collapsed to
zero beneficial episodes — *because the evaluator was broken, not the
learner*:
- a single scalar `grounded_outcome` let "replacement/reversal" change
  evidence without changing hidden world state;
- historical state equaled final truth, so KEEP was already correct;
- targets used clairvoyant ex-post best-of labels;
- warrant read evaluator correctness (circular).

**Why it matters.** After repair, the *same* battery produced valid negatives
instead of invalid collapses. The program can now distinguish "the learner
failed" from "the test was broken" — and treats leakage as the default
suspect behind any good number.

**Do instead (mandatory discipline).** Truth_by_time trajectories; frozen
terminal controllers; nonzero oracle-positive prevalence gates;
evaluator-blind helpers that take **no** mode/truth/seed/target arguments;
fresh-seed discipline; sealed partitions; matched controls (E51AJ: 6,480
unique training + 6,480 unique probe trajectories); **consumed probes are
never reused as fresh validation** (R33 N13A/N14/N16 gates are consumed —
do-not-rerun). Source: `docs/hypotheses/H-07-evaluator-separation.md`.

---

## 5. R33-B000: five confirmed native boundary defects

**What was found.** The boundary audit confirmed 5/5 defects in native
engineering:
1. substrate transform loses channel order;
2. acoustic window misses unsampled detail;
3. **trace helper silently drops an event at saturation**
   (8,193 attempts → 8,192 records) — a defect in the very machinery meant to
   guarantee traceability;
4. output limits silently omit tails;
5. (fifth defect documented in the B000 run dir).

**Do instead.** Corrective implementation is the active B001 workstream
(`docs/generations/R33/runs/R33_B001_C02_RUN_PRIMARY_V1`,
`R33_B001_C03_RUN_PRIMARY_V1`). Never build on the prototype trace helper
without the B001 gate. Sources: `docs/hypotheses/H-10-traceability.md`,
`docs/hypotheses/MATRIX.md`.

---

## 6. R31 shadow results are REFERENCE_ONLY — never promote on them

**What was tried.** The R31 shadow program produced the repo's strongest
numbers: dual-route ablation (raw+chunk 0.9209 hard / 0.85 compression),
support-gap recruitment (~0.89–0.92), context specialization (0.9423),
sequential evidence policy (0.9698 hard-correct, 1.396 probes).

**The law.** All of it is **REFERENCE_ONLY** — shadow runtime, never natively
quantified. The repo marks reference-only scores as non-promoting. Native
confirmation is required before any of these becomes a claim about TNN.

**Related rejections (do not rebuild these):**
- **Chunk-only sensory representation: rejected.** Compresses strongly
  (0.8525) but loses hidden grounding (0.7533 vs 0.9213 raw). Dual route
  retained instead — `docs/hypotheses/H-02-dual-routes.md`.
- **Predictive-surprise / giant-span chunk objectives: rejected** as primary
  criteria (impressive compression, mediocre grounding).
- **Always-reinspect: rejected.** Context-disagreement-triggered reinspection
  (0.9017) beat always-reinspect (0.8439) — "always asking again is not the
  answer."
- **Clean 1.0 scores are treated as suspicious** (support-gap recruitment).

Sources: `docs/hypotheses/H-02-dual-routes.md`,
`docs/hypotheses/H-03-endogenous-chunking.md`,
`docs/hypotheses/H-05-inquiry-as-action.md`.

---

## 7. BLOCKED / NOT_QUALIFIED — do not claim these

- **R27 behavioral continuity: BLOCKED.** The canonical brain is at step
  60,423 with a 33/33 verifier rerun (engineering continuity fact), but the
  original source chain is unrecovered — do not claim behavioral continuity
  from the accepted state alone. Source: `docs/hypotheses/H-08`.
- **Audio and vision: NOT_QUALIFIED.** Only synthetic-temporal evidence is
  partial; R31 speech tests were synthetic eSpeak research only. Do not claim
  natural speech/video capability. Source: `docs/hypotheses/H-01`.
- **Memory autonomy, active-inquiry scenario battery, training-technique
  tournament with withdrawal: PLAN_NOT_EXECUTED / NOT_QUALIFIED.**
  Source: `docs/hypotheses/H-06-staged-autonomy.md`.
- **Teacher-withdrawal measurement: specified, not run.** Do not claim
  learner autonomy without the withdrawal test (H-06 anti-facade tests).
- **Consequence-model learning: untested natively** (H-04).
- **znc full compiler self-host/fixpoint: unqualified;** generated compilers
  have crashed on the full-source workload. Keep native workloads small and
  harnessed. Source: toolchain provenance docs in `src/tools/toolchain/`.

---

## 8. Banned practices (process law)

1. **Newborn restarts to hide interference.** One developmental lineage
   continues; accepted floors are regression constraints
   (`docs/hypotheses/H-08`).
2. **Hardcoding answers into the learner.** Hardcoding allowed only for core
   infrastructure/safety or with strong controlled evidence, and every
   instance is ledgered. Hardcoded teachers are acceptable *only* as
   attributed teaching aids whose knowledge is never copied into the learner
   as answer tables — and teacher dependence must be measured after
   withdrawal. User's explicit preference, recorded 2026-08-20
   (`docs/hypotheses/H-09-training-first.md`).
3. **Crediting teacher/evaluator knowledge to the learner**
   (`docs/hypotheses/H-07`).
4. **Confidence-threshold abstention.** Abstention must be earned from
   grounded value, not a probability bucket
   (`docs/hypotheses/H-05-inquiry-as-action.md`).
5. **Architecture churn before training-first diagnosis.** When a result is
   weak, diagnose training first (data, lesson quality, contrasts,
   curriculum, rehearsal, teacher); change architecture only for a measured
   plateau. E51's escalation ladder tests ordinary explanations before
   representation/memory/topology expansion
   (`docs/hypotheses/H-09-training-first.md`).
6. **Reusing consumed probes as fresh validation** (§4).
7. **Aggregate-only reporting of retention or capability** (§2).

## HT1 (2026-09-19): the 2x2 score table is a toy — permanent negative

Head-to-head under a randomized switching curriculum (10 true flips, 15% noise,
identical episodes): the unmodified R34 v3 table learner suffered **357 switches
(35x switch-storm), two 0/16 collapsed blocks, and one regime destroyed at
endpoint (0/16)**. The replacement mechanism (contexts as deliberately-managed
memory partitions, switching as a verified deliberate op with intrinsic
corroboration, no score table anywhere) committed 11 switches, zero collapsed
blocks, 16/16 on both regimes. Mechanism: any substrate whose decision step is
a single reflexive function evaluation with no corroboration requirement and no
refusal path cannot survive unpredictable change. N×N table scale-ups are not
progress toward intelligence (LH-6's table scaling stays banned) — but scaling
itself is allowed: real mechanisms must be designed to survive 10x/100x scale.
What is banned is scaling the toy, not scaling. And no randomness lives in the
AI's decision paths — no random exploration, no random tie-breaks, no stochastic
policies; educated guesses, logic, hypotheses, verification. Deterministic given
state. Evidence:
`docs/lab/wave2/posttable/`.
