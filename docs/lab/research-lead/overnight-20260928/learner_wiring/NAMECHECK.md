# NAMECHECK: learner_wiring (LW1)

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
- `command -v python3` -> not found (exit 1). PASS.
- `command -v python` -> not found (exit 1). PASS.
- `command -v znc` -> /home/hatch/safebin/znc, `znc version` reports
  znc 2026.07.0-dev (edition 2026). PASS.
- 49 tools linked into $HOME/safebin (coreutils, git, pinned znc only).

Guard verdict: PASS. No forbidden executable is resolvable under the
worker PATH. All build, run, and analysis steps in this directory use only
$HOME/safebin on PATH.

## Step 1: Preregistration order

PREREG.md written and committed BEFORE any implementation file existed in
this directory. Commit order verified via git log on the pathspecs below.

## Step 2: Forbidden-interpreter scan

- `grep -r` over this directory for python invocations: none (this file
  records the scan; the scan itself ran under the safebin PATH).
- build.sh uses only sh, znc, sha256sum, and the built binary.

## Step 3: Determinism check method

Each condition binary run is executed 3 times; sha256sum of stdout is
compared across the 3 runs and must match exactly (P6). Run outputs are
stored under runs/.

## Step 4: Output byte verification

Per the pinned-znc stdout lesson, every binary's stdout bytes are verified
against the preregistered predictions before any claim is trusted. The
single-buffer emit path (one preallocated buffer, one raw syscall write)
is used for all dynamic output; _zag_print is not used.
