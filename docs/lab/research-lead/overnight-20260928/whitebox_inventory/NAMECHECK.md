# NAMECHECK: White-Box Interrogator

## Step 0: Toolchain guard

- Safebin activated: `export PATH="$HOME/safebin"` run before all work.
- `which python3 python` returned nothing. Zero forbidden executables invoked.
- All computation in pure Zag (`inspect_state.zag`, compiled with the pinned
  `znc_linux_x86_64_abed8aa1`). Shell used only to invoke znc, run the
  binary, and move files.

## Scope

Read-only white-box inventory of frozen TNN-2 learner state.

## Input provenance

- Layout constants extracted by READING `tnn2_build/tnn2.zag`
  (SHA-256 prefix `a29972ca8183b285`). The file was never modified.
- State bins read: `core_freeze_tnn2_eval/runs/fw_run1/fw{1,2,3,4,5,6,6b,7,8}_state.bin`,
  `fw_run1/state.bin`, `w_run1/state.bin`. These are evaluator-saved learner
  states, read via `_zag_read_file`. No sealed world definition files opened.
- The frozen `tnn2_bin` was never executed by this worker. A separate
  inspector binary (`inspect_state_bin`, built from `inspect_state.zag`)
  was the only binary run.

## Constraints honored

- READ-ONLY: no state file modified, no TNN-2 source modified, no sealed
  world executed or opened.
- Zero em dashes in all deliverables (byte-verified).
- Paper untouched. Nothing pushed.

## Deliverables

- `inspect_state.zag` (the inspector source)
- `inspect_state_bin` (compiled inspector)
- `WHITEBOX_INVENTORY.md` (the inventory)
- Raw dumps: `fw_cumulative.txt`, `fw1_only.txt`, `w_cumulative.txt`,
  `fw{2,3,4,5,6,6b,7,8}_chk.txt`

## Verdict

WHITEBOX-INVENTORY-COMPLETE.
