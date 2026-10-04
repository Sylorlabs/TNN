# NAMECHECK.md -- Causal to Intervention L2 Worker

## Step 0: Toolchain Guard (mandatory, recorded before any work)

Worker startup executed:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING. Only `guard-check-done` printed.
Safebin active. PATH=$HOME/safebin.

The pinned znc was not on PATH, so it was linked into the safebin
explicitly from the repo toolchain:
`ln -sf ~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1 $HOME/safebin/znc`.
sha256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`,
identical to the pinned 2026-09-30 znc recorded in the xdomain_l2_ts
NAMECHECK.

**Attestation:** Zero Python invocations in this worker's session. All
computation via the pinned znc above or safebin coreutils. Shell used
only to invoke znc, run binaries, git ops, and move/copy files.

Any forbidden executable invocation = PROCESS-FAIL (none occurred).

## Prereg adoption (before implementation)

PREREG.md in this directory was authored by this worker for this task,
frozen 2026-10-02 before any implementation file was created, and
committed ALONE (commit 912044b54, explicit pathspec, exactly 1 file
in the commit) before the first source file existed. Prereg
commit-order self-check: satisfied. The prereg is never edited after
freezing; this NAMECHECK.md is not frozen.

## Assemblies

- `cl_h1.zag`: H1 typed contracts + learner-driven TRUNCATE/SPECIALIZE
  on the causal walk. Standalone. Mechanism logic follows the
  xdomain H1 lineage (kind probe, typed contract filtering, two-phase
  solver); new: the threshold-gated causal walk behavior (threshold
  computed as minimum training node value, never a literal), the
  generic TRUNCATE (depth cap) and SPECIALIZE (threshold) operators,
  the generic reachability candidate scan, exhaustive Phase 2 with
  per-world success accounting and provenance records. Output via the
  mandatory e1str/e1i64 + single `_zag_raw_syscall` flush (no
  `_zag_print`, per the 2026-10-02 znc miscompile workaround).
- `cl_h2.zag`: H2 value composition + learner-driven
  TRUNCATE/SPECIALIZE on the stage 1 walk. Standalone. Mechanism
  logic follows the xdomain H2 lineage (ordered mode pairs, value
  passing between stages, capability evidence via has_behav); new:
  the threshold-gated walk as stage 1, the same two generic operators
  applied at the stage level, exhaustive Phase 2. Modes 1=WALK,
  2=INTERVENE are the inherited H2 mechanism vocabulary (capability
  slots), not new cognitive modes. Same safe output pattern.

## Build Record

- Toolchain: pinned znc (sha256 above), safebin PATH, zero Python
  invocations (Step 0 attestation above).
- `cl_h1.zag` -> `cl_h1_bin`: compiles clean (only the standard zagd
  notice). 3/3 runs byte-identical, sha256
  `34504d7bd42fc820814108f911736c6b7566a103b970ff31a71b46e04722a179`.
- `cl_h2.zag` -> `cl_h2_bin`: compiles clean (only the standard zagd
  notice). 3/3 runs byte-identical, sha256
  `bfe37d69add725e73ebd684e658377c3f3abdb06208a0340a2a9be97236cf771`.
- Commit order (prereg commit-order self-check satisfied):
  PREREG freeze (PREREG.md only, explicit pathspec, commit 912044b54),
  then H1/H2 implementation sources,
  then binaries, run outputs, compile logs, NAMECHECK.md, REPORT.md.
- All commits local on `tnn-native-lab`; nothing pushed.
- No em dashes or en dashes in any file (verified by byte grep
  before commit).

## Trace audit notes (before verdict)

The first-run traces were audited line by line against the prereg
predicted outcomes before any verdict was claimed. No implementation
bugs were found; the traces match the predictions exactly:

- H1 TREAT-T: TEACH X sig=1->1 thresh=11 (computed) ep11=13. Phase 1:
  singles Y(41)=-1, D2(41)=1; pairs (X,Y) mid=44 r=106, (X,D2) r=0,
  (D1,Y) r=-1, (D1,D2) r=1. Phase 2: SPECIALIZE T=41->106 rejected,
  T=42,43,44->-1 rejected; TRUNCATE k=1->-1 rejected, k=2->43->
  Y(43)=105 success. Exactly 1 success: op=1 param=2 b=Y.
- H1 TREAT-S: X(5)=5 (threshold blocks). Phase 1 all fail.
  Phase 2: SPECIALIZE T=5->7->Y(7)=112 success; T=6,7->-1 rejected;
  TRUNCATE k=1->5 (gate still blocks)->-1 rejected. Exactly 1
  success: op=2 param=5 b=Y.
- H2 TREAT-T: VC-COMPOSE ok m1=1 m2=2 op=1 param=2; all SPECIALIZE
  candidates tried and rejected in the trace.
- H2 TREAT-S: VC-COMPOSE ok m1=1 m2=2 op=2 param=5.
- All L1-ONLY / ABL-X / ABL-Y / FRESH arms fail as expected in both
  worlds for both mechanisms. TOTAL 10/10 for both binaries.

K-CI-7 audit: 105 and 112 occur only in world-setup fact lines,
arm-harness query literals, arm verdict checks (test oracle), and
comments; never in operator, candidate-scan, threshold-learning, or
composer logic. No literal truncate/specialize parameter in mechanism
code; the threshold value 11 is computed by chain_nodes_min, never a
source literal (verified by grep).

K-CI-8 audit: CAUSAL_TO_INTERVENTION / CAUSAL_INTERVENE appear only
in PREREG.md kill-bar text declaring their absence; zero occurrences
in mechanism code.
