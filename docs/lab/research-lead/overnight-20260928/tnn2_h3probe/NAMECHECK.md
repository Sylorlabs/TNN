# NAMECHECK.md - H3 Feasibility Prober

## Step 0: Toolchain guard (mandatory)

Executed before any analysis work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` printed with no python3/python paths resolved.
Safebin active for the entire session. No forbidden executable invoked.
This worker is analysis only: no implementation, no compilation, no binary
execution. All source reads were read-only (`sed -n`, `grep -n`, `muse.read`).

## Scope

- Owned path: `docs/lab/research-lead/overnight-20260928/tnn2_h3probe/`
- Read-only inputs: `tnn2_build/tnn2.zag` (frozen TNN-2 source), red-team
  synthesis at commit `42b4dfa91`, alternative-explanation attack at
  commit `ccee9e5e6`, revision generalization analysis at commit
  `edbb0e9b5`, MUL Rung B build report.
- No source edits. No edits outside the owned path. Paper untouched.

## Verdict

H3-FEASIBILITY-PROBE-COMPLETE.
