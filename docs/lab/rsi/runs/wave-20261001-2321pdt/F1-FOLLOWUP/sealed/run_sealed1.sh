#!/bin/sh
# Sealed evaluation runner, Part 1 (wave-20261001-2321pdt lane F1-FOLLOWUP).
# Frozen binaries only. Each invocation executed 3 times (runs1/1,2,3);
# corresponding outputs are cmp-verified byte-identical.
# Pure shell + frozen binaries + cmp/sha256sum. No Python.
set -u
F1D="$(dirname "$0")/.."
LDIR="$(cd "$F1D" && pwd)"
BIN="/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2321pdt/F1/impl/f1_learn"
OLD_BIN="/home/hatch/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2021pdt/F1/dev/bin/f1_learn"
SEALED="$LDIR/sealed"
RUNS="$LDIR/runs1"

want="6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847"
got="$(sha256sum "$BIN" | cut -d' ' -f1)"
if [ "$got" != "$want" ]; then echo "BINARY MISMATCH: $got"; exit 1; fi
echo "binary OK: $got"
oldwant="0c571abca5a3c16695115228114c327bb3370081304c9c3a1ea1354840aa2727"
oldgot="$(sha256sum "$OLD_BIN" | cut -d' ' -f1)"
if [ "$oldgot" != "$oldwant" ]; then echo "OLD BINARY MISMATCH: $oldgot"; exit 1; fi
echo "old binary OK: $oldgot"
(cd "$SEALED" && sha256sum -c FIXTURE_SHA256.txt > /dev/null) || { echo "FIXTURE MISMATCH"; exit 1; }
echo "fixtures OK"

do3() {
    # do3 <binary> <episodes> <state_in> <outbase>
    # state_in may contain {r} replaced by the repetition number.
    bin="$1"; ep="$2"; sin="$3"; base="$4"
    r=1
    while [ $r -le 3 ]; do
        d="$RUNS/$r"
        mkdir -p "$d"
        s_in="$sin"
        case "$s_in" in *"{r}"*) s_in="$(echo "$s_in" | sed "s/{r}/$r/g")";; esac
        "$bin" "$ep" "$s_in" "$d/$base.state" "$d/$base.trace" "$d/$base.pred" \
            > "$d/$base.stdout" 2> "$d/$base.stderr"
        echo "$?" > "$d/$base.rc"
        r=$((r+1))
    done
}

S="$SEALED"
for T in tA tB tC tD; do
    do3 "$BIN" "$S/${T}_train.ep" "-" "${T}_train"
    do3 "$BIN" "$S/${T}_hidden.ep" "$RUNS/{r}/${T}_train.state" "${T}_hidden"
    do3 "$BIN" "$S/${T}_hidden.ep" "-" "${T}_abl"
done
do3 "$BIN" "$S/cA_clean.ep" "-" "cA"
do3 "$BIN" "$S/cB_train.ep" "-" "cB_train"
do3 "$BIN" "$S/cB_clean.ep" "$RUNS/{r}/cB_train.state" "cB"
do3 "$BIN" "$S/cC_train.ep" "-" "cC_train"
do3 "$BIN" "$S/cC_clean.ep" "$RUNS/{r}/cC_train.state" "cC"
# Corrected K-C0C-REG Leg W2: prior-wave validated fixtures, both binaries.
do3 "$BIN" "$S/w2_train.ep" "-" "w2_train"
do3 "$BIN" "$S/w2_hidden.ep" "$RUNS/{r}/w2_train.state" "w2_hidden"
do3 "$OLD_BIN" "$S/w2_train.ep" "-" "w2old_train"
do3 "$OLD_BIN" "$S/w2_hidden.ep" "$RUNS/{r}/w2old_train.state" "w2old_hidden"
do3 "$BIN" "$S/rW3_train.ep" "-" "rW3_train"
do3 "$BIN" "$S/rW3_hidden.ep" "$RUNS/{r}/rW3_train.state" "rW3_hidden"
do3 "$OLD_BIN" "$S/tA_train.ep" "-" "nc_old"

echo "runs complete; verifying byte-identical across repetitions..."
fail=0
for base in tA_train tA_hidden tA_abl tB_train tB_hidden tB_abl tC_train tC_hidden tC_abl tD_train tD_hidden tD_abl cA cB_train cB cC_train cC w2_train w2_hidden w2old_train w2old_hidden rW3_train rW3_hidden nc_old; do
    for ext in state trace pred; do
        if ! cmp -s "$RUNS/1/$base.$ext" "$RUNS/2/$base.$ext"; then echo "DIFF $base.$ext 1v2"; fail=1; fi
        if ! cmp -s "$RUNS/1/$base.$ext" "$RUNS/3/$base.$ext"; then echo "DIFF $base.$ext 1v3"; fail=1; fi
    done
done
if [ $fail -eq 0 ]; then echo "DETERMINISM OK: all 3 repetitions byte-identical"; else echo "DETERMINISM FAIL"; exit 1; fi
(cd "$RUNS/1" && sha256sum *.state *.trace *.pred | sort > ../DETERMINISM_SHA256.txt)
echo "wrote $RUNS/DETERMINISM_SHA256.txt"
