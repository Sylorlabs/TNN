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

- PREREG.md first commit hash:
  c21e49503f198bed89067785646ff31b3199c445
  (2026-10-02 14:52:00 UTC). Verified via git ls-tree: that commit
  contains ONLY PREREG.md + NAMECHECK.md under xio_third/
  (no driver, no binary, no run outputs, no report).
- Implementation file (x3_driver.zag) was written after 14:52 UTC
  and is committed separately, strictly later.
- Self-check: PASS (no implementation at or before c21e49503).

## Step 4: Build and run log

- Assembly: cat ../composition_A/cx_core.zag
  ../xio_adapters/xio_core.zag x3_driver.zag > x3_full.zag
  (2200 lines; both bases verbatim, zero edits).
- Core reuse verified: sha256 of ../xio_adapters/xio_core.zag is
  4d4d2e0e932b6a472e3cd8456d7e1c633218e611ce5df51d03507218440a8a7f
  before assembly and after the runs, identical to the C229/HARDER
  freeze value. The adapter mechanism was not copied, forked, or
  edited: the assembly recipe references the sibling file directly.
- Compile: success, warnings only (682 warning lines, same A0102
  ignored-return-value class as sibling workers; the em dashes in
  x3_compile.txt are znc's own warning text, also present in the
  sibling compile logs). Binary x3_bin 272546 bytes
  (pinned znc, safebin /home/hatch/safebin/znc).
- The cx_core.zag internal test battery references ev_query; as in
  H-XIO-1/H-XIO-2, the driver defines ev_query as
  xio_query(...,xio_on=1). The battery is never invoked.
- Runs: 3/3 byte-identical, sha256
  d3ad77208ddc8771427a911a74bb80571ec2fd154ed1c7f78dfb452ad4a10220.
- Key trace (TREAT + AUDIT, identical all 3 runs):
  census: 2 chain MAPs (plen 4, oty 0), 2 sum MAPs (plen -1, oty 1,
  all-INC graphs); X1=14, X2=18, Y1=8, Y2=12.
  PAIR-AUDIT on (41,93): tried=8; the 4 (chain,sum) pairs show
  v1=44 v2=1; the 4 (sum,chain) pairs show v1=-999999 v2=-999999.
  Zero XIO-BUILD and zero XIO-REUSE lines in the full output.
  Z1=Z2a=Z2b=-2 in TREAT, ABL-XIO, ABL-X, ABL-Y, FRESH;
  adapters=0 throughout.

## Step 5: Kill-bar scorecard

- K1 Z1 boundary (Z1=-2, adapters=0, no XIO-BUILD): PASS
- K2 oty observation (2 chain oty 0 + 2 sum oty 1, no other MAPs):
  PASS (S2 ruled out)
- K3 mismatch gate (audit tried=8 differing pairs): PASS
  (S3 ruled out)
- K4 stage diagnosis ((chain,sum): v1=44 v2=1; (sum,chain):
  v1=-999999; never v2=10): PASS
- K5 ablations (all arms Z1/Z2a/Z2b=-2, adapters=0): PASS
- K6 competence (X1=14, X2=18, Y1=8, Y2=12): PASS
- K7 core unchanged (sha256 match; no SUM_CHAIN/CHAIN_SUM template,
  no type-conversion table in driver): PASS
- K8 determinism (3/3 byte-identical, sha256 d3ad7720...): PASS
- Diagnostic signature: S4 observed as predicted. S1/S2/S3 not
  observed.
- Verdict: XIO-THIRD-COMPLETE (H-XIO-3 rejected; generality boundary
  localized at stage assembly)

## Constraints observed

- Pure Zag. Zero em/en dashes in docs, code, and output (byte-checked
  before the verdict commit).
- Paper untouched. Nothing pushed (local commits only).
- 0 modes / 0 bridges / 0 handlers / 0 new core semantic cases.
- No hardcoded type-conversion table; no SUM_CHAIN / CHAIN_SUM pair
  template (grep-verified before the verdict commit).
- xio_try remains a uniform miss-policy stage, not a task mode.
