# NAMECHECK (REDTEAM): lane TNN3H1, wave-20261001-2021pdt

## Step 0: independent safebin activation

- Date: 2026-10-01 (task received 20:50 PDT).
- Ran `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  in the working copy /home/hatch/workspace/tnn-rsi, branch tnn-native-lab;
  PATH exported to $HOME/safebin only. Setup reported SAFEBIN-READY
  (36 tools, pinned znc OK).
- `which python3` prints NOTHING (exit 1). `which python` also absent per
  safebin verify output. Not BLOCKED.
- Independence: this worker is independent of the TNN3H1, TNN3H1-IMPL, and
  TNN3H1-ADVERSARY workers. No files shared with them except committed lane
  records read as evidence.

## Toolchain posture for this task

- READ-ONLY analysis. Shell used only for: safebin setup, `which` check,
  `grep`/`diff`/`sha256sum` over committed lane files, and writing the two
  deliverables (NAMECHECK_REDTEAM.md, REDTEAM_FABRICATION.md).
- Zero compilation, zero binary execution, zero forbidden executables.
- No `git commit`, no push, no reset, no rebase. All writes are new files
  inside docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H1/ only.
- Pure Zag observed trivially: this task performs no research logic at all,
  only read-only inspection and report writing.

## Step 0b: working copy state at start

- Branch: tnn-native-lab (confirmed via `git branch --show-current`).
- Lane directory exists with all builder/adversary artifacts present
  (PREREG_H1.md, IMPLEMENTATION.md, h1_dev.zag, h1_dev_run1.log, tnn3.zag,
  tnn3.zag.pre, tnn3_bin, SEALED_EVAL.md, adv_inspect.zag, etc.).
- Frozen baseline identity verified: sha256(tnn3.zag.pre) equals
  sha256(docs/lab/research-lead/overnight-20260928/tnn2_build/tnn2.zag)
  = a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd,
  matching the hash recorded in PREREG_H1.md and IMPLEMENTATION.md.
