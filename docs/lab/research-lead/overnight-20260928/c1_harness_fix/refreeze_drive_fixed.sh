#!/bin/bash
# refreeze_drive_fixed.sh - clean re-freeze: all 60 Zag-driver runs.
# FIX (c1_harness_fix): rm -rf "$d" before mkdir ensures no stale state
# survives a resume after interruption. Without this, the Zag driver
# (which does mkdir but never clears state/) re-ingests all turns on
# top of partial state, doubling every weight and flipping abstention
# decisions. See FLAKINESS_REPORT.md (commit e98a976a0) for root cause.
# Shell only invokes the compiled pure-Zag driver binary (orchestration).
# Zero Python. PATH is restricted to the safe bin by the caller.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
D="$(cd "$HERE/.." && pwd)"
DRIVER="$D/c1_zagdriver/zag_driver_bin"
WORLDS="$D/c1_clean/worlds"
C1BIN="$D/c1_clean/contestant_bin"
BASE="$D/c1_baseline"
OUT="$HERE/runs"

run_one() {
  local name=$1 bin=$2 world=$3 rep=$4
  local d="$OUT/${name}_${world}_r${rep}"
  if [ -f "$d/costs.txt" ]; then
    echo "skip $name $world r$rep (already done)"
    return 0
  fi
  # FIX: clear any partial state from an interrupted prior run.
  # The Zag driver never clears state/ itself; without this, resume
  # re-ingests turns on stale state and doubles all weights.
  rm -rf "$d"
  mkdir -p "$d"
  "$DRIVER" "$WORLDS/$world" "$bin" "$d" > "$d/driver.log" 2>&1
  echo "done $name $world r$rep: $(grep 'queries=' "$d/costs.txt" | head -1)"
}

export -f run_one
export HERE D DRIVER WORLDS C1BIN BASE OUT

JOBS=""
for w in w0 w1 w2 h0 h1; do
  for r in 1 2 3; do
    JOBS="$JOBS c1:$C1BIN:$w:$r mem:$BASE/mem_bin:$w:$r freq:$BASE/freq_bin:$w:$r rand:$BASE/rand_bin:$w:$r"
  done
done

echo "$JOBS" | tr ' ' '\n' | grep -v '^$' | xargs -P 4 -I {} bash -c '
  IFS=":" read -r name bin world rep <<< "{}"
  run_one "$name" "$bin" "$world" "$rep"
'
echo ALL-DONE
