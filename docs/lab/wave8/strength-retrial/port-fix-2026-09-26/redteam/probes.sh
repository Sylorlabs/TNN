#!/bin/bash
# probes.sh — focused regression probes for the two red-team fixes.
# Usage: probes.sh <rt_bin> <out>
# Each probe prints PASS/FAIL with expected rc sequences.
set -u
BIN="$1"; OUT="$2"
: > "$OUT"
pass=0; fail=0
probe() {
    local name="$1"; local expected="$2"; shift 2
    local got
    got=$("$BIN" "$@" 2>&1 | grep "^RT " | awk '{print $4}' | tr '\n' ' ' | sed 's/ $//')
    if [ "$got" = "$expected" ]; then
        echo "PASS $name" >> "$OUT"; pass=$((pass+1))
    else
        echo "FAIL $name: got [$got] want [$expected]" >> "$OUT"; fail=$((fail+1))
    fi
}
# F1: 64-bit episode identity
probe f1_alias_lo_hi "0 0 0" G ADD90 CITE0 CITE4294967296
probe f1_dup64 "0 0 111" G ADD90 CITE4294967296 CITE4294967296
probe f1_bit31a "0 0" G ADD90 CITE2147483648
probe f1_bit31b "0 0" G ADD90 CITE4294967295
probe f1_2p33 "0 0 0" G ADD90 CITE4294967296 CITE8589934592
probe f1_maxvalid "0 0" G ADD90 CITE36028797018963967
probe f1_overmax "0 2001" G ADD90 CITE36028797018963968
probe f1_xslot_nospend "0 0 0 0 0 0 0 0 0 0 0 0" G ADD90 CITE4294967296 CITE4294967297 CITE4294967298 CITE4294967299 JUST KILL ADD90 CITE0 CITE1 CITE2 CITE3
probe f1_xslot_spent121 "0 0 0 0 0 0 0 0 0 0 0 0 0 121" G ADD90 CITE4294967296 CITE4294967297 CITE4294967298 CITE4294967299 JUST KILL ADD90 CITE4294967296 CITE4294967297 CITE4294967298 CITE4294967299 JUST KILL
# F2: over-cite refusal
probe f2_kill "0 0 0 0 0 122 0 0" G ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 JUST KILL
probe f2_del "0 0 0 0 0 122 0 0" G ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 JUST DEL
probe f2_killt "0 0 0 0 0 122 0 0" G ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 JUST KILLT
probe f2_ow "0 0 0 0 0 122 0 0" G ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 JUST OW95
probe f2_rb "0 0 0 0 0 122 108 0 0" G ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 RB JUST KILL
probe f2_reopen "0 0 0 0 0 122 0 0" G ADD90 CITE0 CITE1 CITE2 CITE3 CITE4 STR95 CITE4
probe f2_spentfresh "0 0 0 0 0 0 0 0 0 0 122 0 0" G ADD90 CITE0 CITE1 CITE2 CITE3 STR95 CITE4 CITE5 CITE6 CITE7 CITE8 JUST KILL
# pre-existing shapes unchanged
probe base_4cite_kill "0 0 0 0 0 0 0" G ADD90 CITE0 CITE1 CITE2 CITE3 JUST KILL
echo "probes pass=$pass fail=$fail" >> "$OUT"
echo "pass=$pass fail=$fail"
