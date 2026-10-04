#!/bin/bash
# SCALING-EVICT continuation runner. One rung, detached, bounded.
# setsid does not exist on this host, so the watchdog is launched under
# nohup+disown and the polling happens in a SEPARATE loop that survives the
# orchestrating shell. Never call `$W reg` in the foreground.
# Usage: ./run1.sh <name> <secs> <cmd...>
cd "$(dirname "$0")"
W=/Users/Shared/micah/Documents/TNN/TNN/tools/tnnwatch.sh
n="$1"; s="$2"; shift 2
nohup "$W" reg "$n" "$s" "$@" >/dev/null 2>&1 </dev/null &
disown 2>/dev/null
i=0
while [ $i -lt 400 ]; do
  sleep 3
  st=$(grep -o 'status=[A-Z]*' "/Users/Shared/micah/Documents/TNN/.runs/$n.meta" 2>/dev/null | head -1)
  if [ -z "$st" ]; then i=$((i+1)); continue; fi
  case "$st" in
    *RUNNING*) ;;
    *) break ;;
  esac
  i=$((i+1))
done
mkdir -p out
cp "/Users/Shared/micah/Documents/TNN/.runs/$n.log" "out/$n.log" 2>/dev/null
printf '=== %s %s bytes=%s ===\n' "$n" "$(tr '\n' ' ' < "/Users/Shared/micah/Documents/TNN/.runs/$n.meta" 2>/dev/null)" "$(wc -c < "out/$n.log" 2>/dev/null | tr -d ' ')"
exit 0
