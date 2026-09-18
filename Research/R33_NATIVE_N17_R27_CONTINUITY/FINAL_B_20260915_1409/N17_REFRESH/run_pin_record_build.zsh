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
 printf '%s\t%s\t%s\t%s\n' "$label" "$result" "$expected" "$role" >> "$E/pin_commands.tsv"
 print "$label: $result expected $expected"
 [[ $result == $expected ]] || return 71
}
: > "$E/pin_commands.tsv"
run project_pinmatch 0 native_projection "$P" "$E/sources/match_inputs.zag" "$E/projected/match_inputs.zag" "$E/projected/match_inputs.provenance" || exit 71
run build_pinmatch 0 native_build "$C" "$E/projected/match_inputs.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/match_inputs" || exit 71
run pinmatch 0 native_input_admission "$E/bin/match_inputs" "$E/inputs/target_pins.tsv" "$E/logs/candidates_expanded_final.stdout" "$E/INPUT_ADMISSIONS.json" || exit 71
run project_record_corrected 0 native_projection "$P" "$E/sources/evidence_record.zag" "$E/projected/evidence_record_corrected.zag" "$E/projected/evidence_record_corrected.provenance" || exit 71
run build_record_corrected 0 native_build "$C" "$E/projected/evidence_record_corrected.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/evidence_record" || exit 71
