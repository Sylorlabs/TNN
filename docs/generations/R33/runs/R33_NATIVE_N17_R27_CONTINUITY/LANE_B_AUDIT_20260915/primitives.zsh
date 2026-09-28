#!/bin/zsh
set -u
cd /Users/Shared/micah/Documents/TNN/TNN || exit 90
audit=Research/R33_NATIVE_N17_R27_CONTINUITY/LANE_B_AUDIT_20260915
cp "$audit/primitives.zag" "$audit/FROZEN/Research/R33_NATIVE_N17_R27_CONTINUITY/LANE_B_AUDIT_20260915/" || exit 91
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
record compile.primitives /Users/Shared/micah/Documents/zag/znc "$audit/FROZEN/Research/R33_NATIVE_N17_R27_CONTINUITY/LANE_B_AUDIT_20260915/primitives.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$audit/BUILD/primitives"
record primitives "$audit/BUILD/primitives"
rg --files "$audit/FROZEN" | LC_ALL=C sort | while IFS= read -r file; do shasum -a 256 "$file"; done > "$audit/FROZEN_FINAL.sha256"
rg --files "$audit/BUILD" | LC_ALL=C sort | while IFS= read -r file; do shasum -a 256 "$file"; done > "$audit/BINARY_FINAL.sha256"
record frozen.complete.recheck shasum -a 256 -c "$audit/FROZEN_FINAL.sha256"
record custody.complete.recheck shasum -a 256 -c "$audit/custody.before.sha256"
sed -n '1,30p' "$audit/primitives.stdout"
