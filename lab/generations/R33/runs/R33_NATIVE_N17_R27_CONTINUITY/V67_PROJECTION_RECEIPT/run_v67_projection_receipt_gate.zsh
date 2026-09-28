#!/bin/zsh
set -eu
ROOT=/Users/Shared/micah/Documents/TNN/TNN
COMP=/Users/Shared/micah/Documents/Zag/znc
EXPECTED=3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956
SRC=$ROOT/Research/R33_NATIVE_N17_R27_CONTINUITY/V67_PROJECTION_RECEIPT
BUILD=$SRC/BUILD_V67
mkdir -p "$BUILD"
actual=$(shasum -a 256 "$COMP" | awk '{print $1}')
[[ "$actual" == "$EXPECTED" ]] || exit 90
"$COMP" "$SRC/r27_projection_receipt_gate_v1_tests.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$BUILD/tests" >"$BUILD/compile.stdout" 2>"$BUILD/compile.stderr" || exit 91
"$BUILD/tests" >"$BUILD/run.stdout" 2>"$BUILD/run.stderr" || exit 92
grep -q '^R27_PROJECTION_RECEIPT_GATE_V1_FAILURES,0$' "$BUILD/run.stdout" || exit 93
grep -q '^R27_PROJECTION_RECEIPT_GATE_V67_OPEN_SURFACES,17$' "$BUILD/run.stdout" || exit 94
print -r -- 'status=PASS_FAIL_CLOSED_PROJECTION_LEDGER' > "$BUILD/BUILD_RECORD.txt"
print -r -- 'final_projection_receipt_digest=UNAVAILABLE' >> "$BUILD/BUILD_RECORD.txt"
print -r -- 'learn_authority=0' >> "$BUILD/BUILD_RECORD.txt"
