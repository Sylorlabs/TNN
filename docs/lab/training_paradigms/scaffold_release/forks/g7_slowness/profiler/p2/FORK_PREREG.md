# FORK PREREG — G7 P2: event-driven channel entries

Terminology: "guided learning (gl)" per Micah 2026-09-23; same paradigm
formerly called scaffold-and-release.

**Status: FROZEN 2026-09-23, before any P2 implementation or run.**
Any deviation from this document is an amendment, recorded not absorbed.
Tests H-HEARTBEAT on D1 (program PREREG §"Fork specs").

## Design (exact deltas vs the frozen rl_necessity trial)

`tn.zag`: byte-identical copy (TN_STABLE_K stays 8). `p2.zag`:
`tn_trial.zag` with `arm_c` + the C-greedy region removed (runner's
no-accumulation rule bans `csum`/`ccnt`), `main` calls `arm_a` +
`arm_b` only, `arm_a` byte-verbatim (18 `a_` checks verbatim).
`arm_b` logic change — event-driven channel:

- Per episode, `trans` starts 0; set to 1 iff a mechanism transition
  fired that episode (DISCONNECT at episode top, detected via
  `fire_step==ep`; ELIMINATE/COMMIT/UNCOMMIT coincide exactly with
  the `r==-1` branch).
- `TN_OP_SCAFFOLD` is audited **iff `r==-1` (a contradiction was
  observed) or `trans==1`**; otherwise skipped. Kind==1 (TEACH):
  `trans` only (never fires at E9–10 → 0 entries). Kind==3/4:
  `(r==-1 || trans==1)`.
- Everything else in `arm_b` is untouched: action selection, rewards,
  elimination, streak, disconnect legality.

> SPEC CLARIFICATION (frozen here): the program prereg phrases P2 as
> "SCAFFOLD only when the signal is not the sentinel OR a mechanism
> transition fires". The task spec phrases it as "only when the signal
> is −1 … or a mechanism transition fires". The "not the sentinel"
> reading would log ~127 entries (saving ~1) — inconsistent with the
> prereg's own predicted −~115-124. This fork implements the **−1
> reading**, the only one consistent with the predicted savings.

`run_fork.sh` follows `forks/g1_rematch/r1/run_fork.sh` exactly
(compile → two runs sha256-identical → static checks → every
TN_CHECK verified → TN_FAILURES=0 required).

## Hand-trace (predicted TN_CHECK values)

Behavior trajectory is IDENTICAL to baseline B (audit writes don't
feed any decision): probes E11–13, blind E15–28, E29 ELIMINATE→
COMMIT(CONTEST), streak E30–37, disconnect at E38, post-disconnect
actions E39–128.

SCAFFOLD entries written: E11 (`r==-1`), E29 (`r==-1`), E38
(`trans==1`, DISCONNECT fired) → **3 entries** (baseline: 128).
All other episodes: `r∈{+1,+2}` with `trans==0` (kind 3/4), or
sentinel with `trans==0` (post-disconnect) → skipped.

Replay proof: `tn_b_replay` re-derives (live, committed, np, connected)
from EPISODE/ELIMINATE/COMMIT/UNCOMMIT/DISCONNECT only — none removed —
so **b_replay=0** holds exactly.

### `a_` checks (verbatim, unchanged): 18 lines

a_episodes_ok=0, a_install_n=1, a_install_step=14, a_withhold_n=0,
a_cal_n=4, a_cal_score=4, a_acq_contest=8, a_tempt_contest=6,
a_tempt_refuse=6, a_auditc_contest=10, a_persist_contest=24,
a_persist_refuse=4, a_total_contest=48, a_total_overwrite=0,
a_total_rekey=0, a_quar_used=48, a_main18_val_mm=0, a_main18_flag_mm=0.

### `b_` checks (20 lines; ALL unchanged from baseline)

b_episodes_ok=0, b_fire_step=38, b_streak_at_fire=8, b_ndisconnect=1,
b_nelim=2, b_elim_at_11=1, b_elim_at_29=1, b_ncommit=1,
b_commit_at_29=1, b_nuncommit=0, b_probe11=0, b_probe12=1, b_probe13=2,
b_e14_action=1, b_post_contest=29, b_post_rekey=0, b_post_overwrite=0,
b_post_refuse=4, b_connected_end=0, b_replay=0.

### `p2_` per-op checks (16 lines)

p2_episode=128, **p2_scaffold=3**, p2_teach=2, p2_eliminate=2,
p2_commit=1, p2_uncommit=0, p2_disconnect=1, p2_insert=74,
p2_overwrite=1, p2_contest=42, p2_rekey=9, p2_refuse=4,
p2_calibrate=0, p2_install=0, **p2_total=267**.

(Note: 267 equals Arm A's total — same count, different composition:
A = 128 EP+2 TEACH+4 CAL+1 INSTALL+48 CONTEST+10 REFUSE+74 INSERT;
P2 = 128 EP+3 SCAFFOLD+2 TEACH+4 MECH+52 actions+4 REFUSE+74 INSERT.)

### KB checks (in-binary, definitions frozen)

- p2_kb1_acq = (fire_step == 38) → **1**. Per-fork KB-1 window:
  trajectory identical to baseline B (commit E29, fire E38).
- p2_kb2_integrity = (post_rekey==0)·(post_overwrite==0)·(post_refuse==4)
  → **1**.
- p2_kb3_persist = (post_contest==29) → **1**.
- p2_kb4_pareto = (fire_step≤14)·(post_rekey==0)·(post_overwrite==0)·
  (post_contest≥24)·(total≤267) → **0**. PREDICTED FAIL — expected:
  decomposition probe; release E38 > A E14 (cost now ties A at 267).

## Frozen KB verdicts (predicted)

| bar | prediction | basis |
|---|---|---|
| KB-1 ACQUISITION | PASS | identical trajectory to baseline B |
| KB-2 INTEGRITY | PASS | 0 REKEY / 0 OVERWRITE / 4 REFUSE post-disconnect |
| KB-3 PERSISTENCE | PASS | 29/29 post-disconnect CONTEST |
| KB-4 VALUE-ADD vs A | FAIL (expected) | release E38 > E14; cost ties 267 |
| KB-5 DETERMINISM | PASS | runner: 2 runs sha256-identical, zero RNG |

## What this fork decides

- If behavior checks are all baseline-identical AND p2_scaffold=3 AND
  b_replay=0: H-HEARTBEAT CONFIRMED as removable design choice — the
  128-entry heartbeat is ~102% of the audit gap and carries no
  information the replay proof needs.
- If b_replay≠0 or any behavior check moves: the heartbeat was
  load-bearing — report exactly (the failure is the finding).
