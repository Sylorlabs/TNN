# NAMECHECK: learner_wiring_lw2 (LW2)

## Step 0: Toolchain guard (2026-10-02, before any implementation)

Setup executed:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum \
         git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
```

Verification results:
- `which python3 python` -> no output (both unresolvable). PASS.
- `command -v znc` -> /home/hatch/safebin/znc, `znc version` reports
  znc 2026.07.0-dev (edition 2026). PASS.
- Guard output line "guard-check-done" observed with no python paths
  above it.

Guard verdict: PASS. No forbidden executable is resolvable under the
worker PATH. All build, run, and analysis steps in this directory use only
$HOME/safebin on PATH.

## Step 1: Preregistration order

PREREG.md written and committed BEFORE any implementation file existed in
this directory. Commit order verified via git log on the pathspecs below.
At the prereg commit, this directory contained only PREREG.md and
NAMECHECK.md.

## Step 2: Forbidden-interpreter scan

- `grep -r` over this directory for python invocations: none (this file
  records the scan; the scan itself ran under the safebin PATH).
- build.sh uses only sh, znc, sha256sum, cmp, and the built binary.

## Step 3: Determinism check method

Each condition binary run is executed 3 times; sha256sum of stdout is
compared across the 3 runs and must match exactly (P5). Run outputs are
stored under runs/. cmp is also applied pairwise as a second check.

## Step 4: Output byte verification

Per the pinned-znc stdout lesson, every binary's stdout bytes are verified
against the preregistered predictions before any claim is trusted. The
single-buffer emit path (one preallocated buffer, one raw syscall write)
is used for all dynamic output; _zag_print is not used. The allocator is
lw_alloc on _zag_malloc (this znc build has no nio_alloc); all state
cells are u8-backed with little-endian put64/get64 helpers; no
`as *i32` slice construction inside functions.

## Step 5: Em/en dash scan

All documentation in this directory is scanned for em dashes and en
dashes before commit; none are permitted in loop documentation.
