# MA1 trial results — 2026-09-19

Native Zag, Linux x86-64, `znc 2026.07.0-dev` (pinned lab compiler).
Runner: `trial/run_memory_agency.sh`. Evidence: `trial/EVIDENCE_20260919T222823Z/`.

## Result: 58/58 checks pass, `MA_FAILURES,0`, exit 0.

## What the trial proves (PREREG_MA1 — CONFIRMED)

1. **Deliberate kill works.** The learner killed its own low-value memory
   (slot 0, value 10): slot cleared, value zeroed, audited.
2. **Deliberate pin protects.** The high-value memory (slot 2, value 90)
   was pinned; a subsequent KILL was refused `REFUSED_PINNED` (102) with
   the slot byte-identical afterwards. After explicit UNPIN, the same
   KILL succeeded — protection is a deliberate state, not a property of
   the data.
3. **CORE is structurally unkillable.** KILL on the core slot refused
   `REFUSED_CORE` (101), value 100 intact; PIN on core refused as redundant
   (101) — the audit log records the attempt honestly instead of a silent
   no-op.
4. **Staged autonomy gates hold.** At stage ADD(1), KILL and PIN both
   refused `REFUSED_STAGE` (105); at stage NONE(0), ADD refused. Stage
   changes themselves are audited ops (`MA_OP_SETSTAGE`).
5. **Capacity is fail-closed.** ADD to a full 8-slot store refused
   `REFUSED_FULL` (104), out_slot=-1.
6. **Refusals never mutate.** Global ledger scan: every refused op has
   before==after on all snapshot words (`audit_clean_refusals`).
7. **Rollback works.** `ma_rollback_last` restored the pre-demote tier
   (LONG) from the audit entry's before-snapshot; the rollback itself
   was audited.
8. **The ledger is the state.** Replaying all 28 audit entries from
   genesis reconstructs the exact live slot fields, stage, and entry
   count (`ledger_replay`) — the testable definition of "conscious":
   no state change without an audit entry.

## What it does NOT show (per the prereg)

Value-judgment quality: values were protocol-fixed, so this proves the
*machinery* (deliberate ops, refusals, audit, rollback), not good taste
in what to remember. Judgment training is MA3 / safety Phase 4.

## Notes for future agents

- Integer-only, playbook-proven subset; compiled warning-free first try
  after the byte-packing idiom was copied from the white-box suite.
- `nio_alloc` is not zeroed — `ma_init` zeroes every buffer by hand.
- `ma_kill` on a bad slot index is a *caller bug* (`cl_bad`, 2001, not
  audited); all learner-reachable refusals are audited result codes.
- Audit ledger is fixed at 64 entries and fail-closed on overflow
  (`REFUSED_AUDITFULL`); the trial used 28.
- Binary `ma_trial_linux` removed after the run; the runner rebuilds it.
