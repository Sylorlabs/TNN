#!/bin/zsh
set -u
ROOT=/Users/Shared/micah/Documents/TNN/TNN
cd "$ROOT" || exit 99
E="$ROOT/Research/R33_FINISH_RECOVERY_$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$E/sources" "$E/bin" "$E/logs" "$E/runtime"
print -r -- "$E" > /tmp/r33_finish_recovery_20260915_b/evidence_path
cp /tmp/r33_finish_recovery_20260915_b/integration.zsh "$E/integration.zsh"
cp Research/R33_CLOSEOUT_20260915T174458Z/canonical.sha256 "$E/canonical.sha256"
cp Research/R33_CLOSEOUT_20260915T174458Z/protected.sha256 "$E/protected.sha256"
git status --porcelain=v1 > "$E/git.before.status"
git diff --binary > "$E/git.before.diff"
run() {
 local label=$1 expected=$2; shift 2
 local out="$E/logs/$label.stdout" err="$E/logs/$label.stderr" rc=0
 local started=$(date -u +%Y-%m-%dT%H:%M:%SZ)
 "$@" > "$out" 2> "$err" || rc=$?
 local ended=$(date -u +%Y-%m-%dT%H:%M:%SZ)
 local oh=$(shasum -a 256 "$out" | cut -d ' ' -f1) eh=$(shasum -a 256 "$err" | cut -d ' ' -f1)
 jq -cn --arg label "$label" --arg cwd "$ROOT" --arg started "$started" --arg ended "$ended" --argjson exit_code "$rc" --argjson expected "$expected" --arg stdout "$out" --arg stderr "$err" --arg stdout_sha256 "$oh" --arg stderr_sha256 "$eh" --args -- '{label:$label,argv:$ARGS.positional,cwd:$cwd,started_utc:$started,ended_utc:$ended,exit_code:$exit_code,expected_exit_code:$expected,expected_exit_matched:($exit_code==$expected),stdout:$stdout,stderr:$stderr,stdout_sha256:$stdout_sha256,stderr_sha256:$stderr_sha256}' "$@" >> "$E/commands.jsonl"
 print -r -- "$label exit=$rc expected=$expected"
}
freeze() {
 local src=$1 rel=${1#$ROOT/} imported resolved
 [[ -f "$E/sources/$rel" ]] && return 0
 mkdir -p "$E/sources/${rel:h}"
 cp "$src" "$E/sources/$rel"
 while IFS= read -r imported; do
  resolved=$(realpath "${src:h}/$imported")
  [[ "$resolved" == "$ROOT/"* ]] || return 1
  freeze "$resolved" || return 1
 done < <(sed -n 's/^@import("\([^"]*\)").*/\1/p' "$src")
}
run canonical_before 0 shasum -a 256 -c "$E/canonical.sha256"
run protected_before 0 shasum -a 256 -c "$E/protected.sha256"
D=Research/R33_CONTINUING_LIFE_V1
N=Research/R33_NATIVE_N17_R27_CONTINUITY
for spec in "v92:$N/V92_STATE_IMAGE_QUAL/state_image_qual_v92.zag" "integration:$D/lane_d_packet_integration.zag" "baseline:$D/lane_d_baseline_driver.zag"; do
 local label=${spec%%:*} src=${spec#*:}
 freeze "$ROOT/$src" || exit 99
 if [[ "$label" == baseline ]]; then
  cp "$E/sources/$src" "$E/sources/$src.original"
  sed -e "s|Research/R33_CONTINUING_LIFE_V1/LANE_D_20260915/BASELINE_RUNTIME|${E#$ROOT/}/runtime/baseline|g" -e "s|$ROOT/Research/R33_CONTINUING_LIFE_V1/LANE_D_20260915/baseline_driver|$E/bin/baseline|g" "$E/sources/$src.original" > "$E/sources/$src"
  diff -u "$E/sources/$src.original" "$E/sources/$src" > "$E/baseline_routing.diff" || true
 fi
 run build_$label 0 /Users/Shared/micah/Documents/zag/znc "$E/sources/$src" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/$label"
done
mkdir "$E/runtime/v92"
for mode in selftest write read write-corrupt read-corrupt write-truncated read-truncated write-packet read-packet write-packet-corrupt read-packet-corrupt write-packet-truncated read-packet-truncated; do
 run v92_$mode 0 "$E/bin/v92" "$mode" "$E/runtime/v92"
done
for dir in good corrupt inner torn; do mkdir "$E/runtime/$dir"; done
for spec in write:good reload:good corrupt:corrupt refuse:corrupt inner:inner refuse:inner torn:torn refuse:torn; do
 local mode=${spec%%:*} dir=${spec#*:}
 run integration_${mode}_${dir} 0 "$E/bin/integration" "$mode" "$E/runtime/$dir" "$E/runtime/v92"
done
run integration_reload_final 0 "$E/bin/integration" reload "$E/runtime/good" "$E/runtime/v92"
run integration_argc_refusal 64 "$E/bin/integration" reload "$E/runtime/good"
mkdir "$E/runtime/missing_packet" "$E/runtime/missing_outer"
run integration_missing_packet 1 "$E/bin/integration" write "$E/runtime/missing_outer" "$E/runtime/missing_packet"
run baseline_supervise 0 "$E/bin/baseline" supervise
run canonical_after 0 shasum -a 256 -c "$E/canonical.sha256"
run protected_after 0 shasum -a 256 -c "$E/protected.sha256"
find "$E/sources" -type f -exec shasum -a 256 {} \; > "$E/source.sha256"
find "$E/bin" -type f -exec shasum -a 256 {} \; > "$E/binary.sha256"
find "$E/runtime" -type f -exec shasum -a 256 {} \; > "$E/runtime.sha256"
jq -s '{commands:length,unexpected:[.[]|select(.expected_exit_matched==false)]}' "$E/commands.jsonl" > "$E/qualification_summary.json"
print -r -- "EVIDENCE=$E"
