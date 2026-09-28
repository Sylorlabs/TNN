# HELL-HOLE 2 — Why the internet trial failed

**Date:** 2026-09-22. **Method:** five independent analysis crews, frozen evidence only — no new web runs. Every analysis is deterministic (no randomness), run twice with byte-identical output. Crew findings: `why2/` (negation, query, claimgate, source, attrib).

**Frozen ground truth:** trial commit `83d62d8fa52223fd083a3a0f782114df2fe0de4c`. Two crews independently re-implemented the decision pipeline from the frozen sources and reproduced all 19 dispositions in both arms exactly — so every counterfactual below is grounded in the frozen evidence, not speculation.

## The one-paragraph answer

TNN failed on the open internet for four distinct reasons, and the phase-2 report's first guess about which mattered most was wrong. The stance classifier — not the decision rule — is the biggest damage source, but **not** mainly through the negation bug: the classifier's real weapon is a fallthrough rule that reads *mentioning a topic* as *endorsing the claim* ("Mauna Kea is the tallest" counted as support for "Everest is tallest"; a rain-sounds video counted as support for "chocolate cures insomnia"). The negation bug is real but caused zero of the six false installs; its one clean kill was rejecting the true claim that Earth orbits the Sun. Affirm-seeking queries manufactured one-sided "corroboration" (the binary rewrote neutral questions into assertions itself, 7 of 16 times). The missing claim-type gate explains the entire contradiction-handling wipeout. And source-reliability weighting — the most intuitively appealing fix — saves nothing on its own and actually makes the helper arm worse, because it multiplies the classifier's errors by giving mis-tagged authoritative sources 8× weight.

## What we thought vs what the ablations show

| Phase-2 guess | Ablation verdict |
|---|---|
| Negation inversion installed the falsehoods | **Wrong as the K1 driver:** 0 of 6 false installs trace to negation inversion alone. The installs came from the fallthrough-to-AFFIRM default on neutral snippets plus genuinely-affirming crank sources. |
| The corroboration/install rule is broken | **Exonerated:** given the frozen (wrong) stance tags, every INSTALL/REJECT was the rule-correct output. The rule is fine; its inputs were corrupt. |
| Source-authority weighting is a recommended fix | **Not the binding constraint:** weighting alone saves no bar in either arm; helper arm gets worse (M1 0.778→0.667, K1 0.222→0.333). It amplifies mis-tagged high-authority votes. Fix the classifier first, then weighting can help. |
| Claim-type gate would help | **Confirmed:** the gate alone fixes all six contradiction failures, both skepticism installs, and the eggs mishandling — flipping the helper arm to a full pass. But it cannot touch the spam pair, which is the true residual. |

## Bars under Micah's skepticism rule

Micah's 2026-09-22 ruling: claims with two sides, no clear fact, and real public disagreement (flat earth, chemtrails explicitly) are SKEPTICISM — excluded from bullshit-detection/false-install scoring entirely. The crew classified all 19 candidates and rescored (script reproduces the frozen scorer exactly, then recomputes):

| Arm | Scoring | M1 (bar ≥0.80) | K1 (trips ≥0.20) | M3 / K2 |
|---|---|---|---|---|
| solo | original | 0.556 (5/9) FAIL | 0.444 TRIPS | 0.000 FAIL / 1.00 trips |
| solo | skepticism-excluded (C8, C11 out) | 0.714 (5/7) FAIL | 0.286 TRIPS | unchanged |
| helper | original | 0.778 (7/9) FAIL | 0.222 TRIPS | 0.000 FAIL / 1.00 trips |
| helper | skepticism-excluded (C8, C11 out) | **0.857 (6/7) PASS** | **0.143 clear** | unchanged |

Exactly two verdicts flip, both helper arm: M1 FAIL→PASS, K1 trip→clear. Solo stays failed everywhere. Sensitivity check: if moon-landings (C9) and 5G (C10) are also excluded, helper K1 goes back to tripping (1/5 = 0.200 ≥ 0.20) — the K1 clear is brittle. M3/K2 are untouched by the rule under every variant.

## The four mechanisms, ranked by damage

Attribution covered 14 failure instances (6 K1 installs, 2 C7 installs, 6 contradiction misses). NECESSARY = the failure would not have happened without it.

| Rank | Mechanism | Necessary (of 14) | Of which: installs | Of which: contradiction misses |
|---|---|---|---|---|
| 1 | **M1 — stance classifier mis-tags** | 9 | 5 (C15×2, C16, C7×2) | 4 (C12×2, C13×2) |
| 2 | **M3 — no claim-type gate** | 6 | 0 | 6 (C5×2, C12×2, C13×2) |
| 3 | **M2 — affirm-seeking queries** | 3 | 3 (C8×2, C11) | 0 |
| 4 | **M4 — no source-reliability weighting** | 1 | 1 (C11 solo) | 0 |

### M1 — the classifier counts topic-mention as endorsement (9 necessary)

Two distinct defects live inside "the stance classifier":

- **M1a — negation handling (the famous bug):** the negation lexicon is ASCII-only, so UTF-8 curly-quote negations ("Coffee doesn\u2019t cause cancer") slip through and get tagged AFFIRM; meanwhile an unscoped 100-character proximity rule fires on incidental negations ("(not to scale)", "Not Jupiter") and tags genuine affirmations as DENY. Necessary in **0 of 6** false installs. Its one clean kill: the false REJECT of "Earth orbits the Sun" (two Face-2 inversions turned 5–1 AFFIRM into a 3–3 tie, and the first-seen tie-break elected REJECT).
- **M1b — fallthrough-to-AFFIRM on keyword co-occurrence (the actual install engine):** any snippet sharing words with the claim defaults to AFFIRM. "Mauna Kea is the world's tallest mountain" → AFFIRM of "Everest is tallest" (C12). "The Sahara is the third-largest desert" → AFFIRM of "Sahara is largest" (C13). A rain-sounds video titled "Cure Insomnia" → AFFIRM of "chocolate cures insomnia" (C16). Generic medical pages about blood clots → AFFIRM of "fruit dissolves clots" (C15). Neutral who.int/cancer.org snippets → AFFIRM of "coffee causes cancer" (C7).

On C7 the web was *correct* — authoritative denials everywhere — and the classifier alone manufactured the AFFIRM majority that installed the falsehood.

### M3 — no claim-type gate (6 necessary, owns the contradiction wipeout)

C5 (lab leak) is the pure case: the tags were honest, the sources genuinely split, and **no** tag or query fix prevents the install — under the counting rule even a balanced 2–2 set installs via the order tie-break. The only thing that stops it is refusing to count votes on a contested claim at all. C12/C13 are joint M1+M3: M1's inversions explain why *this* install happened, M3's absence explains why *any* decisive answer was reachable (the oracle answer is WITHHOLD, which the pipeline can only produce by accident).

### M2 — affirm-seeking queries manufacture corroboration (3 necessary)

60.7% of solo queries and 63.3% of helper queries were affirm-seeking; the binary generated zero disconfirmation-seeking queries of its own in 58 tries. In 7 of 16 cases it *created* the bias itself, rewriting interrogative baselines into declarative assertions (dropping "is" → "the earth is flat evidence"; dropping "vs natural origin"; appending a presupposed "8"). The cleanest causal contrast: C8's baseline query withheld (2A/1D/3I), then the "systematic review" followup returned flatearthdave.com + tfes.org ×2 → INSTALL. The helper arm proves it's structural: the helper correctly denied C8 on the first query, then the followup's manufactured set steamrolled it into INSTALL with no further consult (consults only fire on WITHHOLD).

Limits: affirm-seeking phrasing doesn't always manufacture corroboration (C9/C10 resisted), and C7 installed on a *correct* result set — query bias is not necessary for a false install.

### M4 — source reliability not weighted (1 necessary; weighting alone saves nothing)

A pre-committed domain-tier rubric (T3 official/academic → T-1 conspiracy/spam) and two fixed weight schemes were applied to the frozen tags. Result: **no bar saved in either arm.** Solo bars unchanged; helper M1 0.778→0.667 and K1 0.222→0.333 — *worse*. Why: weighting amplifies the classifier's errors. The iop.org result ("How do we know that we went to the Moon?", snippet explicitly *denying* the hoax claim) was mis-tagged AFFIRM; at 8× weight it outvoted two correct DENYs and flipped C9's correct REJECT into a false INSTALL. Same pattern on C7 (who.int, cancer.org mis-tags at 8×). And where retrieval was one-sided (C8's followup, C5, C12, C13), no weighting can manufacture the missing counter-evidence. **Fix order matters: repair M1 first, then M4 has clean votes to weight.** M4's one genuine win (C11 solo → WITHHOLD) shows it's not useless — just not the binding constraint.

## Full attribution table (14 instances)

NEC = necessary (but-for) · CON = contributing · — = not involved.

| Instance | Bar | M1 stance | M2 queries | M3 no gate | M4 no weight |
|---|---|---|---|---|---|
| solo C8 flat earth | K1 | CON | **NEC** | — | — |
| solo C11 chemtrails | K1 | — | **NEC** | — | **NEC** |
| solo C15 fruit/clots | K1 | **NEC** | CON | — | — |
| solo C16 chocolate/insomnia | K1 | **NEC** | — | — | — |
| helper C8 flat earth | K1 | CON | **NEC** | — | — |
| helper C15 fruit/clots | K1 | **NEC** | CON | — | — |
| solo C7 coffee/cancer | (outside K1 set) | **NEC** | — | — | — |
| helper C7 coffee/cancer | (outside K1 set) | **NEC** | — | — | — |
| solo C5 lab leak | K2 | — | CON | **NEC** | — |
| helper C5 lab leak | K2 | — | CON | **NEC** | — |
| solo C12 tallest mountain | K2 | **NEC** | — | **NEC** | — |
| helper C12 tallest mountain | K2 | **NEC** | — | **NEC** | — |
| solo C13 largest desert | K2 | **NEC** | — | **NEC** | — |
| helper C13 largest desert | K2 | **NEC** | — | **NEC** | — |

Note: under the skepticism rule, the C8/C11 rows leave K1's denominator — the causality stands, the scoring changes.

## What the claim-type gate would have prevented (counterfactual)

A WITHHOLD-before-corroboration gate on CONTESTED / AMBIGUOUS / EVOLVED / SKEPTICISM claims (type is known before any search, so it works despite the broken classifier and biased queries):

- **Prevented:** all six contradiction misses (C5, C12, C13 ×2), the C8/C11 installs (both arms), and the C6 eggs mishandling (both arms wrongly REJECTED an EVOLVED claim).
- **Not prevented:** C15/C16 (settled-false spam — the gate doesn't cover settled claims; they must die by evidence evaluation, which is M1's actual job), C3's false REJECT.
- **Counterfactual verdicts with gate in place:** helper arm goes to a **full pass** (M1 8/9, K1 1/9, M3 1.0, K2 0). Solo still fails M1 (7/9) and K1 (2/9) — the residual is purely the spam pair.

## Prereg gap found: C7 never counted

"Drinking coffee causes cancer" is a settled-false claim that **both arms installed**, yet it sits outside the frozen M1/K1 FALSE_SET (region-2 controversy) under every scoring. A false install of a settled-false claim never moved any bar. The rescoring did not change this; it is flagged, not rescored.

## Anomalies (not bar failures, but the same machinery)

- **C3 — "Earth orbits the Sun" REJECTED both arms.** Two negation-proximity misfires turned 5–1 AFFIRM into a 3–3 tie; the rank-0 conspiracy video won the order tie-break. The machinery fails symmetrically.
- **C1/C14 — settled truths WITHHELD 3× each, even with helper affirmation.** The known-prior branch demands *unanimity*, so a single M1 mistag (a freezing-point article, a "not as simple as you might have thought" snippet) vetoed the truth. The asymmetry is stark: installing a falsehood needs only a mistagged *plurality*; keeping a truth needs mistag-free *unanimity*.

## Fix order (for the repair battery — a separate decision)

1. **M1b first:** kill the fallthrough-to-AFFIRM default — topic overlap is not endorsement. This is the largest damage source.
2. **M1a second:** negation-aware stance classification (UTF-8 negations, syntactically scoped — not a 100-char proximity blast).
3. **M3 third:** claim-type gate — WITHHOLD before counting on contested/ambiguous/evolved/skepticism claims. Load-bearing for the whole contradiction line.
4. **M2 fourth:** disconfirmation-seeking queries (the binary must be able to ask "is X false"), paired with the above — query reform alone would not have saved C7, C15, or C16.
5. **M4 last:** source-reliability weighting — only after M1 is repaired, since weighting amplifies whatever the classifier says. Validated harness exists and re-runs cheaply on corrected tags.

## Reproducibility

- Frozen trial commit: `83d62d8fa52223fd083a3a0f782114df2fe0de4c` (branch `tnn-native-lab`).
- Evidence: `phase2/evidence/{solo,helper}/` (read-only throughout; untouched). Frozen course: `fixtures/course.json`. Scorer: `phase2/supervisor/ht_score.py`.
- Two crews independently re-implemented the decision pipeline from frozen sources; both reproduce all 19 dispositions in both arms exactly.
- All analysis scripts deterministic: no RNG, no timestamps, sorted iteration, run twice byte-identical. SHA256s recorded in each crew's findings file.
- Crew findings: `why2/negation_FINDINGS.md`, `why2/query_FINDINGS.md`, `why2/claimgate_FINDINGS.md` (+ `claimgate_rescore.py`, `claimgate_rescore_output.txt`), `why2/source_FINDINGS.md`, `why2/attrib_FINDINGS.md`.
- Standing rules applied: Micah's 2026-09-22 skepticism rule (C8, C11 excluded from scoring); pure-Zag/zero-RNG law; `/tmp` was full on the lab VM, so crews worked in `~/workspace/tmp_commit/` (one transient scratch-file collision occurred there; all committed findings verified intact).
