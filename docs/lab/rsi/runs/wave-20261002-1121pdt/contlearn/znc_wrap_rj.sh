#!/bin/sh
# znc_wrap_rj.sh -- K1b wrapper for the refusal exercise (a). Logs every
# znc invocation, then execs the pinned znc. The log must contain exactly
# the pre-run builds before the runs, and gain 0 entries during the runs.
LOG="/home/hatch/workspace/tnn-rsi-work/wave-20261002-1121pdt/contlearn/docs/lab/rsi/runs/wave-20261002-1121pdt/contlearn/znc_invocations_rj.log"
printf '%s\n' "znc $*" >> "$LOG"
exec /home/hatch/safebin/znc "$@"
