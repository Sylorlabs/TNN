#!/bin/sh
# znc_wrap_pf.sh -- K1b wrapper for CONTLEARN3. Logs every znc invocation,
# then execs the pinned znc. The log must contain exactly 2 entries (the
# two pre-run builds, one per binary) before the runs, and gain 0 entries
# during the 6 runs.
LOG="/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261002-0221pdt/CONTLEARN/znc_invocations_pf.log"
printf '%s\n' "znc $*" >> "$LOG"
exec /home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1 "$@"
