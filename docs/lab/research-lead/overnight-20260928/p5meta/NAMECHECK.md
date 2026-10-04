# NAMECHECK: p5meta

- lane: p5meta, worktree /Users/Shared/micah/Documents/TNN/.worktrees/p5meta
- base commit at lane creation: 87a822426
- toolchain: /Users/Shared/micah/Documents/TNN/.bin/znc --target macos-arm64
  --no-zagd --no-analyze --no-foreground-cache
- pure-zag report: VERDICT: PURE-ZAG-CLEAN (forbidden_count=0); PATH shims only
- no _zag_raw_syscall used for output anywhere; _zag_print / _zag_println only
  (brief 4.0). No forbidden executable was invoked in this lane.

## commits (explicit pathspecs, never `git commit -a`, never pushed)
- 24c133b42  PREREG.md + NAMECHECK.md ONLY, no .zag. prereg frozen alone.
- 4ccea61be  p5.zag + diag.zag + diag_run{1,2,3}.txt + REPORT.md

## sha256
- p5.zag         ddffded2f3b69f4255640c625ca90ff97afb1c88b688293fd1ac4afa14638012
- diag.zag       634fc49c55f4fbfbd6ca28feb79591ebfa60fa075abbc2e87b37e481a32cbedd
- diag_run*.txt  8a86b09353bc4327222c04a417d0462e9a1b4e35a9f0ae9d8d41bd35b02aae4e
  (cmp run1==run2==run3: PASS, 3/3 byte-identical, non-empty: 15 labelled lines)

## status
BLOCKED. diag.zag passes; p5.zag run_ep returns an internally inconsistent
record. No kill bar evaluated, no verdict, no claim. See REPORT.md.
