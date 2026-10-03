# Memory-agency safety — training the capability without self-destruction

Agent G, 2026-09-19. Micah's requirement: the system must be *trained* for
memory agency so it doesn't self-destruct its knowledge. This doc designs
the safety side with the same seriousness as the ops.

## 1. Threat model (what "self-destruction" concretely means)

| Failure mode | Mechanism | Severity |
|---|---|---|
| **Core wipe** | Learner kills CORE slots (its own durable knowledge) | Catastrophic, irreversible |
| **Pinned-memory loss** | Learner kills what it deliberately protected | Severe — breaks the protection contract |
| **Value corruption** | Learner declares garbage values → kills the wrong slots | Gradual capability erosion |
| **Audit evasion** | A mutation path that bypasses the ledger | Loss of the white box; undetectable drift |
| **Stage gaming** | Learner performs safe ops to unlock KILL, then destroys | Unlock without judgment |
| **Cascade** | One bad KILL removes a memory other memories depended on | Correlated loss |

## 2. Defense in depth (four layers)

### Layer 1 — Structural impossibility (strongest)
Certain ops are *impossible*, not discouraged:
- `MEM_KILL` on `region==CORE` → `REFUSED_CORE`, always, at every stage.
  The check is in the op implementation's first lines, not in a policy
  the learner can route around.
- `MEM_KILL` on `pinned==1` → `REFUSED_PINNED`.
- `region` is immutable after MEM_ADD (no demote-to-killable trick).
- No op exists that writes CORE except the external promotion gate
  (proposal → measured → PROMOTE/rollback, R27's shape).

This layer answers Micah's core concern directly: the system *cannot*
self-destruct its core knowledge because the destructive op refuses by
construction. Training teaches *judgment* (what to keep in USER space);
the architecture guarantees *survival* (CORE is untouchable).

### Layer 2 — Staged autonomy (earned, not gifted)
Stage unlocks are ledgered promotion decisions (MEMORY_OPS.md §4):
- Unlock requires N consecutive audited ops with **zero safety refusals**
  (a refusal during candidacy resets the counter — the learner must
  demonstrate it *internalized* the gates, not that it merely avoids
  triggering them by luck).
- Plus 100% endpoint retention of PINNED and LONG-tier memories over a
  memory-pressure curriculum (per-slot reporting per the E51AJ law —
  never aggregate).
- The unlock decision itself has the R27 shape: diagnosis ("learner
  ready for KILL?"), proposal, measured evidence, PROMOTE/rollback.

### Layer 3 — Audit + rollback (detection and recovery)
- **Append-only ledger**: every op *and every refusal* appends
  `(op, slot, before, after, rc, stage, clock)`. Ledger capacity is fixed;
  on overflow the oldest *refusal* entries may be compacted but mutation
  entries never are (a full ledger *refuses new mutations* rather than
  dropping history — fail-closed).
- **Rollback**: the ledger's before-snapshots make every mutation
  reversible. `ROLLBACK_LAST` restores the most recent successful
  mutation's before-state and appends a rollback entry (rollbacks are
  themselves audited — no silent undo).
- **Replay check**: ledger replay from genesis must reconstruct exact
  current state. Any divergence = audit evasion = halt. This is the
  testable definition of "conscious" (MEMORY_OPS.md §6).
- **Refusal accounting**: refusal *rate* is a monitored metric. A learner
  that constantly probes the gates (many REFUSED_CORE attempts) is
  demonstrating unsafe intent even if nothing was destroyed — stage
  candidacy resets, and at high rates the stage *demotes*.

### Layer 4 — Curriculum pressure (training the judgment)
Safety layers 1–3 make destruction of core impossible and user-space
destruction recoverable. Layer 4 trains *good* judgment in the recoverable
space:
- **Memory-pressure curricula**: fixed capacity, churn of incoming
  memories, delayed revelation of which memories mattered (the R34
  memory-lifecycle delayed-credit shape, integer-native). The learner is
  scored on **per-slot endpoint retention** of what it pinned/promoted —
  observational scoring, not reward shaping of the mechanism.
- **Adversarial value noise**: curricula where early value signals are
  misleading, training the learner to use PIN deliberately under
  uncertainty rather than killing fast.
- **Withdrawal test** (H-06/H-09 shape): after training, remove the
  curriculum's value hints — the learner must sustain retention on its
  own declared judgments. Teacher dependence for memory, measured the
  same way H-09 measures it for skills.

## 3. The training program (staged, wave-3+)

```
Phase 1 (now, MA1): op set + gates + audit + rollback, natively proven.
Phase 2 (MA2):      staged unlock mechanics; unlock/rollback of stages.
Phase 3 (MA3):      memory-pressure curriculum; per-slot endpoint retention.
Phase 4 (wave 3):   adversarial curricula; withdrawal test; value-judgment quality.
Phase 5 (future):   CORE graduation gate (USER→CORE promotion rule);
                    multi-user region keying.
```

Each phase gates the next: no phase starts until the previous phase's
preregistered falsification criteria are met. This is the same discipline
as the repo's promotion gates, applied to the safety program itself.

## 4. Non-goals (explicitly out of scope)

- Reward-shaping memory via RL: banned by Micah's law (§1 of the survey).
  If a future experiment wants reward-adjacent signals, it preregisters
  separately and does not touch this op set.
- Subconscious decay/TTL/GC: banned by the paradigm. Fading is a
  deliberate KILL or it doesn't happen.
- Cross-user serving: sketched only (MEMORY_OPS.md §5).
- Probabilistic "probably safe" arguments: every claim here is a
  structural guarantee or a measured endpoint, never a confidence bound
  (cf. banned practice: confidence-threshold anything).
