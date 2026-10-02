# NAMECHECK.md: H-XIO-4 Generalization Worker

## Step 0: Worker toolchain guard (mandatory, recorded at startup)

Executed before any other work, 2026-10-02 ~07:56 PDT:

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

XIO Generalization Worker (H-XIO-4). Mission: repair the XIO
generality boundary localized by XIO-THIRD (prereg c21e49503,
results 920584056): the 2-bucket oty conflates the count and sum
families in bucket 1 while the bucket-1 stage executor hardcodes
count re-derivation. Build the UNFROZEN variant: a richer
learner-observed structural type signature (xio_sclass: guard
presence, INC-only vs mixed cells, no researcher domain labels)
plus per-structural-class stage dispatch (class 0: chain
re-derivation; class 1: count re-derivation; class 2: new sum
re-derivation via the MAP-observed licensing relation and the
learner's own t2_asm_sum, verified with trial's own s0=0 sum frame).
Test battery: chain->count (C229, no regression), count->chain
(C235, no regression), chain->sum (must now solve, Z=10).
Target verdict: XIO-GENERAL-COMPLETE (with 3-pair battery).

Frozen design summary (PREREG.md): xio_oty kept verbatim as the
coarse 2-bucket view; mismatch gate moves from oty-difference to
sclass-difference (same admitted pair sets on the three test pairs,
additionally admits future cross-family pairs such as count/sum);
xio_stage_exec dispatches on sclass 0/1/2/-1; class-2 stage mirrors
trial's sum branch exactly (relation from MAP DEP edges, direct
facts of the stage input under that relation, t2_asm_sum, masked
verify with slot0=0). White-box prediction: PAIR-A and PAIR-B
reproduce C229/C235 values exactly; PAIR-C Z1=10 via XIO-BUILD
(c1=0 c2=2 mid=44 ans=10), Z2a reuse, Z2b second adapter.

## Step 2: Frozen vs unfrozen inventory

FROZEN (read-only, never modified):
- docs/lab/research-lead/overnight-20260928/composition_A/cx_core.zag
  (TNN-2 integration base; trial, assemblers, 4-op ISA)
  sha256: dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
- docs/lab/research-lead/overnight-20260928/xio_adapters/xio_core.zag
  (the C229 adapter mechanism; REFERENCED for lineage only, never
  copied into the new build)
  sha256: 4d4d2e0e932b6a472e3cd8456d7e1c633218e611ce5df51d03507218440a8a7f
- docs/lab/research-lead/overnight-20260928/xio_adapters/xio_driver.zag
  (C229 world; PAIR-A facts/queries replicated from it)
- docs/lab/research-lead/overnight-20260928/xio_harder/xhio_driver.zag
  (C235 world; PAIR-B facts/queries replicated from it)
- docs/lab/research-lead/overnight-20260928/xio_third/x3_driver.zag
  (XIO-THIRD world; PAIR-C facts/queries replicated from it)
- everything else outside xio_general/

UNFROZEN (this worker's new files, all under xio_general/):
- PREREG.md (frozen FIRST: H-XIO-4, design, kill bars K1-K8)
- NAMECHECK.md (this file)
- REPORT.md (written after runs)
- xio_core2.zag (new: generalized XIO core; richer structural
  signature + per-class stage dispatch; the ONLY mechanism change)
- xg_driver.zag (new: 3-pair battery driver; the ONLY other source)
- xg_full.zag (assembled: ../composition_A/cx_core.zag verbatim +
  xio_core2.zag + xg_driver.zag)
- xg_bin (compiled binary, pinned znc)
- xg_run1.txt, xg_run2.txt, xg_run3.txt (3/3 outputs)
- xg_compile.txt (compiler output)

Assembly recipe:
```
cd docs/lab/research-lead/overnight-20260928/xio_general
export PATH="$HOME/safebin"
cat ../composition_A/cx_core.zag xio_core2.zag xg_driver.zag > xg_full.zag
znc xg_full.zag -o xg_bin 2> xg_compile.txt
./xg_bin > xg_run1.txt; ./xg_bin > xg_run2.txt; ./xg_bin > xg_run3.txt
sha256sum xg_run1.txt xg_run2.txt xg_run3.txt
```

## Step 3: Prereg commit-order self-check

- PREREG.md first commit hash: (filled after commit)
- Verified via git ls-tree: that commit contains ONLY PREREG.md +
  NAMECHECK.md under xio_general/ (no core, no driver, no binary,
  no run outputs, no report).
- Implementation files (xio_core2.zag, xg_driver.zag) written
  strictly after the prereg commit timestamp.
- Self-check: (PASS/FAIL filled after commit)

## Step 4: Build and run log

(filled after runs)

## Step 5: Kill-bar scorecard

(filled after runs; verdict requires 8/8)

## Constraints observed

- Pure Zag. Zero em/en dashes in docs, code, and output
  (byte-checked before the verdict commit).
- Paper untouched. Nothing pushed (local commits only).
- 0 modes / 0 bridges / 0 handlers / 0 new core semantic cases.
- No researcher domain labels in the type system: no domain type
  names, no type-conversion table, no pair templates in
  xio_core2.zag (grep-verified before the verdict commit).
- xio_try remains a uniform miss-policy stage, not a task mode.
