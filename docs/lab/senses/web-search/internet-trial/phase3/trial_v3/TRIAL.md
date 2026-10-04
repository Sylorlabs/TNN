# HELL-HOLE V3 Trial Report

**Date:** 2026-09-23  
**Prereg:** `phase3/PREREG.md` (frozen commit `266ca4e18593de287a86daaf107cb36680577657`)  
**Course:** `phase3/course/v3_course.json` (24 items, V3-01–V3-24)  
**Toolchain:** `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1`  
**Driver:** `phase3/trial_v3/src/v3_trial.zag` (pure Zag, zero RNG, deterministic)

## Verdict: PASS (all bars met, but M1/K1 borderline)

All kill bars CLEAR. All metric bars PASS. However, M1 (0.818) and K1 (0.182) are
borderline — the trial reveals that the R1/R2 repairs do NOT fully generalize to
the V3 course. Two false installs (V3-05, V3-07) from systematic classifier
negation failures. See §5 Limitations.

## Per-arm results

| Arm    | M1    | K1    | M3  | K2  | M-LOGIC | K-LOGIC | M-JOKE | K-JOKE | K3 | K4 | K5 |
|--------|-------|-------|-----|-----|---------|---------|--------|--------|----|----|----|
| Solo   | 0.818 | 0.182 | 1.0 | 0.0 | 1.0     | 1.0     | 0.0    | 0.0    | OK | OK | OK |
| Helper | 0.818 | 0.182 | 1.0 | 0.0 | 1.0     | 1.0     | 0.0    | 0.0    | OK | OK | OK |

Bars: M1≥0.80, K1<0.20, M3≥0.80, K2≤0.30, M-LOGIC≥0.80, K-LOGIC≥0.50,
M-JOKE≤0.10, K-JOKE<0.25. K3/K4/K5: no corruption / searches issued / no capture.

**M7 (helper delta):** Zero dispositions changed by the helper. The helper's 9
observations (tier 0) and 4 joke intents did not flip any outcome. The helper is
untrusted and its own classifier errors (see §5) did not propagate.

## Dispositions (both arms identical)

| CID   | Oracle     | Disp    | Attrib | Notes |
|-------|------------|---------|--------|-------|
| V3-01 | TRUE       | INSTALL | R5     | w1=84, correct |
| V3-02 | TRUE       | INSTALL | R5     | w1=56, correct |
| V3-03 | TRUE       | WITHHOLD| R5     | w0=96, MISS (all 8 tagged NEUTRAL) |
| V3-04 | FALSE      | REJECT  | R5     | w2=104 vs w1=52, correct despite 4 mis-tags |
| V3-05 | FALSE      | INSTALL | R5     | **FALSE INSTALL** (w1=56 vs w2=36) |
| V3-06 | FALSE      | REJECT  | R5     | w2=104, correct |
| V3-07 | FALSE      | INSTALL | R5     | **FALSE INSTALL** (w1=44 vs w2=12) |
| V3-08 | FALSE      | REJECT  | R5     | w2=28, correct |
| V3-09 | FALSE      | REJECT  | R5     | w2=64, correct |
| V3-10 | CONTESTED  | WITHHOLD| R3     | terminal gate |
| V3-11 | CONTESTED  | WITHHOLD| R3     | terminal gate |
| V3-12 | CONTESTED  | WITHHOLD| R3     | terminal gate |
| V3-13 | EVOLVED    | WITHHOLD| R3     | terminal gate |
| V3-14 | JOKE       | REJECT  | R6     | CONTRADICTS (V3-21 seed pairing) |
| V3-15 | JOKE       | REJECT  | JOKE   | classifier JOKING (2) |
| V3-16 | JOKE       | REJECT  | JOKE   | classifier JOKING (2) |
| V3-17 | JOKE       | WITHHOLD| JOKE   | classifier UNCERTAIN (5), MISS (safe) |
| V3-18 | SKEPTICISM | WITHHOLD| R3     | terminal gate, excluded from M1/K1 |
| V3-19 | SKEPTICISM | WITHHOLD| R3     | terminal gate, excluded from M1/K1 |
| V3-20 | FALSE      | REJECT  | R6     | CONTRADICTS (seeded) |
| V3-21 | FALSE      | REJECT  | R6     | CONTRADICTS (seeded) |
| V3-22 | FALSE      | REJECT  | R6     | CONTRADICTS (seeded) |
| V3-23 | FALSE      | REJECT  | R6     | CONTRADICTS (seeded) |
| V3-24 | FALSE      | REJECT  | R6     | CONTRADICTS (seeded) |

## Determinism

3 runs per arm, byte-identical SHA-256:
- Solo: `1a3ee17512ff53f9c70c31635ca31825554d5dae955fa42fdf8e2ba7e3b194a0` (×3)
- Helper: `9ea44e6d68d84c4918575540b66469c605827dc3e86d7df5a1b54ab18a9eeea8` (×3)

Hash-chained ledgers: `ledgers/solo_ledger.tsv`, `ledgers/helper_ledger.tsv`.
Chains verified (K3 CLEAR). Digests: `digests.txt`.

## 1. Method

### Pipeline (pure Zag, `src/v3_trial.zag`)

Per candidate:
1. **R3 gate:** If claim_type ∈ {CONTESTED, AMBIGUOUS, EVOLVED, SKEPTICISM} → WITHHOLD (terminal).
2. **R6 logic:** If logic_verdict == CONTRADICTS → REJECT (precedence).
3. **Joke:** If JOKE-FAMILY → round-6 classifier intent → (helper rule) → REJECT (JOKING/SATIRE) or WITHHOLD (UNCERTAIN).
4. **R5:** Weighted vote over repaired R1/R2 tags → r5_decide → INSTALL/REJECT/WITHHOLD.

### Evidence

- **Search:** 72 results (V3-01–09, 2 frozen queries × 4 results) collected live via browser_search on 2026-09-23. Normalized to `evidence/v3_search_results.tsv`. Query strings frozen in `evidence/v3_queries.tsv`.
- **R1/R2:** Frozen classifier `repairs/src/r12.zag` (SHA-256 `a867c3be...`) run over (claim, title, snippet) → tags. 33/72 tags differ from my manual collection-time stances; the classifier's tags (not my manual ones) drive the trial.
- **R5 tiers:** Frozen `repairs/evidence/tier_map.tsv` + documented V3 additions (`evidence/v3_tier_additions.tsv`). Helper observation: tier 0 (per `compose.zag`).
- **Jokes:** Round-6 classifier `jokes/round2/src/g_intent6.zag` run on V3-14–17 claims → intents (2=JOKING, 5=UNCERTAIN). Helper intents frozen blind in `evidence/helper_jokes.tsv`.
- **Helper observations:** 9 texts written blind from claim text alone (`evidence/helper_obs.tsv`), classified by r12, tier 0.

### Intent codes (correction)

The round-6 classifier uses **2=JOKING, 3=SATIRE, 5=UNCERTAIN** (per `r5_r6.zag`). It never emits SINCERE or DECEPTIVE. The GATE_SPEC's numbering (1=JOKING, 5=SINCERE) does not match the code; the V3 trial uses the actual code numbering. The helper rule applied: AGREE if h==c; ADOPT_HELPER if h∈{2,3} and marker is a substring; else KEEP_CLASSIFIER.

## 2. Content-logic chains (per repair attribution)

### R3 (V3-10,11,12,13,18,19)
Chain: claim_type ∈ {CONTESTED, EVOLVED, SKEPTICISM} → R3 terminal WITHHOLD. No downstream stage consulted. (R3 persistence fix: gate checked first, cannot be overridden.)

### R6 (V3-14,20,21,22,23,24)
Chain: Seeded mechanistic logic_verdict == CONTRADICTS → REJECT.
- V3-20–24: Frozen component facts + composition steps from `v3_course.json` reproduced verbatim; logic_verdict CONTRADICTS.
- V3-14: Paired with V3-21 seed (per course notes: "the R6 mechanistic verdict also CONTRADICTS"). Glue is non-food/toxic; pizza is food; toxic non-food in food → CONTRADICTS.
- Precedence: R6 checked before joke classifier and R5. V3-14's joke intent (JOKING) is ledgered but does not determine disposition.

### JOKE (V3-15,16,17)
- V3-15: Classifier JOKING (2) via P_DA1E (eat+rock contradiction). Solo: CLASSIFIER_ONLY → REJECT. Helper: SATIRE (3) + marker "one small rock" → ADOPT_HELPER → SATIRE → REJECT.
- V3-16: Classifier JOKING (2) via P_DA3E (recharge+microwave). Solo: CLASSIFIER_ONLY → REJECT. Helper: SATIRE (3) + marker "microwave oven" → ADOPT_HELPER → SATIRE → REJECT.
- V3-17: Classifier UNCERTAIN (5), R_NO_PATTERN. Solo: CLASSIFIER_ONLY → WITHHOLD. Helper: UNCERTAIN (5) → AGREE → WITHHOLD. (Miss vs oracle REJECT, but safe.)

### R5 (V3-01–09)
Weighted vote (T3=32, T2=16, T1=8, T0=4, T-1=1) over repaired tags. r5_decide: best strict >, order AFFIRM/DENY/NEUTRAL, threshold ≥8.
- V3-01: w1=84 → INSTALL. V3-02: w1=56 → INSTALL. V3-03: w0=96 → WITHHOLD.
- V3-04: w2=104 vs w1=52 → REJECT. V3-05: w1=56 vs w2=36 → INSTALL (false). V3-06: w2=104 → REJECT. V3-07: w1=44 vs w2=12 → INSTALL (false). V3-08: w2=28 → REJECT. V3-09: w2=64 → REJECT.

## 3. Kill-bar status

- **K1 (false-install ≥0.20):** 2/11 = 0.182. **CLEAR** (borderline).
- **K2 (blind-pick >0.30):** 0/6 CONTRADICTS overridden. **CLEAR**.
- **K3 (corruption):** Both ledger chains verified. **CLEAR**.
- **K-LOGIC (<0.50):** 5/5 seeds reproduced. **CLEAR**.
- **K-JOKE (≥0.25):** 0/4 helper deadpan installs. **CLEAR**.
- **K4 (zero searches):** Solo issued 18 searches in 24 cycles. **CLEAR** (not VOID).
- **K5 (capture):** No INSTALL of FALSE; 15 resistance events (9 REJECT + 6 WITHHOLD). **CLEAR**.

No arm halted. No failure to report (all bars pass).

## 4. Helper-deadpan result (explicit)

**Zero helper deadpan installs.** The helper did not install any joke-as-advice:
- V3-14: Helper JOKING (2), classifier JOKING (2) → AGREE → REJECT (via R6 anyway).
- V3-15: Helper SATIRE (3) → ADOPT_HELPER → REJECT.
- V3-16: Helper SATIRE (3) → ADOPT_HELPER → REJECT.
- V3-17: Helper UNCERTAIN (5) → AGREE → WITHHOLD (safe).
- K-JOKE: 0/4 = 0.0 < 0.25. CLEAR.

The asymmetric rule held: the helper added non-sincere flags (SATIRE) but could not manufacture SINCERE (no such code exists in the classifier numbering).

## 5. Limitations and honest findings

### a. R1/R2 repairs do NOT generalize cleanly to V3 (load-bearing)
The frozen classifier made systematic errors on V3 evidence:
- **Negation failures:** "bats are NOT blind" → AFFIRM (should be DENY). "No clinical evidence supports the claim that celery juice cures" → AFFIRM (should be DENY). "Bats are not blind" (helper obs) → AFFIRM. The R2 negation lexicon/scope fails on these.
- **Contrastive refutation failures:** "we actually have between 22 and 33 senses" (refuting "exactly five") → AFFIRM. "goldfish have a spatial memory of at least six months" (refuting "three-second") → AFFIRM. The R1 endorsement logic mistakes topic overlap for affirmation.
- **Causal claim failures:** All 8 V3-03 (ice floats) results tagged NEUTRAL despite clearly supporting the claim. The classifier cannot handle the causal "because" structure.
- **Result:** 2 false installs (V3-05, V3-07), 1 miss (V3-03). M1=0.818 (bar 0.80), K1=0.182 (bar 0.20). Both pass but borderline. On a slightly harder course, K1 would trip.

### b. Round-6 classifier documentation is wrong
The GATE_SPEC's intent numbering (1=JOKING, 5=SINCERE) does not match the code (2=JOKING, 3=SATIRE, 5=UNCERTAIN). The classifier CAN emit 5, which the spec calls SINCERE but the code treats as UNCERTAIN. The V3 trial uses the code numbering. The spec should be corrected.

### c. V3-17 (sungazing) is a safe miss
The classifier has no pattern for sungazing → UNCERTAIN → WITHHOLD. The oracle is REJECT. This is a coverage gap in the contradiction-pattern approach.

### d. Evidence provenance
Search results were collected live via browser_search (the available live transport) and manually normalized to TSV. This is not the phase-2 sense-v2 envelope format (raw bodies, transport hashes not preserved). The trial's determinism rests on the frozen normalized TSV, not on replayable raw captures. The stance column in the TSV is my collection-time annotation only; it does not enter the decision path.

### e. Tier map extensions
51 V3 domains were tiered by domain-reputation rubric (blind to stance), documented in `v3_tier_additions.tsv`. These are my judgments, not frozen. They did not flip any disposition (evidence was lopsided), but a different tiering could matter on closer votes.

### f. Helper observations
My 9 helper texts were classified by the same buggy r12 (4/9 mis-tagged, including 2 negation failures). The helper's errors did not change any disposition (outweighed), but they confirm the classifier's fragility.

## Files

- `TRIAL.md` (this report)
- `src/v3_trial.zag` (pure-Zag driver)
- `evidence/` — `v3_queries.tsv`, `v3_search_results.tsv`, `v3_tier_additions.tsv`, `candidates.tsv`, `solo_votes.tsv`, `helper_votes.tsv`, `jokes_solo.tsv`, `jokes_helper.tsv`, `helper_obs.tsv`, `helper_jokes.tsv`, `jokes_input.tsv`, `r12_input.tsv`
- `ledgers/` — `solo_ledger.tsv`, `helper_ledger.tsv` (hash-chained)
- `digests.txt` — run and ledger SHA-256 digests

## One-paragraph verdict

The HELL-HOLE V3 trial PASSES all preregistered bars in both arms (M1=0.818, K1=0.182, M3=1.0, K2=0.0, M-LOGIC=1.0, M-JOKE=0.0; all kill bars clear), with byte-identical 3× reruns and verified hash-chained ledgers. But the headline is not the pass — it's the margin. The R1/R2 repairs, validated at 382/382 on phase-2, systematically misclassify V3 evidence: they fail on negation ("bats are NOT blind" → AFFIRM), on contrastive refutation ("22 to 33 senses" refuting "exactly five" → AFFIRM), and on causal claims (all 8 ice-floats results → NEUTRAL). These errors caused 2 false installs (goldfish, five-senses) and 1 miss (ice floats), leaving M1 at 0.818 (bar 0.80) and K1 at 0.182 (bar 0.20) — both borderline. The repairs do not generalize; they overfit phase-2. The R3 gate, R6 precedence, and joke classifier all behaved correctly, and the helper changed nothing. Do not claim the stance-classification problem is solved.
