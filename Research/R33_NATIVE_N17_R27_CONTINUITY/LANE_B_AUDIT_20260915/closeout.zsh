#!/bin/zsh
set -eu
cd /Users/Shared/micah/Documents/TNN/TNN
audit=Research/R33_NATIVE_N17_R27_CONTINUITY/LANE_B_AUDIT_20260915
n17=Research/R33_NATIVE_N17_R27_CONTINUITY
{
 rg --files "$audit" | LC_ALL=C sort | while IFS= read -r file; do
  case "$file" in
   "$audit/CLOSEOUT.sha256"|"$audit/CLOSEOUT_VERIFIED.txt"|"$audit/CLOSEOUT_VERIFY.stderr") continue ;;
  esac
  shasum -a 256 "$file"
 done
 for leaf in VERIFIER_CHECK_MATRIX_V2.json VERIFIER_CHECK_MATRIX_V3.json R26_VERIFIER_CHECK_MATRIX_V1.json R25_LINEAGE_RECORD.json PARENT_TYPE_INVENTORY.json EVIDENCE_REGISTER.json STATUS.json KNOWN_ANSWER_FIXTURE_SPEC.json NEGATIVE_FIXTURE_SPEC.json PARENT_RUNTIME_BOUNDARY.md IMPLEMENTATION_DECISION.md VERIFY_CONTRACT.md; do
  shasum -a 256 "$n17/$leaf"
 done
} > "$audit/CLOSEOUT.sha256"
shasum -a 256 -c "$audit/CLOSEOUT.sha256" > "$audit/CLOSEOUT_VERIFIED.txt" 2> "$audit/CLOSEOUT_VERIFY.stderr"
shasum -a 256 "$audit/CLOSEOUT.sha256" "$audit/AUDIT.json"
