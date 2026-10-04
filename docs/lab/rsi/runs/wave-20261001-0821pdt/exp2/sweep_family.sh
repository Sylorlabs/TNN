#!/bin/sh
# sweep_family.sh <lawdir> <maxprobes> <outdir>
# AH7 diagnostic: run the FROZEN expseq_bin (wave-20261001-0221pdt) against
# 16 fresh law files (all (A,B) pairs, authored by this adversary worker,
# not the sealed 1121pdt laws). Reports probes-to-IDENTIFIED per law.
# Deterministic. Diagnostic only; not a kill-bar run.
set -u
lawdir="$1"; maxp="$2"; outdir="$3"
BINDIR=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$outdir" || exit 1
: > "$outdir/sweep.tsv"
for A in 0 1 2 3; do
  for B in 0 1 2 3; do
    law="$lawdir/law_${A}_${B}.txt"
    wd="$outdir/w_${A}_${B}"
    mkdir -p "$wd" || exit 1
    ( cd "$wd" || exit 1
      "$BINDIR/expworld_bin" "$law" state.txt > init.out 2> init.err || { echo "world-init-fail"; exit 1; }
      : > history.txt
      : > rounds.log
      cat init.out >> rounds.log
      round=1
      while true; do
        "$BINDIR/expseq_bin" history.txt state.txt > round.out 2> round.err
        rc=$?
        cat round.out >> rounds.log
        if grep -q '^IDENTIFIED ' round.out; then echo "IDENTIFIED round=$round $(grep '^IDENTIFIED' round.out)"; break; fi
        if grep -q '^STALLED' round.out; then echo "STALLED round=$round"; break; fi
        if grep -q '^INCONSISTENT' round.out; then echo "INCONSISTENT round=$round"; break; fi
        if [ "$rc" -ne 0 ]; then echo "rc=$rc round=$round"; break; fi
        nprobe=$(wc -l < history.txt)
        if [ "$nprobe" -ge "$maxp" ]; then echo "BUDGET-EXHAUSTED round=$round"; break; fi
        grep '^PROBE ' round.out | cut -d ' ' -f2- > probe.txt
        start=$(cat state.txt)
        "$BINDIR/expworld_bin" "$law" state.txt probe.txt > world.out 2> world.err || { echo "world-fail round=$round"; break; }
        traj=$(grep '^OUT' world.out | cut -d ' ' -f2-)
        echo "H $start $(cat probe.txt) $traj" >> history.txt
        round=$((round + 1))
      done
    ) > "$wd.done" 2>&1
    echo "${A} ${B} $(cat $wd.done)" >> "$outdir/sweep.tsv"
  done
done
cat "$outdir/sweep.tsv"
exit 0
