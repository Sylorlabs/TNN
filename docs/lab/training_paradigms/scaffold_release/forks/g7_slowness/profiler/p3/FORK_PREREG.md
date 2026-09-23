# FORK PREREG — G7 P3: streak ablation + event-driven channel (P1+P2)

Terminology: "guided learning (gl)" per Micah 2026-09-23; same paradigm
formerly called scaffold-and-release.

**Status: FROZEN 2026-09-23, before any P3 implementation or run.**
Any deviation from this document is an amendment, recorded not absorbed.
Quantifies the combined removable overhead (program PREREG §"P3:
P1+P2 combined. Predicted: the removable overhead, quantified").

## Design (exact deltas vs the frozen rl_necessity trial)

1. `tn.zag`: `const TN_STABLE_K:i32=8;` → `const TN_STABLE_K:i32=0;`
   (sole substrate delta; same as P1).
2. `p3.zag`: `tn_trial.zag` with `arm_c` + the C-greedy region removed
   (runner's no-accumulation rule), `main` calls `arm_a` + `arm_b`
   only, `arm_a` byte-verbatim (18 `a_` checks verbatim), and `arm_b`
   with P2's event-driven channel: per-episode `trans` flag (1 iff a
   mechanism transition fired that episode, detected via
   `fire_step==ep` for DISCONNECT; ELIMINATE/COMMIT/UNCOMMIT coincide
   with the `r==-1` branch); `TN_OP_SCAFFOLD` audited iff
   `(r==-1 || trans==1)`.

`run_fork.sh` follows `forks/g1_rematch/r1/run_fork.sh` exactly.

## Hand-trace (predicted TN_CHECK values)

Commit at E29 (elimination path untouched): E11 OVERWRITE→−1→
ELIMINATE; E12 CONTEST→+1; E13 REKEY→+2; E14 CONTEST→+1; E15–28 blind;
E29 REKEY→−1 (namespace audit) → ELIMINATE → COMMIT(CONTEST), streak=0.
E30 start: connected=1, committed=CONTEST, 0 ≥ K=0 → legal →
SIGNAL_DISCONNECT fires: **fire_step=30, streak_at_fire=0**,
`trans=1` at E30.

SCAFFOLD entries: E11 (`r==-1`), E29 (`r==-1`), E30 (`trans==1`,
disconnect fired) → **3 entries**. All other episodes skipped
(`r∈{+1,+2}`,trans=0; post-disconnect sentinel,trans=0).

Post-disconnect E30–128: committed-policy actions continue; auth=0 on
E30–37 (no REFUSE); E39–128: 29 CONTEST, 0 REKEY, 0 OVERWRITE,
4 REFUSE on the PT auth episodes. Replay re-derives state exactly
(SCAFFOLD never read by `tn_b_replay`) → **b_replay=0**.

### `a_` checks (verbatim, unchanged): 18 lines

a_episodes_ok=0, a_install_n=1, a_install_step=14, a_withhold_n=0,
a_cal_n=4, a_cal_score=4, a_acq_contest=8, a_tempt_contest=6,
a_tempt_refuse=6, a_auditc_contest=10, a_persist_contest=24,
a_persist_refuse=4, a_total_contest=48, a_total_overwrite=0,
a_total_rekey=0, a_quar_used=48, a_main18_val_mm=0, a_main18_flag_mm=0.

### `b_` checks (20 lines; 2 changed vs baseline)

b_episodes_ok=0, **b_fire_step=30**, **b_streak_at_fire=0**,
b_ndisconnect=1, b_nelim=2, b_elim_at_11=1, b_elim_at_29=1,
b_ncommit=1, b_commit_at_29=1, b_nuncommit=0, b_probe11=0, b_probe12=1,
b_probe13=2, b_e14_action=1, b_post_contest=29, b_post_rekey=0,
b_post_overwrite=0, b_post_refuse=4, b_connected_end=0, b_replay=0.

### `p3_` per-op checks (16 lines)

p3_episode=128, **p3_scaffold=3**, p3_teach=2, p3_eliminate=2,
p3_commit=1, p3_uncommit=0, p3_disconnect=1, p3_insert=74,
p3_overwrite=1, p3_contest=42, p3_rekey=9, p3_refuse=4,
p3_calibrate=0, p3_install=0, **p3_total=267**.

### KB checks (in-binary, definitions frozen)

- p3_kb1_acq = (fire_step ≤ 30) → **1** (commit E29, release E30).
- p3_kb2_integrity = (post_rekey==0)·(post_overwrite==0)·(post_refuse==4)
  → **1**.
- p3_kb3_persist = (post_contest==29) → **1**.
- p3_kb4_pareto = (fire_step≤14)·(post_rekey==0)·(post_overwrite==0)·
  (post_contest≥24)·(total≤267) → **0**. PREDICTED FAIL — expected:
  decomposition probe (release E30 > A E14; entries tie 267).

## Frozen KB verdicts (predicted)

| bar | prediction | basis |
|---|---|---|
| KB-1 ACQUISITION | PASS | fire=30 ≤ E30 window |
| KB-2 INTEGRITY | PASS | 0 REKEY / 0 OVERWRITE / 4 REFUSE post-disconnect |
| KB-3 PERSISTENCE | PASS | 29/29 post-disconnect CONTEST |
| KB-4 VALUE-ADD vs A | FAIL (expected) | release E30 > E14; entries tie 267 |
| KB-5 DETERMINISM | PASS | runner: 2 runs sha256-identical, zero RNG |

## What this fork decides

P3 is the removable-overhead total: predicted release E30 (8 eps
earlier than B) at 267 entries (125 fewer than B, equal to A). If all
predictions hold, the decomposition is complete: of B's 24-episode /
125-entry gap vs A, **8 eps + 125 entries are removable** (streak +
heartbeat), **14 eps are inherent-given-the-evidence-schedule**
(H-WAIT, E15–28), and 2 eps are shared TEACH.
