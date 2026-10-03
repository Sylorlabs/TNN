# NAMECHECK: goalinf_decoyfix

Worker: Goalinf Decoy-Structure Repair Worker (RETRY-2).
Task: repair goal-inference decoy-structure kill (Attack A, red-team 808ee293f).

## Step 0: toolchain guard (mandatory)

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

Result: `which python3 python` printed nothing; only `guard-check-done`.
Neither python3 nor python resolves in the worker PATH. All shell work
uses safebin tools only (sh, bash, ls, cp, mv, rm, mkdir, cat, grep,
sed, awk, wc, cmp, sha256sum, git). All computational research logic is
implemented in Zag and compiled with the pinned znc. No forbidden
executable invoked. Guard: PASS.

## Prereg commit order

PREREG.md written and committed before any implementation source file
was created. Self-check: the commit adding PREREG.md (and NAMECHECK.md)
strictly precedes the commit adding src/*.zag. Implementation commits
reference the frozen prereg; no post-hoc bar changes.

## Build verification

Each binary's stdout bytes are verified directly (od -c / sha256sum)
before any verdict is trusted, per the emit-helper discipline: all
dynamic output is formatted into one preallocated buffer with
cursor-returning emit helpers (e1put/e1str/e1i64) and written with a
single _zag_raw_syscall(1,1,ptr,len). _zag_print is never used for
dynamic content.

## Commit log (local only, never pushed)

* c1f0e5c30 PREREG.md + NAMECHECK.md frozen (no src yet)
* 53a50e762 src/*.zag implementation
* 5b17c2e16 bin/* compiled binaries + outputs/*.txt + sha256sums.txt
* dd1b403b6 REPORT.md + NAMECHECK.md SHAs

(SHAs filled at commit time.)
