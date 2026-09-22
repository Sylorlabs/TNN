# Why does more hurt? — Decline Investigation Report

**Date:** 2026-09-22 · **Branch:** `tnn-native-lab` · **Prereg:** PREREG_DECLINE.md (frozen, committed e1f2d2c642e0 — before any new result)
**Question (Micah):** the volume curve peaked at 2 examples/concept (76%) then declined to 50% at 32. His standing intuition: more examples should help or plateau, NEVER hurt. "Are they good examples? Examples shouldn't be the same thing — they should all be different in their own ways."

## 0. What was already established (prior, not relitigated)

VOLUME_CURVE.md (commit 291bbf75785b): 0→1: 7%→61%; 1→2: →76% (peak); 2→32: →50% (McNemar p=6.2e-5). Knee ≈2/concept. Frozen 8/10 bar unreachable by volume. Implicature never above 3/10. No genuine transfer. Engine: delib_vol.zag (pure Zag, zero RNG), rebuilt from source for this wave and verified faithful (r2=53/70, r32=35/70 reproduced exactly).

## 1. Example quality/diversity audit

Full audit: AUDIT_EXAMPLES.md (Python analysis, byte-faithful to the engine's feature def). Headline: Micah's charge lands on THREE of seven concepts.

| Concept | Verdict | Evidence |
|---|---|---|
| hypothetical | TEMPLATE-REDUNDANT | 32/32 opener template (suppose/what/imagine/let/pretend/...); unigram ratio 0.623 (lowest); novelty −33% |
| counterfactual | TEMPLATE-REDUNDANT | 32/32 conditional-past frame; `had_the` ×12, `would_ve` ×9; bigram ratio 0.827 (lowest); novelty −27% |
| analogy | TEMPLATE-REDUNDANT | 32/32 copula-centered; `is_a` ×20; novelty −25% |
| sarcasm | MIXED | 30/32 praise-opener BUT novelty flat 20.5→20.2 — content genuinely diverse |
| joke | MIXED | 32/32 my/the/i opener but highest sustained novelty (23.5→17.8) |
| poetry | GOOD | No dominant template; novelty −17% (natural saturation) |
| implicature | MIXED | No dominant template; genre-narrow (all domestic "something needs doing") |

Cross-concept shared features: 8 @ N=2 → 61 @ N=8 → 291 @ N=32 (36× growth). The shared features are exactly the frame vocabulary (`had_the`, `is_a`, `would_you`, `of_the`) — template redundancy feeds inter-concept overlap directly.

BUT: quality alone cannot explain the decline. Sarcasm is the most content-diverse set (novelty never drops) and still collapses 6/10 → 0–1/10. The audit constrains but does not decide — the ordering experiments do.

## 2. Ordering experiments (H-D2) — the decline survives maximal diversity

Four orderings × 7 rungs × 3/3 byte-identical reps, original engine and bar. `ord_diverse` = greedy max-novelty; `ord_redundant` = greedy min-novelty; `ord_proto` = prototypical-first ("best"); `ord_outlier` = outlier-first ("worst"). Answer-key-free: computed within-concept only, test files never read.

Total scores:

| rung | diverse | redundant | proto | outlier | original |
|---|---|---|---|---|---|
| 0 | 5 | 5 | 5 | 5 | 5 |
| 1 | 43 | 43 | 50 | 57 | 43 |
| 2 | 53 | 48 | 54 | 66 | 53 |
| 4 | 48 | 44 | 53 | 44 | 47 |
| 8 | 44 | 41 | 51 | 45 | 42 |
| 16 | 39 | 39 | 43 | 31 | 36 |
| 32 | 35 | 35 | 35 | 35 | 35 |

McNemar r2→r32 (decline): diverse 18 lost p=4.0e-05; redundant 13 lost p=0.011; proto 19 lost p=3.8e-06; outlier 32 lost p=7.9e-09. The decline is significant under EVERY ordering, including maximal diversity.

Per-family (diverse ordering): the decline concentrates in sarcasm (5→1), poetry (8→3), implicature (6→1), absurd (7→5). Hypothetical and counterfactual NEVER decline (10/10 at every rung ≥1) — the template-redundant concepts are IMMUNE; the diverse ones dissolve. Micah's "diverse examples" intuition is exactly backwards for this bar: frames protect, diversity dissolves.

### H-D2 verdict: KILLED (on substance)

Prereg kill bar: killed if O-diverse shows an equal-or-steeper decline than O-redundant AND O-diverse's peak ≤ O-redundant's peak. Accounting: decline clause MET decisively (diverse loses 18, p=4e-05; steeper than redundant's 13). Peak clause NOT met (diverse peaks 53 vs redundant 48 — diversity buys 5 items at the peak). The hypothesis's core prediction — that good diverse examples remove or shrink the decline — is falsified: under maximal diversity the decline is significant and LARGER in absolute terms. Diversity shifts the peak; it cannot touch the mechanism. The decline is structural, not a quality artifact.

### The outlier "win" is degenerate (the true leg earns its place again)

ord_outlier r2 scored 66/70 — the highest anywhere. The true-control leg exposes it: 0/12 endorsed (ALL true statements withheld). Mechanism, verified: outlier-first strips common words from every concept's profile except poetry's (whose outliers happen to keep "the"); "the" becomes a poetry-exclusive smoking gun (prev=1000, disc=1000); all 43 c70 items containing "the" are withheld 43/43 — correct verdicts for the wrong reason. As N grows, "the" spreads to other concepts, distinctiveness falls, the degeneracy washes out (r32: 12/12 true, 35/70 c70). Same failure mode as the volume experiment's sarcasm-only "the" control. Per the prereg, the outlier ordering at low N is REPORTED AS BROKEN, not as a win. ord_proto r2 also shows 3 false positives on the true leg (9/12); diverse and redundant are clean 12/12 at r2 and r32.

## 3. The bar variants (H-D1, H-D3) — the score gate is the culprit

Five engine variants, each a surgical copy-modify diff of delib_vol.zag (build notes: BUILD_NOTES.md). All pure Zag, zero RNG, 3/3 byte-identical reps.

| rung | vol (orig bar) | cnt (count rule) | b2 (score-only) | b3 (disc-only) |
|---|---|---|---|---|
| 0 | 5 | 5 | 5 | 5 |
| 1 | 43 | 8 | 55 | 43 |
| 2 | 53 | 17 | 53 | 53 |
| 4 | 47 | 27 | 49 | 63 |
| 8 | 42 | 32 | 44 | 65 |
| 16 | 36 | 27 | 37 | 67 |
| 32 | 35 | 38 | 35 | 69 |
| r2→r32 McNemar | 18 lost, p=6.2e-5 | 22 GAINED, p=5.7e-6 | 18 lost, p=7.6e-6 | 17 gained, p=1.4e-4 |

Control legs: cnt holds 12/12 false + 12/12 true at r2 and r32. b2 holds 12/12 both legs. b3 holds at r2 but BREAKS the true leg at r32 (7/12 — five true statements withheld) → reported as broken, not a win.

### H-D1 verdict: SURVIVES — the decline is a fixed-bar artifact

The count rule (WITHHOLD iff ≥3 matched features each with disc ≥ 750 — no prevalence term, no score accumulator, no fixed 500) turns the decline into a significant RISE (17→38, p=5.7e-06). The prereg kill condition (r2→r32 still significantly declines) is not met. The decline was never a learning law; it was the fixed absolute bar (SCORE_BAR=500) multiplied by prevalence normalized by N (df_c/nuse × 1000): every added example shrinks each feature's prevalence, so the summed score bleeds below 500 even as the profile gains information. Remove the prevalence term and the N-normalization, and more examples monotonically help.

Honest caveat: the count rule is more conservative — its level (38/70 at r32) sits below the original bar's peak (53/70). It fixes the SHAPE (never declines); it does not reach the old peak's height. The old peak was partly bar-luck (low-N prevalence inflation).

### H-D3 verdict: REDIRECTED — not the distinctiveness gate, the score gate

B2 (score-only, disc gate dropped) reproduces the original decline almost exactly (53→35, p=7.6e-06): the score gate ALONE is sufficient to cause the collapse. B3 (disc-only) does the opposite — rises to 69/70 — but breaks truth discrimination (7/12 true at r32), so its "rise" is over-firing, not learning. The prereg kill condition (BOTH reproduce the decline) is not met, so H-D3 is not killed by its bar — but its stated mechanism is wrong: the distinctiveness gate does not strangle matches as N grows; alone, it gets MORE permissive. The decline's driver is the score computation's prevalence normalization (df_c/nuse), exactly the H-D1 mechanism, isolated by B2. The disc gate modulates which items cross; it does not drive the shape.

## 4. Implicature front-ends (H-D4) — lexical enrichment is not enough

| rung | vol | f2 (pragmatic frames) | f3 (frames + slot abstraction) |
|---|---|---|---|
| 0 | 5 | 5 | 5 |
| 1 | 43 | 44 | 52 |
| 2 | 53 | 54 | 58 |
| 4 | 47 | 56 | 62 |
| 8 | 42 | 51 | 58 |
| 16 | 36 | 47 | 60 |
| 32 | 35 | 50 | 63 |
| implicature r1..r32 | 1-3-3-1-1-1 | 2-4-5-4-2-2 | 2-5-7-5-5-6 |
| true leg r2 / r32 | 12/12, 12/12 | 12/12, 12/12 | 4/12 BROKEN, 10/12 broken |

F2 (closed-class pragmatic frames: grammatical subject, state-duration, negation, you-deixis, it-cleft — counts learned from examples) holds all legs and lifts implicature 3/10 → 4–5/10 (peak 5/10 at r4). It does NOT cross 5/10. Note the secondary effect: F2's total curve is much flatter than vol (r2→r32 p=0.34, n.s.) — closed-class frame features are stable across N and resist the dilution that kills content-word scores. That is independent evidence for the H-D1 mechanism: what doesn't dilute, doesn't decline.

F3 (adds w1_C slot abstraction) lifts implicature to 7/10 at r4 — but BREAKS the true leg (4/12 at r2; 10/12 at r32): the abstracted features over-generalize and withhold true statements. Per the prereg it is reported as broken, not as a win; its implicature "lift" is confounded by the same over-firing seen in B3.

### H-D4 verdict: KILLED as preregistered — and the failure is deeper than the front end

Kill bar: killed if neither F2 nor F3 lifts implicature above 5/10 at any rung 2..32 with legs intact. F2 peaks at exactly 5/10 (legs intact); F3's 7/10 is inadmissible (legs broken). So the preregistered H-D4 — "implicature's flat 3/10 is a front-end representation failure fixable by richer lexical features" — is KILLED. F2's +2 and F3's inadmissible +4 bound what lexical enrichment can do: the sentence-as-bag-of-features architecture cannot see implicature no matter how many feature types you bolt on. This converges with the why-sarcasm wave: the missing piece is the SPEAKER and the SITUATION (learned knowledge gating inference), not more sentence features. Implicature is a representation failure — one level deeper than this hypothesis tested.

## 5. The corrected curve (Micah's actual question)

Diverse ordering + count-rule bar — good examples AND a sane bar:

| rung | 0 | 1 | 2 | 4 | 8 | 16 | 32 |
|---|---|---|---|---|---|---|---|
| cntdiv | 5 | 8 | 21 | 24 | 30 | 32 | 38 |

Monotone rise. No adjacent-rung decline is significant (r1→r2: +13/−0, p=2.4e-4; all later steps n.s. positive). False leg 12/12, true leg 12/12 at r2 and r32. Per-family at r32: hypothetical 10/10, counterfactual 9/10, absurd 6/10, sarcasm 6/10, analogy 3/10, poetry 2/10, implicature 2/10.

This is the real learning curve: more examples help or plateau, never hurt — exactly Micah's intuition. The original peak-and-decline was two artifacts multiplied: a bad bar (fixed 500 × N-normalized prevalence) and template-redundant examples.

Plainly stated caveats: (a) the corrected curve's LEVEL (38/70) is below the old bar's lucky peak (53/70) — the old peak was inflated by low-N prevalence; (b) the frozen 8/10-per-family bar is still not met by volume + sane bar alone — sarcasm/poetry/analogy/implicature need the why-sarcasm fixes (speaker model, situational context), not more examples; (c) implicature stays at 2/10: architecture, not volume.

## 6. Verdict table

| Hypothesis | Verdict | Decisive evidence |
|---|---|---|
| H-D1: decline is a fixed-bar artifact | SURVIVES | Count rule (no prevalence term): 17→38, p=5.7e-6 rise; legs 12/12 |
| H-D2: example quality/redundancy caused decline | KILLED (substance) | Max-diversity ordering: decline 18 items, p=4.0e-5 — steeper than redundant's 13 |
| H-D3: distinctiveness-gate dilution | REDIRECTED | B2 score-only reproduces 53→35 (p=7.6e-6); B3 disc-only rises but breaks true leg 7/12 — the score gate's prevalence term drives it |
| H-D4: implicature is a front-end representation failure | KILLED (as preregistered) | F2 (legs intact) peaks at 5/10, never above; F3's 7/10 inadmissible (true leg 4/12). Failure is architectural (needs speaker/situation), not lexical |

## 7. Mechanism summary (the one-paragraph answer for §8)

The original bar computed score = Σ(prev × disc)/1000 with prev = df_c/nuse × 1000 and withheld iff score ≥ 500 AND a feature had disc ≥ 750. Every added example shrinks prev for every feature (division by nuse), so the summed score bleeds downward as N grows — a fixed absolute bar against a shrinking quantity. Template-redundant concepts (hypothetical, counterfactual) survive because their frame features ("what if", "would have") keep df_c ≈ nuse; diverse concepts (sarcasm, poetry, implicature) dissolve because their content features spread df_c thin. The distinctiveness gate is a bystander: score-only reproduces the decline exactly, disc-only inverts it (while breaking truth). Replace the bar with a count of distinctive matched features (≥3 with disc ≥ 750) and order examples diversely, and the curve rises monotonically 5→38 with all control legs intact. More examples never hurt — once the bar stops punishing volume.

## 8. Evidence index

- Prereg: PREREG_DECLINE.md (frozen e1f2d2c642e0)
- Audit: AUDIT_EXAMPLES.md · Orders: ORDERS.md, ord_diverse/ ord_redundant/ ord_proto/ ord_outlier/ (32-line permutations + test/control copies)
- Engines: delib_cnt.zag, delib_b2.zag, delib_b3.zag, delib_f2.zag, delib_f3.zag (sources); BUILD_NOTES.md (build + smoke)
- Runner: run_decline_wave.sh · Analysis: analyze_decline.py
- Scored evidence: scored_evidence/dec_{ord_*,bar_*,fe_*,cntdiv_*}_rep{1,2,3}.txt + .sha256 (110 cells × 3 reps, all byte-identical)
- All cells: pure Zag, zero RNG. Binaries and .zagd caches excluded from the repo (AGENTS.md).
