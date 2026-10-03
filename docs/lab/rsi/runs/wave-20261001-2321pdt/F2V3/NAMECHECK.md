# NAMECHECK.md - wave-20261001-2321pdt / F2V3 research worker

## Step 0: Toolchain guard (mandatory, before any other work)

Date: 2026-10-01 23:25 PDT (Thu)
Worker: research worker (depth 2/2), lane F2V3 (F2 v4 depth-9 candidate)

Actions taken:
1. Ran `docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
   from ~/workspace/tnn-rsi. Exact output:
   ```
   safebin: /home/hatch/safebin
   linked: 36 tools
   znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
   verify: python3 absent from safebin PATH (OK)
   verify: python absent from safebin PATH (OK)
   SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
   ```
2. Exported PATH="$HOME/safebin" (safebin only, no other entries)
3. `which python3` -> nothing found (exit 1) (OK)
4. `which python` -> nothing found (exit 1) (OK)
5. `git branch --show-current` -> tnn-native-lab

Toolchain status: PURE-ZAG PATH active. python3 and python do not resolve.
No forbidden executable has been invoked. This record satisfies Step 0.

Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab.
Write scope: docs/lab/rsi/runs/wave-20261001-2321pdt/F2V3/ only.
No implementation files will be written before the prereg commit
(UNVERIFIABLE ORDERING voids the prereg). No pushes, ever.
