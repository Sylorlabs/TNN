# ROUTER2_RESULT: H-ROUTER2 Learned Routing Predicates

**Verdict: H-ROUTER2 SURVIVES.** All four frozen kill bars pass.
**Frozen prereg:** `PREREG_ROUTER2.md` (commit `635787932`), strictly before
implementation. No amendments.
**Date:** 2026-09-29
**Raw evidence:** `ROUTER2_RAW_OUTPUT.txt` (md5
`fc7fc102da7407ee4075611fb0f60142`, 3 runs byte-identical)
**Implementation:** `router2_learn.zag` (causal machinery copied verbatim from
`causal/causal_learn.zag`, `main()` replaced; feature extractors copied from
`route_learn.zag`; new curriculum/test driver)
**Pure Zag. No Python.**

## Kill bar results

**K-R2A (inspectability): PASS.** The `list_hypos` dump after the marked phase
shows 11 ACTIVE entries with fully readable conditions and SET effects. The
induced routing rules, in plain language:

- `s2=1` -> PROC_QUERY (13); `s2=2` -> CAUS_QUERY (14)
- `s0=1 & s1=2` -> PROC_LEARN (11); `s0=1 & s1=3` -> PROC_LEARN;
  `s0=1 & s1=4` -> PROC_LEARN; `s0=1 & s1=1` -> WITHHOLD (10)
- `s0=2 & s1=2` -> CAUS_LEARN (12); `s0=2 & s1=3` -> CAUS_LEARN;
  `s0=2 & s1=4` -> CAUS_LEARN; `s0=2 & s1=1` -> WITHHOLD (10)
- fallback `any` -> WITHHOLD (10)

where s0 = pair_kind (1 = all str>str, 2 = all iii>ii), s1 = nseg,
s2 = query_kind (1 = bare string, 2 = 3-int tuple). No routing predicate was
authored; every rule above was induced from the 18 marked episodes by the
causal learner's SPLIT machinery (single-variable equality splits, chained
through parent/child condition inheritance).

**K-R2B (suite match): 16/16 PASS.** All 10 H-ROUTER suite items route exactly
as the authored predicates decide (L1/L3 -> PROC_LEARN, L2 -> CAUS_LEARN,
Q1 -> PROC_QUERY, Q2/Q3 -> CAUS_QUERY, A1..A4 -> WITHHOLD), plus 6 novel
surface strings with seen feature combos (N1..N6) all correct.

**K-R2C (novel withhold): 4/4 PASS.** Feature-novel inputs
(`(1,5,0)`, `(2,5,0)`, `(3,1,0)`, `(3,3,0)`) all WITHHOLD via the induced
fallback rule. The learner does not confidently misroute outside its
experience.

**K-R2D (determinism): PASS.** Three consecutive runs byte-identical.

## What was genuinely learned

The induction trace (in the raw output) shows the mechanism, not a lookup:

1. The unconditional ROUTE entry split on s0 (pair_kind) when CAUS_LEARN
   episodes contradicted PROC_LEARN outcomes.
2. A fresh unconditional entry (created when query episodes matched no
   ACTIVE entry) split on s2 (query_kind) when CAUS_QUERY contradicted
   PROC_QUERY.
3. The pair-kind children split on s1 (nseg) when single-pair WITHHOLD
   episodes arrived, producing the critical `s1=1 -> WITHHOLD` rules.
4. The remaining WITHHOLD episodes formed a consistent unconditional
   fallback entry.

The split ORDER and the chosen split VARIABLES were selected by the
machinery's own candidate test (unique resolving variable), not by the
researcher. The researcher supplied: the feature extractors, the 18 marked
episodes in a fixed order, and the task-code numbering (deliberately offset
10..14 so no numeric coincidence with feature values could masquerade as
learning).

## Honest boundary (predicted in prereg, confirmed)

The induced rules are per-(pair_kind, nseg) equalities, NOT a general
`nseg>=2` threshold. Three separate children (`s1=2`, `s1=3`, `s1=4`) each
independently conclude PROC_LEARN/CAUS_LEARN. A novel nseg=5 input matches no
specific child and falls back to the unconditional WITHHOLD rule. This is the
causal vocabulary's equality-only limitation manifesting exactly as
predicted: honest degradation (withhold) rather than misrouting, but NOT
threshold generalization. Vocabulary enrichment (ranges, inequalities)
remains an open frontier and is now concretely motivated.

## Classification

Bounded L2 structural learning: the learner constructed a routing decision
structure from generic machinery, and the exact rule set did not exist in
source. NOT L3: the input features are authored, the task codes are supplied
as marks in the curriculum phase, and the SPLIT induction mechanism is
pre-existing. The learner did not invent a new representation, primitive, or
procedure. What moved from researcher to learner is the ROUTING POLICY
itself: H-ROUTER's authored `if 2+ segs, str>str then PROC_LEARN` style
predicates are now induced entries.

## Lineage

H-ROUTER (authored predicates, SURVIVES) remains the valid baseline.
H-ROUTER2 supersedes it as the routing layer for future unified-learner work,
with the documented per-value boundary. The feature extractors
(`field_kind`, segment split) remain authored; learned feature discovery is
still open (does not block adoption).
