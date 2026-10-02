# NAMECHECK.md - wave-20261001-2021pdt / F2v3 research worker

## Step 0: Toolchain guard (mandatory, before any other work)

Date: 2026-10-01 20:26 PDT (Thu)
Worker: research worker (depth 2/2), lane F2v3 (F2 v3 with X-rule distinguishability)

Actions taken:
1. Ran `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
   - Result: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
   - znc pinned toolchain present: /home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1
   - Safebin verify reported: python3 absent from safebin PATH (OK), python absent (OK)
2. Exported PATH="$HOME/safebin" (safebin only, no other entries)
3. `which python3` -> nothing found (OK)
4. `which python` -> nothing found (OK)

Toolchain status: PURE-ZAG PATH active. python3 and python do not resolve.
No forbidden executable has been invoked. This record satisfies Step 0.

Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab.
Write scope for this phase: docs/lab/rsi/runs/wave-20261001-2021pdt/F2v3/ only.
No implementation files will be written before coordinator authorization
(UNVERIFIABLE ORDERING voids the prereg). No commits by this worker.
