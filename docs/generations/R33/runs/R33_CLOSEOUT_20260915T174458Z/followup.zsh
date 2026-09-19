#!/bin/zsh
set -u
ROOT=/Users/Shared/micah/Documents/TNN/TNN
cd "$ROOT" || exit 99
E=$(cat /tmp/r33_integrator_evidence_path)
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
mkdir "$E/probe_sources"
cp "$E/sources/$D/lane_d_packet_integration.zag" "$E/probe_sources/integration_hardcoded.zag"
cp "$ROOT/$D/lane_d_packet_integration.zag" "$E/sources/$D/lane_d_packet_integration.zag"
run build_integration_fresh 0 /Users/Shared/micah/Documents/zag/znc "$E/sources/$D/lane_d_packet_integration.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/integration_fresh"
for dir in good corrupt inner torn; do mkdir "$E/runtime/fresh_$dir"; done
for spec in write:good reload:good corrupt:corrupt refuse:corrupt inner:inner refuse:inner torn:torn refuse:torn; do
 mode=${spec%%:*}; dir=${spec#*:}; run fresh_integration_${mode}_${dir} 0 "$E/bin/integration_fresh" "$mode" "$E/runtime/fresh_$dir" "$E/runtime/v92"
done
run fresh_integration_reload_final 0 "$E/bin/integration_fresh" reload "$E/runtime/fresh_good" "$E/runtime/v92"
sed 's|/runtime/baseline|/runtime/baseline_fresh|g' "$E/sources/$D/lane_d_baseline_driver.zag" > "$E/sources/$D/lane_d_baseline_driver.zag.routed"
mv "$E/sources/$D/lane_d_baseline_driver.zag.routed" "$E/sources/$D/lane_d_baseline_driver.zag"
run build_baseline_fresh 0 /Users/Shared/micah/Documents/zag/znc "$E/sources/$D/lane_d_baseline_driver.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/baseline"
run baseline_supervise_fresh 0 "$E/bin/baseline" supervise
for spec in "rows:$N/LANE_B_AUDIT_20260915/rows.zag" "structure:$N/LANE_B_AUDIT_20260915/structure.zag" "primitives:$N/LANE_B_AUDIT_20260915/primitives.zag" "r26:$N/r26_digest.zag" "r27:$N/r27_digest.zag" "v91tests:$N/V91_SEMANTIC_KAT/v91_semantic_kat_tests.zag" "v91rows:$N/V91_SEMANTIC_KAT/v91_emit_rows.zag" "v91gate:$N/V91_SEMANTIC_KAT/v91_admission_gate.zag"; do
 label=${spec%%:*}; src=${spec#*:}; freeze "$ROOT/$src"
 expected=0; [[ $label == v91tests || $label == v91rows ]] && expected=1
 run build_$label $expected /Users/Shared/micah/Documents/zag/znc "$E/sources/$src" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/$label"
done
for label in rows structure primitives; do run n17_$label 0 "$E/bin/$label"; done
run n17_r26_selftest 0 "$E/bin/r26" selftest
run n17_r26_digest 0 "$E/bin/r26" digest
run n17_r27_digest 0 "$E/bin/r27" digest
run n17_v91gate 91 "$E/bin/v91gate"
run match_r26 0 rg -x 'R26_NATIVE_DIGEST,44d36746ffb9e8d46080376a6e26bb824772d9d4b5e429add404195d02888649' "$E/logs/n17_r26_digest.stdout"
run match_r27 0 rg -x 'R27_NATIVE_DIGEST,562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04' "$E/logs/n17_r27_digest.stdout"
run protected_final 0 shasum -a 256 -c "$E/protected.sha256"
run canonical_final 0 shasum -a 256 -c "$E/canonical.sha256"
find "$E/sources" -type f -exec shasum -a 256 {} \; > "$E/source.sha256"
find "$E/bin" -type f -exec shasum -a 256 {} \; > "$E/binary.sha256"
cp /tmp/r33_integrate_followup.zsh "$E/followup.zsh"
