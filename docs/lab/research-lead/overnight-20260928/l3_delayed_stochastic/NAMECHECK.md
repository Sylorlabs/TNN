# NAMECHECK: L3 Delayed-Stochastic Worker

Worker: L3 Delayed-Stochastic Worker (subagent, 2026-10-02).
Scope: `docs/lab/research-lead/overnight-20260928/l3_delayed_stochastic/`
only.
Prereg: `PREREG.md` (frozen, committed alone before any implementation
existed; zero amendments).

## Step 0: Toolchain guard (mandatory, recorded before any work)

Ran at worker startup:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp \
  sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```
Result: `which python3 python` printed nothing; `guard-check-done`
confirmed. No python3/python in PATH for the whole task. All
computational work (including the pre-prereg independent checker in
/tmp/dscheck.zag and the awk attribution audit, which is a log check,
not research logic) done with safebin tools and pure Zag via the
pinned znc. No forbidden executable invoked: no PROCESS-FAIL.

## Build record

- learner_ds.zag: NEW delayed+noisy learner (PREREG.md section 3).
  Calls exactly two world-side symbols: w_sched_ds, w_arrive_ds
  (delayed noisy consequence channel). Per-step ledger records
  (tag, cand, thri, k); arrivals attributed by schedule step, never
  by recency; each threshold score is a sum of exactly K attributed
  arrivals (count-verified). Zero label/expected/w_tab/margin/
  correct/_mode/bridge/handler/w_conseq/w_val/menu_/nz_ tokens
  (shell audit in REPORT).
- world_ds.zag: SETTLE-DS environment; frozen episode tables (same as
  l3_verify/l3_delayed/l3_stochastic); hidden margin rule
  margin = e0+e1-e2; seeded counter-based noise (seed 7000, same spec
  as l3_stochastic); w_sched_ds (returns nothing), w_arrive_ds
  (consequence C_true + noise computed only at step s+3);
  w_conseq_det (experiment-side deterministic immediate oracle for
  the uniqueness sweep only); menu controls.
- driver_ds.zag: experiment-side driver. Teaches X train+test, seeds
  M0, creates the world state, runs the learner's l_experiment
  (inherit, construct+revise, deploy held-out), dumps M/MPREV, runs
  the experiment-side uniqueness sweep and the NOM and MENU arms
  (menu via experiment-side immediate noisy K-sums), runs the K=1
  single-sample control arm through the delayed channel, prints the
  kill-bar summary.
- audit_attr_ds.awk: frozen attribution audit (every ATTR line:
  arr - sched == 3, DEPLOY at sched with same tag and same k, no
  ATTR-BAD / ATTR-COUNT-BAD).
- ds_full.zag: concatenation learner_ds+world_ds+driver_ds.
- ds_bin: compiled with pinned znc
  src/tools/toolchain/znc_linux_x86_64_abed8aa1.
- Runs: ds_run1.txt, ds_run2.txt, ds_run3.txt (3/3 byte-identical,
  sha256 recorded in REPORT.md).

## Commit record

- fdac1ee31: PREREG.md + NAMECHECK.md alone (frozen,
  pre-implementation; explicit pathspecs).
- a183745df: implementation + REPORT (explicit pathspecs for
  `git add`; the shared branch index also held 10 pre-staged
  contract_drift_detect files from a concurrent worker, which were
  swept into the same commit; no data lost, directories are
  separate; see REPORT.md).
- Nothing pushed; branch tnn-native-lab.
