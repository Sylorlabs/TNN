#!/bin/bash
# Wave 9 trust-tiers native Zag trial — matrix runner.
# One binary; argv[1] alone selects the cell: {T,N,B}_{A0..A6,N0}_{0,1,2}_{00..11}_{0,1}_{1,10}
#   T = tiered arm, N = T-NC (no-collusion ablation), B = baseline control
#   Example: T_A1_0_00_0_1
#
# Modes:
#   ./run_matrix.sh smoke   — required smoke only (A1/v0/inst0/runs 0,1, T/N/B), paired diffs
#   ./run_matrix.sh full    — full matrix (NOT run automatically; requires explicit opt-in)
#   ./run_matrix.sh purity  — Arm-B tier-purity textual check
#
# Static gates (fail fast):
#   - binary exists and is executable
#   - invalid selectors return 65 (not 0, no stdout)
#   - Arm-B region contains no "tier" (case-insensitive) outside its banner comment

set -e
SUBSTRATE="$(cd "$(dirname "$0")" && pwd)"
BIN="$SUBSTRATE/trust_tiers.bin"
SRC="$SUBSTRATE/trust_tiers.zag"

die(){ echo "GATE FAIL: $1" >&2; exit 1; }

# --- static gate: binary exists ---
[ -x "$BIN" ] || die "binary not found/executable: $BIN"

# --- static gate: invalid selectors rejected with 65 ---
for bad in "" "X_A1_0_00_0_1" "T_A1_0_00_0_2" "T_A1_0_00_0_1_EXTRA" "T_Z9_0_00_0_1" "T_A1_0_12_0_1"; do
    if [ -z "$bad" ]; then
        "$BIN" >/dev/null 2>&1 || rc=$?
        [ $rc -eq 64 ] || die "empty argv[1] should return 64, got $rc"
    else
        out=$("$BIN" "$bad" 2>&1) || rc=$?
        [ $rc -eq 65 ] || die "selector '$bad' should return 65, got $rc (out: $out)"
        [ -z "$out" ] || die "selector '$bad' should emit no stdout on reject"
    fi
done
echo "gate: invalid selectors rejected OK"

# --- static gate: Arm-B region tier-purity ---
# The B decision path (between TT-B-GATE-BEGIN and TT-B-GATE-END) must not
# read per-source rank. We check textually: no "tier" (any case) in the region,
# excluding the banner comment lines that describe the requirement itself.
if [ -f "$SRC" ]; then
    bregion=$(awk '/TT-B-GATE-BEGIN/{f=1;next}/TT-B-GATE-END/{f=0}f' "$SRC")
    # strip banner comment lines (starting with //) then search
    hits=$(echo "$bregion" | grep -v '^\s*//' | grep -i "tier" || true)
    [ -z "$hits" ] || die "Arm-B region mentions tier: $hits"
    echo "gate: Arm-B tier-purity OK"
fi

mode="${1:-smoke}"

run_cell(){
    local sel="$1" out="$2"
    "$BIN" "$sel" > "$out" 2>&1 || die "cell $sel exited $?"
}

if [ "$mode" = "purity" ]; then
    echo "purity gates passed"
    exit 0
fi

if [ "$mode" = "smoke" ]; then
    echo "== smoke: A1/v0/inst0, runs 0+1, arms T/N/B =="
    for arm in T N B; do
        run_cell "${arm}_A1_0_00_0_1" "/tmp/tt_smoke_${arm}_0.out"
        run_cell "${arm}_A1_0_00_1_1" "/tmp/tt_smoke_${arm}_1.out"
        if diff -q "/tmp/tt_smoke_${arm}_0.out" "/tmp/tt_smoke_${arm}_1.out" >/dev/null; then
            echo "PASS $arm paired stdout byte-identical"
        else
            die "$arm paired runs differ"
        fi
    done
    echo "smoke: all 3 arms paired-identical"
    exit 0
fi

if [ "$mode" = "full" ]; then
    echo "full matrix requested."
    echo "This runs 8 campaigns x 3 variants x 12 instances x 2 runs x 3 arms (S1) = 1728 cells."
    read -p "Type RUN-FULL to proceed: " ans
    [ "$ans" = "RUN-FULL" ] || die "aborted (full matrix needs explicit RUN-FULL)"
    mkdir -p "$SUBSTRATE/out_full"
    for arm in T N B; do
        for camp in A0 A1 A2 A3 A4 A5 A6 N0; do
            for var in 0 1 2; do
                for inst in 00 01 02 03 04 05 06 07 08 09 10 11; do
                    # A0 is arm-T only
                    if [ "$camp" = "A0" ] && [ "$arm" != "T" ]; then continue; fi
                    for run in 0 1; do
                        sel="${arm}_${camp}_${var}_${inst}_${run}_1"
                        out="$SUBSTRATE/out_full/${sel}.out"
                        run_cell "$sel" "$out"
                    done
                    # paired determinism check per cell
                    s0="$SUBSTRATE/out_full/${arm}_${camp}_${var}_${inst}_0_1.out"
                    s1="$SUBSTRATE/out_full/${arm}_${camp}_${var}_${inst}_1_1.out"
                    diff -q "$s0" "$s1" >/dev/null || die "nondeterminism: ${arm}_${camp}_${var}_${inst}"
                done
            done
        done
    done
    echo "full matrix complete; all paired runs byte-identical"
    exit 0
fi

die "unknown mode: $mode (use smoke|full|purity)"
