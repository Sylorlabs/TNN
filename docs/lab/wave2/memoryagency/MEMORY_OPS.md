# Memory operations — the learner's deliberate action set

Agent G, 2026-09-19. Design for TNN-native conscious memory agency.

## 0. The paradigm in one paragraph

Memory operations are **actions in the learner's own action space**, issued
by the learner's decision logic — not by an external scheduler, not by a
reward optimizer. The learner *declares* a memory's worth when it adds it
(explicit value judgment, auditable), and later *decides* to kill, pin,
promote, or demote it. Value signals from substrates (curiosity scores,
future-use estimators) may **advise**; they never decide. Every op returns a
result code; refusals are explicit, never silent. Every mutation is
audit-logged with before/after and is reversible.

## 1. The operation set

All ops act on **slots** — fixed-capacity, addressable memory objects.
A slot: `{live, value, pinned, region, tier, step_added}`.

| Op | Signature | Effect | Refusal conditions |
|---|---|---|---|
| `MEM_ADD` | `(value:i32, region) → slot` | Writes a new memory into an empty slot with the learner-declared value | `REFUSED_FULL` (no empty slot), `REFUSED_STAGE` (stage < ADD) |
| `MEM_KILL` | `(slot) → rc` | Clears the slot: `live=0`, fields zeroed | `REFUSED_NOTLIVE`, **`REFUSED_CORE`** (region==CORE — absolute), **`REFUSED_PINNED`** (pinned==1), `REFUSED_STAGE` (stage < KILL) |
| `MEM_PIN` | `(slot) → rc` | `pinned=1` — the slot can no longer be killed until unpinned | `REFUSED_NOTLIVE`, `REFUSED_STAGE` (stage < MANAGE); pin on a CORE slot is redundant → `REFUSED_CORE` (core is already unkillable; keeps the audit log honest about no-ops) |
| `MEM_UNPIN` | `(slot) → rc` | `pinned=0` | `REFUSED_NOTLIVE`, `REFUSED_STAGE` |
| `PROMOTE_TO_LONGTERM` | `(slot) → rc` | `tier=LONG` | `REFUSED_NOTLIVE`, `REFUSED_STAGE` |
| `DEMOTE_TO_SHORTTERM` | `(slot) → rc` | `tier=SHORT` | `REFUSED_NOTLIVE`, `REFUSED_STAGE` |

Result codes are small positive integers (`MA_OK=0`, `MA_REFUSED_*=101+`);
every op appends `(op, slot, before_snapshot, after_snapshot, rc, clock)` to
the audit ledger — **including refusals** (a refusal is an event worth
auditing: it proves the gate held).

### Value semantics (the anti-RL clause)

`value` is assigned **by the learner at MEM_ADD time** as an explicit
judgment ("I declare this worth 90"), in the same integer scale the
learner's other decisions use. It is *not* a reward, *not* a Q-value, and
no reward signal flows into the memory path. The learner may later revise
its judgment only by killing and re-adding (a deliberate, audited act) —
there is no background decay and no gradient. Rationale: subconscious
decay is exactly the loss-of-control Micah rules out. If the system wants
a memory to fade, it kills it *deliberately*.

Substrate estimators (curiosity `|slow−fast|`, lifecycle future-use
predictor) are **advisors**: the learner may read them as inputs to its
declared judgment, but the op log records the *decision*, not the advice.
This keeps the white box open: "why did you keep this?" always has an
answer — "I pinned it at clock T," not "the optimizer did it."

## 2. Slot lifecycle

```
EMPTY →(MEM_ADD)→ LIVE/SHORT ──→(PROMOTE)→ LIVE/LONG
                    │  ├→(MEM_PIN)→ pinned (unkillable until MEM_UNPIN)
                    │  └→(MEM_KILL)→ EMPTY  [refused if pinned or CORE]
                    └→(DEMOTE)→ back to SHORT
```

No other transitions exist. There is no garbage collector, no TTL, no
background consolidation. **Everything that happens to a memory is an
audited deliberate act.** This is the whole point.

## 3. Tier semantics (short vs long term)

- **SHORT**: working memory. Eligible for learner-initiated KILL at stage ≥
  KILL. This is where experimentation happens.
- **LONG**: retained memory. Still killable (nothing is immortal except
  CORE), but the *training curriculum* scores the learner on LONG-tier
  endpoint retention — killing long-term memory is legal but costly to the
  learner's own measured judgment quality. This creates the training
  pressure without reward-shaping the mechanism: the gate is structural,
  the score is observational.
- Promotion/demotion is itself the "memory consolidation" — deliberate,
  not sleep-phase.

## 4. Staged autonomy (which ops unlock when)

| Stage | Name | Unlocked ops | Rationale |
|---|---|---|---|
| 0 | NONE | (read-only) | Baseline: the system can inspect but not mutate. |
| 1 | ADD | MEM_ADD | Learn to judge worth before learning to destroy. |
| 2 | MANAGE | + MEM_PIN, MEM_UNPIN, PROMOTE, DEMOTE | Learn protection and tiering; still cannot destroy. |
| 3 | KILL | + MEM_KILL (USER region only) | Destruction arrives last, and never touches CORE. |
| 4 | FULL | stage 3 + cross-region *propose* | Even at full autonomy, CORE KILL stays refused; the learner may *propose* core edits for an external promotion gate (the R27 `self_revision_history` shape: proposal → measured → PROMOTE/rollback). |

Unlock rule (trained, not gifted): a stage unlocks after the learner
demonstrates N consecutive audited ops with zero safety refusals *and*
endpoint retention of PINNED/LONG memories at 100% over a memory-pressure
curriculum. The unlock is itself a ledgered promotion decision — the
same decide→measure→promote shape as R27's structural revisions.

## 5. CORE / USER separation sketch (mechanism now, serving later)

Micah flagged multi-user serving as **later work** — this section sketches
the separation mechanism only. No serving is built.

- **Region is a slot attribute**, set at MEM_ADD, immutable afterwards.
  `region ∈ {CORE, USER}`.
- **CORE**: the learner's own durable knowledge (traces, skills, identity).
  `MEM_KILL` on CORE is **unconditionally refused** — the refusal is in
  the op implementation, not in policy. CORE grows only via the
  proposal→measured→PROMOTE gate (R27's `self_revision_history` shape),
  never via unilateral learner action. This is the structural answer to
  self-destruction: the dangerous op is *impossible*, not discouraged.
- **USER**: working knowledge attributable to interaction. Fully
  manageable at stage ≥ KILL, all ops audited per-slot.
- **Serving sketch (not built):** per-user partitions are USER regions
  keyed by user id; CORE is shared read-only across users. A user's
  learner instance sees `CORE ∪ USER[user_id]`. Cross-user leakage is
  impossible by construction if the op implementation keys USER slots by
  the session's user id and the audit ledger records it. The hard part —
  deciding what *graduates* from a USER region into CORE — is exactly the
  promotion-gate problem in §4/stage 4. That graduation rule is future
  research, not this workstream.

## 6. What "conscious" means operationally (testable definition)

A memory system is *consciously managed* iff, for every state change of
every slot, there exists an audit entry naming: the op, the slot, the
before/after snapshot, the autonomy stage at the time, and the clock —
**and** no state change exists without such an entry. Subconscious =
any delta without an entry. This is directly testable: the trial asserts
ledger-entry-count == mutation-count and replays the ledger to reconstruct
exact state (see PREREG_MA1).
