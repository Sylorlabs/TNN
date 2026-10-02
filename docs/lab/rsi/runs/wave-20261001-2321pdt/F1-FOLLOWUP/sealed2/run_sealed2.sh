#!/bin/sh
# Part 2 sealed runs (wave-20261001-2321pdt lane F1-FOLLOWUP).
# Runs the frozen F1 binary (constructor read-only) on the 24 sealed
# sum2 worlds. Each invocation executed 3 times (runs2/1,2,3);
# corresponding outputs are cmp-verified byte-identical.
# Pure shell + frozen binaries + cmp/sha256sum. No Python.
set -u
LDIR="$(cd "$(dirname "$0")/.." && pwd)"
BIN="/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2321pdt/F1/impl/f1_learn"
S2="$LDIR/sealed2"
RUNS="$LDIR/runs2"

want="6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847"
got="$(sha256sum "$BIN" | cut -d' ' -f1)"
if [ "$got" != "$want" ]; then echo "BINARY MISMATCH: $got"; exit 1; fi
echo "binary OK: $got"
(cd "$S2" && sha256sum -c FIXTURE_SHA256.txt > /dev/null) || { echo "FIXTURE MISMATCH"; exit 1; }
echo "fixtures OK"

i=0
while [ $i -lt 24 ]; do
    r=1
    while [ $r -le 3 ]; do
        d="$RUNS/$r"
        mkdir -p "$d"
        "$BIN" "$S2/s2_train_$i.ep" "-" "$d/s2_${i}_train.state" "$d/s2_${i}_train.trace" "$d/s2_${i}_train.pred" \
            > "$d/s2_${i}_train.stdout" 2> "$d/s2_${i}_train.stderr"
        echo "$?" > "$d/s2_${i}_train.rc"
        "$BIN" "$S2/s2_hidden_$i.ep" "$d/s2_${i}_train.state" "$d/s2_${i}_hidden.state" "$d/s2_${i}_hidden.trace" "$d/s2_${i}_hidden.pred" \
            > "$d/s2_${i}_hidden.stdout" 2> "$d/s2_${i}_hidden.stderr"
        echo "$?" > "$d/s2_${i}_hidden.rc"
        r=$((r + 1))
    done
    i=$((i + 1))
done

echo "runs complete; verifying byte-identical across repetitions..."
fail=0
i=0
while [ $i -lt 24 ]; do
    for base in "s2_${i}_train" "s2_${i}_hidden"; do
        for ext in state trace pred; do
            if ! cmp -s "$RUNS/1/$base.$ext" "$RUNS/2/$base.$ext"; then echo "DIFF $base.$ext 1v2"; fail=1; fi
            if ! cmp -s "$RUNS/1/$base.$ext" "$RUNS/3/$base.$ext"; then echo "DIFF $base.$ext 1v3"; fail=1; fi
        done
    done
    i=$((i + 1))
done
if [ $fail -eq 0 ]; then echo "DETERMINISM OK: all 24 seeds x 3 repetitions byte-identical"; else echo "DETERMINISM FAIL"; exit 1; fi
(cd "$RUNS/1" && sha256sum *.state *.trace *.pred | sort > ../DETERMINISM_SHA256.txt)
echo "wrote $RUNS/DETERMINISM_SHA256.txt"
