#!/bin/sh
set -eu
cd /Users/Shared/micah/Documents/TNN/TNN
E=$(cat /tmp/r33_integrator_evidence_path)
cp /tmp/r33_freeze_evidence.sh "$E/freeze_evidence.sh"
: > "$E/verification.jsonl"
verify() {
 label=$1; shift
 rc=0
 "$@" > "$E/$label.stdout" 2> "$E/$label.stderr" || rc=$?
 command_text=$(printf '%s ' "$@")
 oh=$(shasum -a 256 "$E/$label.stdout" | cut -d ' ' -f1)
 eh=$(shasum -a 256 "$E/$label.stderr" | cut -d ' ' -f1)
 jq -cn --arg label "$label" --arg command "$command_text" --argjson exit_code "$rc" --arg stdout_sha256 "$oh" --arg stderr_sha256 "$eh" '{label:$label,command:$command,exit_code:$exit_code,stdout_sha256:$stdout_sha256,stderr_sha256:$stderr_sha256}' >> "$E/verification.jsonl"
 [ "$rc" -eq 0 ]
}
verify json_syntax jq -e . "$E/final_closeout.json"
verify json_n17 jq -e . Research/R33_NATIVE_N17_R27_CONTINUITY/STATUS.json
verify json_n19 jq -e . Research/R33_NATIVE_N19_RUNTIME_BOUNDARY/STATUS.json
verify closeout_invariants jq -e '.scientific_exposure==0 and .canonical_r27_mutated==false and .learner_authority_granted==false and .N17.terminal_blocker_count==32 and (.N17.source_row_blockers|length)==30 and .V92.expanded_selftest_passes==339 and ([.commands[]|select(.claim_role=="CURRENT_ENGINEERING_EVIDENCE" and .expected_exit_matched==false)]|length)==0' "$E/final_closeout.json"
verify sources_verified shasum -a 256 -c "$E/source.sha256"
verify binaries_verified shasum -a 256 -c "$E/binary.sha256"
verify canonical_verified shasum -a 256 -c "$E/canonical.sha256"
verify protected_verified shasum -a 256 -c "$E/protected.sha256"
verify git_check git diff --check
verify tracked_diff_preserved cmp "$E/git.before.diff" "$E/git.after.diff"
jq -s . "$E/verification.jsonl" > "$E/verification.json"
cat > "$E/CLAIM_BOUNDARY.md" <<DOC
# Frozen R33 integrated qualification — 2026-09-15

Full R33 status: FAIL_CLOSED. Scientific exposure=0; canonical_r27_mutated=false;
learner_authority_granted=false. Canonical R27 remains step 60423, newborn restarts 0.
No learn command was invoked by this integrator. No behavioral learning, successor
promotion, Python/foreign-ML execution, or equal-comparison superiority is claimed.

V71, expanded V92 (339 checks and all fresh valid/corrupt/truncated modes), corrected
fresh packet integration, five-child engineering baseline, and repaired-current N19
narrow qualification pass. V68 fails seven checks; V73 returns 81. N17 has 30 exact
source-row deficits plus native V91 parity and terminal independent review (32).
See final_closeout.json for each command, exact exits, stdout/stderr hashes,
source/binary/compiler hashes, exclusions, row-specific blockers and frontier.

Commands were executed using correct separate argv values. commands.jsonl includes
corrected display serialization plus argv; original display-only escaped joining is
retained in commands.raw_serialization_witness.jsonl. Campaign/followup scripts
retain actual orchestration, including additive mkdir/copy/hash operations. Initial
hardcoded integration and precreated baseline root are excluded superseded probes.
Baseline source routing changes only fixture-root and self-exec paths in its frozen
copy; the canonical or existing baseline driver was not changed. Read-only native
parent map is an input substrate, not a copied or freshly projected learner state.

N19 independent Lane C review applies because all three repaired binary SHA-256
values reproduce exactly. Integration review is reconciliation, not a separate
independent terminal N17 or scientific review. Excluded durability/containment/race
claims remain excluded even though bounded fixtures pass. The directory is frozen
by SHA256SUMS. The manifest excludes itself and manifest verification outputs to
avoid a circular receipt. No repository commit, reset, checkout, clean or deletion.
DOC
(cd "$E"; find . -type f ! -name SHA256SUMS ! -name manifest_verified.stdout ! -name manifest_verified.stderr ! -name manifest_verified.exit -print | LC_ALL=C sort | while IFS= read -r item; do shasum -a 256 "$item"; done) > "$E/SHA256SUMS"
(cd "$E"; shasum -a 256 -c SHA256SUMS) > "$E/manifest_verified.stdout" 2> "$E/manifest_verified.stderr"
printf '0\n' > "$E/manifest_verified.exit"
REL=${E#/Users/Shared/micah/Documents/TNN/TNN/}
cat > /tmp/r33_superagent_20260915_1022/integrator.final <<REPORT
R33 integrated engineering closeout complete; full R33 remains FAIL_CLOSED.
Frozen evidence: $REL/ (final_closeout.json, exact command/exit/stdout/stderr hashes, compiler/source/binary SHA-256, matrices/blockers, independent N19 review, verification.json, checked SHA256SUMS).

Fresh results: V68 exit 1/seven failures/first section 2002; V71 exit 0; V73 exit 1/RC81. V92 339 selftest passes and all 13 modes exit 0, including fresh valid packet and corrupt/truncated expected refusals. Fresh-packet integration nine modes exit 0; five-child baseline regression exit 0. N19 repaired-current host tests/crash matrix/resource and asserted fixtures exit 0; operational refusals exit 1; five crash phases pass, 11 children reaped, resource signal25/file32. Rebuilt N19 binaries exactly match independently reviewed Lane C repair; historical BUILD_08 remains REQUEST_CHANGES. N17 fresh 38 native static rows, negative controls and R26/R27 digests pass; V91 two builds exit1 and gate CLOSED/91.

Changed targeted files: continuing-life lane_d_packet_integration.zag now requires explicit fresh packet root; CURRENT_ENTRY_POINT.md and WORKLOG.md; V92 README; N17 STATUS.json; N19 STATUS.json and new INTEGRATION_REVIEW_20260915.md. Frozen baseline copy routes only root/self-binary paths. Initial historical-packet bridge and precreated-root baseline exit80 retained and excluded; corrected reruns pass.

Remaining blockers: original V68/V73 caller closure; N17 seven R27 and 23 R26 exact source rows (row-specific minimal blockers frozen), native retained-generator 16-string V91 parity, fresh independent terminal equivalence review. Missing exact release/member/policy/media/lineage inputs and reviewed native runtime semantics remain genuine deficits. No full R33 or behavioral equivalence claim.

JSON syntax/semantic invariants, source/binary hashes, manifest, git diff --check all exit0. Tracked diff unchanged from campaign start; canonical raw parent/policy/current-state/registries/compiler hashes unchanged. R27 step60423/newborn0; scientific_exposure=0, canonical_r27_mutated=false, learner_authority_granted=false. No learn invocation, promotion, Python/foreign ML, commit/push/reset/checkout/clean or deletion; unrelated artifacts preserved.

Next engineering frontier: pass unchanged original V68/V73 under stable compiler, supply exact missing native N17 inputs/runtime replacements and V91 generator parity, then obtain independent terminal verifier-equivalence review. No TNN-over-LLM claim without equal-comparison benchmark evidence.
REPORT
printf 'FROZEN %s\n' "$E"
