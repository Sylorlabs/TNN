# NAMECHECK: EXP2 worker, wave-20260930-1121pdt

Step 0 toolchain verification (per 2026-09-30 worker toolchain guard).

- `which python3` returns /usr/bin/python3 (present on the system image).
  Full removal from PATH is not technically possible here: /usr/bin also
  holds sh, git, grep, cmp, all required for orchestration. Documented
  per the guard's "or document why" clause.
- Commitment: no python3/python invocation for any purpose in this wave.
  All computation is pure Zag compiled with znc; shell is used only to
  invoke znc, run binaries, do git ops, and move/copy files.
- Verified: this NAMECHECK file and all wave docs pass check_no_dash.sh.
- znc binary: docs/lab/rsi/runs/wave-20260929-0821pdt/evidence/build_host/znc
  (pinned Linux build, used for all compiles in this wave).
