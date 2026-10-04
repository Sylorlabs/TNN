# NAMECHECK.md: lane BATTERY, wave wave-20261002-0221pdt

## Step 0: toolchain guard verification (worker startup)

- Ran: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
- Output: `linked: 36 tools`, `znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)`, `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`
- `which python3` in safebin PATH: NOT FOUND. `which python`: NOT FOUND.
- Every shell command in this lane uses `export PATH="$HOME/safebin"` first.
- No Python, C/C++, JavaScript, or Rust anywhere in this lane. Pure Zag + shell.
- Dash scans: `docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh` on all lane docs before commit.

## Steps

- Step 1: read triviality review (wave-20261001-1721pdt/TRIVIALITY), extract 6 corrections.
- Step 2: freeze PREREG_BATTERY_E9.md ALONE (no implementation in that commit).
- Step 3: build battery in pure Zag; verify frozen pins (znc 498abcb5..., tnn2.zag a29972ca...).
- Step 4: run sealed; record SEALED_RESULTS.md.
- Step 5: battery self red team (BATTERY_REDTEAM.md); dash scan; commit lane dir with explicit pathspec.
