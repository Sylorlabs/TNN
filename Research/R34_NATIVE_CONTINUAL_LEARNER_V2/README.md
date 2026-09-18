# R34 Native Continual Learner V2

This additive lane moves the R34 learner from immediate task/reward fixtures into the persistent R33 world with observation packets, delayed touch consequences, hidden regime changes, latent context reuse, complete checkpointing, and fresh-process continuation.

`r34_continuing_learner_v2.zag` contains the learner plus a quarantined evaluation harness. Reward policy and hidden regime state remain in `R33_CONTINUING_LIFE_V1/world.zag`. The learner is never passed the regime bit.

`run_native.zsh` builds with the local Zag compiler, runs the preregistered campaign and controls, verifies exact fresh-process continuation, exercises corrupt/torn refusal, records resource output and hashes, and leaves canonical R27 and `learn` untouched.
