#!/bin/zsh
set -u
cd /Users/Shared/micah/Documents/TNN/TNN || exit 90
audit=Research/R33_NATIVE_N17_R27_CONTINUITY/LANE_B_AUDIT_20260915
n17=Research/R33_NATIVE_N17_R27_CONTINUITY
for leaf in r25_full_digest_exact_parent_v1_runner r25_numpy_payload_map_v1 r25_torch_payload_map_v1 r25_full_digest_v1 r25_release_identity_v1 r25_digest_component_schema_v1 r25_digest_preimage_v1 r27_migration_admission_v2; do cp "$n17/$leaf.zag" "$audit/FROZEN/Research/R33_NATIVE_N17_R27_CONTINUITY/" || exit 91; done
cp Research/R33_NATIVE_SHA256_V2.zag "$audit/FROZEN/Research/" || exit 92
cp Research/R33_NATIVE_IO_V1.zag "$audit/FROZEN/Research/" || exit 93
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
record compile.r25 /Users/Shared/micah/Documents/zag/znc "$audit/FROZEN/Research/R33_NATIVE_N17_R27_CONTINUITY/r25_full_digest_exact_parent_v1_runner.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$audit/BUILD/r25"
record missing.r25import test -f "$n17/r27_native_state_semantics_v1.zag"
record local.members zsh -c 'rg --files --hidden --no-ignore Research /private/tmp/r33-v68 /private/tmp/r33-v71-clean /private/tmp/r33-v73 2>/dev/null | rg "(verify_r26.py$|verify_r27.py$|r26_summary.json$|r27_summary.json$|r26_experiments.py$|general-learning.zip$|r25-accepted-state.pkl$|r26-accepted-state.pkl$|r26-accepted-policy.json$)"'
rg --files "$audit/FROZEN" | LC_ALL=C sort | while IFS= read -r file; do shasum -a 256 "$file"; done > "$audit/FROZEN_FINAL.sha256"
record frozen.final.recheck shasum -a 256 -c "$audit/FROZEN_FINAL.sha256"
sed -n '1,80p' "$audit/compile.r25.stderr"
