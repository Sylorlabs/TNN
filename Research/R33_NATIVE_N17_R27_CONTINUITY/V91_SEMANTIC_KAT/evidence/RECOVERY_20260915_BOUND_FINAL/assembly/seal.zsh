#!/bin/zsh
set -u
E=/tmp/r33_finish_recovery_20260915_b/v91/QUAL_20260915_BOUND_FINAL
A=/tmp/r33_finish_recovery_20260915_b/v91/assembly
function run {
 local label=$1 expected=$2 role=$3; shift 3
 printf '%s\n' "$@" > "$E/logs/$label.argv"
 "$@" > "$E/logs/$label.stdout" 2> "$E/logs/$label.stderr"
 local observed=$?; printf '%s\n' "$observed" > "$E/logs/$label.exit"
 printf '%s\t%s\t%s\t%s\n' "$label" "$observed" "$expected" "$role" >> "$E/commands.tsv"
 [[ $observed == $expected ]] || exit 80
}
run assembly_build_json_validator 0 native_evidence_validation_build /Users/Shared/micah/Documents/zag/znc "$A/json_validate.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$A/json_validate"
run assembly_json_validate 0 native_record_json_validation "$A/json_validate" "$E/RECORD.json"
printf '{' > "$A/invalid.json"
run assembly_json_negative 1 native_record_json_negative_validation "$A/json_validate" "$A/invalid.json"
run assembly_author_unchanged 0 final_author_source_identity shasum -a 256 -c /tmp/r33_finish_recovery_20260915_b/v91/AUTHOR_BOUND_FINAL.sha256
printf 'native_evidence_validator_source\t%s\n' "$A/json_validate.zag" >> "$E/files.tsv"
printf 'native_evidence_validator_binary\t%s\n' "$A/json_validate" >> "$E/files.tsv"
printf 'negative_evidence_json_fixture\t%s\n' "$A/invalid.json" >> "$E/files.tsv"
printf 'final_author_source_manifest\t%s\n' /tmp/r33_finish_recovery_20260915_b/v91/AUTHOR_BOUND_FINAL.sha256 >> "$E/files.tsv"
label=assembly_reseal_record
printf '%s\n' "$E/bin/record" "$E" "$E/files.tsv" > "$E/logs/$label.argv"
: > "$E/logs/$label.stdout"; : > "$E/logs/$label.stderr"
printf '%s\t0\t0\tnative_record_final_serialization\n' "$label" >> "$E/commands.tsv"
"$E/bin/record" "$E" "$E/files.tsv" > "$E/logs/$label.stdout" 2> "$E/logs/$label.stderr"
result=$?; printf '%s\n' "$result" > "$E/logs/$label.exit"; [[ $result == 0 ]] || exit 81
"$A/json_validate" "$E/RECORD.json" > "$A/final_validate.stdout" 2> "$A/final_validate.stderr"
printf '%s\n' "$?" > "$A/final_validate.exit"
[[ $(cat "$A/final_validate.exit") == 0 ]] || exit 82
cp "$E/RECORD.json" /tmp/r33_finish_recovery_20260915_b/v91/RECORD.json
