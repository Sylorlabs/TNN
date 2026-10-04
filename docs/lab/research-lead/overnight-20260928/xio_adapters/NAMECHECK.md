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

- PREREG.md first commit hash: 12e7bc30129b5fa404c0eb209785c97c09cde1a7
  (2026-10-02 14:25:36 UTC). Note: the commit also carried a sibling
  worker's staged prereg pair (meta_applicability_rerun); no xio
  implementation file was in that commit (verified via git show/ls-tree:
  only PREREG.md + NAMECHECK.md under xio_adapters/).
- Implementation files (xio_core.zag, xio_driver.zag) first commit
  hash: (this commit, strictly after 12e7bc301; filled at commit time)
- Self-check: PASS on prereg side (no implementation at or before
  12e7bc301). Final verdict pending the implementation commit.
- Post-stat-fix note: after the first 3/3 green runs, one cosmetic
  fix was applied BEFORE the implementation commit: xio_try now
  records tried/rejected pair counts into header field 16 and
  xio_adapt zeroes it, so Z-line trial stats are honest (previously
  they showed stale stats from the prior trial query). No prereg
  bar covers these stats; mechanism and kill bars unchanged.
  Recompiled, reran 3/3, all bars re-verified.

## Step 4: Build and run log

- Assembly: cat ../composition_A/cx_core.zag xio_core.zag
  xio_driver.zag > xio_full.zag (2096+ lines; cx_core.zag verbatim).
- First compile failed: cx_core.zag's internal test battery
  references ev_query (defined in cx_patch.zag, deliberately not
  included). Resolved by defining ev_query in xio_driver.zag as
  xio_query(...,xio_on=1); battery never invoked.
- Second compile: success, warnings only (same A0102 class as
  sibling workers), binary xio_bin 262527 bytes (pinned znc).
- Runs: 3/3 byte-identical, sha256
  3b10e33ebdbb99d6826b945cd6ffbcb35c99ed17a6f4da3a84fb26d0325c9e98.
- Key trace (TREAT): XIO-BUILD id=380 m1=27 m2=115 o1=0 o2=1
  rel1=81 rel2=82 qr=93 mid=34 ans=2; XIO-REUSE id=380 (Z2a);
  XIO-BUILD id=467 qr=94 mid=74 ans=2 (Z2b).

## Step 5: Kill-bar scorecard

- K1 Z success (Z1=2, one adapter, o1=0 o2=1, mid=34): PASS
- K2 Reuse (Z2a=2 via REUSE, adapters stay 1): PASS
- K3 Generalization (Z2b=2, second adapter qr=94): PASS
- K4 Ablation (ABL-XIO all -2, adapters 0): PASS
- K5 No-MAP controls (ABL-X/ABL-Y/FRESH all -2): PASS
- K6 Competence (14/18/3/4, matches C215): PASS
- K7 Learner-built (census + grep, no table/template): PASS
- K8 Determinism (3/3 identical sha256): PASS
- Verdict: XIO-ADAPTERS-COMPLETE

## Constraints observed

- Pure Zag. Zero em/en dashes in docs, code, and output (byte-checked).
- Paper untouched. Nothing pushed (local commits only).
- 0 modes / 0 bridges / 0 handlers / 0 new core semantic cases.
- No hardcoded type-conversion table; no CHAIN_COUNT template
  (grep-verified before the verdict commit).
- xio_try is a uniform miss-policy stage, not a task mode: attempted on
  any query where lookup+rebind failed and learner state holds a typed
  MAP, with no task-label routing.
