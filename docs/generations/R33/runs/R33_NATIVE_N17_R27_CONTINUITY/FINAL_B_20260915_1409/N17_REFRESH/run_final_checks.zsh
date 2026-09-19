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
 printf '%s\t%s\t%s\t%s\n' "$label" "$result" "$expected" "$role" >> "$E/final_commands.tsv"
 print "$label: $result expected $expected"
 [[ $result == $expected ]] || return 71
}
function build {
 local label=$1 source=$2
 run project_$label 0 native_import_projection "$P" "$source" "$E/projected/$label.zag" "$E/projected/$label.provenance" || return 71
 run build_$label 0 native_build "$C" "$E/projected/$label.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/$label"
}
: > "$E/final_commands.tsv"
build policy_final "$E/sources/policy_native.zag" || exit 71
run policy_final 0 native_policy_and_negatives "$E/bin/policy_final" "$E/inputs/r27-policy.json" || exit 71
run policy_missing_final 66 native_missing_refusal "$E/bin/policy_final" "$E/inputs/absent-policy.json" || exit 71
run corrupt_policy_setup_final 0 fixture_setup dd if=/dev/zero of="$E/inputs/corrupt-policy.json" bs=1 count=8 || exit 71
run policy_corrupt_final 71 native_hash_refusal "$E/bin/policy_final" "$E/inputs/corrupt-policy.json" || exit 71
build classifier "$E/sources/classify_rows.zag" || exit 71
run classifier 0 native_80_row_classification "$E/bin/classifier" "$E" "$E/inputs/row_spec.tsv" "$E/ROW_CLASSIFICATIONS.json" || exit 71
run candidates_expanded 0 native_expanded_member_identity "$E/bin/candidates" "$E/inputs/candidates_expanded.txt" || exit 71
run final_canonical 0 preservation shasum -a 256 -c "$REPO/Research/R33_CLOSEOUT_20260915T174458Z/canonical.sha256" || exit 71
run final_protected 0 preservation shasum -a 256 -c "$REPO/Research/R33_CLOSEOUT_20260915T174458Z/protected.sha256" || exit 71
run final_compiler 0 preservation shasum -a 256 "$C" || exit 71
run final_compiler_compare 0 preservation cmp "$E/logs/compiler_before.stdout" "$E/logs/final_compiler.stdout" || exit 71
