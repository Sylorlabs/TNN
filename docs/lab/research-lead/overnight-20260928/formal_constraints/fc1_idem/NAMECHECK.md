# NAMECHECK.md, FC-1 (formal_constraints/fc1_idem)

Worker: FORMAL-CONSTRAINTS worker, session 0582e43a-47d5-439c-80a6-7e31e46ce17b.
Lane: docs/lab/research-lead/overnight-20260928/formal_constraints/fc1_idem/
Repo: ~/workspace/tnn-rsi, branch lane-gensubsumesu-20261003.
Commits local only, never pushed. Explicit pathspecs only.

## Step 0: toolchain guard (mandatory, recorded 2026-10-03)

Commands run at session start:

    bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
    export PATH="$HOME/safebin"

Guard evidence (recorded verbatim):

- `which python3` -> (empty, no output)
- `which python` -> (empty, no output)
- `which znc` -> /home/hatch/safebin/znc
- setup script verify lines: "verify: python3 absent from safebin PATH (OK)",
  "verify: python absent from safebin PATH (OK)",
  "SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)"

Guard: PASS. No forbidden interpreter exists in the worker PATH.
All FC-1 work (editing, building, running, verifying) uses only
safebin tools and the pinned znc. Any invocation of a forbidden
executable would make this wave PROCESS-FAIL; none occurred.

## Standing rules for this lane

- Pure Zag only. No Python anywhere, for any purpose.
- Prereg commit-order self-check: PREREG.md's first commit must
  strictly precede the implementation's first commit.
- Frozen kill bars (K-FC-1..K-FC-6) are named verbatim in the
  verdict; no weakening after results.
- No em dashes in loop documentation or source comments.
- Never commit binaries. Never push. Explicit pathspecs only.
- Prior lane result noted: 2026-10-02 formal_constraints worker,
  verdict FORMAL-CONSTRAINTS-COMPLETE (parent directory
  REPORT.md). FC-1 is a distinct experiment; its files live in
  fc1_idem/ and do not modify the prior worker's files.
