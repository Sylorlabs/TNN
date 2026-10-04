#!/bin/sh
# F1-REPAIR sealed runs (wave-20261001-2321pdt).
# Runs the frozen F1 binary (constructor read-only) on the 24 fresh
# sealed sum2 worlds (6100-series). Each invocation executed 3 times
# (runs4/1,2,3); corresponding outputs are cmp-verified byte-identical.
# Scores with the frozen pure-Zag f1_score copy, extracts the
# repair-burst signature with the frozen pure-Zag repsig, and applies
# the frozen decision rule with repapply (PREREG_REPAIR.md sections
# 2 and 3). Pure shell + frozen binaries + cmp/sha256sum. No Python.
set -u
LDIR="$(cd "$(dirname "$0")/.." && pwd)"
BIN="/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2321pdt/F1/impl/f1_learn"
S4="$LDIR/sealed4"
RUNS="$LDIR/runs4"
DEV="$LDIR/dev"

want="6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847"
got="$(sha256sum "$BIN" | cut -d' ' -f1)"
if [ "$got" != "$want" ]; then echo "BINARY MISMATCH: $got"; exit 1; fi
echo "binary OK: $got"
(cd "$S4" && sha256sum -c FIXTURE_SHA256.txt > /dev/null) || { echo "FIXTURE MISMATCH"; exit 1; }
echo "fixtures OK"

i=0
while [ $i -lt 24 ]; do
    r=1
    while [ $r -le 3 ]; do
        d="$RUNS/$r"
        mkdir -p "$d"
        "$BIN" "$S4/s4_train_$i.ep" "-" "$d/s4_${i}_train.state" "$d/s4_${i}_train.trace" "$d/s4_${i}_train.pred" \
            > "$d/s4_${i}_train.stdout" 2> "$d/s4_${i}_train.stderr"
        echo "$?" > "$d/s4_${i}_train.rc"
        "$BIN" "$S4/s4_hidden_$i.ep" "$d/s4_${i}_train.state" "$d/s4_${i}_hidden.state" "$d/s4_${i}_hidden.trace" "$d/s4_${i}_hidden.pred" \
            > "$d/s4_${i}_hidden.stdout" 2> "$d/s4_${i}_hidden.stderr"
        echo "$?" > "$d/s4_${i}_hidden.rc"
        r=$((r + 1))
    done
    i=$((i + 1))
done

echo "runs complete; verifying byte-identical across repetitions..."
fail=0
i=0
while [ $i -lt 24 ]; do
    for base in "s4_${i}_train" "s4_${i}_hidden"; do
        for ext in state trace pred; do
            if ! cmp -s "$RUNS/1/$base.$ext" "$RUNS/2/$base.$ext"; then echo "DIFF $base.$ext 1v2"; fail=1; fi
            if ! cmp -s "$RUNS/1/$base.$ext" "$RUNS/3/$base.$ext"; then echo "DIFF $base.$ext 1v3"; fail=1; fi
        done
    done
    i=$((i + 1))
done
if [ $fail -eq 0 ]; then echo "DETERMINISM OK: all 24 seeds x 3 repetitions byte-identical"; else echo "DETERMINISM FAIL"; exit 1; fi
(cd "$RUNS/1" && sha256sum *.state *.trace *.pred | sort > ../DETERMINISM_SHA256.txt)

echo "scoring hidden sets and extracting repair signatures..."
: > "$RUNS/fresh_scores.txt"
: > "$RUNS/fresh_table.txt"
: > "$RUNS/fresh_reps.txt"
notrig=0
parsefail=0
i=0
while [ $i -lt 24 ]; do
    acc="$("$DEV/f1_score" acc "$RUNS/1/s4_${i}_hidden.pred" "$S4/s4_truth_$i.ep")"
    # acc prints: ACC <got> 30 <pct>
    set -- $acc
    gotn=$2
    if [ "$gotn" -ge 24 ]; then lab=CORRECT; else lab=OVERFIT; fi
    echo "seed $i acc=$gotn/30 $lab" >> "$RUNS/fresh_scores.txt"
    out="$("$DEV/repsig" "$RUNS/1/s4_${i}_train.trace")"
    echo "seed $i: $out" >> "$RUNS/fresh_reps.txt"
    set -- $out
    if [ "$1 $2" = "REPSIG NOTRIG" ]; then
        echo "NOTRIG seed $i"
        notrig=$((notrig + 1))
        echo "SEED $i $lab DEG=0 S=0 TRIG=-1 NREP=0" >> "$RUNS/fresh_table.txt"
    elif [ "$1 $2" = "REPSIG PARSEFAIL" ]; then
        echo "PARSEFAIL seed $i"
        parsefail=$((parsefail + 1))
        echo "SEED $i $lab DEG=0 S=0 TRIG=-2 NREP=0" >> "$RUNS/fresh_table.txt"
    else
        trig=${2#trig=}; deg=${3#deg=}; s=${4#S=}; nrep=${5#nrep=}
        echo "SEED $i $lab DEG=$deg S=$s TRIG=$trig NREP=$nrep" >> "$RUNS/fresh_table.txt"
    fi
    echo "seed $i: acc=$gotn/30 $lab sig=($out)"
    i=$((i + 1))
done
echo "NOTRIG=$notrig PARSEFAIL=$parsefail"
echo "wrote $RUNS/fresh_table.txt $RUNS/fresh_scores.txt $RUNS/fresh_reps.txt"

echo "applying frozen decision rule..."
"$DEV/repapply" "$RUNS/fresh_table.txt" | tee "$RUNS/verdict.txt"
