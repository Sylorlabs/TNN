# NAMECHECK.md wave-20261001-1721pdt GOV lane

## Step 0: Worker Toolchain Guard (mandatory, before any other work)

- Executed: docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
- Result: SAFEBIN-READY, 36 tools linked, znc OK (src/tools/toolchain/znc_linux_x86_64_abed8aa1)
- `which python3` -> no output, exit 1 (absent). `which python` -> no output, exit 1 (absent).
- PATH restricted to $HOME/safebin for all subsequent work in this lane.
- Guard status: PASS. No forbidden executable invocations.

Note: the pinned znc from 2026-09-30 has the known `as *i32` + `q[0..n]` slice miscompile issue. This lane runs no new Zag builds (investigation + fork battery only), so the workaround is noted for any verification builds if needed.
