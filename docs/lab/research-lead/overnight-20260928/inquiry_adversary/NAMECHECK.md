# NAMECHECK: Inquiry Adversary Worker

## Step 0: Toolchain guard (mandatory, recorded before any work)

Safebin setup executed 2026-10-02:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned EMPTY (no output before
`guard-check-done`). PATH=/home/hatch/safebin. No forbidden executable
in PATH. Pure Zag for all computational research operations; shell only
for invoking znc, running binaries, git ops, moving/copying files.

Toolchain: pinned znc at
`$HOME/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(same pinned binary used by the hardening worker).

Status: GUARD PASS. Any forbidden executable invocation would be
PROCESS-FAIL; none occurred.

## Step 1: Prereg commit order

PREREG.md committed BEFORE any implementation (this commit). The
implementation commit strictly follows. Verified via git log order.

## Step 2: Source provenance

(TBD after implementation: SHA-256 of the byte copies plus cmp
verification against inquiry_hardened/.)

## Step 3: Determinism

(TBD after runs: 3/3 byte-identical, SHA-256 recorded.)

## Step 4: Modes/bridges/handlers

(TBD: expected 0; teachers and driver are plain functions; the hardened
mechanism is not modified.)
