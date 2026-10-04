# NAMECHECK: ARENA-K5E (K5(e) generality probe, execution only)
Lane: ARENA-K5E, wave-20261001-2021pdt
Role: execute the frozen K5(e) generality probe for the TCNP BUILD-PASS verdict.
This worker is independent of the ARENA-IMPL builder and the ARENA-ADVERSARY
worker. No shared implementation source, no sealed world design was reused.

## Step 0: safebin activation (worker toolchain guard)

- Ran: bash docs/lab/research-lead/overnight-20260928/safebin_setup/setup_safebin.sh
- Exported: PATH="$HOME/safebin" (36 tools, pinned znc verified by setup)
- `which python3` prints NOTHING (exit 1). `which python` also prints nothing.
- Guard status: PASS. Pure Zag only for all computation in this lane.
- All shell commands in this lane run with PATH="$HOME/safebin".
- No forbidden executable was invoked at any point in this lane.
  Zero Python, zero other interpreters. Shell only sequenced the pinned znc,
  ran built binaries, git read ops, and file copies/moves.

## Step 1: frozen binary integrity (before any run)

- docs/lab/rsi/runs/wave-20261001-2021pdt/ARENA/bin/tcn_p
- sha256: 71ea78f717e5cf25146487b1da110b05173573af1924a00e726ade0579cdda2b
- Matches the committed SEALED_EVAL.md record and the builder/adversary/red-team
  records. (The task text carried a one hex digit transcription difference in
  this hash; the on-disk value matches every committed lane record.)

## Step 2: scope (from the assigned task)

- Design ONE fresh world (new rule, new seed, same pshow/ptest protocol),
  rule in the 8-op ISA, structurally different from worlds A-E,
  3 shown pairs, 6 hidden probes.
- Write the world file to ARENA/k5e/, record its sha256 in K5E_PROBE.md
  BEFORE running.
- Run the FROZEN bin/tcn_p binary ONCE on the world (no re-runs for tuning).
- Score the 6 hidden probes: >= 4/6 is K5(e) PASS, below 4/6 is FAIL.
- Report: world spec, pre-run hash, 6 probe results, K5(e) PASS/FAIL.
- Stop after the single probe run.
- No commits (coordinator commits). No push. No git reset, no rebase.
- Files written only inside
  docs/lab/rsi/runs/wave-20261001-2021pdt/ARENA/ as new files:
  NAMECHECK_K5E.md, K5E_PROBE.md, k5e/ (world files).
- Documentation rule: no em-dash bytes in lane docs.

## Independence notes

- The K5(e) world rule was chosen by this worker alone, after the sealed
  battery, and appears in no builder-visible or adversary-visible material.
- The reference check tool (gen_k5e / refcheck, pure Zag, pinned znc) is this
  worker's own design-time tooling, written from the frozen prereg's published
  8-op ISA and protocol only. It never runs the contestant binary.
- Scoring keys are computed by mechanical rule application, never by running
  the contestant.
