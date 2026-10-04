# NAMECHECK: H-DECEPT-3 (belief_repeated)

## Step 0: Toolchain guard (mandatory, before any work)

Executed 2026-10-02 before any file was written:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp \
  sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` printed NOTHING (no forbidden executable
resolves in the safebin PATH). Only `guard-check-done` was echoed.
znc resolves: `znc 2026.07.0-dev (edition 2026)`.
Safebin tools confirmed present: git, znc, sh, bash, ls, cp, mv, rm,
mkdir, cat, grep, sed, awk, wc, cmp, sha256sum, plus coreutils
(basename, chmod, cut, date, diff, dirname, echo, find, head, ln, od,
printf, sort, stat, tail, tee, timeout, touch, tr, uname, uniq, which).

No python3/python invocation occurred at any point in this wave. All
research logic is pure Zag compiled with the pinned znc. Commit order
self check: PREREG.md and this NAMECHECK.md commit before any
implementation source exists (explicit pathspecs on every git
operation).

## Step 1: Frozen discipline

Unfrozen variant only. The frozen belief_deception sources, the frozen
belief_trajectory sources, the frozen C211/C223 sources, and the paper
are untouched. Nothing pushed to GitHub (commits stay local on
tnn-native-lab). Explicit pathspecs on all git add/commit commands.

## Step 2: Determinism

3/3 runs byte identical (sha256 recorded in REPORT.md). Stdout byte
verified with od -c spot check before trusting the binary output.
