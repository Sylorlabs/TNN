#!/bin/bash
# no_rng_check.sh — K2: static zero-RNG audit over the W1 Zag sources.
# Fails if any randomness/clock/entropy token appears in impl/*.zag or
# impl/substrate (vendored substrate included — it must be clean too).
# Usage: no_rng_check.sh <impl-dir>
set -u
IMPL="${1:?usage: no_rng_check.sh <impl-dir>}"
PAT='rand|srand|random|urandom|getentropy|getrandom|rdtsc|clock_gettime|gettimeofday|time\(|nanosleep|usleep'
hits=$(grep -rEin "$PAT" "$IMPL" --include='*.zag' || true)
if [ -n "$hits" ]; then
  echo "K2_RNG_HIT_FAIL"
  echo "$hits"
  exit 20
fi
echo "K2_ZERO_RNG_PASS"
