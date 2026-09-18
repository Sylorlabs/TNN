#!/bin/zsh
set -u
REPO=/Users/Shared/micah/Documents/TNN/TNN
N=$REPO/Research/R33_NATIVE_N17_R27_CONTINUITY
E=$N/FINAL_B_20260915_1409/N17_REFRESH
C=/Users/Shared/micah/Documents/zag/znc
P=$N/FINAL_B_20260915_1409/V91_REFRESH/bin/project
mkdir -p "$E/projected"
: > "$E/commands.tsv"
function run {
 local label=$1 expected=$2 role=$3
 shift 3
 printf '%s\n' "$@" > "$E/logs/$label.argv"
 "$@" > "$E/logs/$label.stdout" 2> "$E/logs/$label.stderr"
 local result=$?
 printf '%s\n' "$result" > "$E/logs/$label.exit"
 printf '%s\t%s\t%s\t%s\n' "$label" "$result" "$expected" "$role" >> "$E/commands.tsv"
 print "$label: $result expected $expected"
 [[ $result == $expected ]] || return 71
}
function build {
 local label=$1 source=$2
 run project_$label 0 native_import_projection "$P" "$source" "$E/projected/$label.zag" "$E/projected/$label.provenance" || return 71
 run build_$label 0 native_build "$C" "$E/projected/$label.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/$label"
}
run canonical_before 0 preservation shasum -a 256 -c "$REPO/Research/R33_CLOSEOUT_20260915T174458Z/canonical.sha256" || exit 71
run protected_before 0 preservation shasum -a 256 -c "$REPO/Research/R33_CLOSEOUT_20260915T174458Z/protected.sha256" || exit 71
run compiler_before 0 compiler_pin shasum -a 256 "$C" || exit 71
build rows "$N/LANE_B_AUDIT_20260915/FROZEN/Research/R33_NATIVE_N17_R27_CONTINUITY/LANE_B_AUDIT_20260915/rows.zag" || exit 71
build structure "$N/LANE_B_AUDIT_20260915/FROZEN/Research/R33_NATIVE_N17_R27_CONTINUITY/LANE_B_AUDIT_20260915/structure.zag" || exit 71
build primitives "$N/LANE_B_AUDIT_20260915/FROZEN/Research/R33_NATIVE_N17_R27_CONTINUITY/LANE_B_AUDIT_20260915/primitives.zag" || exit 71
build r26 "$N/LANE_B_AUDIT_20260915/FROZEN/Research/R33_NATIVE_N17_R27_CONTINUITY/r26_digest.zag" || exit 71
build r27 "$N/LANE_B_AUDIT_20260915/FROZEN/Research/R33_NATIVE_N17_R27_CONTINUITY/r27_digest.zag" || exit 71
build reviewed "$N/RECOVERY_20260915_B_INDEPENDENT/review_native.zag" || exit 71
build memo "$N/RECOVERY_20260915_B_INDEPENDENT/memo_negative.zag" || exit 71
build policy "$E/sources/policy_native.zag" || exit 71
run rows 0 static_source_rows "$E/bin/rows" || exit 71
run structure 0 head_width_and_static_negatives "$E/bin/structure" || exit 71
run primitives 0 sha_known_answers_canary "$E/bin/primitives" || exit 71
run r26_selftest 0 digest_components "$E/bin/r26" selftest || exit 71
run r26_digest 0 direct_native_digest "$E/bin/r26" digest || exit 71
run r27_digest 0 direct_native_digest "$E/bin/r27" digest || exit 71
run r26_match 0 witness_comparison rg -x 'R26_NATIVE_DIGEST,44d36746ffb9e8d46080376a6e26bb824772d9d4b5e429add404195d02888649' "$E/logs/r26_digest.stdout" || exit 71
run r27_match 0 witness_comparison rg -x 'R27_NATIVE_DIGEST,562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04' "$E/logs/r27_digest.stdout" || exit 71
run reviewed 0 independently_reviewed_inert_equivalents "$E/bin/reviewed" || exit 71
run memo 0 negative_memo_identity "$E/bin/memo" || exit 71
cp "$N/LANE_B_AUDIT_20260915/FROZEN/r27-policy.json" "$E/inputs/r27-policy.json"
run policy 0 direct_native_policy "$E/bin/policy" "$E/inputs/r27-policy.json" || exit 71
run policy_missing 66 source_refusal "$E/bin/policy" "$E/inputs/absent-policy.json" || exit 71
run corrupt_policy_setup 0 fixture_setup dd if=/dev/zero of="$E/inputs/corrupt-policy.json" bs=1 count=8 || exit 71
run policy_corrupt 71 source_refusal "$E/bin/policy" "$E/inputs/corrupt-policy.json" || exit 71
run canonical_after 0 preservation shasum -a 256 -c "$REPO/Research/R33_CLOSEOUT_20260915T174458Z/canonical.sha256" || exit 71
run protected_after 0 preservation shasum -a 256 -c "$REPO/Research/R33_CLOSEOUT_20260915T174458Z/protected.sha256" || exit 71
run compiler_after 0 compiler_pin shasum -a 256 "$C" || exit 71
run compiler_equal 0 preservation cmp "$E/logs/compiler_before.stdout" "$E/logs/compiler_after.stdout" || exit 71
