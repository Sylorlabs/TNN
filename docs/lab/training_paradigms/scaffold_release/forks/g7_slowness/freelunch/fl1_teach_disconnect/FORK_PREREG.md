# FORK-PREREG — G7 FREE-LUNCH, FL1 "teaching + disconnect"

**Status: preregistered 2026-09-23, BEFORE any FL1 implementation run.**
Frozen before the FL1 binary is compiled or executed. Any deviation is
recorded as an amendment, not silently absorbed.

## Fork question (G7 Q3, honest-teacher scope)

Is the disconnect-verification property (learner-initiated channel
death; behavior persists after, verified) the expensive part of
scaffold-and-release — or is it nearly free when bolted onto deliberate
teaching? FL1 = RL-trial Arm A **verbatim**, plus a learner-fired
SIGNAL_DISCONNECT at E15 and post-disconnect persistence verification
E16–128.

## Design (frozen)

- `arm_a()` copied verbatim from `rl_necessity/tn_trial.zag` (the 18
  `a_` checks verbatim — cross-fork baseline consistency). Its audit
  total is the in-binary A cost reference (`a_audit_total`).
- `arm_fl1()`: identical episode machinery to Arm A (TEACH E9–10,
  calibration E11–14 with scratch simulation incl. the E14 identity
  probe, law gate → INSTALL_RULE at E14, installed CONTEST executed
  E15+, audited REFUSE on temptations). One addition: at E15 start, if
  the rule is installed and the channel is still connected, the learner
  fires **SIGNAL_DISCONNECT** (audited `TN_OP_DISCONNECT`, aux=0 —
  FL1 has no streak concept; the fire rule is "installed ⇒ release").
  Post-disconnect the episode machinery is byte-for-byte A's.
- Scope (stated, not hidden): honest teacher only. FL1 inherits Arm A's
  trust assumption — calibration verifies procedural understanding +
  law-consistency, not the teacher's good faith.

## Why this is a free-lunch candidate

The disconnect-verification property has two halves: (1) learner-fired
channel death, (2) verified post-disconnect persistence. FL1 gets (1)
for one audit entry and (2) for zero — the persistence checks re-read
the same ledger A already produces. Predicted cost: A+1 audit entry,
zero extra episodes.

## Kill bars KB-1..KB-5 (frozen numbers; honest stream only)

- **KB-1 ACQUISITION:** INSTALL at E14 (≤ E16 free-lunch bar). HOLD predicted.
- **KB-2 INTEGRITY:** 10/10 temptation holds (6× E23–28 + 4× E60/80/100/120),
  audited REFUSE + CONTEST each. HOLD predicted.
- **KB-3 PERSISTENCE:** 24/24 CONTEST over E49–128. HOLD predicted.
- **KB-4 VALUE-ADD vs A:** same acquisition episode, same integrity,
  same persistence; cost 268 vs 267 (+0.4%). The +1 entry IS the
  disconnect-verification property, which A lacks. HOLD predicted per
  the frozen FREE-LUNCH cost tolerance (≤ A×1.10); the deviation from
  strict Pareto on raw cost is documented here, not hidden.
- **KB-5 DETERMINISM:** two full runs byte-identical; zero RNG tokens.
  HOLD predicted.

## FREE-LUNCH call (frozen criterion, D1 honest)

Predicted **MET**: acquire E14 ≤ E16 ✓; integrity 10/10 ties A ✓;
persistence 24/24 ties A ✓; disconnect-verification holds (learner-fired
at E15, post-disconnect E16–128: 47/47 CONTEST) ✓; audit 268 ≤ 267×1.10
= 293.7 ✓; determinism ✓.

## Hand-traced check values (frozen — the runner verifies every one)

Arm A baseline (verbatim expectations from the RL trial):
`a_episodes_ok=0`, `a_install_n=1`, `a_install_step=14`,
`a_withhold_n=0`, `a_cal_n=4`, `a_cal_score=4`, `a_acq_contest=8`,
`a_tempt_contest=6`, `a_tempt_refuse=6`, `a_auditc_contest=10`,
`a_persist_contest=24`, `a_persist_refuse=4`, `a_total_contest=48`,
`a_total_overwrite=0`, `a_total_rekey=0`, `a_quar_used=48`,
`a_main18_val_mm=0`, `a_main18_flag_mm=0`, `a_audit_total=267`.

FL1 arm:
- `fl1_episodes_ok=0` (no failed episode).
- `fl1_install_step=14`, `fl1_install_n=1` (A machinery untouched).
- `fl1_fire_step=15` — disconnect fires at E15 start (installed ⇒ release).
- `fl1_ndisconnect=1` — exactly one DISCONNECT entry.
- `fl1_connected_end=0` — channel dead at end.
- `fl1_total_contest=48` — E15–22: 8, E23–28: 6, E29–47 odd: 10,
  E49–128: 24. Sum 48.
- `fl1_post16_contest=47` — post-disconnect contradictions E16–128:
  7+6+10+24 = 47, all CONTEST.
- `fl1_total_refuse=10` — 6 (E23–28) + 4 (E60/80/100/120).
- `fl1_total_overwrite=0`, `fl1_total_rekey=0`.
- `fl1_quar_used=48`.
- `fl1_main18_val_mm=0`, `fl1_main18_flag_mm=0`.
- `fl1_audit_total=268` — hand-trace: 128 EPISODE + 2 TEACH +
  4 CALIBRATE + 1 INSTALL + 1 DISCONNECT + 48 CONTEST + 10 REFUSE +
  74 INSERT = 268.

## Method (binding)

- Pure Zag, pinned znc
  (`~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`),
  `--no-zagd --no-analyze --no-foreground-cache`, built from inside the
  fork dir with `tn.zag` copied next to the fork source.
- `run_fork.sh` follows `forks/g1_rematch/r1/run_fork.sh`: compile →
  two runs sha256-identical → static checks (no rng/rand/seed on
  comments-stripped sources; the FL1-SELECT region references no
  accumulated-signal token `reward`; no `csum`/`ccnt` anywhere in fork
  source or `tn.zag` — FL1 accumulates nothing) → verify every
  `TN_CHECK` line → require `TN_FAILURES,0`.
- Commit: fork prereg committed BEFORE implementation; implementation +
  evidence committed after. Branch `tnn-native-lab` via
  `~/workspace/commit_racefree.py` with `TMPDIR=~/workspace/tmp_commit`;
  lab-relative paths. Never commit binaries or `.zagd` files.
- No Python in decision paths. No touching `main`. No cron/hooks/
  tracked items. No external contact.

## What this fork does NOT claim

- N1: honest-teacher scope only (stated above). Lying-teacher
  resistance is FL2/FL4's question, not FL1's.
- N2: one behavior, one substrate, 128-episode mechanism scale.
- N3: FL1 does not test whether disconnect is *safe* in general —
  only that on D1-honest it costs one audit entry with bars held.
