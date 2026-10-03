#!/bin/sh
# gen_hidden_inputs.sh - generate hidden test INPUTS for procedure-invention attacks.
# Part of frozen attack battery (PI_ADVERSARY_PREREG.md, attacks A2-A4).
# Usage: gen_hidden_inputs.sh <seed_u64> <count> <alphabet>
#   alphabet: ascii-lower | ascii-print | digits | symbols | unicode
# Output: one input string per line on stdout.
# Expected outputs are computed at reveal time by an independent reference
# implementation (never the Builder's code). The seed is published with the
# red-team report so anyone can regenerate these inputs and audit the test.
set -u

seed="$1"; count="$2"; alpha="$3"

# xorshift64 state in shell arithmetic (signed 64-bit wraparound is fine)
state="$seed"
xorshift() {
  # $1 = current state; echoes next state
  s="$1"
  s=$(( s ^ (s << 13) ))
  s=$(( s ^ (s >> 7) ))
  s=$(( s ^ (s << 17) ))
  echo "$s"
}

# alphabet definitions (no Python; pure shell)
alpha_chars() {
  case "$1" in
    ascii-lower) printf 'abcdefghijklmnopqrstuvwxyz' ;;
    digits)      printf '0123456789' ;;
    symbols)     printf '!@#$%%^&*()-_=+[]{};:,.<>?' ;;
    ascii-print) printf 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$\%%^&*()' ;;
    unicode)     printf 'a\xce\xb1\xe2\x82\xac\xc3\xa9\xe4\xb8\xad\xf0\x9f\x98\x80' ;;
  esac
}

chars="$(alpha_chars "$alpha")"
# count characters (bytes are fine for single-byte alphabets; unicode handled by byte slicing which may split codepoints - acceptable: tests robustness)
nchars=$(printf '%s' "$chars" | wc -c)

i=0
while [ "$i" -lt "$count" ]; do
  # length: 1 + (prng mod 20), plus forced edge cases appended by caller
  state=$(xorshift "$state")
  # make non-negative mod
  r=$(( state & 9223372036854775807 ))
  len=$(( 1 + r % 20 ))
  str=""
  j=0
  while [ "$j" -lt "$len" ]; do
    state=$(xorshift "$state")
    r=$(( state & 9223372036854775807 ))
    idx=$(( r % nchars ))
    # 0-based byte index into chars
    c=$(printf '%s' "$chars" | cut -c $(( idx + 1 )))
    str="${str}${c}"
    j=$(( j + 1 ))
  done
  printf '%s\n' "$str"
  i=$(( i + 1 ))
done
