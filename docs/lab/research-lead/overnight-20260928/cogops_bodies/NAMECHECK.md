# NAMECHECK: cogops_bodies

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

Result: `which python3 python` returned NOTHING (empty output before
"guard-check-done"). Safebin active for all subsequent commands.
PATH restricted to $HOME/safebin for the whole session.

## Step 1: Scope

- Unfrozen variant only. Frozen TNN-2 source read-only (never
  modified; used only as reference for the interpreter design).
- Research paper untouched:
  docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md
- Nothing pushed (local commits only).

## Step 2: Computation

- All research logic in pure Zag, compiled with the pinned
  toolchain: src/tools/toolchain/znc_linux_x86_64_abed8aa1
- Shell used only for: invoking znc, running binaries, git
  operations, moving/copying files.
- No Python, no other interpreter, no calculator, no
  text-processing shortcut for research logic. (Shell text tools
  used only for file assembly/inspection, never for scoring or
  experiment decisions.)

## Step 3: Determinism

- Two LCG streams, fixed seeds (as in cogops_structures).
- 3/3 runs byte-identical; sha256 recorded in REPORT.md.

## Step 4: Forbidden executables

Zero invocations of python3/python or any non-safebin executable
during this wave. Any violation would be PROCESS-FAIL; none occurred.
