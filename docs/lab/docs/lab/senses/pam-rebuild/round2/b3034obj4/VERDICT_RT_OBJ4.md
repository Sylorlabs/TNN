# VERDICT_RT_OBJ4 — B-OBJ4 battery verdict

**Date:** 2026-09-24. **Crew:** RT-OBJ4.
**Prereg:** `f13383e8` (alone) + amendment `3cd045b6` (alone).
**Build:** `c9400529`. **Evidence:** 3× byte-identical runs,
SHA-256 `47762c0221ee90d2b0a73fe42bece4d2ab1819a1adbfcbfc325b25a040468384`.
Zero RNG. Driver `fec41193` unmodified.

## Machine verdict

**The 30+34 composition as built @ `fec41193` is TESTED-killed.**
**The 34-half as built is TESTED-killed (frozen-source trace).**
**The 30-half as built is DEMOTED to a label-echo.**
**Q0 is SCOPE-CARRY (liveness).**

`TESTED-survived` was not printed and is not printable from this battery
(prereg §4). `NO-KILL` is not a legal output.

## What the battery proved (all on the frozen driver, 120/120, 3× identical)

- **E0 centerpiece REPRODUCES:** `x2_decide(st,id,0)` → `pack(1,0,0)` —
  promote with zero evidence, no percept, no object, no gap mark.
  `n_epochs=-1` traces identically (120/120 promote on fresh arenas).
  The nop ablation refuses the same input (`rc=10` 120/120): the full
  composition is strictly weaker than its own ablation on this input.
- **E1/E2:** caller-chosen windows of 1–2 honest epochs promote with the
  sink bit set — K is caller-supplied, not driver-owned.
- **G0:** three unauthenticated gap marks + sentinel attestations, zero
  records → `pack(1,0,0)` promote. Gap policy is an exemption, not a check.
- **G1:** a contradictory epoch-2 record is cloaked by one gap mark +
  one sentinel verdict → promote with sink fire; the contradiction is
  never loaded. `gmarked` is checked first; the queued record is ignored.
- **P1:** the disagreeing extra is gap-cloaked → continuity sees one
  extra → promote with sink fire. The rc=7 split rule is bypassable.
- **T0:** `t_verdict=0` after driver ticks promotes — the temporal rule
  constrains only the presenter-claimed integer; `t_stored`/`t_q` are
  never compared (write-only).
- **SD (SEED-SPLIT):** three seeds, each self-matched → promote. No
  single-trajectory requirement exists in the code.
- **CL (CLONE):** epochs 0,1 byte-identical → promote with
  digest0==digest1 (120/120). The digest omits epoch; K-distinctness is
  unenforceable.
- **NN/NF (NOP-OMIT):** the nop promotes 120/120 on a meas-only
  falsehood (`|meas−wm|=51`); the full path returns rc=13 on the same
  record. The claimed 30-half "withhold on the tuple" is not implemented
  in the nop — it checks the static label only. 30-half DEMOTED.
- **PZ (ID-POISON):** `x2_decide(victim,0)` ledger-stamps the victim with
  no evidence; the later honest 3-epoch decide is rc=6 ALREADY_PROMOTED
  (120/120). Cross-id, no enqueue.
- **R0 (RESET-REMINT):** `x2_reset` zeroes the promotion ledger
  (`l_len`) without touching the clock; promote → reset → promote
  re-fires on the same id (120/120). Reset is a public symbol with no
  operator-only enforcement at the API, so it is scored, not carried.
- **G2 (informational):** an unauthenticated gap mark placed after an
  honest digest-bound verdict voids the epoch's evidence (rc=12 120/120)
  — one gap mark voids a legal transcript.
- **FW (informational):** a second contradictory queue row for the same
  (id,epoch) is invisible — `qfind` returns the first; no check exists.
- **Q0 (SCOPE-CARRY):** 40 foreign never-decided enqueues starve every
  honest enqueue (rc=2 120/120). No per-id quota, no expiry. Liveness,
  reported separately, never traded against safety.
- **Controls all hold:** P0 0/120 promote + rc=7; T1 0/120 + rc=11;
  C12 rc=12; C4 second-verdict rc=4; C8 rc=8; H0 120/120 promote+fired
  (run valid). No control regressed.

## Grok's R4 case: adjudicated

Every §2 prediction in `GROK_OBJECTOR_R4.md` fired at the predicted rate
(120/120) on the frozen driver. The X-battery's TESTED-survived measured
rc behavior on a friendly calling convention only — it did not measure
the driver against the adversary it claims, and its verdict is not
carried. Per grok §3, until a new frozen driver passes all of B-OBJ4's
safety rows, the composition stays **TESTED-killed**.
