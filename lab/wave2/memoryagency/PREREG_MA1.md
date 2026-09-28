# PREREG_MA1 — Conscious kill/pin with the safety gate (BUILT 2026-09-19)

## Hypothesis
A learner can deliberately kill a low-value memory and pin a high-value one,
with the safety gate refusing every illegal destruction — and the audit
ledger exactly reconstructing final state (the operational definition of
"conscious" in MEMORY_OPS.md §6).

## Mechanics
Native Zag trial (`trial/`): 8-slot store, stage=KILL(3).
- ADD 4 USER memories (values 10/50/90/30) + 1 CORE memory (value 100).
- PIN the value-90 slot (deliberate protection).
- KILL the value-10 slot → must succeed (deliberate destruction of the
  learner's own low-value judgment).
- KILL pinned slot → must refuse `REFUSED_PINNED`, state unchanged.
- KILL core slot → must refuse `REFUSED_CORE`, state unchanged.
- KILL empty slot → must refuse `REFUSED_NOTLIVE`.
- PROMOTE/DEMOTE tier moves on live slots; ADD to full store →
  `REFUSED_FULL`; KILL at stage=ADD → `REFUSED_STAGE`.
- ROLLBACK_LAST restores the most recent mutation's before-state.
- Final: ledger replay from genesis == exact current state; every
  CL_CHECK actual==expected.

## Falsification criteria
- FAIL if any illegal KILL succeeds (pinned/core/non-live slot cleared).
- FAIL if any legal op is refused.
- FAIL if ledger count != op count, or replay diverges from live state.
- FAIL if a refusal mutates state (before != after on a refused op).

## What it does NOT show
That the learner's value *judgments* are good (values are protocol-fixed
here). Judgment quality is MA3/Phase-4 work. MA1 proves the *machinery*:
deliberate ops, refusals, audit, rollback.
