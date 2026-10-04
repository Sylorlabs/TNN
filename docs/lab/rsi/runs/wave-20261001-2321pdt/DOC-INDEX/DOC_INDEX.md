# Documentation index: wave-20261001-2321pdt

Wave: wave-20261001-2321pdt (Thu 2026-10-01, 23:21 PDT), branch tnn-native-lab.
47 verdicts recorded. Lane worker: DOC-INDEX (replacement), pure shell, no Python, no experiments.

## Parent report section key

- (a) Verdicts: VERDICT-LIST/VERDICT_LIST.md, backed by WAVE_RECORD.md verdicts and the verdict lane documents below.
- (b) Debate outcomes: DEBATE-SLATE/DEBATE_SLATE.md and DEBATE/JUDGE_RULING.md, backed by the six syntheses.
- (c) Per-fork results: FORK/FORK_BATTERY.md.
- (d) Queued next: QUEUED-CHECK/QUEUED_CHECK.md and the "Queued next" section of WAVE_RECORD.md.
- (e) LOOP_STATE text: LOOPSTATE-DRAFT/LOOPSTATE_DRAFT.md (draft exists); LOOPSTATE-FINAL/ is EMPTY as of 2026-10-02 ~00:47 PDT (lane not yet complete).
- (f) Escalation items: ESCALATION-LIST/ESCALATION_LIST.md.

All paths are relative to docs/lab/rsi/runs/wave-20261001-2321pdt/.

## Core wave documents

- WAVE_RECORD.md: The wave record. Lane list, standing rules, repair-branch check, staging-race note, the 47 verdict bullets with evidence and commit chains, queued next. Feeds every parent report section.
- VERDICT-LIST/VERDICT_LIST.md: The 47 verdicts numbered with labels and one-sentence substance. Section (a).
- WAVE-SUMMARY/WAVE_SUMMARY.md: Parent-facing executive summary. Verdict breakdown by label, most important findings, most important qualifications. Feeds all sections.
- PARENT-PREP/PARENT_REPORT_SECTIONS.md: Assembles parent report sections (a), (d), (f) from VERDICT_LIST.md, WAVE_SUMMARY.md, WAVE_RECORD.md; marks (b), (c), (e) pending where data was not yet in.
- WAVE-STATUS/WAVE_STATUS.md: Snapshot as of 2026-10-02 ~00:45 PDT: 47 verdicts all [NEW] and coherent; lane status for the coordinator.
- FINAL-CONFIRM/FINAL_CONFIRM.md: Final confirmation lane verdict that the parent report is ready.

## The six debate syntheses (section b)

1. DEBATE-PREP/DEBATE_BRIEF.md: Original 40-verdict brief compiled from WAVE_RECORD.md alone; the debate minimum document.
2. ARENA-SYNTH/ARENA_SYNTHESIS.md: ARENA5 trio synthesis. Exactly what each verdict established, how they relate, and the precise bounded claim that remains.
3. OWNED-SYNTH/OWNED_SYNTHESIS.md: Learner-owned quintet. Five verdicts on learner-owned integration synthesized for the debate group and TNN-3 governance.
4. H5R2-SYNTH/H5R2_SYNTHESIS.md: H5R2 quartet. The four gate verdicts (BASELINE-MATCHES, DECOY-DISCRIMINATES, SKEPTIC-SURVIVES, SEPARATED) in one table for the debate.
5. QUAL-SUMMARY/QUAL_SUMMARY.md: Every qualification, supersession, narrowing, and refinement in the wave, cross-referenced to WAVE_RECORD.md lines. Reference for the debate group.
6. CLUSTER-FINAL/CLUSTER_FINAL.md: Final synthesis of the Cluster 1 + Cluster 2 discrimination program on frozen TNN-2.

Related, not one of the six: CLUSTER-SYNTHESIS/CLUSTER_SYNTHESIS.md: decided evidence from the post-freeze battery cluster discriminators (intermediate synthesis feeding CLUSTER-FINAL).

## Debate group documents (section b)

- DEBATE-SLATE/DEBATE_SLATE.md: Final debate slate. Eight questions stated with verdicts involved, key evidence, and what uphold vs overturn means. Governance escalation items are out of scope and not listed.
- DEBATE/JUDGE_RULING.md: Adjudication of the eight debate questions by the debate judge.
- DEBATE/ADVOCATE_BRIEF.md and DEBATE/SKEPTIC_BRIEF.md: Advocate and skeptic briefs for the mandatory debate group.
- DEBATE-PREP2/DEBATE_MATERIALS.md: Materials package for the debate group (replacement worker completion).
- DEBATE-READY/DEBATE_READINESS.md: Readiness check: debate minimum (DEBATE_BRIEF + CLUSTER_FINAL + ARENA_SYNTHESIS) present in HEAD; verdict READY TO PROCEED.
- FINAL-REVIEW/FINAL_REVIEW.md: Review-lane readiness check of WAVE_RECORD.md verdict count and coherence for the debate.

## Governance and escalation (section f)

- ESCALATION-LIST/ESCALATION_LIST.md: Items requiring Micah's governance decision or awareness: TNN3-SUBSTRATE adoption (5 verbatim decisions), EXECUTE placement ruling (pending since 2026-09-30), three paused boundary-overreach repair threads, ~142k files deleted in HEAD, H6R B4 standing/retention gap, learner-authority-over-integration gap, LLM baseline pending (no credential), plus three info items.
- ESCALATION-UPDATE/ESCALATION_UPDATE.md: Addendum on frozen files not in HEAD (addendum to escalation item 4).
- ESCALATION-VERIFY/ESCALATION_VERIFY.md: Verifies ESCALATION_LIST.md is present in HEAD at commit c3b62ab4d1b9b844bf9a405ffe2a9391b55d7e69.
- URGENT-FLAG/URGENT_FLAG.md: Urgent flag for the parent report: Decisions 4A/4B (frozen files not in HEAD).
- REPO-SCOPE/REPO_SCOPE_ASSESSMENT.md: Repo scope assessment backing the ~142k-file finding.
- LANE-AUDIT/LANE_AUDIT_REPORT.md: Git hygiene incident audit: commit f461e812d deleted 147,296 files repo-wide, 4,833 under the wave dir.

## Verification and audit meta-documents

- FINAL-COUNT/FINAL_COUNT_REPORT.md: WAVE_RECORD.md coherence and verdict count check.
- RECORD-CHECK/RECORD_CHECK_REPORT.md: Record consistency check (44 at its check time; header count drift noted).
- EVIDENCE-CHECK/EVIDENCE_CHECK.md: Verdict evidence completeness: each of the 47 verdicts has a lane dir with a JUDGE_BRIEF.md or verdict file.
- DRAFT-CHECK/DRAFT_CHECK_REPORT.md: Draft vs wave record cross-check (read only).
- REPORT-CHECK/REPORT_CHECK.md: Report check lane document.
- MECH-VERIFY/MECH_VERIFY_REPORT.md: Independent verification of the LEARNER-MECH root-cause analysis against frozen TNN-2 sources.
- LEARNER-MECH/LEARNER_MECH_ANALYSIS.md: Root-cause analysis of why the continuing learner cannot own integration (analysis only, no patch).
- GAP-DOC/GAP_DOCUMENTATION.md: Verified mechanism gap: learner cannot initiate structure construction in frozen TNN-2.
- HEALTH-CHECK/HEALTH_CHECK.md: Health check as of 2026-10-02 00:46 PDT (toolchain guard PASS).
- SWARM-HEALTH/SWARM_HEALTH_REPORT.md: Swarm health report checked 2026-10-02 00:30 to 00:35 PDT.
- SENSORY-CHECK/SENSORY_STATUS.md, SENSORY-PREP/SENSORY_PREP.md, SENSORY-WATCH/: Sensory lane status, prep, and watch documents.

## Verdict lane documents (section a evidence)

Each lane dir holds PREREG_*.md (frozen prereg), SEALED_EVAL*.md (sealed evaluation), JUDGE_BRIEF.md (provenance header + verdict evidence), and EVAL/IMPLEMENTATION records. Verdict labels are copied from VERDICT_LIST.md.

Build and experiment lanes:

- HPIREV2/: BUILD-PASS. Step-7 single-conflict bound as narrowed claim; passes all frozen kill bars on 5 fresh sealed worlds; revision counts match pre-freeze mechanical predictions exactly.
- TNN3-SUBSTRATE/: DESIGN-COMPLETE. 197-line zero-new-opcode substrate addition package (learner construction service, contradiction trigger, learner-writable standing); ADOPTION_RECOMMENDATION.md records the governance decision for Micah.
- TNN3H5R/: BUILD-PASS (H5R2 ADVANCES). Trial-loop stale-provenance fix; all kill bars including KB-W2R 12/12 (previously the 8/12 kill); net -4 cognition lines vs TNN-2.
- DEVANG3/: BUILD-PASS. Segmenter fix (one cognition line, linear length penalty); clears both killing bars at 12/12 and 20/20; no regression on the wave's worlds.
- F1/: BUILD-FAIL. Generic windowed interleaved-error trigger fires correctly but trips K-C0C-REG 0/30 on R-W2, a pre-existing constructor limitation reproduced byte-identically on the prior wave's frozen binary.
- F1-FOLLOWUP/: Part 1 BUILD-PASS, Part 2 NOT-FOUND. Trigger re-test passes corrected bars on validated fixtures; no frozen whole-fixture property separates the 25 percent overfit seeds.
- F1-REPAIR/: GREEDY-CONFIRMED with trace-verified nuance. Frozen signature forces GREEDY-CONFIRMED; later partial-buffer repair burst refines the story to the relaxed S-prime signature.
- F1-REPAIR2/: REPAIR2-CONFIRMED. Relaxed S-prime repair signature holds on 27/27 degenerate-path seeds; POLICY-R repair-time policy passes within its stated boundary.
- F1-BUFFER/: BUFFER-NOT-PREDICTIVE. Trigger-time-buffer overfit rule misclassifies 7/24 fresh seeds against the frozen at-most-2 bar; buffer fully determines the greedy burst's second construct.
- F2V3/: BUILD-PASS. Raising the DPDS discrimination bound from 8 to 9 passes all eight kill bars on both fresh sealed worlds.
- H2R/: PASS surviving half (EVAL_RESULTS.md, SEED_RECORD.md).
- H6R/: BUILD-FAIL. Standing values live on unpinned kind-904 record nodes invisible to the lbid selector; eviction always destroys standing first; B3 trips at the predicted margin of zero.
- H7R/: BUILD-PASS. Substrate trigger plus construction service suffices for genuine contradiction-driven re-derivation; zero new semantic cases; learner-authored REDERIVE tickets.
- H5R2-BASELINE/: BASELINE-MATCHES via (a) REVERT-TO-LATEST. t2_prov_ok gate not shown necessary on four sealed worlds; recency heuristic matches it on every bar.
- H5R2-DECOY/: DECOY-DISCRIMINATES. On decoy probes the t2_prov_ok gate anchors correctly 8/8 while recency anchors to the decoy 8/8; resolves BASELINE-MATCHES in the gate's favor.
- H5R2-REPRO/: REPRO-PASS. Independent re-execution from committed source reproduces every sealed H5R2 number exactly; 3x byte-identical rebuild matches the frozen binary.
- H5R2-SKEPTIC2/: SKEPTIC-SURVIVES. Stronger NEWEST-LIVE-ON-KEY skeptic survives the chained decoy family 8/8; gate necessity still unproven against it.
- H5R2-SKEPTIC3/: SEPARATED. Two live facts on one key without supersession finally discriminates the gate from NEWEST-LIVE-ON-KEY with the exact pre-registered divergence signature, favoring newest-live as the better tie-breaker.
- CONSEQ/: VALIDATION-PASS. Frozen Node2-v2 K-H3 prereg independently re-executed passes 5/5 kill bars; both causal ablations confirm necessity of the consequence record and the production read.
- CONTLEARN/: BUILD-PASS (LEARNOWN-DEMONSTRATED). All K0-K6 pass including unsupervised store 13/13 and reuse 20/20; integration later shown machinery-dependent.
- CONTLEARN-OWNED/: MACHINERY-DEPENDENT. With machinery absent from the query path the continuing learner integrates 0/6 fresh 2-hop chains vs 6/6 with machinery present; integration sits on the researcher side of the control-plane line.
- CONTLEARN-OWNED2/: MACHINERY-DEPENDENT. Independent replication confirms 0/6 vs 6/6; the frozen core has no learner-invoked path from miss to structure construction.
- C174/: VALIDATION-PASS. Shared tag-61 consequence store graduates from EMERGES to validated infrastructure; passes all 5 kill bars including store-serves-two, behavior-change, and ablation causality.
- C9BAT/: GEN-PASS. Corrected causal battery generator passes all 8 bars; defeats the old positional gaming exploit; admits a genuine two-stage interventional solution.

Arena family (capability battery):

- ARENA/: BUILD-PASS. C8 inquiry: generic ask-observe-answer loop takes C8 0.000 to 1.000 and arena total to 0.853 with zero regressions.
- ARENA2/: BUILD-PASS. C12 transfer-by-recoding takes C12 0.000 to 1.000 and arena total to 0.882; sibling collision with ARENA3 to be reconciled in debate.
- ARENA3/: BUILD-PASS. C12 transfer-by-relabeling on the INQ base takes C12 to 1.000 and total to 0.941.
- ARENA4/: BUILD-PASS. C15 roster: persistent experience-built entity roster takes C15 0.000 to 0.947 with zero regressions; K6 ablation causal; 164 lines added, zero new modes/bridges/routers/gates/semantic cases.
- ARENA5/: BUILD-PASS. DEFRECALL: generic default action for bare prompts replaces the dedicated listnames handler; holds C15 at 0.947 with zero goal-string references.
- ARENA-BLIND/: ORACLE-FREE. Mandated E3-style audit: the ROSTER mechanism never sees oracle or expected fields and generates exactly one candidate; ARENA4's BUILD-PASS stands without a masked re-test.
- ARENA-GEN/: NARROW. DEFRECALL enumerates correctly on listnames/recall/who but blindly enumerates on whattime/invent; extensionally a bare-prompt handler; qualified, not refuted.
- ARENA-GEN-VERIFY/VERIFY_REPORT.md: Verification report for the ARENA-GEN generality claim.

Battery family (post-freeze adversarial battery on the three new mechanisms; Part 1 VALIDATED, Part 2 1/6 PASS):

- BATTERY/: Battery v3 design per the 6 queued triviality-review corrections; POSTFREEZE_RUN.md and VALIDATION_RUN_V3.md for the two parts.
- BATTERY-CLUSTER/CLUSTER_ANALYSIS.md: The post-freeze 1/6 failures cluster into two shared causes (derivation subordination; guide content decoupling) with 8 hypotheses and a ranked discriminating-experiment program; no patches proposed.
- BATTERY-E1/: E1-FIRSTCLASS. Licensed-structure inspector finds licensed derived structures in frozen TNN-2 white-box state; kills H1c; refines the cluster cause to read-path subordination.
- BATTERY-E2/: E2-CONTENT-BLIND. Two materially different single guides produce byte-identical CHOICE 30 actions; confirms H2a (absent content channel at the guide-to-ACT interface); kills H2b concurrency collapse.
- BATTERY-E3/: E3-ORACLE-DEPENDENT. Blind composition emits spurious composites 0/2 while oracle-present scores 2/2; reframes construction observations as BFS enumeration plus oracle selection; mandates blind re-examination of all wave construction claims.
- BATTERY-E4/: E4-PRECEDENCE. Precedence-reversal world confirms subordination as pure read-path precedence; licensed derived structure persists intact through flat-fact teaching and contradiction.
- BATTERY-E5/: E5-INSTANCE-ONLY. Contradicting two instances of a two-hop law leaves the unseen third instance and the analogous relation unrevised; confirms H1b instance-only write path.
- BATTERY-E6/: E6-CONTENT-READ with H2C-STICKY. Guide-store inspector shows guides are never retired (sticky); only the subject tag plus a constant action value reach ACT; redirects Cluster 2 toward H2d output bandwidth.
- BATTERY-E8/: E8-BANDWIDTH. Varying a live guide's contextual actionability with presence held constant yields different actions (30 vs 0); confirms H2d output bandwidth as a contributing cause; narrows H2a's strong form.
- SENSORY/: Sensory realism lane (PREREG_SENSORY_H2V1.md, h2v1/IMPLEMENTATION.md); new bigger-lever realism candidate after H1v2 BUILD-FAIL; blind A/B pair for Micah if READY.

Red-team reviews (independent red team of the builder evidence):

- RT-EXEC/RT-EXEC_REVIEW.md: EVIDENCE-HOLDS. Verifies F1 and TNN3H5R evidence; recommends UPHOLD of the F1 BUILD-FAIL and standing of H5R2 ADVANCES.
- RT-INT/RT-INT_REVIEW.md: EVIDENCE-HOLDS. Verifies CONSEQ and CONTLEARN with all attacks held; qualifications on CONSEQ's non-adversarial sealing and CONTLEARN's label hazard.
- RT-GOV/RT-GOV_REVIEW.md: HOLDS with one QUALIFY. TNN3-SUBSTRATE passes the ONE-SYSTEM rule, ISA freeze, and governance axes; qualifies Amendments 1-2 committed inside the prototype commit rather than re-frozen alone.
- RT-C174/RT-C174_REVIEW.md: EVIDENCE-HOLDS. All 7 attacks on the C174 validation failed; qualifies bar (c) as reversion to shared-code fallback and bar (d) as bounded to K-H3 migration compat.
- RT-SENSE/RT-SENSE_REVIEW.md: QUALIFY. DEVANG3 BUILD-PASS stands on the frozen bars, but the K_SEAL leg does not discriminate the learner from the trivial fixed-width-3 control (both 20/20 on fresh Family C).
- RT-ARENA4/RT-ARENA4_REVIEW.md: Red-team review of the ARENA4 C15 roster claim.
- RT-ARENA5/RT-ARENA5_REVIEW.md: QUALIFY. All 8 ARENA5 bars independently reproduced with zero goal handlers holding; qualified because the sealed battery contains only one bare-prompt test item.
- RT-HPIREV2/RT-HPIREV2_REVIEW.md: Part 1 QUALIFY, Part 2 bound PARTIALLY survives. BUILD-PASS stands on the five tested worlds with a certification defect and load-bearing rank-biased world design; the post-freeze adversarial family confirms a probe-dependent BREAK on masked second conflicts.
- RT-F2V3/, RT-F2V3-CHECK/RT_F2V3_STATUS.md: Red-team and status documents for the F2V3 claim.

Notes and caveats for the parent:

- Each lane dir also carries NAMECHECK.md with the safebin Step 0 record; those are governance bookkeeping, not content documents.
- Raw experiment artifacts (transcripts, stderr logs, .zag sources, compiled binaries, sealed world files, .zag-cache) are omitted from this index; the canonical per-lane evidence is PREREG_*.md, SEALED_EVAL*.md, JUDGE_BRIEF.md, and EVAL/IMPLEMENTATION records.
- LOOPSTATE-FINAL/ is empty as of 2026-10-02 ~00:47 PDT; the section (e) LOOP_STATE text is not yet finalized. The draft is at LOOPSTATE-DRAFT/LOOPSTATE_DRAFT.md.
- Verdict count drift: WAVE_SUMMARY.md reports 47 [NEW] verdicts; older meta-docs (FINAL-COUNT, RECORD-CHECK, QUAL-SUMMARY) reference 44 to 46 because lanes landed after those checks ran. The 47 count is the current canonical figure.
