# NAMECHECK: H-DECEPT-4 (belief_antifarm)

## Step 0: Toolchain guard (mandatory, before any work)

Executed 2026-10-02 before any file was written:

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` printed NOTHING (no forbidden executable
resolves in the safebin PATH). Only `guard-check-done` was echoed.
znc resolves: `znc 2026.07.0-dev (edition 2026)` at
`/home/hatch/safebin/znc`.

No python3/python invocation occurred at any point in this wave. All
research logic is pure Zag compiled with the pinned znc. Commit order
self check: PREREG.md committed (e443c5bd9) strictly before any
implementation source existed; this NAMECHECK.md, the source, binary,
and run outputs are committed after the frozen runs completed.
Explicit pathspecs on every git operation.

## Step 1: Frozen discipline

Unfrozen variant only. The frozen belief_deception, belief_trajectory,
and belief_repeated sources are untouched (read only for reference).
The paper (TNN_RESEARCH_PAPER_20260929.md) is untouched. Nothing pushed
to GitHub: commits stay local on tnn-native-lab. Explicit pathspecs on
all git add/commit commands.

## Step 2: Determinism

Binary `belief_antifarm_bin` run 3 times; all exit 0; outputs byte
identical (sha256
4a6e18b39f561b6652c4ad7de3040288ed7bc40f0c5b4bb3e7a45d9a255327ae).
Stdout byte verified with od -c spot check (head and tail): clean
ASCII, ends with "ALL PASS\n". Single preallocated output buffer,
cursor returning emit helpers, one _zag_raw_syscall write; no
_zag_print anywhere (toolchain lesson 2026-10-02). u8-backed cells
with get32/set32 helpers; no `as *i32` slice construction.

## Step 3: Architecture accounting

Capability added to protected core: 0 lines. New hardcoded semantic
cases: 0. Modes/bridges/handlers: 0. Learner-state structures created:
1 (the per-source betrayal count cell, cell 3 of the source row;
source row widened 4 -> 5 cells, offsets recomputed, counted
honestly). Researcher-authored machinery: the betrayal-history rule
form (new, counted honestly, not learner-invented). Test
instrumentation: header cell 14 last_penalty reuse from H-DECEPT-3.
