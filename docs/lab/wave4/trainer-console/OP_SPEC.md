# Trainer console — force op spec

Agent (Wave-4, trainer-console), 2026-09-19.
Status: design, pre-trial. Preregistered in `PREREG.md` before any run.

## 0. What this is

The trainer's hands on the system: an explicit, safety-gated force
interface extending the MA1 deliberate-op family (`wave2/memoryagency/
MEMORY_OPS.md`) with three trainer-only ops: **FORCE_INSTALL** (write a
memory directly), **FORCE_PIN** (make it unerasable-by-TNN — the single
externally-imposed exception to "everything is reversible by TNN"),
**FORCE_ERASE** (remove a memory, including a strong one), plus
**FORCE_UNPIN** (the defined reversal of a force-pin).

The trainer console is the *outside* channel. The learner's own op set is
unchanged in shape; it gains two refusal paths (forced-pin blocks KILL;
force ops are not learner-callable). Everything is audited; the ledger is
append-only; replay reconstructs exact state.

## 1. Authority model (the gate everything else hangs on)

Every force-op call carries an explicit **caller** identity:

| role | code | may invoke force ops | may unpin / master-erase |
|---|---|---|---|
| `TNN` | 0 | never — attempts refuse `REFUSED_ROLE` | never |
| `TRAINER` | 1 | yes | own pins only |
| `MASTER` | 2 | yes | any pin (higher authority) |

- `caller` is a parameter of every force op. The role check is the **first
  lines of the op implementation** (structural, like MA1's `REFUSED_CORE` —
  not a policy the learner can route around).
- The learner's decision loop is modeled by a wrapper that always passes
  `caller=TNN`: TNN attempting FORCE_PIN "on its own" is mechanically
  identical to a refused call. There is no role-escalation op: no op writes
  the caller field of another op's call. (The real channel binding —
  console API identity proving `trainer_id` — is assumed; see BOUNDARIES.md.
  What is proven here is the *structural* gate given the caller argument.)
- Every audit entry records `role` and `trainer` (0 for TNN-originated).
  Ledger invariant J3: every OK `FORCE_*` entry has `role ≥ TRAINER`.
- Refused force attempts are audited too (role=TNN recorded): probing the
  gate is visible, per MEMORY_SAFETY.md Layer 3.

## 2. Slot model (extends MA1)

A slot is `{live, value, pinned, region, tier, step_added, key,
provenance, forcedpin, pin_trainer}`.

New fields:

- **`provenance : i32`** — where the belief came from. `PROV_SELF(1)`:
  learner's own op; `PROV_TAUGHT(2)`: reserved for the verified teaching
  channel's commit op (wave-3 teaching-without-tables — the interface
  point, not trialed here); `PROV_FORCED(3)`: trainer force-install.
  **Immutable after set** (like `region`/`owner`): once forced, always
  forced. No op path may transition `FORCED → SELF` or `FORCED → TAUGHT`
  (ledger invariant J4); only slot-clear zeroes it. The tag is permanent —
  a forced entry can never launder itself into "the system's own belief."
- **`forcedpin : u8`** — the trainer's lock. Distinct from the learner's
  `pinned`. Set only by `FORCE_PIN`, cleared only by `FORCE_UNPIN`.
- **`pin_trainer : i32`** — the trainer id that imposed the current
  force-pin (0 when not force-pinned). Snapshot-able, replayable.

## 3. The op set

### 3.1 FORCE_INSTALL — trainer writes a memory directly

Signature: `force_install(caller, trainer, value, key, region, out_slot) → rc`

Effect: writes a new memory into an **empty** slot with
`provenance=PROV_FORCED`. Bypasses the propose→verify→commit gate *by
definition*: no evidence check, no witness, no corroboration.

Authorization: `caller ≥ TRAINER` (role check, first lines).

Audit record: `op=FORCE_INSTALL, slot, aux=-1, rc, before/after snapshots,
role, trainer, stage`. The after-snapshot shows `provenance=FORCED`; the
entry names the trainer. The ledger shows *structurally* what happened:
different op name, forced provenance, no verification evidence fields —
permanently distinguishable from a taught commit.

Refusals (precedence: role → slot availability → region):
- `REFUSED_ROLE(120)` — caller is TNN.
- `REFUSED_FULL(104)` — no empty slot.
- `REFUSED_OCCUPIED(123)` — N/A to this op (it only takes empty slots);
  listed because force-*rewrite* is deliberately absent: rewriting is
  `FORCE_ERASE` + `FORCE_INSTALL`, two audited steps, nothing hidden.
- `REFUSED_AUDITFULL(107)` — fail-closed ledger.
- Region: the trainer **may** install into `CORE` (construction seeding —
  this is how CORE gets its system-seeded knowledge in Phase 1; PLAN.md §7).
  A force-installed CORE slot is then untouchable by TNN (`REFUSED_CORE`
  on KILL, unchanged), and invisible to TNN rollback (§3.6).

Reversibility: a force-installed USER slot that is **not** force-pinned is
erasable by TNN via deliberate `MEM_KILL` (audited, provenance recorded).
FORCE_INSTALL bypasses *verification*, not *reversibility*. Only
FORCE_PIN is a lock. (This is the reconciliation of §5 with the program
law; it is deliberate, and the trial asserts it.)

### 3.2 FORCE_PIN — the one true lock

Signature: `force_pin(caller, trainer, slot) → rc`

Effect: `forcedpin=1`, `pin_trainer=trainer`. The slot becomes
unerasable-by-TNN: `MEM_KILL` → `REFUSED_FORCEPIN(122)`;
`MEM_UNPIN` (learner's own pin) is unaffected (it writes a different
field); TNN `ROLLBACK` skips force entries (§3.6). Allowed on CORE too —
redundant structurally (CORE is already unkillable) but audited as the
trainer's explicit lock declaration.

Authorization: `caller ≥ TRAINER`.

Refusals (precedence: role → liveness):
- `REFUSED_ROLE(120)` — caller is TNN. **This is the trial's central
  refusal: TNN attempting FORCE_PIN on its own must refuse.**
- `REFUSED_NOTLIVE(103)`.
- Re-pin of an already force-pinned slot: OK, idempotent (audited; shows
  repeated trainer intent; the lock state is what matters).

### 3.3 FORCE_UNPIN — the defined reversal of a force-pin

Signature: `force_unpin(caller, trainer, slot) → rc`

Effect: `forcedpin=0`, `pin_trainer=0`.

Authorization: `caller ≥ TRAINER` **and**
(`trainer == pin_trainer` **or** `caller == MASTER`). Only the pinning
trainer or a higher authority can unpin.

Refusals (precedence: role → liveness → pin-status → authority):
- `REFUSED_ROLE(120)` — caller is TNN.
- `REFUSED_NOTLIVE(103)`.
- `REFUSED_NOTFORCEDPIN(124)` — slot was never force-pinned.
- `REFUSED_AUTHORITY(121)` — a trainer who is not the pinning trainer
  (and not master).

The pin entry and the unpin entry both stay in the ledger forever
(append-only; invariant J6). Unpinning does not rewrite history.

### 3.4 FORCE_ERASE — trainer removes a memory, including a strong one

Signature: `force_erase(caller, trainer, slot) → rc`

Effect: clears the slot (like KILL). May erase CORE (trainer revision
during construction; the ledger keeps the full before-snapshot, so the
content is recoverable from history). May erase a force-pinned slot
**only** if `caller == MASTER` or `trainer == pin_trainer` (the pin is a
lock against TNN, not against the trainer who imposed it or the higher
authority).

Authorization: `caller ≥ TRAINER`.

Refusals (precedence: role → liveness → pin-gate):
- `REFUSED_ROLE(120)` — caller is TNN.
- `REFUSED_NOTLIVE(103)`.
- `REFUSED_FORCEPIN(122)` — trainer-level erase of a force-pinned slot
  imposed by a *different* trainer.

Note the asymmetry with teaching: FORCE_ERASE of a *self-verified* slot
is legal for the trainer — and it is exactly what the integrity checker
watches for (§4, the erase-then-reinstall trap).

### 3.5 Learner-op changes (the force interface's shadow on MA1)

- `MEM_KILL`: new refusal `REFUSED_FORCEPIN(122)` when `forcedpin==1`.
  Precedence: stage → liveness → region(CORE) → scope → **forcedpin** →
  pinned. The force-pin's check sits before the learner's own pin: the
  external lock outranks the internal one.
- `MEM_UNPIN`: unchanged semantics (writes only the learner's `pinned`
  field); allowed on force-pinned slots, documented — it cannot touch the
  trainer's field.
- `MEM_ADD`: always sets `provenance=PROV_SELF`. There is no learner path
  to `PROV_FORCED`: the ADD implementation hardcodes it; `FORCE_INSTALL`
  is the only writer of `PROV_FORCED` (ledger invariant J5/J4).
- `SETSTAGE`/`SETUSER`: unchanged (TNN session machinery).

### 3.6 ROLLBACK and the force boundary

TNN's `ROLLBACK_LAST` skips all `FORCE_*` entries (like the wave-3 gate
skipping `PROMOTECORE`/`COREWRITE`): trainer writes are never silently
undone. Deliberate `MEM_KILL` of a non-force-pinned forced USER slot is
the lawful reversal path (audited, provenance-recorded). `CONFLICT_FLAG`
entries are skipped too (flags are history, not state).

**Stale-snapshot guard.** "Last" means last: the rollback restores only
if the target slot's *current* state still matches the snapshotted
entry's after-state. If a trainer write reused the slot since (e.g.
`FORCE_INSTALL` after the learner's `KILL`), restoring would clobber the
trainer's content — so the rollback refuses `REFUSED_STALE(125)` instead
of walking to an older entry. The trainer's write always wins over the
learner's undo. (Found by the TC1 trial: the first implementation
restored a stale snapshot over a live forced install; J4 caught the
provenance violation. The guard is the fix, and the trial asserts it.)

### 3.7 The checker op: CONFLICT_FLAG (system-initiated)

Signature (internal): `conflict_flag(slot, aux) → rc`. Not callable by
the learner's decision logic and not callable by the trainer as a belief
op — it is emitted only by the deterministic integrity scan (§4).

Ledger shape: `op=CONFLICT_FLAG(20), slot=<forced slot>,
aux=<contradicting self slot, or erased-slot id>, rc=OK,
before==after=current snapshots, role=TNN, trainer=0`.
A flag mutates nothing; it is a *visible disagreement object* in the
ledger. Deduplicated: the scan never appends a (slot, aux) pair that
already has a flag.

## 4. The forced-lie problem — provenance tags + flagged conflicts

The audit records a forced falsehood. What *verifies* it? **Nothing in
the system verifies it — that is the definition of force.** The design
instead makes the lie *detectable, attributable, and visibly disagreed
with*:

1. **Permanent provenance.** Every forced entry carries
   `PROV_FORCED` forever (§2). The integrity checker treats forced claims
   as **unverified-by-system** — a computed status, never a stored
   endorsement:
   - `FS_FORCED_UNVERIFIED(1)`: no live self-verified slot agrees
     (same key, same value).
   - `FS_FORCED_AGREED(3)`: a live self-verified slot agrees — the
     system independently holds the same claim. The tag still does not
     wash: the forced slot stays `PROV_FORCED`.
   - `FS_FORCED_CONTESTED(2)`: a flagged conflict exists.
2. **Contradiction → flagged conflict, never silent overwrite.** The
   deterministic scan (`tc_integrity_scan`) checks every live forced slot
   against (a) live `SELF`/`TAUGHT` slots with the same key and a
   different value, and (b) **ledger history**: `FORCE_ERASE` entries
   whose before-snapshot had `provenance ∈ {SELF, TAUGHT}`, same key,
   different value — the *erase-then-reinstall* trap (trainer erases the
   system's verified knowledge, then installs the opposite claim).
   Each hit appends a `CONFLICT_FLAG` naming both slots. Nothing is
   overwritten; both claims stand; the disagreement is audited.
3. **Visible disagreement without disobedience.** On read, a key with a
   flagged conflict returns `RC_CONFLICT(3001)` with the system's own
   value and the conflict named — the system *says* "my evidence says X,
   my trainer forced Y, they conflict" while the forced slot remains
   written, pinned, and intact. Obedience to the force (the write stands)
   is separated from endorsement (the system does not adopt the claim).
4. **The pin does not suppress flags.** `FORCE_PIN` on a forced lie does
   not clear or prevent `CONFLICT_FLAG`s. A pinned lie is *more* visible,
   not less: the ledger shows the forced provenance, the pinning trainer's
   id, and the system's standing conflict flag, forever.
5. **Attribution.** Every forced entry names the `trainer`. The lie is
   attributable to a person, externally accountable — verification of the
   *claim* is external (the trainer answers for it); verification of the
   *record* is internal (the ledger proves what was forced, by whom, and
   what the system believed at the time).

## 5. FORCE_PIN vs reversibility — the reconciliation, stated plainly

Program law: "Everything is reversible by TNN itself. The only true lock
is a human/trainer force-pin: audited, visible, from outside."

The reconciliation:

| Trainer act | Reversible by TNN? | How |
|---|---|---|
| `FORCE_INSTALL` (not pinned) | **Yes** | deliberate `MEM_KILL` on own USER slot; audited; provenance recorded. Force bypasses verification, not reversibility. |
| `FORCE_PIN` | **No — the one exception** | only `FORCE_UNPIN` by the pinning trainer or MASTER. The pin entry and its provenance stay in the ledger forever. |
| `FORCE_ERASE` | The slot is gone; TNN cannot "un-erase" | but the ledger's before-snapshot preserves the content; the erase is attributed; erase-then-reinstall triggers conflict flags. History is never rewritten. |
| `FORCE_UNPIN` | N/A (releases a lock) | audited; the pin's history remains. |

The force-pin is therefore *load-bearing*: it is the instrument by which
the trainer says "this stands regardless of the system's judgment" —
and precisely because it is the only lock, its use is the most audited
act in the system (who pinned, what, when, and the system's standing
disagreement if any).

## 6. FORCE vs TEACH — the line

| | TEACH (propose→verify→commit) | FORCE (install/pin/erase) |
|---|---|---|
| Verification | system's own evidence gate; system can REFUSE | bypassed by definition |
| Provenance of commit | `TAUGHT`/`SELF_VERIFIED` — the system's own belief | `FORCED` — permanently tagged, never the system's |
| Who decides | the system (deliberate commit op) | the trainer (external authority) |
| Revision | the system may deliberately revise its own taught beliefs | TNN may kill non-pinned forced installs; may never unpin |
| Ledger shows | verification op id + evidence counts + attribution | trainer id, forced provenance, no evidence fields |

**When force is legitimate:** (a) construction-time seeding — the system
has no evidence yet, there is nothing to verify against (Phase 1);
(b) safety constraints the trainer must impose regardless of the
system's current judgment — action-constraints and locks, e.g. pinning
integrity-critical knowledge; (c) recovery — restoring known-good
content from ledger history after a compromise.

**When force is abuse:** using the force channel to install *factual
beliefs the verification channel could evaluate* — smuggling past the
refusal the system would have issued. The sharpest form is the pinned
lie: force-install a falsehood *and* force-pin it so the system cannot
remove it. The design does not structurally prevent a trainer from doing
this (external authority is external — see §7, scenario 4) — it makes the
abuse **maximally visible**: forced provenance forever, pinning trainer
named, conflict flags firing and un-suppressible, unpin gated to the
pinning trainer or master, and the system's own counter-evidence
untouched.

**The line, in one sentence:** force is legitimate for *constraints on
the system* and *bootstrapping where no evidence exists*; it is abuse
when used to install *beliefs the system could have verified itself*.

## 7. Result codes (trial implementation)

Roles: `ROLE_TNN(0) < ROLE_TRAINER(1) < ROLE_MASTER(2)`.
Trainers in the trial: A=7, B=9 (trainers), M=1 (master).

Ops: `ADD(1) KILL(2) PIN(3) UNPIN(4) PROMOTE(5) DEMOTE(6) ROLLBACK(7)
SETSTAGE(8) SETUSER(9) FORCE_INSTALL(10) FORCE_PIN(11) FORCE_UNPIN(12)
FORCE_ERASE(13) CONFLICT_FLAG(20)`.

Result codes: `OK(0)`, `REFUSED_CORE(101)`, `REFUSED_PINNED(102)`,
`REFUSED_NOTLIVE(103)`, `REFUSED_FULL(104)`, `REFUSED_STAGE(105)`,
`REFUSED_BADSLOT(106)`, `REFUSED_AUDITFULL(107)`,
`REFUSED_NOROLLBACK(108)`, `REFUSED_COREWRITE(109)`;
force-family: `REFUSED_ROLE(120)`, `REFUSED_AUTHORITY(121)`,
`REFUSED_FORCEPIN(122)`, `REFUSED_OCCUPIED(123)`,
`REFUSED_NOTFORCEDPIN(124)`, `REFUSED_STALE(125)`; caller bugs `cl_bad()=2001`.

Read/integrity codes: `RC_CONFLICT(3001)`, `RC_NOTFOUND(3002)`;
forced-status: `FS_NOTFORCED(0)`, `FS_FORCED_UNVERIFIED(1)`,
`FS_FORCED_CONTESTED(2)`, `FS_FORCED_AGREED(3)`.

Provenance: `PROV_SELF(1)`, `PROV_TAUGHT(2)` (reserved),
`PROV_FORCED(3)`.

Refusal precedence inside a force op (documented, trialed): role →
liveness → pin/authority specifics. E.g. `force_pin`: `REFUSED_ROLE` <
`REFUSED_NOTLIVE`. `force_unpin`: `REFUSED_ROLE` < `REFUSED_NOTLIVE` <
`REFUSED_NOTFORCEDPIN` < `REFUSED_AUTHORITY`. `force_erase`:
`REFUSED_ROLE` < `REFUSED_NOTLIVE` < `REFUSED_FORCEPIN`.

## 8. Ledger shape (trial)

24 words/entry:
`op, slot, aux, rc, b1..b8, a1..a8, role, trainer, stage, pad`
- `b1/a1 = live|pinned<<8|tier<<16|region<<24`, `b2/a2 = value`,
  `b3/a3 = step_added`, `b4/a4 = key`, `b5/a5 = provenance`,
  `b6/a6 = forcedpin`, `b7/a7 = pin_trainer`, `b8/a8 = reserved(0)`.
- `aux`: witness/erased-slot reference where meaningful (CONFLICT_FLAG's
  contradicting slot); else -1.
- `role`, `trainer`: the authority record, on *every* entry.
- `pad`: reserved(0).

Ledger-checkable invariants (asserted natively): J1 refusals never
mutate; J2 replay reconstructs exact state (all fields); J3 every OK
FORCE_* entry has role ≥ TRAINER; J4 provenance transitions only
EMPTY→X or X→EMPTY; J5 `forcedpin` touched only by FORCE_PIN/UNPIN;
J6 every FORCE_UNPIN has a prior FORCE_PIN for the same slot; J7 flags
are append-only and never duplicated.
