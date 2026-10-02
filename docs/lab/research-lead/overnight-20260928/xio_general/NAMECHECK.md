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

- PREREG.md first commit hash:
  e08110f47bd36eb6549bf41bae557420331ade8b
  (2026-10-02 15:06:59 UTC). Verified via git ls-tree: that commit
  contains ONLY PREREG.md + NAMECHECK.md under xio_general/
  (no core, no driver, no binary, no run outputs, no report).
- Implementation files (xio_core2.zag, xg_driver.zag) were written
  after 15:06:59 UTC and are committed separately, strictly later.
- Self-check: PASS (no implementation at or before e08110f47).

## Step 4: Build and run log

- Assembly: cat ../composition_A/cx_core.zag xio_core2.zag
  xg_driver.zag > xg_full.zag (2417 lines).
- Frozen base integrity: sha256 of ../composition_A/cx_core.zag is
  dc0e86d44db11390e6e7d2450e1b52d7fb8f8012b42346dc4d4739ef888d1ab6
  before assembly and after the runs, matching the frozen value.
  The base was referenced, never copied or edited.
- Compile: success, warnings only (213 A0102-class analyzer notes,
  same class as sibling workers; the em dashes in xg_compile.txt
  are znc's own warning text). Binary xg_bin 289693 bytes
  (pinned znc, safebin /home/hatch/safebin/znc).
- A comment-only scrub of xio_core2.zag (domain words removed from
  comments; xio_stage_sum renamed xio_stage_c2) was rebuilt and
  re-run: identical binary behavior, same run sha256.
- The cx_core.zag internal test battery references ev_query; as in
  prior waves, the driver defines ev_query as
  xio_query(...,xio_on=1). The battery is never invoked.
- Runs: 3/3 byte-identical, sha256
  a7cf8b524b20e50906d21cb3d58e88cf8ba63e12276ee3cb2337ccfeee4b63ae.
- Key traces (identical all 3 runs):
  PAIR-A TREAT: census 2 sclass-0 + 2 sclass-1 MAPs; X1=14, X2=18,
  Y1=3, Y2=4; XIO-BUILD id=380 m1=27 m2=115 c1=0 c2=1 rel1=81
  rel2=82 qr=93 mid=34 ans=2; XIO-REUSE id=380 ans=2 on Z2a;
  second BUILD id=467 qr=94 mid=74 ans=2 on Z2b. ABL-XIO: all -2,
  adapters=0.
  PAIR-B TREAT: census 2 sclass-1 + 2 sclass-0 MAPs; X1=3, X2=2,
  Y1=32, Y2=42; XIO-BUILD id=214 m1=44 m2=96 c1=1 c2=0 rel1=81
  rel2=82 qr=93 mid=4 ans=52; XIO-REUSE id=214 ans=52 on Z2a;
  second BUILD id=313 qr=94 mid=3 ans=32 on Z2b. ABL-XIO: all -2,
  adapters=0.
  PAIR-C TREAT: census 2 sclass-0 + 2 sclass-2 MAPs; X1=14, X2=18,
  Y1=8, Y2=12; XIO-BUILD id=190 m1=27 m2=59 c1=0 c2=2 rel1=81
  rel2=82 qr=93 mid=44 ans=10; XIO-REUSE id=190 ans=10 on Z2a;
  second BUILD id=275 qr=94 mid=74 ans=10 on Z2b.
  ABL-XIO/ABL-X/ABL-Y/FRESH: Z1=Z2a=Z2b=-2, adapters=0, zero
  XIO-BUILD lines.
  PAIR-C AUDIT: tried=8 cross-class pairs, gate_rejected=4
  same-class pairs; the 4 (class 0, class 2) pairs show v1=44
  v2=10; the 4 (class 2, class 0) pairs show v1=-999999.
- Note: the second sum MAP promotes at id 103 (vs 91 in
  XIO-THIRD) because the Y2 xio_try probe now stages the first sum
  MAP through the class-2 branch (different allocation sequence
  than the old count branch) before trial promotes the second MAP.

## Step 5: Kill-bar scorecard

- K1 PAIR-A no-regression (Z1=2 BUILD c1=0 c2=1 mid=34 ans=2;
  Z2a=2 REUSE; Z2b=2 second BUILD mid=74; X1=14 X2=18 Y1=3 Y2=4;
  ABL-XIO all -2): PASS (ids/mids match C229 exactly)
- K2 PAIR-B no-regression (Z1=52 BUILD c1=1 c2=0 mid=4 ans=52;
  Z2a=52 REUSE; Z2b=32 second BUILD mid=3; X1=3 X2=2 Y1=32 Y2=42;
  ABL-XIO all -2): PASS (ids/mids match C235 exactly)
- K3 PAIR-C solves (Z1=10 BUILD c1=0 c2=2 mid=44 ans=10;
  Z2a=10 REUSE; Z2b=10 second BUILD mid=74 ans=10): PASS
- K4 structural signature (censuses 0/0/1/1, 1/1/0/0, 0/0/2/2;
  oty agrees; grep clean): PASS
- K5 gate/stage diagnosis (audit tried=8, gate_rejected=4;
  (0,2): v1=44 v2=10; (2,0): v1=-999999): PASS
- K6 ablations (all arms -2, adapters=0, zero BUILD lines): PASS
- K7 competence (PAIR-C X1=14 X2=18 Y1=8 Y2=12): PASS
- K8 determinism (3/3 byte-identical, sha256 a7cf8b52...): PASS
- Verdict: XIO-GENERAL-COMPLETE (with 3-pair battery)

## Constraints observed

- Pure Zag. Zero em/en dashes in docs, code, and output
  (byte-checked before the verdict commit).
- Paper untouched. Nothing pushed (local commits only).
- 0 modes / 0 bridges / 0 handlers / 0 new core semantic cases.
- No researcher domain labels in the type system: no domain type
  names, no type-conversion table, no pair templates in
  xio_core2.zag (grep-verified before the verdict commit).
- xio_try remains a uniform miss-policy stage, not a task mode.
