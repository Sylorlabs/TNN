#!/bin/zsh
set -u
ROOT=/Users/Shared/micah/Documents/TNN/TNN
E=$ROOT/Research/R33_FINAL_INTEGRATION_20260915T2145Z
cd "$ROOT"
i=0;failures=0
run() { local label=$1 expected=$2 rc=0; shift 2; i=$((i+1));local stem="$E/verification/${i}_$label";print -r -- "cwd=$PWD command=${(q)@}" > "$stem.command";"$@" > "$stem.stdout" 2> "$stem.stderr" || rc=$?;print -r -- "$label,$expected,$rc" >> "$E/verification/exits.csv";print "$rc" > "$stem.exit";[[ $rc == $expected ]] || failures=$((failures+1)); }
mkdir -p "$E/verification"
run immutable_unchanged 0 shasum -a 256 -c "$E/immutable.before.sha256"
run canonical_hashes_unchanged 0 shasum -a 256 -c "$ROOT/Research/R33_CLOSEOUT_20260915T174458Z/canonical.sha256"
run stable_frozen_identity 0 cmp /Users/Shared/micah/Documents/zag/znc "$E/compiler.stable.znc"
run candidate_frozen_identity 0 cmp /private/tmp/znc-import-const-fix "$E/compiler.candidate.znc"
run current_root_closeout_identity 0 cmp "$ROOT/R33_FINAL_CLOSEOUT.json" "$E/final_closeout.json"
for p in "$ROOT/R33_FINAL_CLOSEOUT.json" "$E"/*.json "$ROOT/Research/R33_NATIVE_N17_R27_CONTINUITY/STATUS.json" "$ROOT/Research/R33_NATIVE_N17_R27_CONTINUITY/EVIDENCE_REGISTER.json" "$ROOT/Research/R33_NATIVE_N17_R27_CONTINUITY/VERIFIER_CHECK_MATRIX_V3.json" "$ROOT/Research/R33_NATIVE_N17_R27_CONTINUITY/R26_VERIFIER_CHECK_MATRIX_V1.json" "$ROOT/Research/R33_NATIVE_N17_R27_CONTINUITY/R25_LINEAGE_RECORD.json" "$ROOT/Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/STATUS.json" "$E/v91_fresh/RECORD.json"; do run "json_${i}_${p:t}" 0 jq empty "$p"; done
for file in "$E/sources"/Research/**/*.zag; do
 rel=${file#$E/sources/};[[ -f "$ROOT/$rel" ]] && run "source_${i}" 0 cmp "$ROOT/$rel" "$file"
done
run tracked_diff_capture 0 git diff --binary
run tracked_diff_preserved_against_lane_c 0 cmp "$E/verification/${i}_tracked_diff_capture.stdout" "$ROOT/Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/RECOVERY_20260915_C/INDEPENDENT_NATIVE_LANE_C_2/git.before.diff"
run whitespace 0 git diff --check -- Research/R33_CONTINUING_LIFE_V1 Research/R33_NATIVE_N17_R27_CONTINUITY Research/R33_NATIVE_N19_RUNTIME_BOUNDARY
run receipt_json 0 jq empty "$E/r25_custody/historical_receipt.json"
run receipt_hash 0 shasum -a 256 -c "$E/r25_custody/receipt.sha256"
print "verification_failures,$failures" > "$E/verification/summary.txt"
exit $((failures != 0))
