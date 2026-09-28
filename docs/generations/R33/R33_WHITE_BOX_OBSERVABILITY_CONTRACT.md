# R33 white-box observability contract

Status: target contract; current implementation has open gaps
[SA-05/06/08/09/11](R33_SUBSTRATE_AUDIT.md). An integer reason code or printed
checksum is not complete causal observability or a cryptographic signature.

## Required trace

Evidence → memory retrieval → live hypotheses → active mechanism/version →
predicted values/uncertainty → decision → consequence → update/regret.
Every material mutation records its authorized owner, trigger, before/after
state digest, changed coordinate/region, rule/version, causal evidence and
resource charge. A route decision also records considered alternatives and
which computations actually ran. Do not fabricate alternatives not evaluated.

## Mutable-state inventory

Checkpoint coverage must include numerical parameters and optimizer accumulators;
episodic raw payload references and checksums; codebook versions and chunk
expansions; hypothesis alternatives and confidence state; retrieval indices,
cache/tier/rehearsal policy; routing gates and recurrent buffers; source-trust
history; candidate module programs and lifecycle state; RNG stream position;
pending observations/actions; permissions and grant references; resource counters;
trace cursor and append-chain state. Every field has an owner, encoding, size,
integrity rule, provenance, version/migration rule and serialization test.

Coverage is measured as accounted mutable regions versus the instrumented
reachable runtime inventory, plus event-level attribution coverage. A high
coverage percentage cannot excuse an unobserved policy, capability, or rollback
field. Any important unaccounted state blocks the corresponding qualification.

Classify state as reversible learner state or non-rewindable supervisor state.
Restoring a checkpoint never restores an older revocation epoch, clears a spent
nonce, refunds cumulative resource charges, or removes audit history. Retained
grant references must be checked against current supervisor authority.

## Failure behavior

Logging must reserve capacity before a consequential transaction commits. On
disk/buffer exhaustion, block mutation or stop the run with durable incomplete
status; never silently drop records. Recovery replays committed transactions
once, ignores uncommitted writes, preserves sequence/parent identity, and records
any authorized external side effect separately. A failed rollout remains in
provenance after rollback; rollback restores operational state, not history.

Bounded negative tests include trace-capacity+1, failed append, dangling parent,
duplicated event, reordered event, codebook changed after encoding, missing RNG,
missing optimizer state, corrupted checkpoint, incomplete transaction and
unauthorized policy edit. Reconstruct decisions from records in a clean process,
then continue learning and compare against an uninterrupted control.

## Explanation and causal claims

Use distinct labels: RECORDED_STATE, DERIVED_METRIC, CAUSAL_INTERVENTION,
HEURISTIC_DIAGNOSIS, and UNMEASURED. A learning delta can be attributed to an
update transaction; attributing an eventual gain to one parameter requires
additional controlled intervention. Abstain from a causal conclusion when
several changes or support differences are confounded.

Human-readable self-report must reference actual accessible state, uncertainty
and evidence. Calibration is an empirical property checked against outcomes,
not a value assigned by a trace wrapper. Real internal conflict and unknown
state may be reported without inventing a narrative of understanding.

The read-only R33 documentation validator checks registry/contract consistency;
it is not the protected native supervisor and grants no runtime authority.
