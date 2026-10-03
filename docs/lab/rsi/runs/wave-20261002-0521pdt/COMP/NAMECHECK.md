# NAMECHECK: COMP lane, wave-20261002-0521pdt

Worker: COMP (composition A/B/C comparative adversarial), subagent 6d98415a.
Lane dir: docs/lab/rsi/runs/wave-20261002-0521pdt/COMP/
Working copy: ~/workspace/tnn-rsi, branch tnn-native-lab.
Parent wave context: prereg frozen 23dc15498 (0221pdt), amended pre-implementation
with Amendment A1 (uncommitted in 0221 dir); this wave re-freezes the amended
prereg ALONE in its own lane dir, then builds and runs the battery.

## Step 0: worker toolchain guard (2026-10-02, owner red line)

- Ran: `bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh`
  Result: SAFEBIN-READY: /home/hatch/safebin (36 tools, no python)
- Every shell in this lane: `export PATH="$HOME/safebin"` first.
- `which python3` -> nothing (exit 1). `which python` -> nothing (exit 1).
- `which znc` -> /home/hatch/safebin/znc (pinned toolchain OK).
- PURE ZAG ONLY for all research logic. No Python anywhere in this lane.
- Forbidden-executable invocation = automatic PROCESS-FAIL; none occurred.
- Zag compiler quirk (AGENTS.md): checked lane sources for `as *i32`
  slice construction inside functions; none found (u8-cell idiom used).
- Dash rule: loop docs use hyphens only; verified with
  docs/lab/research-lead/overnight-20260928/worker_snippets/check_no_dash.sh
  before each commit.

## Steps

- [x] Step 0: toolchain guard verified (above), 2026-10-02 ~05:30 PDT
- [x] Step 1: amended PREREG_COMP.md frozen ALONE at cc9acf48e
      (no implementation in that commit)
- [x] Step 2: implementation rebuild (pure Zag) in this lane dir only;
      3x byte-identical builds, sha256s in build_sha256.txt
- [x] Step 3: comparative eval, 3/3 byte-identical reruns (B/C/C0/D;
      A incomplete: D4 blowup)
- [x] Step 4: red-team self-review (REDTEAM_SELF.md)
- [x] Step 5: VERDICT line (BUILD-PASS + scoped findings, no SURVIVES)
- [ ] Step 6: commits local only, explicit pathspec, never push

## Commit log (this lane only)

- (pending) amended prereg freeze
- (pending) implementation + eval + redteam + verdict
