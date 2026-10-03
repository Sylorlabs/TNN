#!/bin/zsh
set -u
cd /Users/Shared/micah/Documents/TNN/TNN || exit 90
audit=Research/R33_NATIVE_N17_R27_CONTINUITY/LANE_B_AUDIT_20260915
compiler=/Users/Shared/micah/Documents/zag/znc
cp "$audit/structure.zag" "$audit/FROZEN/Research/R33_NATIVE_N17_R27_CONTINUITY/LANE_B_AUDIT_20260915/" || exit 91
shasum -a 256 "$audit/FROZEN/Research/R33_NATIVE_N17_R27_CONTINUITY/LANE_B_AUDIT_20260915/structure.zag" > "$audit/SUPPLEMENT_SOURCE.sha256"
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
record compile.structure "$compiler" "$audit/FROZEN/Research/R33_NATIVE_N17_R27_CONTINUITY/LANE_B_AUDIT_20260915/structure.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$audit/BUILD/structure"
record structure "$audit/BUILD/structure"
record match.r26 rg -x 'R26_NATIVE_DIGEST,44d36746ffb9e8d46080376a6e26bb824772d9d4b5e429add404195d02888649' "$audit/r26.digest.stdout"
record match.r27 rg -x 'R27_NATIVE_DIGEST,562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04' "$audit/r27.digest.stdout"
record match.policy rg '^983db6a9c771f4952392d288459d65dfb04c33a7cbca37ac9f10a4365c7887a8 ' "$audit/policy.hash.stdout"
record custody.final shasum -a 256 -c "$audit/custody.before.sha256"
record supplement.recheck shasum -a 256 -c "$audit/SUPPLEMENT_SOURCE.sha256"
rg --files "$audit/BUILD" | LC_ALL=C sort | while IFS= read -r file; do shasum -a 256 "$file"; done > "$audit/BINARY_FINAL.sha256"
sed -n '1,80p' "$audit/exits.tsv"
