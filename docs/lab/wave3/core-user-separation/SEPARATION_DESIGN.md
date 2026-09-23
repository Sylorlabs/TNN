# CORE/USER separation — mechanism design

Agent (wave-3 investigator), 2026-09-19. Micah's requirement: TNN must
partition CORE knowledge from per-user USER knowledge **on its own** —
deliberately, structurally, not by sysadmin config. Serving many users is
LATER; this is mechanism design only. No serving build.

Prior art: `wave2/memoryagency/MEMORY_OPS.md` (§5 sketch: CORE immutable
after ADD; per-user USER partitions keyed by user id, shared read-only
CORE), `MEMORY_SAFETY.md` (4-layer defense; staged autonomy), the MA1/MA2/MA3
native trials (deliberate ops, refusals, audit, replay — 58/58 native).

Program law applied from the start: the promotion rule must be **logic, not
a threshold**; no score tables; no RL reward-shaping; **no RNG anywhere in
the system's decision paths** (deterministic given state); adversity comes
from **designed curricula**, and the verdict must separate "the system is
deterministic" from "the test was adversarial".

## 1. The partition model

A slot is `{live, value, key, owner, pinned, region, tier, step_added}`.

- `region ∈ {CORE, USER}` — set at MEM_ADD, **immutable afterwards** (MA1).
- `owner : i32` — the user id that owns the slot; `0` = system/CORE.
  Set at MEM_ADD, **immutable afterwards** (new: closes the
  demote-to-killable trick in the ownership dimension — a slot can never
  be re-homed to another user or to CORE).
- `key : i32` — the learner-declared content address. Two slots with the
  same `key` make claims about the same fact; same key + same value =
  agreement; same key + different value = **contradiction**. (Integer-native
  stand-in for content; the logic is over key/value equality, never over
  scores.)
- A learner instance operates under a **session user** (`current_user`,
  itself audited state changed only by the audited `SETUSER` op). Every
  mutating op is scoped: it may touch only slots with
  `owner == current_user`, plus the promotion gate's CORE writes. Cross-user
  leakage is impossible by construction, not by policy.

Read precedence (serving-later, fixed now so the mechanism is coherent):
`own USER partition` > `CORE` > never another user's partition. Conflicts
are resolved by **scope**, never by arbitration.

## 2. The promotion rule: logic, not a threshold

The hard question: who decides what belongs in CORE, and what does the
system have to *earn*? Answer: **the learner proposes; a deterministic gate
verifies.** Promotion to CORE is the op `PROMOTECORE(candidate, witness)`
and it succeeds iff ALL of the following hold (equalities and quantifiers
over store state — no tunable cutoff anywhere):

1. **Stage.** Session stage ≥ FULL(4). (Staged autonomy: CORE graduation is
   the last unlock, earned per MEMORY_SAFETY layer 2.)
2. **Candidate standing.** `live(c) ∧ region(c)=USER ∧ tier(c)=LONG ∧
   owner(c)=current_user`. The learner must already have deliberately
   consolidated the memory to LONG tier — the first, learner-side gate
   precedes the CORE gate. You cannot promote working memory straight to
   CORE.
3. **Corroboration (the witness).** There exists a *named* witness slot `w`
   with `live(w) ∧ region(w)=USER ∧ owner(w)≠owner(c) ∧ key(w)=key(c) ∧
   value(w)=value(c)`. Two **disjoint** attestations agree. The owner-
   inequality is the anti-sybil logic: a user cannot corroborate itself.
   The number "two" is not a tuned quorum — it is the *meaning* of
   independent corroboration (one claim, one independent check). A third,
   fourth attestation adds nothing to the logic.
4. **No contradiction anywhere.** `¬∃ live slot x: key(x)=key(c) ∧
   value(x)≠value(c)` — scanned over CORE *and* every USER partition.
   A disputed fact cannot enter CORE, period.

Why this is logic and not a threshold: every clause is a checkable
predicate (equality, inequality, existential/universal quantification over
a bounded store). There is no scalar, no cutoff, no confidence, no
"score ≥ 80". If any clause fails, the op refuses with a *named* code
(`REFUSED_NOTLONG`, `REFUSED_UNCORROBORATED`, `REFUSED_CONTRADICTED`,
`REFUSED_SCOPE`, `REFUSED_STAGE`) and the refusal is audited — the gate
holds *visibly*.

The shape is R27's `self_revision_history`: **diagnosis → proposal →
measured → PROMOTE/rollback**. The learner diagnoses ("this looks
core-worthy"), proposes (the op call, audited), the gate measures
(re-executes the four clauses), and decides PROMOTE (gate writes CORE) or
refusal (rollback-equivalent: nothing happens, refusal audited).

**Second witness form (specified, not trialed):** a self-verified trace.
Per `brain/STATE_SCHEMA.md` §5, the white-box learning atom is a Trace —
symbolic opcodes over a cue with `provenance: SELF_VERIFIED`. A memory
whose content is a trace carries its own proof: the gate re-executes the
trace and checks `replay == recorded result`. That is equality-logic, same
as cross-user attestation, and it lets single-user knowledge earn CORE
without a second user. The trial below implements cross-user attestation;
trace-replay witnessing is the named next mechanism.

**What single-user deployments get:** with one user id, clause 3 can never
hold (no disjoint owner exists). CORE then holds only system-seeded
knowledge and never grows. That is the *principled* answer, not a
limitation: uncorroborated idiosyncratic knowledge has not earned CORE.

## 3. Contamination prevention: structural, like REFUSED_CORE

USER knowledge can never contaminate CORE because there is **no unilateral
write path to CORE**:

- `MEM_ADD(..., region=CORE, ...)` → `REFUSED_COREWRITE` (109... — codes
  below), audited. The learner *can* express the attempt (so the refusal is
  visible in the audit), but the op implementation refuses in its first
  lines. Same structural position as MA1's `REFUSED_CORE` on KILL.
- `region` and `owner` are immutable after ADD — no re-homing a USER slot
  into CORE, no stealing another user's slot.
- The **only** op that creates a CORE slot is the gate's internal
  `COREWRITE`, which exists *only* as the second half of a successful
  `PROMOTECORE`. It is not learner-callable.
- **CORE purity invariant** (ledger-checkable): every audit entry whose
  after-state has `region=CORE` has `op=COREWRITE`, and every COREWRITE
  immediately follows a `PROMOTECORE`-OK entry naming the same candidate.
  The trial asserts this by scanning the full ledger.
- `PIN`/`PROMOTE`(tier)/`DEMOTE` on a CORE slot → `REFUSED_CORE`: CORE has
  no tiers and needs no pinning (it is already unkillable); the audit stays
  honest about the no-op attempt. (MA1 refused PIN-on-CORE as redundant;
  this design additionally refuses tier moves on CORE — tiering is a
  USER-partition concept.)
- `MEM_KILL` on CORE → `REFUSED_CORE` at every stage, for every user,
  **including the user whose knowledge was promoted** (MA1-proven, re-
  asserted in the trial).

Result: the dangerous writes are *impossible*, not discouraged
(MEMORY_SAFETY layer 1). Training teaches judgment in USER space; the
architecture guarantees CORE survival.

## 4. Where conflicts live

When user A holds `(k, 1)` and user B holds `(k, 2)`:

1. **Both slots coexist** in their own USER partitions. Nothing is
   silently dropped, merged, or averaged — there is no arbitration function
   to be gamed.
2. The conflict **blocks CORE promotion** for key `k` (clause 4 fails →
   `REFUSED_CONTRADICTED`, naming the contradicting slot in the audit).
   CORE never contains contested claims.
3. The conflict is **recorded**: the refused promotion entry names
   candidate, witness-attempt, and the contradicting slot. The conflict is
   a first-class audited object.
4. **Resolution is deliberate and owned:** only the contradicting slot's
   owner can remove it (deliberate `MEM_KILL` on own partition, audited —
   the forget path, §5), after which promotion becomes eligible. The system
   never resolves a conflict unilaterally. A future verified
   contradiction-resolution op (both sides' supporting traces re-executed,
   the one that replays wins) is specified in §7 as next work; it is not
   needed for the base mechanism.

Read-side: A reads `(k,1)` (own partition wins by scope); B reads `(k,2)`;
a user with no `(k,·)` reads CORE's `(k,v)` if present. Deterministic,
no judgment involved.

## 5. Forget semantics

| Request | Mechanism | Result |
|---|---|---|
| User asks to forget own USER memory | Learner `MEM_KILL`s own slot (stage ≥ KILL) | OK, audited, exact. Forgetting is deliberate, like all destruction. |
| User asks to forget another user's memory | `MEM_KILL` on `owner≠current_user` | `REFUSED_SCOPE` — ownership is structural. |
| User asks to forget CORE knowledge — even knowledge that originated from them | `MEM_KILL` on CORE | `REFUSED_CORE`, always. **The right to be forgotten ends at the CORE boundary.** CORE is the system's durable knowledge; a user's request cannot unilaterally destroy it. |
| Forgetting a USER copy of a promoted fact | KILL own USER slot | OK — the CORE copy persists (it was corroborated; it no longer belongs to one user). |

CORE retraction (system-level, not user-level) goes through the same gate
shape: a *revision proposal* — corroborated new fact naming a superseded
slot; the gate verifies and marks the old CORE slot **superseded**
(audited; history is never rewritten). Specified in §7, trialed next.

## 6. Audit, replay, and the checkable invariants

The ledger is extended for separation (16 words/entry):
`op, slot, aux, rc, b1..b5, a1..a5, stage, user`
where the 5 snapshot words cover `live|pinned|tier|region`, `value`,
`step`, `key`, `owner`; `aux` = witness (PROMOTECORE) or candidate
(COREWRITE); `user` = session user at op time.

Machine-checked invariants (all asserted natively in the trial):

- **I1 — refusals never mutate:** every refused entry has before==after
  on all 5 snapshot words.
- **I2 — ledger replay:** replaying from genesis reconstructs exact live
  state (all fields, stage, session user, entry count). The testable
  definition of "conscious" (MEMORY_OPS §6), extended to owners/keys.
- **I3 — CORE purity:** after-region=CORE ⟹ op=COREWRITE; every COREWRITE
  follows a PROMOTECORE-OK naming the same candidate. (The structural
  no-contamination proof, as a ledger property.)
- **I4 — cross-user isolation:** every OK mutating entry touched only
  slots with `owner == entry.user` (before- or after-owner), except
  COREWRITE (owner 0, gate-only) and session ops (SETSTAGE/SETUSER).
- **I5 — determinism:** the system contains no RNG in any decision path;
  two runs of the trial binary produce byte-identical output. (Program law
  2; "the system is deterministic" is checked separately from "the test
  was adversarial".)

## 7. Scale argument (program law 1) and next scale test

The mechanism is designed to scale; the trial is small-scale. The scaling
claims, each with the reason it holds:

- **More slots (10x/100x).** Per-op costs: ADD/KILL/PIN are O(CAP) worst-
  case (first-empty scan) on a bounded CAP; PROMOTECORE's contradiction
  scan is O(CAP). At 100x slots the scan is still a rare-gate cost, but the
  *designed* path is an **audited key-index**: `key → slot list`, where
  index entries are ledgered state maintained by the ops themselves (an
  index entry exists iff the slot does — checkable by replay). Then
  corroboration/contradiction checks are O(1) index lookups. The index is
  not built in this trial; the trial's linear scan is the correct base
  that the index must reproduce exactly.
- **More partitions (10x/100x users).** `owner` is an opaque i32; no op
  iterates users; I4 is per-entry. Partition count changes no machinery.
- **Longer horizons.** No TTL, no decay, no time-dependent logic except the
  monotonic clock. Horizon-independence is structural (the anti-RL clause:
  nothing fades unless deliberately killed).
- **The promotion rule is scale-free.** "Two disjoint attestations agree
  ∧ no contradiction" has no quorum parameter to retune at scale — this is
  exactly what "logic, not a threshold" buys.

**Next scale test (specified, not run):** same protocol at CAP=4096 with
100 user partitions and the audited key-index; assert identical verdicts,
per-op probe counts ≤ O(index depth), and a 100k-op soak ending in an exact
replay check (I2) with the fail-closed ledger refusal exercised.

## 8. Open items (honest negatives / next work)

- **N1 — trace-replay witness:** specified (§2), not implemented. Native
  proof needed: a Trace whose ops re-execute to the recorded result
  promotes without a second user.
- **N2 — supersession/revision gate:** specified (§4–§5), not implemented.
  Without it, CORE is append-only per key (first corroborated fact wins
  the key). The trial asserts the base refusal; the revision gate is the
  follow-up trial.
- **N3 — key-index at scale:** specified (§7), not built.
- **N4 — stage-FULL unlock curriculum:** the unlock rule is inherited from
  MEMORY_SAFETY layer 2 (ledgered, zero-refusal candidacy + retention
  endpoints); the MA2-style native unlock trial for stage 4 is not run
  here.
- **N5 — multi-learner concurrency:** one learner instance with a session
  user is trialed; true concurrent learners sharing a store need a
  serialization discipline (append-only ledger already serializes; session
  scoping is per-op). Serving is out of scope per the brief.

## 9. Op and result-code reference (trial implementation)

Stages: `NONE(0) < ADD(1) < MANAGE(2) < KILL(3) < FULL(4)`.

Ops: `ADD(1) KILL(2) PIN(3) UNPIN(4) PROMOTE(5) DEMOTE(6) ROLLBACK(7)
SETSTAGE(8) PROMOTECORE(9) COREWRITE(10) SETUSER(11)`.

Result codes: `OK(0)`, `REFUSED_CORE(101)`, `REFUSED_PINNED(102)`,
`REFUSED_NOTLIVE(103)`, `REFUSED_FULL(104)`, `REFUSED_STAGE(105)`,
`REFUSED_BADSLOT(106)`, `REFUSED_AUDITFULL(107)`, `REFUSED_NOROLLBACK(108)`,
`REFUSED_COREWRITE(109)`, `REFUSED_SCOPE(110)`,
`REFUSED_UNCORROBORATED(111)`, `REFUSED_CONTRADICTED(112)`,
`REFUSED_NOTLONG(113)`; caller bugs `cl_bad()=2001` (bad slot index,
null store, illegal enum — never audited).

Refusal precedence inside an op (documented, trialed): stage → liveness →
region/owner structural checks → operation-specific verification. E.g.
`ma_add`: `REFUSED_STAGE` < `REFUSED_FULL` < `REFUSED_COREWRITE` <
`REFUSED_SCOPE`. `ma_promotecore`: `REFUSED_STAGE` < `REFUSED_NOTLIVE` <
`REFUSED_SCOPE`(candidate not own) < `REFUSED_NOTLONG` <
`REFUSED_UNCORROBORATED` < `REFUSED_CONTRADICTED`.
