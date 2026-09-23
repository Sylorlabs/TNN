#!/bin/sh
# m8_gate.sh — M8 determinism gate runner (prereg §6 / M-34..M-37, A-1).
# Usage: m8_gate.sh <binary> <config> [workdir]
#
# Runs the battery binary 5 times: run 1 clean (perturb 0), runs 2-5 with
# adversarial perturbations passed as argv[2]:
#   1 = heap pre-fragmentation, 2 = ASLR-equivalent base offset,
#   3 = entropy/clock canary, 4 = free-list order reversal.
# The binary must be built with m8_armor.zag and print capture lines:
#   M8_STORE_IMAGE,<hex>  M8_LEDGER,<hex>  M8_ALLOC_TRACE,<hex>
# PASS iff all 5 runs exit 0 AND normalized stdout is byte-identical AND
# stderr is byte-identical AND the three capture lines are identical across
# runs. Anything else = FAIL, fail-closed: the binary is DISQUALIFIED, numbers
# are forensics-only (M-37).
# A behavior change under the canary perturbation = FAIL even if the final
# outputs match (M-35).
set -u
BIN="$1"; CFG="$2"; WORK="${3:-/tmp/m8_gate_work}"
mkdir -p "$WORK" || exit 2

pass=1
ref_out=""; ref_err=""; ref_cap=""
i=0
while [ $i -lt 5 ]; do
  out="$WORK/run${i}.out"; err="$WORK/run${i}.err"
  "$BIN" "$CFG" "$i" >"$out" 2>"$err"
  rc=$?
  if [ $rc -ne 0 ]; then
    echo "M8_GATE,run=$i,exit=$rc,FAIL(nonzero-exit)"
    pass=0
  fi
  # stdout with the perturbation label stripped (it differs by construction)
  norm="$WORK/run${i}.norm"
  grep -v '^M8_PERTURB,' "$out" > "$norm"
  h=$(sha256sum "$norm" | cut -d' ' -f1)
  # stderr: hashed raw (no normalization — nothing in it differs by construction)
  eh=$(sha256sum "$err" | cut -d' ' -f1)
  # capture lines
  cap=$(grep -E '^M8_(STORE_IMAGE|LEDGER|ALLOC_TRACE),' "$out" | sort)
  ncap=$(printf '%s' "$cap" | grep -c .)
  if [ "$ncap" -ne 3 ]; then
    echo "M8_GATE,run=$i,FAIL(capture-lines=$ncap, want 3)"
    pass=0
  fi
  if [ $i -eq 0 ]; then
    ref_out="$h"; ref_err="$eh"; ref_cap="$cap"
  else
    if [ "$h" != "$ref_out" ]; then
      echo "M8_GATE,run=$i,FAIL(stdout-diverged-vs-run1)"
      pass=0
    fi
    if [ "$eh" != "$ref_err" ]; then
      echo "M8_GATE,run=$i,FAIL(stderr-diverged-vs-run1)"
      pass=0
    fi
    if [ "$cap" != "$ref_cap" ]; then
      echo "M8_GATE,run=$i,FAIL(captures-diverged-vs-run1)"
      pass=0
    fi
  fi
  i=$((i+1))
done

if [ $pass -eq 1 ]; then
  echo "M8_GATE,PASS,binary=$BIN,config=$CFG,runs=5"
  printf '{"m8_gate":"PASS","binary":"%s","config":"%s","runs":5}\n' "$BIN" "$CFG"
  exit 0
else
  echo "M8_GATE,FAIL — DISQUALIFIED,binary=$BIN,config=$CFG"
  printf '{"m8_gate":"FAIL — DISQUALIFIED","binary":"%s","config":"%s","runs":5}\n' "$BIN" "$CFG"
  exit 1
fi
