# NAMECHECK.md -- Invention H3 Red-Team Worker (adversarial)

## Step 0: Toolchain guard (mandatory)

Executed at startup:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returns nothing. `guard-check-done` printed.
Safebin active for all subsequent commands. Zero forbidden executables
invoked. Pure Zag for all computational research operations.

## Step 1: Identity

Worker: Invention H3 red team (independent adversarial attack).
Target: commits 75583d6ee (prereg) and 31391237a (results) in
`docs/lab/research-lead/overnight-20260928/invention_constraint/`.
Claim under test: backtracking DFS over individual facts pruned by goal
constraints constructs novel MAP forms; trial is form-blind; construction
uses facts, never selects existing MAPs.

## Step 2: Base and mechanism under test

- Base: `../composition_C/cc_base.zag` lines 1-1677, copied to
  `rt_base.zag` as a frozen reference. Never modified.
- Mechanism under test: `../invention_constraint/invent_patch.zag`,
  copied to `rt_mech.zag` byte-identical. Never modified. This is the
  artifact being attacked; all red-team drivers call its `ev_query_c` /
  `invent_try` / `invent_check` entry points exactly as the H3 driver did.
- Red-team drivers (`rt_driver_*.zag`) are new, unfrozen, adversarial
  worlds and constraint sets. They contain no changes to the mechanism.

## Step 3: Outputs

- `NAMECHECK.md` (this file)
- `REPORT.md`: per-attack verdicts KILL / BOUND / SURVIVE
- `rt_base.zag`: frozen base reference copy
- `rt_mech.zag`: frozen mechanism copy (system under test)
- `rt_driver_*.zag`: adversarial drivers (new)
- `rt_full_*.zag`: assembled sources
- `rt_bin_*`: compiled binaries (pinned znc)
- `rt_run*.txt`: run transcripts (3x each, byte-identical check)
- `rt_timing.txt`: scaling measurements

Pure Zag. Paper untouched. Nothing pushed. 0 modes/bridges/handlers.
No em/en dashes in loop documentation.
