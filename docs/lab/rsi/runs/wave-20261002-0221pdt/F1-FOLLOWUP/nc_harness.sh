#!/bin/sh
# NC-HARNESS calibration (F1-FOLLOWUP, wave-20261002-0221pdt).
# PREREG_F1FOLLOWUP.md section 6: regenerate prior Part 2 fixtures i=0..5
# with this lane's generator copy, cmp byte-identical against the prior
# lane's sealed2/ fixtures, run all 6 through this lane's run protocol
# (3/3 byte-identical), and require the known outcomes:
#   i in {2,3,5}: hidden acc < 30/30 (known overfits)
#   i in {0,1,4}: hidden acc = 30/30 (known corrects)
# plus hidden pred outputs byte-identical to the prior lane's runs2/1.
# Any mismatch -> VOID (harness miscalibrated). Pure shell. No Python.
set -u
LDIR="$(cd "$(dirname "$0")" && pwd)"
WGEN="$LDIR/dev/f1_wgen"
SCORE="$LDIR/dev/f1_score"
PRIOR="/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2321pdt/F1-FOLLOWUP"
BIN="$PRIOR/../F1/impl/f1_learn"
NC="$LDIR/ncharness"
mkdir -p "$NC/fix" "$NC/runs"

want="6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847"
got="$(sha256sum "$BIN" | cut -d' ' -f1)"
if [ "$got" != "$want" ]; then echo "NC BINARY MISMATCH: $got"; exit 1; fi
echo "NC binary OK"

# 1. regenerate prior fixtures and cmp
i=0
while [ $i -lt 6 ]; do
    ts=$((5100 + 2 * i)); hs=$((5101 + 2 * i))
    "$WGEN" sum2 "$ts" 24 train "$NC/fix/nc_train_$i.ep" > /dev/null
    "$WGEN" sum2 "$hs" 30 hide "$NC/fix/nc_hidden_$i.ep" > /dev/null
    "$WGEN" sum2 "$hs" 30 truth "$NC/fix/nc_truth_$i.ep" > /dev/null
    cmp -s "$NC/fix/nc_train_$i.ep" "$PRIOR/sealed2/s2_train_$i.ep" || { echo "NC FIXTURE DIFF train $i"; exit 1; }
    cmp -s "$NC/fix/nc_hidden_$i.ep" "$PRIOR/sealed2/s2_hidden_$i.ep" || { echo "NC FIXTURE DIFF hidden $i"; exit 1; }
    cmp -s "$NC/fix/nc_truth_$i.ep" "$PRIOR/sealed2/s2_truth_$i.ep" || { echo "NC FIXTURE DIFF truth $i"; exit 1; }
    i=$((i + 1))
done
echo "NC fixtures: 6/6 byte-identical to prior sealed2/"

# 2. run all 6, 3 repetitions
i=0
while [ $i -lt 6 ]; do
    r=1
    while [ $r -le 3 ]; do
        d="$NC/runs/$r"; mkdir -p "$d"
        "$BIN" "$NC/fix/nc_train_$i.ep" "-" "$d/nc_${i}_train.state" "$d/nc_${i}_train.trace" "$d/nc_${i}_train.pred" > /dev/null 2>&1
        "$BIN" "$NC/fix/nc_hidden_$i.ep" "$d/nc_${i}_train.state" "$d/nc_${i}_hidden.state" "$d/nc_${i}_hidden.trace" "$d/nc_${i}_hidden.pred" > /dev/null 2>&1
        r=$((r + 1))
    done
    i=$((i + 1))
done
# 3. determinism + outcome checks
fail=0
i=0
while [ $i -lt 6 ]; do
    for base in "nc_${i}_train" "nc_${i}_hidden"; do
        for ext in state trace pred; do
            cmp -s "$NC/runs/1/$base.$ext" "$NC/runs/2/$base.$ext" || { echo "NC DETERM DIFF $base.$ext 1v2"; fail=1; }
            cmp -s "$NC/runs/1/$base.$ext" "$NC/runs/3/$base.$ext" || { echo "NC DETERM DIFF $base.$ext 1v3"; fail=1; }
        done
    done
    cmp -s "$NC/runs/1/nc_${i}_hidden.pred" "$PRIOR/runs2/1/s2_${i}_hidden.pred" || { echo "NC PRED DIFF vs prior runs2/1 seed $i"; fail=1; }
    acc="$("$SCORE" acc "$NC/runs/1/nc_${i}_hidden.pred" "$NC/fix/nc_truth_$i.ep")"
    set -- $acc
    # acc format: ACC <num> <den> <pct>
    num=$2; den=$3
    case $i in
        2|3|5) if [ "$num" -ge "$den" ]; then echo "NC OUTCOME FAIL seed $i: expected overfit, got $num/$den"; fail=1; fi ;;
        0|1|4) if [ "$num" -ne "$den" ]; then echo "NC OUTCOME FAIL seed $i: expected 30/30, got $num/$den"; fail=1; fi ;;
    esac
    echo "NC seed $i: acc $num/$den"
    i=$((i + 1))
done
if [ $fail -eq 0 ]; then echo "NC-HARNESS: PASS (calibration holds)"; else echo "NC-HARNESS: FAIL -> VOID"; exit 1; fi
