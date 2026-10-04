# NAMECHECK: BELIEF-SEALED (sealed adversarial re-test of the antifarm rule)

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

No python3/python invocation occurred at any point in this wave. All
research logic is pure Zag compiled with the pinned znc. Commit order
self check: PREREG.md committed strictly before any sealed-world
implementation source existed; this NAMECHECK.md, the source, binary,
and run outputs are committed after the frozen runs completed.
Explicit pathspecs on every git operation.

## Step 1: Frozen discipline

Unfrozen variant only. The frozen belief_deception, belief_trajectory,
belief_repeated, and belief_antifarm sources are untouched (read only
for reference; the rule layer is copied byte-identical, verified by
diff, not retyped). The paper is untouched. Nothing pushed to GitHub:
commits stay local on tnn-native-lab. Explicit pathspecs on all git
add/commit commands.

## Step 2: Determinism

Binary `belief_sealed_bin` run 3 times; all exit 0; outputs byte
identical (sha256 recorded in REPORT.md). Stdout byte verified with
od -c spot check (head and tail): clean ASCII, ends with "ALL PASS\n".
Single preallocated output buffer, cursor returning emit helpers, one
_zag_raw_syscall write; no _zag_print anywhere (toolchain lesson
2026-10-02). u8-backed cells with get32/set32 helpers; no `as *i32`
slice construction.

## Step 3: Architecture accounting

Capability added to protected core: 0 lines. New hardcoded semantic
cases: 0. Modes/bridges/handlers: 0. Learner-state structures created:
0 (the per-source betrayal count cell is reused unchanged from
H-DECEPT-4). Researcher-authored machinery: the four sealed worlds
(new scenario code only; the rule layer is frozen). The binary asserts
the frozen PREREG rule predictions; per-world SURVIVE/KILL/BOUND
verdicts are scored in REPORT.md against the frozen rationality bars,
not by the binary.
