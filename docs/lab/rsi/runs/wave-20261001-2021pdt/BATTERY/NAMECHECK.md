# NAMECHECK.md BATTERY lane wave-20261001-2021pdt

## Step 0: Worker toolchain guard (mandatory, recorded before any other work)

- Ran: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh` from /home/hatch/workspace/tnn-rsi; result SAFEBIN-READY: /home/hatch/safebin (36 tools, no python).
- Exported PATH="$HOME/safebin" for all subsequent work in this session.
- Ran `which python3` under the safebin PATH: prints NOTHING (exit 1). `which python` likewise absent. Setup script self-verify also reported python3 absent from safebin PATH (OK).
- Toolchain commitment: PURE ZAG ONLY for all research logic. This task is WRITING ONLY (prereg document plus this NAMECHECK), so no computation is performed and no executables beyond the verification above are invoked. Any computational step later will use only the pinned znc at /home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1 invoked through the safebin PATH; shell tools limited to coreutils/git/file ops. Any accidental forbidden executable invocation in this worker's wave is automatic PROCESS-FAIL, reported honestly.
- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab (verified via git rev-parse). NEVER push. No git reset --hard, no rebase, no commits by this worker. Writes confined to docs/lab/rsi/runs/wave-20261001-2021pdt/BATTERY/.
- Documentation rule: no em-dashes in any written file (verified by grep before report).

## Step 0b: BATTERY-IMPL worker toolchain guard (implementation phase)

- Re-ran: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`; result SAFEBIN-READY (36 tools, no python).
- Exported PATH="$HOME/safebin" for this worker session.
- Ran `which python3` under the safebin PATH: prints NOTHING (exit 1). `which python` likewise absent. znc resolves to /home/hatch/safebin/znc (znc 2026.07.0-dev (edition 2026), pinned binary at /home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1).
- Toolchain commitment: PURE ZAG ONLY. World generator, envelopes, and scorer are all Zag; shell only invokes pinned znc, runs binaries, git ops, file moves/copies. Any forbidden executable invocation is automatic PROCESS-FAIL; reported honestly.
- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab (verified via git rev-parse). NEVER push. Never git reset --hard, never rebase. Do NOT git commit; coordinator commits. Write ONLY inside docs/lab/rsi/runs/wave-20261001-2021pdt/BATTERY/.
- Documentation rule: no em-dashes anywhere in written files. Determinism: 3/3 byte-identical reruns.
- Prereg ordering verified: implementation files are written only into the working tree after prereg commit d43fe32c5 (git log shows d43fe32c5 as HEAD and its tree does not contain implementation files); commit-order self-check passes.
