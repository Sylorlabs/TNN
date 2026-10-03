# NAMECHECK.md: Strong Learning-to-Learn Worker

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
- All computation in pure Zag via pinned znc (`src/tools/toolchain/znc_linux_x86_64_abed8aa1`).
- Shell used only for: invoking znc, running binaries, git ops, file moves.
- Zero forbidden executables invoked.

## Base

- `sl2l_base.zag`: verbatim copy of `adaptive_threshold/at_core_adaptive.zag` (Node2-v2 + adaptive threshold splice).
- `sl2l_mech.zag`: adaptive machinery extracted from `adaptive_threshold/at_tests.zag` lines 1-113 (at_get_default, at_reveal, at_ev_get, resolve_uncertainty_adaptive, at_guide_action). No modifications.
- `sl2l_driver.zag`: new 4-arm driver (this worker).

## Constraints honored

- Unfrozen variant only. Frozen source read-only.
- Pure Zag. Zero em/en dashes in docs (byte-verified before commit).
- Research paper untouched.
- Nothing pushed (local commits only).
