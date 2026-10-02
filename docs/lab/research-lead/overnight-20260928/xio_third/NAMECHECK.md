# NAMECHECK.md -- H-XIO-3 Third-Domain Worker

## Step 0: Worker toolchain guard (mandatory, recorded at startup)

Executed before any other work, 2026-10-02 ~07:42 PDT:

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
Safebin active: /home/hatch/safebin. Toolchain verification: PASS.

All computation in this wave is pure Zag (znc) plus POSIX shell
utilities for assembly, hashing, and git. No Python, no C, no other
interpreters. If any forbidden executable is invoked, this wave is
automatically PROCESS-FAIL.

## Step 1: Task and verdict

XIO Third-Domain Worker (H-XIO-3). Mission: test whether the XIO
typed I/O adapter mechanism (H-XIO-1 C229, H-XIO-2 harder pair)
generalizes UNCHANGED to a third domain pair with MAP types
structurally different from chain/count: sequence->aggregate, i.e.
X = CHAIN (oty 0), Y = SUM (oty 1, unrolled INC cells, no guards),
Z = SUM(CHAIN(s)). Target verdict: XIO-THIRD-COMPLETE with a
generality-boundary diagnosis.

White-box prediction (frozen in PREREG.md): H-XIO-3 is predicted to
FAIL at STAGE ASSEMBLY (signature S4): the oty proxy classifies sum
as NUMBER correctly, the mismatch gate fires (8 differing pairs),
but the oty-1 stage branch re-derives COUNT semantics (v2=1, not the
sum 10), so no adapter builds and Z1=-2. The pairing/gating logic
generalizes; the staged execution does not.

## Step 2: Frozen vs unfrozen inventory

FROZEN (read-only, never modified):
- docs/lab/research-lead/overnight-20260928/composition_A/cx_core.zag
  (TNN-2 integration base)
  sha256: dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
- docs/lab/research-lead/overnight-20260928/xio_adapters/xio_core.zag
  (the C229 adapter mechanism)
  sha256 at freeze time:
  4d4d2e0e932b6a472e3cd8456d7e1c633218e611ce5df51d03507218440a8a7f
  This file is REFERENCED by the assembly recipe, never copied,
  never edited. Zero adapter-mechanism changes is a frozen claim.
- everything else outside xio_third/

UNFROZEN (this worker's new files, all under xio_third/):
- PREREG.md (frozen FIRST: H-XIO-3, kill bars K1-K8, diagnostic
  signatures S1-S4, predicted S4)
- NAMECHECK.md (this file)
- REPORT.md (written after runs)
- x3_driver.zag (new: third-pair world, arms, census, pair audit;
  the ONLY new source this wave)
- x3_full.zag (assembled: cx_core.zag + xio_core.zag + x3_driver.zag,
  both bases verbatim)
- x3_bin (compiled binary, pinned znc)
- x3_run1.txt, x3_run2.txt, x3_run3.txt (3/3 outputs)
- x3_compile.txt (compiler output)

Assembly recipe:
```
cd docs/lab/research-lead/overnight-20260928/xio_third
export PATH="$HOME/safebin"
cat ../composition_A/cx_core.zag ../xio_adapters/xio_core.zag x3_driver.zag > x3_full.zag
znc x3_full.zag -o x3_bin 2> x3_compile.txt
./x3_bin > x3_run1.txt; ./x3_bin > x3_run2.txt; ./x3_bin > x3_run3.txt
sha256sum x3_run1.txt x3_run2.txt x3_run3.txt
```

## Step 3: Prereg commit-order self-check

(To be filled after the prereg commit. Must show: PREREG.md first
commit hash and timestamp, verification that the commit contains ONLY
PREREG.md + NAMECHECK.md under xio_third/, and that the
implementation commit (x3_driver.zag) is strictly later.)

## Step 4: Build and run log

(To be filled after implementation: assembly, core sha256 recheck,
compile result, run hashes, key trace lines.)

## Step 5: Kill-bar scorecard

(To be filled after runs: K1-K8 PASS/FAIL against the frozen bars,
observed diagnostic signature S1/S2/S3/S4, verdict.)

## Constraints observed

- Pure Zag. Zero em/en dashes in docs, code, and output (byte-checked
  before the verdict commit).
- Paper untouched. Nothing pushed (local commits only).
- 0 modes / 0 bridges / 0 handlers / 0 new core semantic cases.
- No hardcoded type-conversion table; no SUM_CHAIN / CHAIN_SUM pair
  template (grep-verified before the verdict commit).
- xio_try remains a uniform miss-policy stage, not a task mode.
