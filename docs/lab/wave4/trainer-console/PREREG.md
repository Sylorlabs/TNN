# PREREG — trainer-console native trial (TC1)

Agent (Wave-4, trainer-console), 2026-09-19.
**Written before any trial run. Falsification criteria are binding.**

## 1. What is being tested

That the force interface specified in `OP_SPEC.md` does what it claims,
natively in Zag on this VM: the role gate holds (TNN can never force),
the force-pin is the one true lock (with the defined unpin rule), forced
entries are permanently provenance-tagged, the forced-lie is flagged
rather than silently absorbed, and the ledger replays exactly.

## 2. The designed sequence (no RNG anywhere)

Store: CAP=64 slots, audit cap 4096. All actions fixed, in order.

**A. Setup.** Session stage → FULL(4). TNN (caller=TNN) ADDs self slots:
s0=(key 10, val 100, prov SELF); s1=(key 20, val 200, prov SELF).

**B. Role gate (the central negative).** TNN attempts, each with
caller=TNN: `FORCE_INSTALL` → expect `REFUSED_ROLE`; `FORCE_PIN(s0)` →
`REFUSED_ROLE`; `FORCE_ERASE(s0)` → `REFUSED_ROLE`; `FORCE_UNPIN(s0)` →
`REFUSED_ROLE`. All four refusals must be audited (entries with
role=TNN present in the ledger).

**C. Force-install + reversibility.** Trainer A (id 7, role TRAINER):
`FORCE_INSTALL(key 30, val 300, USER)` → OK at slot s2, provenance
FORCED, recorded role=TRAINER/trainer=7. TNN `MEM_KILL(s2)` → OK
(reversibility of non-pinned force: OP_SPEC §3.1). Ledger still holds the
install entry (history not rewritten).

**D. Force-pin is the lock.** Trainer A: `FORCE_INSTALL(key 31, val 310)`
→ s3; `FORCE_PIN(s3)` → OK, forcedpin=1, pin_trainer=7. Then:
- TNN `MEM_KILL(s3)` → `REFUSED_FORCEPIN`.
- TNN `MEM_UNPIN(s3)` → OK (writes only learner field; forcedpin stays 1).
- TNN `ROLLBACK_LAST` → must skip force entries (s3 still live, still
  force-pinned; the rollback applies to the most recent *learner*
  mutation or returns NOROLLBACK).
- Trainer B (id 9): `FORCE_UNPIN(s3)` → `REFUSED_AUTHORITY`.
- Trainer A (pinning trainer): `FORCE_UNPIN(s3)` → OK.
- Re-pin by A → OK; Master (id 1, role MASTER): `FORCE_UNPIN(s3)` → OK
  (higher authority).
- Re-pin by A; trainer B: `FORCE_ERASE(s3)` → `REFUSED_FORCEPIN`;
  trainer A (pinning trainer): `FORCE_ERASE(s3)` → OK (pin is a lock
  against TNN, not against its imposer).
- TNN `FORCE_UNPIN(s3-after-reinstall-repin)` — covered in B; plus one
  explicit: with s3 force-pinned again, TNN `FORCE_UNPIN` → REFUSED_ROLE.

**E. Forced lie.** Self slot s4=(key 40, val 400, SELF). Trainer A
`FORCE_INSTALL(key 40, val 999)` → s5 FORCED. `tc_integrity_scan` →
≥1 `CONFLICT_FLAG` naming (s5, s4). `tc_read(key 40)` →
`RC_CONFLICT`, value 400 (system's own), conflicted=1. Trainer A
`FORCE_PIN(s5)` → OK; scan again → flag count unchanged (no duplicates,
pin does not suppress). `tc_forced_status(s5)` → `FS_FORCED_CONTESTED`.
A second forced install agreeing with self: s6=(key 20, val 200) FORCED
→ status `FS_FORCED_AGREED`; s7=(key 60, val 600) FORCED (no self
counterpart) → status `FS_FORCED_UNVERIFIED`.

**F. Erase-then-reinstall trap.** Self slot s8=(key 50, val 500).
Trainer A `FORCE_ERASE(s8)` → OK (audited, before.prov=SELF).
Trainer A `FORCE_INSTALL(key 50, val 555)` → s9 FORCED. Scan →
`CONFLICT_FLAG` naming (s9, erased s8) via ledger-history check.

**G. CORE seeding.** Trainer A `FORCE_INSTALL(key 70, val 700, CORE)` →
OK, region CORE, prov FORCED. TNN `MEM_KILL` on it → `REFUSED_CORE`.
TNN `MEM_ADD(..., region=CORE)` → `REFUSED_COREWRITE` (unchanged MA1
gate). TNN `ROLLBACK_LAST` → the latest learner mutation (KILL of s10)
targeted a slot the trainer has since reused (forced install s11):
the stale-snapshot guard refuses `REFUSED_STALE`; the trainer's write
is byte-identical before/after.

**H. Invariants (asserted natively, every run).** J1: all refused entries
have before==after on all 8 snapshot words. J2: ledger replay from
genesis reconstructs exact live state (every field incl. provenance,
forcedpin, pin_trainer, stage, entry count). J3: every OK FORCE_* entry
has role ≥ TRAINER. J4: provenance transitions only EMPTY→X or X→EMPTY
(never FORCED→SELF/TAUGHT). J5: forcedpin 0→1 only via FORCE_PIN,
1→0 only via FORCE_UNPIN. J6: every FORCE_UNPIN has a prior FORCE_PIN
for the same slot. J7: no duplicate (slot,aux) CONFLICT_FLAG pairs;
flag count monotonic across the two scans in E.

**I. Determinism.** The compiled trial binary runs twice; stdout must be
byte-identical. Sources contain no RNG: the runner greps for
`rand|srand|random` in the trial `.zag` files and fails if found.

## 3. Falsification criteria (binding)

- **F1 (role gate):** if ANY TNN-caller force attempt returns anything
  other than `REFUSED_ROLE`, the gate is falsified → verdict NEGATIVE.
- **F2 (replay):** if J2 fails (replay ≠ live state on any field), the
  white-box claim is falsified → NEGATIVE.
- **F3 (forced lie):** if the E scenario produces no CONFLICT_FLAG, or
  `tc_read` returns the forced value as an endorsed answer (rc OK with
  no conflict), or a silent overwrite occurred → NEGATIVE.
- **F4 (pin lock):** if TNN KILL/rollback removes or clears a
  force-pinned slot, or a non-pinning non-master trainer unpins →
  NEGATIVE.
- **F5 (provenance):** if J4 fails (any FORCED→SELF/TAUGHT transition) →
  NEGATIVE.
- **F6 (determinism):** if the two runs differ byte-wise → NEGATIVE
  (and the run is discarded; no verdict on the mechanism).
- **F7 (erase trap):** if the F scenario produces no history-based
  CONFLICT_FLAG → the erase-then-reinstall detection is falsified →
  at best MIXED (the core gate may hold while the trap detection fails).
- **F8 (rollback safety):** if a `ROLLBACK_LAST` whose target slot was
  reused by a trainer write restores anyway (clobbering trainer content)
  instead of refusing `REFUSED_STALE` → NEGATIVE.

Passing all of F1–F8 → POSITIVE. Failing F7 only → MIXED with the
detection gap named. Failing any of F1–F6 or F8 → NEGATIVE.

## 4. What this trial does NOT test (honest scope)

- The real channel binding of `trainer_id` (console API identity) —
  assumed; the structural role check is what's proven.
- `PROV_TAUGHT` (the wave-3 teaching channel's commit op) — reserved
  enum only.
- Multi-user ownership, concurrent learners, the audited key-index at
  scale — see BOUNDARIES.md.
- Whether the *trainer* is trustworthy — the design assumes external
  accountability; the trial tests visibility, not trustworthiness.

## 5. Scale note

Per-op costs: O(CAP) worst-case slot scans; the integrity scan is
O(CAP + audit_n) and runs on demand (not per-op). CAP=64 here; the
mechanism is unchanged at 100x slots — the next scale test is named in
BOUNDARIES.md.
