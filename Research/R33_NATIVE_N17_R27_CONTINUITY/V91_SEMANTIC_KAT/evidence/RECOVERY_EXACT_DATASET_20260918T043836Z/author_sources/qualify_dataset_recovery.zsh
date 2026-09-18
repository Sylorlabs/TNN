#!/bin/zsh
set -u
setopt PIPE_FAIL

REPO=/Users/Shared/micah/Documents/TNN/TNN
OWN=$REPO/Research/R33_NATIVE_N17_R27_CONTINUITY/V91_SEMANTIC_KAT
COMPILER=/Users/Shared/micah/Documents/zag/znc
PROJECT=$OWN/recovery_exact_20260917/work/project
RECOVERED=$OWN/recovery_exact_20260917/r23_experiments.py
FROZEN_REF=$OWN/evidence/RECOVERY_20260915_BOUND_FINAL/QUAL_20260915_BOUND_FINAL/logs/canonical_before.stdout
CANON_STATE=$REPO/Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-state.pkl
CANON_POLICY=$REPO/Research/R33_PARENT_RECOVERED_V1/parent-r27-accepted-policy.json
E=${1:?usage: qualify_dataset_recovery.zsh NEW_EVIDENCE_DIRECTORY}

[[ ! -e "$E" ]] || exit 70
mkdir -p "$E/logs" "$E/projected" "$E/bin" "$E/author_sources" "$E/historical_source"
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
  r23_blake2b64_person_tests.zag \
  r25_mt19937_v1.zag \
  v91_semantic_kat.zag \
  v91_semantic_kat_tests.zag \
  v91_emit_rows.zag \
  qualify_dataset_recovery.zsh; do
  cp "$OWN/$source" "$E/author_sources/$source" || exit 72
done
cp "$RECOVERED" "$E/historical_source/r23_experiments.py" || exit 72
cp "$FROZEN_REF" "$E/logs/canonical_frozen_reference.stdout" || exit 72

run compiler_identity 0 exact_compiler_input shasum -a 256 "$COMPILER"
run recovered_r23_identity 0 exact_historical_source shasum -a 256 "$RECOVERED"
run canonical_before 0 protected_input_identity shasum -a 256 "$CANON_STATE" "$CANON_POLICY"
run canonical_matches_frozen 0 protected_input_equality cmp "$E/logs/canonical_before.stdout" "$E/logs/canonical_frozen_reference.stdout"

build blake2_kat r23_blake2b64_person_tests.zag
build rows_test v91_semantic_kat_tests.zag
build rows_emit v91_emit_rows.zag

run blake2_kat 0 native_blake2_qualification "$E/bin/blake2_kat"
run rows_test 0 native_dataset_order_qualification "$E/bin/rows_test"
run rows_emit 0 native_reconstructed_rows_evidence "$E/bin/rows_emit"

run require_blake_empty 0 evidence_assertion grep -Fx 'BLAKE2B64_EMPTY_KAT,PASS' "$E/logs/blake2_kat.stdout"
run require_blake_abc 0 evidence_assertion grep -Fx 'BLAKE2B64_ABC_KAT,PASS' "$E/logs/blake2_kat.stdout"
run require_person_fixture 0 evidence_assertion grep -Fx 'R23_PERSONALIZED_FIXTURE,1f9d6d837c4418f0' "$E/logs/blake2_kat.stdout"
run require_person_mod7 0 evidence_assertion grep -Fx 'R23_PERSONALIZED_MOD7,6' "$E/logs/blake2_kat.stdout"
run require_counts 0 evidence_assertion grep -Fx 'V91_RAW_TRAIN,3626' "$E/logs/rows_test.stdout"
run require_holdout_count 0 evidence_assertion grep -Fx 'V91_RAW_TEST,622' "$E/logs/rows_test.stdout"
run require_rows16 0 evidence_assertion grep -Fx 'V91_RECONSTRUCTED_ROWS_MATCHED,16' "$E/logs/rows_test.stdout"
run require_failures0 0 evidence_assertion grep -Fx 'V91_FAILURES,0' "$E/logs/rows_test.stdout"
run require_generated0 0 evidence_assertion grep -Fx 'V91_GENERATED_OUTPUTS,0' "$E/logs/rows_test.stdout"

run canonical_after 0 protected_input_identity shasum -a 256 "$CANON_STATE" "$CANON_POLICY"
run canonical_unchanged 0 protected_input_equality cmp "$E/logs/canonical_before.stdout" "$E/logs/canonical_after.stdout"

cat > "$E/RECEIPT.txt" <<'EOF'
V91_DATASET_RECOVERY_V1
scope=hash_primitive_dataset_split_and_first16_intended_rows
blake2_kat_pass=true
personalized_fixture_match=true
personalized_fixture_hex=1f9d6d837c4418f0
personalized_fixture_mod7=6
raw_train=3626
raw_test=622
intended_rows_matched=16
generated_outputs=0
generator_parity=false
v91_gate_open=false
canonical_r27_mutated=false
learn_authority_granted=false
historical_python_executed=false
foreign_ml_runtime_used=false
zag_u64_logical_shift_workaround=true
zag_u64_unsigned_mod7_workaround=true
EOF

(cd "$E" && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 shasum -a 256 > SHA256SUMS) || exit 73
(cd "$E" && shasum -a 256 -c SHA256SUMS) > "$E/SHA256_VERIFY.txt" 2>&1 || exit 74
chmod -R a-w "$E" || exit 75
print "$E"
