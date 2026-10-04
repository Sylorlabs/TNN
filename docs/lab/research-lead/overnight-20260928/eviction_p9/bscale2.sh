#!/bin/bash
# Ladder 2: LINEAR (mode bit2 clear) vs INDEXED (mode=4) t2_lu_first, same
# world, same phase. Strictly serial. Each rung 3/3 for byte-identity is done
# by zbuild-style repetition in the verify step, not here, to keep each
# watchdog slot short.
cd "$(dirname "$0")"
W=/Users/Shared/micah/Documents/TNN/TNN/tools/tnnwatch.sh
run() {
  local n="$1"; local secs="$2"; shift 2
  nohup "$W" reg "$n" "$secs" "$@" >/dev/null 2>&1 </dev/null &
  disown 2>/dev/null
  while :; do
    sleep 4
    local st
    st=$(grep -o 'status=[A-Z]*' "/Users/Shared/micah/Documents/TNN/.runs/$n.meta" 2>/dev/null | head -1)
    case "$st" in *RUNNING*) ;; *) break ;; esac
  done
  cp "/Users/Shared/micah/Documents/TNN/.runs/$n.log" "out/$n.log" 2>/dev/null
  printf '%-12s %s\n' "$n" "$(tr '\n' ' ' < "/Users/Shared/micah/Documents/TNN/.runs/$n.meta")"
}
# A. equivalence kill bar, small world
run eq300      300 ./e11_prof 300 4 8 0
# B. answers: linear vs indexed at D=1000, full 9-phase battery
run a_lin1000  400 ./e11_prof 1000 0 3 0
run a_idx1000  200 ./e11_prof 1000 4 3 0
# C. scale on the indexed path
run b_idx5000  300 ./e11_prof 5000 4 3 0
run b_idx10000 400 ./e11_prof 10000 4 3 0
run b_idx20000 600 ./e11_prof 20000 4 3 0
exit 0