#!/bin/bash
# run_matrix.sh — M8 evidence matrix for B-T2 / B-T3 (crew B-ABLDOSE).
# Usage: run_matrix.sh <cfgname> <leg 0|1> <binary-path> <outdir> [done-marker]
# Skips any perturb whose .out already ends with the done-marker (resumable).
# Runs perturbations 0..4 plus a repeated perturbation-0 run, saves
# stdout/stderr per run, then verifies byte-identical outputs.
# Exit 0 iff all six runs byte-identical and every run exited 0.
set -u
CFG="$1"; LEG="$2"; BIN="$3"; OUTDIR="$4"; DONE_MARK="${5:-DONE}"
mkdir -p "$OUTDIR"
if [ ! -x "$BIN" ]; then echo "missing binary $BIN"; exit 3; fi

fail=0
for P in 0 1 2 3 4 0r; do
    OUT="$OUTDIR/${CFG}_leg${LEG}_p${P}.out"
    if [ -f "$OUT" ] && [ "$(tail -1 "$OUT" 2>/dev/null)" = "$DONE_MARK" ]; then
        echo "skip cfg=$CFG leg=$LEG perturb=$P (already complete)" >&2
        continue
    fi
    PA="$P"
    if [ "$P" = "0r" ]; then PA=0; fi
    OUT="$OUTDIR/${CFG}_leg${LEG}_p${P}.out"
    ERR="$OUTDIR/${CFG}_leg${LEG}_p${P}.err"
    "$BIN" "$LEG" "$PA" >"$OUT" 2>"$ERR"
    RC=$?
    echo "run cfg=$CFG leg=$LEG perturb=$P rc=$RC" >&2
    if [ $RC -ne 0 ]; then echo "FAIL rc=$RC cfg=$CFG leg=$LEG p=$P"; fail=1; fi
done

# byte-identical check across all six runs (stdout and stderr)
BASE="$OUTDIR/${CFG}_leg${LEG}_p0.out"
BASEE="$OUTDIR/${CFG}_leg${LEG}_p0.err"
for P in 1 2 3 4 0r; do
    if ! cmp -s "$BASE" "$OUTDIR/${CFG}_leg${LEG}_p${P}.out"; then
        echo "FAIL stdout differs: p0 vs p$P (cfg=$CFG leg=$LEG)"; fail=1
    fi
    if ! cmp -s "$BASEE" "$OUTDIR/${CFG}_leg${LEG}_p${P}.err"; then
        echo "FAIL stderr differs: p0 vs p$P (cfg=$CFG leg=$LEG)"; fail=1
    fi
done
if [ $fail -eq 0 ]; then echo "M8_IDENTICAL cfg=$CFG leg=$LEG runs=6"; fi
exit $fail
