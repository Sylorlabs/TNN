#!/bin/bash
# J1 M8 gate runner — 5 perturbations, byte-identical check
set -e
J1=~/workspace/tnn-lab/units/arms/J1/work/j1
CORPORA=~/workspace/tnn-lab/units/arms/harness/corpora/r1
WORK=~/workspace/tnn-lab/units/arms/J1/work/battery/r1_1x/m8

mkdir -p "$WORK"
echo "=== M8 gate: 5 perturbations ===" | tee "$WORK/GATE.txt"

for pert in clean frag aslr starve freelist; do
    echo "--- pert: $pert ---" | tee -a "$WORK/GATE.txt"
    outdir="$WORK/$pert"
    mkdir -p "$outdir"
    # Run twice for byte-identical check
    timeout 1800 $J1 m8-1x "$CORPORA" "$outdir/run1" "$pert" > "$outdir/run1.log" 2>&1
    rc1=$?
    timeout 1800 $J1 m8-1x "$CORPORA" "$outdir/run2" "$pert" > "$outdir/run2.log" 2>&1
    rc2=$?
    if [ $rc1 -ne 0 ] || [ $rc2 -ne 0 ]; then
        echo "PERT $pert FAILED: rc1=$rc1 rc2=$rc2" | tee -a "$WORK/GATE.txt"
        echo "M8-GATE-FAIL" >> "$WORK/GATE.txt"
        exit 1
    fi
    # Compare artifacts (store_hashes.txt, store_chain.txt, ledger_chain.txt)
    for f in store_hashes.txt store_chain.txt ledger_chain.txt; do
        if ! diff -q "$outdir/run1/$f" "$outdir/run2/$f" > /dev/null 2>&1; then
            echo "PERT $pert: $f DIFFERS between runs" | tee -a "$WORK/GATE.txt"
            echo "M8-GATE-FAIL" >> "$WORK/GATE.txt"
            exit 1
        fi
    done
    echo "PERT $pert: byte-identical PASS" | tee -a "$WORK/GATE.txt"
done

# Cross-perturbation: all should be identical (determinism across perturbations)
# Compare clean/run1 vs others/run1
for pert in frag aslr starve freelist; do
    for f in store_hashes.txt store_chain.txt ledger_chain.txt; do
        if ! diff -q "$WORK/clean/run1/$f" "$WORK/$pert/run1/$f" > /dev/null 2>&1; then
            echo "CROSS-PERT: $pert/$f differs from clean" | tee -a "$WORK/GATE.txt"
            echo "M8-GATE-FAIL" >> "$WORK/GATE.txt"
            exit 1
        fi
    done
done

echo "M8-GATE-PASS" | tee -a "$WORK/GATE.txt"
