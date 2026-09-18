#!/bin/zsh
set -u
REPO=/Users/Shared/micah/Documents/TNN/TNN
N=$REPO/Research/R33_NATIVE_N17_R27_CONTINUITY
E=$N/FINAL_B_20260915_1409/N17_REFRESH
C=/Users/Shared/micah/Documents/zag/znc
P=$N/FINAL_B_20260915_1409/V91_REFRESH/bin/project
function run {
 local label=$1 expected=$2 role=$3
 shift 3
 printf '%s\n' "$@" > "$E/logs/$label.argv"
 "$@" > "$E/logs/$label.stdout" 2> "$E/logs/$label.stderr"
 local result=$?
 printf '%s\n' "$result" > "$E/logs/$label.exit"
 printf '%s\t%s\t%s\t%s\n' "$label" "$result" "$expected" "$role" >> "$E/receipt_commands.tsv"
 print "$label: $result expected $expected"
 [[ $result == $expected ]] || return 71
}
: > "$E/receipt_commands.tsv"
run classifier_final 0 native_row_classification "$E/bin/classifier" "$E" "$E/inputs/row_spec.tsv" "$E/ROW_CLASSIFICATIONS.json" || exit 71
run candidates_expanded_final 0 native_member_identity "$E/bin/candidates" "$E/inputs/candidates_expanded.txt" || exit 71
run receipt_canonical 0 preservation shasum -a 256 -c "$REPO/Research/R33_CLOSEOUT_20260915T174458Z/canonical.sha256" || exit 71
run receipt_protected 0 preservation shasum -a 256 -c "$REPO/Research/R33_CLOSEOUT_20260915T174458Z/protected.sha256" || exit 71
run receipt_compiler 0 preservation shasum -a 256 "$C" || exit 71
run receipt_compiler_compare 0 preservation cmp "$E/logs/compiler_before.stdout" "$E/logs/receipt_compiler.stdout" || exit 71
run project_record_final 0 native_projection "$P" "$E/sources/evidence_record.zag" "$E/projected/evidence_record.zag" "$E/projected/evidence_record.provenance" || exit 71
run build_record_final 0 native_build "$C" "$E/projected/evidence_record.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/evidence_record" || exit 71
