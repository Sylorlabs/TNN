#!/bin/zsh
set -eu
ROOT=/Users/Shared/micah/Documents/TNN/TNN
DIR=$ROOT/Research/R33_NATIVE_PURITY_V1
COMP=/Users/Shared/micah/Documents/Zag/znc
BUILD=$DIR/BUILD_V1
mkdir -p "$BUILD"
"$COMP" "$DIR/purity_gate_tests.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$BUILD/purity-tests"
"$BUILD/purity-tests" "$DIR"
"$COMP" "$DIR/purity_gate.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$BUILD/purity-gate"
"$BUILD/purity-gate" "$ROOT"

