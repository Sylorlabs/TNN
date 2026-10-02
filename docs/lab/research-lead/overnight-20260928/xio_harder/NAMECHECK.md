# NAMECHECK.md -- H-XIO-2 Harder-Pair Worker

## Step 0: Worker toolchain guard (mandatory, recorded at startup)

Executed before any other work, 2026-10-02 ~07:33 PDT:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` printed NOTHING (no output before
"guard-check-done"). No forbidden executable resolves in PATH.
Safebin active: /home/hatch/safebin (znc resolves to the pinned
/home/hatch/safebin/znc, version 2026.07.0-dev). Toolchain
verification: PASS.

All computation in this wave is pure Zag (znc) plus POSIX shell
utilities for assembly, hashing, and git. No Python, no C, no other
interpreters. If any forbidden executable is invoked, this wave is
automatically PROCESS-FAIL.

## Step 1: Task and verdict

XIO Harder-Pair Worker (H-XIO-2, P0). Mission: test whether the XIO
typed I/O adapter mechanism (H-XIO-1, C229) generalizes UNCHANGED to
the harder cross-domain pair (transform-then-navigate, d09995951):
X = COUNT (oty 1), Y = CHAIN on numeric subjects (oty 0),
Z = Y(X(s)) with computed intermediate k=4. Target verdict:
XIO-HARDER-COMPLETE (with handoff analysis).

Key challenge from the xdomain-harder worker: the intermediate k=4 is
a COMPUTED NUMBER, not a fact-store node; Y's chains must be
re-subjected to it. Test: does the unmodified staged execution handle
the number to subject handoff?

## Step 2: Frozen vs unfrozen inventory

FROZEN (read-only, never modified):
- docs/lab/research-lead/overnight-20260928/composition_A/cx_core.zag
  (TNN-2 integration base: world layout, 4-op ISA, execute(), trial,
  rebind, teach/query primitives)
- docs/lab/research-lead/overnight-20260928/xio_adapters/xio_core.zag
  (the C229 adapter mechanism: xio_oty, xio_dep_rel, xio_stage_exec,
  xio_try, xio_build, xio_exec, xio_find, xio_adapt, xio_query)
  sha256 at freeze time:
  4d4d2e0e932b6a472e3cd8456d7e1c633218e611ce5df51d03507218440a8a7f
  This file is REFERENCED by the assembly recipe, never copied,
  never edited. Zero adapter-mechanism changes is a frozen claim.
- everything else outside xio_harder/

UNFROZEN (this worker's new files, all under xio_harder/):
- PREREG.md (frozen FIRST, this wave's kill bars K1-K8 + handoff
  signatures S1-S4)
- NAMECHECK.md (this file)
- REPORT.md (written after runs)
- xhio_driver.zag (new: harder-pair world, arms, census, main;
  the ONLY new source this wave)
- xhio_full.zag (assembled input: cx_core.zag + xio_core.zag +
  xhio_driver.zag, both bases verbatim)
- xhio_bin (compiled binary, pinned znc)
- xhio_run1.txt, xhio_run2.txt, xhio_run3.txt (3/3 outputs)
- xhio_compile.txt (compiler output)

Assembly recipe:
```
cd docs/lab/research-lead/overnight-20260928/xio_harder
export PATH="$HOME/safebin"
cat ../composition_A/cx_core.zag ../xio_adapters/xio_core.zag xhio_driver.zag > xhio_full.zag
znc xhio_full.zag -o xhio_bin 2> xhio_compile.txt
./xhio_bin > xhio_run1.txt; ./xhio_bin > xhio_run2.txt; ./xhio_bin > xhio_run3.txt
sha256sum xhio_run1.txt xhio_run2.txt xhio_run3.txt
```

## Step 3: Prereg commit-order self-check (filled at commit time)

- PREREG.md first commit hash: (filled at commit time)
- Implementation file (xhio_driver.zag) first commit hash: (filled at
  commit time; must be strictly after the prereg commit)
- Self-check: (filled at commit time)

## Step 4: Build and run log (filled after runs)

## Step 5: Kill-bar scorecard (filled after runs)

## Constraints observed

- Pure Zag. Zero em/en dashes in docs, code, and output (byte-checked).
- Paper untouched. Nothing pushed (local commits only).
- 0 modes / 0 bridges / 0 handlers / 0 new core semantic cases.
- No hardcoded type-conversion table; no COUNT_CHAIN / CHAIN_COUNT
  pair template (grep-verified before the verdict commit).
- xio_try is a uniform miss-policy stage, not a task mode.
