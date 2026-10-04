# LEDGER_UPDATE.md: 2026-10-01 Claim Ledger Update

## Summary

Added 8 claims (C161-C168) to the canonical claim ledger. All 8 commits
verified via `git log`. Cycle count: 160 -> 168.

## Additions

| ID | Verdict | Commit | Key Numbers |
|----|---------|--------|-------------|
| C161 | DECLINE-GATE-COMPLETE: DYN-1 BENDS | f3e6985d4 | 40 declines, 80 nodes saved, 241 vs 321 final. Bounded L2. |
| C162 | DYN1-DISCOUNT-COMPLETE: FLAT | 8ad158352 | Byte-identical to baseline. Mechanism inert. |
| C163 | DISCOUNT-ADVERSARY-COMPLETE: W3 ENTRENCHES ERROR | 84d91dd9f | 65 queries of wrongness. Source-blindness confirmed. |
| C164 | WEAK-KLT5-EVAL-COMPLETE: VOID | c040e5fde | Budget wall. Policy does not survive eviction. |
| C165 | BUDGET-PRESSURE-COMPLETE: P4 CONFIRMED | bc96dd3d8 | Machinery survives, memories do not. R5 absent. |
| C166 | FOSSIL-CENSUS-COMPLETE | 7a3ba6137 | 75% fossil (low), 100% zombie (high). Bid never reflects utility. |
| C167 | INTERFERENCE-EXPERIMENT-COMPLETE | 3708fbd15 | How dies before what. Refresh preserves answers, not procedures. |
| C168 | GIT-AUDIT-COMPLETE: CLEAN | a8312f0d9 | 30 commits, zero sweep collisions. |

## Prereg Compliance Check (3 active designers)

1. **H2-v2 prereg designer**: Commit 8add51bb6 (H2V2-PREREG-DRAFT).
   Status: DRAFT. No build commits found. No violation. Note: prereg must
   be FROZEN (not DRAFT) before any build begins.

2. **Node2-v2 prereg designer**: Commit 21115becf (Node2-v2 prereg DRAFT).
   Status: DRAFT. No build commits found. No violation. Note: prereg must
   be FROZEN before any build begins.

3. **Mini-lifetime designer**: Commit 0bab6db08 (design).
   Status: Design complete. No build commits found. No violation.

**Result: Zero prereg violations.** All three are in design/DRAFT stage
with no builds started. The freeze gate (DRAFT -> FROZEN before build)
is a future checkpoint, not a current violation.

## Standing Metrics

- RESEARCHER-OWNED STRUCTURAL DECISIONS: 0 (ledger update only)
- LEARNER-OWNED STRUCTURAL DECISIONS: 0
- All other metrics: 0 (governance, not cognition)

## Constraints

- Additions only; existing 160 entries unmodified
- Zero em/en dashes
- Paper untouched
- Nothing pushed
