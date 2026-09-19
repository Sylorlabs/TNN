#!/bin/zsh
set -u
E=/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N17_R27_CONTINUITY/FINAL_B_20260915_1409/N17_REFRESH
label=log_hash_inventory
printf '%s\n' "$E/bin/candidates" "$E/inputs/log_inventory_paths.txt" > "$E/logs/$label.argv"
"$E/bin/candidates" "$E/inputs/log_inventory_paths.txt" > "$E/logs/$label.stdout" 2> "$E/logs/$label.stderr"
result=$?;printf '%s\n' "$result" > "$E/logs/$label.exit"
printf '%s\t%s\t0\tnative_operational_log_hash_inventory\n' "$label" "$result" >> "$E/commands.tsv"
[[ $result == 0 ]] || exit 71
printf 'native_log_byte_hash_inventory\t%s\n' "$E/logs/$label.stdout" >> "$E/files.tsv"
printf 'native_log_inventory_selector\t%s\n' "$E/inputs/log_inventory_paths.txt" >> "$E/files.tsv"
label=serialize_evidence
printf '%s\n' "$E/bin/evidence_record" "$E" "$E/files.tsv" > "$E/logs/$label.argv"
: > "$E/logs/$label.stdout";: > "$E/logs/$label.stderr"
printf '%s\t0\t0\tnative_evidence_serialization\n' "$label" >> "$E/commands.tsv"
"$E/bin/evidence_record" "$E" "$E/files.tsv" > "$E/logs/$label.stdout" 2> "$E/logs/$label.stderr"
result=$?;printf '%s\n' "$result" > "$E/logs/$label.exit"
[[ $result == 0 ]] || exit 72
