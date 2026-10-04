#!/bin/sh
# znc_wrap.sh -- K1b wrapper. Logs every znc invocation, then execs the real
# pinned znc binary. The log must contain exactly 2 entries (the two
# pre-run builds: ow_control and ow_treat) before the runs, and gain 0
# entries during the 6 runs.
LOG="/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN-OWNED/znc_invocations.log"
printf '%s\n' "znc $*" >> "$LOG"
exec /home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1 "$@"
