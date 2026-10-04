#!/bin/bash
# SCALING-MISSPATH run launcher. Detached, watchdog-enforced, never foreground.
#
# WHY DETACHED: setsid is NOT available on this darwin/arm64 host, so $W reg
# falls back to a plain background child and the watchdog's own poll loop is a
# child of THIS shell. A foreground $W reg would therefore lose its timeout the
# moment the caller's 120s limit fires, leaving the experiment running with NO
# timeout enforcement -- the exact wave-2 failure. So: always nohup+disown and
# return immediately, then poll the .meta file.
#
# Usage: ./wrun.sh <name> <secs> <cmd...>
W=/Users/Shared/micah/Documents/TNN/TNN/tools/tnnwatch.sh
n="$1"; s="$2"; shift 2
nohup "$W" reg "$n" "$s" "$@" >/dev/null 2>&1 </dev/null &
disown 2>/dev/null
sleep 1
printf 'launched %s limit=%s meta=%s\n' "$n" "$s" "$(tr '\n' ' ' < "/Users/Shared/micah/Documents/TNN/.runs/$n.meta" 2>/dev/null)"
exit 0
