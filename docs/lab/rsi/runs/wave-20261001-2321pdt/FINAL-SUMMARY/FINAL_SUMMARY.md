# Final summary: wave-20261001-2321pdt

Date: 2026-10-02. Lane: FINAL-SUMMARY (replacement worker). Branch: tnn-native-lab, working copy ~/workspace/tnn-rsi. All commits local only, never pushed.
Sources (read only): VERDICT-LIST/VERDICT_LIST.md, ACHIEVEMENTS/ACHIEVEMENTS.md, DEBATE.md, WAVE-SUMMARY/WAVE_SUMMARY.md, WAVE-ARCHIVE/WAVE_ARCHIVE_MANIFEST.md, URGENT-FLAG/URGENT_FLAG.md.

This is the last lane summary before the parent's final report.

## Urgent: Decisions 4A/4B must reach Micah before the wave closes

The wave's 47 verdicts rest on frozen bytes that are NOT in HEAD: tnn2.zag (SHA-256 a29972ca8183b2857c0c7b262d004fce6e4547c02a971a7aef035b44aa76a8bd), freeze_shim2_bin (SHA-256 9217054c5af6dec057c4530c4de3ba246f521acc6df741d1989a4504acc72954), and the pinned znc linux x86_64 binary (SHA-256 498abcb5ab346f8cb246222a1ca63699d035a4277dedfba4782e1373137e58ef). They exist only as untracked files on this disk; a `git clean -fdx`, a VM replacement, or a fresh checkout destroys them, and with them the reproducibility of every frozen-battery verdict. Decision 4A: approve committing the minimal pinned set (about 30 files, about 30 MB) into HEAD. Decision 4B: approve a protective tar snapshot of the full untracked set with a SHA-256 manifest alongside the bundle backups. Both require Micah's approval; nothing has been done yet, and `git clean -fdx` is forbidden in this working copy until 4A and 4B are complete. Present this at the top of the final report, not in an appendix.

## The 47 verdicts (all [NEW])

1. [NEW] Fork battery: FRESH PASS / RE-CERT PASS: 59 refs frozen-fork battery with 0 FAIL (2 fresh PASS, 55 re-cert PASS, 2 re-cert UNTESTABLE on standing cause) and 48/48 archive immutability.
2. [NEW] H-PI-REV2: BUILD-PASS: narrowed single-conflict claim passes all frozen kill bars on 5 fresh sealed worlds, with revision counts matching pre-freeze mechanical predictions exactly.
3. [NEW] RT-EXEC: EVIDENCE-HOLDS: independent red team verifies F1 and TNN3H5R evidence, recommending UPHOLD of the F1 BUILD-FAIL and standing of H5R2 ADVANCES.
4. [NEW] TNN3-SUBSTRATE: DESIGN-COMPLETE: 197-line zero-new-opcode substrate addition package (learner construction service, contradiction trigger, learner-writable standing) verifies on the dev prototype with zero architecture growth; adoption is Micah's governance decision.
5. [NEW] H5R2-REPRO: REPRO-PASS: independent re-execution from committed source reproduces every sealed H5R2 number exactly, with 3x byte-identical rebuild matching the frozen binary.
6. [NEW] CONSEQ: VALIDATION-PASS: frozen Node2-v2 K-H3 prereg independently re-executed passes 5/5 kill bars, with both causal ablations confirming necessity of the consequence record and the production read.
7. [NEW] CONTLEARN: BUILD-PASS (LEARNOWN-DEMONSTRATED): all K0-K6 pass including unsupervised store 13/13 and reuse 20/20, though the integration was later shown machinery-dependent.
8. [NEW] TNN-3 H5R2: BUILD-PASS (H5R2 ADVANCES): trial-loop stale-provenance fix passes all kill bars including KB-W2R 12/12 (previously the 8/12 kill), with net -4 cognition lines vs the TNN-2 base.
9. [NEW] ARENA (C8 inquiry): BUILD-PASS: generic ask-observe-answer loop takes C8 0.000 to 1.000 and arena total to 0.853 with zero regressions on the other capabilities.
10. [NEW] F1 (interleaved-error trigger): BUILD-FAIL: the generic windowed trigger fires correctly on all interleaved patterns but trips K-C0C-REG 0/30 on R-W2, a pre-existing constructor limitation reproduced byte-identically on the prior wave's frozen binary.
11. [NEW] RT-INT: EVIDENCE-HOLDS: independent red team verifies CONSEQ and CONTLEARN with all attacks held, carrying qualifications on CONSEQ's non-adversarial sealing and CONTLEARN's label hazard.
12. [NEW] RT-GOV: HOLDS with one QUALIFY: TNN3-SUBSTRATE passes the ONE-SYSTEM rule, ISA freeze, and governance axes, with a qualify on Amendments 1-2 committed inside the prototype commit rather than re-frozen alone.
13. [NEW] ARENA2 (C12 REMAP): BUILD-PASS: transfer-by-recoding takes C12 0.000 to 1.000 and arena total to 0.882 with zero regressions and both ablation halves causal.
14. [NEW] ARENA3 (C12 TRX on INQ base): BUILD-PASS: transfer-by-relabeling takes C12 to 1.000 and total to 0.941, a sibling collision with ARENA2 to be reconciled in debate.
15. [NEW] F1-FOLLOWUP: Part 1 BUILD-PASS, Part 2 NOT-FOUND: trigger re-test passes all corrected bars on validated fixtures with zero regression, but no frozen whole-fixture property separates the 25 percent overfit seeds from correct ones.
16. [NEW] C174: VALIDATION-PASS: the shared tag-61 consequence store graduates from EMERGES to validated infrastructure, passing all 5 kill bars including store-serves-two, behavior-change, and ablation causality.
17. [NEW] BATTERY: Part 1 VALIDATED, Part 2 1/6 PASS: Battery v3 validates clean on frozen TNN-2, but the post-freeze sealed adversarial battery on the three new mechanisms passes only 1/6, failing construction, uncertainty-guidance, and revision.
18. [NEW] DEVANG3: BUILD-PASS: the segmenter fix (one cognition line, length bonus to linear penalty) clears both killing bars at 12/12 and 20/20 with no regression on the 2021pdt worlds.
19. [NEW] RT-C174: EVIDENCE-HOLDS: all 7 red-team attacks on the C174 validation failed, with qualifications that bar (c) proves reversion to shared-code fallback and bar (d) is bounded to K-H3 migration compat.
20. [NEW] RT-HPIREV2: Part 1 QUALIFY, Part 2 bound PARTIALLY survives: BUILD-PASS stands on the five tested worlds but with a certification defect and load-bearing rank-biased world design; the post-freeze adversarial family confirms a probe-dependent BREAK on masked second conflicts.
21. [NEW] BATTERY-CLUSTER: COMPLETE: the post-freeze 1/6 failures cluster into two shared causes (derivation subordination; guide content decoupling) with 8 hypotheses and a ranked discriminating-experiment program, no patches proposed.
22. [NEW] H5R2-BASELINE: BASELINE-MATCHES via (a) REVERT-TO-LATEST: the t2_prov_ok gate is not shown necessary on four sealed worlds because a recency heuristic matches it on every bar, though H5R2 alone holds 46/46 on the built-in battery.
23. [NEW] C9BAT: GEN-PASS: the corrected causal battery generator passes all 8 bars, defeating the old positional gaming exploit and admitting a genuine two-stage interventional solution.
24. [NEW] RT-SENSE: QUALIFY: DEVANG3 BUILD-PASS stands on the frozen bars, but the K_SEAL leg does not discriminate the learner from the trivial fixed-width-3 control, both scoring 20/20 on the fresh Family C.
25. [NEW] F1-BUFFER: BUFFER-NOT-PREDICTIVE: the trigger-time-buffer overfit rule misclassifies 7/24 fresh seeds against the frozen at-most-2 bar, though the buffer fully determines the greedy burst's second construct.
26. [NEW] ARENA4 (C15 ROSTER): BUILD-PASS: a persistent experience-built entity roster takes C15 0.000 to 0.947 with zero regressions, showing C15 is achievable by a general mechanism, unlike C9.
27. [NEW] BATTERY-E2: E2-CONTENT-BLIND: two materially different single guides produce byte-identical CHOICE 30 actions, confirming H2a (absent content channel at the guide-to-ACT interface) and killing H2b concurrency collapse.
28. [NEW] H7R: BUILD-PASS: the substrate trigger plus construction service suffices for genuine contradiction-driven re-derivation, with zero new semantic cases and learner-authored REDERIVE tickets.
29. [NEW] BATTERY-E1: E1-FIRSTCLASS: the licensed-structure inspector finds licensed derived structures in frozen TNN-2 white-box state, killing H1c and refining the cluster cause to read-path subordination.
30. [NEW] H5R2-DECOY: DECOY-DISCRIMINATES: on decoy probes where the newest fact is not the live one, the t2_prov_ok gate anchors correctly 8/8 while recency anchors to the decoy 8/8, resolving BASELINE-MATCHES in the gate's favor.
31. [NEW] F1-REPAIR: GREEDY-CONFIRMED with trace-verified nuance: the frozen signature forces GREEDY-CONFIRMED, but the trace shows a later partial-buffer repair burst to zero explains the CORRECT counterexample, refining the story to the relaxed S-prime signature.
32. [NEW] BATTERY-E3: E3-ORACLE-DEPENDENT: blind composition emits spurious composites 0/2 while oracle-present scores 2/2, reframing construction observations as BFS enumeration plus oracle selection and mandating blind re-examination of all wave construction claims.
33. [NEW] F2V3 (depth-9): BUILD-PASS: raising the DPDS discrimination bound from 8 to 9 passes all eight kill bars on both fresh sealed worlds with no regressions.
34. [NEW] BATTERY-E6: E6-CONTENT-READ with H2C-STICKY: the guide-store inspector shows guides are never retired (sticky) and only the subject tag plus a constant action value reach ACT, redirecting Cluster 2 toward H2d output bandwidth.
35. [NEW] H6R: BUILD-FAIL: standing values live on unpinned kind-904 record nodes invisible to the lbid selector, so eviction always destroys standing first, tripping B3 at exactly the predicted 50/80 margin of zero.
36. [NEW] BATTERY-E4: E4-PRECEDENCE: the precedence-reversal world confirms subordination as pure read-path precedence, with the licensed derived structure persisting intact through flat-fact teaching and contradiction.
37. [NEW] ARENA5 (DEFRECALL): BUILD-PASS: a generic default action for bare prompts replaces the dedicated listnames handler, holding C15 at 0.947 with zero goal-string references and causal ablation on both halves.
38. [NEW] F1-REPAIR2: REPAIR2-CONFIRMED: the relaxed S-prime repair signature holds on 27/27 degenerate-path seeds across three series, and the POLICY-R repair-time policy passes within its stated boundary.
39. [NEW] BATTERY-E5: E5-INSTANCE-ONLY: contradicting two instances of a two-hop law leaves the unseen third instance and the analogous relation unrevised, confirming H1b instance-only write path at behavioral and state levels.
40. [NEW] ARENA-BLIND: ORACLE-FREE: the mandated E3-style audit shows the ROSTER mechanism never sees oracle or expected fields and generates exactly one candidate, so ARENA4's BUILD-PASS stands without a masked re-test.
41. [NEW] H5R2-SKEPTIC2: SKEPTIC-SURVIVES: the stronger NEWEST-LIVE-ON-KEY skeptic survives the chained decoy family 8/8, leaving the t2_prov_ok gate's necessity still unproven against it.
42. [NEW] BATTERY-E8: E8-BANDWIDTH: varying a live guide's contextual actionability with presence held constant yields different actions (30 vs 0), confirming H2d output bandwidth as a contributing cause and narrowing H2a's strong form.
43. [NEW] RT-ARENA5: QUALIFY: all 8 ARENA5 bars independently reproduced with zero goal handlers holding, qualified by the fact that the sealed battery contains only one bare-prompt test item, so generality rests on intension plus dev probes.
44. [NEW] CONTLEARN-OWNED: MACHINERY-DEPENDENT: with researcher machinery absent from the query path, the continuing learner integrates 0/6 fresh 2-hop chains vs 6/6 with machinery present, placing the integration on the researcher side of the control-plane line.
45. [NEW] ARENA-GEN: NARROW: DEFRECALL enumerates correctly on listnames/recall/who but blindly enumerates on whattime/invent, so its generality is extensionally a bare-prompt handler and the mechanism qualifies without being refuted.
46. [NEW] CONTLEARN-OWNED2: MACHINERY-DEPENDENT: independent replication confirms 0/6 integration without machinery vs 6/6 with, strengthening the finding that the frozen core has no learner-invoked path from miss to structure construction.
47. [NEW] H5R2-SKEPTIC3: SEPARATED: two live facts on one key without supersession finally discriminate the gate from NEWEST-LIVE-ON-KEY with the exact pre-registered divergence signature, favoring newest-live as the better tie-breaker.

## Debate: 8 rulings (6 UPHOLD, 2 OVERTURN)

Advocate argued all 8 verdicts should stand; skeptic argued for overturn or further narrowing on all 8, opening with the verbatim provenance probe ("What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"). Judge ruled with cited evidence. Full briefs and ruling committed in DEBATE/.

- Q1 F1 BUILD-FAIL vs PARTIAL-narrowed: UPHOLD. PARTIAL is not a defined verdict; inventing it post-hoc would be bar-weakening.
- Q2 H-PI-REV2 qualifications vs further narrowing: OVERTURN (further narrowing). The bound holds only on rank-diagnosable single conflicts with probe-dependent trip; ADV-S4 falsified the unqualified statement. Citation must carry both qualifiers.
- Q3 ARENA2 REMAP vs ARENA3 TRX sibling collision: UPHOLD independent standing, no subsumption. Frozen collision clause satisfied; composition is a later experiment.
- Q4 BATTERY-E3 blind re-examination mandate scope: OVERTURN (narrow mandate). Blind re-test required for selection-step claims; single-candidate mechanisms cleared via the A1-A6 audit.
- Q5 H5R2: does SEPARATED undermine BUILD-PASS: UPHOLD (scope-standing) with mandatory scope boundary. BUILD-PASS stands on the frozen battery (KB-W2R 12/12, KB-W3 8/8); the re-teach separator family is named as an explicit open gap, not a retroactive bar move.
- Q6 ARENA5: does NARROW undermine BUILD-PASS: UPHOLD (bounded scope). All frozen bars met; discriminating generality was never a frozen bar. The "general default action" claim is untenable without the discrimination result and must not be cited.
- Q7 CONTLEARN: does MACHINERY-DEPENDENT overturn BUILD-PASS: UPHOLD (bounded) with binding citation form "LEARNOWN-DEMONSTRATED (machinery-enabled scope; strong sense measured absent, CONTLEARN-OWNED/OWNED2)".
- Q8 CONSEQ/CONTLEARN: qualified citation vs stripped claims: UPHOLD qualified citation with binding forms. CONSEQ cites reproduction-fidelity plus causal ablations with the adversary clause open; CONTLEARN per Q7.

The 5 RT-GOV governance decisions were excluded from debate; they are Micah's alone.

## 94 lanes inventoried

The WAVE-ARCHIVE lane inventoried all 94 lane directories under docs/lab/rsi/runs/wave-20261001-2321pdt/ (see WAVE-ARCHIVE/WAVE_ARCHIVE_MANIFEST.md for the full manifest with per-lane verdicts, key commits, and JUDGE_BRIEF.md coverage). Of these: 45 experimental lanes with verdicts in WAVE_RECORD.md, 6 verification/synthesis lanes (ARENA-GEN-VERIFY, MECH-VERIFY, LEARNER-MECH, ARENA-SYNTH, CLUSTER-SYNTHESIS, CLUSTER-FINAL, H5R2-SYNTH, OWNED-SYNTH), 4 in-progress lanes (SENSORY, RT-F2V3, RT-F2V3-CHECK, SENSORY-CHECK), and the remainder governance, records, and infrastructure lanes. Known process incidents recorded: staging races (H5R2-SKEPTIC2 f461e812d deletions restored byte-identical; BATTERY-E4 prereg attribution corrected), the three boundary-overreach repair threads paused 2026-10-01 19:14 UTC leaving no recoverable repo state (escalated), and a SENSORY near-miss python3 invocation that failed to resolve (nothing executed).

## Key achievements (from ACHIEVEMENTS/ACHIEVEMENTS.md)

1. E3 reframed construction claims: assembly is real, selection is oracle-dependent. The blind trial assembles executable 4-op ISA graphs at runtime and executes them to correct answers with no oracle access; what fails blind is SELECTION (BFS-first emission with two chains available).
2. MACHINERY-DEPENDENT confirmed twice: two independent lanes showed 6/6 integration with machinery present and 0/6 absent; the frozen core provides no learner-invoked path from a miss to structure construction.
3. H5R2 SEPARATED: across BASELINE, DECOY, SKEPTIC2, SKEPTIC3, the provenance gate proved a stale-provenance filter whose oldest-first tie-breaking comes from forward node-id enumeration order; any next gate must combine the filter with newest-live tie-breaking.
4. Both cluster discrimination programs complete: Cluster 1 (H1a pure read-path precedence, H1b instance-only write path, H1c killed, H1d refined) and Cluster 2 closed with E8; concrete architectural implications, no patches proposed.
5. F1 BUILD-FAIL upheld: the frozen bar was not weakened to force a pass; the trigger mechanism itself passed every trigger-specific bar, and F1-REPAIR found the repair hypothesis alive in relaxed S-prime form.
6. H6R BUILD-FAIL: the sealed run named the exact substrate gap (learner-writable standing) blocking the H2/H4/H6/H7 re-attempts, a gap the TNN3-SUBSTRATE package was designed to close.
7. ARENA5 NARROW: the goal was completed by a generic default action, not a handler; but the pass is narrow (extensionally a bare-prompt handler) and the spec's multi-step tool-use autonomy was not demonstrated.
8. E8-BANDWIDTH: output bandwidth is in the causal chain of whether guide content differences manifest behaviorally, killing the strong form of H2a.
9. TNN3-SUBSTRATE DESIGN-COMPLETE: a 197-line cognition-layer package (zero new semantic cases, zero modes, zero bridges, zero protected-core ops) closing the three frozen-substrate gaps, prototype-verified; adoption reserved as Micah's governance decision.
10. Fork battery: 59 refs, 0 FAIL, 48/48 archive immutability; the whole ref set is hygiene-certified for the wave.

## Outstanding

- SENSORY: still running. H2v1 prereg committed; base1/base2 rendering done; h2v1a done; h2v1b rendering; verdict after the verifier runs. It needs red-team coverage when it lands (RT-SENSE QUALIFY attaches to DEVANG3; the SENSORY lane itself is outstanding).
- RT-F2V3: still running. Red-team review of the F2 v4 BUILD-PASS verdict in progress (deep read of prereg/implementation/sealed eval/judge brief); verdict pending.
- Syntheses in progress: OWNED-SYNTH, H5R2-SYNTH; queued-next work continues per the standing execution rule.

## For the parent's final report

- The 47 verdicts are all [NEW], all landed under frozen preregistered kill bars, all 7 red-team reviews complete with qualifications on record, and the debate group ruled 6 UPHOLD / 2 OVERTURN with no verdict changed without cited evidence.
- The single most important items to put before Micah: (1) Decisions 4A/4B on the frozen artifacts, before the wave closes; (2) the E3 blind re-examination mandate and its narrowed scope; (3) the MACHINERY-DEPENDENT finding (twice replicated); (4) TNN3-SUBSTRATE adoption as a governance decision; (5) the H5R2 newest-live separator design.
- Nothing here requires Micah's ruling except Decisions 4A/4B and the TNN3-SUBSTRATE adoption (RT-GOV recorded adoption as Micah's governance decision). Everything else is reported evidence.
