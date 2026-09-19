#!/bin/zsh
set -eu
ROOT=/Users/Shared/micah/Documents/TNN/TNN
DIR=$ROOT/Research/R33_CONTINUING_LIFE_V1
COMP=/Users/Shared/micah/Documents/Zag/znc
EXPECTED=3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956
BUILD=$DIR/BUILD_V68_OUTER_LEARNER_PACKET
mkdir -p "$BUILD"
actual=$(shasum -a 256 "$COMP" | awk '{print $1}')
[[ "$actual" == "$EXPECTED" ]] || { print -r -- "status=REFUSED_COMPILER_IDENTITY" > "$BUILD/BUILD_RECORD.txt"; exit 90; }
"$COMP" "$DIR/outer_learner_packet_bridge_v68_tests.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$BUILD/tests" >"$BUILD/compile.stdout" 2>"$BUILD/compile.stderr" || exit 91
"$BUILD/tests" >"$BUILD/run.stdout" 2>"$BUILD/run.stderr" || exit 92
grep -q '^CL_V68_FAILURES,0$' "$BUILD/run.stdout" || exit 93
{
  print -r -- "status=PASS_OUTER_ATOMIC_LEARNER_PACKET_TRANSPORT"
  print -r -- "learner_packet_bytes=245536"
  print -r -- "learn_authority=0"
  print -r -- "parent_admission=pending"
  print -r -- "canonical_r27_touched=false"
  print -r -- "scientific_exposure=0"
} > "$BUILD/BUILD_RECORD.txt"
shasum -a 256 "$DIR/checkpoint.zag" "$DIR/outer_learner_packet_bridge_v68_tests.zag" "$BUILD/tests" "$BUILD/run.stdout" > "$BUILD/MANIFEST.sha256"
cat "$BUILD/run.stdout"
