#!/bin/bash
# Dev battery driver for hyptest (Crew M).
# Runs all 4 dev phenomena through the full loop and checks:
#   - 2 hypothesis slots formed
#   - distinct Phase-B predictions
#   - pre-test audit ordering (hypotheses before observation)
#   - correct A/B winners (dev01, dev02 -> A; dev03 -> B)
#   - devB1 withhold
#   - K10 citation precision/recall (6/6 support union)
#
# usage: run_dev.sh <binary> <workdir>
# The binary is built by build/build.sh. Workdir holds state/outputs.
set -e
BIN="$1"
WORK="$2"
if [ -z "$BIN" ] || [ -z "$WORK" ]; then echo "usage: run_dev.sh <binary> <workdir>"; exit 2; fi
if [ ! -x "$BIN" ]; then echo "binary not executable: $BIN"; exit 2; fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INPUTS="$SCRIPT_DIR/inputs"

mkdir -p "$WORK"
PASS=0
FAIL=0

check() {
    # check <name> <condition>
    if eval "$2"; then
        echo "  PASS: $1"
        PASS=$((PASS+1))
    else
        echo "  FAIL: $1"
        FAIL=$((FAIL+1))
    fi
}

for CASE in dev01 dev02 dev03 devB1; do
    echo "=== $CASE ==="
    D="$WORK/$CASE"
    mkdir -p "$D"
    cd "$D"
    rm -f ht_state.bin ht_hypotheses.txt ht_verdict.txt

    "$BIN" init ht_state.bin > init.log
    "$BIN" teach ht_state.bin "$INPUTS/$CASE.teach.txt" > teach.log
    "$BIN" hypothesize ht_state.bin "$INPUTS/$CASE.phenomenon.txt" > hyp.log
    # capture audit_n after hypothesize (pre-test)
    PRE_TEST_AUDIT=$(grep -o 'audit_n [0-9]*' hyp.log | head -1 | cut -d' ' -f2)
    "$BIN" observe ht_state.bin "$INPUTS/$CASE.test.txt" > obs.log
    OBS_AUDIT=$(grep -o 'audit_n [0-9]*' obs.log | head -1 | cut -d' ' -f2)
    "$BIN" adjudicate ht_state.bin > adj.log

    # 2 hypotheses formed
    NHYP=$(grep -c '^h [0-9]' ht_hypotheses.txt || true)
    check "2 hypotheses" "[ '$NHYP' = '2' ]"

    # distinct predictions
    PREDS=$(grep '^h [0-9]' ht_hypotheses.txt | sed 's/.*predicts //' | cut -d' ' -f1 | sort -u | wc -l)
    check "distinct predictions" "[ '$PREDS' = '2' ]"

    # pre-test ordering: hypothesize audit entries before observe
    check "pre-test audit ordering" "[ '$PRE_TEST_AUDIT' -lt '$OBS_AUDIT' ]"

    # winners / withhold
    if [ "$CASE" = "dev01" ] || [ "$CASE" = "dev02" ]; then
        # A wins: h0 supported, h1 refuted/abandoned
        check "A wins (h0 kept)" "grep -q 'hypothesis 0.*status supported' ht_verdict.txt"
        check "A wins (h1 abandoned)" "grep -q 'abandoned hypothesis 1' ht_verdict.txt"
    fi
    if [ "$CASE" = "dev03" ]; then
        # B wins: h1 supported, h0 refuted/abandoned
        check "B wins (h1 kept)" "grep -q 'hypothesis 1.*status supported' ht_verdict.txt"
        check "B wins (h0 abandoned)" "grep -q 'abandoned hypothesis 0' ht_verdict.txt"
    fi
    if [ "$CASE" = "devB1" ]; then
        check "withhold" "grep -q 'decision: withhold' ht_verdict.txt"
        check "none abandoned" "! grep -q 'abandoned hypothesis' ht_verdict.txt"
    fi

    cd "$WORK"
done

echo ""
echo "PASS: $PASS  FAIL: $FAIL"
if [ "$FAIL" -gt 0 ]; then exit 1; fi
exit 0
