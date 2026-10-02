#!/bin/sh
# F1-BUFFER sealed runs (wave-20261001-2321pdt).
# Runs the frozen F1 binary (constructor read-only) on the 24 fresh
# sealed sum2 worlds (8100-series). Each invocation executed 3 times
# (runs3/1,2,3); corresponding outputs are cmp-verified byte-identical.
# Scores with the frozen pure-Zag f1_score copy, extracts first-trigger
# buffer features with the frozen pure-Zag bufx, and applies the frozen
# rule with bufapply (T>=12 predicts OVERFIT, per PREREG_BUFFER.md).
# Pure shell + frozen binaries + cmp/sha256sum. No Python.
set -u
LDIR="$(cd "$(dirname "$0")/.." && pwd)"
BIN="/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2321pdt/F1/impl/f1_learn"
S3="$LDIR/sealed3"
RUNS="$LDIR/runs3"
DEV="$LDIR/dev"

want="6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847"
got="$(sha256sum "$BIN" | cut -d' ' -f1)"
if [ "$got" != "$want" ]; then echo "BINARY MISMATCH: $got"; exit 1; fi
echo "binary OK: $got"
(cd "$S3" && sha256sum -c FIXTURE_SHA256.txt > /dev/null) || { echo "FIXTURE MISMATCH"; exit 1; }
echo "fixtures OK"

i=0
while [ $i -lt 24 ]; do
    r=1
    while [ $r -le 3 ]; do
        d="$RUNS/$r"
        mkdir -p "$d"
        "$BIN" "$S3/s3_train_$i.ep" "-" "$d/s3_${i}_train.state" "$d/s3_${i}_train.trace" "$d/s3_${i}_train.pred" \
            > "$d/s3_${i}_train.stdout" 2> "$d/s3_${i}_train.stderr"
        echo "$?" > "$d/s3_${i}_train.rc"
        "$BIN" "$S3/s3_hidden_$i.ep" "$d/s3_${i}_train.state" "$d/s3_${i}_hidden.state" "$d/s3_${i}_hidden.trace" "$d/s3_${i}_hidden.pred" \
            > "$d/s3_${i}_hidden.stdout" 2> "$d/s3_${i}_hidden.stderr"
        echo "$?" > "$d/s3_${i}_hidden.rc"
        r=$((r + 1))
    done
    i=$((i + 1))
done

echo "runs complete; verifying byte-identical across repetitions..."
fail=0
i=0
while [ $i -lt 24 ]; do
    for base in "s3_${i}_train" "s3_${i}_hidden"; do
        for ext in state trace pred; do
            if ! cmp -s "$RUNS/1/$base.$ext" "$RUNS/2/$base.$ext"; then echo "DIFF $base.$ext 1v2"; fail=1; fi
            if ! cmp -s "$RUNS/1/$base.$ext" "$RUNS/3/$base.$ext"; then echo "DIFF $base.$ext 1v3"; fail=1; fi
        done
    done
    i=$((i + 1))
done
if [ $fail -eq 0 ]; then echo "DETERMINISM OK: all 24 seeds x 3 repetitions byte-identical"; else echo "DETERMINISM FAIL"; exit 1; fi
(cd "$RUNS/1" && sha256sum *.state *.trace *.pred | sort > ../DETERMINISM_SHA256.txt)

echo "scoring hidden sets and extracting buffer features..."
: > "$RUNS/fresh_table.txt"
: > "$RUNS/fresh_scores.txt"
i=0
while [ $i -lt 24 ]; do
    acc="$("$DEV/f1_score" acc "$RUNS/1/s3_${i}_hidden.pred" "$S3/s3_truth_$i.ep")"
    # acc prints: ACC <got> 30 <pct>
    set -- $acc
    gotn=$2
    if [ "$gotn" -ge 24 ]; then lab=CORRECT; else lab=OVERFIT; fi
    echo "seed $i acc=$gotn/30 $lab" >> "$RUNS/fresh_scores.txt"
    out="$("$DEV/bufx" "$RUNS/1/s3_${i}_train.trace")"
    set -- $out
    if [ "$1" = "BUF" ] && [ "$2" = "NOTRIG" ]; then echo "NOTRIG seed $i"; echo "SEED $i $lab S0=0 S1=0 N=0 TRIG=-1" >> "$RUNS/fresh_table.txt"; else
        trig=${2#trig=}; nn=${3#n=}; s0=${4#S0=}; s1=${5#S1=}
        echo "SEED $i $lab S0=$s0 S1=$s1 N=$nn TRIG=$trig" >> "$RUNS/fresh_table.txt"
    fi
    echo "seed $i: $acc -> $lab"
    i=$((i + 1))
done
echo "wrote $RUNS/fresh_table.txt"
