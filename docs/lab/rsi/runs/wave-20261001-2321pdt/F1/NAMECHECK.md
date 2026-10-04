# NAMECHECK.md - wave-20261001-2321pdt lane F1 (generic executable semantics: interleaved-error trigger)

## Step 0: Worker toolchain guard (safebin activation)

- Ran: `cd ~/workspace/tnn-rsi && sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh && export PATH="$HOME/safebin"`
- Result: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
- znc: OK (src/tools/toolchain/znc_linux_x86_64_abed8aa1)
- Verification: `which python3` prints NOTHING (exit 1). `which python` prints nothing (exit 1). Exact verification output recorded below.
- PATH exported to $HOME/safebin at startup; all subsequent work runs through safebin.
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
which_exit=1
```
(`which python3` printed nothing; exit code 1 confirms absence.)

## Lineage

- Prior wave: wave-20261001-2021pdt lane F1, BUILD-FAIL.
- Primary killing bar: K-C0C on W1 (15/30 = 50% < 80%). Root cause: the
  K1=2 consecutive-failure trigger never fires on interleaved errors; the
  consecutive counter resets on every correct prediction.
- Secondary: K-C0C on W4 (isomorphism leg; adversary-designed near-variant,
  not a trigger defect; prereg prescribed adversary redesign, not builder patch).
- This wave addresses the trigger defect only, with a generic
  windowed failure-density trigger. No researcher-authored semantic cases
  added (SUB, DIV, PARITY, threshold COND, and equivalents remain forbidden).
