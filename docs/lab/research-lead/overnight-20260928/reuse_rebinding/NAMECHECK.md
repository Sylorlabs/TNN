# NAMECHECK: reuse_rebinding (Reuse-Rebinding Experiment Builder)

## Step 0: Toolchain guard (mandatory, recorded first)

Activation performed at worker start:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `guard-check-done` with no python3/python paths printed.
`which python3` and `which python` return nothing under the safebin PATH.

## Scope

- UNFROZEN VARIANT ONLY. Frozen TNN-2 source is read-only.
- `rb_base.zag` is a verbatim copy of the frozen base; SHA-256 verified
  `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  before any work.
- The rebinding mechanism lives in `rb_patch.zag` (treatment only).
  The control binary uses the verbatim base with no patch.
- Pure Zag via the pinned compiler
  `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
- Shell used only to invoke znc, run binaries, do git operations,
  and move/copy files.
- Zero em/en dashes in all loop documentation (byte-verified).
- No sealed worlds touched. Paper untouched. Nothing pushed.

## Forbidden-executable check

No python3, python, or other forbidden interpreter was invoked at any
point. Any such invocation would have made this wave PROCESS-FAIL.

## Input provenance

- Frozen base: `docs/lab/research-lead/overnight-20260928/decline_gate/dg_base.zag`
  (verbatim frozen TNN-2, hash above).
- Trial/MAP mechanics studied from the same file (t2_trial, promote_graph,
  t2_asm_chain, t2_try_verify, activate, ev_query).
- Task: parent-agent directive 2026-10-01 (reuse-rebinding experiment;
  Micah's cross-domain transfer directive).
