#!/bin/zsh
set -eu
ROOT=${TNN_ROOT:-/Users/Shared/micah/Documents/TNN/TNN}
R=$ROOT/Research
STAMP=$(date -u '+%Y%m%dT%H%M%SZ')
OUT=${TNN_R34_CHAIN_V2_EVIDENCE_ROOT:-$R/R34_NATIVE_CHAIN_V2_EVIDENCE}/$STAMP
mkdir -p "$OUT"
run_stage() { local name=$1 script=$2; [[ -f "$script" ]] || { print -u2 -- "missing stage: $script"; return 80; }; zsh "$script" >"$OUT/$name.stdout" 2>"$OUT/$name.stderr"; }
run_stage smoke "$R/R34_NATIVE_QUALIFICATION_STAGE_20260916/detached_smoke_stage.zsh"
grep -Fq 'R34_DETACHED_SMOKE_PASS' "$OUT/smoke.stdout"
run_stage unit "$R/R34_NATIVE_QUALIFICATION_STAGE_20260916/run_r34_native_qualification_v1.zsh"
unit_evidence=$(tail -n 1 "$OUT/unit.stdout")
[[ -f "$unit_evidence/RECEIPT.txt" ]] || exit 81
grep -Fqx 'R34_NATIVE_QUALIFICATION_V1,UNIT_LAYER_PASS' "$unit_evidence/RECEIPT.txt"
run_stage continuing "$R/R34_CONTINUING_LIFE_INTEGRATION_STAGE_20260916/run_r34_continuing_integration_v1.zsh"
continuing_evidence=$(tail -n 1 "$OUT/continuing.stdout")
[[ -f "$continuing_evidence/RECEIPT.txt" ]] || exit 82
grep -Fqx 'R34_CONTINUING_LIFE_INTEGRATION_V1,PASS' "$continuing_evidence/RECEIPT.txt"
run_stage behavior "$R/R34_BEHAVIORAL_HELDOUT_STAGE_20260916/run_r34_behavioral_heldout_v3.zsh"
behavior_evidence=$(tail -n 1 "$OUT/behavior.stdout")
[[ -f "$behavior_evidence/RECEIPT.txt" ]] || exit 83
grep -Fqx 'R34_BEHAVIORAL_HELDOUT_V3,NATIVE_PASS' "$behavior_evidence/RECEIPT.txt"
{
 print -- 'R34_NATIVE_CHAIN_V2,PASS'
 print -- "unit_evidence=$unit_evidence"
 print -- "continuing_evidence=$continuing_evidence"
 print -- "behavior_evidence=$behavior_evidence"
 print -- 'learn_authority=0'
 print -- 'phase6_self_modification=CLOSED'
 print -- "finished_utc=$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
} > "$OUT/RECEIPT.txt"
print -- "$OUT"
