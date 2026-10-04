#!/bin/bash
# Detached watchdog launcher.
# NOTE: setsid is NOT available on this darwin/arm64 host (command -v -> rc=1),
# so the watchdog's own reg falls back to a plain background child. The watchdog
# parent must therefore survive the orchestrating shell call, hence nohup+disown
# and an immediate return. Never call `$W reg` in the foreground: the shell
# tool's 120s kill would take the watchdog's poll loop with it and leave the
# experiment running with NO timeout enforcement.
# Usage: ./wrun.sh <name> <secs> <cmd...>
W=/Users/Shared/micah/Documents/TNN/TNN/tools/tnnwatch.sh
n="$1"; s="$2"; shift 2
nohup "$W" reg "$n" "$s" "$@" >/dev/null 2>&1 </dev/null &
disown 2>/dev/null
sleep 2
printf 'launched %s limit=%s meta=%s\n' "$n" "$s" "$(cat "/Users/Shared/micah/Documents/TNN/.runs/$n.meta" | tr '\n' ' ')"
exit 0