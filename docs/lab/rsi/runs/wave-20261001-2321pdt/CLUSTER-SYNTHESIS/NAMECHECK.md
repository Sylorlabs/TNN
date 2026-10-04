# CLUSTER-SYNTHESIS NAMECHECK

Lane: CLUSTER-SYNTHESIS, wave wave-20261001-2321pdt.
Role: synthesis/documentation worker. No new experiments are run
in this lane; this lane only synthesizes the decided evidence from
BATTERY-CLUSTER analysis and the BATTERY-E1 through E6 verdicts.

## Step 0: Worker toolchain guard verification

- Executed: `cd ~/workspace/tnn-rsi && sh
  docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
- Setup output: `linked: 36 tools`, `znc: OK
  (/home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1)`,
  `verify: python3 absent from safebin PATH (OK)`,
  `verify: python absent from safebin PATH (OK)`,
  `SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)`
- After `export PATH="$HOME/safebin"`:
  - `which python3` printed NOTHING (exit code 1)
  - `which python` printed NOTHING (exit code 1)
  - `which znc` -> `/home/hatch/safebin/znc`
- Verdict: SAFEBIN ACTIVE, no forbidden interpreter in PATH.
  Pure Zag constraint honored from this point on.
- Forbidden-interpreter invocation policy: PROCESS-FAIL with
  disclosure and clean re-freeze if the result matters.

## Lane READ-ONLY constraints

Read-only toward: BATTERY, BATTERY-CLUSTER, and BATTERY-E1
through E6 lane dirs. Committed sources extracted with `git
show` only; nothing copied from lane dirs into this lane.
Never write outside
docs/lab/rsi/runs/wave-20261001-2321pdt/CLUSTER-SYNTHESIS/.
Never `git reset --hard`, never rebase, never push. All commits
use explicit pathspec under CLUSTER-SYNTHESIS/ only.

## Scope reminder

CLUSTER_SYNTHESIS.md and JUDGE_BRIEF.md only. This lane adds no
evidence; it cites verdicts and commit ids recorded by the
E-lanes. BATTERY-E8 is still running; recorded as PENDING.
