# NAMECHECK.md — Reuse Path Experimenter

## Step 0: Toolchain Guard

**Date:** 2026-10-01 (UTC)
**Worker:** Reuse Path Experimenter (subagent)

### Safebin Activation
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```
**Result:** `guard-check-done` with no python3/python output. Zero forbidden executables invoked.

### UNFROZEN VARIANT Declaration

This worker creates and experiments with an **UNFROZEN VARIANT** of TNN-2.

- **Frozen source:** `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
  (SHA-256: `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`)
  **NOT MODIFIED.** Verified by diff: the frozen file is untouched.
- **Frozen binary:** `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2_bin`
  **NOT MODIFIED, NOT REBUILT.**
- **Variant source:** `docs/lab/research-lead/overnight-20260928/reuse_experiment/tnn2_reuse_variant.zag`
  This is a COPY with two researcher-authored modifications (see below).
- **Variant binary:** `docs/lab/research-lead/overnight-20260928/reuse_experiment/tnn2_reuse_variant_bin`
  Built from the variant source with the pinned znc.

Per Micah's ruling: "try stuff unfrozen as you go on as thats what i imagine
TNN being in production." This is an experiment, NOT a TNN-3 implementation.
No frozen bars govern it. No ledger claims are made.

### Variant Modifications (vs frozen tnn2.zag)

1. **`promote_graph` (line 541):** Deleted `ev_teach_in(W,s,r,ans);`
   (the shadow teach). Replaced with a comment. The MAP becomes the
   promoted artifact; no exact-match fact shadows it.

2. **`ev_query` (after line 814):** Inserted 19-line MAP-first lookup:
   scan live tag-20 MAPs for (s,r), most-recent wins by field24,
   execute via `t2_exec`, on success do activate-equivalent bookkeeping
   and return, on -999999 fall through to the existing fact path.
   Includes white-box instrumentation: `hg(W,32)` counts MAP-branch
   executions.

Total cognition delta: 19 lines added, 1 line replaced with comment.
Zero new modes, bridges, handlers, semantic cases, opcodes.

### Scope

- Experiment ONLY on the unfrozen variant.
- White-box inspection per Micah's instruction ("TNN should stay a white
  box architecture if you need to find something use the white box").
- Pure Zag for all research logic. Shell only for znc invocation, git,
  file operations.
- No em dashes in documentation.
- Paper untouched. Nothing pushed.

## Verdict Discipline

This worker reports REUSE-EXPERIMENT-COMPLETE with white-box evidence.
It does NOT claim C0-D satisfaction, L3, SUF, or any TNN-3 bar passage.
The honest finding (see REUSE_EXPERIMENT.md): the reuse path works
mechanically (MAPs execute on re-query, no shadow facts), but cross-subject
transfer still rebuilds rather than invokes (value-trace limitation intact,
as the design predicted).
