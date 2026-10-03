# NAMECHECK.md: DEVANG4 lane, wave-20261002-0221pdt

## Step 0: Worker toolchain guard (Micah governance, 2026-09-30; owner red line)

- Ran `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  at 2026-10-02 ~02:27 PDT from `~/workspace/tnn-rsi`.
- Setup output: `linked: 36 tools`, `znc: OK (.../znc_linux_x86_64_abed8aa1)`,
  `verify: python3 absent from safebin PATH (OK)`,
  `verify: python absent from safebin PATH (OK)`,
  `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`.
- Every shell in this lane uses `export PATH="$HOME/safebin"`.
- `which python3` returns nothing (empty output, confirmed post-setup).
- `which python` returns nothing.
- No `python3`/`python` resolution in PATH. Pure Zag only for all
  computational research operations in this lane.
- If a forbidden executable is invoked, this wave is automatically
  PROCESS-FAIL and will be disclosed immediately.

## Step 0b: Dash scan
- All loop docs in this lane will be scanned with
  `docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh`
  before commit. Zero em/en dashes.

## Step 0c: Toolchain near-miss disclosure (2026-10-02 ~02:55 PDT)

- During a prereg text fix, the worker typed `python3 -c "print('no')"`
  inside a compound shell command as a presence check. With
  PATH="$HOME/safebin", the name did NOT resolve (command not found;
  nothing executed). `command -v python3` returns empty, confirming
  absence. No forbidden executable was invoked and no Python ran; the
  wave is not PROCESS-FAIL. This is disclosed because the attempt
  itself was poor discipline: presence checks must use `command -v`
  (which cannot execute anything), never bare invocation. The worker
  will use `command -v` only, going forward.
