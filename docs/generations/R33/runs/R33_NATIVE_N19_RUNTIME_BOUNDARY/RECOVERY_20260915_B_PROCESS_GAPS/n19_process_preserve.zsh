#!/bin/zsh
set -eu
cd /Users/Shared/micah/Documents/TNN/TNN
E=Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/RECOVERY_20260915_B_PROCESS_GAPS
for pair in c_restored:c.restoration.expected.sha256 full_reviewer_baseline:../RECOVERY_20260915_B_INDEPENDENT/preserved.before.sha256; do
 label=${pair%:*}; path=${pair#*:}; stem="$E/logs/900_$label"
 printf 'shasum -a 256 -c %q\n' "$E/$path" > "$stem.command"
 set +e
 shasum -a 256 -c "$E/$path" > "$stem.stdout" 2> "$stem.stderr"
 rc=$?
 set -e
 printf '%s\n' "$rc" > "$stem.exit"
 printf '%s expected=0 actual=%s\n' "$label" "$rc" >> "$E/restoration.results.txt"
done
