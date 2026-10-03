#!/bin/sh
# F1-REPAIR2 sealed runs (wave-20261001-2321pdt).
# Runs the frozen F1 binary (constructor read-only) on the 24 fresh
# sealed sum2 worlds (7300-series). Each invocation executed 3 times
# (runs5/1,2,3); corresponding outputs are cmp-verified byte-identical.
# Scores with the frozen pure-Zag f1_score copy, extracts S-prime and
# the POLICY-R check with the frozen pure-Zag r2sig, and applies the
# frozen decision rule with r2apply (PREREG_REPAIR2.md sections 2,3).
# Pure shell + frozen binaries + cmp/sha256sum. No Python.
set -u
LDIR="$(cd "$(dirname "$0")/.." && pwd)"
BIN="$LDIR/dev/f1_learn"
S5="$LDIR/sealed5"
RUNS="$LDIR/runs5"
DEV="$LDIR/dev"

want="6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847"
got="$(sha256sum "$BIN" | cut -d' ' -f1)"
if [ "$got" != "$want" ]; then echo "BINARY MISMATCH: $got"; exit 1; fi
echo "binary OK: $got"
(cd "$S5" && sha256sum -c FIXTURE_SHA256.txt > /dev/null) || { echo "FIXTURE MISMATCH"; exit 1; }
echo "fixtures OK"

i=0
while [ $i -lt 24 ]; do
    r=1
    while [ $r -le 3 ]; do
        d="$RUNS/$r"
        mkdir -p "$d"
        "$BIN" "$S5/s5_train_$i.ep" "-" "$d/s5_${i}_train.state" "$d/s5_${i}_train.trace" "$d/s5_${i}_train.pred" \
            > "$d/s5_${i}_train.stdout" 2> "$d/s5_${i}_train.stderr"
        echo "$?" > "$d/s5_${i}_train.rc"
        "$BIN" "$S5/s5_hidden_$i.ep" "$d/s5_${i}_train.state" "$d/s5_${i}_hidden.state" "$d/s5_${i}_hidden.trace" "$d/s5_${i}_hidden.pred" \
            > "$d/s5_${i}_hidden.stdout" 2> "$d/s5_${i}_hidden.stderr"
        echo "$?" > "$d/s5_${i}_hidden.rc"
        r=$((r + 1))
    done
    i=$((i + 1))
done

echo "runs complete; verifying byte-identical across repetitions..."
fail=0
i=0
while [ $i -lt 24 ]; do
    for base in "s5_${i}_train" "s5_${i}_hidden"; do
        for ext in state trace pred; do
            if ! cmp -s "$RUNS/1/$base.$ext" "$RUNS/2/$base.$ext"; then echo "DIFF $base.$ext 1v2"; fail=1; fi
            if ! cmp -s "$RUNS/1/$base.$ext" "$RUNS/3/$base.$ext"; then echo "DIFF $base.$ext 1v3"; fail=1; fi
        done
    done
    i=$((i + 1))
done
if [ $fail -eq 0 ]; then echo "DETERMINISM OK: all 24 seeds x 3 repetitions byte-identical"; else echo "DETERMINISM FAIL"; exit 1; fi
(cd "$RUNS/1" && sha256sum *.state *.trace *.pred | sort > ../DETERMINISM_SHA256.txt)

echo "scoring hidden sets and extracting S-prime / POLICY-R..."
: > "$RUNS/fresh_scores.txt"
: > "$RUNS/fresh_table.txt"
: > "$RUNS/fresh_sigs.txt"
notrig=0
parsefail=0
i=0
while [ $i -lt 24 ]; do
    acc="$("$DEV/f1_score" acc "$RUNS/1/s5_${i}_hidden.pred" "$S5/s5_truth_$i.ep")"
    # acc prints: ACC <got> 30 <pct>
    set -- $acc
    gotn=$2
    if [ "$gotn" -ge 24 ]; then lab=CORRECT; else lab=OVERFIT; fi
    echo "seed $i acc=$gotn/30 $lab" >> "$RUNS/fresh_scores.txt"
    out="$("$DEV/r2sig" "$i" "$RUNS/1/s5_${i}_train.trace")"
    echo "seed $i: $out" >> "$RUNS/fresh_sigs.txt"
    set -- $out
    if [ "$3" = "NOTRIG" ]; then
        echo "NOTRIG seed $i"
        notrig=$((notrig + 1))
        echo "SEED $i $lab DEG=0 SPRIME=0 TRIG=-1 NREP=0 POLOK=1" >> "$RUNS/fresh_table.txt"
    elif [ "$3" = "PARSEFAIL" ]; then
        echo "PARSEFAIL seed $i"
        parsefail=$((parsefail + 1))
        echo "SEED $i $lab DEG=0 SPRIME=0 TRIG=-2 NREP=0 POLOK=1" >> "$RUNS/fresh_table.txt"
    else
        trig=${3#trig=}; deg=${4#deg=}; s=${5#Sprime=}; nrep=${6#nrep=}; polok=${7#polok=}
        echo "SEED $i $lab DEG=$deg SPRIME=$s TRIG=$trig NREP=$nrep POLOK=$polok" >> "$RUNS/fresh_table.txt"
    fi
    echo "seed $i: acc=$gotn/30 $lab sig=($out)"
    i=$((i + 1))
done
echo "NOTRIG=$notrig PARSEFAIL=$parsefail"
echo "wrote $RUNS/fresh_table.txt $RUNS/fresh_scores.txt $RUNS/fresh_sigs.txt"

echo "applying frozen decision rule..."
"$DEV/r2apply" "$RUNS/fresh_table.txt" | tee "$RUNS/verdict.txt"
