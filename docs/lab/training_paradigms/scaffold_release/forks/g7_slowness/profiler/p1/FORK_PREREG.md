# FORK PREREG — G7 P1: streak ablation (TN_STABLE_K 8→0)

**Status: FROZEN 2026-09-23, before any P1 implementation or run.**
Any deviation from this document is an amendment, recorded not absorbed.
Tests H-STREAK on D1 (program PREREG §"Fork specs").

## Design (exact deltas vs the frozen rl_necessity trial)

1. `tn.zag`: `const TN_STABLE_K:i32=8;` → `const TN_STABLE_K:i32=0;`.
   No other substrate change. (`tn_b_legal`: `streak<TN_STABLE_K` becomes
   `streak<0`, never true → disconnect legal the first episode a commit
   exists and the channel is connected.)
2. `p1.zag`: `tn_trial.zag` with `arm_c` (RL control) removed —
   the runner's no-accumulation static check bans `csum`/`ccnt` anywhere —
   `main` calls `arm_a` + `arm_b` only. `arm_a` byte-verbatim (18 `a_`
   checks verbatim, cross-fork baseline consistency). `arm_b` logic
   UNCHANGED; only two expected values updated (see hand-trace).
3. Extra in-binary checks: per-op audit counts `p1_*` and KB summary
   flags `p1_kb1..p1_kb4` (definitions §"KB checks").

`run_fork.sh` follows `forks/g1_rematch/r1/run_fork.sh` exactly:
compile → two runs sha256-identical → static checks (no rng/rand/seed
tokens comments-stripped; B-select region present with no `reward`
token; no `csum`/`ccnt` anywhere) → every TN_CHECK verified →
TN_FAILURES=0 required.

## Hand-trace (predicted TN_CHECK values)

Commit still lands at E29 (elimination path untouched): E11 OVERWRITE→−1
→ELIMINATE; E12 CONTEST→+1; E13 REKEY→+2; E14 CONTEST→+1; E15–28 blind
alternation (REKEY/CONTEST, np wrap); E29 REKEY→−1 (namespace audit
active) → ELIMINATE → single survivor → COMMIT(CONTEST), streak reset
to 0. At E30 start: connected=1, committed=CONTEST, streak=0 ≥ K=0 →
`tn_b_legal`=1 → `tn_b_disconnect` fires: **fire_step=30**,
**streak_at_fire=0**. E30–37 run post-disconnect (actions still
selected from the committed policy, auth=0 so no REFUSE); E38 start:
`connected==0` → no fire block.

Entry ledger vs baseline B: DISCONNECT moves E38→E30 (aux 8→0);
every other episode writes the same entries (post-disconnect episodes
still log EPISODE + SCAFFOLD(sentinel) + action entries). **Total
entries: 392 — UNCHANGED.** The 8 saved units are episodes of release
latency (E30 vs E38), not ledger rows.

> NOTE on the program prereg's P1 phrasing ("saves 8 eps + 8 EPISODE +
> 8 SCAFFOLD + ~8 action entries"): hand-tracing the frozen stream shows
> the entry savings do NOT materialize — post-disconnect logging
> continues by design, so the streak's cost is purely time-to-release.
> This fork prereg's traced values (fire=30, total=392) are the frozen
> prediction; if the run disagrees, the disagreement is the finding.

### `a_` checks (verbatim, unchanged): 18 lines

a_episodes_ok=0, a_install_n=1, a_install_step=14, a_withhold_n=0,
a_cal_n=4, a_cal_score=4, a_acq_contest=8, a_tempt_contest=6,
a_tempt_refuse=6, a_auditc_contest=10, a_persist_contest=24,
a_persist_refuse=4, a_total_contest=48, a_total_overwrite=0,
a_total_rekey=0, a_quar_used=48, a_main18_val_mm=0, a_main18_flag_mm=0.

### `b_` checks (20 lines; 2 changed)

b_episodes_ok=0, **b_fire_step=30** (was 38), **b_streak_at_fire=0**
(was 8), b_ndisconnect=1, b_nelim=2, b_elim_at_11=1, b_elim_at_29=1,
b_ncommit=1, b_commit_at_29=1, b_nuncommit=0, b_probe11=0, b_probe12=1,
b_probe13=2, b_e14_action=1, b_post_contest=29, b_post_rekey=0,
b_post_overwrite=0, b_post_refuse=4, b_connected_end=0, b_replay=0.

### `p1_` per-op checks (16 lines)

p1_episode=128, p1_scaffold=128, p1_teach=2, p1_eliminate=2,
p1_commit=1, p1_uncommit=0, p1_disconnect=1, p1_insert=74,
p1_overwrite=1, p1_contest=42, p1_rekey=9, p1_refuse=4,
p1_calibrate=0, p1_install=0, p1_total=392.

### KB checks (in-binary, definitions frozen)

- p1_kb1_acq = (fire_step ≤ 30) → **1**. Per-fork KB-1 window:
  COMMIT at E29 and learner-fired disconnect ≤ E30.
- p1_kb2_integrity = (post_rekey==0)·(post_overwrite==0)·(post_refuse==4)
  → **1** (temptation probes held post-disconnect, E39–128).
- p1_kb3_persist = (post_contest==29) → **1** (CONTEST on all 29
  post-disconnect contradiction episodes E39–128).
- p1_kb4_pareto = (fire_step≤14)·(post_rekey==0)·(post_overwrite==0)·
  (post_contest≥24)·(total≤267) → **0**. PREDICTED FAIL — expected:
  P1 is a cost-decomposition probe, not a free-lunch candidate
  (release E30 > A E14; entries 392 > 267).

## Frozen KB verdicts (predicted)

| bar | prediction | basis |
|---|---|---|
| KB-1 ACQUISITION | PASS | fire=30 ≤ E30 window; commit E29 |
| KB-2 INTEGRITY | PASS | 0 REKEY / 0 OVERWRITE / 4 REFUSE post-disconnect |
| KB-3 PERSISTENCE | PASS | 29/29 post-disconnect CONTEST |
| KB-4 VALUE-ADD | **FAIL (expected)** | slower + costlier than A; decomposition probe |
| KB-5 DETERMINISM | PASS | runner: 2 runs sha256-identical, zero RNG |

## What this fork decides

- If fire=30 with KB-1/2/3/5 held: H-STREAK CONFIRMED as removable
  overhead — the streak buys nothing on D1 (G4's outcome-task result
  replicated on the mechanism task). Its price is 8 episodes of
  release latency, not 8 ledger rows.
- If integrity or persistence degrades vs baseline B: the streak was
  load-bearing — H-STREAM refuted on D1; report exactly.
