# NAMECHECK.md - wave-20261001-2021pdt lane F1 (generic executable semantics frontier)

## Step 0: Worker toolchain guard (safebin activation)

- Ran: bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
- Result: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
- znc: OK (src/tools/toolchain/znc_linux_x86_64_abed8aa1)
- Verification: `which python3` returns NOTHING (exit 1); `which python` returns nothing.
- PATH exported to $HOME/safebin at startup; all subsequent work runs through safebin.
- Commitment: pure Zag only. No Python for glue, analysis, verifiers, harnesses, or fixture provisioning. Shell invokes only pinned znc, compiled binaries, git ops, file moves/copies.
- Any forbidden executable invocation = automatic PROCESS-FAIL, to be reported honestly.

## Step 0b: Worker toolchain guard (implementation turn, 2026-10-01 20:34 PDT)

- Re-ran safebin setup at task start: SAFEBIN-READY, 36 tools, znc OK.
- `which python3` prints NOTHING (exit 1). `which python` prints nothing.
- PATH=$HOME/safebin for this turn. Pure Zag only; shell invokes pinned znc,
  runs binaries, git ops, cmp/sha256sum, grep for audits, file moves/copies.
- Any forbidden executable invocation = automatic PROCESS-FAIL (none occurred).
