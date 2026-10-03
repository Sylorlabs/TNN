# NAMECHECK: utility_signal (Utility Signal Designer)

## Step 0: Toolchain guard (mandatory, recorded before any work)

Executed at task start:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING. `guard-check-done` printed.
Neither `python3` nor `python` resolves in the safebin PATH.

## Scope declaration

- DESIGN ONLY. No implementation, no unfrozen variant, no binary built, no experiment run.
- Frozen source treated as READ-ONLY reference (field-layout reads via grep/awk only).
- No frozen file modified. No sealed world opened.
- Paper (`TNN_RESEARCH_PAPER_20260929.md`) untouched.
- Nothing pushed. Local commit only.

## Toolchain compliance

- All file reads and text processing done via shell builtins and safebin tools
  (grep, awk, sed, cat, ls, mkdir).
- No Python, C, JavaScript, or Rust invoked at any point in this task.
- `which python3 python` verified empty AFTER safebin activation, before any work.

## Forbidden-executable record

- Forbidden executables invoked during this design task: NONE.
- Process status: CLEAN (no PROCESS-FAIL condition triggered).

## Deliverables

- `UTILITY_SIGNAL.md`: analysis of the bid failure, learner-owned utility
  mechanism design, integration specification, One-System Rule audit.
- This file.
- Committed with explicit pathspecs only.
