# NAMECHECK.md -- Invention Hypothesis 3 Worker (Constraint-Driven Novel Form)

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

Worker: Invention Hypothesis 3 (constraint-driven novel form).
Task: test whether TNN can construct a genuinely novel MAP form via
backtracking search guided by goal constraints, where no existing MAP works,
trial cannot produce the form, and the form is source-underdetermined
(determined by goal constraints plus world facts, not by source enumeration).

## Step 2: Base

Unfrozen variant only. Base = `composition_C/cc_base.zag`
(knowledge_composition core: rebind + trial + revision machinery),
lines 1-1677 (everything before `ev_query`). Frozen source read-only,
never modified.

## Step 3: Outputs

- `PREREG.md`: frozen preregistration with kill bars (committed before
  implementation).
- `invent_patch.zag`: invention mechanism + `ev_query` + `ev_query_c`.
- `invent_driver.zag`: 3-problem experiment driver with controls.
- `invent_full.zag` / `invent_full_ni.zag`: assembled sources (one-line diff:
  `invent_on()` 1 vs 0).
- `invent_bin` / `invent_ni_bin`: compiled binaries (pinned znc).
- `invent_run1/2/3.txt`, `invent_ni_run1/2/3.txt`: 3/3 byte-identical
  transcripts per binary.
- `REPORT.md`: full analysis with SUF evaluation.

Pure Zag. Paper untouched. Nothing pushed. 0 modes/bridges/handlers.
No finite menu: the search is constructive backtracking over fact
combinations, not selection from enumerated candidates.
