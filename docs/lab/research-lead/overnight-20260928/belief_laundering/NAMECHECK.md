# NAMECHECK: Belief Laundering Mitigation Worker

Worker: belief laundering mitigation (parameter free mitigation for the
C286 forgiveness rule laundering vulnerability).
Task: reproduce the R,R,W laundering attack, design a parameter free
mitigation using only learner owned state, and test that it blocks
laundering while preserving legitimate forgiveness.
Lane: unfrozen only. Frozen read-only. Paper untouched. Nothing pushed.

## Step 0: toolchain guard (mandatory, recorded before any work)

Setup executed 2026-10-02:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```
Result: `which python3 python` returned nothing; guard-check-done printed.
PATH=/home/hatch/safebin. No forbidden executables available to this
worker. Pure Zag for all research logic (compile via znc, run binaries,
shell only for file and git ops). Any forbidden executable invocation
would be PROCESS-FAIL; none occurred.

## Step 1: prereg commit-order self-check

PREREG.md and NAMECHECK.md commit strictly before any implementation
source exists. Verify with: git log --oneline -- <prereg paths> precedes
the implementation commit; and the prereg commit tree contains no .zag
source for this experiment.

## Step 2: determinism

3/3 runs byte identical: sha256(run1.txt) == sha256(run2.txt) ==
sha256(run3.txt). Any mismatch is PROCESS-FAIL for the wave.

## Step 3: governance

0 modes, 0 bridges, 0 handlers, 0 new semantic cases. Unfrozen variant
only (new directory belief_laundering/). Frozen source untouched.
Paper untouched. Nothing pushed (commits local only). Explicit
pathspecs on every git add/commit.

## Step 4: toolchain lessons applied (AGENTS.md)

- Single preallocated output buffer, cursor returning emit helpers
  (e_str/e_i64), one _zag_raw_syscall write at the end. No _zag_print.
- No `as *i32` + `q[0..n]` slice construction inside functions.
- `as []f64` style casts not used; no .len trusted on cast slices.
- New learner cell `ret` uses the established u8 backed cell block with
  get32/set32 helpers, same as all other per source state.
- Byte verify binary stdout before trusting it (od -c spot check,
  sha256 across the three runs).
