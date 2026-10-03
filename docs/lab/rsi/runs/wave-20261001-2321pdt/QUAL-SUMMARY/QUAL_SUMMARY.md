# QUAL_SUMMARY: every qualification, supersession, narrowing, and refinement in wave-20261001-2321pdt

Reference for the debate group. Source: docs/lab/rsi/runs/wave-20261001-2321pdt/WAVE_RECORD.md (46 verdict bullets on lines 33-79; the header still says 45 because CONTLEARN-OWNED2 landed later without the header being updated). Each row: verdict | type | one-sentence substance | line reference.

## RED-TEAM QUALIFY

| Verdict | Type | Substance | Line |
|---|---|---|---|
| DEVANG3 | RED-TEAM QUALIFY (RT-SENSE) | K_SEAL (20/20 on fresh Family C) does not discriminate the learner from the trivial fixed-width-3 control C2, which also scores 20/20; the "11/20 to 20/20" framing compares two differently structured families, not a same-set improvement; the wave establishes only the merge-pathology fix on ambiguity probes (K_SEG 12/12 fresh; 12/12 on the 2021pdt regression set where the baseline was 8/12). | L57 |
| H-PI-REV2 | RED-TEAM QUALIFY (RT-HPIREV2, Q1) | Certification defect: 24/25 sealed files match prereg hashes; D2_FW.txt has a 62-char truncated hash line in the prereg (a transcription typo), so the lane's "25/25 verified, all match" sentence is not literally true (defect is certification, not experimental: same file committed, staged, run). | L53 |
| H-PI-REV2 | RED-TEAM QUALIFY (RT-HPIREV2, Q2) | Load-bearing: all five lane worlds accommodate the frozen rank-biased diagnosis by disclosed pre-freeze design, so the narrowed claim as literally stated was never tested against a conflict the rank bias does not select; reviewer recommends restating with a rank-diagnosability qualifier and the bound-trip half with a probe-dependence qualifier; debate must adjudicate BUILD-PASS-with-qualifications vs further narrowing. | L53 |
| H-PI-REV2 | RED-TEAM QUALIFY (RT-HPIREV2, Part 2) | The bound PARTIALLY survives the post-freeze adversarial family: ADV-S1/S2/S3 pass, ADV-S4 BREAK CONFIRMED (true trigger (2,66) the rank bias cannot select: fails_total=1), ADV-M1 SILENT SUCCESS (masked second conflict: fails=0, zero detection), ADV-M2 explicit trip CONFIRMED; the bound-trip signal is PROBE-DEPENDENT (explicit when the uncovered conflict is probed alone, silent when masked). | L53 |
| ARENA5 | RED-TEAM QUALIFY (RT-ARENA5) | All 8 frozen bars hold as frozen and were independently reproduced, but the sealed battery contains exactly 1 bare-prompt test item, so extensionally the default action equals a listnames handler on this battery; generality rests on intension plus reproduced dev probes, not sealed-battery discrimination; a future battery with diverse bare prompts would discriminate extensionally; Amendment 1 seed change is clean; remaining blemishes are verdict-neutral. | L76 |
| TNN3-SUBSTRATE | RED-TEAM QUALIFY (RT-GOV) | HOLDS on all three axes (ONE-SYSTEM RULE, ISA RULING, GOVERNANCE) with one QUALIFY: Amendments 1-2 were applied in place and committed inside the prototype commit, not re-frozen alone (flagged for Micah's amendment-discipline decision). | L45 |
| CONSEQ | RED-TEAM QUALIFY (RT-INT, carried) | The independent-adversary clause was never met (builder-sealed worlds); this wave confirms reproduction fidelity, not adversarial validation. | L44 |
| CONTLEARN | RED-TEAM QUALIFY (RT-INT, carried) | The "LEARNOWN-DEMONSTRATED" label is a hazard; keep the weak/strong distinction attached whenever it is cited. | L44 |
| C174 | RED-TEAM QUALIFY (RT-C174, carried) | Bar (c) proves "reverts to fixed rules" via a shared-code fallback, not independent convergence; bar (d) is properly bounded to K-H3-world migration compat (independently verified against the CONSEQ K-H3 record). | L52 |

## SUPERSESSION

| Verdict | Type | Substance | Line |
|---|---|---|---|
| CONTLEARN | SUPERSESSION (by CONTLEARN-OWNED) | The CONTLEARN "LEARNOWN-DEMONSTRATED" label is refined: integration is MACHINERY-DEPENDENT (0/6 with machinery disabled vs 6/6 control); the demonstrated integration sits on the researcher side of the control-plane line. | L40 |
| CONTLEARN | SUPERSESSION (by CONTLEARN-OWNED2) | Independent replication strengthens the CONTLEARN-OWNED discrimination (6/6 with machinery present, 0/6 absent, standing retrieval intact in both); the red-team QUALIFY stands. | L79 |
| H7R | SUPERSESSION (by H6R BUILD-FAIL) | The worker's "3/3 passing" report claim is superseded: substrate halves are H2R PASS, H7R PASS, H6R FAIL (H6R's B3 kill and B4 SUBSTRATE-INSUFFICIENT gap stand). | L61 |
| ARENA2 | SUPERSESSION (by ARENA4) | ARENA4 refutes ARENA2's C15 rejection reason "ordering-fragile" as factually wrong: the frozen scorer is order-insensitive set F1, not exact match. | L59 |
| PF battery (all construction claims) | SUPERSESSION (by BATTERY-E3) | E3 REFRAMES EVERY PF construction observation as BFS enumeration plus oracle selection, not selective construction; every wave construction claim resting on unmasked QUERY evidence must be re-examined blind. | L65 |
| H2a (strong form) | SUPERSESSION (by BATTERY-E8) | E8 kills H2a's strong form ("content never reaches action selection in any form"); the surviving claim is narrower (see NARROW below). | L75 |
| H1c | SUPERSESSION (by BATTERY-E1) | E1 white-box evidence KILLS H1c as stated ("no standing derived structure exists at all"): licensed derived structures exist (E1-W2 DERIVED=1/BYPASS=1; E1-W4 DERIVED=1/FIRSTCLASS=1). | L62 |
| F1 | SUPERSESSION refused (RT-EXEC) | PARTIAL-narrowed rejected: not a defined verdict in the frozen rules; inventing one post-hoc would be bar-weakening; F1 stays BUILD-FAIL and the windowed trigger proceeds as a NEW candidate (F1-FOLLOWUP). | L35 |

## NARROW

| Verdict | Type | Substance | Line |
|---|---|---|---|
| ARENA5 | NARROW (ARENA-GEN) | DEFRECALL's "generality" is extensionally a bare-prompt handler: it enumerates correctly on listnames/recall/who but also incorrectly on whattime/invent (AG-2 5/7 FAIL); this qualifies but does not refute ARENA5, and ARENA5's dev demonstration was one-sided (only prompts where enumeration is appropriate). | L78 |
| H-PI-REV2 | NARROW (built-in) | The surviving claim is the step-7 single-conflict bound only; step-7 FAIL-with-bounding is untouched, worlds are non-independent by disclosed design, no L3/representational-invention/broad-generality claim, and the candidate is not SURVIVES (transfer/reuse beyond the single probe, second independent red team, governance audit all remain). | L34 |
| TNN-3 H5R2 | NARROW (H5R2-BASELINE) | The claim is bounded: the t2_prov_ok gate beats no-gate and random but REVERT-TO-LATEST matches it on every bar of the four sealed worlds, so its necessity was untestable there; disclosed cost: recency regresses the built-in battery to 45/46 (F2 FAIL) while H5R2 holds 46/46. | L55 |
| TNN-3 H5R2 | NARROW (H5R2-SKEPTIC2) | The gate's necessity is STILL UNPROVEN against the stronger skeptic NEWEST-LIVE-ON-KEY (both 8/8 on chained decoys); it beats recency, no-gate, and chance at every chain level, but not the per-key newest-live heuristic. | L74 |
| H2a | NARROW (BATTERY-E8) | Surviving claim: the subject-identity content of an actionable guide does not differentiate the emitted action (E2's result stands for its instrument); the protocol-reachable CHOICE vocabulary remains {0,30}. | L75 |
| ARENA5 | NARROW (self) | On this battery the default action is extensionally equivalent to a listnames handler (the C15 probe is the only bare prompt); generality rests on intension (flagged for the judge); the battery expresses the goal as a test-turn bare prompt; multi-step tool protocol remains unimplemented. | L70 |

## REFINEMENT

| Verdict | Type | Substance | Line |
|---|---|---|---|
| TNN-3 H5R2 | REFINEMENT (H5R2-DECOY) | BASELINE-MATCHES is RESOLVED, not contradicted: recency explained the four-world battery only because there the newest fact happened to be the live one; on decoy worlds where the newest fact is not live, H5R2 anchors to the live fact 8/8 while REVERT-TO-LATEST anchors to the decoy 8/8. | L63 |
| Cluster 1 shared cause | REFINEMENT (BATTERY-E1) | The shared cause refines from "no derived structures" to "derived structures exist but have no privileged standing in the read path; the flat instance-fact layer is consulted first and wins" (DERIVATION SUBORDINATION vindicated as the deeper cause); H1a wins for W1/W2, W3 supports H1b; the prereg prediction miss (predicted E1-ABSENT) is reported plainly. | L62 |
| H2a | REFINEMENT (BATTERY-E6) | H2a-as-literally-stated is refined, not just confirmed: the distinguishing uncertainty content has no read path into ACT; the only content reaching ACT is the subject tag (recency gate) plus a construction-constant action value (30); this redirects Cluster 2 toward H2d; H2c-STICKY confirmed as decided evidence (guides are never retired, updated, unlinked, aged, or evicted on resolution). | L67 |
| F1 line | REFINEMENT (F1-BUFFER) | The F1-FOLLOWUP hypothesis is refined, not confirmed: trigger-time buffer mass predicts the greedy second step (verified: 5100-series seeds 6 and 18 share the exact first-trigger buffer multiset and take identical first two constructs), not the final overfit, which is decided by later-trigger repair dynamics. | L58 |
| F1 line | REFINEMENT (F1-REPAIR) | GREEDY-CONFIRMED per the frozen rule with a trace-verified nuance: the counterexamples refute the frozen signature's buf=8 clause, NOT the repair story (seed 10's partial-buffer burst runs to zero and repairs the degenerate doubling); relaxed signature S-prime holds 20/20 degenerate-path seeds; H-GREEDY's gloss ("repair is epiphenomenal") is UNSUPPORTED. | L64 |
| F1 line | REFINEMENT (F1-REPAIR2) | S-prime confirmed on fresh 7300-series worlds (27/27 degenerate-path seeds across three series); POLICY-R characterizes typical degenerate-path repair dynamics within its stated boundary (mispredicts 2/32 non-degenerate seeds); it is a mechanism characterization, not a repair patch; no fix proposed for the F1 line. | L71 |
| TNN3-SUBSTRATE | REFINEMENT (RT-GOV) | Doc fix requested: "904 ticket nodes" should read "type-904 ticket nodes"; two disclosed residuals: (a) ls_bump +1/-1 polarities are researcher constants, (b) lbid's record-wins-else-bid default may need H6R override. | L45 |
| CONSEQ | REFINEMENT (scope) | Scope honestly held: validates the consequence re-entry template, not the shared tag-61 substrate itself (C174 remains EMERGES, exploratory). | L39 |
| C174 | REFINEMENT (scope) | Honest scope: dev-harness validation of the store as infrastructure, not TNN-2/TNN-3 integration; thresholds/weights are researcher scaffolding; migration boundary documented (per-value counters and shift register coincide only on non-interleaved worlds); no L3/FW1-FW9/generality claims; broader worlds untested. | L49 |
| C9BAT | REFINEMENT (scope) | Scope honesty: C9GEN is a CANDIDATE instrument for a future wave's governance decision, not a replacement; the 24/24 is evidence about the instrument (admits a genuine experiment-driven solution), not evidence any learner is causal in general; no L3/substrate/score claims. | L56 |
| ARENA inquiry (C8) | REFINEMENT (caveats) | The "15 capabilities" count does not reproduce from sealed records (16 capabilities, 68 items; flagged, not asserted); canonical 0.573 unmoved; L3 explicitly disclaimed (L1/L2 infrastructure); disclosure: the worker incidentally saw observe_result values during protocol verification, never used (zero-hit grep audit). | L42 |
| ARENA4 | REFINEMENT (flags) | 0.947 is the honest experience-based ceiling (Segunu never observed in exposure); the implemented C15 is a single probe while the prereg spec described autonomous goal completion with tools (future battery work). | L59 |
| BATTERY Part 2 | REFINEMENT (PF-A2 caveat) | PF-A2 world weakly discriminates (2/2 via BFS+oracle traversal, not selective abstraction); recorded as a methods note with no verdict weight. | L50 |
| BATTERY Part 2 | REFINEMENT (PF-C1 caveat) | PF-C1 PASS was via direct-fact shadowing, not graph revision; recorded. | L50 |
| BATTERY-E4 | REFINEMENT (design honesty) | The behavioral SUPPRESSION signature is unobservable because the frozen contradiction protocol supersedes rather than deletes; the honest discriminator is the white-box DERIVED leg. | L69 |
| DEVANG3 | REFINEMENT (caveat) | Single worker, no independent adversary (mitigations: fresh vocab/episodes, blind generation, hashes pre-run, no inspection between); residual attestation-based risk disclosed. | L51 |
| TNN-3 H5R2 | REFINEMENT (seal note) | Single worker as coordinator/builder/evaluator; mitigations (seeds, ranges, patterns, driver template hash f2d60568) frozen pre-implementation; one procedural blemish (DRIVER_TMPL.zag committed with the implementation commit, content binding holds via the prereg hash). | L41, L35 |
| ARENA2 / ARENA3 | REFINEMENT (sibling collision) | Two independent C12 candidates (ARENA2 REMAP on v6 base, ARENA3 TRX on INQ base); per the frozen collision clause these are independent competing runs, not duplication; the debate must compare/reconcile the two mechanisms. | L47 |
| F1 | REFINEMENT (bar correction) | The worker owns a bar-calibration mistake: K-C0C-REG used an unvalidated fresh seed, conflating trigger regression with constructor seed-robustness; BUILD-FAIL vs PARTIAL-narrowed goes to the debate. | L43 |
| ARENA4 / ARENA5 | REFINEMENT (ARENA-BLIND) | The E3 re-examination mandate is satisfied for ROSTER by audit: ORACLE-FREE (test turns carry only turn/kind/item/cap/q; ROSTER generates exactly one candidate), so the masked re-test branch is not triggered and ARENA4 BUILD-PASS stands. | L73 |
| F1-FOLLOWUP | REFINEMENT (verdict scope) | Part 1 BUILD-PASS is a NEW candidate with corrected bars, not a verdict change to the F1 BUILD-FAIL; Part 2 NOT-FOUND (no pre-registered whole-fixture property separates overfit from correct within the frozen <=2 misclassification bar). | L48 |
| TNN3-SUBSTRATE | REFINEMENT (governance scope) | RECOMMENDS but does not adopt: adoption into the TNN-2 cognition layer, and any protected-core change (none requested), are Micah's governance decisions; five verbatim-ready decisions recorded as escalation items. | L36 |
| H5R2-BASELINE | REFINEMENT (process) | Git-race disclosure: fc2f910e5 swept in six F1-BUFFER files staged by a concurrent worker (safely committed; attribution blurred, no data lost). | L55 |

## PREREG / RECORD CORRECTIONS

| Verdict | Type | Substance | Line |
|---|---|---|---|
| BATTERY-E4 | PREREG CORRECTION | The original record line cited b63f80289 as E4's prereg; b63f80289 is ARENA5's commit (its message says "ARENA5: freeze DEFRECALL prereg") which swept E4's staged prereg files in a staging race; E4's prereg content was restored byte-identical at 5a2c7c91c before any E4 implementation commit, and the correct attributed chain is 5a2c7c91c -> f26ddb294 -> 67680ebb1 -> 61df738fe. | L69 |
| C174 | RECORD CORRECTION | Post-seal disclosed fix (not a bar move): the C174_EVAL arm= metadata line was removed from eval stdout because it made bar (c)'s whole-output SHA comparison vacuous; no prereg/world/logic changes; documented in EVAL_RESULTS.md. | L49 |
| BATTERY-E4 | RECORD CORRECTION | Incident: H5R2-SKEPTIC2 worker commit f461e812d accidentally deleted BATTERY-E4/PREREG_E4.md and NAMECHECK.md (411 deletions); both restored byte-identical before any implementation commit; E4-K1 holds. | L69 |

## PROCESS QUALIFICATIONS (record-keeping)

| Verdict | Type | Substance | Line |
|---|---|---|---|
| Wave skeleton | RECORD-KEEPING | Staging race: skeleton commit c5ea959d4 swept in composition_compare/ files another worker had staged; the files are genuine loop work but attribution is wrong; history left as-is (no rewrite). | L12-L13 |
| Repair branches | RECORD-KEEPING | No repair branch exists in the working copy for the three boundary-overreach repair threads paused 2026-10-01 19:14 UTC; the threads left no recoverable state in the repo; recorded as an escalation item for Micah (corrections still pending, scope to be re-established). | L12 |
| F2V3 / SENSORY | RECORD-KEEPING | SENSORY lane still running at RT-SENSE time; it needs red-team coverage when it lands. | L57 |

## SUMMARY COUNTS

- RED-TEAM QUALIFY: 9 (RT-SENSE 1, RT-HPIREV2 3, RT-ARENA5 1, RT-GOV 1, RT-INT carried 2, RT-C174 carried 2)
- SUPERSESSION: 8 (CONTLEARN by CONTLEARN-OWNED, CONTLEARN-OWNED2 replication, H7R "3/3" by H6R FAIL, ARENA2 C15-reason by ARENA4, E3 reframe of all PF construction claims, H2a strong form by E8, H1c by E1, PARTIAL-narrowed rejection by RT-EXEC)
- NARROW: 6 (ARENA-GEN on ARENA5, H-PI-REV2 built-in, H5R2-BASELINE, H5R2-SKEPTIC2, H2a surviving claim, ARENA5 self-caveat)
- REFINEMENT: 23
- PREREG / RECORD CORRECTIONS: 3
- PROCESS QUALIFICATIONS: 3
- TOTAL: 52 qualifications and corrections catalogued
