# NAMECHECK: wave-20261001-0521pdt fork_battery lane

Lane worker: fork testing (standing FORK TESTING rule).
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab (local only, no push).

## Step 0: Worker toolchain guard (Micah governance ruling 2026-09-30)

- Safebin setup script found at
  docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
  (path relative to ~/workspace/tnn-rsi). Ran 2026-10-01 ~05:27 PDT.
- Setup result: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python);
  znc OK at src/tools/toolchain/znc_linux_x86_64_abed8aa1 (relative to
  ~/workspace/tnn-rsi).
- PATH exported to $HOME/safebin for all subsequent shell work this session.
- Verification (mandatory): `which python3` returns nothing; `which python`
  returns nothing. Both confirmed absent after export.
- Guard status: PASS. No forbidden executable invoked; no PROCESS-FAIL.
- This lane uses only: safebin shell tools (grep, sort, wc, awk-free), znc,
  and compiled binaries. No Python in verifiers, scorers, harnesses,
  analysis, or scratch.

## Subsequent steps

- Step 1: Enumerate every branch and fork (local and remote) in the working
  copy: git branch -a, git for-each-ref, stash entries.
- Step 2: PRE-RUN GATE: assert entry labels unique before any battery run.
- Step 3: Run frozen test battery per entry (reuse frozen driver from latest
  prior fork_battery lane; no new battery, no moved bars).
- Step 4: Report per entry; update fork_battery/MANIFEST.md.
