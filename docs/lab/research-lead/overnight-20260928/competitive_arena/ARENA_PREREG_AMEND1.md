# AMENDMENT A1 to CA-1 prereg (frozen 2026-09-29)

Date: 2026-09-29. Committed alone before the harness code it affects runs.

## A1.1 C15 scoring: F1 instead of binary

Prereg section 6 C15 said: "Score per goal: 1 if predicate holds within budget
else 0". Changed to: listfilter goals score the F1 of the returned entity set
against the true set (order-insensitive); count goals keep exact-match (0/1).
Rationale: with a 20-step tool budget and 24 entities, a contestant that
rationally prioritizes and returns a high-precision partial list demonstrates
more capability than a binary 0 suggests; F1 preserves the incentive to be
complete while measuring partial competence. The budget constraint is still
enforced (no tools beyond budget) and cost is reported separately.

## A1.2 Briefing content restriction (entity facts excluded)

Prereg section 4.4 described the briefing as containing the world overview and
examples. Clarified: the briefing contains entity NAMES, the attribute and
relation vocabulary, alias tables, tool documentation, budgets, Zem example
pairs, the transformation DSL definition with shown pairs, cluster training
labels, causal observational counts, and worked non-test examples. It does NOT
contain entity attribute values or relation pairs; those are learned only
through the exposure stream and the OBSERVE tool. Rationale: otherwise C1/C2/C13
(one-shot, delayed, retention) would be trivially answered from the briefing
for both contestants and would not measure learning. Both contestants receive
the identical restricted content.

## A1.3 C5 no-revert probe placement

Prereg section 6 C5: the round-2 probe (no-revert after interference) is
implemented as a re-ask of the 5 C5 items at the end of the P2 test phase,
after all other test questions (which serve as the interference). Score is the
mean of round-1 and round-2 accuracy. Battery carries 5 C5 items; the harness
duplicates them as c5r2_xx for round 2.

## A1.4 C9 elimination rule constant

The elimination threshold 0.5 (eliminate hypotheses assigning P(observed
outcome) < 0.5) is part of the frozen protocol, documented in the briefing for
both contestants, and implemented identically in the harness scorer and the
TNN contestant. Discriminating-intervention threshold: minimum pairwise
total-variation distance > 0.15 across the three hypotheses' predicted outcome
distributions.

No other prereg terms change.
