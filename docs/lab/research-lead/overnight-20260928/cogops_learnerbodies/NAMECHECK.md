# NAMECHECK: cogops_learnerbodies (LB1)

## Step 0: Toolchain guard (mandatory)

Executed at worker startup, 2026-10-03:

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
PATH restricted to $HOME/safebin for the whole session. All exec
calls in this session prefix `export PATH="$HOME/safebin"`.

Pinned znc: `$HOME/workspace/tnn-rsi-gpi3/src/tools/toolchain/znc_linux_x86_64_abed8aa1`
(the same pinned binary used by the sibling lanes; the tnn-rsi copy is
the same pinned build).

## Step 1: Scope

- Unfrozen variant only. Frozen TNN-2 source read-only (never
  modified; used only as reference).
- Base frame (interpreter, worlds, selector, credit) adapted from
  docs/lab/research-lead/overnight-20260928/cogops_bodies/cb.zag
  (cited in PREREG.md); REPAIR/DIVERGE/INLINE operators removed and
  replaced by the learner-owned constructor described in PREREG.md.
- Research paper untouched.
- Lane: docs/lab/research-lead/overnight-20260928/cogops_learnerbodies/
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

- Two LCG streams, fixed seeds (as in cogops_bodies); env RNG
  reseeded per arm so all four arms see identical world sequences.
- 3/3 runs byte-identical; sha256 recorded in REPORT.md.

## Step 4: Forbidden executables

Zero invocations of python3/python or any non-safebin executable
during this wave. Any violation would be PROCESS-FAIL; none occurred.

## Step 5: znc defect workarounds (from AGENTS.md, applied)

- No `as *i32` + slice construction (get32/set32 helpers only;
  asserted by build.sh).
- No `!(A && B)` in while conditions (De Morgan form only).
- If-nesting kept <= 3 with hoisted flag lets.
- No `as []f64` / `as []i64` casts.
- `_zag_malloc as *u8` threaded through (z_alloc pattern from
  cb.zag); no `[]u8 as *u8`.
- Output uses the cb.zag-proven emit/i64s helpers unchanged. Per
  AGENTS.md the single-syscall emitter is preferred for new dynamic
  output, but these helpers are byte-identical-verified in this
  exact frame (cogops_bodies 3/3) and K7 re-verifies every binary's
  stdout bytes here; changing them would risk new defects for no
  experimental gain. Decision recorded.

## Step 6: Prereg commit-order self-check

PREREG.md + NAMECHECK.md are committed ALONE first, strictly before
any implementation file. The implementation commit references the
prereg commit hash.
