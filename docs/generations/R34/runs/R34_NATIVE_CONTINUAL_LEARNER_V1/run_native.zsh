#!/bin/zsh
set -u
BASE=${0:A:h}
COMP=/Users/Shared/micah/Documents/zag/znc
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
E="$BASE/EVIDENCE_$STAMP"
ROOT="$E/root"
BIN="$E/r34_learner"
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
shasum -a 256 "$BASE/r34_learner.zag" "$BASE/PREREGISTRATION.md" "$BASE/README.md" > "$E/source.sha256"
run compile "$COMP" "$BASE/r34_learner.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$BIN"
if [[ -x "$BIN" ]]; then
  shasum -a 256 "$BIN" > "$E/binary.sha256"
  run selftest "$BIN"
  run write "$BIN" write "$ROOT"
  run reload "$BIN" reload "$ROOT"
  run write_corrupt "$BIN" write-corrupt "$ROOT"
  run refuse_corrupt "$BIN" refuse-corrupt "$ROOT"
  run write_torn "$BIN" write-torn "$ROOT"
  run refuse_torn "$BIN" refuse-torn "$ROOT"
fi
print -r -- "failures=$fail" > "$E/RECEIPT.txt"
print -r -- "scientific_exposure=0" >> "$E/RECEIPT.txt"
print -r -- "canonical_r27_mutated=false" >> "$E/RECEIPT.txt"
print -r -- "learner_authority_granted=false" >> "$E/RECEIPT.txt"
(cd "$E"; find . -type f ! -name SHA256SUMS -print | LC_ALL=C sort | while IFS= read -r f; do shasum -a 256 "$f"; done) > "$E/SHA256SUMS"
print -r -- "$E"
exit $(( fail != 0 ))
