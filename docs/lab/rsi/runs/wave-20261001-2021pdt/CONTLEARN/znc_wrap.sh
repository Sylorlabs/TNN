#!/bin/sh
# znc_wrap.sh -- K1b wrapper. Logs every znc invocation, then execs the real
# pinned znc binary. The log must contain exactly 1 entry (the pre-run build)
# before the runs, and gain 0 entries during the 7 runs.
LOG="/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2021pdt/CONTLEARN/znc_invocations.log"
printf '%s\n' "znc $*" >> "$LOG"
exec /home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1 "$@"
