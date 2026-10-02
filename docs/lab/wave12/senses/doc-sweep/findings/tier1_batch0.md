# tier1_batch0 findings — 52 files read (all R33/R32-era research docs, Sept 2026)

Baseline: BASELINE.md. No ghost/koryphaios mentions anywhere in this batch (those hits live in files 0416/0424/0436/0476/0568 — NOT in this batch; flag for those batch readers).

Note: 0000–0010 are cumulative snapshots of one journal (each a strict prefix of the next). 0015–0019 are cumulative README snapshots. 0038/0039 byte-identical.

---

## 0000_R33_EXECUTION_JOURNAL.md
- Drive: TNN/TNN/Research/R33_EXECUTION_JOURNAL.md · 124,814 B · 2026-09-18
- Verdict: **NEW**
- Findings: (a) N13 legacy-Torch-view primary FAILED at the inventory RSS gate (409,862,144 B observed vs 402,653,184 frozen; diagnosis: `_zag_free` is a no-op and bump allocations accumulate; 140,083,200 B header-table + 110,333,672 B copied by two evaluator fingerprints). (b) N13A corrective regression (1,216-byte reused SHA scratch per fingerprint) PASSED: 6/6 children, 24,601 child checks, peak child RSS 316,833,792 B, exact fresh-process replay, independent `CONFIRM_BOUNDED_ENGINEERING_PASS`. (c) N14 (S1 sensor-information preservation) closed `COMPLETED_VERIFIED_CONSUMED_BOUNDED_S1_ENGINEERING_PASS`, 182 child checks. (d) N15 stability/plasticity closed CONSUMED NEGATIVE (`CONFIRM_CONSUMED_NEGATIVE_WITH_PROMISING_FRONTIER_SIGNAL`): additive+preservation reduced interference but "protected-anchor coverage did not generalize sufficiently" — 156 arm-population exposures. (e) N16 (old-support protection + selective additive specialist routing) reached FULL qualification: native gates 1/1/1 across dev/validation/confirmation, 498 fresh arm-population exposures, `CONFIRM_FULL_PREREGISTERED_SYNTHETIC_N16_QUALIFICATION`. (f) J080 (Sept 15): the original R27 release archive was RECOVERED — `tnn-pre-v1-r27-general-learning.zip` (56,777,645 B, SHA256 `7042ff8497…b65e`) matched the historical release checksum; embedded `state/r27-accepted-state.pkl` matched canonical `31e670fc…96e5a`; recovered `r27_experiments.py` lineage, `R27State.digest()`, `scripts/verify_r27.py`, 33-check verifier semantics. This partially supersedes the baseline's "unrecoverable" framing for the R27 release specifically (trace-op/perceptual semantics remain unrecovered). (g) N17 (native R27 continuity) and N18 (frozen-core sidecar) remain DESIGN-ONLY; the sidecar shortcut was rejected: "an unchanged R27 file does not make an unqualified native execution path canonical R27." Independent reviewer identity "Euler" recurs across N12–N18 reviews.
- Quote: "Byte custody proves non-mutation, not behavioral continuity."

## 0001_R33_EXECUTION_JOURNAL.md
- Drive: TNN/TNN/Research/R33_REMEDIATION_20260915T2152Z/before/Research/R33_EXECUTION_JOURNAL.md · 124,076 B · 2026-09-18
- Verdict: **SUPERSEDED** — strict prefix of 0000 (missing only the final dated remediation line, 2026-09-15T21:57:24Z: "safe custody seal repair and stale R26-46 receipt wording correction are complete").

## 0002_R33_EXECUTION_JOURNAL.md
- Drive: TNN/TNN/Research/R33_NATIVE_N16_SUPPORT_ROUTING/PREFLIGHT_01/R33_EXECUTION_JOURNAL.md · 96,873 B · 2026-09-18
- Verdict: **SUPERSEDED** — prefix of 0000 (ends at J072, N16 preregistration/reservation; N16 execution, J080 recovery, N17/N18 all live only in 0000).

## 0003_JOURNAL_AT_RESERVATION.md
- Drive: TNN/TNN/Research/R33_NATIVE_N15_PRESERVATION_ADDITIVE/PREFLIGHT_01/JOURNAL_AT_RESERVATION.md · 91,018 B · 2026-09-18
- Verdict: **SUPERSEDED** — prefix of 0000 (ends at J068, N15 preregistration).

## 0004_JOURNAL_AT_RESERVATION.md
- Drive: TNN/TNN/Research/R33_NATIVE_N14_SENSOR_INFORMATION/PREFLIGHT_01/JOURNAL_AT_RESERVATION.md · 83,402 B · 2026-09-18
- Verdict: **SUPERSEDED** — prefix of 0000 (ends at J064, N14 preregistration).

## 0005_R33_EXECUTION_JOURNAL.md
- Drive: TNN/TNN/Research/R33_N13A_CLOSEOUT_SNAPSHOT_V1/Research/R33_EXECUTION_JOURNAL.md · 80,986 B · 2026-09-18
- Verdict: **SUPERSEDED** — prefix of 0000 (ends at J060, N13A approval/reservation).

## 0006_JOURNAL_AT_RESERVATION.md
- Drive: TNN/TNN/Research/R33_NATIVE_N13A_FINGERPRINT_SCRATCH/PREFLIGHT_04/JOURNAL_AT_RESERVATION.md · 75,517 B · 2026-09-18
- Verdict: **SUPERSEDED** — prefix of 0000 (ends at J058, N13 failure closeout).

## 0007_R33_EXECUTION_JOURNAL.md
- Drive: TNN/TNN/Research/R33_N13_CLOSEOUT_SNAPSHOT_V1/Research/R33_EXECUTION_JOURNAL.md · 71,814 B · 2026-09-18
- Verdict: **SUPERSEDED** — prefix of 0000 (ends at J053, N12 postrun closeout).

## 0008_R33_EXECUTION_JOURNAL.md
- Drive: TNN/TNN/Research/R33_N12_CLOSEOUT_SNAPSHOT_V1/Research/R33_EXECUTION_JOURNAL.md · 61,376 B · 2026-09-18
- Verdict: **SUPERSEDED** — prefix of 0000 (ends at J047, N11 closeout; N12 execution entries live only in later files).

## 0009_R33_EXECUTION_JOURNAL.md
- Drive: TNN/TNN/Research/R33_PROGRESS_CLOSEOUT_SNAPSHOT_20260906_V1/Research/R33_EXECUTION_JOURNAL.md · 53,521 B · 2026-09-18
- Verdict: **SUPERSEDED** — prefix of 0000 (ends at J048, Sept 6 completion map; also contains the four-byte parameter-table warning: "N05B observed eight-byte native integer stride. Future parameter/optimizer layout must be measured rather than assumed from wire or logical sizes").

## 0010_R33_EXECUTION_JOURNAL.md
- Drive: TNN/TNN/Research/R33_N11_CLOSEOUT_SNAPSHOT_V1/Research/R33_EXECUTION_JOURNAL.md · 50,813 B · 2026-09-18
- Verdict: **SUPERSEDED** — earliest prefix of 0000 (ends at J047; contains the pre-N12 engineering trajectory).

## 0011_TNN_CAPABILITY_MASTER_PLAN_20260918.md
- Drive: TNN/TNN/Research/TNN_CAPABILITY_MASTER_PLAN_20260918.md · 38,926 B · 2026-09-18
- Verdict: **NEW**
- Findings: design rationale the baseline lacks. Highest research priority stated as a loop: "hypothesis formation → reasoning → experiment → abstraction → invention", with prediction demoted to "one instrument inside this loop", "not the definition of intelligence". Five-variable separation: architecture / training / learning-credit / governance-autonomy / evaluation. Vision/audio target: "Learn useful concepts from raw sensory experience" (senses-adjacent, extends baseline's senses inventory with the intended end state). Also: "Historical R25/R26/R27 continuity remains a required foundation track. It does **not** count as new intelligence merely because old outputs are reproduced."

## 0012_TNN_MEGA_PLAN_WHITE_BOX_DEVELOPMENTAL_ARCHITECTURE.md
- Drive: TNN/TNN/Research/TNN_MEGA_PLAN_WHITE_BOX_DEVELOPMENTAL_ARCHITECTURE.md · 34,372 B · 2026-09-05
- Verdict: **NEW**
- Findings: (a) PAM origins: M2 — "Non-core module/PAM creation in shadow": "create/clone/train/specialize candidate PAMs from generic primitives" — earliest articulation of the PAM Foundry concept; M2 also lists "sparse top-k PAM/expert routing". (b) Master concept: "an automated Master is only an attributed teaching aid" (Trainer = human). (c) Design rules the baseline lacks: "a capability gain does not buy the right to destroy an accepted capability" (prefigures the deliberate-repair law); "Every negative result and failed architecture candidate remains documented to prevent future agents from repeating it blindly." (d) "Active TNN and future Foundry remain graph-free: the broad family-neutral statement below preserves historical comparison context, not authority to reintroduce graph cognition" — graph-free stated as a retained rule.
- Quote: "The trainer does **not** manually choose low-level weights, memory addresses, chunks, PAM wiring, benchmark answers, or hidden-set labels and then count that as learning."

## 0013_R32_E51_EXECUTION_JOURNAL.md
- Drive: TNN/TNN/Research/R32_E51_EXECUTION_JOURNAL.md · 32,896 B · 2026-09-18
- Verdict: **NEW**
- Findings: R32-era retention research journal (Sept 4–5). E51AJ verified three-replica closure: outcome `REPLAY_ORDER_DOSE_DIAGNOSTIC_COMPLETE` with `MIXED_OR_UNREPLICATED_RETENTION_DIRECTION`; final shared-anchor losses sequential/replay: 1/14, 9/11, 17/6 — replicated-retention claim fails; "no favorable checkpoint or pooled reversal is substituted." Independent review identities: `chatgpt-web/pro` reviewer and `chatgpt web E51AJ experimental-design reviewer` (uuid `01a07027-7ea7-7b62-a0d1-b2c8bdcf211e`) — the Noether E51AI reviewer failed with browser concurrency limits. E51AI journal: longitudinal closure, run `33949274757`, 1,091 s native execution.
- People/dates: anchors R32 E51 program to Sept 4–5, 2026 Pacific.

## 0014_INDEPENDENT_FINAL_REVIEW.md
- Drive: TNN/TNN/Research/R33_NATIVE_N13_TORCH_VIEWS/INDEPENDENT_FINAL_REVIEW.md · 32,467 B · 2026-09-18
- Verdict: **CONFIRMS** — N13 review V1 `REQUEST_CHANGES` (R1–R4: dot-key oracle offset, capacity misclassification, fixture-allocation masquerading as negative control, indexed writes before allocation checks); confirms the journal's J055 entry. Engineering review detail, no new test results.

## 0015_README.md
- Drive: TNN/TNN/README.md · 32,361 B · 2026-09-18
- Verdict: **CONFIRMS** — current TNN README. One line: Sept 12 note — native continuing-life workstream's first five-child engineering run passed with fresh-process recovery and measured resource accounting; N13A closed as bounded engineering evidence; "26 recorded diagnostic batches and zero R33 training runs."

## 0016_README.md
- Drive: TNN/TNN/Research/R33_CONTINUING_LIFE_V1/HISTORY_BEFORE/README.md · 31,756 B · 2026-09-18
- Verdict: **SUPERSEDED** — older README snapshot (superseded by 0015).

## 0017_README.md
- Drive: TNN/TNN/Research/R33_N13A_CLOSEOUT_SNAPSHOT_V1/README.md · 31,188 B · 2026-09-18
- Verdict: **SUPERSEDED** — older README snapshot.

## 0018_README.md
- Drive: TNN/TNN/Research/R33_N12_CLOSEOUT_SNAPSHOT_V1/README.md · 31,055 B · 2026-09-18
- Verdict: **SUPERSEDED** — older README snapshot.

## 0019_README.md
- Drive: TNN/TNN/Research/R33_PROGRESS_CLOSEOUT_SNAPSHOT_20260906_V1/README.md · 30,829 B · 2026-09-18
- Verdict: **SUPERSEDED** — older README snapshot (Sept 6 era).

## 0020_INDEPENDENT_FINAL_REVIEW.md
- Drive: TNN/TNN/Research/R33_NATIVE_N13A_FINGERPRINT_SCRATCH/INDEPENDENT_FINAL_REVIEW.md · 29,294 B · 2026-09-18
- Verdict: **CONFIRMS** — N13A review `APPROVE_FOR_PREREGISTRATION` ("N13 remains a consumed failure; neither its primary nor a standalone old replay" is qualified); confirms journal J060.

## 0021_R33_B001_SENSORY_REVIEW.md
- Drive: TNN/TNN/Research/R33_B001_SENSORY_REVIEW.md · 29,067 B · 2026-09-18
- Verdict: **CONFIRMS** — this is the B001 review producing the baseline-known C01-01..C01-11 component bugs. Adds rationale context: the raw-bypass diagnostic "must not inject the evaluator's [coordinate] to the learner"; "a passing same-process round trip [must not] be mistaken for durable storage"; C01 can support only "bounded PCM16LE decode/encode and RGB8 carrier-copy routines behave as specified" — NOT "raw sensory ingress passed S0"; "the earlier byte-originated RawRecord test remains the minimum S0 gate." No results beyond baseline.

## 0022_TNN_MASTER_ARCHITECTURE_PLAN_R27_COMPLETION.md
- Drive: TNN/TNN/Research/TNN_MASTER_ARCHITECTURE_PLAN_R27_COMPLETION.md · 27,954 B · 2026-08-23
- Verdict: **NEW**
- Findings: (a) Test results never seen: the prior integrated run — "93.33% spoken-name resolution and 100% different-entity rejection but 0% same-entity changed-view identity and 0% sibling teaching" — Phase B orders a fairness/sabotage audit of those 0% failures before redesigning. (b) Design rationale: "State Continuity Bridge" — reconcile the developmental R25–R27 lineage with native Zag v2 via one-time migration; "If exact structural migration is impossible, create a deterministic behavioral migration and separately mark which old internal structures could not be represented. Do not silently claim internal identity when only behavioral parity exists." (c) Scientific rules: "Training first, architecture when justified"; "Core PAMs are protected from TNN self-mutation, not sacred"; "Hardcoded Master is permitted as teacher, not learner. Teacher knowledge cannot be counted as TNN competence and must be withdrawn before qualification." (d) "No evaluator leakage" rule enumerating object IDs, category names, transcript labels, score keys as evaluator-only.

## 0023_TNN_NEXT_RUN_PLAN_NO_GRAPH_ASSOCIATIVE_EPISODIC.md
- Drive: TNN/TNN/Research/TNN_NEXT_RUN_PLAN_NO_GRAPH_ASSOCIATIVE_EPISODIC.md · 26,968 B · 2026-08-23
- Verdict: **NEW**
- Findings: the design rationale for abandoning graph as the cognitive substrate — not ideology but an experiment: "The last factorial campaign changed the problem. The strongest finding was not that one graph variant won. It was that the associative-episodic identity family had a massive true-switch advantage while graph/persistence-heavy architectures frequently achieved high aggregate scores by refusing to change identity. That is unacceptable for a system intended to develop open-ended world models." Replacement: Associative Episodic Identity Fabric (AEIF, 9 properties listed). Graph kept "only as frozen falsification controls and optional derived relation indexes" — "The graph hypothesis is not deleted from science." Also introduces "Innate System Fluency" as a protected core skill: "TNN can be born knowing how to invoke its generic machinery—PAM/substrate creation, fibers, memory operations, traces, shadow tests, rollback, reinspection—without knowing which mechanism or answer is correct." Fills baseline gap: WHY graphs died.
- Quote: "Persistent identity is grounded first in episodic evidence, temporal hypotheses, prediction, and active observation—not in an authoritative entity graph."

## 0024_POSTRUN_INDEPENDENT_REVIEW.md
- Drive: TNN/TNN/Research/R33_NATIVE_N13_TORCH_VIEWS/POSTRUN_INDEPENDENT_REVIEW.md · 25,346 B · 2026-09-18
- Verdict: **NEW**
- Findings: terminal disposition `FAIL_CONSUMED — INVENTORY_WRITE_RSS_LIMIT_EXCEEDED` for the N13 sole primary (the independent confirmation of the journal's J057 failure). A bounded-engineering FAIL verdict the baseline's wave results don't enumerate.

## 0025_INDEPENDENT_REVIEW_DRAFT.md
- Drive: TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/INDEPENDENT_REVIEW_DRAFT.md · 24,497 B · 2026-09-18
- Verdict: **CONFIRMS** — N12 initial static review, superseded by the final reviews; engineering detail only.

## 0026_INDEPENDENT_FINAL_REVIEW.md
- Drive: TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/INDEPENDENT_FINAL_REVIEW.md · 23,438 B · 2026-09-18
- Verdict: **CONFIRMS** — N12 review `BLOCKING CHANGES REQUIRED BEFORE PREREGISTRATION` (V1); confirms the journal's review-loop story.

## 0027_R33_PROGRESS_SUMMARY_20260906.md
- Drive: TNN/TNN/Research/R33_PROGRESS_SUMMARY_20260906.md · 23,155 B · 2026-09-18
- Verdict: **CONFIRMS** — Sept 6 program-wide status reconciliation: 28 diagnostic batches, 2 synthetic training-stage invocations, N15 closed negative; "It is not 28 successful scientific experiments, 28 learned capabilities"; "Natural multimodal development: Encoded-file fixtures exist; natural audio/video/action transfer is unqualified." Confirms baseline senses status.

## 0028_INDEPENDENT_FINAL_REVIEW_V2.md
- Drive: TNN/TNN/Research/R33_NATIVE_N13_TORCH_VIEWS/INDEPENDENT_FINAL_REVIEW_V2.md · 22,356 B · 2026-09-18
- Verdict: **CONFIRMS** — N13 V2 review `APPROVE_FOR_PREREGISTRATION`; confirms journal J056.

## 0029_R33_PROGRESS_SUMMARY_20260906.md
- Drive: TNN/TNN/Research/R33_PROGRESS_CLOSEOUT_SNAPSHOT_20260906_V1/Research/R33_PROGRESS_SUMMARY_20260906.md · 22,312 B · 2026-09-18
- Verdict: **SUPERSEDED** — closeout-snapshot copy of 0027.

## 0030_R33_NATIVE_TELEMETRY_DESIGN_V1.md
- Drive: TNN/TNN/Research/R33_NATIVE_TELEMETRY_BUILD_01/R33_NATIVE_TELEMETRY_DESIGN_V1.md · 22,079 B · 2026-09-18
- Verdict: **CONFIRMS** — native competency-telemetry V1 design; status "COMPILED, NOT EXECUTED" (event-sourced accumulator, 16+88×capacity i32 words, capacity 0–128 events, no allocation/syscall in mutation path). Design-only, no results.

## 0031_tnn-current-debug-summary.txt
- Drive: TNN/TNN/Research/tnn-current-debug-summary.txt · 21,499 B · 2026-08-23
- Verdict: **NEW**
- Findings: historical workspace state (Aug 23). Test result: `english_broad_evaluation.json` — `"pass": false, "reason": "No native free-form binary passed strict compilation."` Senses fixtures present: `audio_features.json` (2 B — empty), `video_features.json` (6,758 B), `run_pam_tournament.py`, `pam_stress.zag`, `real_pam_streams.zag`, `adaptive_motif.zag`; results include `pam_tournament.json` (1,474 B) and `adaptive_motif_tournament.json` — a PAM tournament was actually run historically. Extends baseline: first concrete evidence of historical PAM tournament experiments (real_pam_streams).

## 0032_R32_E51_LONGITUDINAL_RESEARCH_PLAN.md
- Drive: TNN/TNN/Research/R32_E51_LONGITUDINAL_RESEARCH_PLAN.md · 19,679 B · 2026-09-18
- Verdict: **NEW**
- Findings: (a) Test result never seen: E51AH — "an integrity-valid development negative: local replay lost 121 of 12,622 union successes while rescuing 159; net +38 did not pass its zero-loss gate. Validation and confirmation remain sealed." (b) Design rationale: diagnostic lane vs qualification lane ("The diagnostic lane cannot retrospectively relax AH gates, unlock AH holdouts, update Baseline V1, or confer promotion"); Family S (same-generator retention) vs Family T (distinct tasks) must not be merged into a generality score; exposure ladder tiers (Acquisition/Short cycle/Repeated cycle/Extended cycle, up to 66,560 new training episodes, 261 checkpoint panels).
- Quote: "Partial recovery, positive net change, or a favorable final checkpoint cannot erase earlier required-gate failures."

## 0033_POSTRUN_INDEPENDENT_REVIEW.md
- Drive: TNN/TNN/Research/R33_N12_CLOSEOUT_SNAPSHOT_V1/Research/R33_NATIVE_N12_NUMERIC_VIEWS/POSTRUN_INDEPENDENT_REVIEW.md · 18,813 B · 2026-09-18
- Verdict: **CONFIRMS** — N12 postrun `CONFIRM_BOUNDED_ENGINEERING_PASS`; confirms journal J053.

## 0034_TERMINAL_REVIEW.txt
- Drive: TNN/TNN/Research/R33_NATIVE_N17_R27_CONTINUITY/RECOVERY_20260915_B_INDEPENDENT/TERMINAL_SUPPLEMENT_20260915/TERMINAL_REVIEW.txt · 18,140 B · 2026-09-18
- Verdict: **NEW**
- Findings: N17 terminal engineering review COMPLETED — receipt `FAIL_CLOSED`; all 26 remaining blockers reviewed (5 R27, 21 R26); 0 full-row acceptance. Senses-relevant NEW: R27-08 `abstraction_s2g` and R27-09 `abstraction_g2s` — "Serialized abstraction model SOCIAL_FAR accuracy >= .95" / "mixed SOCIAL_NEAR/FAR accuracy >= .90": the serialized abstraction-model bytes EXIST but "complete inference semantics and SOCIAL_NEAR/SOCIAL_FAR examples, labels, evaluation and tie rules are not admitted" — stored accuracy is witness data, not recomputed. This gives the baseline's "perceptual origins unrecoverable" claim concrete content: R27's social-abstraction models are the unrecovered perceptual artifact. Also R27-33 r26_verifier `UNRESOLVED_NATIVE_AGGREGATE_DEPENDENCIES`; R27-06 r26_sha missing exact standalone bytes.

## 0035_FINAL_TERMINAL_REVIEW.txt
- Drive: TNN/TNN/Research/R33_NATIVE_N17_R27_CONTINUITY/RECOVERY_20260915_B_INDEPENDENT/TERMINAL_SUPPLEMENT_20260915/COMPATIBILITY_CORRECTION_20260915/FINAL_TERMINAL_REVIEW.txt · 17,658 B · 2026-09-18
- Verdict: **CONFIRMS** — N17 final terminal review, same `FAIL_CLOSED` with the 26 blockers re-verified; adds one CLOSED correction (imported numeric-const initialization for isolated R25 compatibility entrypoint; allocator bounds 1..33554432 validated) and notes "V91 parity working per integrator/user". No new verdict.

## 0036_R32_E45_NEGATIVE_RESULTS_AND_EVALUATOR_REPAIR.md
- Drive: TNN/TNN/Research/R32_E45_NEGATIVE_RESULTS_AND_EVALUATOR_REPAIR.md · 17,394 B · 2026-08-29
- Verdict: **CONFIRMS** — the baseline-known R32 E45/E48 valid negatives with classification detail (`EVALUATOR + REPRESENTATION`, `ONE_PASS_ONLINE_VS_SPECIFIED_BATCH_FIT_INSUFFICIENT_WITH_CURRENT_LINEAR_VALUE_GEOMETRY`). Elaborates but reports nothing the baseline doesn't know.

## 0037_R33_NATIVE_N01_REVIEW.md
- Drive: TNN/TNN/Research/R33_NATIVE_N01_REVIEW.md · 16,707 B · 2026-09-18
- Verdict: **CONFIRMS** — N01 native-supervision-primer independent review (2026-09-05): strongest criticism is the overstated timeout guarantee ("a supervisor that can die while leaving an unbounded child is not yet a complete supervision boundary"); findings N01-R1 (missing native primary admission/create primitive), N01-R2 (write-scope contradiction). Engineering detail; no scientific results.

## 0038_DESIGN.md
- Drive: TNN/TNN/Research/R33_NATIVE_N13_TORCH_VIEWS/DESIGN.md · 16,093 B · 2026-09-18
- Verdict: **CONFIRMS** — N13 torch-views pre-execution design (grammar, 102 matrix / 123 refusal cases, resource/effect limits). Confirms journal content; byte-identical to 0039.

## 0039_INHERITED_N13_DESIGN.md
- Drive: TNN/TNN/Research/R33_NATIVE_N13A_FINGERPRINT_SCRATCH/INHERITED_N13_DESIGN.md · 16,093 B · 2026-09-18
- Verdict: **SUPERSEDED** — byte-identical duplicate of 0038 (md5 `68f9a16f34052e81d4379d7e0a6494ce`).

## 0040_R33_NATIVE_N03_REVIEW.md
- Drive: TNN/TNN/Research/R33_NATIVE_N03_REVIEW.md · 15,959 B · 2026-09-18
- Verdict: **CONFIRMS** — N03 review; verdict conditional on N03-R1/R2 disposition; capacity-envelope mismatch noted. Engineering detail only.

## 0041_TNN_R28_COMPLETION_AND_R29_PLAN.md
- Drive: TNN/TNN/Research/TNN_R28_COMPLETION_AND_R29_PLAN.md · 15,928 B · 2026-08-23
- Verdict: **NEW**
- Findings: binding architecture decisions with rationale the baseline lacks: (a) No graphs in the TNN runtime — "Graph identity, graph relation indexes, graph routing, graph world models, graph PAMs, and graph-backed memory authority are removed from the forward architecture. Historical graph experiments remain archived only as negative/control evidence." (b) Memory default: "privileged heuristic, controlled by TNN" — birth/default representation policy is a privileged generic heuristic TNN can override; "LRU may be used only as a low-level eviction mechanism after TNN has decided representation/value" — prefigures the strength-is-judgment law. (c) CTC acoustic PAM direction: "The current CTC experiment is external Python reference code, not yet a native TNN PAM. Port the CTC-style acoustic sequence learner into native Zag. If the native implementation demonstrates durable connected-speech gains, preserves anonymity/no English hardcoding, survives teacher withdrawal and sealed tests, it becomes the R28/R29 core acoustic PAM." This is an acoustic-PAM origin + stated bar (baseline's "R32 acoustic PAMs DROPPED" covers the GRU machinery, not this CTC plan). (d) Speech target: "near-100% hard connected speech with no supplied VAD/boundaries. Isolated motif success does not count as connected-speech success."

## 0042_TNN_ARCHITECTURE_ROLES_AND_CONNECTIONS.md
- Drive: TNN/TNN/Research/TNN_ARCHITECTURE_ROLES_AND_CONNECTIONS.md · 15,646 B · 2026-09-18
- Verdict: **NEW**
- Findings: (a) Naming anchor: "**TNN means True Neural Network.** 'Grounded, Active, Non-Token Cognition' is a descriptive phrase for the research direction, not the acronym expansion." (b) "Trainer means a human/person/group, never a Master module or automated training program." (c) "Active cognition and future Foundry are graph-free under the retained explicit user correction" — the no-graph rule is recorded as Micah's explicit correction. (d) Historical R18: "Historical R18 material includes a temporal-attention component, but active R33 cognition is not qualified as a transformer or an attention-based LLM. Any attention mechanism must remain subordinate to the grounded evidence, memory, hypothesis, consequence, and action loop." (e) Current-vs-target table: "Small learned value heads, routed local experts/cells" as current; learner-created structures after milestone gates as target.
- Quote: "TNN is a white-box, grounded, active, continual-learning cognitive architecture built around persistent episodic/hypothesis state, learned action value, learner-owned memory/representation, and progressively learner-owned structural plasticity."

## 0043_INDEPENDENT_FINAL_REVIEW_V2.md
- Drive: TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/INDEPENDENT_FINAL_REVIEW_V2.md · 15,410 B · 2026-09-18
- Verdict: **CONFIRMS** — N12 V2 `APPROVE_FOR_PREREGISTRATION` for the exact revised package; confirms journal J049.

## 0044_DESIGN.md
- Drive: TNN/TNN/Research/R33_NATIVE_N12_NUMERIC_VIEWS/DESIGN.md · 14,970 B · 2026-09-18
- Verdict: **CONFIRMS** — N12 strict numeric-view engineering design; confirms journal content.

## 0045_R32_E51AJ_RESULT.md
- Drive: TNN/TNN/Research/R32_E51AJ_RESULT.md · 14,868 B · 2026-09-18
- Verdict: **NEW**
- Findings: completed R32 retention experiment, run completed 2026-09-05 Pacific. Preregistered primary table (final missing shared-anchor successes, sequential vs replay): replica 0: 1/14, replica 1: 9/11, replica 2: 17/6 — retention direction yes only in replica 2; "No replica is discarded or favorable checkpoint selected." The separate aggregate no-final-tradeoff rule fails in EVERY replica; replay-vs-sequential reachability differences −3/−1/−8 known, −5/−1/+8 no-unique. A-only fitting "lost shared-anchor successes in all three replicas, including successes on A itself. Thus losses occur without post-fork alternation among cohorts." 1,101,600 probe-episode rows, 427,680 scheduled primary-fit presentations. New R32-era test results not in baseline.
- Quote: "Lower cumulative disruption and better final recovery are different properties; neither can stand in for the other."

## 0046_TNN_NEXT_RUN_PLAN_ENTITY_FLUENCY_SUBSTRATE_TOURNAMENT.md
- Drive: TNN/TNN/Research/TNN_NEXT_RUN_PLAN_ENTITY_FLUENCY_SUBSTRATE_TOURNAMENT.md · 14,780 B · 2026-08-23
- Verdict: **NEW**
- Findings: design rationale complementing 0023. Four independent axes to isolate: training/curriculum, computational substrate, innate system fluency, memory/search policy. "Training and architecture stay separate variables" — "If a learned mechanism loses to random, the default interpretation is that its learning/credit formulation is bad until deeper learning formulations have been tested." The run is "centered on the unresolved persistent-entity problem because identity continuity is upstream of naming, affordance, sibling teaching, and integrated world understanding" — explains why entity work precedes naming/speech. Phase 0 restores native Zag authority via GitHub Actions checkout of Sylorlabs/zag and its trusted `znc` seed ("Do not substitute a different compiler version merely because it is easier to obtain") — prefigures the Sept compiler work.

## 0047_INDEPENDENT_INITIAL_REVIEW.md
- Drive: TNN/TNN/Research/R33_NATIVE_N13_TORCH_VIEWS/AUTHORING_INITIAL_V1/INDEPENDENT_INITIAL_REVIEW.md · 14,508 B · 2026-09-18
- Verdict: **CONFIRMS** — N13 initial static review ("Euler independently authored the literal oracle table … This was not approval"). Confirms journal J054.

## 0048_DESIGN.md
- Drive: TNN/TNN/Research/R33_NATIVE_N13_TORCH_VIEWS/PREREVIEW_V1/DESIGN.md · 14,455 B · 2026-09-18
- Verdict: **CONFIRMS** — N13 prereview design snapshot; confirms journal content.

## 0049_R33_NATIVE_N03_BUILD02_REVIEW.md
- Drive: TNN/TNN/Research/R33_NATIVE_N03_BUILD02_REVIEW.md · 14,105 B · 2026-09-18
- Verdict: **CONFIRMS** — N03 build02 review with frozen-finding dispositions; engineering detail only.

## 0050_DESIGN.md
- Drive: TNN/TNN/Research/R33_NATIVE_N18_R27_FROZEN_CORE_SIDECAR/DESIGN.md · 14,029 B · 2026-09-18
- Verdict: **NEW**
- Findings: design rationale for rejecting the frozen-core sidecar loophole. "The proposed shortcut—keep the canonical R27 file unchanged and attach the qualified N16 arm19 learner—does not, by itself, establish that the native execution path is canonical R27. Byte custody proves non-mutation, not behavioral continuity." The packet instead proposes (not enacted) a separate `FROZEN_PARENT_NATIVE_SURROGATE_COMPOSITE` methodology class, under which the strongest permitted label is `NATIVE_SURROGATE_COMPOSITE_BEATS_SURROGATE_PARENT`, never "beats canonical R27." Design controls (four fixed conditions, paired fresh namespaces, exact input-custody freeze) without qualification claims. Shows the program's claim-hygiene at work — a rationale the baseline lacks.

## 0051_R32_E51AI_RESULT.md
- Drive: TNN/TNN/Research/R32_E51AI_RESULT.md · 13,375 B · 2026-09-18
- Verdict: **NEW**
- Findings: completed R32 longitudinal diagnostic, run completed 2026-09-04 Pacific. Real one-step history: final reachability 2,085 vs 2,073 (arm 0) and 2,073 (arm 2) — history exceeds both controls in total/known reachability (+12 total, +15/+25 known) but FAILS both the no-unique-preservation condition (452 vs 455/465) and the zero-union-loss condition (38 union successes lost). History+replay (arm 3): 2,084 total, ends missing 5 shared anchors vs 21 without replay — "a bounded retention/preservation tradeoff, not exact rescue, proof that memory is necessary, cross-task continual learning, or promotion authority." 293,760 probe-episode rows. New R32-era test results not in baseline.
- Quote: "Positive net gain does not imply preservation."

---

## Tally
- Read: 52/52
- NEW: 16 (0000, 0011, 0012, 0013, 0022, 0023, 0024, 0031, 0032, 0034, 0041, 0042, 0045, 0046, 0050, 0051)
- CONFIRMS: 21 (0014, 0015, 0020, 0021, 0025, 0026, 0027, 0028, 0030, 0033, 0035, 0036, 0037, 0038, 0040, 0043, 0044, 0047, 0048, 0049)
- SUPERSEDED: 15 (0001–0010 journal snapshots; 0016–0019 README snapshots; 0029 progress-summary snapshot; 0039 byte-duplicate of 0038)
- NOISE: 0
- Contradictions with baseline: none loud. One qualification: J080's Sept 15 recovery of the original R27 release ZIP partially supersedes the "unrecoverable" framing — but only for the R27 release/digest/verifier artifacts; trace-op semantics and perceptual origins (R27-08/09 SOCIAL_NEAR/FAR abstraction models: bytes exist, inference semantics unadmitted) remain unrecovered. The "pre-git session-file hunt is cancelled" note concerns session transcripts, not the release archive — no conflict.
- Lead for other batch readers: ghost/koryphaios mentions exist at 0416_candidates_expanded.txt, 0424_exact_size_hashes.txt, 0436_candidates.txt, 0476_AUTHORS.txt, 0568_archives.txt — outside this batch.
