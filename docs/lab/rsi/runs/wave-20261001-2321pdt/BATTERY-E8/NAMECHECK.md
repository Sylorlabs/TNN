# BATTERY-E8 NAMECHECK

Lane: BATTERY-E8 (wave wave-20261001-2321pdt), replacement worker executing Cluster 2 discriminator E8 (orthogonal-signal ACT bandwidth probe, tests H2d).

## Step 0: Worker toolchain guard verification

- Executed: `cd ~/workspace/tnn-rsi && sh docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
- Setup output: `linked: 36 tools`, `znc: OK (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)`, `verify: python3 absent from safebin PATH (OK)`, `verify: python absent from safebin PATH (OK)`, `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`
- After `export PATH="$HOME/safebin"`:
  - `which python3` printed NOTHING (exit code 1)
  - `which python` printed NOTHING (exit code 1)
  - `which znc` -> `/home/hatch/safebin/znc`
- Verdict: SAFEBIN ACTIVE, no forbidden interpreter in PATH. Pure Zag constraint honored from this point on.
- Forbidden-interpreter invocation policy: PROCESS-FAIL with disclosure and clean re-freeze if the result matters.

## Lane READ-ONLY constraints

Read-only toward: BATTERY, BATTERY-CLUSTER, BATTERY-E2, BATTERY-E6 lane dirs. Extract committed sources via `git show` from recorded commits only. Never write outside `docs/lab/rsi/runs/wave-20261001-2321pdt/BATTERY-E8/`. Never `git reset --hard`, never rebase, never push.

## Discriminator mapping

- E2 tested H2a/H2b at the guide-to-ACT interface: verdict E2-CONTENT-BLIND confirmed H2a (absent content channel), killed H2b.
- E6 tests H2c (guide-store lifecycle).
- E8 tests H2d (ACT output bandwidth).
