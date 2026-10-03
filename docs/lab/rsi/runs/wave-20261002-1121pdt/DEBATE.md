# DEBATE.md: wave-20261002-1121pdt mandatory debate

Format: inline three-voice debate convened by the wave coordinator (advocate FOR each adoption, skeptic AGAINST, judge ruling with numbers cited). Inline rather than spawned subagents because the runtime killed two lane workers in the last hour (restart-drain exec rejections); spawning debate agents against a hostile runtime risks losing the transcript. The skeptic's mandatory provenance probe appears verbatim below; a transcript lacking it is void.

Wave verdict slate under judgment (from LANE_RESULTS.md, 16 of 17 original lanes closed: 15 verdicts, 1 PROCESS-FAIL, 1 PARTIAL; sensory H5 NO VERDICT after two runtime kills; recovery evidence preserved and rolled).

## The provenance probe (mandatory, asked of every motion)

SKEPTIC: "What is the provenance of the artifacts under judgment, and what exactly is new versus inherited?"

## Motion 1: ADOPT composition_l2 EXTEND/TRUNCATE/SPECIALIZE as L2 adaptive-reuse evidence (l2adapt Candidate A)

ADVOCATE: 12/12 frozen kill bars PASS on an independent clean safebin reproduction, 3/3 byte-identical runs per binary, output digests matching the prior report byte-for-byte (l2_bin 529e0e7d.., l2_na_bin aabe551d..). Prereg c521249ba intact (zero diff since freeze) and strictly preceding implementation (16:17:22 UTC vs 17:09:32 UTC). The one-line adapt_on toggle is a clean causal control: operators fire on learner-state preconditions only. This is the top-priority queue item (Micah's L2 adaptive reuse directive) finally getting its clean run.

SKEPTIC: Provenance first. The implementation source is inherited from the prior wave (8974bbac4/053a08c5e); what is new this wave is the independent rebuild and rerun (commit ed0fe46b7), not new mechanism. The committed binaries differ in sha256 from clean rebuilds (same source, same pinned compiler, same sizes): the prior binaries came from a different environment, so the provenance chain has a hygiene gap. The operators are researcher-authored: a menu-selection attack kills any L3 claim, correctly narrowing this to L2, and the prereg claims L2 only, so no overclaim, but let us be clear this is evidence of adaptive reuse of researcher-supplied operators, not invention. SPECIALIZE's locality prior keys on node-ID proximity, a representation artifact that can misfire under adversarial IDs. The battery has only 3 treat arms; generality is untested.

JUDGE: ADOPT as L2 adaptive-reuse evidence (NOT L3), with bounds recorded. The numbers are clean: 12/12 on frozen bars, commit order clean, prereg intact, causal control clean. The skeptic's points become conditions, not kills: (1) the binary sha mismatch is a provenance hygiene flag: future waves rebuild from source, never trust committed binaries; the kill bars constrain outputs, and outputs match byte-for-byte, so the verdict stands. (2) The L3 ceiling is conceded by the prereg itself; no L3 claim is made or adopted. (3) SPECIALIZE ID-scheme sensitivity and the 3-arm battery are recorded limitations. Motion 1 CARRIES.

## Motion 2: ADOPT H5R3 as ADVANCES (hpi)

ADVOCATE: H5R2 provenance gate sustains the DEP revision chain through full revert cycles. KB-S1 PASS (byte-identical rebuilds), KB-W0 32/32, KB-CY 6/6, KB-RR 2/2, KB-BCY 18/18, KB-BRR 6/6, KB-G3/KB-P3, KB-D3 3/3 byte-identical. Post-freeze adversarial 3/3 SURVIVE. Prereg order clean (bfb01b47e/b675b1d5a precede implementation 5d7e6691d/1dac7588a).

SKEPTIC: Provenance: the mechanism under test is the H5R2 gate, inherited; what is new is the H5R3 implementation targeting the revision-chain-through-revert gap. A prereg transcription defect was found (operative gate intact, defect recorded). No L3 claimed, but the adversary was single-worker: post-freeze adversarial 3/3 is thin. The re-teach separator family is queued, meaning the claim's generality is still open.

JUDGE: ADOPT as ADVANCES with caveats recorded. The numbers are strong across the KB battery (32/32, 18/18, 6/6) and the transcription defect did not touch the operative gate. Single-worker adversary and the queued re-teach are bounds, not kills. Motion 2 CARRIES.

## Motion 3: ADOPT the CAUSAL-DAG mechanism for DAG-structured worlds (trades)

ADVOCATE: 10/10 on non-chain sealed worlds (forks, colliders, diamonds), every win a unique-survivor verdict (final Hn=1, survivor index = true DAG, zero chain indices in any survivor list, no tie-break involved). All 11 frozen kill bars pass; 60 sealed runs byte-identical in pure Zag. Red team: chain-only ablation 0/10 on non-chain worlds and 2/2 on chain controls, proving DAG hypotheses are load-bearing, not decorative. The one miss (world 2012) is a proven observational equivalence under the frozen forward-model semantics, disclosed and bounded.

SKEPTIC: Provenance: the mechanism is the causal-intervention machinery built this wave under frozen prereg 3415c217f (commit-order PASS); the worlds are fresh sealed (seeds 2001..2012). What is new: the DAG-space expansion beyond chains. What is inherited: the intervention semantics, the scorer (byte-exact streq). The 12/36 hypothesis spaces are researcher-enumerated, so this is L2 structural use, correctly not claimed as L3. The 2012 miss shows the expanded space can lose chain points it previously held: 11/12 overall vs a chain-only baseline that would take the chains. The cost ratio WIDE/SINGLE = 9.78 sits inside the [8,12] bound but near the top.

JUDGE: ADOPT for DAG-structured worlds, no L3. The numbers carry it: 10/10 unique-survivor wins, all 11 bars, ablation proves the DAG machinery does the work. The 2012 tie is honestly disclosed as proven observational equivalence, and the follow-up (per-variable-noise forward model) is queued. Motion 3 CARRIES.

## Motion 4: ADOPT the t2_revise_graph index hook C1 (index)

ADVOCATE: Closes the 0521pdt red-team gap. Control R3 reproduces the hole (idx_validate 1 to 0, cause 3 plen mismatch); candidate holds idx/fidx/deep=1 across R1/R2/R3, 3/3 byte-identical per binary. Answers untouched everywhere. Noop check: 6/6 runs byte-identical, all hashing to the 0521pdt sealed canonical 54df6230..: the hook is output-silent on the healthy eviction path. 1 hook line + 2 refile lines in base, 0 new modes/bridges/handlers/semantic cases. Commit-order PASS with one transparent pre-implementation amendment.

SKEPTIC: Provenance: the hook is new this wave (commits 6667a9c4d prereg, b2dd706e2 implementation); the base it patches is the sealed 0521pdt base. What is inherited: everything else. The adoption comes with admitted bounds: revert-path collateral coverage loss, N-way sharing orphans. And the same lane's EVICT SOAK killed a sealed base eviction hook (idx_chain_hits hard-codes strict 102/101 chain alternation; walker false-negatives on non-alternating shapes). Adopting a revise hook while the base eviction hook is known-broken: are we certifying a subsystem with a known hole?

JUDGE: ADOPT C1 with the admitted bounds. The skeptic's worry is answered by separation: C1 is the revise-path hook; the killed hook is the base eviction walker, a different component, and the lane's pure-Zag deep validator (itself validated by catching the bug) is the instrument that found it. The base-hook fix is queued as a new prereg'd candidate next wave, not smuggled into this adoption. The noop check (sealed canonical hash preserved) is the strongest evidence the hook does no harm. Motion 4 CARRIES.

## Motion 5: ADOPT contestant_int.zag as the continuing contestant binary (arena)

ADVOCATE: 67/68 = 0.985 on fixrun2, 3/3 runs, per-capability 1.000 except C15 0/1 (expected). Baselines on the same world: v6 54/68 = 0.794, parts 57 to 60/68. All frozen kill bars pass: I1 (per-cap >= max of individuals), I2, I3 (3/3 byte-identical streams 0699f524..), I4 (pure Zag, double build byte-identical f1eb7313..), I5 (additive only). Verbatim lineage-block assembly, no new modes/bridges/handlers. Adversarial families: ADV-A kills C8 (0/4 as predicted, mechanistically confirmed), ADV-D kills C12 (0/6 as predicted), both surgical with controls intact. Multi-seed C9: 3/3 every run on 5 admissible seeds, zero variance; 3 inadmissible seeds honestly reported, not replaced.

SKEPTIC: Provenance: the contestant is an assembly of inherited parts (v6 + INQ + REMAP + CAUSAL), verbatim; what is new is the integration and its sealed measurement. Now the governance problem. The worker reports a single unexplained `1` from a `python3 -c` probe inside a compound command, then claims repeated re-verification shows python3 does not resolve under safebin PATH, and judges this "not a PROCESS-FAIL". This report is internally inconsistent: if python3 printed `1`, it resolved in that compound command's PATH. The guard is automatic on invocation: hpirev2 took PROCESS-FAIL this very wave for a deliberate `python3 -c`. Why should arena's `python3 -c` be treated differently? If the guard means anything, an admitted `python3 -c` invocation is PROCESS-FAIL, the 27 runs are quarantined, and this motion is void.

ADVOCATE (rebuttal): The distinction is deliberate use versus an uncorroborated anomaly. hpirev2's worker deliberately invoked python3 to produce prereg content: the artifact under judgment was tainted. Here the worker cannot establish that python3 ran at all: a single unreproducible character, contradicted by immediate repeated re-verification under the safebin PATH, with no Python output entering any research artifact. All 27 runs are pure-Zag sealed batteries; the binary double-builds byte-identical. The guard's automatic trigger requires an established invocation; an uncorroborated anomaly is not an establishment.

JUDGE: This is the hardest ruling of the wave. The skeptic is right that the report is inconsistent and that the guard must stay a bright line. The advocate is right that deliberate use (hpirev2) and an uncorroborated anomaly differ in what they taint. Ruling: the evidence does NOT establish a forbidden-interpreter invocation (single unreproducible `1`, no corroboration, contradicted by repeated re-verification; the worker cannot show python3 resolved). The guard's automatic PROCESS-FAIL requires an established invocation, which this is not. Motion 5 CARRIES: contestant_int.zag ADOPTED as the continuing contestant. BUT: the lane's toolchain-guard record carries a permanent IMPAIRED-CLARITY flag, the anomaly is recorded verbatim in LANE_RESULTS.md, and the next wave must re-verify the arena toolchain guard before any arena work. If Micah overrules this distinction, the adoption is void and the lane re-freezes clean. The ruling and the hpirev2 precedent are both on the record; the difference (deliberate use producing tainted artifacts vs uncorroborated anomaly with no artifact contact) is the cited basis.

## Motion 6: ADOPT the contlearn keeps (ledger-as-control gating, state-driven scheduler, cross-kind content reuse + t2_sig)

ADVOCATE: Three bounded/scoped passes, 0 kill bars fired, 30 frozen runs byte-identical 3x. (a) Refusal-branch: identical probes refused 6/6 under contradicted history and engaged 6/6 under confirmed history; hard control refuses under both (state-invariant costume). (b) Scheduler fires at evidx 5 vs evidx 83 across schedules, killing fixed-position hypotheses; negation probe correctly no-fire. (c) COUNT content rebound as CHAIN-kind on the unmodified frozen core after 63 interference events, 6/6 retention. 16 red-team attacks; only scope limitations sustained.

SKEPTIC: Provenance: all three instruments are new this wave under five pre-implementation preregs (K0 self-checks pass); the frozen core is inherited and unmodified. Caveat 3 binds all three: the gating/scheduling policy is researcher-authored, so this is bounded L2 evidence of state-caused behavior, not learner-authored policy. And (c) was scoped DOWN by its own red team: attack 1 proved the rebound is fact-level content reuse, not MAP-transformation; the stronger claim does not hold and is honestly not claimed. So what is adopted is narrower than the queue item asked for.

JUDGE: ADOPT the keeps with the bounds as stated. The skeptic's narrowing is exactly what the lane reported: (c) is content reuse, MAP-transformation rebind is queued; caveat 3 still binds. The crux experiments (A-R2, B-S1, C-R2) are clean state-causation demonstrations with honest controls. The lane's honesty about (c) is a point in favor, not against. Motion 6 CARRIES.

## Motion 7: RECORD the F1 finding's promotion step 10 as COMPLETE (f1rt)

ADVOCATE: Independent red team SURVIVES. Independent reproduction byte-identical (all 40 seeds x 3, all 240 determinism hashes match; R=13, T=2, D_ops=9, Cmax_ops=15 confirmed from scratch). All alternative explanations killed: not a harness artifact (constructor takes no seed arg), not the data (train data identifies the law; greedy search trapped), not tie-breaking (strict argmin), ablation robust to trigger timing (FMIN 2 to 4: R 13 to 8, identical compounding signature persists). Commit order clean.

SKEPTIC: Provenance: the finding is inherited (655c8d7d6, lane-f1-20261002-0821pdt); what is new is the independent attack, which failed to kill it. Two framing qualifications weaken the description: "overfit" is a misnomer (these are greedy traps that underfit train at 3 to 8/24), and T=2 is not causal. So the surviving claim is narrower than its label.

JUDGE: Step 10 recorded COMPLETE. The qualifications are adopted as corrections: R is relabeled a greedy-trap rate in future citations, and T=2 is not cited as causal. The numbers survive; the label is fixed. Motion 7 CARRIES.

## Motion 8: RECORD comp SURVIVES-ADV-A (no adoption)

ADVOCATE: Frozen satisfy bytes; trial-path-free battery 3/3, supervised breakers 6/6, post-freeze diamond-DAG PASS, 17/17 predictions including honest failures (B3U greedy commit). Bounds recorded, not kills.

SKEPTIC: No new artifact is under judgment; the motion is only to record survival. KB6 PARTIAL trial-path confound stands from 0521pdt. No L3 claimed.

JUDGE: Recorded as SURVIVES-ADV-A. No adoption motion needed or made. The bounds (greedy unsupervised, no intrinsic tie-break, partial composites promoted) stand as the honest description. Motion 8 CARRIES as a recording.

## Motion 9: ADOPT the records typo correction (records)

ADVOCATE: One genuine typo fixed (JUDGE_BRIEF.md line 82 now carries the verified true TNN-2 core SHA-256, confirmed via git show f4de7ff46:tnn2_build/tnn2.zag | sha256sum). Two other occurrences intentionally left as evidence quotations. Full sweep of seven 2321pdt dirs: no other malformed SHA-256 claims.

SKEPTIC: Provenance: the fix replaces a corrupted string with a hash verified from the git object store; the evidence quotations are left to avoid falsifying the record. Trivial but correct.

JUDGE: ADOPTED. Committed b6c99561c. Motion 9 CARRIES.

## Items not under adoption (recorded for the slate)

- battery: T-K5/T-K9/T-K11 all FAIL as standing failures, verbatim match to frozen 0521pdt verdicts; NO REGRESSION at tip. Nothing to adopt.
- ddes: step-10 independent red team SURVIVES; adversary OOD 8/8 PASS; governance audit 10 of 11 (step 9 transfer/reuse is the sole promotion blocker). Bounded L2, no SURVIVES. Not adopted.
- tnn3: trial-reclamation integration DESIGN only (commit 673f5e9d9, zero code). Frozen T-RECLAIM-1 proposal with K1 to K10 ready for a future implementing wave. Not adopted (design).
- devang: DEVANG6 BUILD-FAIL on K_SEAL (9/20 < 12/20), mechanism result, bar stands. FINREG/POSSEG DISCARDED as sealed-generalization solution. Recalibrated K_ABL VALIDATED (gap 7 >= 4). Not adopted.
- f2: PARTIAL (K6-R1/R2/R3 PASS; K6-R4/R5 UNMEASURED, compute-time artifact; K6-R7 UNMET; K6-R8 inherited PASS). Matches and strengthens 0521pdt PARTIAL. Not adopted.
- sensory SA1b: BUILD-FAIL (terminal; integer-period quantization washout, knowledge result). Sensory H5: NO VERDICT (battery never ran; two runtime kills; rolled to next wave).
- hpirev2: PROCESS-FAIL (python3 invocation, self-disclosed). Quarantined materials committed as reference for clean re-freeze. Not adopted.
- fork: FORK-BATTERY-COMPLETE, hygiene certification only. Zero FAIL across 93 refs / 44 fresh-tested SHAs.
- l2adapt B (SUBSTITUTE) and C (SUBSEQ): implemented, batteries blocked (training >4-link MAPs fails); NO VERDICT; battery-design negative, not operator negative. Rolled.
- Fourth znc miscompile (negated conjunction in while condition): documented in ~/AGENTS.md line 20 with mandatory workaround. GOVERNANCE FLAG: four independent znc miscompile patterns now documented; toolchain fitness for sealed evaluation deserves Micah's review.
- index EVICT SOAK kill of the sealed base eviction hook: queued as a new prereg'd candidate next wave. Distinct from the operand-encoding defect Micah ruled on 2026-10-02.

## Judge's final slate

ADOPTED: l2adapt-A (L2 evidence, not L3), hpi H5R3 (ADVANCES), trades CAUSAL-DAG (DAG worlds), index C1 (bounded), arena contestant_int.zag (continuing contestant; guard record flagged IMPAIRED-CLARITY, arena guard re-verification required next wave), contlearn keeps (bounded/scoped), f1rt step-10 complete (with greedy-trap relabel), comp SURVIVES-ADV-A (recorded), records typo fix.
NOT ADOPTED: battery (no regression, nothing to adopt), ddes (bounded L2), tnn3 (design), devang (BUILD-FAIL), f2 (PARTIAL), sensory SA1b (BUILD-FAIL terminal), sensory H5 (NO VERDICT, rolled), hpirev2 (PROCESS-FAIL, quarantined), fork (hygiene), l2adapt B/C (NO VERDICT, rolled).
No coordinator verdict was overturned; the debate's one hard ruling (Motion 5) is flagged for Micah's awareness and possible overrule.
