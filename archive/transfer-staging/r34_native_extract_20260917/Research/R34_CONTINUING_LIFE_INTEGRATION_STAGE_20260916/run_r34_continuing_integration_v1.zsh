#!/bin/zsh
set -eu

HERE=${0:A:h}
ROOT=${TNN_ROOT:-/Users/Shared/micah/Documents/TNN/TNN}
CL=$ROOT/Research/R33_CONTINUING_LIFE_V1
N17=$ROOT/Research/R33_NATIVE_N17_R27_CONTINUITY
EXPECTED_COMPILER_SHA=3093d12dba9cc81b1dee69d2d4e604158d093b58f8f01ddab26c0f4297029956
ZNC=${TNN_ZNC:-}
if [[ -z "$ZNC" ]]; then
  if [[ -x /Users/Shared/micah/Documents/Zag/znc ]]; then ZNC=/Users/Shared/micah/Documents/Zag/znc
  elif [[ -x /Users/Shared/micah/Documents/zag/znc ]]; then ZNC=/Users/Shared/micah/Documents/zag/znc
  else print -u2 -- 'pinned Zag compiler not found'; exit 70
  fi
fi
OUT_ROOT=${TNN_R34_CONTINUING_EVIDENCE_ROOT:-"$HERE/EVIDENCE"}
stamp=$(date -u '+%Y%m%dT%H%M%SZ')
OUT="$OUT_ROOT/$stamp"
mkdir -p "$OUT" "$OUT/run1" "$OUT/run2"

hash_only() { shasum -a 256 "$1" | awk '{print $1}'; }
hash_line() { shasum -a 256 "$1"; }
require_hash() {
  local file=$1 expected=$2
  [[ -f "$file" ]] || { print -u2 -- "missing dependency: $file"; exit 71; }
  local got=$(hash_only "$file")
  [[ "$got" == "$expected" ]] || { print -u2 -- "dependency hash mismatch: $file $got"; exit 72; }
}

[[ -x "$ZNC" ]] || { print -u2 -- "compiler not executable: $ZNC"; exit 73; }
[[ "$(hash_only "$ZNC")" == "$EXPECTED_COMPILER_SHA" ]] || { print -u2 -- 'compiler SHA mismatch'; exit 74; }
[[ -f "$CL/checkpoint.zag" && -f "$CL/world.zag" ]] || { print -u2 -- 'R33 continuing-life base files missing'; exit 75; }
[[ -f "$CL/r33_fresh_process_equivalence_v1.zag" ]] || { print -u2 -- 'R33 V71 source missing'; exit 76; }

require_hash "$CL/r33_live_outer_checkpoint_binding_v1.zag" 2d7d233929e1cfe8821baeff8b73d42df386edfdbe9d4fa9cd716bbf2a72a113
require_hash "$CL/r33_pending_credit_relation_v1.zag" 11a1f2b3a2c93ee46f1160a6f5de3993622fba71d8cf37a1f0d745cb3095596a
require_hash "$N17/r27_native_state_sections_v4.zag" ee86ce84cb27981025e02d21407dde92b5ebff831a0d9b564a420767a64068af
require_hash "$N17/r27_native_state_image_v4.zag" 22c267dcfd928c49646749c1896415d781a03688d5857b282da9edbea9834ce1
require_hash "$N17/r27_native_state_semantics_v4.zag" 77ec25fc9f6aca2aa26137f978be7982d4eeaa7a648b05ac3758ce414c1e0cda
require_hash "$N17/r33_continuing_learner_checkpoint_v1.zag" d3b013806459923a16a75de2a6a93d003ed0f9afca47560d294dd62e44614f08
require_hash "$N17/r33_packet_sha256_v1.zag" 28bf9e7bc1561978b4efe1a9cd2b929912e649187fd006d646817abd945e5fe1
require_hash "$N17/V68_PROJECTION_RECEIPT/r27_projection_receipt_v2.zag" a216a1f609d86ab4505fb7d5d3e7058673682dc0152db3c1f549688ab48762d6
require_hash "$CL/r33_fresh_process_equivalence_v1.zag" 75ec2005c731467a452b915d6ca834da9f6138bd4dc1fe5e15f4d478d5f2ffc3

FLAGS=(--target macos-arm64 --no-zagd --no-analyze --no-foreground-cache)
# Requalify the exact inherited continuing-life boundary before adding R34 state.
mkdir -p "$OUT/r33_v71_case"
"$ZNC" "$CL/r33_fresh_process_equivalence_v1.zag" $FLAGS -o "$OUT/r33_v71" >"$OUT/r33_v71.compile.stdout" 2>"$OUT/r33_v71.compile.stderr"
"$OUT/r33_v71" supervise "$OUT/r33_v71_case" >"$OUT/r33_v71.stdout" 2>"$OUT/r33_v71.stderr"
grep -Fq 'R33_FRESH_PROCESS_EQUIVALENCE_V71_FAILURES,0' "$OUT/r33_v71.stdout" || { print -u2 -- 'R33 V71 prerequisite failed'; exit 77; }

compile_one() {
  local src=$1 bin=$2 stem=$3
  "$ZNC" "$src" $FLAGS -o "$bin" >"$OUT/$stem.compile.stdout" 2>"$OUT/$stem.compile.stderr"
}
compile_one "$HERE/r34_native_sidecar_v1_tests.zag" "$OUT/sidecar_tests" sidecar
compile_one "$HERE/r34_continuing_envelope_v1_tests.zag" "$OUT/envelope_tests" envelope
compile_one "$HERE/r34_fresh_process_equivalence_v1.zag" "$OUT/r34_fresh_v1" fresh

"$OUT/sidecar_tests" >"$OUT/sidecar.run1.stdout" 2>"$OUT/sidecar.run1.stderr"
"$OUT/sidecar_tests" >"$OUT/sidecar.run2.stdout" 2>"$OUT/sidecar.run2.stderr"
cmp "$OUT/sidecar.run1.stdout" "$OUT/sidecar.run2.stdout"
cmp "$OUT/sidecar.run1.stderr" "$OUT/sidecar.run2.stderr"
grep -Fqx 'R34_NATIVE_SIDECAR_V1_FAILURES,0' "$OUT/sidecar.run1.stdout"

"$OUT/envelope_tests" >"$OUT/envelope.run1.stdout" 2>"$OUT/envelope.run1.stderr"
"$OUT/envelope_tests" >"$OUT/envelope.run2.stdout" 2>"$OUT/envelope.run2.stderr"
cmp "$OUT/envelope.run1.stdout" "$OUT/envelope.run2.stdout"
cmp "$OUT/envelope.run1.stderr" "$OUT/envelope.run2.stderr"
grep -Fqx 'R34_CONTINUING_ENVELOPE_V1_FAILURES,0' "$OUT/envelope.run1.stdout"

"$OUT/r34_fresh_v1" supervise "$OUT/run1" >"$OUT/fresh.run1.stdout" 2>"$OUT/fresh.run1.stderr"
"$OUT/r34_fresh_v1" supervise "$OUT/run2" >"$OUT/fresh.run2.stdout" 2>"$OUT/fresh.run2.stderr"
cmp "$OUT/fresh.run1.stdout" "$OUT/fresh.run2.stdout"
cmp "$OUT/fresh.run1.stderr" "$OUT/fresh.run2.stderr"
grep -Fqx 'R34_FRESH_PROCESS_EQUIVALENCE_V1_FAILURES,0' "$OUT/fresh.run1.stdout"
grep -Fqx 'R34_FRESH_PROCESS_EQUIVALENCE_V1_RESULT_BYTES,246688' "$OUT/fresh.run1.stdout"
grep -Fqx 'R34_FRESH_PROCESS_EQUIVALENCE_V1_LEARN_AUTHORITY,0' "$OUT/fresh.run1.stdout"
cmp "$OUT/run1/uninterrupted.bin" "$OUT/run1/reloaded.bin"
cmp "$OUT/run2/uninterrupted.bin" "$OUT/run2/reloaded.bin"

{
  hash_line "$ZNC"
  hash_line "$CL/checkpoint.zag"
  hash_line "$CL/world.zag"
  hash_line "$CL/r33_live_outer_checkpoint_binding_v1.zag"
  hash_line "$CL/r33_pending_credit_relation_v1.zag"
  hash_line "$N17/r33_continuing_learner_checkpoint_v1.zag"
  for f in "$HERE"/*.zag "$HERE"/*.zsh; do hash_line "$f"; done
  hash_line "$OUT/sidecar_tests"
  hash_line "$OUT/envelope_tests"
  hash_line "$OUT/r34_fresh_v1"
  hash_line "$OUT/run1/uninterrupted.bin"
} > "$OUT/SHA256SUMS"

{
  print -- 'R34_CONTINUING_LIFE_INTEGRATION_V1,PASS'
  print -- 'inherited_r33_v71=PASS'
  print -- 'fresh_process_byte_equivalence=PASS'
  print -- 'inner_sidecar_corruption_refusal=PASS'
  print -- 'torn_envelope_refusal=PASS'
  print -- 'pending_credit_cross_relation_refusal=PASS'
  print -- 'learn_authority=0'
  print -- 'phase6_self_modification=CLOSED'
  print -- 'claim_boundary=Quarantined native engineering integration only; no scientific promotion or autonomous architecture modification.'
  print -- "finished_utc=$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
} > "$OUT/RECEIPT.txt"
print -- "$OUT"
