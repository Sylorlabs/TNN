# R34 v3 isolated native continual learner preregistration

R34 v3 is a quarantined engineering campaign. It grants no R27 continuity, learner authority, successor status, or scientific exposure.

The campaign is pure Zag and must use `/Users/Shared/micah/Documents/zag/znc`. Python, PyTorch, TensorFlow, JAX, NumPy, Hugging Face, pickle execution, historical Python verifier execution, and foreign ML runtimes are excluded from qualification.

## Structural isolation gate

The learner core is `r34_learner_core.zag`.

- It may import the observation contract.
- It must not import `world.zag` or `checkpoint.zag`.
- It must contain no `cw_` calls or `CWOutcome` references.
- Hidden regime state, reward generation, world mutation, persistence orchestration, and evaluator controls belong to the harness.
- The learner may receive observations, delayed scalar outcomes, and the causal action identity needed to match pending credit.

## Behavioral gates

- isolated untrained regime-A baseline: 8/16 positive
- after 24 A experiences: 16/16 positive at zero-update evaluation
- after hidden switch and 24 B experiences: 16/16 positive at zero-update evaluation
- two latent contexts represented after A+B
- return to A: 15/16 positive with no score/count updates during return evaluation
- exactly 48 learner updates during A+B training
- update-disabled B control: zero updates and 12/24 positive
- reward-scrambled A training control: 0/16 actual positive at zero-update evaluation
- equal seeds and equal experience streams: exact learner, world, and ingress state

## Continuity and integrity gates

- learner state has its own SHA-256 integrity digest
- the outer R33 12-section checkpoint carries learner, world, and ingress state
- a checkpoint written while delayed causal credit is pending must continue identically in a fresh process
- inner learner corruption must be refused even when the outer checkpoint digest is recomputed
- torn outer checkpoint must be refused
- resource telemetry must be recorded natively

The campaign does not support a claim of general intelligence or superiority to LLMs.

## ⚠️ Contamination notice — 2026-09-20 (R34 hidden-randomness remediation)

**Status: QUARANTINED.** The results recorded in this document are tainted by
hidden randomness in the learner's decision path. The R34 v3 qualification
campaign's training phases (`train_A` / `train_B`, plus the `scramble_train`
control; learner seed `7331`) ran with `explore_enabled=1`, which engaged a
seeded LCG inside the learner core — `r34v3_rng` (`(rng*997+7919) mod 1000003`)
in `r34_learner_core.zag` — driving 1-in-5 pseudo-random explore flips in
`r34v3_choose`. The explore decision was made by a dice-like stream, not by
learner judgment, violating the no-randomness law ("no random exploration").
Verified by the r34 RNG probe (workstream 2/8): investigation commits
`072f25aa` and `4976cbf5` on branch `tnn-native-lab`; Micah's ruling: REMEDIATE.
The runs remain reproducible engineering evidence (byte-identical reruns hold)
but are **not law-compliant evidence** of no-RNG intelligence. Do not cite
these results as canonical until clean reruns exist (exploration replaced by a
deliberate or state-varying mechanism, then re-qualified).
The original text above is left intact for the record.
