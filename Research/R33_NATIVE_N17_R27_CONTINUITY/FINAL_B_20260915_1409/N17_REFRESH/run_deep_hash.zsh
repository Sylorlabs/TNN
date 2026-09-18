#!/bin/zsh
set -u
E=/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N17_R27_CONTINUITY/FINAL_B_20260915_1409/N17_REFRESH
function run {
 local label=$1 expected=$2 role=$3
 shift 3
 printf '%s\n' "$@" > "$E/logs/$label.argv"
 "$@" > "$E/logs/$label.stdout" 2> "$E/logs/$label.stderr"
 local result=$?
 printf '%s\n' "$result" > "$E/logs/$label.exit"
 printf '%s\t%s\t%s\t%s\n' "$label" "$result" "$expected" "$role" >> "$E/deep_commands.tsv"
 print "$label: $result expected $expected"
 [[ $result == $expected ]] || return 71
}
: > "$E/deep_commands.tsv"
run deep_candidate_hashes 0 native_exact_input_hashes "$E/bin/candidates" "$E/inputs/candidates_deep.txt" || exit 71
run deep_pinmatch 0 native_exact_pin_comparison "$E/bin/match_inputs" "$E/inputs/target_pins_deep.tsv" "$E/logs/deep_candidate_hashes.stdout" "$E/INPUT_ADMISSIONS_DEEP.json" || exit 71
