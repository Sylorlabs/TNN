#!/bin/sh
set -u
cd /Users/Shared/micah/Documents/TNN/TNN || exit 99
BASE=Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/INDEPENDENT_V3_FRESH
E=${N19_REVIEW_ROOT:-$BASE}
B=$BASE/n19
run() {
  printf 'COMMAND'; printf ' %s' "$@"; printf '\n'
  "$@"
  rc=$?
  printf 'EXIT %s\n' "$rc"
}
mkdir "$E/host" "$E/crash" "$E/resource" "$E/ops" "$E/old_crash" "$E/old_resource"
run "$BASE/n19_host_tests" unit "$E/host"
run "$BASE/n19_qual" crash-matrix "$B" "$E/crash"
run "$BASE/n19_qual" resource "$B" "$E/resource"
run "$BASE/n19_qual" crash-matrix Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/BUILD_08/n19_v3b "$E/old_crash"
run "$BASE/n19_qual" resource Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/BUILD_08/n19_v3b "$E/old_resource"
for mode in case-malformed case-overflow case-capacity case-recovery case-corruption case-recovery-atomicity case-error-classification case-limit; do run "$B" "$mode"; done
run "$B" case-host-abi "$E/ops"
run "$B" case-io "$E/ops" io.bin
run "$B" case-write "$E/ops" append.bin
run "$B" case-append-existing "$E/ops" append.bin
run "$B" case-recover-file "$E/ops" append.bin
run "$B" case-probe-existing "$E/ops" append.bin
run "$B" case-retained-sequence "$E/ops" retained.bin
run "$B" case-torn "$E/ops" torn.bin
run "$B" case-fault-open "$E/ops"
run "$B" case-fault-fsync "$E/ops" fsync.bin
run "$B" case-fault-close "$E/ops" close.bin
run "$B" case-fault-host-probe "$E/ops"
run "$B" case-recover-file "$E/ops" missing.bin
run "$B" case-probe-existing "$E/ops" missing.bin
run "$B" case-write "$E/ops" append.bin
run "$B" case-append-existing "$E/ops" missing.bin
run "$B" case-host-abi "$E/ops/missing"
run "$B" case-probe-existing "$E/host" sym.bin
run "$B" case-probe-existing "$E/host" hard.bin
run "$B" case-probe-existing "$E/host" fifo
run "$B" case-probe-existing "$E/host" directory
run "$B" case-recover-file "$E/ops/missing" missing.bin
stat -f '%N %z %Lp %l' "$E/resource/resource.bin" "$E/old_resource/resource.bin" "$E/ops/append.bin"
shasum -a 256 -c "$BASE/protected.sha256"
shasum -a 256 -c "$BASE/old_evidence.sha256"
