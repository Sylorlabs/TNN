# NAMECHECK S7-RT: step-7 V1-V4 independent red-team certification

Lane: HPIREV2-S7-RT
Worker: independent red-team certifier (depth-2 subagent)
Date: 2026-10-01

## Step 0: worker toolchain guard (independent activation)

This certifier is independent of the S7 worker, the S7-ADV worker, and all prior
HPIREV2 workers. Toolchain activation was performed fresh at session start:

- Ran: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
- Result: SAFEBIN-READY, /home/hatch/safebin (36 tools, no python)
- Ran: `which python3` under the safebin PATH; printed NOTHING (exit 1)
- Verified: `python3` absent from safebin PATH, `python` absent from safebin PATH
- `znc` check: OK (pinned toolchain binary present)

Guard check: PASS. No forbidden executable was invoked or will be invoked.
Mode: read-only static analysis of committed world files and the frozen prereg.
The mechanism will NOT be run on the sealed worlds (that is the implementation
worker's job).

## Branch and file discipline

- Working copy: /home/hatch/workspace/tnn-rsi, branch tnn-native-lab
- Writes limited to docs/lab/rsi/runs/wave-20261001-2021pdt/HPIREV2/
- New files only: NAMECHECK_S7_RT.md (this file), CERT_S7_V1V4.md
- No push, no git reset --hard, no rebase, no commits (coordinator commits)

## Documentation rule

No em-dashes used anywhere in this file or in the certification deliverable.
