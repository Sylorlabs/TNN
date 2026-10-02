# NAMECHECK.md -- H-XIO-1 Typed I/O Adapter Worker

## Step 0: Worker toolchain guard (mandatory, recorded at startup)

Executed before any other work, 2026-10-02 ~07:20 PDT:

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
/home/hatch/safebin/znc). Toolchain verification: PASS.

All computation in this wave is pure Zag (znc) plus POSIX shell
utilities for assembly, hashing, and git. No Python, no C, no other
interpreters. If any forbidden executable is invoked, this wave is
automatically PROCESS-FAIL.

## Step 1: Task and verdict

Typed I/O Adapter Worker (H-XIO-1, P0). Mission: learner-built typed
I/O adapters to rescue cross-domain composition (C215 clean negative).
Target verdict: XIO-ADAPTERS-COMPLETE (with adapter reuse and ablation
evidence).

## Step 2: Frozen vs unfrozen inventory

FROZEN (read-only, never modified, included verbatim where needed):
- docs/lab/research-lead/overnight-20260928/composition_A/cx_core.zag
  (TNN-2 integration base: world layout, 4-op ISA, execute(), trial,
  rebind, teach/query primitives)
- everything else outside xio_adapters/

UNFROZEN (this worker's new files, all under xio_adapters/):
- PREREG.md (frozen FIRST, this wave's kill bars K1-K8)
- NAMECHECK.md (this file)
- REPORT.md (written after runs)
- xio_core.zag (adapter machinery: xio_oty, xio_dep_rel,
  xio_stage_exec, xio_try, xio_build, xio_exec, xio_find,
  xio_adapt, xio_query)
- xio_driver.zag (world, arms, census, main)
- xio_full.zag (assembled input: cx_core.zag + xio_core.zag +
  xio_driver.zag)
- xio_bin (compiled binary, pinned znc)
- xio_run1.txt, xio_run2.txt, xio_run3.txt (3/3 outputs)
- xio_compile.txt (compiler output)

Assembly recipe:
```
cd docs/lab/research-lead/overnight-20260928/xio_adapters
export PATH="$HOME/safebin"
cat ../composition_A/cx_core.zag xio_core.zag xio_driver.zag > xio_full.zag
znc xio_full.zag -o xio_bin 2> xio_compile.txt
./xio_bin > xio_run1.txt; ./xio_bin > xio_run2.txt; ./xio_bin > xio_run3.txt
sha256sum xio_run1.txt xio_run2.txt xio_run3.txt
```

## Step 3: Prereg commit-order self-check

- PREREG.md first commit hash: (filled below after commit)
- Implementation files (xio_core.zag, xio_driver.zag) first commit
  hash: (filled below; MUST be strictly after the prereg commit)
- Self-check: PASS / FAIL (filled below)

No implementation file may exist in git history at or before the
prereg commit. Working-tree scratch before the prereg commit is
allowed only if never committed; this worker wrote NO implementation
before the prereg commit (only PREREG.md and NAMECHECK.md exist).

## Step 4: Build and run log

(filled as the wave proceeds)

## Step 5: Kill-bar scorecard

(filled from runs; see REPORT.md)

## Constraints observed

- Pure Zag. Zero em/en dashes in docs, code, and output (byte-checked).
- Paper untouched. Nothing pushed (local commits only).
- 0 modes / 0 bridges / 0 handlers / 0 new core semantic cases.
- No hardcoded type-conversion table; no CHAIN_COUNT template
  (grep-verified before the verdict commit).
- xio_try is a uniform miss-policy stage, not a task mode: attempted on
  any query where lookup+rebind failed and learner state holds a typed
  MAP, with no task-label routing.
