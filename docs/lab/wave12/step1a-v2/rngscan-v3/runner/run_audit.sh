#!/bin/sh
# run_audit.sh — RUNAUDIT-2026-09-20-v2
# Deterministic shell glue for the RNGSCAN v3 audit (prereg §7.6).
# The Zag checker cannot spawn processes, so this runner:
#   1. runs the module binary 8 times with identical logical inputs across
#      4 argv/env layout variants (L0 normal, L1 empty env, L2 long argv[0],
#      L3 8KB-padded env), 2 runs per layout; all 8 outputs byte-compared
#      (byte_identical),
#   2. runs it once more with a different state file (must differ:
#      varies_with_state),
#   3. writes the replay evidence file (deterministic key=value lines),
#   4. invokes the Zag checker, which validates the evidence, performs the
#      source scan + object byte scan + vendored hash verification, and
#      writes the attestation.
# No RNG anywhere. Deterministic given inputs.
# usage: run_audit.sh <checker-bin> <module.zag> <module-bin> <state> <input> <alt-state> <evidence> <attestation>
set -u
checker="$1"; module="$2"; modbin="$3"; state="$4"; input="$5"; altstate="$6"; evidence="$7"; att="$8"
work="$(mktemp -d)"
if command -v timeout >/dev/null 2>&1; then TO="timeout 120"; else TO=""; fi
LONGNAME="$(printf 'A%.0s' $(seq 1 256))"
PAD8K="$(printf 'P%.0s' $(seq 1 8192))"
exit_ok=1
run_layout() {
  layout="$1"; n="$2"
  case "$layout" in
    0) $TO "$modbin" "$state" "$input" >"$work/out$n.bin" 2>"$work/err$n" ;;
    1) $TO env -i "$modbin" "$state" "$input" >"$work/out$n.bin" 2>"$work/err$n" ;;
    2) $TO bash -c 'exec -a "$0" "$1" "$2" "$3"' "$LONGNAME" "$modbin" "$state" "$input" >"$work/out$n.bin" 2>"$work/err$n" ;;
    3) $TO env "RNGSCAN_PAD=$PAD8K" "$modbin" "$state" "$input" >"$work/out$n.bin" 2>"$work/err$n" ;;
  esac
  if [ $? -ne 0 ]; then exit_ok=0; fi
}
n=1
for layout in 0 1 2 3; do
  run_layout "$layout" "$n"; n=$((n+1))
  run_layout "$layout" "$n"; n=$((n+1))
done
$TO "$modbin" "$altstate" "$input" >"$work/out_alt.bin" 2>"$work/err_alt"
if [ $? -ne 0 ]; then exit_ok=0; fi
byte_identical=0
if [ "$exit_ok" -eq 1 ]; then
  byte_identical=1
  i=2
  while [ "$i" -le 8 ]; do
    if ! cmp -s "$work/out1.bin" "$work/out$i.bin"; then byte_identical=0; fi
    i=$((i+1))
  done
fi
varies=0
if [ "$exit_ok" -eq 1 ] && ! cmp -s "$work/out1.bin" "$work/out_alt.bin"; then varies=1; fi
state_words=$(($(wc -c <"$state") / 8))
{
  echo "byte_identical=$byte_identical"
  echo "varies_with_state=$varies"
  echo "state_words=$state_words"
  echo "runs=8"
  echo "exit_ok=$exit_ok"
  echo "layouts=4"
} >"$evidence"
rm -f "$att"
"$checker" "$module" "$modbin" "$evidence" "$att"
rc=$?
rm -rf "$work"
exit "$rc"
