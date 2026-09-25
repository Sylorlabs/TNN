# MATH R2 Incremental Evidence (2026-09-25)

Formal batteries B2R/B3R/B4R/B4X/B6X, KB2, B1N, B7F. B5X still running.

## Formal battery results (solved/incorrect, 3x byte-identical, zero divergence)

| Battery | ONE-R1 | DUAL-R1 | HYB | REF-FIRST | NFEE | LEARN-FORM* |
|---------|--------|---------|-----|-----------|------|-------------|
| B2R (12) | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| B3R (10) | 10/10 | 10/10 | 10/10 | 10/10 | 9/10 | 10/10 |
| B4R (15) | 15/15 | 15/15 | 15/15 | 12/15 | 15/15 | 15/15 |
| B4X (15) | 10/15 | 10/15 | 10/15 | 6/15 | 10/15 | 10/15 |
| B6X (3, bound 128) | 3/3 | 3/3 | 2/3 | 3/3 | 2/3 | 3/3 |

*LEARN-FORM formal path uses byte-identical ONE core (build-verified).

All incorrect are false_withheld (no false_derived anywhere). Zero divergent.

## KB2 (20 pairs, R1 manifest unrecoverable; documented construction)
- DUAL-bar (>=18/20): ONE 20/20, DUAL 20/20, HYB 20/20, REF-FIRST 20/20, NFEE 19/20, LEARN-FORM 20/20 — all PASS
- ONE-bar (allpass): all PASS except NFEE (fails on B3_03: conf 0 on solvable)

## B1N (LEARN-FORM NL->formalize)
- 9 DERIVED, all via unfaithful P01-template (imp(p,q),p|-q) applied to distinct problems
- P05 [open_or_impossible]: FALSELY DERIVED via template (critical)
- 3 FORMALIZE-ABSTAIN, 10 WITHHELD (correct abstentions)
- Other engines: exit 4 (clean parse failure) on raw NL — verified

## B7F (formalization quality, checker-scored /100)
- LEARN-FORM: mean 2.5 (12 abstain, 8 scored 0-17)
- Curated baseline: mean 47.9
- H4 FALSIFIED (needs >=70 AND beat baseline)

## Findings
- F-SEAL-01: SEALED_B2.sol marks B2_07 DERIVED but fixture is underivable; all engines withhold; corrected to WITHHELD.
- F-SEAL-02: SEALED_B7F README "19/20 WITHHELD" stale; actual .sol has 18 DERIVED + 2 WITHHELD.
- NFEE: B3 coverage gap (B3_03), B6X_03 UNSUPPORTED.
- REF-FIRST: weak on B4X (6/15) and B4R (12/15); slow (referee search).
- HYB: misses B6X_03 (120-chain) despite long-chain design goal.
- Zero RNG: grep clean. Sealed guard: exit 3 on all 9 binaries.
- B6X bound-128: evaluation-only variants (one_b6x/dual_b6x/hyb_b6x) with bound literal 8->128; REF-FIRST/NFEE via argv[3]=128.
