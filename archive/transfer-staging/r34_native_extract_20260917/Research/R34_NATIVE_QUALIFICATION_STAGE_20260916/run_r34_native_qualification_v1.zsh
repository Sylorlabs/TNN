#!/bin/zsh
set -eu

HERE=${0:A:h}
ZNC=${TNN_ZNC:-/Users/Shared/micah/Documents/zag/znc}
OUT_ROOT=${TNN_R34_NATIVE_EVIDENCE_ROOT:-"$HERE/EVIDENCE"}
stamp=$(date -u '+%Y%m%dT%H%M%SZ')
OUT="$OUT_ROOT/$stamp"
mkdir -p "$OUT"

if [[ ! -x "$ZNC" ]]; then
  print -u2 -- "compiler missing or not executable: $ZNC"
  exit 70
fi

hash_file() {
  if command -v shasum >/dev/null 2>&1; then shasum -a 256 "$1"
  elif command -v sha256sum >/dev/null 2>&1; then sha256sum "$1"
  else print -u2 -- 'no SHA-256 utility'; return 71
  fi
}

compile_one() {
  local src=$1 bin=$2 log=$3
  rm -f "$bin"
  if "$ZNC" "$src" -o "$bin" >"$log.stdout" 2>"$log.stderr"; then return 0; fi
  rm -f "$bin"
  if "$ZNC" -o "$bin" "$src" >>"$log.stdout" 2>>"$log.stderr"; then return 0; fi
  return 72
}

run_case() {
  local id=$1 test=$2 marker=$3
  local src="$HERE/$test" bin="$OUT/$id" compile="$OUT/$id.compile"
  compile_one "$src" "$bin" "$compile"
  if [[ ! -x "$bin" ]]; then print -u2 -- "binary missing: $id"; return 73; fi
  "$bin" >"$OUT/$id.run1.stdout" 2>"$OUT/$id.run1.stderr"
  "$bin" >"$OUT/$id.run2.stdout" 2>"$OUT/$id.run2.stderr"
  cmp "$OUT/$id.run1.stdout" "$OUT/$id.run2.stdout"
  cmp "$OUT/$id.run1.stderr" "$OUT/$id.run2.stderr"
  grep -Fqx -- "$marker" "$OUT/$id.run1.stdout"
  hash_file "$src" >> "$OUT/SHA256SUMS"
  hash_file "$bin" >> "$OUT/SHA256SUMS"
}

: > "$OUT/SHA256SUMS"
{
  print -- "started_utc=$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  print -- "compiler=$ZNC"
  hash_file "$ZNC"
} > "$OUT/ENVIRONMENT.txt"

run_case memory_lifecycle r34_memory_lifecycle_v1_tests.zag 'R34_MEMORY_LIFECYCLE_V1_FAILURES,0'
run_case hypothesis_state r34_hypothesis_state_v1_tests.zag 'R34_HYPOTHESIS_STATE_V1_FAILURES,0'
run_case memory_association r34_memory_association_v1_tests.zag 'R34_MEMORY_ASSOCIATION_V1_FAILURES,0'
run_case provenance_reliability r34_provenance_reliability_v1_tests.zag 'R34_PROVENANCE_RELIABILITY_V1_FAILURES,0'
run_case curiosity_progress r34_curiosity_progress_v1_tests.zag 'R34_CURIOSITY_PROGRESS_V1_FAILURES,0'
run_case self_model r34_self_model_v1_tests.zag 'R34_SELF_MODEL_V1_FAILURES,0'

{
  print -- 'R34_NATIVE_QUALIFICATION_V1,UNIT_LAYER_PASS'
  print -- "finished_utc=$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  print -- 'claim_boundary=Primitive native unit/determinism layer only; continuing-life integration, save/reload, held-out native behavior, and promotion gates remain separate.'
} > "$OUT/RECEIPT.txt"
print -- "$OUT"
