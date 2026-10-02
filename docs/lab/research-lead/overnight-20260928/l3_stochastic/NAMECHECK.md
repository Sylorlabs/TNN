# NAMECHECK: L3 Stochastic Worker

Worker: L3 Stochastic Worker (subagent, 2026-10-02).
Scope: `docs/lab/research-lead/overnight-20260928/l3_stochastic/` only.
Prereg: `PREREG.md` (frozen, commit 68c590d32, committed alone before
any implementation existed; zero amendments).

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
computational work (including the pre-prereg independent check in
/tmp/scheck.zag: direct value formulas, seed search, frozen-number
derivation, register-machine cross-check XCHECK-BAD=0) done in pure
Zag via the pinned znc. No forbidden executable invoked: no
PROCESS-FAIL.

## Build record

- learner_s.zag: NEW noisy-consequence learner (section 3 of PREREG).
  Calls exactly two world-side symbols: w_conseq_train_nz,
  w_conseq_test_nz (K-sample noisy aggregate coin oracles). Zero
  label/expected/w_tab/margin/correct/_mode/bridge/handler tokens and
  zero references to the deterministic oracles (shell audit in
  REPORT).
- world_s.zag: SETTLE-NZ environment; frozen episode tables (same as
  l3_verify); hidden margin rule margin = e0+e1-e2; seeded
  counter-based noise (seed 7000, draws in {-1,0,1}); the two noisy
  oracles; menu controls.
- driver_s.zag: stage protocol (inherit, construct+revise K=64,
  single-sample K=1 control, deploy held-out), arms (NOM, MENU),
  kill-bar summary lines.
- stochastic_full.zag: concatenation learner_s+world_s+driver_s.
- stochastic_bin: compiled with pinned znc
  src/tools/toolchain/znc_linux_x86_64_abed8aa1.
- Runs: stochastic_run1.txt, stochastic_run2.txt, stochastic_run3.txt
  (3/3 byte-identical, sha256 recorded in REPORT.md).

## Commit record

- 68c590d32: PREREG.md alone (frozen, pre-implementation).
- TBD: implementation (explicit pathspecs; nothing pushed; branch
  tnn-native-lab).
