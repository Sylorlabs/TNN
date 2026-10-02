# NAMECHECK: wave-20261002-0521pdt coordinator

## Step 0: toolchain guard (coordinator)

- 2026-10-02 05:22 PDT: ran
  docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh;
  exported PATH="$HOME/safebin".
- `which python3` returns nothing under safebin PATH (only znc and the 36
  allowed tools resolve).
- PURE ZAG ONLY mandated for this wave and every child worker. Any
  forbidden-executable invocation is PROCESS-FAIL for that worker's current
  scientific wave and must be cleanly re-frozen if its result matters.
- Every child worker must record its own Step 0 in its lane NAMECHECK.md.
- Git discipline: pathspec-only commits (no git add -A, no stash, no reset,
  no clean). Workers re-briefed (process blemish carried from 0221pdt).

## Wave metadata

- Wave id: wave-20261002-0521pdt. Started 2026-10-02 05:22 PDT.
- Branch: tnn-native-lab. Working copy: ~/workspace/tnn-rsi.
- Pre-wave tip: db3cc7086. All commits LOCAL ONLY, never pushed.
- Lock: ~/workspace/tnn-rsi/.wave_lock (written by parent run).

## Standing rule reminders issued to children

- Prereg commit-order self-check before any verdict: prereg first commit
  must strictly precede implementation first commits; UNVERIFIABLE ORDERING
  cannot be adopted.
- Kill bars frozen before implementation, never moved after.
- Documentation: zero em-dashes (check with check_no_dash.sh).
- No-patch-treadmill: cluster fresh-world failures by shared architectural
  cause; no benchmark-specific handlers/opcodes; new modes/bridges/routers
  presumptively rejected.
- Provenance honesty: no recycled renders presented as fresh; blind A/B
  pairs for judge-ready image candidates; Micah is sole image judge.
- Escalation only for: protected-core boundary changes, irreversible
  architecture commitments, experimentally indiscriminable choices,
  governance decisions. Ordinary continuation does not require permission.
