#!/bin/sh
# Sealed evaluation runner for F1 trigger wave (wave-20261001-2321pdt).
# Runs the frozen binary on sealed fixtures only. Each invocation is
# executed 3 times (runs/1, runs/2, runs/3); corresponding outputs are
# cmp-verified byte-identical. Pure shell + frozen binaries + cmp/sha256sum.
set -u
F1D="$(dirname "$0")/.."
BIN="$F1D/impl/f1_learn"
SEALED="$F1D/sealed"
OLD_BIN="$HOME/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2021pdt/F1/dev/bin/f1_learn"

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

# NOTE: f1_learn writes outputs to paths given as args 3,4,5. We pass
# per-repetition paths via do3 below.

do3() {
    # do3 <tag> <binary> <episodes> <state_in> <outbase>
    # state_in may contain {r} which is replaced by the repetition number,
    # so each repetition's hidden run uses its own repetition's train state.
    tag="$1"; bin="$2"; ep="$3"; sin="$4"; base="$5"
    r=1
    while [ $r -le 3 ]; do
        d="$SEALED/runs/$r"
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
    do3 "${T}_train" "$BIN" "$S/${T}_train.ep" "-" "${T}_train"
    do3 "${T}_hidden" "$BIN" "$S/${T}_hidden.ep" "$S/runs/{r}/${T}_train.state" "${T}_hidden"
    do3 "${T}_abl" "$BIN" "$S/${T}_hidden.ep" "-" "${T}_abl"
done
do3 "cA" "$BIN" "$S/cA_clean.ep" "-" "cA"
do3 "cB_train" "$BIN" "$S/cB_train.ep" "-" "cB_train"
do3 "cB" "$BIN" "$S/cB_clean.ep" "$S/runs/{r}/cB_train.state" "cB"
do3 "cC_train" "$BIN" "$S/cC_train.ep" "-" "cC_train"
do3 "cC" "$BIN" "$S/cC_clean.ep" "$S/runs/{r}/cC_train.state" "cC"
do3 "rW2_train" "$BIN" "$S/rW2_train.ep" "-" "rW2_train"
do3 "rW2_hidden" "$BIN" "$S/rW2_hidden.ep" "$S/runs/{r}/rW2_train.state" "rW2_hidden"
do3 "rW3_train" "$BIN" "$S/rW3_train.ep" "-" "rW3_train"
do3 "rW3_hidden" "$BIN" "$S/rW3_hidden.ep" "$S/runs/{r}/rW3_train.state" "rW3_hidden"
do3 "nc_old" "$OLD_BIN" "$S/tA_train.ep" "-" "nc_old"

echo "runs complete; verifying byte-identical across repetitions..."
fail=0
for base in tA_train tA_hidden tA_abl tB_train tB_hidden tB_abl tC_train tC_hidden tC_abl tD_train tD_hidden tD_abl cA cB_train cB cC_train cC rW2_train rW2_hidden rW3_train rW3_hidden nc_old; do
    for ext in state trace pred; do
        if ! cmp -s "$S/runs/1/$base.$ext" "$S/runs/2/$base.$ext"; then echo "DIFF $base.$ext 1v2"; fail=1; fi
        if ! cmp -s "$S/runs/1/$base.$ext" "$S/runs/3/$base.$ext"; then echo "DIFF $base.$ext 1v3"; fail=1; fi
    done
done
if [ $fail -eq 0 ]; then echo "DETERMINISM OK: all 3 repetitions byte-identical"; else echo "DETERMINISM FAIL"; exit 1; fi
(cd "$S/runs/1" && sha256sum *.state *.trace *.pred | sort > ../DETERMINISM_SHA256.txt)
echo "wrote $S/runs/DETERMINISM_SHA256.txt"
