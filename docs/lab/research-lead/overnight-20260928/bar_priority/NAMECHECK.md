# NAMECHECK.md -- Bar Prioritizer

## Step 0: Toolchain guard (mandatory)

- Ran the safebin setup: `mkdir -p $HOME/safebin`, symlinked the 17
  allowed tools (git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat,
  grep, sed, awk, wc, cmp, sha256sum, git-receive-pack,
  git-upload-pack), exported `PATH="$HOME/safebin"`.
- Verification: `which python3 python` printed nothing
  (guard-check-done). No forbidden executable was invoked at any
  point in this task.
- Any forbidden executable invocation would have been an automatic
  PROCESS-FAIL. None occurred.

## Scope

Prioritize the 24 kill bars inventoried in `bar_inventory/`
(commit `1722884ad`) for implementation and evaluation order.
Prioritization only: no new bars created, no bar text modified,
no implementation, no source edits.

## Input provenance (all read-only)

- Bar inventory: `docs/lab/research-lead/overnight-20260928/bar_inventory/BAR_INVENTORY.md` (`1722884ad`)
- Prereg structure (dependencies, order): `docs/lab/research-lead/overnight-20260928/tnn3_prereg_struct/PREREG_STRUCTURE.md` (`206499c03`)
- Gap bars (K-H2 sub-clauses, K-COMP-OP, K-INQ-INFO, K-XMECH, K-STATE-RET): `docs/lab/research-lead/overnight-20260928/gap_bars/GAP_BARS.md` (`36e5a70e1`)
- Roadmap order: `67a420cca` (referenced, not re-read)

## Constraints honored

- Owned path only: `docs/lab/research-lead/overnight-20260928/bar_priority/`.
- Prioritize only. No new bars.
- No em dashes (byte-verified after writing).
- Research paper untouched.
- Nothing pushed; commit is local only.

## Verdict

BAR-PRIORITY-COMPLETE.
