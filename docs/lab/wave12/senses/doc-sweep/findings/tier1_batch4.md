# Tier-1 batch 4 findings — 52 files read, all against BASELINE.md

Local files were `docs_local/0208–0259` (manifest indexes 0000–0051 map 1:1 in order).
All Drive files modified 2026-09-18T22:21Z. No koryphaios/ghost mentions in this batch.

## NEW findings (24)

### 0000 — TNN/TNN/Research/R48_INTEGRATED_CAPABILITY_PACKET_20260918/R48_RESULT.md (3,783 B)
**NEW.** First integrated research-platform packet closeout, never seen. Test results: multi-hypothesis symbolic reasoning 20/20; causal experiment selection 30/30 at 1.27 mean interventions vs 2.37 random; learner exact-memory policy 34.85% vs FIFO 26.52%/random 26.14% (video 34.69% vs 26.53%); 4-input 5-comparator sorting network found after 2,698 candidates; learner-owned connection fabric scaled to 5M edges (42 logical bytes/edge, ~0.87M updates/s, ~0.008 ms latency). R49 supplement fixed two preserved failures (curiosity picked noise 87.78% of tail; self-model best-strategy ID 25%→100% via structured/windowed learnability + UCB-style exploration). Claim boundary: I5/I6 general invention NOT EARNED. Fills gap: no R48–R58 content in baseline beyond R51–R54 vision NO_GOs.
> "R48 failures preserved: The original curiosity policy selected random noise on 87.78% of the tail because positive one-step error fluctuations masqueraded as learning progress."
> "General invention remains NOT EARNED because I5/I6 multi-domain superiority/transfer has not been shown."

### 0001 — TNN/TNN/Research/R32_E51R_RESULT.md (3,761 B)
**NEW.** R32 E51R optimization-dose result (2026-08-30): extending coordinate-optimizer ceiling 12→24→48 sweeps on frozen 32-cell architecture — capability flat from 24→48 (no-unique UNKNOWN 1,166/1,200) even though the 48-sweep optimizer "was still accepting strict-loss updates". Training-first rule invoked; E51S justified. Extends baseline E45/E48 knowledge with the E51 series' training-first doctrine.
> "Raw optimizer convergence is not yet a sufficient stopping criterion." (via E51S) / "If episode reachability remains flat while training loss/sign accuracy continue moving, the mechanism is capability-limited rather than merely under-optimized."

### 0002 — TNN/TNN/Research/R32_E51S_RESULT.md (3,761 B)
**NEW.** E51S extended-dose: 48/96/192 sweeps — 192 gains only +2 no-unique vs 96, and 192 sweeps did NOT Pareto-dominate the simpler global-linear sign calibration (+18 no-unique but −3 known). Unresolved question recorded: "whether later optimization is monotonically repairing the same episodes or merely swapping which trajectories are solved." Extends E51R; feeds E51T audit.

### 0004 — TNN/TNN/Research/R33_B000_ANALYSIS.md (3,731 B)
**NEW.** Records that R33-B000's execution record shows a successful native compile but **zero native fixture executions** — "Expected values in the configuration and parser unit tests are authored fixtures, never native evidence." Fills gap: baseline knows the R33 S0/S1/S2 contract, not this specific zero-evidence caveat on B000.

### 0005 — TNN/TNN/Research/R32_E51F_STATE_ALIASING_AUDIT_PREREG.md (3,727 B)
**NEW.** Design rationale we lack: preregistered causal audit distinguishing (1) representation aliasing vs (2) value-function/capacity as the E51E residual cause — with "irreducible exact alias conflict" defined as the optimal-action-mask intersection going to zero over exact feature-vector equivalence classes, hash treated only as index. Motivating data: E51E made known reachability 4,200/4,200 while UNKNOWN stayed unreachable in 75/1,200 no-unique episodes.

### 0006 — TNN/TNN/Research/R32_E51K_RESULT.md (3,687 B)
**NEW.** E51K result: `VALID DIAGNOSTIC — CALIBRATOR_FIT_LIMITED`. The calibrated arms' development-to-validation gap was only ~0.1–0.6 pp — "The dominant error therefore already exists on the development distribution"; misplacing ~1/4 of positive and negative top-commit states on its own training worlds. Classifies the E51J failure as fit/objective-limited, not generalization-limited. Test result never seen.

### 0007 — TNN/TNN/Research/R32_E51L_RESULT.md (3,669 B)
**NEW.** E51L: `VALID NEGATIVE — NO_TESTED_TOP_COMMIT_SIGN_CALIBRATION_RESCUE`. Sign supervision raised positive-side accuracy to 88.5% but collapsed negative-side to 53.4% (hinges recovered only to 59–60%). New clearer frontier isolated: the state contains enough info to move between commitment/abstention, but the low-capacity scalar boundary can't represent the heterogeneous decision surface. Design rationale for the next training/capacity curve before any topology rewrite.

### 0008 — TNN/TNN/Research/R33_NATIVE_N17_R27_CONTINUITY/IMPLEMENTATION_DECISION.md (3,649 B)
**NEW.** N17 implementation decision: explicit six-criterion gate for ever adding a native digest/verifier (exact selector, reviewed type, byte-order rule, individual input hash, known-answer fixture, negative control) and the design rationale "This is a positive engineering decision, not an abandoned work item. The available native evidence is enough to design the boundary, but not enough to write a trustworthy R26/R27 semantic digest or verifier." Superseding 2026-09-15 decision: code that "merely returns the retained R26/R27 digest, counts historical checks, or recursively guesses R25 is prohibited and would invalidate continuity."

### 0010 — TNN/TNN/Research/R32_E51X_RESULT.md (3,599 B)
**NEW.** E51X: `CONFIRMED RESCUE — EXTENDED_TRAJECTORY_DOSE_RESCUE_CONFIRMED`. Trajectory-critical objective at 384 sweeps hit **5,400/5,400** on untouched validation and **8,400/8,400 + 2,400/2,400** on sealed confirmation — "exact terminal action reachability was obtained without graph or cross-context connectivity." Explicitly not R32 promotion. Key causal result the baseline lacks.
> "the existing native 32-cell conditional-weight substrate contains enough learner-visible information and capacity to achieve exact terminal action reachability... when trained with the trajectory-critical objective at sufficient optimization dose."

### 0012 — TNN/TNN/Research/R33_NATIVE_N07_AUTHORITY/REVIEW.md (3,578 B)
**NEW.** N07 authority/authentication engineering review: RFC2104 HMAC construction with seven RFC4231 SHA256 known-answer cases; "HMAC is symmetric authentication, not asymmetric/nonrepudiable human identity"; every request body byte MAC-covered; partial intents "deliberately block recovery rather than guessing a grant or refunding a charge" (fail-closed). Extends baseline's trainer-console auth item with the pre-existing N07 grant/authority engineering rationale and its stated limits.

### 0013 — TNN/TNN/Research/R32_E51W_RESULT.md (3,571 B)
**NEW.** E51W trajectory-dose: `VALID STABLE PARTIAL`. 96-sweep arm within **2/1,200** of the exact gate (4,200/4,200 known, 1,198/1,200 no-unique UNKNOWN) — "the tested fixed local conditional-weight substrate is already within two validation trajectories of the exact terminal-reachability gate," so no graph/cross-context connectivity justified yet. Training-first diagnosis strengthened.

### 0014 — TNN/TNN/Research/R33_SELF_MODEL_CONSCIOUSNESS_RESEARCH_PLAN.md (3,551 B)
**NEW.** The R33 self-model/consciousness research plan: 11-capability operational battery (self/world distinction, introspective access, autobiographical continuity, uncertainty knowledge, failure prediction, value/policy conflict, information seeking, metacognitive strategy, self-directed learning, safe self-revision, grounded self-report), each with explicit falsifiers. Governance: "Current TNN is not claimed conscious" and positive results "neither resolve theories of consciousness nor confer personhood." Design rationale + governance never in baseline.

### 0016 — TNN/TNN/Research/R33_NATIVE_N05B_RESULT.md (3,490 B)
**NEW.** N05B bounded durable telemetry: corrective regression PASSED (41 children, 749 child + 406 parent checks; five deliberate exit-73 deaths + one parent-enforced SIGKILL as registered). Corrected root cause: "remove the four-byte native-storage assumption" — allocator stride measured 8-byte. Root cause pairing with N05A failure (see 0045). Fills telemetry-engineering history the baseline lacks.

### 0018 — TNN/TNN/Research/R33_B001_C02_RESULT.md (3,469 B)
**NEW.** C02 result (2026-09-05): 48 native process cases matched independent byte/metadata/state oracles; 144,384 vector values checked; malformed/capacity/corrupt cases rejected; "This is not a learner, natural-perception certificate, signed/durable brain checkpoint or R33 promotion." Test result never seen (baseline only knows the C01 11-bug review).

### 0024 — TNN/TNN/Research/R32_E51U_RESULT.md (3,411 B)
**NEW.** E51U learner-owned local-interaction Foundry: `VALID NATIVE NEGATIVE — NO_TESTED_LOCAL_INTERACTION_RESCUE`. 64 learner-selected deterministic pairwise terms (2/cell) "did alter the learned boundary, yet those state-level changes did not translate into a larger set of trajectories with a valid stopping action" — a mismatch between state-level residual fitting and the trajectory-level control objective. Motivates a trajectory-aware multiple-instance objective before any cross-context connectivity. Abandoned-direction evidence (generic local interactions ruled out at this frontier).

### 0025 — TNN/TNN/Research/R47_STATE_RESIDUAL_MIXTURE_20260918/R47_RESULT.md (3,397 B)
**NEW.** R47 closeout: **DEVELOPMENT NO-GO / FRESH UNOPENED** (2026-09-18). Three state-conditioned residual-mixture candidates over the retained R39 70/30 factor/stable predictor; best (`mix_balanced`) passed 7/8 gates, missing only cross-noise; all NO-GO, so fresh family never opened. 60 jobs, CPython 3.13.12 + NumPy 2.3.5. Test results never seen; extends the R39–R42 reliability branch the baseline doesn't cover.
> "The next bounded discriminator should preserve local specialization but make noise abstention itself learned from delayed reliability rather than a fixed scalar penalty."

### 0026 — TNN/TNN/Research/R32_E51T_RESULT.md (3,363 B)
**NEW.** E51T paired stability audit: 96→192 sweeps on fresh worlds — known 4,198/4,198 both; no-unique 1,170/1,170 both, with **5 gained / 5 lost**: "the later optimizer does not form a success superset. It changes which ambiguous trajectories are solved while leaving aggregate no-unique reachability unchanged." Causal conclusion: `OPTIMIZATION_BOUNDARY_INSTABILITY` — further coordinate dose unjustified; training-first gate satisfied for the local-interaction Foundry (which became E51U). Major diagnostic rationale.

### 0028 — TNN/TNN/Research/R32_E51Q_RESULT.md (3,310 B)
**NEW.** E51Q margin-geometry audit: uniform-margin rescue IMPOSSIBLE — weakest known correct trajectory needs margin down to ≈+734 while worst blocked no-unique stays at ≈+828; "the printed uniform interval bounds do not overlap" (`e51q_uniform_interval_exists=0`). Exact residual aliases: 0; blocked minima spread across 10 routed cells, separated from weakest-known states in learner-visible feature space. Residual failure is local and learner-distinguishable → dose-first, not interactions. Design rationale never seen.

### 0029 — TNN/TNN/Research/R42_STATE_CONDITIONED_RELIABILITY_20260917/PREREGISTRATION.md (3,299 B)
**NEW.** R42 preregistration (2026-09-17, freeze revision 2): bounded state-conditioned correction to the retained R36 posterior + R39 70% factor/30% stable blend; three candidates (`state_cautious/balanced/fast` with exact hyperparams); eight admission gates vs paired retained R39 rows; "If no candidate passes every gate, the inherited R41 fresh family remains unopened." Prereg + design rationale never seen (R40/R41/R42 branch not in baseline).

### 0030 — TNN/TNN/Research/TNN_R50_R58_P1_P2_SYNTHESIS_20260918.md (3,290 B)
**NEW.** R50–R58 synthesis extends baseline's "R51–R54 vision honest NO_GOs (Python)": R50 bounded positives — grounded compositional language 100% synthetic (C4), acoustic motifs + held-out phrase compositions 100%/100%, cross-modal grounding 100% on four randomized correspondences, object persistence passed; R51 learned tool-plan selection 94.5% vs 20% update-disabled. Visual lineage: R52–R58 ALL NO_GO with exact floors — best learned branches (R56 conv: clean 97.83%, occluded 81.22%, active reinspection 96.29%; R58: clean 97.95%, occluded 81.80%) unmet on single-view occlusion (~82%) and heavy sparse noise (~66–67%). "No visual failure was converted into a pass by changing a previously exposed threshold."
> "Natural video perception: NOT EARNED. Natural connected speech: NOT EARNED. Broad natural language: NOT EARNED."

### 0040 — TNN/TNN/Research/R33_CONTINUING_LIFE_V1/CONTINUING_LIFE_DESIGN.md (3,208 B)
**NEW.** Continuing-life design — the shared boundary for simulated and real-sensory tracks: observation = raw payload + source/clock identity + sequence + SHA-256; 12-section checkpoint (1–10 learner-owned, 11 world-owned, 12 ingress-owned); "Delayed outcomes remain in world state and in the checkpoint; they are never filled in from evaluator knowledge." Integration rule: fresh-process reload must restore learner + causal trace + world + sensory stream "as a single accepted continuation" — "A frozen parent file plus a separately initialized learner does not satisfy this rule." Ingress at this stage: "encoded PCM16LE and RGB8 transport only... not a physical microphone/camera or perception qualification." Senses-origins design rationale we lack.

### 0043 — TNN/TNN/Research/R32_E51D_TERMINAL_REACHABILITY_AUDIT_PREREG.md (3,105 B)
**NEW.** E51D prereg design rationale: with E50's terminal head frozen, "is a correct terminal action reachable at any resource-feasible stopping time on each valid E51B validation episode?" — an oracle ceiling audit. Decision rule: if any episode lacks a reachable successful terminal action, "stop treating continuation-only changes as sufficient" → joint action-value Foundry over terminal actions + CONTINUE (UNKNOWN fixed at neutral zero). Anchors the E51 causal chain (E51A "continuation cannot help when the terminal controller never produces UNKNOWN"; E51C's saturated seed allocator invalidated its validation).

### 0045 — TNN/TNN/Research/R33_NATIVE_N05A_RESULT.md (3,012 B)
**NEW.** N05A preserved initial-recovery failure with root cause: the new allocator used `_zag_malloc(n*4)` for `[]i32` and assumed four bytes per in-memory word — retained root showed last three config words "overwritten with pathname-like bytes rather than 1,1,1"; recovery returned −8108. "The failure belongs to the new adapter, not the unchanged N04 accumulator or R27." Preserved frozen, never edited; N05B (see 0016) is the corrective regression. Engineering root-cause rationale.

### 0049 — TNN/TNN/Research/R33_NATIVE_N17_R27_CONTINUITY/RECOVERY_20260915_B_INDEPENDENT/REVIEW.txt (2,953 B)
**NEW.** N17 independent-review addendum: FOUR native engineering identity/type equivalents PASS (R27-01, R26-01, R27-18, R26-34) — "identity is descriptor equality, exact type is the exact module/name tagged class"; full native pm_scan/pm_validate over 15,871,908 raw bytes, 375,763 nodes — all match. People anchor: "Carson handoff: earlier SERIALIZED_EQUIVALENCE_REVIEW.txt was an authored, explicitly non-independent receipt... No Carson acknowledgment claimed." Anchors a person (Carson) to a specific authorship/review event.

## CONFIRMS (one line each)

- 0011 LANE_B_AUDIT_20260915/README.md — CONFIRMS 0008's superseding decision: 50 direct static passes, 30 unresolved rows, R26 `44d36746…` from 391,221 preimage bytes, R27 `562aaaed…` from 17,764 bytes, V91 still requires native generation.
- 0015 R48 PREREGISTRATION.md — CONFIRMS 0000: the frozen R48 packet design (fresh-seed-after-freeze, learn_authority=0, adversarial controls, I5/I6 exclusion).
- 0023 R32_E51K_CALIBRATION_GENERALIZATION_AUDIT_PREREG.md — CONFIRMS 0006's audit framing (fit-vs-generalization question, frozen sign convention ≥0/<0).
- 0035 R33_NATIVE_N14_SENSOR_INFORMATION/INDEPENDENT_FINAL_REVIEW.md — CONFIRMS baseline N14 S1 PASS lineage: V2 APPROVE_FOR_PREREGISTRATION, exact per-child evidence counts (79/70/33), 12 metadata fields preserved.
- 0036 R33_FINAL_INTEGRATION_20260915T2145Z/N17_INDEPENDENT_REVIEW.md — CONFIRMS 0008/0011: 54-row bounded PASS, FAIL-CLOSED for full verifier/V91/R25; adds nuggets: V91 generates zero strings; exact 508-byte R25 historical receipt present and hash-checked.
- 0037 R34_NATIVE_CONTINUAL_LEARNER_V3/ADVERSARIAL_REVIEW.md — CONFIRMS baseline's V3 checklist awareness: anti-cheat failure modes (hidden-state/reward-answer leakage, continual-learning illusion, persistence illusion, torn-checkpoint refusal).

## SUPERSEDED (one line each)

- 0044 R33_REMEDIATION_FINAL_20260915/before/…/IMPLEMENTATION_DECISION.md — SUPERSEDED: byte-identical pre-audit copy of 0008's rationale, retained for custody.
- 0047 INDEPENDENT_REVIEW_FINAL_INTEGRATION_20260915.md — SUPERSEDED: byte-identical duplicate of 0046's N19 review.
- 0051 R33_NATIVE_N14_SENSOR_INFORMATION/INDEPENDENT_REVIEW_V1.md — SUPERSEDED by 0035's V2: V1 REQUEST_CHANGES (supervisor ran superseded BUILD_01; child-count check too weak).

## NOISE (one line each)

- 0003, 0017, 0031 (N19 recovery results.txt ×3) — all expected=actual; pure process checklists.
- 0009 N12 BUILD_AND_REVIEW_HISTORY.md — provenance-only; one person anchor: independent reviewer "Mill" inspected the N12 numeric-view source (F01–F05).
- 0019, 0020, 0021, 0032, 0033 (process.final/integrated/results.txt, recovery B) — all expected=actual.
- 0022 (fresh_1409 final), 0039 (repair), 0041 (recovery B results), 0042 (recovery B final) — all expected=actual.
- 0027 (recovery B independent final.results.txt) — all expected=actual EXCEPT `preserved expected=0 actual=1` — the ONLY mismatch across all 16 process .txt files; flag for the sweep coordinator (unclear which preservation check flipped).
- 0034, 0048, 0050 (N01P/N01/N01A preregs) — prospective native-supervisor process preregs, no results.
- 0038 (N05A pre-exposure review), 0046 (N19 repaired integration review) — bounded engineering reviews, no new science.
- 0047 note: `reproduce_poison_bypass expected=1 actual=1` — a poison-bypass that was *expected* to reproduce, reproduced.

## Contradictions with baseline

None loud. The batch is consistent: E51 series diagnostics reinforce (not contradict) the training-first doctrine; R48/R50–R58 claim boundaries explicitly disclaim I5/I6 and natural perception, matching baseline. One item to watch: 0027's `preserved expected=0 actual=1` is a check-expectation mismatch in an otherwise green recovery battery.
