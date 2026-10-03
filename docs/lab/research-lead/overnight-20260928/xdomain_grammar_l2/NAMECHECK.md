# NAMECHECK.md -- Grammar to Program L2 Worker

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

The pinned znc was already linked into the safebin from the repo toolchain:
`$HOME/safebin/znc -> ~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
sha256 `498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`,
identical to the pinned 2026-09-30 znc recorded in the xdomain_causal_l2
NAMECHECK. `znc --version` reports `znc 2026.07.0-dev (edition 2026)`.

**Attestation:** Zero Python invocations in this worker's session. All
computation via the pinned znc above or safebin coreutils. Shell used
only to invoke znc, run binaries, git ops, and move/copy files.

Any forbidden executable invocation = PROCESS-FAIL (none occurred).

## Prereg adoption (before implementation)

PREREG.md in this directory was authored by this worker for this task,
frozen 2026-10-02 before any implementation file was created, and
committed ALONE (explicit pathspec, exactly 1 file in the commit)
before the first source file existed. Prereg commit-order self-check:
satisfied. The prereg is never edited after freezing; this
NAMECHECK.md is not frozen.

## Assemblies

- `gp_h1.zag`: H1 typed contracts + learner-driven TRUNCATE/EXTEND
  on the grammar PARAM map. Standalone. Mechanism logic follows the
  xdomain H1 lineage (kind probe, typed contract filtering, two-phase
  solver); new: the PARAM behavior (licensed program length
  extraction via r=71, rebound to the discovered k when adapted),
  the EXEC behavior (canonical L-op program trace encoding =
  repunit with a generic i32 overflow guard), the generic TRUNCATE
  (rebind over k in [1,L)) and EXTEND (rebind over k in (L,2L])
  operators with exhaustive Phase 2 try-and-validate and provenance
  records (adapt_of, adapt_op, adapt_param). Output via the
  mandatory e1str/e1i64 + single `_zag_raw_syscall` flush (no
  `_zag_print`, per the 2026-10-02 znc miscompile workaround).
- `gp_h2.zag`: H2 value composition + learner-driven
  TRUNCATE/EXTEND on the stage 1 grammar extraction. Standalone.
  Mechanism logic follows the xdomain H2 lineage (ordered mode
  pairs, value passing between stages, capability evidence via
  has_behav); new: stage 1 is the GRAMMAR licensed-length
  extraction with the same two generic operators applied as a
  rebind, stage 2 is the PROGRAM executor. Modes 1=GRAMMAR,
  2=PROGRAM are the inherited H2 mechanism vocabulary (capability
  slots), not new cognitive modes. Same safe output pattern.

## Build Record

- Toolchain: pinned znc (sha256 above), safebin PATH, zero Python
  invocations (Step 0 attestation above).
- `gp_h1.zag` -> `gp_h1_bin`: compiles clean (only the standard
  zagd notice). 3/3 runs byte-identical, sha256
  `0a8e1121fc5fb880d8f79cae4e4a2e28f6ee3fa1a32268b9c02428263db03468`.
  TOTAL 10/10.
- `gp_h2.zag` -> `gp_h2_bin`: compiles clean (only the standard
  zagd notice). 3/3 runs byte-identical, sha256
  `718f09eff7406c77588f865e85d3bf2ca72a6b8934f95837151df0e5c6451f3f`.
  TOTAL 10/10.
- Commit order (prereg commit-order self-check satisfied):
  PREREG freeze (PREREG.md only, explicit pathspec, commit
  436998cce), then H1/H2 implementation sources, binaries, run
  outputs, compile logs, NAMECHECK.md, REPORT.md (explicit
  pathspecs).
- All commits local on `tnn-native-lab`; nothing pushed.
- No em dashes or en dashes in any file (verified by byte grep
  before commit).

## Trace audit notes (before verdict)

The first-run traces were audited line by line against the prereg
predicted outcomes before any verdict was claimed. No implementation
bugs were found; the traces match the predictions exactly:

- H1 TREAT-E: TEACH X id=0 sig=1->1 x1=2; Y id=1 sig=1->2 y2=11.
  Phase 1: singles Y(1)=1, D1(1)=7; pairs (X,Y) mid=2 r=11,
  (X,D1) mid=2 r=5, (D2,Y) mid=1 r=1, (D2,D1) mid=1 r=7; L1-FAIL.
  Phase 2: TRUNCATE k=1 rejected (r=1, r=7); EXTEND k=3 rejected
  (r=111, r=-1); EXTEND k=4 -> mid=4 -> Y(4)=1111 success.
  Z-COMP z=7 a=6 b=1; Z-PROV adapt_of=0 op=2 param=4. Exactly 1
  success.
- H1 TREAT-T: Phase 1: singles Y(2)=11, D1(2)=5; pairs (X,Y)
  mid=4 r=1111, (X,D1) mid=4 r=-1, (D2,Y) mid=2 r=11, (D2,D1)
  mid=2 r=5; L1-FAIL. Phase 2: TRUNCATE k=1 -> r=1, k=2 -> r=11
  rejected; k=3 -> mid=3 -> Y(3)=111 success; EXTEND k=5..8 ->
  r=11111..11111111 rejected. Z-PROV adapt_of=0 op=1 param=3.
  Exactly 1 success.
- H2 TREAT-E: Phase 1 (1,1)->4, (1,2)->11, (2,1)->2, (2,2)->1;
  L1-FAIL. Phase 2: TRUNCATE k=1 rejected; EXTEND k=3 -> v2=111
  rejected, k=4 -> v2=1111 success. VC-COMPOSE ok
  m1=1 m2=2 op=2 param=4.
- H2 TREAT-T: Phase 1 (1,1)->-1, (1,2)->1111, (2,1)->-1,
  (2,2)->-1 (overflow guard); L1-FAIL. Phase 2: TRUNCATE k=1 ->
  v2=1, k=2 -> v2=11 rejected, k=3 -> v2=111 success; EXTEND
  k=5..8 rejected. VC-COMPOSE ok m1=1 m2=2 op=1 param=3.
- All L1-ONLY / ABL-X / ABL-Y / FRESH arms fail as expected in both
  worlds for both mechanisms. TOTAL 10/10 for both binaries.

K-GP-7 audit: 1111 and 111 occur only in arm-harness comments and
query literals; never in operator, candidate-range, or composer
logic. The literals 4 and 3 in mechanism code are byte offsets,
behavior codes, or the training fact (2,71,4); candidate loops use
pure arithmetic on the learned L (k<L, k<=2*L). Discovered params
appear as literals only in arm verdict checks (test oracle).

K-GP-8 audit: GRAMMAR_TO_PROGRAM / GRAMMAR_PROGRAM appear only in
PREREG.md kill-bar text declaring their absence; zero occurrences
in mechanism code.
