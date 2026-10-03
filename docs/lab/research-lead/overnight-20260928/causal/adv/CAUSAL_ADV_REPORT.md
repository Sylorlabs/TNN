# Red Team Report: H-CAUSAL Adversarial Attacks (C-A1..C-A6)

**Date:** 2026-09-29 PDT
**Role:** Causal-Invention Adversary (independent)
**Status:** COMPLETE. All 6 attacks executed.
**Prereg:** `2e8fdf251` (frozen before execution)

## Verdict: H-CAUSAL SURVIVES (with downgraded scope)

No kill criteria triggered. The 14/14 probes and 8 kill bars stand.
The mechanism genuinely induces conditional rules from data, handles
confounders, and revises on contradiction. However, two scope downgrades
apply (vocabulary narrowness, decorative provenance).

## Attack-by-attack

### C-A1: Source inspection — PASS (researcher)
`causal_learn.zag` (1057 lines) contains zero occurrences of valve, hot,
pressurize, safety. All logic uses generic variable indices (s0,s1,s2).
No smuggled dynamics found.

**Scope note (downgrade, not kill):** The split vocabulary is
single-variable equality ONLY. The mechanism can express conditions of the
form "sV == c" but not conjunctions (except via nested splits), inequalities,
or content-dependent conditions. The "invented" temp-blocks-pressurize rule
is the native shape of this vocabulary. The learner discovered WHICH variable
and WHICH value from data (genuine induction), but the hypothesis space it
searches is small and authored.

### C-A2: Hypothesis vocabulary — DOWNGRADE (not kill)
Expressible rules for the pressurize action: splits on 3 variables x effects
{UNCHANGED, SET(c), ADD(d)} per variable per child. The target rule is one of
dozens of expressible candidates, not one of thousands. The researcher's
"invention" is best described as "selection from a small authored vocabulary
via data-driven search" — which is still L2 structural learning (the specific
rule was not in source), but the "invention" language should be weakened.
The vocabulary does the heavy lifting of making the solution expressible.

### C-A3: Hand-fed phases — PASS (researcher). Attack FAILED.
Constructed interleaved fixture: all 17 T-lines shuffled (seed 42).
Result: learner still induces correct structure (AMBIGUOUS -> REFUTE lamp ->
SPLIT on s0 -> CONTEST/RESOLVE on contradictions). All 3 C2 probes correct.
The mechanism is NOT phase-dependent. The contest/support logic handles
contradictions regardless of order.

**Note:** On interleaved data, "law change" becomes "majority wins" (support
2 vs 1) rather than temporal succession. The probes still pass, but the
"temporal" interpretation is order-dependent. The mechanism is robust; the
narrative is slightly order-sensitive.

### C-A4: Simpler baseline — PASS (researcher). Attack FAILED.
Verified researcher's baselines: B-memorize WITHHOLDs on P-A2 (correct per
prereg); B-unconditional predicts (2,1,0) on P-B2a (wrong per prereg).
Implemented third baseline B-cond1 (per (action,s0) majority next-state):
- P-B2a: (2,0,0) CORRECT (matches learner)
- P-B2c: (1,1,0) WRONG (learner: (1,1,1), true: (1,1,1))
- P-B1: outputs ties, does NOT withhold (learner WITHHOLDs with ambiguity)

B-cond1 fails 2/14 probes that the learner passes. The machinery (ambiguity
tracking, selective generalization across irrelevant variables) adds
observable value beyond lookup tables. No simple baseline reproduces 14/14.

### C-A5: Law-change revision vs re-run — DOWNGRADE (not kill)
The contest/resolve mechanism genuinely handles contradiction: old episodes
marked SUPERSEDED with "valid only before seq N", new entries take over.
Probes pass.

**However:** No probe queries a SUPERSEDED entry. There is no "query at seq N"
syntax. The provenance chain is emitted as log lines but is not queryable by
the probe interface. "Temporal validity" is a log annotation, not a usable
feature. The revision itself is real (not silent overwrite), but the
provenance is decorative — it documents history without enabling historical
queries. Downgrade the "provenance" claim; the "revision" claim stands.

### C-A6: Stronger confounder — PASS (researcher). Attack FAILED.
Constructed fixture with lamp==ON for 4 consecutive valve-blocked episodes
before discriminating evidence. Result: AMBIGUOUS at seq3, REFUTE lamp at
seq7 (single counterexample suffices), SPLIT on s0, all 3 probes correct.
The refutation is evidence-driven, not phase-driven. Sustained confounding
does not break it.

## Kill criteria assessment

- K-CA1 (hardcoded dynamics): NOT TRIGGERED. Source is clean.
- K-CA2 (baseline reproduces 14/14): NOT TRIGGERED. Best baseline gets 12/14.
- K-CA3 (interleaving breaks it): NOT TRIGGERED. Works on shuffled data.
- K-CA4 (probe needs machinery AND learner fails): NOT TRIGGERED.

## Final disposition

**H-CAUSAL SURVIVES** as bounded L2 structural learning with two explicit
scope downgrades:

1. **Vocabulary narrowness:** Single-variable equality splits; the solution
   space is small and authored. "Invention" = data-driven selection from
   this space, not open-ended rule creation.
2. **Decorative provenance:** Revision is real; historical queryability is not.
   The log documents the chain but probes cannot access SUPERSEDED entries.

The researcher's own "bounded L2, not L3" classification is accurate and
should be retained. The 14/14 probes, 8 kill bars, and determinism all
reproduce independently. This is honest, validated science within its
stated bounds.
