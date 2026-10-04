# NAMECHECK: Per-Candidate Applicability Worker

## Step 0: toolchain guard (2026-10-02, before any work)

Safebin activation executed at session start:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` printed nothing; only `guard-check-done`.
No forbidden executable is reachable in the worker PATH. All subsequent
commands in this task run with `export PATH="$HOME/safebin"`. Pure Zag
for all research logic (compiler: the pinned znc used by the rerun).

## Step 1: identity

- Task: Per-Candidate Applicability Worker (per-MAP applicability
  judgments, next frontier from the meta-applicability rerun K3
  analysis).
- Work dir: `docs/lab/research-lead/overnight-20260928/applicability_permap/`
  under `~/workspace/tnn-rsi` (branch `tnn-native-lab`).
- Base sources: verbatim copies of the rerun's unfrozen sources
  (`ma_base.zag` with the t2 reclaim fix, `ma_patch.zag` problem-level
  APPL, `ma_driver.zag`). The frozen TNN-2 base is read-only and
  untouched.

## Step 2: ordering

- PREREG.md frozen and committed BEFORE the per-candidate
  implementation is written, built, or run: prereg-alone commit
  1403e0b57 (2026-10-02), explicit pathspecs, verified
  `git show --stat HEAD` lists only the two prereg files.
- Control arms (TREAT/NAIVE/FRESH) rebuild the rerun sources verbatim;
  their output hashes must match the frozen rerun hashes or the setup
  change is reported and the comparison voided.

## Step 3: verdict rule

Verdict APPLICABILITY-PERMAP-COMPLETE requires P1-P8 all PASS. Any bar
failed: verdict is FAIL with the bar named, no reinterpretation.
