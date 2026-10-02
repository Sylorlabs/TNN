# NAMECHECK.md -- Composition Hypothesis C Worker

## Step 0: Toolchain guard (mandatory)

Executed at startup:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returns nothing. `guard-check-done` printed.
Safebin active for all subsequent commands. Zero forbidden executables invoked.

## Step 1: Identity

Worker: Composition Hypothesis C (constraint-driven assembly).
Task: test whether TNN can compose X+Y->Z by matching MAP structural
properties (relation sequences extracted from executable graphs) against
goal-derived constraints, with no paired examples, no hint, no task label.

## Step 2: Base

Unfrozen variant only. Base = `knowledge_composition/kc_core.zag`
(persistent-connections variant: rebind + LINK14), lines 1-1677
(everything before `ev_query`). Frozen source read-only, never modified.

## Step 3: Outputs

- `cc_patch.zag`: composition mechanism + new `ev_query`
  (compose_try hooked between rebind_try and trial).
- `cc_driver.zag`: 5-arm experiment driver.
- `cc_full.zag` / `cc_full_nc.zag`: assembled sources (one-line diff:
  `compose_on()` 1 vs 0).
- `cc_bin` / `cc_nc_bin`: compiled binaries (pinned znc).
- `cc_run1/2/3.txt`, `cc_nc_run1/2/3.txt`: 3/3 byte-identical transcripts.
- `REPORT.md`: full analysis.

Pure Zag. Paper untouched. Nothing pushed. 0 modes/bridges/handlers.
