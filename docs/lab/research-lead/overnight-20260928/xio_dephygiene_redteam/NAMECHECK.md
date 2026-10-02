# NAMECHECK: XIO-DEPHYGIENE Red Team (fresh, 2026-10-02)

Worker: TNN red-team worker (watchdog-assigned)
Lane: docs/lab/research-lead/overnight-20260928/xio_dephygiene_redteam/
Prereg: PREREG.md (this lane)
Target: XIO-DEPHYGIENE PASS, ledger C308, commit 5318cbfc9
(prereg c8c811a73, verdict XIO-DEPHYGIENE-COMPLETE)

## Step 0: Toolchain guard (mandatory, executed before any work)

Setup (2026-10-02, session start):

    bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
    export PATH="$HOME/safebin"

Setup output: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python).

Verification (2026-10-02, after setup, before any work):

    which python3; which python; echo done

Result: both return nothing. Neither python3 nor python resolves in
the worker PATH.

Pinned compiler: znc 2026.07.0-dev (edition 2026) via $HOME/safebin/znc,
which resolves to src/tools/toolchain/znc_linux_x86_64_abed8aa1.

Guard re-verified after PREREG.md was written and before the freeze
commit: still empty. Any forbidden-executable invocation is
PROCESS-FAIL per governance; none occurred. All research logic is pure
Zag; shell is used only to invoke the pinned znc, run binaries, git
operations, file moves, hashing, and text comparison.

Stdout discipline per toolchain lesson: the frozen base's own
emit/e64 helpers are used verbatim for all output (no new dynamic
number printer written); no _zag_print for researcher-written dynamic
content. No `as *i32` plus slice construction in functions. The
`as []f64` / `as []i64` .len rule is respected (not used). No
`!(... && ...)` in while conditions (grep-audited before every build).
If-nesting kept at 3 or fewer in new code. All four compiler-defect
workarounds honored.

Target files are COPIES. The C308 committed files
(docs/lab/research-lead/overnight-20260928/xio_dephygiene/*) are never
modified; needed sources are copied into this lane and their hashes
verified against the committed originals before use.

## Namecheck

Toolchain: safebin active, no python. Branch: tnn-native-lab.
Commits stay local, never pushed. Fork caveat honored: the repair
targets the XIO-IDFIX lineage; no fork unification attempted.
Sealed worlds not touched (no sealed-world content inspected except
via the authorized evaluator path, which this lane does not use).
