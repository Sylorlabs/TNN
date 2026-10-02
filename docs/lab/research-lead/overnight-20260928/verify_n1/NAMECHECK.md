# NAMECHECK: Verify N1 Worker

Worker: Verify N1 Worker (subagent, 2026-10-02).
Scope: `docs/lab/research-lead/overnight-20260928/verify_n1/`
only. The frozen sibling directories `l3_delayed_stochastic/` and
`verify_transfer/` are read-only; `learner_ds.zag` will be a
byte-identical copy of `verify_transfer/learner_ds.zag`, never
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
/tmp/n1check.zag and the awk attribution audit, which is a log check,
not research logic) done with safebin tools and pure Zag via the
pinned znc. No forbidden executable invoked: no PROCESS-FAIL.

## Build record

- learner_ds.zag: BYTE-IDENTICAL COPY of the frozen
  `verify_transfer/learner_ds.zag` (sha256
  45ad35d892d629971a4679ffd2085b8bd54bf9c328d1e8eb1cededcc3ef3ae65;
  `cmp` clean). NOT modified, NOT rewritten, NOT adapted. Calls
  exactly two world-side symbols: w_sched_ds, w_arrive_ds (delayed
  noisy consequence channel). Per-step ledger records (tag, cand,
  thri, k); arrivals attributed by schedule step, never by recency;
  each threshold score is a sum of exactly K attributed arrivals
  (count-verified). Zero label/expected/w_tab/margin/correct/_mode/
  bridge/handler/w_conseq/w_val/menu_/nz_ tokens (shell audit in
  REPORT). Its frozen 3-step drain covers the N=1 delay with two
  spare polls.
- world_dn1.zag: new SETTLE-DN1 environment (experiment side only).
  Same frozen episode tables and hidden margin rule
  margin = e0+e1-e2 as the sibling family; delay N=1 (the only
  behavioral change from SETTLE-DN2: w_arrive_ds returns the
  deployment scheduled at step-1); SAME noise (seed 109, draws
  (h mod 5)-2 in {-2,-1,0,1,2}). w_sched_ds (returns nothing),
  w_arrive_ds (consequence C_true + noise computed only at step s+1);
  w_conseq_det (experiment-side deterministic immediate oracle for
  the uniqueness sweep only); menu controls.
- driver_dn1.zag: new experiment-side driver (mirrors driver_vt).
  Teaches X train+test, seeds M0, creates the world state, runs the
  learner's l_experiment (inherit, construct+revise, deploy held-out),
  evaluates NOM/MENU arms, runs the K=1 single-sample control arm
  through the N=1 delayed channel, runs the experiment-side
  uniqueness sweep, prints the kill-bar summary with N1 markers and
  the frozen seed-109 numbers.
- audit_attr_n1.awk: frozen attribution audit (every ATTR line:
  arr - sched == 1, DEPLOY at sched with same tag and same k, no
  ATTR-BAD / ATTR-COUNT-BAD).
- n1_full.zag: concatenation learner_ds+world_dn1+driver_dn1.
- n1_bin: compiled with pinned znc
  src/tools/toolchain/znc_linux_x86_64_abed8aa1.
- Runs: n1_run1.txt, n1_run2.txt, n1_run3.txt (3/3 byte-identical,
  sha256
  2aa06398cc3b0a25f4b8727ab1cb5c059843396d7b325bc6b88c8bdcb64b20fc;
  11,453,048 bytes each; recorded in REPORT.md).

Pre-prereg independent check: /tmp/n1check.zag (pure Zag, separate
code path, no delay, no channel) re-derived every frozen number
before PREREG.md was written; all matched the VERIFY-TRANSFER
numbers exactly.

## Commit record

- eb2c03f8c: PREREG.md + NAMECHECK.md alone (frozen,
  pre-implementation; explicit pathspecs).
- c3b2da062: implementation + REPORT.md + NAMECHECK.md build-record
  update (explicit pathspecs; frozen sibling directories untouched).
- Nothing pushed; branch tnn-native-lab.
