#!/bin/zsh
set -eu
cd /Users/Shared/micah/Documents/TNN/TNN
E=Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/RECOVERY_20260915_B
mkdir "$E"
mkdir "$E/sources" "$E/bin" "$E/logs" "$E/roots"
C=Research/R33_CLOSEOUT_20260915T174458Z
cp "$C"/sources/Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/*.zag "$E/sources/"
shasum -a 256 "$E"/sources/*.zag > "$E/source.original.sha256"
cp "$C/canonical.sha256" "$E/canonical.before.sha256"
shasum -a 256 Research/R33_CURRENT_STATE.json Research/R33_EXPERIMENT_REGISTRY.json Research/R33_CONSUMED_EVIDENCE_REGISTRY.json Research/R33_HANDOFF.md Research/R33_EXECUTION_JOURNAL.md Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/STATUS.json /Users/Shared/micah/Documents/zag/znc > "$E/protected.before.sha256"
find "$C" -type f -exec shasum -a 256 {} + > "$E/closeout.before.sha256"
git diff --binary > "$E/git.before.diff"
sw_vers > "$E/host.txt"
uname -a >> "$E/host.txt"
integer idx=0 failures=0
run() {
 local label=$1 expected=$2; shift 2
 idx=$((idx+1))
 local stem="$E/logs/${idx}_${label}"
 printf '%q ' "$@" > "$stem.command"; printf '\n' >> "$stem.command"
 set +e
 "$@" > "$stem.stdout" 2> "$stem.stderr"
 local rc=$?
 set -e
 printf '%s\n' "$rc" > "$stem.exit"
 printf '%s expected=%s actual=%s\n' "$label" "$expected" "$rc" >> "$E/results.txt"
 if [[ $rc != $expected ]]; then failures=$((failures+1)); fi
}
for pair in 'n19_runtime_boundary_v4_review.zag:n19' 'n19_qual_driver_v2_review.zag:n19_qual' 'n19_host_v2_tests.zag:n19_host_tests'; do
 run build_${pair#*:} 0 /Users/Shared/micah/Documents/zag/znc "$E/sources/${pair%:*}" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/${pair#*:}"
done
if (( failures != 0 )); then exit 1; fi
B="$E/bin/n19"
for round in a b; do
 R="$E/roots/$round"
 mkdir "$R" "$R/host" "$R/crash" "$R/resource" "$R/ops"
 run host_$round 0 "$E/bin/n19_host_tests" unit "$R/host"
 run crash_$round 0 "$E/bin/n19_qual" crash-matrix "$B" "$R/crash"
 run resource_$round 0 "$E/bin/n19_qual" resource "$B" "$R/resource"
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
 stat -f '%N %z %Lp %l' "$R/resource/resource.bin" "$R/ops/append.bin" > "$R/stat.txt"
done
run canonical_preserved 0 shasum -a 256 -c "$E/canonical.before.sha256"
run protected_preserved 0 shasum -a 256 -c "$E/protected.before.sha256"
run closeout_preserved 0 shasum -a 256 -c "$E/closeout.before.sha256"
git diff --binary > "$E/git.after.diff"
run tracked_diff_preserved 0 cmp "$E/git.before.diff" "$E/git.after.diff"
shasum -a 256 "$E/bin/"* > "$E/binary.sha256"
shasum -a 256 "$E/sources/"* > "$E/source.sha256"
printf 'failures=%s commands=%s\n' "$failures" "$idx" > "$E/summary.txt"
find "$E/logs" -type f -exec shasum -a 256 {} + > "$E/logs.sha256"
cat "$E/summary.txt"
exit $((failures != 0))
