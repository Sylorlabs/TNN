# CORE-FREEZE-TNN1 Root-Cause Analysis: NAMECHECK

Date: 2026-10-01. Worker: CORE-FREEZE-TNN1 Root-Cause Analyst (subagent).
Task: root-cause analysis of CORE-FREEZE-TNN1 failures per Micah's
directive (cluster into shared architectural causes, not per-world
patches). Analysis only; no source edits, no builds.

## Step 0: Toolchain guard (safebin)

- Set up restricted PATH before any work:
  linked git, znc, sh, bash, ls, cp, mv, rm, mkdir, cat, grep, sed,
  awk, wc, cmp, sha256sum, git-receive-pack, git-upload-pack into
  $HOME/safebin and exported PATH="$HOME/safebin".
- Verified: `command -v python3` and `command -v python` return
  nothing. Forbidden interpreters do not resolve in this PATH.
- This wave is analysis only (reading committed reports, transcripts,
  and frozen source; reasoning). No research computation was
  performed. No Python, C/C++, JavaScript, or Rust invoked.

## Step 1: Sources read

- `core_freeze_tnn1_eval/FREEZE_REPORT.md` (verdict
  FREEZE-EVAL-COMPLETE; FW 4/9; OLD-WORLD 4/9).
- Per-world transcripts in `core_freeze_tnn1_eval/runs/fw_run1/`
  (FW3, FW6 treatment/control/b-annex, FW7, FW8, FW9a/b, FW5).
- `core_freeze_tnn1/CORE_FREEZE_TNN1_PREREG.md` (frozen prereg
  60f1ff0bf; Micah's five rulings).
- `core_freeze_tnn1_shim/SHIM_REPORT.md` (shim zero-cognition
  attestation; K-FZ3).
- Frozen TNN-1 cognition path as preserved verbatim in
  `core_freeze_tnn1_shim/freeze_shim.zag` lines 1-1093, 1095-1328
  (`ev_query` 648, `ev_observe` 669, `ev_act` 691, `execute` 195,
  `exec_plan` 427, `mp_build` 498, plan templates 331-358).
- `core_freeze_tnn1_eval/run_fw_battery.sh` (FW6 responder contract).

## Step 2: Output

- `core_freeze_tnn1_eval/ROOT_CAUSE_ANALYSIS.md`: per-cluster
  architectural diagnosis, three pointed questions answered,
  shared-cause clustering into a 3-change minimal set, next
  generation build list, deprioritized items.
- This NAMECHECK file (Step 0 safebin record).

## Standing rules observed

- Owned path only: core_freeze_tnn1_eval/. Appended new files; did
  not modify FREEZE_REPORT.md or NAMECHECK.md.
- No TNN-1 or shim source edits. No new opcodes proposed. No
  per-world patches proposed.
- No em dashes in loop documentation.
- Contaminated paper untouched (zero-diff; file not opened).
- Explicit git pathspecs for the final commit.
