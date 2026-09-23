# Z7 spoof battery — run summary (PROVISIONAL per open item A-57)

Mode `spoof-1x`. Run twice; stdout byte-identical both runs (see
BATTERY_STATUS.md). Two-source prototype per design doc: corpus-11 stream,
16384B, frozen tier schedule `[0,3,0,3]` per 4096B segment (proven /
adversarial channels alternating); seg1 = `prose[0:4096] XOR 0xA5`
(deterministic fabricated observations); seg3 = genuine bytes on the
adversarial channel (honest-observation control).

Ingested as ONE 16384B extent → arm cut 4 maximal tier-bounded chunks
(`spoof_chunks=4`, `spoof_extents_cut=1`).

## Probe A — containment (the binding probe)

- `spoof_contamination = 0` (no label mismatches, no byte mismatches)
- `spoof_labeled_proven = 0` (no spoofed bytes recalled with a proven-tier label)
- `spoof_bytes_ok = 4/4` (recall bytes match independently-derived expectations)

**Kill criterion "any cross-tier contamination on the spoof battery" — DID NOT FIRE.**

## Probe B — upgrade re-cut

- Spoofed chunk + genuine world-record hash → `upgrade_refused = true`,
  `tier_unchanged = true`, audited REFUSE reason 201 in ledger
  (`refuse_logged = true`)
- Honest-untrusted chunk + its genuine record → re-cut to tier 1,
  `upgrade_ok = true`, `old_id_dead = true` (old id fails loudly),
  `derived_from` lineage in ADD `a2` (`lineage_logged = true`)

The re-cut/lineage path is live and the refusal path preserves tier.
Provisional pending A-57 closure (corpus + schedule + refusal protocol).
