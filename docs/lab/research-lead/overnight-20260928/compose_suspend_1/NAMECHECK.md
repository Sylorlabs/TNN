# NAMECHECK.md -- COMPOSE-SUSPEND-1 Worker (implements COMPOSE-GENERAL-1 Hypothesis B)

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, before any other work:

```
export PATH="$HOME/safebin"
sh ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
```

Verification, run 2026-10-03 with PATH=$HOME/safebin:
- `which python3` -> NOTHING (empty, exit 1)
- `which python` -> NOTHING (empty, exit 1)
- `which znc` -> /home/hatch/safebin/znc (znc 2026.07.0-dev, edition 2026)
- setup_safebin.sh reports: SAFEBIN-READY (36 tools, no python)

Result: PASS. No python3/python reachable in PATH. All subsequent commands in
this task run with PATH=$HOME/safebin (exported in every shell invocation).
Git write operations use /usr/bin/git by absolute path (the safebin git
symlink has a known EPERM-on-write defect; see ~/AGENTS.md).

Pinned compiler for all builds:
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(the safebin `znc` symlink target).

Recursion check: a 5-line recursive factorial test compiled and ran
correctly under the pinned znc (120 printed), so recursive Zag fns
(demand evaluation, DAG copy, regressive enumeration) are available.

Known-defect avoidance rules adopted for all new Zag in this lane
(per ~/AGENTS.md): no `as *i32` + slice construction (u8 arenas with
get32/set32 only); no `!(A && B)` in while conditions (De Morgan form);
if-nesting at most 3 with hoisted call results; no `_zag_print` for
dynamic content (o_app/o_i64 buffer helpers + one raw syscall);
`[]u8 as *u8` never used (`_zag_malloc as *u8` threaded through only).

This NAMECHECK.md + PREREG.md are committed alone before any
implementation file exists; the prereg is adopted as frozen without
modification (commit-order self-check).
