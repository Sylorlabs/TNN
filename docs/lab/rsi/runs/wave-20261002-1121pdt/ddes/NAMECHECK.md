# NAMECHECK.md - lane DDES, wave-20261002-1121pdt

Lane branch: lane-ddes-20261002-1121pdt. Task queue item 5: DDES steps 10 (independent red team on t*=0 repair), 11 (governance audit of the 11-step pipeline), plus an adversary OOD probe on the t*=0 repair.

## Step 0: toolchain guard (recorded first)

Setup command: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
Setup output verbatim: "safebin: /home/hatch/safebin / linked: 36 tools / znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1) / verify: python3 absent from safebin PATH (OK) / verify: python absent from safebin PATH (OK) / SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)"

With PATH=/home/hatch/safebin exported:
- `which python3` -> NOTHING (resolves to nothing, required)
- `which python` -> NOTHING
- `which znc` -> /home/hatch/safebin/znc (safebin path, required)

Guard: PASS. All research logic this wave is pure Zag; shell is used only to invoke znc, run binaries, git ops, and file moves.
