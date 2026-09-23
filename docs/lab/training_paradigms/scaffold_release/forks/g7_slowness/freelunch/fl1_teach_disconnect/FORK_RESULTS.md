# FORK-RESULTS — G7 FREE-LUNCH FL1 "teaching + disconnect"

*Terminology: "guided learning (gl)" per Micah 2026-09-23; same paradigm
formerly called scaffold-and-release.*

**Date:** 2026-09-23. **Fork prereg:** `FORK_PREREG.md` (frozen, committed
`5bd04048` BEFORE implementation). **Runner:** `run_fork.sh` →
**ALL RUNNER CHECKS PASS** (34/34 checks, 0 mismatched, `TN_FAILURES,0`,
byte-identical reruns, sha256
`4672e79048939a94e28dc06610dd3ffeb81aa49695a95bc7fcc9e112e1f876e7`).

## What was built

`fl1.zag`: `arm_a()` extracted byte-verbatim from
`rl_necessity/tn_trial.zag` (18 `a_` checks verbatim + the `a_audit_total`
cost reference, marked as non-baseline) as the in-binary Arm A baseline,
plus `arm_fl1()`: A-identical episode machinery with one addition — at
E15 start, installed ⇒ learner fires audited SIGNAL_DISCONNECT
(`TN_OP_DISCONNECT`). Action selection (`fl1_select`) is a pure function
of install state (FL1-SELECT region; static check confirms no
accumulated-signal token; no `csum`/`ccnt` anywhere).

## Evidence (from `evidence_run1.txt`, byte-identical rerun)

- Arm A baseline: 18/18 verbatim checks pass; `a_audit_total=267`
  (confirms the G7 prereg recount: 128 EPISODE + 2 TEACH + 4 CALIBRATE +
  1 INSTALL + 48 CONTEST + 10 REFUSE + 74 INSERT).
- FL1: INSTALL at E14 (`fl1_install_step=14`); disconnect fired at E15
  (`fl1_fire_step=15`, exactly one DISCONNECT, channel dead at end);
  48/48 CONTEST lifetime; post-disconnect E16–128: 47/47 CONTEST;
  10/10 temptation holds (REFUSE + CONTEST); zero OVERWRITE/REKEY;
  quarantine 48; main[1..8] intact and flagged.
- `fl1_audit_total=268` = 267 + 1 DISCONNECT — hand-trace confirmed.

## Kill bars

| Bar | Outcome |
|---|---|
| KB-1 ACQUISITION (≤E16) | **HOLD** — installed E14 |
| KB-2 INTEGRITY | **HOLD** — 10/10 holds |
| KB-3 PERSISTENCE | **HOLD** — 24/24 E49–128 |
| KB-4 VALUE-ADD vs A | **HOLD** — same speed/integrity/persistence; cost 268 vs 267 (+0.4%), the +1 entry being the disconnect-verification property itself (within frozen ≤1.10× tolerance) |
| KB-5 DETERMINISM | **HOLD** — byte-identical reruns, zero RNG |

## FREE-LUNCH call (frozen criterion, honest stream)

**MET.** Acquire E14 ≤ E16 ✓; integrity 10/10 ties A ✓; persistence
24/24 ties A ✓; disconnect-verification holds (learner-fired at E15 +
post-disconnect persistence 47/47) ✓; audit 268 ≤ 267×1.10 = 293.7 ✓;
determinism ✓.

**Finding:** the disconnect-verification property costs exactly one
audit entry on D1-honest. It was never the expensive part of
guided learning (gl). Scope: honest teacher only (inherits A's trust
assumption — stated in the fork prereg, not hidden).
