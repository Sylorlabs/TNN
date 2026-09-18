# R34 native held-out behavioral qualification V2 preregistration

V1 development construction failed before held-out execution because three controls were invalid: association erased cue/context identity, curiosity made the noise arm itself drift, and self-model evaluation covered only the final regime where one fixed strategy had zero regret. V1 is retained unchanged as negative construction evidence.

V2 changes only those evaluator constructions. The six learner primitives and V1 thresholds remain unchanged.

Held-out seeds remain frozen and unseen: `34211`, `34213`, `34217`.

Association now uses five learner-visible cue nodes, each with three opaque candidate neighbors. A hidden mapping changes once; retrieval-linked consequence credit and co-use-only control see identical cue/retrieval events.

Curiosity now uses a stationary high-error noise arm, a gradually learnable arm, and a sparse contradiction arm. This tests noise avoidance rather than tracking evaluator-generated jitter.

Self-model regret is measured over both a pre-drift and post-drift evaluation window. The best fixed strategy is therefore a valid lifetime control rather than an oracle for the final regime.

Pass gates are exactly the six numerical thresholds preregistered in V1. No threshold changes are allowed under V2.
