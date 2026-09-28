#!/bin/zsh
set -u
cd /Users/Shared/micah/Documents/TNN/TNN || exit 90
audit=Research/R33_NATIVE_N17_R27_CONTINUITY/LANE_B_AUDIT_20260915
n17=Research/R33_NATIVE_N17_R27_CONTINUITY
compiler=/Users/Shared/micah/Documents/zag/znc
mkdir -p "$audit/FROZEN/Research/R33_NATIVE_N17_R27_CONTINUITY/LANE_B_AUDIT_20260915" "$audit/FROZEN/Research/R33_NATIVE_N13A_FINGERPRINT_SCRATCH" "$audit/FROZEN/Research/R33_NATIVE_N17_R27_CONTINUITY/V91_SEMANTIC_KAT" "$audit/BUILD"
for leaf in tensor storage views binding mapio inert R33_NATIVE_SHA256_V2 R33_NATIVE_IO_V1; do
 cp "Research/R33_NATIVE_N13A_FINGERPRINT_SCRATCH/$leaf.zag" "$audit/FROZEN/Research/R33_NATIVE_N13A_FINGERPRINT_SCRATCH/" || exit 91
done
for leaf in identity r26_digest r27_digest; do cp "$n17/$leaf.zag" "$audit/FROZEN/Research/R33_NATIVE_N17_R27_CONTINUITY/" || exit 92; done
cp "$audit/rows.zag" "$audit/FROZEN/Research/R33_NATIVE_N17_R27_CONTINUITY/LANE_B_AUDIT_20260915/" || exit 93
for leaf in v91_semantic_kat v91_semantic_kat_tests v91_emit_rows v91_admission_gate r23_blake2b64_person_v1 r25_blake2b64_v1 r25_mt19937_v1; do
 cp "$n17/V91_SEMANTIC_KAT/$leaf.zag" "$audit/FROZEN/Research/R33_NATIVE_N17_R27_CONTINUITY/V91_SEMANTIC_KAT/" || exit 94
done
cp Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-policy.json "$audit/FROZEN/r27-policy.json" || exit 95
rg --files "$audit/FROZEN" | LC_ALL=C sort | while IFS= read -r file; do shasum -a 256 "$file"; done > "$audit/FROZEN.sha256"
shasum -a 256 "$compiler" Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-state.pkl Research/R33_NATIVE_N10_RUN_PRIMARY_V1/parent-map/manifest.bin > "$audit/custody.before.sha256"
function record {
 local label=$1
 shift
 printf '%s' "$label" >> "$audit/commands.tsv"
 printf '\t%q' "$@" >> "$audit/commands.tsv"
 printf '\n' >> "$audit/commands.tsv"
 "$@" > "$audit/$label.stdout" 2> "$audit/$label.stderr"
 local rc=$?
 printf '%s\t%s\n' "$label" "$rc" >> "$audit/exits.tsv"
 return 0
}
src="$audit/FROZEN/Research/R33_NATIVE_N17_R27_CONTINUITY"
record compile.rows "$compiler" "$src/LANE_B_AUDIT_20260915/rows.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$audit/BUILD/rows"
record compile.r26 "$compiler" "$src/r26_digest.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$audit/BUILD/r26"
record compile.r27 "$compiler" "$src/r27_digest.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$audit/BUILD/r27"
record compile.v91tests "$compiler" "$src/V91_SEMANTIC_KAT/v91_semantic_kat_tests.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$audit/BUILD/v91tests"
record compile.v91rows "$compiler" "$src/V91_SEMANTIC_KAT/v91_emit_rows.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$audit/BUILD/v91rows"
record compile.v91gate "$compiler" "$src/V91_SEMANTIC_KAT/v91_admission_gate.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$audit/BUILD/v91gate"
record rows "$audit/BUILD/rows"
record r26.selftest "$audit/BUILD/r26" selftest
record r26.digest "$audit/BUILD/r26" digest
record r27.digest "$audit/BUILD/r27" digest
record v91tests "$audit/BUILD/v91tests"
record v91rows "$audit/BUILD/v91rows"
record v91gate "$audit/BUILD/v91gate"
record policy jq -e '.format == "TNN_PRE_V1_R27_POLICY" and (.locked_gates | sort) == (["TEENAGER_ENGLISH","ADULT_ENGLISH","NATURAL_VIDEO_AUDIO","HUMAN_SUPERIORITY","NATIVE_ZAG","OPEN_ENDED_RECURSIVE_SELF_IMPROVEMENT","AHI","PRODUCTION_TNN_V1"] | sort) and .active_promotions == ["STRONGER_MASTER_GENERAL_SPECIFIC_BRIDGE"]' "$audit/FROZEN/r27-policy.json"
record policy.hash shasum -a 256 "$audit/FROZEN/r27-policy.json"
record frozen.recheck shasum -a 256 -c "$audit/FROZEN.sha256"
shasum -a 256 "$compiler" Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-state.pkl Research/R33_NATIVE_N10_RUN_PRIMARY_V1/parent-map/manifest.bin > "$audit/custody.after.sha256"
record custody.compare cmp "$audit/custody.before.sha256" "$audit/custody.after.sha256"
rg --files "$audit/BUILD" | LC_ALL=C sort | while IFS= read -r file; do shasum -a 256 "$file"; done > "$audit/BINARY.sha256"
sed -n '1,80p' "$audit/exits.tsv"
