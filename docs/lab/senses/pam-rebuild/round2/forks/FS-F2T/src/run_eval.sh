#!/bin/bash
# run_eval.sh -- FS-F2T evaluation driver (glue only; all decisions in Zag).
# Runs the f2t_form binary in batch mode over:
#   1. the fresh timbredisc gating draw (1000)
#   2. the three unchanged-task regression batteries (FS-E2 lists)
# and scores each against .truth sidecars. Run number is $1 (1 or 2).
# Outputs: evidence/eval/run$1_*.log (raw stdout), evidence/eval/run$1_*.tsv
set -e
RUN="$1"
FORKDIR="$(dirname "$(dirname "$(readlink -f "$0")")")"
cd "$FORKDIR"
BIN="src/f2t_form"
EV="evidence/eval"

run_one() {
    local name="$1"; local list="$2"
    python3 src/run_phase0.py "$BIN" "$list" "$EV/run${RUN}_${name}.tsv" \
        > "$EV/run${RUN}_${name}.log" 2>&1
}

run_one fresh_timbredisc "$EV/fresh_timbredisc.list"
run_one reg_colordisc   "../FS-E2/evidence/phase0/lists/r2n_colordisc.list"
run_one reg_pitchdisc   "../FS-E2/evidence/phase0/lists/r2n_pitchdisc.list"
run_one reg_motiondir   "../FS-E2/evidence/phase0/lists/r2n_motiondir.list"
echo "run $RUN complete"
