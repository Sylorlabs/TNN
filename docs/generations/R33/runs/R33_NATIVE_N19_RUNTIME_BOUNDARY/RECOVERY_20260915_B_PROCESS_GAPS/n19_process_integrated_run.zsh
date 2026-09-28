#!/bin/zsh
set -eu
cd /Users/Shared/micah/Documents/TNN/TNN
E=Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/RECOVERY_20260915_B_PROCESS_GAPS
integer i=700 failures=0
run() {
 local label=$1 expected=$2; shift 2
 i=$((i+1)); local stem="$E/logs/${i}_${label}"
 printf '%q ' "$@" > "$stem.command"; printf '\n' >> "$stem.command"
 set +e; "$@" > "$stem.stdout" 2> "$stem.stderr"; local rc=$?; set -e
 printf '%s\n' "$rc" > "$stem.exit"
 printf '%s expected=%s actual=%s\n' "$label" "$expected" "$rc" >> "$E/process.integrated.results.txt"
 if [[ $rc != $expected ]]; then failures=$((failures+1)); fi
}
# Existing additive log directory; final rounds use fresh roots.
run build_qual 0 /Users/Shared/micah/Documents/zag/znc "$E/sources/n19_qual_driver_v3_recovery.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/n19_qual"
run build_host 0 /Users/Shared/micah/Documents/zag/znc "$E/sources/n19_host_v2_tests.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/n19_host_tests"
P="$E/sources/n19_runtime_boundary_v6_recovery.zag"
run build_repaired 0 /Users/Shared/micah/Documents/zag/znc "$P" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/n19_repaired"
B="$E/bin/n19_repaired"
for round in e f; do
 R="$E/roots/$round"; mkdir "$R" "$R/poison" "$R/crash" "$R/resource" "$R/ops" "$R/host"
 run wait_$round 0 "$E/bin/n19_qual" wait-tests
 run resource_predicate_$round 0 "$E/bin/n19_qual" resource-predicate-tests
 run cpu_$round 0 "$E/bin/n19_qual" cpu-ceiling "$B" "$R/resource"
 run invariants_$round 0 "$B" case-extra-invariants
 run poison_$round 0 "$B" case-poisoned-append "$R/poison" journal.bin
 run crash_$round 0 "$E/bin/n19_qual" crash-matrix "$B" "$R/crash"
 run resource_$round 0 "$E/bin/n19_qual" resource "$B" "$R/resource"
 run host_$round 0 "$E/bin/n19_host_tests" unit "$R/host"
 for mode in case-malformed case-overflow case-capacity case-recovery case-corruption case-recovery-atomicity case-error-classification case-limit; do run ${round}_${mode} 0 "$B" "$mode"; done
 for mode in case-host-abi case-fault-open case-fault-host-probe; do run ${round}_${mode} 0 "$B" "$mode" "$R/ops"; done
 for pair in case-io:io.bin case-write:append.bin case-append-existing:append.bin case-recover-file:append.bin case-probe-existing:append.bin case-retained-sequence:retained.bin case-torn:torn.bin case-fault-fsync:fsync.bin case-fault-close:close.bin; do run ${round}_${pair%:*} 0 "$B" "${pair%:*}" "$R/ops" "${pair#*:}"; done
 for mode in case-recover-file case-probe-existing case-append-existing; do run ${round}_missing_${mode} 1 "$B" "$mode" "$R/ops" missing.bin; done
 run ${round}_duplicate 1 "$B" case-write "$R/ops" append.bin
 run ${round}_missing_root 1 "$B" case-host-abi "$R/ops/missing"
 run ${round}_missing_recover_root 1 "$B" case-recover-file "$R/ops/missing" missing.bin
 for leaf in sym.bin hard.bin one.bin fifo directory; do run ${round}_unsafe_${leaf} 1 "$B" case-probe-existing "$R/host" "$leaf"; done
 ln -s ops "$R/root_symlink"
 run ${round}_symlink_root 1 "$B" case-host-abi "$R/root_symlink"
 run ${round}_symlink_recover 1 "$B" case-recover-file "$R/root_symlink" append.bin
 run ${round}_traversal 1 "$B" case-probe-existing "$R/ops" ../append.bin
 run ${round}_absolute 1 "$B" case-probe-existing "$R/ops" /append.bin
 stat -f '%N %z %Lp %l' "$R/resource/resource.bin" "$R/ops/append.bin" "$R/poison/journal.bin" > "$R/stat.txt"
done
run canonical_preserved 0 shasum -a 256 -c "$E/canonical.before.sha256"
run protected_preserved 0 shasum -a 256 -c "$E/protected.before.sha256"
run closeout_preserved 0 shasum -a 256 -c "$E/closeout.before.sha256"
git diff --binary > "$E/git.repaired.diff"
run tracked_diff_preserved 0 cmp "$E/git.before.diff" "$E/git.repaired.diff"
shasum -a 256 "$E/bin/"* > "$E/binary.sha256"
shasum -a 256 "$E/sources/"* > "$E/source.sha256"
find "$E/logs" -type f -exec shasum -a 256 {} + > "$E/logs.sha256"
printf 'failures=%s commands=%s\n' "$failures" "$((i-700))" > "$E/process.integrated.summary.txt"
cat "$E/process.integrated.summary.txt"
exit $((failures != 0))
