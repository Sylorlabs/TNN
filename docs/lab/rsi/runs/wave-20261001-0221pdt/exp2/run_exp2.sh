#!/bin/sh
# run_exp2.sh <world> <lawfile> <maxprobes> <workdir>
# H-EXP2 v2 orchestration loop (orchestration only; no decision logic).
# The learner (expseq) chooses; the world (expworld) executes.
# Appends every expseq round trace to rounds.log. Prints a DONE line.
set -u
world="$1"; law="$2"; maxp="$3"; wd="$4"
BINDIR=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$wd" || exit 1
cd "$wd" || exit 1
"$BINDIR/expworld_bin" "$law" state.txt > init.out 2> init.err || { echo "DONE expworld-init-fail"; exit 1; }
: > history.txt
: > rounds.log
cat init.out >> rounds.log
round=1
while true; do
  "$BINDIR/expseq_bin" history.txt state.txt > round.out 2> round.err
  rc=$?
  cat round.out >> rounds.log
  if grep -q '^IDENTIFIED ' round.out; then echo "DONE IDENTIFIED round=$round"; break; fi
  if grep -q '^STALLED' round.out; then echo "DONE STALLED round=$round"; break; fi
  if grep -q '^INCONSISTENT' round.out; then echo "DONE INCONSISTENT round=$round"; break; fi
  if [ "$rc" -ne 0 ]; then echo "DONE expseq-rc=$rc round=$round"; break; fi
  nprobe=$(wc -l < history.txt)
  if [ "$nprobe" -ge "$maxp" ]; then echo "BUDGET-EXHAUSTED" >> rounds.log; echo "DONE BUDGET-EXHAUSTED round=$round"; break; fi
  grep '^PROBE ' round.out | cut -d ' ' -f2- > probe.txt
  start=$(cat state.txt)
  "$BINDIR/expworld_bin" "$law" state.txt probe.txt > world.out 2> world.err || { echo "DONE expworld-fail round=$round"; break; }
  traj=$(grep '^OUT' world.out | cut -d ' ' -f2-)
  echo "H $start $(cat probe.txt) $traj" >> history.txt
  round=$((round + 1))
done
exit 0
