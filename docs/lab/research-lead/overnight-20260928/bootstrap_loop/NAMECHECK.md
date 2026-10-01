# NAMECHECK: Bootstrap Loop Prober

## Step 0: Toolchain guard

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
Result: `guard-check-done` with no python3/python paths printed. Safebin active.
Zero forbidden executables invoked in this wave. All computation in pure Zag
via the pinned compiler `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
Shell used only to invoke znc, run the binary, git ops, and move/copy files.

## Scope

EXPERIMENT. Tests the teach-observe prediction (`8744796fb`): bootstrap teaches
its own inferred value as a FACT, later bootstrap scans count it as an
"observation", so the k=3 threshold's evidence base becomes progressively
self-referential until the scan window contains zero externally-grounded
observations (circular confidence loop).

## Lineage

- Frozen source: `docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag`
  SHA-256 `a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd`
  verified before copying. Frozen source, binary, and build NEVER modified
  (hash re-verified at end).
- `bl_base.zag`: verbatim copy of frozen source (SHA-256 identical, verified).
- `bl_full.zag`: `bl_base.zag` with the original test `main` (line 1357,
  `fn main()i32 { return run_all(); }`) removed and `bl_driver.zag` appended.
  Cognition code (lines 1-1356, 1358-1591) byte-identical to frozen.
- `bl_bin`: compiled from `bl_full.zag` with the pinned znc.

## Constraints

- UNFROZEN VARIANT ONLY. Frozen TNN-2 untouched.
- Pure Zag. Zero em dashes in deliverables (byte-verified).
- Paper untouched. No sealed worlds opened. Nothing pushed.
- 3/3 byte-identical runs required.
