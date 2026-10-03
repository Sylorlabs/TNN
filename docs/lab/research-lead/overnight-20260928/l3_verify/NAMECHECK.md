# NAMECHECK: L3 Verification Worker

Worker: L3 Verification Worker (subagent, 2026-10-02).
Scope: `docs/lab/research-lead/overnight-20260928/l3_verify/` only.
Prereg: `PREREG.md` (frozen, commit 6467fc547, committed alone before
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
computational work (including the pre-prereg independent table
verification in /tmp/vcheck.zag) done in pure Zag via the pinned znc.
No forbidden executable invoked: no PROCESS-FAIL.

## Build record

- learner.zag: NEW consequence-driven learner (section 3 of PREREG).
  Calls exactly two world-side symbols: w_conseq_train,
  w_conseq_test (aggregate coin oracles). Zero label/expected/margin/
  correct/mode/bridge/handler tokens (shell audit in REPORT).
- world.zag: SETTLE environment; frozen episode tables; hidden margin
  rule margin = e0+e1-e2; coin oracles; menu controls.
- driver.zag: stage protocol (inherit, construct+revise, deploy
  held-out), arms (NOM, MENU), kill-bar summary lines.
- verify_full.zag: concatenation learner+world+driver.
- verify_bin: compiled with pinned znc
  src/tools/toolchain/znc_linux_x86_64_abed8aa1.
- Runs: verify_run1.txt, verify_run2.txt, verify_run3.txt (3/3
  byte-identical, sha256 recorded in REPORT.md).

## Commit record

- 6467fc547: PREREG.md alone (frozen, pre-implementation).
- (implementation commit hash recorded in REPORT.md; explicit
  pathspecs used; nothing pushed; branch tnn-native-lab.)
