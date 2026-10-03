#!/bin/sh
# nc_harness.sh - NC-HARNESS calibration (PREREG_SEEDSENS.md section 6).
# With this lane's generator copy, regenerate prior Part 2 fixtures
# i = 0..5 (train seeds 5100, 5102, ..., 5110), cmp-verify byte-identical
# against the prior lane's sealed2/ fixtures, run all 6 through the
# frozen F1 binary (3/3 byte-identical reruns), and require the known
# hidden accuracies (i in {2,3,5}: 5/30, 0/30, 2/30; i in {0,1,4}: 30/30)
# with hidden preds byte-identical to the prior lane's runs2/1 preds.
# Runs in /tmp only; nothing here enters the sealed battery.
# Pure shell + frozen binaries. No Python.
set -u
LDIR="$(cd "$(dirname "$0")" && pwd)"
WGEN="$LDIR/dev/f1_wgen"
SCORE="$LDIR/dev/f1_score"
BIN="$HOME/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2321pdt/F1/impl/f1_learn"
PRI="$HOME/workspace/tnn-rsi/docs/lab/rsi/runs/wave-20261001-2321pdt/F1-FOLLOWUP"
FROZEN_HASH="6f2b155b233a95ad1a8323e8565b9a798dc822db6eff57e065b71b5be8882847"

echo "$BIN" | { read -r b; h=$(sha256sum "$b" | awk '{print $1}'); [ "$h" = "$FROZEN_HASH" ] || { echo "BIN HASH MISMATCH $h"; exit 1; }; }
echo "binary hash OK"

NC=/tmp/f1s_nc
rm -rf "$NC"; mkdir -p "$NC"

i=0
while [ $i -lt 6 ]; do
    ts=$((5100 + 2 * i))
    hs=$((5101 + 2 * i))
    "$WGEN" sum2 "$ts" 24 train "$NC/nc_train_$i.ep" > /dev/null
    "$WGEN" sum2 "$hs" 30 hide "$NC/nc_hidden_$i.ep" > /dev/null
    "$WGEN" sum2 "$hs" 30 truth "$NC/nc_truth_$i.ep" > /dev/null
    cmp -s "$NC/nc_train_$i.ep" "$PRI/sealed2/s2_train_$i.ep" || { echo "NC FAIL fixture train $i"; exit 1; }
    cmp -s "$NC/nc_hidden_$i.ep" "$PRI/sealed2/s2_hidden_$i.ep" || { echo "NC FAIL fixture hidden $i"; exit 1; }
    cmp -s "$NC/nc_truth_$i.ep" "$PRI/sealed2/s2_truth_$i.ep" || { echo "NC FAIL fixture truth $i"; exit 1; }
    i=$((i + 1))
done
echo "NC fixtures 6/6 byte-identical"

i=0
while [ $i -lt 6 ]; do
    r=1
    while [ $r -le 3 ]; do
        "$BIN" "$NC/nc_train_$i.ep" "-" "$NC/nc_$i.train.state.$r" "$NC/nc_$i.train.trace.$r" "$NC/nc_$i.train.pred.$r" > /dev/null 2>&1 || { echo "NC FAIL run train $i r$r"; exit 1; }
        "$BIN" "$NC/nc_hidden_$i.ep" "$NC/nc_$i.train.state.$r" "$NC/nc_$i.hidden.state.$r" "$NC/nc_$i.hidden.trace.$r" "$NC/nc_$i.hidden.pred.$r" > /dev/null 2>&1 || { echo "NC FAIL run hidden $i r$r"; exit 1; }
        r=$((r + 1))
    done
    cmp -s "$NC/nc_$i.train.trace.1" "$NC/nc_$i.train.trace.2" || { echo "NC FAIL determinism train $i"; exit 1; }
    cmp -s "$NC/nc_$i.train.trace.1" "$NC/nc_$i.train.trace.3" || { echo "NC FAIL determinism train $i"; exit 1; }
    cmp -s "$NC/nc_$i.hidden.pred.1" "$NC/nc_$i.hidden.pred.2" || { echo "NC FAIL determinism hidden $i"; exit 1; }
    cmp -s "$NC/nc_$i.hidden.pred.1" "$NC/nc_$i.hidden.pred.3" || { echo "NC FAIL determinism hidden $i"; exit 1; }
    cmp -s "$NC/nc_$i.hidden.pred.1" "$PRI/runs2/1/s2_${i}_hidden.pred" || { echo "NC FAIL pred identity $i"; exit 1; }
    acc=$("$SCORE" acc "$NC/nc_$i.hidden.pred.1" "$NC/nc_truth_$i.ep")
    echo "NC seed $i: $acc"
    i=$((i + 1))
done

# known accuracies
chk() { # i expected_num
    a=$("$SCORE" acc "$NC/nc_$1.hidden.pred.1" "$NC/nc_truth_$1.ep" | awk '{print $2}')
    [ "$a" = "$2" ] || { echo "NC FAIL acc $1: got $a want $2"; exit 1; }
}
chk 0 30; chk 1 30; chk 2 5; chk 3 0; chk 4 30; chk 5 2
echo "NC-HARNESS PASS: 6/6 known outcomes, byte-identical"
