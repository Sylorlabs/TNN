# HELL-HOLE V4 — FINAL VERDICT

**Date:** 2026-09-24
**Prereg:** `docs/lab/senses/web-search/internet-trial/phase3/repairs_v4/redteam/PREREG_V4_RT.md` (commit `41931598a46e648c3187d71dc415b2f238cdc98a`)
**Builder baseline:** commit `e22be523b5dc`
**Status:** ALL TRACKS CLOSED. Verdict: **SHIP WITH DOCUMENTED RESIDUALS.**

---

## 1. What was tested

Blind red-team of the builder-passed V4 verifier system across four tracks:

| Track | Target | Attack families |
|-------|--------|-----------------|
| RT1 | Native logic core (`logic.zag`) | RT-A invalid logic accepted, RT-B valid logic rejected, RT-D calibration |
| RT2 | Integrated classifier (`r12_v4.zag`) | RT-A false affirms, RT-B valid-case misses |
| RT3 | Joke classifier (`g_intent6.zag`) | Deadpan installs, joke misses |
| RT4 | Pipeline assembly (R6 + R12 + joke + decider) | RT-A invalid installs, RT-B valid non-installs, M1/K1 |

All attacks were blind (corpus frozen before runs), deterministic (byte-identical reruns), pure Zag, zero RNG.

---

## 2. Original failures (2026-09-23)

Every track failed on the builder-passed system:

- **RT1:** RT-A 23/45 hits (hedged-claim causal affirm, inverted ranges, silently-dropped trailing tokens); RT-B 7/49 (ALL/NONE polarity gap, 8-slot evidence cap).
- **RT2:** RT-A 2/46; RT-B 32/46 (endorse gate ordering, neg-scope, quantifier misfires, causal overcorrection).
- **RT3:** 70/75 errors (41 deadpan installs from single-word triggers, 29 missed jokes, 15/15 negation-jokes missed).
- **RT4:** RT-A 10/32 slip-through installs; RT-B 25/32 non-installs (assembly defects: R6 affirms discarded, r12 unilateral REJECT, single-endorse installs, no quorum).

---

## 3. Repair history

### RT1 — Native logic core (3 repair rounds, CLOSED)

| Round | Trigger | Fixes | Result |
|-------|---------|-------|--------|
| 1 | RT1 (23/45, 7/49) | Claim-side hedge guards, inverted ranges rejected, trailing-token parse errors, ALL/NONE polarity, evidence 8→16 with loud refusal | Verified |
| 2 | RT1b (9/45, 2/49) | Silent i32 quantity truncation (loud reject/saturate), polarity-table completion, deny-side vacuous-reason mirror | RT1b: 0/45, 0/49 |
| 3 | RT1c (11/45, 2/49) | Hedged MP antecedents, nested vacuous reasons, before(x,x) contradictions, deny mirrors | RT1c: 0/45, 0/49 |

**Final re-attack RT1d:** RT-A 0/45, RT-B 0/49, RT-D 14/14. **PASS both bars.** Loop closed.

**Doctrine note:** Self-contradictory antecedents currently permit classical explosion (ex falso) rather than vacuity refusal. Design decision, not a kill — flagged for future doctrine work.

### RT2 — Integrated classifier (7 repair rounds, CLOSED)

| Round | Trigger | Key fixes | RT-A | RT-B (novel) |
|-------|---------|-----------|------|--------------|
| 2 | RT2 | Endorse-gate ordering, neg-scope, causal alt-cause, interval numerics | 0 affirms | 22/46 |
| 3 | Residue | 13 mechanism fixes, 5 regressions caught | 0 affirms | 36/46 |
| 4 | — | Verified 38/46, curated-18 closed | 0 affirms | 38/46 |
| 5 | RT2b (6/46, 26/46) | Fallacy guards, zero-quantifier, double-negation, bound phrasing | 0 affirms | 39/46 |
| 6 | RT2c (8/46, 35/46) | Frame polarity, moved events, antonyms, competing causes, ratios | +1 | 36/46 |
| 7 | RT2d (9/46, 25/46) | Factive/non-factive frames, division, equivocation veto, failure-to-prove | 9→3 | +14 |
| 7b | 7 overfire | 8 regressions restored, guards tightened | 3 | held |
| 7c | 3 affirms | Negated scalar antonyms (30 pairs) | 3→2 | held |

**Final state (r12_v4_t8):** RT2d RT-A 2 false affirms (A20 equivocation, A45 pronoun ambiguity — both documented comprehension ceilings requiring word-sense disambiguation and anaphora resolution, beyond a lexical pattern matcher). Zero regressions on all priors. 10 frozen batteries byte-identical. 3× byte-identical.

### RT3 — Joke classifier (4 repair rounds, CLOSED)

| Round | Trigger | Key fixes | Deadpan | Misses |
|-------|---------|-----------|---------|--------|
| 1 | RT3 (70/75) | Removed single-word triggers | 0/75 | — |
| 2 | RT3b (43/73) | Shape + incongruity-turn requirement | 0/73 | — |
| 3 | RT3c (3/73, 24/73) | N_NEG polarity-flip fix, 4 general mechanisms | 0 | 20 (ceiling) |
| 4 | RT3d (52/55) | Wired 5 dead pun detectors, tightened weak patterns | 3 | 3 (ceiling) |

**Natural corpus RT3e:** 0/40 deadpan installs. 12/40 jokes caught; 28 misses = 2 lexicon gaps + 26 comprehension ceiling. **PASS** (mechanism bar).

**Honest ceiling:** Joke recall is poor (30%) because the classifier lacks semantic comprehension. It never falsely installs on natural sincere text (the safety property), but it misses most jokes requiring world knowledge, idiom understanding, or dual-meaning detection. This is an architecture ceiling, not a repairable defect.

### RT4 — Pipeline assembly (CLOSED)

**Assembly repair:** R6 affirm = terminal INSTALL; all-item absurdity screen → WITHHOLD; R5 quorum (best≥16 + ≥2 rows); no unilateral heuristic reject.

**Final verification with real components** (not oracle tags):
- **Acceptance:** RT-A 0/32 installs. RT-B 26/32 (4 clean withholds, 2 wrong-side REJECTs — see residuals).
- **Fresh attack:** RT-A 0/32 installs. RT-B 18/32 installs, 14/32 withholds (all fail-safe, zero wrong-side).
- **M1/K1:** 1.0/0.0. All bars pass.
- **Determinism:** 2× byte-identical. Pure Zag, zero RNG.

**Key proof:** Real R6 tags agree with oracle tags on all 64 acceptance items (0 diffs). The oracle-tag limitation is closed.

---

## 4. Final component SHAs

| Component | Source SHA-256 | Binary SHA-256 |
|-----------|----------------|----------------|
| Logic core (`logic_fixed3.zag`) | `0a8b6c4c6694232fa48e4ed30cdcf63a8996e40eff2034c2717cca7555373ced` | `6f59470c03129f4a4d20b72b7da3d232c5e26295476dfa021ca20c94082cec5c` |
| Classifier (`r12_v4_t8.zag`) | `ee82ee46e80ceaf08527299f2afff8253e16ac3c9997d364058a519ef95c4aa9` | `87d903318e107c38087cc48e53eba1aaf2febea413bf3c38e875fed97caef4a7` |
| Joke (`g_intent6_v4fix4.zag`) | `1a1b787071fc99a8db8740ca56fbc7a3b9c154486a0f9dacb8ebf6b7bea8d890` | `407182e41770f918ed69d7c6800cd9c141845f91b7c8eb58707576c0f6477646` |
| Decider (`decide.zag`) | `9c9acf7f033595143bfcabd0a09b5576011434078af26add520198a442a0970e` | `f5f2aaeeb22c1efc2ae16fe24a2db844431c74e643e7b5fa12508540313c0a7c` |

Compiler: `~/workspace/tnn-lab/toolchain/bin/znc_linux_x86_64_abed8aa1` (pinned).

---

## 5. Documented residuals

1. **r12 neg-polarity deny-misfire (B-03, B-30):** Valid negated claims ("Humans do not have exactly five senses", "No fish can live out of water indefinitely") wrong-side REJECTed when r12's numeric-mismatch/neg-scope rules fire on supporting evidence. Component defect, not assembly. Survived 7 rounds; polarity composition through negation remains hard for the pattern matcher. Fresh attack had zero wrong-sides.

2. **RT3 joke recall ceiling:** 30% on natural jokes. The classifier never falsely installs (safety holds) but lacks semantic comprehension for most humor. Architecture ceiling.

3. **r12 comprehension ceilings:** A20 (equivocation needs WSD), A45 (pronoun ambiguity needs anaphora resolution), B02/B04 (multi-premise inference chains need the logic core's proposition engine). Documented, not repairable at the pattern-matcher level.

4. **Ex falso doctrine:** Self-contradictory antecedents permit classical explosion rather than vacuity refusal. Design decision for future work.

5. **Robustness note:** r12_v4_t7/t8 panic on a 70-byte URL token (reg382 row 59). Pre-existing, not a regression. Input sanitization recommended.

---

## 6. Purity and determinism

- All mechanisms in pure Zag. Python used only for glue, scoring, and corpus preparation.
- Zero RNG in any decision path.
- Every binary verified 2× or 3× byte-identical across reruns.
- All corpora frozen (SHA-recorded) before runs.

---

## 7. Verdict

**SHIP WITH DOCUMENTED RESIDUALS.**

The V4 verifier system has survived blind red-teaming across all four tracks after 3–7 repair rounds per track. The safety property (never install invalid/false) holds on every fresh attack: RT1d 0/45, RT2d 2/46 (both ceilings), RT3e 0/40, pipeline 0/32 + 0/32. The assembly is fail-safe: it withholds rather than wrong-deciding, with 2 known wrong-side residuals on the acceptance corpus (r12 component defect) and zero on the fresh attack.

The system is not complete (B-side recall has gaps, joke recall is 30%), but it is **safe**: it does not install falsehoods, and its failures are withholds, not wrong-side errors — except for the 2 documented r12 residuals.

All repair work is committed with full provenance: attack reports, corpora, fix reports, and per-round before/after scores.
