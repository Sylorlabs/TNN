#!/bin/zsh
set -u
setopt PIPE_FAIL

REPO=/Users/Shared/micah/Documents/TNN/TNN
OWN=$REPO/Research/R33_NATIVE_N17_R27_CONTINUITY/V91_SEMANTIC_KAT
COMPILER=/Users/Shared/micah/Documents/zag/znc
PROJECT=$OWN/recovery_exact_20260917/work/project
RECOVERED=$OWN/recovery_exact_20260917/r23_experiments.py
OLD=$OWN/evidence/RECOVERY_20260915_BOUND_FINAL/QUAL_20260915_BOUND_FINAL/inputs
FROZEN_REF=$OWN/evidence/RECOVERY_20260915_BOUND_FINAL/QUAL_20260915_BOUND_FINAL/logs/canonical_before.stdout
CANON_STATE=$REPO/Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-state.pkl
CANON_POLICY=$REPO/Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-policy.json
E=${1:?usage: qualify_native_generator_recovery.zsh NEW_EVIDENCE_DIRECTORY}

[[ ! -e "$E" ]] || exit 70
mkdir -p "$E/logs" "$E/projected" "$E/bin" "$E/author_sources" "$E/historical_source" "$E/inputs" "$E/generated"
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
  run project_$label 0 native_projection "$PROJECT" "$OWN/$source" "$E/projected/$label.zag" "$E/projected/$label.provenance"
  run build_$label 0 native_build "$COMPILER" "$E/projected/$label.zag" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/$label"
}

for source in \
  r25_blake2b64_v1.zag \
  r23_blake2b64_person_v1.zag \
  r25_mt19937_v1.zag \
  v91_semantic_kat.zag \
  v91_condition_frame_emit.zag \
  v91_numeric_components.zag \
  v91_native_naive_v1.zag \
  v91_native_naive_emit.zag \
  v91_native_naive_compare.zag \
  qualify_native_generator_recovery.zsh; do
  cp "$OWN/$source" "$E/author_sources/$source" || exit 72
done
cp "$RECOVERED" "$E/historical_source/r23_experiments.py" || exit 72

for leaf in \
  emb.weight.f32le ch.weight.f32le ch.bias.f32le ce.weight.f32le ce.bias.f32le \
  rnn.weight_ih_l0.f32le rnn.weight_hh_l0.f32le rnn.bias_ih_l0.f32le rnn.bias_hh_l0.f32le \
  out.weight.f32le out.bias.f32le bpe.framed.bin oracle.framed.bin; do
  cp "$OLD/$leaf" "$E/inputs/$leaf" || exit 72
done
cp "$FROZEN_REF" "$E/logs/canonical_frozen_reference.stdout" || exit 72

run compiler_identity 0 exact_compiler_input shasum -a 256 "$COMPILER"
run projector_identity 0 exact_projector_input shasum -a 256 "$PROJECT"
run recovered_r23_identity 0 exact_historical_source shasum -a 256 "$RECOVERED"
run old_input_identities 0 retained_and_oracle_input_identity shasum -a 256 \
  "$E/inputs/emb.weight.f32le" "$E/inputs/ch.weight.f32le" "$E/inputs/ch.bias.f32le" \
  "$E/inputs/ce.weight.f32le" "$E/inputs/ce.bias.f32le" \
  "$E/inputs/rnn.weight_ih_l0.f32le" "$E/inputs/rnn.weight_hh_l0.f32le" \
  "$E/inputs/rnn.bias_ih_l0.f32le" "$E/inputs/rnn.bias_hh_l0.f32le" \
  "$E/inputs/out.weight.f32le" "$E/inputs/out.bias.f32le" "$E/inputs/bpe.framed.bin" "$E/inputs/oracle.framed.bin"
run canonical_before 0 protected_input_identity shasum -a 256 "$CANON_STATE" "$CANON_POLICY"
run canonical_matches_frozen 0 protected_input_equality cmp "$E/logs/canonical_before.stdout" "$E/logs/canonical_frozen_reference.stdout"

build conditions v91_condition_frame_emit.zag
build inference v91_native_naive_emit.zag
build compare v91_native_naive_compare.zag

# Fail closed if the isolated inference closure contains any oracle/custody hook.
run inference_oracle_scan_author 1 structural_isolation rg -n \
  'v91_expected_naive|V91ORC01|oracle\.framed|v91_semantic_kat|lena moved the key|historical_naive_custody' \
  "$E/author_sources/v91_native_naive_v1.zag" "$E/author_sources/v91_native_naive_emit.zag"
run inference_oracle_scan_projected 1 structural_isolation rg -n \
  'v91_expected_naive|V91ORC01|oracle\.framed|v91_semantic_kat|lena moved the key|historical_naive_custody' \
  "$E/projected/inference.zag"

run conditions 0 native_condition_reconstruction "$E/bin/conditions" "$E/inputs/conditions.framed.bin"
run inference 0 isolated_native_inference "$E/bin/inference" "$E/inputs" "$E/inputs/conditions.framed.bin" "$E/generated/native_naive.framed.bin"
run inference_repeat 0 deterministic_native_inference "$E/bin/inference" "$E/inputs" "$E/inputs/conditions.framed.bin" "$E/generated/native_naive.repeat.framed.bin"
run inference_deterministic 0 generated_artifact_equality cmp "$E/generated/native_naive.framed.bin" "$E/generated/native_naive.repeat.framed.bin"
run compare 0 posthoc_oracle_comparison "$E/bin/compare" "$E/generated/native_naive.framed.bin" "$E/inputs/oracle.framed.bin"

run require_condition_rows 0 evidence_assertion grep -Fx 'V91_CONDITION_ROWS,16' "$E/logs/conditions.stdout"
run require_train 0 evidence_assertion grep -Fx 'V91_RAW_TRAIN,3626' "$E/logs/conditions.stdout"
run require_test 0 evidence_assertion grep -Fx 'V91_RAW_TEST,622' "$E/logs/conditions.stdout"
run require_generated16 0 evidence_assertion grep -Fx 'V91_ACTUAL_NATIVE_GENERATED,16' "$E/logs/inference.stdout"
run require_generated16_repeat 0 evidence_assertion grep -Fx 'V91_ACTUAL_NATIVE_GENERATED,16' "$E/logs/inference_repeat.stdout"
run require_matches16 0 evidence_assertion grep -Fx 'V91_NATIVE_ORACLE_MATCHES,16' "$E/logs/compare.stdout"
run require_failures0 0 evidence_assertion grep -Fx 'V91_NATIVE_ORACLE_FAILURES,0' "$E/logs/compare.stdout"

run generated_identity 0 generated_artifact_identity shasum -a 256 "$E/generated/native_naive.framed.bin"
run condition_identity 0 condition_artifact_identity shasum -a 256 "$E/inputs/conditions.framed.bin"
run canonical_after 0 protected_input_identity shasum -a 256 "$CANON_STATE" "$CANON_POLICY"
run canonical_unchanged 0 protected_input_equality cmp "$E/logs/canonical_before.stdout" "$E/logs/canonical_after.stdout"

cat > "$E/RECEIPT.txt" <<'EOF'
V91_NATIVE_GENERATOR_RECOVERY_V1
scope=historical_naive_n1_generator_parity
conditions_reconstructed=16
raw_train=3626
raw_test=622
actual_native_generated=16
oracle_matches=16
oracle_failures=0
native_frame_deterministic=true
naive_n1_generator_parity=true
inference_oracle_import=false
historical_python_executed=false
foreign_ml_runtime_used=false
canonical_r27_mutated=false
learn_authority_granted=false
successor_promoted=false
roundtrip_n128_parity=false
full_v91_generator_semantics_complete=false
v91_naive_lane_open=true
v91_full_gate_open=false
EOF

(cd "$E" && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 shasum -a 256 > SHA256SUMS) || exit 73
(cd "$E" && shasum -a 256 -c SHA256SUMS) > "$E/SHA256_VERIFY.txt" 2>&1 || exit 74
chmod -R a-w "$E" || exit 75
print "$E"
