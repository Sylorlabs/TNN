#!/bin/zsh
set -u
ROOT=/Users/Shared/micah/Documents/TNN/TNN
cd "$ROOT" || exit 99
E=$(cat /tmp/r33_finish_recovery_20260915_b/evidence_path)
OLD="$ROOT/Research/R33_CLOSEOUT_20260915T174458Z"
run() {
 local label=$1 expected=$2; shift 2
 local out="$E/logs/$label.stdout" err="$E/logs/$label.stderr" rc=0
 "$@" > "$out" 2> "$err" || rc=$?
 local oh=$(shasum -a 256 "$out" | cut -d ' ' -f1) eh=$(shasum -a 256 "$err" | cut -d ' ' -f1)
 jq -cn --arg label "$label" --arg cwd "$ROOT" --argjson exit_code "$rc" --argjson expected "$expected" --arg stdout "$out" --arg stderr "$err" --arg stdout_sha256 "$oh" --arg stderr_sha256 "$eh" --args -- '{label:$label,argv:$ARGS.positional,cwd:$cwd,exit_code:$exit_code,expected_exit_code:$expected,expected_exit_matched:($exit_code==$expected),stdout:$stdout,stderr:$stderr,stdout_sha256:$stdout_sha256,stderr_sha256:$stderr_sha256}' "$@" >> "$E/commands.jsonl"
 print -r -- "$label exit=$rc expected=$expected"
}
cp /tmp/r33_finish_recovery_20260915_b/native_followup.zsh "$E/native_followup.zsh"
run original_frozen_manifest 0 shasum -a 256 -c "$OLD/SHA256SUMS"
N=Research/R33_NATIVE_N17_R27_CONTINUITY
for spec in "rows:$N/LANE_B_AUDIT_20260915/rows.zag" "structure:$N/LANE_B_AUDIT_20260915/structure.zag" "primitives:$N/LANE_B_AUDIT_20260915/primitives.zag" "r26:$N/r26_digest.zag" "r27:$N/r27_digest.zag"; do
 local label=${spec%%:*} src=${spec#*:}
 run build_n17_$label 0 /Users/Shared/micah/Documents/zag/znc "$OLD/sources/$src" --target macos-arm64 --no-zagd --no-analyze --no-foreground-cache -o "$E/bin/n17_$label"
done
for label in rows structure primitives; do run n17_$label 0 "$E/bin/n17_$label"; done
run n17_r26_selftest 0 "$E/bin/n17_r26" selftest
run n17_r26_digest 0 "$E/bin/n17_r26" digest
run n17_r27_digest 0 "$E/bin/n17_r27" digest
run n17_match_r26 0 rg -x 'R26_NATIVE_DIGEST,44d36746ffb9e8d46080376a6e26bb824772d9d4b5e429add404195d02888649' "$E/logs/n17_r26_digest.stdout"
run n17_match_r27 0 rg -x 'R27_NATIVE_DIGEST,562aaaedb5b9ceec2f50482f631992c247cbe50e9f6d2321b811e311ecf73b04' "$E/logs/n17_r27_digest.stdout"
run canonical_final_native 0 shasum -a 256 -c "$E/canonical.sha256"
run protected_final_native 0 shasum -a 256 -c "$E/protected.sha256"
find "$E/bin" -type f -exec shasum -a 256 {} \; > "$E/binary.sha256"
jq -s '{commands:length,unexpected:[.[]|select(.expected_exit_matched==false)]}' "$E/commands.jsonl" > "$E/qualification_summary.json"
