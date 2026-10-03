# NAMECHECK.md: Meta-Learning Applicability Worker

## Step 0: Toolchain Guard (MANDATORY)

Activated: 2026-10-01

```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returns nothing. Guard check passed.

- Safebin PATH active for all build/run commands.
- All computation in pure Zag via pinned znc
  (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- Shell used only for: invoking znc, running binaries, git ops, file moves.
- Zero forbidden executables invoked.

## Base

- `ma_base.zag`: verbatim copy of
  `learning_to_learn/l2l_base_trim.zag` (TNN-2 base, no ev_query, no main).
- `ma_patch.zag`: APPL applicability mechanism (new) + two-pass rebind
  (`rb_chain_plen`, `pc_is_linked`, `pc_try_one` verbatim from
  `learning_to_learn/l2l_patch.zag`; `rebind_try` refactored to accept
  pre-gathered paths so the gate and rebind share one gather).
- `ma_driver.zag`: 3-arm driver (this worker). `build.sh` stamps the two
  hook functions per arm via sed (verified by grep counts).
- Full files: `ma_full_treat.zag`, `ma_full_fresh.zag`, `ma_full_naive.zag`
  (base + patch + driver, one `fn main` each).

## Constraints honored

- Unfrozen variant only. Frozen source read-only.
- Pure Zag. Zero em/en dashes in docs (byte-verified before commit).
- Research paper untouched.
- Nothing pushed (local commits only).
- 0 modes/bridges/handlers/semantic cases.
- No researcher domain labels anywhere in cognition. The applicability
  gate sees only observable problem features (path counts/plens, relation
  homogeneity, query relation). Domain identity is never an input.

## Implementation notes (2026-10-01)

- `ma_patch.zag` adds an `ev_query` wrapper (5-arg, matches trimmed-base
  test signature) that delegates to `ma_query` with fresh AP/ST. The base's
  built-in test battery references `ev_query`; the wrapper satisfies those
  references. The driver uses `ma_query` directly.
- Bug fixed: `rebind_try_paths` Pass 2 had `m=m-1` (should be `m=m+1`),
  causing negative node IDs and slice-out-of-bounds panic. Fixed 2026-10-01.
- Bug fixed: driver `main` was missing `tnn2_init(W)` after `z_alloc`.
  Without TNN-2 initialization, `t2_trial` fails (returns -2). The l2l
  driver's `main` calls `tnn2_init(W)`; the MA driver now does too.
- `ma_query` calls the trial via `mp_run` (base) which extracts
  masked/dc/di from flags. Trial verify counts read from `hg(W,16)`.
- Driver `main` saves C0 features to AP+1440 and runs counterfactual
  replay (`appl_decide` on saved C0 features under final weights).
