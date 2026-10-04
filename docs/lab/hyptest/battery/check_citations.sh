#!/bin/bash
# K10 citation verification for hyptest (Crew M).
# For each dev case, verifies that the union of citations across the linked
# hypothesis+prediction slots covers all 6 gold support episodes per hypothesis.
#
# usage: check_citations.sh <binary> <workdir>
set -e
BIN="$1"
WORK="$2"
if [ -z "$BIN" ] || [ -z "$WORK" ]; then echo "usage: check_citations.sh <binary> <workdir>"; exit 2; fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INPUTS="$SCRIPT_DIR/inputs"
GOLD="/home/hatch/workspace/hyptest/phenomena/dev/gold.tsv"

mkdir -p "$WORK"
PASS=0
FAIL=0

for CASE in dev01 dev02 dev03 devB1; do
    echo "=== $CASE ==="
    D="$WORK/$CASE"
    mkdir -p "$D"
    cd "$D"
    rm -f ht_state.bin
    "$BIN" init ht_state.bin >/dev/null
    "$BIN" teach ht_state.bin "$INPUTS/$CASE.teach.txt" >/dev/null
    "$BIN" hypothesize ht_state.bin "$INPUTS/$CASE.phenomenon.txt" >/dev/null

    # Get gold support episodes for this case
    # Gold columns: phenomenon_id, ..., winner, support_h_a, support_h_b
    # Support like "dev01.t.07;dev01.t.08;..." -> episode 7,8,...
    for H in hA hB; do
        if [ "$H" = "hA" ]; then COL=8; else COL=9; fi
        GOLD_SUPP=$(grep -P "^$CASE\t" "$GOLD" | cut -f$COL)
        # Convert dev01.t.07 -> 7 (episode = teach line number)
        GOLD_EPS=$(echo "$GOLD_SUPP" | tr ';' '\n' | sed 's/.*\.t\.0*//' | sort -n | tr '\n' ' ')
        echo "  $H gold support episodes: $GOLD_EPS"

        # Get actual citations from audit ledger (op 22 = st_evidence)
        # Slots: hA -> 0,1 ; hB -> 2,3 (from hypothesize order)
        if [ "$H" = "hA" ]; then SLOTS="0 1"; else SLOTS="2 3"; fi
        ACTUAL=""
        for S in $SLOTS; do
            EPS=$("$BIN" dump ht_state.bin 2>/dev/null | grep -a "op 22 slot $S " | sed 's/.*d2 //' | cut -d' ' -f1 | sort -n | tr '\n' ' ')
            ACTUAL="$ACTUAL $EPS"
        done
        ACTUAL_UNION=$(echo $ACTUAL | tr ' ' '\n' | sort -n -u | tr '\n' ' ')
        echo "  $H actual union: $ACTUAL_UNION"

        # Compare
        if [ "$GOLD_EPS" = "$ACTUAL_UNION " ] || [ "$GOLD_EPS " = "$ACTUAL_UNION" ]; then
            # normalize and compare
            G_NORM=$(echo $GOLD_EPS | tr ' ' '\n' | sort -n | tr '\n' ' ')
            A_NORM=$(echo $ACTUAL_UNION | tr ' ' '\n' | sort -n | tr '\n' ' ')
            if [ "$G_NORM" = "$A_NORM" ]; then
                echo "  PASS: $H citation recall 6/6"
                PASS=$((PASS+1))
            else
                echo "  FAIL: $H mismatch (gold: $G_NORM, actual: $A_NORM)"
                FAIL=$((FAIL+1))
            fi
        else
            G_NORM=$(echo $GOLD_EPS | tr ' ' '\n' | sort -n | tr '\n' ' ')
            A_NORM=$(echo $ACTUAL_UNION | tr ' ' '\n' | sort -n | tr '\n' ' ')
            if [ "$G_NORM" = "$A_NORM" ]; then
                echo "  PASS: $H citation recall 6/6"
                PASS=$((PASS+1))
            else
                echo "  FAIL: $H mismatch (gold: $G_NORM, actual: $A_NORM)"
                FAIL=$((FAIL+1))
            fi
        fi
    done
    cd "$WORK"
done

echo ""
echo "PASS: $PASS  FAIL: $FAIL"
if [ "$FAIL" -gt 0 ]; then exit 1; fi
exit 0
