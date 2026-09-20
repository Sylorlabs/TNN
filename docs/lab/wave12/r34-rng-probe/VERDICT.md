# VERDICT — R34 "deterministic RNG" probe (workstream 2 of 8)

Date: 2026-09-20. Investigator: TNN lab worker (subagent depth 2).

## Verdict: PROBLEM-REQUIRING-ACTION

`r34_learner_core.zag` contains a seeded LCG (`r34v3_rng`: `(v*997+7919) mod 1000003`) that
drives **pseudo-random exploration inside the learner's action-decision function**
(`r34v3_choose`: 1-in-5 greedy-action flip when `explore_enabled==1`). Training phases —
including the R34 v3 qualification training and every LH long-horizon training visit — run
with `explore=1`. This satisfies the law's engineering clause (deterministic given state,
byte-identical reruns, fixed seeds, rng state serialized in checkpoints) but collides with the
law's explicit "no random exploration" ban and Micah's "no randomness in the AI, period"
reasoning: the explore decision is made by a dice-like stream, not by learner judgment.
I cannot certify this BENIGN without unilaterally reinterpreting the law — that ruling is
Micah's alone.

## Required actions

1. **Quarantine (immediate, no approval needed):** R34 v3 may not be cited as canonical until
   resolved. The R34 v3 qualification results and the LH delayed-credit long-horizon results
   were produced with LCG-driven exploration during training. They stand as reproducible
   engineering evidence but are not law-compliant evidence of no-RNG intelligence.
2. **Remediate via one of (needs Micah's dated approval either way):**
   a. Remove the exploration LCG and replace it with a deliberate or state-varying
      (non-dice) exploration mechanism — e.g. extend the existing compliant `decisions%2`
      pattern — then rerun R34 v3 qualification and the LH legs and re-certify; OR
   b. A dated prereg amendment, approved by Micah, explicitly ruling that seeded deterministic
      PRNG exploration is law-compliant, with the reasoning recorded. The amendment must also
      close the prereg gap: exploration is currently undeclared (0302_PREREGISTRATION.md never
      mentions it).
3. **Scanner/red-team rule (recommendation):** any seeded PRNG stream consumed inside a decision
   path must be declared; "deterministic RNG" as acceptable *substrate* (hashing, fixture
   generation, replay) must not be conflated with PRNG-driven *decision* mechanisms.

## Not implicated

- Eval and return-eval phases (`explore=0`) — pure greedy, deterministic.
- World/harness side — the RNG is learner-side only; the structural isolation claims hold.
- Whitebox tests' use of `r34v3_rng` (seed-sensitivity / serialization checks) — benign fixture use.
- No true randomness anywhere: no entropy source, no time-seeded runs; byte-identical reruns hold.

## Evidence index

- Source: tnn-native-lab `docs/generations/R34/runs/R34_NATIVE_CONTINUAL_LEARNER_V3/r34_learner_core.zag`
  (blob sha `488cdedaad2eab7f04fdde8ab53ae620deb6ced4`); identical copies in
  `~/workspace/tnn-lab/toolchain/r34v3/` and LH-4/LH-5/LH-7 variant toolchains.
- Worklog quote: Drive corpus `0621_WORKLOG_20260916.md:9`.
- Design-note quote: Drive corpus `0011_TNN_CAPABILITY_MASTER_PLAN_20260918.md:1088`.
- Prereg: Drive corpus `0302_PREREGISTRATION.md` (no exploration mention); adversarial review `0245`;
  qualification checklist `0311_TNN_R34_V3_QUALIFICATION_CHECKLIST.md`.
- Full mechanism trace: INVESTIGATION.md in this directory.
