# NAMECHECK: Weak K-LT-5 Clean Sealed Test

## Step 0: Toolchain Guard

Date: 2026-10-01.
Worker: Node1 Clean Sealed Test Builder.

Guard activation (run at task start):
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING. `guard-check-done` printed.
`znc` resolves via safebin to the pinned toolchain binary.

Scope: This worker builds a FRESH prereg, FRESH sealed world, and runs the
clean weak K-LT-5 evaluation. All research computation in pure Zag via the
pinned `znc`. Shell used only to invoke znc, run binaries, do git operations,
and move/copy files. Zero Python invocations. Zero em/en dashes in docs.

## Step 1: Input Provenance

- Prior VOID evaluation: commit `c040e5fde` (report WEAK_KLT5_EVAL.md). Read for
  mechanism understanding and budget numbers only. Its sealed world is NOT
  reused. Its world contents are NOT reproduced here.
- H3-lite Node 1 implementation: `docs/lab/research-lead/overnight-20260928/h3lite_node1/`
  (report H3LITE_NODE1.md, source h3n1_base.zag, h3n1_funcs.zag). Frozen
  cognition is used verbatim; the Node-1 variant is the unfrozen build from
  `45c55ed83` lineage as in the prior eval.
- Frozen prereg `weak_klt5/WEAK_KLT5_PREREG.md`: superseded by the fresh prereg
  in this directory. The order discrepancy ([2,1,0,3,4,5] text vs [0,1,2,3,4,5]
  actual) is resolved by specifying the ACTUAL built order.

## Step 2: Independence

This worker did not build H3-lite Node 1. The fresh sealed world is designed
by this worker to the fresh prereg's functional requirements (R1-R5). The
world is sealed by SHA-256 before any evaluation binary runs against it.

## Step 3: Commit Discipline

Explicit pathspecs on both `git add` and `git commit`. No sweep-in.
Prereg committed (frozen) BEFORE world construction. World sealed (hash
recorded) BEFORE evaluation. Nothing pushed. Paper untouched.
