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

## Step 3: Prereg commit-order self-check

- PREREG.md first commit hash:
  bea72f336d107f14e943922eeb224e3d58e8e262
  (2026-10-02 14:38:42 UTC). Verified via git show/ls-tree: that
  commit contains ONLY PREREG.md + NAMECHECK.md under xio_harder/
  (no driver, no binary, no run outputs).
- Implementation file (xhio_driver.zag) first commit hash: (this
  commit, strictly after bea72f336; filled at commit time)
- Self-check: PASS on prereg side (no implementation at or before
  bea72f336). Final verdict pending the implementation commit.

## Step 4: Build and run log

- Assembly: cat ../composition_A/cx_core.zag
  ../xio_adapters/xio_core.zag xhio_driver.zag > xhio_full.zag
  (2130 lines; both bases verbatim, zero edits).
- Core reuse verified: sha256 of ../xio_adapters/xio_core.zag is
  4d4d2e0e932b6a472e3cd8456d7e1c633218e611ce5df51d03507218440a8a7f,
  identical to the value recorded at freeze time (Step 2). The
  adapter mechanism was not copied, forked, or edited: the assembly
  recipe references the sibling file directly.
- Compile: success, warnings only (171 warning lines, same A0102
  ignored-return-value class as sibling workers; the em dashes in
  xhio_compile.txt are znc's own warning text, also present 162x in
  the sibling's compile log). Binary xhio_bin 268371 bytes
  (pinned znc 2026.07.0-dev).
- The cx_core.zag internal test battery references ev_query; as in
  H-XIO-1, the driver defines ev_query as xio_query(...,xio_on=1).
  The battery is never invoked.
- Runs: 3/3 byte-identical, sha256
  6909ba0c576b3204c110e259411cbb71970f3caa39912f812a2d7761188ab51a.
- Key trace (TREAT, identical all 3 runs):
  XIO-BUILD id=214 m1=44 m2=96 o1=1 o2=0 rel1=81 rel2=82 qr=93
  mid=4 ans=52
  (m1=44: learner-promoted count MAP r=91 s=11; m2=96:
  learner-promoted chain MAP r=92 s=3; mid=4 is the computed
  number-to-subject handoff value)
  XIO-REUSE id=214 ans=52 (Z2a)
  XIO-BUILD id=313 m1=44 m2=96 o1=1 o2=0 rel1=81 rel2=82 qr=94
  mid=3 ans=32 (Z2b)

## Step 5: Kill-bar scorecard

- K1 Z success (Z1=52, one adapter, o1=1 o2=0, rel1=81 rel2=82,
  qr=93, mid=4, tried=1 rejected=0): PASS
- K2 Reuse (Z2a=52 via XIO-REUSE id=214, adapters stay 1): PASS
- K3 Generalization (Z2b=32 via second adapter qr=94 mid=3,
  adapters become 2): PASS
- K4 Ablation (ABL-XIO Z1=Z2a=Z2b=-2, adapters 0; d09995951
  negative reproduced): PASS
- K5 No-MAP controls (ABL-X/ABL-Y/FRESH all -2, adapters 0): PASS
- K6 Competence (X1=3, X2=2, Y1=32, Y2=42, matches d09995951): PASS
- K7 Learner-built (census: 2 count MAPs plen -1 oty 1, 2 chain
  MAPs plen 4 oty 0; adapter fields reference learner MAP ids 44,
  96; core sha256 unchanged; grep finds no type-conversion table
  and no COUNT_CHAIN/CHAIN_COUNT template in xhio_driver.zag): PASS
- K8 Determinism (3/3 byte-identical, sha256
  6909ba0c576b3204c110e259411cbb71970f3caa39912f812a2d7761188ab51a):
  PASS
- Handoff signature: S1 observed (BUILD o1=1 o2=0 mid=4 ans=52,
  tried=1 rejected=0). S2/S3/S4 not observed.
- Verdict: XIO-HARDER-COMPLETE

## Constraints observed

- Pure Zag. Zero em/en dashes in docs, code, and output (byte-checked).
- Paper untouched. Nothing pushed (local commits only).
- 0 modes / 0 bridges / 0 handlers / 0 new core semantic cases.
- No hardcoded type-conversion table; no COUNT_CHAIN / CHAIN_COUNT
  pair template (grep-verified before the verdict commit).
- xio_try is a uniform miss-policy stage, not a task mode.
