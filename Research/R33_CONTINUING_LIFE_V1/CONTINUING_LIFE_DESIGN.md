# Continuing-life design

This design gives the simulated and real-sensory tracks one boundary. It does
not claim that either track is already an integrated learner.

## Shared interfaces

An observation contains raw payload, source identity, clock identity, sequence,
tick, action ancestry, encoding, dimensions/rate, channel count, and a SHA-256
over the exact header and payload. The native observer retains the original
bytes. It rejects malformed headers, invalid channel counts, duplicate or
backwards sequence/time, clock changes, overlap, and corrupted payloads.

An action is recorded before its consequence is interpreted. A consequence
contains the action that caused it, the tick at which it became available, and
the observable result. Delayed outcomes remain in world state and in the
checkpoint; they are never filled in from evaluator knowledge.

A checkpoint has one parent identity, one predecessor digest, a monotonic
sequence, all twelve required sections, exact lengths, and a final digest.
Sections 1–10 are reserved for complete learner-owned state, section 11 is
world-owned, and section 12 is ingress-owned. The current fixture fills the
learner sections with tagged placeholders so the transport contract is tested
without pretending that a learner exists.

## Simulated continuing life

`world.zag` provides a persistent bounded world with positions, occlusion,
changing regime, inspection cost, delayed consequences, returning state, and
rendered observations. The regime and object identity are hidden from the
observation bytes. Invalid actions and an action submitted while a delayed
consequence is pending are refused without mutating world state.

The first scientific world campaign should expose returning situations and
unfamiliar combinations after earlier learning. It should include matched
ordinary-update, frozen-behavior, and resource-control arms. N16 may be one
candidate mechanism, but a mechanism-removal arm must test whether it causes
the effect. The evaluator must hold hidden state and fresh labels outside the
learner process.

## Real sensory experience

The current ingress layer qualifies encoded PCM16LE and RGB8 transport only.
It preserves raw samples or pixels with format, timing, dimensions, and source
metadata. This is the correct first boundary for audio and vision, but it is
not a physical microphone/camera or perception qualification.

The next sensory work should qualify device transport, clock behavior,
ordering, loss, and accessible distinguishing information separately. Semantic
segmentation, hidden identities, and evaluator labels must remain outside the
learner input. Once transport passes, learned perception can be tested across
changed lighting, noise, viewpoint, timing, and returning stimuli while raw
evidence is retained beside learned abstractions.

## Integration rule

The two tracks join only through the shared observation, action/consequence,
checkpoint, and attributed-update interfaces. A fresh-process reload must
restore learner state, causal trace, world state, and sensory stream state as a
single accepted continuation. A frozen parent file plus a separately initialized
learner does not satisfy this rule.

