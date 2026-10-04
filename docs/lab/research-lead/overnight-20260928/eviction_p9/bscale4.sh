#!/bin/bash
# Ladder 4 -- BOTH learner indices live, reclamation actually exercised.
#   idx_mode = mode&7.  bit0 (1) = MAP plen-bucket index + indexed rebind.
#                          bit2 (4) = FACT subject index (t2_lu_first).
#   mode bit3 (8)  -> eviction policy 1, fast structural buckets.
#   mode bit5 (32) -> eviction policy 2, LRU-by-oldest-id CONTROL.
# mode=13 is therefore "both indices + fast structural eviction".
# Serial, preregistered limits, no extension after a miss.
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
  printf '%-14s %s\n' "$n" "$(tr '\n' ' ' < "/Users/Shared/micah/Documents/TNN/.runs/$n.meta")"
}
# A. answers + scan counter with BOTH indices, no eviction yet
run d_1k    200 ./e11_prof 1000  13 3 0
run d_5k    200 ./e11_prof 5000  13 3 0
run d_10k   250 ./e11_prof 10000 13 3 0
run d_20k   300 ./e11_prof 20000 13 3 0
# B. past the arena: reclamation runs
run e_40k   400 ./e11_prof 40000 13 3 0
run e_50k   500 ./e11_prof 50000 13 3 0
run e_100k  800 ./e11_prof 100000 13 3 0
exit 0