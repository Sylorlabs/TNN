# R34 Native Continual Learner V3

R34 v3 structurally separates the learner from the evaluator/world used by R34 v2.

`r34_learner_core.zag` owns learner state, action choice, delayed-credit matching, latent-context switching, observation decoding, and learner serialization. It imports only the R33 observation layer.

`r34_continuing_harness_v3.zag` owns the R33 world, hidden regime changes, evaluator controls, checkpoint assembly, persistence, fresh-process continuation, corruption fixtures, and campaign reporting.

The lane is additive and quarantined. It does not modify canonical R27, open `learn`, grant learner authority, consume scientific exposure, or promote a successor.

Run `run_native.zsh` to create a timestamped evidence directory with source/compiler/binary hashes, structural isolation checks, the behavioral campaign, pending-credit fresh-process continuation, corrupt/torn refusal, resource output, and a final receipt.
