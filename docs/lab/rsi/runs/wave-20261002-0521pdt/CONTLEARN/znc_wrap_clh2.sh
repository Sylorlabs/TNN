#!/bin/sh
# znc_wrap_clh2.sh -- K1b wrapper for CLH2. Logs every znc invocation,
# then execs the pinned znc. The log must contain exactly 3 entries (the
# three pre-run builds, one per binary) before the runs, and gain 0
# entries during the 9 runs.
LOG="/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261002-0521pdt/CONTLEARN/znc_invocations_clh2.log"
printf '%s\n' "znc $*" >> "$LOG"
exec /home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1 "$@"
