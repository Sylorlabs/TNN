# New Knowledge from the Drive Document Sweep

**Date:** 2026-09-20
**Scope:** every document (`.md` / `.txt`) under `My Drive / TNN` — 1,068 catalog entries, read and compared against the repo wave 1–12 baseline.
**Coverage:** 892 unique byte-contents (SHA256); 103 duplicate groups / 279 entries sharing content. All 872 primary documents fully or skim-read by 12 readers; all entries content-verified.
**Disposition:** no loud contradictions with the baseline. The sweep is dominated by **design-rationale origins** (the written reasons behind standing laws), **unseen test numbers**, and **abandoned directions with stated reasons**. One partial supersession (R27 archive recovery), one naming correction, one compiler-bug-count question, one open RNG question.

---

## Part 1 — Where the standing laws came from (design rationale, dated)

### 1.1 The 40-preference file: the program's written constitution
**Doc:** `TNN_USER_RESEARCH_PREFERENCES.md` (Drive `TNN/TNN/Research/`), created 2026-08-20, updated 2026-08-21 / 08-23 / 09-05. 40 numbered preferences with dated rows.

This is the single most important rationale find: the standing laws Micah enforces are not folklore — they were written down, dated, and revised:

- **Training-first diagnosis (#3):** "When a result is weak, first determine whether the failure is caused by insufficient data, poor lesson quality, missing contrasts, bad curriculum ordering, inadequate rehearsal, or a weak teacher. Change architecture only when the learning curve or error structure shows that training is no longer the main bottleneck." This is the written ancestor of the program's training-first discipline — and it is why R30's no-VAD result (0% → 96.56% from training alone, §3.2) was read as a training win rather than an architecture prompt.
- **Pure-Zag law, dated (#32-adjacent, 2026-09-05 entry):** "Effective: direct human instruction 2026-09-05, after C03. This supersedes earlier permissions to use Python as external supervision, packaging or evaluation." So the pure-Zag rule is a **direct instruction with an effective date**, not a convention that drifted in. The native-migration audit of 2026-08-29 counted the split it closed: **148 Python files and 32 native Zag source files; all 148 Python files removed from the checked-out tree.**
- **Consciousness (#38):** "Consciousness is a project goal/research lane, not a current capability claim" — the program pursues it while separating measurements from unsupported claims. This matches the baseline's R33 honesty framing and the wave-11 decision to treat consciousness-related work as research-lane only.
- **UNKNOWN as structured epistemic state (#32):** the program had an explicit unknown-state before the current work — relevant to the wave-11+ honesty instrumentation.
- **Equal-fighting-chance comparisons (#37):** comparisons must use scaling curves / Pareto fronts, not single-point wins — the written ancestor of no-free-lunch benchmarking.
- **Graph retirement (#23):** "Large context-switching architecture replacements are acceptable and desirable when evidence indicates the current substrate constrains capability" — the permission slip used when graphs were retired (§4.1).
- **Scaffold arm (#19):** an `INNATE_SYSTEM_FLUENCY` arm existed as an explicit experimental option — early scaffolding vocabulary.
- Also: **"Do not store TNN project details in universal memory; keep them in project-local cloud files"** (`TNN_USER_RESPONSE_LOG.md`) — this is why the entire corpus lives in Drive/local files rather than any shared memory system. It explains the organization of everything we just swept.

### 1.2 Promotion doctrine: Pareto dominance, not average wins
**Doc:** `R32_R27_DOMINANCE_PROGRAM.md` (2026-08-29). Promotion requires **"Pareto-style capability dominance,"** not better average scores: "preserve the accepted R27 substrate and regression battery, add general capabilities R27 lacks, and demonstrate that the improvements survive fresh native qualification without evaluator leakage, newborn restart, or researcher-written domain policy."

Learner-owned decisions are enumerated: what reusable chunks/constructions to recruit; what non-core PAM topology to create, specialize, combine or delete; what questions to ask teachers/siblings; when a learned mechanism should be rolled back after regret. Disallowed shortcuts: **newborn restart used to hide interference**, and **promoting Python/reference behavior as native TNN capability**. This is the direct ancestor of the current program's promotion skepticism (wave 11's phase-transition gates, the pure-trainer 0→1 gate).

### 1.3 Autonomy: how, not what
**Doc:** `TNN_AUTONOMY_POSITION.md`. "TNN should become more autonomous in deciding **how to learn**, not in silently deciding what it is allowed to do." Autonomy ladder A0 (passive) → A5 (developmental learner, owns learning strategy, architecture-search policy, and when not to modify itself). "Higher autonomy must be earned through evidence. It is not unlocked because the system produces convincing explanations, passes a language benchmark, or asks for permission in natural language." — This sentence is doing real work: it rules out exactly the LLM-style autonomy theater the baseline warns about.

### 1.4 Authority: permission is an intersection
**Doc:** `R33_AUTHORITY_MILESTONE_LADDER.md`. Effective permission = intersection of (architecture qualification × authenticated human-trainer grant × supervisor policy limits). **"A high score is not permission. A trainer may restrict an instance below the maximum scientifically qualified level."** M7 (integrated high-autonomy development) carries an explicit "not a consciousness certificate" caveat. Extends the baseline's phase-gate knowledge.

### 1.5 Naming correction — TNN is not an acronym for "Grounded, Active, Non-Token Cognition"
**Doc:** `TNN_CATEGORY_COMPARISON.md`. "Canonical name: **TNN = True Neural Network**. 'Grounded, Active, Non-Token Cognition' describes the direction; it is not the acronym expansion." The baseline has used the phrase as if it were the expansion — that wording should be corrected wherever it appears. The same doc carries a 20-row TNN-vs-LLM-vs-conventional-NN-vs-symbolic-vs-RL-vs-cognitive-architecture comparison table; its bottom line: "deliberate combination of neural computation, continual learning, active inference, episodic memory, cognitive architecture, and governed structural plasticity. Its proposed differentiator is the **integration and ownership model**, not the claim that every component is individually unprecedented."

### 1.6 Trainer interface and telemetry
**Doc:** `R33_TRAINER_INTERFACE_AND_TELEMETRY.md`. Trainer workflow: the trainer declares competency/goals/constraints; teaches goals and consequences, **not hidden answers**; plus a required measurements table (learning speed vs unique experience, generalization, memorization, retention/forgetting). This is the written origin of the trainer-console discipline and the telemetry-first stance in current work.

### 1.7 The scaffold-and-release origin: a Micah-requested hardcoded-English experiment
**Doc:** `tnn-pre-v1-r6-rsi-HARDCODED_ENGLISH_CONTROL.md` (2026-08-23). "The user requested a deliberate hardcoded-English experiment." A co-trained raw-text substrate retained bounded language after the prosthesis was withdrawn (**0.9375 exact**); the prosthesis alone scored covered-grammar 1.000 but **outside-grammar 0.000**. Quote: "A generic raw-text substrate trained while the prosthesis supplies meanings retains much of the bounded language after the prosthesis is removed. That suggests a temporary scaffold may accelerate acquisition." This is the historical precedent for the current program's scaffold-and-release paradigm (learner-initiated `SIGNAL_DISCONNECT`) — the baseline records the mechanism as law but had no recorded origin. Note it also carried an early honest-evaluation boundary: the scaffold result "cannot contribute to any TNN production gate."

### 1.8 Test discipline, written down
**Doc:** `SCIENTIFIC_CAMPAIGN_GATE.md`. "A failure determines the next controlled investigation; **more checkpoints or longer execution do not count as improved cognition**." — the written ancestor of the kill-criteria culture.

### 1.9 R33 scenario battery: planned, never executed
**Doc:** `R33_SCENARIO_BATTERY.md`. "Status: scenario definitions, not allocated evidence." Includes the design line "All developmental scenarios retain one branch's continuing history." Planned-but-unexecuted — do not cite as evidence.

### 1.10 New hypotheses that were never allocated
**Doc:** `R33_NOVEL_TNN_EXPERIMENTS_20260911.md` (2026-09-11). Six new R33 hypotheses E01–E06 (starting with E01 adaptive support-manifold routing). "No scientific population for E01–E06 may be allocated from this document." Portfolio only — relevant as candidate directions, not results.

---

## Part 2 — Senses and PAM origins (what the old sensory stack actually was)

### 2.1 The original PAM definition
**Docs:** R5-era research notes. A PAM is "a local adaptive neural field near a sensory receptor" — it may normalize, denoise, compress, track temporal structure, and emit motifs. It has **no private identity/goals/autobiography/world model**. And: **"PAMs are not fibers."** (The fibers concept is separate — see §2.9.)

### 2.2 The R5 sensory tournament (2026-08-23) — why the old winners won
- **Recurrent visual PAM + global-identity/local-temporal hybrid audio PAM** won the pre-v1 tournament.
- `noisy_then_clean` training was the strongest regime.
- **"Video first, language much later" was rejected:** language and video worked better trained in the same persistent state.
- **Broad surprise-span memory was abandoned** because it regressed established meaning and consumed excessive compute.
- Oldest senses roadmap (`tnn-pre-v1-r5-NEXT_STAGE_HANDOFF.md`): Priority 1 — one-shot motif binding without interference; Priority 3 — natural developmental media.

### 2.3 The PAM Foundry — and why it was later killed
**Docs:** R27-era Foundry records. Two opcode-credit learners **underperformed random generation**; whole-graph evolutionary shadow search produced **+55.93 hidden gain and 99.33% hidden win rate**. The historical document called it "the canonical Foundry design in the shadow Zag source." This is an **archaeology lead, not permission to revive graphs** — later R28/R33 evidence explicitly killed graph cognition (§4.1). The R28 handoff demanded improving the Foundry "from six-profile meta-search to many procedurally distinct landscapes and require clear learned-over-random replication" — the learned-over-random bar is the ancestor of current no-free-lunch benchmarking.

### 2.4 R31 endogenous chunking — the numbers behind the dual route
**Docs:** `R31_FINAL_REPORT.md` (shadow), `TNN_USER_RESPONSE_LOG.md`. No transformer/LLM/BPE/fixed tokenizer/next-token objective, and no supplied VAD or word boundaries:
- raw-active grounding **~0.9213**; chunk-only **~0.7533**; dual route **~0.9209 with ~85% compression**.
- "Causal ablation rejected chunk-only sensory cognition: chunk-only hard grounding ~0.753 while raw-active ~0.921; dual-active preserved ~0.921 hard grounding while retaining ~0.852 compression gain and slightly improving near-twin discrimination."
- **Decision:** "self-chunking is retained as a compression/indexing/grounded-construction/memory route, but it must not erase or replace raw episodic evidence."
- Adaptive Motif evidence: **33,450 raw units compressed to 2,789 motif units with exact round trip**; regime memory "reduced context-model thrashing from ~2,147 switches to ~13."
- **Exact replay: PASS_EXACT_EQUIVALENCE** — seed 9700 rerun identical, maximum absolute delta 0.0. The earlier V3 synthetic A control was "superseded as an evaluator and remains retained only as a rejected diagnostic."
- The Motif Microscope doc gives the hierarchy the old stack actually learned: "messy overlapping compression motifs → grounded discriminative alternatives → construction schemas → one-shot support-gap binding." Only ~14–30% of the lower Adaptive Motif layer's top-160 motifs aligned with known surface values; the higher contrastive-memory layer isolated clean cores (1.0000 / 0.9683).

### 2.5 Acoustic PAM head-to-head (the "don't force boundaries" rule)
**Docs:** `R32_COMPACT_HANDOFF_CURRENT.md`, `NEXT_AGENT_START_HERE.md`. On seeds 35000/35200: temporal-convolution raw-temporal PAM — overall **0.8409**, hard mean **0.8559** (seed 35000); segmental recurrent / learned-boundary PAM — overall **0.7917**, hard mean **0.7928**; seed 35200 temporal convolution — overall **0.9104**, hard mean **0.9235**. The drawn rationale: "the current learned segmentation gate is probably throwing away useful temporal evidence. **Do not force boundary decisions into the core sensory route.**" A v2 decision-policy overcorrection hit `ambiguous_unknown_rate=1.0` (automatically suspicious) while resolvable correctness fell to ~0.22–0.48 across hostile conditions — corrective rule: "Train the decision policy only from delayed utility/regret."

### 2.6 What the old brain actually contained
**Doc:** `r26_digest_excerpt.py.txt`. The R26 state dataclass carried `video_encoder`, `speech_segmenter`, `speech_index`, `semantic_generator`, `self_revision_history` — a genuine sensory architecture, not a stub list.
**Doc:** `TNN_R27_TRACEABILITY.md`. The old causal pipeline contract: "raw evidence → core signature → PAM route → entity hypothesis → memory retrieval → world/language binding → decision → error → failure diagnosis → PAM/memory revision."

### 2.7 R28 acoustic-speech direction and the CTC rejection
**Docs:** R28 handoff and failure records. Direction: "Attack connected speech as **context-conditioned acoustic sequence learning, not as isolated motifs plus guessed hard cuts**. Preserve all failed CTC/DTW/EM/transition branches." Numbers: isolated acoustic pretraining **91.81%**; CTC fine-tuning **5.14%**; hard connected speech **22.08%** — the CTC formulation was rejected on evidence. Memory default stayed the researcher-authored privileged heuristic with explicit training of the TNN override to surpass it; LRU stayed eviction-only.

### 2.8 V39 GRU PAM rejection — the stated causal rationale
**Doc:** `R32_EPISTEMIC_R31_MATCHED_V39_INTERPRETATION.md`. The GRU PAM "broadened the action region rather than identifying the positive option-value boundary. This rejects the idea that replacing summaries with an opaque recurrent embedding is sufficient." The baseline recorded V39's failure without this causal sentence.

### 2.9 Resource envelope / fibers
**Doc:** `tnn-v1-current-execution-COMPUTE-EFFICIENCY.md` (2026-08-23). "The human defines the total **Resource Envelope**. TNN—not the trainer—must decide how many **fibers** exist and how much of the envelope each fiber consumes." Caveat, kept honest: "This is a controlled evaluator, not yet the final endogenous allocation mechanism. Production TNN must learn its allocation behavior from consequences rather than receiving the evaluator's formula."

### 2.10 What the old senses were NOT
- **N06/N14 are encoded-file transport/information passes**, not live microphone/camera or S2 perception. N14 authoring history: the PCM fixture was "strengthened from a small mixed-sign sample to the maximum 131,072-byte mono payload"; BUILD_01/02 byte-identical binaries superseded pre-review.
- **Continuing-life design** is explicit: current ingress is encoded PCM16LE/RGB8 only, and a frozen parent plus a separately initialized learner does not constitute continuing life.
- **R52–R58 vision lineage: all NO_GO.** Best clean ~97.8–97.95%, occluded ~81–82%, heavy sparse noise ~66–67%. R54's diagnosis: "hand-selected geometric summaries are the current visual bottleneck." R55–R58 progressively tested dense learned, convolutional, scanned template, and support-channel approaches. Natural vision remains not earned.
- **TNN v1 beta gates, all false:** `archive_cleanroom_pass: false`, `controlled_native_english_pass: false`, `real_senses_probe_pass: false`, `tnn_v1_beta: false` — a dated snapshot of how far the old program was from claiming anything production.
- **No live-device evidence anywhere in the sweep.** Audio and vision remain NOT_QUALIFIED, consistent with the current program.

---

## Part 3 — Test results the baseline never had

### 3.1 R27 archive: recovered bytes, still-missing semantics (partial supersession)
**Finding:** `tnn-pre-v1-r27-general-learning.zip` — **56,777,645 bytes, SHA256 `7042ff8497…b65e`** — was recovered from **Micah's ChatGPT Library**. The embedded accepted state matched the canonical `31e670fc…96e5a`; `r27_experiments.py`, `R27State.digest()`, and the 33-check verifier semantics were recovered. V91 receipts add: 16/16 oracle matches, native frame deterministic, but `v91_full_gate_open=false` and generator parity blocked.
**Honest reading:** this partially supersedes "R27 unrecoverable" — but **not** the unrecovered perceptual-inference semantics or trace-op semantics (R27-08/09 SOCIAL_NEAR/FAR bytes exist with no admitted inference/evaluation semantics). The recovered Lane-B supplement is explicit: "V91 remains unimplementable faithfully from available bytes: original dataset, special tokens, forward/input construction, arithmetic and seeded sampling…" And the custody caveat, worth quoting: **"Byte custody proves non-mutation, not behavioral continuity."** Lane-B's deep search is quantified: 947,360 returned paths, 889,854 hashed files, 157 archive inventories, all 1,610 Git blobs (744,029,506 bytes) hashed. "No missing exact source/state/manifest input admitted."

### 3.2 R30 no-VAD speech: training, not architecture
**Result (2026-08-23):** no-VAD speech moved from **0% at 1,024 utterances to 96.56% at 100,000** without changing the core architecture — the program's canonical "diagnose training before architecture" evidence. **Caveat:** this is a reconstructed SHADOW report after znc/workspace loss; R30's raw artifacts were lost in a container reset, and the recovery ledger was built from printed metrics only — explicitly non-promotable. R30 stays shadow/reference.

### 3.3 R28 memory battery: the privileged-heuristic origin
**Result (2026-08-23):** 12-seed battery. Pure LRU won raw recall but sacrificed exact-detail retention. The researcher-authored `PRIVILEGED_HEURISTIC_DEFAULT` + TNN override had the highest defined utility. LRU became subordinate eviction mechanics, not memory authority. The default was explicitly hardcoded and **"not credited as learned cognition."** This is the written origin of the current memory-policy shape.

### 3.4 R6 support-gap recruitment
First unprotected schema branch was rolled back after established exactness fell **0.9911 → 0.9291**; the replacement recruited only unsupported raw spans and protected familiar grounded spans. The R6 human-comparison protocol is explicit: "R6 does **not** claim to beat humans. No matched human participants were tested."

### 3.5 N15/N16 stability–plasticity
N15: zero protected-anchor loss can coexist with unseen old-probe loss. N16: full bounded synthetic stability/plasticity qualification passed with arm19 over **498 exposures**, reducing old loss to **12/7 on disjoint holdouts**. (This does not establish R27 continuity.)

### 3.6 E51 terminal/replay arc
- **E51X:** 5,400/5,400 untouched validation; 8,400/8,400 known + 2,400/2,400 no-unique sealed confirmation; exact terminal reachability **without graphs or cross-context connectivity** — a bounded R32 result, not broad promotion.
- **E51T:** 96→192 sweeps gained five and lost five ambiguous trajectories — later optimization was **not** a success superset.
- **E51AH** local replay rescued 159 but lost 121 previously successful cases — the zero-loss gate failed. **E51AJ** final old-success losses: **1/14, 9/11, 17/6** across replicas; the preregistered retention rule **failed 2 of 3 replicas**; the no-final-behavioral-tradeoff flag failed in every replica. Replay improved some disruption/recovery measures but is **not** a preservation cure.
- **E51 causal map:** E51AF permanently invalid (historical prerequisite mismatch, never run); E51AH grounded preservation replay frozen-not-run.
- **Oracle caveat:** several E51 reports say an evaluator-only oracle assigned `success=1` rather than evaluating the selected action — this qualifies expressivity interpretations, not necessarily all learned-arm comparisons.
- **E51N:** seed-namespace exhaustion — the allocator failed after 8,352 of 18,360 requested worlds. Negative result, kept.

### 3.7 R36–R46: the full NO-GO series (state-conditioned reliability)
**Doc:** `SESSION_FINDING_SNAPSHOT.md` = `TNN_SESSION_FINDING_20260917_STATE_CONDITIONED_RELIABILITY.md` (2026-09-17). R36–R41 archives restored; R39 fixed 70/30 online-factor/stable blend; R40 (120 dev jobs, zero candidates) and R41 (120 dev jobs, zero candidates) both development NO-GOs — "global channel-level scalar reliability is too coarse (R40)"; "strategy-specific scalar reliability is still too coarse (R41)." R42 state-conditioned correction: NO-GO. R46 continuous factorized residual: NO-GO ("could strongly improve specific recurrence behavior, but those gains interfered with broader post-change, recombination, and noise performance"). Verified conclusion: "The remaining problem is not solved by progressively finer scalar reliability memories or by one continuously learned additive residual surface… The next hypothesis needs **multiple locally valid predictive corrections with explicit interference control** rather than one shared correction." **Caveat:** this campaign ran on CPython 3.13.12/NumPy 2.3.5 — reference/shadow discipline, not native Zag.
- R36 selection freeze: `eig_012` selected after preregistered development aggregation; fresh challenge on seeds 36203/36209/36217 on `abaca`, `gradual`, `success_only`, `long_return`; "No source or threshold change is permitted before the fresh result."
- R39 implementation correction (2026-09-18): an honest prereg deviation record — the first probe revealed factor creation could never fire (posterior max identically 1.0 with one expert vs required <0.78); corrected pre-tournament; the pre-correction probe preserved under `invalid_pre_freeze_probe/` and not scored.

### 3.8 R34 learner worklogs
- **R34 v2** (2026-09-16): "after 24 A experiences: 16/16 positive at zero-update evaluation"; "after hidden switch and 24 B experiences: 16/16 positive" — latent-context memory numbers the baseline lacked.
- **R34 v3** worklog notes `r34_learner_core.zag` "contains learner state, deterministic RNG, action choice…" — the RNG driver is unexplained. **Open question** (see §5.4), not a contradiction.

### 3.9 R48–R58 campaign detail
- **R48:** 20/20 symbolic reasoning; 30/30 causal selection (1.27 vs 2.37 random interventions); 4-input 5-comparator sorting network after 2,698 candidates; connection fabric tested to 5M edges; **curiosity failed** — selected noise in 87.78% of its tail; I5/I6 general invention not earned. R49 repaired the curiosity/self-model issues → PASS.
- **R50:** bounded synthetic positives included synthetic language/hearing/cross-modal/object persistence. **R51:** tool-plan selection 94.5% vs 20% control.
- **R52–R58:** all NO_GO (see §2.10).

### 3.10 Native-purity evidence
- **R33 purity gate (2026-09-14): QUALIFIED PASS** — compiler pinned at `/Users/Shared/micah/Documents/Zag/znc` (SHA `3093d12d…`), fail-closed on Python/PyTorch/NumPy/sklearn/jq references.
- Old program-induction native test (`tnn-debug-script.txt`): Zag source compiled and run against hidden tests — a native-first testing precedent from pre-R33.
- Evidence-custody rule (`history.py.txt`): "Historical interpreter source is inert byte evidence only. It is never executed."

---

## Part 4 — Abandoned directions, with the stated reasons

| Direction | Stated reason for abandonment | Source |
|---|---|---|
| Graphs as active cognition | AEIF 93.57% vs graph-authority 80.71%; graph-heavy systems scored by **refusing to change identity**; graphs retained only as frozen controls/derived indexes. R33 contract: historical graph controls do not justify restarting the tournament | R28 AEIF records; R33 architecture contract |
| Whole-graph evolutionary Foundry | Worked in shadow (+55.93 hidden gain) but graph cognition retired; superseded by learned-over-random replication bar | R27 Foundry; R28 handoff |
| Broad surprise-span memory | Regressed established meaning; excessive compute | R5 (2026-08-23) |
| "Video first, language much later" staging | Language+video better in the same persistent state | R5 |
| CTC/DTW/EM/transition branches for connected speech | 5.14% CTC fine-tune vs 91.81% isolated; formulation rejected, branches preserved as evidence | R28 failures |
| Opcode-credit Foundry learners | Underperformed random generation | R27 Foundry |
| Hardcoded English as production path | 0.000 outside grammar; scaffold only, cannot touch production gates | R6 control (Micah-requested) |
| Opaque recurrent (GRU) PAM embedding | Broadened action region instead of finding the positive option-value boundary | V39 interpretation |
| Learned segmentation boundaries in the core sensory route | Gate threw away useful temporal evidence (0.7917 vs 0.8409/0.9104) | R32 handoff |
| Local replay as preservation cure | Rescued 159, lost 121; helps disruption/recovery, not preservation | E51AH |
| Scalar reliability memories / one additive residual | R40/R41/R42/R46 all NO-GO; need multiple locally valid corrections with interference control | R36–R46 campaign |
| Hand-selected geometric visual summaries | "The current visual bottleneck" (R54); R52–R58 all NO_GO | R54–R58 |
| Pretrained vision models | Explicitly forbidden by the hardcoding ledger | R28 hardcoding ledger |
| E51AF branch | Prerequisite mismatch → INVALID, never run | E51 causal map |
| R6 unprotected schema branch | Exactness 0.9911→0.9291, rolled back | R6 |

---

## Part 5 — Tensions and corrections vs the baseline

### 5.1 R27 recoverability — partial supersession (honest version)
The baseline's "proven unrecoverable" needs the amendment from §3.1: the general-learning archive bytes **are** recovered with matching accepted state and verifier semantics, and Lane-B quantified the search. What remains unrecovered is unchanged: perceptual-inference semantics and trace-op semantics. Recommended baseline wording: "Archive bytes recovered and checksummed; behavioral continuity not established; perceptual inference and trace-op semantics remain unrecovered."

### 5.2 Naming — "True Neural Network"
Correct the baseline wherever it expands TNN as "Grounded, Active, Non-Token Cognition." Canonical: **TNN = True Neural Network**; the phrase describes the direction.

### 5.3 Compiler bug count — two new candidates need reconciliation
The baseline carries three known znc bugs. The Drive documents add two apparently distinct candidates: (1) imported top-level/bare `const` lowering across import boundaries — the parser-local const recognition doesn't propagate to the importing parser, so imported integer constants arrive as address/function-like values; (2) a compound boolean expression cast directly to `i32` failing to return the required `1` (explicit `return 1/0` fixes it). Neither should be called "the fourth bug" until it's determined whether they're distinct from each other and from the already-known arm64 syscall-lowering bug.

### 5.4 R34 v3 "deterministic RNG" — open question
A worklog describes `r34_learner_core.zag` as containing "learner state, deterministic RNG, action choice…" The RNG driver is unexplained. This is not a contradiction of the no-RNG law on its own (it may be an experimental driver), but it needs a look before anyone cites R34 v3 as canonical evidence.

### 5.5 Recovery anomalies — need context, not verdicts
`restoration.results.txt` reports `c_restored expected=0 actual=127` and `full_reviewer_baseline expected=0 actual=127`; another recovery result shows `preserved expected=0 actual=1`. These read like anomalies only without their surrounding procedure — do not cite as defects until the procedure is understood.

### 5.6 No other contradictions found
Twelve readers, 872 documents, targeted keyword sweeps for PAM/audio/speech/TTS/vision/sensor/perception, memory operations, abandoned/retired/failure/NO_GO/PASS, and architecture origins. **No document contradicted the wave 1–12 baseline's load-bearing claims** (determinism, memory agency results, phase gates, native-purity direction). The qualification in §5.1 and the corrections in §5.2–5.5 are the complete list.

---

## Part 6 — Dated anchors (people, dates, places)

- **2026-08-20** — preferences file created (40 preferences).
- **2026-08-21 / 08-23** — preference updates; 08-23 is the big pre-v1 research day (R5, R6, R28, R31, R33-era docs, hardcoded-English control, motif microscope).
- **2026-08-29** — native migration audit (148 Python / 32 Zag); R32→R27 dominance program; E51A run request ("This file contains no learner logic").
- **2026-08-31** — R32 agent snapshot request on branch `r32-agent-sequential-frontier` (nonce `e51ad-recovery-20260831-cce846d1`); "R27 remains canonical."
- **2026-09-05** — pure-Zag direct human instruction (after C03).
- **2026-09-06** — N14 postrun artifact verification 50/50 OK.
- **2026-09-11** — R33 novel experiments E01–E06 portfolio.
- **2026-09-14** — R33 native-purity gate QUALIFIED PASS.
- **2026-09-15** — R33 closeout/integration/remediation runs; evidence-freeze timestamps (EVIDENCE_FROZEN_UTC=2026-09-15T18:18:30Z); N17/N18/N19 verify contracts (eight policy gates locked).
- **2026-09-16** — R34 v2/v3 worklogs.
- **2026-09-17** — R36–R46 reliability snapshot; R23/R27 recovery provenance work.
- **2026-09-18** — R39 implementation correction.
- **Places:** `/Users/Shared/micah/Documents/TNN` (research root), `/Users/Shared/micah/Documents/Zag/znc` (pinned compiler, SHA `3093d12d…`), `/Users/Shared/micah/Downloads/TNN_COMPLETE_R1_R32_FULL_BACKUP.tar.gz` (full R1–R32 backup, SHA256 `f966c0c7f1649feb1e83436b21d7c51a41442e8a9f3f4f41c33f08affbb3d748`), Micah's ChatGPT Library (R23/R27 archive recovery provenance), koryphaios at `/Users/Shared/micah/Documents/koryphaios` (one archive-inventory path hit only — no code overlap).
- **N17 blockers** name old capabilities never natively re-implemented: serialized abstraction model, original SOCIAL_FAR evaluator, name memory, social evaluators.
- **R28 lineage:** `PARENT_FORMAT=TNN_PRE_V1_R27_GENERAL_LEARNING`, `PARENT_STEP=60423`, `BRANCH=TNN_R28_AEIF_NO_GRAPH_REBUILD`, `CANONICAL_PROMOTION=BLOCKED_PENDING_NATIVE_ZAG`.

---

## Part 7 — What the sweep did NOT find (negative results)

- **No live microphone/camera evidence.** No S2 perception claim. Audio/vision NOT_QUALIFIED stands.
- **No ghost hits** beyond incidental dependency/path text. **One koryphaios hit** — an archive-inventory path only; no code overlap.
- **No unrestricted-English evidence.** The strongest historical English result is the bounded hardcoded-English scaffold: 0.9375 exact inside grammar, **0.000 outside grammar**. This supports the standing answer: the current English pilot is a bounded curriculum result, not Muse-like conversation.
- **No RNG-in-canonical-decisions evidence** beyond the unexplained R34 v3 driver mention (§5.4).
- **No document disputes** the byte-identical replay results, the memory-agency findings, or the phase-gate structure.

---

## Appendix — method and coverage

- Enumeration: 3,595 folders, 44,285 files; 1,068 `.md`/`.txt` document entries (653 `.md`, 415 `.txt`; 63,732,366 listed bytes). No `.doc`/`.docx` or Google-native docs.
- Download: all 1,068 entries retrieved; every byte count verified against Drive metadata; SHA256 over downloaded bytes. The 196 remainder entries first returned CLI error payloads (the script omitted the required `--output` flag) — detected by content inspection, re-downloaded correctly, stale payload files deleted.
- Dedupe: **892 unique SHA256 contents**; 103 multi-file duplicate groups covering 279 entries (byte-identical). 135 of the 196 remainder entries duplicate already-read main-batch content (`.scratch/` extraction copies, run-dir duplicates).
- The 57 remainder-only unique contents were content-classified: 4 lane diff-witnesses (machine-generated line diffs), 4 path/object inventories, 8 inert reference source dumps (CPython pickle, NumPy, PyTorch, RFC 6234, generated `acodegen` Zag), run-metadata flags (exit codes, checksums, run IDs), and one procedural checklist (`PREFREEZE_MANIFEST_REQUIREMENTS.md` — N18 freeze-manifest discipline: hash every input file, TOCTOU refusal, seed-namespace collision checks; no scientific content). Spot-reads (E50 negative-rescue exit code 1, R34 v2 receipt `failures=0`) held no new scientific signal.
- Reading: 12 reader agents; all 872 primary documents received at least a skim/keyword pass, Tier-1 (416) fully read; promising Tier-2 fully read. Targeted sweeps: PAM/audio/speech/TTS/vision/sensor/perception; memory operations; abandoned/retired/failure/NO_GO/PASS; architecture origins; koryphaios/ghost.
- Known gap: one Tier-2 findings file (`tier2_batch0.md`) was truncated mid-write at finding 11 of 18 — its range (0416–0529) was independently covered by a second reader (`tier2_batch3.md`, 16 findings), so no range lost coverage, but 7 of that reader's grouped findings survive only in its handoff summary.
- Machine-readable artifacts: `docs.json` (1,068 entries with Drive id/path/size/modifiedTime), `manifest.json` + `download_rest` mapping (local files), `dedupe_by_content.json` (hash → entries), `error_payload_entries.json` (superseded failed-download record).
