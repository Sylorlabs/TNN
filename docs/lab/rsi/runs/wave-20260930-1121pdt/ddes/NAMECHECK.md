# NAMECHECK: DDES worker, wave 20260930-1121pdt

Worker role: DDES (t*=0 soundness repair, wave 2).
Working directory: docs/lab/rsi/runs/wave-20260930-1121pdt/ddes/
Branch: tnn-native-lab. Commits local only, never push.

## Step 0: toolchain guard check (per AGENTS.md worker toolchain guard)

- `which python3` returns /usr/bin/python3 (present in PATH). The guard
  instruction (remove python from PATH where technically possible) was
  considered; python3 was NOT removed because /usr/bin also hosts the
  shell toolchain, but python3 is NEVER invoked by this worker at any
  stage. All research computation is pure Zag compiled and run via the
  shipped znc binary; all orchestration is shell (znc, binary runs,
  md5sum, diff, grep) and git. Zero Python invocations this wave.
- No new files outside the worker workdir are staged or committed.
- No em-dash or en-dash bytes in any committed file (checked with
  check_no_dash.sh before each docs commit).

## Scope

- Prereg PREREG_DDESREPAIR2.md: frozen, committed alone (d31e901b0).
- Implementation ddesr2.zag: new implementation by this worker from the
  BUILD-PASS source ddes.zag @ 56db8d606 plus the frozen repair spec
  (eff_waits clamp, t*=0 boundary flag, World F regression harness).
- This worker reports BUILD-PASS/BUILD-FAIL only, never SURVIVES.
