#!/bin/sh
set -eu
cd /Users/Shared/micah/Documents/TNN/TNN
E=$(cat /tmp/r33_integrator_evidence_path)
REL=${E#/Users/Shared/micah/Documents/TNN/TNN/}
N=Research/R33_NATIVE_N17_R27_CONTINUITY
H=Research/R33_NATIVE_N19_RUNTIME_BOUNDARY
D=Research/R33_CONTINUING_LIFE_V1
cp "$N/LANE_B_AUDIT_20260915/AUDIT.json" "$E/N17_LANE_B_AUDIT_WITNESS.json"
cp "$N/VERIFIER_CHECK_MATRIX_V3.json" "$E/N17_R27_MATRIX.json"
cp "$N/R26_VERIFIER_CHECK_MATRIX_V1.json" "$E/N17_R26_MATRIX.json"
cp "$H/INDEPENDENT_REVIEW_V3.md" "$E/N19_INDEPENDENT_REVIEW_V3.md"
cp "$H/INDEPENDENT_V3_FRESH/RECORD.json" "$E/N19_LANE_C_RECORD_WITNESS.json"
jq '.unresolved_source_rows' "$E/N17_LANE_B_AUDIT_WITNESS.json" > "$E/N17_EXACT_SOURCE_ROW_BLOCKERS.json"
find Research/R33_NATIVE_N10_RUN_PRIMARY_V1/parent-map -type f -exec shasum -a 256 {} \; > "$E/read_only_map_inputs.sha256"
shasum -a 256 "$N/STATUS.json" "$H/STATUS.json" "$D/CURRENT_ENTRY_POINT.md" "$D/WORKLOG.md" "$N/V92_STATE_IMAGE_QUAL/README.md" > "$E/status_before_updates.sha256"
jq --arg evidence "$REL/final_closeout.json" '.full_verifier_equivalent_continuity="FAIL_CLOSED" | .integrated_closeout={record:$evidence,status:"ENGINEERING_MECHANICS_NARROW_PASS_FULL_VERIFIER_FAIL_CLOSED",terminal_blocker_count:32,canonical_r27_mutated:false,learner_authority_granted:false,scientific_exposure:0} | .canonical_r27_mutated=false' "$N/STATUS.json" > "$E/n17.status.updated"
cp "$E/n17.status.updated" "$N/STATUS.json"
jq --arg evidence "$REL/final_closeout.json" --arg build "$REL/bin" '.status="REPAIRED_CURRENT_ENGINEERING_PASS_WITH_NARROW_SCOPE_FULL_R33_FAIL_CLOSED" | .latest_independent_review="INDEPENDENT_REVIEW_V3.md" | .latest_independent_review_disposition="PASS_WITH_NARROW_SCOPE_REPAIRED_CANDIDATE_ONLY_BUILD_08_REQUEST_CHANGES" | .historical_build_08_disposition="REQUEST_CHANGES_HOST_PROBE_IO_MISCLASSIFICATION" | .historical_active_build="BUILD_08" | .active_build=$build | .active_build_record=$evidence | .runtime_result=$evidence | .host_abi_status="REPAIRED_HOST_PROBE_FSYNC_CLOSE_IO_CLASSIFICATION_PASS" | .remaining_blockers=[] | .next_gate="N17 full verifier equivalence remains fail-closed; no authority or exposure permitted in this closeout" | .canonical_r27_mutated=false | .learner_authority_granted=false | .integrated_closeout=$evidence | .scope_exclusions += ["concurrent_hostile_same_user_races","exhaustive_socket_device_failures","cpu_ceiling_enforcement","interrupted_wait_fallback","fresh_root_identity_authentication"]' "$H/STATUS.json" > "$E/n19.status.updated"
cp "$E/n19.status.updated" "$H/STATUS.json"
cat > "$H/INTEGRATION_REVIEW_20260915.md" <<DOC
# N19 integration reconciliation — 2026-09-15

Current disposition: PASS_WITH_NARROW_SCOPE for the additive repaired candidate.
Historical BUILD_08 remains REQUEST_CHANGES: ordinary host-probe fsync/close
failure was misclassified as HOST_ABI. Historical files were not repaired or repinned.

Independent review is INDEPENDENT_REVIEW_V3.md (Lane C); this integration review
is a reconciliation, not a new independent scientific or terminal N17 review.
Fresh rebuild runtime SHA-256 c465815cba4abad84cc486a35693bf7aea225c7e1d5f58ae62e3e37c7b98b170,
qualifier be3b6b4ca27e3d7a9224179493f98360d0ae18f1450634c32a382a60d8b773ec,
and host tests c0885ffe5039c3a7edbfcde6373ce43ae5c2af1259dc26646054fa8e3570ec6f
exactly reproduce the independently reviewed repaired binaries.

Evidence: ../../$REL/final_closeout.json (repository-relative path: $REL).
Commands, exits and stdout/stderr hashes are in its command array. Fresh host
tests, five crash phases and separate recovery processes pass; all 11 supervised
children report second_wait=-10. RLIMIT_FSIZE=32 produces signal 25 and independently
observed file size 32, CPU 672 us, RSS 1490944 bytes. Closed-root host probe reports
IO -1905. Valid append/recovery, retained-root sequence and expected operational
refusals pass. Assertion refusal fixtures exit 0; rejected operational requests exit 1.

Only exercised owner-created local fixtures, direct-child successful reaping,
process-death recovery and mapping inputs are qualified. Exclusions: power-loss
durability, host-admin rollback protection, descendant groups, hostile concurrent
same-user races, exhaustive device/socket faults, CPU ceiling enforcement,
interrupted-wait fallback, and fresh-root identity authentication. No learner,
training, scientific exposure, successor promotion or full R33 closure is established.
DOC
cat >> "$N/V92_STATE_IMAGE_QUAL/README.md" <<DOC

## Integrated closeout — 2026-09-15

Latest integrated fresh qualification: [$REL](../../${REL#Research/}/final_closeout.json).
All 339 expanded selftest checks pass; valid packet and corrupt/truncated
expected-refusal readers pass as separate processes. Exact commands, exits,
complete imported source pins, binary pins and stdout/stderr hashes are frozen
there. The continuing-life bridge now requires an explicit freshly generated
packet-root argument; this campaign supplies its own V92 runtime directory.
Historical lane packet bytes are excluded from integrated admission evidence.
N17 remains fail-closed with 32 terminal blockers. No learn command was invoked
by the integrator; source refusal was inspected. No learner authority or exposure.
DOC
cat >> "$D/CURRENT_ENTRY_POINT.md" <<DOC

## Integrated exact status — 2026-09-15

Authoritative integrated closeout: [$REL](../${REL#Research/}/final_closeout.json).
Fresh V71, 339-check V92 plus fresh packet/refusals, five-child baseline regression,
and complete packet/outer/world/ingress recovery and delayed continuation pass.
N19 repaired current candidate reproduces Lane C independently reviewed binaries
and passes the bounded native rerun; historical BUILD_08 remains REQUEST_CHANGES.
V68 still exits 1 with seven failures (first section status 2002); V73 exits 1
with RC 81. Successful single-output bridge transport does not close these caller rows.
N17 remains FAIL_CLOSED: 7 R27 + 23 R26 source rows, V91 generator parity,
and fresh independent terminal closure review remain unresolved (32 terminal blockers).
Exact row blockers are in the closeout JSON and N17_EXACT_SOURCE_ROW_BLOCKERS.json.
The bridge invocation is now: integration MODE OUTER_ROOT FRESH_V92_PACKET_ROOT.
It requires all three arguments and has no hardcoded historical packet source.
Learn remains refused in source and was not invoked by this integrator. Canonical
R27 remains step 60423, newborn restarts 0; raw parent/policy and current-state/
registries/compiler hashes were verified unchanged. Scientific exposure 0,
learner authority false, no successor promotion. R33 is not fully complete.
DOC
cat >> "$D/WORKLOG.md" <<DOC

## 2026-09-15 integration and frozen engineering closeout

Read all four lane logs/finals and actual files; repository evidence prevailed
over lane prose. N19 STATUS was stale and now distinguishes rejected historical
BUILD_08 from repaired current PASS_WITH_NARROW_SCOPE backed by independent Lane C
review and exactly reproduced binary hashes. N17 PENDING equivalence label is now
explicit FAIL_CLOSED; no unresolved row was promoted to a pass.

Evidence directory: $REL. Builds exclusively used /Users/Shared/micah/Documents/zag/znc.
Integrated packet source was changed narrowly to require explicit packet-root argv[3]
and argc=4, so qualification reads this campaign's fresh V92-generated packet.
The preliminary hardcoded bridge run is retained but excluded from fresh admission.
Baseline first supervise exited 80 because the shell precreated its root; source
requires mkdir of an absent directory. A frozen copy with only root/self-binary
path substitutions reran in a distinct absent directory and passed all five children.
Both preliminary probes remain visible in commands.jsonl and final JSON.

V68 failed seven checks, V73 RC 81; no compiler-root-cause claim or compiler change.
V71 and fresh V92 passed. Corrected packet bridge passed write/reload, outer corrupt,
re-signed inner corrupt and torn refusal with unchanged output, exact pending-credit,
world/ingress retention and delayed continuation. N19 repaired native host/crash/
resource/status/custody campaign passed with operational refusals exiting 1.
Fresh N17 native static/digest/negative checks pass while V91 tests/emitter builds
fail and admission returns CLOSED/91. Full verifier continuity and R25 lineage
remain blocked; exact 30 source rows plus two terminal gates are recorded.

No learn invocation by integrator, training, learner callback, authority, exposure,
successor promotion, foreign ML runtime or Python execution. Canonical serialized
bytes were shell-hashed only; canonical parent/policy/current-state/registries and
compiler verified unchanged. Existing unrelated modified/untracked research artifacts
were preserved. Frontier: resolve original caller shape/lowering under the stable
compiler and supply/reconstruct the exact missing native N17 release/runtime inputs;
obtain terminal independent equivalence review before any future scientific gate.
DOC
cp /tmp/r33_closeout_docs.sh "$E/closeout_docs.sh"
