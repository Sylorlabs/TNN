# NAMECHECK: XIO DEP-Hygiene Repair (fresh, 2026-10-02)

Worker: TNN research revival worker (watchdog-assigned)
Lane: docs/lab/research-lead/overnight-20260928/xio_dephygiene/
Prereg: PREREG.md (this lane), verdict name XIO-DEPHYGIENE-COMPLETE

## Step 0: Toolchain guard (mandatory, executed before any work)

Setup (2026-10-02, session start):

    bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
    export PATH="$HOME/safebin"

Setup output: SAFEBIN-READY: /home/hatch/safebin (no python).

Verification (2026-10-02T20:17:23Z, after setup, before any work):

    which python3 python 2>/dev/null; echo "which-exit=$?"

Result: empty output, exit 1. Neither python3 nor python resolves in
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
content. No `as *i32` plus slice construction in functions. No
`!(... && ...)` in while conditions (grep-audited). If-nesting kept
at 3 or fewer in new code.

## Namecheck

- Lane directory: docs/lab/research-lead/overnight-20260928/xio_dephygiene/
- Prereg: PREREG.md (kill bars K1-K10, frozen here)
- Repair source: src/dephygiene_core.zag (idfix core + section-2 changes)
- Driver: src/dephy_driver.zag (H0/H1/H2/H34/H5a/H5b, unfrozen)
- Assemblies: dephy_full.zag, dephy_c229.zag, dephy_c235.zag
- Binaries: bin/dephy_full, bin/dephy_c229, bin/dephy_c235
- Harness: build.sh, run.sh, verify.sh (shell only)
- Outputs: outputs/ (run logs, sha256sums)
- Report: REPORT.md

## Prereg ordering attestation

PREREG.md + NAMECHECK.md (this file, Step 0 only) are committed ALONE
in a single commit before any implementation source, driver,
assembly, binary, or run output for this prereg exists. The commit
hash is recorded here after the commit:

- Freeze commit: (recorded post-commit)

The exploratory_uncommitted_20261002/ directory holds the earlier
never-committed pass (retained for provenance, not evidence). No file
outside this lane is modified by this experiment. The paper and
composition_integration/ are untouched.

## Red lines observed

No em or en dashes in deliverable documentation (audited by
worker_snippets/check_no_dash.sh before the freeze commit). Paper
untouched. Nothing pushed (commits local only). Frozen artifacts
read-only (frozen base extracted per assembly and cmp-verified, never
edited). Zero new modes/bridges/handlers (audited in verify.sh, K10).
