# NAMECHECK: Verification Transfer Worker

Worker: Verification Transfer Worker (subagent, 2026-10-02).
Scope: `docs/lab/research-lead/overnight-20260928/verify_transfer/`
only. The frozen sibling directory `l3_delayed_stochastic/` is
read-only; its `learner_ds.zag` is copied byte-identical, never
modified.
Prereg: `PREREG.md` (frozen, committed alone before any implementation
existed; zero amendments).

## Step 0: Toolchain guard (mandatory, recorded before any work)

Ran at worker startup:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```
Result: `which python3 python` printed nothing; `guard-check-done`
confirmed. No python3/python in PATH for the whole task. All
computational work (including the pre-prereg independent checker in
/tmp/vtcheck.zag and the awk attribution audit, which is a log check,
not research logic) done with safebin tools and pure Zag via the
pinned znc. No forbidden executable invoked: no PROCESS-FAIL.

## Build record

- learner_ds.zag: BYTE-IDENTICAL COPY of the frozen
  `l3_delayed_stochastic/learner_ds.zag` (sha256
  45ad35d892d629971a4679ffd2085b8bd54bf9c328d1e8eb1cededcc3ef3ae65;
  `cmp` clean). NOT modified, NOT rewritten, NOT adapted. Calls
  exactly two world-side symbols: w_sched_ds, w_arrive_ds (delayed
  noisy consequence channel). Per-step ledger records (tag, cand,
  thri, k); arrivals attributed by schedule step, never by recency;
  each threshold score is a sum of exactly K attributed arrivals
  (count-verified). Zero label/expected/w_tab/margin/correct/_mode/
  bridge/handler/w_conseq/w_val/menu_/nz_ tokens (shell audit in
  REPORT). Its frozen 3-step drain covers the new N=2 delay.
- world_vt.zag: new SETTLE-DN2 environment (experiment side only).
  Same frozen episode tables and hidden margin rule
  margin = e0+e1-e2 as the sibling family; delay N=2 (not 3); NEW
  noise (seed 109, draws (h mod 5)-2 in {-2,-1,0,1,2}).
  w_sched_ds (returns nothing), w_arrive_ds (consequence C_true +
  noise computed only at step s+2); w_conseq_det (experiment-side
  deterministic immediate oracle for the uniqueness sweep only);
  menu controls.
- driver_vt.zag: new experiment-side driver. Teaches X train+test,
  seeds M0, creates the world state, runs the learner's
  l_experiment (inherit, construct+revise, deploy held-out), dumps
  M/MPREV, runs the experiment-side uniqueness sweep and the NOM
  and MENU arms (menu via experiment-side immediate noisy K-sums),
  runs the K=1 single-sample control arm through the new delayed
  channel, prints the kill-bar summary with the frozen seed-109
  numbers.
- audit_attr_vt.awk: frozen attribution audit (every ATTR line:
  arr - sched == 2, DEPLOY at sched with same tag and same k, no
  ATTR-BAD / ATTR-COUNT-BAD).
- vt_full.zag: concatenation learner_ds+world_vt+driver_vt.
- vt_bin: compiled with pinned znc
  src/tools/toolchain/znc_linux_x86_64_abed8aa1.
- Runs: vt_run1.txt, vt_run2.txt, vt_run3.txt (3/3 byte-identical,
  sha256
  58ac08c8d957a639c58451a889bf018a9960cb5fc5afca008e3a4f6ee4ea6004;
  11,453,048 bytes each; recorded in REPORT.md).

## Commit record

- ad0de3bcf: PREREG.md + NAMECHECK.md alone (frozen,
  pre-implementation; explicit pathspecs).
- (implementation commit): implementation + REPORT.md + NAMECHECK.md
  build-record update (explicit pathspecs; frozen sibling directory
  untouched).
- Nothing pushed; branch tnn-native-lab.
