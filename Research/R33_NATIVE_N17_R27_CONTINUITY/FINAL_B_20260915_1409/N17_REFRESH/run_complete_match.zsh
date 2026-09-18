#!/bin/zsh
E=/Users/Shared/micah/Documents/TNN/TNN/Research/R33_NATIVE_N17_R27_CONTINUITY/FINAL_B_20260915_1409/N17_REFRESH
label=complete_pinmatch
printf '%s\n' "$E/bin/match_inputs" "$E/inputs/target_pins_deep.tsv" "$E/inputs/deep_complete_hashes.tsv" "$E/INPUT_ADMISSIONS_DEEP.json" > "$E/logs/$label.argv"
"$E/bin/match_inputs" "$E/inputs/target_pins_deep.tsv" "$E/inputs/deep_complete_hashes.tsv" "$E/INPUT_ADMISSIONS_DEEP.json" > "$E/logs/$label.stdout" 2> "$E/logs/$label.stderr"
result=$?; printf '%s\n' "$result" > "$E/logs/$label.exit"
printf '%s\t%s\t0\tnative_complete_input_pin_comparison\n' "$label" "$result" > "$E/complete_commands.tsv"
exit "$result"
