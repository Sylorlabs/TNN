# BATTERIES FROZEN (round-2 re-freeze)

**Frozen:** 2026-09-23 17:45:19 UTC — round-2 re-freeze, supersedes the
2026-09-23 15:21:21 UTC record (whose SHAs matched 0/10 current TSVs;
batteries had been regenerated at 15:44 after the binary build, breaking
the freeze chain — see PROOF.md "Re-freeze record").

**Why re-frozen:** the round-1 freeze is unrecoverable (no git/backups under
`scratch-hellhole/`). The re-freeze happened AFTER 11 spec-mandated oracle
corrections (the oracles contradicted the frozen PROPSYNTAX.md rule
semantics; each correction is documented before/after in PROOF.md) and
BEFORE any round-2 engine change. Order of operations, round 2:
oracle corrections → re-freeze (this file) → engine fix → single scoring run.

**No further battery edits, ever.** `gen_batteries.py` re-derives these TSVs
byte-identically (verified 10/10 at re-freeze time) and exists only to prove
reproducibility, never to edit.

Anti-overfit rule: batteries MUST NOT be edited after engine scores are
observed. The 11 oracle corrections above predate the re-freeze and the
round-2 scoring run; they follow the engine spec, not the scores.

## SHA-256

```
58a2ef38e5cc18279b4b2d8248cd10aae384bf598fcff8e9fdc874aa0a9255c5  g_cau.tsv
49c325814104391817be30b43df9ca15083a003f53782ae4f2231e6d219ce3d0  g_cmp.tsv
e295ef6b680e1ae96b9fe8e78f15309f2684d38ea7262f4ac311368f36172603  g_con.tsv
77587bffacead9df75ead151d630ff68ff4a9d2dadc5b99aa889689e22da478c  g_cond.tsv
f661cd7e53d33ffcbc90a89321b2587d8a984c3c7f451758216109668d8d2f18  g_hedge.tsv
98adc0167232279096edff4e11d41879b8f878f601e6b9d5ac311ee5a1c1eed4  g_neg.tsv
5ff7e77314b0d16bcd4ab0ff608f375b7ec63ecea553e8fbdc06200c6308da50  g_qnt.tsv
ed988ef69510190600e227bf2643f3ea0ce5a877382a6c7d194907b9172fb92a  g_tmp.tsv
315c656d6e15e2ca1a117c117cfe47959176da5d8f4003f8f021560243e4c456  mlogic.tsv
9021cd8753995264e39b25288c633c5ec27aa9434faa113417b8396df91dcc94  v3proof.tsv
```

168 items total: 8 families × 20 + v3proof × 3 + mlogic × 5.

## Battery notes (authoring rationale, unchanged from round 1)

- Oracles follow the PROPSYNTAX.md rule semantics: DENY on structural
  negation/contradiction/disjoint intervals; AFFIRM on structural identity,
  causal consequent match with a substantive reason, evidence-interval ⊆
  claim-interval, or modus ponens; NEUTRAL otherwise (including hedged
  evidence — a hedge neither affirms nor denies, even against itself — lone
  conditionals, mere overlap, and predicate pairs the engine has no
  opposition knowledge for, e.g. FLOATS vs SINKS).
- v3proof items are faithful proposition encodings of the v3 evidence
  (full claim→proposition mapping documented in PROOF.md):
  VP-ICE (V3-03 causal "because" → AFFIRM), VP-GOLDFISH (V3-05
  contrastive → DENY), VP-SENSES (V3-07 contrastive → DENY).
- mlogic items encode the 5 R6 seed composition chains from
  v3_course.json as `CAUSE(r, NOT(claim))` (seeds 20–23: the seed's own
  "X entails ¬claim" step) or `NOT(antecedent)` (seed 24: named mechanism
  absent), all → DENY.
