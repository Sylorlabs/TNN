#!/bin/bash
# Ladder 3: push past the arena so RECLAMATION actually runs. live nodes are
# ~7.07 per MAP, so NN=262144 is crossed at ~37000 MAPs. Serial, short limits.
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
# policy 1 = fast structural buckets (mode bit3). policy 0 = frozen scan.
run c_idx50k   600 ./e11_prof 50000 12 3 0
run c_idx100k  900 ./e11_prof 100000 12 3 0
# control at the same scale: policy 2 = LRU-by-oldest-id (mode bit5)
run c_lru50k   600 ./e11_prof 50000 36 3 0
exit 0