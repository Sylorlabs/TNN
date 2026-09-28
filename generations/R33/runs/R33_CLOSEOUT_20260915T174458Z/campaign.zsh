#!/bin/zsh
set -u
ROOT=/Users/Shared/micah/Documents/TNN/TNN
cd "$ROOT" || exit 99
E=Research/R33_CLOSEOUT_$(date -u +%Y%m%dT%H%M%SZ)
mkdir "$E" || exit 99
E=$ROOT/$E
print -r -- "$E" > /tmp/r33_integrator_evidence_path
mkdir -p "$E/sources" "$E/bin" "$E/logs" "$E/runtime"
cp /tmp/r33_integrate_campaign.zsh "$E/campaign.zsh"
git status --short > "$E/git.before.status"
git diff > "$E/git.before.diff"
shasum -a 256 -c Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/INDEPENDENT_V3_FRESH/canonical_raw.sha256 > "$E/canonical.before.verify" 2>&1
print $? > "$E/canonical.before.exit"
cp Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/INDEPENDENT_V3_FRESH/canonical_raw.sha256 "$E/canonical.sha256"
shasum -a 256 Research/R33_CURRENT_STATE.json Research/R33_EXPERIMENT_REGISTRY.json Research/R33_CONSUMED_EVIDENCE_REGISTRY.json /Users/Shared/micah/Documents/zag/znc > "$E/protected.sha256"
for lane in a b c d; do
 cp /tmp/r33_superagent_20260915_1022/$lane.final "$E/lane_$lane.final"
 shasum -a 256 /tmp/r33_superagent_20260915_1022/$lane.log >> "$E/lane_logs.sha256"
 rg -n 'diff --git|^\+|^-' /tmp/r33_superagent_20260915_1022/$lane.log > "$E/lane_$lane.diff_witness.txt"
done
freeze() {
 local src=$1 rel=${1#$ROOT/} imported resolved
 [[ -f "$E/sources/$rel" ]] && return 0
 mkdir -p "$E/sources/${rel:h}"
 cp "$src" "$E/sources/$rel"
 while IFS= read -r imported; do
  resolved=$(realpath "${src:h}/$imported")
  [[ "$resolved" == "$ROOT/"* ]] || return 1
  freeze "$resolved"
 done < <(sed -n 's/^@import("\([^"]*\)").*/\1/p' "$src")
}
run() {
 local label=$1 expected=$2; shift 2
 local out=$E/logs/$label.stdout err=$E/logs/$label.stderr rc=0 cmd="${(q)@}"
 "$@" > "$out" 2> "$err" || rc=$?
 local oh=$(shasum -a 256 "$out" | cut -d ' ' -f1) eh=$(shasum -a 256 "$err" | cut -d ' ' -f1)
 jq -cn --arg label "$label" --arg command "$cmd > ${(q)out} 2> ${(q)err}" --arg cwd "$ROOT" --argjson exit_code "$rc" --argjson expected "$expected" --arg stdout "$out" --arg stderr "$err" --arg stdout_sha256 "$oh" --arg stderr_sha256 "$eh" '{label:$label,command:$command,cwd:$cwd,exit_code:$exit_code,expected_exit_code:$expected,expected_exit_matched:($exit_code==$expected),stdout:$stdout,stderr:$stderr,stdout_sha256:$stdout_sha256,stderr_sha256:$stderr_sha256}' >> "$E/commands.jsonl"
 print "$label exit=$rc expected=$expected"
}
D=Research/R33_CONTINUING_LIFE_V1
N=Research/R33_NATIVE_N17_R27_CONTINUITY
H=Research/R33_NATIVE_N19_RUNTIME_BOUNDARY
for spec in "v68:$D/outer_learner_packet_bridge_v68_tests.zag" "v71:$D/zag_checkpoint_module_repro_v71.zag" "v73:$D/zag_checkpoint_sliceparam_repro_v73.zag" "v92:$N/V92_STATE_IMAGE_QUAL/state_image_qual_v92.zag" "integration:$D/lane_d_packet_integration.zag" "baseline:$D/lane_d_baseline_driver.zag" "n19:$H/n19_runtime_boundary_v4_review.zag" "n19_qual:$H/n19_qual_driver_v2_review.zag" "n19_host:$H/n19_host_v2_tests.zag"; do
 label=${spec%%:*}; src=${spec#*:}; freeze "$ROOT/$src"
 if [[ $label == baseline ]]; then
  sed -e "s|Research/R33_CONTINUING_LIFE_V1/LANE_D_20260915/BASELINE_RUNTIME|${E#$ROOT/}/runtime/baseline|g" -e "s|$ROOT/Research/R33_CONTINUING_LIFE_V1/LANE_D_20260915/baseline_driver|$E/bin/baseline|g" "$E/sources/$src" > "$E/sources/$src.routed"
  mv "$E/sources/$src.routed" "$E/sources/$src"
 fi
 run build_$label 0 /Users/Shared/micah/Documents/zag/znc "$E/sources/$src" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/$label"
done
run v68 1 "$E/bin/v68"
run v71 0 "$E/bin/v71"
run v73 1 "$E/bin/v73"
mkdir "$E/runtime/v92"
for mode in selftest write read write-corrupt read-corrupt write-truncated read-truncated write-packet read-packet write-packet-corrupt read-packet-corrupt write-packet-truncated read-packet-truncated; do
 run v92_$mode 0 "$E/bin/v92" "$mode" "$E/runtime/v92"
done
mkdir "$E/runtime/baseline"
run baseline_supervise 0 "$E/bin/baseline" supervise
for dir in good corrupt inner torn; do mkdir "$E/runtime/$dir"; done
for spec in write:good reload:good corrupt:corrupt refuse:corrupt inner:inner refuse:inner torn:torn refuse:torn; do
 mode=${spec%%:*}; dir=${spec#*:}; run integration_${mode}_${dir} 0 "$E/bin/integration" "$mode" "$E/runtime/$dir"
done
run integration_reload_final 0 "$E/bin/integration" reload "$E/runtime/good"
# learn is deliberately not invoked: source-level refusal remains closed.
for dir in host crash resource ops; do mkdir "$E/runtime/n19_$dir"; done
run n19_host 0 "$E/bin/n19_host" unit "$E/runtime/n19_host"
run n19_crash 0 "$E/bin/n19_qual" crash-matrix "$E/bin/n19" "$E/runtime/n19_crash"
run n19_resource 0 "$E/bin/n19_qual" resource "$E/bin/n19" "$E/runtime/n19_resource"
for mode in case-malformed case-overflow case-capacity case-recovery case-corruption case-recovery-atomicity case-error-classification case-limit; do run n19_$mode 0 "$E/bin/n19" "$mode"; done
run n19_host_abi 0 "$E/bin/n19" case-host-abi "$E/runtime/n19_ops"
for spec in case-io:io.bin case-write:append.bin case-append-existing:append.bin case-recover-file:append.bin case-probe-existing:append.bin case-retained-sequence:retained.bin case-torn:torn.bin case-fault-fsync:fsync.bin case-fault-close:close.bin; do
 mode=${spec%%:*}; leaf=${spec#*:}; run n19_${mode} 0 "$E/bin/n19" "$mode" "$E/runtime/n19_ops" "$leaf"
done
run n19_fault_open 0 "$E/bin/n19" case-fault-open "$E/runtime/n19_ops"
run n19_fault_host_probe 0 "$E/bin/n19" case-fault-host-probe "$E/runtime/n19_ops"
for mode in case-recover-file case-probe-existing case-append-existing; do run n19_missing_$mode 1 "$E/bin/n19" "$mode" "$E/runtime/n19_ops" missing.bin; done
run n19_duplicate_write 1 "$E/bin/n19" case-write "$E/runtime/n19_ops" append.bin
run n19_missing_root 1 "$E/bin/n19" case-host-abi "$E/runtime/n19_ops/missing"
for leaf in sym.bin hard.bin fifo directory; do run n19_type_$leaf 1 "$E/bin/n19" case-probe-existing "$E/runtime/n19_host" "$leaf"; done
ln -s n19_ops "$E/runtime/n19_root_symlink"
run n19_root_symlink 1 "$E/bin/n19" case-host-abi "$E/runtime/n19_root_symlink"
run n19_root_symlink_lookup 1 "$E/bin/n19" case-probe-existing "$E/runtime/n19_root_symlink" append.bin
run protected_unchanged 0 shasum -a 256 -c "$E/protected.sha256"
run canonical_unchanged 0 shasum -a 256 -c "$E/canonical.sha256"
find "$E/sources" -type f -exec shasum -a 256 {} \; > "$E/source.sha256"
find "$E/bin" -type f -exec shasum -a 256 {} \; > "$E/binary.sha256"
print "EVIDENCE=$E"
