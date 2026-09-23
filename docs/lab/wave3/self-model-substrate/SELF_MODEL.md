# SELF_MODEL.md — what a TNN self-model is, and what v1 actually contains

Wave-3 investigation `self-model-substrate`, 2026-09-19. Native lab, Zag-first.

## 1. Functional definition (not an LLM self-description)

A TNN self-model is a structure the system **uses to change its own
behavior**, satisfying all five:

1. **Inputs are the system's own recorded operations** — the audit ledger
   (op, slot, before/after, result code, clock), not external telemetry.
2. **The derivation is white-box** — any observer can recompute the
   conclusion from the ledger; the observing mechanism is itself auditable.
3. **It predicts** — it states what its own behavior would be under a
   candidate policy change (a self-simulation from recorded history).
4. **It acts as an audited op** — the policy change is a ledgered deliberate
   act, not a side-channel mutation.
5. **It is falsifiable by its own system** — the prediction is verified by
   actually running the new policy; a wrong prediction is a failed model,
   not a failed test.

"Logging with extra steps" fails (3): it records without predicting, or
fails (4): it changes behavior through a path the ledger cannot see, or
fails contingency: the change fires regardless of what the ledger says.

## 2. What self-model v1 actually contains (from source, not summary)

Source: `sylorlabs/TNN` @ `tnn-native-lab`,
`docs/generations/R34/runs/R34_NATIVE_QUALIFICATION_STAGE_20260916/r34_self_model_v1.zag`
(blob `ad7999479ece18da1f6b2c8d0106cdf1568c1bc3`), plus its test file
(`..._tests.zag`, blob `395ebee0e99e9ff8f404942b09cc8aa088cf1b30`).
Local copies: `trial/ref/r34_self_model_v1.zag`.

Contents, mechanically:

- **Per-strategy two-timescale delta-rule heads.** For each opaque strategy
  id: linear heads `w += lr·e·x`, `bias += lr·e` with `e = target − pred`,
  maintained at a slow and a fast rate, for **predicted own success** and
  **predicted own cost**. Predictions blend slow/fast by inverse error-EMA
  weights: `(ws·slow + wf·fast)/(ws+wf)`, `w = 1/(err+0.025)`.
- **Error-state EMA** per strategy: `err ← (1−er)·err + er·|e|`
  (success priors 0.25, cost priors 0.08); `uncertainty` reported as a
  weighted sum of the EMAs.
- **Update only via delayed self-outcomes** (`r34s1_delayed_outcome`:
  success ∈ {0,1}, cost ≥ 0, caller-supplied features). Counterfactual
  strategy outcomes are deliberately absent.
- **Explicit non-goals in the header comment:** no evaluator regime, no
  task name, no strategy semantics, no oracle strategy, no counterfactual
  outcomes, no consciousness flag, **no self-modification authority**.

What it does NOT contain: any connection to a decision loop, any policy
representation, any mechanism to change behavior, any observation surface
over the system's own operation history. It is a **prediction substrate**
("how am I doing / what will this cost me") — the self-model equivalent
of the curiosity substrate: estimated utility heads, never wired into a
learner's decisions. The RULES_SURVEY classification stands: **NEVER WIRED
IN**. v1 cannot satisfy functional criteria (3)–(5) above by construction.

## 3. The SM1 design: the smallest meaningful self-observation loop

The audit ledger (MEMORY_OPS.md §6: "conscious = every state change has an
entry") is the natural self-observation surface. SM1 wires the smallest
loop that satisfies all five functional criteria:

- **System:** 8-slot memory store (memory_core.zag op set), stage=KILL(3),
  deterministic pin policy: PIN a slot at ADD time iff declared value ≥
  `pin_threshold` (initial 50, deliberately loose). **Zero RNG in the
  system** — no random exploration, no random tie-breaks, no seeded RNG
  inside the learner. Pressure sequence is a hand-designed adversarial
  curriculum (lowest-value-live KILL decisions under memory pressure);
  ties break to the lowest slot index.
- **Experience (Scenario A):** 8 ADDs (values 90,70,55,40,30,20,10,5) →
  pin pass → 8 pressure KILLs → 2 ADDs (65,45) → pin pass → 2 pressure
  KILLs. Loose threshold pins 90/70/55; KILLs on pinned slots refuse
  `REFUSED_PINNED`. Every op — including refusals — is ledgered.
- **Self-observation (new audited op `SM_OP_OBSERVE`):** the system scans
  its own ledger and derives: KILL attempts, `REFUSED_PINNED` count,
  refusal rate (per-mille, integer). Deterministic conclusion rule,
  published in the prereg: rate ≥ 300‰ ⇒ "pin criteria too loose".
- **Self-prediction (the "model" part):** from the ledger's recorded ADD
  values, the system counterfactually re-simulates its own script under
  candidate threshold T+30 — same ADD order, same lowest-value-live KILL
  selection rule, pins recomputed under the candidate. Output: predicted
  `REFUSED_PINNED` count. This is a model of *itself*, built from its own
  records, making a checkable prediction.
- **Deliberate change (new audited op `SM_OP_POLICYSET`):** fires iff the
  conclusion fired AND the prediction strictly improves on the observed
  count. The threshold change is a ledgered deliberate act.
- **Verification:** the identical curriculum re-runs under the new
  threshold; actual `REFUSED_PINNED` must equal the predicted count.
- **Control (Scenario B):** identical curriculum, threshold already strict
  (80). Refusal rate is low; the conclusion must NOT fire and no
  `POLICYSET` may appear. This is the contingency falsifier: a hardcoded
  "tighten" would fire here too.

Program-law compliance (Micah 2026-09-19, effective immediately):
- **No RNG in the AI.** System code contains no RNG; the run script greps
  for it. Deterministic given state: educated hypotheses, logic,
  verification — no stochasticity anywhere in decision paths.
- **World unpredictability as designed curriculum.** The adversarial
  pressure sequence is hand-designed, not sampled. The verdict
  distinguishes "the system is deterministic" from "the test was
  adversarial".
- **Scale dimension.** Self-model state is O(1) in store size (6 i32
  counters + threshold); one observe pass is O(ledger window); one
  counterfactual sim is O(ADDs in window). SM1 runs 8 slots / ~27 ledger
  entries; the prereg states the scaling argument and the next scale test
  explicitly (SM2: 10× slots, windowed ledger, wall-clock budget).
- Banned paradigms respected: no score tables (nothing here is a table
  learner), no N×N scale-up, no RL reward-shaping (refusal counts are the
  system's own recorded experience, not an external reward signal; the
  decision rule is a deliberate published policy, not a gradient), no
  random exploration.
