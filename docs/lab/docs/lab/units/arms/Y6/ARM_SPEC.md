# Arm Y6 — Forgettable (tombstone-native) IDs (`STORE` family): Arm Specification

Round 1, Track A representation bake-off. Author: Arm Y6 crew (ARM CREW Y6,
subagent of the Track A coordinator). Date: 2026-09-21.

Authority order for this spec (per coordinator corrections received
2026-09-21): (1) `units/arms/briefs/Y6.json`; (2) the second correction's
byte-verified frozen §3 row; (3) nothing else previously written. The first
correction voided the original mistaken dispatch ("Cross-corpus
generalization", family ADV); the second correction superseded the first
correction's paraphrased §3 row (including an alternate M3 physical-deletion
criterion). The binding kill criterion is quoted verbatim in VERDICT.md.

## 1. Mechanism (frozen §3: "Y6 — Forgettable (tombstone-native) IDs")

- **Tombstone-native IDs.** Every unit is addressed by a 32-bit serial
  `(corpus << 24) | index`. The ID→slot mapping is a persistent
  open-addressing table the arm maintains (multiplicative hash +
  linear probe). Y6 is an **ID arm** per ARM_INTERFACE.md §9.
- **Refcounted.** Each slot carries `refs` (i32). `PIN`/`PROMOTE` take a
  holding reference (+1, audited); kill of a referenced ID is refused.
- **Checker-provable total deletion.** `y6_checker` (pure Zag, independent
  ledger walk + live table scan) verifies: (C1) no ADD re-issues a
  (serial,gen) a KILL/EVICT tombstoned; (C2) no live slot's (serial,gen) was
  ever tombstoned; (C3) every tombstoned slot has refs==0; (C4) kill-refusals
  counted. Returns 0/1; prints one `Y6CHECK` TAG line per audit.
- **Per-chunk cascade policy set at creation.** `pol` (i32 per slot), frozen
  to `POL_REFUSE_LOUD` at insert. A kill with refs>0 refuses LOUDLY: an
  `OP_REFUSE` ledger entry with reason code `RC_KILL_REFS` (201) plus a
  nonzero return — never silent.
- **Generation discipline.** Re-adding a tombstoned serial mints gen+1; the
  old (serial,gen) ID is never re-issued. Fresh serials start at gen 0.
- **Deliberate operations** (all audit-logged, 64-byte entries, 16 words):
  `ADD` (d1=generation), `KILL` (d2=generation), `PIN`, `PROMOTE`, `WEAKEN`,
  `REVISE`, `EVICT` (d2=generation), `REFUSE` (d1=reason code), plus the
  B-64-inherited `MARK_VALUABLE`/`TRAINER_*` bookkeeping ops.

## 2. Laws obeyed

Pure Zag cognition, zero RNG in any decision path (no RNG constructs in
source; byte-identical reruns on all 18 battery legs ×2 and all 10 M8
perturbation runs). No slice above `2^25` indexed (largest single buffer:
16.6MB M8 ledger). `_zag_arg` results never freed; `_zag_strcmp` equality
is `1`; no slice `==`; large-struct array fields aliased to locals before
indexing (AGENTS.md ZNC-2026-09-21-004 workaround: slice fields aliased via
pointer, never off a local struct value). One binary; `argv[1]` selects the
mode. Imports bare and relative. Battery workdirs under `~/workspace`.

## 3. Store layout (M5)

Slot table: 11 parallel i32/i64 arrays
(`ids, offs, lens, corps, flags, shifts, pidx, gens, refs, pol, ins`),
40 bytes/slot. M5 1x: 4,747,476 bytes slot table (118,687 slots),
5,486,784 bytes ledger (85,731 entries), corpus buffer 5,422,721 bytes.

## 4. ID-arm declarations

- M1 swap probe (A15): implemented, 64/64 PASS (provisional-pending-freeze;
  remap schedule `(slot+1)%nslots` every `ceil(n/64)` recalls).
- M7: implemented with the validator's proposed procedure (first-byte XOR
  0xFF C′ edit on every 100th unit; `(l*37)%n` lookups 1666/1667/1667);
  PROVISIONAL-PENDING-FREEZE per A7/A8 (Micah has not frozen the C′ edit or
  lookup schedule). All three bars pass: hit 100.0 ≥ 90, reuse 2.06 ≥ 1.5,
  dedup 0.50 ≥ 0.4.

## 5. Negative controls (checker liveness)

`y6-selftest` mode (diagnostic, not a harness mode): 5/5 PASS —
kill-with-refs refuses loudly and keeps the ID live; kill-without-refs
tombstones; re-add mints gen+1; the checker passes the valid lifecycle; and
a forged ledger ADD re-issuing a tombstoned (serial,gen) makes the checker
FAIL (C1). The checker is provably not vacuous.
