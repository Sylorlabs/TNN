# NAMECHECK.md -- Prereg Checker

Worker: Prereg Checker (subagent of the TNN research coordinator).
Task: Check if the TNN-3 preregistration is ready to be frozen.
Verdict discipline: PREREG-CHECK-COMPLETE on completion.

## Step 0: Toolchain guard

Date: 2026-10-01 (UTC).

Setup run at worker start:
```
mkdir -p $HOME/safebin
for t in git znc sh bash ls cp mv rm mkdir cat grep sed awk wc cmp sha256sum git-receive-pack git-upload-pack; do
  p=$(which $t 2>/dev/null | head -1)
  [ -n "$p" ] && [ ! -e $HOME/safebin/$t ] && ln -sf $p $HOME/safebin/$t
done
export PATH="$HOME/safebin"
which python3 python 2>/dev/null; echo "guard-check-done"
```

Result: `which python3 python` returned nothing under the safebin PATH.
Zero forbidden executables invoked during this task.
All file reads were via the read tool; all writes to the owned
`prereg_check/` directory only. Git operations (log, show) read-only.

## Scope

Check only. This worker did NOT write, freeze, amend, or weaken any
preregistration or kill bar. No implementation. No source edits.
No sealed contents inspected.

## Inputs consulted (all committed, read-only)

- `tnn3_prereg_struct/PREREG_STRUCTURE.md` (`206499c03`): bar inventory,
  dependencies, priority order, gaps, the 10-section frozen-prereg outline,
  the 6 open questions.
- `tnn3_killbars/TNN3_KILLBARS_DRAFT.md` (`76231baa8`): 11 bars, DRAFT-NOT-FROZEN.
- `tnn3_killbar_review/KILLBAR_REVIEW.md` (`eb354e3a2`): achievability review,
  recommendations on Q1-Q6, redundancy check.
- `gap_bars/GAP_BARS.md` (`36e5a70e1`): K-H2-1..4, K-COMP-OP, K-INQ-INFO,
  K-XMECH, K-STATE-RET, DRAFT-NOT-FROZEN.
- `bar_inventory/BAR_INVENTORY.md` (`1722884ad`): 24 bars counted, no duplicates.
- `bar_priority/BAR_PRIORITY.md` (`20d810d4b`): 21 minimal bars ordered P0-P4+PX.
- `roadmap_update/ROADMAP_WITH_BARS.md` (in `bbe79ddf1`): bars mapped to roadmap phases.
- `treadmill_guard/TREADMILL_GUARD.md` (`1646b9732`): DRAFT guard spec.
- `property_name/PROPERTY_DEFINITION.md` (`64eec921f`): SUF, PROPOSAL status.
- `floor_preserve/FLOOR_SPEC.md` (`f383dd11c`): DRAFT preservation spec, 7 capabilities.
- `protected_core_decision/PROTECTED_CORE_BRIEF.md` (`092566072`): PREPARED FOR MICAH - NOT DECIDED.
- `morning_checklist/MORNING_CHECKLIST.md` (`d895c7b44`): the 4 banked decisions.
- `tnn2_h3lite/H3LITE_DESIGN.md` (`22197da2c`): K-H3, DRAFT-NOT-FROZEN.

## Constraints honored

Owned path only (`prereg_check/`). No em dashes in documentation
(byte-verified before commit). Paper untouched
(`docs/lab/research-lead/overnight-20260928/TNN_RESEARCH_PAPER_20260929.md`
not modified; `git status --porcelain` on it empty). Explicit pathspecs on
commit. Nothing pushed.
