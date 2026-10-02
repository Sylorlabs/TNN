# R34 "deterministic RNG" probe — investigation notes (workstream 2 of 8)

Date: 2026-09-20. Investigator: TNN lab worker (subagent depth 2).
Task: resolve the "deterministic RNG" mention in `r34_learner_core.zag` against Micah's no-RNG law.
Verdict: **PROBLEM-REQUIRING-ACTION** (see VERDICT.md in this directory).

## 1. Where the mention was found

Two hits in the Drive doc-sweep corpus (`~/workspace/tnn-lab/wave12/senses/doc-sweep/docs_local/`):

- `0621_WORKLOG_20260916.md` line 9 (R34 v3 worklog, 2026-09-16):
  > "`r34_learner_core.zag` contains learner state, **deterministic RNG**, action choice, score/count updates, latent-context switching, causal pending-credit state, observation decoding, and learner serialization."
- `0011_TNN_CAPABILITY_MASTER_PLAN_20260918.md` line 1088, listing "deterministic RNG" under
  "Appropriate fixed substrate — Likely acceptable" (alongside hashing, checkpoint format, etc.) —
  i.e. old design thinking treated a deterministic RNG as acceptable *substrate infrastructure*,
  not as a decision mechanism.

`r34_learner_core.zag` itself is real and committed on tnn-native-lab at
`docs/generations/R34/runs/R34_NATIVE_CONTINUAL_LEARNER_V3/r34_learner_core.zag`
(blob sha `488cdedaad2eab7f04fdde8ab53ae620deb6ced4`, 98 lines) — byte-identical to the
workspace copies (`~/workspace/tnn-lab/toolchain/r34v3/` and the LH-4/LH-5/LH-7 variant
toolchains; diff-clean).

## 2. What the mechanism actually is

Not a test driver, not a harness utility, not offline fixture generation. It is a **seeded
linear-congruential PRNG living inside the learner core** and consumed by the learner's
action-decision function:

```zag
fn r34v3_rng(s:*R34V3State)i32 {let v:i32=r34v3_mod(s.*.rng*997+7919,1000003);s.*.rng=v;return v;}
```

- State: `rng:i32` field of `R34V3State`, initialized from a fixed seed via `r34v3_init(seed)`.
- Seeds used in harnesses are all fixed constants: `7331` (R34 v3 campaign), `991`
  (replay-determinism check), `4441` (checkpoint mid), `47111` (`LH4_LEARNER_SEED`).
  No time-based, OS-entropy, or run-varying seed anywhere in any harness.
- The `rng` field is serialized into checkpoints (`cl_put(out,48,s.*.rng)`), bounds-checked on
  decode, covered by `r34v3_equal` and the state fingerprint `r34v3_fp`. Reruns are byte-identical
  (the `deterministic_learner` check — two runs from seed 991 — passes exactly because the stream
  replays identically).

## 3. How it feeds an AI decision

Single production consumer — `r34v3_choose`, the learner's action-choice function:

```zag
fn r34v3_choose(s:*R34V3State,explore_enabled:i32,was_explore:*i32)i32 {
    ...
    let obj:i32=r34v3_best(s,s.*.active);let ex:i32=0;
    if(explore_enabled==1 && r34v3_mod(r34v3_rng(s),5)==0){obj=1-obj;ex=1;}
    ...
}
```

Characterization: **epsilon-greedy-style pseudo-random exploration**. When `explore_enabled==1`,
the LCG output decides a 1-in-5 flip of the greedy action (`r34v3_best`); the flip is recorded in
`pending_explore` so exploratory failures don't trigger latent-context switches
(`r34v3_accept` requires `s.*.pending_explore==0` before switching). The greedy policy itself is
deterministic (`r34v3_best`, with a state-varying `s.*.decisions%2` tie-break — a compliant
deterministic pattern). The exploration *decision* is made by the LCG stream, not by any
learner judgment.

Call sites with `explore=1` (R34 v3 harness `r34v3_campaign`):
- `train_A` / `train_B` — the qualification training phases behind "trained A: 16/16, trained B: 16/16"
- `scramble_train` control
- the `deterministic_learner` replay check

Call sites with `explore=1` (LH-4 `lh4_campaign`, the long-horizon leg): **every training visit**
(`lh4_phase(...,regime,LH4_TRAIN_N,1,1,0,1,&tp)` — explore is the final `1`).
Eval / return-eval phases run `explore=0` (pure greedy). The learner core is diff-identical across
all variants, so the same holds for LH-5 and LH-7.

## 4. What it is NOT

- Not true randomness: no entropy source; fully deterministic given (seed, episode count);
  byte-identical reruns hold and are certified by the qualification's own determinism check.
- Not world-side: the learner core imports only the observation contract (per the adversarial
  review's structural rules); the RNG lives strictly learner-side.
- The whitebox tests (`wb_whitebox_tests.zag` lines 155-156, 179) use `r34v3_rng` only to check
  seed-sensitivity and serialization round-trip — test-fixture use, benign.
- Not declared in the prereg: `0302_PREREGISTRATION.md` never mentions exploration; the
  adversarial review (`0245`) and qualification checklist (`0311`) don't address it either.
  The prereg defines determinism operationally ("equal seeds and equal experience streams: exact
  learner, world, and ingress state") but never states that action choices during training are
  pseudo-randomly perturbed 1-in-5.

## 5. Assessment against the no-RNG law

Standing law: "no randomness anywhere in the AI's decision paths — no random exploration, no
random tie-breaks, no stochastic policies; every mechanism must be deterministic given state
('the world can be unpredictable; the mind can't be dice')".

- Engineering clause ("deterministic given state", byte-identical reruns): SATISFIED.
- Explicit clause ("no random exploration") and Micah's stated reasoning ("RNG is not intelligence;
  no randomness in the AI, period"): VIOLATED IN SPIRIT. The explore/no-explore decision on every
  training episode is made by a dice-like LCG stream rather than by learner judgment. A replayable
  die is still a die for the purpose of "the mind can't be dice".
- The old design note (0011) that "deterministic RNG" is acceptable *substrate* does not cover this:
  the mechanism is in the decision path, not in the substrate.

## 6. Claims implicated

- R34 v3 qualification results (trained A 16/16, trained B 16/16, return A 15/16, 48 updates) —
  training ran with explore=1.
- LH long-horizon headline results (delayed-credit rule stable at 100x horizon, 16/16 throughout) —
  all training visits ran with explore=1.
- The results remain valid engineering evidence (deterministic, byte-identical, white-box); they are
  not fabrications. But they were produced with LCG-driven exploration in the training decision path,
  so they cannot be cited as canonical no-RNG-law evidence until resolved.
