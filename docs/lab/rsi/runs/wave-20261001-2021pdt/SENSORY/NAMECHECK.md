# NAMECHECK.md - wave-20261001-2021pdt SENSORY lane

Worker: sensory lane research worker (depth 2/2), started 2026-10-01 20:26 PDT.
Lane dir (ALL output): docs/lab/rsi/runs/wave-20261001-2021pdt/SENSORY/
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.
No git commits, no git push, .wave_lock untouched. No child subagents.
Phase 1 (this file's scope): PREREG_SENSORY_H1V2.md WRITING ONLY.
No H1v2 generator, verifier, render, or binary exists.

## Step 0: Toolchain guard activation (recorded before any other work)

Commands run:
```
bash ~/workspace/tnn-rsi/docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
export PATH="$HOME/safebin"
which python3
```
Outputs:
```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
SAFEBIN PATH ACTIVE
which python3 exit: 1
```
`which python3` prints NOTHING (exit 1). Guard check: PASS, not blocked.
Effective PATH during all work: /home/hatch/safebin only.
Toolchain pinned: src/tools/toolchain/znc_linux_x86_64_abed8aa1,
sha256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef
(matches the frozen toolchain hash from wave-20260924-1121pdt).
Pure Zag only.

Forbidden set: python3, python, node, any compiler or interpreter outside
safebin. Shell, git (read-only + local file writes, no commits), znc, and
safebin coreutils only. Em/en dash byte checks use the shell-only snippet
docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh.

## Step 1: Prereg ordering evidence (phase 1)

PREREG_SENSORY_H1V2.md is written in this phase, before any H1v2
implementation artifact exists. Ordering evidence: this NAMECHECK.md
Step 0/Step 1 and the prereg file's mtime + sha256 predate every H1v2
source, binary, render, and verifier artifact. The coordinator commits
the prereg alone; implementation begins only after that commit.
UNVERIFIABLE ORDERING voids the prereg.

Context re-derived from (not cited from memory):
- docs/lab/rsi/runs/wave-20261001-1721pdt/SENSORY/PREREG_H1_CLOUDS_1721.md
- docs/lab/rsi/runs/wave-20261001-1721pdt/SENSORY/VERDICT_H1_DISCARDED.md
- docs/lab/rsi/runs/wave-20261001-1721pdt/SENSORY/JUDGE_BRIEF.md
- docs/lab/rsi/runs/wave-20261001-1721pdt/SENSORY/h1/h1_clouds.zag
  (frozen block lines 268-320; frozen 3D sun b_sunx/y/z = -0.617, 0.191,
  -0.764 at lines 191-193; frozen azimuth (-0.628, -0.778) used at
  lines 242, 291, 295-296)

## Step 2: Forbidden-executable audit (phase 1)

Phase 1 scope is writing only: no computational step ran. One `git`
status/branch read (read-only), `ls`, `sed`/`grep` reads of prior-wave
sources, and file writes. Zero invocations of python3, python, node, or
any interpreter/compiler outside safebin. No PROCESS-FAIL.
