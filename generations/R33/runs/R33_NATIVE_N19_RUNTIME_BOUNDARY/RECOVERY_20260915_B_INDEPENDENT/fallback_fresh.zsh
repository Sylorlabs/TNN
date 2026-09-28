#!/bin/zsh
set -eu
E=Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/RECOVERY_20260915_B_INDEPENDENT
run() {
 local stem="$E/logs/$1"; shift
 printf '%q ' "$@" > "$stem.command"
 set +e; "$@" > "$stem.stdout" 2> "$stem.stderr"; local rc=$?; set -e
 printf '%s\n' "$rc" > "$stem.exit"
 [[ $rc == 0 ]]
}
run 100_build_fallback /Users/Shared/micah/Documents/zag/znc "$E/sources/independent_supervisor.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/supervisor_fresh"
for n in 1 2 3 4; do
 run 10${n}_fallback "$E/bin/supervisor_fresh" independent-fallback "$E/bin/corners" "$E/roots/a/poison"
done
