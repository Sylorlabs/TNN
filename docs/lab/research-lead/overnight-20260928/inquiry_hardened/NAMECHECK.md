# NAMECHECK: Inquiry Hardening Worker

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
(same pinned binary used by the advteacher worker).

Status: GUARD PASS. Any forbidden executable invocation would be
PROCESS-FAIL; none occurred.

## Step 1: Prereg commit order

PREREG.md committed BEFORE any implementation (this commit). The
implementation commit strictly follows. Verified via git log order.

## Step 2: Source provenance

- h_base.zag: byte copy of
  `inquiry_advteacher/a_base.zag` (SHA-256
  a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd),
  UNMODIFIED.
- h_patch.zag: starts as byte copy of
  `inquiry_advteacher/a_patch.zag` (SHA-256
  1c88c5d9afdbf06b2370e6e140547b24cdb8fc7002e7019d74d086c1b37d6de9);
  hardening edits applied AFTER the prereg commit, recorded in REPORT.md.
- h_driver.zag: new hardened driver (teachers copied from the
  preregistered adversarial teachers; inquiry loop replaced with the
  provenance plus corroboration plus waste-budget loop).
- Frozen dirs `grammar_inquiry/` and `inquiry_advteacher/` untouched
  (read-only). Paper untouched. Nothing pushed.

## Step 3: Determinism

3/3 runs byte-identical; SHA-256 recorded in h_run1/2/3.txt and REPORT.md.

## Step 4: Modes/bridges/handlers

0. All learner additions and all teachers are plain functions. No new
opcodes, no semantic cases, no task-specific gates.
