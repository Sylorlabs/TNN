# NAMECHECK: H1-L2 Integration Worker

Task: test whether H1's learned type contracts can DRIVE L2 adaptation.
The type mismatch must be the TRIGGER for adaptation, and the mismatch
type must GUIDE which adaptation operator the learner selects.

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, 2026-10-02:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` printed NOTHING before `guard-check-done`.
No forbidden executable is reachable in this worker's PATH.

Compiler check: `sha256sum` of `$HOME/safebin/znc` equals the sha256 of
`~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1`:
`498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef`.
All computation in this task is pure Zag; shell is used only to invoke
znc, run binaries, and do git/file operations.

## Step 1: Preregistration first

PREREG.md written and committed ALONE before any implementation source.
Commit order self-check: the prereg commit strictly precedes the
implementation commit. No kill bar may be weakened after results.

## Step 2: Implementation

Single-file `hl.zag` plus one-line-toggle ablation variant `hl_na.zag`
(diff-verified to differ by exactly the `type_on` line, mirroring the
L2 lane's adapt_on methodology). Pinned compiler only.

## Step 3: Determinism

3/3 byte-identical runs per binary; sha256 digests recorded in REPORT.md.
Stdout bytes verified for the znc print miscompile (single-buffer emit
plus one raw write syscall per the mandatory workaround).

## Step 4: Report

REPORT.md with per-bar verdicts naming the exact frozen bars, cost notes,
architecture accounting, and honest boundaries. Committed with explicit
pathspecs. Nothing pushed.
