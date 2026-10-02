# Tier-2 Batch 0 findings — doc sweep (files 0416–0529, 114 files)

Skimmed: 114. Read fully / in depth: ~24. NEW findings: 18 (grouped below).
No contradictions with BASELINE.md found — all status/doc claims are consistent with known program state (R27 canonical, R33 fail-closed, recovery blocked).

## NEW findings

### 1. TNN_USER_RESEARCH_PREFERENCES.md — dated living constraint file (2026-08-20, updated 2026-09-05)
`0422_TNN_USER_RESEARCH_PREFERENCES.md` (TNN/TNN/Research/TNN_USER_RESEARCH_PREFERENCES.md, 50,787 B, modified 2026-09-18).
NEW: the program's standing laws as of 2026-08-20, explicitly attributed to the user, far richer than the baseline's list. Preferences 1–16 + decision hierarchy + hardcoding ledger rule:
- Minimize hardcoding; "Hardcoded Master TNN may be highly capable because it is a teacher working with the base TNN, not a hidden implementation of the learner's final cognition" — with evidence: "Adaptive/grounded Master teaching repeatedly outperformed symbolic yes/no"; "R27's stronger Master bridge improved general-to-specific abstraction from 66.67% to 94.44% without a new named social-language module."
- Training-first 7-step diagnosis sequence (architecture only at a measured plateau).
- Promotion decision hierarchy: hidden capability/transfer > regression safety > teacher-withdrawal/delayed retention > provenance/evaluator-leak audit > noise/counterexample robustness > state continuity/deterministic reload > cost > elegance.
- Item 15, Memory autonomy: "TNN-controlled" — "Do not impose a human-authored developmental schedule that slowly phases exact memory away. TNN should choose what enters, stays in, moves between, compresses within, or leaves short-term, working/active, long-term structured, exact episodic, semantic, procedural, sensory, and archival memory."
- Item 12: TNN-created non-core PAMs must be autonomously instantiated ("PAM proposals must be executable structures, not English suggestions that require a researcher to translate them into source"); item 14: core PAMs protected but NOT sacred — researcher may redesign if deep evidence shows substrate bottleneck.
- 2026-09-05 entries: native-Zag-only correction ("This supersedes earlier permissions for Python external glue"), continuation correction (keep executing, not stop at convenient milestones), consciousness/independence pursued as a research goal while separating measurable self-model capability from unsupported consciousness claims.
Extends baseline standing laws; dates: 2026-08-20 / 2026-09-05.

### 2. E45–E48 terminal-controller outcomes (2026-08-28)
`0447_TNN_USER_RESPONSE_LOG.md` (TNN/TNN/Research/TNN_USER_RESPONSE_LOG.md, 21,738 B).
Baseline knows "four valid negatives" but not the verdicts:
- "E45 established a real no-unique safety failure under the repaired causal evaluator, not an evaluator collapse."
- E46: "none of six schedules met every-cell safety and known-performance gates"; revealed abstention-vs-known-resolution tradeoff.
- E47's two grounded co-presence statistics "did not rescue the blocked linear head."
- E48: `NO_TESTED_BATCH_SAFETY_RESCUE` — 346/1,020 safe cells (baseline) or 318/1,020 (joint).
- Binding operational guidance: "Do not repeat order sweeps or turn UNKNOWN into an evaluator-visible ambiguity class... UNKNOWN remains 'no warranted commit has positive grounded value.' The next bounded causal question is whether a minimal grounded nonlinear commit-value head or richer endogenous causal representation can repair the every-cell abstention / known-resolution tradeoff."

### 3. R30 shadow report — long-training validation
`0485_R30_FINAL_REPORT.md` (11,? KB, modified 2026-08-23). NEW test results + rationale, never in baseline:
- no-VAD speech, same fixed-acoustic-identity CTC learner: exact 0% at 1,024 utterances → 96.56% hard exact-sequence accuracy at 100,000 utterances "without changing the core speech architecture" — "direct evidence that the early zeros were undertraining, not proof of architectural failure."
- "User-requested extreme-score policy": exact 0%/100% repeatedly flagged undertraining/evaluator saturation; 100% silence-shift result "Automatically quarantined by the perfect-score suspicion rule."
- Three seeds at 57,600 utterances: 94.06% / 95.31% / 91.56%.
- CAVEAT (self-declared): R30 is a SHADOW — local znc couldn't be materialized and a container reset erased the unpersisted workspace; metrics reconstructed into durable recovery ledger, "not being relabeled as native-Zag evidence."

### 4. R31 shadow report — endogenous self-chunking architecture
`0478_R31_FINAL_REPORT.md` + `0506_R31_HANDOFF.md` (2026-08-23). NEW design rationale from the user's correction to R30:
- "R31 answers the user's correction to R30: TNN should not be evaluated or architected as a fixed-token/transformer-style sequence model. The forward architecture is **endogenous self-chunking over raw experience plus a high-fidelity raw/episodic bypass**."
- "No graph cognition. No transformer. No LLM. No BPE/fixed tokenizer. No next-token objective. No supplied VAD/phoneme/word/chunk boundary."
- Central ablation: raw active hard grounding 0.9213 / chunk-only 0.7533 / dual raw+chunk 0.9209 + ~85% compression — "self-chunking is retained as a compression/indexing/grounded-construction/memory route, but it must not erase or replace raw episodic evidence."
- Adaptive Motif lineage numbers: "33,450 raw held-out units were represented by 2,789 adaptive motif units with exact round-trip in the prior tournament."
- R31 handoff: binding constraints + a 13-variant acoustic self-chunking tournament plan (raw waveform only, matched doses).
- CAVEAT: R31 also SHADOW (couldn't materialize usable znc; graph-free native Zag target passes static source contract only).

### 5. E51AC–E51AJ arc — preservation/replay verdicts
`0482_R32_E51_PROGRAM_CHARTER.md`, `0501_R32_E51AC_AH_ARC_REPORT.md`, `0465_R32_COMPACT_HANDOFF_CURRENT.md`, `0474_R32_HANDOFF.md`, `0493_R32_E51_CAUSAL_MAP.md`, `0512_TABLES.md`, `0528_VALIDATION.md`. Entire arc absent from baseline. Key verdicts:
- E51AC: deployable hybrid 5,213 vs 5,156 mature controller, but lost 22 no-unique successes; evaluator union still missed 140 known trajectories.
- E51AD: conservative router failed held-out (5,175 vs 5,204 score-max vs 5,247 evaluator union) — "Routing cannot create support outside the fixed union."
- E51AE: residuals rescued 230 development misses but lost 509 union successes — "not a loss-free repair."
- E51AG: known gains 72/80/94 outweighed by no-unique losses 217/213/217 across three partitions.
- E51AH: `PRESERVATION_REPLAY_DEVELOPMENT_FAILURE` — global replay lost 236 union successes / rescued 6; local replay lost 121 / rescued 159; stages 109/110 stayed sealed.
- E51AF: permanently invalid (zero-execution integrity closure).
- E51AI: replay cut final anchor losses 22→9 and shared-anchor losses 21→5, but "failed preservation... a bounded tradeoff, not qualification."
- E51AJ: three-replica retention rule FAILS — sequential/replay final anchor losses 1/14, 9/11, 17/6; "More repeated fitting alone is not an established remedy." (1,101,600 probe rows, 67,860 coefficients, 1,212.888s native.)
- `0502` is an earlier .scratch snapshot of the E51 charter (Frontier amendment 2026-09-01) vs the main copy (Shared-start control amendment 2026-09-05).

### 6. R36–R46 state-conditioned reliability campaign
`0507_SESSION_FINDING_SNAPSHOT.md` = `0508_TNN_SESSION_FINDING_20260917_STATE_CONDITIONED_RELIABILITY.md` (7,151 B, 2026-09-17). Never in baseline:
- R36–R41 archives restored to the Mac (all MANIFEST.sha256 passed); R39 fixed 70/30 online-factor/stable blend; R40 (120 dev jobs, zero candidates) and R41 (120 dev jobs, zero candidates) both development NO-GOs — "global channel-level scalar reliability is too coarse (R40)"; "strategy-specific scalar reliability is still too coarse (R41)."
- R42 state-conditioned correction: NO-GO. R46 continuous factorized residual: NO-GO ("could strongly improve specific recurrence behavior, but those gains interfered with broader post-change, recombination, and noise performance").
- Verified conclusion: "The remaining problem is not solved by progressively finer scalar reliability memories or by one continuously learned additive residual surface... The next hypothesis needs multiple locally valid predictive corrections with explicit interference control rather than one shared correction."
- Caveat: this campaign ran on CPython 3.13.12/NumPy 2.3.5 — reference/shadow discipline, not native Zag.

### 7. R32→R27 Dominance Program — promotion rationale
`0480_R32_R27_DOMINANCE_PROGRAM.md` (2026-08-29). NEW design rationale: promotion requires "Pareto-style capability dominance," not better average scores — "preserve the accepted R27 substrate and regression battery, add general capabilities R27 lacks, and demonstrate that the improvements survive fresh native qualification without evaluator leakage, newborn restart, or researcher-written domain policy."
- Learner-owned decisions listed: "what reusable chunks/constructions to recruit... what non-core PAM topology to create, specialize, combine or delete... what questions to ask teachers/siblings... when a learned mechanism should be rolled back after regret."
- Disallowed shortcuts include "newborn restart used to hide interference" and "promoting Python/reference behavior as native TNN capability."

### 8. TNN autonomy position — A0–A5
`0525_TNN_AUTONOMY_POSITION.md`. NEW: "TNN should become more autonomous in deciding **how to learn**, not in silently deciding what it is allowed to do." Autonomy levels A0 (passive) → A5 (developmental learner, owns "learning strategy, architecture-search policy and when not to modify itself"); "Higher autonomy must be earned through evidence. It is not unlocked because the system produces convincing explanations, passes a language benchmark, or asks for permission in natural language."

### 9. TNN category comparison — identity statement
`0520_TNN_CATEGORY_COMPARISON.md`. NEW: "Canonical name: **TNN = True Neural Network**. 'Grounded, Active, Non-Token Cognition' describes the direction; it is not the acronym expansion." Plus a 20-row TNN-vs-LLM-vs-conventional-NN-vs-symbolic-vs-RL-vs-cognitive-architecture comparison table; bottom line: "deliberate combination of neural computation, continual learning, active inference, episodic memory, cognitive architecture, and governed structural plasticity. Its proposed differentiator is the **integration and ownership model**, not the claim that every component is individually unprecedented."

### 10. Authority milestone ladder M0–M7
`0519_R33_AUTHORITY_MILESTONE_LADDER.md`. NEW design spec: effective permission = intersection of (architecture qualification × authenticated human-trainer grant × supervisor policy limits). "A high score is not permission. A trainer may restrict an instance below the maximum scientifically qualified level." M7: integrated high-autonomy development with "not a consciousness certificate" caveat. Extends baseline's phase-gate knowledge.

### 11. Trainer interface + telemetry spec
`0511_R33_TRAINER_INTERFACE_AND_TELEMETRY.md`. NEW: trainer workflow (trainer declares competency/goals/constraints; teaches goals and consequences, not hidden answers) + required measurements table (learning speed vs unique experience, generalization, memorization, retention/forg
...[truncated 12402 chars]