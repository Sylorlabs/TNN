# Learning-rule survey — every learning rule tried in the repo

Agent F (rules lab), 2026-09-19. Mechanics extracted from source, not summaries.
"Learning" in TNN means: what changes in the learner as a function of experience,
and by what exact update.

---

## 1. R27 canonical brain — structural self-revision (historical, Python)

Source: `parent-r27-accepted-state.pkl` via `docs/lab/wave1/brain/STATE_SCHEMA.md`.

- **Update:** 58 `self_revision_history` entries. Each: `diagnosis` (what's wrong)
  → `proposal` (structural change) → measured `base_accuracy` vs
  `candidate_accuracy` + `compute_multiplier` → `PROMOTE` or rollback.
- **Learning atom:** `Trace` — a verified *symbolic op-sequence*
  (e.g. `(('FILTER_GT','PARAM'),('MAP_MUL',2))`) over a 512-dim cue vector,
  with support, sources, age, `provenance='SELF_VERIFIED'`. Operations, not gradients.
- **Memory:** `ProtectedSkillMemory` with `fast`/`slow` two-speed tables;
  entity/event graphs; motif programs. All structural, all inspectable.
- **Tensors:** 76 torch Parameters confined to perceptual components; zero
  optimizer state, zero gradient payloads in a 121,094-node sweep.
- **Status:** canonical accepted state (step 60,423, 0 restarts). Source chain
  unrecovered; not executable. This is the *target semantics* — no native rule
  below implements it yet.

## 2. R34 v1 online learner — delta rule (native Zag, executable)

Source: `docs/generations/R34/runs/R34_NATIVE_CONTINUAL_LEARNER_V1/r34_learner.zag`.

- **State:** 2×2 q-table (task×action), LCG rng, update counter, pending slot.
- **Choose:** argmax; ties → `rng % 2`.
- **Update (Rescorla–Wagner / delta rule):** `q ← q + (reward − q) * 250/1000`.
  Reward **hardcoded** ±1000 (`r34_reward`: +1000 if action==task else −1000).
- **Credit:** single pending slot; reward computed inline (no world delay).
- **Exploration:** none beyond tie-breaks. No contexts.

## 3. R34 v2/v3 continual learner — additive score + context recruitment (native Zag, executable)

Sources: `.../R34_NATIVE_CONTINUAL_LEARNER_V2/r34_continuing_learner_v2.zag`,
`.../R34_NATIVE_CONTINUAL_LEARNER_V3/r34_learner_core.zag` (+ Linux port in
`docs/lab/wave1/toolchain/`).

- **State:** 2×2 score table (context×object), visit counts, LCG rng
  (`rng ← (rng*997+7919) % 1000003`), `active` context, `contexts ∈ {1,3}`,
  pending credit slot (action/context/object/explore flag),
  decisions/switches/outcomes counters.
- **Choose:** argmax score for active context; **ε-greedy 1/5**: if
  `rng % 5 == 0`, flip object (marked explore).
- **Delayed credit:** action → pending slot → world returns delayed outcome
  (3-tick delay) → `score[c][o] += reward*100`, clamped to ±30000; `updates++`.
- **Context recruitment (the continual-learning mechanism):** on negative
  reward, non-explore, old score > 0: if `contexts==1`, recruit (`contexts=3`,
  `active=1`, `switches++`); else switch `active` to the alternate context if
  its best score > 0.
- **v2 → v3:** the *rule is byte-identical*; v3 added the apparatus —
  checkpoint/continuity, SHA-256 integrity digests, corruption/torn refusal,
  determinism checks, disabled/scrambled controls, resource telemetry.
- **Campaign (quarantined):** regime A 24 train → eval 16/16 → regime B 24 →
  eval 16/16, 2 contexts → return A 15/16 with zero updates; exactly 48 updates.

## 4. R34 curiosity substrate v1 — two-speed prediction-error (native Zag, NEVER WIRED IN)

Source: `docs/generations/R34/runs/R34_NATIVE_QUALIFICATION_STAGE_20260916/r34_curiosity_progress_v1.zag`.

- **Update:** per-slot fast/slow exponential moving averages of *experienced
  prediction error* (caller-supplied):
  `fast ← (1−fr)·fast + fr·error`, `slow ← (1−sr)·slow + sr·error`;
  `count++`, `last_seen=step`.
- **Curiosity score:** `|slow − fast| + novelty·(1 + age/mean_age)`,
  `novelty = novelty_scale/(1+count)`.
- **Status:** qualification-stage substrate. Never drove a learner's decisions.

## 5. R34 memory-lifecycle v1 — delayed full-information delta credit (NEVER WIRED IN)

Source: `.../R34_NATIVE_QUALIFICATION_STAGE_20260916/r34_memory_lifecycle_v1.zag`.

- **Predictor:** bounded-linear future-use estimator
  `pred = clamp01(0.5 + 0.25·(bias + w·x))`, 8 features.
- **Update:** `w ← w + lr·error·g·x`, `bias ← bias + lr·error·g`,
  `g=0.25` (0.05 at saturation so regret can recover a saturated model).
- **Retention:** when the exact store is full, evict the lowest predicted
  future-use slot (ties → oldest); an incoming episode must *strictly beat*
  the worst to displace it.

## 6. R34 hypothesis-state v1 — pairwise contrastive credit (NEVER WIRED IN)

Source: `.../R34_NATIVE_QUALIFICATION_STAGE_20260916/r34_hypothesis_state_v1.zag`.

- **Update:** `w[i] += learning_rate · strength · (features_a[i] − features_b[i])`
  — pure Hebbian-style contrast between two hypotheses' features. No error
  term, no normalization.

## 7. R34 self-model v1 — per-strategy delta heads + error EMA (NEVER WIRED IN)

Source: `.../R34_NATIVE_QUALIFICATION_STAGE_20260916/r34_self_model_v1.zag`.

- **Update:** per-strategy linear head `w += lr·e·x`, `bias += lr·e`,
  `e = target − pred` (delta rule); error-state EMA
  `err ← (1−er)·err + er·|e|`. Separate fast/slow heads for success and cost.
- Delayed outcomes only; counterfactual strategy outcomes deliberately absent.

---

## What the rules have in common (the native design language)

1. **Additive/delta updates on small integer tables** — no gradients anywhere.
2. **Delayed credit via explicit pending slots**, never backprop-through-time.
3. **Determinism by construction** — LCG rng, exact-equality checks.
4. **The R27 semantics (structural PROMOTE/rollback over symbolic traces)
   have no native implementation.** The v2/v3 rule is a bandit learner with
   context recruitment — a long way from `self_revision_history`.

## Banned by DO_NOT_REPEAT (do not reintroduce)

- Confidence-threshold abstention; gradient-based updates of any kind;
- aggregate-only retention reporting (always per-arm/per-cohort endpoints);
- hardcoding answers into the learner; crediting teacher/evaluator knowledge;
- reusing consumed probes as fresh validation.

## Open gaps (rules-lab preregistrations)

- **P1 STRUCT-PROMOTE** — schema-faithful accepted/candidate structural
  revision with per-arm endpoint promotion gates (preregistered, not yet built).
- **P2 TWO-SPEED** — fast/candidate + slow/accepted consolidation in the
  decision loop (built + trialed 2026-09-19 — see TRIAL_RESULTS.md).
- **P3 ADAPTIVE-EPS** — surprise-modulated exploration period
  (built + trialed 2026-09-19 — see TRIAL_RESULTS.md).
- Nonzero-UNKNOWN abstention geometry (E45–E50 candidate mechanism) — needs
  world/harness support; deferred to a world-extension prereg.
