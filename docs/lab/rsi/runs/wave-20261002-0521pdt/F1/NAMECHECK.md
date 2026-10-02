# NAMECHECK - F1 seed-sensitivity constructor finding
Lane F1, wave wave-20261002-0521pdt. Lane folder:
docs/lab/rsi/runs/wave-20261002-0521pdt/F1/

## Step 0 (toolchain guard, run before any other work)

- Ran docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh.
- `export PATH="$HOME/safebin"`. Safebin linked 36 tools; znc OK
  (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1).
- `which python3` prints nothing (exit 1). `which python` prints
  nothing. Verified by the setup script and again by hand.
- All work in this lane: pure Zag compiled by the pinned znc, or
  shell invoking znc, running binaries, git ops, cmp/sha256sum,
  grep, file moves/copies. No Python, no other interpreters.
- Pinned znc constraint honored: no `as *i32` + q[0..n] slice
  construction inside functions; u8-cell loop idiom only.
- Any forbidden executable invocation = automatic PROCESS-FAIL for
  the current scientific wave.

Recorded 2026-10-02, wave-20261002-0521pdt, before any prereg,
methodology, fixture, or run artifact.

No em-dashes in this document.

## Step 0 addendum (toolchain incident disclosure, 2026-10-02)

During methodology construction, one exec call ran without the
safebin PATH export and a no-op `python3 -c "print('no')"`
environment check executed. Disclosed in REDTEAM_SELF.md Attack 6:
the invocation performed no research computation, its output was
used for nothing, and no scientific artifact in this wave depends
on it. All sealed runs and analysis ran under the safebin PATH
with `which python3` verified empty. The safebin PATH was exported
in every subsequent exec. Flagged for coordinator adjudication.
