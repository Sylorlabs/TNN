#!/bin/sh
# run_hexp.sh -- H-EXP evidence runs (wave-20260929-0821pdt).
# Evidence only: builds exp_learn.zag with the pinned znc and runs the
# seven preregistered executions, saving stdout/stderr/exit per run.
# No verdict logic lives here; verdicts are in redteam/REDTEAM_H_EXP.md.
# Pure shell + git + sha256sum + pinned znc. Zero Python.
set -u
R="$HOME/workspace/tnn-rsi"
W="$R/docs/lab/rsi/runs/wave-20260929-0821pdt"
ZNC="$R/src/tools/toolchain/znc_linux_x86_64_abed8aa1"
B="$W/evidence/build_host"
mkdir -p "$B"
cp "$W/impl/exp_learn.zag" "$B/"
cp "$W/prereg"/hyp_p*.txt "$B/"
cp "$ZNC" "$B/znc"
chmod +x "$B/znc"
cd "$B" || exit 1
./znc exp_learn.zag -o exp_learn > build.log 2>&1
echo "build exit: $?"
sha256sum exp_learn exp_learn.zag | tee binary.sha
run() { # run <name> <hyp1> <hyp2>
  ./exp_learn "$2" "$3" > "$1.out" 2> "$1.err"
  echo "$? $(wc -c < "$1.out") $(wc -c < "$1.err")" > "$1.status"
}
run p1_r1 hyp_p1_a.txt hyp_p1_b.txt
run p1_r2 hyp_p1_a.txt hyp_p1_b.txt
run p2_r1 hyp_p2_a.txt hyp_p2_b.txt
run p3_r1 hyp_p3_a.txt hyp_p3_b.txt
run p3_r2 hyp_p3_a.txt hyp_p3_b.txt
cp hyp_p1_a.txt renamed_x.txt; cp hyp_p1_b.txt renamed_y.txt
run p1_ren renamed_x.txt renamed_y.txt
cmp p1_r1.out p1_r2.out && echo P1_IDENTICAL
cmp p3_r1.out p3_r2.out && echo P3_IDENTICAL
cp "$B"/*.out "$B"/*.err "$B"/*.status "$B"/binary.sha "$B"/build.log "$W/evidence/"
echo "evidence saved to $W/evidence/"
