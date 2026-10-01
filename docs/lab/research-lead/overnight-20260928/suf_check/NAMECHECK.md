# NAMECHECK.md -- SUF Checker

## Step 0: Toolchain guard (mandatory)

Executed before any work:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned nothing. Safebin active. Zero forbidden
executables invoked. All computation was file reads (`read`, `grep`, `sed`)
and file writes only.

## Scope

Apply the 4-step SUF operational test (from PROPERTY_DEFINITION.md, commit
`64eec921f`) to TNN-2's three mechanisms: construction, inquiry, revision.

## Method

Read-only inspection of the frozen TNN-2 source
(`docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`, SHA-256
prefix `a29972ca8183b285`, verified against the frozen build record before
reading). No source edits, no binaries executed, no worlds run. Line numbers
below refer to that file. The DOF map (commit `d2af26581`) was used as the
decision-enumeration template, per the SUF definition's own instruction.

## Verdict discipline

Each mechanism: list structural decisions (Step 1), classify each as
(a) source-enumerable or (b) source-underdetermined (Step 2), report whether
the (b) list is nonempty (Step 3), construct the source-only enumeration as a
negative control (Step 4), deliver SUF PASS or SUF FAIL.

## Constraints honored

Owned path only (`docs/lab/research-lead/overnight-20260928/suf_check/`).
Check only, no implementation. No em dashes (byte-verified zero). The research
paper untouched. Nothing pushed.
