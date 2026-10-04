# NAMECHECK / TOOLCHAIN GUARD

Lane: `propertyzag/`. Worktree
`/Users/Shared/micah/Documents/TNN/.worktrees/propertyzag`.

## Step 0 (recorded before any implementation existed)

```
$ . /Users/Shared/micah/Documents/TNN/.env/pure-zag.sh
$ tnn_pure_zag_report
  ZNC_TARGET=macos-arm64
  ZAG COMPILER: /Users/Shared/micah/Documents/TNN/.bin/znc
  forbidden_count=0
  VERDICT: PURE-ZAG-CLEAN
```

Isolation confirmed before any file was written:

```
$ WT=$(/Users/Shared/micah/Documents/TNN/TNN/tools/lane.sh new propertyzag)
  created lane/propertyzag at /Users/Shared/micah/Documents/TNN/.worktrees/propertyzag
$ git rev-parse --show-toplevel
/Users/Shared/micah/Documents/TNN/.worktrees/propertyzag
$ git branch --show-current
lane/propertyzag
```

The toplevel is the worktree, NOT
`/Users/Shared/micah/Documents/TNN/TNN`. All git operations and all files are
inside the worktree. Frozen lanes `cogops_learnosc2/`, `compression_exec/`,
`cogops_rescueaware/` are READ-ONLY and unmodified; `git status` on them is
clean at the end of the lane.

## Forbidden interpreters

`python`, `python3`, `node`, `cc`, `gcc`, `make`, and the rest are shadowed by
hard-fail shims under `.env/shims` and are not reachable by name. This lane
invoked NONE of them, by name or by absolute path, at any point. Every number in
`REPORT.md` comes from a pinned-znc Zag binary. Shell was used only for:
worktree creation, `cat` concatenation of Zag sources, `sed -E -f ren.sed`
mechanical rename, `znc` invocation, running the produced binaries, `sha256sum`,
`diff`, `grep`, and `git`.

## Determinism gate

Every binary is run 3 times via `tools/zbuild.sh <src> --rep 3`, which asserts
3/3 byte-identical stdout. Per-binary sha256 recorded in `REPORT.md`.

## Output path

`_zag_raw_syscall` is INERT on this host (brief section 4.0). This lane uses
`_zag_print` on every output path. Every driver asserts emitted byte count > 0
in-binary (K1) in addition to the shell check.