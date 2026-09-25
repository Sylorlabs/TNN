# MATH R2 Interim Hypothesis Assessment (2026-09-25, B5X pending)

## H1: HYB (long-chain assembly)
- Bar: KB1X pairwise net wins >=5 vs BOTH ONE and DUAL on B3R, AND not worse by >2 on B4X.
- B3R: ONE 10/10, DUAL 10/10, HYB 10/10. Pairwise wins: HYB-vs-ONE = 0, HYB-vs-DUAL = 0.
- **H1: FAIL** (0 < 5). HYB does not beat ONE/DUAL on interleaved revision.

## H2: REF-FIRST (contradiction-first)
- Bar: Falsified iff B5X false_withheld >= 2x DUAL's false_withheld.
- **PENDING** (B5X running).

## H3: NFEE (no-free-elimination)
- Bar: Match/beat DUAL on B6X (2/3, zero false_derived) AND derive B6X_03.
- B6X: NFEE 2/3 (B6X_03 UNSUPPORTED), DUAL 3/3.
- **H3: FAIL** (B6X_03 not derived; also worse than DUAL 2/3 vs 3/3).

## H4: LEARN-FORM (learned formalizer)
- Bar: >=70% schema-equivalence on B7F AND beat curated baseline (47.9).
- LEARN-FORM: 2.5 mean. Curated: 47.9.
- **H4: FAIL** (2.5 < 70; 2.5 < 47.9). The 1-template learner cannot formalize.

## H5: QUOT (quota-bounded)
- Bar: Repaired and enters battery, else BLOCKED-WITH-EVIDENCE.
- **BLOCKED-WITH-EVIDENCE** (repair not received; local partial panics on B2_01).

## PB1: New engine wins >=2/3 primary bars vs BOTH ONE-R1 and DUAL-R1
- HYB: 0/3 (H1 fail)
- REF-FIRST: 0/2 so far, H2 pending
- NFEE: 0/3 (H3 fail)
- LEARN-FORM: 0/3 (H4 fail)
- **PB1: LIKELY FAIL** (pending B5X; REF-FIRST would need H2 win + another bar).

## PB2/PB3: Pending B5X.
