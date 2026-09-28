#!/bin/zsh
set -u
setopt PIPE_FAIL
REPO=/Users/Shared/micah/Documents/TNN/TNN
OWN=$REPO/Research/R33_NATIVE_N17_R27_CONTINUITY/V91_SEMANTIC_KAT
COMPILER=/Users/Shared/micah/Documents/zag/znc
E=${1:?usage: qualify_native.zsh NEW_EVIDENCE_DIRECTORY}
[[ ! -e "$E" ]] || exit 70
mkdir -p "$E/logs" "$E/projected" "$E/bin" "$E/inputs" "$E/nested_r23" "$E/author_sources" "$E/negative/missing_pages" "$E/negative/bad_manifest" "$E/negative/truncated_page" "$E/negative/corrupt_tensor" "$E/negative/truncated_tensor"
: > "$E/commands.tsv"
function run {
 local label=$1 expected=$2 role=$3
 shift 3
 printf '%s\n' "$@" > "$E/logs/$label.argv"
 "$@" > "$E/logs/$label.stdout" 2> "$E/logs/$label.stderr"
 local result=$?
 printf '%s\t%s\t%s\t%s\n' "$label" "$result" "$expected" "$role" >> "$E/commands.tsv"
 printf '%s\n' "$result" > "$E/logs/$label.exit"
 [[ $result == $expected ]] || { print -u2 "unexpected exit $label: $result expected $expected"; exit 71; }
}
function build {
 local label=$1 source=$2
 run project_$label 0 native_projection "$E/bin/project" "$OWN/$source" "$E/projected/$label.zag" "$E/projected/$label.provenance"
 run build_$label 0 native_build "$COMPILER" "$E/projected/$label.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/$label"
}
for source in "$OWN"/*.zag "$OWN/qualify_native.zsh"; do cp "$source" "$E/author_sources/$(basename "$source")" || exit 72; done
run compiler_identity 0 exact_compiler_input shasum -a 256 "$COMPILER"
run canonical_before 0 protected_input_identity shasum -a 256 "$REPO/Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-state.pkl" "$REPO/Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-policy.json"
run build_project 0 native_build "$COMPILER" "$OWN/v91_project_native.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/project"
build layout v91_allocation_probe.zag
build oracle v91_oracle_custody_runner.zag
build extract v91_retained_extract.zag
build numeric v91_numeric_components_tests.zag
build bpe v91_bpe_components_tests.zag
build negative v91_negative_admission.zag
build rows_test v91_semantic_kat_tests.zag
build rows_emit v91_emit_rows.zag
build gate v91_admission_gate.zag
build record v91_record.zag
run layout 0 compiler_layout_qualification "$E/bin/layout"
run extract 0 retained_tensor_bpe_custody "$E/bin/extract" "$E/inputs"
run extract_nested_r23 0 ancestor_retained_tensor_bpe_custody "$E/bin/extract" "$E/nested_r23" --nested-r23
for input in "$E/inputs"/*; do run "retention_$(basename "$input")" 0 exact_retained_input_equality cmp "$input" "$E/nested_r23/$(basename "$input")"; done
run oracle 0 original_nested_oracle_custody "$E/bin/oracle" "$E/inputs"
run oracle_repeat 0 custody_repeat "$E/bin/oracle" "$E/inputs"
run oracle_repeat_equal 0 custody_repeat_equality cmp "$E/logs/oracle.stdout" "$E/logs/oracle_repeat.stdout"
run numeric 0 isolated_numeric_components "$E/bin/numeric" "$E/inputs"
run numeric_repeat 0 isolated_components_repeat "$E/bin/numeric" "$E/inputs"
run numeric_repeat_equal 0 component_repeat_equality cmp "$E/logs/numeric.stdout" "$E/logs/numeric_repeat.stdout"
run bpe 0 bpe_graph_components "$E/bin/bpe" "$E/inputs/bpe.framed.bin"
run rows_test 1 failed_author_reconstruction "$E/bin/rows_test"
run rows_emit 1 failed_author_reconstruction "$E/bin/rows_emit"
run gate 91 closed_gate_with_real_oracle "$E/bin/gate" "$E/inputs"
run gate_no_input 91 closed_gate_no_inputs "$E/bin/gate"
run gate_fake_receipt 91 anti_fake_supplied_oracle "$E/bin/gate" --generated "$E/inputs/oracle.framed.bin"
MAP=$REPO/Research/R33_NATIVE_N10_RUN_PRIMARY_V1/parent-map
run copy_missing_manifest 0 negative_fixture_setup cp "$MAP/manifest.bin" "$E/negative/missing_pages/manifest.bin"
run copy_bad_manifest 0 negative_fixture_setup cp "$MAP/manifest.bin" "$E/negative/bad_manifest/manifest.bin"
run corrupt_manifest 0 negative_fixture_setup dd if=/dev/zero of="$E/negative/bad_manifest/manifest.bin" bs=1 count=8 conv=notrunc
run copy_truncated_manifest 0 negative_fixture_setup cp "$MAP/manifest.bin" "$E/negative/truncated_page/manifest.bin"
run truncate_page 0 negative_fixture_setup dd if="$MAP/nodes-1.bin" of="$E/negative/truncated_page/nodes-1.bin" bs=1 count=63
run refuse_missing_pages 0 native_byte_table_negative_admission "$E/bin/negative" "$E/negative/missing_pages"
run refuse_corrupt_manifest 0 native_byte_table_negative_admission "$E/bin/negative" "$E/negative/bad_manifest"
run refuse_truncated_page 0 native_byte_table_negative_admission "$E/bin/negative" "$E/negative/truncated_page"
for input in "$E/inputs"/*.f32le; do cp "$input" "$E/negative/corrupt_tensor/"; cp "$input" "$E/negative/truncated_tensor/"; done
run corrupt_tensor 0 negative_fixture_setup dd if=/dev/zero of="$E/negative/corrupt_tensor/emb.weight.f32le" bs=65664 count=1
run truncate_tensor 0 negative_fixture_setup dd if="$E/inputs/emb.weight.f32le" of="$E/negative/truncated_tensor/emb.weight.f32le" bs=1 count=63
run refuse_corrupt_tensor 20 tensor_hash_negative_admission "$E/bin/numeric" "$E/negative/corrupt_tensor"
run refuse_truncated_tensor 20 tensor_extent_negative_admission "$E/bin/numeric" "$E/negative/truncated_tensor"
run bad_bpe_fixture 0 negative_fixture_setup dd if=/dev/zero of="$E/negative/bpe.corrupt.bin" bs=3946 count=1
run refuse_bad_bpe 10 bpe_hash_negative_admission "$E/bin/bpe" "$E/negative/bpe.corrupt.bin"
run canonical_after 0 protected_input_identity shasum -a 256 "$REPO/Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-state.pkl" "$REPO/Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-policy.json"
run canonical_unchanged 0 protected_input_equality cmp "$E/logs/canonical_before.stdout" "$E/logs/canonical_after.stdout"
run diff_check 0 owned_source_whitespace git -C "$REPO" diff --check -- Research/R33_NATIVE_N17_R27_CONTINUITY/V91_SEMANTIC_KAT
: > "$E/files.tsv"
for p in "$E/author_sources"/*; do printf 'frozen_author_source\t%s\n' "$p" >> "$E/files.tsv"; done
for p in "$E/projected"/*; do printf 'frozen_projected_closure\t%s\n' "$p" >> "$E/files.tsv"; done
awk -F '\t' '/^FILE\t/ {print $3}' "$E"/projected/*.provenance | sort -u > "$E/import_paths.txt"
while IFS= read -r dep; do
 rel=${dep/}; target="$E/import_closure/$rel"
 mkdir -p "$(dirname "$target")"; cp "$dep" "$target" || exit 72
 printf 'frozen_native_import_source\t%s\n' "$target" >> "$E/files.tsv"
done < "$E/import_paths.txt"
for p in "$E/bin"/*; do printf 'native_binary\t%s\n' "$p" >> "$E/files.tsv"; done
for p in "$E/inputs"/* "$E/nested_r23"/*; do printf 'native_extracted_exact_input\t%s\n' "$p" >> "$E/files.tsv"; done
for p in "$MAP"/*; do printf 'admitted_parent_map_member\t%s\n' "$p" >> "$E/files.tsv"; done
printf 'stable_compiler\t%s\n' "$COMPILER" >> "$E/files.tsv"
printf 'exact_parent_serialization\t%s\n' "$REPO/Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-state.pkl" >> "$E/files.tsv"
printf 'command_journal\t%s\n' "$E/commands.tsv" >> "$E/files.tsv"
# Record serialization is silent. Predeclare this final journal row, then
# require the observed exit to agree; its empty stdout/stderr hashes are stable.
label=serialize_record
printf '%s\n' "$E/bin/record" "$E" "$E/files.tsv" > "$E/logs/$label.argv"
: > "$E/logs/$label.stdout"; : > "$E/logs/$label.stderr"
printf '%s\t0\t0\tnative_record_serialization\n' "$label" >> "$E/commands.tsv"
"$E/bin/record" "$E" "$E/files.tsv" > "$E/logs/$label.stdout" 2> "$E/logs/$label.stderr"
result=$?; printf '%s\n' "$result" > "$E/logs/$label.exit"
[[ $result == 0 ]] || exit 73
print "$E"
