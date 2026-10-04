#!/bin/bash
# Ladder 5 -- POST-C551 (index scaffolding exempt from reclamation).
# K4 (charter 32, mission priority 1) runs FIRST because it is the item that
# was previously vacuous at zero evictions. 100k is omitted here: run e_100k in
# ladder 4 already covers it post-fix with the same binary line.
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
# K4 charter-32: RECENT JUNK vs OLD FOUNDATIONAL, with REAL reclamation.
#   mode 13 = both indices + fast structural policy
#   mode 45 = both indices + LRU-by-oldest-id CONTROL (must lose)
run k4_fast40k 600 ./e11_prof 0 13 4 40000
run k4_lru40k  600 ./e11_prof 0 45 4 40000
# regression: canonical levels must be untouched by C551
run f_1k    200 ./e11_prof 1000  13 3 0
run f_10k   250 ./e11_prof 10000 13 3 0
run f_20k   300 ./e11_prof 20000 13 3 0
# scale past the arena
run g_40k   400 ./e11_prof 40000 13 3 0
run g_50k   500 ./e11_prof 50000 13 3 0
# namespace battery re-run under the new layout
run h_nsbatt 300 ./e11_prof 0 13 5 0
exit 0