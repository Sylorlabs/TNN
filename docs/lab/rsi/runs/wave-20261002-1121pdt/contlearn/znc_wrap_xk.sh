#!/bin/sh
# znc_wrap_xk.sh -- K1b wrapper for the cross-kind rebind (c).
LOG="/home/hatch/workspace/tnn-rsi-work/wave-20261002-1121pdt/contlearn/docs/lab/rsi/runs/wave-20261002-1121pdt/contlearn/znc_invocations_xk.log"
printf '%s\n' "znc $*" >> "$LOG"
exec /home/hatch/safebin/znc "$@"
