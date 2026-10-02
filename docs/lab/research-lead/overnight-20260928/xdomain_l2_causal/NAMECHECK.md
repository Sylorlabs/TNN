# NAMECHECK: XDOMAIN-L2-IFACE (causal path model to intervention selector)

Worker: XDomain L2 Interface-Adaptation Worker. Branch: tnn-native-lab.
Local only, never pushed.

## Step 0: toolchain guard (mandatory, verified before any implementation)

- Ran `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`;
  result `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`.
- `export PATH="$HOME/safebin"` active for all build/run commands.
- `which python3` returns nothing (rc=1). `which python` returns nothing (rc=1).
- Pinned compiler only: `src/tools/toolchain/znc_linux_x86_64_abed8aa1`.
- All computation in pure Zag. Shell used only for: znc invocation, running
  compiled binaries, git ops, file moves, sha256sum, grep/diff checks.
- Any forbidden-interpreter invocation would make this wave PROCESS-FAIL;
  none occurred.

## Compiler-defect compliance (all four recorded lessons)

1. Never `as *i32` plus `q[0..n]` slice construction inside functions.
   Workspace is u8-backed with get32/set32 little-endian helpers (ig/is style).
2. Never `_zag_print` for dynamic content. Output uses one preallocated OUT
   buffer with cursor-returning emit helpers (e1str/e1i64 style: digit count,
   fill from the end, no second allocation), then a single
   `_zag_raw_syscall(1,1,ptr,len)` write. Every binary's stdout bytes are
   verified (3/3 byte-identical runs, sha256 recorded).
3. No `as []f64` / `as []i64` casts on []u8; `.len` never trusted on a cast.
4. FOURTH defect (added 2026-10-02): never `!(A && B)` in a `while`
   condition. All loop conditions are written in De Morgan form
   `(A' || B')` from the start. Compliance check run on every new .zag file:
   `grep -n 'while.*!(' *.zag` must return no matches (recorded below).
   Loop results are verified on known inputs before being trusted.
   Additionally: sub-conditions hoisted into flag lets, `if` nesting kept
   at 3 or fewer (third defect workaround).

## Fourth-defect grep record

(To be filled after implementation files are written; must show zero hits.)

## Scope

Unfrozen: `docs/lab/research-lead/overnight-20260928/xdomain_l2_causal/` only.
Nothing else is modified. Paper untouched. No shared history amended.
