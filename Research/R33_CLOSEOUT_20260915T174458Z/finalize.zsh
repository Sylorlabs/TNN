#!/bin/zsh
set -eu
ROOT=/Users/Shared/micah/Documents/TNN/TNN
cd "$ROOT"
E=$(cat /tmp/r33_integrator_evidence_path)
REL=${E#$ROOT/}
cp "$E/commands.jsonl" "$E/commands.raw_serialization_witness.jsonl"
# All recorded arguments are whitespace-free paths/flags/digest patterns. Repair
# the zsh display-only joining escape; executions used the correct "$@" argv.
jq -c '.command |= gsub("\\\\ ";" ") | .argv=(.command|split(" > ")[0]|split(" "))' "$E/commands.raw_serialization_witness.jsonl" > "$E/commands.jsonl"
cp /tmp/r33_finalize.zsh "$E/finalize.zsh"
N=Research/R33_NATIVE_N17_R27_CONTINUITY
H=Research/R33_NATIVE_N19_RUNTIME_BOUNDARY
D=Research/R33_CONTINUING_LIFE_V1
mkdir "$E/final_status"
for file in "$N/STATUS.json" "$H/STATUS.json" "$H/INTEGRATION_REVIEW_20260915.md" "$D/CURRENT_ENTRY_POINT.md" "$D/WORKLOG.md" "$D/lane_d_packet_integration.zag" "$N/V92_STATE_IMAGE_QUAL/README.md"; do
 mkdir -p "$E/final_status/${file:h}"
 cp "$file" "$E/final_status/$file"
done
cp "$ROOT/$D/lane_d_baseline_driver.zag" "$E/probe_sources/baseline_original.zag"
sed -e "s|Research/R33_CONTINUING_LIFE_V1/LANE_D_20260915/BASELINE_RUNTIME|$REL/runtime/baseline|g" -e "s|$ROOT/Research/R33_CONTINUING_LIFE_V1/LANE_D_20260915/baseline_driver|$E/bin/baseline|g" "$E/probe_sources/baseline_original.zag" > "$E/probe_sources/baseline_initial_routed.zag"
diff -u "$E/probe_sources/integration_hardcoded.zag" "$D/lane_d_packet_integration.zag" > "$E/integration.source.diff" || [[ $? == 1 ]]
git diff > "$E/git.after.diff"
git status --short > "$E/git.after.status"
git diff --check > "$E/git.diff_check.stdout" 2> "$E/git.diff_check.stderr"
print 0 > "$E/git.diff_check.exit"
cmp "$E/git.before.diff" "$E/git.after.diff" > "$E/tracked_diff_unchanged.stdout" 2> "$E/tracked_diff_unchanged.stderr"
print 0 > "$E/tracked_diff_unchanged.exit"
shasum -a 256 -c "$E/canonical.sha256" > "$E/canonical.closeout.stdout" 2> "$E/canonical.closeout.stderr"
print 0 > "$E/canonical.closeout.exit"
shasum -a 256 -c "$E/protected.sha256" > "$E/protected.closeout.stdout" 2> "$E/protected.closeout.stderr"
print 0 > "$E/protected.closeout.exit"
shasum -a 256 -c "$E/read_only_map_inputs.sha256" > "$E/map.closeout.stdout" 2> "$E/map.closeout.stderr"
print 0 > "$E/map.closeout.exit"
find "$E/probe_sources" -type f -exec shasum -a 256 {} \; > "$E/probe_sources.sha256"
for name in source binary probe_sources protected canonical read_only_map_inputs; do
 jq -Rn '[inputs | capture("^(?<sha256>[0-9a-f]{64})  (?<path>.*)$")]' "$E/$name.sha256" > "$E/$name.hashes.json"
done
jq -s --arg date "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg evidence "$REL" --slurpfile sources "$E/source.hashes.json" --slurpfile binaries "$E/binary.hashes.json" --slurpfile probes "$E/probe_sources.hashes.json" --slurpfile protected "$E/protected.hashes.json" --slurpfile canonical "$E/canonical.hashes.json" --slurpfile maps "$E/read_only_map_inputs.hashes.json" --slurpfile audit "$E/N17_LANE_B_AUDIT_WITNESS.json" '
{
 schema_version:1,identity:"R33_INTEGRATED_NATIVE_ENGINEERING_CLOSEOUT",date_utc:$date,evidence_directory:$evidence,status:"FAIL_CLOSED_FULL_R33_NOT_COMPLETE",
 scientific_exposure:0,canonical_r27_mutated:false,learner_authority_granted:false,learn_invoked_by_integrator:false,learn_status:"FAIL_CLOSED_SOURCE_REFUSAL_INSPECTED_NO_INVOCATION",successor_promoted:false,
 compiler:{path:"/Users/Shared/micah/Documents/zag/znc",sha256:"3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956",replaced:false},canonical_r27:{step:60423,newborn_restarts:0,raw_and_policy_hashes:$canonical[0],current_state_and_registry_preservation:$protected[0],claim_boundary:"Raw canonical serialization hashed only, never deserialized or mutated; values agree with preserved current-state record."},
 commands:map(. + {claim_role:(if .label=="baseline_supervise" or .label=="build_baseline" or .label=="build_integration" or (.label|startswith("integration_")) then "EXCLUDED_SUPERSEDED_PROBE" elif (.label|startswith("build_v91")) or .label=="n17_v91gate" or .label=="v68" or .label=="v73" then "DIRECT_FAIL_CLOSED_BLOCKER_EVIDENCE" else "CURRENT_ENGINEERING_EVIDENCE" end)}),
 source_sha256:$sources[0],binary_sha256:$binaries[0],excluded_probe_source_sha256:$probes[0],read_only_map_input_sha256:$maps[0],
 V68:{status:"BLOCKED",exit_code:1,failures:7,first_section_status:2002,observed_offset:1876189488,minimal_blocker:"Original multi-slice caller must pass unchanged V68 and V73 with the stable compiler; successful single-output integration does not qualify this caller. No compiler root cause established."},
 V71:{status:"PASS",exit_code:0,four_call_forms:true},V73:{status:"BLOCKED",exit_code:1,rc:81},
 V92:{status:"PASS_ENGINEERING_ONLY",expanded_selftest_passes:339,selftest_failures:0,all_13_mode_exits:0,fresh_valid_packet:"PASS_EXACT_IMAGE_AND_INTEGRITY",corrupt_packet:"PASS_EXPECTED_REFUSAL",truncated_packet:"PASS_EXPECTED_REFUSAL",image_bytes:245472,packet_bytes:245536,claim_boundary:"Fresh synthetic engineering V4 image/packet; not canonical behavioral projection or full verifier equivalence."},
 continuing_life:{status:"PASS_NARROW_FRESH_PACKET_TRANSPORT_AND_BASELINE",baseline_five_child_regression_exit:0,packet_source:"This evidence directory runtime/v92/learner-packet.bin generated by rebuilt V92",source_change:"Explicit argv[3] packet root required; argc=4; removed hardcoded historical fixture path",fresh_packet_mode_exits:0,outer_bytes:245924,qualified:["whole_record_and_packet_exact_recovery","inner_and_outer_integrity","outer_corrupt_refusal","resigned_inner_corrupt_refusal","torn_refusal","unchanged_caller_output_on_refusal","checked_commit_refusal","pending_credit_world_ingress_retention","delayed_continuation"],excluded_probes:["Initial bridge used the old lane fixture and is excluded from fresh integrated admission.","Initial baseline precreated-root supervise exit 80; corrected absent-root rerun passes; original result retained."]},
 N17:{status:"FAIL_CLOSED",r26_digest:"44d36746ffb9e8d46080376a6e26bb824772d9d4b5e429add404195d02888649",r27_digest:"562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04",fresh_integrator_native_static_rows:38,static_negative_controls:"PASS",lane_b_static_accounting:$audit[0].accounting,source_row_blockers:$audit[0].unresolved_source_rows,terminal_blocker_count:32,v91:$audit[0].v91,r25:$audit[0].r25,independent_terminal_closure_review:"NOT_OBTAINED",full_runtime_equivalence_passes:0,historical_metrics_regenerated:false},
 N19:{status:"PASS_WITH_NARROW_SCOPE_REPAIRED_CURRENT_ONLY",historical_build_08:"REQUEST_CHANGES_HOST_PROBE_IO_MISCLASSIFICATION",independent_review:"N19_INDEPENDENT_REVIEW_V3.md Lane C; pinned repaired binaries reproduced exactly",integration_review:"Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/INTEGRATION_REVIEW_20260915.md",host_tests_exit:0,crash_matrix_exit:0,crash_matrix_failures:0,crash_phases:5,direct_children_reaped:11,second_wait_required:-10,resource:{limit_bytes:32,observed_bytes:32,signal:25,cpu_us:672,peak_rss_bytes:1490944},host_probe_closed_root_status:-1905,operational_refusals_exit:1,asserted_expected_refusals_exit:0,remaining_narrow_blockers:[]},
 remaining_blockers:["V68 seven failures and V73 RC81 on original multi-slice caller under fixed stable compiler", "N17 30 required source-row deficits (7 R27, 23 R26), including R25 lineage without native replacement", "V91 retained native generator/inference/BPE/seeded sampler must reproduce all 16 exact bound strings; test allocation fixes or oracle emission alone cannot close parity", "Fresh independent terminal verifier-equivalence closure review"],
 claim_boundary:"Engineering mechanics only. R33 remains fail-closed; no complete R27 behavioral runtime or historical verifier equivalence claimed. Lane historical receipts are witnesses only. N17 lane static accounting is distinguished from integrator native rerun rows.",
 scope_exclusions:["Python execution","PyTorch","NumPy","pickle/reducer execution","historical Python verifier execution","foreign ML runtime","learning/training","learner callbacks or credit application","scientific exposure","successor promotion","canonical R27 mutation","equal-comparison LLM superiority claim","physical audio/vision/timing qualification","power-loss durability","host-admin rollback protection","descendant process-group containment","concurrent hostile same-user races","exhaustive socket/device failures","CPU ceiling enforcement","interrupted wait fallback","fresh-root identity authentication"],
 verification:{json_syntax_command:"jq -e . final_closeout.json",receipts:"verification.json; SHA256SUMS; manifest verification receipt",git_diff_check_exit:0,tracked_diff_unchanged_from_campaign_start:true,canonical_and_policy_hash_check_exit:0,protected_state_registry_compiler_check_exit:0,read_only_map_check_exit:0},
 next_engineering_frontier:"Fix original caller shape/lowering with the stable compiler, obtain exact missing release/member/policy/media/lineage inputs and reviewed native runtime replacements for the explicit N17 rows, implement native V91 generator parity, then obtain independent terminal equivalence review. No authority/exposure granted by this task."
}' "$E/commands.jsonl" > "$E/final_closeout.json"
