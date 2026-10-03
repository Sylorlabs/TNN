#!/bin/sh
# run_sealed.sh - sealed runs for the F1 seed-sensitivity finding lane,
# wave-20261002-0521pdt. Frozen run protocol: PREREG_SEEDSENS.md
# section 4. 40 seeds x 3 repetitions with the frozen F1 binary,
# K-DET cmp verification on state/trace/pred for train and hidden,
# DETERMINISM_SHA256.txt. Pure shell + frozen binary. No Python.
set -u
LDIR="$(cd "$(dirname "$0")" && pwd)"
BIN="$HOME/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2321pdt/F1/impl/f1_learn"
FROZEN_HASH="6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847"
S="$LDIR/sealed5"
RUNS="$LDIR/runs"

got="$(sha256sum "$BIN" | awk '{print $1}')"
if [ "$got" != "$FROZEN_HASH" ]; then echo "BINARY MISMATCH: $got"; exit 1; fi
echo "binary hash OK"
(cd "$S" && sha256sum -c FIXTURE_SHA256.txt > /dev/null) || { echo "FIXTURE MANIFEST MISMATCH"; exit 1; }
echo "fixture manifest OK"

i=0
while [ $i -lt 40 ]; do
    r=1
    while [ $r -le 3 ]; do
        d="$RUNS/$r"
        mkdir -p "$d"
        "$BIN" "$S/s5_train_$i.ep" "-" "$d/s5_${i}_train.state" "$d/s5_${i}_train.trace" "$d/s5_${i}_train.pred" \
            > "$d/s5_${i}_train.stdout" 2> "$d/s5_${i}_train.stderr"
        echo "$?" > "$d/s5_${i}_train.rc"
        "$BIN" "$S/s5_hidden_$i.ep" "$d/s5_${i}_train.state" "$d/s5_${i}_hidden.state" "$d/s5_${i}_hidden.trace" "$d/s5_${i}_hidden.pred" \
            > "$d/s5_${i}_hidden.stdout" 2> "$d/s5_${i}_hidden.stderr"
        echo "$?" > "$d/s5_${i}_hidden.rc"
        r=$((r + 1))
    done
    i=$((i + 1))
done

echo "runs complete; verifying byte-identical across repetitions..."
fail=0
i=0
while [ $i -lt 40 ]; do
    for base in "s5_${i}_train" "s5_${i}_hidden"; do
        for ext in state trace pred; do
            if ! cmp -s "$RUNS/1/$base.$ext" "$RUNS/2/$base.$ext"; then echo "DIFF $base.$ext 1v2"; fail=1; fi
            if ! cmp -s "$RUNS/1/$base.$ext" "$RUNS/3/$base.$ext"; then echo "DIFF $base.$ext 1v3"; fail=1; fi
        done
    done
    i=$((i + 1))
done
if [ $fail -ne 0 ]; then echo "K-DET FAIL"; exit 1; fi
echo "K-DET PASS: 40 seeds x 3 repetitions byte-identical"
(cd "$RUNS/1" && sha256sum s5_*_train.state s5_*_train.trace s5_*_train.pred s5_*_hidden.state s5_*_hidden.trace s5_*_hidden.pred | sort > "$RUNS/DETERMINISM_SHA256.txt")
echo "wrote $RUNS/DETERMINISM_SHA256.txt"
