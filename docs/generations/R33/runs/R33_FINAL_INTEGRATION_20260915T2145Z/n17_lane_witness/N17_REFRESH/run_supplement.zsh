#!/bin/zsh
set -u
REPO=/Users/Shared/micah/Documents/TNN/TNN
N=$REPO/Research/R33_NATIVE_N17_R27_CONTINUITY
E=$N/FINAL_B_20260915_1409/N17_REFRESH
C=/Users/Shared/micah/Documents/zag/znc
P=$N/FINAL_B_20260915_1409/V91_REFRESH/bin/project
S=$N/RECOVERY_20260915_B_INDEPENDENT/TERMINAL_SUPPLEMENT_20260915/COMPATIBILITY_CORRECTION_20260915/sources/N17
function run {
 local label=$1 expected=$2 role=$3
 shift 3
 printf '%s\n' "$@" > "$E/logs/$label.argv"
 "$@" > "$E/logs/$label.stdout" 2> "$E/logs/$label.stderr"
 local result=$?
 printf '%s\n' "$result" > "$E/logs/$label.exit"
 printf '%s\t%s\t%s\t%s\n' "$label" "$result" "$expected" "$role" >> "$E/supplement_commands.tsv"
 print "$label: $result expected $expected"
 [[ $result == $expected ]] || return 71
}
function build {
 local label=$1 source=$2
 run project_$label 0 native_import_projection "$P" "$source" "$E/projected/$label.zag" "$E/projected/$label.provenance" || return 71
 run build_$label 0 native_build "$C" "$E/projected/$label.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/$label"
}
: > "$E/supplement_commands.tsv"
build candidates "$E/sources/candidate_hashes.zag" || exit 71
run candidates 0 native_candidate_identity "$E/bin/candidates" "$E/inputs/candidates.txt" || exit 71
for entry in constant_probe bounded_allocator_tests independent_admission_tests forbidden_selector_tests r25_full_digest_exact_parent_v1_runner repaired_exact_source_gate; do
 build "$entry" "$S/$entry.zag" || exit 71
done
for entry in constant_probe bounded_allocator_tests independent_admission_tests forbidden_selector_tests; do
 run "$entry" 0 isolated_compatibility_mechanics "$E/bin/$entry" || exit 71
done
run r25_usage 64 fail_closed_no_bundle "$E/bin/r25_full_digest_exact_parent_v1_runner" || exit 71
run r25_missing 66 fail_closed_missing_bundle "$E/bin/r25_full_digest_exact_parent_v1_runner" "$E/inputs" absent_r25.pkl absent_r23.pkl absent_speech.pkl absent_noise.pkl absent_arch.json absent_sibling.json absent_learning.json || exit 71
run source_gate_missing 66 fail_closed_missing_whole_source "$E/bin/repaired_exact_source_gate" "$E/inputs" absent_r26.py || exit 71
run supplement_canonical 0 preservation shasum -a 256 -c "$REPO/Research/R33_CLOSEOUT_20260915T174458Z/canonical.sha256" || exit 71
run supplement_protected 0 preservation shasum -a 256 -c "$REPO/Research/R33_CLOSEOUT_20260915T174458Z/protected.sha256" || exit 71
