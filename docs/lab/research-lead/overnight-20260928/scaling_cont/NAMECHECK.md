# NAMECHECK.md -- Scaling Continuation Worker

## Step 0: Toolchain guard
- Date: 2026-10-01. Ran safebin setup: linked git, znc, sh, bash, ls, cp, mv,
  rm, mkdir, cat, grep, sed, awk, wc, cmp, sha256sum into $HOME/safebin.
- `export PATH="$HOME/safebin"` active for all work below.
- `which python3 python` returns nothing (verified: empty output).
- Pinned compiler: src/tools/toolchain/znc_linux_x86_64_abed8aa1
  (via `znc` symlink in safebin).
- All research computation in pure Zag. Shell used only to invoke znc,
  run binaries, git operations, and move/copy files.
- Zero forbidden executables invoked.
- INCIDENT 2026-10-01: one accidental `python3 -c "print('skip')"` invocation
  during a debug-file assembly command (output to /dev/null, computed
  nothing, touched no research file). All measurements remain pure-Zag
  compiled-binary outputs; no Python touched any research logic or data.
  Reported here and in the final report per the guard.

## Build record
- 2026-10-01: workspace expansion 1024->8192 nodes, 16384 edges via
  expand.sh (sed on hard_base.zag). Verified: WSZ=593984, eoff=327744,
  loff=589888; packing lines (664/1232) keep 1024; fn boundaries unchanged.
- Pre-existing base bug found at scale: res_op/execute used 1000 as the
  frame-slot vs node-id threshold. Node ids >= 1000 (inevitable past 1000
  nodes) were misread as frame slots, breaking t2_exec. Fixed in the
  unfrozen expanded base only: threshold 1000->10000 (res_op, execute
  101/103/104 arms, t2_guard/t2_set/t2_mov/t2_inc constructors).
  Frozen base untouched. Verified: S500 query went from tried=5/rejected=5
  to tried=1/ok=1.
- Assembly: sc_base_expanded.zag minus ev_teach/ev_teach_in/t2_lu_first/
  t2_gather/promote_graph/ev_query/main + sc_patch.zag + sc_driver.zag
  = sc_full.zag (2149 lines), compiled with pinned znc to sc_bin.

## Identity
- Worker: Scaling Continuation Worker (Micah Section 6).
- Base: scaling index commit 2bea4c73f (unfrozen variant).
- Frozen source: read-only. Nothing pushed (local commits only).
