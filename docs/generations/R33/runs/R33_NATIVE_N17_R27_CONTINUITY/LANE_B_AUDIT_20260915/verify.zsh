#!/bin/zsh
set -eu
cd /Users/Shared/micah/Documents/TNN/TNN
audit=Research/R33_NATIVE_N17_R27_CONTINUITY/LANE_B_AUDIT_20260915
n17=Research/R33_NATIVE_N17_R27_CONTINUITY
jq -e '.native_pass_count == 26 and .unresolved_required_row_count == 7 and ([.rows[] | select(.status == "PASS_FRESH_NATIVE_STATIC_INVARIANT_NOT_FULL_RUNTIME_QUALIFICATION")] | length) == 26 and (.rows | length) == 33' "$n17/VERIFIER_CHECK_MATRIX_V3.json"
jq -e '.native_pass_count == 24 and .unresolved_required_row_count == 23 and ([.rows[] | select(.status == "PASS_FRESH_NATIVE_STATIC_INVARIANT_NOT_FULL_RUNTIME_QUALIFICATION")] | length) == 24 and (.rows | length) == 47 and ([.rows[] | select(.class == "HISTORICAL_WITNESS_ONLY")] | length) == 1' "$n17/R26_VERIFIER_CHECK_MATRIX_V1.json"
jq -e '.native_count == null and (.rows | length) == 33 and ([.rows[] | select(.status == "SUPERSEDED_PLACEHOLDER_NO_NATIVE_CREDIT")] | length) == 3' "$n17/VERIFIER_CHECK_MATRIX_V2.json"
jq -e '.accounting.direct_native_static_passes == 50 and .accounting.terminal_blocker_count == 32 and (.unresolved_source_rows | length) == 30 and ([.unresolved_source_rows[] | select(.class == "DEFERRED_BLOCKER")] | length) == 29 and ([.unresolved_source_rows[] | select(.class == "HISTORICAL_WITNESS_ONLY")] | length) == 1 and .terminal_claim_allowed == false and .v91.all_16_strings_generated == false and .r25.lineage_closed == false' "$audit/AUDIT.json"
for leaf in EVIDENCE_REGISTER R25_LINEAGE_RECORD PARENT_TYPE_INVENTORY KNOWN_ANSWER_FIXTURE_SPEC NEGATIVE_FIXTURE_SPEC STATUS; do jq -e . "$n17/$leaf.json" >/dev/null; done
test "$(rg -c '^B_ROW,.*PASS,' "$audit/rows.stdout")" = 37
test "$(rg -c '^B_ROW,.*PASS,' "$audit/structure.stdout")" = 1
if rg '^B_ROW,.*FAIL,' "$audit/rows.stdout" "$audit/structure.stdout"; then exit 91; fi
rg -x 'B_PRIMITIVE_FAILURES,0' "$audit/primitives.stdout"
shasum -a 256 -c "$audit/FROZEN_FINAL.sha256"
shasum -a 256 -c "$audit/BINARY_FINAL.sha256"
shasum -a 256 -c "$audit/custody.before.sha256"
printf '%s\n' 'LANE_B_ACCOUNTING_AND_NATIVE_PINS_PASS'
