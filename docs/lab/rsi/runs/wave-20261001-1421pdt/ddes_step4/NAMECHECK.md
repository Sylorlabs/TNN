# NAMECHECK.md - DDES V2 step 4 independent reproduction lane

Wave: wave-20261001-1421pdt. Lane: ddes_step4 (pipeline step 4,
independent reproduction from committed source). Lane owner: worker
d0e09bcb (this task runs inline; the descendant-subagent runtime defect
is a parent-orchestrator concern; this lane does not spawn workers).

## Step 0: Toolchain Guard Check (mandatory)

Date: 2026-10-01. Before any work:

1. Ran `bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
   (36 tools linked; znc pinned and OK).
2. `export PATH="$HOME/safebin"` for every subsequent command.
3. `which python3` prints nothing (exit 1). Safebin rollout verify line
   printed SAFEBIN-READY.

Result: python3 and python are absent from the active PATH. Zero
forbidden-executable invocations this lane (all work is shell, git,
the pinned znc, sha256sum, grep, od, and coreutils). Pure Zag only:
the only compiled program is the extracted committed Zag source;
analysis is shell commands only, no interpreted logic beyond
checksumming and byte comparison.

## Mission

Step 4 of the 11-step pipeline for DDES follow-up V2
(wave-20261001-1121pdt, BUILD-PASS): reproduce the sealed evaluation
from the COMMITTED source only. Verify tracked status, extract with
`git show HEAD:<path>`, do not edit, compile with the pinned znc, run
the sealed protocol exactly as frozen, compare sha256 against the
wave's run1.txt/run2.txt/run3.txt. Report REPRODUCED or NOT-REPRODUCED.

Frozen prereg: docs/lab/rsi/runs/wave-20261001-0821pdt/ddes/
PREREG_DDES_FOLLOWUP_V2.md plus AMENDMENT1 (re-frozen K-G1). Claimed
boundaries: bounded L2, no L3 claim.

## Provenance checks (all pass)

- `git ls-files` lists docs/lab/rsi/runs/wave-20261001-1121pdt/ddes/
  ddesp2.zag as TRACKED; committed in 3420bff8e (wave-20261001-1121pdt
  ddes lane commit, after AMENDMENT1 re-freeze).
- 3420bff8e is an ancestor of HEAD (1963e994dd549dd6bb32360d3e44ff51ca79a64e).
- `git show HEAD:.../ddesp2.zag` extracted to this lane as
  ddesp2_repro.zag (21229 bytes); `git diff --no-index` against the
  worktree ddesp2.zag: zero differences. Source was NOT edited.

## Build and run

- Pinned znc (~/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1):
  exit 0, executable ddesp2_repro_bin produced.
- repro_build.err: 93 bytes, the single documented unconditional
  zagd-availability warning line (byte-identical class to the R2
  REPAIR-PASS build evidence), zero other bytes.
- repro_run1/2/3: exit 0, 1004 bytes each, zero stderr bytes each.

No em dashes or en dashes in any lane file (byte-checked before this
write; none written). No commits, pushes, checkouts, or branch changes
made by this lane (files left uncommitted per task).
