#!/bin/bash
# Build-only scaling probe: D in a geometric ladder, phase=2 (returns right
# after the after_build dump). Short watchdog limits, run strictly serially so
# the shared machine is not oversubscribed.
cd "$(dirname "$0")"
W=/Users/Shared/micah/Documents/TNN/TNN/tools/tnnwatch.sh
for d in 2000 4000 8000 12000 16000; do
  nohup "$W" reg "bs_$d" 300 ./e11_prof "$d" 0 2 0 >/dev/null 2>&1 </dev/null &
  disown 2>/dev/null
  # wait for the watchdog to finish this rung before launching the next
  while :; do
    sleep 5
    st=$(grep -o 'status=[A-Z]*' "/Users/Shared/micah/Documents/TNN/.runs/bs_$d.meta" 2>/dev/null | head -1)
    case "$st" in
      *RUNNING*) ;;
      *) break ;;
    esac
  done
  cp "/Users/Shared/micah/Documents/TNN/.runs/bs_$d.log" "out/bs_$d.log" 2>/dev/null
  printf 'rung %s done: %s\n' "$d" "$(grep -o 'status=[A-Z]*' "/Users/Shared/micah/Documents/TNN/.runs/bs_$d.meta" | head -1)"
done
exit 0