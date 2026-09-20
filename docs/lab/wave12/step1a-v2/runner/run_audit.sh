#!/bin/sh
# run_audit.sh — RUNAUDIT-2026-09-20-v1
# Deterministic shell glue for the RNGSCAN v2 audit (prereg §7.5).
# The Zag checker cannot spawn processes, so this runner:
#   1. runs the module binary twice with identical argv (state, input),
#      byte-comparing stdout (byte_identical),
#   2. runs it a third time with a different state file (must differ:
#      varies_with_state),
#   3. writes the replay evidence file (deterministic key=value lines),
#   4. invokes the Zag checker, which validates the evidence, performs the
#      source scan + object byte scan, and writes the attestation.
# No RNG anywhere. Deterministic given inputs.
# usage: run_audit.sh <checker-bin> <module.zag> <module-bin> <state> <input> <alt-state> <evidence> <attestation>
set -u
checker="$1"; module="$2"; modbin="$3"; state="$4"; input="$5"; altstate="$6"; evidence="$7"; att="$8"
work="$(mktemp -d)"
if command -v timeout >/dev/null 2>&1; then TO="timeout 120"; else TO=""; fi
$TO "$modbin" "$state" "$input" >"$work/out1.bin" 2>"$work/err1"; r1=$?
$TO "$modbin" "$state" "$input" >"$work/out2.bin" 2>"$work/err2"; r2=$?
$TO "$modbin" "$altstate" "$input" >"$work/out3.bin" 2>"$work/err3"; r3=$?
exit_ok=1
if [ "$r1" -ne 0 ] || [ "$r2" -ne 0 ] || [ "$r3" -ne 0 ]; then exit_ok=0; fi
byte_identical=0
if [ "$exit_ok" -eq 1 ] && cmp -s "$work/out1.bin" "$work/out2.bin"; then byte_identical=1; fi
varies=0
if [ "$exit_ok" -eq 1 ] && ! cmp -s "$work/out1.bin" "$work/out3.bin"; then varies=1; fi
state_words=$(($(wc -c <"$state") / 8))
{
  echo "byte_identical=$byte_identical"
  echo "varies_with_state=$varies"
  echo "state_words=$state_words"
  echo "runs=2"
  echo "exit_ok=$exit_ok"
} >"$evidence"
rm -f "$att"
"$checker" "$module" "$modbin" "$evidence" "$att"
rc=$?
rm -rf "$work"
exit "$rc"
