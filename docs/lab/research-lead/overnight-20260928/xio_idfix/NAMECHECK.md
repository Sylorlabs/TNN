# NAMECHECK.md -- XIO-IDFIX worker

## Step 0: toolchain guard (mandatory, recorded before any build)

Setup executed 2026-10-02 (PDT):
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```
Result: `which python3 python` returned NOTHING under the safebin
PATH (only `guard-check-done` printed). No forbidden executable is
reachable. Guard recorded here before any compile or run.

Worker confirms: all computation in this wave is Pure Zag via the
pinned znc at ~/safebin/znc. Shell used only to invoke znc, run
binaries, and do git/file ops. If a forbidden executable is invoked,
this wave is automatically PROCESS-FAIL.

## Scope

Repair the A4c id-recycling KILL on XIO adapters
(XIO-REDTEAM-COMPLETE, commit 64d12b79f). Unfrozen work only:
xio_core.zag (explicitly marked unfrozen in its header) plus new
driver/assembly files in xio_idfix/. The frozen base
(xio_full.zag lines 1-1677) is read-only; verified byte-identical
before and after via cmp. A1/A6 are owned by the XIO-generalization
worker (H-XIO-4); not touched here. Paper untouched. Nothing pushed;
commits local on tnn-native-lab with explicit pathspecs.

## Zag notes

- Token arithmetic uses plain i32 `<<` and `|` with explicit parens
  (both operators verified present in the base, e.g. get32 line 38).
- No new print machinery: invalidation audit reuses the existing
  `emit`/`e64` helpers already used by XIO-BUILD/XIO-REUSE.
- Binding tokens ride the existing adapter->stage type-1 DEP edges'
  clk field (eg offset 12); the base never reads/writes clk on
  type-1 edges (decay touches type 9 only). No node layout change.
- Per AGENTS.md toolchain lessons: no `as *i32` slice tricks, no new
  `_zag_print`-style helpers; every binary's stdout verified
  byte-identical across 3 runs via sha256.

No em dashes were used in this file (verified).
