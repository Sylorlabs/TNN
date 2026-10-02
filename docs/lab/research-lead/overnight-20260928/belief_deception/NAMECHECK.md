# NAMECHECK: Belief Deception Worker (H-DECEPT-1, P1)

Worker: H-DECEPT-1 belief deception.
Task: belief-stance trajectories detect source defection.
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
shell only for file and git ops).

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
only (new directory belief_deception/). Frozen source untouched. Paper
untouched. Nothing pushed (commits local only). Explicit pathspecs on
every git add and git commit. No em/en dashes in loop documentation.

## Step 4: verdict discipline

Verdict names the exact frozen bars (K1-K5) and the frozen hypothesis
verdict rule from PREREG.md. A moved bar invalidates the verdict.
H-DECEPT-1 is supported / partially supported / not supported per the
frozen rule only.
