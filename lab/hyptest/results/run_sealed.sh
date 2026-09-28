#!/bin/bash
# Sealed battery driver for hyptest (coordinator-run).
# Runs the 6 sealed phenomena through the full loop. No gold consulted here;
# scoring happens separately against the broker-held gold.
# usage: run_sealed.sh <binary> <inputs_dir> <workdir>
set -u
BIN="$1"; INPUTS="$2"; WORK="$3"
BIN="$(cd "$(dirname "$BIN")" && pwd)/$(basename "$BIN")"
INPUTS="$(cd "$INPUTS" && pwd)"
mkdir -p "$WORK"; WORK="$(cd "$WORK" && pwd)"
for CASE in seal01 seal02 seal03 seal04 sealB1 sealB2; do
    D="$WORK/$CASE"; mkdir -p "$D"; cd "$D"
    rm -f ht_state.bin ht_hypotheses.txt ht_verdict.txt
    "$BIN" init ht_state.bin > init.log 2>&1
    "$BIN" teach ht_state.bin "$INPUTS/$CASE.teach.txt" > teach.log 2>&1
    "$BIN" hypothesize ht_state.bin "$INPUTS/$CASE.phenomenon.txt" > hyp.log 2>&1
    grep -o 'audit_n [0-9]*' hyp.log | head -1 | cut -d' ' -f2 > pre_test_audit.txt
    "$BIN" observe ht_state.bin "$INPUTS/$CASE.test.txt" > obs.log 2>&1
    grep -o 'audit_n [0-9]*' obs.log | head -1 | cut -d' ' -f2 > obs_audit.txt
    "$BIN" adjudicate ht_state.bin > adj.log 2>&1
    "$BIN" dump ht_state.bin > dump.log 2>&1
    sha256sum ht_state.bin ht_hypotheses.txt ht_verdict.txt > sha.txt
    cd "$WORK"
done
echo "sealed run complete: $WORK"
