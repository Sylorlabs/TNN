# Tier2 gap-fill skim findings (228 files)

Batch: gap-fill ranges 0530_*–0643_* (114 files) and 0758_*–0871_* (114 files) in `docs_local/`.
Baseline read first at `/home/hatch/workspace/tnn-lab/wave12/senses/doc-sweep/BASELINE.md`.
Protocol: skimmed all files; full read only when content looked new vs the baseline.
Range A (0530–0643) re-verifies the tier2_batch1 set (identical file set, confirmed programmatically);
range B (0758–0871) was skimmed fresh this session.

## Counts

- Files skimmed: 228 (114 per range)
- Files fully read: range A 4 + V-family decision sections (from prior session, same protocol); range B: the 13 candidate files were all short enough to be captured in full by the skim (headers + full contents)

## Range A verdicts (0530–0643, 114 files)

- 0530 R33_FIRST_DELIVERABLE.md — **CONFIRMS**: R33 delivery boundary; R27 canonical.
- 0531 V91_STATUS.md — **CONFIRMS**: V91 parity fail-closed.
- 0532 R33_PARENT_SOURCE_RECOVERY_N12_LEADS.md — **CONFIRMS**: Recovery leads remain leads; aligns with "unrecoverable".
- 0533 GATE_FAILURES.md — **NOISE**: C compile-gate failure log.
- 0534 CURRENT_ENTRY_POINT.md — **CONFIRMS**: R33 closeout entry-point status.
- 0535 agent_evidence_report.md — **CONFIRMS**: V91 semantic-generator recovery detail.
- 0536 R32_EPISTEMIC_R31_MATCHED_V38_INTERPRETATION.md — **CONFIRMS**: V38 repeated-continuation retained (V-family, REFERENCE_ONLY).
- 0537 R32_E51_GENERALITY_SCORECARD.md — **CONFIRMS**: E51 generality scorecard; E51AJ MIXED, E51AH FROZEN_NOT_RUN (see 0566 NEW).
- 0538 R33_PROGRAM_CHARTER.md — **CONFIRMS**: R33 program charter; white-box autonomy target.
- 0539 R33_NOVEL_TNN_EXPERIMENTS_20260911.md — **NEW-minor**: "## E01 — adaptive support-manifold routing" — six new R33 hypotheses E01–E06; "No scientific population for E01–E06 may be allocated from this document." Baseline has no experiment portfolio; extends it.
- 0540 VERIFY_CONTRACT.md — **NEW-minor**: N17 verify contract names eight policy gates and the single active promotion; "eight policy gates remain locked". Baseline's N17 item lacks the gate names — extends.
- 0541 R33_PARENT_SOURCE_RECOVERY_AFTER_N11.md — **CONFIRMS**: Searched Micah's Codex sessions/attachments; no match; N11 "explicitly main-author".
- 0542 V91_STATUS.md — **CONFIRMS**: V91 parity fail-closed, 0 strings.
- 0543 HOST_ABI_CONTRACT_V1.md — **CONFIRMS**: N19 capability-based host contract (prospective).
- 0544 VERIFY_CONTRACT.md — **NEW-minor**: N18 verify-contract lane inventory (see 0540).
- 0545 R32_E45_ARM64_7CAC_AGGREGATE_ABI_REPORT.md — **NOISE**: Compiler determinism diagnostic; byte-identical binaries.
- 0546 R32_EPISTEMIC_R31_MATCHED_V33_INTERPRETATION.md — **CONFIRMS**: V33 interpretation (V-family, REFERENCE_ONLY).
- 0547 R32_E45_E48_NATIVE_QUALIFICATION_REPORT.md — **CONFIRMS**: "FOUR VALID NATIVE NEGATIVES — R27 REMAINS CANONICAL".
- 0548 policy_native.initial_missing_reader.txt — **CONFIRMS**: Zag policy parser; gate list overlaps N17 names.
- 0549 R32_EPISTEMIC_R31_MATCHED_V37_INTERPRETATION.md — **CONFIRMS**: V37 interpretation (V-family, REFERENCE_ONLY).
- 0550 CURRENT_ENTRY_POINT.md — **CONFIRMS**: R33 closeout entry-point status (copy of 0534).
- 0551 R32_EPISTEMIC_R31_MATCHED_V29_INTERPRETATION.md — **CONFIRMS**: V29 interpretation (V-family, REFERENCE_ONLY).
- 0552 R32_EPISTEMIC_R31_MATCHED_V39_INTERPRETATION.md — **NEW**: V39 GRU PAM rejection: "it broadened the action region rather than identifying the positive option-value boundary. This rejects the idea that replacing summaries with an opaque recurrent embedding is sufficient." Baseline's item 11 lacked the stated causal rationale — fills it.
- 0553 SHA256_VERIFY.txt — **NOISE**: Checksum inventory.
- 0554 R32_E51_CAUSAL_MAP.md — **NEW-minor**: E51 causal map with dead branches: "E51AF: historical prerequisites mismatch -> INVALID, never run"; "E51AH: grounded preservation replay [FROZEN_NOT_RUN]". Baseline lacks the frozen/invalid branch inventory — extends.
- 0555 RECOVERY_EXACT_R23_SOURCE_20260917.md — **NEW-minor**: R23 provenance: "The original release archive `tnn-pre-v1-r27-general-learning.zip` was recovered from the user's existing ChatGPT Library artifact". Baseline lacks this provenance — extends (dates/people).
- 0556 v91_final.txt — **NEW-minor**: V91 closeout: "GENERATOR PARITY BLOCKED"; "Native anti-fake admission gate: CLOSED, exit 91" with 16/16 oracle custody. Baseline lacks the V91 closeout numbers — extends.
- 0557 N17_BLOCKERS.txt — **NEW-minor**: N17 blockers name old capabilities: "No reviewed native implementation of the serialized abstraction model and original SOCIAL_FAR evaluator." Baseline lacks these capability names — fills.
- 0558 FINAL.txt — **NEW-minor**: Lane-B recovery scale: "Deep search: 947360 returned paths, 889854 hashed files, 157 archive inventories, all1610 Git blobs (744029506 bytes) hashed. No missing exact source/state/manifest input admitted." Quantifies baseline's "proven unrecoverable" — extends.
- 0559 final_transport.commands.txt — **NOISE**: Command log.
- 0560 R33_SCENARIO_BATTERY.md — **NEW-minor**: R33 scenario battery: "Status: scenario definitions, not allocated evidence"; "All developmental scenarios retain one branch's continuing history." Planned-but-unexecuted scenario families; baseline lacks — extends.
- 0561 R33_PARENT_SOURCE_RECOVERY_POST_N13A_20260906.md — **CONFIRMS**: Post-N13A parent-source recovery; earlier remote check references `Sylorlabs/TNN`; aligns with "unrecoverable".
- 0562 R33_WHITE_BOX_OBSERVABILITY_CONTRACT.md — **CONFIRMS**: White-box observability contract; mutable-state inventory includes RNG stream position (checkpoint coverage, not a no-RNG contradiction).
- 0563 VERIFY_CONTRACT.md — **NEW-minor**: N19 verify-contract lane inventory (see 0540).
- 0564 extend.txt — **NOISE**: CPython venv file inside R42.
- 0565 R32_EPISTEMIC_R31_MATCHED_V32_INTERPRETATION.md — **CONFIRMS**: V32 interpretation (V-family, REFERENCE_ONLY).
- 0566 VALIDATION.md — **NEW-minor**: E51AJ validation: "The preregistered retention rule fails in replicas 0 and 1 and passes in replica" [2 of 3]; "no-final-behavioral-tradeoff flag fails in every replica." Baseline item 9 lacked replica-level specifics — extends.
- 0567 R33_B000_LAUNCH_CONTRACT.md — **CONFIRMS**: B000 launcher sandbox limits.
- 0568 archives.txt — **NEW-minor**: koryphaios hit (archive path only): "/Users/Shared/micah/Documents/koryphaios/.koryphaios/eval-tools/deno/2.9.6/download.zip". No ghost hits. Confirms no koryphaios code overlap; dates/people-adjacent.
- 0569 R32_EPISTEMIC_R31_MATCHED_V41_INTERPRETATION.md — **CONFIRMS**: V41 interpretation (V-family; live resolution rejected).
- 0570 LICENSE.md — **NOISE**: CPython LICENSE file inside R42.
- 0571 R32_EPISTEMIC_R31_MATCHED_V31_INTERPRETATION.md — **CONFIRMS**: V31 interpretation (V-family; predictive-dynamics ceiling).
- 0572 R32_EPISTEMIC_R31_MATCHED_V44_INTERPRETATION.md — **NOISE**: Artifact checksum list.
- 0573 R32_EPISTEMIC_R31_MATCHED_V34_INTERPRETATION.md — **CONFIRMS**: V34 interpretation (V-family, REFERENCE_ONLY).
- 0574 R32_EPISTEMIC_R31_MATCHED_V30_INTERPRETATION.md — **CONFIRMS**: V30 interpretation (V-family, REFERENCE_ONLY).
- 0575 R32_V35_SHA256.txt — **NOISE**: V35 checksum inventory.
- 0576 API_CHANGES.txt — **NOISE**: CPython API_CHANGES inside R42.
- 0577 AMENDMENT_REQUEST.md — **SUPERSEDED**: Proposed FROZEN_PARENT_NATIVE_SURROGATE_COMPOSITE class; proposal only, no effect — superseded by later custody design.
- 0578 R32_EPISTEMIC_R31_MATCHED_V40_INTERPRETATION.md — **CONFIRMS**: V40 interpretation (V-family; hazard state retained).
- 0579 R25_LINEAGE_REQUIREMENTS.md — **CONFIRMS**: R25 lineage requirements; r25 hashes absent; receipt witness-only.
- 0580 R33_NATIVE_N11_PREFLIGHT_PINS.txt — **NOISE**: Pin file.
- 0581 POSTRUN_SOURCE_PINS.txt — **NOISE**: Pin file.
- 0582 n11-pins.txt — **NOISE**: Pin file.
- 0583 HASH_ORACLE_PROVENANCE.md — **CONFIRMS-minor**: Hash oracle provenance "transcribed by the main author" = Micah (people anchor).
- 0584 R32_E51_GENERALITY_SCORECARD.md — **CONFIRMS**: E51 generality scorecard (copy of 0537).
- 0585 tnn-debug-script.txt — **NEW-minor**: Old program-induction native test: Zag source compiled and run against hidden tests ("compiles it, and runs hidden tests"); native-first testing precedent from pre-R33 — extends baseline's native-testing history.
- 0586 R32_EPISTEMIC_R31_MATCHED_V35_INTERPRETATION.md — **CONFIRMS**: V35 interpretation (V-family, REFERENCE_ONLY).
- 0587 R32_E51N_SEED_NAMESPACE_DIAGNOSTIC.md — **NEW-minor**: E51N seed-namespace exhaustion: "The allocator failed after allocating 8,352 of the 18,360 requested E51N worlds." Negative result; baseline item 12-adjacent — extends.
- 0588 DIAGNOSIS.md — **NEW-minor**: N13 postrun diagnosis: "_zag_free evaluates its argument but does not reclaim" — toolchain defect root cause; baseline lacked — fills.
- 0589 TNN_R27_TRACEABILITY.md — **NEW**: Old R27 causal-traceability contract: "`raw evidence -> core signature -> PAM route -> entity hypothesis -> memory retrieval -> world/language binding -> decision -> error -> failure diagnosis -> PAM/memory revision`". Baseline had no old-pipeline trace contract — fills (senses/PAM origins).
- 0590 CURRENT_ENTRY_POINT.md — **CONFIRMS**: R33 closeout entry-point status (copy of 0534).
- 0591 R32_EPISTEMIC_R31_MATCHED_V28_INTERPRETATION.md — **CONFIRMS**: V28 interpretation (V-family, REFERENCE_ONLY).
- 0592 AUTHORING_HISTORY.md — **NEW-minor**: N14 authoring history: PCM fixture "strengthened from a small mixed-sign sample to the maximum 131,072-byte mono payload"; BUILD_01/02 byte-identical binaries superseded pre-review. Baseline N14 item lacked authoring detail — extends.
- 0593 R33_NATIVE_N08B_ARTIFACTS_VERIFIED.txt — **NOISE**: Artifact checksum list.
- 0594 R32_EPISTEMIC_R31_MATCHED_V26_INTERPRETATION.md — **CONFIRMS**: V-interpretation family member (REFERENCE_ONLY).
- 0595 R32_EPISTEMIC_R31_MATCHED_V36_INTERPRETATION.md — **CONFIRMS**: V-interpretation family member (REFERENCE_ONLY).
- 0596 R32_E51AE_IMPLEMENTATION_CONTRACT.md — **CONFIRMS**: E51AE implementation contract frozen; UNKNOWN=0.
- 0597 import_paths.txt — **NOISE**: Path listing.
- 0598 R32_EPISTEMIC_R31_MATCHED_V27_INTERPRETATION.md — **CONFIRMS**: V-interpretation family member (REFERENCE_ONLY).
- 0599 R25_LINEAGE_REQUIREMENTS.md — **CONFIRMS**: R25 lineage requirements (copy of 0579).
- 0600 R33_PARENT_SOURCE_RECOVERY_POST_N13A_20260906.md — **CONFIRMS**: Post-N13A parent-source recovery (copy of 0561).
- 0601 WORKLOG_20260916.md — **NEW**: R34 v2 continual-learner worklog: "after 24 A experiences: 16/16 positive at zero-update evaluation"; "after hidden switch and 24 B experiences: 16/16 positive" — latent-context memory test results; baseline item 14 mentions R34 files but not v2 numbers — fills.
- 0602 R32_E47_TERMINAL_REPRESENTATION_DISCRIMINATOR_NEGATIVE_B7B49F4D_NO_TESTED_REPRESENTATION_RESCUE_SHA256SUMS.txt — **NOISE**: E47 checksum inventory.
- 0603 R32_EPISTEMIC_R31_MATCHED_V10_PRELIM_3SEED_INTERPRETATION.md — **CONFIRMS**: V10 prelim 3-seed interpretation (V-family, REFERENCE_ONLY).
- 0604 R33_NATIVE_N09_PREFLIGHT_PINS.txt — **NOISE**: N09 pin file.
- 0605 R33_NATIVE_N11_PREFLIGHT_N09_PINS.txt — **NOISE**: N09 pin file.
- 0606 tnn-pre-v1-r5-NEXT_STAGE_HANDOFF.md — **NEW**: R5 pre-v1 continuation plan: "## Priority 1 — one-shot motif binding without interference"; "## Priority 3 — natural developmental media". Oldest senses roadmap found (modified 2026-08-23) — fills a baseline gap on pre-v1 senses.
- 0607 R32_E51AH_IMPLEMENTATION_CONTRACT.md — **CONFIRMS**: E51AH implementation contract frozen.
- 0608 R25_LINEAGE_REQUIREMENTS.md — **NOISE**: Artifact checksum list.
- 0609 r26_digest_excerpt.py.txt — **NEW**: R26State dataclass: old brain state carried `video_encoder`, `speech_segmenter`, `speech_index`, `semantic_generator`, `self_revision_history` — old senses architecture; baseline lacked — fills (senses/PAM origins).
- 0610 R33_TRAINING_TECHNIQUE_TOURNAMENT.md — **CONFIRMS**: Prospective training-technique tournament plan.
- 0611 evidence_record.initial_transform_failure.txt — **NOISE**: Zag serializer source.
- 0612 tnn-pre-v1-r6-rsi-NEXT_STAGE_HANDOFF.md — **NEW**: R6 pre-v1 RSI handoff: "Replace the finite candidate list with a compositional mutation grammar that can..." create operators, memory organizations, sensory policies, training policies; verifier/rollback stay independent. The actual self-architecture plan; baseline lacked — fills (abandoned/rationale).
- 0613 R33_NATIVE_ONLY_EXECUTION_CONTRACT.md — **NEW**: Pure-Zag law origin: "Effective: direct human instruction 2026-09-05, after C03. This supersedes older permissions to use Python as external supervision, packaging or evaluation." Dated direct-instruction date; baseline item 1 lacks the date — fills.
- 0614 R32_EPISTEMIC_R31_MATCHED_V43_INTERPRETATION.md — **CONFIRMS**: V43 interpretation (V-family; stage routing rejected).
- 0615 R33_NATIVE_N08A_ARTIFACTS_VERIFIED.txt — **NOISE**: N08A artifacts-verified checksum inventory.
- 0616 HOST_V2_WORKLOG_20260913.md — **NOISE**: Host-adapter authoring checkpoint.
- 0617 SOURCE_SHA256SUMS.txt — **NOISE**: Source checksum list.
- 0618 R32_EPISTEMIC_R31_MATCHED_V9_INTERPRETATION.md — **CONFIRMS**: V9 interpretation (V-family; runaway fixed/economics wrong).
- 0619 R33_NATIVE_N08_ARTIFACTS_VERIFIED.txt — **NOISE**: N08 artifacts-verified checksum inventory.
- 0620 FINAL.txt — **CONFIRMS**: N19 process-gaps FINAL (PASS_BOUNDED_NATIVE_ENGINEERING).
- 0621 WORKLOG_20260916.md — **NEW-minor**: R34 v3 worklog: "`r34_learner_core.zag` contains learner state, deterministic RNG, action choice..." — RNG driver unexplained (open question, not a contradiction). Baseline item 14-adjacent — extends.
- 0622 R32_EPISTEMIC_R31_MATCHED_V17_INTERPRETATION.md — **CONFIRMS**: V-interpretation family member (REFERENCE_ONLY).
- 0623 R32_E49_GROUNDED_QUADRATIC_COMMIT_VALUE_NEGATIVE_62326D58_NO_TESTED_QUADRATIC_RESCUE_SHA256SUMS.txt — **NOISE**: E49 checksum inventory.
- 0624 R32_EPISTEMIC_R31_MATCHED_V5_INTERPRETATION.md — **CONFIRMS**: V-interpretation family member (REFERENCE_ONLY).
- 0625 R32_E48_ONLINE_BATCH_REPRESENTATION_NEGATIVE_24E8098F_NO_TESTED_BATCH_SAFETY_RESCUE_SHA256SUMS.txt — **NOISE**: E48 checksum inventory.
- 0626 TNN_NATIVE_MIGRATION_STATUS.md — **NEW-minor**: Native migration audit: "The repository contains 148 Python files and 32 native Zag source files"; "All 148 Python files have been removed from the checked-out tree." Quantifies the Python→Zag split; baseline lacked — extends.
- 0627 R32_E51_ACTION_VALUE_GEOMETRY_AUDIT.md — **CONFIRMS**: E45–E50 terminal target semantics; UNKNOWN fixed at zero by E50.
- 0628 R32_E51AG_IMPLEMENTATION_CONTRACT.md — **CONFIRMS**: E51AG implementation contract frozen.
- 0629 CREDITS.txt — **NOISE**: CPython CREDITS file inside R42.
- 0630 R32_EPISTEMIC_R31_MATCHED_V10_PRELIM_2SEED_INTERPRETATION.md — **CONFIRMS**: V-interpretation family member (REFERENCE_ONLY).
- 0631 R32_EPISTEMIC_R31_MATCHED_V15A_INTERPRETATION.md — **CONFIRMS**: V-interpretation family member (REFERENCE_ONLY).
- 0632 R32_EPISTEMIC_R31_MATCHED_V16_INTERPRETATION.md — **CONFIRMS**: V-interpretation family member (REFERENCE_ONLY).
- 0633 R32_V10_REUSABLE_PROBE_HARDENING_INTERPRETATION.md — **CONFIRMS**: V10 reusable-probe hardening: FAILED HARDENING / CURRICULUM-ROUTING GAP (family detail).
- 0634 CLAIM_BOUNDARY.md — **CONFIRMS**: R33 FAIL_CLOSED claim boundary (V68 7 fails / V73 81 / V92 339).
- 0635 R32_V12_REUSABLE_PROBE_HARDENING_INTERPRETATION.md — **CONFIRMS**: V12 probe-hardening interpretation (family detail).
- 0636 R32_EPISTEMIC_R31_MATCHED_V15B_INTERPRETATION.md — **CONFIRMS**: V-interpretation family member (REFERENCE_ONLY).
- 0637 R32_EPISTEMIC_R31_MATCHED_V7_PRELIM_3SEED_INTERPRETATION.md — **CONFIRMS**: V-interpretation family member (REFERENCE_ONLY).
- 0638 R32_V33_SHA256.txt — **NOISE**: V33 checksum inventory.
- 0639 import-closure.txt — **NOISE**: Import-closure path listing.
- 0640 FINAL.md — **NEW-minor**: Fresh native Lane-B supplement: "V91 remains unimplementable faithfully from available bytes: original dataset, special tokens, forward/input construction, arithmetic and seeded sampling..." — anchors baseline's "proven unrecoverable".
- 0641 R32_EPISTEMIC_R31_MATCHED_V18_INTERPRETATION.md — **CONFIRMS**: V-interpretation family member (REFERENCE_ONLY).
- 0642 R32_V11_REUSABLE_PROBE_HARDENING_INTERPRETATION.md — **CONFIRMS**: V-interpretation family member (REFERENCE_ONLY).
- 0643 staging_hash_comparison.txt — **NOISE**: Staging hash comparison.

## Range B verdicts (0758–0871, 114 files)

- 0758 POSTRUN_DEPENDENCY_PINS.txt — **NOISE**: Postrun dependency pins; all OK (znc toolchain, N07 authority, N09 checkpoint, sandbox-exec).
- 0759 RECEIPT.txt — **NEW**: V91_NATIVE_ROUNDTRIP_RECOVERY_V1: "actual_native_generated=16"; "oracle_matches=16"; "native_frame_deterministic=true"; but "v91_full_gate_open=false" and "independent_adversarial_review_complete=false". Historical R27 semantic-recovery lane results; baseline lacked V91 closeout detail — extends.
- 0760 tnn-r27-native-master-shadow-CHECKSUMS.txt — **NOISE**: tnn-r27-native-master shadow checksum inventory.
- 0761 R32_V16_SHA256.txt — **NOISE**: V16 checksum inventory.
- 0762 R32_V37_SHA256.txt — **NOISE**: V37 checksum inventory.
- 0763 R33_NATIVE_N14_POSTRUN_ARTIFACTS_VERIFIED.txt — **CONFIRMS**: N14 postrun artifact verification: 50/50 OK on 2026-09-06.
- 0764 tnn-r30-big-boom-shadow-CHECKSUMS.txt — **NOISE**: tnn-r30-big-boom shadow checksum inventory.
- 0765 R32_V23_SHA256.txt — **NOISE**: V23 checksum inventory.
- 0766 R32_V44_SHA256.txt — **NOISE**: V44 checksum inventory.
- 0767 R32_V41_SHA256.txt — **NOISE**: V41 checksum inventory.
- 0768 R32_V21_PREHARDENING_SHA256.txt — **NOISE**: V21 pre-hardening checksum inventory.
- 0769 R32_V36_SHA256.txt — **NOISE**: V36 checksum inventory.
- 0770 behavior_leads.txt — **NOISE**: Behavior-lead file path list.
- 0771 R32_R31_EXACT_REPLAY_INTERPRETATION.md — **NEW**: R31 exact replay: "Status: **PASS_EXACT_EQUIVALENCE**"; seed 9700 rerun identical, "maximum absolute delta is 0.0"; "The earlier V3 synthetic A control is superseded as an evaluator and remains retained only as a rejected diagnostic." Baseline item 8 lacked the V3-supersession — fills.
- 0772 R32_V15A_SHA256.txt — **NOISE**: V15A checksum inventory.
- 0773 R32_V15B_SHA256.txt — **NOISE**: V15B checksum inventory.
- 0774 LICENSE.txt — **NOISE**: Apache license text.
- 0775 RECEIPT.txt — **NEW-minor**: V91 generator-recovery receipt: 16/16 oracle matches, "historical_python_executed=false", "foreign_ml_runtime_used=false", but "roundtrip_n128_parity=false" and "v91_full_gate_open=false". See 0759.
- 0776 RECEIPT.txt — **NEW-minor**: V91 dataset-recovery receipt: blake2 KAT pass, personalized fixture match; notes "zag_u64_logical_shift_workaround=true". See 0759.
- 0777 R32_V22_PREHARDENING_SHA256.txt — **NOISE**: V22 pre-hardening checksum inventory.
- 0778 R32_AGENT_FINAL_PACKAGE_REQUEST.txt — **NEW-minor**: R32 agent ran on branch `r32-agent-sequential-frontier`; 2026-08-31 snapshot request (nonce `e51ad-recovery-20260831-cce846d1`) to resume E51AD routing work after local workspace recycling; "R27 remains canonical." People/dates anchor — extends.
- 0779 R32_V31_SHA256.txt — **NOISE**: V31 checksum inventory.
- 0780 R32_V27_SHA256.txt — **NOISE**: V27 checksum inventory.
- 0781 RUNTIME_ENVIRONMENT.txt — **NOISE**: CI runtime environment pins (GitHub Actions Azure Linux runner).
- 0782 full_behavior_sources.txt — **NOISE**: Behavior-source path list (confirms /Users/Shared/micah/Documents/TNN local path).
- 0783 COORDINATION.md — **NEW**: Independent candidate: "sources/independent_supervisor.zag adds bounded kill-fallback EINTR retries and observed second-wait verification; fallback failure stays fail-closed." Supervisor-side engineering candidate; baseline lacked — fills.
- 0784 R32_V14A_SHA256.txt — **NOISE**: V14A checksum inventory.
- 0785 R32_V14B_SHA256.txt — **NOISE**: V14B checksum inventory.
- 0786 VERIFIED.txt — **CONFIRMS**: N13 artifact custody: all OK.
- 0787 R32_V42_SHA256.txt — **NOISE**: V42 checksum inventory.
- 0788 R32_V41_NEXT_CAUSAL_PROTOCOL.md — **CONFIRMS**: V41 next causal protocol: "No parseable V39 or V40 result... no scientific claim" — aligns with baseline items 10/11 (V39 rejected, V40 no interpretable result).
- 0789 tnn-v1-current-execution-FINAL-STATUS.md — **NEW-minor**: TNN v1 final status: `"archive_cleanroom_pass": false`, `"controlled_native_english_pass": false`, `"real_senses_probe_pass": false`, `"tnn_v1_beta": false` — all beta gates false. Baseline lacked a TNN-v1 gate snapshot — extends.
- 0790 stat.txt — **NOISE**: stat record (N19 recovery roots).
- 0791 SELECTION_FREEZE.md — **NEW**: R36 selection freeze: "Selected after preregistered development aggregation: `eig_012`"; fresh challenge "seeds 36203, 36209, 36217 on `abaca`, `gradual`, `success_only`, `long_return`"; "No source or threshold change is permitted before the fresh result." Baseline lacked R36 selection detail — fills.
- 0792 stat.txt — **NOISE**: stat record.
- 0793 stat.txt — **NOISE**: stat record.
- 0794 stat.txt — **NOISE**: stat record.
- 0795 stat.txt — **NOISE**: stat record.
- 0796 R32_V42_PRELIM_BUG_BOUNDARY.md — **CONFIRMS**: V42 diagnostic boundary: failed first launch corrected and rerun; no failed-run metric retained (execution-hygiene record).
- 0797 stat.txt — **NOISE**: stat record.
- 0798 stat.txt — **NOISE**: stat record.
- 0799 vendor.txt — **NOISE**: Vendored pip package list.
- 0800 R32_E51A_AGENT_RUN_REQUEST.md — **CONFIRMS**: E51A run request 2026-08-29: "This file contains no learner logic and changes no experimental factor" — preregistered execution trigger only.
- 0801 IMPLEMENTATION_NOTE.md — **NEW-minor**: E51G implementation note: "E51G must reuse the E51E sequential-state generator and terminal utilities exactly"; "evaluator-side desired action is used only as a training/evaluation consequence label and is never exposed as an input feature." Design rule; baseline lacked — extends.
- 0802 stat.txt — **NOISE**: stat record.
- 0803 stat.txt — **NOISE**: stat record.
- 0804 TRANSPORT_NOTE.md — **CONFIRMS**: E51AE transport: executable source assembled deterministically from fragments; binaries integrity-checked, never learner-visible.
- 0805 remote_refs.txt — **NEW-minor**: Git remote branches beyond the agent frontier: `r32-e52-joint-action-value-frontier`, `r32-e53-conservative-average-cost`. Baseline lacked branch names — extends.
- 0806 download_archive_candidates.txt — **NEW-minor**: Archive candidate list includes `TNN_COMPLETE_R1_R32_FULL_BACKUP.tar.gz` in Micah's Downloads — full R1–R32 backup existed; baseline lacked — extends (see 0836).
- 0807 tnn-v1-evidence-fibers-senses-search-CURRENT_STATUS.md — **NEW-minor**: TNN v1 status: "NATIVE_NEXT_STAGE_SUITE=PASS"; "EVALUATOR_CHECKS=23/23 PASS"; "TNN_V1_BETA=0"; "NATURAL_SENSES_READY=0". See 0789.
- 0808 R32_V38_AUTOCONTINUE_INTERPRETATION.md — **NEW-minor**: V38 autocontinue: "Files discovered: **1**; parseable JSON files: **0**"; "Status: **INCOMPLETE_OR_NO_PARSEABLE_RESULT**"; "No scientific interpretation was generated." New arm-level detail; baseline family verdict only — extends.
- 0809 stat.txt — **NOISE**: stat record.
- 0810 ENVIRONMENT.txt — **NOISE**: Environment pins (macOS znc toolchain hash).
- 0811 LINEAGE.txt — **NEW**: R28 lineage: "PARENT_FORMAT=TNN_PRE_V1_R27_GENERAL_LEARNING"; "PARENT_STEP=60423"; "BRANCH=TNN_R28_AEIF_NO_GRAPH_REBUILD"; "CANONICAL_PROMOTION=BLOCKED_PENDING_NATIVE_ZAG". Baseline lacked R28 lineage — fills.
- 0812 R32_E51G_STATUS.md — **CONFIRMS**: E51G status: staging started 2026-08-30; no scientific result claimed until native workflow executes.
- 0813 tnn-r31-endogenous-chunking-shadow-CHECKSUMS.txt — **NOISE**: tnn-r31-endogenous-chunking shadow checksums.
- 0814 POSTRUN_DEPENDENCY_PINS.txt — **NOISE**: Postrun dependency pins; all OK.
- 0815 RUN_REQUEST_20260830T2203_PDT.txt — **CONFIRMS**: E51AB run request: execution trigger only; "R27 remains canonical".
- 0816 entry_points.txt — **NOISE**: numpy entry-points listing.
- 0817 tnn-pre-v1-r28-aeif-no-graph-shadow-CHECKSUMS.txt — **NOISE**: tnn-pre-v1-r28-aeif-no-graph shadow checksums.
- 0818 host.txt — **NOISE**: Host OS record (macOS 26.6.2 / ARM64).
- 0819 stat.txt — **NOISE**: stat record.
- 0820 tnn-pre-v1-r5-goldilocks-CHECKSUMS.txt — **NOISE**: tnn-pre-v1-r5-goldilocks shadow checksums.
- 0821 BINARY_SHA256SUMS.txt — **NOISE**: E51AH build checksum list (two byte-identical builds).
- 0822 tnn-pre-v1-r6-rsi-CHECKSUMS.txt — **NOISE**: tnn-pre-v1-r6-rsi shadow checksums.
- 0823 RUN_REQUEST.txt — **CONFIRMS**: E51C run request: no factor changed.
- 0824 RECEIPT.txt — **CONFIRMS**: Receipt: failures=0, canonical R27 unmutated, no learner authority.
- 0825 host.txt — **NOISE**: Host OS record.
- 0826 RUN_REQUEST.txt — **CONFIRMS**: E51D run request: frozen-terminal reachability audit trigger.
- 0827 CLAIM_BOUNDARY.md — **CONFIRMS**: E51G claim boundary: "This directory does not establish a result by existence alone."
- 0828 RECEIPT.txt — **CONFIRMS**: Receipt: failures=1, canonical R27 unmutated (negative receipt kept).
- 0829 RUN_REQUEST.txt — **CONFIRMS**: E51B run request: no factor changed.
- 0830 R32_V39_FILELIST.txt — **CONFIRMS**: V39 file list includes R32_V39_FAILED.json — matches baseline item 10.
- 0831 R32_V40_FILELIST.txt — **CONFIRMS**: V40 file list includes R32_V40_FAILED.json — matches baseline item 11.
- 0832 RUNTIME_ENVIRONMENT.txt — **NOISE**: Linux runtime environment record.
- 0833 EXECUTION_BOUNDARY.md — **CONFIRMS**: E51G execution boundary: "remains unexecuted until a native workflow run exists."
- 0834 COMPILER_SHA256SUMS.txt — **NOISE**: Compiler checksum.
- 0835 R33_NATIVE_N12_POSTRUN_ADMISSION_PINS.txt — **CONFIRMS**: N12 freeze/admission pins OK.
- 0836 drive_backup_checksum.txt — **NEW-minor**: Drive backup checksum for `TNN_COMPLETE_R1_R32_FULL_BACKUP.tar.gz`: `f966c0c7f1649feb1e83436b21d7c51a41442e8a9f3f4f41c33f08affbb3d748` (see 0806).
- 0837 final_entry.command_exit.txt — **NOISE**: Final-entry exit code 0.
- 0838 R33_NATIVE_N13_FINAL_ADMISSION_VERIFIED.txt — **CONFIRMS**: N13 freeze/admission pins OK.
- 0839 R32_MIDCAMPAIGN_SNAPSHOT_SHA256.txt — **CONFIRMS**: R32 midcampaign snapshot archived.
- 0840 RECEIPT.txt — **CONFIRMS**: Receipt: failures=0, canonical R27 unmutated.
- 0841 PROCESS_CLEANUP.txt — **NOISE**: Process cleanup record.
- 0842 entry_points.txt — **NOISE**: pip entry-points listing.
- 0843 history.py.txt — **NEW-minor**: Evidence-custody practice: "Historical interpreter source is inert byte evidence only. It is never executed." Baseline lacked this custody rule — extends.
- 0844 PROCESS_CLEANUP.txt — **NOISE**: Process cleanup record.
- 0845 R32_V10_REUSABLE_PROBE_HARDENING_SOURCE_SHA256.txt — **NOISE**: V10 hardening source checksum.
- 0846 NO_EVIDENCE_YET.md — **CONFIRMS**: E51G: "Native E51G evidence pending implementation and execution."
- 0847 PLACEHOLDER.md — **NOISE**: Placeholder file.
- 0848 SOURCE_COMMIT.txt — **NOISE**: Source commit SHA record.
- 0849 FROZEN.txt — **NEW-minor**: Date anchor: "EVIDENCE_FROZEN_UTC=2026-09-15T18:18:30Z". Baseline lacked — extends.
- 0850 isolation.txt — **CONFIRMS**: learner_core_isolation=true.
- 0851 receipt.txt — **CONFIRMS**: Receipt: qualification_failures 0.
- 0852 end_utc.txt — **NOISE**: End-UTC timestamp.
- 0853 start_utc.txt — **NOISE**: Start-UTC timestamp.
- 0854 end-utc.txt — **NOISE**: End-UTC timestamp.
- 0855 start-utc.txt — **NOISE**: Start-UTC timestamp.
- 0856 WORKFLOW_RUN_ID.txt — **NOISE**: Workflow run-id record.
- 0857 LOCAL_X86_RUNTIME_SECONDS.txt — **NOISE**: Runtime-seconds record.
- 0858 RUNTIME_SECONDS.txt — **NOISE**: Runtime-seconds record.
- 0859 LOCAL_EXIT_CODE.txt — **NOISE**: Exit-code record.
- 0860 LOCAL_X86_EXIT_CODE.txt — **NOISE**: Exit-code record.
- 0861 BYTE_IDENTICAL.txt — **NOISE**: Byte-identical flag record.
- 0862 EXIT_CODE.txt — **NOISE**: Exit-code record.
- 0863 SOURCE_PIN_GATE.txt — **NOISE**: Source-pin gate record.
- 0864 LOCAL_RUNTIME_SECONDS.txt — **NOISE**: Runtime-seconds record.
- 0865 RUN_ATTEMPT.txt — **NOISE**: Run-attempt record.
- 0866 exit_code.txt — **NOISE**: Exit-code record.
- 0867 exit-code.txt — **NOISE**: Exit-code record.
- 0868 r27_general_archive_candidates.txt — **NOISE**: Empty file.
- 0869 source_definition_hits.txt — **NOISE**: Empty file.
- 0870 large_unreachable_blob_search.txt — **NOISE**: Empty file.
- 0871 isolation.forbidden.txt — **NOISE**: Empty file.

## Keyword sweep (both ranges)

- `koryphaios`: one hit — 0568_archives.txt, an archive inventory path (`/Users/Shared/micah/Documents/koryphaios/.koryphaios/...`); no koryphaios code content anywhere.
- `ghost`: zero hits in both ranges.
- `sylorlabs`: two hits — 0561/0600 (post-N13A parent-source recovery) referencing the scoped `Sylorlabs/TNN` GitHub remote check; confirms the sylorlabs org as the canonical remote (baseline-known).
- No contradictions with the baseline were found in either range.

## Five most important NEW items

1. **R6 pre-v1 RSI handoff** (0612): compositional mutation grammar replacing the finite candidate list, able to create operators/memory organizations/sensory policies/training policies, verifier+rollback independent — the actual self-architecture plan; fills baseline gap on self-arch.
2. **R26State / R27 trace contract** (0609/0589): old brain state had `video_encoder`, `video_entity_policy`, `speech_segmenter`, `speech_index`, `semantic_generator`, `self_revision_history`; R27 trace contract was `raw evidence -> core signature -> PAM route -> entity hypothesis -> memory retrieval` — fills baseline gap on senses/PAM origins.
3. **R36 selection freeze** (0791): `eig_012` selected after preregistered aggregation; fresh challenge on seeds 36203/36209/36217 (`abaca`, `gradual`, `success_only`, `long_return`) — new experiment-line state not in baseline.
4. **R31 exact replay** (0771): PASS_EXACT_EQUIVALENCE (seed 9700, delta 0.0), and the V3 synthetic A control explicitly "superseded as an evaluator and remains retained only as a rejected diagnostic" — fills baseline item 8's missing supersession detail.
5. **Pure-Zag law date** (0613): direct human instruction 2026-09-05 after C03 superseded older Python-for-supervision permission — dates the native-only contract; fills baseline gap.
