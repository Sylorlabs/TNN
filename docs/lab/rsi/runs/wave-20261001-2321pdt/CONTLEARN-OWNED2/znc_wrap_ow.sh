#!/bin/sh
# znc_wrap_ow.sh -- K1b wrapper for CONTLEARN-OWNED2. Logs every znc
# invocation to znc_invocations_ow.log, then execs the pinned znc.
# The log must contain exactly 2 entries (the two pre-run builds, one per
# binary) before the runs, and gain 0 entries during the 6 runs.
LOG="/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2321pdt/CONTLEARN-OWNED2/znc_invocations_ow.log"
printf '%s\n' "znc $*" >> "$LOG"
exec /home/hatch/workspace/tnn-rsi/src/tools/toolchain/znc_linux_x86_64_abed8aa1 "$@"
