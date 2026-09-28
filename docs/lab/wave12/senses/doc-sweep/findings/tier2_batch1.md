# Tier2 batch1 skim findings (114 files)

Batch: `batches/tier2_batch1.json`. Skim method: first ~25 lines + keyword sweep
(verdict/PASS/FAIL/NO_GO/abandon/PAM/vision/audio/memory/kill/pin/koryphaios/ghost/RSI/seed/prereg/author)
per file; full read for 4 files + decision-section extraction for the 30-file R32
V-interpretation family. Note: the batch manifest's `local` names were stale
renumbering; real local filenames resolved via `manifest.json` (download-index
names like `0530_...`, `0612_...`). Identifiers below use the Drive path.

**Counts:** 114 skimmed (digest) · 4 read fully (V39 interpretation, R5 handoff,
R6 RSI handoff, R34 v3 worklog) + full-decision sections for the V-family ·
**22 NEW findings** (incl. minors) · 92 CONFIRMS/NOISE/SUPERSEDED.

No contradictions with the baseline were found. One open question flagged (R34 v3
"deterministic RNG" use, §8 below) — recorded as a question, not a contradiction.

---

## NEW findings

### 1. Dated origin of the pure-Zag law — direct human instruction 2026-09-05
- `TNN/TNN/Research/R33_NATIVE_ONLY_EXECUTION_CONTRACT.md` (2506 bytes, 2026-09-18T22:21:14Z)
- Verdict: **NEW** (category 6: people/dates anchoring). Baseline has "pure Zag over Python" as a standing law but not when/why it became a contract.
- > "Effective: direct human instruction2026-09-05, after C03. This supersedes older
permissions to use Python as external supervision, packaging or evaluation."
- Extends the standing-laws baseline: the law crystallized as a dated human instruction after the C03 gate, explicitly revoking older permissions.

### 2. R5 pre-v1 continuation plan — motif binding + developmental-media senses roadmap
- `TNN/TNN/Research/tnn-pre-v1-r5-NEXT_STAGE_HANDOFF.md` (2678 bytes, 2026-08-23T20:27:27Z)
- Verdict: **NEW** (categories 1, 4). Old roadmap naming mechanisms the baseline lacks.
- > Priority 1 — one-shot motif binding without interference: "support-gap recruitment using explicit motif confidence; reversible longest-match cells rather than additive substring voting; context-indexed exact spans; shadow replay against old constructions and delayed interference."
- > Priority 3 — natural developmental media: "synchronized raw speech and environmental audio;" ... "no pretrained vision, OCR, speech-to-text, or LLM inside TNN cognition."
- Fills senses-origins and memory-origins gaps: R5-era plan used reversible motif cells, shadow replay, and set the original senses doctrine (raw speech/audio, no pretrained models inside cognition).

### 3. R6 pre-v1 RSI handoff — the actual self-architecture plan, 7 priorities
- `TNN/TNN/Research/tnn-pre-v1-r6-rsi-NEXT_STAGE_HANDOFF.md` (2536 bytes, 2026-08-23T20:27:30Z)
- Verdict: **NEW** (categories 1, 4). Baseline only notes a "pre-v1 RSI self-architecture revision note"; this is the full R6 continuation handoff.
- > "Priority 6 — expand recursive self-improvement: Replace the finite candidate list with a compositional mutation grammar that can create new local operators, memory organizations, sensory policies, and training policies. The verifier and rollback mechanism must remain independent of any candidate under test."
- > Priority 1 shadow-tests policies: "consolidate now; request one more example; re-inspect the sensors; preserve alternatives; stop learning this motif; split a context-specific meaning."
- Also names "protected Grounded Contrastive Schema Memory" (old memory system name) and Priority 3's "controlled caption timing". Extends the RSI-origins baseline item substantially.

### 4. R26State dataclass — old brain state had video/speech subsystems
- `TNN/TNN/Research/R33_NATIVE_N17_R27_CONTINUITY/SOURCE_REFERENCES/r26_digest_excerpt.py.txt` (2644 bytes, 2026-09-18T22:21:13Z)
- Verdict: **NEW** (category 4: senses origins). Baseline knows PAMs were dropped but not this state layout.
- > "@dataclass class R26State: ... video_encoder:Any / video_entity_policy:Dict[str,Any] / speech_segmenter:Any / speech_index:Dict[str,int] / ... semantic_generator:Any / sibling_policy:Dict[str,Any] / ... self_revision_history:List[Dict[str,Any]]"
- Establishes video_encoder, video_entity_policy, speech_segmenter, speech_index were first-class fields of the pre-v1 brain state — the perceptual machinery was structurally central, not a bolt-on.

### 5. R27-era causal-traceability contract — old pipeline had PAM + entity stages
- `TNN/TNN/Research/TNN_R27_TRACEABILITY.md` (3102 bytes, 2026-09-18T22:21:15Z)
- Verdict: **NEW** (categories 1, 4). Baseline's five-organ architecture doesn't include these stages.
- > "Stages cover sensor, PAM, routing, entity, memory, world model, language, social learning, architecture revision, and action/observation decisions."
- > Intent trace chain: "raw evidence -> core signature -> PAM route -> entity hypothesis -> memory retrieval -> world/language binding -> decision -> error -> failure diagnosis -> PAM/memory revision"
- Adds the old R27 cognitive pipeline (core signature → PAM route → entity hypothesis) the current architecture lacks; the 2026-09-05 extension made traceability "a promotion gate for all future mutable cognition".

### 6. V39 GRU PAM rejection — the stated causal rationale
- `TNN/TNN/Research/R32_EPISTEMIC_R31_MATCHED_V39_INTERPRETATION.md` (4083 bytes, 2026-08-23T20:23:22Z, read fully)
- Verdict: **NEW** (category 2: abandoned direction + why). Baseline knows "R32 acoustic PAMs DROPPED" and "V39 2-layer GRU PAM" but not this experiment's stated reason.
- > "**Generic recurrent model capacity is not the missing mechanism.** The ordered raw prefix was available, the recurrent route trained and converged, and a modest recall increase was possible, but it broadened the action region rather than identifying the positive option-value boundary."
- Decision-positive MAE 0.23289→0.23560 (no gain); recurrent variance head weaker (R² 0.36059→0.21972); recurrent mean+variance arm selected realized advantage −0.07726 vs V38. The PAM was rejected for broadening action without identifying the value boundary, not for implementation failure.

### 7. R34 v2 native continual-learner worklog — latent-context memory test results
- `TNN/TNN/Research/R34_NATIVE_CONTINUAL_LEARNER_V2/WORKLOG_20260916.md` (2819 bytes, 2026-09-18T22:21:15Z)
- Verdict: **NEW** (category 3: test results never seen). Baseline mentions R34 memory files + delayed-credit drop, not v2 numbers.
- > "The learner maintains two latent context memories. A negative surprise on an exploit decision can allocate or reselect a context; no hidden regime label is passed to the learner."
- Results: untrained regime-A 8/16 → 16/16 after 24 A experiences; after hidden switch, 16/16 on B; return to A 15/16 with zero score/count updates during return; 48 updates total; reward-scrambled control 0/16; byte-identical rerun (ingress 302/302, tick 301000/301000); inner-state corruption refused (status 2005).

### 8. R34 v3 worklog — structural evaluator isolation + unexplained "deterministic RNG"
- `TNN/TNN/Research/R34_NATIVE_CONTINUAL_LEARNER_V3/WORKLOG_20260916.md` (2367 bytes, read fully)
- Verdict: **NEW-partial + OPEN QUESTION**. New: v3 made the evaluator boundary structural — "The learner core is now a separate source module and imports only the observation contract. World mutation, hidden regime changes, reward production, checkpoint assembly, persistence orchestration, and qualification controls live in the harness." Same 8/16→16/16, 48-updates witness.
- Flag (not a contradiction — the law bans RNG in AI decision paths; use is undocumented): "`r34_learner_core.zag` contains learner state, deterministic RNG, action choice, score/count updates, latent-context switching..." — what the deterministic RNG drives is not stated. Recommend asking a later sweep reader to trace it.

### 9. N17 verify contract — the eight named policy gates + single active promotion
- `TNN/TNN/Research/R33_FINAL_INTEGRATION_20260915T2145Z/n17_lane_witness/prior_status/VERIFY_CONTRACT.md` (4643 bytes)
- Verdict: **NEW-minor** (extends gates baseline; senses-adjacent). Baseline knows phase-transition gates but not the old gate names.
- Eight gates: `TEENAGER_ENGLISH, ADULT_ENGLISH, NATURAL_VIDEO_AUDIO, HUMAN_SUPERIORITY, NATIVE_ZAG, OPEN_ENDED_RECURSIVE_SELF_IMPROVEMENT, AHI, PRODUCTION_TNN_V1`; "exactly one active promotion: STRONGER_MASTER_GENERAL_SPECIFIC_BRIDGE". R26 verifier rows included video-artifact/frame thresholds, speech candidate failure + retained VAD control, and "preserved negative/partial dispositions for ... speech, visual debate and video-noise proposals".

### 10. N17 blockers — old capability names: social evaluators, name memory
- `TNN/TNN/Research/R33_CLOSEOUT_20260915T174458Z/N17_BLOCKERS.txt` (3870 bytes)
- Verdict: **NEW-minor** (category 4-adjacent: old systems). R27-08/09: "serialized abstraction model and original SOCIAL_FAR evaluator", "mixed SOCIAL_NEAR/FAR evaluator"; R26-16: "No reviewed native implementation of name_memory.resolve and original true_to_node mapping"; R26-08/09: absent exact video artifact bytes. Adds old capability inventory the baseline lacks.

### 11. E51AJ validation specifics — retention rule failed 2 of 3 replicas
- `TNN/TNN/Research/R32_E51AJ_ANALYSIS/VALIDATION.md` (3602 bytes)
- Verdict: **NEW-minor** (category 3). Baseline only notes E51AJ as the completed frontier.
- > "The preregistered retention rule fails in replicas 0 and 1 and passes in replica" [2];
"The separate aggregate no-final-behavioral-tradeoff flag fails in every replica." Validated over 1,101,600 native episode rows and 67,860 coefficient rows. Matches the baseline scorecard's MIXED_OR_UNREPLICATED retention direction with exact numbers.

### 12. E51N — seed-namespace exhaustion negative result
- `TNN/TNN/Research/R32_E51N_SEED_NAMESPACE_DIAGNOSTIC.md` (3140 bytes, executed 2026-08-30)
- Verdict: **NEW-minor** (category 3). "The allocator failed after allocating 8,352 of the 18,360 requested E51N worlds. Continuing with new stage numbers or more retries cannot provide the required complete fresh partition under this finite global-component-disjointness contract." A concrete infrastructure negative never seen by the program.

### 13. N13 postrun diagnosis — `_zag_free` doesn't reclaim (toolchain defect root cause)
- `TNN/TNN/Research/R33_N13_POSTRUN_MEMORY_DIAGNOSIS/DIAGNOSIS.md` (3107 bytes)
- Verdict: **NEW-minor**. Beyond the 3 known znc bugs: "At compiler source line2129, _zag_free evaluates its argument but does not reclaim memory. At3540 onward, the allocator bumps through64MiB arenas." Root-caused the N13 RSS blowout (409,862,144 bytes RSS). Toolchain-history fact.

### 14. Native migration audit 2026-08-29 — the 148-Python/32-Zag split, named native files
- `TNN/TNN/Research/TNN_NATIVE_MIGRATION_STATUS.md` (2249 bytes)
- Verdict: **NEW-minor** (category 6). "The repository contains 148 Python files and 32 native Zag source files" — 116 explicitly REFERENCE_ONLY; the rest "none is called by a native .zag program or enters the native compiler execution path as learner cognition." Names old native cognition: `tnn_r28_aeif.zag`, `tnn_r30_big_boom.zag`, `tnn_r31_endogenous_chunking.zag`, `tnn_r32_epistemic_chunking.zag`, E45–E50 terminal controllers.

### 15. Lane-B final — quantified scale of the failed recovery search
- `TNN/TNN/Research/R33_NATIVE_N17_R27_CONTINUITY/LANE_B_FINAL_NATIVE_20260915/FINAL.md` (1923 bytes)
- Verdict: **NEW-minor** (anchors baseline's "proven unrecoverable"). "Deep search: 947360 returned paths, 889854 hashed files, 157 archive inventories, all1610 Git blobs (744029506 bytes) hashed. No missing exact source/state/manifest input admitted." Also: the 508-byte R25 historical receipt "was recovered from ZIP and TAR under an R28 alternate member" — witness custody only.

### 16. R33 scenario battery — planned-but-unexecuted scenario families
- `TNN/TNN/Research/R33_SCENARIO_BATTERY.md` (3829 bytes)
- Verdict: **NEW-minor** (category 1). 14 scenario families for future scientific campaigns: sensor integrity, identity, temporal causality, memory pressure, human withdrawal (H0–H5), social provenance ("correct, stale, correlated, conflicting and misleading reports"; teacher separation), self-model, plasticity, and "Continuous multimodal life: Natural audio/video/action under delay, pressure, withdrawal and revisions". Unexecuted design inventory.

### 17. archives.txt — koryphaios sighting + old bundle names
- `TNN/TNN/Research/R33_NATIVE_N17_R27_CONTINUITY/RECOVERY_20260915_B_INDEPENDENT/TERMINAL_SUPPLEMENT_20260915/evidence/archives.txt` (3526 bytes)
- Verdict: **NEW-minor** (category 7 + people anchoring). Lists `/Users/Shared/micah/Documents/koryphaios/.koryphaios/eval-tools/deno/2.9.6/download.zip` — only koryphaios hit in batch; anchors the project on Micah's machine alongside TNN. Also old bundle names: `R32_V38/V39/V40_BUNDLE.tar.gz`, `tnn-pre-v1-r5-goldilocks.zip`, `tnn-r30-big-boom-shadow.zip`, `tnn-v1-evidence-fibers-senses-search.zip`, `tnn-pre-v1-r6-rsi.zip`.

### 18. Old program-induction native test artifact
- `TNN/TNN/.scratch/tnn-debug-script.txt` (3169 bytes, 2026-08-23)
- Verdict: **NEW-minor** (old capability). A generator/evaluator harness for program-induction tasks (task,a,b,c,d,hidden_ok,nearest_ok) ending in `TNN_V1_PROGRAM_INDUCTION_NATIVE_PASS,1`. Baseline has no program-induction artifact.

### 19. R23 archive provenance — recovered from Micah's ChatGPT Library
- `TNN/TNN/Research/R33_NATIVE_N17_R27_CONTINUITY/V91_SEMANTIC_KAT/RECOVERY_EXACT_R23_SOURCE_20260917.md` (3984 bytes)
- Verdict: **NEW-minor** (category 6 anchoring). "The original release archive `tnn-pre-v1-r27-general-learning.zip` was recovered from the user's existing ChatGPT Library artifact" — locates where the missing R23 source turned up.

### 20. Novel TNN experiment portfolio 2026-09-11 — six new hypotheses E01–E06
- `TNN/TNN/Research/R33_NOVEL_TNN_EXPERIMENTS_20260911.md` (4663 bytes)
- Verdict: **NEW-minor** (category 1; hypotheses, not results). E01 adaptive support-manifold routing; E02 conflict-triggered specialist isolation; E03 future-relevance rehearsal memory ("rehearsal priority estimates future decision utility rather than recency/frequency alone"); E04 uncertainty-budgeted active inquiry; E05 motif-generated connectivity with exact reconstruction; E06 structural-value meta-controller. Not in the baseline's experiment inventory.

### 21. E51 causal map — lineage with invalid/frozen branches
- `TNN/TNN/.scratch/e51ah/actions-33944536498-yhVo1A/extracted/Research/R32_E51_CAUSAL_MAP.md` (4057 bytes)
- Verdict: **NEW-minor** (category 2). Lineage E51X→E51Y→E51Z/AA→AB/AC→AD→AE→AF (INVALID, never run; "historical prerequisites mismatch") →AG (stable negative on 3 fresh partitions; "critical residual support omits slot-covered cases") →AH (FROZEN_NOT_RUN). Documents which branches died how.

### 22. N14 sensor authoring — built on N06 sensor source, max-PCM fixture
- `TNN/TNN/Research/R33_NATIVE_N14_SENSOR_INFORMATION/AUTHORING_HISTORY.md` (2994 bytes)
- Verdict: **NEW-minor** (extends senses inventory). "The candidate `sensor.zag` is byte-identical to the consumed N06 sensor source"; PCM minimum-rate fixture "strengthened ... to the maximum 131,072-byte mono payload containing every signed PCM16 codeword exactly once."

---

## R32 V-interpretation family — collective verdict (30 files, all REFERENCE_ONLY)

The 30 `R32_EPISTEMIC_R31_MATCHED_V*_INTERPRETATION.md` + 3 probe-hardening files
form one coherent retained/rejected-arm log. **CONFIRMS/NOISE as a family** —
their decisions are consistent with the baseline's inherited-frontier framing;
only V39 carried NEW rationale (see §6). Family statuses:
V5 overabstention; V7 temporal-state retained; V9 runaway fixed/economics wrong;
V10 prelim mechanism retained; V10 hardening FAILED (curriculum-routing gap);
V11 overcorrection; V12 curriculum-only repair rejected; V15A episodic credit
retained/stopping failure; V15B stopping improved; V16 current-epoch retained;
V17 balance rejected; V18 broadcast rejected; V25–V30 resource shadow price,
candidate history retained, absolute gates rejected; V31–V37 predictive-dynamics
ceiling audits; V38 repeated-continuation retained; V40 hazard state retained,
live qualification next; V41 live resolution rejected; V43 stage routing
rejected; V44 option-completion failure confirmed. Notable sub-detail: V44
found only 16.57% of initial states have positive multi-trial option value —
"much of V41's abstention is economically correct rather than an architectural failure."

## Per-file verdicts (CONFIRMS / SUPERSEDED / NOISE)

- 0530 R33_FIRST_DELIVERABLE.md — CONFIRMS (R33 delivery boundary, R27 canonical).
- 0531 V91_STATUS.md — CONFIRMS (V91 parity fail-closed; 0/16 oracle match lines match baseline).
- 0532 R33_PARENT_SOURCE_RECOVERY_N12_LEADS.md — CONFIRMS (leads remain leads; aligns with "recovery unrecoverable").
- 0533 GATE_FAILURES.md — NOISE (C compile-gate failure log).
- 0534 / 0550 / 0590 CURRENT_ENTRY_POINT.md (3 copies) — CONFIRMS (R33 closeout status; V92 339 checks, V68 fails 7, V73 exits 81 — new counts kept at §104).
- 0535 agent_evidence_report.md — CONFIRMS (V91 semantic-generator recovery detail).
- 0537 / 0584 R32_E51_GENERALITY_SCORECARD.md (2 copies) — CONFIRMS + minor NEW folded into §11/§21 (E51AJ outcome MIXED, E51AH FROZEN_NOT_RUN).
- 0538 R33_PROGRAM_CHARTER.md — CONFIRMS ("TNN means True Neural Network"; white-box autonomy target).
- 0540 / 0544 / 0563 VERIFY_CONTRACT.md (3 lanes) — CONFIRMS (N17/N18/N19 contract inventories) except §9's new gate names.
- 0541 R33_PARENT_SOURCE_RECOVERY_AFTER_N11.md — CONFIRMS (searched Micah's Codex sessions/attachments: `/Users/Shared/micah/.codex/...`, 131 pre-Sep-5 session files, no match; N11 "explicitly main-author").
- 0542 V91_STATUS.md — CONFIRMS (fail-closed, 0 strings).
- 0543 HOST_ABI_CONTRACT_V1.md — CONFIRMS (N19 capability-based host contract, prospective).
- 0545 R32_E45_ARM64_7CAC_AGGREGATE_ABI_REPORT.md — NOISE (compiler determinism diagnostic, byte-identical binaries).
- 0547 R32_E45_E48_NATIVE_QUALIFICATION_REPORT.md — CONFIRMS ("FOUR VALID NATIVE NEGATIVES — R27 REMAINS CANONICAL").
- 0548 policy_native.initial_missing_reader.txt — CONFIRMS (Zag policy parser; gate list overlaps §9).
- 0553 SHA256_VERIFY.txt / 0568 n11-pins / 0580/0581/0582 pin files / 0604/0605 N09 pins / 0572/0593/0608/0619 artifact SHA lists — NOISE (checksum inventories).
- 0559 final_transport.commands.txt — NOISE (command log).
- 0562 R33_WHITE_BOX_OBSERVABILITY_CONTRACT.md — CONFIRMS (trace chain "Evidence → memory retrieval → live hypotheses → ... → update/regret"; mutable-state inventory includes RNG stream position — checkpoint coverage item, not a contradiction of the no-RNG law).
- 0564 extend.txt / 0570 LICENSE.md / 0576 API_CHANGES.txt / 0629 CREDITS.txt — NOISE (CPython venv files inside R42).
- 0566 VALIDATION.md — see §11 NEW-minor.
- 0567 R33_B000_LAUNCH_CONTRACT.md — CONFIRMS (B000 launcher sandbox limits).
- 0571 V31 … (see family verdict).
- 0577 AMENDMENT_REQUEST.md — SUPERSEDED/CONFIRMS (proposed FROZEN_PARENT_NATIVE_SURROGATE_COMPOSITE class; proposal only, no effect).
- 0579 / 0599 / 0608 R25_LINEAGE_REQUIREMENTS.md — CONFIRMS (r25 member hashes absent; R25 receipt witness-only).
- 0583 HASH_ORACLE_PROVENANCE.md — CONFIRMS-minor ("transcribed by the main author" = Micah, from NIST/RFC — people anchor).
- 0585 tnn-debug-script.txt — see §18 NEW-minor.
- 0587 E51N diagnostic — see §12 NEW-minor.
- 0594/0595/0598/0622/0624/0630/0631/0632/0636/0637/0641/0642 V-family — see family verdict.
- 0596 R32_E51AE_IMPLEMENTATION_CONTRACT.md / 0628 R32_E51AG_IMPLEMENTATION_CONTRACT.md / 0607 R32_E51AH_IMPLEMENTATION_CONTRACT.md — CONFIRMS (E51AE/AG/AG frozen contracts; UNKNOWN=0, stage pins).
- 0597 import_paths.txt / 0639 import-closure.txt — NOISE (path listings).
- 0601 R34 v2 worklog — see §7 NEW. 0621 R34 v3 worklog — see §8 NEW/question.
- 0610 R33_TRAINING_TECHNIQUE_TOURNAMENT.md — CONFIRMS (prospective technique tournament plan).
- 0611 evidence_record.initial_transform_failure.txt — NOISE (Zag serializer source).
- 0615 N08A / 0619 N08 / 0593 N08B ARTIFACTS_VERIFIED.txt — NOISE (checksum inventories).
- 0616 HOST_V2_WORKLOG_20260913.md — NOISE (host-adapter authoring checkpoint; notes a revoked tool token, "Tool failure is not a compiler failure").
- 0617 SOURCE_SHA256SUMS.txt / 0638 R32_V33_SHA256.txt / 0602 E47 SHA / 0623 E49 SHA / 0625 E48 SHA — NOISE.
- 0620 FINAL.txt (N19 process gaps) — CONFIRMS (PASS_BOUNDED_NATIVE_ENGINEERING) + notes an agent-caused dir rename, restored; engineering receipt.
- 0627 R32_E51_ACTION_VALUE_GEOMETRY_AUDIT.md — CONFIRMS (E45–E50 terminal target semantics; UNKNOWN fixed at zero by E50; missing "continuation of an initiated investigation" action).
- 0634 CLAIM_BOUNDARY.md — CONFIRMS (R33 FAIL_CLOSED; V68 7 fails / V73 81 / V92 339; N17 30+32 deficits).
- 0643 staging_hash_comparison.txt — NOISE.

**Cross-batch keyword sweep:** only koryphaios hit in batch is §17 (archives.txt).
No "ghost" hits. No additional PAM/vision/audio origins beyond §2/§3/§4/§9/§10/§22.
