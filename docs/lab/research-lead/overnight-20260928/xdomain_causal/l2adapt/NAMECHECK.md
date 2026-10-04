# NAMECHECK.md -- Cross-Domain Causal-Intervention L2 Worker

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

Result: `which python3 python` returned NOTHING. Only `guard-check-done`
printed. Safebin active. PATH=$HOME/safebin.

**Attestation:** Zero Python invocations in this worker's session. All
computation via pinned znc or safebin coreutils. Shell used only to
invoke znc, run binaries, git ops, and move/copy files.

Any forbidden executable invocation = PROCESS-FAIL (none occurred).

## Prereg freeze (before implementation)

PREREG.md in `xdomain_causal/l2adapt/` was authored by this worker and
committed BEFORE any implementation file was created (prereg commit
strictly precedes implementation, per loop governance). The prereg is
never edited after freezing; this NAMECHECK.md is not frozen.

Prior work read, not modified: C273 battery in `xdomain_causal/`
(PREREG.md, REPORT.md, commits 2dc11c883, 664c04d8d); C275
struct_composition (sc_do sever+recompute); C279 xdomain_l2 (REBIND
operator, l2_h1.zag, l2_h2.zag). Mechanism logic for H1/H2 follows the
C279 implementations; only the world facts, the causal behaviors, and
the intervention setup are new.

## Build Record

h1.zag: H1 typed contracts + REBIND. Compiles warning-free with pinned znc
(src/tools/toolchain/znc_linux_x86_64_abed8aa1). Binary: h1_bin (81061 bytes).

h2.zag: H2 value composition (modes) + REBIND. Compiles with 2 benign
warnings (unused variable, ignored syscall return; not errors). Binary:
h2_bin (42523 bytes).

**Implementation bug found and fixed (documented, not hidden):**
During testing, the fact store used a 12-byte stride but each fact needs
16 bytes (4x i32: used, subj, rel, obj). The obj of slot i overwrote the
used flag of slot i+1, corrupting the store after ~35 facts. Fixed by
changing to 16-byte stride with 48 slots (48*16=768 bytes; 64+768=832,
exactly abutting the MAP area at 832). This is an implementation bug,
not a prereg change: the world (40 facts) and mechanism logic are
unchanged. The PREREG's scientific claims are unaffected.

**Zero Python attestation (reaffirmed):** No Python was invoked at any
point. The bug was diagnosed via Zag debug prints and fixed via sed.
All computation via znc or safebin coreutils.

## Determinism Record

H1: 3 runs, byte-identical.
SHA256: 5e8341c843627f31ccd28866f850c4f73ba9508f396c7d36b00572e0a45c9f1a
(h1_run1.txt = h1_run2.txt = h1_run3.txt)

H2: 3 runs, byte-identical.
SHA256: bd3068e103c9f7bbd84d907afccb3a98c6d3c6eda6c1a533255a0459410d5ba9
(h2_run1.txt = h2_run2.txt = h2_run3.txt)

Binaries: h1_bin, h2_bin. Run outputs: h1_run1/2/3.txt, h2_run1/2/3.txt.
All in `xdomain_causal/l2adapt/`.
