# NAMECHECK.md: MECH-VERIFY lane, wave wave-20261001-2321pdt

## Step 0: worker toolchain guard (mandatory, first)

- Ran `sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  and `export PATH="$HOME/safebin"` before any other work.
- Safebin output: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python);
  znc OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1).
- Exact verification output:
  - `which python3` -> NOT FOUND (empty; prints nothing)
  - `which python` -> NOT FOUND (empty; prints nothing)
- Guard status: PASS. No forbidden interpreter in PATH.

## Scope

Independent verification of the three key claims in
docs/lab/rsi/runs/wave-20261001-2321pdt/LEARNER-MECH/LEARNER_MECH_ANALYSIS.md
against the frozen TNN-2 source (blob b226b223cb3ee0be742af673653fb8ea8605f281
from commit f4de7ff46). Verification lane only: no new experiments, no
Python, no patch proposed. Shell for git and file operations only; no
compilation or execution was needed, so znc was not invoked.
