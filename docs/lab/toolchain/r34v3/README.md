# R34 Native Continual Learner V3

R34 v3 structurally separates the learner from the evaluator/world used by R34 v2.

`r34_learner_core.zag` owns learner state, action choice, delayed-credit matching, latent-context switching, observation decoding, and learner serialization. It imports only the R33 observation layer.

`r34_continuing_harness_v3.zag` owns the R33 world, hidden regime changes, evaluator controls, checkpoint assembly, persistence, fresh-process continuation, corruption fixtures, and campaign reporting.

The lane is additive and quarantined. It does not modify canonical R27, open `learn`, grant learner authority, consume scientific exposure, or promote a successor.

Run `run_native.zsh` to create a timestamped evidence directory with source/compiler/binary hashes, structural isolation checks, the behavioral campaign, pending-credit fresh-process continuation, corrupt/torn refusal, resource output, and a final receipt.

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
