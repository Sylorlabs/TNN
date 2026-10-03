# NAMECHECK.md: Bar Counter

## Step 0: Toolchain Guard

- Safebin activated at `$HOME/safebin` (36 allowed tools linked: coreutils, git, pinned znc).
- `which python3 python` returned nothing. Guard check passed.
- Zero forbidden executables invoked. This task used only: `ls`, `grep`, `sed`, `git log`, `mkdir`, `cat` (read-only on inputs; writes only to the owned output directory).
- No code written or executed. Count and inventory only.

## Scope

Count and categorize every kill bar drafted during the overnight TNN-2/TNN-3 cycle. No new bars created. No bar text modified.

## Input provenance (read-only)

| Source document | Commit | Bars contributed |
|---|---|---|
| `tnn3_killbars/TNN3_KILLBARS_DRAFT.md` | `76231baa8` | 11 (K-T3-*) |
| `tnn2_h3lite/H3LITE_DESIGN.md` | `22197da2c` | 1 (K-H3) |
| `tnn2_targetsel/TARGET_SELECTION_DESIGN.md` | `01c2aacfe` | 2 (K-TSEL-1/2) |
| `tnn2_reusepath/REUSE_PATH_DESIGN.md` | `5f15b9309` | 2 (K-REUSE-1/2) |
| `tnn2_h2probes/H2_PROBE_DESIGN.md` | `4631c5918` | 4 (K-H2-1/2/3/4) |
| `gap_bars/GAP_BARS.md` | `36e5a70e1` | 4 (K-COMP-OP, K-INQ-INFO, K-XMECH, K-STATE-RET) |
| `tnn3_prereg_struct/PREREG_STRUCTURE.md` | `206499c03` | synthesis only (no new bars) |

All 7 commits verified via `git log` on the branch `tnn-native-lab`.

## Constraints honored

- Owned path only: `docs/lab/research-lead/overnight-20260928/bar_inventory/`.
- Count only. No new bars.
- No em dashes (byte-verified).
- Paper untouched.
- No sealed world contents inspected.
