#!/bin/zsh
set -u
BASE=${0:A:h}
COMP=/Users/Shared/micah/Documents/zag/znc
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
ROOT="$E/root"
BIN="$E/r34_v2"
mkdir -p "$E" "$ROOT"
chmod 700 "$ROOT"
fail=0
run() {
  local label=$1
  shift
  print -r -- "$*" > "$E/$label.command"
  "$@" > "$E/$label.stdout" 2> "$E/$label.stderr"
  local ec=$?
  print -r -- "$ec" > "$E/$label.exit"
  if (( ec != 0 )); then fail=$((fail+1)); fi
}
shasum -a 256 "$COMP" > "$E/compiler.sha256"
shasum -a 256 "$BASE/r34_continuing_learner_v2.zag" "$BASE/PREREGISTRATION.md" "$BASE/README.md" > "$E/source.sha256"
run compile "$COMP" "$BASE/r34_continuing_learner_v2.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$BIN"
if [[ -x "$BIN" ]]; then
  shasum -a 256 "$BIN" > "$E/binary.sha256"
  run campaign "$BIN"
  run reference_mid "$BIN" reference-mid
  run write_mid "$BIN" write-mid "$ROOT"
  run reload_mid "$BIN" reload-mid "$ROOT"
  if ! cmp -s "$E/reference_mid.stdout" "$E/reload_mid.stdout"; then
    print -r -- "fresh_process_continuation_mismatch" > "$E/continuation.diff"
    diff -u "$E/reference_mid.stdout" "$E/reload_mid.stdout" >> "$E/continuation.diff" 2>&1
    fail=$((fail+1))
  else
    print -r -- "exact_match=true" > "$E/continuation.diff"
  fi
  run write_inner_corrupt "$BIN" write-inner-corrupt "$ROOT"
  run refuse_inner_corrupt "$BIN" refuse-inner-corrupt "$ROOT"
  run write_torn "$BIN" write-torn "$ROOT"
  run refuse_torn "$BIN" refuse-torn "$ROOT"
fi
print -r -- "failures=$fail" > "$E/RECEIPT.txt"
print -r -- "scientific_exposure=0" >> "$E/RECEIPT.txt"
print -r -- "canonical_r27_mutated=false" >> "$E/RECEIPT.txt"
print -r -- "learner_authority_granted=false" >> "$E/RECEIPT.txt"
print -r -- "learn_opened=false" >> "$E/RECEIPT.txt"
print -r -- "foreign_ml_runtime_used=false" >> "$E/RECEIPT.txt"
(cd "$E"; find . -type f ! -name SHA256SUMS -print | LC_ALL=C sort | while IFS= read -r f; do shasum -a 256 "$f"; done) > "$E/SHA256SUMS"
print -r -- "$E"
exit $(( fail != 0 ))
