# NAMECHECK: cogops_adaptiveplen

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, 2026-10-03:

```
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned NOTHING (empty output before
"guard-check-done"). Safebin active for all subsequent commands.
PATH restricted to $HOME/safebin for the whole session.

Pinned znc: `$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(the same pinned binary used by the sibling lanes; verified present
before use).

Worktree: `$HOME/workspace/tnn-rsi-gpi3` on branch `tnn-native-lab`.

## Step 1: Scope

- Unfrozen variant only. Frozen TNN-2 source read-only (never
  modified; used only as reference).
- Base frame (interpreter, worlds, selector, credit, constructor,
  P1 composite fitness, P2 compression, refinement) adapted from
  docs/lab/research-lead/overnight-20260928/cogops_parsimony/pp.zag
  (cited in PREREG.md); the ONLY behavioral changes are:
  (a) the hardcoded PLEN=3 in pop_fit/off_beats_pop becomes
  plen_of(S) (==3 for pmode!=3, learner cell 2370 for pmode==3);
  (b) new pmode 3 (A-FULL) with per-generation plen_adapt and
  post-adopt PLEN updates; (c) inversion diagnostic counting
  (pmode==3 only, reporting only). pmode 0 (NP) and pmode 2
  (F-FULL) paths must replicate LB1 arm 0 and PARSIMONY P-FULL
  exactly (K3).
- Research paper untouched.
- Lane: docs/lab/research-lead/overnight-20260928/cogops_adaptiveplen/
  on branch tnn-native-lab. Nothing pushed (local commits only,
  explicit pathspecs).

## Step 2: Computation

- All research logic in pure Zag, compiled with the pinned znc.
- Shell used only for: invoking znc, running binaries, git
  operations, moving/copying files, and build.sh guard greps.
- No Python, no other interpreter, no calculator, no
  text-processing shortcut for research logic. (Shell text tools
  used only for file assembly/inspection and guard assertions,
  never for scoring or experiment decisions.)

## Step 3: Determinism

- Two LCG streams, fixed seeds (as in cogops_parsimony); fresh
  learner state per arm with identical seeds so all three arms
  see identical world sequences.
- 3/3 runs byte-identical; sha256 recorded in REPORT.md.

## Step 4: Forbidden executables

Zero invocations of python3/python or any non-safebin executable
during this wave. Any violation would be PROCESS-FAIL; none occurred.

## Step 5: znc defect workarounds (from AGENTS.md, applied)

- No `as *i32` + slice construction (get32/set32 helpers only;
  asserted by build.sh).
- No `!(A && B)` in while conditions (flag lets only;
  asserted by build.sh).
- If-nesting kept <= 3 with hoisted flag lets.
- No `as []f64` / `as []i64` casts.
- `_zag_malloc as *u8` threaded through (z_alloc pattern from
  pp.zag); no `[]u8 as *u8`.
- No `break`/`continue` in while loops (flag-let pattern).
- Output uses the pp.zag-proven emit/i64s helpers unchanged;
  K7 re-verifies every binary's stdout bytes.

## Step 6: Prereg commit-order self-check

PREREG.md + NAMECHECK.md are committed ALONE first, strictly before
any implementation file. The implementation commit references the
prereg commit hash.
