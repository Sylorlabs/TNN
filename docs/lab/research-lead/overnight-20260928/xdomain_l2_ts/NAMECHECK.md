# NAMECHECK.md -- Cross-Domain L2 Truncate/Specialize Worker

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

**Attestation:** Zero Python invocations in this worker's session. All
computation via pinned znc (sha256
498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef,
identical to `src/tools/toolchain/znc_linux_x86_64_abed8aa1`) or safebin
coreutils. Shell used only to invoke znc, run binaries, git ops, and
move/copy files.

Any forbidden executable invocation = PROCESS-FAIL (none occurred).

## Prereg adoption (before implementation)

PREREG.md in this directory was authored by this worker for this task,
frozen 2026-10-02 before any implementation file was created, and committed
ALONE (explicit pathspec, no other files in the commit) before the first
source file existed. Prereg commit-order self-check: satisfied. The prereg
is never edited after freezing; this NAMECHECK.md is not frozen.

## Assemblies

- `ts_h1.zag`: H1 typed contracts + learner-driven TRUNCATE/SPECIALIZE.
  Standalone. Mechanism logic follows the xdomain_l2 H1 lineage (typed
  contract filtering, two-phase solver); new: sequence kinds
  (SEQk/SEQANY), the SWEEP/PLAN3/RISK3/TOTAL behaviors, the generic
  TRUNCATE and SPECIALIZE operators, exhaustive Phase 2 with per-world
  success accounting. Output via the mandatory e1str/e1i64 + single
  `_zag_raw_syscall` flush (no `_zag_print`, per the 2026-10-02 znc
  miscompile workaround).
- `ts_h2.zag`: H2 value composition + learner-driven TRUNCATE/SPECIALIZE.
  Standalone. Mechanism logic follows the xdomain_l2 H2 lineage (ordered
  mode pairs, value passing between stages, capability evidence via
  has_behav); new: shared sequence buffer between stages, the same two
  generic operators applied to stage 1 output, exhaustive Phase 2. Same
  safe output pattern.

## Build Record

- Toolchain: pinned znc (sha256 above), safebin PATH, zero Python
  invocations (Step 0 attestation above).
- `ts_h1.zag` -> `ts_bin_h1`: compiles warning-free. 3/3 runs
  byte-identical (sha256 recorded in REPORT.md).
- `ts_h2.zag` -> `ts_bin_h2`: compiles warning-free. 3/3 runs
  byte-identical (sha256 recorded in REPORT.md).
- Commit order (prereg commit-order self-check satisfied):
  PREREG freeze (PREREG.md only, explicit pathspec),
  then H1/H2 implementation sources,
  then binaries, run outputs, compile logs, NAMECHECK.md, REPORT.md.
- All commits local on `tnn-native-lab`; nothing pushed.
- No em dashes or en dashes in any file (verified by grep before commit).

## Implementation bugs found and fixed during trace audit (before any verdict)

Two bugs were caught by auditing the first run traces against the prereg
predictions, before any verdict was claimed. Both were fixed in the
implementation only; PREREG.md was never edited.

1. Fact entry stride: entries were laid out at 12-byte stride for four
   4-byte fields (used,subj,rel,obj), so each entry's object field
   overlapped the next entry's used flag. The 21st fact landed outside
   the 40-entry scan range and was silently dropped; subjects swept 4
   readings instead of 5, so the world did not match the prereg.
   Fixed: 16-byte stride, facts at 64 + i*16, regions relocated.
2. MAP slot exhaustion: 10 slots but Phase 2 can create up to 12 MAPs
   (taught + 5 specialized + 4 truncated + 1 composite). The 11th created
   MAP overlapped the candidate/seqbuf region and was corrupted into a
   phantom second success (a TRUNCATE map read back as SPECIALIZE).
   Fixed: 16 MAP slots, candidates/seqbuf relocated.

Earlier run outputs (from the buggy builds) were superseded; the
committed run outputs are the fixed-build traces, 3/3 byte-identical
with sha256 hashes recorded in REPORT.md. The superseded hashes are
retained here for the audit trail: H1 f99783c7..., H2 0143299d... (buggy
builds; do not use).
