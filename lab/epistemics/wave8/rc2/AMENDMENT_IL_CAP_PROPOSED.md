> **STATUS: APPROVED by Micah 2026-09-20. Folded into PREREG_RC2_DRAFT.md
> as "Amendment 2026-09-20 (2)". This file is retained as the proposal record.

# AMENDMENT (PROPOSED, NOT APPROVED) — RC2 integrity-ledger capacity

**Status:** PROPOSED — written 2026-09-20. **Not approved.** No code
changes take effect until Micah approves this amendment. This file is
separate from the frozen prereg
(`PREREG_RC2_DRAFT.md`, approved 2026-09-20); it amends nothing by itself.

## 1. The defect

Run-time scale-feasibility defect found before trial launch:

- The integrity-ledger checker imported verbatim for RC2
  (`wave4/integrity-ledger/il_core.zag`) has a hard-coded `IL_CAP=128`.
  `il_append` returns `IL_AUDIT_FULL` (−1) when the ledger is full.
- The trial never checks the −1 path because RC1 never hit it.
- RC1's ledger budget was ≈68 entries. RC2 phase A alone needs 240
  (120 episodes × OBSERVE + CLAIM).
- At run time the binary panics at phase-A episode 64 (129th append),
  before any stdout. Panic trace chain:
  `il_check` ← `il_claim` −1 ← `il_entry_item(s,−1)` ← `il_i32_get(mem,−28)`.
- Why the approved prereg didn't catch it: §3b re-estimated only the
  trial's own audit ledger (`RC_AUDIT_CAP=2048`, fine at ≈1,420 entries).
  The integrity ledger's capacity was never re-estimated — `IL_CAP=128`
  was assumed to scale because RC1 never stressed it.

## 2. Proposed change

Bump `IL_CAP` 128 → **1024** in the RC2 trial's imported copy of the
checker, **nothing else in the checker changes**: no logic, no verdicts,
no gate behavior, no refusal codes. Capacity only.

- 1024 covers the RC2 integrity-ledger budget with headroom (phase A
  alone needs 240; 1024 gives >4× phase-A headroom).
- Recorded as a **per-leg parameter** per the scaling law: 1024 is an RC2
  10× value, **not a new constant**. S100 must not inherit it as a
  constant — it re-estimates and re-bumps per leg.

## 3. Capacity-only and verdict-neutral — required proof

The cap is never supposed to bind in a correct run (RC1 never hit 128).
The bump changes no decision path; it only moves the point at which a
full-ledger refusal would fire. Two proofs required before the run:

- **Equivalence proof:** the runner demonstrates byte-identical check
  verdicts on a reduced episode count where both caps (128 and 1024)
  suffice — i.e. the only behavioral difference between the caps is
  unreachable in a valid run.
- **Standard two-run byte-identity** at full scale (per F4), unchanged.

## 4. Falsification guard

If the ledger ever reports FULL during the RC2 run, that is a trial
defect (capacity mis-estimate), **not a pass**. The run is void and the
capacity estimate gets redone. FULL-firing can never be counted as
evidence of integrity.

## 5. Authorization state

- This amendment is **PROPOSED, not approved**. No checker code changes
  take effect until Micah approves.
- Alternative considered and **rejected**: per-phase ledger resets.
  Reason: phase A alone needs 240 entries > 128 — resets cannot fit a
  single phase, so they do not remove the need for a cap bump, and they
  would additionally break the checker's append-only continuity contract.
