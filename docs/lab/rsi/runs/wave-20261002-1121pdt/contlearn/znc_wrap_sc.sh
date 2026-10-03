#!/bin/sh
# znc_wrap_sc.sh -- K1b wrapper for the scheduling exercise (b).
LOG="/home/hatch/workspace/tnn-rsi-work/wave-20261002-1121pdt/contlearn/docs/lab/rsi/runs/wave-20261002-1121pdt/contlearn/znc_invocations_sc.log"
printf '%s\n' "znc $*" >> "$LOG"
exec /home/hatch/safebin/znc "$@"
