# NAMECHECK.md - wave-20261001-2321pdt lane F1-FOLLOWUP (replacement worker)

## Step 0: Worker toolchain guard (safebin activation)

- Ran: `cd ~/workspace/tnn-rsi && sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh && export PATH="$HOME/safebin"`
- Result: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
- znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
- Verification: `which python3` prints NOTHING (exit 1). `which python` prints nothing (exit 1).
- PATH exported to $HOME/safebin; every subsequent exec call in this lane re-exports it.
- Commitment: pure Zag only. No Python for glue, analysis, verifiers, harnesses, fixture provisioning, or scratch. Shell invokes only pinned znc, compiled binaries, git ops, cmp/sha256sum, grep for audits, file moves/copies.
- Any forbidden executable invocation = automatic PROCESS-FAIL, to be reported honestly. None occurred.

Exact Step 0 verification output:
```
safebin: /home/hatch/safebin
linked: 36 tools
znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)
verify: python3 absent from safebin PATH (OK)
verify: python absent from safebin PATH (OK)
SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
PATH=/home/hatch/safebin
--- which python3:
exit=1
```
(`which python3` printed nothing; exit code 1 confirms absence.)

## Lineage

- Parent lane: wave-20261001-2321pdt lane F1, BUILD-FAIL (self-owned bar-calibration mistake: K-C0C-REG used an unvalidated fresh seed for R-W2, conflating trigger regression with constructor seed-robustness).
- This lane is a narrowed follow-up with two fresh preregs: Part 1 (trigger re-test with the corrected bar on prior-wave validated W2 fixtures) and Part 2 (constructor seed-sensitivity characterization). No new trigger design, no implementation changes. READ-ONLY toward the F1 lane dir.
- Frozen artifacts reused read-only: new binary F1 impl/f1_learn (sha256 6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847), old binary wave-20261001-2021pdt F1 dev/bin/f1_learn (sha256 0c571abca5a3c16695115228114c327bb3370081304c9c3a1ea1354840aa2727).
