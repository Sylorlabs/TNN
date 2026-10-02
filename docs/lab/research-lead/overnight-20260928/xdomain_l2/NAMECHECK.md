# NAMECHECK.md -- Cross-Domain L2 Adaptive Worker

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
computation via pinned znc (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`)
or safebin coreutils. Shell used only to invoke znc, run binaries, git ops,
and move files.

Any forbidden executable invocation = PROCESS-FAIL (none occurred).

### Step 0 (continuation worker, 2026-10-02 ~10:05 PDT)

Re-ran the guard in a fresh shell before any work:
`which python3 python` returned NOTHING (only `guard-check-done` printed).
PATH=$HOME/safebin (49 tools). Pinned znc:
`src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
Zero Python invocations in this session. All computation via pinned znc
or safebin coreutils. Shell only to invoke znc, run binaries, git ops,
move/copy files.

## Prereg adoption (before implementation)

PREREG.md in this directory was authored by a parallel worker for this
same task (present in the working tree, uncommitted, timestamped
2026-10-02 16:22 UTC, before this session's implementation began).
Reviewed: the design matches the mission exactly (H1 typed contracts +
H2 value composition, generic REBIND adaptation operator, on the
arithmetic->planning L1 world from the first arith_plan prereg, sealed
relation shift 71->73 with a 74 distractor). Committed UNCHANGED before
any implementation file was created (prereg commit strictly precedes
implementation, per loop governance). The prereg is never edited after
freezing; this NAMECHECK.md is not frozen.

## Assemblies

- `l2_h1.zag`: H1 typed contracts + learner-driven REBIND. Standalone,
  structure follows `xdomain_typed/xt.zag` (mechanism logic unmodified;
  only world facts, parameterized behaviors, and the L2 rebind search are new).
  Output via the mandatory e1str/e1i64 + single `_zag_raw_syscall` flush
  (no `_zag_print`, per the 2026-10-02 znc miscompile workaround).
- `l2_h2.zag`: H2 value composition + learner-driven REBIND. Standalone,
  structure follows `xdomain_causal_interv/ci_h2.zag` (mechanism logic
  unmodified; only modes, parameterized relations, and L2 search are new).
  Same safe output pattern.

## Build Record

- Toolchain: pinned `src/tools/toolchain/znc_linux_x86_64_abed8aa1`,
  safebin PATH, zero Python invocations (Step 0 attestation above).
- `l2_h1.zag` -> `l2_bin_h1`: compiles warning-free. 3/3 runs
  byte-identical, sha256
  `0dd8e67761a37ad08efb4eca9da318cbd826deb79b5efcc48aa505c21d2f6a7f`
  (`l2_run_h1_1/2/3.txt`).
- `l2_h2.zag` -> `l2_bin_h2`: compiles warning-free. 3/3 runs
  byte-identical, sha256
  `2bd7afaa5541bb0418dc0fd3346548d6b2487e4e2281301c29953f83fcdcc9af`
  (`l2_run_h2_1/2/3.txt`).
- Commit order (prereg commit-order self-check satisfied):
  `418db9bd4` PREREG freeze (PREREG.md only),
  `2108d5d45` H1/H2 implementation,
  `aee652eb0` REPORT (verdict XDOMAIN-L2-COMPLETE).
- All commits local on `tnn-native-lab`; nothing pushed.
- A concurrent worker's early uncompilable drafts are preserved
  unmodified under `sibling_draft_uncompilable/` for the record; the
  committed implementation is independent and post-dates the prereg
  freeze.
