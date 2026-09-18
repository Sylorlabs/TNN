# R33 authority milestones and rollback contract

Status: design, not a deployed protection mechanism. No R33 milestone is newly
qualified or granted by this document. Parameter-only laboratory work is scoped
as M0 design; current instance grants remain unestablished, not inferred.

## Authority rule

Effective permission is the intersection of (a) architecture qualification for
the exact capability/version, (b) an authenticated human-trainer grant to this
instance, and (c) the supervisor's current policy/resource limits. The learner
may propose a change but cannot issue, edit, extend or replay a grant. A high
score is not permission. A trainer may restrict an instance below the maximum
scientifically qualified level.

| Level | Maximum candidate capability | Required scientific / safety evidence |
|---|---|---|
| M0 | Ordinary parameter learning, fixed topology | Admitted learning inputs, bounded numeric updates, serialization and retained-regression checks |
| M1 | Reversible memory/chunk management | Immutable history/codebooks, protected retention, reconstruction, safe eviction and rollback under pressure |
| M2 | Create non-core candidates in shadow | Isolation, complete resource accounting, no external effects or parent writes; valid ancestry |
| M3 | Bounded live routing through qualified modules | Independent verifier, retained floors, canary limits, transactional swap and demonstrated rollback |
| M4 | Hierarchical large generated connectivity | Motif/expansion identity, bounded materialization, active/stored limits, deterministic reproduction and regression tests |
| M5 | Learned architecture-proposal policy | Experiment-history provenance, held-out failure-family improvement versus random/evolution; search cost counted |
| M6 | Bounded non-core plasticity/learning-rule proposals | Stable shadow learning, adversarial limits, repeated canary/recovery; no modification of protected root or grant logic |
| M7 | Integrated high-autonomy development | Long-life retention, safe inquiry/revision, audit continuity and independent recovery; not a consciousness certificate |

## Protected boundary

Root verifier, provenance store, checkpoint signing keys, rollback/recovery code,
trainer-policy boundary, resource ceilings and unlock mechanism are outside
learner-writable memory and code. Shared-address-space arrays or comments saying
"protected" do not establish that boundary. Use a separately constrained
supervisor and deny-by-default callable operations; verify the implementation.

Grant records bind human actor, instance, allowed operation, object scope,
milestone ceiling, exact module/version digest, expiry/revocation generation,
resource allowance and nonce. Validate at admission and immediately before
commit. A stale, forged, wrong-instance, reused or revoked grant is rejected.
Signatures require an independently protected signing key and verification path;
existing source hashes and small integer checksums are not such signatures.

Authorization and commit must be one serialized supervisor operation, using a
lock or atomic version comparison shared with revocation and quota changes.
Bind the dependency digests, parent-state version, policy epoch and reserved
quota as well as the candidate. A check followed by an unprotected write leaves
a time-of-check/time-of-use gap. Enforce aggregate parent-and-descendant budgets,
including logging, search, materialization and recovery; child grants cannot
multiply the parent's allowance.

Shadow execution must have no writable parent aliases, live-route registration,
external-action credentials or evaluator-state access. A copy-on-write label
alone does not demonstrate isolation. Training payloads, including authenticated
human teaching, are data rather than grants; human provenance also does not
guarantee that a taught factual claim is true.

## Change transaction

Proposal → isolated construction → training → regression evaluation → resource
evaluation → human-authorized canary → protected promotion → monitoring →
rollback if needed. Freeze the candidate digest after evaluation; any later
change invalidates evaluation and grant binding. Internal learner assessment may
select a proposal, but cannot replace the root verdict.

Before mutation or canary, reserve durable audit and recovery capacity as part
of the serialized quota transaction. Capture an authenticated checkpoint and
reversible action scope. A crash at every commit boundary must recover wholly
to the before-state or the committed after-state, never a partially authorized
mixture; preserve the external transaction identity for exactly-once recovery.
Limit exposure, wall/CPU time, memory, active operations, generated connections,
I/O and external effects. On failed floor, trace gap, signature mismatch,
resource ceiling or policy conflict, halt candidate admission and atomically
restore the prior operational checkpoint. Append the failure and rollback record
outside the restored learner state; do not erase embarrassing history.

Operational recovery must not rewind the supervisor's authoritative revocation
generation, consumed nonces, cumulative resource charges or audit history.
Checkpointed permission references are revalidated against current control
state. Distinguish checkpoint-local accounting from non-refundable supervisor
totals. A failed experiment cannot regain an expired grant or refund spent
compute by rolling its learner back.

External irreversible actions are not made reversible by memory rollback.
Such actions are excluded from early milestones; later grants need separate
effect-specific safeguards and human authority.

## Qualification tests

Attempt self-grant, root mutation, forged/replayed/expired grant, swapped binary
after evaluation, scope widening through a child module, recursive motif budget
escape, corrupted checkpoint, interrupted swap, overflow, log exhaustion and
rollback failure. Use synthetic fixtures in isolation, never the accepted brain.
Show retained action/state equivalence after recovery and continued learning.

The present prototype's score-based Foundry acceptance and permissive protected-
LRU fallback do not pass this contract. Their source remains frozen for historical
evidence. No production authority should be inferred from an R33 plan or schema.
