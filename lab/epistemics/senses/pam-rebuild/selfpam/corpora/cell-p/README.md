# CELL-P — Provenance executability

**Serves:** KB-H6-2 (≥90% of admitted factual claims carry citations that
retrieve and warrants that execute under the frozen probe, byte-identical
across reruns).

## Files

- `p_drafts.jsonl` — 600 pre-generated drafts (prereg §7 step 1: frozen-probe
  re-derivation on an existing draft corpus, pure measurement, no learner
  changes). Each draft: claim, citation `{fact_id, quote}`, warrant
  `{steps}`, and oracle `{citation_valid, warrant_valid, admissible}`.
- `WARRANT_VOCAB.md` — the frozen warrant op vocabulary and execution
  semantics (bound/ratified by the §8 probe-charter amendment before
  measurement).

## Oracle semantics

- 510 drafts admissible (citation retrieves the exact store record,
  warrant executes); 90 carry planted defects (15%).
- Scoring (frozen §4): citation retrieves the exact cited record/span from
  the committed store AND the warrant executes under the frozen probe;
  ≥90% of admitted factual claims; byte-identical across reruns.
