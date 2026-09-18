#!/bin/zsh
set -eu
ROOT=${TNN_ROOT:-/Users/Shared/micah/Documents/TNN/TNN}
COMP=/Users/Shared/micah/Documents/zag/znc
if [[ ! -x "$COMP" ]]; then COMP=/Users/Shared/micah/Documents/Zag/znc; fi
EXPECTED=3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956
HERE=${0:A:h}
STAMP=$(date -u '+%Y%m%dT%H%M%SZ')
OUT=${TNN_R34_BEHAVIOR_EVIDENCE_ROOT:-$ROOT/Research/R34_BEHAVIORAL_HELDOUT_EVIDENCE}/$STAMP
mkdir -p "$OUT"
[[ -x "$COMP" ]] || { print -u2 -- "compiler missing: $COMP"; exit 90; }
[[ "$(shasum -a 256 "$COMP" | awk '{print $1}')" == "$EXPECTED" ]] || { print -u2 -- 'compiler hash mismatch'; exit 91; }
cp "$HERE"/*.zag "$OUT/"
cp "$HERE"/PREREGISTRATION*.md "$OUT/"
cp "$HERE"/R34_BEHAVIORAL_REFERENCE_V3.json "$OUT/" 2>/dev/null || true
FLAGS=(--target macos-arm64 --no-zagd --no-analyze --no-foreground-cache)
"$COMP" "$OUT/r34_behavioral_heldout_v3.zag" $FLAGS -o "$OUT/r34_behavioral_heldout_v3" >"$OUT/compile.stdout" 2>"$OUT/compile.stderr"
"$OUT/r34_behavioral_heldout_v3" >"$OUT/run1.stdout" 2>"$OUT/run1.stderr"
"$OUT/r34_behavioral_heldout_v3" >"$OUT/run2.stdout" 2>"$OUT/run2.stderr"
cmp -s "$OUT/run1.stdout" "$OUT/run2.stdout" || { print -u2 -- 'nondeterministic output'; exit 92; }
grep -Fqx 'R34_BEHAVIORAL_HELDOUT_V3_FAILURES,0' "$OUT/run1.stdout" || exit 93
grep -Fqx 'R34_BEHAVIORAL_HELDOUT_V3_PASS,1' "$OUT/run1.stdout" || exit 94
grep -Fqx 'R34_BEHAVIORAL_HELDOUT_V3_LEARN_AUTHORITY,0' "$OUT/run1.stdout" || exit 95
{
  print -- 'R34_BEHAVIORAL_HELDOUT_V3,NATIVE_PASS'
  print -- 'learn_authority=0'
  print -- 'phase6_self_modification=CLOSED'
  print -- "finished_utc=$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
} > "$OUT/RECEIPT.txt"
shasum -a 256 "$COMP" "$OUT"/*.zag "$OUT/r34_behavioral_heldout_v3" > "$OUT/SHA256SUMS"
print -- "$OUT"
