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

- h_base_nomain.zag: byte copy of
  `inquiry_hardened/h_base_nomain.zag` (SHA-256
  b63cce0403a4e3a321dfaf0bc366ded1bfe39b876f082affe5b4861b66f85210),
  verified by cmp, UNMODIFIED.
- h_patch.zag: byte copy of `inquiry_hardened/h_patch.zag` (SHA-256
  d67f909e9961abe46ad0f263379850521babd2a030ebfc528d3c56cfd88e58fb),
  verified by cmp, UNMODIFIED. The hardened mechanism is the target;
  it was not modified.
- adv_driver.zag: new adversary driver (four adversarial teachers
  a2_teacher_answer, world loop a2_world, provenance spoof audit
  a2_spoof_check; NEG-AMB teaching, grammar reporting, and battery
  snippets copied verbatim from h_driver.zag).
- adv_build.sh: assemble plus pinned-znc compile script.
- Frozen dirs `grammar_inquiry/`, `inquiry_advteacher/`,
  `inquiry_hardened/` untouched (read-only). Paper untouched. Nothing
  pushed.

## Step 3: Determinism

3/3 runs byte-identical; SHA-256
8159122b40c4af251450c54f4393809d57672e45a98740086cc01bec1d0eb4d1
recorded in adv_run1/2/3.txt and REPORT.md.

## Step 4: Modes/bridges/handlers

0. All teachers and the driver are plain functions. No new opcodes, no
semantic cases, no task-specific gates. The hardened learner gained 0
cognition lines (unmodified).
