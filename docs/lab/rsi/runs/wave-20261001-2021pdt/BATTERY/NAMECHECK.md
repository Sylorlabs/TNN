# NAMECHECK.md BATTERY lane wave-20261001-2021pdt

## Step 0: Worker toolchain guard (mandatory, recorded before any other work)

- Ran: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh` from /home/hatch/workspace/tnn-rsi; result SAFEBIN-READY: /home/hatch/safebin (36 tools, no python).
- Exported PATH="$HOME/safebin" for all subsequent work in this session.
- Ran `which python3` under the safebin PATH: prints NOTHING (exit 1). `which python` likewise absent. Setup script self-verify also reported python3 absent from safebin PATH (OK).
- Toolchain commitment: PURE ZAG ONLY for all research logic. This task is WRITING ONLY (prereg document plus this NAMECHECK), so no computation is performed and no executables beyond the verification above are invoked. Any computational step later will use only the pinned znc at /home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1 invoked through the safebin PATH; shell tools limited to coreutils/git/file ops. Any accidental forbidden executable invocation in this worker's wave is automatic PROCESS-FAIL, reported honestly.
- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab (verified via git rev-parse). NEVER push. No git reset --hard, no rebase, no commits by this worker. Writes confined to docs/lab/rsi/runs/wave-20261001-2021pdt/BATTERY/.
- Documentation rule: no em-dashes in any written file (verified by grep before report).
