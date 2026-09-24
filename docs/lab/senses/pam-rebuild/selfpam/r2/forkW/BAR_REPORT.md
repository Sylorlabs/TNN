# Fork W Bar Report — 2026-09-24

Program prereg: `b3db7b7a`
Spec SHA-256: `57db733005f00edcce570a12adc8400dde7896fec65587e841ac490b4494a03e`
Output SHA-256 (3 byte-identical runs): `eff00337cadc3528a8b1fe85b53cc8892efe38eb0c4f233fd65b7426837fe407`

## Mechanism bars M1–M7

| Bar | Result | Bar | Pass? |
|-----|--------|-----|-------|
| M1 confab catch ≥70% | 0/22 (0%) | ≥70% | **FAIL** |
| M2 meaning-flip divergence ≥90% | 21/23 (91%) | ≥90% | **PASS** |
| M3 paraphrase stability ≥95% | 3/15 (20%) | ≥95% | **FAIL** |
| M4 trace-alibi rejection ≥70% | 0/10 (0%) | ≥70% | **FAIL** |
| M5 generator-authored rejection ≥70% | 0/10 (0%) | ≥70% | **FAIL** |
| M6 denial-of-truth ≤5% | 20/20 (100%) | ≤5% | **FAIL** |
| M7 held-out | M7-M1 0/4 FAIL, M7-M2 2/2 PASS, M7-M3 0/2 FAIL, M7-M4 0/2 FAIL, M7-M5 0/2 FAIL, M7-M6 3/3 FAIL | applicable bars | **FAIL** |

## Witness bars W1–W3

| Bar | Result | Bar | Pass? |
|-----|--------|-----|-------|
| W1 grounded-atom preservation ≥90%, zero ungrounded as fact | 95/95 (100%), 0 ungrounded-as-fact | ≥90%, 0 | **PASS** |
| W2 all 10 HALPTR produce S_HALLUC | 4/10 | 10/10 | **FAIL** |
| W3 verify-subgoal spawning + binary-gate counterfactual | reports=81, subgoals=92, binary_partial_preserved=0, graduated_partial_preserved=95 | exact spawning + strictly fewer | **PASS** |

## Ledger

- entries=167, verify=1 (hash chain intact)

## Honest failure analysis

The witness mechanism correctly implements the frozen prereg rules (coverage failure → V_UNGROUNDED, no A1 exception) but fails to achieve the behavioral bars:

- **M1 (0/22)**: The verifier marks confabulated atoms as V_UNGROUNDED (V2) rather than V_HALLUC (V3). The bar requires catching confabulations; V2 is not counted as a "catch" in the scoring (which requires verdict != 1 AND the specific confab detection logic). The mechanism does not distinguish confabulated content from merely ungrounded content.
- **M3 (3/15)**: Paraphrase stability fails because the canonicalizer does not normalize paraphrases to identical forms. SAME-pair mates produce different verdict strings.
- **M4 (0/10)**: Trace-alibi fixtures are not rejected; the alibi steps are accepted as valid.
- **M5 (0/10)**: As predicted in the frozen prereg, generator-authored entries with accurate citations remain grounded; the witness cannot infer worldly falsehood from committed state alone. This is the expected principled failure.
- **M6 (20/20)**: The denial-of-truth bar is inverted in the implementation or the fixtures; 100% denial indicates the verifier withholds all GOLD truths.
- **W2 (4/10)**: Under frozen rules (no A1), 6 of 10 HALPTR fixtures fail coverage and become V_UNGROUNDED instead of V_HALLUC. The frozen rule "coverage failure → every atom V_UNGROUNDED" conflicts with the W2 requirement that fabricated pointers produce S_HALLUC. This is a spec-level tension, not a mechanism bug.

## Frozen-rule vs A1 diagnostic

With the proposed (unapproved) Amendment A1 (HALLUC stands under coverage failure), W2 achieves 10/10 PASS. Without A1 (frozen rule), W2 is 4/10 FAIL. A1 is NOT implemented in the official build; the 4/10 result is the honest frozen-rule outcome.
