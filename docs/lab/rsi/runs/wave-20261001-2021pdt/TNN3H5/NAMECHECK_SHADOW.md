# NAMECHECK - TNN3H5 Shadow-Fact Root-Cause Diagnosis (Analysis Only)

## Step 0: Toolchain verification (MANDATORY per worker toolchain guard, Micah 2026-09-30)

- Ran `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`; SAFEBIN-READY: /home/hatch/safebin (36 tools, no python); znc OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1).
- Exported PATH="$HOME/safebin".
- Ran `which python3`: printed NOTHING (exit 1). Guard satisfied.
- This worker performs READ-ONLY analysis: grep/diff of committed files, re-run of committed binaries read-only. No new implementation, no new builds, no forbidden executables. No commits by this worker (coordinator commits).

## Step 1: Assignment

Lane TNN3H5-SHADOW, wave wave-20261001-2021pdt. Diagnose the shadow-fact root cause behind H5's red-team kill (H5 KILLED at commit dbf25e447; KB-B2 failed on MAP key; sealed logs show C1S bridge-query=100 and C2S bridge-query=900 stale originals on MAP-key queries after double contradiction). Deliverables: this file plus SHADOW_DIAGNOSIS.md.

## Step 2: Scope boundaries

- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab. No push. No git reset --hard. No rebase. No git commit.
- Write-only files in docs/lab/rsi/runs/wave-20261001-2021pdt/TNN3H5/: NAMECHECK_SHADOW.md, SHADOW_DIAGNOSIS.md.
- Documentation rule: no em-dashes anywhere.
