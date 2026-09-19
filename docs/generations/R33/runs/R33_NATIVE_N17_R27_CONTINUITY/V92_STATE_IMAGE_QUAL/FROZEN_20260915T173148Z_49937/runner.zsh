#!/bin/zsh
set -eu
ROOT=/Users/Shared/micah/Documents/TNN/TNN
COMP=/Users/Shared/micah/Documents/zag/znc
HERE=$ROOT/Research/R33_NATIVE_N17_R27_CONTINUITY/V92_STATE_IMAGE_QUAL
EVIDENCE=$HERE/FROZEN_$(date -u +%Y%m%dT%H%M%SZ)_$$
mkdir "$EVIDENCE"
mkdir "$EVIDENCE/sources" "$EVIDENCE/runtime"
cd "$ROOT"
cp "$COMP" "$EVIDENCE/compiler.znc"
cp "$HERE/run_v92_state_image_qual.zsh" "$EVIDENCE/runner.zsh"
freeze_source() {
  local source_path=$1 relative=${1#$ROOT/} imported resolved
  [[ -f "$EVIDENCE/sources/$relative" ]] && return 0
  mkdir -p "$EVIDENCE/sources/${relative:h}"
  cp "$source_path" "$EVIDENCE/sources/$relative"
  while IFS= read -r imported; do
    resolved=$(realpath "${source_path:h}/$imported")
    [[ "$resolved" == "$ROOT/"* ]] || return 1
    freeze_source "$resolved"
  done < <(sed -n 's/^@import("\([^"]*\)").*/\1/p' "$source_path")
}
freeze_source "$HERE/state_image_qual_v92.zag"
SOURCE=$EVIDENCE/sources/Research/R33_NATIVE_N17_R27_CONTINUITY/V92_STATE_IMAGE_QUAL/state_image_qual_v92.zag
BIN=$EVIDENCE/state_image_qual_v92
typeset -i failures=0
run_check() {
  local label=$1
  shift
  print -r -- "cwd=$ROOT" >> "$EVIDENCE/commands.txt"
  print -r -- "${(q)@} > ${(q)EVIDENCE}/$label.stdout 2> ${(q)EVIDENCE}/$label.stderr" >> "$EVIDENCE/commands.txt"
  local rc=0
  "$@" > "$EVIDENCE/$label.stdout" 2> "$EVIDENCE/$label.stderr" || rc=$?
  print -r -- "$label,$rc" >> "$EVIDENCE/exit_codes.csv"
  (( rc == 0 )) || failures=$((failures+1))
  return 0
}
shasum -a 256 "$COMP" > "$EVIDENCE/compiler.before.sha256"
run_check compile "$COMP" "$SOURCE" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$BIN"
if [[ -x "$BIN" ]]; then
  for mode in selftest write read write-corrupt read-corrupt write-truncated read-truncated write-packet read-packet write-packet-corrupt read-packet-corrupt write-packet-truncated read-packet-truncated; do
    run_check "$mode" "$BIN" "$mode" "$EVIDENCE/runtime"
  done
else
  failures=$((failures+1))
fi
shasum -a 256 "$COMP" > "$EVIDENCE/compiler.after.sha256"
run_check compiler_unchanged cmp "$EVIDENCE/compiler.before.sha256" "$EVIDENCE/compiler.after.sha256"
if [[ -f "$EVIDENCE/runtime/learner-packet.bin" ]]; then
  wc -c "$EVIDENCE"/runtime/*.bin > "$EVIDENCE/fixture_bytes.txt"
fi
print -r -- "qualification_failures,$failures" > "$EVIDENCE/receipt.txt"
print -r -- "EVIDENCE=$EVIDENCE"
print -r -- "qualification_failures=$failures"
(cd "$EVIDENCE"; find . -type f ! -name SHA256SUMS -print | LC_ALL=C sort | while IFS= read -r item; do shasum -a 256 "$item"; done) > "$EVIDENCE/SHA256SUMS"
(( failures == 0 ))
