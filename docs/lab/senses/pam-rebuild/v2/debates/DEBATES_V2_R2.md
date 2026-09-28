# DEBATES V2 — Round 4 (grounded): Sol vs the landed autopsies

**Date:** 2026-09-23. **Team 5b: Sol Round 4 (grounded in real autopsy findings).**
**Second opinion:** gpt-5.6-sol via UnoRouter (`~/workspace/skills/unorouter/bin/sol.py`), one live round, verbatim reply below.
**Moderator:** native Muse subagent (debate infrastructure — no mechanisms built).

## 0. Evidence base and tooling log

This round re-runs Round 1 items (c) and (d), which were briefed PROVISIONAL, against the now-landed sibling autopsies — per `DEBATES_V2.md` §6 recommendation 3. All four Team 2/3/4 autopsies were read in full:

- `v2/autopsy/AUTOPSY_R2-4.md` — R2-4 white-box autopsy: KNOWLEDGE with the trial-1145 qualification (pointwise adjudication machinery-impossible; fix must be historical)
- `v2/autopsy/AUTOPSY_DEATHBOARD.md` — 12-kill death board: 9 KNOWLEDGE / 1 MACHINERY (narrow) / 1 UNRECOVERABLE / 1 BENCHMARK BUG; "no detectable signal" synthesis refuted; H2 not a safety failure
- `v2/autopsy/AUTOPSY_KB4_CHANNELS.md` — C2/C3 MACHINERY ceiling, frozen-threat-model scoped; C1-class independent-corroboration recommendation; F2 WRAPS
- `v2/autopsy/SURVIVOR_MECHANISMS.md` — R2-3 withhold-only (cannot admit truths); R2-8 leg-ii load-bearing (13.70pp), extreme conservatism (36/11,630); prereg/implementation mapping discrepancy
- `v2/diagnostics/DIAG_VERDICT_R24_RK3.md` — harness verdict KNOWLEDGE + SPEC-TENSION; knowledge-delivery gap (K2 824/1,102 vs K1 1,062/1,102)

**Sol call log:** the brief was sent as a single condensed prompt (4,532 bytes, ~1,200 prompt tokens), max_tokens 6000. It succeeded on the first try. **Tooling lesson (extends `DEBATES_V2.md` §0):** four earlier drafts of this brief at ~5.3–14 KB (2,030–2,963 prompt tokens) all returned empty completions (`choices: null`, 0 completion tokens) — the same failure mode Round 1 hit twice on its long brief. The working envelope is roughly ≤ ~4.5 KB / ~1,200 prompt tokens. Future Sol rounds: keep briefs inside that envelope; compress findings to headline numbers rather than splitting across calls (Sol has no memory between calls, so splitting does not help).

Raw request/response files: `briefs/ROUND4_brief.txt` (the brief as sent), `briefs/ROUND4_sol_raw.txt` (verbatim reply).

## 1. ROUND 4 — brief fed to Sol (full text as sent)

> Second opinion, structured debate. ROUND 4 (final). No memory of prior calls — self-contained. Plain language, zero RNG.
>
> YOUR PRIOR POSITIONS: R1: five failure modes MACHINERY-FAILURE; disputed generality (12 dead forks = ONE pattern = one data point). R2 ranked: (1) versioned revisable install gate, (2) pure native interventional adjudication, (3) independent evidence escrow with claim-local installation. R3: RETRACTED universal machinery claim, DEMOTED Direction 1; held: (a) frozen intervention registry = enumeration plus actuation, (b) FS-G bars don't provably specify contradiction behavior. Disagreements: (1) knowledge vs machinery; (2) revisable active claim; (3) intervention vs enumeration; (4) FS-G completeness; (5) death-board weight.
>
> FROZEN FINDINGS. A. R2-4 (replay 0/11,840 mismatches): conflict rule consults ONLY jcode; confidence parsed then NEVER used; mrgF/strong/agree unread (no read path). VERDICT: KNOWLEDGE — corroborated-revision replay recovered all 621 withheld correct PASSes, 0 false installs. QUALIFICATION: pointwise adjudication is machinery-impossible — trial 1145 was WRONG yet conf=874, mrgF=10410, strong=1, agree=1, dominating its incumbent (605/2300) on every axis; naive per-trial revision installed it false. Fix must be HISTORICAL. Missing: 621 gate-withheld, 99 suppressed, 278 never reached PASS at sense level. Gate ceiling 824/1,102 = 74.8% < 85% — ARITHMETIC. System HAD the knowledge (96.4%) but 25% never reached the gate's input (DELIVERY gap).
> B. DEATHBOARD: "no detectable signal" FALSE. 9 KNOWLEDGE, 1 MACHINERY (narrow: flat-patch COL-2), 1 UNRECOVERABLE (MOT-1: truth unobservable from pixels), 1 BENCHMARK BUG (CCN-2: 338/340 mislabeled). H2 NOT a safety failure (0/10,000 false). Signals: gl_b>0 PERFECT separator (400/400 false, 0/722 clean; pure-Zag glide_gate prevents 400/400). Texture correlation 0.9989 fooled vs 0.062 true; texcorr_gate rescues 82/95 (86%). R2-5: threshold 15 vs optimal 5.0 (268/720 missed).
> C. KB4 CHANNELS: MACHINERY ceiling, FROZEN-THREAT-MODEL SCOPED. C2: 0.0000 bits. C3: 0.0049 pooled (5x below bar). C1 (independent analytic scout, judge queried EXACTLY once): 0.9968 bits, 15/15, 0.0% false. Four preregistered knowledge augmentations refuted (DPI held on novel transforms; amplitude sweep flat; re-observations -> 0.0000 bits; structured noise). 14/14 NULL. Fool is a fixed point of the perturbation family. v2: C1-class independent-corroboration; never rebuild C2/C3 for the frozen threat model (F2 WRAPS). Limits: C1 pitchdisc-only, 15 fixtures; per-family batteries needed.
> D. SURVIVORS: R2-3 (ALIVE) is WITHHOLD-ONLY — withholding 100% scores 100% on B5; keep as admission harness. R2-8 (DEAD on purity — Python, inadmissible): leg-ii ablation 13.81% -> 0.11% (13.70pp load-bearing); 36/11,630 installs (~0.3%). MAPPING DISCREPANCY: prereg says perturb the independent source; evidence perturbed X. v2's NEW work: admit-path calibration on a new frozen suite with true controls.
>
> TASK — five numbered sections, ~1,500 words max. (a) Accept the 9/1/1/1 split and "no detectable signal" refutation? Accept R2-4 KNOWLEDGE + trial-1145 qualification? Accept C2/C3 ceiling scoped and C1-class? Where did real evidence move you from provisional R1? (b) Does the death-board change your ranking? Does trial-1145 change the adjudicator fork — Direction 1 envisioned per-conflict revision; only HISTORICAL corroboration is safe. Effect on #2? (c) Which disagreements stand, collapse, get new settling experiments? Does the delivery gap change #1's design? (d) STEELMAN that the 9 KNOWLEDGE verdicts are OVERCLAIMED, then evaluate: replay-demonstrated knowledge (Python glue; post-hoc signals never in any preregistered bar's admissible input) != knowledge installable under frozen bars. gl_b/texcorr measured post-hoc; cf1's 0-false recovery is Python glue, not a Zag-verified gate, reaching only 65.8% — below the arithmetically unreachable 85% bar. If "knowledge failure" means "fixable gap" but the fix is not demonstrated under the frozen deploy criterion (pure Zag, frozen battery, bars as written), the label is a promissory note. Does it land? Which of the 9 does it touch, which does it miss? (e) PREREG: (i) 85% RK-3 unreachable — SPEC-CHANGE or sub-bars? (ii) does trial-1145 demand a prereg ban on pointwise revision rules in all v2 gates? (iii) does C2/C3 WRAPS plus your enumeration objection (#3) require a prereg ban on judgment-side acceptance channels for the frozen threat model? Preserve live disagreements as numbered items with both sides stated.

## 2. Sol's reply — VERBATIM

[BEGIN VERBATIM — Sol / gpt-5.6-sol, Round 4]
I’ll treat the supplied findings as the complete record and separate three claims that are easy to conflate: the signal existed, the frozen gate could admit it, and a deployable adjudicator can safely act on it. The final position will preserve the unresolved disagreements rather than collapsing them into a single verdict.1. **What I accept**

I accept the `9 KNOWLEDGE / 1 MACHINERY / 1 UNRECOVERABLE / 1 BENCHMARK BUG` split as the best classification supported by the findings, with one qualification: it is a classification of the demonstrated failure mechanisms, not a universal claim that every analogous failure will have the same cause.

The “no detectable signal” conclusion is refuted. The evidence is too direct to leave that as a live description:

- `gl_b > 0` perfectly separated the tested false cases: 400/400 false and 0/722 clean.
- `texcorr` was highly informative in the relevant comparison and rescued 82/95 cases.
- The C1 analytic scout produced 0.9968 bits, 15/15 correct, and 0% false on its fixtures.
- H2 produced no false positives in 10,000 trials, so it is not a safety failure.

I also accept R2-4 as a **knowledge** result, but only in the historical sense demonstrated by the replay. Corroborated revision recovered all 621 withheld correct PASSes, with 0 false installs over 11,840 replays. That is strong evidence that the system had recoverable information which the original path failed to use.

Trial 1145 prevents a stronger conclusion. The trial was wrong but had `conf=874`, `mrgF=10410`, `strong=1`, and `agree=1`, dominating the incumbent on every available axis. A pointwise rule that revises whenever a new conflict has stronger apparent support would install the wrong answer. The safe result is therefore:

> Historical corroboration can support revision in this tested replay. Per-trial apparent strength cannot safely authorize revision.

I accept the C2/C3 ceiling, but only as scoped to the frozen threat model and tested channel structure. C2 produced zero information and C3 only 0.0049 pooled bits, below the bar. The four preregistered augmentations did not change that result. C1 supports an independent-corroboration class, not a universal claim that all useful interventions have been exhausted. Its evidence is limited to pitch discrimination, 15 fixtures, and one exact judge query per fixture.

The real movement from R1 is therefore not simply “machinery was wrong.” It is a sharper division:

- R1 overgeneralized from a small set of dead forks into a universal machinery-failure claim.
- The death-board now shows many failures were knowledge or delivery failures.
- R2-4 shows that historical use of latent evidence can work.
- Trial 1145 shows that active installation remains a separate safety problem.
- C1 shows that independent analytic evidence can be real and useful, while C2/C3 show that many proposed channels genuinely add nothing under the frozen threat model.

2. **Ranking and the adjudicator fork**

The death-board changes the ranking’s interpretation more than its order.

My revised ranking is:

1. **A revisable admission or install gate, redesigned around delivery and historical corroboration.**
2. **Native interventional adjudication, but only with preregistered channel semantics and explicit contradiction handling.**
3. **Evidence escrow with claim-local installation.**

The first position remains because the largest quantified deficit is delivery. The system had relevant knowledge in 96.4% of the cases, but only 74.8% reached the gate input. That is not a marginal tuning issue. A quarter of the available cases were lost before the gate could act. The gate must therefore be designed as an admission and coverage system, not merely a confidence threshold.

However, “revisable” must no longer mean “replace the incumbent when this trial looks stronger.” The safe design is historical:

- retain prior observations and adjudications;
- require corroboration across time, source, or independently generated evidence;
- make revision an episode-level or claim-level decision;
- prohibit a single current conflict from installing a new answer solely because its local score is higher.

That moves some of the burden toward #2. Native interventional adjudication is more important when a claim cannot be safely revised from local evidence. But it does not rescue an underspecified pointwise rule. An intervention can produce a highly persuasive wrong result, as trial 1145 demonstrates, unless its provenance, independence, temporal relationship, and contradiction behavior are defined.

The finding does not eliminate escrow. Escrow remains useful when evidence should be preserved without immediately changing a live claim. But it is weaker as a primary solution to the delivery gap: evidence that is never admitted, surfaced, or adjudicated remains operationally unavailable.

3. **Disagreements that remain**

**1. Knowledge versus machinery**

The old universal machinery claim collapses. The remaining disagreement is whether “knowledge failure” should describe recoverable information that the frozen system cannot install. Both sides are now partly right:

- One side says the replay establishes knowledge because the correct answer was recoverable from existing evidence.
- The other says deployable knowledge must be usable by the admissible system, not merely by post-hoc analysis.

The settling experiment is an end-to-end frozen-gate test using only preregistered inputs, with no Python-only signal extraction and no post-hoc judge features.

**2. Revisable active claims**

Pointwise revision as a general rule is rejected by trial 1145. Historical corroboration remains live. The disagreement is whether historical corroboration is a sufficiently specified mechanism or only a replay success.

The settling experiment is a preregistered sequential protocol with explicit history windows, contradiction cases, delayed evidence, repeated false corroboration, and a no-install rule for isolated high-scoring conflicts. The primary metric must include false installations, not only recovered correct installs.

**3. Intervention versus enumeration**

This disagreement stands. C1 proves that one independent analytic channel can help. C2/C3 do not prove that the intervention space is exhausted. Conversely, the existence of one successful channel does not establish an unbounded intervention program.

The settling experiment is a finite registry: list every permitted intervention family, define what counts as independent, and test each family against controls and transforms. Claims should then be limited to the registered families. “We found one useful scout” and “we have enumerated the useful channels” are different claims.

**4. FS-G completeness**

This also stands. FS-G bars do not, by themselves, specify what happens when evidence conflicts, when a corroborator is wrong, or when a stronger signal contradicts an incumbent. Trial 1145 is a concrete demonstration of the gap.

The settling experiment is a contradiction matrix covering incumbent/new-answer conflicts, confidence reversals, correlated corroborators, missing history, and ties. Each cell needs a preregistered outcome.

**5. Death-board weight**

The “no detectable signal” conclusion collapses. The remaining disagreement concerns how much weight the board should place on replay recoverability versus frozen deployability.

The board should carry both labels where needed: **recoverable signal**, **admissible under frozen gate**, and **safe to install**. A single label hides the difference between these states.

4. **The overclaim case**

The steelman is strong. The nine verdicts may be overclaimed if “knowledge failure” means “the frozen deployment could have fixed this.” The replay used Python glue, and the successful features were discovered or evaluated after the original preregistered bars were fixed. `gl_b` and `texcorr` were not admissible inputs to the Zag-verified gate. The `cf1` recovery reached only 65.8%, below the 85% criterion. Since the current 85% RK-3 path is arithmetically capped at 74.8%, the system cannot meet that bar without changing either the inputs, the gate, or the metric.

On that definition, “knowledge failure” is indeed a promissory note. It means: “there appears to be recoverable information, and a future redesign might install it.” That is weaker than demonstrated deployability.

The criticism lands against the **operational strength** of all nine knowledge verdicts, unless a particular verdict was independently reproduced through its frozen admissible path. It does not necessarily overturn their causal diagnosis. A case can still be correctly diagnosed as knowledge-limited rather than machinery-limited even though the proposed repair has not been demonstrated under deployment rules.

It does not touch the separate classifications in the same way:

- It does not turn MOT-1 into knowledge merely because a post-hoc feature exists; truth unobservable from pixels remains unrecoverable.
- It does not alter CCN-2, which remains a benchmark-label bug.
- It does not erase the narrow COL-2 machinery finding.
- It does not weaken the scoped C1 result, but it does prevent treating C1 as a general frozen-gate deployment result.

So I would revise the terminology to avoid overclaiming:

> Nine cases had replay-recoverable or externally demonstrated signal, but frozen-gate installation was not established.

That wording preserves the evidence without calling an unimplemented repair a solved failure.

5. **Preregistration consequences**

**(i) The 85% RK-3 requirement**

As written, the bar is unreachable because the gate ceiling is 824/1,102, or 74.8%. This requires a **spec change**, not merely sub-bars. Sub-bars may diagnose where the loss occurs, but they cannot make an unreachable aggregate target valid.

The revised preregistration should state whether 85% is:

- a deployment requirement after adding admissible channels;
- a conditional rate over cases reaching the gate;
- or a benchmark target that is explicitly impossible under the current input path.

The denominator, admission population, and treatment of withheld or never-reached cases must be fixed before further scoring.

**(ii) Pointwise revision**

Yes: v2 gates should ban pointwise revision rules that install a new claim solely because one current conflict has higher confidence, margin, or agreement. The ban should apply to every gate that changes a live claim.

That does not require banning all revision. Historical corroboration, claim-local escrow, and preregistered multi-observation adjudication can remain allowed if their temporal and contradiction rules are explicit.

**(iii) Judgment-side acceptance channels**

For the frozen threat model, unregistered judgment-side acceptance channels should be banned. C2/C3 wrapping means that merely asking the same judgment mechanism through another acceptance path does not count as independent evidence.

I would not ban every independent analytic scout. C1 shows why: an explicitly registered, independently computed channel can provide real information. But it must be enumerated, preregistered, independently validated, and counted as an acceptance channel with its own false-installation budget. The live disagreement is therefore:

- **Strict view:** freeze the threat model and ban all new judgment-side acceptance paths.
- **Permissive but controlled view:** ban unregistered judgment-side paths, while allowing registered independent analytic channels.

The second is the more useful rule, provided “independent,” “registered,” and “acceptance” are defined before testing.

[END VERBATIM — Sol / gpt-5.6-sol, Round 4]

## 3. Moderation notes (Round 4)

**What Sol moved on.** (1) Accepts the 9/1/1/1 death-board split — but qualified as "a classification of the demonstrated failure mechanisms, not a universal claim that every analogous failure will have the same cause." (2) Accepts the "no detectable signal" refutation outright, citing gl_b (400/400), texcorr (82/95), C1 (0.9968 bits), and H2 (0/10,000). (3) Accepts R2-4 as KNOWLEDGE — "but only in the historical sense demonstrated by the replay." (4) Accepts the trial-1145 qualification verbatim: "Historical corroboration can support revision in this tested replay. Per-trial apparent strength cannot safely authorize revision." (5) Accepts the C2/C3 machinery ceiling as frozen-threat-model scoped, and the C1-class recommendation — restating C1's limits (pitchdisc-only, 15 fixtures, one judge query) unprompted. (6) Concedes the overclaim steelman **lands on operational strength**: "Nine cases had replay-recoverable or externally demonstrated signal, but frozen-gate installation was not established" — while holding that it does NOT overturn the causal diagnoses (knowledge-limited vs machinery-limited) and does not touch MOT-1, CCN-2, COL-2, or C1's separate classifications.

**The ranking flip.** Sol's Round 3 ranking had Direction 3 (escrow) as least-contested #1 and Direction 1 demoted. Round 4 inverts this: **(1) revisable admission/install gate redesigned around delivery and historical corroboration, (2) native interventional adjudication with preregistered channel semantics + explicit contradiction handling, (3) evidence escrow with claim-local installation.** Direction 1 returns — but it is not the same Direction 1 Sol demoted in R3: "revisable" no longer means per-conflict revision (which trial 1145 kills); it means a gate designed as an *admission and coverage system* (the delivery gap: 96.4% knowledge present, 74.8% reaching the gate input) with *historical corroboration* as the only revision path. Direction 3 is demoted because "evidence that is never admitted, surfaced, or adjudicated remains operationally unavailable" — escrow preserves but does not deliver.

**Sol's new analytic contribution.** The three-way split — (i) the signal existed, (ii) the frozen gate could admit it, (iii) a deployable adjudicator can safely act on it — maps exactly onto the autopsy/harness structure (K1 program knowledge / K2 delivery / cf2 surface-patch-blocked) and is the cleanest framing of the (d) concession. Its prescription — the board should carry three labels per case (**recoverable signal** / **admissible under frozen gate** / **safe to install**) — is directly actionable as a documentation change.

**Flagged tension.** Sol's new #1 partially reopens disagreement #2 in a new form: "explicit temporal and contradiction rules" is now doing the work that "revision authority" did in Round 3. The contradiction-matrix experiment (disagreement #4's revised settling experiment) should run before this gate is built, or v2 repeats the R2-4 mistake of unspecified contradiction behavior.

**What Sol did not address.** (1) It did not say whether the delivery gap changes disagreement #1's *factorial* design — it replaced the experiment with an end-to-end frozen-gate test instead. Moderator: keep both; the factorial should add the delivery path (K1→K2) as an explicit factor. (2) It did not take up the R2-8 prereg/implementation mapping discrepancy — still open, see §6 recommendation 4.

**No false consensus.** Sol preserved all five disagreements as live items (reframed, not collapsed) and explicitly separated "recoverable signal" from "demonstrated deployability" — the round's anti-false-consensus output.

## 4. Preserved disagreements (updated, no false consensus)

| # | Issue | Muse-side (crews, frozen debates + autopsies) | Sol (Round 4 final) | Settling experiment (revised) |
|---|---|---|---|---|
| 1 | Knowledge vs machinery | Replay recoverability establishes the knowledge diagnosis: the correct answer was recoverable from existing evidence; the fix is rule-addition + program-teaching (AUTOPSY_R2-4 §2.2, §4) | The universal machinery claim collapses, but "knowledge failure" should not describe recoverable-but-not-installable information. "Both sides are now partly right": deployable knowledge must be usable by the admissible system, not merely by post-hoc analysis | End-to-end frozen-gate test using ONLY preregistered inputs — no Python-only signal extraction, no post-hoc judge features (Sol's revision). Moderator: retain the factorial too, with the K1→K2 delivery path as an explicit factor |
| 2 | Revisable active claim | Pointwise revision was never defended (the crew's own autopsy disqualifies it via trial 1145); cf1 shows the historical-corroboration rule shape — needs Zag verification | Pointwise revision as a general rule is rejected by trial 1145. Historical corroboration remains live but is it a sufficiently specified mechanism or only a replay success? | Preregistered sequential protocol: explicit history windows, contradiction cases, delayed evidence, repeated false corroboration, no-install rule for isolated high-scoring conflicts; primary metric INCLUDES false installations, not only recovered correct installs |
| 3 | Intervention vs enumeration | Native intervention is principled adjudication if the registry is frozen before evidence is observed | STANDS, reframed: one useful scout (C1) ≠ an enumerated channel space. A fixed registry is enumerable; claims must be limited to registered families | Finite registry: list every permitted intervention family, define "independent," test each family against controls and transforms; "we found one useful scout" and "we have enumerated the useful channels" are different claims |
| 4 | FS-G completeness | Admission + discrimination + ablation + H2's external-prediction count fully specify safe installation | STANDS: bars don't specify contradiction behavior; trial 1145 is a concrete demonstration of the gap | Contradiction matrix: incumbent/new-answer conflicts, confidence reversals, correlated corroborators, missing history, ties — each cell preregistered. Formal; cheapest of the four — run first |
| 5 | Death-board weight | 12 kills as causal-diagnosis data points (now 9 KNOWLEDGE diagnoses) | The "no detectable signal" conclusion collapses; remaining question is weight on replay recoverability vs frozen deployability | Resolved by labeling, not experiment: board carries three labels per case — recoverable signal / admissible under frozen gate / safe to install. Parent decides which label the v2 bars target |

## 5. Ranked v2 directions (post-Round 4)

**Rank 1 — Revisable admission/install gate redesigned around delivery and historical corroboration** (Sol's new #1; ex-Direction 1, resurrected with new semantics). Mechanism: the gate is designed as an admission-and-coverage system attacking the delivery gap (K2: 25% of correct-highconf knowledge never reached the gate's input); the ONLY revision path is historical corroboration (cf1-class: corroborated second observation within tolerance, episode/claim-level decision); pointwise revision rules are banned by prereg. Biggest risk: "explicit temporal and contradiction rules" becomes the new untestable homunculus (reopened disagreement #2) — answered by running the contradiction-matrix experiment before building. Kill experiment: end-to-end frozen-gate test on preregistered inputs only; dies on >0 false installs, on any need for a pointwise-revision rule, or if delivery-gap closure doesn't move installs.

**Rank 2 — Pure native interventional adjudication with preregistered channel semantics and explicit contradiction handling** (Sol #2, rank unchanged). R2-8's numbers remain inadmissible (Python); any v2 interventional leg is pure Zag from birth with a machine-checkable purity audit per intervention. Sol's retained warning now has a concrete form: the finite intervention registry must be published and each family tested — disagreement #3's revised experiment is in the prereg or the direction replays R2-2's novel-family death with actuators.

**Rank 3 — Independent evidence escrow with claim-local installation** (Sol #3, demoted from Round-3 #1). Still the most conservative (no semantic revision of permanence, M1-safe), but demoted because escrow preserves evidence without delivering it — it does not close the K1→K2 delivery gap that is now the largest quantified deficit. Kill experiment unchanged: 1,200 held-out tasks with shared-cause traps; dies on >0/1,200 false active permanent installs, <85% correct installs, or <5× ablation effect.

**Consensus components (unchanged):** R2-37 union (R2-3 admission instrument + R2-7 discriminative challenge runner) as the admission front end — Sol agrees as component, still disputes sufficiency (disagreement #4). C1-class independent-corroboration as the recommended acceptance-channel architecture: registered, per-family preregistered batteries (G1), own false-installation budget — per Sol's (e)(iii) permissive-but-controlled rule.

**Not ranked — new self-flagging forks.** Debate D Front (b) ruling stands unchanged.

## 6. Recommendations to the parent

1. **Terminology fix (Sol's (d) concession — documentation only, no experiment needed):** relabel the death-board's 9 KNOWLEDGE verdicts. Adopt Sol's three labels per case — **recoverable signal** / **admissible under frozen gate** / **safe to install**. The causal diagnoses (knowledge-limited vs machinery-limited) survive; the "fixable under frozen rules" implication is withdrawn until demonstrated. This is the round's most immediately applicable output.
2. **Prereg-level decisions (all need Micah's re-approval per standing law):**
   - (a) **RK-3 85%: SPEC-CHANGE, not sub-bars.** Sol: "Sub-bars may diagnose where the loss occurs, but they cannot make an unreachable aggregate target valid." The revised prereg must state whether 85% is a deployment requirement after adding admissible channels, a conditional rate over cases reaching the gate, or an explicitly impossible benchmark target — and must fix the denominator, the admission population, and the treatment of never-reached/withheld cases before further scoring.
   - (b) **Ban pointwise revision rules in every v2 gate that changes a live claim** (the trial-1145 rule). Historical corroboration, claim-local escrow, and preregistered multi-observation adjudication remain allowed ONLY with explicit temporal and contradiction rules.
   - (c) **Ban unregistered judgment-side acceptance channels for the frozen threat model** (C2/C3 WRAPS + Sol's enumeration objection); allow registered independent analytic channels (C1-class) with their own false-installation budgets — Sol's "permissive but controlled" view. Note: this is a prereg ban the crew's F2 verdict already implies; Sol's framing makes the registered/unregistered distinction the load-bearing line.
3. **Run the settling experiments in this order:** contradiction matrix (#4 — formal, cheapest) → sequential historical-corroboration protocol (#2) → finite intervention registry (#3) → end-to-end frozen-gate test on preregistered inputs (#1). Do not build the Rank-1 revisable gate before #4 resolves, or v2 rebuilds R2-4's unspecified-contradiction-behavior.
4. **R2-8 mapping discrepancy still unresolved** (Sol didn't take it up): v2 must freeze one perturbation mapping (prereg says perturb the independent source; measured evidence perturbed X), run both in the calibration battery, and report the delta — before any interventional leg is frozen.
5. **Delivery gap is now the top-ranked v2 attack surface** (Sol's ranking flip rationale): 96.4% knowledge present at the program level, 74.8% reaching the gate input. Any v2 direction that cannot name its delivery-path mechanism (how K1 knowledge becomes K2 gate input) is not addressing the largest quantified deficit.

## Appendix — files

- `briefs/ROUND4_brief.txt` — the brief as sent (condensed; 4,532 bytes / ~1,200 prompt tokens)
- `briefs/ROUND4_sol_raw.txt` — Sol's verbatim reply (11,660 bytes, 5 sections)
- Tooling note: four prompt drafts at ~5.3–14 KB (2,030–2,963 prompt tokens) returned empty completions (`choices: null`, 0 completion tokens); the ~4.5 KB draft succeeded first try. Keep future Sol briefs ≤ ~4.5 KB / ~1,200 prompt tokens.

*Laws observed: debate infrastructure only — no mechanisms built, no code written; zero RNG in any decision path; all numbers copied from the frozen autopsies (AUTOPSY_R2-4, AUTOPSY_DEATHBOARD, AUTOPSY_KB4_CHANNELS, SURVIVOR_MECHANISMS, DIAG_VERDICT_R24_RK3); Sol's reply is verbatim including its own formatting.*
